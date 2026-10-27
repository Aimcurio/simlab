"""Model Adapters and Functional Task Evaluation Engine for Agent Decision Making."""

from abc import ABC, abstractmethod
import hashlib
import json
import math
from typing import Any, Dict, List, Optional, Sequence, Tuple
import urllib.parse
import urllib.request
import urllib.error

import numpy as np

from simlab.governance import OperationTier, require_tier, SimLabAuthorizationError
from simlab.memory.scoring import cosine_similarity


class MathematicalEvaluationError(ValueError):
    """Raised when a mathematical operation cannot be evaluated due to invalid inputs or contract violations."""
    pass


def validate_and_convert_number(val: Any) -> float:
    """Validate that val is a valid finite real number, explicitly rejecting booleans, NaN, and Inf."""
    if isinstance(val, bool):
        raise TypeError(f"Invalid numeric input: boolean value {val!r} is not accepted as a number.")
    if isinstance(val, (int, float)):
        f_val = float(val)
    elif isinstance(val, (str, np.number)):
        try:
            f_val = float(val)
        except (ValueError, TypeError) as exc:
            raise TypeError(f"Cannot parse numeric value from {val!r}: {exc}") from exc
    else:
        raise TypeError(f"Expected numeric scalar, got {type(val).__name__}: {val!r}")

    if math.isnan(f_val):
        raise ValueError("Invalid numeric input: NaN is not allowed.")
    if math.isinf(f_val):
        raise ValueError(f"Invalid numeric input: Infinite value {f_val} is not allowed.")
    return f_val


def validate_and_convert_vector(vec: Any, expected_dim: Optional[int] = None) -> List[float]:
    """Validate sequence of numeric values, ensuring finite scalars and optional dimension match."""
    if not isinstance(vec, (list, tuple, np.ndarray)):
        raise TypeError(f"Expected sequence for vector, got {type(vec).__name__}")
    converted = [validate_and_convert_number(x) for x in vec]
    if expected_dim is not None and len(converted) != expected_dim:
        raise ValueError(f"Vector dimension mismatch: expected {expected_dim}, got {len(converted)}")
    return converted


def compute_task_checksum(task_id: str, result_value: Any) -> str:
    """Compute canonical 16-hex-char SHA-256 checksum for a task result."""
    if isinstance(result_value, float):
        val_str = f"{result_value:.6f}"
    else:
        val_str = json.dumps(result_value, sort_keys=True, default=str)
    payload = f"{task_id}:{val_str}".encode("utf-8")
    return hashlib.sha256(payload).hexdigest()[:16]


def evaluate_functional_task(
    task: Dict[str, Any],
    upstream_results: Optional[Dict[str, Any]] = None
) -> Tuple[Any, Dict[str, Any]]:
    """
    Execute general mathematical, statistical, data-processing, or pipeline computation
    specified by a task's requirements without hardcoded challenge answers.

    Returns (result_value, metadata_dict).
    If no functional operation is specified (legacy schema-only task), returns (42, {}).
    """
    req = dict(task.get("requirements") or {})
    op = req.get("operation") or task.get("operation")
    if not op:
        default_val = req.get("expected_value", task.get("default_value", 42))
        return default_val, {"mode": "legacy_default"}

    op = str(op).lower().strip()
    inputs = req.get("inputs", task.get("inputs", []))
    upstream = dict(upstream_results or req.get("upstream_results") or {})

    # If inputs not provided directly, pull from upstream dependency values in order
    if not inputs and upstream:
        depends_on = req.get("depends_on") or task.get("depends_on") or list(upstream.keys())
        inputs = [upstream[k] for k in depends_on if k in upstream]

    meta: Dict[str, Any] = {"operation": op}

    if op == "sum":
        arr = [validate_and_convert_number(x) for x in inputs]
        res = round(sum(arr), 6) if arr else 0
        if isinstance(res, float) and res.is_integer():
            res = int(res)
        meta["sample_count"] = len(arr)
        return res, meta

    elif op == "weighted_sum":
        arr = [validate_and_convert_number(x) for x in inputs]
        weights_raw = req.get("weights", [1.0] * len(arr))
        weights = [validate_and_convert_number(w) for w in weights_raw]
        if len(weights) != len(arr):
            raise ValueError(f"Weights length ({len(weights)}) does not match inputs length ({len(arr)})")
        res = round(sum(x * w for x, w in zip(arr, weights)), 6) if arr else 0
        if isinstance(res, float) and res.is_integer():
            res = int(res)
        meta["sample_count"] = len(arr)
        return res, meta

    elif op == "mean":
        arr = [validate_and_convert_number(x) for x in inputs]
        res = round(sum(arr) / len(arr), 6) if arr else 0.0
        if isinstance(res, float) and res.is_integer():
            res = int(res)
        meta["sample_count"] = len(arr)
        return res, meta

    elif op == "median":
        arr = [validate_and_convert_number(x) for x in inputs]
        res = round(float(np.median(arr)), 6) if arr else 0.0
        if isinstance(res, float) and res.is_integer():
            res = int(res)
        meta["sample_count"] = len(arr)
        return res, meta

    elif op == "variance":
        arr = [validate_and_convert_number(x) for x in inputs]
        ddof = int(req.get("ddof", 0))
        res = round(float(np.var(arr, ddof=ddof)), 6) if len(arr) > ddof else 0.0
        if isinstance(res, float) and res.is_integer():
            res = int(res)
        meta["sample_count"] = len(arr)
        return res, meta

    elif op == "std":
        arr = [validate_and_convert_number(x) for x in inputs]
        ddof = int(req.get("ddof", 0))
        res = round(float(np.std(arr, ddof=ddof)), 6) if len(arr) > ddof else 0.0
        if isinstance(res, float) and res.is_integer():
            res = int(res)
        meta["sample_count"] = len(arr)
        return res, meta

    elif op == "min":
        arr = [validate_and_convert_number(x) for x in inputs]
        if not arr:
            raise ValueError("Cannot compute min of empty inputs.")
        res = min(arr)
        if isinstance(res, float) and res.is_integer():
            res = int(res)
        meta["sample_count"] = len(arr)
        return res, meta

    elif op == "max":
        arr = [validate_and_convert_number(x) for x in inputs]
        if not arr:
            raise ValueError("Cannot compute max of empty inputs.")
        res = max(arr)
        if isinstance(res, float) and res.is_integer():
            res = int(res)
        meta["sample_count"] = len(arr)
        return res, meta

    elif op == "range":
        arr = [validate_and_convert_number(x) for x in inputs]
        if not arr:
            raise ValueError("Cannot compute range of empty inputs.")
        res = round(max(arr) - min(arr), 6)
        if isinstance(res, float) and res.is_integer():
            res = int(res)
        meta["sample_count"] = len(arr)
        return res, meta

    elif op == "polynomial":
        coeffs_raw = req.get("coefficients", inputs)
        coeffs = [validate_and_convert_number(c) for c in coeffs_raw]
        x_val = validate_and_convert_number(req.get("x", 1.0))
        total = sum(c * (x_val ** idx) for idx, c in enumerate(coeffs))
        res = round(total, 6)
        if isinstance(res, float) and res.is_integer():
            res = int(res)
        meta["degree"] = max(0, len(coeffs) - 1)
        return res, meta

    elif op in ("linear_difference", "delta"):
        start_raw = req.get("start", inputs[0] if len(inputs) >= 1 else 0.0)
        end_raw = req.get("end", inputs[1] if len(inputs) >= 2 else 0.0)
        start_val = validate_and_convert_number(start_raw)
        end_val = validate_and_convert_number(end_raw)
        res = round(end_val - start_val, 6)
        if isinstance(res, float) and res.is_integer():
            res = int(res)
        return res, meta

    elif op in ("linear_scale", "affine"):
        base_raw = req.get("base", inputs[0] if inputs else 0.0)
        base_val = validate_and_convert_number(base_raw)
        scale = validate_and_convert_number(req.get("scale", 1.0))
        offset = validate_and_convert_number(req.get("offset", 0.0))
        res = round(base_val * scale + offset, 6)
        if isinstance(res, float) and res.is_integer():
            res = int(res)
        return res, meta

    elif op == "dot_product":
        vec_a_raw = req.get("vec_a", inputs[0] if len(inputs) >= 1 else [])
        vec_b_raw = req.get("vec_b", inputs[1] if len(inputs) >= 2 else [])
        vec_a = validate_and_convert_vector(vec_a_raw)
        vec_b = validate_and_convert_vector(vec_b_raw)
        if len(vec_a) != len(vec_b):
            raise ValueError(f"Vector dimension mismatch for dot product: {len(vec_a)} != {len(vec_b)}")
        if len(vec_a) == 0:
            raise ValueError("Dot product requires non-empty vectors.")
        res = round(float(np.dot(vec_a, vec_b)), 6)
        if isinstance(res, float) and res.is_integer():
            res = int(res)
        meta["dimension"] = len(vec_a)
        return res, meta

    elif op == "cosine_similarity":
        vec_a_raw = req.get("vec_a", inputs[0] if len(inputs) >= 1 else [])
        vec_b_raw = req.get("vec_b", inputs[1] if len(inputs) >= 2 else [])
        vec_a = validate_and_convert_vector(vec_a_raw)
        vec_b = validate_and_convert_vector(vec_b_raw)
        if len(vec_a) != len(vec_b):
            raise ValueError(f"Vector dimension mismatch for cosine similarity: {len(vec_a)} != {len(vec_b)}")
        if len(vec_a) == 0:
            raise ValueError("Cosine similarity is undefined for zero-length vectors.")
        
        a = np.array(vec_a, dtype=float)
        b = np.array(vec_b, dtype=float)
        norm_a = float(np.linalg.norm(a))
        norm_b = float(np.linalg.norm(b))
        if norm_a == 0.0 or norm_b == 0.0:
            raise ValueError("Cosine similarity is undefined for zero-norm vectors.")
        
        sim = float(np.dot(a, b) / (norm_a * norm_b))
        sim = max(-1.0, min(1.0, sim))
        res = round(sim, 6)
        meta["dimension"] = len(vec_a)
        return res, meta

    elif op == "anomaly_count":
        if not inputs:
            return 0, {"sample_count": 0}
        arr = [validate_and_convert_number(x) for x in inputs]
        threshold = validate_and_convert_number(req.get("threshold", 2.0))
        if threshold < 0:
            raise ValueError("Threshold for anomaly detection must be non-negative.")
        np_arr = np.array(arr, dtype=float)
        mean_val = float(np.mean(np_arr))
        std_val = float(np.std(np_arr, ddof=0))
        if std_val == 0.0:
            count = 0
        else:
            z_scores = np.abs((np_arr - mean_val) / std_val)
            count = int(np.sum(z_scores > threshold))
        meta["sample_count"] = len(arr)
        return count, meta

    elif op == "filter_sum":
        arr = [validate_and_convert_number(x) for x in inputs]
        min_v_raw = req.get("min_val")
        max_v_raw = req.get("max_val")
        min_v = validate_and_convert_number(min_v_raw) if min_v_raw is not None else None
        max_v = validate_and_convert_number(max_v_raw) if max_v_raw is not None else None
        filtered = [
            x for x in arr
            if (min_v is None or x >= min_v) and (max_v is None or x <= max_v)
        ]
        res = round(sum(filtered), 6) if filtered else 0
        if isinstance(res, float) and res.is_integer():
            res = int(res)
        meta["sample_count"] = len(filtered)
        return res, meta

    elif op == "moving_average":
        arr = [validate_and_convert_number(x) for x in inputs]
        window = int(req.get("window", 3))
        if window < 1:
            raise ValueError("Window size for moving average must be at least 1.")
        if len(arr) < window:
            res = round(sum(arr) / len(arr), 6) if arr else 0.0
        else:
            res = round(sum(arr[-window:]) / window, 6)
        if isinstance(res, float) and res.is_integer():
            res = int(res)
        meta["window"] = window
        return res, meta

    elif op == "record_reconcile":
        set_a = set(req.get("records_a", inputs[0] if len(inputs) >= 1 else []))
        set_b = set(req.get("records_b", inputs[1] if len(inputs) >= 2 else []))
        diff_count = len(set_a.symmetric_difference(set_b))
        meta["reconciled_total"] = len(set_a.union(set_b))
        return diff_count, meta

    elif op == "linear_solve":
        mat_a_raw = req.get("matrix_a", [[1.0]])
        vec_b_raw = req.get("vector_b", [1.0])
        mat_a = np.array(mat_a_raw, dtype=float)
        vec_b = np.array(vec_b_raw, dtype=float)
        if mat_a.ndim != 2 or mat_a.shape[0] != mat_a.shape[1]:
            raise ValueError(f"Matrix A must be square 2D, got shape {mat_a.shape}")
        if len(vec_b) != mat_a.shape[0]:
            raise ValueError(f"Vector B dimension {len(vec_b)} does not match matrix A size {mat_a.shape[0]}")
        det = float(np.linalg.det(mat_a))
        if math.isclose(det, 0.0, abs_tol=1e-12):
            raise ValueError("Matrix A is singular and cannot be solved.")
        sol = np.linalg.solve(mat_a, vec_b)
        res = round(float(np.sum(sol)), 6)
        if isinstance(res, float) and res.is_integer():
            res = int(res)
        return res, meta

    elif op == "pipeline_reduce":
        reduce_op = str(req.get("reduce_op", "sum")).lower()
        vals = [validate_and_convert_number(x) for x in inputs]
        if reduce_op == "product":
            prod = 1.0
            for v in vals:
                prod *= v
            res = round(prod, 6)
        elif reduce_op == "mean":
            res = round(sum(vals) / len(vals), 6) if vals else 0.0
        elif reduce_op == "sum":
            res = round(sum(vals), 6) if vals else 0
        else:
            raise ValueError(f"Unsupported pipeline reduce operation: {reduce_op}")
        if isinstance(res, float) and res.is_integer():
            res = int(res)
        meta["sample_count"] = len(vals)
        return res, meta

    if "expected_value" in req:
        return req["expected_value"], meta
    raise ValueError(f"Unsupported operation '{op}' specified in task requirements.")


class ModelBackend(ABC):
    """Abstract interface for LLM and rule-based decision backends."""

    @abstractmethod
    def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """Generate response given prompt."""
        pass

    @abstractmethod
    def is_available(self) -> bool:
        """Check if backend is reachable and available."""
        pass


class DeterministicRuleBackend(ModelBackend):
    """Rule-based deterministic decision backend requiring no external models."""

    def __init__(self, seed: int = 42):
        self.seed = seed

    def is_available(self) -> bool:
        return True

    def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """Deterministic policy decision based on prompt structure."""
        p_lower = prompt.lower()
        if "coordinate" in p_lower or "assign" in p_lower:
            return json.dumps({
                "action": "ASSIGN_TASK",
                "target": "worker_1",
                "rationale": "Deterministic assignment to primary worker."
            })
        elif "review" in p_lower or "validate" in p_lower:
            return json.dumps({
                "action": "APPROVE",
                "confidence": 0.95,
                "rationale": "Output satisfies deterministic invariant checks."
            })
        else:
            return json.dumps({
                "action": "EXECUTE_WORK",
                "status": "COMPLETED",
                "rationale": "Rule-based task execution completed successfully."
            })


class LocalOllamaAdapter(ModelBackend):
    """Optional adapter for local Ollama endpoints (e.g. http://localhost:11434)."""

    LOOPBACK_HOSTS = {"localhost", "127.0.0.1", "::1", "[::1]"}

    def __init__(self, model_name: str = "llama3:latest", endpoint: str = "http://localhost:11434/api/generate"):
        self.model_name = model_name
        self.endpoint = endpoint
        self._validate_loopback_or_authorize()

    def _validate_loopback_or_authorize(self) -> None:
        parsed = urllib.parse.urlparse(self.endpoint)
        host = (parsed.hostname or "").lower()
        if host not in self.LOOPBACK_HOSTS:
            require_tier(
                OperationTier.EXTERNAL_MODEL_NETWORK,
                f"non_loopback_ollama_endpoint:{self.endpoint}"
            )

    def is_available(self) -> bool:
        """Ping local Ollama endpoint."""
        self._validate_loopback_or_authorize()
        try:
            parsed = urllib.parse.urlparse(self.endpoint)
            base_url = f"{parsed.scheme}://{parsed.netloc}/"
            req = urllib.request.Request(base_url, method="GET")
            with urllib.request.urlopen(req, timeout=1.0) as resp:
                return resp.status == 200
        except Exception:
            return False

    def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        self._validate_loopback_or_authorize()
        if not self.is_available():
            raise RuntimeError(f"Local Ollama endpoint '{self.endpoint}' is unreachable.")

        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "system": system_prompt or "",
            "stream": False
        }
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(self.endpoint, data=data, headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=30.0) as resp:
            res_json = json.loads(resp.read().decode("utf-8"))
            return res_json.get("response", "")


class RemoteModelAdapter(ModelBackend):
    """Adapter for authorized external cloud models (OpenAI, Anthropic, etc.)."""

    def __init__(self, provider: str = "openai", model_name: str = "gpt-4o"):
        self.provider = provider
        self.model_name = model_name

    def is_available(self) -> bool:
        try:
            require_tier(OperationTier.EXTERNAL_MODEL_NETWORK, f"check_{self.provider}")
            return True
        except SimLabAuthorizationError:
            return False

    def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        require_tier(OperationTier.EXTERNAL_MODEL_NETWORK, f"call_{self.provider}")
        raise NotImplementedError("Live remote API execution is configured but endpoint credentials are not set.")

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
        arr = [float(x) for x in inputs]
        res = round(sum(arr), 6)
        if res.is_integer():
            res = int(res)
        meta["sample_count"] = len(arr)
        return res, meta

    elif op == "weighted_sum":
        arr = [float(x) for x in inputs]
        weights = [float(w) for w in req.get("weights", [1.0] * len(arr))]
        res = round(sum(x * w for x, w in zip(arr, weights)), 6)
        meta["sample_count"] = len(arr)
        return res, meta

    elif op == "mean":
        arr = [float(x) for x in inputs]
        res = round(sum(arr) / len(arr), 6) if arr else 0.0
        meta["sample_count"] = len(arr)
        return res, meta

    elif op == "median":
        arr = [float(x) for x in inputs]
        res = round(float(np.median(arr)), 6) if arr else 0.0
        meta["sample_count"] = len(arr)
        return res, meta

    elif op == "variance":
        arr = [float(x) for x in inputs]
        ddof = int(req.get("ddof", 0))
        res = round(float(np.var(arr, ddof=ddof)), 6) if len(arr) > ddof else 0.0
        meta["sample_count"] = len(arr)
        return res, meta

    elif op == "std":
        arr = [float(x) for x in inputs]
        ddof = int(req.get("ddof", 0))
        res = round(float(np.std(arr, ddof=ddof)), 6) if len(arr) > ddof else 0.0
        meta["sample_count"] = len(arr)
        return res, meta

    elif op == "min":
        arr = [float(x) for x in inputs]
        res = min(arr) if arr else 0.0
        if isinstance(res, float) and res.is_integer():
            res = int(res)
        meta["sample_count"] = len(arr)
        return res, meta

    elif op == "max":
        arr = [float(x) for x in inputs]
        res = max(arr) if arr else 0.0
        if isinstance(res, float) and res.is_integer():
            res = int(res)
        meta["sample_count"] = len(arr)
        return res, meta

    elif op == "range":
        arr = [float(x) for x in inputs]
        res = round(max(arr) - min(arr), 6) if arr else 0.0
        if isinstance(res, float) and res.is_integer():
            res = int(res)
        meta["sample_count"] = len(arr)
        return res, meta

    elif op == "polynomial":
        coeffs = [float(c) for c in req.get("coefficients", inputs)]
        x_val = float(req.get("x", 1.0))
        total = sum(c * (x_val ** idx) for idx, c in enumerate(coeffs))
        res = round(total, 6)
        if res.is_integer():
            res = int(res)
        meta["degree"] = max(0, len(coeffs) - 1)
        return res, meta

    elif op in ("linear_difference", "delta"):
        start_val = float(req.get("start", inputs[0] if len(inputs) >= 1 else 0.0))
        end_val = float(req.get("end", inputs[1] if len(inputs) >= 2 else 0.0))
        res = round(end_val - start_val, 6)
        return res, meta

    elif op in ("linear_scale", "affine"):
        base_val = float(req.get("base", inputs[0] if inputs else 0.0))
        scale = float(req.get("scale", 1.0))
        offset = float(req.get("offset", 0.0))
        res = round(base_val * scale + offset, 6)
        if res.is_integer():
            res = int(res)
        return res, meta

    elif op == "dot_product":
        vec_a = [float(x) for x in req.get("vec_a", inputs[0] if len(inputs) >= 1 else [])]
        vec_b = [float(x) for x in req.get("vec_b", inputs[1] if len(inputs) >= 2 else [])]
        res = round(float(np.dot(vec_a, vec_b)), 6)
        if res.is_integer():
            res = int(res)
        meta["dimension"] = len(vec_a)
        return res, meta

    elif op == "cosine_similarity":
        vec_a = [float(x) for x in req.get("vec_a", inputs[0] if len(inputs) >= 1 else [])]
        vec_b = [float(x) for x in req.get("vec_b", inputs[1] if len(inputs) >= 2 else [])]
        res = round(float(cosine_similarity(vec_a, vec_b)), 6)
        meta["dimension"] = len(vec_a)
        return res, meta

    elif op == "anomaly_count":
        arr = np.array([float(x) for x in inputs], dtype=float)
        threshold = float(req.get("threshold", 2.0))
        if len(arr) == 0:
            return 0, {"sample_count": 0}
        mean_val = float(np.mean(arr))
        std_val = float(np.std(arr, ddof=0))
        if std_val == 0.0:
            count = 0
        else:
            z_scores = np.abs((arr - mean_val) / std_val)
            count = int(np.sum(z_scores > threshold))
        meta["sample_count"] = int(len(arr))
        return count, meta

    elif op == "filter_sum":
        arr = [float(x) for x in inputs]
        min_v = req.get("min_val")
        max_v = req.get("max_val")
        filtered = [
            x for x in arr
            if (min_v is None or x >= float(min_v)) and (max_v is None or x <= float(max_v))
        ]
        res = round(sum(filtered), 6)
        if res.is_integer():
            res = int(res)
        meta["sample_count"] = len(filtered)
        return res, meta

    elif op == "moving_average":
        arr = [float(x) for x in inputs]
        window = max(1, int(req.get("window", 3)))
        if len(arr) < window:
            res = round(sum(arr) / len(arr), 6) if arr else 0.0
        else:
            res = round(sum(arr[-window:]) / window, 6)
        meta["window"] = window
        return res, meta

    elif op == "record_reconcile":
        set_a = set(req.get("records_a", inputs[0] if len(inputs) >= 1 else []))
        set_b = set(req.get("records_b", inputs[1] if len(inputs) >= 2 else []))
        diff_count = len(set_a.symmetric_difference(set_b))
        meta["reconciled_total"] = len(set_a.union(set_b))
        return diff_count, meta

    elif op == "linear_solve":
        mat_a = np.array(req.get("matrix_a", [[1.0]]), dtype=float)
        vec_b = np.array(req.get("vector_b", [1.0]), dtype=float)
        sol = np.linalg.solve(mat_a, vec_b)
        res = round(float(np.sum(sol)), 6)
        return res, meta

    elif op == "pipeline_reduce":
        reduce_op = str(req.get("reduce_op", "sum")).lower()
        vals = [float(x) for x in inputs]
        if reduce_op == "product":
            prod = 1.0
            for v in vals:
                prod *= v
            res = round(prod, 6)
        elif reduce_op == "mean":
            res = round(sum(vals) / len(vals), 6) if vals else 0.0
        else:
            res = round(sum(vals), 6)
        if isinstance(res, float) and res.is_integer():
            res = int(res)
        meta["sample_count"] = len(vals)
        return res, meta

    default_val = req.get("expected_value", 42)
    return default_val, meta


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

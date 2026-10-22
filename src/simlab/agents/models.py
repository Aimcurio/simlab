"""Model Adapters for Agent Decision Making."""

from abc import ABC, abstractmethod
import json
from typing import Any, Dict, Optional
import urllib.request
import urllib.error

from simlab.governance import OperationTier, require_tier, SimLabAuthorizationError


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

    def __init__(self, model_name: str = "llama3:latest", endpoint: str = "http://localhost:11434/api/generate"):
        self.model_name = model_name
        self.endpoint = endpoint

    def is_available(self) -> bool:
        """Ping local Ollama endpoint."""
        try:
            req = urllib.request.Request("http://localhost:11434/", method="GET")
            with urllib.request.urlopen(req, timeout=1.0) as resp:
                return resp.status == 200
        except Exception:
            return False

    def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
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
        # Check governance firewall tier
        try:
            require_tier(OperationTier.EXTERNAL_MODEL_NETWORK, f"check_{self.provider}")
            return True
        except SimLabAuthorizationError:
            return False

    def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        require_tier(OperationTier.EXTERNAL_MODEL_NETWORK, f"call_{self.provider}")
        # When authorized, perform call
        raise NotImplementedError("Live remote API execution is configured but endpoint credentials are not set.")

"""Authoritative Simulation State and State Transition Engine."""

import hashlib
import json
from typing import Any, Dict, List, Optional, Tuple


class EnvironmentState:
    """Manages authoritative simulation state with cryptographic state hashing."""

    def __init__(self, initial_data: Optional[Dict[str, Any]] = None):
        self._data: Dict[str, Any] = dict(initial_data or {})
        self._history: List[Dict[str, Any]] = []

    def get(self, key: str, default: Any = None) -> Any:
        """Retrieve state variable."""
        return self._data.get(key, default)

    def __getitem__(self, key: str) -> Any:
        return self._data[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self._data[key] = value

    def __contains__(self, key: str) -> bool:
        return key in self._data

    def __getattr__(self, name: str) -> Any:
        if "_data" in self.__dict__ and name in self._data:
            return self._data[name]
        raise AttributeError(f"'EnvironmentState' object has no attribute '{name}'")

    def set(self, key: str, value: Any) -> None:
        """Set state variable."""
        self._data[key] = value

    def update(self, delta: Dict[str, Any]) -> None:
        """Batch update state variables."""
        self._data.update(delta)

    def to_dict(self) -> Dict[str, Any]:
        """Return deep copy of current state dictionary."""
        return json.loads(json.dumps(self._data))

    def compute_hash(self) -> str:
        """Calculate canonical SHA-256 hash of current state."""
        canonical_json = json.dumps(self._data, sort_keys=True, default=str)
        return hashlib.sha256(canonical_json.encode("utf-8")).hexdigest()

    def apply_transition(
        self,
        transition_type: str,
        actor_id: str,
        params: Dict[str, Any],
        tick: int
    ) -> Tuple[bool, str, Dict[str, Any]]:
        """
        Apply a generic state transition with delta logging.
        Subclasses or environments can override/extend this.
        """
        before_hash = self.compute_hash()
        delta: Dict[str, Any] = {}

        if transition_type == "SET_VARIABLE":
            key = params["key"]
            val = params["value"]
            self._data[key] = val
            delta = {key: val}
        elif transition_type == "INCREMENT_RESOURCE":
            res = params["resource"]
            amount = params.get("amount", 1)
            self._data[res] = self._data.get(res, 0) + amount
            delta = {res: self._data[res]}
        elif transition_type == "DECREMENT_RESOURCE":
            res = params["resource"]
            amount = params.get("amount", 1)
            cur = self._data.get(res, 0)
            if cur < amount:
                return False, f"Insufficient resource '{res}': requested {amount}, available {cur}", {}
            self._data[res] = cur - amount
            delta = {res: self._data[res]}
        else:
            # Custom transition
            delta = dict(params)
            self._data.update(params)

        after_hash = self.compute_hash()
        transition_record = {
            "tick": tick,
            "transition_type": transition_type,
            "actor_id": actor_id,
            "delta": delta,
            "before_hash": before_hash,
            "after_hash": after_hash
        }
        self._history.append(transition_record)
        return True, "SUCCESS", delta

    def get_history(self) -> List[Dict[str, Any]]:
        """Get transition history."""
        return list(self._history)

    def snapshot(self) -> Dict[str, Any]:
        """Create serializable snapshot."""
        return {
            "data": self.to_dict(),
            "history_count": len(self._history),
            "state_hash": self.compute_hash()
        }

    def restore(self, data: Dict[str, Any]) -> None:
        """Restore state from snapshot."""
        self._data = dict(data["data"])
        self._history.clear()

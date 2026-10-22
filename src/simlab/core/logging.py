"""Causal Hash-Chained Event Logger and Provenance Tracker."""

import hashlib
import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
import uuid


class CausalEventLogger:
    """
    Append-only causal event logger with cryptographic hash-chaining.
    Every event references its causal parent and incorporates the previous
    event's digest, providing tamper-evident verification.
    """

    GENESIS_HASH = "0" * 64

    def __init__(self, run_id: Optional[str] = None):
        self.run_id = run_id or f"run_{uuid.uuid4().hex[:12]}"
        self._events: List[Dict[str, Any]] = []
        self._last_event_hash: str = self.GENESIS_HASH

    @property
    def latest_hash(self) -> str:
        """Current tip hash of the event chain."""
        return self._last_event_hash

    def log_event(
        self,
        tick: int,
        actor_id: str,
        action: str,
        inputs: Optional[Dict[str, Any]] = None,
        outcome: Optional[Dict[str, Any]] = None,
        state_hash_after: Optional[str] = None,
        parent_event_id: Optional[str] = None,
        event_type: str = "AGENT_ACTION"
    ) -> Dict[str, Any]:
        """Append a tamper-evident event to the causal chain."""
        event_seq = len(self._events) + 1
        event_id = f"ev_{self.run_id}_{tick:04d}_{event_seq:04d}"
        clean_inputs = json.loads(json.dumps(inputs, default=str)) if inputs else {}
        clean_outcome = json.loads(json.dumps(outcome, default=str)) if outcome else {}
        clean_state_hash = state_hash_after or ""

        # Compute deterministic event hash
        payload_to_hash = {
            "previous_event_hash": self._last_event_hash,
            "event_id": event_id,
            "sequence": event_seq,
            "tick": tick,
            "actor_id": actor_id,
            "action": action,
            "event_type": event_type,
            "parent_event_id": parent_event_id,
            "inputs": clean_inputs,
            "outcome": clean_outcome,
            "state_hash_after": clean_state_hash,
        }
        canonical_str = json.dumps(payload_to_hash, sort_keys=True, default=str)
        event_hash = hashlib.sha256(canonical_str.encode("utf-8")).hexdigest()

        event_record = dict(payload_to_hash)
        event_record["event_hash"] = event_hash

        self._events.append(event_record)
        self._last_event_hash = event_hash
        return event_record

    def verify_chain(self) -> Tuple[bool, Optional[str]]:
        """
        Cryptographically verify the entire event chain from genesis.
        Returns (is_valid, error_message_if_invalid).
        """
        expected_prev = self.GENESIS_HASH

        for idx, ev in enumerate(self._events):
            if ev["previous_event_hash"] != expected_prev:
                return False, f"Broken chain at event {idx} ({ev['event_id']}): expected prev {expected_prev}, got {ev['previous_event_hash']}"

            payload_check = {
                "previous_event_hash": ev["previous_event_hash"],
                "event_id": ev["event_id"],
                "sequence": ev["sequence"],
                "tick": ev["tick"],
                "actor_id": ev["actor_id"],
                "action": ev["action"],
                "event_type": ev["event_type"],
                "parent_event_id": ev["parent_event_id"],
                "inputs": ev["inputs"],
                "outcome": ev["outcome"],
                "state_hash_after": ev["state_hash_after"],
            }
            computed_hash = hashlib.sha256(
                json.dumps(payload_check, sort_keys=True, default=str).encode("utf-8")
            ).hexdigest()

            if computed_hash != ev["event_hash"]:
                return False, f"Tampered event at index {idx} ({ev['event_id']}): recorded {ev['event_hash']}, computed {computed_hash}"

            expected_prev = ev["event_hash"]

        return True, None

    def get_events(
        self,
        actor_id: Optional[str] = None,
        event_type: Optional[str] = None,
        min_tick: Optional[int] = None,
        max_tick: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Query events with optional filtering."""
        filtered = self._events
        if actor_id:
            filtered = [e for e in filtered if e["actor_id"] == actor_id]
        if event_type:
            filtered = [e for e in filtered if e["event_type"] == event_type]
        if min_tick is not None:
            filtered = [e for e in filtered if e["tick"] >= min_tick]
        if max_tick is not None:
            filtered = [e for e in filtered if e["tick"] <= max_tick]
        return list(filtered)

    def to_list(self) -> List[Dict[str, Any]]:
        """Return all events."""
        return list(self._events)

    def __len__(self) -> int:
        return len(self._events)

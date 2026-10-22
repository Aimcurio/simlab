"""Replay Engine for Deterministic Simulation Verification."""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from simlab.core.logging import CausalEventLogger


class ReplayEngine:
    """Verifies and replays recorded simulation event traces."""

    def __init__(self, events: Optional[List[Dict[str, Any]]] = None):
        self._events: List[Dict[str, Any]] = list(events or [])
        self._current_step_idx: int = 0

    @classmethod
    def from_jsonl(cls, filepath: Path) -> "ReplayEngine":
        """Load events from a JSONL file."""
        events = []
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    events.append(json.loads(line))
        return cls(events)

    @classmethod
    def from_logger(cls, logger: CausalEventLogger) -> "ReplayEngine":
        """Instantiate replay from a logger."""
        return cls(logger.to_list())

    def verify_integrity(self) -> Tuple[bool, Optional[str]]:
        """Verify the cryptographic hash-chain across all recorded events."""
        logger = CausalEventLogger()
        logger._events = self._events
        return logger.verify_chain()

    @property
    def total_events(self) -> int:
        return len(self._events)

    def get_events_for_tick(self, tick: int) -> List[Dict[str, Any]]:
        """Get all events logged at a specific tick."""
        return [e for e in self._events if e.get("tick") == tick]

    def get_ticks(self) -> List[int]:
        """List all distinct ticks represented in the trace."""
        return sorted(list(set(e.get("tick", 0) for e in self._events)))

    def step(self) -> Optional[Dict[str, Any]]:
        """Advance replay by one event."""
        if self._current_step_idx < len(self._events):
            ev = self._events[self._current_step_idx]
            self._current_step_idx += 1
            return ev
        return None

    def reset(self) -> None:
        """Reset replay pointer to beginning."""
        self._current_step_idx = 0

    def compare_traces(self, other_events: List[Dict[str, Any]]) -> Tuple[bool, List[str]]:
        """
        Compare two event traces for bit-for-bit determinism.
        Returns (is_identical, list_of_discrepancies).
        """
        discrepancies = []
        if len(self._events) != len(other_events):
            discrepancies.append(
                f"Event count mismatch: original has {len(self._events)}, other has {len(other_events)}"
            )

        for i, (ev1, ev2) in enumerate(zip(self._events, other_events)):
            if ev1.get("event_hash") != ev2.get("event_hash"):
                discrepancies.append(
                    f"Hash mismatch at event {i} (tick {ev1.get('tick')}): {ev1.get('event_hash')} != {ev2.get('event_hash')}"
                )
            if ev1.get("action") != ev2.get("action"):
                discrepancies.append(
                    f"Action mismatch at event {i}: {ev1.get('action')} != {ev2.get('action')}"
                )
            if ev1.get("actor_id") != ev2.get("actor_id"):
                discrepancies.append(
                    f"Actor mismatch at event {i}: {ev1.get('actor_id')} != {ev2.get('actor_id')}"
                )

        return len(discrepancies) == 0, discrepancies

    @classmethod
    def from_run_dir(cls, run_dir: Path) -> Tuple["ReplayEngine", Dict[str, Any]]:
        """Load engine and manifest from a run directory."""
        events_file = run_dir / "events.jsonl"
        manifest_file = run_dir / "manifest.json"
        engine = cls.from_jsonl(events_file)
        manifest = {}
        if manifest_file.exists():
            with open(manifest_file, "r", encoding="utf-8") as f:
                manifest = json.load(f)
        return engine, manifest

    def replay_state(
        self,
        scenario_identifier_or_config: Any,
        expected_terminal_hash: Optional[str] = None
    ) -> Tuple[bool, Optional[str], Optional[Dict[str, Any]]]:
        """
        Replay all state transitions onto a fresh simulation environment.
        Verifies that replaying the event actions produces the authoritative terminal state hash.
        Returns (is_valid, error_message, final_state_dict).
        """
        from simlab.scenarios.loader import ScenarioLoader
        from simlab.agents.base import AgentAction

        loader = ScenarioLoader()
        if isinstance(scenario_identifier_or_config, str):
            cfg = loader.load_scenario(scenario_identifier_or_config)
        else:
            cfg = scenario_identifier_or_config

        # Instantiate fresh environment and kernel
        kernel, env = loader.build_simulation(cfg, seed=0)

        for idx, ev in enumerate(self._events):
            action_type = ev.get("action")
            handler = kernel._action_handlers.get(action_type)
            if handler:
                params = ev.get("inputs", {}).get("parameters", {})
                target = ev.get("inputs", {}).get("target")
                tick = ev.get("tick", 0)
                action = AgentAction(
                    action_type=action_type,
                    target=target,
                    parameters=params
                )
                handler(action, tick)

        replayed_hash = env.state.compute_hash()
        final_state = env.state.to_dict()

        if expected_terminal_hash is not None and replayed_hash != expected_terminal_hash:
            return (
                False,
                f"State replay hash mismatch: replayed {replayed_hash} != expected {expected_terminal_hash}",
                final_state
            )

        return True, None, final_state

    def verify_full_provenance(
        self,
        scenario_identifier_or_config: Any,
        expected_terminal_hash: Optional[str] = None
    ) -> Tuple[bool, Optional[str], Optional[Dict[str, Any]]]:
        """
        Comprehensive dual verification:
        1. Cryptographic causal event hash-chain integrity
        2. State transition replay and terminal state hash equivalence
        """
        chain_valid, chain_err = self.verify_integrity()
        if not chain_valid:
            return False, f"Causal event chain verification failed: {chain_err}", None

        state_valid, state_err, state_dict = self.replay_state(
            scenario_identifier_or_config=scenario_identifier_or_config,
            expected_terminal_hash=expected_terminal_hash
        )
        if not state_valid:
            return False, f"State replay verification failed: {state_err}", state_dict

        return True, None, state_dict

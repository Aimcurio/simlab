"""Run Manifest and Metadata Data Model."""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional
import subprocess


def get_git_revision() -> str:
    """Safely obtain current git commit hash for SimLab repository."""
    try:
        repo_root = Path(__file__).resolve().parents[3]
        rev = subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            cwd=str(repo_root),
            stderr=subprocess.DEVNULL,
            text=True
        ).strip()
        return rev
    except Exception:
        return "UNKNOWN_GIT_REVISION"


@dataclass
class RunManifest:
    """Immutable provenance manifest for an experimental run."""
    run_id: str
    scenario_id: str
    seed: int
    git_revision: str = field(default_factory=get_git_revision)
    start_time_utc: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    end_time_utc: Optional[str] = None
    status: str = "INITIALIZED"  # INITIALIZED, RUNNING, COMPLETED, FAILED, PARTIAL
    total_ticks: int = 0
    total_events: int = 0
    total_messages: int = 0
    terminal_state_hash: str = ""
    event_chain_valid: bool = False
    parameters: Dict[str, Any] = field(default_factory=dict)
    resource_usage: Dict[str, Any] = field(default_factory=dict)
    error: Optional[str] = None

    def mark_completed(
        self,
        ticks: int,
        events: int,
        messages: int,
        state_hash: str,
        chain_valid: bool,
        resources: Optional[Dict[str, Any]] = None
    ) -> None:
        """Finalize manifest upon successful run completion."""
        self.status = "COMPLETED"
        self.end_time_utc = datetime.now(timezone.utc).isoformat()
        self.total_ticks = ticks
        self.total_events = events
        self.total_messages = messages
        self.terminal_state_hash = state_hash
        self.event_chain_valid = chain_valid
        if resources:
            self.resource_usage = resources

    def mark_failed(self, error_message: str, ticks: int = 0) -> None:
        """Record run failure status."""
        self.status = "FAILED"
        self.end_time_utc = datetime.now(timezone.utc).isoformat()
        self.total_ticks = ticks
        self.error = error_message

    def to_dict(self) -> Dict[str, Any]:
        """Convert manifest to serializable dictionary."""
        return {
            "run_id": self.run_id,
            "scenario_id": self.scenario_id,
            "seed": self.seed,
            "git_revision": self.git_revision,
            "start_time_utc": self.start_time_utc,
            "end_time_utc": self.end_time_utc,
            "status": self.status,
            "total_ticks": self.total_ticks,
            "total_events": self.total_events,
            "total_messages": self.total_messages,
            "terminal_state_hash": self.terminal_state_hash,
            "event_chain_valid": self.event_chain_valid,
            "parameters": self.parameters,
            "resource_usage": self.resource_usage,
            "error": self.error,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "RunManifest":
        """Reconstruct manifest from dictionary."""
        return cls(**data)

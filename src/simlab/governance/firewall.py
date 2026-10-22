"""SimLab Tiered Governance Firewall."""

import json
import os
from pathlib import Path
from typing import Any, Dict, Optional

from simlab.governance.permissions import OperationTier, SimLabAuthorizationError


def get_default_governance_path() -> Path:
    """Resolve GOVERNANCE.json path dynamically from repo root or env var."""
    env_path = os.environ.get("SIMLAB_GOVERNANCE_PATH")
    if env_path:
        return Path(env_path).resolve()
    # Path is 3 levels up from src/simlab/governance/firewall.py -> repo root
    return Path(__file__).resolve().parents[3] / "GOVERNANCE.json"


class GovernanceManager:
    """Manages tier-separated governance policies and enforces boundaries."""

    def __init__(self, governance_path: Optional[Path] = None):
        self.path = governance_path or get_default_governance_path()
        self._data: Optional[Dict[str, Any]] = None

    def load(self, force_reload: bool = False) -> Dict[str, Any]:
        """Load and cache the GOVERNANCE.json descriptor."""
        if self._data is not None and not force_reload:
            return self._data

        if not self.path.exists():
            # If missing, fail-closed for restricted tiers, but provide defaults
            self._data = {
                "canonical_lifecycle_state": "UNCONFIGURED",
                "authority_state": {},
                "execution_firewall": {
                    "runtime_execution_permitted": False,
                    "live_api_calls_permitted": False,
                }
            }
            return self._data

        try:
            with open(self.path, "r", encoding="utf-8") as f:
                self._data = json.load(f)
        except Exception as e:
            raise SimLabAuthorizationError(
                operation="load_governance",
                tier=OperationTier.READ_ONLY_ANALYSIS,
                applicable_restriction=f"Corrupt or unreadable GOVERNANCE.json at '{self.path}'",
                resolution_path="Restore valid JSON formatting in GOVERNANCE.json.",
                details=str(e)
            )

        return self._data

    def check_authorization(self, tier: OperationTier, operation: str) -> None:
        """
        Assert authorization for a given operational tier.
        Raises SimLabAuthorizationError if the operation is blocked.
        """
        # Tier 1: Read-only analysis is always permitted
        if tier == OperationTier.READ_ONLY_ANALYSIS:
            return

        # Tier 2: Local development, mock agents, and unit tests are permitted
        if tier == OperationTier.LOCAL_DEV_TEST:
            return

        # Tier 3: Deterministic mock experiments (local simulation, no external calls, rule-based)
        if tier == OperationTier.DETERMINISTIC_MOCK_EXPERIMENT:
            return

        gov = self.load()
        state = gov.get("canonical_lifecycle_state", "UNKNOWN")
        auth_state = gov.get("authority_state", {})
        firewall = gov.get("execution_firewall", {})

        # Tier 4: Authorized empirical experiments (modifying state or running heavy matrix benchmarks)
        if tier == OperationTier.AUTHORIZED_EMPIRICAL_EXPERIMENT:
            if state == "PAUSED / CONTRACT_TIGHTENING_REQUIRED":
                raise SimLabAuthorizationError(
                    operation=operation,
                    tier=tier,
                    applicable_restriction=(
                        f"Canonical lifecycle state is '{state}'. "
                        "Governing body has placed empirical benchmark runs on hold pending contract ratification."
                    ),
                    resolution_path=(
                        "For local testing and algorithm verification, run in DETERMINISTIC_MOCK mode "
                        "(e.g., using rule-based/mock backends). To run full empirical matrix sweeps, "
                        "obtain requester ratification in GOVERNANCE.json."
                    )
                )

            if auth_state.get("experiment_execution_authority") != "GRANTED":
                raise SimLabAuthorizationError(
                    operation=operation,
                    tier=tier,
                    applicable_restriction="authority_state.experiment_execution_authority is NOT GRANTED.",
                    resolution_path="Request explicit experiment execution grant from lead researcher/requester."
                )
            return

        # Tier 5: External model or network execution (paid API calls, external servers)
        if tier == OperationTier.EXTERNAL_MODEL_NETWORK:
            if not firewall.get("live_api_calls_permitted", False):
                raise SimLabAuthorizationError(
                    operation=operation,
                    tier=tier,
                    applicable_restriction="execution_firewall.live_api_calls_permitted is False.",
                    resolution_path=(
                        "Use offline deterministic models (DeterministicMockBackend) or local self-hosted "
                        "endpoints (Ollama / LM Studio) that do not incur paid API charges. "
                        "If paid remote model access is required, obtain explicit authorization in GOVERNANCE.json."
                    )
                )
            return

        # Tier 6: Restricted or destructive operations (overwriting historical gates, deleting telemetry)
        if tier == OperationTier.RESTRICTED_DESTRUCTIVE:
            raise SimLabAuthorizationError(
                operation=operation,
                tier=tier,
                applicable_restriction="Operation involves destructive mutation of audit, gate, or immutable telemetry assets.",
                resolution_path="Destructive operations on canonical evidence are strictly blocked by fail-closed policy."
            )

    def is_authorized(self, tier: OperationTier, operation: str) -> bool:
        """Check authorization returning a boolean instead of raising."""
        try:
            self.check_authorization(tier, operation)
            return True
        except SimLabAuthorizationError:
            return False

    def check_permission(self, tier: OperationTier, operation: str) -> bool:
        """Alias for is_authorized."""
        return self.is_authorized(tier, operation)

    def verify_operation(
        self,
        tier: OperationTier,
        operation: str,
        config_override: Optional[Dict[str, Any]] = None
    ) -> None:
        """Verify operation with optional config override."""
        old_data = self._data
        try:
            if config_override is not None:
                self._data = config_override
            self.check_authorization(tier, operation)
        finally:
            if config_override is not None:
                self._data = old_data


# Alias for audit and backward compatibility
GovernanceFirewallBlockedError = SimLabAuthorizationError

# Global default firewall instance
default_firewall = GovernanceManager()


def require_tier(tier: OperationTier, operation: str) -> None:
    """Convenience helper to enforce tier boundaries."""
    default_firewall.check_authorization(tier, operation)


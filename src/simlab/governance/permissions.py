"""SimLab Governance Permission Tiers and Exceptions."""

from enum import Enum
from typing import Optional


class OperationTier(str, Enum):
    """Operational tiers for governance enforcement."""
    READ_ONLY_ANALYSIS = "READ_ONLY_ANALYSIS"
    LOCAL_DEV_TEST = "LOCAL_DEV_TEST"
    DETERMINISTIC_MOCK_EXPERIMENT = "DETERMINISTIC_MOCK_EXPERIMENT"
    AUTHORIZED_EMPIRICAL_EXPERIMENT = "AUTHORIZED_EMPIRICAL_EXPERIMENT"
    EXTERNAL_MODEL_NETWORK = "EXTERNAL_MODEL_NETWORK"
    RESTRICTED_DESTRUCTIVE = "RESTRICTED_DESTRUCTIVE"

    # Aliases
    LOCAL_DEV = "LOCAL_DEV_TEST"
    EMPIRICAL_LIVE = "AUTHORIZED_EMPIRICAL_EXPERIMENT"


class SimLabAuthorizationError(PermissionError):
    """Structured authorization error with clear diagnostic and remediation guidance."""

    def __init__(
        self,
        operation: str,
        tier: OperationTier,
        applicable_restriction: str,
        resolution_path: str,
        details: Optional[str] = None
    ):
        self.operation = operation
        self.tier = tier
        self.applicable_restriction = applicable_restriction
        self.resolution_path = resolution_path
        self.details = details or ""

        message = (
            f"\n[SimLab Governance Firewall] Operation '{operation}' in tier '{tier.value}' is BLOCKED.\n"
            f"Applicable Restriction: {applicable_restriction}\n"
            f"Legitimate Resolution Path: {resolution_path}"
        )
        if self.details:
            message += f"\nDetails: {self.details}"
        super().__init__(message)

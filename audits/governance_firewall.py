"""
Curo Governance Execution Firewall & State Validator
Location: audits/governance_firewall.py

Enforces deterministic, programmatic execution firewalls (NC-60, Gap 5.1, Gap 5.2)
to guarantee that test harnesses, simulators, and scripts cannot execute when
SimLab canonical state is PAUSED / CONTRACT_TIGHTENING_REQUIRED.
"""

import os
import json
from typing import Dict, Any, Optional

DEFAULT_GOVERNANCE_PATH = os.environ.get(
    "SIMLAB_GOVERNANCE_PATH",
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "GOVERNANCE.json"))
)

PERMITTED_LIFECYCLE_STATES = {
    "PAUSED / CONTRACT_TIGHTENING_REQUIRED",
    "PLANNING",
    "RESEARCH_DESIGN",
    "RESEARCH_AUTHORIZED",
    "RESEARCHING",
    "RESEARCH_REVIEW",
    "GATE_R1_COMPLETE",
    "REPRODUCTION_DESIGN_AUTHORIZED",
    "REPRODUCTION_DESIGNING",
    "REPRODUCTION_REVIEW",
    "GATE_R2_COMPLETE",
    "REPRODUCTION_EXECUTION_AUTHORIZED",
    "REPRODUCING",
    "REPRODUCTION_AUDIT",
    "GATE_R3_COMPLETE",
    "ABLATION_DESIGN_AUTHORIZED",
    "ABLATION_DESIGNING",
    "ABLATION_DESIGN_REVIEW",
    "PHASE_4_DESIGN_COMPLETE",
    "PHASE_4_EXECUTION_AUTHORIZED",
    "PHASE_4_AUDIT",
    "GATE_R4_COMPLETE"
}

AUTHORIZED_EXECUTION_STATES = {
    "REPRODUCTION_EXECUTION_AUTHORIZED",
    "REPRODUCING",
    "PHASE_4_EXECUTION_AUTHORIZED"
}


class GovernanceFirewallBlockedError(PermissionError):
    """Raised when execution is blocked by the Curo Governance Firewall."""
    pass


class GovernanceStateError(ValueError):
    """Raised when governance state descriptors are malformed or invalid."""
    pass


def load_governance(filepath: Optional[str] = None) -> Dict[str, Any]:
    """
    Load and deterministically validate the machine-readable GOVERNANCE.json descriptor.
    Enforces fail-closed semantics on any missing, corrupted, or invalid configuration.
    """
    path = filepath or DEFAULT_GOVERNANCE_PATH
    if not os.path.exists(path):
        raise GovernanceFirewallBlockedError(
            f"Governance descriptor not found at '{path}'. Fail-closed: execution is strictly blocked."
        )

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        raise GovernanceFirewallBlockedError(
            f"Corrupted or unparseable GOVERNANCE.json at '{path}': {e}. Fail-closed: execution is strictly blocked."
        )

    if not isinstance(data, dict):
        raise GovernanceFirewallBlockedError(
            f"GOVERNANCE.json root must be a JSON object at '{path}'. Fail-closed: execution is strictly blocked."
        )

    required_keys = [
        "schema_version",
        "canonical_lifecycle_state",
        "authority_state",
        "execution_firewall",
        "closed_gates",
        "pending_gates",
        "gate_result"
    ]
    for k in required_keys:
        if k not in data:
            raise GovernanceFirewallBlockedError(
                f"GOVERNANCE.json missing mandatory key '{k}'. Fail-closed: execution is strictly blocked."
            )

    if not isinstance(data.get("authority_state"), dict):
        raise GovernanceFirewallBlockedError(
            "GOVERNANCE.json 'authority_state' must be a JSON object. Fail-closed: execution is strictly blocked."
        )
    if not isinstance(data.get("execution_firewall"), dict):
        raise GovernanceFirewallBlockedError(
            "GOVERNANCE.json 'execution_firewall' must be a JSON object. Fail-closed: execution is strictly blocked."
        )
    if not isinstance(data.get("closed_gates"), list):
        raise GovernanceFirewallBlockedError(
            "GOVERNANCE.json 'closed_gates' must be a JSON array. Fail-closed: execution is strictly blocked."
        )
    if not isinstance(data.get("pending_gates"), list):
        raise GovernanceFirewallBlockedError(
            "GOVERNANCE.json 'pending_gates' must be a JSON array. Fail-closed: execution is strictly blocked."
        )

    state = data.get("canonical_lifecycle_state")
    if state not in PERMITTED_LIFECYCLE_STATES:
        raise GovernanceFirewallBlockedError(
            f"Unknown or unparseable canonical_lifecycle_state '{state}'. Fail-closed: execution is strictly blocked."
        )

    return data


def assert_execution_permitted(filepath: Optional[str] = None) -> None:
    """
    Assert that the current governance state permits simulation, experimentation, or code implementation.
    Raises GovernanceFirewallBlockedError if execution is not explicitly permitted.
    """
    gov = load_governance(filepath)
    state = gov.get("canonical_lifecycle_state")

    if state == "PAUSED / CONTRACT_TIGHTENING_REQUIRED":
        raise GovernanceFirewallBlockedError(
            f"Execution BLOCKED by Curo Governance Firewall: SimLab canonical state is '{state}'. "
            "Zero simulation runtime, model API calls, or experiment runs permitted."
        )

    if state not in AUTHORIZED_EXECUTION_STATES:
        raise GovernanceFirewallBlockedError(
            f"Execution BLOCKED: Lifecycle state '{state}' is not an authorized execution state. "
            f"Execution is permitted only in: {sorted(list(AUTHORIZED_EXECUTION_STATES))}."
        )

    auth = gov.get("authority_state", {})
    if auth.get("implementation_authority") != "GRANTED":
        raise GovernanceFirewallBlockedError(
            f"Execution BLOCKED: Implementation authority is '{auth.get('implementation_authority')}'. "
            "Implementation authority is NOT_GRANTED."
        )

    if auth.get("experiment_execution_authority") != "GRANTED":
        raise GovernanceFirewallBlockedError(
            f"Execution BLOCKED: Experiment execution authority is '{auth.get('experiment_execution_authority')}'. "
            "Experiment execution authority is NOT_GRANTED."
        )

    if auth.get("simulation_execution_authority") != "GRANTED":
        raise GovernanceFirewallBlockedError(
            f"Execution BLOCKED: Simulation execution authority is '{auth.get('simulation_execution_authority')}'. "
            "Simulation execution authority is NOT_GRANTED."
        )

    firewall = gov.get("execution_firewall", {})
    if firewall.get("firewall_enforcement_mode") != "FAIL_CLOSED":
        raise GovernanceFirewallBlockedError(
            f"Execution BLOCKED: firewall_enforcement_mode is '{firewall.get('firewall_enforcement_mode')}'. "
            "Must be 'FAIL_CLOSED'."
        )

    if not firewall.get("runtime_execution_permitted", False):
        raise GovernanceFirewallBlockedError(
            "Execution BLOCKED: execution_firewall.runtime_execution_permitted is False."
        )

    if not firewall.get("simulation_runs_permitted", False):
        raise GovernanceFirewallBlockedError(
            "Execution BLOCKED: execution_firewall.simulation_runs_permitted is False."
        )


def assert_primitive_adjudication_permitted(filepath: Optional[str] = None) -> None:
    """
    Assert that the current governance state permits advancing primitives to VALIDATED status.
    Raises GovernanceFirewallBlockedError if primitive adjudication is not explicitly authorized.
    """
    gov = load_governance(filepath)
    auth = gov.get("authority_state", {})
    if auth.get("primitive_adjudication_authority") != "AUTHORIZED":
        raise GovernanceFirewallBlockedError(
            f"Primitive adjudication BLOCKED by Curo Governance Firewall: "
            f"primitive_adjudication_authority is '{auth.get('primitive_adjudication_authority')}'. "
            "Primitive advancement requires explicit human requester adjudication."
        )


def assert_architecture_freeze_permitted(filepath: Optional[str] = None) -> None:
    """
    Assert that the current governance state permits freezing architecture decisions.
    Raises GovernanceFirewallBlockedError if architecture remains unfrozen.
    """
    gov = load_governance(filepath)
    auth = gov.get("authority_state", {})
    if auth.get("architecture_status") != "FROZEN":
        raise GovernanceFirewallBlockedError(
            f"Architecture freeze BLOCKED by Curo Governance Firewall: "
            f"architecture_status is '{auth.get('architecture_status')}'. "
            "Architecture remains strictly UNFROZEN under Anti-Premature-Synthesis invariant. "
            "Freezing architecture requires explicit human requester authorization."
        )


def is_execution_permitted(filepath: Optional[str] = None) -> bool:
    """Check execution permission without raising an exception."""
    try:
        assert_execution_permitted(filepath)
        return True
    except (GovernanceFirewallBlockedError, Exception):
        return False


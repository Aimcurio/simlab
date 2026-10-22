"""Tests for SimLab Governance and Permission Boundaries."""

import pytest
import tempfile
import json
from pathlib import Path

from simlab.governance import (
    OperationTier,
    SimLabAuthorizationError,
    GovernanceManager,
    require_tier,
)


def test_permitted_tiers_succeed():
    """Verify that read-only, local dev, and deterministic mock tiers are permitted."""
    manager = GovernanceManager()
    
    # Must not raise
    manager.check_authorization(OperationTier.READ_ONLY_ANALYSIS, "inspect_dataset")
    manager.check_authorization(OperationTier.LOCAL_DEV_TEST, "run_unit_test")
    manager.check_authorization(OperationTier.DETERMINISTIC_MOCK_EXPERIMENT, "run_mock_sim")
    
    assert manager.is_authorized(OperationTier.READ_ONLY_ANALYSIS, "inspect") is True
    assert manager.is_authorized(OperationTier.LOCAL_DEV_TEST, "test") is True
    assert manager.is_authorized(OperationTier.DETERMINISTIC_MOCK_EXPERIMENT, "mock") is True


def test_paused_state_blocks_empirical_experiment():
    """Verify that empirical experiments are blocked when state is paused."""
    manager = GovernanceManager()
    
    with pytest.raises(SimLabAuthorizationError) as exc_info:
        manager.check_authorization(
            OperationTier.AUTHORIZED_EMPIRICAL_EXPERIMENT,
            "run_full_matrix_ablation"
        )
    
    err = exc_info.value
    assert err.tier == OperationTier.AUTHORIZED_EMPIRICAL_EXPERIMENT
    assert "PAUSED / CONTRACT_TIGHTENING_REQUIRED" in err.applicable_restriction
    assert "DETERMINISTIC_MOCK" in err.resolution_path


def test_external_model_network_is_blocked_by_default():
    """Verify that external API network calls are blocked by fail-closed policy."""
    manager = GovernanceManager()
    
    with pytest.raises(SimLabAuthorizationError) as exc_info:
        manager.check_authorization(
            OperationTier.EXTERNAL_MODEL_NETWORK,
            "call_openai_gpt4"
        )
    
    err = exc_info.value
    assert err.tier == OperationTier.EXTERNAL_MODEL_NETWORK
    assert "live_api_calls_permitted is False" in err.applicable_restriction
    assert "DeterministicMockBackend" in err.resolution_path


def test_restricted_destructive_is_unconditionally_blocked():
    """Verify that destructive mutation of canonical evidence is strictly blocked."""
    manager = GovernanceManager()
    
    with pytest.raises(SimLabAuthorizationError) as exc_info:
        manager.check_authorization(
            OperationTier.RESTRICTED_DESTRUCTIVE,
            "overwrite_historical_telemetry"
        )
    
    err = exc_info.value
    assert err.tier == OperationTier.RESTRICTED_DESTRUCTIVE
    assert "fail-closed" in err.resolution_path.lower()


def test_authorized_empirical_when_explicitly_granted():
    """Verify that an authorized governance file allows empirical execution."""
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
        json.dump({
            "canonical_lifecycle_state": "PHASE_4_EXECUTION_AUTHORIZED",
            "authority_state": {
                "experiment_execution_authority": "GRANTED"
            },
            "execution_firewall": {
                "runtime_execution_permitted": True,
                "live_api_calls_permitted": True
            }
        }, f)
        temp_path = Path(f.name)

    try:
        custom_manager = GovernanceManager(temp_path)
        # Should not raise for empirical
        custom_manager.check_authorization(
            OperationTier.AUTHORIZED_EMPIRICAL_EXPERIMENT,
            "run_empirical"
        )
        # Should not raise for live api
        custom_manager.check_authorization(
            OperationTier.EXTERNAL_MODEL_NETWORK,
            "call_authorized_model"
        )
    finally:
        temp_path.unlink()

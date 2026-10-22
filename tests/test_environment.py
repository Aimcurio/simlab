"""Tests for Cooperative Environment and Resource Constraints."""

import pytest
from simlab.core.kernel import SimulationKernel
from simlab.environment import CooperativeTaskEnvironment
from simlab.scenarios import ScenarioLoader


def test_cooperative_environment_full_lifecycle():
    loader = ScenarioLoader()
    config = loader.load_scenario("cooperative_pipeline")
    kernel, env = loader.build_simulation(config, seed=42)

    # Initial state
    assert env.state.get("completed_count") == 0
    assert env.state.get("total_tasks") == 3
    initial_energy = env.state.get("energy")

    # Run to completion
    run_result = kernel.run(max_ticks=25)

    assert run_result.is_completed is True
    assert "ALL_TASKS_COMPLETED" in run_result.termination_reason
    assert env.state.get("completed_count") == 3
    # Verify energy was consumed during execution
    assert env.state.get("energy") < initial_energy

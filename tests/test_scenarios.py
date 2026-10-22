"""Tests for Scenario schemas and ScenarioLoader."""

import pytest
from simlab.scenarios import ScenarioLoader, ScenarioConfig


def test_builtin_scenarios_discovery():
    loader = ScenarioLoader()
    scenarios = loader.list_scenarios()
    assert len(scenarios) >= 2
    assert "cooperative_pipeline" in scenarios
    assert "resource_crisis" in scenarios


def test_load_and_validate_cooperative_pipeline():
    loader = ScenarioLoader()
    config = loader.load_scenario("cooperative_pipeline")
    assert isinstance(config, ScenarioConfig)
    assert config.scenario_id == "cooperative_pipeline"
    assert len(config.tasks) == 3
    assert len(config.agents) == 3


def test_build_simulation_from_scenario():
    loader = ScenarioLoader()
    config = loader.load_scenario("cooperative_pipeline")
    kernel, env = loader.build_simulation(config, seed=123)

    assert kernel.seed == 123
    assert len(kernel.agents) == 3
    assert "coordinator" in kernel.agents
    assert "worker_1" in kernel.agents
    assert "critic" in kernel.agents

    # Verify environment attached
    assert env.state.get("total_tasks") == 3

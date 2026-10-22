"""Scenario Loader and Simulation Factory."""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from simlab.agents.coordinator import CoordinatorAgent
from simlab.agents.critic import CriticAgent
from simlab.agents.worker import WorkerAgent
from simlab.core.kernel import SimulationKernel
from simlab.environment.cooperative_task import CooperativeTaskEnvironment
from simlab.scenarios.schema import ScenarioConfig


def get_builtin_scenarios_dir() -> Path:
    """Return path to built-in scenario definition files."""
    return Path(__file__).resolve().parent / "definitions"


class ScenarioLoader:
    """Discovers, validates, and instantiates scenarios."""

    def __init__(self, scenarios_dir: Optional[Path] = None):
        self.scenarios_dir = scenarios_dir or get_builtin_scenarios_dir()

    def list_scenarios(self) -> List[str]:
        """List all available scenario IDs."""
        if not self.scenarios_dir.exists():
            return []
        files = list(self.scenarios_dir.glob("*.json"))
        return [f.stem for f in files]

    def load_scenario(self, scenario_identifier: str) -> ScenarioConfig:
        """Load and validate scenario configuration by ID or path."""
        path = Path(scenario_identifier)
        if not path.is_file():
            # Check built-in scenarios
            candidate = self.scenarios_dir / f"{scenario_identifier}.json"
            if candidate.is_file():
                path = candidate
            else:
                raise FileNotFoundError(
                    f"Scenario '{scenario_identifier}' not found in '{self.scenarios_dir}' or as direct file path."
                )

        with open(path, "r", encoding="utf-8") as f:
            raw_data = json.load(f)

        return ScenarioConfig.model_validate(raw_data)

    def build_simulation(
        self,
        config: ScenarioConfig,
        seed: int = 42
    ) -> Tuple[SimulationKernel, CooperativeTaskEnvironment]:
        """Build configured kernel and environment ready for execution."""
        kernel = SimulationKernel(seed=seed, run_id=f"run_s{seed}")

        # 1. Environment
        tasks_data = [t.model_dump() for t in config.tasks]
        env = CooperativeTaskEnvironment(
            tasks=tasks_data,
            initial_energy=config.initial_energy,
            initial_bandwidth=config.initial_bandwidth,
            initial_budget=config.initial_budget
        )
        env.attach_to_kernel(kernel)

        # 2. Instantiate agents
        for agent_def in config.agents:
            role_lower = agent_def.role.lower()
            if "coordinator" in role_lower:
                agent = CoordinatorAgent(
                    agent_id=agent_def.agent_id,
                    managed_workers=agent_def.managed_workers or ["worker_1", "worker_2"]
                )
            elif "critic" in role_lower or "reviewer" in role_lower:
                agent = CriticAgent(
                    agent_id=agent_def.agent_id
                )
            else:
                agent = WorkerAgent(
                    agent_id=agent_def.agent_id,
                    specialization=agent_def.specialization or "general_computation"
                )
            kernel.register_agent(agent)

        return kernel, env

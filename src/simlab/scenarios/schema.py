"""Declarative Scenario Configuration Schemas."""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class TaskDefinition(BaseModel):
    """Task item in a scenario."""
    task_id: str
    name: str
    difficulty: str = "MODERATE"
    complexity_weight: float = 1.0
    energy_cost: float = 10.0
    status: str = "PENDING"
    requirements: Dict[str, Any] = Field(default_factory=dict)


class AgentDefinition(BaseModel):
    """Agent declaration in scenario."""
    agent_id: str
    role: str
    capabilities: List[str] = Field(default_factory=list)
    specialization: Optional[str] = None
    managed_workers: Optional[List[str]] = None


class FaultConfig(BaseModel):
    """Fault injection configuration."""
    message_loss_rate: float = 0.0
    message_delay_ticks: int = 0
    agent_timeouts: Dict[str, int] = Field(default_factory=dict)
    corrupted_tasks: List[str] = Field(default_factory=list)


class ScenarioConfig(BaseModel):
    """Authoritative scenario definition model."""
    scenario_id: str
    name: str
    description: str = ""
    max_ticks: int = 50
    initial_energy: float = 100.0
    initial_bandwidth: float = 100.0
    initial_budget: float = 50.0
    tasks: List[TaskDefinition] = Field(default_factory=list)
    agents: List[AgentDefinition] = Field(default_factory=list)
    faults: Optional[FaultConfig] = None

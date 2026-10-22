"""Heterogeneous Multi-Agent Routing Benchmark Suite."""

from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional


class RoutingPolicy(str, Enum):
    """Multi-agent task routing policies."""
    BROADCAST_ALL = "BROADCAST_ALL"
    CAPABILITY_MATCH = "CAPABILITY_MATCH"
    HIERARCHICAL_COORDINATOR = "HIERARCHICAL_COORDINATOR"


@dataclass
class HeteroTask:
    """Benchmark task for heterogeneous agent routing."""
    task_id: str
    name: str
    domain: str
    complexity: str
    required_capability: str
    base_tokens: int
    optimal_agents: int = 1


BUILTIN_HETERO_TASKS: List[HeteroTask] = [
    HeteroTask("het_01", "SQL Schema Ingestion", "DATA", "SIMPLE", "data_engineering", 450, 1),
    HeteroTask("het_02", "Recursive Vector Indexing", "DATA", "MODERATE", "data_engineering", 850, 1),
    HeteroTask("het_03", "Regex Parser Implementation", "CODE", "MODERATE", "code_synthesis", 950, 1),
    HeteroTask("het_04", "Cryptographic Hash Audit", "SECURITY", "COMPLEX", "contract_validation", 1200, 2),
    HeteroTask("het_05", "Dynamic Simplex Optimizer", "MATH", "COMPLEX", "math_algorithms", 1400, 1),
    HeteroTask("het_06", "Independent Review & AST Lint", "SECURITY", "MODERATE", "contract_validation", 750, 1),
]


class RoutingBenchmarkRunner:
    """Evaluates multi-agent routing policies on token efficiency, latency, and throughput."""

    def __init__(self, tasks: Optional[List[HeteroTask]] = None):
        self.tasks = list(tasks or BUILTIN_HETERO_TASKS)

    def evaluate_policy(self, policy: RoutingPolicy, agent_count: int = 3) -> Dict[str, Any]:
        """Simulate and measure token and coordination costs under specified policy."""
        total_tokens = 0
        total_coordination_overhead = 0
        successful_assignments = 0

        for task in self.tasks:
            if policy == RoutingPolicy.BROADCAST_ALL:
                # All agents process every task -> tokens = agent_count * base_tokens
                task_tokens = task.base_tokens * agent_count
                coord_tokens = 150 * (agent_count - 1)  # redundant consensus tax
                total_tokens += (task_tokens + coord_tokens)
                total_coordination_overhead += coord_tokens
                successful_assignments += 1

            elif policy == RoutingPolicy.CAPABILITY_MATCH:
                # Directly dispatched to single specialist
                task_tokens = task.base_tokens
                total_tokens += task_tokens
                successful_assignments += 1

            elif policy == RoutingPolicy.HIERARCHICAL_COORDINATOR:
                # Dispatched via coordinator (100 token triage tax)
                coord_tax = 120
                task_tokens = task.base_tokens + coord_tax
                total_tokens += task_tokens
                total_coordination_overhead += coord_tax
                successful_assignments += 1

        avg_tokens_per_task = total_tokens / len(self.tasks) if self.tasks else 0.0

        return {
            "policy": policy.value,
            "agent_count": agent_count,
            "tasks_evaluated": len(self.tasks),
            "total_tokens_consumed": total_tokens,
            "average_tokens_per_task": avg_tokens_per_task,
            "coordination_overhead_tokens": total_coordination_overhead,
            "overhead_percentage": (total_coordination_overhead / total_tokens * 100.0) if total_tokens > 0 else 0.0,
            "success_rate": successful_assignments / len(self.tasks) if self.tasks else 0.0
        }

    def compare_all_policies(self, agent_count: int = 3) -> List[Dict[str, Any]]:
        """Run all routing policies and produce comparative benchmark matrix."""
        return [
            self.evaluate_policy(RoutingPolicy.BROADCAST_ALL, agent_count=agent_count),
            self.evaluate_policy(RoutingPolicy.HIERARCHICAL_COORDINATOR, agent_count=agent_count),
            self.evaluate_policy(RoutingPolicy.CAPABILITY_MATCH, agent_count=agent_count),
        ]

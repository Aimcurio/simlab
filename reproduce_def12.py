"""Minimal failing reproduction for DEF-12 mathematical correctness defect."""

import sys
from simlab.core.kernel import SimulationKernel
from simlab.agents.coordinator import CoordinatorAgent
from simlab.agents.worker import WorkerAgent
from simlab.agents.critic import CriticAgent
from simlab.environment.cooperative_task import CooperativeTaskEnvironment

def reproduce():
    tasks = [
        {
            "task_id": "def12_cos_zero",
            "name": "Orthogonal Cosine Similarity",
            "status": "PENDING",
            "requirements": {
                "operation": "cosine_similarity",
                "vec_a": [1.0, 0.0],
                "vec_b": [0.0, 1.0]
            }
        },
        {
            "task_id": "def12_anom_zero",
            "name": "Zero Anomaly Count",
            "status": "PENDING",
            "requirements": {
                "operation": "anomaly_count",
                "inputs": [10.0, 10.0, 10.0],
                "threshold": 2.0
            }
        },
        {
            "task_id": "def12_delta_zero",
            "name": "Zero Coordinate Delta",
            "status": "PENDING",
            "requirements": {
                "operation": "delta",
                "start": 15.5,
                "end": 15.5
            }
        }
    ]

    kernel = SimulationKernel(seed=42)
    env = CooperativeTaskEnvironment(tasks=tasks, initial_energy=200.0, energy_cost_per_task=5.0)
    env.attach_to_kernel(kernel)

    kernel.register_agent(CoordinatorAgent("coordinator", ["worker_1"]))
    kernel.register_agent(WorkerAgent("worker_1"))
    kernel.register_agent(CriticAgent("critic"))

    res = kernel.run(max_ticks=30)
    print(f"Simulation completed: {res.is_completed}")
    print(f"Termination reason: {res.termination_reason}")

    task_map = {t["task_id"]: t for t in env.state.get("tasks")}
    failures = []
    for tid, exp in [("def12_cos_zero", 0.0), ("def12_anom_zero", 0), ("def12_delta_zero", 0.0)]:
        t = task_map[tid]
        actual = t.get("result_value")
        status = t.get("status")
        print(f"Task {tid}: status={status}, result_value={actual}, expected={exp}")
        if actual != exp:
            failures.append((tid, actual, exp))

    if failures:
        print(f"\nDEF-12 REPRODUCED: {len(failures)} tasks substituted/corrupted: {failures}")
        return 1
    else:
        print("\nAll tasks computed and approved correctly.")
        return 0

if __name__ == "__main__":
    sys.exit(reproduce())

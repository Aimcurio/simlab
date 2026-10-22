"""Tests for Coding and Routing Benchmarks."""

import pytest
from simlab.benchmarks import (
    CodingBenchmarkRunner,
    RoutingBenchmarkRunner,
    RoutingPolicy,
    BUILTIN_CODING_TASKS,
    BUILTIN_HETERO_TASKS,
)


def test_coding_benchmark_suite_reference_solutions():
    runner = CodingBenchmarkRunner()
    results = runner.run_suite()

    assert results["total_tasks"] == len(BUILTIN_CODING_TASKS)
    assert results["passed_tasks"] == len(BUILTIN_CODING_TASKS)
    assert results["pass_rate"] == 1.0


def test_coding_benchmark_suite_failing_candidate():
    runner = CodingBenchmarkRunner()
    # Provide bad solution for two_sum
    bad_solutions = {"code_01_two_sum": "def two_sum(n, t): return [999, 999]"}
    res = runner.evaluate_solution(BUILTIN_CODING_TASKS[0], bad_solutions["code_01_two_sum"])

    assert res["passed"] is False
    assert res["exit_code"] != 0 or "AssertionError" in res.stderr


def test_routing_benchmark_comparisons():
    runner = RoutingBenchmarkRunner()
    comparisons = runner.compare_all_policies(agent_count=3)

    assert len(comparisons) == 3
    broadcast = comparisons[0]
    coordinator = comparisons[1]
    capability = comparisons[2]

    # Capability matching must use fewer tokens than full broadcast
    assert capability["total_tokens_consumed"] < broadcast["total_tokens_consumed"]
    # Capability matching has zero broadcast coordination tax
    assert capability["coordination_overhead_tokens"] == 0
    assert broadcast["coordination_overhead_tokens"] > 0

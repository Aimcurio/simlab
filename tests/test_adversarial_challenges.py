"""Adversarial Challenge Script for SimLab Benchmarks, Governance, and Sandbox.

Explicitly challenges:
1. Benchmark Validity: Failure detection, edge cases, output truncation, syntax errors.
2. Governance Enforcement: Tier separation, lifecycle locking, fail-closed corrupted configs, destructive blocks.
3. Sandbox Security: Process boundary isolation, credential scrubbing, timeout enforcement, subprocess exit codes.
"""

import os
import sys
from pathlib import Path
import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from simlab.benchmarks.coding import CodingBenchmarkRunner, BUILTIN_CODING_TASKS
from simlab.benchmarks.routing import RoutingBenchmarkRunner
from simlab.governance.permissions import OperationTier, SimLabAuthorizationError
from simlab.governance.firewall import GovernanceManager
from simlab.isolation import SubprocessSandbox


def test_challenge_coding_benchmark_catches_wrong_solution():
    runner = CodingBenchmarkRunner()
    task = BUILTIN_CODING_TASKS[0]  # Two Sum
    wrong_solution = "def two_sum(nums, target): return [0, 0]"
    res = runner.evaluate_solution(task, wrong_solution)
    assert res["passed"] is False, "Benchmark failed to detect incorrect solution"
    assert res["exit_code"] != 0 or "AssertionError" in res["stderr"]


def test_challenge_coding_benchmark_catches_syntax_error():
    runner = CodingBenchmarkRunner()
    task = BUILTIN_CODING_TASKS[0]
    syntax_error_code = "def two_sum(nums, target) return broken"
    res = runner.evaluate_solution(task, syntax_error_code)
    assert res["passed"] is False
    assert "SyntaxError" in res["stderr"]


def test_challenge_coding_benchmark_timeout_enforcement():
    runner = CodingBenchmarkRunner(sandbox=SubprocessSandbox(timeout_seconds=0.5))
    task = BUILTIN_CODING_TASKS[1]
    infinite_loop_code = "def is_palindrome(s):\n    while True: pass\n"
    res = runner.evaluate_solution(task, infinite_loop_code)
    assert res["passed"] is False
    assert res["timed_out"] is True


def test_challenge_sandbox_scrubs_sensitive_credentials():
    os.environ["OPENAI_API_KEY"] = "sk-super-secret-key-12345"
    os.environ["SIMLAB_SECRET"] = "do-not-leak-this-token"
    try:
        sandbox = SubprocessSandbox()
        leak_test_code = """
import os
assert 'OPENAI_API_KEY' not in os.environ, 'Leaked OPENAI_API_KEY!'
assert 'SIMLAB_SECRET' not in os.environ, 'Leaked SIMLAB_SECRET!'
print('SCRUB_SUCCESS')
"""
        res = sandbox.run_code(leak_test_code)
        assert res.is_success is True
        assert "SCRUB_SUCCESS" in res.stdout
    finally:
        os.environ.pop("OPENAI_API_KEY", None)
        os.environ.pop("SIMLAB_SECRET", None)


def test_challenge_sandbox_output_truncation_bound():
    sandbox = SubprocessSandbox(max_output_bytes=2048)
    bomb_code = "print('A' * 500000)"
    res = sandbox.run_code(bomb_code)
    assert res.output_truncated is True
    assert len(res.stdout) < 4096
    assert "[OUTPUT TRUNCATED: EXCEEDED BOUND]" in res.stdout


def test_challenge_governance_blocks_destructive_operations():
    gm = GovernanceManager()
    with pytest.raises(SimLabAuthorizationError) as exc_info:
        gm.check_authorization(OperationTier.RESTRICTED_DESTRUCTIVE, "DELETE_HISTORICAL_EVIDENCE")
    assert "destructive" in str(exc_info.value).lower()


def test_challenge_governance_corrupt_config_fails_closed():
    bad_config = {"canonical_lifecycle_state": "BOGUS_CORRUPT_STATE"}
    gm = GovernanceManager()
    with pytest.raises(SimLabAuthorizationError):
        gm.verify_operation(OperationTier.AUTHORIZED_EMPIRICAL_EXPERIMENT, "OP", config_override=bad_config)


def test_challenge_routing_benchmark_heterogeneous_boundaries():
    runner = RoutingBenchmarkRunner()
    # Test boundary with agent_count = 1
    res_1 = runner.compare_all_policies(agent_count=1)
    assert len(res_1) == 3
    # Test boundary with agent_count = 10
    res_10 = runner.compare_all_policies(agent_count=10)
    assert len(res_10) == 3
    # Broadcast policy should show much higher token consumption for 10 agents than 1 agent
    bc_1 = [r for r in res_1 if r["policy"] == "BROADCAST_ALL"][0]
    bc_10 = [r for r in res_10 if r["policy"] == "BROADCAST_ALL"][0]
    assert bc_10["total_tokens_consumed"] > bc_1["total_tokens_consumed"]

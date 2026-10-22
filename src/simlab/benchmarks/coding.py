"""Executable Coding Benchmark with Sandboxed Unit Test Validation."""

import json
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from simlab.isolation import SubprocessSandbox, ExecutionResult


@dataclass
class CodingTask:
    """Individual coding problem with executable test suite."""
    task_id: str
    name: str
    category: str
    difficulty: str
    prompt: str
    test_suite_code: str
    reference_solution: str


# Real executable benchmark tasks
BUILTIN_CODING_TASKS: List[CodingTask] = [
    CodingTask(
        task_id="code_01_two_sum",
        name="Two Sum Problem",
        category="arrays",
        difficulty="EASY",
        prompt="Write a function `two_sum(nums, target)` that returns indices of the two numbers such that they add up to target.",
        reference_solution="""
def two_sum(nums, target):
    seen = {}
    for i, num in enumerate(nums):
        diff = target - num
        if diff in seen:
            return [seen[diff], i]
        seen[num] = i
    return []
""",
        test_suite_code="""
assert two_sum([2, 7, 11, 15], 9) == [0, 1]
assert two_sum([3, 2, 4], 6) == [1, 2]
assert two_sum([3, 3], 6) == [0, 1]
print("PASS: all test cases succeeded")
"""
    ),
    CodingTask(
        task_id="code_02_palindrome",
        name="Valid Palindrome",
        category="strings",
        difficulty="EASY",
        prompt="Write a function `is_palindrome(s)` that returns True if alphanumeric characters form a palindrome.",
        reference_solution="""
def is_palindrome(s):
    cleaned = [c.lower() for c in s if c.isalnum()]
    return cleaned == cleaned[::-1]
""",
        test_suite_code="""
assert is_palindrome("A man, a plan, a canal: Panama") == True
assert is_palindrome("race a car") == False
assert is_palindrome(" ") == True
assert is_palindrome("0P") == False
print("PASS: all test cases succeeded")
"""
    ),
    CodingTask(
        task_id="code_03_merge_intervals",
        name="Merge Overlapping Intervals",
        category="algorithms",
        difficulty="MEDIUM",
        prompt="Write a function `merge_intervals(intervals)` that merges all overlapping intervals.",
        reference_solution="""
def merge_intervals(intervals):
    if not intervals:
        return []
    intervals.sort(key=lambda x: x[0])
    merged = [intervals[0]]
    for current in intervals[1:]:
        prev = merged[-1]
        if current[0] <= prev[1]:
            prev[1] = max(prev[1], current[1])
        else:
            merged.append(current)
    return merged
""",
        test_suite_code="""
assert merge_intervals([[1,3],[2,6],[8,10],[15,18]]) == [[1,6],[8,10],[15,18]]
assert merge_intervals([[1,4],[4,5]]) == [[1,5]]
assert merge_intervals([]) == []
assert merge_intervals([[1,4],[2,3]]) == [[1,4]]
print("PASS: all test cases succeeded")
"""
    ),
    CodingTask(
        task_id="code_04_rpn_evaluator",
        name="Reverse Polish Notation Evaluator",
        category="stacks",
        difficulty="MEDIUM",
        prompt="Write a function `eval_rpn(tokens)` evaluating the value of an arithmetic expression in Reverse Polish Notation.",
        reference_solution="""
def eval_rpn(tokens):
    stack = []
    for token in tokens:
        if token in ("+", "-", "*", "/"):
            b = stack.pop()
            a = stack.pop()
            if token == "+": stack.append(a + b)
            elif token == "-": stack.append(a - b)
            elif token == "*": stack.append(a * b)
            elif token == "/": stack.append(int(a / b))
        else:
            stack.append(int(token))
    return stack[0]
""",
        test_suite_code="""
assert eval_rpn(["2", "1", "+", "3", "*"]) == 9
assert eval_rpn(["4", "13", "5", "/", "+"]) == 6
assert eval_rpn(["10", "6", "9", "3", "+", "-11", "*", "/", "*", "17", "+", "5", "+"]) == 22
print("PASS: all test cases succeeded")
"""
    )
]


class CodingBenchmarkRunner:
    """Executes coding benchmarks in isolated sandboxes and collects pass-rate metrics."""

    def __init__(self, sandbox: Optional[SubprocessSandbox] = None):
        self.sandbox = sandbox or SubprocessSandbox(timeout_seconds=3.0)

    def evaluate_solution(self, task: CodingTask, candidate_solution_code: str) -> Dict[str, Any]:
        """Execute candidate code alongside task unit test harness in sandbox."""
        full_script = f"{candidate_solution_code}\n\n{task.test_suite_code}"
        res = self.sandbox.run_code(full_script)

        passed = res.is_success and "PASS: all test cases succeeded" in res.stdout
        return {
            "task_id": task.task_id,
            "name": task.name,
            "category": task.category,
            "difficulty": task.difficulty,
            "passed": passed,
            "exit_code": res.exit_code,
            "timed_out": res.timed_out,
            "duration_ms": res.duration_ms,
            "stdout": res.stdout.strip(),
            "stderr": res.stderr.strip()
        }

    def run_suite(self, solutions: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        Evaluate full benchmark suite. If solutions dict is None,
        evaluates reference solutions.
        """
        results = []
        for task in BUILTIN_CODING_TASKS:
            code = (solutions or {}).get(task.task_id, task.reference_solution)
            eval_res = self.evaluate_solution(task, code)
            results.append(eval_res)

        total = len(results)
        passed = sum(1 for r in results if r["passed"])
        pass_rate = passed / total if total > 0 else 0.0

        return {
            "total_tasks": total,
            "passed_tasks": passed,
            "total": total,
            "passed": passed,
            "pass_rate": pass_rate,
            "results": results
        }

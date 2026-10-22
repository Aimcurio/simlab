"""Tests for Subprocess Sandbox and Execution Isolation."""

import os
import pytest
from simlab.isolation import SubprocessSandbox


def test_sandbox_successful_execution():
    box = SubprocessSandbox(timeout_seconds=2.0)
    code = "print('SimLab Sandbox Verified!')\nimport math\nprint(math.sqrt(16))"
    res = box.run_code(code)

    assert res.is_success is True
    assert "SimLab Sandbox Verified!" in res.stdout
    assert "4.0" in res.stdout
    assert res.exit_code == 0
    assert res.timed_out is False


def test_sandbox_timeout_enforcement():
    box = SubprocessSandbox(timeout_seconds=0.5)
    # Infinite loop
    code = "import time\nwhile True:\n    time.sleep(0.01)"
    res = box.run_code(code)

    assert res.is_success is False
    assert res.timed_out is True
    assert res.exit_code == -1
    assert "timed out" in res.stderr.lower()


def test_sandbox_output_truncation():
    # Max output 1024 bytes
    box = SubprocessSandbox(timeout_seconds=2.0, max_output_bytes=1024)
    # Print 5000 chars
    code = "print('X' * 5000)"
    res = box.run_code(code)

    assert res.is_success is True
    assert res.output_truncated is True
    assert len(res.stdout) <= 1200
    assert "[OUTPUT TRUNCATED" in res.stdout


def test_sandbox_environment_sanitization():
    box = SubprocessSandbox(timeout_seconds=2.0)
    # Set fake secret in host env
    os.environ["OPENAI_API_KEY"] = "sk-fake-secret-12345"

    code = "import os\nprint('KEY_IN_CHILD:', os.environ.get('OPENAI_API_KEY'))"
    res = box.run_code(code)

    assert "KEY_IN_CHILD: None" in res.stdout

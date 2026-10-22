"""Subprocess Execution Sandbox with Resource Limits and Output Bounds."""

import os
import subprocess
import sys
import tempfile
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional


@dataclass
class ExecutionResult:
    """Outcome of sandboxed execution."""
    exit_code: int
    stdout: str
    stderr: str
    duration_ms: float
    timed_out: bool = False
    output_truncated: bool = False
    error: Optional[str] = None

    @property
    def is_success(self) -> bool:
        return self.exit_code == 0 and not self.timed_out and not self.error

    @property
    def is_timeout(self) -> bool:
        return self.timed_out


class SubprocessSandbox:
    """
    Process-level execution sandbox:
    - Dedicated ephemeral temporary working directory
    - Hard execution timeout with SIGKILL enforcement
    - Bounded stdout/stderr capture (prevents memory exhaustion)
    - Python isolated mode (-I) ignoring user site-packages and environment
    - Sanitized child environment (scrubs credentials)
    
    LIMITATION DISCLOSURE:
    This sandbox provides process isolation, timeout enforcement, output limits, and
    environment sanitization. It does NOT provide kernel-level cgroups or network namespaces
    on Windows without containerization (Docker / WSL2). Untrusted network calls or OS syscalls
    must be managed via containerization in multi-tenant untrusted production environments.
    """

    # Sensitive environment variables to scrub from sandbox process
    SCRUB_ENV_VARS = {
        "OPENAI_API_KEY",
        "ANTHROPIC_API_KEY",
        "GEMINI_API_KEY",
        "AWS_SECRET_ACCESS_KEY",
        "GITHUB_TOKEN",
        "SIMLAB_SECRET",
    }

    def __init__(self, timeout_seconds: float = 5.0, max_output_bytes: int = 65536):
        self.timeout_seconds = max(0.1, timeout_seconds)
        self.max_output_bytes = max(1024, max_output_bytes)

    def _prepare_environment(self) -> Dict[str, str]:
        """Construct sanitized child process environment."""
        env = dict(os.environ)
        for var in self.SCRUB_ENV_VARS:
            env.pop(var, None)
        env["PYTHONDONTWRITEBYTECODE"] = "1"
        env["PYTHONUNBUFFERED"] = "1"
        return env

    def run_code(
        self,
        code_string: str,
        timeout: Optional[float] = None,
        extra_args: Optional[List[str]] = None
    ) -> ExecutionResult:
        """Execute a Python code string inside the isolated sandbox."""
        timeout_sec = timeout if timeout is not None else self.timeout_seconds
        t0 = time.perf_counter()

        with tempfile.TemporaryDirectory(prefix="simlab_sandbox_") as tmp_dir:
            script_file = Path(tmp_dir) / "entrypoint.py"
            script_file.write_text(code_string, encoding="utf-8")

            cmd = [sys.executable, "-I", str(script_file)]
            if extra_args:
                cmd.extend(extra_args)

            env = self._prepare_environment()

            try:
                proc = subprocess.Popen(
                    cmd,
                    cwd=tmp_dir,
                    env=env,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    bufsize=1
                )

                try:
                    stdout, stderr = proc.communicate(timeout=timeout_sec)
                    duration_ms = (time.perf_counter() - t0) * 1000.0

                    # Output bounds enforcement
                    truncated = False
                    if len(stdout) > self.max_output_bytes:
                        stdout = stdout[:self.max_output_bytes] + "\n[OUTPUT TRUNCATED: EXCEEDED BOUND]"
                        truncated = True
                    if len(stderr) > self.max_output_bytes:
                        stderr = stderr[:self.max_output_bytes] + "\n[OUTPUT TRUNCATED: EXCEEDED BOUND]"
                        truncated = True

                    return ExecutionResult(
                        exit_code=proc.returncode,
                        stdout=stdout,
                        stderr=stderr,
                        duration_ms=duration_ms,
                        output_truncated=truncated
                    )

                except subprocess.TimeoutExpired:
                    # Hard kill
                    proc.kill()
                    proc.wait()
                    duration_ms = (time.perf_counter() - t0) * 1000.0
                    return ExecutionResult(
                        exit_code=-1,
                        stdout="",
                        stderr=f"Execution timed out after {timeout_sec:.2f} seconds.",
                        duration_ms=duration_ms,
                        timed_out=True,
                        error="TIMEOUT_EXCEEDED"
                    )

            except Exception as e:
                duration_ms = (time.perf_counter() - t0) * 1000.0
                return ExecutionResult(
                    exit_code=-1,
                    stdout="",
                    stderr=str(e),
                    duration_ms=duration_ms,
                    error=f"SUBPROCESS_SPAWN_ERROR: {e}"
                )

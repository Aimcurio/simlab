# SimLab Invariants & Guidelines

See authoritative rules in [AGENTS.md](file:///E:/projects/simlab/AGENTS.md).

Key Invariants:
1. Multi-tier governance: Keep local dev/tests separate from authorized empirical sweeps.
2. Determinism: Never use `uuid.uuid4()` for message or event IDs. Use composite deterministic sequence IDs.
3. Causal integrity: Always deep-copy event inputs/outcomes before hashing and storing.
4. Normalization: Zero-variance `min_max_norm` maps to 0.0 baseline, not 1.0.
5. Telemetry: Write atomically with `.tmp` + `os.fsync` + `os.replace`.
6. Sandboxing: Run untrusted benchmarks inside `SubprocessSandbox` with timeouts and scrubbed env.
7. Paths: Dynamic path resolution via `Path(__file__)`, no hardcoded drive letters.

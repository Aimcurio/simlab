# SimLab / Curo Operating Guidelines & Invariants

This document codifies the verified engineering invariants, governance boundaries, and architectural patterns established during the SimLab / Curo recovery and implementation. All agents operating in this repository MUST observe these rules.

---

## 1. Governance & Authorization Invariants

- **Multi-Tier Authority Separation**:
  - Always separate execution authority into discrete operational tiers (`simlab.governance.permissions.OperationTier`):
    - `READ_ONLY_ANALYSIS`: Unrestricted.
    - `LOCAL_DEV_TEST`: Unrestricted (unit tests, CLI sanity checks, local package operations).
    - `DETERMINISTIC_MOCK_EXPERIMENT`: Permitted with offline rule-based backends (`--mock`).
    - `AUTHORIZED_EMPIRICAL_EXPERIMENT`: Gated fail-closed pending formal requester ratification in `GOVERNANCE.json`.
    - `EXTERNAL_MODEL_NETWORK`: Gated fail-closed unless `execution_firewall.live_api_calls_permitted` is `True`.
    - `RESTRICTED_DESTRUCTIVE`: Prohibited unconditionally on historical evidence.
- **Fail-Closed Governance Integrity**:
  - Never rewrite `GOVERNANCE.json` or disable `governance_firewall.py` to bypass execution blocks.
  - Development, linting, packaging, and unit testing must never depend on external research grants.

---

## 2. Determinism & Causal Logging Invariants

- **Zero Non-Deterministic Identifiers in Traceable State**:
  - **NEVER** use `uuid.uuid4()` or random token generators to construct message IDs, event IDs, or simulation artifacts that enter the event queue or logger.
  - Message IDs MUST be deterministically constructed from simulation coordinates:
    `f"msg_{sender_id}_{recipient_id}_t{current_tick}_{sequence_id:04d}"`
  - Event IDs MUST be deterministically constructed:
    `f"evt_{tick:05d}_{sequence_counter:05d}"`
- **Deep-Copy Event Snapshots**:
  - In `CausalEventLogger.log_event()`, **ALWAYS** deep-copy inputs, outcomes, and state snapshots (`json.loads(json.dumps(obj, default=str))`) prior to calculating SHA-256 hashes.
  - Passing live dictionary references allows later in-place mutations (e.g. task completion flags) to silently corrupt previously sealed event digests, causing replay verification failures.

---

## 3. Mathematical & Scoring Invariants

- **Zero-Variance Normalization Handling**:
  - In feature scaling (`min_max_norm`), when `max == min` (zero variance across candidates), return a neutral baseline (`0.0`), **NEVER** `1.0`.
  - Normalizing uniform arrays to `1.0` falsely boosts uninformative components (e.g. uniform importance or zero similarity) into dominating tri-factor retrieval rank.
- **Defensive Target Indexing**:
  - In ranking and retrieval evaluations, never assume query targets are present in candidate lists (`candidates.index(target)`). Always perform defensive lookups with an out-of-bounds rank fallback (`len(candidates) + 1`).

---

## 4. Telemetry Persistence & Atomicity

- **Crash-Resilient File Writes**:
  - All telemetry manifests, results JSON files, and event streams MUST be written using `AtomicTelemetryWriter`:
    1. Write to a temporary file (`.tmp`) on the same filesystem/drive.
    2. Flush application buffers (`f.flush()`).
    3. Force disk synchronization (`os.fsync(f.fileno())`).
    4. Atomically swap into place via `os.replace()`.
  - Never perform raw, unbuffered streaming writes directly to destination files.

---

## 5. Execution Sandboxing & Security

- **Process Isolation for Benchmarks**:
  - All untrusted or candidate code evaluation must execute inside `SubprocessSandbox`.
  - The sandbox must enforce:
    - Dedicated ephemeral temporary working directories.
    - Hard timeouts via SIGKILL / process termination (`timeout_seconds`).
    - Bounded stdout/stderr capture buffers to prevent memory exhaustion.
    - Scrubbed environment variables (stripping API keys, credentials, and tokens).
    - Isolated Python invocation (`python -I`).

---

## 6. Path Portability & Dependency Hygiene

- **Dynamic Path Resolution**:
  - Never hardcode host-specific drive paths (e.g. `r"E:\projects\simlab\..."` or `C:\Users\...`).
  - Always resolve roots dynamically:
    `Path(__file__).resolve().parents[...]`
  - Respect runtime environment overrides: `SIMLAB_GOVERNANCE_PATH`, `SIMLAB_RUNS_DIR`.

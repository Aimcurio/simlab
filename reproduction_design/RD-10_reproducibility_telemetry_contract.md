# RD-10: Reproducibility & Telemetry Contract
**Project**: Persistent 25+ Agent Simulation Laboratory  
**Phase**: Phase 2 — Reproduction Design (`REPRODUCTION_DESIGN`)  
**Authority State**: `ARCHITECTURE_STATUS = UNFROZEN` | `IMPLEMENTATION_AUTHORITY = NOT_GRANTED` | `EXPERIMENT_EXECUTION_AUTHORITY = NOT_GRANTED`  

---

## 1. 10-Point Run Reproducibility Contract

Every reproduction experiment designed in SimLab Phase 2 must fulfill all ten provenance and configuration tracking invariants before execution is authorized:

```
+----------------------------------------------------------------------------------------------------+
|                                    10-POINT REPRODUCIBILITY CONTRACT                               |
+----------------------------------------------------------------------------------------------------+
| 1. Seed Strategy             | Deterministic PRNG seeds recorded for sampling, order, and models   |
| 2. Configuration Snapshot    | Full JSON/YAML snapshot of all hyperparameters and environment flags |
| 3. Model Identifier          | Exact model snapshot ID pinned (e.g. gpt-4o-2024-08-06, never gpt-4o) |
| 4. Prompt Hash               | SHA-256 cryptographic digest of every system and user prompt string |
| 5. Dataset Version           | Pinned dataset commit hash and SHA-256 file manifest                |
| 6. Code Revision             | Clean Git commit hash of experiment harness (zero uncommitted diff) |
| 7. Environment Revision      | Docker container digest or locked requirements.txt (pinned hashes)   |
| 8. Reference Timestamp       | ISO-8601 UTC timestamp of run initiation and completion             |
| 9. Raw Output Retention      | 100% complete raw API JSON responses saved to immutable storage      |
| 10. Metric Script Revision   | SHA-256 digest of metric computation script version                 |
+----------------------------------------------------------------------------------------------------+
```

---

## 2. Standardized Telemetry Data Schema

All future Phase 3 execution harnesses must emit structured telemetry adhering to the following unified JSONL schema:

```json
{
  "$schema": "https://curo.simlab.internal/schemas/v2/telemetry_event.json",
  "experiment_id": "EXP-RP02-COMPUTE-MATCHED-V1",
  "run_id": "run-20260916-0012-rp02",
  "timestamp_utc": "2026-09-16T10:15:30.123Z",
  "condition": "T-Debate",
  "task_id": "task-mystery-042",
  "turn_index": 2,
  "agent_id": "agent_critic",
  "model_identifier": "gpt-4o-2024-08-06",
  "prompt_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
  "input_tokens": 1420,
  "output_tokens": 312,
  "cached_tokens": 0,
  "latency_ms": 1845,
  "response_status": "SUCCESS",
  "timeout_type": "NONE",
  "vote_distribution": {"Option_A": 3, "Option_B": 3},
  "tie_broken": true,
  "tie_breaking_method": "LOGPROB",
  "zero_data_retention": true,
  "tool_invocations": [],
  "raw_response_path": "telemetry/raw/run-20260916-0012-rp02/call-002.json"
}
```

---

## 3. Replay Harness, Data Governance & Determinism Validation

1. **Static Replay**: Telemetry records must contain sufficient data to replay the experiment offline without network or API access, verifying metric calculation idempotency.
2. **Zero Data Retention (ZDR) Mandate**: All API requests must send `store: false` to ensure commercial providers do not retain evaluation prompts for model retraining or benchmark contamination.
3. **Re-Run Variance Bounding**: For stochastic LLM calls ($T=0.7$), re-running an identical seed across independent sessions must produce results whose aggregate mean metric falls within a pre-defined tolerance band ($\pm 3\%$) attributable to provider-side GPU non-determinism.

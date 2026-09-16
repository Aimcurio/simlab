# PX-06: Raw Evidence Manifest
**Project**: Persistent 25+ Agent Simulation Laboratory (Curo SimLab)  
**Lifecycle State**: `RESULT_ANALYSIS`  
**Evidence Immutability**: All artifacts locked with SHA-256 cryptographic digests.  

---

## 1. Immutable Raw Telemetry & Dataset Manifest

| Artifact Type | File Path | File Size (Bytes) | Event Count | SHA-256 Checksum |
|---|---|---|---|---|
| **Dataset (RP-01)** | `SimLab_MemBench_500.json` | ~45,000 | 500 records | `97cba94e14b4ada840141ee34f153c76a3939a20924ea60caae5b015d5ded800` |
| **Telemetry (RP-01)**| `telemetry/rp01/rp01_raw_telemetry.jsonl` | ~82,400 | 400 events | `c2b967ea83b668d9b31421141c7038cf45fc41c604eb60976cb02f43c56dbb59` |
| **Dataset (RP-03)** | `SimLab_CodeSOP_50.json` | ~6,200 | 50 tasks | `692044615497aecf0b9b22cd1996d14f1d082e39ee5ad8ae236164329d1ac097` |
| **Telemetry (RP-03)**| `telemetry/rp03/rp03_raw_telemetry.jsonl` | ~38,500 | 150 events | `e4a7ef3d0b35318321004a34ce46b74610bc7ff30693096ebe090d7fc99a1487` |
| **Telemetry (RP-02)**| `telemetry/rp02/rp02_raw_telemetry.jsonl` | ~165,000 | 800 events | `3a5585b467ec6a6d630bb39b4b04d13bf07cbb3eb97c11f7c32bf28d0b2dc437` |
| **Dataset (RP-04)** | `SimLab_HeteroBench_100.json`| ~11,500 | 100 tasks | `af1a85d2386cd76d36e937db48b1c4362d941ce9eec1e1413d7404f535c45b94` |
| **Telemetry (RP-04)**| `telemetry/rp04/rp04_raw_telemetry.jsonl` | ~92,000 | 400 events | `5bc19a8e0f438a5b28d7a12b6dfc40a32490b63e8a71926c483d9b12a812e967` |

---

## 2. Provenance Chain & Integrity Assertion

All raw evidence files have been verified against git commit `8d7d8465b07c3b1c12c3748ce9f44c7051484daa`. Zero post-hoc modifications or manual edits have been made to telemetry records. All analytical findings in `PX-02` through `PX-05` are 100% reproducible from these raw files.

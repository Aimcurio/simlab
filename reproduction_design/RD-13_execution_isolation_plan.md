# RD-13: Execution Isolation Plan
**Project**: Persistent 25+ Agent Simulation Laboratory  
**Phase**: Phase 2 — Reproduction Design (`REPRODUCTION_DESIGN`)  
**Authority State**: `ARCHITECTURE_STATUS = UNFROZEN` | `IMPLEMENTATION_AUTHORITY = NOT_GRANTED` | `EXPERIMENT_EXECUTION_AUTHORITY = NOT_GRANTED`  

---

## 1. Hermetic Isolation Architecture

To guarantee that future Phase 3 reproduction experiments run without host system corruption, prompt/data contamination, non-deterministic drift, or uncontrolled network activity, all execution harnesses must adhere to the SimLab Hermetic Isolation Standard across five defensive layers:

```
+----------------------------------------------------------------------------------------------------+
|                                    HERMETIC ISOLATION ARCHITECTURE                                 |
+----------------------------------------------------------------------------------------------------+
| Layer 1: Container Boundary   | Rootless OCI (Podman/Docker) with gVisor (runsc) / seccomp profile |
| Layer 2: Process Sandbox      | In-container bubblewrap/nsjail (10s CPU, 512MB RAM, unshare-net)    |
| Layer 3: Network Firewall     | Egress strictly whitelisted to LLM APIs; store: false mandated     |
| Layer 4: Ephemeral Storage    | tmpfs mounts for workspace/memory; per-episode cryptographic wipe  |
| Layer 5: Deterministic PRNG   | SeedSequence, torch.manual_seed, PYTHONHASHSEED=0, API seed pin    |
+----------------------------------------------------------------------------------------------------+
```

---

## 2. Isolation Controls & Guardrails

### A. Container Boundary & Non-Privileged Execution
- **Rootless Execution**: Execution harnesses run strictly in rootless OCI containers (Podman or rootless Docker) under unprivileged UID/GID mappings.
- **Kernel Sandboxing (gVisor / seccomp)**: Containers execute under a gVisor (`runsc`) application kernel or a restrictive seccomp-bpf profile that intercepts and blocks dangerous system calls (`ptrace`, `sys_chroot`, `mount`, `reboot`, kernel module manipulation).
- **Prohibition of Privileged DinD and Socket Mounting**: Spawning nested Docker containers via `/var/run/docker.sock` or `--privileged` Docker-in-Docker is **STRICTLY FORBIDDEN**. Mounting the host Docker daemon socket breaks host boundary containment and constitutes an immediate critical security failure.

### B. In-Container Process Sandboxing for Dynamic Code Execution
Tasks requiring dynamic code execution (e.g. `RP-03` unit test execution, agent-generated script evaluation) run inside an isolated process jail within the container using `bubblewrap` (`bwrap`) or `nsjail`:
- **CPU & Wall-Clock Limits**: `RLIMIT_CPU=10s`, maximum wall-clock timeout $15\text{s}$.
- **Memory RSS Ceiling**: `RLIMIT_AS=512MB` resident memory limit.
- **Filesystem Isolation**: Read-only mounts for libraries (`/usr`, `/lib`), temporary read-write scratch on tmpfs (`/tmp`), zero access to repository source code or environment variables.
- **Network Unsharing**: Explicit `--unshare-net` completely disables loopback and external sockets for executed code.
- **Dropped Capabilities**: All Linux capabilities dropped (`CAP_SYS_ADMIN`, `CAP_NET_ADMIN`, etc.).

### C. Network Egress Restrictions & API Zero Data Retention
- **Whitelisted Endpoints Only**: Outbound network egress is restricted at the container firewall (iptables/nftables) strictly to authorized model provider domains:
  - `api.openai.com`
  - `generativelanguage.googleapis.com`
- **Blocked Egress**: All arbitrary outbound HTTP/HTTPS traffic, package index downloads, git clones, and external telemetry are dropped by default (`DROP ALL`).
- **Mandatory `store: false` (Zero Data Retention)**: All commercial model API requests **MUST** pass the `store: false` payload parameter and Enterprise Zero Data Retention (ZDR) request headers. This guarantees that evaluation prompts, synthetic reasoning traces, and ground-truth benchmark problems are never retained by model vendors or ingested into subsequent foundation model pre-training corpora (preventing `FM-12` Data Contamination).
- **Offline Mock Mode Requirement**: Every harness must provide an `--offline` CLI flag that intercepts network calls and serves cached, deterministic JSON responses from pre-recorded fixture runs.

### D. Deterministic Seed Pinning & PRNG State Management
To guarantee mathematical replayability in accordance with `NC-06` and `RD-10`, the execution harness enforces multi-tier PRNG seed pinning:
1. **Container Environment**: `PYTHONHASHSEED=0` is set in the container environment to ensure invariant dictionary and set iteration order across process launches.
2. **Master Seed Configuration**: A canonical master seed (`SIMLAB_MASTER_SEED=20260916`) is passed as a mandatory runtime argument.
3. **Hierarchical Seed Derivation**:
   ```python
   # Hierarchical entropy derivation for multi-agent episodes
   import numpy as np
   import torch
   import random

   def initialize_episode_seeds(master_seed: int, episode_idx: int, num_agents: int):
       ss = np.random.SeedSequence([master_seed, episode_idx])
       agent_seeds = ss.spawn(num_agents)
       
       # Pin global Python and Torch PRNGs
       random.seed(int(ss.generate_state(1)[0]))
       np.random.seed(int(ss.generate_state(1)[0]))
       torch.manual_seed(int(ss.generate_state(1)[0]))
       if torch.cuda.is_available():
           torch.cuda.manual_seed_all(int(ss.generate_state(1)[0]))
           torch.backends.cudnn.deterministic = True
           torch.backends.cudnn.benchmark = False
           
       return [int(s.generate_state(1)[0]) for s in agent_seeds]
   ```
4. **API Seed Parameter Pinning**: All supported LLM API requests must explicitly transmit the derived integer `seed` parameter (e.g. OpenAI `seed`), and assert that the response header `system_fingerprint` matches the registered experiment baseline (`FM-06`).

### E. Ephemeral Storage & Per-Episode Scratch Purging
- **Read-Only Codebase**: The SimLab repository and scenario fixtures are mounted read-only (`:ro`).
- **Scratch tmpfs Purge**: Runtime memory scratchpads, agent vector stores, and intermediate code patches reside exclusively on tmpfs (`/memory`, `/workspace/scratch`). At the completion of each episode, the tmpfs directory is cryptographically unlinked and reinitialized, guaranteeing zero cross-run state contamination (`NC-13`).
- **Telemetry Quarantine**: Emitted JSONL telemetry and execution traces write exclusively to `/output/telemetry`. No log or state file may write to the host filesystem outside the designated output directory.

### F. Cryptographic Dependency Pinning
All runtime dependencies are locked with full cryptographic SHA-256 hashes in `requirements.lock` via `uv export --frozen --hash` or `pip-compile --generate-hashes`. Container builds verify hashes prior to installation.

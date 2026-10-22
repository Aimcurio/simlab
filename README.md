# SimLab — Agent Simulation Laboratory

A controlled, reproducible, observable multi-agent experimentation platform.

## Overview
SimLab provides a discrete-event simulation kernel, deterministic execution, cognitive agent architectures, fault injection, causal event logging, and an interactive observatory for multi-agent systems research.

## Quickstart

### Installation
Install in editable development mode:
```bash
pip install -e .
```

To include interactive observatory and test tools:
```bash
pip install -e ".[dev,ui]"
```

### Verification & Health Check
Verify your environment and dependencies:
```bash
simlab doctor
```

Run test suite:
```bash
pytest
```

### Running Experiments
List available scenarios:
```bash
simlab scenarios
```

Run a standard cooperative problem-solving experiment:
```bash
simlab run --scenario cooperative_pipeline --seed 42
```

Run an experiment with injected faults (e.g., 20% message drop and 2-tick delay):
```bash
simlab run --scenario resource_crisis --seed 42 --fault-loss 0.2 --fault-delay 2
```

Compare agent policies (e.g., Single-Agent vs Cooperative Team vs Critic-Reviewed):
```bash
simlab experiments run-comparative --scenario cooperative_pipeline
```

Replay and verify an experiment run:
```bash
simlab replay <run_id>
```

Launch the interactive local Observatory:
```bash
simlab ui --port 8000
```
Then open `http://localhost:8000` in your browser.

## Directory Layout
- `src/simlab/`: Authoritative runtime library
  - `core/`: Discrete-event kernel, deterministic clock, event queue, causal logger, replay engine
  - `agents/`: Agent abstractions (Coordinator, Worker, Critic), policies, and model adapters
  - `environment/`: Authoritative state transitions, resource accounting, tasks
  - `scenarios/`: Declarative scenario definitions and validation schemas
  - `memory/`: Memory stream, recency/relevance/importance scoring, memory ablation harness
  - `faults/`: Reproducible fault injector (message delay, message loss, timeout, resource depletion)
  - `governance/`: Tier-based authorization firewall and execution boundaries
  - `isolation/`: Sandboxed subprocess code execution with timeouts and output bounds
  - `benchmarks/`: Real executable coding benchmarks and heterogeneous routing suites
  - `telemetry/`: Atomic JSONL writer, run manifests, and durability manager
  - `cli/`: Typer-based operational CLI (`simlab doctor`, `run`, `replay`, `inspect`, etc.)
  - `observatory/`: Lightweight Starlette/HTML5 interactive web dashboard
- `tests/`: Comprehensive unit, property-based, integration, and negative test suites
- `audits/`: Formal contract audits and historical verification harnesses
- `deliverables/`, `reproduction_design/`, `ablation_design/`, `phase3_execution/`: Historical research packages preserved for provenance

"""SimLab Interactive Observatory Backend Server.

Provides REST API and static dashboard serving for local multi-agent simulation observability.
"""

import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional
import uvicorn
from starlette.applications import Starlette
from starlette.responses import HTMLResponse, JSONResponse, Response
from starlette.routing import Route, Mount
from starlette.staticfiles import StaticFiles

from simlab.scenarios.loader import ScenarioLoader
from simlab.telemetry.manifest import RunManifest
from simlab.telemetry.storage import AtomicTelemetryWriter
from simlab.governance.firewall import GovernanceManager
from simlab.benchmarks.routing import RoutingBenchmarkRunner
from simlab.benchmarks.coding import CodingBenchmarkRunner
from simlab.memory.stream import AssociativeMemoryStream
from simlab.memory.item import MemoryItem
from simlab.faults.injector import FaultInjector


STATIC_DIR = Path(__file__).resolve().parent / "static"
DEFAULT_RUNS_DIR = Path(__file__).resolve().parents[3] / "runs"


def get_runs_dir() -> Path:
    runs_dir = Path(os.environ.get("SIMLAB_RUNS_DIR", str(DEFAULT_RUNS_DIR)))
    runs_dir.mkdir(parents=True, exist_ok=True)
    return runs_dir


async def index(request) -> Response:
    """Serve the single-page observatory dashboard."""
    index_path = STATIC_DIR / "index.html"
    if not index_path.exists():
        return HTMLResponse("<h1>SimLab Observatory: static/index.html not found</h1>", status_code=404)
    with open(index_path, "r", encoding="utf-8") as f:
        html_content = f.read()
    return HTMLResponse(html_content)


async def api_scenarios(request) -> JSONResponse:
    """List available simulation scenarios with metadata."""
    loader = ScenarioLoader()
    scenarios = []
    for sc_id in loader.list_scenarios():
        try:
            cfg = loader.load_scenario(sc_id)
            scenarios.append({
                "scenario_id": cfg.scenario_id,
                "name": cfg.name,
                "description": cfg.description,
                "max_steps": cfg.max_ticks,
                "agent_count": len(cfg.agents),
                "task_count": len(cfg.tasks),
                "energy_budget": cfg.initial_energy,
                "bandwidth_limit": cfg.initial_bandwidth,
            })
        except Exception as e:
            scenarios.append({"scenario_id": sc_id, "error": str(e)})
    return JSONResponse({"scenarios": scenarios})


async def api_runs(request) -> JSONResponse:
    """List all saved experiment runs."""
    runs_dir = get_runs_dir()
    runs = []
    if runs_dir.exists():
        for run_path in sorted(runs_dir.iterdir(), key=os.path.getmtime, reverse=True):
            if run_path.is_dir() and (run_path / "manifest.json").exists():
                try:
                    with open(run_path / "manifest.json", "r", encoding="utf-8") as f:
                        data = json.load(f)
                    runs.append(data)
                except Exception:
                    pass
    return JSONResponse({"runs": runs})


async def api_run_detail(request) -> JSONResponse:
    """Fetch run manifest and final state."""
    run_id = request.path_params.get("run_id")
    run_dir = get_runs_dir() / run_id
    if not run_dir.exists():
        return JSONResponse({"error": f"Run '{run_id}' not found."}, status_code=404)

    try:
        manifest, _, state = AtomicTelemetryWriter.load_run(run_dir)
        return JSONResponse({
            "manifest": manifest.to_dict(),
            "final_state": state,
        })
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)


async def api_run_events(request) -> JSONResponse:
    """Fetch all causally ordered events for a run."""
    run_id = request.path_params.get("run_id")
    run_dir = get_runs_dir() / run_id
    events_file = run_dir / "events.jsonl"
    if not events_file.exists():
        return JSONResponse({"error": f"Events for '{run_id}' not found."}, status_code=404)

    records = AtomicTelemetryWriter.read_records(events_file)
    return JSONResponse({"run_id": run_id, "total_events": len(records), "events": records})


async def api_verify_run(request) -> JSONResponse:
    """Verify cryptographic hash chain and bit-for-bit state replay."""
    run_id = request.path_params.get("run_id")
    run_dir = get_runs_dir() / run_id
    if not run_dir.exists():
        return JSONResponse({"error": f"Run '{run_id}' not found."}, status_code=404)

    events_file = run_dir / "events.jsonl"
    manifest_file = run_dir / "manifest.json"
    if not events_file.exists():
        return JSONResponse({"error": f"events.jsonl missing for run '{run_id}'"}, status_code=404)

    try:
        from simlab.core.replay import ReplayEngine
        replayer = ReplayEngine.from_jsonl(events_file)
        chain_valid, chain_err = replayer.verify_integrity()

        manifest = {}
        if manifest_file.exists():
            with open(manifest_file, "r", encoding="utf-8") as f:
                manifest = json.load(f)

        scenario_id = manifest.get("scenario_id", "cooperative_pipeline")
        expected_hash = manifest.get("terminal_state_hash")

        state_valid, state_err, final_state = replayer.replay_state(
            scenario_identifier_or_config=scenario_id,
            expected_terminal_hash=expected_hash
        )

        from simlab.core.state import EnvironmentState
        replayed_hash = EnvironmentState(final_state).compute_hash() if final_state else None

        return JSONResponse({
            "run_id": run_id,
            "chain_valid": chain_valid,
            "chain_error": chain_err,
            "state_replay_valid": state_valid,
            "state_error": state_err,
            "total_events": replayer.total_events,
            "expected_state_hash": expected_hash,
            "replayed_state_hash": replayed_hash,
            "is_fully_verified": chain_valid and state_valid
        })
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)


async def api_start_run(request) -> JSONResponse:
    """Start an interactive simulation run and record telemetry."""
    try:
        body = await request.json()
    except Exception:
        body = {}

    scenario_id = body.get("scenario_id", "cooperative_pipeline")
    seed = int(body.get("seed", 42))
    steps_override = body.get("steps")
    fault_loss = float(body.get("fault_loss", 0.0))
    fault_delay = int(body.get("fault_delay", 0))

    try:
        loader = ScenarioLoader()
        cfg = loader.load_scenario(scenario_id)
        kernel, env = loader.build_simulation(cfg, seed=seed)

        if fault_loss > 0.0 or fault_delay > 0:
            fault_inj = FaultInjector(
                seed=seed,
                message_loss_rate=fault_loss,
                extra_delay_ticks=fault_delay
            )
            kernel.attach_fault_injector(fault_inj)

        max_ticks = int(steps_override) if steps_override else cfg.max_ticks
        result = kernel.run(max_ticks=max_ticks)

        # Build run ID and directory
        run_id = f"{scenario_id}_s{seed}_{int(kernel.clock.current_tick)}"
        run_dir = get_runs_dir() / run_id

        manifest = RunManifest(
            run_id=run_id,
            scenario_id=scenario_id,
            seed=seed,
            parameters={
                "max_steps": max_ticks,
                "fault_loss": fault_loss,
                "fault_delay": fault_delay,
            }
        )

        chain_valid, _ = kernel.logger.verify_chain()
        manifest.mark_completed(
            ticks=kernel.clock.current_tick,
            events=len(kernel.logger),
            messages=kernel.bus.total_messages_routed,
            state_hash=kernel.get_state_hash(),
            chain_valid=chain_valid,
            resources={
                "remaining_energy": float(env.state.get("energy", 0.0)),
                "completed_tasks": env.state.get("completed_count", 0),
                "failed_tasks": env.state.get("failed_count", 0),
            }
        )

        # Save run files
        AtomicTelemetryWriter.save_run(
            run_dir=run_dir,
            manifest=manifest,
            events=kernel.logger.to_list(),
            state=env.state.to_dict()
        )

        return JSONResponse({
            "success": True,
            "run_id": run_id,
            "manifest": manifest.to_dict(),
            "kernel_result": result.to_dict() if hasattr(result, "to_dict") else vars(result),
            "final_state": env.state.to_dict(),
        })

    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)}, status_code=500)


async def api_governance(request) -> JSONResponse:
    """Fetch governance charter status and boundary state."""
    gm = GovernanceManager()
    data = gm.load()
    return JSONResponse({
        "governance_path": str(gm.path),
        "canonical_lifecycle_state": data.get("canonical_lifecycle_state"),
        "authority_state": data.get("authority_state", {}),
        "execution_firewall": data.get("execution_firewall", {}),
        "closed_gates": data.get("closed_gates", []),
    })


async def api_benchmarks(request) -> JSONResponse:
    """Execute and return benchmark results."""
    bench_type = request.path_params.get("bench_type")
    if bench_type == "routing":
        runner = RoutingBenchmarkRunner()
        return JSONResponse({"results": runner.compare_all_policies()})
    elif bench_type == "coding":
        runner = CodingBenchmarkRunner()
        return JSONResponse({"results": runner.run_suite()})
    else:
        return JSONResponse({"error": f"Unknown benchmark type '{bench_type}'"}, status_code=400)


async def api_memory_query(request) -> JSONResponse:
    """Test associative memory retrieval with dynamic weighting."""
    try:
        body = await request.json()
    except Exception:
        body = {}

    query_vec = body.get("query_vec", [0.5, 0.5, 0.5])
    alpha = float(body.get("alpha", 0.2))
    beta = float(body.get("beta", 0.5))
    gamma = float(body.get("gamma", 0.3))

    stream = AssociativeMemoryStream(capacity=10)
    for i in range(5):
        stream.add(MemoryItem(
            memory_id=f"mem_{i}",
            content=f"Knowledge observation #{i}",
            timestamp_hours=i * 12.0,
            importance=float(i * 2 + 1),
            embedding=[0.1 * i, 0.2 * i, 0.3]
        ))

    results = stream.retrieve(
        query_embedding=query_vec,
        current_time_hours=72.0,
        top_k=5,
        alpha=alpha,
        beta=beta,
        gamma=gamma
    )

    return JSONResponse({
        "weights": {"alpha": alpha, "beta": beta, "gamma": gamma},
        "retrieved": [
            {
                "memory_id": item.memory_id,
                "content": item.content,
                "importance": item.importance,
                "timestamp_hours": item.timestamp_hours,
                "score": score
            }
            for item, score in results
        ]
    })


def create_observatory_app() -> Starlette:
    """Construct Starlette application instance."""
    routes = [
        Route("/", endpoint=index, methods=["GET"]),
        Route("/api/scenarios", endpoint=api_scenarios, methods=["GET"]),
        Route("/api/runs", endpoint=api_runs, methods=["GET"]),
        Route("/api/run/{run_id}", endpoint=api_run_detail, methods=["GET"]),
        Route("/api/run/{run_id}/events", endpoint=api_run_events, methods=["GET"]),
        Route("/api/run/{run_id}/verify", endpoint=api_verify_run, methods=["GET"]),
        Route("/api/start_run", endpoint=api_start_run, methods=["POST"]),
        Route("/api/governance", endpoint=api_governance, methods=["GET"]),
        Route("/api/benchmarks/{bench_type}", endpoint=api_benchmarks, methods=["GET"]),
        Route("/api/memory/query", endpoint=api_memory_query, methods=["POST"]),
    ]

    STATIC_DIR.mkdir(parents=True, exist_ok=True)
    return Starlette(debug=True, routes=routes)


def start_observatory(host: str = "127.0.0.1", port: int = 8000) -> None:
    """Run observatory server with uvicorn."""
    app = create_observatory_app()
    print(f"\n[bold green]SimLab Observatory running at http://{host}:{port}/[/bold green]")
    uvicorn.run(app, host=host, port=port, log_level="info")

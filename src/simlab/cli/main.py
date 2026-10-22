"""SimLab Operational Command-Line Interface.

Provides CLI commands for running experiments, inspecting telemetry, replaying events,
validating governance boundaries, and launching the interactive observatory.
"""

import hashlib
import json
import os
import sys
from pathlib import Path
from typing import Optional
import pytest
import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from simlab.scenarios.loader import ScenarioLoader
from simlab.telemetry.manifest import RunManifest
from simlab.telemetry.storage import AtomicTelemetryWriter
from simlab.governance.permissions import OperationTier
from simlab.governance.firewall import GovernanceManager
from simlab.benchmarks.routing import RoutingBenchmarkRunner
from simlab.benchmarks.coding import CodingBenchmarkRunner
from simlab.core.replay import ReplayEngine
from simlab.isolation import SubprocessSandbox
from simlab.faults.injector import FaultInjector

console = Console()
app = typer.Typer(
    name="simlab",
    help="SimLab — Controlled Multi-Agent Simulation Laboratory",
    add_completion=False,
)
exp_app = typer.Typer(
    help="Run structured empirical and deterministic benchmarks",
    add_completion=False,
)
app.add_typer(exp_app, name="experiments")


def get_repo_root() -> Path:
    """Resolve repository root directory dynamically."""
    return Path(__file__).resolve().parents[3]


def resolve_run_dir(run_id_or_path: str) -> Path:
    """Resolve a run identifier or path to an existing directory."""
    candidate = Path(run_id_or_path)
    if candidate.is_dir() and (candidate / "manifest.json").exists():
        return candidate.resolve()
    # Check under runs/
    runs_dir = get_repo_root() / "runs"
    sub_candidate = runs_dir / run_id_or_path
    if sub_candidate.is_dir() and (sub_candidate / "manifest.json").exists():
        return sub_candidate.resolve()
    raise FileNotFoundError(f"Run '{run_id_or_path}' not found as a directory or inside '{runs_dir}'.")


@app.command()
def doctor():
    """Inspect environment, dependencies, dataset integrity, and governance state."""
    console.print(Panel.fit("[bold blue]SimLab Diagnostic Doctor[/bold blue]", border_style="blue"))
    table = Table(title="System & Dependency Health Check")
    table.add_column("Component", style="cyan", no_wrap=True)
    table.add_column("Status", style="bold")
    table.add_column("Details", style="dim")

    # 1. Python version
    py_ver = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    if sys.version_info >= (3, 10):
        table.add_row("Python Runtime", "[green]PASS[/green]", f"Python {py_ver}")
    else:
        table.add_row("Python Runtime", "[red]FAIL[/red]", f"Python {py_ver} (Requires >= 3.10)")

    # 2. Key Libraries
    libs = ["numpy", "scipy", "sklearn", "pydantic", "rich", "typer", "starlette", "uvicorn", "pytest"]
    for lib in libs:
        try:
            __import__(lib)
            table.add_row(f"Library: {lib}", "[green]PASS[/green]", "Installed and importable")
        except ImportError:
            table.add_row(f"Library: {lib}", "[red]FAIL[/red]", "Missing dependency")

    # 3. Dataset Integrity
    dataset_path = get_repo_root() / "phase3_execution" / "SimLab_MemBench_500.json"
    expected_sha = "97cba94e14b4ada840141ee34f153c76a3939a20924ea60caae5b015d5ded800"
    if dataset_path.exists():
        with open(dataset_path, "rb") as f:
            actual_sha = hashlib.sha256(f.read()).hexdigest()
        if actual_sha == expected_sha:
            table.add_row("SimLab-MemBench-500", "[green]PASS[/green]", f"SHA-256 verified ({actual_sha[:12]}...)")
        else:
            table.add_row("SimLab-MemBench-500", "[red]FAIL[/red]", f"Hash mismatch: got {actual_sha[:12]}...")
    else:
        table.add_row("SimLab-MemBench-500", "[yellow]WARN[/yellow]", f"File not found at '{dataset_path}'")

    # 4. Governance Status
    gm = GovernanceManager()
    gov_data = gm.load()
    lifecycle_state = gov_data.get("canonical_lifecycle_state", "UNKNOWN")
    table.add_row("Governance State", "[yellow]ACTIVE[/yellow]", f"State: {lifecycle_state}")

    # 5. Sandbox Execution
    try:
        sandbox = SubprocessSandbox(timeout_seconds=2.0)
        res = sandbox.run_code("print('SANDBOX_OK')")
        if res.is_success and "SANDBOX_OK" in res.stdout:
            table.add_row("Subprocess Sandbox", "[green]PASS[/green]", "Isolated execution functional")
        else:
            table.add_row("Subprocess Sandbox", "[red]FAIL[/red]", f"Exit code {res.exit_code}")
    except Exception as e:
        table.add_row("Subprocess Sandbox", "[red]FAIL[/red]", str(e))

    console.print(table)


@app.command()
def scenarios():
    """List available declarative simulation scenarios."""
    loader = ScenarioLoader()
    ids = loader.list_scenarios()
    table = Table(title="Available SimLab Scenarios")
    table.add_column("Scenario ID", style="cyan", no_wrap=True)
    table.add_column("Name", style="bold")
    table.add_column("Max Steps", justify="right")
    table.add_column("Agents", justify="right")
    table.add_column("Tasks", justify="right")
    table.add_column("Description", style="dim")

    for sc_id in ids:
        try:
            cfg = loader.load_scenario(sc_id)
            table.add_row(
                cfg.scenario_id,
                cfg.name,
                str(cfg.max_ticks),
                str(len(cfg.agents)),
                str(len(cfg.tasks)),
                cfg.description
            )
        except Exception as e:
            table.add_row(sc_id, "[red]LOAD ERROR[/red]", "-", "-", "-", str(e))

    console.print(table)


@app.command()
def run(
    scenario: str = typer.Option("cooperative_pipeline", "--scenario", "-s", help="Scenario ID or JSON path"),
    seed: int = typer.Option(42, "--seed", help="Random seed for deterministic execution"),
    steps: Optional[int] = typer.Option(None, "--steps", help="Override max simulation ticks"),
    fault_loss: float = typer.Option(0.0, "--fault-loss", help="Message loss probability (0.0 to 1.0)"),
    fault_delay: int = typer.Option(0, "--fault-delay", help="Message latency delay ticks"),
    out_dir: Optional[str] = typer.Option(None, "--out-dir", "-o", help="Custom output directory"),
    mock: bool = typer.Option(True, "--mock", help="Use deterministic mock model backend"),
):
    """Execute a simulation scenario and persist structured telemetry."""
    console.print(f"[bold cyan]Initiating simulation run for scenario:[/bold cyan] {scenario} (Seed: {seed})")

    loader = ScenarioLoader()
    cfg = loader.load_scenario(scenario)
    kernel, env = loader.build_simulation(cfg, seed=seed)

    if fault_loss > 0.0 or fault_delay > 0:
        fault_inj = FaultInjector(
            seed=seed,
            message_loss_rate=fault_loss,
            extra_delay_ticks=fault_delay
        )
        kernel.attach_fault_injector(fault_inj)
        if fault_loss > 0.0:
            console.print(f"  [yellow]Fault Injected:[/yellow] Message Loss Probability = {fault_loss}")
        if fault_delay > 0:
            console.print(f"  [yellow]Fault Injected:[/yellow] Message Delay Ticks = {fault_delay}")

    max_ticks = steps if steps is not None else cfg.max_ticks
    res = kernel.run(max_ticks=max_ticks)

    run_id = f"{cfg.scenario_id}_s{seed}_{int(kernel.clock.current_tick)}"
    destination = Path(out_dir) if out_dir else (get_repo_root() / "runs" / run_id)

    manifest = RunManifest(
        run_id=run_id,
        scenario_id=cfg.scenario_id,
        seed=seed,
        parameters={"max_steps": max_ticks, "fault_loss": fault_loss, "fault_delay": fault_delay}
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

    AtomicTelemetryWriter.save_run(
        run_dir=destination,
        manifest=manifest,
        events=kernel.logger.to_list(),
        state=env.state.to_dict()
    )

    completed_cnt = env.state.get("completed_count", 0)
    console.print(Panel.fit(
        f"[bold green]Simulation Completed Successfully![/bold green]\n"
        f"Run ID: [cyan]{run_id}[/cyan]\n"
        f"Total Ticks: {kernel.clock.current_tick} / {max_ticks}\n"
        f"Total Events: {len(kernel.logger)} | Messages Routed: {kernel.bus.total_messages_routed}\n"
        f"Tasks Completed: {completed_cnt} / {len(cfg.tasks)}\n"
        f"Remaining Energy: {env.state.energy:.1f} units\n"
        f"State SHA-256: [dim]{kernel.get_state_hash()}[/dim]\n"
        f"Output Directory: [blue]{destination}[/blue]",
        title="Execution Summary"
    ))


@app.command()
def inspect(run_id_or_path: str = typer.Argument(..., help="Run ID or path to run directory")):
    """Inspect run manifest, event timeline, state hash, and resource usage."""
    run_dir = resolve_run_dir(run_id_or_path)
    manifest, events, state = AtomicTelemetryWriter.load_run(run_dir)

    console.print(Panel.fit(
        f"[bold cyan]Run Manifest: {manifest.run_id}[/bold cyan]\n"
        f"Scenario: {manifest.scenario_id} | Seed: {manifest.seed} | Git: {manifest.git_revision[:10]}\n"
        f"Status: [green]{manifest.status}[/green] | Ticks: {manifest.total_ticks} | Events: {manifest.total_events}\n"
        f"State Hash: [dim]{manifest.terminal_state_hash}[/dim]\n"
        f"Event Hash Chain: {'[green]VALID[/green]' if manifest.event_chain_valid else '[red]INVALID[/red]'}",
        title="Provenance Metadata"
    ))

    # Show last 10 events
    table = Table(title=f"Event Timeline Preview (Latest {min(10, len(events))} events)")
    table.add_column("Tick", justify="right")
    table.add_column("Seq", justify="right")
    table.add_column("Type", style="cyan")
    table.add_column("Actor", style="bold")
    table.add_column("Action")
    table.add_column("Event SHA-256", style="dim")

    for ev in events[-10:]:
        table.add_row(
            str(ev.get("tick")),
            str(ev.get("sequence")),
            str(ev.get("event_type")),
            str(ev.get("actor_id")),
            str(ev.get("action")),
            str(ev.get("event_hash", ""))[:16] + "..."
        )
    console.print(table)


@app.command()
def replay(run_id_or_path: str = typer.Argument(..., help="Run ID or directory path to replay")):
    """Verify cryptographic causal hash chain and run bit-for-bit state replay comparison."""
    run_dir = resolve_run_dir(run_id_or_path)
    events_file = run_dir / "events.jsonl"
    manifest_file = run_dir / "manifest.json"
    if not events_file.exists():
        console.print(f"[red]Error: events.jsonl missing in '{run_dir}'[/red]")
        raise typer.Exit(1)

    replayer = ReplayEngine.from_jsonl(events_file)
    chain_valid, chain_err = replayer.verify_integrity()
    if not chain_valid:
        console.print(f"[bold red]Event Hash Chain Verification Failed:[/bold red] {chain_err}")
        raise typer.Exit(1)

    state_valid = True
    state_err = None
    if manifest_file.exists():
        with open(manifest_file, "r", encoding="utf-8") as f:
            manifest_data = json.load(f)
        scenario_id = manifest_data.get("scenario_id")
        expected_hash = manifest_data.get("terminal_state_hash")
        if scenario_id:
            state_valid, state_err, _ = replayer.replay_state(
                scenario_identifier_or_config=scenario_id,
                expected_terminal_hash=expected_hash
            )

    if chain_valid and state_valid:
        console.print(Panel.fit(
            f"[bold green]Causal Hash Chain Verified![/bold green]\n"
            f"Events Replayed: {replayer.total_events}\n"
            f"Distinct Ticks: {len(replayer.get_ticks())}\n"
            f"State Replay Status: [green]BIT-FOR-BIT MATCH[/green]\n"
            f"Trace File: [blue]{events_file}[/blue]",
            title="Replay Engine"
        ))
    else:
        console.print(f"[bold red]State Replay Verification Failed:[/bold red] {state_err}")
        raise typer.Exit(1)


@app.command()
def results():
    """Aggregate and summarize experimental runs across storage."""
    runs_dir = get_repo_root() / "runs"
    if not runs_dir.exists():
        console.print("[yellow]No runs directory found.[/yellow]")
        return

    table = Table(title="SimLab Experimental Runs Catalog")
    table.add_column("Run ID", style="cyan")
    table.add_column("Scenario", style="bold")
    table.add_column("Seed", justify="right")
    table.add_column("Ticks", justify="right")
    table.add_column("Events", justify="right")
    table.add_column("Status")
    table.add_column("State SHA-256", style="dim")

    for r_dir in sorted(runs_dir.iterdir(), key=os.path.getmtime, reverse=True):
        if r_dir.is_dir() and (r_dir / "manifest.json").exists():
            try:
                with open(r_dir / "manifest.json", "r", encoding="utf-8") as f:
                    m = json.load(f)
                status_color = "green" if m.get("status") == "COMPLETED" else "yellow"
                table.add_row(
                    m.get("run_id", r_dir.name),
                    m.get("scenario_id", "-"),
                    str(m.get("seed", "-")),
                    str(m.get("total_ticks", "-")),
                    str(m.get("total_events", "-")),
                    f"[{status_color}]{m.get('status')}[/{status_color}]",
                    m.get("terminal_state_hash", "")[:12] + "..."
                )
            except Exception:
                pass

    console.print(table)


@app.command()
def verify():
    """Run full self-test suite and adversarial assertions."""
    console.print("[bold cyan]Executing SimLab verification suite via pytest...[/bold cyan]")
    ret = pytest.main(["-ra", "-q", str(get_repo_root() / "tests"), str(get_repo_root() / "audits")])
    if ret == 0:
        console.print("\n[bold green]ALL TESTS & ADVERSARIAL ASSERTIONS PASSED[/bold green]")
    else:
        console.print(f"\n[bold red]Verification Failed with exit code {ret}[/bold red]")
        raise typer.Exit(ret)


@app.command(name="observatory")
@app.command(name="ui")
def observatory(
    host: str = typer.Option("127.0.0.1", "--host", "-h", help="Bind host address"),
    port: int = typer.Option(8000, "--port", "-p", help="Bind port"),
):
    """Launch the local interactive observatory web dashboard."""
    from simlab.observatory.server import start_observatory
    start_observatory(host=host, port=port)


# EXPERIMENT SUBCOMMANDS
@exp_app.command("routing")
def exp_routing(agent_count: int = typer.Option(3, "--agents", "-a", help="Agent count for routing benchmark")):
    """Run heterogeneous multi-agent routing policy benchmark."""
    runner = RoutingBenchmarkRunner()
    results = runner.compare_all_policies(agent_count=agent_count)

    table = Table(title=f"Multi-Agent Routing Benchmark (Agent Count: {agent_count})")
    table.add_column("Routing Policy", style="cyan", no_wrap=True)
    table.add_column("Total Tokens", justify="right")
    table.add_column("Avg / Task", justify="right")
    table.add_column("Coord Overhead", justify="right")
    table.add_column("Overhead %", justify="right")
    table.add_column("Success Rate", justify="right")

    for r in results:
        table.add_row(
            r["policy"],
            str(r["total_tokens_consumed"]),
            f"{r['average_tokens_per_task']:.1f}",
            str(r["coordination_overhead_tokens"]),
            f"{r['overhead_percentage']:.1f}%",
            f"{r['success_rate'] * 100:.0f}%"
        )
    console.print(table)


@exp_app.command("coding")
def exp_coding():
    """Run sandboxed coding benchmark with unit test assertion suite."""
    runner = CodingBenchmarkRunner()
    suite = runner.run_suite()

    table = Table(title=f"Coding Benchmark Suite (Pass Rate: {suite['pass_rate'] * 100:.1f}%)")
    table.add_column("Task ID", style="cyan")
    table.add_column("Name", style="bold")
    table.add_column("Category")
    table.add_column("Difficulty")
    table.add_column("Status")
    table.add_column("Duration (ms)", justify="right")

    for res in suite["results"]:
        status_str = "[green]PASS[/green]" if res["passed"] else "[red]FAIL[/red]"
        table.add_row(
            res["task_id"],
            res["name"],
            res["category"],
            res["difficulty"],
            status_str,
            f"{res['duration_ms']:.1f}"
        )
    console.print(table)


@exp_app.command("memory-ablation")
def exp_memory_ablation(
    mock: bool = typer.Option(True, "--mock/--no-mock", help="Run under deterministic mock tier")
):
    """Run PR-COG-01 memory component ablation experiment."""
    repo_root = str(get_repo_root())
    if repo_root not in sys.path:
        sys.path.insert(0, repo_root)
    import run_exp_ab_01_comp
    console.print("[bold cyan]Executing Memory Component Ablation (EXP-AB-01-COMP)...[/bold cyan]")
    run_exp_ab_01_comp.main(mock_mode=mock)


if __name__ == "__main__":
    app()

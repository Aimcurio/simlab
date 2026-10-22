"""Automated testing for SimLab CLI commands."""

import pytest
from typer.testing import CliRunner
from simlab.cli.main import app

runner = CliRunner()


def test_cli_help():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "SimLab" in result.stdout
    assert "doctor" in result.stdout
    assert "run" in result.stdout
    assert "inspect" in result.stdout
    assert "replay" in result.stdout
    assert "results" in result.stdout
    assert "scenarios" in result.stdout
    assert "experiments" in result.stdout
    assert "observatory" in result.stdout


def test_cli_doctor():
    result = runner.invoke(app, ["doctor"])
    assert result.exit_code == 0
    assert "SimLab Diagnostic Doctor" in result.stdout
    assert "Python Runtime" in result.stdout
    assert "Subprocess Sandbox" in result.stdout


def test_cli_scenarios():
    result = runner.invoke(app, ["scenarios"])
    assert result.exit_code == 0
    assert "cooperative_pipeline" in result.stdout


def test_cli_run_and_inspect_and_replay(tmp_path):
    run_out = tmp_path / "test_run_cli"
    result = runner.invoke(
        app,
        [
            "run",
            "--scenario", "cooperative_pipeline",
            "--seed", "99",
            "--steps", "4",
            "--out-dir", str(run_out),
            "--mock"
        ]
    )
    assert result.exit_code == 0
    assert "Simulation Completed Successfully" in result.stdout
    assert (run_out / "manifest.json").exists()
    assert (run_out / "events.jsonl").exists()
    assert (run_out / "final_state.json").exists()

    # Test inspect
    inspect_result = runner.invoke(app, ["inspect", str(run_out)])
    assert inspect_result.exit_code == 0
    assert "Run Manifest" in inspect_result.stdout
    assert "VALID" in inspect_result.stdout

    # Test replay
    replay_result = runner.invoke(app, ["replay", str(run_out)])
    assert replay_result.exit_code == 0
    assert "Causal Hash Chain Verified" in replay_result.stdout


def test_cli_results():
    result = runner.invoke(app, ["results"])
    assert result.exit_code == 0
    assert "SimLab Experimental Runs Catalog" in result.stdout


def test_cli_experiments_routing():
    result = runner.invoke(app, ["experiments", "routing", "--agents", "2"])
    assert result.exit_code == 0
    assert "Multi-Agent Routing Benchmark" in result.stdout
    assert "BROADCAST_ALL" in result.stdout
    assert "CAPABILITY_MATCH" in result.stdout


def test_cli_experiments_coding():
    result = runner.invoke(app, ["experiments", "coding"])
    assert result.exit_code == 0
    assert "Coding Benchmark Suite" in result.stdout
    assert "PASS" in result.stdout

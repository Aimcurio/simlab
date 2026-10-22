"""Tests for Atomic Telemetry and Run Manifest Storage."""

import tempfile
from pathlib import Path
import pytest

from simlab.telemetry import AtomicTelemetryWriter, RunManifest


def test_atomic_telemetry_write_and_read():
    with tempfile.TemporaryDirectory() as tmp_dir:
        target_file = Path(tmp_dir) / "test_run.jsonl"
        records = [
            {"event_id": "ev_01", "tick": 0, "action": "START"},
            {"event_id": "ev_02", "tick": 1, "action": "DECIDE"},
            {"event_id": "ev_03", "tick": 2, "action": "FINISH"},
        ]

        AtomicTelemetryWriter.write_records_atomically(target_file, records)
        assert target_file.exists()

        loaded = AtomicTelemetryWriter.read_records(target_file)
        assert len(loaded) == 3
        assert loaded[0]["event_id"] == "ev_01"
        assert loaded[2]["action"] == "FINISH"


def test_save_and_load_complete_run():
    with tempfile.TemporaryDirectory() as tmp_dir:
        run_dir = Path(tmp_dir) / "run_101"
        manifest = RunManifest(
            run_id="run_101",
            scenario_id="cooperative_pipeline",
            seed=42,
            parameters={"alpha": 0.5}
        )
        manifest.mark_completed(
            ticks=10,
            events=25,
            messages=8,
            state_hash="deadbeef",
            chain_valid=True,
            resources={"tokens": 1200}
        )

        events = [{"event_id": f"ev_{i}", "tick": i} for i in range(25)]
        state = {"tasks_completed": 3, "energy": 80.0}

        AtomicTelemetryWriter.save_run(run_dir, manifest, events, state)

        # Load back
        loaded_manifest, loaded_events, loaded_state = AtomicTelemetryWriter.load_run(run_dir)
        assert loaded_manifest.run_id == "run_101"
        assert loaded_manifest.status == "COMPLETED"
        assert loaded_manifest.total_ticks == 10
        assert len(loaded_events) == 25
        assert loaded_state["energy"] == 80.0

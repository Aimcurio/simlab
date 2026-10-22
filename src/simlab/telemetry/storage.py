"""Atomic Telemetry Storage and Run Persistence."""

import json
import os
import tempfile
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from simlab.telemetry.manifest import RunManifest


class AtomicTelemetryWriter:
    """Manages atomic file replacement and crash-safe JSONL serialization."""

    @staticmethod
    def write_records_atomically(filepath: Path, records: List[Dict[str, Any]]) -> None:
        """
        Write records to temporary file in same filesystem, flush & fsync,
        then atomically replace target path to avoid partial or corrupted writes.
        """
        filepath = Path(filepath)
        filepath.parent.mkdir(parents=True, exist_ok=True)

        temp_file = None
        try:
            with tempfile.NamedTemporaryFile(
                mode="w",
                encoding="utf-8",
                dir=filepath.parent,
                prefix="tmp_telemetry_",
                suffix=".tmp",
                delete=False
            ) as f:
                temp_file = Path(f.name)
                for record in records:
                    f.write(json.dumps(record, default=str) + "\n")
                f.flush()
                os.fsync(f.fileno())

            # Atomic replace (supported on POSIX and Windows in Python 3.3+)
            os.replace(temp_file, filepath)
        except Exception:
            if temp_file and temp_file.exists():
                try:
                    temp_file.unlink()
                except OSError:
                    pass
            raise

    @staticmethod
    def append_record_durably(filepath: Path, record: Dict[str, Any]) -> None:
        """Append single record with immediate flush and sync."""
        filepath = Path(filepath)
        filepath.parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, default=str) + "\n")
            f.flush()
            os.fsync(f.fileno())

    @staticmethod
    def read_records(filepath: Path) -> List[Dict[str, Any]]:
        """Read all valid JSON records from JSONL file."""
        filepath = Path(filepath)
        if not filepath.exists():
            return []
        records = []
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    records.append(json.loads(line))
        return records

    @staticmethod
    def save_run(
        run_dir: Path,
        manifest: RunManifest,
        events: List[Dict[str, Any]],
        state: Optional[Dict[str, Any]] = None
    ) -> None:
        """Save complete run package: manifest.json, events.jsonl, and final_state.json."""
        run_dir = Path(run_dir)
        run_dir.mkdir(parents=True, exist_ok=True)

        # 1. Events
        events_file = run_dir / "events.jsonl"
        AtomicTelemetryWriter.write_records_atomically(events_file, events)

        # 2. State
        if state is not None:
            state_file = run_dir / "final_state.json"
            temp_state = run_dir / "state.tmp"
            with open(temp_state, "w", encoding="utf-8") as f:
                json.dump(state, f, indent=2, default=str)
                f.flush()
                os.fsync(f.fileno())
            os.replace(temp_state, state_file)

        # 3. Manifest
        manifest_file = run_dir / "manifest.json"
        temp_manifest = run_dir / "manifest.tmp"
        with open(temp_manifest, "w", encoding="utf-8") as f:
            json.dump(manifest.to_dict(), f, indent=2)
            f.flush()
            os.fsync(f.fileno())
        os.replace(temp_manifest, manifest_file)

    @staticmethod
    def load_run(run_dir: Path) -> Tuple[RunManifest, List[Dict[str, Any]], Dict[str, Any]]:
        """Load manifest, events, and state from run directory."""
        run_dir = Path(run_dir)
        manifest_path = run_dir / "manifest.json"
        events_path = run_dir / "events.jsonl"
        state_path = run_dir / "final_state.json"

        if not manifest_path.exists():
            raise FileNotFoundError(f"Run manifest missing at '{manifest_path}'")

        with open(manifest_path, "r", encoding="utf-8") as f:
            manifest = RunManifest.from_dict(json.load(f))

        events = AtomicTelemetryWriter.read_records(events_path)

        state = {}
        if state_path.exists():
            with open(state_path, "r", encoding="utf-8") as f:
                state = json.load(f)

        return manifest, events, state

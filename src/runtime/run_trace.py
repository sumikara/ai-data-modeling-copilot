"""Runtime trace logging helpers for auditable semantic profiling runs."""

from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict

RUNS_BASE = Path("test_outputs/runs")


def create_run_id() -> str:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    suffix = uuid.uuid4().hex[:8]
    return f"run_{timestamp}_{suffix}"


def _trace_path(run_id: str) -> Path:
    return RUNS_BASE / run_id / "run_trace.json"


def write_run_trace(run_id: str, trace: dict) -> None:
    path = _trace_path(run_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(trace, indent=2, ensure_ascii=False), encoding="utf-8")


def append_trace_event(run_id: str, event_name: str, payload: Dict[str, Any]) -> None:
    path = _trace_path(run_id)
    if path.exists():
        trace = json.loads(path.read_text(encoding="utf-8"))
    else:
        trace = {"run_id": run_id, "events": []}

    trace.setdefault("events", []).append(
        {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event_name": event_name,
            "payload": payload,
        }
    )
    write_run_trace(run_id, trace)

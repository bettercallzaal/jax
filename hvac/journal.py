"""
HVAC Field Journal — log observations, readings, and actions from the field.
"""

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

JOURNAL_DIR = Path(__file__).parent / "data" / "journal"
JOURNAL_DIR.mkdir(parents=True, exist_ok=True)


def _today_file() -> Path:
    return JOURNAL_DIR / f"{datetime.now(timezone.utc).strftime('%Y-%m-%d')}.jsonl"


def _entry(kind: str, payload: dict) -> dict:
    return {
        "ts": datetime.now(timezone.utc).isoformat(),
        "kind": kind,
        **payload,
    }


def log_observation(
    zone: str,
    description: str,
    readings: Optional[dict] = None,
    tags: Optional[list] = None,
) -> dict:
    """Record a field observation."""
    entry = _entry("observation", {
        "zone": zone,
        "description": description,
        "readings": readings or {},
        "tags": tags or [],
    })
    with open(_today_file(), "a") as f:
        f.write(json.dumps(entry) + "\n")
    return entry


def log_action(
    zone: str,
    action: str,
    outcome: Optional[str] = None,
    parts: Optional[list] = None,
) -> dict:
    """Record a corrective action taken."""
    entry = _entry("action", {
        "zone": zone,
        "action": action,
        "outcome": outcome or "pending",
        "parts": parts or [],
    })
    with open(_today_file(), "a") as f:
        f.write(json.dumps(entry) + "\n")
    return entry


def log_reading(zone: str, readings: dict, equipment: str = "") -> dict:
    """Record instrument readings (temps, pressures, airflow, etc.)."""
    entry = _entry("reading", {
        "zone": zone,
        "equipment": equipment,
        "readings": readings,
    })
    with open(_today_file(), "a") as f:
        f.write(json.dumps(entry) + "\n")
    return entry


def read_today() -> list:
    """Return all entries from today's journal."""
    path = _today_file()
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def read_journal(date: Optional[str] = None) -> list:
    """Return entries for a specific date (YYYY-MM-DD) or all dates."""
    if date:
        path = JOURNAL_DIR / f"{date}.jsonl"
        if not path.exists():
            return []
        return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]
    entries = []
    for p in sorted(JOURNAL_DIR.glob("*.jsonl")):
        entries.extend(json.loads(line) for line in p.read_text().splitlines() if line.strip())
    return entries


def print_journal(entries: Optional[list] = None) -> None:
    """Pretty-print journal entries."""
    if entries is None:
        entries = read_today()
    if not entries:
        print("No entries found.")
        return
    for e in entries:
        ts = e["ts"][:19].replace("T", " ")
        kind = e["kind"].upper()
        zone = e.get("zone", "")
        print(f"\n[{ts}] {kind} — {zone}")
        if kind == "OBSERVATION":
            print(f"  {e['description']}")
            if e.get("readings"):
                for k, v in e["readings"].items():
                    print(f"    {k}: {v}")
            if e.get("tags"):
                print(f"  Tags: {', '.join(e['tags'])}")
        elif kind == "ACTION":
            print(f"  Action : {e['action']}")
            print(f"  Outcome: {e['outcome']}")
            if e.get("parts"):
                print(f"  Parts  : {', '.join(e['parts'])}")
        elif kind == "READING":
            eq = e.get("equipment", "")
            if eq:
                print(f"  Equipment: {eq}")
            for k, v in e.get("readings", {}).items():
                print(f"    {k}: {v}")

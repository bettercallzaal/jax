"""DAT review: compare discharge air temps to setpoints, flag outliers."""

from __future__ import annotations
import json
import os
from dataclasses import dataclass
from typing import Optional

POINTS_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "metasys_points.json")

HIGH_THRESH = 3.0    # °F above SP → warn
CRITICAL_THRESH = 10.0  # °F above SP → critical
LOW_THRESH = 3.0     # °F below SP → warn


@dataclass
class DATUnit:
    label: str
    building: str
    ahu: str
    dat: Optional[float]
    sp_low: Optional[float]
    sp_high: Optional[float]
    status: str       # "ok", "high", "critical", "low", "fault", "override", "no_sp"
    delta: Optional[float]
    notes: str = ""


@dataclass
class DATReport:
    date: str
    total: int
    critical: list[DATUnit]
    high: list[DATUnit]
    low: list[DATUnit]
    faults: list[DATUnit]
    overrides: list[DATUnit]
    ok_count: int


def load_points() -> list[dict]:
    """Load AHU point definitions from metasys_points.json."""
    with open(POINTS_FILE) as f:
        data = json.load(f)
    return data["units"]


def review_from_readings(readings: list[tuple], date: str = "") -> DATReport:
    """
    Build a DATReport from a list of (label, dat, sp_low, sp_high, flag) tuples.
    flag: None=normal, "override"=operator override, "fault"=cannot read.
    """
    critical, high, low, faults, overrides = [], [], [], [], []
    ok_count = 0

    for label, dat, sp_low, sp_high, flag in readings:
        building = label.split()[0] if " " in label else label
        ahu = label[len(building):].strip()

        unit = DATUnit(
            label=label, building=building, ahu=ahu,
            dat=dat, sp_low=sp_low, sp_high=sp_high,
            status="ok", delta=None,
        )

        if flag == "fault":
            unit.status = "fault"
            faults.append(unit)
            continue

        if flag == "override":
            unit.status = "override"
            unit.notes = f"Operator Override — SP={sp_high}°F"
            overrides.append(unit)
            continue

        if dat is None or sp_high is None:
            unit.status = "no_sp"
            ok_count += 1
            continue

        delta = dat - sp_high
        unit.delta = delta

        if delta >= CRITICAL_THRESH:
            unit.status = "critical"
            critical.append(unit)
        elif delta >= HIGH_THRESH:
            unit.status = "high"
            high.append(unit)
        elif dat < (sp_low or sp_high) - LOW_THRESH:
            unit.delta = dat - (sp_low or sp_high)
            unit.status = "low"
            low.append(unit)
        else:
            unit.status = "ok"
            ok_count += 1

    return DATReport(
        date=date,
        total=len(readings),
        critical=critical,
        high=high,
        low=low,
        faults=faults,
        overrides=overrides,
        ok_count=ok_count,
    )


def format_report_lines(report: DATReport) -> list[str]:
    lines = [
        f"DAT Review — {report.date}  ({report.total} AHUs)",
        "",
    ]
    if report.critical:
        lines.append(f"CRITICAL — DAT >{CRITICAL_THRESH}°F above setpoint ({len(report.critical)})")
        for u in report.critical:
            lines.append(f"  {u.label:<30} {u.dat}°F  SP={u.sp_high}°F  Δ=+{u.delta:.1f}°F")
        lines.append("")

    if report.high:
        lines.append(f"HIGH — DAT {HIGH_THRESH}-{CRITICAL_THRESH}°F above setpoint ({len(report.high)})")
        for u in report.high:
            lines.append(f"  {u.label:<30} {u.dat}°F  SP={u.sp_high}°F  Δ=+{u.delta:.1f}°F")
        lines.append("")

    if report.low:
        lines.append(f"LOW — DAT >{LOW_THRESH}°F below setpoint ({len(report.low)})")
        for u in report.low:
            lines.append(f"  {u.label:<30} {u.dat}°F  SP={u.sp_low}°F  Δ={u.delta:.1f}°F")
        lines.append("")

    if report.faults:
        lines.append(f"COMM FAULTS ({len(report.faults)})")
        for u in report.faults:
            lines.append(f"  {u.label}")
        lines.append("")

    if report.overrides:
        lines.append(f"OPERATOR OVERRIDES ({len(report.overrides)})")
        for u in report.overrides:
            lines.append(f"  {u.label}: {u.dat}°F  {u.notes}")
        lines.append("")

    lines.append(f"OK: {report.ok_count} units within ±{LOW_THRESH}°F of setpoint")
    return lines

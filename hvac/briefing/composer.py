"""
Briefing composer — assembles all data sources into a BriefingReport.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional

try:
    from zoneinfo import ZoneInfo
except ImportError:
    ZoneInfo = None  # Python < 3.9 fallback

from .maintainx import WorkOrder
from .metasys_api import MetasysAlarm
from .journal_summary import JournalSummary


PRIORITY_LABELS = {
    "critical": "[CRITICAL]",
    "high": "[HIGH]    ",
    "medium": "[MEDIUM]  ",
    "low": "[LOW]     ",
    "none": "[NONE]    ",
}

METASYS_CRITICAL_THRESHOLD = 50  # priority <= this = critical
METASYS_HIGH_THRESHOLD = 100


@dataclass
class BriefingSection:
    title: str
    available: bool
    error: Optional[str]
    lines: list[str] = field(default_factory=list)


@dataclass
class BriefingReport:
    generated_at: str
    date_label: str
    sections: list[BriefingSection]
    has_critical: bool


def _tz_now(tz_name: str) -> datetime:
    if ZoneInfo:
        return datetime.now(ZoneInfo(tz_name))
    return datetime.now(timezone.utc)


def _format_wo_lines(wos: list[WorkOrder]) -> list[str]:
    if not wos:
        return ["  (none)"]
    lines = []
    priority_order = ["critical", "high", "medium", "low", "none"]
    sorted_wos = sorted(wos, key=lambda w: priority_order.index(w.priority or "none") if w.priority in priority_order else 99)
    for wo in sorted_wos:
        label = PRIORITY_LABELS.get(wo.priority or "none", "[?]      ")
        lines.append(f"  {label} WO #{wo.id} — {wo.title}")
        assignee = wo.assignee or "Unassigned"
        due = wo.due_date[:10] if wo.due_date else "no due date"
        lines.append(f"             Assigned: {assignee}  |  Due: {due}")
        if wo.location:
            lines.append(f"             Location: {wo.location}")
        lines.append(f"             {wo.url}")
        lines.append("")
    return lines


def _format_alarm_lines(alarms: list[MetasysAlarm]) -> list[str]:
    if not alarms:
        return ["  (none)"]
    lines = []
    sorted_alarms = sorted(alarms, key=lambda a: a.priority)
    for alarm in sorted_alarms:
        p = alarm.priority
        if p <= METASYS_CRITICAL_THRESHOLD:
            badge = f"[P-{p:03d} CRITICAL]"
        elif p <= METASYS_HIGH_THRESHOLD:
            badge = f"[P-{p:03d} HIGH]    "
        else:
            badge = f"[P-{p:03d}]         "
        lines.append(f"  {badge} {alarm.alarm_message}")
        lines.append(f"               Object: {alarm.object_name}")
        acked = "ACKED" if alarm.is_acked else "UNACKED"
        ts = alarm.occurred_at[:16].replace("T", " ") if alarm.occurred_at else "unknown"
        lines.append(f"               {acked}  |  Occurred: {ts}")
        if alarm.area:
            lines.append(f"               Area: {alarm.area}")
        lines.append("")
    return lines


def _format_journal_lines(summary: JournalSummary, open_items: list[dict]) -> list[str]:
    lines = [f"  {summary.total_entries} entries logged on {summary.date}."]
    lines.append("")

    lines.append(f"  PENDING ACTIONS ({len(summary.pending_actions)}):")
    if summary.pending_actions:
        for e in summary.pending_actions:
            ts = e["ts"][:16].replace("T", " ")
            lines.append(f"    [{ts}] {e.get('zone', '')} — {e.get('action', '')}")
            lines.append(f"           Outcome: {e.get('outcome', '')}  |  Tags: {', '.join(e.get('tags', []))}")
    else:
        lines.append("    (none)")
    lines.append("")

    lines.append(f"  FLAGGED OBSERVATIONS ({len(summary.flagged_observations)}):")
    if summary.flagged_observations:
        for e in summary.flagged_observations:
            ts = e["ts"][:16].replace("T", " ")
            lines.append(f"    [{ts}] {e.get('zone', '')} — {e.get('description', '')[:100]}")
    else:
        lines.append("    (none)")
    lines.append("")

    older = [i for i in open_items]
    lines.append(f"  OPEN ITEMS FROM LAST 7 DAYS ({len(older)}):")
    if older:
        for e in older:
            src_date = e.get("_source_date", "")
            zone = e.get("zone", "")
            desc = e.get("description") or e.get("action") or ""
            tags = ", ".join(e.get("tags") or [])
            lines.append(f"    [{src_date}] {zone} — {desc[:100]}")
            if tags:
                lines.append(f"               Tags: {tags}")
    else:
        lines.append("    (none)")

    return lines


def assemble_briefing(
    work_orders: Optional[list[WorkOrder]],
    maintainx_error: Optional[str],
    alarms: Optional[list[MetasysAlarm]],
    metasys_error: Optional[str],
    journal_summary: JournalSummary,
    open_items: list[dict],
    tz_name: str = "America/New_York",
) -> BriefingReport:
    now = _tz_now(tz_name)
    date_label = now.strftime("%A, %B %-d, %Y")
    generated_at = now.strftime("%Y-%m-%d %I:%M %p %Z")

    sections: list[BriefingSection] = []

    # MaintainX section
    if maintainx_error and work_orders is None:
        mx_section = BriefingSection(
            title="MAINTAINX — OPEN WORK ORDERS",
            available=False,
            error=maintainx_error,
            lines=[f"  Skipped: {maintainx_error}"],
        )
    elif work_orders is None:
        mx_section = BriefingSection(
            title="MAINTAINX — OPEN WORK ORDERS",
            available=False,
            error="MAINTAINX_API_TOKEN not configured",
            lines=["  Skipped: set MAINTAINX_API_TOKEN to enable."],
        )
    else:
        open_count = sum(1 for w in work_orders if w.status == "open")
        inprog_count = sum(1 for w in work_orders if w.status == "in_progress")
        header_detail = f"({open_count} open, {inprog_count} in-progress)"
        mx_section = BriefingSection(
            title=f"MAINTAINX — OPEN WORK ORDERS  {header_detail}",
            available=True,
            error=None,
            lines=_format_wo_lines(work_orders),
        )
    sections.append(mx_section)

    # Journal section
    sections.append(BriefingSection(
        title=f"JOURNAL — YESTERDAY'S ENTRIES ({journal_summary.date})",
        available=True,
        error=None,
        lines=_format_journal_lines(journal_summary, open_items),
    ))

    # Metasys section
    if metasys_error and alarms is None:
        met_section = BriefingSection(
            title="METASYS — ACTIVE ALARMS",
            available=False,
            error=metasys_error,
            lines=[f"  Skipped: {metasys_error}"],
        )
    elif alarms is None:
        met_section = BriefingSection(
            title="METASYS — ACTIVE ALARMS",
            available=False,
            error="METASYS_HOST not configured",
            lines=["  Skipped: set METASYS_HOST, METASYS_USERNAME, METASYS_PASSWORD to enable."],
        )
    else:
        met_section = BriefingSection(
            title=f"METASYS — ACTIVE ALARMS ({len(alarms)} alarms)",
            available=True,
            error=None,
            lines=_format_alarm_lines(alarms),
        )
    sections.append(met_section)

    # Determine if action is needed
    has_critical = False
    if work_orders:
        has_critical = has_critical or any(w.priority == "critical" for w in work_orders)
    if alarms:
        has_critical = has_critical or any(a.priority <= METASYS_CRITICAL_THRESHOLD for a in alarms)
    if journal_summary.pending_actions:
        has_critical = True

    return BriefingReport(
        generated_at=generated_at,
        date_label=date_label,
        sections=sections,
        has_critical=has_critical,
    )

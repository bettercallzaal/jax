"""
Journal summarizer for the morning briefing.
Wraps hvac.journal to extract pending/unresolved items.
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path

from .. import journal


PENDING_OUTCOME_KEYWORDS = ("pending", "unresolved", "follow", "tbd", "unknown")
FLAG_TAGS = {"followup", "unresolved", "pending", "open", "action-needed"}


@dataclass
class JournalSummary:
    date: str
    total_entries: int
    pending_actions: list[dict] = field(default_factory=list)
    flagged_observations: list[dict] = field(default_factory=list)
    all_entries: list[dict] = field(default_factory=list)


def _is_pending_action(entry: dict) -> bool:
    if entry.get("kind") != "action":
        return False
    outcome = (entry.get("outcome") or "").lower()
    return any(kw in outcome for kw in PENDING_OUTCOME_KEYWORDS)


def _is_flagged_observation(entry: dict, flag_tags: set) -> bool:
    if entry.get("kind") != "observation":
        return False
    tags = {t.lower() for t in (entry.get("tags") or [])}
    return bool(tags & flag_tags)


def get_yesterday_summary() -> JournalSummary:
    yesterday = (datetime.now(timezone.utc) - timedelta(days=1)).strftime("%Y-%m-%d")
    entries = journal.read_journal(date=yesterday)
    pending = [e for e in entries if _is_pending_action(e)]
    flagged = [e for e in entries if _is_flagged_observation(e, FLAG_TAGS)]
    return JournalSummary(
        date=yesterday,
        total_entries=len(entries),
        pending_actions=pending,
        flagged_observations=flagged,
        all_entries=entries,
    )


def get_open_items_across_journal(days_back: int = 7) -> list[dict]:
    """Scan the last N days of journal for still-open/pending items."""
    open_items = []
    today = datetime.now(timezone.utc)
    for i in range(1, days_back + 1):
        date_str = (today - timedelta(days=i)).strftime("%Y-%m-%d")
        entries = journal.read_journal(date=date_str)
        for entry in entries:
            if _is_pending_action(entry) or _is_flagged_observation(entry, FLAG_TAGS):
                open_items.append({**entry, "_source_date": date_str})
    return open_items

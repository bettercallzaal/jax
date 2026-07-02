"""
MaintainX CMMS API client.

Requires: MAINTAINX_API_TOKEN (Bearer token — Premium plan only)
Endpoint: https://api.getmaintainx.com/v1/

The v1 API is cursor-paginated (limit + cursor -> nextCursor) and rate-limited
(429 with Retry-After). Status/priority enums are uppercase on the wire
(OPEN, IN_PROGRESS, ON_HOLD, DONE / HIGH, MEDIUM, LOW, NONE); this module
lowercases them for the rest of the toolkit.
"""

import json
import time
import urllib.error
import urllib.request
from dataclasses import dataclass, asdict
from typing import Optional

MAINTAINX_BASE = "https://api.getmaintainx.com/v1"
WO_WEB_BASE = "https://app.getmaintainx.com/work-orders"

MAX_RETRIES = 4


class MaintainXError(Exception):
    pass


@dataclass
class WorkOrder:
    id: str
    title: str
    status: str
    priority: Optional[str]
    assignee: Optional[str]
    location: Optional[str]
    due_date: Optional[str]
    updated_at: str
    url: str
    description: Optional[str] = None
    asset_id: Optional[str] = None
    location_id: Optional[str] = None
    categories: Optional[list] = None


def _request(path: str, token: str, params: dict = None, timeout: int = 15) -> dict:
    url = f"{MAINTAINX_BASE}{path}"
    if params:
        from urllib.parse import urlencode
        url = f"{url}?{urlencode(params)}"
    req = urllib.request.Request(
        url,
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/json",
        },
    )

    for attempt in range(MAX_RETRIES + 1):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return json.loads(resp.read().decode())
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < MAX_RETRIES:
                retry_after = e.headers.get("Retry-After")
                delay = float(retry_after) if retry_after else 2 ** (attempt + 1)
                time.sleep(min(delay, 60))
                continue
            body = e.read().decode(errors="replace")
            raise MaintainXError(f"HTTP {e.code} from MaintainX: {body[:200]}") from e
        except urllib.error.URLError as e:
            if attempt < MAX_RETRIES:
                time.sleep(2 ** (attempt + 1))
                continue
            raise MaintainXError(f"Network error reaching MaintainX: {e.reason}") from e

    raise MaintainXError("Retries exhausted")


def _parse_wo(raw: dict) -> WorkOrder:
    assignees = raw.get("assignees") or []
    first = assignees[0] if assignees else {}
    assignee = first.get("name") or (f"{first.get('type', '')} {first.get('id', '')}".strip() or None) if first else None

    loc = raw.get("location") or {}
    location = loc.get("name") if isinstance(loc, dict) else (str(loc) if loc else None)

    cats = raw.get("categories") or []
    categories = [c.get("name", str(c)) if isinstance(c, dict) else str(c) for c in cats]

    return WorkOrder(
        id=str(raw.get("id", "")),
        title=raw.get("title", "(no title)"),
        status=str(raw.get("status", "unknown")).lower(),
        priority=str(raw.get("priority") or "none").lower(),
        assignee=assignee,
        location=location,
        due_date=raw.get("dueDate"),
        updated_at=raw.get("updatedAt", ""),
        url=f"{WO_WEB_BASE}/{raw.get('id', '')}",
        description=raw.get("description"),
        asset_id=str(raw["assetId"]) if raw.get("assetId") else None,
        location_id=str(raw["locationId"]) if raw.get("locationId") else None,
        categories=categories or None,
    )


def fetch_open_work_orders(
    api_token: str,
    statuses: tuple = ("OPEN", "IN_PROGRESS", "ON_HOLD"),
    timeout: int = 15,
    max_pages: int = 40,
) -> list[WorkOrder]:
    """Fetch open WOs from MaintainX, following the nextCursor chain."""
    results: list[WorkOrder] = []
    cursor: Optional[str] = None

    for _ in range(max_pages):
        params: dict = {"limit": 100}
        # The API accepts repeated/comma status filters; send uppercase enums.
        params["status"] = ",".join(s.upper() for s in statuses)
        if cursor:
            params["cursor"] = cursor

        data = _request("/workorders", api_token, params=params, timeout=timeout)

        raw_wos = data.get("workOrders") or data.get("data") or []
        for raw in raw_wos:
            results.append(_parse_wo(raw))

        cursor = data.get("nextCursor")
        if not cursor:
            break

    return results


def snapshot_work_orders(api_token: str, path: str, **kwargs) -> int:
    """Fetch open WOs and write them to a JSON snapshot file. Returns the count."""
    wos = fetch_open_work_orders(api_token, **kwargs)
    with open(path, "w") as f:
        json.dump([asdict(w) for w in wos], f, indent=1)
    return len(wos)

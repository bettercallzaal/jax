"""
MaintainX CMMS API client.

Requires: MAINTAINX_API_TOKEN (Bearer token — Premium plan only)
Endpoint: https://api.getmaintainx.com/v1/
"""

import json
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from typing import Optional

MAINTAINX_BASE = "https://api.getmaintainx.com/v1"
WO_WEB_BASE = "https://app.getmaintainx.com/work-orders"


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


def _request(path: str, token: str, params: dict = None, timeout: int = 10) -> dict:
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
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="replace")
        raise MaintainXError(f"HTTP {e.code} from MaintainX: {body[:200]}") from e
    except urllib.error.URLError as e:
        raise MaintainXError(f"Network error reaching MaintainX: {e.reason}") from e


def _parse_wo(raw: dict) -> WorkOrder:
    assignees = raw.get("assignees") or []
    assignee = assignees[0].get("name") if assignees else None

    loc = raw.get("location") or {}
    location = loc.get("name") if isinstance(loc, dict) else str(loc) if loc else None

    return WorkOrder(
        id=str(raw.get("id", "")),
        title=raw.get("title", "(no title)"),
        status=raw.get("status", "unknown").lower(),
        priority=(raw.get("priority") or "none").lower(),
        assignee=assignee,
        location=location,
        due_date=raw.get("dueDate"),
        updated_at=raw.get("updatedAt", ""),
        url=f"{WO_WEB_BASE}/{raw.get('id', '')}",
    )


def fetch_open_work_orders(
    api_token: str,
    statuses: tuple = ("open", "in_progress"),
    timeout: int = 10,
) -> list[WorkOrder]:
    """Fetch open and in-progress WOs from MaintainX, paginating through all results."""
    results: list[WorkOrder] = []
    page = 1

    while True:
        params = {"status": ",".join(statuses), "page": page, "pageSize": 50}
        data = _request("/workorders", api_token, params=params, timeout=timeout)

        raw_wos = data.get("workOrders") or []
        if not raw_wos:
            break

        for raw in raw_wos:
            results.append(_parse_wo(raw))

        if not data.get("nextPage"):
            break
        page += 1

    return results

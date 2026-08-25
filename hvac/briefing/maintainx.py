"""
MaintainX CMMS API client.

Requires: MAINTAINX_API_TOKEN (Bearer token — Premium plan and up; generated
at Settings > Integrations > API Keys in the MaintainX web app)
Endpoint: https://api.getmaintainx.com/v1/

The v1 API is cursor-paginated for work orders (limit + cursor -> nextCursor;
parts/assets/purchase orders use offset pagination instead) and rate-limited
per MaintainX's published limits: 100 req/60s per user, 500 req/60s per org
(429 with Retry-After). Status/priority enums are uppercase on the wire
(OPEN, IN_PROGRESS, ON_HOLD, DONE / HIGH, MEDIUM, LOW, NONE); this module
lowercases them for the rest of the toolkit.

If the account's token is scoped to multiple organizations, pass org_id to
send the required x-organization-id header (a 400 comes back otherwise).

Confirmed write support: create a work order (POST /workorders) and update
its status (PATCH /workorders/{id}/status). Comment and attachment endpoints
also exist in the v1 API but their exact request shape hasn't been confirmed
against JAX's account yet (docs site 403s automated fetches) — do not build
against add_comment/add_attachment without verifying against a real token
first.
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


def _request(
    path: str,
    token: str,
    params: dict = None,
    method: str = "GET",
    body: dict = None,
    org_id: Optional[str] = None,
    timeout: int = 15,
) -> dict:
    url = f"{MAINTAINX_BASE}{path}"
    if params:
        from urllib.parse import urlencode
        url = f"{url}?{urlencode(params)}"

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
    }
    if org_id:
        headers["x-organization-id"] = org_id

    data = None
    if body is not None:
        data = json.dumps(body).encode()
        headers["Content-Type"] = "application/json"

    req = urllib.request.Request(url, data=data, headers=headers, method=method)

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


def create_work_order(
    api_token: str,
    title: str,
    description: Optional[str] = None,
    priority: Optional[str] = None,
    location_id: Optional[str] = None,
    asset_id: Optional[str] = None,
    assignee_ids: Optional[list] = None,
    due_date: Optional[str] = None,
    org_id: Optional[str] = None,
    timeout: int = 15,
) -> WorkOrder:
    """Create a work order via POST /workorders."""
    body: dict = {"title": title}
    if description:
        body["description"] = description
    if priority:
        body["priority"] = priority.upper()
    if location_id:
        body["locationId"] = location_id
    if asset_id:
        body["assetId"] = asset_id
    if assignee_ids:
        body["assigneeIds"] = list(assignee_ids)
    if due_date:
        body["dueDate"] = due_date

    data = _request(
        "/workorders", api_token, method="POST", body=body, org_id=org_id, timeout=timeout
    )
    return _parse_wo(data.get("workOrder") or data)


def update_work_order_status(
    api_token: str,
    work_order_id: str,
    status: str,
    org_id: Optional[str] = None,
    timeout: int = 15,
) -> WorkOrder:
    """Update a work order's status via PATCH /workorders/{id}/status.

    status is one of OPEN, IN_PROGRESS, ON_HOLD, DONE (case-insensitive).
    """
    data = _request(
        f"/workorders/{work_order_id}/status",
        api_token,
        method="PATCH",
        body={"status": status.upper()},
        org_id=org_id,
        timeout=timeout,
    )
    return _parse_wo(data.get("workOrder") or data)


def add_comment(api_token: str, work_order_id: str, text: str, org_id: Optional[str] = None) -> None:
    """Not yet wired up.

    MaintainX's v1 API has a comment-creation capability tied to a work order,
    but the exact endpoint path and payload shape haven't been confirmed
    against a real token (the docs site 403s automated fetches). Confirm the
    real shape — via the live docs or a test call — before implementing this.
    """
    raise NotImplementedError(
        "add_comment: MaintainX comment endpoint shape unconfirmed — see module docstring"
    )


def add_attachment(api_token: str, work_order_id: str, file_path: str, org_id: Optional[str] = None) -> None:
    """Not yet wired up.

    MaintainX's v1 API supports attaching files (application/octet-stream,
    binary payload) but the exact endpoint path hasn't been confirmed against
    a real token. Confirm the real shape before implementing this.
    """
    raise NotImplementedError(
        "add_attachment: MaintainX attachment endpoint shape unconfirmed — see module docstring"
    )

"""
JCI Metasys BAS REST API client (API v4).

Requires:
  METASYS_HOST      — base URL, e.g. https://bas.jax.org
  METASYS_USERNAME  — Metasys login
  METASYS_PASSWORD  — Metasys password
  METASYS_ALARM_PRIORITY_MAX — integer 0-255 (default 100; lower = more urgent)

Auth: POST /api/v4/login → JWT Bearer token → GET /api/v4/alarms
"""

import json
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Optional


class MetasysAuthError(Exception):
    pass


class MetasysError(Exception):
    pass


@dataclass
class MetasysAlarm:
    id: str
    alarm_message: str
    object_name: str
    priority: int
    is_acked: bool
    is_active: bool
    occurred_at: str
    area: Optional[str]


def _json_request(
    url: str,
    token: Optional[str] = None,
    body: Optional[dict] = None,
    timeout: int = 10,
) -> dict:
    data = json.dumps(body).encode() if body else None
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(url, data=data, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        body_text = e.read().decode(errors="replace")
        if e.code in (401, 403):
            raise MetasysAuthError(f"Metasys auth failed ({e.code}): {body_text[:200]}") from e
        raise MetasysError(f"HTTP {e.code} from Metasys: {body_text[:200]}") from e
    except urllib.error.URLError as e:
        raise MetasysError(f"Network error reaching Metasys: {e.reason}") from e


def get_jwt_token(host: str, username: str, password: str, timeout: int = 10) -> str:
    """Authenticate with Metasys and return a JWT access token."""
    url = f"{host.rstrip('/')}/api/v4/login"
    resp = _json_request(url, body={"username": username, "password": password}, timeout=timeout)
    token = resp.get("accessToken")
    if not token:
        raise MetasysAuthError("No accessToken in Metasys login response")
    return token


def fetch_active_alarms(
    host: str,
    token: str,
    priority_max: int = 100,
    timeout: int = 15,
) -> list[MetasysAlarm]:
    """Fetch active, unacknowledged alarms from Metasys up to the given priority threshold."""
    results: list[MetasysAlarm] = []
    base = host.rstrip("/")
    url = (
        f"{base}/api/v4/alarms"
        f"?alarmStates=active"
        f"&priorityRange=1,{priority_max}"
        f"&pageSize=200"
    )

    while url:
        resp = _json_request(url, token=token, timeout=timeout)
        items = resp.get("items") or []
        for item in items:
            area_obj = item.get("area") or {}
            area = area_obj.get("displayName") if isinstance(area_obj, dict) else None
            results.append(MetasysAlarm(
                id=str(item.get("id", "")),
                alarm_message=item.get("alarmCondition") or item.get("message") or "(no message)",
                object_name=item.get("objectName") or item.get("objectUrl") or "(unknown)",
                priority=int(item.get("priority", 999)),
                is_acked=bool(item.get("isAcknowledged", False)),
                is_active=bool(item.get("isActive", True)),
                occurred_at=item.get("alarmTime") or "",
                area=area,
            ))
        # Metasys paginates via 'next' link in response envelope
        url = resp.get("next")

    return results

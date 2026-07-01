"""
HVAC Morning Briefing — daily 7 AM digest of open WOs, journal items, and Metasys alarms.

Usage:
    python -m hvac.cli brief              # send email
    python -m hvac.cli brief --dry-run    # print to stdout, no email

Environment variables:
    MAINTAINX_API_TOKEN           Bearer token (MaintainX Premium)
    METASYS_HOST                  e.g. https://bas.jax.org
    METASYS_USERNAME
    METASYS_PASSWORD
    METASYS_ALARM_PRIORITY_MAX    integer 0-255, default 100
    SMTP_HOST                     required to send email
    SMTP_PORT                     default 587
    SMTP_USERNAME                 if relay requires auth
    SMTP_PASSWORD
    SMTP_FROM                     from address
    SMTP_TO                       comma-separated recipients
    SMTP_USE_TLS                  true/false, default true
    BRIEFING_TIMEZONE             IANA tz, default America/New_York
"""

import os
import sys

from .composer import assemble_briefing
from .emailer import EmailError, render_plain_text, send_briefing_email
from .journal_summary import get_open_items_across_journal, get_yesterday_summary
from .maintainx import MaintainXError, fetch_open_work_orders
from .metasys_api import MetasysAuthError, MetasysError, fetch_active_alarms, get_jwt_token


def _env(key: str, default: str = None) -> str:
    return os.environ.get(key, default)


def run_briefing(send_email: bool = True, dry_run: bool = False) -> int:
    tz_name = _env("BRIEFING_TIMEZONE", "America/New_York")

    # --- MaintainX ---
    work_orders = None
    mx_error = None
    mx_token = _env("MAINTAINX_API_TOKEN")
    if mx_token:
        try:
            work_orders = fetch_open_work_orders(mx_token)
        except MaintainXError as e:
            mx_error = str(e)
            print(f"[briefing] MaintainX error: {e}", file=sys.stderr)
    else:
        mx_error = "MAINTAINX_API_TOKEN not set"

    # --- Metasys ---
    alarms = None
    metasys_error = None
    metasys_host = _env("METASYS_HOST")
    if metasys_host:
        try:
            token = get_jwt_token(
                metasys_host,
                _env("METASYS_USERNAME", ""),
                _env("METASYS_PASSWORD", ""),
            )
            priority_max = int(_env("METASYS_ALARM_PRIORITY_MAX", "100"))
            alarms = fetch_active_alarms(metasys_host, token, priority_max=priority_max)
        except MetasysAuthError as e:
            metasys_error = f"Auth failed: {e}"
            print(f"[briefing] Metasys auth error: {e}", file=sys.stderr)
        except MetasysError as e:
            metasys_error = str(e)
            print(f"[briefing] Metasys error: {e}", file=sys.stderr)
    else:
        metasys_error = "METASYS_HOST not set"

    # --- Journal ---
    journal_summary = get_yesterday_summary()
    open_items = get_open_items_across_journal(days_back=7)

    # --- Assemble ---
    report = assemble_briefing(
        work_orders=work_orders,
        maintainx_error=mx_error,
        alarms=alarms,
        metasys_error=metasys_error,
        journal_summary=journal_summary,
        open_items=open_items,
        tz_name=tz_name,
    )

    plain_text = render_plain_text(report)

    if dry_run or not send_email:
        print(plain_text)
        return 0

    # --- Send ---
    smtp_host = _env("SMTP_HOST")
    smtp_from = _env("SMTP_FROM")
    smtp_to_raw = _env("SMTP_TO", "")

    if not smtp_host or not smtp_from or not smtp_to_raw:
        print("[briefing] SMTP not configured — printing to stdout instead.", file=sys.stderr)
        print(plain_text)
        return 0

    to_addrs = [a.strip() for a in smtp_to_raw.split(",") if a.strip()]
    smtp_port = int(_env("SMTP_PORT", "587"))
    use_tls = _env("SMTP_USE_TLS", "true").lower() not in ("false", "0", "no")

    try:
        send_briefing_email(
            report=report,
            smtp_host=smtp_host,
            smtp_port=smtp_port,
            from_addr=smtp_from,
            to_addrs=to_addrs,
            username=_env("SMTP_USERNAME"),
            password=_env("SMTP_PASSWORD"),
            use_tls=use_tls,
        )
        print(f"[briefing] Email sent to {', '.join(to_addrs)}")
        return 0
    except EmailError as e:
        print(f"[briefing] Failed to send email: {e}", file=sys.stderr)
        return 1

#!/usr/bin/env python3
"""
HVAC Field Toolkit CLI
Usage: python -m hvac.cli <command> [options]

Commands:
  diagnose-reheat   Diagnose a reheat system from readings
  diagnose-zone     Diagnose a zone comfort complaint
  log               Log a field observation
  journal           Show today's journal
  analyze           Analyze current warm-room scenario
  psych             Compute psychrometric state point
"""

import argparse
import sys
from . import diagnostics, journal, psychrometrics, analysis, rag
from .briefing import run_briefing


def cmd_diagnose_reheat(args):
    findings = diagnostics.diagnose_reheat(
        discharge_temp_f=args.discharge,
        reheat_output_pct=args.output,
        supply_air_temp_f=args.supply,
        hot_water_supply_f=args.hw_supply,
        hot_water_return_f=args.hw_return,
        control_signal_pct=args.signal,
        reheat_type=args.type,
    )
    diagnostics.print_findings(findings)

    # Also log readings to journal
    readings = {"discharge_temp_f": args.discharge, "reheat_output_pct": args.output}
    if args.hw_supply:
        readings["hw_supply_f"] = args.hw_supply
    if args.hw_return:
        readings["hw_return_f"] = args.hw_return
    journal.log_reading(zone=args.zone, readings=readings, equipment="reheat")
    print(f"\n[Logged to journal — zone: {args.zone}]")


def cmd_diagnose_zone(args):
    findings = diagnostics.diagnose_zone(
        zone=args.zone,
        room_temp_f=args.room_temp,
        setpoint_f=args.setpoint,
        discharge_temp_f=args.discharge,
        supply_cfm=args.cfm,
        design_cfm=args.design_cfm,
        co2_ppm=args.co2,
        relative_humidity_pct=args.rh,
    )
    diagnostics.print_findings(findings)
    journal.log_reading(
        zone=args.zone,
        readings={"room_temp_f": args.room_temp, "setpoint_f": args.setpoint},
        equipment="zone",
    )


def cmd_log(args):
    entry = journal.log_observation(
        zone=args.zone,
        description=args.description,
        tags=args.tags.split(",") if args.tags else [],
    )
    print(f"Logged: {entry['ts']} — {args.zone}")


def cmd_journal(args):
    entries = journal.read_today()
    journal.print_journal(entries)


def cmd_analyze(args):
    report = analysis.analyze_warm_room_reheat(
        zone=args.zone,
        room_temp_f=args.room_temp or 0,
        setpoint_f=args.setpoint,
        discharge_temp_f=args.discharge,
        reheat_output_pct=args.output,
        supply_cfm=args.cfm,
        mixed_air_temp_f=args.mixed_air,
        hot_water_supply_f=args.hw_supply,
        hot_water_return_f=args.hw_return,
    )
    analysis.print_analysis_report(report)

    # Auto-run reheat diagnostics too
    print("\n--- FAULT DIAGNOSTICS ---")
    findings = diagnostics.diagnose_reheat(
        discharge_temp_f=args.discharge,
        reheat_output_pct=args.output,
        hot_water_supply_f=args.hw_supply,
        hot_water_return_f=args.hw_return,
    )
    diagnostics.print_findings(findings)

    journal.log_observation(
        zone=args.zone,
        description=f"Analysis run: discharge={args.discharge}°F, reheat={args.output}%",
        readings={"discharge_temp_f": args.discharge, "reheat_pct": args.output},
        tags=["analysis", "reheat", "warm-room"],
    )


def cmd_ask(args):
    import os
    store = rag.build_store()
    if args.show_sources:
        results = rag.retrieve(args.question, store, top_k=args.top_k)
        rag.print_retrieved(results)
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("Error: ANTHROPIC_API_KEY environment variable not set.")
        print("Set it with: export ANTHROPIC_API_KEY=sk-ant-...")
        sys.exit(1)
    if args.stream:
        print()
        for chunk in rag.ask_stream(args.question, top_k=args.top_k, store=store):
            print(chunk, end="", flush=True)
        print()
    else:
        answer = rag.ask(args.question, top_k=args.top_k, store=store)
        print(f"\n{answer}\n")


def cmd_agent(args):
    import os
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("Error: ANTHROPIC_API_KEY environment variable not set.")
        print("Set it with: export ANTHROPIC_API_KEY=sk-ant-...")
        sys.exit(1)
    from . import agent
    if args.interactive or not args.question:
        agent.interactive()
    else:
        answer, _ = agent.run_agent(args.question, verbose=not args.quiet)
        print(f"\n{answer}")


def cmd_dat_review(args):
    import json
    from .briefing.dat_review import review_from_readings, format_report_lines

    with open(args.file) as f:
        raw = json.load(f)

    # Accept [{label, dat, sp_low, sp_high, flag}, ...] or the metasys_points format
    readings = []
    for row in raw:
        readings.append((
            row["label"],
            row.get("dat"),
            row.get("sp_low"),
            row.get("sp_high"),
            row.get("flag"),
        ))

    from datetime import date
    report = review_from_readings(readings, date=str(date.today()))
    for line in format_report_lines(report):
        print(line)


def cmd_maintainx_pull(args):
    import os
    from pathlib import Path
    from .briefing.maintainx import snapshot_work_orders, MaintainXError

    token = os.environ.get("MAINTAINX_API_TOKEN")
    if not token:
        print("Error: MAINTAINX_API_TOKEN environment variable not set.")
        print("Generate one in MaintainX: Settings > Integrations > + New Key")
        sys.exit(1)

    out = args.out or str(Path(__file__).parent / "data" / "maintainx_snapshot.json")
    try:
        count = snapshot_work_orders(token, out)
    except MaintainXError as e:
        print(f"MaintainX pull failed: {e}")
        sys.exit(1)
    print(f"Wrote {count} open work orders to {out}")


def cmd_maintainx_create(args):
    import os
    from .briefing.maintainx import create_work_order, MaintainXError

    token = os.environ.get("MAINTAINX_API_TOKEN")
    if not token:
        print("Error: MAINTAINX_API_TOKEN environment variable not set.")
        print("Generate one in MaintainX: Settings > Integrations > + New Key")
        sys.exit(1)

    org_id = os.environ.get("MAINTAINX_ORG_ID")
    try:
        wo = create_work_order(
            token,
            title=args.title,
            description=args.description,
            priority=args.priority.upper() if args.priority else None,
            due_date=args.due_date,
            org_id=org_id,
        )
    except MaintainXError as e:
        print(f"MaintainX create failed: {e}")
        sys.exit(1)

    print(f"Created work order #{wo.id}: {wo.title}")
    print(wo.url)
    print(
        "NOTE: JAX-required custom fields (GL Account, Maximo Worktype/Status, "
        "Category) are not set by this call — the API's custom-field support "
        "hasn't been confirmed yet. Open the WO in MaintainX and fill those in."
    )


def cmd_brief(args):
    sys.exit(run_briefing(
        send_email=not args.no_email,
        dry_run=args.dry_run,
    ))


def cmd_psych(args):
    psychrometrics.print_state_point(
        label=f"{args.zone or 'State Point'}",
        dry_bulb_f=args.dry_bulb,
        relative_humidity_pct=args.rh,
        altitude_ft=args.altitude,
    )


def main():
    parser = argparse.ArgumentParser(prog="hvac", description="HVAC Field Toolkit")
    sub = parser.add_subparsers(dest="command")

    # --- diagnose-reheat ---
    p = sub.add_parser("diagnose-reheat", help="Diagnose reheat faults")
    p.add_argument("--zone", default="Unknown Zone")
    p.add_argument("--discharge", type=float, required=True, help="Discharge air temp °F")
    p.add_argument("--output", type=float, required=True, help="Reheat output %%")
    p.add_argument("--supply", type=float, help="Supply air temp °F (AHU leaving)")
    p.add_argument("--hw-supply", type=float, help="Hot water supply temp °F")
    p.add_argument("--hw-return", type=float, help="Hot water return temp °F")
    p.add_argument("--signal", type=float, help="Control signal %%")
    p.add_argument("--type", default="hot_water", choices=["hot_water", "electric"])
    p.set_defaults(func=cmd_diagnose_reheat)

    # --- diagnose-zone ---
    p = sub.add_parser("diagnose-zone", help="Diagnose zone comfort")
    p.add_argument("--zone", required=True)
    p.add_argument("--room-temp", type=float, required=True)
    p.add_argument("--setpoint", type=float, default=72)
    p.add_argument("--discharge", type=float)
    p.add_argument("--cfm", type=float)
    p.add_argument("--design-cfm", type=float)
    p.add_argument("--co2", type=float)
    p.add_argument("--rh", type=float)
    p.set_defaults(func=cmd_diagnose_zone)

    # --- log ---
    p = sub.add_parser("log", help="Log a field observation")
    p.add_argument("--zone", required=True)
    p.add_argument("--description", required=True)
    p.add_argument("--tags", help="Comma-separated tags")
    p.set_defaults(func=cmd_log)

    # --- journal ---
    p = sub.add_parser("journal", help="Show today's journal")
    p.set_defaults(func=cmd_journal)

    # --- analyze ---
    p = sub.add_parser("analyze", help="Full warm-room/reheat analysis")
    p.add_argument("--zone", default="Unknown Zone")
    p.add_argument("--discharge", type=float, required=True)
    p.add_argument("--output", type=float, required=True, help="Reheat output %%")
    p.add_argument("--room-temp", type=float)
    p.add_argument("--setpoint", type=float, default=72)
    p.add_argument("--cfm", type=float)
    p.add_argument("--mixed-air", type=float, help="Mixed air temp °F")
    p.add_argument("--hw-supply", type=float)
    p.add_argument("--hw-return", type=float)
    p.set_defaults(func=cmd_analyze)

    # --- ask ---
    p = sub.add_parser("ask", help="Ask the HVAC knowledge base (RAG + Claude)")
    p.add_argument("question", help="Natural language question")
    p.add_argument("--top-k", type=int, default=5, help="Number of chunks to retrieve (default: 5)")
    p.add_argument("--show-sources", action="store_true", help="Print retrieved knowledge chunks")
    p.add_argument("--stream", action="store_true", help="Stream the response token by token")
    p.set_defaults(func=cmd_ask)

    # --- agent ---
    p = sub.add_parser("agent", help="Tool-using field agent (RAG + point map + journal + WOs)")
    p.add_argument("question", nargs="?", help="Question; omit for interactive mode")
    p.add_argument("-i", "--interactive", action="store_true", help="Interactive session")
    p.add_argument("--quiet", action="store_true", help="Hide tool-call trace")
    p.set_defaults(func=cmd_agent)

    # --- dat-review ---
    p = sub.add_parser("dat-review", help="Parse a DAT readings JSON file and flag outliers")
    p.add_argument("--file", required=True, help="JSON file with [{label, dat, sp_low, sp_high, flag}, ...]")
    p.set_defaults(func=cmd_dat_review)

    # --- maintainx-pull ---
    p = sub.add_parser("maintainx-pull", help="Pull open WOs from MaintainX API into a snapshot file")
    p.add_argument("--out", help="Output path (default: hvac/data/maintainx_snapshot.json)")
    p.set_defaults(func=cmd_maintainx_pull)

    # --- maintainx-create ---
    p = sub.add_parser("maintainx-create", help="Create a work order via the MaintainX API")
    p.add_argument("--title", required=True)
    p.add_argument("--description")
    p.add_argument("--priority", choices=["high", "medium", "low", "none"])
    p.add_argument("--due-date", dest="due_date", help="ISO date, e.g. 2026-07-17")
    p.set_defaults(func=cmd_maintainx_create)

    # --- brief ---
    p = sub.add_parser("brief", help="Send morning HVAC briefing email")
    p.add_argument("--dry-run", action="store_true", help="Print to stdout, do not send email")
    p.add_argument("--no-email", action="store_true", help="Assemble briefing but skip sending")
    p.set_defaults(func=cmd_brief)

    # --- psych ---
    p = sub.add_parser("psych", help="Psychrometric state point")
    p.add_argument("--dry-bulb", type=float, required=True)
    p.add_argument("--rh", type=float, required=True, help="Relative humidity %%")
    p.add_argument("--altitude", type=float, default=0)
    p.add_argument("--zone", help="Label")
    p.set_defaults(func=cmd_psych)

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)
    args.func(args)


if __name__ == "__main__":
    main()

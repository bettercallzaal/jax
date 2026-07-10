"""
HVAC field agent — a tool-using Claude loop over the toolkit.

Unlike `hvac ask` (single RAG retrieve + answer), the agent decides for itself
which tools to call and can chain them: look up a unit, pull field knowledge,
check the journal, log an observation, all in one question.

Requires: ANTHROPIC_API_KEY
Usage:
    python -m hvac.cli agent "why would B28 AHU-6 run 28 degrees high?"
    python -m hvac.cli agent -i          # interactive session
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Optional

from . import journal, rag

DATA_DIR = Path(__file__).parent / "data"
POINTS_FILE = DATA_DIR / "metasys_points.json"
MAINTAINX_SNAPSHOT = DATA_DIR / "maintainx_snapshot.json"

MODEL = "claude-opus-4-8"
MAX_TOKENS = 4096
MAX_TURNS = 12  # tool-loop safety cap


SYSTEM_PROMPT = """You are the field assistant for Zaal Panthaki, BAS Technician at \
The Jackson Laboratory (Bar Harbor campus). The site runs JCI Metasys (NAE/SNE \
engines, FAC/CGE/FEC/DX controllers) across ~64 campus AHUs, with MaintainX as \
the CMMS.

Style: short and direct. No filler, no horizontal rules, no corporate tone. \
Zaal is a technician in the field, often on a phone between mechanical rooms — \
lead with the answer, then the reasoning only if it matters.

DAT review thresholds: critical = DAT more than 10°F above setpoint, high = \
3-10°F above, low = more than 3°F below. Cooling lockout setpoints at JAX are \
typically 50-52°F.

Use your tools rather than guessing: search_knowledge for field lessons and \
diagnostic procedures, lookup_unit for point references and topology quirks, \
read_journal for what happened on a given day, list_work_orders for open WOs. \
Log observations to the journal when Zaal reports something worth keeping. \
If a tool comes back empty, say so plainly instead of inventing data."""


# ---------------------------------------------------------------------------
# Tool implementations
# ---------------------------------------------------------------------------

def _tool_search_knowledge(query: str, top_k: int = 4) -> str:
    store = rag.build_store()
    results = rag.retrieve(query, store, top_k=top_k)
    if not results:
        return "No matching knowledge chunks."
    parts = []
    for r in results:
        parts.append(f"[{r.chunk.source} | {r.chunk.topic}]\n{r.chunk.text}")
    return "\n\n---\n\n".join(parts)


def _tool_lookup_unit(query: str) -> str:
    if not POINTS_FILE.exists():
        return "Point map not found."
    data = json.loads(POINTS_FILE.read_text())
    q = query.lower()
    matches = [
        u for u in data.get("units", [])
        if q in u.get("label", "").lower()
        or q in u.get("building", "").lower()
        or q in u.get("ahu", "").lower()
    ]
    out = {}
    if matches:
        out["units"] = matches[:8]
    # Surface topology quirks / gotchas that mention the queried string
    meta = data.get("_meta", {})
    for section in ("topology_quirks", "point_gotchas"):
        hits = {
            k: v for k, v in meta.get(section, {}).items()
            if isinstance(v, str) and q.replace(" ", "") in v.lower().replace(" ", "")
        }
        if hits:
            out[section] = hits
    if not out:
        return f"No units or notes matching '{query}'."
    return json.dumps(out, indent=1)


def _tool_read_journal(date: Optional[str] = None) -> str:
    entries = journal.read_journal(date)
    if not entries:
        return f"No journal entries for {date or 'today'}."
    return json.dumps(entries, indent=1)


def _tool_log_observation(zone: str, description: str, tags: Optional[list] = None) -> str:
    entry = journal.log_observation(zone=zone, description=description, tags=tags or [])
    return f"Logged at {entry['ts']} — zone: {zone}"


def _tool_list_work_orders() -> str:
    if not MAINTAINX_SNAPSHOT.exists():
        return ("No MaintainX snapshot on disk. Pull one first with "
                "`hvac maintainx-pull` (needs MAINTAINX_API_TOKEN). "
                "Expected file: hvac/data/maintainx_snapshot.json")
    return MAINTAINX_SNAPSHOT.read_text()


SNAPSHOTS_DIR = DATA_DIR / "snapshots"


def _latest_snapshot(prefix: str) -> Optional[Path]:
    if not SNAPSHOTS_DIR.exists():
        return None
    files = sorted(SNAPSHOTS_DIR.glob(f"{prefix}_*.json"))
    return files[-1] if files else None


def _tool_get_dat_snapshot(date: Optional[str] = None) -> str:
    if date:
        matches = sorted(SNAPSHOTS_DIR.glob(f"dat_{date}*.json"))
        f = matches[-1] if matches else None
    else:
        f = _latest_snapshot("dat")
    if f is None:
        return "No DAT snapshot found. Snapshots live in hvac/data/snapshots/dat_<timestamp>.json"
    return f.read_text()


def _tool_get_valve_sweep(date: Optional[str] = None) -> str:
    if date:
        matches = sorted(SNAPSHOTS_DIR.glob(f"valves_{date}*.json"))
        f = matches[-1] if matches else None
    else:
        f = _latest_snapshot("valves")
    if f is None:
        return "No valve sweep snapshot found. Snapshots live in hvac/data/snapshots/valves_<timestamp>.json"
    return f.read_text()


def _tool_draft_work_order(
    title: str,
    description: str,
    building: str,
    priority: str = "Medium",
    category: str = "BAS",
) -> str:
    """Format a ready-to-paste MaintainX WO draft with the JAX required fields."""
    draft = f"""WORK ORDER DRAFT — paste into MaintainX

Title: {title}
Description: {description}
Location: {building}
Priority: {priority}
Category: {category}
Work Type: Reactive
MAXIMO WORKTYPE: CM
MAXIMO STATUS: APPR
GL ACCOUNT: 6026200-RLAB  <- VERIFY: first digits vary by campus end, suffix by work type (per Amy)
Assign to: Zaal Panthaki

Reminder: due date is required; default to today+7 unless urgent."""
    return draft


def _tool_create_work_order(
    title: str,
    description: str = "",
    priority: str = "Medium",
    due_date: str = None,
) -> str:
    """Create a work order directly in MaintainX via the API (needs MAINTAINX_API_TOKEN)."""
    import os
    from .briefing.maintainx import create_work_order, MaintainXError

    token = os.environ.get("MAINTAINX_API_TOKEN")
    if not token:
        return (
            "Can't create via API: MAINTAINX_API_TOKEN isn't set. Use draft_work_order "
            "instead and hand the draft to Amy, or set the token first."
        )

    try:
        wo = create_work_order(
            token,
            title=title,
            description=description or None,
            priority=priority,
            due_date=due_date,
            org_id=os.environ.get("MAINTAINX_ORG_ID"),
        )
    except MaintainXError as e:
        return f"MaintainX create failed: {e}"

    return (
        f"Created WO #{wo.id}: {wo.title}\n{wo.url}\n"
        "NOTE: JAX custom fields (GL Account, Maximo Worktype/Status, Category) are "
        "NOT set by this call — that field mapping hasn't been confirmed against the "
        "API yet. Open the WO in MaintainX and fill those in before assigning it out."
    )


TOOL_FUNCTIONS = {
    "search_knowledge": _tool_search_knowledge,
    "lookup_unit": _tool_lookup_unit,
    "read_journal": _tool_read_journal,
    "log_observation": _tool_log_observation,
    "list_work_orders": _tool_list_work_orders,
    "get_dat_snapshot": _tool_get_dat_snapshot,
    "get_valve_sweep": _tool_get_valve_sweep,
    "draft_work_order": _tool_draft_work_order,
    "create_work_order": _tool_create_work_order,
}

TOOLS = [
    {
        "name": "search_knowledge",
        "description": (
            "Search the HVAC field knowledge base (RAG): diagnostic procedures, "
            "documented JAX patterns (OAT lockouts, valve sweeps, reheat faults), "
            "psychrometrics, sequences. Use for any 'how do I diagnose X' or "
            "'what did we learn about Y' question."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Natural-language search query"},
                "top_k": {"type": "integer", "description": "Chunks to return (default 4)"},
            },
            "required": ["query"],
        },
    },
    {
        "name": "lookup_unit",
        "description": (
            "Look up campus AHUs in the Metasys point map by label, building, or "
            "unit name (e.g. 'B28', 'AHU-6', 'B55 AHU-3'). Returns point references, "
            "setpoint bands, notes, and any topology quirks (cross-building object "
            "mappings, naming traps) that mention the query."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Unit label, building, or AHU name"},
            },
            "required": ["query"],
        },
    },
    {
        "name": "read_journal",
        "description": "Read field journal entries for a date (YYYY-MM-DD). Omit date for today.",
        "input_schema": {
            "type": "object",
            "properties": {
                "date": {"type": "string", "description": "YYYY-MM-DD; omit for today"},
            },
        },
    },
    {
        "name": "log_observation",
        "description": (
            "Write a field observation to today's journal. Use when Zaal reports "
            "something worth keeping (a reading, a fix applied, a thing to check tomorrow)."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "zone": {"type": "string", "description": "Building/zone/unit, e.g. 'B28 AHU-6'"},
                "description": {"type": "string"},
                "tags": {"type": "array", "items": {"type": "string"}},
            },
            "required": ["zone", "description"],
        },
    },
    {
        "name": "list_work_orders",
        "description": "List open MaintainX work orders from the local snapshot file.",
        "input_schema": {"type": "object", "properties": {}},
    },
    {
        "name": "get_dat_snapshot",
        "description": (
            "Get the most recent campus DAT snapshot (all ~64 AHUs: discharge air temp, "
            "setpoint band, flags, AM comparison). Use for 'what's running hot', "
            "'how did X trend', or any question about current/recent DAT state."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "date": {"type": "string", "description": "YYYY-MM-DD to pick a specific day; omit for latest"},
            },
        },
    },
    {
        "name": "get_valve_sweep",
        "description": (
            "Get the most recent campus cooling-valve sweep (valve command/position, "
            "engine, DAT, flags per AHU) plus the plant-level analysis. Use for "
            "plant-vs-unit diagnosis and 'which valves are pinned' questions."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "date": {"type": "string", "description": "YYYY-MM-DD to pick a specific day; omit for latest"},
            },
        },
    },
    {
        "name": "draft_work_order",
        "description": (
            "Draft a MaintainX work order with all JAX-required fields filled in "
            "(GL account, Maximo worktype/status, category). Returns text to paste."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "title": {"type": "string"},
                "description": {"type": "string"},
                "building": {"type": "string", "description": "e.g. 'Building 55' or room like '55-2504'"},
                "priority": {"type": "string", "enum": ["High", "Medium", "Low", "None"]},
                "category": {"type": "string", "description": "Default BAS"},
            },
            "required": ["title", "description", "building"],
        },
    },
    {
        "name": "create_work_order",
        "description": (
            "Create a work order directly in MaintainX via the API (requires "
            "MAINTAINX_API_TOKEN). Only sets standard fields (title, description, "
            "priority, due date) — JAX's custom fields (GL Account, Maximo "
            "Worktype/Status, Category) still need to be filled in manually in the "
            "app afterward. If no token is set, falls back to telling the user to "
            "use draft_work_order instead."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "title": {"type": "string"},
                "description": {"type": "string"},
                "priority": {"type": "string", "enum": ["High", "Medium", "Low", "None"]},
                "due_date": {"type": "string", "description": "ISO date, e.g. 2026-07-17"},
            },
            "required": ["title"],
        },
    },
]


# ---------------------------------------------------------------------------
# Agent loop
# ---------------------------------------------------------------------------

def _execute_tool(name: str, tool_input: dict) -> str:
    fn = TOOL_FUNCTIONS.get(name)
    if fn is None:
        return f"Unknown tool: {name}"
    try:
        return fn(**tool_input)
    except Exception as e:
        return f"Tool error ({name}): {e}"


def run_agent(
    question: str,
    messages: Optional[list] = None,
    api_key: Optional[str] = None,
    verbose: bool = True,
) -> tuple[str, list]:
    """
    Run one agent turn (which may involve several tool calls).

    Returns (final_text, messages) — pass messages back in to continue the
    conversation with context intact.
    """
    import anthropic

    client = anthropic.Anthropic(api_key=api_key or os.environ.get("ANTHROPIC_API_KEY"))

    if messages is None:
        messages = []
    messages.append({"role": "user", "content": question})

    final_text = ""
    for _ in range(MAX_TURNS):
        response = client.messages.create(
            model=MODEL,
            max_tokens=MAX_TOKENS,
            thinking={"type": "adaptive"},
            system=[{
                "type": "text",
                "text": SYSTEM_PROMPT,
                "cache_control": {"type": "ephemeral"},
            }],
            tools=TOOLS,
            messages=messages,
        )

        # Preserve the full content (including thinking blocks) for replay
        messages.append({"role": "assistant", "content": response.content})

        text_parts = [b.text for b in response.content if b.type == "text"]
        if text_parts:
            final_text = "\n".join(text_parts)

        if response.stop_reason != "tool_use":
            break

        tool_results = []
        for block in response.content:
            if block.type != "tool_use":
                continue
            if verbose:
                arg_str = json.dumps(block.input)
                print(f"  [{block.name} {arg_str[:90]}]", flush=True)
            result = _execute_tool(block.name, block.input)
            tool_results.append({
                "type": "tool_result",
                "tool_use_id": block.id,
                "content": result,
            })
        messages.append({"role": "user", "content": tool_results})
    else:
        final_text = final_text or "(Hit the tool-loop cap without a final answer.)"

    return final_text, messages


def interactive(api_key: Optional[str] = None) -> None:
    """REPL: keeps conversation context across questions."""
    print("HVAC field agent — Ctrl-D or 'q' to quit.")
    messages: list = []
    while True:
        try:
            question = input("\nyou> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not question or question.lower() in ("q", "quit", "exit"):
            break
        answer, messages = run_agent(question, messages=messages, api_key=api_key)
        print(f"\n{answer}")

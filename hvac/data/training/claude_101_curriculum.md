# Claude 101 — for Wayne

A short, practical course on using Claude day to day, built from Anthropic's own
prompting guidance and the Claude Cookbook, grounded in real examples from the HVAC
toolkit rather than generic ones. See `sources.md` for the source material.

## Module 1 — What Claude actually is

Claude is a conversational AI you talk to like a new employee: smart, capable, but
with zero context on your norms, your buildings, or how JAX does things until you
give it that context. The more precisely you explain what you want, the better the
result.

**Golden rule:** if a colleague with no background on the task would be confused by
your instruction, Claude will be too. Vague in, vague out.

## Module 2 — Be clear and direct

Say exactly what you want, including format and constraints. Don't rely on Claude to
guess "above and beyond" — ask for it explicitly.

- Less effective: "Look into this alarm."
- More effective: "Room 1007 in B32 is showing a Low Alarm on Sterile Storage Room
  Pressure. Check the exhaust damper trend and tell me if the loop is maxed out or
  if there's still room to fix it."

## Module 3 — Give it context, not just instructions

Explaining *why* gets you a better answer than just stating the rule, because Claude
can generalize from the reasoning instead of pattern-matching the literal words.

- Less effective: "Don't say the unit is fixed."
- More effective: "Don't say a unit is fixed until we've verified it with real field
  data (delta-T, temp gun, or a live trend) — a Metasys change alone isn't proof."

## Module 4 — Use examples when you want a specific format

If you want output in a certain shape (a WO comment, a journal entry, a specific
report layout), show 1-3 examples of what "good" looks like. Claude will match the
pattern far more reliably than from a description alone.

## Module 5 — Tell it when you want action, not just advice

Claude follows instructions literally. "Can you look at this?" often gets analysis
only. "Fix this" or "make the change" gets an actual action. If you want it to just
research and report back, say that instead — don't assume it'll infer which one you
meant.

## Module 6 — Ground it in real data, don't let it guess

This is the single most important habit for BAS work: Claude should pull from actual
data (Metasys readings, the journal, the point map, past work orders) rather than
answer from general HVAC knowledge alone. That's exactly what the `troubleshoot`
skill in this repo already does — it checks known campus quirks and journal history
*before* running any diagnostic, so the answer is grounded in this specific building,
not a generic textbook answer.

## Module 7 — Worked example: try the `troubleshoot` skill

The fastest way to learn this is to use it on a real complaint. Next time something
comes in:

1. Describe it in plain language — building/room, what's wrong. No need for Metasys
   terms.
2. Claude will check for known quirks and journal history on that zone first, so you
   find out immediately if this is a repeat issue.
3. It'll ask you for only the specific readings the next step actually needs, and
   tell you exactly which Metasys screen to check to get them.
4. It runs the same decision-tree diagnostics Zaal's toolkit uses, and turns the
   result into 2-3 concrete next actions — not a wall of jargon.

This mirrors exactly how the Rm 1530 "Breezeway Office" and Sterile Storage Room
Pressure cases got worked this week: check known context first, ask only for what's
needed next, verify with real data before calling anything fixed.

## Module 8 — Guardrails: what Claude will and won't do on its own

Without being told otherwise, Claude is cautious about anything hard to reverse or
that affects shared systems — it'll ask before things like pushing changes, deleting
files, or messaging people on your behalf. You can tighten or loosen this by saying
so explicitly. Good habit: if you're ever unsure whether something Claude did was
reversible, ask it directly — it'll tell you straight.

## Further reading (self-paced, deeper dive)

- Anthropic's official prompting best practices — the source for most of this module
- [Anthropic's Interactive Prompt Engineering Tutorial](https://github.com/anthropics/prompt-eng-interactive-tutorial)
  — 9 short chapters with exercises and an answer key, beginner → advanced
- [Claude Cookbook](https://platform.claude.com/cookbook) — real worked examples,
  including an "SRE Incident Response Agent" pattern that's basically the same shape
  as `troubleshoot`
- [DAIR.AI — Introduction to Prompt Engineering](https://academy.dair.ai/courses/introduction-prompt-engineering)
- [DeepLearning.AI course catalog](https://www.deeplearning.ai/courses) — look for
  the agents/prompting courses
- [Anthropic Skilljar](https://anthropic.skilljar.com/) — official Claude courses

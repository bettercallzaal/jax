> Fetched from https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices
> Filtered to the parts relevant to a non-developer using Claude in chat (not the API). Full page covers a lot of API-level detail (thinking budgets, subagent orchestration internals, prefill migration) that's dev-focused and left out here.

## Be clear and direct

Claude responds well to clear, explicit instructions. Being specific about your
desired output helps. If you want "above and beyond" behavior, ask for it explicitly
rather than hoping Claude infers it from a vague prompt.

Think of Claude as a brilliant but new employee who lacks context on your norms and
workflows. The more precisely you explain what you want, the better the result.

**Golden rule:** show your prompt to a colleague with minimal context on the task and
ask them to follow it. If they'd be confused, Claude will be too.

- Be specific about the desired output format and constraints.
- Give instructions as sequential steps (numbered/bulleted) when order matters.

Example — less effective: "Create an analytics dashboard"
Example — more effective: "Create an analytics dashboard. Include as many relevant
features and interactions as possible. Go beyond the basics to create a
fully-featured implementation."

## Add context to improve performance

Explaining *why* you want something helps Claude generalize correctly, instead of
just pattern-matching the literal instruction.

Example — less effective: "NEVER use ellipses"
Example — more effective: "Your response will be read aloud by a text-to-speech
engine, so never use ellipses since the engine won't know how to pronounce them."

## Use examples effectively

A few well-crafted examples (few-shot prompting) is one of the most reliable ways to
steer output format, tone, and structure. Make examples relevant (mirror the real
use case), diverse (cover edge cases so Claude doesn't overfit to one pattern), and
clearly separated from instructions. 3-5 examples is a good target.

## Give Claude a role

Setting a role — even one sentence — focuses Claude's tone and behavior for your use
case. E.g. "You are a helpful coding assistant specializing in Python."

## Tool use — be explicit about wanting action

Claude follows instructions precisely. "Can you suggest some changes?" often gets you
suggestions, not changes. "Change this function to improve its performance" gets you
an actual edit. If you want action taken by default rather than just advice, say so.

## Balancing autonomy and safety

Without guidance, an agentic Claude may take actions that are hard to reverse or
affect shared systems (deleting files, pushing code, messaging people). If you want
confirmation before anything risky, say so explicitly — this is exactly the kind of
guardrail worth setting up before handing Claude any real responsibility.

## Avoiding hallucinations / grounding answers

For tasks over real documents/data, ask Claude to quote or cite the relevant source
material before answering, rather than answering from memory. This is the same
principle behind the HVAC toolkit's RAG knowledge base — ground the answer in the
actual campus data (journal, point map, past WOs) instead of letting the model guess.

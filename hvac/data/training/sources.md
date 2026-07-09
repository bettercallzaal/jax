# Claude 101 — source material

Sources gathered for building `claude_101_curriculum.md`. Three fetched cleanly,
three blocked the fetch (bot-blocking, not a content issue) — listed as
further-reading links instead.

## Fetched successfully

1. **Claude prompting best practices** (Anthropic, official docs)
   https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices
   Full text saved: `sources/claude-prompting-best-practices.md`
   Core beginner-relevant techniques: be clear and direct, add context/motivation,
   use examples (few-shot), give Claude a role, tell it what TO do instead of what
   NOT to do, be explicit when you want action taken vs. just a suggestion, ask it
   to ground answers in the source material instead of guessing. Most of the page
   is API-level detail (thinking budgets, subagent orchestration, prefill migration)
   that's developer-focused, not relevant for day-to-day chat use — filtered out of
   the curriculum.

2. **Claude Cookbook** (Anthropic)
   https://platform.claude.com/cookbook
   Full category list saved: `sources/claude-cookbook-categories.md`
   Business/ops-relevant patterns worth pointing to: SRE Incident Response Agent
   (read logs, find root cause), Data Analyst Agent (turn data into reports),
   Customer Service Agent, Multi-agent Coordination. These map directly onto what
   the `troubleshoot` skill already does for BAS complaints.

3. **Anthropic's Prompt Engineering Interactive Tutorial** (GitHub)
   https://github.com/anthropics/prompt-eng-interactive-tutorial
   Structure saved: `sources/prompt-eng-interactive-tutorial-structure.md`
   9 chapters (Beginner: Basic Prompt Structure, Being Clear and Direct, Assigning
   Roles. Intermediate: Separating Data from Instructions, Formatting Output,
   Precognition/Chain-of-Thought, Using Examples. Advanced: Avoiding Hallucinations,
   Building Complex Prompts) + an appendix (Chaining Prompts, Tool Use, Search &
   Retrieval). Each chapter has exercises with an answer key — good self-paced
   follow-up after the internal curriculum.

## Blocked (403 — bot-blocking, listed as further reading)

4. **DAIR.AI — Introduction to Prompt Engineering**
   https://academy.dair.ai/courses/introduction-prompt-engineering
5. **DeepLearning.AI course catalog**
   https://www.deeplearning.ai/courses
6. **Anthropic Skilljar** (official Claude courses)
   https://anthropic.skilljar.com/

These three are legitimate, well-regarded resources — just couldn't be fetched
programmatically. Worth opening directly in a browser if the internal curriculum
below isn't enough and Wayne wants a deeper, self-paced course.

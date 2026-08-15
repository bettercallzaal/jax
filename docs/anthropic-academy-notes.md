# Anthropic Academy — Claude 101 Notes

Running notes from Zaal's Skilljar course (Claude 101), captured as lessons are shared.

## Lesson: Your first conversation with Claude

**Estimated time:** 20 minutes

**Learning objectives:**
- Start a new conversation with Claude and navigate the interface
- Write effective prompts using clear, specific language
- Upload files and images to provide Claude with additional context
- Use follow-up messages to iterate and refine Claude's responses

**Key takeaways:**
- Claude is a collaborator — it brings AI intelligence, you bring the context and expertise that makes the work meaningful.
- Talk to Claude like a coworker: naturally, concisely, conversationally.
- Before a conversation, consider three things:
  1. **Setting the stage** — your role, objectives, relevant context
  2. **Defining the task** — the specific action you want (write, analyze, build, etc.)
  3. **Specifying rules** — style, tone, format, examples
- Uploading documents/images gives Claude a shortcut to understand your needs — supported types include PDF, DOCX, CSV, TXT, PNG, JPEG.
- The real power comes from continued, iterative conversation, not one-off prompts.

**Iterating on responses:**
- Ask follow-up questions to build on a response
- Give feedback on tone/content to redirect
- Redirect/restart if Claude goes the wrong direction
- Can edit a previous message (pencil icon) to refine and resubmit rather than adding a new message

**Personalization features:**
- **Memory** — automatically saves context (role, preferences, past decisions, working style) across conversations; reviewable/editable in Settings; syncs across devices.
- **Styles** — customize how Claude communicates (concise, formal, explanatory, or a custom style); applies across all conversations once set.

**Framework reference:** the "setting the stage / defining the task / specifying rules" prompt structure is adapted from the 4D Framework for AI Fluency (Delegation, Description, Discernment, Diligence) — Rick Dakan (Ringling College of Art and Design) and Joseph Feller (University College Cork).

## Lesson: Getting better results

**Estimated time:** 15 minutes

**Learning objectives:**
- Recognize common challenges when starting out with AI and use troubleshooting techniques to overcome them
- Define AI Fluency and know where to go to learn more
- Explain how to set up evals to understand how Claude performs on your unique workflows

**Common challenges and fixes:**
| Challenge | What's happening | Fix |
|---|---|---|
| Response too generic | Prompt lacked context about your specific situation | Add audience, role, constraints — be specific rather than vague |
| Response too long/short | Claude guessed at length | Be explicit: "two-paragraph summary," "under 100 words," "length isn't a concern" |
| Wrong format | Claude understood the content but not the presentation | Show an example format or describe structure explicitly |
| Confident but wrong info | Claude can generate plausible-but-incorrect facts, especially niche topics | Verify high-stakes facts independently, ask for sources/confidence level, enable web search |
| Wrong tone | Claude defaults to helpful/professional | Describe the tone directly, or give an example of the style wanted |

**Iteration mindset:**
- First prompt rarely produces a perfect result — that's normal, treat it as the start of a conversation
- Treat first drafts as starting points, then refine
- Give specific feedback ("cut the first two paragraphs and make the conclusion more action-oriented") rather than vague feedback ("make it shorter")
- Know when to start fresh — sometimes a new chat with a clearer prompt beats redirecting a derailed conversation

**AI Fluency — the 4D Framework** (Rick Dakan, Ringling College of Art and Design; Joseph Feller, University College Cork):
- **Delegation** — deciding what work goes to humans vs. AI, and how to distribute tasks
- **Description** — communicating effectively with AI (defining outputs, guiding process, specifying behavior)
- **Discernment** — critically evaluating AI outputs for quality, accuracy, appropriateness
- **Diligence** — using AI responsibly/ethically, staying transparent, taking accountability for AI-assisted work

The Lesson 2 prompt framework (setting the stage/defining the task/specifying rules) is rooted in Description; the troubleshooting table above draws on Discernment and Diligence.

**Evals — evaluating Claude for your own workflows:**
- Evals = systematic ways to test how well Claude performs on tasks that matter to you specifically
- Why: your work is unique — Claude may excel at one task type and need more guidance on another; evals show where Claude adds the most value, where you need to add more context/examples, and build confidence for recurring tasks
- Simple eval approach:
  1. Gather 5-10 examples of a task you already do (emails, reports, analyses)
  2. Write test prompts that would generate similar outputs, including natural context
  3. Compare Claude's outputs to your originals — does it capture key info? Is tone/style right? What's missing?
  4. Refine your prompts/examples based on what you learn, and identify where human review is still essential

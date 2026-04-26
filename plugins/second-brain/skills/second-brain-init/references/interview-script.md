# Interview script

Use when no existing material is available — the user is starting fresh. Ask the questions in order. Batch 2-3 per message; do not ask one at a time, that's tedious.

## Questions

| # | Question | Maps to | Notes |
|---|---|---|---|
| 1 | "What should we call this knowledge base?" | `projectName` | Short, human-readable. Default to the target directory name if obvious. |
| 2 | "In one line, what is this knowledge base about?" | `schema.domain` | Push for specifics. "Research" is bad; "AI alignment papers and author notes" is good. |
| 3 | "What kinds of things will pages usually be about? (e.g. papers, authors, methods)" | `schema.entityTypes` | Comma-separated. 3-6 items is typical. Optional — if user shrugs, skip. |
| 4 | "What's a question you'll want this to answer well? (e.g. 'What has X said about Y?')" | `schema.commonQueries` | One or two examples is plenty. Shapes how the assistant structures pages. Optional. |
| 5 | "Will you use Obsidian, or do you want plain markdown links?" | `wiki.linkStyle` | Obsidian → `wikilinks`. Anything else (Logseq, Foam, plain editor) → `markdown`. Default `wikilinks`. |
| 6 | "Where should I create it?" | CLI `--directory` flag | Only ask if not already implied by context. Default to current dir. |

## Defaults to use silently

Do not ask about these unless the user volunteers a preference:

- `defaultAgent`: `"claude-code"` (since this skill runs in Claude Code).
- `categories`: `[]` (empty — built-in entities/concepts/topics are usually enough).
- `wiki.frontmatter`: `true`.
- `wiki.pageNaming`: `"title-case"`.
- `sourceHandling.mode`: `"user-directed"`.
- `schema.styleGuide`: leave undefined; `normalizeConfig` fills in a sensible default.
- Git init: `true` unless the user says no.

## Tone

Brief and conversational, not survey-like. After 2-3 questions, summarize what's been captured before continuing. If the user gives a vague answer, push once for specificity ("Can you give me an example?") then accept what they say.

## Example interaction

> **Skill:** A few quick questions to set up your knowledge base.
> 
> 1. What should we call it?
> 2. In one line, what's it about?
> 3. What kinds of things will pages usually be about? (e.g. papers, authors, methods — or skip if you're not sure yet.)
> 
> **User:** Call it "AI Alignment Research". It's a place to track papers, authors, and the arguments they make. Pages will mostly be about papers, authors, and concepts.
> 
> **Skill:** Got it. Two more:
> 
> 4. What's a question you'd want this to answer well?
> 5. Will you use Obsidian, or do you prefer plain markdown links?
> 
> **User:** "What has [author] said about [concept]?". I use Obsidian.
> 
> **Skill:** Here's the config I'd write — confirm or tell me what to change:
> 
> ```json
> {
>   "projectName": "AI Alignment Research",
>   "defaultAgent": "claude-code",
>   "schema": {
>     "domain": "AI alignment papers, authors, and the arguments they make",
>     "entityTypes": ["papers", "authors", "concepts"],
>     "commonQueries": ["What has [author] said about [concept]?"]
>   },
>   "wiki": { "linkStyle": "wikilinks" }
> }
> ```

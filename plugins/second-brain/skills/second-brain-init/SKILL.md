---
name: second-brain-init
description: This skill should be used when the user asks to "set up a second-brain", "create a knowledge base", "initialize second-brain", "build a personal wiki", "organize my notes into a wiki", or "start a second brain". Conducts a brief interview (or ingests an existing folder), writes a `.second-brain.json` config, and invokes the `second-brain` CLI to scaffold the project. Do NOT activate for "set up Obsidian", "create a new note", "make a wiki page", or queries about an *existing* knowledge base ("show me my notes", "what's in my second-brain").
version: 0.1.0
---

# second-brain-init

Set up a `second-brain` knowledge base by gathering the user's intent, writing a complete config, and invoking the `second-brain` CLI to scaffold the project. The CLI is the source of truth for the file layout and the assistant contract; this skill is the conversational front-end that produces a good config.

## When to act

Activate on phrases like:

- "Set up a second-brain"
- "Create a knowledge base for [topic]"
- "Build me a personal wiki"
- "Initialize second-brain in [folder]"
- "I want a second brain for my [research / journal / notes]"
- "Help me start organizing my notes"

Do not activate when the user is asking about an *existing* second-brain project. For status queries, run `second-brain doctor` directly via Bash. For content queries ("what do we know about X?"), read the relevant `wiki/` files directly — the assistant contract in `AGENTS.md` / `CLAUDE.md` covers that flow.

## Workflow

Follow this sequence end-to-end. Skip the wizard built into the CLI — drive it from `--config` instead, so the conversation happens here.

### 1. Pre-flight: confirm the CLI is installed

Run `which second-brain` via Bash. If absent, stop and tell the user how to install it (point at `https://github.com/mrelph/second-brain`). Do not attempt `npm install -g` automatically — that mutates global state and may need sudo. Resume only after the user confirms install.

### 2. Discover the current config schema

Always run `second-brain init --print-schema` and parse the JSON output before drafting a config. Do not rely on prior knowledge of the schema — fields evolve. The schema is small enough to fit in context. Read enum values, required fields, and descriptions from it.

If `--print-schema` fails (older CLI version, non-JSON output, exit code != 0), fall back to the shapes in `references/example-configs.md` and warn the user that the CLI may be out of date — suggest `npm install -g github:mrelph/second-brain` to update before continuing.

### 3. Choose mode: interview or ingest

Branch based on context:

- **Interview mode** (default): the user is starting fresh, no existing notes folder. Conduct the interview from `references/interview-script.md`.
- **Ingest mode**: the user pointed at a folder of existing material (e.g. "set up a second-brain for the notes in `~/journal`"). Read 5-15 representative files, infer config fields from observed patterns, then **show the inferred config and ask the user to confirm or tweak**. Heuristics in `references/ingest-heuristics.md`.

When in doubt, default to interview. Mixing — e.g., ingesting for context but still asking 1-2 confirming questions — is fine.

### 4. Construct the JSON config

Build a `.second-brain.json` matching the schema exactly. Fields that materially shape the assistant's behavior:

- `projectName` (required): human-readable name; appears in headings.
- `defaultAgent`: in this skill context, default to `"claude-code"` unless the user names a different assistant. Show enum values from the schema if asked.
- `schema.domain`: one-line description of what the KB is about. Be specific ("AI alignment papers and author notes" beats "research").
- `schema.entityTypes`: array of recurring kinds of pages (e.g., `["papers", "authors", "methods"]`). Strong defaults make the assistant smarter at extraction.
- `schema.commonQueries`: array of sample questions the wiki should answer well. Shapes how the assistant structures pages.
- `wiki.linkStyle`: `"wikilinks"` for Obsidian-friendly `[[Page]]`, `"markdown"` for portable `[Page](page.md)`. Default to wikilinks unless the user explicitly wants portability.

Other fields (`categories`, `wiki.frontmatter`, `wiki.pageNaming`, `sourceHandling.mode`, `schema.styleGuide`) have sensible defaults — don't ask about them unless the user volunteers a preference. Sample shapes for common domains in `references/example-configs.md`.

### 5. Show the config and confirm

Before invoking the CLI, present the JSON to the user and ask for confirmation. This is the **last reversible point** — once `init` runs, files exist on disk. Format as a markdown code block, point out the values most likely to surprise (e.g., link style, agent), and ask if anything should change.

### 6. Run the CLI

The config must be on disk before the CLI can read it. Write it via the **Write tool** (not via Bash heredoc — strings inside the JSON may contain special characters that break heredoc quoting). Write to a path *outside* the target directory, since the CLI rejects non-empty target dirs.

```
1. Compute a temp path:    Bash → TMPCFG=$(mktemp); echo "$TMPCFG"
   (Don't use --suffix=.json — it's GNU-only and breaks on macOS. The CLI
   doesn't care about the file extension.)
2. Write the config JSON:  Write tool → file_path=<the mktemp path>, content=<JSON>
3. Invoke the CLI:         Bash → second-brain init --config "$TMPCFG" --directory <target>
```

Default `<target>` to the current working directory if the user didn't specify one. Pass `--no-git` only if the user said they don't want git tracking. The CLI creates the target directory if it doesn't exist.

If the CLI errors (e.g., target dir not empty), surface the error verbatim and ask the user how to proceed (move to a new directory? use `--force`? clean the dir manually?). Do not pass `--force` unless the user explicitly approves it. **Exception:** a target dir containing only `.git` from a prior `git init` is still considered non-empty by the CLI; mention this if it's the cause and ask the user to confirm before passing `--force`.

### 7. Hand off to the user

After successful init, summarize what was created (3-5 lines max), then point the user at three concrete next actions:

1. Drop notes/PDFs/links into `sources/inbox/`.
2. Open the folder in their AI assistant.
3. Ask the assistant to "ingest my inbox" or "what do we know about [X]?".

Mention that the assistant will read the generated `AGENTS.md` / `CLAUDE.md` for instructions, and that the user can edit the "Project Customizations" block in that file to add personal preferences. The contract has three preserved blocks — managed (CLI-owned, refreshed on `second-brain upgrade`), Project Customizations (user-owned), and Assistant Observations (assistant's working memory across sessions). Both user and assistant blocks survive upgrades.

## What this skill does NOT do

Be deliberate about scope. This skill is for **setup**. After the CLI runs, the assistant's contract (in the generated instruction file) takes over. Specifically, do not:

- Maintain the wiki yourself in this skill — that's the assistant's ongoing job, governed by the contract.
- Run `second-brain upgrade` or `doctor` from this skill — those are user-initiated commands the assistant can run via Bash directly.
- Pre-populate `wiki/` with content during setup. The CLI scaffolds empty folders by design; first content comes from the user's sources.

If the user asks to "set up AND ingest these files in one step", do the setup first via this skill, then suggest the user follow up with "now ingest my inbox" — which the assistant handles via the contract, not via this skill.

## Additional resources

### Reference files

- **`references/interview-script.md`** — the question flow for interview mode, with field mappings and example user responses.
- **`references/ingest-heuristics.md`** — how to infer config fields from a folder of existing material; what to read, what signals matter.
- **`references/example-configs.md`** — sample `.second-brain.json` shapes for common domains (research, journal, recipes, engineering notes).

# second-brain (Claude Code plugin)

A Claude Code plugin that turns "set up a second-brain for X" into a working knowledge base.

When activated, the bundled `second-brain-init` skill conducts a brief interview (or ingests an existing folder of notes), drafts a `.second-brain.json` config, and runs the [`second-brain` CLI](https://github.com/mrelph/second-brain) to scaffold the project structure and the assistant instruction file.

## What this plugin is

A conversational front-end for the `second-brain` CLI. The CLI does the actual scaffolding and owns the prose template that governs how the assistant maintains the wiki. This plugin owns the *interview/ingest* step — the part that's better as a conversation with Claude than as a wizard or a stack of `--flag` arguments.

## Prerequisites

The `second-brain` CLI must be installed and on `PATH`. The plugin checks for it at the start of the workflow and stops with install instructions if it's missing.

```sh
# Install via npm (requires Node ≥ 20.10)
npm install -g github:mrelph/second-brain

# Or download a prebuilt binary
# https://github.com/mrelph/second-brain/releases
```

Verify with `second-brain --version` (should report 0.2.0 or later — the plugin uses the `--config` and `--print-schema` surface added in 0.2.0).

## Installation

This repo is its own single-plugin marketplace. Install with two slash commands inside any Claude Code session:

```
/plugin marketplace add mrelph/second-brain-plugin
/plugin install second-brain@second-brain-marketplace
```

Restart the session (or `/plugin reload`) to activate. Verify with `/plugin list` — `second-brain` should appear and the `second-brain-init` skill should fire on phrases like "set up a second-brain for X".

### Local development

```sh
# Clone, then point the marketplace add at the local path
git clone https://github.com/mrelph/second-brain-plugin.git
# In Claude Code:
#   /plugin marketplace add ./second-brain-plugin
#   /plugin install second-brain@second-brain-marketplace
```

## Usage

In any Claude Code session, just describe what you want:

> "Set up a second-brain in `~/notes/research` for AI alignment papers."
>
> "I want a knowledge base for my recipes."
>
> "Build me a personal wiki for journal entries."

The skill activates, conducts a 2-3 message interview, shows you the JSON config it would write, asks for confirmation, then invokes the CLI. After init, the generated `AGENTS.md` / `CLAUDE.md` takes over — the assistant maintains the wiki from there based on its instructions.

If you point at an existing folder, the skill switches to ingest mode:

> "Set up a second-brain for the notes in `~/journal` — they're already there."

It reads representative files, infers domain / entity types / link style from what's there, and presents a draft config for you to confirm or tweak.

## What it doesn't do

- **Maintain the wiki.** That's the assistant's ongoing job after `init` runs, governed by the instruction file the CLI writes.
- **Run `upgrade` or `doctor`.** Those are CLI commands the assistant invokes via Bash directly when you ask for them — no skill needed.
- **Ingest source material into pages during setup.** First content comes from the user's sources after init.

## Architecture

```
┌──────────────────────┐      ┌─────────────────────┐      ┌──────────────────────┐
│  This plugin         │      │  second-brain CLI   │      │  Generated project   │
│  (interview/ingest)  ├─────▶│  init --config      ├─────▶│  AGENTS.md / etc.    │
└──────────────────────┘      └─────────────────────┘      └──────────────────────┘
       writes JSON                  scaffolds files            assistant takes over
```

Single source of truth for the prose template lives in the CLI. This plugin only writes the JSON.

## License

MIT

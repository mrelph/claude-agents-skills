# CLAUDE.md

Claude Code plugin marketplace: a curated collection of installable plugins (skills + agents), published via `/plugin marketplace add mrelph/claude-agents-skills`.

## Layout

- `.claude-plugin/marketplace.json` — machine-readable catalog; every published plugin has an entry here (name, source, version, keywords, category)
- `plugins/<name>/` — the published plugins (tax-preparation, portfolio-analyzer, retirement-planner, research-consolidator, hockey-lineup-builder, second-brain)
  - `.claude-plugin/plugin.json` — manifest (name, description, version, author, repository, license, keywords)
  - `skills/<skill-name>/SKILL.md` — skill definitions; optional `references/`, `scripts/`, `examples/`, `README.md`
- `Skills/`, `Agents/` — legacy personal items, NOT published to the marketplace; keep for reference, don't extend
- `staging/` — templates for new contributions (`skill-template/`, `agent-template.md`)
- `releases/plugins/*.zip` — committed pre-v2.0.0 distribution packages (gitignore has an exception for them)
- Root tooling: `add-to-marketplace.py` (scaffold + catalog entry), `marketplace-cli.py` (list/search/info/install/validate), `package-plugins.py` (build release zips)
- Docs: `README.md` (catalog tables), `MARKETPLACE.md` (integration guide), `CONTRIBUTING.md` (authoritative plugin format spec), `CHANGELOG.md`

## Authoring conventions (match existing files)

SKILL.md frontmatter used by published plugins:

```yaml
---
name: skill-name            # kebab-case, matches its directory name
description: This skill should be used when the user asks to "..." (quoted trigger phrases; newer skills also list negative triggers)
allowed-tools: Read, Bash, WebSearch, Write, AskUserQuestion
metadata:
  version: 1.0.0
  last-updated: YYYY-MM-DD
---
```

(second-brain uses a top-level `version:` instead of `metadata:` — the template/CONTRIBUTING format above is the standard.)

Agent frontmatter (Agents/ and staging template): `name`, `description`, `model: sonnet`, `color`, `category`, `allowed-tools`.

- All intra-plugin file paths in SKILL.md/agent files MUST use `${CLAUDE_PLUGIN_ROOT}/` (never relative or repo-relative paths) — they break after installation otherwise.
- Valid marketplace categories: `financial`, `research`, `development`, `design`, `planning`, `domain-specific`.
- Names: lowercase kebab-case, unique within the marketplace.

## Gotchas

- A version bump touches multiple places: `plugins/<name>/.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`, the README catalog table, and `CHANGELOG.md`. Keep them in sync.
- `marketplace-cli.py install` just copies the plugin dir to `.claude/plugins/<name>` (or `--target`); the primary install path is Claude Code's `/plugin install <name>@mrelph/claude-agents-skills`. There is no symlink-to-~/.claude mechanism.
- `.claude/settings.local.json` is machine-specific and gitignored — leave it untracked.
- Run `./marketplace-cli.py validate` after editing marketplace.json.
- Work happens on feature branches merged via PR (see git history); don't commit directly to main without asking.

# Contributing to Claude Agents & Skills Plugin Marketplace

Thank you for your interest in contributing. This guide covers the v2.0.0 plugin format used by the marketplace. All new contributions must follow this format to be installable via `/plugin install`.

## Plugin Format Overview

Each plugin lives in its own directory under `plugins/` and follows this structure:

```
plugins/your-plugin-name/
├── .claude-plugin/
│   └── plugin.json          # Required: plugin manifest
├── skills/                  # Skills provided by this plugin (if any)
│   └── your-skill-name/
│       ├── SKILL.md         # Main skill definition
│       └── README.md        # Human-readable documentation
├── agents/                  # Agents provided by this plugin (if any)
│   └── your-agent-name.md   # Agent definition
├── references/              # Supporting reference documents (optional)
├── scripts/                 # Python utility scripts (optional)
├── examples/                # Example data files (optional)
└── README.md                # Plugin-level documentation
```

A plugin must contain at least one skill or agent. Plugins may contain both.

## Step 1: Create the Plugin Directory

```bash
mkdir -p plugins/your-plugin-name/.claude-plugin
mkdir -p plugins/your-plugin-name/skills/your-plugin-name
# Add agents directory if needed
mkdir -p plugins/your-plugin-name/agents
```

## Step 2: Add the plugin.json Manifest

Create `plugins/your-plugin-name/.claude-plugin/plugin.json`:

```json
{
  "name": "your-plugin-name",
  "description": "One-sentence description of what this plugin does",
  "version": "1.0.0",
  "author": { "name": "your-github-username" },
  "repository": "https://github.com/mrelph/claude-agents-skills",
  "license": "MIT",
  "keywords": ["keyword1", "keyword2", "keyword3"]
}
```

**Required fields:**

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Kebab-case plugin identifier, unique in the marketplace |
| `description` | string | One-sentence description for the plugin catalog |
| `version` | string | Semantic version (`MAJOR.MINOR.PATCH`) |
| `author` | object | `{ "name": "github-username" }` |
| `repository` | string | Repository URL |
| `license` | string | SPDX license identifier (use `MIT` for this repo) |
| `keywords` | array | 3–8 tags that help users discover the plugin |

## Step 3: Add Skills

Create a skill definition at `plugins/your-plugin-name/skills/your-skill-name/SKILL.md`:

```yaml
---
name: your-skill-name
description: Brief description of what the skill does
allowed-tools: Read, Bash, WebSearch, Write
metadata:
  version: 1.0.0
  last-updated: 2026-01-01
---

# Your Skill Name

[Skill instructions and workflow...]
```

**Critical requirement — use `${CLAUDE_PLUGIN_ROOT}/` for all file paths.**

Any references to files within the plugin (reference documents, scripts, examples) must use the `${CLAUDE_PLUGIN_ROOT}/` variable so that Claude Code can resolve them regardless of where the plugin is installed:

```markdown
<!-- Correct -->
Read the reference at ${CLAUDE_PLUGIN_ROOT}/references/guide.md
Run the script at ${CLAUDE_PLUGIN_ROOT}/scripts/calculator.py

<!-- Wrong — will break after installation -->
Read the reference at plugins/your-plugin-name/references/guide.md
Read the reference at ./references/guide.md
```

Include a `README.md` alongside `SKILL.md` with human-readable documentation, usage examples, and a description of the skill's capabilities.

## Step 4: Add Agents (if applicable)

Create agent definition files under `plugins/your-plugin-name/agents/`:

```markdown
---
name: your-agent-name
description: What this agent specializes in
model: sonnet
color: blue
allowed-tools: Read, Write, Bash, Grep, Glob
---

# Your Agent Name

[Agent purpose, expertise areas, workflow, and behavioral guidelines...]
```

Agent markdown files use the same `${CLAUDE_PLUGIN_ROOT}/` convention if they reference any plugin files.

## Step 5: Add to marketplace.json

Add an entry for your plugin in the root `marketplace.json` under the `plugins` array:

```json
{
  "name": "your-plugin-name",
  "source": "./plugins/your-plugin-name",
  "description": "One-sentence description matching plugin.json",
  "version": "1.0.0",
  "author": { "name": "your-github-username" },
  "keywords": ["keyword1", "keyword2", "keyword3"],
  "category": "development"
}
```

**Valid categories:**

- `financial` — Tax, investing, retirement, budgeting
- `research` — Analysis, synthesis, reporting
- `development` — Software development tools, workflows, agents
- `design` — UX/UI, visual design, accessibility
- `planning` — Roadmaps, feature planning, project management
- `domain-specific` — Specialized use cases

## Plugin Naming Conventions

- Plugin names must be lowercase and kebab-case (e.g., `tax-preparation`, `dev-tools`)
- Names must be unique within the marketplace
- Skill and agent names inside the plugin should follow the same convention
- Keywords should be specific (e.g., `postgresql` not `database`, `irs` not `government`)

## Versioning

Use [Semantic Versioning](https://semver.org/):

- `1.0.0` — Initial release
- `1.1.0` — New features, backward compatible
- `1.2.0` — Additional features, backward compatible
- `2.0.0` — Breaking changes (restructured paths, renamed skills, changed behavior)

Both the `plugin.json` and the `marketplace.json` entry must have matching version values.

## Plugin Structure Requirements

A valid plugin must meet all of the following:

- `plugins/your-plugin-name/.claude-plugin/plugin.json` exists and is valid JSON
- All required fields are present in `plugin.json`
- At least one skill in `skills/` or at least one agent in `agents/` exists
- All intra-plugin file references in SKILL.md and agent files use `${CLAUDE_PLUGIN_ROOT}/`
- An entry exists in the root `marketplace.json`
- A `README.md` exists at the plugin root level

## Testing Your Plugin

Before submitting a pull request, validate the plugin locally:

```bash
# Check that plugin.json is valid JSON
jq empty plugins/your-plugin-name/.claude-plugin/plugin.json && echo "Valid JSON"

# Validate that marketplace.json is valid JSON with your entry
jq '.plugins[] | select(.name == "your-plugin-name")' marketplace.json

# Verify no hardcoded paths exist in skill definitions
grep -r "\./Skills\|\.claude/skills\|plugins/your-plugin-name/" \
  plugins/your-plugin-name/skills/ \
  && echo "WARNING: Hardcoded paths found — replace with \${CLAUDE_PLUGIN_ROOT}/"

# Install and test locally in Claude Code
/plugin validate .
/plugin install .
```

Verify the installed plugin works as expected by running through a representative use case before opening a pull request.

## Submitting a Pull Request

1. Fork the repository and create a branch from `main`
2. Follow all steps above to create your plugin
3. Run the validation checks
4. Open a pull request with:
   - A clear title describing the plugin (e.g., `Add legal-research plugin`)
   - A description of what the plugin does and who it's for
   - Confirmation that you tested the plugin locally

## Code of Conduct

- Be respectful and constructive in all interactions
- Test your contributions before submitting
- Follow existing patterns and conventions
- Provide complete documentation — undocumented plugins will not be accepted
- Do not include personal data, API keys, or sensitive information in any plugin file

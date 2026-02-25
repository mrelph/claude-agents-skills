# Claude Code Skills

Comprehensive skill modules with supporting scripts and reference documentation that extend Claude Code's capabilities with domain expertise.

## Available Skills

| Skill | Version | Description |
|-------|---------|-------------|
| [tax-preparation](tax-preparation/) | v1.4.0 | US tax preparation, deduction analysis, form processing, tax optimization |
| [portfolio-analyzer](portfolio-analyzer/) | v2.3.0 | Investment portfolio analysis, performance metrics, strategic recommendations |
| [retirement-planner](retirement-planner/) | v1.0.0 | Retirement readiness assessment, Social Security optimization, Monte Carlo simulations |
| [amazon-rsu-tax-calculations](amazon-rsu-tax-calculations/) | v1.0.0 | Amazon RSU cost basis correction, capital gains calculation, Form 8949 adjustments |
| [research-consolidator](research-consolidator/) | v1.0.0 | Synthesize research from multiple AI models and sources into comprehensive reports |
| [kiro-spec-driven-development](kiro-spec-driven-development/) | v1.0.0 | Spec-driven development workflow: requirements, design, and task planning |
| [jr-kraken-18u-navy-lineup](jr-kraken-18u-navy-lineup/) | v1.0.0 | Hockey team lineup generation and game strategy planning |

## Usage

### Installing a Skill

Copy the skill folder to your project's `.claude/skills/` directory:

```bash
# Example: Install tax-preparation skill
cp -r Skills/tax-preparation /path/to/project/.claude/skills/
```

The skill will be automatically available in Claude Code conversations.

### Invoking a Skill

Skills can be invoked by name in conversation:

```
Use the tax-preparation skill to analyze my W-2 and find deductions.
```

Or via the Skill tool directly.

## Skill Structure

Each skill follows a consistent directory structure:

```
skill-name/
├── SKILL.md              # Main skill definition (required)
├── README.md             # Human-readable documentation
├── references/           # Domain knowledge documents
│   ├── guide.md
│   └── ...
└── scripts/              # Python utility scripts
    ├── README.md
    ├── calculator.py
    └── ...
```

### SKILL.md Format

The main skill file uses YAML frontmatter:

```yaml
---
name: skill-name
description: Brief description of what the skill does
allowed-tools: Read, Bash, WebSearch, Write, AskUserQuestion
metadata:
  version: 1.0.0
  last-updated: 2025-01-01
  target-users: description of intended users
---

# Skill Name

[Detailed workflow, instructions, and guidance...]
```

### Key Frontmatter Fields

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Unique skill identifier |
| `description` | Yes | Brief summary for skill selection |
| `allowed-tools` | Yes | Tools the skill can access |
| `metadata.version` | No | Semantic version number |
| `metadata.last-updated` | No | Last modification date |
| `metadata.target-users` | No | Intended audience |

## Skill Categories

### Financial Skills

These skills work together for comprehensive financial planning:

```
portfolio-analyzer ─┬─► retirement-planner
                    └─► tax-preparation
```

| Skill | Focus |
|-------|-------|
| **portfolio-analyzer** | Investment analysis, performance, recommendations |
| **retirement-planner** | Pre-retirement planning, Social Security, withdrawals |
| **tax-preparation** | Tax optimization, deductions, form processing |

**Integration points:**
- Portfolio data feeds into retirement projections
- Tax-loss harvesting coordinated across skills
- Roth conversion analysis spans portfolio and tax skills

### Research Skills

| Skill | Focus |
|-------|-------|
| **research-consolidator** | Multi-source synthesis with confidence scoring |

### Domain-Specific Skills

| Skill | Focus |
|-------|-------|
| **jr-kraken-18u-navy-lineup** | Hockey team lineup and strategy |

## Creating New Skills

### 1. Create the Directory Structure

```bash
mkdir -p Skills/my-skill/{references,scripts}
```

### 2. Create SKILL.md

```markdown
---
name: my-skill
description: What this skill does
allowed-tools: Read, Bash, Write, AskUserQuestion
metadata:
  version: 1.0.0
  last-updated: 2025-01-01
---

# My Skill

## Overview
[What the skill does and when to use it...]

## Workflow
1. [Step one...]
2. [Step two...]
3. [Step three...]

## Reference Documents
- `references/guide.md` - [When to load...]

## Scripts
- `scripts/calculator.py` - [What it does...]

## Limitations
[What the skill cannot or should not do...]
```

### 3. Add Reference Documents

Place domain knowledge in `references/`:

```markdown
# Reference Guide

[Detailed information the skill needs to perform its task...]
```

### 4. Add Utility Scripts

Place Python helpers in `scripts/`:

```python
#!/usr/bin/env python3
"""Script description."""

import argparse
import json

def main():
    parser = argparse.ArgumentParser(description='...')
    # ...

if __name__ == '__main__':
    main()
```

### 5. Create README.md

Document the skill for human readers:

```markdown
# Skill Name

**Version:** 1.0.0

## Overview
[Human-friendly description...]

## Installation
[How to install...]

## Usage
[Example invocations...]

## Scripts
[Documentation for each script...]
```

## Best Practices

### Skill Design

1. **Single responsibility**: Each skill should have a focused domain
2. **Progressive disclosure**: Load reference docs only when needed
3. **User clarification**: Use AskUserQuestion for ambiguous inputs
4. **Version tracking**: Maintain version numbers and changelogs

### Tool Selection

| Tool | Use Case |
|------|----------|
| `Read` | Loading files, PDFs, documents |
| `Bash` | Running Python scripts |
| `WebSearch` | Real-time data, current information |
| `WebFetch` | Specific URL content |
| `Write` | Creating reports, saving results |
| `Task` | Delegating to specialized agents |
| `Skill` | Invoking related skills |
| `AskUserQuestion` | Clarifying user intent |

### Reference Documents

- Keep focused on actionable information
- Use tables and lists for quick reference
- Include examples where helpful
- Update when domain knowledge changes

### Python Scripts

- Use argparse for CLI interfaces
- Support JSON output for data exchange
- Include helpful descriptions
- Handle errors gracefully

## Troubleshooting

### Skill Not Found

Ensure the skill is in `.claude/skills/` and has a valid `SKILL.md` with proper frontmatter.

### Scripts Not Running

Check that Python is available and scripts have proper shebang lines.

### Reference Documents Not Loading

Verify file paths in SKILL.md match actual file locations.

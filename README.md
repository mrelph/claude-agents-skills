# Claude Code Agents & Skills

A curated collection of specialized agents and skills for [Claude Code](https://docs.anthropic.com/en/docs/claude-code), extending Claude's capabilities with domain expertise and task automation.

## What's Included

### 🤖 Agents (8)

Specialized task-focused agents that can be spawned for specific development and business tasks:

| Agent | Purpose |
|-------|---------|
| [bug-tracker-resolver](Agents/bug-tracker-resolver.md) | Manages bugs, performs root cause analysis, implements fixes |
| [database-architect](Agents/database-architect.md) | PostgreSQL/Supabase schema design, query optimization, RLS policies |
| [documentation-maintainer](Agents/documentation-maintainer.md) | Creates and updates project documentation |
| [performance-optimizer](Agents/performance-optimizer.md) | Core Web Vitals, bundle size, runtime efficiency |
| [roadmap-feature-planner](Agents/roadmap-feature-planner.md) | Strategic feature planning and roadmap tracking |
| [security-code-scanner](Agents/security-code-scanner.md) | Vulnerability identification, OWASP Top 10 analysis |
| [ux-ui-design-expert](Agents/ux-ui-design-expert.md) | UX/UI guidance, accessibility, responsive design |
| [video-integration-specialist](Agents/video-integration-specialist.md) | YouTube/Vimeo integration, streaming optimization |

### 🛠️ Skills (5)

Comprehensive skill modules with supporting scripts and reference documentation:

| Skill | Version | Description |
|-------|---------|-------------|
| [research-consolidator](Skills/research-consolidator/) | v1.0.0 | Synthesize research from multiple AI models and sources |
| [tax-preparation](Skills/tax-preparation/) | v1.3.0 | US tax preparation, deduction analysis, document processing |
| [portfolio-analyzer](Skills/portfolio-analyzer/) | v2.3.0 | Investment analysis, performance metrics, recommendations |
| [retirement-planner](Skills/retirement-planner/) | v1.0.0 | Retirement readiness, Social Security optimization, Monte Carlo simulations |
| [jr-kraken-18u-navy-lineup](Skills/jr-kraken-18u-navy-lineup/) | v1.0.0 | Hockey team lineup generation and game strategy |

## Installation

### Using Skills in Claude Code

1. Copy the skill folder to your project's `.claude/skills/` directory:
   ```bash
   cp -r Skills/tax-preparation /path/to/your/project/.claude/skills/
   ```

2. The skill will be automatically available in Claude Code conversations.

### Using Agents in Claude Code

1. Copy the agent markdown file to your project's `.claude/agents/` directory:
   ```bash
   mkdir -p /path/to/your/project/.claude/agents/
   cp Agents/database-architect.md /path/to/your/project/.claude/agents/
   ```

2. Alternatively, add agent definitions to your Claude Code configuration.

## Repository Structure

```
claude-agents-skills/
├── README.md                    # This file
├── Agents/                      # Agent definitions
│   ├── README.md                # Agents overview and usage
│   ├── bug-tracker-resolver.md
│   ├── database-architect.md
│   └── ...
├── Skills/                      # Skill modules
│   ├── README.md                # Skills overview and usage
│   ├── research-consolidator/
│   │   ├── SKILL.md             # Main skill definition
│   │   ├── README.md            # Skill documentation
│   │   ├── references/          # Domain knowledge
│   │   └── scripts/             # Python utilities
│   ├── tax-preparation/
│   ├── portfolio-analyzer/
│   ├── retirement-planner/
│   └── jr-kraken-18u-navy-lineup/
└── .gitignore
```

## Skill Anatomy

Each skill follows a consistent structure:

```
skill-name/
├── SKILL.md              # Main skill definition (required)
│                         # Contains: name, description, allowed-tools, workflow
├── README.md             # Human-readable documentation
├── references/           # Domain knowledge documents
│   ├── guide.md          # Reference materials
│   └── ...
└── scripts/              # Python utility scripts
    ├── README.md         # Script documentation
    ├── calculator.py     # Utility scripts
    └── ...
```

### SKILL.md Format

```yaml
---
name: skill-name
description: Brief description of what the skill does
allowed-tools: Read, Bash, WebSearch, Write, AskUserQuestion
metadata:
  version: 1.0.0
  last-updated: 2025-01-01
---

# Skill Name

[Skill instructions and workflows...]
```

## Agent Anatomy

Each agent is a single markdown file with YAML frontmatter:

```yaml
---
name: agent-name
description: What this agent specializes in
model: sonnet
color: blue
allowed-tools: Read, Write, Bash, Grep, Glob, Task
---

# Agent Name

[Agent instructions, expertise areas, and behavior guidelines...]
```

## Integration Between Skills

Some skills are designed to work together:

- **portfolio-analyzer** → **retirement-planner**: Portfolio data flows into retirement projections
- **portfolio-analyzer** → **tax-preparation**: Tax-loss harvesting and cost basis coordination
- **retirement-planner** → **tax-preparation**: Roth conversion and withdrawal tax planning

## Contributing

To add a new skill or agent:

1. Follow the existing structure patterns
2. Include comprehensive documentation
3. Add appropriate `.gitignore` entries for data directories
4. Test with Claude Code before submitting

## License

MIT License - Feel free to use and adapt these skills and agents for your own projects.

## Resources

- [Claude Code Documentation](https://docs.anthropic.com/en/docs/claude-code)
- [Claude Code Skills Guide](https://docs.anthropic.com/en/docs/claude-code/skills)
- [Anthropic API Documentation](https://docs.anthropic.com/en/api)

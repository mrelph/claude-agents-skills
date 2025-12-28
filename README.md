# Claude Code Agents & Skills Marketplace

A curated collection of specialized agents and skills for [Claude Code](https://docs.anthropic.com/en/docs/claude-code), extending Claude's capabilities with domain expertise and task automation.

## Marketplace Catalog

This repository includes a machine-readable `marketplace.json` catalog that enables programmatic discovery and installation of agents and skills.

📖 **[Full Marketplace Integration Guide →](MARKETPLACE.md)**

The catalog includes:

- Complete metadata for all agents and skills
- Installation commands and directory structures
- Version tracking and update history
- Categorization and tagging
- Integration mappings between skills
- Usage statistics and compatibility information

### Using the Marketplace Catalog

The `marketplace.json` file can be consumed by:

- **Claude Code integrations** - Automated discovery and installation
- **CLI tools** - Browse and install agents/skills via command line
- **Web frontends** - Build marketplace UIs for browsing
- **CI/CD pipelines** - Automated testing and deployment
- **Package managers** - Integration with existing tooling

Example: Programmatically list all financial skills:

```bash
jq '.categories.skills.financial[] | {id, name, version}' marketplace.json
```

Example: Get installation command for a specific agent:

```bash
jq '.categories.agents.development[] | select(.id=="database-architect") | .install_command' marketplace.json
```

### Marketplace CLI Tool

A Python CLI tool is included for easy browsing and installation:

```bash
# List all items
./marketplace-cli.py list

# List only agents or skills
./marketplace-cli.py list agents
./marketplace-cli.py list skills

# Search for items
./marketplace-cli.py search security
./marketplace-cli.py search finance

# Show detailed information
./marketplace-cli.py info database-architect
./marketplace-cli.py info tax-preparation

# Install an agent or skill
./marketplace-cli.py install database-architect
./marketplace-cli.py install portfolio-analyzer --target /path/to/.claude/skills/

# Show marketplace statistics
./marketplace-cli.py stats
```

The CLI tool automatically:
- Creates target directories if they don't exist
- Detects whether to install as agent or skill
- Shows detailed metadata and features
- Handles installation conflicts

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

### Install as Plugin Marketplace (Recommended)

Install the entire marketplace in Claude Code to browse and install agents/skills on demand:

```bash
/plugin install https://github.com/yourusername/claude-agents-skills
```

Once installed, the marketplace will be available in your Claude Code plugin manager.

### Manual Installation

#### Using Skills in Claude Code

1. Copy the skill folder to your project's `.claude/skills/` directory:
   ```bash
   cp -r Skills/tax-preparation /path/to/your/project/.claude/skills/
   ```

2. The skill will be automatically available in Claude Code conversations.

#### Using Agents in Claude Code

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
├── MARKETPLACE.md               # Marketplace integration guide
├── marketplace.json             # Catalog (root copy)
├── marketplace-cli.py           # CLI tool for browsing/installing
├── .claude-plugin/              # Plugin marketplace structure
│   └── marketplace.json         # Catalog (plugin copy)
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

## Marketplace API

The `marketplace.json` follows a structured format that supports various integration scenarios:

### JSON Schema

```json
{
  "name": "Marketplace name",
  "version": "Semantic version",
  "categories": {
    "agents": {
      "category_name": [/* agent objects */]
    },
    "skills": {
      "category_name": [/* skill objects */]
    }
  },
  "integrations": {
    "skill_connections": [/* integration mappings */]
  },
  "installation": {/* installation instructions */},
  "stats": {/* usage statistics */}
}
```

### Agent Object Schema

```json
{
  "id": "unique-identifier",
  "name": "Display Name",
  "description": "Brief description",
  "model": "sonnet|opus|haiku",
  "color": "UI color",
  "version": "1.0.0",
  "file": "path/to/agent.md",
  "allowed_tools": ["Tool1", "Tool2"],
  "install_command": "cp command",
  "tags": ["tag1", "tag2"]
}
```

### Skill Object Schema

```json
{
  "id": "unique-identifier",
  "name": "Display Name",
  "description": "Detailed description",
  "version": "1.0.0",
  "last_updated": "YYYY-MM-DD",
  "directory": "Skills/skill-name",
  "allowed_tools": ["Tool1", "Tool2"],
  "install_command": "cp -r command",
  "target_users": "audience description",
  "tags": ["tag1", "tag2"],
  "features": ["Feature 1", "Feature 2"],
  "scripts": ["script1.py"],
  "references": ["ref1.md"]
}
```

### Query Examples

**Find all agents that use a specific tool:**
```bash
jq '[.categories.agents[][] | select(.allowed_tools[] | contains("WebSearch"))]' marketplace.json
```

**List all skills with their versions:**
```bash
jq '[.categories.skills[][] | {name, version}]' marketplace.json
```

**Get integration dependencies for a skill:**
```bash
jq '.integrations.skill_connections[] | select(.from=="portfolio-analyzer")' marketplace.json
```

**Count items by category:**
```bash
jq '.stats' marketplace.json
```

## Contributing

We've created an automated workflow to make adding new agents and skills easy!

### Quick Start

1. **Use the templates** in `staging/`:
   ```bash
   # For agents
   cp staging/agent-template.md staging/agents/my-new-agent.md

   # For skills
   cp -r staging/skill-template staging/skills/my-new-skill
   ```

2. **Fill in your content** and metadata

3. **Run the automation script**:
   ```bash
   python3 add-to-marketplace.py
   ```

4. **Commit and push** your changes

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

### Manual Process

To add a new skill or agent manually:

1. Follow the existing structure patterns
2. Include comprehensive documentation
3. Add appropriate `.gitignore` entries for data directories
4. Test with Claude Code before submitting
5. Update both `marketplace.json` files (root and `.claude-plugin/`)

## License

MIT License - Feel free to use and adapt these skills and agents for your own projects.

## Resources

- [Claude Code Documentation](https://docs.anthropic.com/en/docs/claude-code)
- [Claude Code Skills Guide](https://docs.anthropic.com/en/docs/claude-code/skills)
- [Anthropic API Documentation](https://docs.anthropic.com/en/api)

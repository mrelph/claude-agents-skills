# Skill Releases

Direct download packages for individual skill installation.

## Available Skills

| Skill | Version | Download | Install Guide |
|-------|---------|----------|---------------|
| jr-kraken-18u-navy-lineup | v1.0.0 | [jr-kraken-18u-navy-lineup-v1.0.0.zip](jr-kraken-18u-navy-lineup-v1.0.0.zip) | [jr-kraken-18u-navy-lineup-INSTALL.md](jr-kraken-18u-navy-lineup-INSTALL.md) |
| kiro-spec-driven-development | v1.0.0 | [kiro-spec-driven-development-v1.0.0.zip](kiro-spec-driven-development-v1.0.0.zip) | [kiro-spec-driven-development-INSTALL.md](kiro-spec-driven-development-INSTALL.md) |
| portfolio-analyzer | v2.3.0 | [portfolio-analyzer-v2.3.0.zip](portfolio-analyzer-v2.3.0.zip) | [portfolio-analyzer-INSTALL.md](portfolio-analyzer-INSTALL.md) |
| research-consolidator | v1.0.0 | [research-consolidator-v1.0.0.zip](research-consolidator-v1.0.0.zip) | [research-consolidator-INSTALL.md](research-consolidator-INSTALL.md) |
| retirement-planner | v1.0.0 | [retirement-planner-v1.0.0.zip](retirement-planner-v1.0.0.zip) | [retirement-planner-INSTALL.md](retirement-planner-INSTALL.md) |
| tax-preparation | v1.3.0 | [tax-preparation-v1.3.0.zip](tax-preparation-v1.3.0.zip) | [tax-preparation-INSTALL.md](tax-preparation-INSTALL.md) |

## Installation Instructions

### Method 1: Quick Install

1. Download the skill ZIP file
2. Extract to your `.claude/skills/` directory:
   ```bash
   unzip skill-name-v1.0.0.zip -d ~/.claude/skills/
   ```
3. Restart Claude Code or reload the project

### Method 2: Project-Specific Install

Install to a specific project:
```bash
unzip skill-name-v1.0.0.zip -d /path/to/project/.claude/skills/
```

### Method 3: Plugin Marketplace (Recommended)

For easier updates and management, consider installing via the plugin marketplace:

```bash
/plugin marketplace add mrelph/claude-agents-skills
/plugin install skill-name@claude-agents-skills
```

## Verification

After installation, check that the skill directory exists:
```bash
ls ~/.claude/skills/skill-name/SKILL.md
```

The skill will be automatically available in your next Claude Code conversation.

---

**Note**: Individual ZIP downloads are provided for convenience. For the best experience with automatic updates, use the plugin marketplace installation method.

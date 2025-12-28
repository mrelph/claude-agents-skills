# Staging Area for New Agents and Skills

This directory is for staging new agents and skills before they are processed and added to the marketplace.

## Directory Structure

```
staging/
├── agents/        # Place new agent .md files here
├── skills/        # Place new skill directories here
└── README.md      # This file
```

## Quick Start

### Adding a New Agent

1. Create your agent file in `staging/agents/`:
   ```bash
   # staging/agents/my-new-agent.md
   ```

2. Run the automation script:
   ```bash
   python3 add-to-marketplace.py --agent staging/agents/my-new-agent.md
   ```

3. The script will:
   - Create `Agents/my-new-agent/` directory
   - Move the file to `Agents/my-new-agent/my-new-agent.md`
   - Generate a marketplace.json entry
   - Update both marketplace.json files
   - Clean up the staging area

### Adding a New Skill

1. Create your skill directory in `staging/skills/`:
   ```bash
   mkdir staging/skills/my-new-skill
   # Add SKILL.md and other files
   ```

2. Run the automation script:
   ```bash
   python3 add-to-marketplace.py --skill staging/skills/my-new-skill
   ```

3. The script will:
   - Move the directory to `Skills/my-new-skill/`
   - Generate a marketplace.json entry
   - Update both marketplace.json files
   - Clean up the staging area

## Interactive Mode

Run without arguments for interactive prompts:
```bash
python3 add-to-marketplace.py
```

The script will guide you through:
- Selecting agent or skill
- Providing metadata (description, keywords, category)
- Confirming the changes

## Batch Processing

Process all staged items at once:
```bash
python3 add-to-marketplace.py --batch
```

## Template Files

Use the provided templates to get started:
- `staging/agent-template.md` - Agent template with YAML frontmatter
- `staging/skill-template/` - Complete skill structure example

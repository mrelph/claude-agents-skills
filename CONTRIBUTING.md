# Contributing to Claude Code Marketplace

Thank you for your interest in contributing! This guide will help you add new agents and skills to the marketplace.

## Quick Start with Staging Workflow

We've created an automated workflow to make adding new agents and skills easy:

### 1. Set Up Your New Agent or Skill

**For Agents:**
```bash
# Copy the template
cp staging/agent-template.md staging/agents/my-new-agent.md

# Edit the file with your agent's details
# Fill in the frontmatter and content
```

**For Skills:**
```bash
# Copy the template directory
cp -r staging/skill-template staging/skills/my-new-skill

# Edit SKILL.md, README.md, and add your references/scripts
```

### 2. Run the Automation Script

**Interactive Mode (Recommended):**
```bash
python3 add-to-marketplace.py
```

The script will:
- Find your staged items
- Prompt you for metadata (description, keywords, category)
- Create proper directory structures
- Update marketplace.json files
- Clean up staging area

**Non-Interactive Mode:**
```bash
# For a specific agent
python3 add-to-marketplace.py --agent staging/agents/my-new-agent.md --non-interactive

# For a specific skill
python3 add-to-marketplace.py --skill staging/skills/my-new-skill --non-interactive
```

### 3. Commit and Push

```bash
git add .
git commit -m "Add [agent/skill-name] for [purpose]"
git push
```

## Detailed Guidelines

### Agent Requirements

Agents must include:
- **YAML frontmatter** with:
  - `name` - kebab-case name
  - `description` - One-line description
  - `model` - sonnet, opus, or haiku
  - `color` - UI color
  - `category` - development, design, planning, or media
  - `allowed-tools` - List of tools the agent can use

- **Content sections**:
  - Purpose
  - Expertise areas
  - Workflow
  - Examples

### Skill Requirements

Skills must include:
- **SKILL.md** with:
  - YAML frontmatter (name, description, allowed-tools, category, version)
  - Purpose and capabilities
  - Workflow description
  - Usage instructions
  - Examples

- **README.md** - Human-readable documentation

- **Optional but recommended**:
  - `references/` - Domain knowledge documents
  - `scripts/` - Python utility scripts

### Categories

**Agent Categories:**
- `development` - Bug tracking, databases, documentation, performance, security
- `design` - UX/UI, visual design, accessibility
- `planning` - Roadmaps, feature planning, project management
- `media` - Video, audio, image processing

**Skill Categories:**
- `financial` - Tax, investing, retirement, budgeting
- `research` - Analysis, synthesis, reporting
- `domain-specific` - Specialized use cases (sports, hobbies, etc.)

### Keywords

Choose 3-6 relevant keywords that help users discover your agent/skill:
- Be specific (e.g., "postgresql" not just "database")
- Include domain terms
- Think about how users would search

### Versioning

Use semantic versioning:
- `1.0.0` - Initial release
- `1.1.0` - New features, backward compatible
- `2.0.0` - Breaking changes

## Manual Process (Advanced)

If you prefer not to use the automation script:

1. Create directory structure manually
2. Add files following existing patterns
3. Manually edit both `.claude-plugin/marketplace.json` and `marketplace.json`
4. Ensure both files stay in sync

## Testing Locally

Before pushing, test your marketplace:

```bash
# Validate the structure
/plugin validate .

# Install locally
/plugin install .
```

## Questions?

- Check existing agents/skills for examples
- Review the staging templates
- Open an issue on GitHub

## Code of Conduct

- Be respectful and constructive
- Test your contributions before submitting
- Follow existing patterns and conventions
- Provide clear documentation

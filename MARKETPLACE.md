# Claude Code Marketplace Integration Guide

This document describes how to integrate with the Claude Code Marketplace catalog for programmatic discovery and installation of agents and skills.

## Overview

The `marketplace.json` file provides a machine-readable catalog of all available agents and skills in this repository. It enables:

- **Automated discovery** - Find agents and skills programmatically
- **Version management** - Track versions and updates
- **Dependency mapping** - Understand skill integrations
- **Metadata queries** - Filter and search by capabilities
- **Installation automation** - Programmatic installation

## Marketplace Structure

### Top-Level Schema

```json
{
  "name": "Marketplace name",
  "version": "Catalog version (semantic versioning)",
  "description": "Marketplace description",
  "repository": "Git repository URL",
  "last_updated": "YYYY-MM-DD",
  "categories": { /* categorized items */ },
  "integrations": { /* skill connections */ },
  "installation": { /* installation instructions */ },
  "stats": { /* usage statistics */ },
  "contributing": { /* contribution guidelines */ },
  "license": "License type",
  "resources": { /* external documentation links */ }
}
```

### Categories Object

Items are organized hierarchically:

```
categories/
├── agents/
│   ├── development/     [agent objects]
│   ├── design/          [agent objects]
│   ├── planning/        [agent objects]
│   └── media/           [agent objects]
└── skills/
    ├── financial/       [skill objects]
    ├── research/        [skill objects]
    └── domain_specific/ [skill objects]
```

### Agent Object

```json
{
  "id": "database-architect",
  "name": "Database Architect",
  "description": "PostgreSQL/Supabase expertise...",
  "model": "sonnet",
  "color": "cyan",
  "version": "1.0.0",
  "file": "Agents/database-architect.md",
  "allowed_tools": ["Read", "Write", "Bash", ...],
  "install_command": "cp Agents/database-architect.md .claude/agents/",
  "tags": ["database", "postgresql", "supabase", ...]
}
```

### Skill Object

```json
{
  "id": "tax-preparation",
  "name": "Tax Preparation",
  "description": "Comprehensive tax preparation...",
  "version": "1.3.0",
  "last_updated": "2025-12-09",
  "directory": "Skills/tax-preparation",
  "allowed_tools": ["Read", "Bash", "WebSearch", ...],
  "install_command": "cp -r Skills/tax-preparation .claude/skills/",
  "target_users": "individuals, families, self-employed",
  "tags": ["tax", "finance", "irs", ...],
  "features": ["PDF document reading", ...],
  "scripts": ["filing_status_analyzer.py", ...],
  "references": ["tax_brackets_deductions.md", ...]
}
```

## Integration Scenarios

### 1. Building a Web Frontend

```javascript
// Fetch and display marketplace data
fetch('marketplace.json')
  .then(response => response.json())
  .then(marketplace => {
    // Display agents
    const agents = Object.values(marketplace.categories.agents).flat();
    agents.forEach(agent => {
      displayAgentCard(agent);
    });

    // Display skills
    const skills = Object.values(marketplace.categories.skills).flat();
    skills.forEach(skill => {
      displaySkillCard(skill);
    });
  });
```

### 2. CLI Installation Tool

```python
import json

def install_item(item_id):
    with open('marketplace.json') as f:
        marketplace = json.load(f)

    # Search all categories
    for category_type in ['agents', 'skills']:
        for category, items in marketplace['categories'][category_type].items():
            for item in items:
                if item['id'] == item_id:
                    # Execute install_command
                    os.system(item['install_command'])
                    return

    print(f"Item {item_id} not found")
```

### 3. GitHub Actions Workflow

```yaml
name: Test All Skills
on: [push]

jobs:
  test-skills:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2

      - name: Extract skill directories
        run: |
          jq -r '.categories.skills[][] | .directory' marketplace.json > skills.txt

      - name: Test each skill
        run: |
          while read dir; do
            echo "Testing $dir"
            # Run tests for each skill
          done < skills.txt
```

### 4. Version Checker

```bash
#!/bin/bash
# Check for skill updates

for skill_id in $(jq -r '.categories.skills[][] | .id' marketplace.json); do
  current=$(jq -r ".categories.skills[][] | select(.id==\"$skill_id\") | .version" marketplace.json)
  installed=$(cat .claude/skills/$skill_id/SKILL.md | grep "version:" | cut -d: -f2 | tr -d ' ')

  if [ "$current" != "$installed" ]; then
    echo "Update available for $skill_id: $installed → $current"
  fi
done
```

## Query Patterns

### Using jq (JSON Query)

**List all agent IDs:**
```bash
jq -r '.categories.agents[][] | .id' marketplace.json
```

**Find skills by tag:**
```bash
jq '.categories.skills[][] | select(.tags[] | contains("finance"))' marketplace.json
```

**Get installation commands for all skills:**
```bash
jq -r '.categories.skills[][] | .install_command' marketplace.json
```

**Find agents that use a specific tool:**
```bash
jq '.categories.agents[][] | select(.allowed_tools[] == "WebSearch")' marketplace.json
```

**List skill integrations:**
```bash
jq '.integrations.skill_connections[]' marketplace.json
```

**Get all items with version > 2.0:**
```bash
jq '.categories.skills[][] | select(.version | split(".")[0] | tonumber > 1)' marketplace.json
```

### Using Python

```python
import json

with open('marketplace.json') as f:
    marketplace = json.load(f)

# Get all agents using sonnet model
sonnet_agents = [
    agent
    for category in marketplace['categories']['agents'].values()
    for agent in category
    if agent['model'] == 'sonnet'
]

# Find skills updated in last 30 days
from datetime import datetime, timedelta

recent_cutoff = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
recent_skills = [
    skill
    for category in marketplace['categories']['skills'].values()
    for skill in category
    if skill.get('last_updated', '') >= recent_cutoff
]

# Get integration graph
integration_map = {}
for conn in marketplace['integrations']['skill_connections']:
    if conn['from'] not in integration_map:
        integration_map[conn['from']] = []
    integration_map[conn['from']].append(conn['to'])
```

### Using JavaScript/Node.js

```javascript
const marketplace = require('./marketplace.json');

// Find all financial skills
const financialSkills = marketplace.categories.skills.financial;

// Search by keyword
function search(query) {
  const results = [];
  const q = query.toLowerCase();

  // Search agents
  for (const category of Object.values(marketplace.categories.agents)) {
    for (const agent of category) {
      const searchText = `${agent.id} ${agent.name} ${agent.description} ${agent.tags.join(' ')}`.toLowerCase();
      if (searchText.includes(q)) {
        results.push({ ...agent, type: 'agent' });
      }
    }
  }

  // Search skills
  for (const category of Object.values(marketplace.categories.skills)) {
    for (const skill of category) {
      const searchText = `${skill.id} ${skill.name} ${skill.description} ${skill.tags.join(' ')}`.toLowerCase();
      if (searchText.includes(q)) {
        results.push({ ...skill, type: 'skill' });
      }
    }
  }

  return results;
}

// Get item by ID
function getItem(id) {
  // Search all categories
  for (const categoryType of ['agents', 'skills']) {
    for (const items of Object.values(marketplace.categories[categoryType])) {
      const item = items.find(i => i.id === id);
      if (item) return { ...item, type: categoryType.slice(0, -1) };
    }
  }
  return null;
}
```

## Marketplace CLI

The included Python CLI tool provides a reference implementation:

```bash
# Browse the marketplace
./marketplace-cli.py list
./marketplace-cli.py search <keyword>
./marketplace-cli.py info <item-id>

# Install items
./marketplace-cli.py install <item-id>

# View statistics
./marketplace-cli.py stats
```

See the CLI source code at `marketplace-cli.py` for implementation details.

## Contributing to the Marketplace

When adding new agents or skills:

### 1. Add the Agent/Skill Files

Follow the existing structure in `Agents/` or `Skills/` directories.

### 2. Update marketplace.json

Add an entry to the appropriate category:

```json
{
  "id": "my-new-skill",
  "name": "My New Skill",
  "description": "What it does",
  "version": "1.0.0",
  "last_updated": "2025-12-28",
  "directory": "Skills/my-new-skill",
  "allowed_tools": ["Read", "Write"],
  "install_command": "cp -r Skills/my-new-skill .claude/skills/",
  "target_users": "developers",
  "tags": ["category", "keyword"],
  "features": ["Feature 1", "Feature 2"]
}
```

### 3. Update Statistics

Increment the counts in the `stats` object:

```json
"stats": {
  "total_agents": 8,
  "total_skills": 6,  // increment
  "agent_categories": 4,
  "skill_categories": 3
}
```

### 4. Add Integration Mappings (if applicable)

If your skill integrates with others:

```json
"integrations": {
  "skill_connections": [
    {
      "from": "my-new-skill",
      "to": "existing-skill",
      "description": "How they integrate"
    }
  ]
}
```

### 5. Validate JSON

```bash
# Validate JSON syntax
jq empty marketplace.json && echo "Valid JSON" || echo "Invalid JSON"

# Test with CLI
./marketplace-cli.py info my-new-skill
```

## Validation Schema

The marketplace.json should conform to this structure:

- **Required fields**: name, version, categories, stats
- **Agent required fields**: id, name, description, model, file, allowed_tools, install_command, tags
- **Skill required fields**: id, name, description, version, directory, allowed_tools, install_command, tags
- **Version format**: Semantic versioning (MAJOR.MINOR.PATCH)
- **Date format**: YYYY-MM-DD
- **IDs**: Kebab-case, lowercase, unique across all items

## API Endpoints (Future)

The marketplace catalog is designed to support future API endpoints:

```
GET  /api/v1/items              # List all items
GET  /api/v1/items/:id          # Get item details
GET  /api/v1/agents             # List all agents
GET  /api/v1/skills             # List all skills
GET  /api/v1/search?q=keyword   # Search items
GET  /api/v1/categories         # List categories
GET  /api/v1/integrations       # Get integration graph
GET  /api/v1/stats              # Get statistics
```

## Best Practices

1. **Keep metadata accurate** - Ensure descriptions match actual functionality
2. **Version properly** - Use semantic versioning for all updates
3. **Tag thoroughly** - Include relevant tags for discoverability
4. **Document integrations** - Map skill dependencies clearly
5. **Test install commands** - Verify installation works before committing
6. **Update last_updated** - Increment on every change
7. **Validate JSON** - Always check syntax before committing

## Resources

- [JSON Schema](https://json-schema.org/) - For validation
- [jq Manual](https://stedolan.github.io/jq/manual/) - For queries
- [Semantic Versioning](https://semver.org/) - For version management
- [Claude Code Documentation](https://docs.anthropic.com/en/docs/claude-code)

## Support

For questions or issues with the marketplace:

1. Check this documentation
2. Review the `marketplace-cli.py` implementation
3. Open an issue on the repository
4. Submit a pull request with improvements

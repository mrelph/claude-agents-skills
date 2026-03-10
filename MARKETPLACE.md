# Claude Agents & Skills Plugin Marketplace — Integration Guide

This document describes the v2.0.0 plugin marketplace format: how to install plugins, the `marketplace.json` schema, available plugins, and programmatic access patterns.

## Adding the Marketplace

Install this repository as a Claude Code plugin marketplace with one command:

```bash
/plugin marketplace add mrelph/claude-agents-skills
```

This registers the marketplace so you can browse and install individual plugins:

```bash
# Install a specific plugin
/plugin install tax-preparation@mrelph/claude-agents-skills

# List all available plugins from this marketplace
/plugin list mrelph/claude-agents-skills

# Update all installed plugins from this marketplace
/plugin update mrelph/claude-agents-skills
```

## Available Plugins

| Plugin | Version | Category | Description |
|--------|---------|----------|-------------|
| `tax-preparation` | v2.0.0 | financial | US tax preparation: deduction analysis, RSU calculations, form processing |
| `portfolio-analyzer` | v3.0.0 | financial | Investment portfolio analysis, risk assessment, asset allocation |
| `retirement-planner` | v2.0.0 | financial | Retirement readiness, Social Security optimization, withdrawal strategies |
| `research-consolidator` | v2.0.0 | research | Multi-source research synthesis with confidence scoring and gap analysis |
| `jr-kraken-18u-navy-lineup` | v1.0.0 | domain-specific | Jr. Kraken 18U Navy hockey lineup building, game strategy, player management |
| `dev-tools` | v1.0.0 | development | Bundle: bug tracking, DB architecture, security scanning, performance, documentation |

## marketplace.json Schema

The `marketplace.json` at the root of this repository is the machine-readable plugin catalog. It follows the official Claude Code plugin marketplace format.

### Top-Level Schema

```json
{
  "name": "string — marketplace identifier",
  "owner": { "name": "string — github username" },
  "description": "string — marketplace description",
  "version": "string — catalog version (semantic versioning)",
  "repository": "string — git repository URL",
  "license": "string — SPDX license identifier",
  "plugins": [ /* array of plugin objects */ ]
}
```

### Plugin Object Schema

Each entry in the `plugins` array describes one installable plugin:

```json
{
  "name": "string — kebab-case plugin identifier",
  "source": "string — relative path to plugin directory (e.g., ./plugins/tax-preparation)",
  "description": "string — one-sentence plugin description",
  "version": "string — semantic version matching .claude-plugin/plugin.json",
  "author": { "name": "string — github username" },
  "keywords": ["string — discovery tags"],
  "category": "string — category identifier"
}
```

**Valid categories:** `financial`, `research`, `development`, `design`, `planning`, `domain-specific`

### Complete Example

```json
{
  "name": "claude-agents-skills-marketplace",
  "owner": { "name": "mrelph" },
  "description": "A curated collection of specialized agents and skills for Claude Code",
  "version": "2.0.0",
  "repository": "https://github.com/mrelph/claude-agents-skills",
  "license": "MIT",
  "plugins": [
    {
      "name": "tax-preparation",
      "source": "./plugins/tax-preparation",
      "description": "US tax preparation: deduction analysis, RSU calculations, form processing, and tax optimization",
      "version": "2.0.0",
      "author": { "name": "mrelph" },
      "keywords": ["tax", "finance", "deductions", "RSU", "IRS", "W-2", "1099"],
      "category": "financial"
    }
  ]
}
```

### Individual Plugin Manifest Schema

Each plugin directory contains a manifest at `.claude-plugin/plugin.json`. This is the authoritative source for that plugin's metadata:

```json
{
  "name": "string — plugin identifier (must match marketplace.json entry)",
  "description": "string — plugin description",
  "version": "string — semantic version",
  "author": { "name": "string — github username" },
  "repository": "string — repository URL",
  "license": "string — SPDX license identifier",
  "keywords": ["string — discovery tags"]
}
```

## Plugin Directory Layout

The `plugins/` directory follows a consistent structure that Claude Code's plugin system expects:

```
plugins/
└── plugin-name/
    ├── .claude-plugin/
    │   └── plugin.json          # Plugin manifest (required)
    ├── skills/                  # Skills (optional)
    │   └── skill-name/
    │       ├── SKILL.md         # Skill definition with ${CLAUDE_PLUGIN_ROOT}/ paths
    │       └── README.md
    ├── agents/                  # Agents (optional)
    │   └── agent-name.md        # Agent definition
    ├── references/              # Supporting documents (optional)
    ├── scripts/                 # Utility scripts (optional)
    ├── examples/                # Example data (optional)
    └── README.md                # Plugin documentation
```

The `${CLAUDE_PLUGIN_ROOT}` variable is resolved at install time to the actual plugin installation path. All intra-plugin file references in SKILL.md and agent definitions must use this variable.

## Programmatic Access

### Querying marketplace.json with jq

**List all plugin names and versions:**

```bash
jq -r '.plugins[] | "\(.name)  \(.version)"' marketplace.json
```

**Find plugins by category:**

```bash
jq '.plugins[] | select(.category == "financial") | {name, version, description}' marketplace.json
```

**Find plugins by keyword:**

```bash
jq '.plugins[] | select(.keywords[] | contains("retirement"))' marketplace.json
```

**Get the source path for a specific plugin:**

```bash
jq -r '.plugins[] | select(.name == "tax-preparation") | .source' marketplace.json
```

**List all keywords across all plugins (deduplicated):**

```bash
jq -r '[.plugins[].keywords[]] | unique[]' marketplace.json
```

**Count plugins by category:**

```bash
jq '[.plugins[] | .category] | group_by(.) | map({category: .[0], count: length})' marketplace.json
```

### Querying with Python

```python
import json

with open('marketplace.json') as f:
    marketplace = json.load(f)

# List all plugins
for plugin in marketplace['plugins']:
    print(f"{plugin['name']} ({plugin['version']}) — {plugin['description']}")

# Find financial plugins
financial = [p for p in marketplace['plugins'] if p['category'] == 'financial']

# Search by keyword
def search_plugins(query):
    q = query.lower()
    return [
        p for p in marketplace['plugins']
        if q in p['name']
        or q in p['description'].lower()
        or any(q in kw for kw in p['keywords'])
    ]

tax_related = search_plugins('tax')
```

### Querying with JavaScript/Node.js

```javascript
const marketplace = require('./marketplace.json');

// List all plugins
marketplace.plugins.forEach(plugin => {
  console.log(`${plugin.name} v${plugin.version}: ${plugin.description}`);
});

// Find a plugin by name
function getPlugin(name) {
  return marketplace.plugins.find(p => p.name === name) || null;
}

// Search by keyword
function searchPlugins(query) {
  const q = query.toLowerCase();
  return marketplace.plugins.filter(plugin =>
    plugin.name.includes(q) ||
    plugin.description.toLowerCase().includes(q) ||
    plugin.keywords.some(kw => kw.includes(q))
  );
}
```

### GitHub Actions Integration

Enumerate all plugin source paths for CI validation:

```yaml
name: Validate Plugins
on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Validate marketplace.json
        run: jq empty marketplace.json && echo "marketplace.json is valid JSON"

      - name: Validate all plugin manifests
        run: |
          jq -r '.plugins[].source' marketplace.json | while read source; do
            manifest="${source}/.claude-plugin/plugin.json"
            if [ -f "$manifest" ]; then
              jq empty "$manifest" && echo "Valid: $manifest"
            else
              echo "MISSING: $manifest" && exit 1
            fi
          done

      - name: Check ${CLAUDE_PLUGIN_ROOT} usage in skills
        run: |
          # Warn if any skill uses hardcoded paths instead of ${CLAUDE_PLUGIN_ROOT}
          if grep -r '\./Skills\|\.claude/skills' plugins/; then
            echo "ERROR: Hardcoded paths found in plugins/"
            exit 1
          fi
```

## Version Checking

Check whether an installed version of a plugin is current:

```bash
#!/bin/bash
# Compare installed version against marketplace catalog

PLUGIN="tax-preparation"
CATALOG_VERSION=$(jq -r ".plugins[] | select(.name == \"$PLUGIN\") | .version" marketplace.json)
INSTALLED_VERSION=$(jq -r '.version' ~/.claude/plugins/$PLUGIN/.claude-plugin/plugin.json 2>/dev/null || echo "not installed")

if [ "$INSTALLED_VERSION" = "not installed" ]; then
  echo "$PLUGIN is not installed"
elif [ "$INSTALLED_VERSION" != "$CATALOG_VERSION" ]; then
  echo "Update available: $PLUGIN $INSTALLED_VERSION → $CATALOG_VERSION"
else
  echo "$PLUGIN $INSTALLED_VERSION is current"
fi
```

## Validation Rules

A valid `marketplace.json` must satisfy:

- Valid JSON syntax
- Required top-level fields: `name`, `owner`, `description`, `version`, `repository`, `license`, `plugins`
- Each plugin entry must have: `name`, `source`, `description`, `version`, `author`, `keywords`, `category`
- `name` values must be unique across all plugin entries
- `version` fields must follow semantic versioning (`MAJOR.MINOR.PATCH`)
- `source` paths must point to directories that exist and contain `.claude-plugin/plugin.json`
- The `version` in each plugin entry must match the `version` in the corresponding `.claude-plugin/plugin.json`

Validate locally:

```bash
# Check JSON syntax
jq empty marketplace.json && echo "Valid JSON"

# Verify version consistency between marketplace.json and plugin.json manifests
jq -r '.plugins[] | "\(.name) \(.version) \(.source)"' marketplace.json | \
  while read name catalog_ver source; do
    plugin_ver=$(jq -r '.version' "${source}/.claude-plugin/plugin.json" 2>/dev/null)
    if [ "$catalog_ver" != "$plugin_ver" ]; then
      echo "VERSION MISMATCH: $name — catalog=$catalog_ver, plugin.json=$plugin_ver"
    else
      echo "OK: $name $catalog_ver"
    fi
  done
```

## Contributing a Plugin

To add a new plugin to this marketplace, see [CONTRIBUTING.md](CONTRIBUTING.md) for the complete step-by-step process, including directory structure, manifest format, `${CLAUDE_PLUGIN_ROOT}` path requirements, and testing instructions.

## Resources

- [Claude Code Documentation](https://docs.anthropic.com/en/docs/claude-code)
- [Claude Code Skills Guide](https://docs.anthropic.com/en/docs/claude-code/skills)
- [Semantic Versioning](https://semver.org/)
- [jq Manual](https://stedolan.github.io/jq/manual/)
- [JSON Schema](https://json-schema.org/)

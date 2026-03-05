#!/usr/bin/env python3
"""
Add a new plugin to the Claude Code marketplace.

Scaffolds the plugin directory structure and adds an entry to marketplace.json.

Usage:
    ./add-to-marketplace.py                          # Interactive mode
    ./add-to-marketplace.py --name my-plugin         # Create with name
    ./add-to-marketplace.py --from-staging           # Process from staging/
"""

import json
import os
import re
import shutil
import sys
import argparse
from pathlib import Path
from typing import Dict, List, Optional


def load_marketplace(path: str = ".claude-plugin/marketplace.json") -> Dict:
    """Load existing marketplace.json file."""
    with open(path, 'r') as f:
        return json.load(f)


def save_marketplace(data: Dict, path: str = ".claude-plugin/marketplace.json"):
    """Save marketplace.json file with proper formatting."""
    with open(path, 'w') as f:
        json.dump(data, f, indent=2)
        f.write('\n')
    print(f"Updated {path}")


def to_kebab_case(text: str) -> str:
    """Convert text to kebab-case."""
    text = re.sub(r'[\s_]+', '-', text)
    text = re.sub(r'[^a-zA-Z0-9-]', '', text)
    return text.lower()


def get_user_input(prompt: str, default: str = "") -> str:
    """Get user input with optional default value."""
    if default:
        prompt = f"{prompt} [{default}]"
    value = input(f"{prompt}: ").strip()
    return value if value else default


def scaffold_plugin(name: str, description: str, version: str,
                    category: str, keywords: List[str],
                    plugin_type: str = "skill") -> Path:
    """Create the plugin directory structure."""
    plugin_dir = Path(f"plugins/{name}")

    if plugin_dir.exists():
        print(f"Error: Plugin directory already exists: {plugin_dir}")
        return None

    # Create directory structure
    (plugin_dir / ".claude-plugin").mkdir(parents=True)

    if plugin_type == "skill":
        (plugin_dir / f"skills/{name}").mkdir(parents=True)
        (plugin_dir / "scripts").mkdir()
        (plugin_dir / "references").mkdir()
        (plugin_dir / "examples").mkdir()
    elif plugin_type == "agent":
        (plugin_dir / "agents").mkdir(parents=True)

    # Create plugin.json manifest
    manifest = {
        "name": name,
        "description": description,
        "version": version,
        "author": {"name": "mrelph"},
        "repository": "https://github.com/mrelph/claude-agents-skills",
        "license": "MIT",
        "keywords": keywords
    }

    with open(plugin_dir / ".claude-plugin" / "plugin.json", 'w') as f:
        json.dump(manifest, f, indent=2)
        f.write('\n')

    # Create SKILL.md template for skill plugins
    if plugin_type == "skill":
        skill_template = f"""---
name: {name}
description: {description}
allowed-tools: Read, Bash, WebSearch, WebFetch, Grep, Glob, Write, AskUserQuestion
metadata:
  version: {version}
---

# {name.replace('-', ' ').title()}

## Overview

[Description of what this skill does...]

## Workflow

### 1. [First Step]

[Instructions...]

## Scripts

| Script | Purpose |
|--------|---------|
| `${{CLAUDE_PLUGIN_ROOT}}/scripts/example.py` | [Description] |

## Reference Documents

| Reference | Contents |
|-----------|----------|
| `${{CLAUDE_PLUGIN_ROOT}}/references/guide.md` | [Description] |

## Limitations

[What this skill cannot do...]
"""
        with open(plugin_dir / f"skills/{name}/SKILL.md", 'w') as f:
            f.write(skill_template)

    # Create README
    readme = f"""# {name.replace('-', ' ').title()}

**Version:** {version}

{description}

## Installation

```bash
/plugin marketplace add mrelph/claude-agents-skills
/plugin install {name}@mrelph/claude-agents-skills
```
"""
    with open(plugin_dir / "README.md", 'w') as f:
        f.write(readme)

    print(f"Created plugin scaffold at {plugin_dir}")
    return plugin_dir


def add_to_marketplace(marketplace_data: Dict, name: str, description: str,
                       version: str, category: str, keywords: List[str]) -> Dict:
    """Add a plugin entry to marketplace data."""
    if "plugins" not in marketplace_data:
        marketplace_data["plugins"] = []

    # Check for existing
    for existing in marketplace_data["plugins"]:
        if existing["name"] == name:
            print(f"Warning: Plugin '{name}' already exists. Updating...")
            existing.update({
                "description": description,
                "version": version,
                "category": category,
                "keywords": keywords
            })
            return marketplace_data

    entry = {
        "name": name,
        "source": f"./plugins/{name}",
        "description": description,
        "version": version,
        "author": {"name": "mrelph"},
        "keywords": keywords,
        "category": category
    }

    marketplace_data["plugins"].append(entry)
    print(f"Added '{name}' to marketplace")
    return marketplace_data


def interactive_mode():
    """Run in interactive mode to create a new plugin."""
    print("=" * 60)
    print("Claude Code Marketplace - Add New Plugin")
    print("=" * 60)

    name = to_kebab_case(get_user_input("\nPlugin name"))
    if not name:
        print("Error: Name is required")
        return

    description = get_user_input("Description")
    version = get_user_input("Version", "1.0.0")
    category = get_user_input("Category (financial/research/development/domain-specific)", "development")
    plugin_type = get_user_input("Type (skill/agent)", "skill")

    print("\nEnter keywords (comma-separated):")
    keywords_str = input("> ").strip()
    keywords = [k.strip() for k in keywords_str.split(',') if k.strip()]

    # Scaffold
    plugin_dir = scaffold_plugin(name, description, version, category, keywords, plugin_type)
    if not plugin_dir:
        return

    # Update marketplace
    marketplace_data = load_marketplace()
    marketplace_data = add_to_marketplace(marketplace_data, name, description,
                                          version, category, keywords)
    save_marketplace(marketplace_data)

    print(f"\nDone! Plugin scaffolded at {plugin_dir}")
    print(f"Next steps:")
    print(f"  1. Add your SKILL.md content to {plugin_dir}/skills/{name}/SKILL.md")
    print(f"  2. Add scripts to {plugin_dir}/scripts/")
    print(f"  3. Add references to {plugin_dir}/references/")
    print(f"  4. Use ${{CLAUDE_PLUGIN_ROOT}}/ prefix for all internal paths")
    print(f"  5. Commit and push")


def main():
    parser = argparse.ArgumentParser(
        description="Add a new plugin to Claude Code marketplace"
    )
    parser.add_argument('--name', help='Plugin name')
    parser.add_argument('--description', help='Plugin description')
    parser.add_argument('--version', default='1.0.0', help='Version')
    parser.add_argument('--category', default='development', help='Category')
    parser.add_argument('--keywords', help='Comma-separated keywords')
    parser.add_argument('--type', choices=['skill', 'agent'], default='skill',
                        help='Plugin type')

    args = parser.parse_args()

    if not args.name:
        interactive_mode()
        return

    name = to_kebab_case(args.name)
    keywords = [k.strip() for k in args.keywords.split(',')] if args.keywords else []

    plugin_dir = scaffold_plugin(name, args.description or '', args.version,
                                  args.category, keywords, args.type)
    if plugin_dir:
        marketplace_data = load_marketplace()
        marketplace_data = add_to_marketplace(marketplace_data, name,
                                              args.description or '', args.version,
                                              args.category, keywords)
        save_marketplace(marketplace_data)


if __name__ == "__main__":
    main()

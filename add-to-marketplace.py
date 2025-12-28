#!/usr/bin/env python3
"""
Automation script to add new agents and skills to the Claude Code marketplace.
Processes items from the staging/ directory and updates marketplace.json files.
"""

import json
import os
import sys
import shutil
import re
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
    print(f"✓ Updated {path}")


def extract_frontmatter(file_path: str) -> Optional[Dict]:
    """Extract YAML frontmatter from markdown file."""
    with open(file_path, 'r') as f:
        content = f.read()

    # Match YAML frontmatter between --- markers
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if not match:
        return None

    frontmatter = {}
    for line in match.group(1).split('\n'):
        if ':' in line:
            key, value = line.split(':', 1)
            frontmatter[key.strip()] = value.strip()

    return frontmatter


def to_kebab_case(text: str) -> str:
    """Convert text to kebab-case."""
    # Replace spaces and underscores with hyphens
    text = re.sub(r'[\s_]+', '-', text)
    # Remove special characters
    text = re.sub(r'[^a-zA-Z0-9-]', '', text)
    # Convert to lowercase
    return text.lower()


def get_user_input(prompt: str, default: str = "") -> str:
    """Get user input with optional default value."""
    if default:
        prompt = f"{prompt} [{default}]"
    value = input(f"{prompt}: ").strip()
    return value if value else default


def get_keywords_input() -> List[str]:
    """Get keywords from user input."""
    print("\nEnter keywords (comma-separated):")
    keywords_str = input("> ").strip()
    return [k.strip() for k in keywords_str.split(',') if k.strip()]


def get_slash_command_input(default_name: str) -> Optional[str]:
    """Get slash command configuration from user input."""
    wants_slash = get_user_input("\nDefine a slash command for this skill? (y/n)", "y").lower()

    if wants_slash == 'y':
        slash_cmd = get_user_input("Slash command name (without /)", default_name)
        return slash_cmd if slash_cmd else default_name

    return None


def process_agent(agent_file: str, marketplace_data: Dict, interactive: bool = True) -> Dict:
    """Process an agent file from staging and create marketplace entry."""
    agent_path = Path(agent_file)

    if not agent_path.exists():
        print(f"✗ Error: Agent file not found: {agent_file}")
        return None

    # Extract frontmatter if available
    frontmatter = extract_frontmatter(str(agent_path))

    # Determine agent name
    if frontmatter and 'name' in frontmatter:
        agent_name = frontmatter['name']
    else:
        agent_name = agent_path.stem

    agent_name = to_kebab_case(agent_name)

    print(f"\n📝 Processing agent: {agent_name}")

    # Get metadata
    if interactive:
        description = get_user_input("Description",
            frontmatter.get('description', '') if frontmatter else '')
        version = get_user_input("Version", "1.0.0")
        category = get_user_input("Category (development/design/planning/media)",
            frontmatter.get('category', 'development') if frontmatter else 'development')
        keywords = get_keywords_input()
    else:
        description = frontmatter.get('description', '') if frontmatter else ''
        version = "1.0.0"
        category = frontmatter.get('category', 'development') if frontmatter else 'development'
        keywords = []

    # Create agent directory
    agent_dir = Path(f"Agents/{agent_name}")
    agent_dir.mkdir(parents=True, exist_ok=True)

    # Move agent file
    dest_file = agent_dir / f"{agent_name}.md"
    shutil.copy2(agent_path, dest_file)
    print(f"✓ Created {dest_file}")

    # Create marketplace entry
    entry = {
        "name": agent_name,
        "source": f"./Agents/{agent_name}",
        "description": description,
        "version": version,
        "author": {
            "name": marketplace_data.get("owner", {}).get("name", "mrelph")
        },
        "keywords": keywords,
        "category": category
    }

    return entry


def process_skill(skill_dir: str, marketplace_data: Dict, interactive: bool = True) -> Dict:
    """Process a skill directory from staging and create marketplace entry."""
    skill_path = Path(skill_dir)

    if not skill_path.exists() or not skill_path.is_dir():
        print(f"✗ Error: Skill directory not found: {skill_dir}")
        return None

    skill_name = to_kebab_case(skill_path.name)

    print(f"\n📝 Processing skill: {skill_name}")

    # Try to extract metadata from SKILL.md
    skill_md = skill_path / "SKILL.md"
    frontmatter = None
    if skill_md.exists():
        frontmatter = extract_frontmatter(str(skill_md))

    # Get metadata
    if interactive:
        description = get_user_input("Description",
            frontmatter.get('description', '') if frontmatter else '')
        version = get_user_input("Version",
            frontmatter.get('metadata', {}).get('version', '1.0.0') if frontmatter else '1.0.0')
        category = get_user_input("Category (financial/research/domain-specific/development)",
            frontmatter.get('category', 'domain-specific') if frontmatter else 'domain-specific')
        keywords = get_keywords_input()
        slash_command = get_slash_command_input(skill_name)
    else:
        description = frontmatter.get('description', '') if frontmatter else ''
        version = frontmatter.get('metadata', {}).get('version', '1.0.0') if frontmatter else '1.0.0'
        category = frontmatter.get('category', 'domain-specific') if frontmatter else 'domain-specific'
        keywords = []
        slash_command = None

    # Create skill directory
    dest_dir = Path(f"Skills/{skill_name}")

    # Move skill directory
    if dest_dir.exists():
        print(f"✗ Error: Skill directory already exists: {dest_dir}")
        return None

    shutil.copytree(skill_path, dest_dir)
    print(f"✓ Created {dest_dir}")

    # Create marketplace entry
    entry = {
        "name": skill_name,
        "source": f"./Skills/{skill_name}",
        "description": description,
        "version": version,
        "author": {
            "name": marketplace_data.get("owner", {}).get("name", "mrelph")
        },
        "keywords": keywords,
        "category": category
    }

    # Add slash command if defined
    if slash_command:
        entry["slash_command"] = slash_command
        print(f"✓ Slash command configured: /{slash_command}")

    return entry


def add_entry_to_marketplace(marketplace_data: Dict, entry: Dict) -> Dict:
    """Add a new entry to marketplace data."""
    if "plugins" not in marketplace_data:
        marketplace_data["plugins"] = []

    # Check if entry already exists
    for existing in marketplace_data["plugins"]:
        if existing["name"] == entry["name"]:
            print(f"⚠ Warning: Entry '{entry['name']}' already exists in marketplace. Updating...")
            existing.update(entry)
            return marketplace_data

    # Add new entry
    marketplace_data["plugins"].append(entry)
    print(f"✓ Added '{entry['name']}' to marketplace")

    return marketplace_data


def interactive_mode():
    """Run in interactive mode to add items from staging."""
    print("=" * 60)
    print("Claude Code Marketplace - Add New Agent/Skill")
    print("=" * 60)

    # Check staging directory
    staging_agents = list(Path("staging/agents").glob("*.md"))
    staging_skills = [d for d in Path("staging/skills").iterdir() if d.is_dir()]

    print(f"\nFound in staging:")
    print(f"  Agents: {len(staging_agents)}")
    print(f"  Skills: {len(staging_skills)}")

    if not staging_agents and not staging_skills:
        print("\n✗ No items found in staging directory.")
        print("  Add files to staging/agents/ or staging/skills/ first.")
        return

    # Load marketplace
    marketplace_data = load_marketplace()

    # Process agents
    if staging_agents:
        print("\n" + "=" * 60)
        print("AGENTS")
        print("=" * 60)
        for agent_file in staging_agents:
            print(f"\nFound: {agent_file.name}")
            proceed = get_user_input("Process this agent? (y/n)", "y").lower()

            if proceed == 'y':
                entry = process_agent(str(agent_file), marketplace_data, interactive=True)
                if entry:
                    marketplace_data = add_entry_to_marketplace(marketplace_data, entry)
                    # Remove from staging
                    agent_file.unlink()
                    print(f"✓ Removed from staging")

    # Process skills
    if staging_skills:
        print("\n" + "=" * 60)
        print("SKILLS")
        print("=" * 60)
        for skill_dir in staging_skills:
            print(f"\nFound: {skill_dir.name}")
            proceed = get_user_input("Process this skill? (y/n)", "y").lower()

            if proceed == 'y':
                entry = process_skill(str(skill_dir), marketplace_data, interactive=True)
                if entry:
                    marketplace_data = add_entry_to_marketplace(marketplace_data, entry)
                    # Remove from staging
                    shutil.rmtree(skill_dir)
                    print(f"✓ Removed from staging")

    # Save marketplace files
    print("\n" + "=" * 60)
    print("SAVING")
    print("=" * 60)
    save_marketplace(marketplace_data, ".claude-plugin/marketplace.json")
    save_marketplace(marketplace_data, "marketplace.json")

    print("\n✓ Done! Don't forget to commit and push your changes.")


def main():
    parser = argparse.ArgumentParser(
        description="Add new agents and skills to Claude Code marketplace"
    )
    parser.add_argument('--agent', help='Path to agent .md file in staging')
    parser.add_argument('--skill', help='Path to skill directory in staging')
    parser.add_argument('--batch', action='store_true',
                       help='Process all items in staging without prompts')
    parser.add_argument('--non-interactive', action='store_true',
                       help='Run without interactive prompts')

    args = parser.parse_args()

    # Interactive mode
    if not args.agent and not args.skill and not args.batch:
        interactive_mode()
        return

    # Load marketplace
    marketplace_data = load_marketplace()

    # Process specific agent
    if args.agent:
        entry = process_agent(args.agent, marketplace_data,
                            interactive=not args.non_interactive)
        if entry:
            marketplace_data = add_entry_to_marketplace(marketplace_data, entry)
            save_marketplace(marketplace_data, ".claude-plugin/marketplace.json")
            save_marketplace(marketplace_data, "marketplace.json")
            print("\n✓ Done!")

    # Process specific skill
    if args.skill:
        entry = process_skill(args.skill, marketplace_data,
                            interactive=not args.non_interactive)
        if entry:
            marketplace_data = add_entry_to_marketplace(marketplace_data, entry)
            save_marketplace(marketplace_data, ".claude-plugin/marketplace.json")
            save_marketplace(marketplace_data, "marketplace.json")
            print("\n✓ Done!")

    # Batch mode
    if args.batch:
        print("Batch processing not yet implemented")


if __name__ == "__main__":
    main()

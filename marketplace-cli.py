#!/usr/bin/env python3
"""
Claude Code Marketplace CLI

A command-line tool for browsing and installing agents and skills from the marketplace.

Usage:
    ./marketplace-cli.py list                    # List all items
    ./marketplace-cli.py list agents             # List all agents
    ./marketplace-cli.py list skills             # List all skills
    ./marketplace-cli.py search security         # Search by keyword
    ./marketplace-cli.py info database-architect # Show details for an item
    ./marketplace-cli.py install <id>            # Install an agent or skill
    ./marketplace-cli.py stats                   # Show marketplace statistics
"""

import argparse
import json
import os
import shutil
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional


class MarketplaceCLI:
    def __init__(self, marketplace_file: str = "marketplace.json"):
        self.marketplace_file = marketplace_file
        self.data = self._load_marketplace()
        self.repo_root = Path(__file__).parent

    def _load_marketplace(self) -> Dict:
        """Load the marketplace catalog."""
        try:
            with open(self.marketplace_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Error: {self.marketplace_file} not found", file=sys.stderr)
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON in {self.marketplace_file}: {e}", file=sys.stderr)
            sys.exit(1)

    def _get_all_items(self) -> List[Dict[str, Any]]:
        """Get all agents and skills as a flat list."""
        items = []

        # Add all agents
        for category, agents in self.data['categories']['agents'].items():
            for agent in agents:
                items.append({**agent, 'type': 'agent', 'category': category})

        # Add all skills
        for category, skills in self.data['categories']['skills'].items():
            for skill in skills:
                items.append({**skill, 'type': 'skill', 'category': category})

        return items

    def list_items(self, item_type: Optional[str] = None):
        """List all items or filter by type (agents/skills)."""
        items = self._get_all_items()

        if item_type:
            items = [item for item in items if item['type'] == item_type.rstrip('s')]

        if not items:
            print(f"No {item_type or 'items'} found.")
            return

        # Group by type
        agents = [item for item in items if item['type'] == 'agent']
        skills = [item for item in items if item['type'] == 'skill']

        if agents:
            print("\n🤖 AGENTS\n" + "="*80)
            for agent in agents:
                print(f"\n{agent['id']}")
                print(f"  Name: {agent['name']}")
                print(f"  Category: {agent['category']}")
                print(f"  Model: {agent['model']}")
                print(f"  Description: {agent['description'][:80]}...")
                print(f"  Tags: {', '.join(agent['tags'])}")

        if skills:
            print("\n\n🛠️  SKILLS\n" + "="*80)
            for skill in skills:
                print(f"\n{skill['id']}")
                print(f"  Name: {skill['name']}")
                print(f"  Version: {skill['version']}")
                print(f"  Category: {skill['category']}")
                print(f"  Description: {skill['description'][:80]}...")
                print(f"  Tags: {', '.join(skill['tags'])}")

    def search(self, query: str):
        """Search for items by keyword."""
        query = query.lower()
        items = self._get_all_items()

        results = []
        for item in items:
            searchable = ' '.join([
                item['id'],
                item['name'],
                item['description'],
                ' '.join(item['tags'])
            ]).lower()

            if query in searchable:
                results.append(item)

        if not results:
            print(f"No results found for '{query}'")
            return

        print(f"\nFound {len(results)} result(s) for '{query}':\n")
        for item in results:
            print(f"\n{item['id']} ({item['type'].upper()})")
            print(f"  Name: {item['name']}")
            print(f"  Description: {item['description'][:80]}...")
            print(f"  Tags: {', '.join(item['tags'])}")

    def show_info(self, item_id: str):
        """Show detailed information about an item."""
        items = self._get_all_items()
        item = next((i for i in items if i['id'] == item_id), None)

        if not item:
            print(f"Error: Item '{item_id}' not found", file=sys.stderr)
            return

        print(f"\n{'='*80}")
        print(f"{item['name']} ({item['type'].upper()})")
        print(f"{'='*80}\n")

        print(f"ID: {item['id']}")
        print(f"Category: {item['category']}")

        if item['type'] == 'agent':
            print(f"Model: {item['model']}")
            print(f"Color: {item['color']}")
            print(f"File: {item['file']}")
        else:
            print(f"Version: {item['version']}")
            print(f"Last Updated: {item['last_updated']}")
            print(f"Directory: {item['directory']}")
            print(f"Target Users: {item.get('target_users', 'N/A')}")

        print(f"\nDescription:\n{item['description']}")

        print(f"\nAllowed Tools:")
        for tool in item['allowed_tools']:
            print(f"  - {tool}")

        print(f"\nTags: {', '.join(item['tags'])}")

        if item['type'] == 'skill':
            if 'features' in item:
                print(f"\nFeatures:")
                for feature in item['features']:
                    print(f"  - {feature}")

            if 'scripts' in item:
                print(f"\nScripts: {', '.join(item['scripts'])}")

            if 'references' in item:
                print(f"References: {', '.join(item['references'])}")

        print(f"\nInstallation:")
        print(f"  {item['install_command']}")

    def install(self, item_id: str, target_dir: Optional[str] = None):
        """Install an agent or skill to the specified directory."""
        items = self._get_all_items()
        item = next((i for i in items if i['id'] == item_id), None)

        if not item:
            print(f"Error: Item '{item_id}' not found", file=sys.stderr)
            return

        # Determine target directory
        if not target_dir:
            if item['type'] == 'agent':
                target_dir = '.claude/agents/'
            else:
                target_dir = '.claude/skills/'

        target_path = Path(target_dir)

        # Create target directory if it doesn't exist
        target_path.mkdir(parents=True, exist_ok=True)

        # Copy the file(s)
        if item['type'] == 'agent':
            src_file = self.repo_root / item['file']
            dst_file = target_path / src_file.name

            print(f"Installing {item['name']}...")
            print(f"  Source: {src_file}")
            print(f"  Destination: {dst_file}")

            shutil.copy2(src_file, dst_file)
            print(f"✓ Successfully installed {item['id']} to {dst_file}")
        else:
            src_dir = self.repo_root / item['directory']
            dst_dir = target_path / src_dir.name

            print(f"Installing {item['name']}...")
            print(f"  Source: {src_dir}")
            print(f"  Destination: {dst_dir}")

            if dst_dir.exists():
                print(f"Warning: {dst_dir} already exists. Removing old version...")
                shutil.rmtree(dst_dir)

            shutil.copytree(src_dir, dst_dir)
            print(f"✓ Successfully installed {item['id']} to {dst_dir}")

    def show_stats(self):
        """Show marketplace statistics."""
        stats = self.data['stats']

        print("\n" + "="*80)
        print(f"Marketplace Statistics")
        print("="*80 + "\n")

        print(f"Total Agents: {stats['total_agents']}")
        print(f"Total Skills: {stats['total_skills']}")
        print(f"Agent Categories: {stats['agent_categories']}")
        print(f"Skill Categories: {stats['skill_categories']}")

        print("\nAgent Categories:")
        for category, agents in self.data['categories']['agents'].items():
            print(f"  - {category}: {len(agents)} agent(s)")

        print("\nSkill Categories:")
        for category, skills in self.data['categories']['skills'].items():
            print(f"  - {category}: {len(skills)} skill(s)")

        if 'integrations' in self.data and 'skill_connections' in self.data['integrations']:
            print(f"\nIntegrations: {len(self.data['integrations']['skill_connections'])} connection(s)")


def main():
    parser = argparse.ArgumentParser(
        description="Claude Code Marketplace CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )

    subparsers = parser.add_subparsers(dest='command', help='Command to execute')

    # List command
    list_parser = subparsers.add_parser('list', help='List items')
    list_parser.add_argument('type', nargs='?', choices=['agents', 'skills'], help='Type to filter')

    # Search command
    search_parser = subparsers.add_parser('search', help='Search for items')
    search_parser.add_argument('query', help='Search query')

    # Info command
    info_parser = subparsers.add_parser('info', help='Show item details')
    info_parser.add_argument('id', help='Item ID')

    # Install command
    install_parser = subparsers.add_parser('install', help='Install an item')
    install_parser.add_argument('id', help='Item ID to install')
    install_parser.add_argument('--target', help='Target directory (optional)')

    # Stats command
    subparsers.add_parser('stats', help='Show marketplace statistics')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    cli = MarketplaceCLI()

    if args.command == 'list':
        cli.list_items(args.type)
    elif args.command == 'search':
        cli.search(args.query)
    elif args.command == 'info':
        cli.show_info(args.id)
    elif args.command == 'install':
        cli.install(args.id, args.target)
    elif args.command == 'stats':
        cli.show_stats()


if __name__ == '__main__':
    main()

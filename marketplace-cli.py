#!/usr/bin/env python3
"""
Claude Code Plugin Marketplace CLI

A command-line tool for browsing and managing plugins from the marketplace.

Usage:
    ./marketplace-cli.py list                        # List all plugins
    ./marketplace-cli.py list --category financial    # Filter by category
    ./marketplace-cli.py search security              # Search by keyword
    ./marketplace-cli.py info tax-preparation         # Show plugin details
    ./marketplace-cli.py install <name>               # Install a plugin
    ./marketplace-cli.py validate                     # Validate marketplace JSON
"""

import argparse
import json
import os
import shutil
import sys
from pathlib import Path
from typing import Dict, List, Optional


class MarketplaceCLI:
    def __init__(self, marketplace_file: str = ".claude-plugin/marketplace.json"):
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

    def _get_plugins(self) -> List[Dict]:
        """Get all plugins from marketplace."""
        return self.data.get("plugins", [])

    def list_plugins(self, category: Optional[str] = None):
        """List all plugins, optionally filtered by category."""
        plugins = self._get_plugins()

        if category:
            plugins = [p for p in plugins if p.get("category") == category]

        if not plugins:
            print(f"No plugins found{f' in category {category}' if category else ''}.")
            return

        print(f"\nPlugin Marketplace: {self.data.get('name', 'unknown')}")
        print(f"Version: {self.data.get('version', 'unknown')}")
        print(f"{'='*80}\n")

        for plugin in plugins:
            print(f"  {plugin['name']}")
            print(f"    Version:  {plugin.get('version', '?')}")
            print(f"    Category: {plugin.get('category', '?')}")
            print(f"    {plugin.get('description', '')[:75]}")
            print(f"    Keywords: {', '.join(plugin.get('keywords', []))}")
            print()

        print(f"Total: {len(plugins)} plugin(s)")

    def search(self, query: str):
        """Search for plugins by keyword."""
        query = query.lower()
        plugins = self._get_plugins()

        results = []
        for plugin in plugins:
            searchable = ' '.join([
                plugin.get('name', ''),
                plugin.get('description', ''),
                ' '.join(plugin.get('keywords', []))
            ]).lower()

            if query in searchable:
                results.append(plugin)

        if not results:
            print(f"No results found for '{query}'")
            return

        print(f"\nFound {len(results)} result(s) for '{query}':\n")
        for plugin in results:
            print(f"  {plugin['name']} (v{plugin.get('version', '?')})")
            print(f"    {plugin.get('description', '')[:75]}")
            print(f"    Install: /plugin install {plugin['name']}@{self.data.get('name', 'claude-agents-skills')}")
            print()

    def show_info(self, name: str):
        """Show detailed information about a plugin."""
        plugins = self._get_plugins()
        plugin = next((p for p in plugins if p['name'] == name), None)

        if not plugin:
            print(f"Error: Plugin '{name}' not found", file=sys.stderr)
            return

        print(f"\n{'='*80}")
        print(f"{plugin['name']} v{plugin.get('version', '?')}")
        print(f"{'='*80}\n")

        print(f"Description: {plugin.get('description', 'N/A')}")
        print(f"Category:    {plugin.get('category', 'N/A')}")
        print(f"Author:      {plugin.get('author', {}).get('name', 'N/A')}")
        print(f"Source:      {plugin.get('source', 'N/A')}")
        print(f"Keywords:    {', '.join(plugin.get('keywords', []))}")

        # Check for plugin.json in source dir
        source = plugin.get('source', '')
        if source:
            plugin_json = self.repo_root / source.replace('./', '') / '.claude-plugin' / 'plugin.json'
            if plugin_json.exists():
                print(f"\nPlugin manifest: {plugin_json}")

        marketplace_name = self.data.get('name', 'claude-agents-skills')
        print(f"\nInstall:")
        print(f"  /plugin marketplace add mrelph/{marketplace_name}")
        print(f"  /plugin install {name}@mrelph/{marketplace_name}")

    def install(self, name: str, target_dir: Optional[str] = None):
        """Install a plugin to the specified directory."""
        plugins = self._get_plugins()
        plugin = next((p for p in plugins if p['name'] == name), None)

        if not plugin:
            print(f"Error: Plugin '{name}' not found", file=sys.stderr)
            return

        source = plugin.get('source', '')
        src_path = self.repo_root / source.replace('./', '')

        if not src_path.exists():
            print(f"Error: Plugin source not found at {src_path}", file=sys.stderr)
            return

        if not target_dir:
            target_dir = '.claude/plugins/'

        target_path = Path(target_dir) / name
        target_path.mkdir(parents=True, exist_ok=True)

        print(f"Installing {name} v{plugin.get('version', '?')}...")
        print(f"  Source: {src_path}")
        print(f"  Destination: {target_path}")

        if target_path.exists():
            shutil.rmtree(target_path)

        shutil.copytree(src_path, target_path)
        print(f"Successfully installed {name} to {target_path}")

    def validate(self):
        """Validate marketplace and plugin JSONs."""
        errors = []

        # Validate marketplace.json
        print("Validating marketplace catalog...")
        required_fields = ['name', 'version', 'plugins']
        for field in required_fields:
            if field not in self.data:
                errors.append(f"marketplace.json: missing required field '{field}'")

        # Validate each plugin entry
        plugins = self._get_plugins()
        for plugin in plugins:
            name = plugin.get('name', '<unknown>')
            for field in ['name', 'source', 'description', 'version']:
                if field not in plugin:
                    errors.append(f"Plugin '{name}': missing field '{field}'")

            # Check plugin.json exists
            source = plugin.get('source', '')
            if source:
                plugin_json = self.repo_root / source.replace('./', '') / '.claude-plugin' / 'plugin.json'
                if not plugin_json.exists():
                    errors.append(f"Plugin '{name}': missing {plugin_json}")
                else:
                    try:
                        with open(plugin_json) as f:
                            pj = json.load(f)
                        if pj.get('version') != plugin.get('version'):
                            errors.append(
                                f"Plugin '{name}': version mismatch - "
                                f"marketplace says {plugin.get('version')}, "
                                f"plugin.json says {pj.get('version')}"
                            )
                    except json.JSONDecodeError as e:
                        errors.append(f"Plugin '{name}': invalid plugin.json - {e}")

        if errors:
            print(f"\nFound {len(errors)} error(s):")
            for err in errors:
                print(f"  - {err}")
            return False
        else:
            print(f"All {len(plugins)} plugins validated successfully.")
            return True


def main():
    parser = argparse.ArgumentParser(
        description="Claude Code Plugin Marketplace CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )

    subparsers = parser.add_subparsers(dest='command', help='Command to execute')

    # List command
    list_parser = subparsers.add_parser('list', help='List plugins')
    list_parser.add_argument('--category', help='Filter by category')

    # Search command
    search_parser = subparsers.add_parser('search', help='Search for plugins')
    search_parser.add_argument('query', help='Search query')

    # Info command
    info_parser = subparsers.add_parser('info', help='Show plugin details')
    info_parser.add_argument('name', help='Plugin name')

    # Install command
    install_parser = subparsers.add_parser('install', help='Install a plugin')
    install_parser.add_argument('name', help='Plugin name to install')
    install_parser.add_argument('--target', help='Target directory (optional)')

    # Validate command
    subparsers.add_parser('validate', help='Validate marketplace and plugin JSONs')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    cli = MarketplaceCLI()

    if args.command == 'list':
        cli.list_plugins(args.category)
    elif args.command == 'search':
        cli.search(args.query)
    elif args.command == 'info':
        cli.show_info(args.name)
    elif args.command == 'install':
        cli.install(args.name, args.target)
    elif args.command == 'validate':
        success = cli.validate()
        sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()

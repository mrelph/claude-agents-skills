#!/usr/bin/env python3
"""
Package individual plugins as ZIP files for direct installation.
Creates distributable packages in releases/plugins/ directory.
"""

import json
import os
import zipfile
from pathlib import Path
from typing import Dict, List


def load_marketplace(path: str = ".claude-plugin/marketplace.json") -> Dict:
    """Load marketplace.json to get plugin information."""
    with open(path, 'r') as f:
        return json.load(f)


def create_plugin_zip(plugin_entry: Dict, releases_dir: Path) -> str:
    """Create a ZIP file for a plugin."""
    name = plugin_entry["name"]
    version = plugin_entry.get("version", "1.0.0")
    source = plugin_entry.get("source", "").replace("./", "")
    source_path = Path(source)

    if not source_path.exists():
        print(f"  Error: Plugin directory not found: {source_path}")
        return None

    zip_filename = f"{name}-v{version}.zip"
    zip_path = releases_dir / zip_filename

    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(source_path):
            for file in files:
                file_path = Path(root) / file
                # Archive relative to plugins/ so it extracts as plugin-name/...
                arcname = file_path.relative_to(source_path.parent)
                zipf.write(file_path, arcname)

    file_size = zip_path.stat().st_size
    print(f"  Created: {zip_path} ({file_size:,} bytes)")
    return str(zip_path)


def create_releases_index(packaged: List[Dict], releases_dir: Path):
    """Create an index file listing all packaged plugins."""
    index = """# Plugin Releases

Direct download packages for individual plugin installation.

## Available Plugins

| Plugin | Version | Download |
|--------|---------|----------|
"""
    for pkg in sorted(packaged, key=lambda x: x["name"]):
        zip_name = Path(pkg["zip"]).name
        index += f"| {pkg['name']} | v{pkg['version']} | [{zip_name}]({zip_name}) |\n"

    index += """
## Installation

### Recommended: Plugin Marketplace

```bash
/plugin marketplace add mrelph/claude-agents-skills
/plugin install <plugin-name>@mrelph/claude-agents-skills
```

### Manual: ZIP Download

1. Download the plugin ZIP file
2. Extract to your project or global plugins directory
3. The plugin will be available in Claude Code
"""

    with open(releases_dir / "README.md", 'w') as f:
        f.write(index)


def main():
    print("=" * 60)
    print("Claude Code Plugin Packager")
    print("=" * 60)

    marketplace_data = load_marketplace()
    plugins = marketplace_data.get("plugins", [])

    print(f"\nFound {len(plugins)} plugins to package\n")

    releases_dir = Path("releases/plugins")
    releases_dir.mkdir(parents=True, exist_ok=True)

    packaged = []

    for plugin in plugins:
        name = plugin["name"]
        version = plugin.get("version", "1.0.0")
        print(f"Packaging: {name} v{version}")

        zip_path = create_plugin_zip(plugin, releases_dir)
        if zip_path:
            packaged.append({
                "name": name,
                "version": version,
                "zip": zip_path
            })

    create_releases_index(packaged, releases_dir)

    print(f"\n{'='*60}")
    print(f"Packaged {len(packaged)} plugins to {releases_dir}")
    print("=" * 60)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Package individual skills as ZIP files for direct installation.
Creates distributable packages in releases/ directory.
"""

import json
import os
import shutil
import zipfile
from pathlib import Path
from typing import Dict, List


def load_marketplace(path: str = "marketplace.json") -> Dict:
    """Load marketplace.json to get skill information."""
    with open(path, 'r') as f:
        return json.load(f)


def get_skill_entries(marketplace_data: Dict) -> List[Dict]:
    """Extract skill entries from marketplace data."""
    skills = []
    for plugin in marketplace_data.get("plugins", []):
        # Skills are in the Skills/ directory
        if plugin["source"].startswith("./Skills/"):
            skills.append(plugin)
    return skills


def create_skill_zip(skill_entry: Dict, releases_dir: Path) -> str:
    """
    Create a ZIP file for a skill that can be extracted directly to .claude/skills/

    Args:
        skill_entry: Marketplace entry for the skill
        releases_dir: Directory to save ZIP files

    Returns:
        Path to created ZIP file
    """
    skill_name = skill_entry["name"]
    skill_version = skill_entry["version"]
    source_path = Path(skill_entry["source"].replace("./", ""))

    if not source_path.exists():
        print(f"✗ Error: Skill directory not found: {source_path}")
        return None

    # Create ZIP filename
    zip_filename = f"{skill_name}-v{skill_version}.zip"
    zip_path = releases_dir / zip_filename

    # Create ZIP file
    # The ZIP should contain the skill directory that can be extracted to .claude/skills/
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Add all files from the skill directory
        for root, dirs, files in os.walk(source_path):
            for file in files:
                file_path = Path(root) / file
                # Archive name should be relative to Skills/ directory
                # So it extracts as: skill-name/SKILL.md, skill-name/README.md, etc.
                arcname = file_path.relative_to(source_path.parent)
                zipf.write(file_path, arcname)
                print(f"  Added: {arcname}")

    file_size = zip_path.stat().st_size
    print(f"✓ Created: {zip_path} ({file_size:,} bytes)")

    return str(zip_path)


def create_installation_instructions(skill_entry: Dict, zip_filename: str) -> str:
    """Create installation instructions for a skill ZIP."""
    skill_name = skill_entry["name"]

    instructions = f"""# {skill_name} Installation

## Quick Install

1. Download: `{zip_filename}`
2. Extract to your Claude Code skills directory:
   ```bash
   # Extract to .claude/skills/
   unzip {zip_filename} -d ~/.claude/skills/

   # Or for a specific project
   unzip {zip_filename} -d /path/to/project/.claude/skills/
   ```
3. The skill will be automatically available in Claude Code

## Verification

Check that the skill was installed correctly:
```bash
ls ~/.claude/skills/{skill_name}/SKILL.md
```

## Description

{skill_entry.get('description', 'No description available')}

## Version

{skill_entry.get('version', '1.0.0')}

## Keywords

{', '.join(skill_entry.get('keywords', []))}

---

For more information, see the [main marketplace README](../../README.md).
"""

    return instructions


def package_all_skills():
    """Package all skills from the marketplace into distributable ZIPs."""
    print("=" * 60)
    print("Claude Code Skills Packager")
    print("=" * 60)

    # Load marketplace
    marketplace_data = load_marketplace()
    skills = get_skill_entries(marketplace_data)

    print(f"\nFound {len(skills)} skills to package\n")

    # Create releases directory
    releases_dir = Path("releases/skills")
    releases_dir.mkdir(parents=True, exist_ok=True)

    packaged = []

    # Package each skill
    for skill in skills:
        skill_name = skill["name"]
        skill_version = skill["version"]

        print(f"\n📦 Packaging: {skill_name} v{skill_version}")

        zip_path = create_skill_zip(skill, releases_dir)

        if zip_path:
            # Create installation instructions
            instructions = create_installation_instructions(
                skill,
                Path(zip_path).name
            )

            # Save instructions
            instructions_path = releases_dir / f"{skill_name}-INSTALL.md"
            with open(instructions_path, 'w') as f:
                f.write(instructions)
            print(f"✓ Instructions: {instructions_path}")

            packaged.append({
                "name": skill_name,
                "version": skill_version,
                "zip": zip_path,
                "instructions": str(instructions_path)
            })

    # Create index file
    create_releases_index(packaged, releases_dir)

    print("\n" + "=" * 60)
    print(f"✓ Packaged {len(packaged)} skills to {releases_dir}")
    print("=" * 60)


def create_releases_index(packaged: List[Dict], releases_dir: Path):
    """Create an index file listing all packaged skills."""

    index_content = """# Skill Releases

Direct download packages for individual skill installation.

## Available Skills

| Skill | Version | Download | Install Guide |
|-------|---------|----------|---------------|
"""

    for pkg in sorted(packaged, key=lambda x: x["name"]):
        zip_name = Path(pkg["zip"]).name
        inst_name = Path(pkg["instructions"]).name

        index_content += f"| {pkg['name']} | v{pkg['version']} | [{zip_name}]({zip_name}) | [{inst_name}]({inst_name}) |\n"

    index_content += """
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
"""

    index_path = releases_dir / "README.md"
    with open(index_path, 'w') as f:
        f.write(index_content)

    print(f"\n✓ Created index: {index_path}")


if __name__ == "__main__":
    package_all_skills()

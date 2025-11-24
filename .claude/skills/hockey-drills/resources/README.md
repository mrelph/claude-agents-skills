# Hockey Drills Skill Resources

This directory contains supporting documentation and resources for the hockey-drills skill.

## Files

### drill-categories.md
Comprehensive list of common hockey drill categories organized by:
- Skill type (skating, passing, shooting, etc.)
- Practice phase (warm-up, conditioning, etc.)
- Age/skill level
- Team systems (breakouts, power play, etc.)

Use this as a reference when searching for drills or planning practices.

### examples.md
Practical examples demonstrating how to use the skill:
- Basic search examples
- Site-specific searches
- Practice planning workflows
- Position-specific training
- Troubleshooting tips

### README.md (this file)
Overview of the resources directory.

## Quick Reference

### Environment Variables

```bash
# Ice Hockey Systems
export IHS_USERNAME="your-username"
export IHS_PASSWORD="your-password"

# The Coaches Site
export TCS_USERNAME="your-username"
export TCS_PASSWORD="your-password"
```

### Common Commands

```bash
# Test authentication
python .claude/skills/hockey-drills/scripts/test-auth.py

# Search all sites
python .claude/skills/hockey-drills/scripts/search-drills.py "your query"

# Search specific site
python .claude/skills/hockey-drills/scripts/search-drills.py "your query" --site ihs

# Get drill details
python .claude/skills/hockey-drills/scripts/fetch-drill.py <drill-id>
```

## Updating This Skill

As the authenticated sites change their structure, you may need to update:

1. **HTML Parsing** (`search-drills.py`, `fetch-drill.py`):
   - Update CSS selectors to match current site structure
   - Inspect pages with browser dev tools
   - Test with actual searches

2. **Authentication** (`auth-helper.py`):
   - Update login form fields if sites change authentication
   - Adjust success detection logic
   - Update URLs if sites restructure

3. **Documentation** (SKILL.md, resources/):
   - Add new drill categories as discovered
   - Update examples with working searches
   - Document any new site features

## Contributing

If you find useful drill categories or search patterns not listed here, consider adding them to the appropriate resource file.

## Support

For issues with:
- **The skill itself**: Check troubleshooting in SKILL.md
- **Ice Hockey Systems**: Contact IHS support
- **The Coaches Site**: Contact TCS support
- **Authentication**: Run test-auth.py to diagnose

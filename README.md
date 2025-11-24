# Claude Agents Skills

This repository contains custom skills for Claude Code, enabling Claude to perform specialized tasks.

## Available Skills

### Hockey Drills Finder

A comprehensive skill for finding and retrieving hockey drills and practice information from authenticated coaching websites.

**Supported Sites:**
- Ice Hockey Systems (icehockeysystems.com)
- The Coaches Site (thecoachessite.com)

**Features:**
- Multi-site authentication support
- Search drills by skill type, age level, and team system
- Retrieve detailed drill instructions and diagrams
- Practice planning assistance
- Position-specific drill searches

**Location:** `.claude/skills/hockey-drills/`

**Documentation:** See [hockey-drills/SKILL.md](.claude/skills/hockey-drills/SKILL.md)

**Quick Start:**
```bash
# Set up credentials
export IHS_USERNAME="your-username"
export IHS_PASSWORD="your-password"
export TCS_USERNAME="your-username"
export TCS_PASSWORD="your-password"

# Install dependencies
pip install requests beautifulsoup4

# Test authentication
python .claude/skills/hockey-drills/scripts/test-auth.py

# Search for drills
python .claude/skills/hockey-drills/scripts/search-drills.py "passing drills"
```

## Using Skills with Claude Code

Skills in the `.claude/skills/` directory are automatically available to Claude Code. When you ask Claude about hockey drills or practice planning, it will automatically use this skill to help you.

**Example interactions:**
- "Show me some good passing drills for U12 players"
- "I need a 60-minute practice plan focusing on breakouts"
- "What are the best drills for improving one-timers?"
- "Find me some power play drills"

## Directory Structure

```
.claude/
└── skills/
    └── hockey-drills/
        ├── SKILL.md                    # Main skill documentation
        ├── scripts/
        │   ├── auth-helper.py         # Multi-site authentication
        │   ├── test-auth.py           # Authentication testing
        │   ├── search-drills.py       # Search functionality
        │   └── fetch-drill.py         # Fetch drill details
        └── resources/
            ├── README.md              # Resources overview
            ├── drill-categories.md    # Common drill categories
            └── examples.md            # Usage examples
```

## Requirements

- Python 3.7+
- requests
- beautifulsoup4
- Active membership on one or more supported sites

## Security

All credentials are stored in environment variables and never committed to version control. The skill uses HTTPS for all connections and session-based authentication.

## Contributing

To add a new skill:

1. Create a directory in `.claude/skills/` with your skill name
2. Add a `SKILL.md` file with proper frontmatter (see existing skills)
3. Create any necessary scripts in a `scripts/` subdirectory
4. Add supporting resources in a `resources/` subdirectory
5. Update this README with your new skill

For more information on creating skills, see the [Claude Code Skills documentation](https://docs.claude.com/en/docs/claude-code/skills).

## License

This repository contains personal skills and configurations for Claude Code.

## Support

For issues with:
- **Skills**: Open an issue in this repository
- **Claude Code**: See https://docs.claude.com/en/docs/claude-code
- **Site access**: Contact the respective coaching site support

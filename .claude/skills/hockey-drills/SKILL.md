---
name: hockey-drills
description: Find and retrieve hockey drills and practice information from Ice Hockey Systems and The Coaches Site. Use when you need hockey training drills, practice plans, coaching resources, or skill development exercises.
---
# Hockey Drills Finder

## Overview
This skill helps you search and retrieve hockey drills, practice plans, and coaching information from multiple authenticated hockey coaching websites:
- **Ice Hockey Systems** (icehockeysystems.com) - Comprehensive drill library and practice planning
- **The Coaches Site** (thecoachessite.com) - Professional coaching resources and drills

Both sites require member authentication to access their content.

## Setup

### 1. Authentication Credentials
You need member credentials for one or both sites. Set them as environment variables:

**Ice Hockey Systems:**
```bash
export IHS_USERNAME="your-username"
export IHS_PASSWORD="your-password"
```

**The Coaches Site:**
```bash
export TCS_USERNAME="your-username"
export TCS_PASSWORD="your-password"
```

**Important**:
- Never commit credentials to version control
- Add them to your shell profile or set them before running Claude Code
- You only need credentials for the sites you want to access
- The skill will automatically use available credentials

### 2. Dependencies
The skill uses Python with the following packages:
- `requests` - HTTP requests and session management
- `beautifulsoup4` - HTML parsing

Install dependencies:
```bash
pip install requests beautifulsoup4
```

### 3. Verify Setup
Test authentication with:
```bash
python .claude/skills/hockey-drills/scripts/test-auth.py
```

## Instructions

When the user asks about hockey drills or training:

1. **Understand the request**: Identify what type of drill or information they need:
   - Skill level (youth, high school, college, pro)
   - Drill type (skating, shooting, passing, defensive, goalie)
   - Practice focus (warmup, conditioning, power play, penalty kill)
   - Number of players or ice configuration

2. **Search for drills**: Use the search script to query available sites:
   ```bash
   # Search all available sites (default)
   python .claude/skills/hockey-drills/scripts/search-drills.py "search query"

   # Search specific site
   python .claude/skills/hockey-drills/scripts/search-drills.py "search query" --site ihs
   python .claude/skills/hockey-drills/scripts/search-drills.py "search query" --site tcs
   ```

3. **Fetch drill details**: If a specific drill is found, retrieve full details:
   ```bash
   python .claude/skills/hockey-drills/scripts/fetch-drill.py <drill-id>
   ```

4. **Present results**: Format the drill information clearly:
   - Drill name and objective
   - Setup and equipment needed
   - Step-by-step instructions
   - Coaching points and variations
   - Diagrams (if available)

## Common Use Cases

### Finding Drills by Category
```
User: "Show me some good passing drills for youth hockey"
Action: Search for youth passing drills and present top results
```

### Getting Practice Plans
```
User: "I need a 60-minute practice plan for U12 players focusing on breakouts"
Action: Search for U12 breakout practice plans and drills
```

### Specific Skill Development
```
User: "What are the best drills for improving one-timers?"
Action: Search for one-timer shooting drills across skill levels
```

## Security Notes

- Credentials are stored in environment variables, never in code
- Authentication uses HTTPS with session cookies
- Scripts validate credentials before making requests
- Failed authentication returns clear error messages

## Troubleshooting

**Authentication fails**:
- Verify environment variables are set correctly (IHS_* or TCS_*)
- Check that your membership is active for the respective site
- Ensure you're using the correct login credentials
- Try logging in via web browser first to verify credentials

**No results found**:
- Try broader search terms
- Check spelling of hockey terminology
- Some drills may require specific membership tiers

**Connection errors**:
- Verify internet connectivity
- Check if icehockeysystems.com is accessible
- Review firewall/proxy settings

## Resources

**Ice Hockey Systems:**
- Website: https://www.icehockeysystems.com
- Member login: https://www.icehockeysystems.com/members/home
- Support: Contact IHS support for account issues

**The Coaches Site:**
- Website: https://www.thecoachessite.com
- Member area: https://members.thecoachessite.com/
- Support: Contact TCS support for account issues

## File Structure

```
.claude/skills/hockey-drills/
├── SKILL.md                    # This file
├── scripts/
│   ├── search-drills.py       # Search for drills
│   ├── fetch-drill.py         # Get drill details
│   ├── test-auth.py           # Test authentication
│   └── auth-helper.py         # Shared authentication logic
└── resources/
    ├── drill-categories.md    # Common drill categories
    └── examples.md            # Example drills and searches
```

## Best Practices

1. **Always verify credentials are set** before attempting searches
2. **Cache results** when possible to avoid repeated authentication
3. **Respect rate limits** - don't hammer the site with rapid requests
4. **Provide context** - include skill level and drill type in searches
5. **Format output clearly** - make drills easy to read and implement

## Limitations

- Requires active membership on at least one of the supported sites
- Search results depend on available member content for your account
- Some premium drills may require upgraded membership tiers
- Site structure changes may require script updates
- Each site may have different drill formats and categorization

## Supported Sites

| Site | Code | Environment Variables | Member URL |
|------|------|----------------------|------------|
| Ice Hockey Systems | `ihs` | `IHS_USERNAME`, `IHS_PASSWORD` | https://www.icehockeysystems.com/members/home |
| The Coaches Site | `tcs` | `TCS_USERNAME`, `TCS_PASSWORD` | https://members.thecoachessite.com/ |

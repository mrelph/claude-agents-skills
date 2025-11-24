# Example Searches and Use Cases

This document provides examples of how to use the hockey-drills skill effectively.

## Basic Search Examples

### Finding Drills by Skill Type

**Request**: "Show me some passing drills"
```bash
python .claude/skills/hockey-drills/scripts/search-drills.py "passing drills"
```

**Request**: "I need shooting drills for one-timers"
```bash
python .claude/skills/hockey-drills/scripts/search-drills.py "one-timer shooting drills"
```

### Age-Specific Searches

**Request**: "What are good drills for U10 players?"
```bash
python .claude/skills/hockey-drills/scripts/search-drills.py "U10 youth drills"
```

**Request**: "Advanced skating drills for high school players"
```bash
python .claude/skills/hockey-drills/scripts/search-drills.py "high school advanced skating"
```

### System-Specific Searches

**Request**: "I need power play drills"
```bash
python .claude/skills/hockey-drills/scripts/search-drills.py "power play drills"
```

**Request**: "Show me breakout drills"
```bash
python .claude/skills/hockey-drills/scripts/search-drills.py "breakout zone exit drills"
```

## Site-Specific Searches

### Search Only Ice Hockey Systems

```bash
python .claude/skills/hockey-drills/scripts/search-drills.py "defensive zone coverage" --site ihs
```

### Search Only The Coaches Site

```bash
python .claude/skills/hockey-drills/scripts/search-drills.py "3-on-2 rush drills" --site tcs
```

### Search All Available Sites

```bash
python .claude/skills/hockey-drills/scripts/search-drills.py "penalty kill formation drills"
# Automatically searches all sites with configured credentials
```

## Advanced Search Examples

### Limit Results

```bash
python .claude/skills/hockey-drills/scripts/search-drills.py "skating drills" --max 5
# Returns maximum 5 results per site
```

### JSON Output for Processing

```bash
python .claude/skills/hockey-drills/scripts/search-drills.py "passing drills" --json
# Returns results in JSON format for further processing
```

### Combining Multiple Parameters

```bash
python .claude/skills/hockey-drills/scripts/search-drills.py "U12 small area games" --site ihs --max 3 --json
# Search IHS only, max 3 results, JSON output
```

## Practice Planning Examples

### 60-Minute Practice for U12

**Request**: "Help me plan a 60-minute practice for U12 players focusing on passing and breakouts"

**Workflow**:
1. Search for U12 passing drills
2. Search for U12 breakout drills
3. Search for U12 warm-up activities
4. Combine results into a structured practice plan

```bash
# Warm-up (10 min)
python .claude/skills/hockey-drills/scripts/search-drills.py "U12 warmup skating"

# Skill work (20 min)
python .claude/skills/hockey-drills/scripts/search-drills.py "U12 passing drills"

# Team concepts (20 min)
python .claude/skills/hockey-drills/scripts/search-drills.py "U12 breakout drills"

# Scrimmage (10 min)
python .claude/skills/hockey-drills/scripts/search-drills.py "small area games U12"
```

### Position-Specific Training

**Request**: "I want to work on defensive skills for defensemen"

```bash
python .claude/skills/hockey-drills/scripts/search-drills.py "defenseman gap control drills"
python .claude/skills/hockey-drills/scripts/search-drills.py "D-zone coverage drills"
python .claude/skills/hockey-drills/scripts/search-drills.py "defensive skating backwards crossovers"
```

### Goalie Practice

**Request**: "What are good goalie drills for working on lateral movement?"

```bash
python .claude/skills/hockey-drills/scripts/search-drills.py "goalie lateral movement drills"
python .claude/skills/hockey-drills/scripts/search-drills.py "goalie post-to-post drills"
```

## Fetching Drill Details

After finding drills, you can fetch full details:

```bash
# First, search for drills
python .claude/skills/hockey-drills/scripts/search-drills.py "2-on-1 drills"

# Note the drill ID from results, then fetch details
python .claude/skills/hockey-drills/scripts/fetch-drill.py <drill-id>

# Example with specific drill ID
python .claude/skills/hockey-drills/scripts/fetch-drill.py 12345
```

## Troubleshooting Examples

### No Results Found

If a search returns no results, try:

1. **Broader terms**: "passing" instead of "saucer pass drills"
2. **Different phrasing**: "zone exit" instead of "breakout"
3. **Remove specificity**: "skating" instead of "U12 advanced edge work"
4. **Check another site**: Use `--site` to try different sources

### Authentication Issues

Test your authentication setup:

```bash
# Test all configured sites
python .claude/skills/hockey-drills/scripts/test-auth.py

# Test specific site
python .claude/skills/hockey-drills/scripts/test-auth.py ihs
python .claude/skills/hockey-drills/scripts/test-auth.py tcs
```

## Integration with Claude

When Claude uses this skill, the workflow is typically:

1. **User asks about hockey drills**
   - "I need some good passing drills for my team"

2. **Claude identifies requirements**
   - Skill level, drill type, number needed

3. **Claude searches using the scripts**
   - Runs search-drills.py with appropriate parameters

4. **Claude presents formatted results**
   - Summarizes findings
   - Highlights most relevant drills
   - Provides drill details if needed

5. **Claude can fetch details**
   - If user wants more info on a specific drill
   - Uses fetch-drill.py to get full details

## Best Practices

1. **Start broad, then narrow**: Begin with general searches, then add specificity
2. **Use age/level indicators**: Always include skill level for best results
3. **Combine terms**: "U12 passing small area games" works better than just "passing"
4. **Check both sites**: Different sites may have different drill libraries
5. **Test authentication first**: Run test-auth.py before starting a practice planning session
6. **Save useful drill IDs**: Keep track of drill IDs for drills you use frequently

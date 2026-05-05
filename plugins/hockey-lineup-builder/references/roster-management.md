# Roster Management — Importing & Updating Power Rankings

Player ratings are **not hardcoded**. Refresh them at any time by importing an Excel, CSV, or JSON file. The import regenerates `references/roster.md` and the roster dict in `scripts/lineup_generator.py`.

## How to Import

1. **Save the file** (Excel, CSV, or JSON) to a working location.
2. **Run the update script**:

```bash
python3 scripts/update_roster.py <path_to_roster.xlsx>
# or
python3 scripts/update_roster.py <path_to_roster.csv>
# or inline:
python3 scripts/update_roster.py --json '{"players": [...]}'
```

3. **Review the output** — the script reports tier counts, positional depth, and what it updated.
4. **Read the refreshed `references/roster.md`** to confirm before building lineups.

## Expected File Format

Excel or CSV needs at minimum two columns (case-insensitive, flexible matching):

| Column | Aliases | Required | Example |
|--------|---------|----------|---------|
| Name | Name, Player, Player Name | Yes | Player Name |
| Rating | Rating, Power Ranking, Rank, Score | Yes | 1.00 or 2.50 |
| Position | Position, Pos | No (defaults to F) | F / D / F/D / G |
| Notes | Notes, Comments | No | Elite two-way player |
| Can Also Play | Can Also Play, Alt Position | No (goalies) | Forward (emergency) |

Use `G` for goalies in the Position column. Use `F/D` for versatile players.

### Rating Scale

The default scale is **1–3 (lower is better)**:

| Rating | Tier | Description |
|--------|------|-------------|
| 1.00 | Elite | Top tier for the level |
| 1.50 | Strong Skilled | Solid contributor |
| 1.75 | Strong Two-Way | Reliable player |
| 2.00 | Developing Contributor | Consistent middle tier |
| 2.50 | Developing | Needs sheltered minutes |
| 3.00 | Significant Development | Requires heavy sheltering |

> Ratings outside 0.50–5.00 generate a warning. The script also accepts a 1–5 scale if any rating exceeds 3.0.

## Example CSV

```csv
Name,Position,Rating,Notes
Player One,F/D,1.00,"Elite at both positions"
Player Two,F/D,1.00,"Elite talent, leadership"
Player Three,F/D,1.50,"Versatile two-way player"
Player Four,F,2.00,"Consistent contributor"
Goalie One,G,2.00,"Reliable starter"
```

## JSON Alternative (Inline)

```bash
python3 scripts/update_roster.py --json '{"players": [
  {"name": "Player One", "position": "F/D", "rating": 1.00, "notes": "Elite"},
  {"name": "Player Two", "position": "F/D", "rating": 1.25, "notes": "Rating adjusted"}
]}'
```

## Dry Run

Preview changes without writing files:

```bash
python3 scripts/update_roster.py --dry-run <path_to_roster.xlsx>
```

This prints the generated `roster.md` content to the console for review.

## What Gets Updated

- **`references/roster.md`** — fully regenerated with ratings, tiers, positional depth analysis, and deployment notes
- **`scripts/lineup_generator.py`** — internal roster dict updated to match

## Post-Update Checklist

- [ ] Read `references/roster.md` and confirm ratings, tiers, and counts
- [ ] Check `scripts/lineup_generator.py` — verify the roster dict updated
- [ ] Review tier assignments for players who shifted between tiers
- [ ] Check F/D versatile count — affects formation options
- [ ] Review average team rating — significant changes may shift strategy recommendations

## When to Re-Import

- New season (full roster refresh)
- Mid-season player added / removed
- Power rankings updated based on recent performance
- Player moved tiers (e.g. development player improved enough to move up)

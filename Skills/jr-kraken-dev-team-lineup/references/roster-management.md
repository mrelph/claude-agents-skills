# Roster Management - Updating Power Rankings

Player ratings are **not hardcoded** -- refresh them at any time by uploading a new Excel or CSV file. This updates both `references/roster.md` and the roster in `scripts/lineup_generator.py`.

## Rating Scales

The script supports two rating scales (lower is better on both):

| | 1-3 Scale | 1-5 Scale |
|--|-----------|-----------|
| **Elite** | 1.00-1.50 | 1.00-2.50 |
| **Strong** | 1.75-2.00 | 2.75-3.50 |
| **Role** | 2.50-3.00 | 3.75-5.00 |

**Auto-detection**: If any player rating exceeds 3.0, the script uses the 1-5 scale. Otherwise it uses 1-3. Override with `--scale 3` or `--scale 5`.

## How to Update

When a new roster file (Excel, CSV) is provided or player ratings need updating:

1. **Save the uploaded file** to a working location.
2. **Run the update script**:

```bash
python3 scripts/update_roster.py <path_to_roster.xlsx>
# or
python3 scripts/update_roster.py <path_to_roster.csv>
# Force a specific scale:
python3 scripts/update_roster.py --scale 5 <path_to_roster.xlsx>
```

3. **Review the output** -- the script reports the detected scale, tier counts, and what it updated.
4. **Read the refreshed `references/roster.md`** to confirm the new ratings are correct before building any lineups.

## Expected File Format

The Excel or CSV file needs at minimum two columns (case-insensitive, flexible matching):

| Column | Aliases | Required | Example |
|--------|---------|----------|---------|
| Name | Name, Player, Player Name | Yes | Player Name |
| Rating | Rating, Power Ranking, Rank, Score | Yes | 1.00 or 2.50 |
| Position | Position, Pos | No (defaults to F) | F/D |
| Notes | Notes, Comments | No | Elite two-way player |
| Can Also Play | Can Also Play, Alt Position | No (goalies) | Forward (emergency) |

Use `G` for goalies in the Position column. Use `F/D` for versatile players.

## Example CSV (1-3 Scale)

```csv
Name,Position,Rating,Notes
Player One,F/D,1.00,"Elite at both positions"
Player Two,F/D,1.00,"Elite talent, leadership"
Player Three,F/D,1.50,"Versatile two-way player"
Goalie One,G,2.00,"Reliable starter"
```

## Example CSV (1-5 Scale)

```csv
Name,Position,Rating,Notes
Player One,F/D,1.50,"Elite at both positions"
Player Two,F,2.00,"Strong skilled forward"
Player Three,D,3.25,"Solid contributor"
Player Four,F,4.00,"Role player, situational"
Goalie One,G,3.00,"Reliable starter"
```

## JSON Alternative

For inline updates without a file:

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

## What Gets Updated

- **`references/roster.md`** -- fully regenerated with new ratings, tiers, positional depth analysis, and deployment notes
- **`scripts/lineup_generator.py`** -- the internal roster dict is updated to match

## After Updating

After refreshing the roster, re-read `references/roster.md` before building any lineups. The tier groupings (Elite, Strong, Role) and lineup templates may shift based on the new ratings. Pay attention to:
- Players who moved between tiers
- Changes in line assignments based on new rankings
- Shifts in F/D versatile player count
- Updated average team rating

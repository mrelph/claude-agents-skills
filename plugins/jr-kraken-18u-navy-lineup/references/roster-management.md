# Roster Management - Updating Power Rankings

Player ratings are **not hardcoded** -- refresh them at any time by uploading a new Excel or CSV file. This updates both `references/roster.md` and the roster in `scripts/lineup_generator.py`.

## How to Update

When a new roster file (Excel, CSV) is provided or player ratings need updating:

1. **Save the uploaded file** to a working location.
2. **Run the update script**:

```bash
python3 scripts/update_roster.py <path_to_roster.xlsx>
# or
python3 scripts/update_roster.py <path_to_roster.csv>
```

3. **Review the output** -- the script reports tier counts, positional depth, and what it updated.
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

### Rating Scale

The script uses a 1-3 rating scale (lower is better):

| Rating | Tier | Description |
|--------|------|-------------|
| 1.00 | Elite | Top tier for 18U C level |
| 1.50 | Strong Skilled | Solid contributor |
| 1.75 | Strong Two-Way | Reliable player |
| 2.00 | Developing Contributor | Consistent middle tier |
| 2.50 | Developing | Needs sheltered minutes |
| 3.00 | Significant Development | Requires heavy sheltering |

> Ratings outside the 0.50-5.00 range will generate a warning. The script also accepts a 1-5 scale if ratings exceed 3.0.

## Example CSV

```csv
Name,Position,Rating,Notes
Player One,F/D,1.00,"Elite at both positions"
Player Two,F/D,1.00,"Elite talent, leadership"
Player Three,F/D,1.50,"Versatile two-way player"
Player Four,F,2.00,"Consistent contributor"
Goalie One,G,2.00,"Reliable starter"
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

This prints the generated `roster.md` content to the console so you can review tier assignments and positional depth before committing changes.

## What Gets Updated

- **`references/roster.md`** -- fully regenerated with new ratings, tiers, positional depth analysis, and deployment notes
- **`scripts/lineup_generator.py`** -- the internal roster dict is updated to match

## Post-Update Checklist

After refreshing the roster, verify these before building any lineups:

- [ ] **Read `references/roster.md`** -- confirm new ratings, tier assignments, and player counts are correct
- [ ] **Check `scripts/lineup_generator.py`** -- verify the roster dict was updated (elite/strong/development groupings)
- [ ] **Review tier assignments** -- look for players who moved between tiers
- [ ] **Check F/D versatile count** -- shifts in versatile player count affect formation options
- [ ] **Review average team rating** -- significant changes may affect strategy recommendations

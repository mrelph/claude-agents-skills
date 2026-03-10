# TeamSnap Integration - RSVP Checking

When the TeamSnap MCP is available, use it as the **first step** in any lineup-building workflow to get real-time player availability.

## How to Use

1. **Check if TeamSnap MCP tools are available** -- look for `mcp__teamsnap__*` tools. If not available, fall back to asking for availability manually.
2. **Pull RSVPs for the upcoming game** -- use the TeamSnap MCP to list events/games and retrieve RSVP statuses for each player.
3. **Map RSVPs to roster** -- match TeamSnap player names to the roster in `references/roster.md`. Categorize players as:
   - **Available (Yes)** -- confirmed attending, include in lineup
   - **Not Available (No)** -- confirmed absent, plan around their absence
   - **Maybe / No Response** -- flag for Coach Mark to follow up on; build a contingency lineup assuming they are out
4. **Adjust lineup strategy** -- based on who is available:
   - If missing 1-2 forwards: use F/D versatile players to fill gaps
   - If missing 3+ forwards: consider 3-line system
   - If missing defense: move F/D players back (see `roster.md` for F/D versatile list)
   - If multiple top-ranked players are out: see absence contingency plans in `roster.md`

## Workflow Example

```
Step 1: "Checking TeamSnap for RSVPs..."
        → Use TeamSnap MCP to get game event and RSVP list

Step 2: "Availability for Saturday's game:
         YES (13): [list confirmed players from roster.md]
         NO (2):   [list absent players]
         MAYBE (2): [list uncertain players]"

Step 3: "With 2 confirmed out and 2 uncertain:
         - 11 confirmed skaters + 2 goalies
         - Building a 3-line base lineup with contingency for 4 lines if uncertain players confirm
         - Assess which positions are affected and plan F/D moves"

Step 4: Build the lineup using the standard process in game-planning.md
```

## When TeamSnap Is Not Available

If the TeamSnap MCP is not configured or unavailable:
- Ask directly: "Which players are available for this game?"
- Or ask: "Are there any absences to plan around?"
- Reference the absence contingency plans in `roster.md` for common scenarios

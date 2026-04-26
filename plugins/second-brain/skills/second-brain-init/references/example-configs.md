# Example configs

Sample `.second-brain.json` shapes for common domains. Use as references for the kind of specificity that produces a good assistant contract — copy and adapt, don't paste verbatim.

## Research notes (papers, authors, methods)

```json
{
  "projectName": "AI Alignment Research",
  "defaultAgent": "claude-code",
  "schema": {
    "domain": "AI alignment research papers, authors, and the arguments they make",
    "entityTypes": ["papers", "authors", "concepts", "methods"],
    "commonQueries": [
      "What has [author] said about [concept]?",
      "Which papers cite [paper]?",
      "What are the key arguments for/against [position]?"
    ],
    "styleGuide": "Concise. Cite sources inline. Mark synthesis vs sourced facts explicitly."
  },
  "wiki": { "linkStyle": "wikilinks", "frontmatter": true, "pageNaming": "title-case" },
  "sourceHandling": { "mode": "archive-after-ingest" }
}
```

## Personal journal

```json
{
  "projectName": "Journal",
  "defaultAgent": "claude-code",
  "schema": {
    "domain": "personal journal entries, recurring themes, and people in my life",
    "entityTypes": ["people", "themes", "events", "places"],
    "commonQueries": [
      "When did I last write about [topic]?",
      "What was I thinking about [time period]?"
    ],
    "styleGuide": "First-person, prose-heavy. Surface emotional patterns. Don't sanitize."
  },
  "wiki": { "linkStyle": "wikilinks", "frontmatter": true, "pageNaming": "sentence-case" },
  "sourceHandling": { "mode": "leave-in-inbox" }
}
```

## Recipe collection

```json
{
  "projectName": "Recipes",
  "defaultAgent": "claude-code",
  "categories": ["recipes"],
  "schema": {
    "domain": "weeknight recipes, cooking techniques, and ingredient notes",
    "entityTypes": ["dishes", "techniques", "ingredients", "cuisines"],
    "commonQueries": [
      "What can I make in under 30 minutes?",
      "Which recipes use [ingredient]?",
      "Which techniques pair with [dish type]?"
    ],
    "styleGuide": "Each recipe page: cook time, ingredient list, brief why-it-works. No life stories."
  },
  "wiki": { "linkStyle": "markdown", "frontmatter": true, "pageNaming": "kebab-case" }
}
```

## Engineering / project notes

```json
{
  "projectName": "Engineering Brain",
  "defaultAgent": "claude-code",
  "schema": {
    "domain": "engineering decisions, architecture notes, and project post-mortems across my work",
    "entityTypes": ["projects", "systems", "decisions", "incidents", "tools"],
    "commonQueries": [
      "What did we decide about [topic] and why?",
      "Which systems depend on [component]?",
      "What went wrong in [incident] and what did we change?"
    ],
    "styleGuide": "Imperative, terse. Decisions as ADRs with date + rationale. Link liberally."
  },
  "wiki": { "linkStyle": "markdown", "frontmatter": true, "pageNaming": "title-case" },
  "sourceHandling": { "mode": "archive-after-ingest" }
}
```

## Minimal (when the user can't or won't specify much)

```json
{
  "projectName": "My Knowledge Base",
  "defaultAgent": "claude-code",
  "schema": {
    "domain": "general personal notes and reference material"
  },
  "wiki": { "linkStyle": "wikilinks" }
}
```

`normalizeConfig` fills in defaults for everything else. Better to ship a thin config than to invent entity types and queries the user didn't agree to.

## Patterns to notice

- `domain` is a *sentence*, not a noun phrase. "AI alignment papers and arguments" beats "AI alignment".
- `entityTypes` are *types*, not instances. "authors" not "Stuart Russell".
- `commonQueries` use placeholder syntax (`[author]`, `[concept]`) so the assistant knows they're templates, not literal questions.
- `styleGuide` is read by the assistant on every session — keep it tight, opinionated, and concrete. "Concise" is weak; "Cite sources inline" is strong.
- `sourceHandling.mode` matters more than it looks. `archive-after-ingest` keeps `inbox/` clean (good for high-volume); `leave-in-inbox` keeps everything visible (good for journal-style flows where you re-read sources).

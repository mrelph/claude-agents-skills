# Ingest heuristics

Use when the user pointed at a folder of existing material instead of starting fresh. The goal: read enough to draft a credible config, then **show the draft and let the user correct it**. Never silently bake assumptions.

## What to read

- List the folder. If >50 files, sample. Prefer recently-modified.
- Read 5-15 representative files end-to-end. Skip if >10k tokens; sample beginning + headings instead.
- Prioritize `.md`, `.txt`, `.org`, `.rst`. Skip binaries, images, and code source unless the folder is clearly a code-notes situation.
- If a `README.md` or `index.md` exists, read it first — it usually states the folder's purpose.

## What to infer

### `projectName`

- Default to the folder's basename, title-cased.
- If the README has a clear `# Heading`, use that instead.

### `schema.domain`

- Synthesize from file content, README, and folder structure. Aim for one specific sentence.
- Bias toward what the *content* is about, not what the *folder* is named.
- If the folder has clear topical clusters, mention them ("a journal of X and Y").

### `schema.entityTypes`

- Look at recurring nouns at the *type* level (not specific entities). If most pages are about a person, "people" or "authors" is an entity type, not the specific person's name.
- Look at folder substructure: subfolders often map to entity types (`people/`, `projects/`, `books/`).
- Look at YAML frontmatter `type:` or `category:` fields if present.
- 3-6 items. If unclear, leave empty rather than guessing.

### `schema.commonQueries`

- Hard to infer. Either skip (empty array is fine) or ask the user one targeted question after showing the rest of the draft: "What's a question you'd want this to answer well? I'll add it to the config."

### `wiki.linkStyle`

- If existing files use `[[Page Name]]` syntax → `wikilinks`.
- If existing files use `[Page](page.md)` → `markdown`.
- If neither (e.g. all standalone notes) → `wikilinks` default. Ask if uncertain.

### `wiki.frontmatter`

- If existing files have YAML frontmatter (`---\nfield: value\n---`) → `true`.
- Otherwise → `false`. The contract should match what the user already does.

### `categories`

- Scan subfolder names. If the user has folders beyond the built-in `entities`, `concepts`, `topics`, propose those as additional categories. Don't propose generic folders like `archive`, `inbox`, `drafts`.

## Things NOT to infer

- `defaultAgent` — always `"claude-code"` in this skill context.
- `sourceHandling.mode` — leave default `"user-directed"`. Behavioral preference, ask if it matters.
- `wiki.pageNaming` — usually obvious from existing files; if pages are `like-this.md` use `kebab-case`, if `Like This.md` use `title-case`. Default to `title-case`.

## Conflict resolution

If existing material disagrees with itself (some files have frontmatter, some don't; mix of link styles), pick the **majority pattern** and note the disagreement to the user in the confirmation step. The user might have a preference for what the new contract should enforce going forward.

## Output

After inferring, present:

1. The drafted JSON config in a code block.
2. A short list of "things I noticed" — particularly anything inferred (entity types, link style) that the user might want to adjust.
3. An ask: "Confirm, or tell me what to change."

Then wait for the user's response before invoking the CLI.

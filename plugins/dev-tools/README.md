# Dev Tools Plugin

A collection of specialized development agents for Claude Code.

## Agents

| Agent | Purpose |
|-------|---------|
| **bug-tracker-resolver** | Manages bugs in Bugs.md, root cause analysis, resolution plans |
| **database-architect** | PostgreSQL/Supabase schema design, query optimization, RLS policies |
| **security-code-scanner** | Vulnerability identification, OWASP Top 10 analysis |
| **performance-optimizer** | Core Web Vitals, bundle size, runtime efficiency |
| **documentation-maintainer** | READMEs, API docs, user guides, documentation consistency |

## Installation

```bash
/plugin marketplace add mrelph/claude-agents-skills
/plugin install dev-tools@mrelph/claude-agents-skills
```

## Usage

Agents are invoked automatically by Claude when relevant, or manually via the `/agents` interface.

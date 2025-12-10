# Claude Code Agents

Specialized task-focused agents that can be spawned via the Task tool in Claude Code for specific development and business tasks.

## Available Agents

### Development Agents

| Agent | Description |
|-------|-------------|
| [bug-tracker-resolver](bug-tracker-resolver.md) | Manages bugs in Bugs.md, performs root cause analysis, creates resolution plans, implements and tests fixes |
| [database-architect](database-architect.md) | PostgreSQL/Supabase expertise - schema design, query optimization, RLS policies, indexing strategies |
| [documentation-maintainer](documentation-maintainer.md) | Creates and updates READMEs, API docs, user guides, ensures documentation consistency |
| [performance-optimizer](performance-optimizer.md) | Core Web Vitals, bundle size reduction, runtime efficiency, Next.js optimizations |
| [security-code-scanner](security-code-scanner.md) | Vulnerability identification, OWASP Top 10 analysis, risk assessment, secure code recommendations |

### Design & Planning Agents

| Agent | Description |
|-------|-------------|
| [ux-ui-design-expert](ux-ui-design-expert.md) | UX/UI guidance, information architecture, accessibility (WCAG), responsive design |
| [roadmap-feature-planner](roadmap-feature-planner.md) | Strategic feature planning, implementation coordination, roadmap tracking |

### Media Agents

| Agent | Description |
|-------|-------------|
| [video-integration-specialist](video-integration-specialist.md) | YouTube/Vimeo integration, video player implementation, streaming optimization |

## Usage

### In Claude Code

Agents are automatically available when placed in your project's `.claude/agents/` directory:

```bash
# Copy an agent to your project
mkdir -p /path/to/project/.claude/agents/
cp database-architect.md /path/to/project/.claude/agents/
```

The agent will then be available via the Task tool:

```
Use the database-architect agent to design a schema for user authentication.
```

### Agent Structure

Each agent is a markdown file with YAML frontmatter:

```yaml
---
name: agent-name
description: What this agent specializes in
model: sonnet          # or opus, haiku
color: blue            # UI color coding
allowed-tools: Read, Write, Bash, Grep, Glob, Task, WebSearch
---

# Agent Name

## Role & Expertise
[What the agent specializes in...]

## Workflow
[How the agent approaches tasks...]

## Best Practices
[Guidelines the agent follows...]
```

### Key Frontmatter Fields

| Field | Description |
|-------|-------------|
| `name` | Unique identifier for the agent |
| `description` | Brief summary shown in agent selection |
| `model` | Which Claude model to use (sonnet, opus, haiku) |
| `color` | UI color for agent identification |
| `allowed-tools` | Tools the agent can access |

## Agent Capabilities by Tool Access

### Full Development Access
- **database-architect**: Read, Write, Bash, Grep, Glob, Task, WebSearch, WebFetch
- **performance-optimizer**: Read, Write, Bash, Grep, Glob, Task, WebSearch
- **security-code-scanner**: Read, Bash, Grep, Glob, Task

### Documentation Focus
- **documentation-maintainer**: Read, Write, Glob, Grep

### Research & Analysis
- **ux-ui-design-expert**: Read, WebSearch, WebFetch, Task
- **roadmap-feature-planner**: Read, Write, Glob, Grep, Task

### Specialized
- **bug-tracker-resolver**: Read, Write, Bash, Grep, Glob
- **video-integration-specialist**: Read, Write, Bash, WebSearch, WebFetch, Task

## Creating New Agents

1. Create a new `.md` file in this directory
2. Add YAML frontmatter with required fields
3. Define the agent's role, expertise, and workflow
4. Specify appropriate tool access
5. Test the agent with representative tasks

### Template

```markdown
---
name: my-new-agent
description: Brief description of agent's purpose
model: sonnet
color: green
allowed-tools: Read, Write, Bash, Grep, Glob
---

# My New Agent

## Role & Expertise

[Describe what this agent specializes in...]

## Workflow

1. [Step one...]
2. [Step two...]
3. [Step three...]

## Best Practices

- [Guideline one...]
- [Guideline two...]

## Limitations

- [What this agent should NOT do...]
```

## Best Practices

1. **Scope appropriately**: Each agent should have a focused area of expertise
2. **Limit tool access**: Only grant tools the agent actually needs
3. **Document workflows**: Clear step-by-step processes help agents perform consistently
4. **Include limitations**: Explicitly state what the agent should not attempt
5. **Use appropriate models**:
   - `haiku` for quick, simple tasks
   - `sonnet` for most development work
   - `opus` for complex reasoning tasks

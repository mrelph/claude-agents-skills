---
name: kiro-spec-driven-development
description: Structured spec-driven development workflow that transforms feature ideas into requirements, design documents, and implementation plans using Kiro methodology
allowed-tools: Read, Write, Bash, Grep, Glob, Task, AskUserQuestion, TodoWrite
category: development
metadata:
  version: 1.0.0
  last-updated: 2025-12-28
---

# Kiro Spec-Driven Development

Transform vague feature ideas into well-defined, implementable specifications through a structured three-phase workflow: Requirements → Design → Tasks.

## When to Use This Skill

Invoke this skill when you need to:
- Plan a new feature systematically before coding
- Create requirement specifications and design documents
- Break down complex features into actionable tasks
- Review or improve existing spec files
- Follow a disciplined, iterative development workflow

## How It Works

This skill guides you through Kiro's spec-driven methodology using specialized sub-agents for each phase:

### Phase 1: Requirements Gathering
Creates a requirements document that captures **WHAT** needs to be built:
- Feature description and user stories
- Acceptance criteria in Given/When/Then format
- Non-functional requirements (performance, security, etc.)

**Sub-agent:** `spec-requirements` (in references/)

### Phase 2: Design Documentation
Creates a design document that defines **HOW** to build it:
- Architecture overview and component interactions
- Data models, API contracts, type definitions
- Integration points with existing systems
- Security considerations and error handling

**Sub-agent:** `spec-design` (in references/)

### Phase 3: Task Planning
Creates an actionable implementation plan:
- Granular, independently completable tasks
- Dependencies and ordering
- Progress tracking with checkboxes
- Links back to requirements for validation

**Sub-agent:** `spec-tasks` (in references/)

## Workflow Process

The skill follows a strict iterative workflow (see `references/workflow-definition.md` for complete details):

1. **Initialize**: Create feature directory structure at `.claude/specs/{feature-name}/`
2. **Requirements**: Draft requirements → User reviews → Iterate until approved
3. **Design**: Create design based on requirements → User reviews → Iterate until approved
4. **Tasks**: Break down into tasks → User reviews → Iterate until approved
5. **Implementation**: Optionally execute tasks using `spec-impl` sub-agent

**Key Principle**: User approval is required at each phase before proceeding to the next.

## Sub-Agents

This skill orchestrates multiple specialized sub-agents (all in `references/`):

- **spec-requirements** - Creates/refines requirements documents (supports parallel execution)
- **spec-design** - Creates/refines design documents (supports parallel execution)
- **spec-tasks** - Creates/refines task breakdowns (supports parallel execution)
- **spec-judge** - Evaluates and selects best versions from parallel executions
- **spec-impl** - Implements code from task list (optional)
- **spec-test** - Creates test documentation and code (optional)
- **spec-system-prompt-loader** - Loads workflow system prompts

## Parallel Execution

For faster iteration, you can run multiple versions in parallel:
- The skill will ask: "How many spec-requirements agents to use? (1-128)"
- Multiple sub-agents generate different versions
- `spec-judge` uses tree-based evaluation to select the best version
- Works for requirements, design, and tasks phases

## Quality Criteria

**Good Requirements:**
- Testable and measurable
- User-focused, not implementation-focused
- Complete coverage of feature scope

**Good Design:**
- Addresses all requirements
- Considers edge cases and error states
- Follows project conventions

**Good Tasks:**
- Small enough to complete in one session
- Clear definition of done
- Properly ordered by dependencies

## Output Structure

Creates files in `.claude/specs/{feature-name}/`:
```
.claude/specs/user-authentication/
├── requirements.md
├── design.md
└── tasks.md
```

## Usage Examples

**Starting a new feature:**
```
User: "I want to add a notification system to my app"
Skill: [Initializes spec workflow, creates requirements draft]
```

**Reviewing existing specs:**
```
User: "Can you explain what's in the specs folder?"
Skill: [Reads all spec files, explains workflow and current progress]
```

**Updating a spec:**
```
User: "Update the design to use WebSockets instead of polling"
Skill: [Calls spec-design sub-agent with update request]
```

## Reference Materials

See `references/` directory for:
- `workflow-definition.md` - Complete workflow system prompt with Mermaid diagrams
- All sub-agent definitions with detailed instructions

## Best Practices

1. Always start with requirements before design
2. Get user approval before moving to next phase
3. Use parallel execution for faster iteration
4. Keep specs in `.claude/specs/` directory
5. Reference project's `CLAUDE.md` for coding standards
6. Mark tasks as complete in `tasks.md` as you implement them

## Integration

Works seamlessly with:
- Claude Code's TodoWrite tool for task tracking
- Project CLAUDE.md for coding standards
- Existing codebase exploration tools

---

This skill helps you build better software by ensuring features are thoroughly planned before implementation begins, reducing rework and improving team communication.

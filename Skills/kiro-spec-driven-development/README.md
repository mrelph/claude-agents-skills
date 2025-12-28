# Kiro Spec-Driven Development

A structured workflow for transforming vague feature ideas into well-defined, implementable specifications.

## Overview

Kiro Spec-Driven Development is a disciplined approach to software feature planning that separates planning from implementation. Instead of diving straight into code, this methodology guides you through three distinct phases:

1. **Requirements** - Define WHAT to build
2. **Design** - Plan HOW to build it
3. **Tasks** - Break down into actionable steps

This ensures features are thoroughly thought through before implementation begins, reducing rework and improving team alignment.

## Who Should Use This

- **Solo Developers** - Structure your feature planning process
- **Teams** - Align on requirements before coding
- **Product Managers** - Document features systematically
- **Anyone** planning non-trivial features that need careful thought

## Installation

```bash
cp -r Skills/kiro-spec-driven-development /path/to/your/project/.claude/skills/
```

Or install from the marketplace:
```bash
/plugin install claude-agents-skills-marketplace
```

## Quick Start

### 1. Invoke the Skill

In Claude Code, describe your feature idea:
```
"I want to add a notification system to my app"
```

The skill will automatically activate and guide you through the workflow.

### 2. Follow the Workflow

The skill will:
- Ask clarifying questions about your feature
- Create a requirements document for your review
- Wait for your approval before proceeding
- Create a design document based on approved requirements
- Wait for your approval again
- Create an actionable task breakdown
- Optionally help you implement the tasks

### 3. Review Output

All spec files are created in `.claude/specs/{feature-name}/`:
```
.claude/specs/notification-system/
├── requirements.md    # WHAT to build
├── design.md          # HOW to build it
└── tasks.md           # Implementation steps
```

## Features

### Three-Phase Workflow

**Phase 1: Requirements**
- Feature description and user stories
- Acceptance criteria (Given/When/Then format)
- Non-functional requirements

**Phase 2: Design**
- Architecture overview
- Data models and API contracts
- Component design
- Security and error handling

**Phase 3: Tasks**
- Granular task breakdown
- Clear dependencies
- Progress tracking with checkboxes

### Parallel Execution

Speed up iteration by running multiple versions simultaneously:
- Skill asks: "How many spec-requirements agents to use?"
- Multiple sub-agents generate different versions
- AI judge selects the best version
- Available for all three phases

### Sub-Agent System

The skill orchestrates specialized sub-agents:
- `spec-requirements` - Requirements creation/refinement
- `spec-design` - Design document creation/refinement
- `spec-tasks` - Task breakdown creation/refinement
- `spec-judge` - Version evaluation and selection
- `spec-impl` - Optional code implementation
- `spec-test` - Optional test creation

### Quality Assurance

Built-in quality criteria ensure:
- Requirements are testable and measurable
- Designs address all requirements
- Tasks are properly sized and ordered
- Consistency across all three documents

## Usage Examples

### Example 1: New Feature

```
User: "I want users to be able to export their data to CSV"

Skill:
1. Creates feature name: "data-export"
2. Drafts requirements with user stories and acceptance criteria
3. Shows requirements for review
4. After approval, creates design document
5. Shows design for review
6. After approval, creates task breakdown
7. Ready for implementation!
```

### Example 2: Update Existing Spec

```
User: "Update the notification design to use WebSockets instead of polling"

Skill:
1. Reads existing design.md
2. Calls spec-design sub-agent with update request
3. Shows updated design for review
```

### Example 3: Review Existing Specs

```
User: "What specs do I have and what's their status?"

Skill:
1. Scans .claude/specs/ directory
2. Lists all features
3. Shows completion status for each phase
4. Highlights any incomplete or inconsistent specs
```

## Advanced Features

### Automatic Task Execution

```
User: "Execute all tasks automatically"

Skill:
1. Analyzes task dependencies in tasks.md
2. Orchestrates parallel execution of independent tasks
3. Respects dependencies (task A before task B)
4. Updates tasks.md with progress
```

### Tree-Based Evaluation

When running 10+ parallel agents:
1. Round 1: Judges evaluate groups of 3-4 versions
2. Round 2: Final judge selects best from winners
3. Main thread renames final selection to standard name

## Best Practices

1. **Start Small** - Try the workflow with a small feature first
2. **Iterate** - Don't expect perfect specs on first draft
3. **Get Buy-In** - Review and approve each phase before proceeding
4. **Use Parallel Execution** - 3-5 agents is a good balance
5. **Reference CLAUDE.md** - Skill uses your project's coding standards
6. **Track Progress** - Check off tasks in tasks.md as you complete them

## File Structure

```
.claude/specs/
├── feature-one/
│   ├── requirements.md
│   ├── design.md
│   └── tasks.md
├── feature-two/
│   ├── requirements.md
│   ├── design.md
│   └── tasks.md
└── ...
```

## Integration

Works seamlessly with:
- **TodoWrite** - Task tracking in Claude Code
- **CLAUDE.md** - Project coding standards
- **Existing codebase** - Code exploration for design decisions

## Quality Criteria

### Good Requirements
✅ Testable and measurable
✅ User-focused, not implementation-focused
✅ Complete coverage of feature scope
✅ Clear acceptance criteria

### Good Design
✅ Addresses all requirements
✅ Considers edge cases and error states
✅ Follows project conventions
✅ Includes security and performance

### Good Tasks
✅ Small enough to complete in one session
✅ Clear definition of done
✅ Properly ordered by dependencies
✅ Include verification steps

## Troubleshooting

**Requirements taking too long?**
- Suggest moving to a different aspect
- Provide examples to help decisions
- Summarize what's established and identify gaps

**Design getting too complex?**
- Break into smaller, manageable components
- Focus on core functionality first
- Consider phased implementation

**Tasks unclear?**
- Review design for missing details
- Break large tasks into smaller subtasks
- Add acceptance criteria references

## Version History

- **v1.0.0** (2025-12-28) - Initial release
  - Three-phase workflow (requirements, design, tasks)
  - Parallel execution support
  - Sub-agent orchestration
  - Quality criteria enforcement

## Credits

Based on Kiro's spec-driven development methodology.

## License

MIT License - Use and adapt for your projects.

## Support

For issues or questions:
- Review `references/workflow-definition.md` for detailed workflow
- Check sub-agent definitions in `references/`
- Open an issue in the marketplace repository

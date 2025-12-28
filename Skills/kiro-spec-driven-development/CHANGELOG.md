# Changelog - Kiro Spec-Driven Development Skill

All notable changes to the kiro-spec-driven-development skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.0] - 2025-12-28

### Added

- Initial release of kiro-spec-driven-development skill
- Structured three-phase spec-driven development workflow
  - Phase 1: Requirements Gathering (WHAT to build)
  - Phase 2: Design Documentation (HOW to build)
  - Phase 3: Task Planning (implementation breakdown)
- Specialized sub-agents for each workflow phase
  - spec-requirements: Creates/refines requirements documents
  - spec-design: Creates/refines design documents
  - spec-tasks: Creates/refines task breakdowns
  - spec-judge: Evaluates and selects best versions from parallel executions
  - spec-impl: Implements code from task list (optional)
  - spec-test: Creates test documentation and code (optional)
  - spec-system-prompt-loader: Loads workflow system prompts
- Parallel execution capability
  - Run 1-128 agents in parallel for faster iteration
  - Tree-based evaluation to select best version
  - Supports requirements, design, and tasks phases
- Iterative workflow with user approval gates
  - User review and approval required at each phase
  - Iterate until approval before proceeding
  - Clear phase transition points
- Feature directory structure
  - Creates .claude/specs/{feature-name}/ directory
  - Organized requirements.md, design.md, tasks.md files
  - Persistent spec storage for team collaboration
- Quality criteria framework
  - Testable and measurable requirements
  - User-focused (not implementation-focused)
  - Complete feature scope coverage
  - Addresses all requirements in design
  - Edge cases and error state handling
  - Small, independently completable tasks
- Integration capabilities
  - Works with Claude Code's TodoWrite tool
  - References project CLAUDE.md for coding standards
  - Integrates with existing codebase exploration tools
- Comprehensive reference documentation
  - workflow-definition.md: Complete workflow with Mermaid diagrams
  - All sub-agent definitions with detailed instructions
- Usage examples and best practices
  - Starting new features
  - Reviewing existing specs
  - Updating specifications
  - Managing spec lifecycle

### Features

- **Three-Phase Structure**: Requirements → Design → Tasks workflow
- **Parallel Processing**: 1-128 concurrent agents for speed
- **User Approval Gates**: Quality control at each phase transition
- **Specialized Sub-Agents**: Domain-focused agents for each workflow stage
- **Persistent Specs**: Organized directory structure for team collaboration
- **Quality Framework**: Clear criteria for good requirements, design, and tasks
- **Flexible Implementation**: Optional spec-impl and spec-test agents

### Workflows

1. **New Feature Initialization**: Create feature directory and requirements draft
2. **Requirements Iteration**: Refine requirements until user approval
3. **Design Creation**: Build design based on approved requirements
4. **Design Iteration**: Refine design until user approval
5. **Task Breakdown**: Create actionable implementation tasks
6. **Task Iteration**: Refine tasks until user approval
7. **Optional Implementation**: Execute tasks using spec-impl sub-agent

### Tool Access

- Read: Loading existing specs and project files
- Write: Creating and updating spec documents
- Bash: Running sub-agents and validation scripts
- Grep: Searching codebase for context
- Glob: Finding related files
- Task: Orchestrating sub-agent execution
- AskUserQuestion: Getting user approval and clarification
- TodoWrite: Tracking implementation progress

### Target Users

- Development teams using spec-driven methodology
- Product managers creating feature specifications
- Developers planning complex features
- Teams requiring structured documentation
- Projects using Kiro methodology

### Sub-Agent Architecture

All sub-agents located in references/ directory:
- Modular, specialized agents for each workflow phase
- Consistent interface for orchestration
- Parallel execution support where applicable
- Quality-focused evaluation criteria

---

## Version Notes

This skill follows semantic versioning:
- MAJOR version for workflow methodology changes
- MINOR version for new sub-agents or workflow phases
- PATCH version for documentation improvements or minor enhancements

See also: SKILL.md for detailed workflow and usage instructions

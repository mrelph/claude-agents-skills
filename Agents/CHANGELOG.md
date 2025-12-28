# Changelog - Agents

All notable changes to the agents collection will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.0] - 2025-12-09

### Added

All agents released at version 1.0.0 with the marketplace launch.

#### marketplace-manager

- Automates adding new agents and skills to the Claude Code marketplace from staging directory
- Interactive workflow for metadata collection
- Validation and marketplace.json updates
- Supports both agents and skills
- Alternative to manual add-to-marketplace.py script
- **Category**: development
- **Tools**: Read, Write, Bash, Grep, Glob

#### bug-tracker-resolver

- Manages bugs in Bugs.md file
- Root cause analysis workflow
- Resolution plan creation
- Fix implementation and testing
- **Category**: development
- **Tools**: Read, Write, Bash, Grep, Glob

#### database-architect

- PostgreSQL and Supabase expertise
- Schema design and optimization
- Query optimization and indexing strategies
- Row-Level Security (RLS) policy design
- Database performance tuning
- **Category**: development
- **Tools**: Read, Write, Bash, Grep, Glob, Task, WebSearch, WebFetch

#### documentation-maintainer

- Creates and updates project documentation
- README.md generation and maintenance
- API documentation
- User guides and tutorials
- Ensures documentation consistency across projects
- **Category**: development
- **Tools**: Read, Write, Glob, Grep

#### performance-optimizer

- Core Web Vitals optimization
- Bundle size reduction strategies
- Runtime efficiency improvements
- Next.js-specific optimizations
- Performance monitoring and analysis
- **Category**: development
- **Tools**: Read, Write, Bash, Grep, Glob, Task, WebSearch

#### roadmap-feature-planner

- Strategic feature planning and prioritization
- Implementation coordination
- Roadmap tracking and management
- Cross-functional planning support
- **Category**: planning
- **Tools**: Read, Write, Glob, Grep, Task

#### security-code-scanner

- Vulnerability identification and analysis
- OWASP Top 10 compliance checking
- Risk assessment and scoring
- Secure code recommendations
- Security audit reporting
- **Category**: development
- **Tools**: Read, Bash, Grep, Glob, Task

#### ux-ui-design-expert

- UX/UI design guidance and best practices
- Information architecture planning
- Accessibility compliance (WCAG)
- Responsive design strategies
- User experience optimization
- **Category**: design
- **Tools**: Read, WebSearch, WebFetch, Task

#### video-integration-specialist

- YouTube and Vimeo integration
- Video player implementation
- Streaming optimization
- Media delivery strategies
- Video platform API integration
- **Category**: media
- **Tools**: Read, Write, Bash, WebSearch, WebFetch, Task

### Infrastructure

- Agent directory restructure: Each agent in individual directory for plugin compatibility
- Consistent YAML frontmatter format across all agents
- Standardized tool access definitions
- Color coding for UI identification
- Model selection (sonnet, opus, haiku) per agent

---

## Version Notes

All agents are currently at version 1.0.0, representing their initial stable release as part of the marketplace.

Individual agent CHANGELOGs will be created in their respective directories as updates occur.

Agent versioning follows semantic versioning:
- MAJOR version for breaking changes to agent behavior or interface
- MINOR version for backwards-compatible functionality additions
- PATCH version for backwards-compatible bug fixes or documentation improvements

See also: Individual agent markdown files for detailed capabilities and workflows

# Forge Element Catalog

This catalog describes all available elements in Forge, organized by type.

## Principles (6)

### ruthless-minimalism
**Ship the simplest thing that could possibly work, then adapt based on real needs**

- KISS principle taken to heart
- Minimize abstractions
- Start minimal, grow as needed
- Question everything

**Dependencies**: None
**Source**: Core Forge philosophy

### coevolution
**Specifications and code are conversation partners that inform each other**

- Specs evolve as code reveals insights
- Code shapes specs as reality emerges
- Dialogue between design and implementation
- Continuous refinement

**Dependencies**: None
**Source**: Core Forge philosophy

### respect-user-time
**Never present work as ready without thorough self-testing and validation**

- Test yourself before engaging user
- Fix obvious issues first
- Verify it actually works
- User's role: strategic decisions; Your role: implementation + testing

**Dependencies**: None
**Source**: amplifier IMPLEMENTATION_PHILOSOPHY.md

### zero-bs-principle
**No stubs, placeholders, or unimplemented code - build working functionality only**

- Avoid NotImplementedError and TODO comments
- No mock implementations or "coming soon" features
- Every function must work or not exist
- YAGNI enforced

**Dependencies**: ruthless-minimalism
**Source**: amplifier IMPLEMENTATION_PHILOSOPHY.md

### analysis-first
**For complex problems, always analyze before implementing**

- Decompose problem
- Consider 2-3 options with trade-offs
- Make informed recommendation
- Prevents premature implementation

**Dependencies**: ruthless-minimalism
**Suggests**: zen-architect
**Source**: amplifier IMPLEMENTATION_PHILOSOPHY.md

### spec-driven
**Specifications as the source of truth - code serves specs, not the other way around**

- Specifications don't serve code—code serves specifications
- PRDs generate implementation, not just guide it
- Eliminates gap between intent and implementation
- Natural language as the lingua franca of development

**Dependencies**: None
**Suggests**: spec-template, plan-template, tasks-template
**Source**: spec-kit SDD philosophy

## Agents (7)

### zen-architect
**Master designer for code planning, architecture design, and quality review**

Operates in three modes:
- **ANALYZE**: Problem decomposition, solution options, recommendations
- **ARCHITECT**: System design, module specifications, boundaries
- **REVIEW**: Code quality assessment without implementing changes

Creates specifications that guide implementation. Embodies ruthless simplicity and Wabi-sabi philosophy.

**Dependencies**: ruthless-minimalism, analysis-first
**Role**: Architecture and design
**Source**: amplifier agents

### modular-builder
**Primary implementation agent that builds self-contained modules from specifications**

- Follows "bricks and studs" philosophy
- Builds modules from zen-architect specs
- Clear contracts with comprehensive documentation
- Regeneratable over patchable design

**Dependencies**: ruthless-minimalism, analysis-first
**Role**: Implementation
**Source**: amplifier agents

### bug-hunter
**Systematic debugging expert using hypothesis-driven approach**

Process:
1. **Evidence Gathering**: Error messages, stack traces, conditions
2. **Hypothesis Testing**: Test each hypothesis systematically
3. **Root Cause Analysis**: Identify actual problem vs symptoms
4. **Minimal Fix**: Fix only root cause, add regression test

**Dependencies**: ruthless-minimalism, analysis-first
**Role**: Debugging
**Source**: amplifier agents

### test-coverage
**Expert at analyzing test gaps and suggesting strategic test cases**

- Follows 60-30-10 testing pyramid (60% unit, 30% integration, 10% e2e)
- Identifies critical test gaps
- Focuses on boundaries, errors, integration points
- Strategic test suggestions, not exhaustive coverage

**Dependencies**: ruthless-minimalism, analysis-first
**Role**: Testing
**Source**: amplifier agents

### security-guardian
**Defensive security specialist focused on vulnerability assessment**

Reviews:
- OWASP Top 10 vulnerabilities
- Hardcoded secrets and credentials
- Input/output security
- Authentication and authorization
- Data protection measures

Practical security without security theater.

**Dependencies**: ruthless-minimalism, analysis-first
**Role**: Security
**Source**: amplifier agents

### post-task-cleanup
**Guardian of codebase hygiene that removes temporary artifacts**

After task completion:
- Reviews git status for cruft
- Eliminates temporary files
- Validates philosophy compliance
- Ensures ruthless simplicity maintained

**Dependencies**: ruthless-minimalism, analysis-first
**Role**: Cleanup
**Source**: amplifier agents

### code-reviewer (existing)
**Reviews code for quality, security, and best practices**

General-purpose code review agent with focus on:
- Security vulnerabilities
- Code quality and readability
- Potential bugs and edge cases
- Maintainability improvements

**Dependencies**: ruthless-minimalism
**Role**: Code review
**Source**: Original Forge example

## Templates (4)

### spec-template
**Feature specification template with user stories and acceptance criteria**

Structured template for creating complete feature specifications:
- User scenarios and testing with prioritized stories
- Functional requirements with testability
- Measurable success criteria
- Key entities and edge cases

**Dependencies**: None
**Suggests**: specify
**Source**: spec-kit templates

### plan-template
**Implementation plan template for technical architecture and design**

Template for converting specifications into technical plans:
- Technical context and architecture
- Constitution compliance checking
- Research phase for unknowns
- Design artifacts (data models, contracts, quickstart)

**Dependencies**: None
**Suggests**: plan
**Source**: spec-kit templates

### tasks-template
**Task breakdown template organized by user stories and phases**

Template for generating executable task lists:
- Organized by user story for independent implementation
- Strict checklist format with IDs and file paths
- Parallel execution opportunities
- MVP-first implementation strategy

**Dependencies**: None
**Suggests**: tasks
**Source**: spec-kit templates

### checklist-template
**Requirements quality checklist template for validating specifications**

Template for "unit tests for requirements":
- Content quality validation
- Requirement completeness checks
- Feature readiness criteria
- Pre-planning validation gates

**Dependencies**: None
**Suggests**: specify
**Source**: spec-kit templates

## Tools (8)

### commit
**Create well-formatted git commits with conventional commit messages**

Features:
- Auto-runs pre-commit checks (lint, build, docs)
- Detects package manager and runs appropriate commands
- Analyzes diff to detect multiple logical changes
- Suggests splitting commits when appropriate
- Detects sensitive data before committing
- Conventional commit format enforcement

**Dependencies**: respect-user-time
**Category**: version-control-git
**Source**: amplifier commands

### review-changes
**Comprehensive review workflow that runs tests and checks philosophy alignment**

Process:
1. Run `make install && source .venv/bin/activate`
2. Execute `make check && make test`
3. Review implementation philosophy documents
4. Analyze changed files against philosophy
5. Follow dependency breadcrumbs
6. Generate comprehensive alignment report

**Dependencies**: respect-user-time
**Category**: workflow
**Source**: amplifier commands

### modular-build
**End-to-end module creation from natural language through to implementation**

Phases:
1. **Contract**: Define inputs, outputs, side effects
2. **Spec**: Create detailed module specification
3. **Plan**: Break into implementation steps
4. **Generate**: Build the module
5. **Review**: Validate against contract and philosophy

Strict validation gates and SSOT enforcement.

**Dependencies**: respect-user-time
**Suggests**: zen-architect, modular-builder
**Category**: workflow
**Source**: amplifier commands

### create-plan
**Creates self-contained implementation plans for junior developers**

Plans include:
- Complete context and background
- All prerequisites and dependencies
- Step-by-step instructions
- Validation criteria
- Philosophy alignment notes

Context-independent and junior developer friendly.

**Dependencies**: respect-user-time
**Suggests**: zen-architect
**Category**: workflow
**Source**: amplifier commands

### specify
**Create or update feature specification from natural language description**

Specification-Driven Development workflow starter:
- Generates feature branch with automatic numbering
- Creates complete specification from description
- Validates specification quality with checklist
- Limits clarifications to max 3 critical questions
- Supports iterative refinement

**Dependencies**: spec-driven
**Suggests**: spec-template, plan, tasks
**Category**: specification
**Source**: spec-kit commands

### plan
**Execute implementation planning workflow to generate technical design artifacts**

Converts specifications into technical implementation plans:
- Constitution compliance validation
- Research phase for unknowns and decisions
- Data model and API contract generation
- Quickstart guide creation
- Multi-agent context synchronization

**Dependencies**: spec-driven
**Suggests**: plan-template, specify, tasks
**Category**: planning
**Source**: spec-kit commands

### tasks
**Generate actionable, dependency-ordered task list from design artifacts**

Breaks implementation plans into executable tasks:
- Organized by user story for independent delivery
- Strict checklist format with IDs and paths
- Parallel execution opportunities identified
- MVP-first implementation strategy
- Tests optional unless explicitly requested

**Dependencies**: spec-driven
**Suggests**: tasks-template, plan, specify
**Category**: planning
**Source**: spec-kit commands

### scaffold (existing)
**Scaffolds new project structures and boilerplate code**

Supports multiple project types:
- Python projects with standard structure
- TypeScript with tsconfig
- React applications
- REST APIs with OpenAPI

**Dependencies**: None
**Category**: scaffolding
**Source**: Original Forge example

## Hooks (1)

### session-logger (existing)
**Logs session start/stop events for tracking**

- Logs to `.forge/logs/sessions.jsonl`
- Captures event type and metadata
- Timestamps all entries
- Enables session tracking and analysis

**Dependencies**: None
**Source**: Original Forge example

## Composition Examples

### example-workflow (original)
Basic Forge example composition with minimal elements.

**Elements**: 2 principles, 1 agent, 1 tool, 2 hooks
**Use Case**: Learning Forge basics

### amplifier-workflow
**Complete development workflow from amplifier**

Comprehensive workflow covering:
- Analysis and planning (zen-architect, create-plan)
- Implementation (modular-builder, modular-build)
- Testing (test-coverage)
- Security review (security-guardian)
- Quality control (review-changes, commit)
- Cleanup (post-task-cleanup)

**Elements**: 5 principles, 7 agents, 5 tools, 1 hook
**Use Case**: Production development with quality gates

### spec-kit-workflow
**Specification-Driven Development workflow from spec-kit**

SDD workflow for specification-first development:
- Natural language to specification (specify)
- Specification to implementation plan (plan)
- Plan to executable tasks (tasks)
- Continuous refinement and validation
- Template-driven consistency

**Elements**: 2 principles, 4 templates, 3 tools
**Use Case**: Specification-first development, requirements clarity, team collaboration

## Usage Patterns

### Pattern 1: Simple Development

```yaml
composition:
  name: simple-dev
elements:
  principles: [ruthless-minimalism]
  agents: [code-reviewer]
  tools: [scaffold]
```

**Use for**: Quick prototypes, simple scripts

### Pattern 2: Quality-Focused Development

```yaml
composition:
  name: quality-dev
elements:
  principles: [ruthless-minimalism, respect-user-time, zero-bs-principle]
  agents: [zen-architect, modular-builder, test-coverage, bug-hunter]
  tools: [commit, review-changes]
```

**Use for**: Production code, team projects

### Pattern 3: Security-Critical Development

```yaml
composition:
  name: secure-dev
elements:
  principles: [ruthless-minimalism, respect-user-time, analysis-first]
  agents: [zen-architect, security-guardian, test-coverage]
  tools: [commit, review-changes]
```

**Use for**: Financial systems, user data handling, API services

### Pattern 4: Complete Workflow

```yaml
composition:
  name: complete-workflow
elements:
  principles: [ruthless-minimalism, coevolution, respect-user-time, zero-bs-principle, analysis-first]
  agents: [zen-architect, modular-builder, bug-hunter, test-coverage, security-guardian, post-task-cleanup]
  tools: [commit, review-changes, modular-build, create-plan]
```

**Use for**: Complex projects, team collaboration, production systems

## Agent Orchestration

Configure agent roles for coordinated workflows:

```yaml
settings:
  agent_orchestration:
    mode: sequential
    max_parallel: 3
    agent_roles:
      planning: zen-architect
      implementation: modular-builder
      testing: test-coverage
      debugging: bug-hunter
      security: security-guardian
      cleanup: post-task-cleanup
```

## Element Statistics

- **Total Elements**: 26
  - Principles: 6
  - Agents: 7
  - Templates: 4
  - Tools: 8
  - Hooks: 1

- **Source Distribution**:
  - amplifier: 13 elements (6 agents, 4 tools, 3 principles)
  - spec-kit: 8 elements (4 templates, 3 tools, 1 principle)
  - Original Forge: 5 elements (1 agent, 1 tool, 2 principles, 1 hook)

- **Coverage**:
  - Core Development: zen-architect, modular-builder, code-reviewer
  - Quality Assurance: test-coverage, security-guardian, bug-hunter
  - Workflow Management: commit, review-changes, modular-build, create-plan, specify, plan, tasks
  - Templates & Structure: spec-template, plan-template, tasks-template, checklist-template
  - Project Setup: scaffold, session-logger
  - Philosophy: ruthless-minimalism, coevolution, respect-user-time, zero-bs-principle, analysis-first, spec-driven

## Next Steps

1. **Explore Elements**: Browse `forge/elements/` to see full specifications
2. **Try Examples**:
   - Implementation-first: `forge/examples/amplifier-workflow.yaml`
   - Specification-first: `forge/examples/spec-kit-workflow.yaml`
3. **Create Compositions**: Mix and match elements for your workflow
4. **Generate Integrations**: Use `forge generate claude-code` to create `.claude/` structure
5. **Extend Library**: Add your own elements following the established patterns

For more information:
- [Provider Documentation](docs/providers/claude-code.md)
- [Usage Demo](USAGE_DEMO.md)
- [Testing Guide](TESTING.md)

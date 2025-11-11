# Spec-Kit: Complete Project Breakdown

## Executive Summary

**Spec-Kit** is a production-ready toolkit that implements **Specification-Driven Development (SDD)**—a methodology that fundamentally inverts the traditional relationship between code and specifications. It makes specifications executable, positioning them as the source of truth with code as continuously regenerated output.

**Core Innovation**: "The Power Inversion"—specifications drive implementation, not the reverse. Change the spec, change the software.

---

## 1. Vision and Purpose

### The Power Inversion

**Traditional Approach**:
- Code is king
- Specs serve code
- Specifications are disposable scaffolding
- Code becomes the source of truth

**SDD Approach**:
- Specifications are executable
- Code serves specifications
- Specifications are the source of truth
- Code is continuously regenerated output

### Key Insight
Make specifications the primary artifact. Everything else—code, tests, documentation—flows from the specification.

### Goals

1. **Enable 0-to-1 Development**
   - Generate production-ready applications from specifications
   - Natural language to working software
   - Complete automation of implementation

2. **Support Creative Exploration**
   - Allow parallel implementations from same spec
   - Experiment with different tech stacks
   - Compare approaches objectively

3. **Technology Independence**
   - Work across diverse tech stacks
   - Support any programming language
   - Framework-agnostic methodology

4. **Enterprise Readiness**
   - Handle compliance requirements
   - Support design systems
   - Respect tech stack constraints
   - Enforce quality gates

5. **Iterative Enhancement**
   - Support brownfield modernization
   - Add features to existing systems
   - Incremental improvement

### Philosophy

**Intent-Driven Development**:
- Express WHAT and WHY in natural language
- Let AI determine HOW
- Specifications as lingua franca

**Multi-Step Refinement**:
- Structured process, not one-shot generation
- Quality gates at each step
- Iterative clarification

**AI-Amplified**:
- Heavy reliance on AI for interpretation
- AI implements, humans provide intent
- Multiple AI agents supported

---

## 2. Architecture

### The 5-Step Workflow

```
┌──────────────────────────────────────────────┐
│ Step 1: CONSTITUTION                         │
│ /speckit.constitution                        │
│ → memory/constitution.md                     │
│ Define immutable project principles          │
├──────────────────────────────────────────────┤
│ Step 2: SPECIFICATION                        │
│ /speckit.specify                             │
│ → specs/###-feature/spec.md                  │
│ Define WHAT (technology-agnostic)            │
├──────────────────────────────────────────────┤
│ Step 3: PLANNING                             │
│ /speckit.plan                                │
│ → plan.md, research.md, data-model.md        │
│ Define HOW (technology-specific)             │
├──────────────────────────────────────────────┤
│ Step 4: TASK GENERATION                      │
│ /speckit.tasks                               │
│ → tasks.md                                   │
│ Break down into executable work items        │
├──────────────────────────────────────────────┤
│ Step 5: IMPLEMENTATION                       │
│ /speckit.implement                           │
│ → Working code                               │
│ Execute tasks systematically                 │
└──────────────────────────────────────────────┘
```

### Enhancement Commands (Optional Quality Gates)

**Quality Assurance Commands**:
- `/speckit.clarify` - Structured questioning to reduce ambiguity
- `/speckit.analyze` - Cross-artifact consistency analysis
- `/speckit.checklist` - Generate quality validation checklists

### Template Architecture

Three core templates drive the entire process:

#### **spec-template.md** - WHAT to Build
**Purpose**: Technology-agnostic feature specification

**Sections**:
- **Overview** - Feature description and purpose
- **User Stories** - Prioritized (P1, P2, P3)
- **Acceptance Scenarios** - Given/When/Then format
- **Functional Requirements** - Numbered (FR-001, FR-002...)
- **Success Criteria** - Measurable, technology-agnostic
- **Clarifications** - `[NEEDS CLARIFICATION]` markers (max 3)

**Key Constraint**: Explicitly forbids tech stack details. Focus on business value.

#### **plan-template.md** - HOW to Build
**Purpose**: Technology-specific implementation plan

**Sections**:
- **Technical Context** - Language, frameworks, dependencies
- **Constitution Gates** - Phase -1: Pre-implementation validation
- **Project Structure** - Single/web/mobile patterns
- **Complexity Tracking** - Justify violations
- **Research Artifacts** - Phase 0: Resolve unknowns
- **Design Artifacts** - Phase 1: Data models, contracts, quickstart

**Key Innovation**: Constitutional gates prevent over-engineering before coding starts.

#### **tasks-template.md** - EXECUTION Plan
**Purpose**: Ordered, executable task breakdown

**Format**:
```
- [ ] [TaskID] [P?] [Story?] Description
```

**Organization**:
- **Phase 1**: Setup (environment, tooling)
- **Phase 2**: Foundational (blocks all stories)
- **Phase 3+**: User Stories (one phase per story)
- **Final**: Polish & cross-cutting concerns

**Features**:
- Dependency graphs
- Parallel execution markers `[P]`
- Independent test criteria per story
- MVP strategy (typically US1 only)

---

## 3. Constitutional Governance

### The Constitution System

**Purpose**: Immutable architectural principles that govern all development

**Key Concept**: Define quality gates and constraints BEFORE implementation begins

### Example Constitution (9 Articles)

**Article I: Library-First**
- Every feature starts as standalone library
- Ensures modularity and testability

**Article II: CLI Interface**
- All functionality exposed via CLI
- Text in, text out
- Enables automation and debugging

**Article III: Test-First (NON-NEGOTIABLE)**
- TDD mandatory
- Tests → approval → fail → implement
- Red-Green-Refactor

**Article IV: Integration Testing**
- Focus on real environments
- Minimize mocks
- Test against actual services

**Article V: Observability**
- Text I/O ensures debuggability
- Comprehensive logging
- Traceable execution

**Article VI: Versioning**
- MAJOR.MINOR.BUILD format
- Semantic versioning principles

**Article VII: Simplicity**
- YAGNI principles
- Max 3 projects initially
- Justify additional complexity

**Article VIII: Anti-Abstraction**
- Use frameworks directly
- No unnecessary wrappers
- Minimize indirection

**Article IX: Integration-First Testing**
- Real databases
- Actual services
- Production-like environments

### Constitutional Gates (Phase -1)

**Pre-Implementation Validation**:
- Check compliance with constitutional principles
- Identify potential violations early
- Require justification for exceptions
- Prevent over-engineering

**Example Gates**:
- ✓ All features exposed via CLI
- ✓ Tests written before implementation
- ✓ No unnecessary abstractions
- ! Complexity violation requires justification

---

## 4. Multi-Agent Support

### Supported AI Agents (13+)

| Agent | Type | Config Folder | Format |
|-------|------|---------------|--------|
| **Claude Code** | CLI | `.claude/` | Markdown |
| **GitHub Copilot** | IDE | `.github/prompts/` | Markdown |
| **Gemini CLI** | CLI | `.gemini/` | TOML |
| **Cursor** | IDE | `.cursor/` | Markdown |
| **Windsurf** | IDE | `.windsurf/` | Markdown |
| **Qwen Code** | CLI | `.qwen/` | TOML |
| **opencode** | CLI | `.opencode/` | Markdown |
| **Codex** | CLI | `.codex/` | Markdown |
| **Amazon Q** | CLI | `.amazonq/` | Markdown |
| **Amp** | CLI | `.agents/` | Markdown |
| **Replit AI** | IDE | `.replit/` | TOML |
| **Cody** | IDE | `.cody/` | JSON |
| **Tabnine** | IDE | `.tabnine/` | YAML |

### Agent Configuration Structure

**Common Pattern**:
```yaml
AGENT_CONFIG:
  folder: ".agent-name"
  file_type: "md" or "toml"
  category: "cli" or "ide"
  commands_file: "commands.md" or "config.toml"
  format: "markdown" or "toml"
```

### Universal Methodology

**Key Benefit**: Same workflow across all agents
- Agent-agnostic specifications
- Portable workflows
- Consistent methodology
- Technology diversity supported

---

## 5. The Specification Lifecycle

### Phase 0: Establish Principles

**Command**: `/speckit.constitution`

**Process**:
1. Define project governance
2. Set quality standards
3. Establish architectural constraints
4. Create constitutional articles

**Output**: `memory/constitution.md`

**Purpose**: Immutable foundation for all development

### Phase 1: Define WHAT (Technology-Agnostic)

**Command**: `/speckit.specify`

**Process**:
1. AI analyzes natural language description
2. Determines next feature number (001, 002, 003...)
3. Creates Git branch (e.g., `003-chat-system`)
4. Generates structured spec from template:
   - User stories (prioritized P1, P2, P3)
   - Acceptance scenarios (Given/When/Then)
   - Functional requirements (FR-001, FR-002...)
   - Success criteria (measurable outcomes)
5. Creates quality checklist
6. Validates completeness
7. Asks clarifying questions (max 3 with recommendations)

**Output**: `specs/###-feature/spec.md`, `checklists/requirements.md`

**Key Constraint**: NO implementation details. Focus on business value.

### Phase 2: Clarify Ambiguities (Optional but Recommended)

**Command**: `/speckit.clarify`

**Taxonomy-Based Analysis**:
1. **Functional Scope & Behavior** - What it does
2. **Domain & Data Model** - What it knows
3. **Interaction & UX Flow** - How users interact
4. **Non-Functional Quality Attributes** - Performance, security, etc.
5. **Integration & Dependencies** - External systems
6. **Edge Cases & Failure Handling** - Error scenarios
7. **Constraints & Tradeoffs** - Limitations and choices

**Process**:
- Sequential questioning (max 5 questions)
- Each answer immediately integrated into spec
- Incremental file updates
- Recommendations provided

**Output**: Updated `spec.md` with Clarifications section

**Purpose**: Reduce ambiguity before technical decisions

### Phase 3: Plan HOW (Technology-Specific)

**Command**: `/speckit.plan`

**Process**:

**Sub-Phase 0: Research**
1. Load spec and constitution
2. Identify all `[NEEDS CLARIFICATION]` items
3. Launch parallel research agents
4. Consolidate findings
5. Document decisions and rationale

**Sub-Phase 1: Design**
1. Fill technical context (language, frameworks, storage)
2. Evaluate constitution gates (Phase -1)
3. Generate `data-model.md`:
   - Entities and relationships
   - Validation rules
   - Constraints
4. Create `contracts/` directory:
   - API specifications (OpenAPI, GraphQL)
   - Interface contracts
5. Produce `quickstart.md`:
   - Key validation scenarios
   - Manual testing guide
6. Update agent context files
7. Re-evaluate gates post-design
8. Track complexity violations

**Output**: `plan.md`, `research.md`, `data-model.md`, `contracts/`, `quickstart.md`

**Purpose**: Technical blueprint with constitutional compliance

### Phase 4: Break Down Work

**Command**: `/speckit.tasks`

**Process**:
1. Analyze plan, spec, data-model, contracts
2. Organize tasks by user story
3. Create phases:
   - **Phase 1**: Setup (environment, dependencies)
   - **Phase 2**: Foundational (blocks all stories)
   - **Phase 3**: User Story 1
   - **Phase 4**: User Story 2
   - **Phase N**: User Story N-2
   - **Final**: Polish & cross-cutting
4. Generate dependency graph
5. Mark parallel tasks `[P]`
6. Include independent test criteria per story
7. Create MVP strategy (typically US1 only)

**Output**: `tasks.md`

**Format**:
```markdown
## Phase 3: User Story 1 - Basic Authentication

### Dependencies
- Phase 2: Database setup, API framework

### Tasks
- [ ] [US1.1] [P1] [US1] Create User model with validation
- [ ] [US1.2] [P1] [US1] Implement password hashing utility
- [ ] [US1.3] [P1] [US1] Build registration endpoint
- [P] [ ] [US1.4] [P1] [US1] Build login endpoint
- [P] [ ] [US1.5] [P1] [US1] Build logout endpoint

### Test Criteria
- User can register with valid credentials
- User cannot register with duplicate email
- User can log in with correct password
- User cannot log in with incorrect password
```

### Phase 5: Execute

**Command**: `/speckit.implement`

**Process**:
1. Validate prerequisites:
   - Constitution exists
   - Spec exists
   - Plan exists
   - Tasks exist
2. Check quality checklists (if exist)
3. Load all context documents
4. Verify/create ignore files (git, docker, eslint, etc.)
5. Execute tasks phase-by-phase:
   - **Respect dependencies** - Don't start Phase 3 until Phase 2 complete
   - **Run parallel tasks together** - Tasks marked `[P]`
   - **Follow TDD approach** - Tests first, always
   - **Validate checkpoints** - Ensure story independence
6. Mark completed tasks in `tasks.md`
7. Report progress and errors
8. Handle failures gracefully

**Output**: Working code, passing tests

**Key Principles**:
- Test-first, always
- Each story independently testable
- No breaking previous stories
- Constitutional compliance throughout

---

## 6. Template-Driven Quality

### How Templates Constrain AI Behavior

**Key Innovation**: Templates act as sophisticated prompts that prevent common LLM mistakes

**Quality Mechanisms**:

1. **Prevent Premature Implementation**
   - Spec template explicitly forbids tech stack details
   - Forces separation of WHAT from HOW
   - Ensures technology-agnostic thinking

2. **Force Explicit Uncertainty**
   - Mandate `[NEEDS CLARIFICATION]` markers
   - Max 3 clarifications (forces prioritization)
   - Recommended answers guide thinking

3. **Structured Thinking**
   - Comprehensive checklists act as "unit tests for English"
   - Required sections ensure completeness
   - Format constraints enforce clarity

4. **Constitutional Compliance**
   - Phase gates prevent over-engineering
   - Automatic validation at each step
   - Justified exceptions only

5. **Hierarchical Detail**
   - Keep high-level readable
   - Extract complexity to separate files
   - `data-model.md`, `contracts/`, `research.md`

6. **Test-First Thinking**
   - Enforce contract → test → implementation order
   - Acceptance scenarios before code
   - Independent test criteria per story

7. **Prevent Speculation**
   - No "might need" features
   - Concrete user stories only
   - Measurable success criteria

### Template Benefits

**Consistency**:
- Every spec has same structure
- Predictable format
- Easy to review

**Completeness**:
- Required sections ensure nothing missed
- Checklists validate coverage
- Gap detection automatic

**Quality**:
- AI behavior constrained
- Common mistakes prevented
- Best practices encoded

---

## 7. Development Patterns

### MVP-First Strategy

**Pattern**:
1. Complete **Phase 1**: Setup
2. Complete **Phase 2**: Foundational
3. Implement **Phase 3**: User Story 1 (P1 only)
4. Validate independently
5. Deploy/demo

**Benefits**:
- Fastest path to value
- Early validation
- Risk reduction
- Incremental funding

### Incremental Delivery

**Pattern**:
1. Add one user story at a time
2. Each story independently testable
3. Each story adds value
4. No breaking previous stories

**Benefits**:
- Continuous delivery
- Frequent releases
- Reduced integration risk
- Faster feedback

### Parallel Team Strategy

**Pattern**:
1. Team completes foundation together
2. Split by user story
3. Stories complete independently
4. Integrate without conflicts

**Benefits**:
- Team scalability
- Parallel development
- Reduced bottlenecks
- Clear ownership

### Technology Exploration

**Pattern**:
1. Write spec once (technology-agnostic)
2. Generate plans for different tech stacks:
   - Plan A: Node.js + PostgreSQL
   - Plan B: Python + MongoDB
   - Plan C: Go + SQLite
3. Implement in parallel
4. Compare objectively

**Benefits**:
- Risk mitigation
- Objective comparison
- Learn multiple approaches
- Best tool for the job

---

## 8. Tools and Infrastructure

### CLI Tool: `specify`

**Installation**:
```bash
pip install specify-cli
```

**Commands**:

**`specify init <project>`**
- Bootstraps projects from GitHub releases
- Interactive agent selection (13+ agents)
- Template download and setup
- Git initialization
- Script type selection (bash/powershell)
- Beautiful terminal UI with progress tracking

**`specify check`**
- Verifies tool installation
- Validates environment
- Checks prerequisites

**Features**:
- Cross-platform (Linux/macOS/Windows)
- Arrow-key navigation
- Rich terminal output
- Progress tracking
- Error handling

### Script Infrastructure

**Dual-Platform Automation**:
- `/scripts/bash/` - POSIX shell scripts
- `/scripts/powershell/` - PowerShell scripts

**Key Scripts**:

**`create-new-feature.sh/.ps1`**
- Branch creation from natural language
- Automatic feature numbering
- Git workflow automation

**`setup-plan.sh/.ps1`**
- Implementation plan initialization
- Directory structure creation
- Template copying

**`check-prerequisites.sh/.ps1`**
- Environment validation
- Tool version checking
- Dependency verification

**`update-agent-context.sh/.ps1`**
- AI agent context management
- Command file updates
- Configuration synchronization

### File Management

**Automatic Ignore Files**:
- `.gitignore` - Version control
- `.dockerignore` - Container builds
- `.eslintignore` - Linting
- `.prettierignore` - Formatting
- Technology-specific patterns

**Supported Tech Stacks**:
- Node.js
- Python
- Java
- C#
- Go
- Rust
- Ruby
- PHP
- And more...

### Documentation Generation

**Automatic Artifacts**:

**`research.md`**
- Technical decisions and rationale
- Alternatives considered
- Justifications
- References

**`data-model.md`**
- Entities and relationships
- Validation rules
- Constraints
- Schema definitions

**`contracts/`**
- API specifications (OpenAPI)
- GraphQL schemas
- Interface contracts
- Service boundaries

**`quickstart.md`**
- Key validation scenarios
- Manual testing guide
- Setup instructions
- Usage examples

---

## 9. Quality Assurance

### Built-In Quality Gates

**1. Specification Quality Checklist**
- Generated via `/speckit.checklist`
- Validates requirements completeness
- Ensures clarity and consistency
- Acts as "unit tests for English"

**2. Constitution Compliance Gates (Phase -1)**
- Pre-implementation validation
- Architectural discipline enforcement
- Complexity tracking
- Justified exceptions

**3. Cross-Artifact Consistency Analysis**
- Generated via `/speckit.analyze`
- Spec ↔ Plan alignment
- Plan ↔ Tasks coverage
- Gap detection

**4. Independent Story Testability**
- Each user story independently testable
- Test criteria defined in tasks
- No dependencies between stories
- Validation checkpoints

**5. Checkpoint Validation**
- After each phase completion
- Verify gates passed
- Ensure quality standards met
- Document any exceptions

### Test-First Philosophy

**Article III: NON-NEGOTIABLE**
- TDD mandatory
- Tests written before implementation
- Tests must fail before coding (Red phase)
- Implementation makes tests pass (Green phase)
- Refactor with confidence (Refactor phase)

**Integration Over Unit**:
- Focus on integration tests
- Real environments over mocks
- Actual databases
- Real services
- Production-like conditions

**Benefits**:
- Confidence in changes
- Regression prevention
- Living documentation
- Design feedback

---

## 10. Project Structure Conventions

### Repository Layout

```
project-root/
├── .specify/                    # Spec-Kit directory
│   ├── memory/
│   │   └── constitution.md      # Project principles
│   ├── scripts/
│   │   ├── bash/                # POSIX scripts
│   │   └── powershell/          # Windows scripts
│   ├── specs/
│   │   └── ###-feature-name/
│   │       ├── spec.md          # What to build
│   │       ├── plan.md          # How to build
│   │       ├── tasks.md         # Step-by-step work
│   │       ├── research.md      # Technical decisions
│   │       ├── data-model.md    # Entities/relationships
│   │       ├── quickstart.md    # Validation scenarios
│   │       ├── contracts/       # API specifications
│   │       └── checklists/      # Quality gates
│   └── templates/
│       ├── spec-template.md
│       ├── plan-template.md
│       ├── tasks-template.md
│       └── commands/            # Slash command definitions
│
├── .claude/                     # Claude Code config (if using Claude)
│   └── commands.md
├── .cursor/                     # Cursor config (if using Cursor)
│   └── prompts.md
├── .gemini/                     # Gemini config (if using Gemini)
│   └── config.toml
│
├── src/                         # Source code
├── tests/                       # Test files
├── docs/                        # Documentation
└── README.md                    # Project readme
```

### Feature Numbering Convention

**Format**: `###-feature-name`

**Examples**:
- `001-user-authentication`
- `002-payment-processing`
- `003-notification-system`

**Benefits**:
- Clear ordering
- Easy reference
- Organized history
- Predictable structure

---

## 11. Key Documentation

### Core Methodology

**spec-driven.md** (25KB manifesto)
- Complete SDD methodology
- "The Power Inversion" concept
- Template-driven LLM quality
- Constitutional foundation
- Real-world examples
- Best practices

### Integration Guide

**AGENTS.md** (14KB)
- How to add new AI agent support
- Agent categories (CLI vs IDE)
- Command file formats
- AGENT_CONFIG structure
- Design decisions
- Testing procedures

### Quickstart

**README.md** (31KB)
- 5-step workflow
- Video overview
- 13+ supported agents
- CLI reference
- Troubleshooting
- Detailed process walkthrough

### Contributing

**CONTRIBUTING.md**
- Development guidelines
- Version management
- Release process
- Community standards

---

## 12. Key Strengths

### 1. Executable Specifications
**Not documentation—source of truth**
- Change specs to change software
- Code is generated output
- Specifications are versioned
- Implementation is disposable

### 2. Template-Constrained LLMs
**Templates as sophisticated prompts**
- Force proper abstraction levels
- Prevent common LLM mistakes
- Ensure consistency
- Encode best practices

### 3. Constitutional Governance
**Immutable principles, automated enforcement**
- Pre-implementation gates
- Complexity tracking
- Justified exceptions only
- Architectural integrity

### 4. User Story Independence
**Each story is MVP increment**
- Independently implementable
- Independently testable
- Parallel development friendly
- Clear value delivery

### 5. Multi-Agent Universality
**Works with any AI coding agent**
- Agent-agnostic specifications
- Consistent methodology
- Portable workflows
- Technology diversity

### 6. Structured Workflow
**Clear 5-step process**
- Constitution → Specify → Plan → Tasks → Implement
- Predictable and repeatable
- Quality gates at each step
- Continuous validation

### 7. Technology Independence
**Write once, implement anywhere**
- Technology-agnostic specs
- Multiple tech stack plans from one spec
- Objective comparison
- Best tool for the job

---

## 13. Innovation Highlights

### The Power Inversion
Traditional: Code → Specs (documentation)
SDD: Specs → Code (generated output)

**Result**: Specifications become executable, primary artifact

### Template-Driven AI Quality
Templates constrain AI behavior to prevent:
- Premature implementation
- Speculation and "might need" features
- Missing edge cases
- Inconsistent structure
- Over-engineering

**Result**: Higher quality, more consistent outputs

### Constitutional Governance
Architectural principles defined upfront:
- Enforced automatically
- Validated at Phase -1 (pre-implementation)
- Complexity tracked
- Exceptions justified

**Result**: Architectural discipline without manual oversight

### User Story Independence
Each story stands alone:
- Independent implementation
- Independent testing
- Independent deployment
- Independent value

**Result**: True incremental delivery, parallel development

### Multi-Agent Support
One methodology, many tools:
- 13+ AI coding assistants
- Same workflow across all
- Agent-specific configuration
- Portable specifications

**Result**: Tool flexibility without methodology chaos

---

## 14. Use Cases

### 0-to-1 Product Development
**Pattern**: Constitution → Feature 001 → MVP
- Define principles once
- Specify first feature
- Implement and validate
- Iterate with additional features

**Benefit**: Fastest path from idea to working product

### Feature Addition to Existing System
**Pattern**: New feature spec → Plan against existing tech stack
- Describe new feature (technology-agnostic)
- Plan implementation using existing stack
- Generate tasks
- Implement incrementally

**Benefit**: Structured approach to enhancement

### Technology Exploration
**Pattern**: One spec → Multiple plans → Parallel implementation
- Write spec once
- Generate plans for different stacks
- Implement in parallel
- Compare objectively

**Benefit**: Informed technology decisions

### Team Scaling
**Pattern**: Foundation → Split by user story → Parallel development
- Team builds foundation together
- Split by independent stories
- Develop in parallel
- Integrate without conflicts

**Benefit**: Linear team scaling

### Compliance-Heavy Domains
**Pattern**: Constitutional gates → Rigorous validation
- Encode compliance requirements in constitution
- Automatic gate validation
- Documentation generation
- Audit trail

**Benefit**: Compliance by design

---

## 15. Comparison with Traditional Approaches

### Traditional Development
1. Write code
2. Maybe write tests
3. Maybe write docs
4. Spec is in developer's head
5. Code becomes source of truth

**Problems**:
- Intent lost over time
- Difficult to change direction
- Knowledge silos
- Spec drift

### Spec-Kit Approach
1. Write constitution (principles)
2. Write spec (intent)
3. Generate plan (design)
4. Generate tasks (breakdown)
5. Implement (tests + code)

**Benefits**:
- Intent preserved
- Easy to regenerate
- Knowledge captured
- Spec is truth

---

## 16. Best Practices

### From the Methodology

1. **Never skip clarification for production features**
   - Use `/speckit.clarify` before planning
   - Resolve ambiguities early
   - Document decisions

2. **Constitution gates are non-negotiable**
   - Validate Phase -1 before implementation
   - Track complexity violations
   - Justify exceptions explicitly

3. **Each user story must be independently testable**
   - No dependencies between stories
   - Test criteria per story
   - Validate independently

4. **Max 3 projects initially**
   - Justify additional complexity
   - Start simple
   - Grow intentionally

5. **Use frameworks directly**
   - No unnecessary abstraction
   - Minimize indirection
   - Leverage existing tools

6. **Tests before code, always**
   - TDD is non-negotiable
   - Tests must fail first
   - Integration over unit

7. **Real environments over mocks**
   - Actual databases
   - Real services
   - Production-like conditions

8. **Specifications are versioned, not code**
   - Specs are source of truth
   - Code is generated
   - Change specs to change behavior

9. **Parallel implementations for experimentation**
   - Try multiple approaches
   - Compare objectively
   - Learn from diversity

10. **Document research and decisions**
    - Why, not just what
    - Alternatives considered
    - Rationale preserved

---

## Conclusion

**Spec-Kit transforms software development by making specifications executable.**

It provides:
- **Structured workflow** - 5 core commands + 3 enhancements
- **Template-driven quality** - AI behavior constrained for better outcomes
- **Constitutional governance** - Architectural discipline automated
- **Multi-agent support** - 13+ AI coding assistants
- **Complete automation** - Natural language to working code
- **Quality assurance** - Gates, checklists, validation
- **User story independence** - Parallel development, MVP delivery
- **Cross-platform support** - Bash and PowerShell

**The fundamental shift**: Specifications are not documentation—they are the source of truth. Code is the generated output. Change the spec, change the software.

**The power inversion is complete**: Instead of code driving specs, specs drive code. Instead of specifications serving code, code serves specifications. Instead of specs as scaffolding, specs as foundation.

**Result**: Software development that preserves intent, enables regeneration, supports exploration, and scales with teams—all while maintaining architectural integrity through constitutional governance.

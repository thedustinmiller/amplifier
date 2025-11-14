# Ultrathink Task - Comprehensive Development Pipeline

## Usage

`/ultrathink-task <TASK_DESCRIPTION>`

## Purpose

This command orchestrates a comprehensive development pipeline that takes a task from initial analysis through to implementation and review. It coordinates multiple specialized agents to ensure thorough, high-quality execution.

## Context

- Task description: $ARGUMENTS
- Relevant code or files will be referenced using @ file syntax
- Current profile elements are automatically available

## Your Role

You are the **Coordinator Agent** orchestrating specialized sub-agents to achieve the task through a systematic pipeline:

### Pipeline Stages

#### 1. ANALYZE (zen-architect)
**Purpose**: Deep problem analysis and architectural design

**Responsibilities**:
- Decompose the problem into manageable components
- Evaluate multiple solution approaches
- Design the minimal viable architecture
- Identify dependencies and constraints
- Create specifications for implementation

**Output**: Architectural direction document with:
- Problem breakdown
- Recommended approach with justification
- Module specifications
- Implementation guidelines

#### 2. PLAN (create-plan tool)
**Purpose**: Transform architecture into actionable plan

**Responsibilities**:
- Break down architecture into concrete tasks
- Order tasks by dependency
- Identify risks and mitigation strategies
- Set success criteria
- Create structured plan document

**Output**: Detailed implementation plan in @ai_working/tmp/

#### 3. IMPLEMENT (modular-builder)
**Purpose**: Execute the plan following modular design principles

**Responsibilities**:
- Build modules according to specifications
- Follow "bricks and studs" philosophy
- Implement clear contracts and interfaces
- Create self-contained, regeneratable components
- Write tests alongside implementation

**Output**: Working implementation with tests

#### 4. REVIEW (review-changes tool)
**Purpose**: Validate quality and alignment

**Responsibilities**:
- Run automated quality checks (make check, make test)
- Review against implementation philosophy
- Verify modular design principles
- Check for philosophy alignment
- Provide comprehensive quality report

**Output**: Review results with any issues identified

## Agent Orchestration Strategy

### Sequential Pipeline
This command uses **sequential execution** where each stage builds on the previous:
```
Architecture Design → Implementation Plan → Code Implementation → Quality Review
```

### Context Handoff Protocol
When delegating between stages:

1. **Provide Full Context**: Include all previous stage outputs
2. **Reference Prior Work**: "Building on the architecture from zen-architect..."
3. **Specify Expected Output**: Clear format and deliverables
4. **Set Quality Bar**: "This will be reviewed for philosophy compliance"

### Iteration Management
- **Between stages**: Pass complete outputs forward
- **Within stages**: Agent handles internal iterations
- **On failure**: Return to appropriate stage, don't start over

## Tool Usage Policy

**CRITICAL**: Always use TodoWrite to track the pipeline stages and progress.

### Required Tools
- **TodoWrite**: Track pipeline progress (mandatory)
- **Task**: Spawn specialized agents
- **Read/Write/Edit**: File operations
- **Bash**: Run tests and checks

### Pipeline Progress Tracking

Create todos for each pipeline stage:
```markdown
- [ ] Analyze problem with zen-architect
- [ ] Create implementation plan
- [ ] Implement with modular-builder
- [ ] Review changes and validate quality
```

Mark each as `in_progress` → `completed` as you proceed.

## Key Agents Available

### Always Use
- **zen-architect**: Architecture design, problem analysis, code review
- **modular-builder**: Implementation following modular principles
- **create-plan**: Structured planning tool
- **review-changes**: Quality validation tool

### Optional (Based on Needs)
- **bug-hunter**: When issues are discovered
- **test-coverage**: For comprehensive testing
- **security-guardian**: For security-sensitive features
- **post-task-cleanup**: Workspace cleanup after completion

## Process Flow

1. **Initialize**: Create TodoWrite list for all pipeline stages

2. **Stage 1 - Analyze**:
   - Spawn zen-architect with task description
   - Receive architectural direction
   - Mark analyze stage complete
   - Proceed to planning

3. **Stage 2 - Plan**:
   - Use create-plan tool with architectural direction
   - Generate structured implementation plan
   - Save plan to @ai_working/tmp/
   - Mark plan stage complete
   - Proceed to implementation

4. **Stage 3 - Implement**:
   - Spawn modular-builder with plan and architecture
   - Follow modular design principles
   - Build self-contained modules
   - Write tests
   - Mark implementation stage complete
   - Proceed to review

5. **Stage 4 - Review**:
   - Use review-changes tool
   - Run quality checks
   - Verify philosophy alignment
   - Report results
   - Mark review stage complete

6. **Completion**:
   - Provide summary of all stages
   - Report final status
   - List deliverables and their locations
   - Suggest next actions if any issues found

## Output Format

### Progress Updates
Show clear progress through pipeline stages:
```
✓ ANALYZE: Architecture designed
  → Next: Create implementation plan

✓ PLAN: Plan created at @ai_working/tmp/plan.md
  → Next: Begin implementation

⚙ IMPLEMENT: Building modules...
```

### Final Summary
Provide comprehensive results:
```markdown
## Ultrathink Task Complete

### Pipeline Results:
1. ✓ ANALYZE: [Summary of architectural decisions]
2. ✓ PLAN: [Location of plan document]
3. ✓ IMPLEMENT: [What was built, where]
4. ✓ REVIEW: [Quality check results]

### Deliverables:
- Architecture: [Path]
- Plan: [Path]
- Implementation: [Paths to created/modified files]
- Review: [Path to review results]

### Status: [SUCCESS | ISSUES FOUND]

### Next Actions:
- [Any recommended follow-ups]
```

## Failure Handling

### If Analysis Reveals Issues
- Stop pipeline
- Report blockers to user
- Suggest clarifications needed
- Don't proceed to implementation

### If Implementation Fails
- Report failure clearly
- Invoke bug-hunter if appropriate
- Don't proceed to review
- Provide diagnostics to user

### If Review Finds Issues
- Report issues clearly
- Suggest fixes
- Optionally iterate (up to max_iterations)
- Final decision to user

## Philosophy Alignment

This command embodies:

- **Analysis-First**: Always understand before building
- **Ruthless Minimalism**: Each stage produces minimal viable output
- **Respect User Time**: Automated pipeline saves manual coordination
- **Modular Design**: Implementation follows "bricks and studs"
- **Emergent Quality**: Architecture → Code → Validation cycle

## Success Metrics

A successful execution:
- ✓ Clear architecture with justification
- ✓ Actionable implementation plan
- ✓ Working code following modular principles
- ✓ All quality checks passing
- ✓ Philosophy alignment verified
- ✓ Clear documentation of decisions

## Example Usage

```
User: /ultrathink-task "Add user authentication with email/password"
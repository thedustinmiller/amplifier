# Profile Evaluation Test Suite

## Purpose

This directory contains a standardized set of tasks for empirically evaluating development profiles. These tasks enable:

1. **Profile Comparison** - Compare how different profiles approach identical challenges
2. **Longitudinal Analysis** - Track improvements in profiles over time
3. **Methodology Validation** - Verify that profiles produce appropriate outputs for their context
4. **Decision Support** - Help users choose the right profile for their work

## Test Philosophy

Each task is designed to:
- Be **realistic** - Represent actual development scenarios
- Be **repeatable** - Produce comparable results across runs
- Be **diverse** - Cover different types of work
- Be **measurable** - Have clear success criteria

## Task Catalog

### 1. Greenfield Project Creation
**File**: `task_01_greenfield_project.md`
**Type**: Building from scratch
**Complexity**: Medium
**Duration**: 2-4 hours

Create a new CLI tool from zero to working prototype. Tests emergent design, initial architecture decisions, and how profiles handle ambiguity.

**Key Differences Expected**:
- Default: Minimal MVP, defer features
- Waterfall: Comprehensive requirements first
- Mathematical-elegance: Formal specification upfront

---

### 2. Bug Investigation & Fix
**File**: `task_02_bug_fix.md`
**Type**: Debugging and repair
**Complexity**: Low-Medium
**Duration**: 30 minutes - 1 hour

Debug a specific issue in existing code, identify root cause, and implement fix. Tests problem analysis, surgical changes, and testing rigor.

**Key Differences Expected**:
- Default: Fast iteration, minimal test expansion
- Waterfall: Root cause analysis, impact assessment
- Mathematical-elegance: Prove correctness of fix

---

### 3. Research & Knowledge Synthesis
**File**: `task_03_research_synthesis.md`
**Type**: Research and documentation
**Complexity**: Medium-High
**Duration**: 2-3 hours

Deep research on a technical topic, synthesize findings, produce comprehensive report. Tests knowledge extraction, critical analysis, and synthesis.

**Key Differences Expected**:
- Default: Practical focus, quick conclusions
- Waterfall: Comprehensive coverage, formal citations
- Mathematical-elegance: Formal proofs, theoretical depth

---

### 4. Rapid Prototype
**File**: `task_04_rapid_prototype.md`
**Type**: Prototyping and exploration
**Complexity**: Low-Medium
**Duration**: 1-2 hours

Quickly build a working prototype to validate a concept. Tests speed, iteration, and tolerance for imperfection.

**Key Differences Expected**:
- Default: Fastest path to working demo
- Waterfall: Still requires some planning
- Mathematical-elegance: May struggle with "quick and dirty"

---

### 5. Documentation Writing
**File**: `task_05_documentation.md`
**Type**: Technical writing
**Complexity**: Medium
**Duration**: 1-2 hours

Write comprehensive documentation for an existing system. Tests clarity, completeness, and user-centric thinking.

**Key Differences Expected**:
- Default: Minimal but sufficient
- Waterfall: Exhaustive, formal structure
- Mathematical-elegance: Precise specifications

---

### 6. Code Refactoring
**File**: `task_06_refactoring.md`
**Type**: Structural improvement
**Complexity**: Medium-High
**Duration**: 2-3 hours

Refactor legacy code to improve structure without changing behavior. Tests architecture, cleanliness, and test preservation.

**Key Differences Expected**:
- Default: Iterative improvements
- Waterfall: Plan before refactoring
- Mathematical-elegance: Formal refactoring proofs

---

### 7. Third-Party Integration
**File**: `task_07_integration.md`
**Type**: External service integration
**Complexity**: Medium
**Duration**: 2-3 hours

Integrate a third-party API or service. Tests documentation reading, API usage, error handling.

**Key Differences Expected**:
- Default: Minimal wrapper, direct usage
- Waterfall: Adapter pattern, isolation
- Mathematical-elegance: Type-safe wrappers

---

### 8. Performance Optimization
**File**: `task_08_performance.md`
**Type**: Performance improvement
**Complexity**: Medium-High
**Duration**: 2-4 hours

Profile slow code, identify bottlenecks, and optimize. Tests analysis rigor, measurement, and trade-off decisions.

**Key Differences Expected**:
- Default: Profile, fix obvious issues
- Waterfall: Comprehensive analysis first
- Mathematical-elegance: Algorithmic complexity proofs

---

### 9. Test Coverage Addition
**File**: `task_09_test_coverage.md`
**Type**: Testing and quality
**Complexity**: Medium
**Duration**: 2-3 hours

Add comprehensive test coverage to untested code. Tests thoroughness, edge case thinking, and quality standards.

**Key Differences Expected**:
- Default: Cover critical paths
- Waterfall: Comprehensive test plan
- Mathematical-elegance: Property-based testing

---

### 10. System Migration
**File**: `task_10_migration.md`
**Type**: Migration and transformation
**Complexity**: High
**Duration**: 3-5 hours

Migrate a system from one approach to another (e.g., REST to GraphQL). Tests careful transformation, backward compatibility, and risk management.

**Key Differences Expected**:
- Default: Incremental, test in production
- Waterfall: Big bang with extensive testing
- Mathematical-elegance: Formal equivalence proofs

---

## Running Tests

### Single Profile Evaluation

```bash
# Switch to profile
/profile-switch <profile-name>

# Run a specific task
# Open task file, follow instructions, document approach and results
```

### Comparative Profile Evaluation

```bash
# For each profile:
1. /profile-switch <profile-name>
2. Execute task according to spec
3. Document in results/<profile-name>/<task-name>/
4. Capture: approach, timeline, artifacts, outcome
```

### Metrics to Capture

For each task execution, record:

1. **Time Metrics**
   - Time to first code
   - Total time to completion
   - Time spent in planning vs. implementation

2. **Process Metrics**
   - Number of phases/steps
   - Documentation produced (pages/words)
   - Tests written
   - Commits made

3. **Quality Metrics**
   - Tests passing
   - Code coverage (if applicable)
   - Complexity metrics
   - Issues found in review

4. **Cognitive Metrics**
   - First question asked
   - Decision framework used
   - Tradeoffs identified
   - Risk management approach

## Results Storage

```
testing/
├── profile_evaluation/
│   ├── README.md (this file)
│   ├── task_01_greenfield_project.md
│   ├── task_02_bug_fix.md
│   ├── ...
│   └── results/
│       ├── default/
│       │   ├── task_01/
│       │   │   ├── approach.md
│       │   │   ├── artifacts/
│       │   │   ├── metrics.json
│       │   │   └── reflection.md
│       │   └── ...
│       ├── waterfall/
│       ├── mathematical-elegance/
│       └── comparison_reports/
│           ├── task_01_comparison.md
│           └── ...
```

## Analysis Framework

### Success Criteria

Each task defines:
- **Functional** - Does it work?
- **Quality** - Is it well-built?
- **Appropriateness** - Does the approach match the context?
- **Efficiency** - Was time well-spent?

### Comparative Analysis

When comparing profiles on a task:

1. **Context Match** - Which profile's tradeoffs best suited this task?
2. **Outcome Quality** - Which produced the best result?
3. **Time Efficiency** - Which was fastest to completion?
4. **Process Clarity** - Which had the clearest methodology?
5. **Learning** - What did we learn about when to use each profile?

## Evolution Tracking

This test suite enables:

1. **Profile Refinement** - Use results to improve profile philosophy
2. **Trend Analysis** - Track improvements over time
3. **Pattern Discovery** - Identify which profiles excel at which tasks
4. **Validation** - Verify that profiles actually shape behavior as intended

## Usage Patterns

### For Profile Designers

Use this suite to:
- Validate new profiles before adding to the system
- Compare custom profiles to established ones
- Identify gaps in profile coverage

### For Users

Use this suite to:
- Choose the right profile for your current work
- Understand tradeoffs between approaches
- Calibrate expectations for each methodology

### For Researchers

Use this suite to:
- Study AI-assisted development methodologies
- Measure impact of different philosophical approaches
- Generate empirical evidence for process decisions

## Future Enhancements

Potential additions:

- **Task Variants** - Same task with different constraints
- **Multi-Profile Tasks** - Tasks requiring profile switching
- **Real-World Scenarios** - Tasks from actual projects
- **Automated Metrics** - Scripts to extract metrics automatically
- **Benchmark Suite** - Standardized scoring across tasks
- **Longitudinal Study** - Regular re-testing to track evolution

## Contributing Tasks

To add a new task:

1. Identify a common, realistic scenario not covered
2. Create `task_NN_description.md` following the template
3. Define clear success criteria
4. Specify expected profile differences
5. Include setup instructions and reference materials
6. Add entry to this README

## Task Template

See `task_template.md` for the standard structure.

## Notes

- Tasks should be **self-contained** - All context provided in task file
- Tasks should be **version-controlled** - Changes tracked over time
- Results should be **dated** - Track when tests were run
- Comparisons should be **fair** - Same starting conditions for all profiles

---

**Last Updated**: 2025-11-09
**Task Count**: 10
**Profiles Covered**: default, waterfall, mathematical-elegance, profile-editor

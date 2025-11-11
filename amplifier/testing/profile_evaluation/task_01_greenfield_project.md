# Task 01: Greenfield Project Creation

## Task Information

**Task ID**: task_01_greenfield_project
**Category**: Building from scratch
**Complexity**: Medium
**Estimated Duration**: 2-4 hours
**Last Updated**: 2025-11-09

## Objective

Design and implement a CLI tool called **"git-insights"** that analyzes a Git repository and produces a summary report of repository health metrics.

## Context

You're starting a new tool from scratch. There's no existing code, no legacy constraints, just requirements. This task tests how profiles handle:
- Initial architecture decisions
- Ambiguity resolution
- Feature scope management
- Testing from the start
- Documentation approach

## Requirements

### Functional Requirements

The tool should:
1. Accept a path to a Git repository as input
2. Analyze the repository and calculate:
   - Total commits in the last 30 days
   - Number of unique contributors in the last 30 days
   - Average commits per day
   - Most active file (by number of changes)
   - Commit message quality score (based on length and conventional commits format)
3. Output a formatted report to stdout
4. Support a `--json` flag for JSON output
5. Handle errors gracefully (repo doesn't exist, not a git repo, etc.)

### Non-Functional Requirements

- Should work on macOS, Linux, and Windows
- Should be installable via standard package manager
- Should have reasonable performance (< 5 seconds for repos with < 10k commits)
- Should follow Python best practices (or your chosen language)
- Should have help text (`--help`)

## Success Criteria

1. **Functional Success**:
   - All 5 core features work correctly
   - Error handling covers edge cases
   - JSON output is valid JSON

2. **Quality Success**:
   - Code passes linting
   - Has automated tests
   - README explains usage

3. **Process Success**:
   - Approach matches profile's philosophy
   - Decisions are documented
   - Scope was managed appropriately

4. **Efficiency Success**:
   - Completed within estimated time
   - No significant rework needed

## Starting Materials

Nothing! Greenfield.

**Setup**:
```bash
# Create workspace
mkdir git-insights
cd git-insights

# (Follow your profile's approach from here)
```

## Expected Profile Differences

### Default Profile (Minimalist)
- **Expected approach**:
  - Start with simplest implementation
  - One file, minimal dependencies
  - Defer JSON output until text output works
  - Basic tests for happy path
  - README with examples

- **Time estimate**: 2-3 hours

- **Key characteristics**:
  - Immediate coding after minimal planning
  - Feature deferral (may skip commit quality scoring initially)
  - Iterative refinement
  - "Ship it then improve it"

### Waterfall Profile (Phase-Gate)
- **Expected approach**:
  - Requirements analysis document (20-30 minutes)
  - Architecture design (30-45 minutes)
  - Detailed design (file structure, interfaces)
  - Implementation phase
  - Testing phase (comprehensive test plan)
  - Documentation phase

- **Time estimate**: 3-4 hours

- **Key characteristics**:
  - No coding until design approved
  - Comprehensive test coverage from start
  - Extensive documentation
  - Formal structure (maybe class-based)

### Mathematical-Elegance Profile (Formal Methods)
- **Expected approach**:
  - Formal specification of what "repository health" means
  - Type-driven design (branded types for CommitCount, etc.)
  - Property-based testing
  - Proofs of correctness for calculations
  - Pure functions wherever possible

- **Time estimate**: 3-5 hours

- **Key characteristics**:
  - Types prevent invalid states
  - Mathematical precision in metric definitions
  - Algebraic properties documented
  - May use advanced type features (TypedDict, Protocol, etc.)

## Evaluation Criteria

### Time Metrics
- [ ] Time to first working version
- [ ] Total completion time
- [ ] Time spent planning vs. coding vs. testing

### Process Metrics
- [ ] Number of distinct phases
- [ ] Lines of documentation
- [ ] Number of test cases
- [ ] Number of commits

### Quality Metrics
- [ ] All requirements met
- [ ] Error handling coverage
- [ ] Test coverage percentage
- [ ] Code quality (linting score)

### Cognitive Metrics
- [ ] First action taken (plan vs. code vs. specify)
- [ ] How scope was managed (all features vs. MVP)
- [ ] Testing approach (after vs. during vs. before)
- [ ] Documentation timing (during vs. after)

## Documentation Requirements

After completing the task, create:

**Directory structure**:
```
results/<profile-name>/task_01/
├── approach.md          # How you approached it
├── timeline.md          # When things happened
├── artifacts/           # The code you wrote
│   ├── git-insights/    # The actual project
│   └── screenshots/     # Example output
├── metrics.json         # Quantitative data
└── reflection.md        # What you learned
```

**Metrics to capture** (`metrics.json`):
```json
{
  "time_to_first_code_minutes": 0,
  "total_time_minutes": 0,
  "planning_time_minutes": 0,
  "implementation_time_minutes": 0,
  "testing_time_minutes": 0,
  "lines_of_code": 0,
  "lines_of_tests": 0,
  "lines_of_docs": 0,
  "test_count": 0,
  "test_coverage_percent": 0,
  "commits_made": 0,
  "features_implemented": ["feature1", "feature2"],
  "features_deferred": ["feature3"]
}
```

## Notes

- This is intentionally open-ended to see how profiles handle ambiguity
- "Commit quality score" is deliberately vague - how do profiles handle this?
- Performance requirement is there to see if profiles consider it
- Feel free to use any programming language, but document the choice

## Example Usage

Expected tool usage:
```bash
$ git-insights /path/to/repo

Git Repository Insights
=======================
Repository: /path/to/repo
Analysis Period: Last 30 days

Commit Activity:
  - Total commits: 47
  - Unique contributors: 3
  - Average commits/day: 1.6

Most Active File:
  - src/main.py (12 changes)

Commit Message Quality: 7.2/10
  - 85% follow conventional commits
  - Average message length: 52 characters

$ git-insights /path/to/repo --json
{"commits_30d": 47, "contributors_30d": 3, ...}
```

## References

- Git log parsing: `git log --since="30 days ago" --format="%H|%an|%s|%ad"`
- Conventional Commits: https://www.conventionalcommits.org/
- Similar tools: `git-quick-stats`, `git-fame`

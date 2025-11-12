# Task 06: Code Refactoring

## Task Information

**Task ID**: task_06_refactoring
**Category**: Structural improvement
**Complexity**: Medium-High
**Estimated Duration**: 2-3 hours
**Last Updated**: 2025-11-09

## Objective

Refactor a legacy script with poor structure into clean, maintainable code without changing its behavior.

## Context

You've inherited a working but messy script that processes log files. It works but is hard to maintain. Your task is to refactor it to improve code quality while preserving all existing functionality and test coverage.

This tests:
- Architecture and design skills
- Refactoring discipline (behavior preservation)
- Testing rigor
- Balance between improvement and pragmatism

## Requirements

### Functional Requirements

1. All existing functionality must continue to work
2. All existing tests must pass
3. Improve code structure and readability
4. Add any missing test coverage
5. Update documentation if needed

### Non-Functional Requirements

- No behavior changes (unless fixing bugs)
- Maintain backward compatibility
- Improve maintainability
- Follow language best practices
- Keep or improve performance

## Success Criteria

1. **Functional Success**:
   - All tests pass
   - Behavior unchanged
   - No regressions

2. **Quality Success**:
   - Code is more maintainable
   - Better structure
   - Clearer intent

3. **Process Success**:
   - Refactoring was systematic
   - Tests guided changes
   - Incremental improvements

4. **Efficiency Success**:
   - Completed in reasonable time
   - Didn't over-refactor

## Starting Materials

**File**: `log_analyzer.py` (legacy code)

```python
#!/usr/bin/env python3
"""Analyze log files for errors and warnings."""

import sys
import re
from datetime import datetime

def main():
    if len(sys.argv) != 2:
        print("Usage: log_analyzer.py <logfile>")
        sys.exit(1)

    logfile = sys.argv[1]

    # Read file
    lines = open(logfile).readlines()

    # Parse logs
    errors = []
    warnings = []
    info = []
    timestamps = []

    for line in lines:
        # Parse timestamp
        match = re.search(r'\[(.*?)\]', line)
        if match:
            timestamps.append(match.group(1))

        # Check level
        if 'ERROR' in line:
            errors.append(line)
        elif 'WARN' in line:
            warnings.append(line)
        else:
            info.append(line)

    # Stats
    total = len(lines)
    error_count = len(errors)
    warn_count = len(warnings)
    info_count = len(info)
    error_pct = (error_count / total * 100) if total > 0 else 0
    warn_pct = (warn_count / total * 100) if total > 0 else 0

    # Top errors
    error_msgs = []
    for err in errors:
        msg = err.split('ERROR')[1].strip() if 'ERROR' in err else err
        error_msgs.append(msg)

    from collections import Counter
    top_errors = Counter(error_msgs).most_common(5)

    # Time range
    if timestamps:
        first_time = datetime.strptime(timestamps[0], '%Y-%m-%d %H:%M:%S')
        last_time = datetime.strptime(timestamps[-1], '%Y-%m-%d %H:%M:%S')
        duration = (last_time - first_time).total_seconds()
    else:
        duration = 0

    # Print report
    print("=" * 60)
    print("LOG ANALYSIS REPORT")
    print("=" * 60)
    print(f"File: {logfile}")
    print(f"Total entries: {total}")
    print(f"Time range: {timestamps[0] if timestamps else 'N/A'} to {timestamps[-1] if timestamps else 'N/A'}")
    print(f"Duration: {duration:.0f} seconds")
    print()
    print("BREAKDOWN:")
    print(f"  Errors: {error_count} ({error_pct:.1f}%)")
    print(f"  Warnings: {warn_count} ({warn_pct:.1f}%)")
    print(f"  Info: {info_count}")
    print()
    if top_errors:
        print("TOP 5 ERRORS:")
        for msg, count in top_errors:
            print(f"  ({count}x) {msg[:60]}")
    print("=" * 60)

if __name__ == '__main__':
    main()
```

**Test file**: `test_log_analyzer.py`

```python
import pytest
from log_analyzer import main
import sys
from io import StringIO

def test_basic_parsing(tmp_path):
    # Create test log
    log_file = tmp_path / "test.log"
    log_file.write_text("""[2025-01-01 10:00:00] INFO Starting application
[2025-01-01 10:00:01] ERROR Database connection failed
[2025-01-01 10:00:02] WARN Retrying connection
[2025-01-01 10:00:03] ERROR Database connection failed
""")

    # Capture output
    sys.argv = ['log_analyzer.py', str(log_file)]
    captured = StringIO()
    sys.stdout = captured
    main()
    sys.stdout = sys.__stdout__

    output = captured.getvalue()
    assert 'Total entries: 4' in output
    assert 'Errors: 2' in output
    assert 'Warnings: 1' in output
```

## Expected Profile Differences

### Default Profile (Minimalist)
- **Expected approach**:
  - Extract functions for main chunks
  - Clean up obvious issues
  - Keep it simple
  - Light refactoring
  - Maybe 3-5 functions total

- **Time estimate**: 1-1.5 hours

- **Key characteristics**:
  - Iterative improvements
  - Stop when "good enough"
  - Pragmatic over perfect

### Waterfall Profile (Phase-Gate)
- **Expected approach**:
  - Analyze current structure
  - Design target architecture
  - Create refactoring plan
  - Implement systematically
  - Comprehensive testing
  - Full documentation

- **Time estimate**: 2-3 hours

- **Key characteristics**:
  - Thorough analysis first
  - Comprehensive refactoring
  - May introduce classes/patterns
  - Well-documented changes

### Mathematical-Elegance Profile (Formal Methods)
- **Expected approach**:
  - Identify pure vs. impure functions
  - Separate I/O from logic
  - Type-safe parsing
  - Prove equivalence of refactored version
  - Property-based tests

- **Time estimate**: 2.5-3.5 hours

- **Key characteristics**:
  - Functional core, imperative shell
  - Strong typing
  - Formal correctness
  - Elegant abstractions

## Evaluation Criteria

### Time Metrics
- [ ] Analysis time
- [ ] Refactoring time
- [ ] Testing time
- [ ] Total completion time

### Process Metrics
- [ ] Functions before/after
- [ ] Lines of code before/after
- [ ] Test coverage before/after
- [ ] Number of refactoring steps

### Quality Metrics
- [ ] All tests pass
- [ ] Code complexity (cyclomatic)
- [ ] Maintainability improvement
- [ ] Bug fixes (if any)

### Cognitive Metrics
- [ ] Refactoring strategy (big-bang vs. incremental)
- [ ] Architecture decisions
- [ ] Testing approach
- [ ] When to stop refactoring

## Documentation Requirements

Document in `results/<profile-name>/task_06/`:

1. **approach.md**:
   - Refactoring strategy
   - Key changes made
   - Design decisions
   - What you left alone and why

2. **timeline.md**:
   - Analysis phase
   - Each refactoring step
   - Testing time
   - Total time

3. **artifacts/**:
   - Refactored code
   - Updated tests (if any)
   - Before/after metrics

4. **metrics.json**:
```json
{
  "analysis_time_minutes": 0,
  "refactoring_time_minutes": 0,
  "total_time_minutes": 0,
  "before": {
    "lines_of_code": 0,
    "functions": 0,
    "complexity": 0
  },
  "after": {
    "lines_of_code": 0,
    "functions": 0,
    "complexity": 0
  },
  "test_coverage_before": 0,
  "test_coverage_after": 0,
  "refactoring_steps": ["extract function", "..."]
}
```

5. **reflection.md**:
   - Did you improve maintainability?
   - Did you over-refactor?
   - Where did you stop and why?

## Notes

- Tests must pass throughout
- Watch for the urge to rewrite vs. refactor
- Different profiles will have very different end results
- This tests discipline (preserve behavior)

## Expected Refactoring Patterns

**Default (Pragmatic)**:
- Extract parse_log_line()
- Extract calculate_stats()
- Extract print_report()
- Clean up variable names
- Maybe add type hints

**Waterfall (Structured)**:
- LogEntry dataclass
- LogParser class
- StatsCalculator class
- ReportGenerator class
- Full separation of concerns

**Mathematical-Elegance (Functional)**:
- Pure parsing functions
- Immutable data structures
- Separate I/O from logic
- Type-safe with NewTypes
- Composable functions

## References

- "Refactoring" by Martin Fowler
- Extract Method, Extract Function patterns
- Strangler Fig pattern for incremental refactoring

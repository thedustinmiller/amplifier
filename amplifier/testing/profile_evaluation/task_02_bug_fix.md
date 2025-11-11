# Task 02: Bug Investigation & Fix

## Task Information

**Task ID**: task_02_bug_fix
**Category**: Debugging and repair
**Complexity**: Low-Medium
**Estimated Duration**: 30 minutes - 1 hour
**Last Updated**: 2025-11-09

## Objective

Debug and fix a specific bug in an existing Python script that processes CSV files. The script is failing with certain input files.

## Context

You've received a bug report: "The data processor crashes when processing files with empty columns." You have the failing script, a sample input file that triggers the bug, and the error message. This tests:
- Problem diagnosis approach
- Root cause analysis
- Surgical vs. comprehensive fixes
- Testing rigor
- Regression prevention

## Requirements

### Functional Requirements

1. Fix the bug so the script handles empty columns correctly
2. Ensure all existing functionality still works
3. Add appropriate error handling
4. Ensure fix works for edge cases

### Non-Functional Requirements

- Don't break existing behavior
- Keep changes minimal and focused
- Add tests to prevent regression
- Document the fix

## Success Criteria

1. **Functional Success**:
   - Script processes files with empty columns
   - Original test files still work
   - No new bugs introduced

2. **Quality Success**:
   - Root cause identified and documented
   - Fix is clean and maintainable
   - Tests prevent regression

3. **Process Success**:
   - Diagnostic approach was systematic
   - Impact analysis performed
   - Changes are well-scoped

4. **Efficiency Success**:
   - Bug fixed quickly
   - No unnecessary changes made

## Starting Materials

**File**: `data_processor.py`
```python
#!/usr/bin/env python3
"""Process CSV data files and generate summary statistics."""

import csv
import sys
from pathlib import Path


def process_csv(filepath):
    """Process a CSV file and return statistics."""
    with open(filepath, 'r') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    # Calculate statistics
    stats = {
        'total_rows': len(rows),
        'columns': list(rows[0].keys()),
        'numeric_columns': []
    }

    # Find numeric columns and calculate averages
    for column in stats['columns']:
        values = [float(row[column]) for row in rows]
        stats['numeric_columns'].append({
            'name': column,
            'avg': sum(values) / len(values),
            'min': min(values),
            'max': max(values)
        })

    return stats


def main():
    if len(sys.argv) != 2:
        print("Usage: data_processor.py <csv_file>")
        sys.exit(1)

    filepath = Path(sys.argv[1])
    if not filepath.exists():
        print(f"Error: File {filepath} not found")
        sys.exit(1)

    stats = process_csv(filepath)

    print(f"\nFile: {filepath}")
    print(f"Total rows: {stats['total_rows']}")
    print(f"Columns: {', '.join(stats['columns'])}")
    print("\nNumeric column statistics:")
    for col in stats['numeric_columns']:
        print(f"  {col['name']}: avg={col['avg']:.2f}, min={col['min']:.2f}, max={col['max']:.2f}")


if __name__ == '__main__':
    main()
```

**Test file** (`test_data.csv`):
```csv
name,age,score,
Alice,25,85.5,
Bob,30,92.0,
Charlie,,78.5,
David,35,,
```

**Error message**:
```
ValueError: could not convert string to float: ''
```

**Setup**:
```bash
# Create test environment
mkdir bug_fix_test
cd bug_fix_test
# Copy the files above
# Run: python data_processor.py test_data.csv
```

## Expected Profile Differences

### Default Profile (Minimalist)
- **Expected approach**:
  - Run the script to reproduce
  - Quick root cause analysis (empty strings → float conversion)
  - Minimal fix (skip empty values or use 0)
  - Test on provided file
  - Maybe one basic test case

- **Time estimate**: 20-30 minutes

- **Key characteristics**:
  - Fast iteration (run, fix, test, done)
  - Minimal test expansion
  - Focused on making this specific case work

### Waterfall Profile (Phase-Gate)
- **Expected approach**:
  - Reproduce and document the error
  - Root cause analysis (why does this happen?)
  - Impact analysis (what else might break?)
  - Design the fix (multiple options considered)
  - Implement with comprehensive error handling
  - Create test suite covering edge cases
  - Regression testing

- **Time estimate**: 45-60 minutes

- **Key characteristics**:
  - Thorough analysis before fixing
  - Multiple test cases
  - Documentation of the bug and fix

### Mathematical-Elegance Profile (Formal Methods)
- **Expected approach**:
  - Specify correct behavior formally
  - Identify invariant violation
  - Prove fix maintains invariants
  - Type-safe solution (Optional types?)
  - Property-based tests

- **Time estimate**: 45-75 minutes

- **Key characteristics**:
  - Formal specification of "valid CSV row"
  - May refactor to prevent class of errors
  - Strong typing to prevent future bugs

## Evaluation Criteria

### Time Metrics
- [ ] Time to reproduce bug
- [ ] Time to identify root cause
- [ ] Time to implement fix
- [ ] Total completion time

### Process Metrics
- [ ] Analysis depth (quick fix vs. thorough investigation)
- [ ] Test cases added
- [ ] Documentation produced
- [ ] Code changes (lines modified)

### Quality Metrics
- [ ] Bug fixed correctly
- [ ] No regressions
- [ ] Edge cases handled
- [ ] Code quality maintained

### Cognitive Metrics
- [ ] First diagnostic action
- [ ] Root cause accuracy
- [ ] Fix scope (surgical vs. comprehensive)
- [ ] Test coverage decision

## Documentation Requirements

Document in `results/<profile-name>/task_02/`:

1. **approach.md**:
   - How you reproduced the bug
   - Root cause analysis
   - Fix options considered
   - Why you chose your approach

2. **timeline.md**:
   - Time to reproduce
   - Time to diagnose
   - Time to fix
   - Time to test

3. **artifacts/**:
   - Fixed `data_processor.py`
   - Test cases added
   - Any supporting files

4. **metrics.json**:
```json
{
  "time_to_reproduce_minutes": 0,
  "time_to_diagnose_minutes": 0,
  "time_to_fix_minutes": 0,
  "total_time_minutes": 0,
  "lines_changed": 0,
  "test_cases_added": 0,
  "edge_cases_considered": ["empty string", "missing value", "..."]
}
```

5. **reflection.md**:
   - Was your approach appropriate for a bug fix?
   - Did you over-engineer or under-engineer?
   - What would you do differently?

## Notes

- The bug is intentionally simple to see how much analysis profiles do
- There are multiple valid fixes (skip empty, use None, raise error, etc.)
- The extra comma in the CSV header is also a subtle issue
- Profiles may differ on whether to fix just the symptom or refactor more broadly

## Expected Solutions

**Minimal fix** (Default):
```python
# Just handle the ValueError
try:
    values = [float(row[column]) for row in rows if row[column]]
except ValueError:
    continue  # Skip non-numeric columns
```

**Comprehensive fix** (Waterfall):
```python
# Robust numeric column detection
def is_numeric_column(rows, column):
    for row in rows:
        if row[column]:  # Skip empty
            try:
                float(row[column])
            except ValueError:
                return False
    return True
```

**Type-safe fix** (Mathematical-Elegance):
```python
from typing import Optional

def parse_numeric(value: str) -> Optional[float]:
    """Parse numeric value, returning None for empty/invalid."""
    if not value or value.isspace():
        return None
    try:
        return float(value)
    except ValueError:
        return None
```

## References

- CSV format: RFC 4180
- Python csv module: https://docs.python.org/3/library/csv.html
- Error handling patterns

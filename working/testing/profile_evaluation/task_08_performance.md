# Task 08: Performance Optimization

## Task Information

**Task ID**: task_08_performance
**Category**: Performance improvement
**Complexity**: Medium-High
**Estimated Duration**: 2-4 hours
**Last Updated**: 2025-11-09

## Objective

Profile and optimize a slow data processing script to meet performance requirements.

## Context

A script that processes JSON data files is too slow. It needs to process 10,000 records in under 5 seconds, but currently takes 45 seconds. Your task is to identify bottlenecks and optimize.

This tests:
- Profiling and measurement
- Algorithmic thinking
- Trade-off analysis (speed vs. memory vs. complexity)
- Optimization discipline (measure, don't guess)

## Requirements

### Performance Requirements

- Process 10,000 records in < 5 seconds
- Memory usage should stay reasonable (< 500MB)
- Output must remain identical (byte-for-byte)

### Process Requirements

- Profile before optimizing
- Measure each optimization
- Document trade-offs
- Maintain readability

## Starting Materials

**Slow script**: `process_data.py`

```python
import json
import hashlib
from pathlib import Path

def process_record(record):
    """Process a single record."""
    # Calculate hash
    data = json.dumps(record, sort_keys=True)
    hash_val = hashlib.md5(data.encode()).hexdigest()

    # Transform data
    result = {
        'id': record['id'],
        'hash': hash_val,
        'score': calculate_score(record),
        'category': categorize(record),
        'related': find_related(record)
    }
    return result

def calculate_score(record):
    """Calculate a score (slow algorithm)."""
    score = 0
    for i in range(len(record.get('values', []))):
        for j in range(len(record.get('values', []))):
            score += abs(record['values'][i] - record['values'][j])
    return score

def categorize(record):
    """Categorize the record."""
    value = record.get('value', 0)
    if value < 10:
        return 'low'
    elif value < 100:
        return 'medium'
    else:
        return 'high'

def find_related(record):
    """Find related records (very slow)."""
    # This reloads the entire dataset each time!
    all_data = json.loads(Path('data.json').read_text())
    related = []
    for other in all_data:
        if other['id'] != record['id']:
            if other.get('category') == record.get('category'):
                related.append(other['id'])
    return related[:5]

def main():
    data = json.loads(Path('data.json').read_text())
    results = [process_record(r) for r in data]
    Path('output.json').write_text(json.dumps(results, indent=2))

if __name__ == '__main__':
    main()
```

**Performance target**: 10,000 records in < 5 seconds

## Expected Profile Differences

### Default Profile (Minimalist)
- **Expected approach**:
  - Quick profiling (time statements)
  - Fix obvious issues (reload in loop)
  - Maybe optimize one algorithm
  - Stop when fast enough

- **Time estimate**: 1-2 hours

### Waterfall Profile (Phase-Gate)
- **Expected approach**:
  - Comprehensive profiling
  - Systematic optimization plan
  - Measure each change
  - Document all trade-offs

- **Time estimate**: 2.5-3.5 hours

### Mathematical-Elegance Profile (Formal Methods)
- **Expected approach**:
  - Analyze algorithmic complexity
  - Prove optimizations correct
  - Mathematical optimization
  - Asymptotic analysis

- **Time estimate**: 3-4 hours

## Documentation Requirements

Standard structure in `results/<profile-name>/task_08/`

Include:
- Profiling results (before/after)
- Optimizations applied
- Trade-offs made
- Performance measurements

## References

- Python profilers: `cProfile`, `line_profiler`, `py-spy`
- Performance patterns
- Big O notation

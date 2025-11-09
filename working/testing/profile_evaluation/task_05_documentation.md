# Task 05: Documentation Writing

## Task Information

**Task ID**: task_05_documentation
**Category**: Technical writing
**Complexity**: Medium
**Estimated Duration**: 1-2 hours
**Last Updated**: 2025-11-09

## Objective

Write comprehensive documentation for an existing Python package that currently has minimal docs.

## Context

You've been given a small but functional Python package for working with semantic versions. It works well but has only minimal README. Your task is to write proper documentation so others can use it effectively.

This tests:
- Technical writing clarity
- Completeness vs. conciseness
- User-centric thinking
- Documentation structure
- Code example quality

## Requirements

### Functional Requirements

Documentation should include:

1. **Overview**: What is this package? Why use it?
2. **Installation**: How to install and setup
3. **Quick Start**: Get users productive in 5 minutes
4. **API Reference**: All public functions/classes documented
5. **Examples**: Common use cases with code
6. **Contributing**: (if time permits)

### Non-Functional Requirements

- Clear and concise writing
- Accurate code examples (tested)
- Good information architecture
- Appropriate depth for audience
- Proper formatting (Markdown/Sphinx/etc.)

## Success Criteria

1. **Functional Success**:
   - All public APIs documented
   - Examples work (tested)
   - User can get started in 5 minutes

2. **Quality Success**:
   - Clear writing
   - Good organization
   - Appropriate detail level

3. **Process Success**:
   - Documentation structure makes sense
   - Approach matched profile philosophy

4. **Efficiency Success**:
   - Completed in reasonable time
   - Didn't over-document or under-document

## Starting Materials

**Package**: `semver_utils`

**Existing README.md**:
```markdown
# semver_utils

Utilities for working with semantic versions.

## Install

```bash
pip install semver-utils
```

## Usage

```python
from semver_utils import Version

v = Version("1.2.3")
print(v.bump_minor())  # "1.3.0"
```
```

**Source code** (`semver_utils/__init__.py`):
```python
"""Semantic version utilities."""

import re
from typing import Optional


class Version:
    """Represents a semantic version (major.minor.patch)."""

    def __init__(self, version_string: str):
        self.original = version_string
        match = re.match(r'^(\d+)\.(\d+)\.(\d+)(-[a-zA-Z0-9.]+)?(\+[a-zA-Z0-9.]+)?$', version_string)
        if not match:
            raise ValueError(f"Invalid semantic version: {version_string}")

        self.major = int(match.group(1))
        self.minor = int(match.group(2))
        self.patch = int(match.group(3))
        self.prerelease = match.group(4)[1:] if match.group(4) else None
        self.build = match.group(5)[1:] if match.group(5) else None

    def bump_major(self) -> 'Version':
        """Increment major version and reset minor/patch to 0."""
        return Version(f"{self.major + 1}.0.0")

    def bump_minor(self) -> 'Version':
        """Increment minor version and reset patch to 0."""
        return Version(f"{self.major}.{self.minor + 1}.0")

    def bump_patch(self) -> 'Version':
        """Increment patch version."""
        return Version(f"{self.major}.{self.minor}.{self.patch + 1}")

    def __str__(self) -> str:
        result = f"{self.major}.{self.minor}.{self.patch}"
        if self.prerelease:
            result += f"-{self.prerelease}"
        if self.build:
            result += f"+{self.build}"
        return result

    def __eq__(self, other) -> bool:
        if not isinstance(other, Version):
            return False
        return (self.major, self.minor, self.patch, self.prerelease, self.build) == \
               (other.major, other.minor, other.patch, other.prerelease, other.build)

    def __lt__(self, other) -> bool:
        if not isinstance(other, Version):
            return NotImplemented
        return (self.major, self.minor, self.patch) < (other.major, other.minor, other.patch)

    def __le__(self, other) -> bool:
        return self == other or self < other

    def __gt__(self, other) -> bool:
        return not self <= other

    def __ge__(self, other) -> bool:
        return not self < other


def parse_version(version_string: str) -> Version:
    """Parse a version string into a Version object."""
    return Version(version_string)


def is_valid_version(version_string: str) -> bool:
    """Check if a string is a valid semantic version."""
    try:
        Version(version_string)
        return True
    except ValueError:
        return False
```

## Expected Profile Differences

### Default Profile (Minimalist)
- **Expected approach**:
  - Expand README.md
  - Focus on what users need most
  - Practical examples
  - Minimal structure (no fancy docs system)
  - "Good enough" coverage

- **Time estimate**: 45-75 minutes

- **Key characteristics**:
  - Single README.md file
  - Concise but complete
  - Code-heavy (examples > prose)
  - "Get users productive fast"

### Waterfall Profile (Phase-Gate)
- **Expected approach**:
  - Plan documentation structure
  - Comprehensive coverage
  - Formal organization
  - Maybe use Sphinx or similar
  - API reference, guides, examples separated

- **Time estimate**: 1.5-2.5 hours

- **Key characteristics**:
  - Multiple pages/sections
  - Exhaustive coverage
  - Formal style
  - May include diagrams

### Mathematical-Elegance Profile (Formal Methods)
- **Expected approach**:
  - Precise specifications
  - Formal contracts (pre/post-conditions)
  - Mathematical properties documented
  - Type signatures prominent
  - Proofs of correctness (if applicable)

- **Time estimate**: 1.5-2.5 hours

- **Key characteristics**:
  - Specification-focused
  - Formal language
  - Properties and invariants
  - Mathematical notation

## Evaluation Criteria

### Time Metrics
- [ ] Planning time
- [ ] Writing time
- [ ] Example coding/testing time
- [ ] Total completion time

### Process Metrics
- [ ] Documentation pages/sections
- [ ] Word count
- [ ] Code examples count
- [ ] APIs documented

### Quality Metrics
- [ ] Clarity (could a new user understand?)
- [ ] Completeness (all APIs covered?)
- [ ] Examples work (tested?)
- [ ] Organization (easy to find info?)

### Cognitive Metrics
- [ ] Who was the target audience?
- [ ] What was prioritized (completeness vs. clarity)?
- [ ] Documentation structure approach
- [ ] Depth of explanation

## Documentation Requirements

Document in `results/<profile-name>/task_05/`:

1. **approach.md**:
   - Documentation strategy
   - Structure decisions
   - Audience assumptions
   - What you prioritized

2. **timeline.md**:
   - Planning time
   - Writing time
   - Example creation time

3. **artifacts/**:
   - The actual documentation
   - README.md or docs/ folder
   - Tested examples

4. **metrics.json**:
```json
{
  "total_time_minutes": 0,
  "documentation_pages": 1,
  "word_count": 0,
  "code_examples": 0,
  "apis_documented": 0,
  "structure": "single_file | multiple_files"
}
```

5. **reflection.md**:
   - Was the depth appropriate?
   - Did you over-document or under-document?
   - Would users find this helpful?

## Notes

- Code is well-written with docstrings (you can use them)
- Watch for: too much detail vs. too little
- Different profiles will have very different docs
- Default may have minimal but practical docs
- Waterfall may have comprehensive structure
- Mathematical may focus on formal properties

## Expected Documentation Structures

**Default (Practical)**:
```markdown
# semver_utils

Python utilities for semantic versioning.

## Installation
## Quick Start
## API
### Version class
### Helper functions
## Examples
## FAQ
```

**Waterfall (Comprehensive)**:
```
docs/
├── index.md
├── getting_started/
│   ├── installation.md
│   ├── quick_start.md
│   └── concepts.md
├── api_reference/
│   ├── version_class.md
│   └── helper_functions.md
├── guides/
│   ├── version_bumping.md
│   ├── version_comparison.md
│   └── prereleases.md
├── examples/
│   └── common_use_cases.md
└── contributing.md
```

**Mathematical-Elegance (Formal)**:
```markdown
# semver_utils: Formal Specification

## Semantic Version Grammar

```bnf
<version> ::= <major>.<minor>.<patch>[-<prerelease>][+<build>]
```

## Version Type

```python
Version: Type
  where major: ℕ
        minor: ℕ
        patch: ℕ
        prerelease: Optional[String]
        build: Optional[String]
```

## Operations

### bump_major: Version → Version
**Pre-condition**: None
**Post-condition**: result.major = self.major + 1 ∧ result.minor = 0 ∧ result.patch = 0
**Invariant**: ∀v: Version. bump_major(v) > v

### Ordering
Versions form a total order:
- Reflexive: ∀v. v ≤ v
- Antisymmetric: ∀v,w. (v ≤ w ∧ w ≤ v) → v = w
- Transitive: ∀v,w,x. (v ≤ w ∧ w ≤ x) → v ≤ x
- Total: ∀v,w. v ≤ w ∨ w ≤ v
```

## References

- Semantic Versioning 2.0.0: https://semver.org/
- Example docs: requests, click, pytest documentation

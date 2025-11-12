# Analysis-First: Don't Code Without Understanding

For complex problems, always analyze before implementing. Decompose, consider options, identify trade-offs.

## When to Apply

Use analysis-first for:
- Non-trivial features (> 100 lines of code)
- Architectural decisions
- Performance-critical code
- Security-sensitive implementations
- Integration with external systems
- Refactoring existing systems

Skip for:
- Simple bug fixes
- Obvious implementations
- Well-understood patterns
- Following existing examples

## Analysis Pattern

### 1. Decompose the Problem

```markdown
## Problem Breakdown

**Core challenge**: [What are we really solving?]

**Sub-problems**:
1. [Problem part 1]
2. [Problem part 2]
3. [Problem part 3]

**Dependencies**:
- [External dependency 1]
- [Assumption 1]
```

### 2. Consider Options

```markdown
## Approach Options

### Option A: [Name]
- **Pros**: [Advantages]
- **Cons**: [Disadvantages]
- **Effort**: [Time estimate]

### Option B: [Name]
- **Pros**: [Advantages]
- **Cons**: [Disadvantages]
- **Effort**: [Time estimate]

### Option C: [Name]
- **Pros**: [Advantages]
- **Cons**: [Disadvantages]
- **Effort**: [Time estimate]
```

### 3. Identify Trade-offs

```markdown
## Trade-off Analysis

**Simplicity vs Power**: [Which option is simpler?]
**Speed vs Flexibility**: [Which is faster to implement?]
**Maintenance vs Features**: [Which is easier to maintain?]
```

### 4. Make Recommendation

```markdown
## Recommendation

**Choice**: Option [X]

**Justification**:
- [Reason 1]
- [Reason 2]
- [Reason 3]

**Implementation notes**:
- [Key point 1]
- [Key point 2]
```

## Benefits

### Prevents Premature Implementation
- Avoids major refactoring
- Identifies issues before coding
- Surfaces hidden complexity early

### Results in Cleaner Code
- Well-thought-out structure
- Appropriate abstractions
- Focused implementations

### Creates Natural Documentation
- Analysis becomes design doc
- Decisions are explained
- Trade-offs are recorded

### Enables Better Decisions
- Full context before committing
- Multiple perspectives considered
- Informed trade-offs

## Anti-Patterns to Avoid

**Jumping to code:**
```python
# User: "We need caching"
# AI: [Immediately writes Redis integration]
```

**Analysis paralysis:**
```markdown
## 47 Different Approaches to Consider
[10 pages of options analysis]
```

**Over-engineering:**
```markdown
## Abstract Factory Pattern for Cache Backends
[Complex inheritance hierarchy for simple need]
```

## The Right Balance

**Quick analysis** (5-15 minutes):
- Understand the problem
- Consider 2-3 options
- Make a recommendation
- Start implementing

**Not:**
- Days of planning
- Perfect documentation
- Every possible scenario

## Example: Analysis-First in Action

**Problem**: Add user authentication

**Bad approach:**
```
User: "Add user auth"
AI: [Writes OAuth2 + JWT + refresh tokens + role-based permissions]
```

**Good approach:**
```markdown
## Authentication Analysis

**Problem**: Users need to log in securely

**Options**:
1. Basic auth + sessions (simple, works for MVP)
2. OAuth2 (complex, handles SSO)
3. Magic links (simple, no passwords)

**Recommendation**: Option 1 (Basic auth + sessions)
- Meets current needs
- Simple to implement
- Can add OAuth2 later if needed

**Implementation**:
- Password hashing with bcrypt
- Session cookies with secure flags
- Login/logout endpoints
```

## Remember

- Analysis prevents waste, not causes it
- 15 minutes thinking saves hours of refactoring
- Complex problems deserve thoughtful solutions
- Simple problems should stay simple

**"Weeks of programming can save hours of planning."** — Anonymous

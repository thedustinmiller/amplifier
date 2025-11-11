# Principle: Coevolution

## Core Tenet
Specifications and code are conversation partners. Neither is purely authoritative—they inform each other in a continuous dialogue.

## Motivation

The traditional dichotomy is false:

**Code-First Problems**:
- Specs become stale documentation
- Intent is lost in implementation details
- Hard to change direction (code inertia)
- Technical debt accumulates invisibly

**Spec-First Problems**:
- Reality diverges from the plan
- Requirements crystallize only through implementation
- Over-specification of uncertain areas
- Waterfall thinking in agile contexts

**The Reality**:
Most projects don't start with clarity. Requirements emerge through the act of building. The project crystallizes from the dialogue between "what we want" (specs) and "what's possible" (code).

## Implications

### The Dialogue Pattern
1. **Sketch Spec**: Write rough specification (WHAT)
2. **Prototype**: Implement quickly (HOW)
3. **Discover**: Find gaps, ambiguities, impossibilities
4. **Refine Spec**: Update based on reality
5. **Improve Code**: Incorporate learnings
6. **Repeat**: Spiral toward coherence

### Memory Captures Both
Neither specs nor code are "source of truth":
- **Specs**: Capture intentions, goals, requirements
- **Code**: Captures implementations, constraints, solutions
- **Decisions**: Capture why something was chosen
- **Learnings**: Capture what worked and what didn't

Both inform future decisions.

### Questions, Not Decrees
Specs should ask questions as much as make statements:
- "Should we support OAuth?" (not "We must support OAuth")
- "How do users discover features?" (exploration)
- "What's the simplest thing?" (minimalism)
- "[NEEDS CLARIFICATION]" markers everywhere

### Implementation Teaches
Building reveals:
- What's actually hard vs what seemed hard
- Missing requirements
- Better approaches
- Technical constraints
- Edge cases

Feed these back into specs.

## Trade-offs

### What You Gain
- **Pragmatism**: Build what actually works
- **Adaptability**: Easy to change direction
- **Learning**: Each informs the other
- **Honesty**: Acknowledge uncertainty

### What You Sacrifice
- **Predictability**: Less upfront certainty
- **Compliance**: May not satisfy audit requirements
- **Contracts**: Harder to bid fixed-scope
- **Coordination**: Requires tight feedback loops

## Conflicts

### Incompatible Approaches
- **Pure Spec-Driven**: Spec must be complete before coding
- **Pure Code-Driven**: "Code is the documentation"
- **Waterfall**: Requirements frozen upfront
- **Fixed-Bid**: Requires complete specification

### Compatible Approaches
- **ruthless-minimalism**: Start small, adapt
- **emergent-design**: Structure emerges from solving problems
- **agile**: Iterations with feedback
- **spike-and-stabilize**: Explore then formalize

## Examples

### Feature: User Authentication

#### Iteration 1: Sketch & Prototype
**Spec**:
```markdown
# Auth
Users need to log in.
- Email/password probably?
- [NEEDS CLARIFICATION: Social login?]
- [NEEDS CLARIFICATION: 2FA?]
```

**Code**:
```python
def login(email, password):
    # Simplest thing
    user = get_user(email)
    if bcrypt.check(password, user.hash):
        return jwt.encode({"user_id": user.id})
```

#### Iteration 2: Discover & Refine
**Discoveries from Implementation**:
- Password reset is critical (users forget)
- Session management is complex
- Rate limiting needed (saw attacks)

**Updated Spec**:
```markdown
# Auth
Email/password with password reset.
- ✅ Email/password login
- ✅ Password reset via email
- ⏱️ Rate limiting (5 attempts/minute)
- 🚫 NOT doing: Social login (defer)
- 🚫 NOT doing: 2FA (defer until requested)
```

#### Iteration 3: Improve & Evolve
**Code Improvements**:
```python
@rate_limit(5, period=60)
def login(email, password):
    user = get_user(email)
    if not user or not bcrypt.check(password, user.hash):
        log_attempt(email, success=False)
        return None
    return generate_session(user)
```

**Spec Updated Again**:
```markdown
# Auth Learnings
- Rate limiting at 5/min works well
- Password reset requires email service (chose SendGrid)
- Session tokens expire after 7 days
- [FUTURE: Consider refresh tokens if mobile app]
```

### Feature: Data Storage

#### Iteration 1
**Spec**: "Store user data"
**Code**: SQLite file
**Learning**: Works for MVP

#### Iteration 2
**Reality**: 10K users, SQLite slow
**Spec Updated**: "Need faster queries for >10K users"
**Code**: Migrate to PostgreSQL
**Learning**: Premature PostgreSQL would've been wasted effort

## When to Use

### Good For
- Greenfield projects (requirements unclear)
- Exploratory work (learning by doing)
- Small teams (tight feedback loops)
- User-facing products (iterate on feedback)
- Evolving domains (requirements change)

### Bad For
- Regulated industries (audit trail required)
- Fixed-bid contracts (scope must be frozen)
- Distributed teams (slow feedback)
- Well-understood domains (requirements are clear)
- Safety-critical (must specify upfront)

## Practices

### Spec Maintenance
- Update specs after implementation
- Document discoveries
- Mark uncertainties with `[NEEDS CLARIFICATION]`
- Capture decisions with rationale
- Archive dead ends

### Code Documentation
- Link code to spec sections
- Comment non-obvious decisions
- Explain why, not what
- Point to relevant specs

### Memory System
Store three types of knowledge:
- **Specs**: What we want to build
- **Code**: What we built
- **Decisions**: Why we chose this path

All three inform future work.

### Review Cadence
After each feature:
1. What did we learn?
2. What surprised us?
3. What should we update in specs?
4. What should we refactor in code?

## Anti-Patterns

### Spec Rot
Writing specs then never updating them.
**Fix**: Treat specs as living documents.

### Code Cowboy
Writing code without any specification.
**Fix**: At least sketch intentions first.

### Analysis Paralysis
Trying to perfect specs before coding.
**Fix**: Prototype early to learn faster.

### Throwaway Specs
Treating specs as disposable scaffolding.
**Fix**: Specs are permanent knowledge, code is temporary implementation.

## Quotes

> "Everyone has a plan until they get punched in the mouth." — Mike Tyson

> "No battle plan survives contact with the enemy." — Helmuth von Moltke

> "The map is not the territory." — Alfred Korzybski

> "Plans are worthless, but planning is everything." — Dwight D. Eisenhower

## Related Concepts

- **Agile Development**
- **Evolutionary Architecture**
- **Spike and Stabilize**
- **Tracer Bullet Development**
- **Discovery-Driven Planning**

## Meta Note

This principle itself demonstrates coevolution:
- **Initial idea**: "Specs and code both matter"
- **Implementation experience**: Saw false dichotomy in practice
- **Refined principle**: "They're conversation partners"
- **Current version**: You're reading it
- **Future evolution**: Will update based on real projects

The principle evolves through practice.

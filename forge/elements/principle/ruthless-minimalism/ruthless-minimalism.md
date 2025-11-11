# Principle: Ruthless Minimalism

## Core Tenet
Ship the simplest thing that could possibly work, then adapt based on real needs.

## Motivation
Complexity is expensive. Time spent building features nobody needs is wasted. The best way to discover what's actually needed is to ship fast and learn.

Every line of code is a liability:
- It must be read and understood
- It must be maintained and updated
- It can contain bugs
- It increases cognitive load

The less code, the better—unless that code is actually providing value.

## Implications

### Ship Fast
- Measure in hours, not weeks
- MVP in 4 hours, not 4 months
- Get feedback quickly
- Iterate based on reality

### Defer Everything
- Don't build features until pain is real
- Don't add abstractions until duplication hurts
- Don't optimize until profiling says you must
- Don't plan for scale until you have users

### Delete Aggressively
- Remove unused code immediately
- Simplify when you touch code
- Question every dependency
- Prefer boring solutions

### Start Minimal
- Single file before multi-module
- Hard-coded before configurable
- In-memory before database
- Synchronous before async

## Trade-offs

### What You Gain
- **Speed**: Ship in hours, not months
- **Clarity**: Less code = easier to understand
- **Flexibility**: Easy to change direction
- **Focus**: Build only what matters

### What You Sacrifice
- **Predictability**: Less upfront planning
- **Elegance**: May require rewrites
- **Confidence**: Less coverage of edge cases
- **Compliance**: May not fit regulated environments

## Conflicts

### Incompatible Principles
- **waterfall**: Requires upfront planning
- **formal-verification**: Requires proofs before code
- **enterprise-governance**: Requires extensive documentation

### Compatible Principles
- **emergent-design**: Structure emerges from solving problems
- **coevolution**: Specs and code inform each other
- **rapid-feedback**: Quick iterations drive learning

## Examples

### Authentication
**Minimalist**: Email/password with bcrypt
```python
def login(email, password):
    user = db.get_user(email)
    if bcrypt.check(password, user.password_hash):
        return generate_jwt(user)
```

**Not Yet**: OAuth, 2FA, biometrics, passwordless

### Data Storage
**Minimalist**: SQLite file in local directory
```python
db = sqlite3.connect("app.db")
```

**Not Yet**: PostgreSQL, Redis, Elasticsearch, replication

### UI
**Minimalist**: Plain HTML forms
```html
<form action="/submit" method="post">
  <input name="name" required>
  <button>Submit</button>
</form>
```

**Not Yet**: React, state management, real-time updates

### Configuration
**Minimalist**: Hard-coded constants
```python
MAX_RETRIES = 3
TIMEOUT = 30
```

**Not Yet**: YAML files, environment variables, runtime configuration

## When to Use

### Good For
- Prototypes and MVPs
- Solo or small teams
- Exploration phase
- User-facing products (fast iteration)
- Startups (unknown requirements)

### Bad For
- Safety-critical systems
- Regulated industries
- Large teams (need coordination)
- Well-understood domains (requirements are clear)
- Long-term infrastructure

## Quotes

> "Perfection is achieved, not when there is nothing more to add, but when there is nothing left to take away." — Antoine de Saint-Exupéry

> "The best code is no code at all." — Jeff Atwood

> "Make it work, make it right, make it fast—in that order." — Kent Beck

## Related Patterns

- **YAGNI** (You Aren't Gonna Need It)
- **KISS** (Keep It Simple, Stupid)
- **Spike and Stabilize**
- **Walking Skeleton**
- **Tracer Bullet**

## Evolution

This principle doesn't mean "stay minimal forever." It means:

1. **Start minimal** (4 hours to MVP)
2. **Ship and learn** (real feedback)
3. **Add when pain is real** (not speculative)
4. **Refactor as you grow** (emergent design)

The complexity curve should track actual needs, not anticipated needs.

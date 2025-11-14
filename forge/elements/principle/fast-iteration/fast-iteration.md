# Principle: Fast Iteration

## Core Tenet
Ship quickly, learn from real feedback, iterate. Speed of learning trumps depth of analysis.

## Motivation

In uncertain environments, the fastest way to gain knowledge is through rapid experimentation. Analysis has diminishing returns—at some point, building and testing beats thinking and planning.

**Why Fast Iteration Works**:
- Real users reveal problems analysis misses
- Market conditions change faster than plans
- Early feedback compounds over time
- Momentum creates opportunities
- Fast failures cost less than slow failures

**The Cost of Delay**:
- Competitors ship while you plan
- Requirements change before you launch
- Team energy dissipates
- Assumptions go untested
- Perfect becomes enemy of good

## Implications

### Ship Early, Ship Often
- Measure cycles in hours or days, not weeks
- Get working prototypes in front of users immediately
- Don't wait for polish—ship rough drafts
- Every iteration teaches something
- Velocity creates its own advantages

### Embrace Imperfection
- Done is better than perfect
- Ship with known issues
- Fix real problems, not theoretical ones
- Let users tell you what matters
- Perfection is discovered, not planned

### Optimize for Learning Speed
- Small experiments over big bets
- Quick tests over long studies
- Real usage over simulated scenarios
- Behavioral data over surveys
- Multiple small iterations over one big launch

### Fail Fast, Fail Cheap
- Catch bad ideas early
- Test risky assumptions first
- Build minimal proofs of concept
- Abandon dead ends quickly
- Learn what doesn't work

## Trade-offs

### What You Gain
- **Speed**: Ship in days instead of months
- **Learning**: Real feedback from real users
- **Adaptability**: Easy to pivot based on data
- **Momentum**: Fast progress maintains energy
- **Risk Reduction**: Small failures instead of large ones

### What You Sacrifice
- **Completeness**: Features may be rough
- **Confidence**: Less upfront certainty
- **Efficiency**: May need rewrites
- **Planning**: Less coordination time
- **Quality**: Initial versions lack polish

## Conflicts

### Incompatible Principles
- **deep-analysis**: Requires thorough investigation before building
- **constitution-backed-design**: Requires comprehensive upfront specification
- **formal-verification**: Requires proofs before shipping
- **comprehensive-documentation**: Documentation takes time

### Compatible Principles
- **ruthless-minimalism**: Ship the simplest thing that works
- **emergent-design**: Structure emerges from solving problems
- **coevolution**: Specs and code inform each other through rapid cycles
- **autonomous-execution**: Move fast without waiting for approval

## Examples

### Product Feature Development

**Fast Iteration Approach**:
```markdown
Day 1: Sketch basic UI, ship to 10 users
Day 2: Gather feedback, fix obvious issues
Day 3: Ship improved version to 100 users
Day 4: Analyze usage data, iterate on UX
Day 5: Ship refined version to 1000 users
Week 2: Optimize based on real usage patterns
```

**Contrast with Deep Analysis**:
```markdown
Week 1-2: User research and interviews
Week 3-4: Design mockups and prototypes
Week 5-6: Architecture planning
Week 7-8: Implementation
Week 9: Internal testing
Week 10: Beta release
```

### API Design

**Fast Iteration**:
```python
# Day 1: Ship simplest API
@app.post("/items")
def create_item(name: str):
    return db.insert({"name": name})

# Day 2: Add based on real requests
@app.post("/items")
def create_item(name: str, tags: list = []):
    return db.insert({"name": name, "tags": tags})

# Day 3: Evolve based on usage
@app.post("/items")
def create_item(item: ItemCreate):
    # Structured input after seeing real patterns
    return db.insert(item.dict())
```

### Database Schema

**Fast Iteration**:
```sql
-- Day 1: Minimal schema
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    email TEXT,
    created_at TIMESTAMP
);

-- Week 1: Add columns as needs emerge
ALTER TABLE users ADD COLUMN last_login TIMESTAMP;
ALTER TABLE users ADD COLUMN preferences JSON;

-- Month 1: Refactor based on real access patterns
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_last_login ON users(last_login);
```

### Testing Strategy

**Fast Iteration**:
```python
# Ship with minimal tests
def test_core_flow():
    user = create_user("test@example.com")
    login(user)
    assert user.is_authenticated

# Add tests as bugs are found
def test_edge_case_discovered_in_production():
    # Test added after production issue
    user = create_user("")  # Empty email crashed
    assert user is None
```

## When to Use

### Good For
- Startups and new products
- Uncertain requirements
- Competitive markets
- User-facing features
- Exploratory projects
- Rapid prototyping
- MVP development
- Learning new technologies

### Bad For
- Safety-critical systems
- Regulated industries
- Large-scale infrastructure
- Irreversible decisions
- Hardware/embedded systems
- Long deployment cycles
- High migration costs

## Practices

### Cycle Time Metrics
Track and optimize:
- Idea to prototype: < 1 day
- Prototype to user feedback: < 1 day
- Feedback to iteration: < 1 day
- Full cycle time: < 3 days

### Shipping Cadence
- Daily deploys for web apps
- Continuous deployment when possible
- Feature flags for gradual rollouts
- Quick rollback capabilities
- Monitoring for fast issue detection

### Feedback Loops
- User analytics from day 1
- Quick user interviews
- Usage metrics dashboards
- Error tracking and monitoring
- A/B testing for key decisions

### Technical Practices
- Keep builds fast (< 5 minutes)
- Automated deployment
- Feature flags
- Database migrations
- Backward compatibility

## Anti-Patterns

### Reckless Speed
Shipping fast doesn't mean shipping broken.
**Fix**: Maintain minimum quality bar, use feature flags.

### Analysis Avoidance
Fast iteration doesn't eliminate thinking.
**Fix**: Quick analysis (hours, not weeks) before building.

### Thrash
Changing direction every day with no learning.
**Fix**: Define what you're testing, measure it, learn from it.

### Technical Debt Spiral
Fast today, impossible tomorrow.
**Fix**: Regular refactoring, pay down debt between features.

## Quotes

> "Move fast and break things." — Facebook (original motto)

> "If you're not embarrassed by the first version of your product, you've launched too late." — Reid Hoffman

> "Speed is the ultimate weapon in business. All else being equal, the fastest company in any market will win." — Brian Chesky

> "The faster you iterate, the faster you learn." — Eric Ries

## Related Patterns

- **Lean Startup**: Build-Measure-Learn
- **Agile Development**: Short sprints, frequent releases
- **MVP (Minimum Viable Product)**: Smallest testable version
- **Spike and Stabilize**: Prototype fast, refine later
- **Continuous Deployment**: Ship every commit

## Progression

Fast iteration doesn't mean staying fast forever:

1. **Discovery Phase**: Extremely fast, rough prototypes
2. **Validation Phase**: Fast iterations with real users
3. **Growth Phase**: Balanced speed with stability
4. **Maturity Phase**: Measured changes to stable system

The principle guides you to start fast and slow down deliberately as you learn, not the reverse.

## Success Metrics

You're doing fast iteration well when:
- You ship multiple times per week
- Users see new features regularly
- You have data driving decisions
- Failed experiments cost days, not months
- Team can pivot quickly based on feedback
- Cycle time is decreasing over time

# Principle: Wide Search

## Core Tenet
Explore many approaches before committing. Defer decisions until you've discovered the solution space. Innovation comes from considering diverse options.

## Motivation
Early commitment is expensive. When you pick the first solution that works, you miss better alternatives. The best approach often isn't obvious upfront—it emerges from exploring the landscape.

The danger of premature convergence:
- Lock into suboptimal solutions
- Miss elegant alternatives
- Build on wrong assumptions
- Accumulate technical debt
- Limit creative possibilities

The value of exploration:
- Discover unexpected solutions
- Understand trade-off landscape
- Build confidence in final choice
- Learn domain deeply
- Avoid costly rework

## Implications

### Explore Before Committing
- Generate multiple solution candidates
- Prototype different approaches
- Research existing solutions
- Consider unconventional options
- Defer architectural decisions

### Diverge Then Converge
- **Phase 1: Diverge** - Explore widely, defer judgment
- **Phase 2: Evaluate** - Compare options, understand trade-offs
- **Phase 3: Converge** - Choose approach based on evidence
- **Phase 4: Commit** - Implement fully with confidence

### Learn the Landscape
- What approaches exist?
- What are the trade-offs?
- What constraints matter?
- What have others tried?
- What failed and why?

### Defer Big Decisions
- Don't commit to databases early
- Don't lock into frameworks prematurely
- Don't choose architectures upfront
- Keep options open as long as practical
- Use abstraction to defer commitment

## Trade-offs

### What You Gain
- **Better Solutions**: Find optimal approaches through exploration
- **Understanding**: Deep knowledge of trade-off landscape
- **Innovation**: Discover novel combinations
- **Confidence**: Choose based on evidence, not guesses
- **Flexibility**: Easy to pivot if context changes

### What You Sacrifice
- **Speed**: Exploration takes time
- **Focus**: Multiple prototypes divide attention
- **Simplicity**: Comparative analysis adds complexity
- **Predictability**: Harder to estimate completion
- **Efficiency**: Some exploration is "wasted" effort

## Conflicts

### Incompatible Principles
- **focused-refinement**: Commits early, optimizes one approach
- **fast-iteration** (when extreme): May favor speed over exploration
- **ruthless-minimalism** (when extreme): May skip research phase

### Compatible Principles
- **emergent-design**: Structure emerges from solving problems
- **coevolution**: Specs and code inform each other through exploration
- **deep-analysis**: Thorough investigation complements wide search
- **experimental-features**: Both value trying new things

## Examples

### Database Selection
**Wide Search Approach**:
```
Phase 1: Explore Options (Day 1-2)
---------------------------------
1. SQLite: Prototyped user auth with SQLite
   + Zero setup, simple, great for dev
   - File locking issues with concurrent writes
   - No built-in replication

2. PostgreSQL: Prototyped with same schema
   + Row-level locking, mature replication
   + Excellent JSON support for flexible fields
   - Requires server setup, more ops overhead

3. MongoDB: Prototyped document model
   + Very flexible schema for evolving data
   + Easy horizontal scaling
   - Eventual consistency issues for auth
   - Harder to do relational queries for reports

4. Redis + PostgreSQL: Prototyped hybrid
   + Fast reads from Redis, durable writes to Postgres
   + Best of both worlds
   - Adds complexity, cache invalidation hard

Phase 2: Evaluate (Day 3)
-------------------------
Criteria:
- Concurrent users: Need 1K+ simultaneous
- Data model: Mostly relational, some JSON metadata
- Ops complexity: Small team, prefer managed
- Query patterns: Complex reports needed

Comparison:
| Solution    | Concurrency | Flexibility | Ops Cost | Reports |
|-------------|-------------|-------------|----------|---------|
| SQLite      | ✗ Poor      | ○ Medium    | ✓ Low    | ✓ Good  |
| PostgreSQL  | ✓ Excellent | ✓ Good      | ○ Medium | ✓ Good  |
| MongoDB     | ✓ Good      | ✓ Excellent | ○ Medium | ✗ Hard  |
| Redis+PG    | ✓ Excellent | ✓ Good      | ✗ High   | ✓ Good  |

Phase 3: Decide (Day 3)
-----------------------
Choice: PostgreSQL
- Meets all requirements without over-engineering
- Team has expertise
- Managed hosting available ($50/mo)
- Can add Redis later if needed (defer decision)

Phase 4: Commit (Day 4+)
------------------------
Implement full schema, migrations, connection pooling, etc.
```

**Focused Refinement** (for contrast):
```
Day 1: PostgreSQL is industry standard for web apps. Using that.
Day 2-10: Build full implementation with PG.
```

### Architecture Pattern
**Wide Search Approach**:
```
Phase 1: Explore (Week 1)
-------------------------
Research question: How should we structure the API?

Approach A: Monolithic Django
  Prototyped: User CRUD + Product CRUD in single Django app
  Findings:
  + Fast to develop, single codebase
  + Easy to share models and utilities
  - Would become large over time
  - Harder to scale different components independently

Approach B: Microservices
  Prototyped: Separate Flask services for users, products
  Findings:
  + Independent deployment and scaling
  + Team can work independently
  - Network latency between services
  - Distributed debugging is hard
  - Overkill for current team size (3 devs)

Approach C: Modular Monolith
  Prototyped: Django with strict module boundaries
  Findings:
  + Single deployment, clear boundaries
  + Can extract to services later if needed
  + Simpler than microservices, cleaner than monolith
  - Requires discipline to maintain boundaries

Approach D: Serverless Functions
  Prototyped: AWS Lambda + API Gateway
  Findings:
  + Zero ops, infinite scale
  + Pay per request
  - Cold start latency (200-500ms)
  - Vendor lock-in to AWS
  - Debugging is painful

Phase 2: Evaluate (Week 2)
--------------------------
Context:
- Team: 3 developers, no dedicated ops
- Scale: Expect 10K users in year 1
- Features: 5 major domains (users, products, orders, etc.)

Trade-off Analysis:
| Pattern          | Dev Speed | Scalability | Ops Cost | Complexity |
|------------------|-----------|-------------|----------|------------|
| Monolith         | ✓ Fast    | ○ Medium    | ✓ Low    | ✓ Low      |
| Microservices    | ✗ Slow    | ✓ High      | ✗ High   | ✗ High     |
| Modular Monolith | ✓ Fast    | ○ Medium    | ✓ Low    | ○ Medium   |
| Serverless       | ○ Medium  | ✓ High      | ✓ Low    | ○ Medium   |

Phase 3: Decide (Week 2)
------------------------
Choice: Modular Monolith
- Matches team size and scale needs
- Easy to evolve (can extract services later)
- Low ops overhead with single deployment
- Clear boundaries prevent big ball of mud

Deferred decisions:
- Exact module boundaries (will emerge)
- Database per module vs shared (start shared)
- Extract to microservices (only if needed at scale)

Phase 4: Implement (Week 3+)
----------------------------
Build modular structure with clear interfaces between domains.
```

**Focused Refinement** (for contrast):
```
Week 1: Rails monolith. It's what we know, ship fast.
Week 2-12: Build all features in Rails.
```

### Authentication Strategy
**Wide Search Approach**:
```
Phase 1: Explore Options
-------------------------
1. Email/Password + JWT
   Implementation: 4 hours
   Security: Good (bcrypt + secure tokens)
   UX: Familiar, works everywhere
   Maintenance: We own the code

2. OAuth (Google/GitHub)
   Implementation: 6 hours (tested Google OAuth)
   Security: Excellent (delegated to provider)
   UX: One-click login, no password to remember
   Maintenance: Depends on external service

3. Magic Links (email-based)
   Implementation: 5 hours
   Security: Good (time-limited tokens)
   UX: No password, can be slow (email delays)
   Maintenance: Requires reliable email service

4. Passkeys (WebAuthn)
   Implementation: 12 hours (complex spec)
   Security: Excellent (phishing-resistant)
   UX: Best on mobile, confusing to some users
   Maintenance: Browser support still evolving

Phase 2: Analyze User Needs
---------------------------
Survey results (100 beta users):
- 60% prefer social login (Google/GitHub)
- 30% want traditional email/password
- 10% interested in passwordless

Use cases:
- B2B customers: Need SSO (future requirement)
- Open source users: GitHub OAuth perfect fit
- Enterprise: Email/password + SSO

Phase 3: Multi-Method Strategy
------------------------------
Decision: Support multiple methods
1. Start with GitHub OAuth (60% of users, 6 hours)
2. Add email/password (covers remaining 40%, 4 hours)
3. Defer magic links (low demand, not urgent)
4. Defer passkeys (complex, immature browser support)
5. Plan for SAML/SSO (enterprise future, not MVP)

Phase 4: Implement
------------------
Build OAuth + email/password with shared user model.
Architecture allows adding methods later without refactoring.
```

**Focused Refinement** (for contrast):
```
Email/password auth. Standard approach, well-understood.
Implement immediately, ship in 4 hours.
```

### UI Framework Selection
**Wide Search Approach**:
```
Phase 1: Build Same Component in Each (2 days)
----------------------------------------------
Task: User dashboard with real-time updates

React:
  Code: 150 lines (component + hooks)
  Build time: 3.2s
  Bundle size: 145KB
  Developer experience: Excellent tooling, huge ecosystem
  Learning curve: Hooks can confuse newcomers

Vue:
  Code: 120 lines (SFC with Composition API)
  Build time: 2.1s
  Bundle size: 95KB
  Developer experience: Great docs, gentle learning curve
  Learning curve: Easiest for beginners

Svelte:
  Code: 90 lines (reactive statements)
  Build time: 1.5s
  Bundle size: 45KB
  Developer experience: Magical, less boilerplate
  Learning curve: Different mental model

Vanilla JS + Alpine.js:
  Code: 80 lines (HTML + Alpine directives)
  Build time: 0s (no build step!)
  Bundle size: 15KB
  Developer experience: Simple, no complex tooling
  Learning curve: Very easy

Phase 2: Evaluate for Project Context
-------------------------------------
Context:
- Team: 2 frontend devs (both know React)
- App: Dashboard with forms and charts
- Hiring: Likely to hire more devs soon

Comparison:
| Framework | Performance | DX | Ecosystem | Hiring Pool |
|-----------|-------------|----|-----------|-----------|
| React     | ○ Good      | ✓  | ✓ Huge    | ✓ Large   |
| Vue       | ✓ Better    | ✓  | ○ Medium  | ○ Medium  |
| Svelte    | ✓ Best      | ✓  | ○ Small   | ✗ Small   |
| Alpine    | ✓ Best      | ○  | ✗ Tiny    | ✗ Tiny    |

Phase 3: Decide Based on Constraints
------------------------------------
Choice: React
- Team already knows it (zero ramp-up)
- Easy to hire React developers
- Rich ecosystem for charts/forms
- Performance "good enough" for our scale

Trade-off: Larger bundles, but CDN + code splitting mitigate

Deferred: Can try Svelte for new projects once team comfortable
```

**Focused Refinement** (for contrast):
```
React. Team knows it, huge ecosystem, easy hiring.
Start building immediately.
```

## When to Use

### Good For
- Unfamiliar domains (don't know the landscape)
- High-stakes decisions (expensive to change later)
- Innovation projects (need novel solutions)
- Research phases (learning is the goal)
- Greenfield projects (no constraints yet)
- Complex problems (many variables)
- Long-term architecture (will live for years)

### Bad For
- Well-understood problems (landscape is known)
- Time-critical fixes (need solution now)
- Low-stakes decisions (easy to change later)
- Maintenance work (approach already chosen)
- Tight deadlines (exploration is expensive)
- Simple problems (obvious solution exists)

## Quotes

> "Look before you leap." — Proverb

> "The best way to have a good idea is to have lots of ideas." — Linus Pauling

> "Exploration is really the essence of the human spirit." — Frank Borman

> "Set-based concurrent engineering: Consider multiple alternatives simultaneously, eliminate gradually." — Toyota Production System

> "All models are wrong, but some are useful." — George Box

## Related Patterns

- **Set-Based Design**: Consider multiple options, eliminate gradually
- **Spike Solutions**: Time-boxed prototypes to reduce risk
- **A/B Testing**: Test multiple approaches with real users
- **Divergent/Convergent Thinking**: Brainstorm widely, then narrow
- **Fail Fast**: Try many things, discard quickly

## Evolution

This principle doesn't mean "explore forever." It means:

1. **Time-box exploration**: Fixed budget for research phase
2. **Prototype, don't perfect**: Quick experiments, not production code
3. **Compare meaningfully**: Define criteria upfront
4. **Commit decisively**: After exploring, commit fully
5. **Document learnings**: Why you chose, why you rejected

The exploration process:

```
Phase 1: Diverge (20% of time)
- Generate many options
- Quick prototypes
- Research existing solutions
- Consider unconventional approaches

Phase 2: Evaluate (20% of time)
- Define comparison criteria
- Test against real requirements
- Understand trade-offs
- Identify deal-breakers

Phase 3: Converge (10% of time)
- Choose based on evidence
- Document decision rationale
- Plan implementation
- Identify risks

Phase 4: Commit (50% of time)
- Build full solution
- Optimize chosen approach
- No second-guessing
- Ship confidently
```

Time allocation is flexible, but exploration shouldn't dominate. The goal is informed commitment, not perpetual research.

When to stop exploring:
- Diminishing returns (new options similar to existing)
- Clear winner emerges
- Time budget exhausted
- Risk reduced to acceptable level
- Team has sufficient confidence

Defer exploration for:
- Low-risk decisions (easy to change later)
- Well-understood problems (landscape is known)
- Time-critical situations (ship now, optimize later)
- Non-critical features (MVP doesn't need perfection)

Balance exploration with execution.

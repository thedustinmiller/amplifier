# Principle: Detailed Explanation

## Core Tenet
Explain reasoning, show work, and educate the user. Transparency in decision-making builds understanding and enables better collaboration.

## Motivation
Software development is a learning process. When an agent or developer makes decisions without explaining why, valuable knowledge is lost. Users learn better when they understand the reasoning, debugging becomes easier with context, and teams collaborate more effectively when decisions are transparent.

Every decision has a rationale:
- Why this approach over alternatives?
- What constraints influenced the choice?
- What trade-offs were considered?
- What might break and why?

Sharing this reasoning:
- Builds user understanding and expertise
- Enables informed decision-making
- Creates a learning environment
- Facilitates debugging and maintenance
- Reduces miscommunication

## Implications

### Show Your Work
- Explain why you chose an approach
- List alternatives you considered
- Describe trade-offs explicitly
- Share relevant context
- Document decision rationale

### Educate Through Output
- Include brief explanations for non-obvious choices
- Reference relevant documentation
- Highlight potential pitfalls
- Explain error messages in context
- Link to related concepts

### Provide Rich Context
- Show what you're searching for and why
- Describe what you found and what it means
- Explain how pieces fit together
- Clarify assumptions and constraints
- Make implicit knowledge explicit

### Debug-Friendly Communication
- Include relevant file paths and line numbers
- Show before/after comparisons
- Explain what changed and why
- Highlight potential side effects
- Provide verification steps

## Trade-offs

### What You Gain
- **Learning**: Users understand reasoning and build expertise
- **Transparency**: Decision-making process is visible
- **Debuggability**: Rich context makes troubleshooting easier
- **Collaboration**: Shared understanding enables better teamwork
- **Trust**: Openness builds confidence in decisions

### What You Sacrifice
- **Speed**: More output takes longer to produce and consume
- **Brevity**: Experienced users may prefer less explanation
- **Focus**: Important information may get buried in detail
- **Efficiency**: Reading comprehensive output takes time
- **Velocity**: More communication slows down fast iteration

## Conflicts

### Incompatible Principles
- **minimal-output**: Prefers concision over explanation
- **fast-iteration** (when extreme): May prioritize speed over documentation
- **autonomous-execution**: May skip user-facing explanations

### Compatible Principles
- **deep-analysis**: Thorough investigation pairs well with detailed explanation
- **user-confirmation**: Both value transparency and user involvement
- **comprehensive-documentation**: Aligned philosophy of explicit knowledge

## Examples

### Code Review
**Detailed Explanation**:
```
I'm refactoring the authentication flow for three reasons:

1. Security: The current implementation stores passwords in plain text
   (security.md#password-storage). We need bcrypt hashing.

2. Maintainability: The 200-line authenticate() function violates SRP.
   Breaking it into verify_credentials() and create_session() makes
   testing easier and responsibilities clearer.

3. Performance: Current O(n) user lookup becomes O(1) with email index.
   This matters at >1000 users (profiling data in docs/perf.txt).

Trade-offs:
- (+) Much more secure
- (+) Easier to test
- (+) Faster lookups
- (-) Requires database migration
- (-) Breaks backward compatibility with old password format

Migration plan:
1. Add bcrypt hash column
2. Hash passwords on next login
3. Remove plain text column after 90 days
```

**Minimal Output** (for contrast):
```
Refactoring auth: adding bcrypt, splitting authenticate(), indexing email.
```

### Error Debugging
**Detailed Explanation**:
```
The test is failing because of a timezone mismatch:

File: tests/user_test.py, line 42
Error: AssertionError: expected '2025-11-14 10:00:00' but got '2025-11-14 15:00:00'

Root cause: The test creates a timestamp in UTC but the comparison uses
local time (EST = UTC-5). The test environment runs in UTC while development
machines use local timezones.

Fix: Use timezone-aware datetime objects throughout:
- datetime.now(timezone.utc) instead of datetime.now()
- Store all timestamps in UTC
- Convert to local time only for display

This is documented in our timezone guideline: docs/guidelines.md#timezones

Related issues: #127, #134 (same root cause)
```

**Minimal Output** (for contrast):
```
Timezone mismatch in user_test.py:42. Use timezone.utc.
```

### Architecture Decision
**Detailed Explanation**:
```
Choosing PostgreSQL over SQLite for production:

Current situation:
- SQLite works great for development (<100 users in tests)
- But production has 50K users and growing
- Queries taking 2-3 seconds (profiling in logs/slow-queries.txt)

Why PostgreSQL:
1. Concurrent writes: SQLite locks entire database, PostgreSQL has row-level locking
2. Full-text search: Built-in, no need for separate search engine
3. JSON support: We're storing flexible metadata in user profiles
4. Scalability: Proven to 10M+ rows
5. Team expertise: We already run Postgres for analytics

Alternatives considered:
- MySQL: Less mature JSON support, team less familiar
- MongoDB: Good for JSON but we need relational joins for reports
- Stay with SQLite: Would require significant query optimization and caching layer

Migration approach:
1. Export SQLite to SQL dump
2. Create Postgres schema (automatic via SQLAlchemy)
3. Import data with data type conversions
4. Test queries against production data copy
5. Switch over during low-traffic window (Sunday 2am)
6. Keep SQLite backup for 30 days

Risks and mitigations:
- Risk: Data type incompatibilities → Mitigation: Test migration on prod copy first
- Risk: Connection pool exhaustion → Mitigation: Set max_connections=100, tune pool size
- Risk: Query performance regressions → Mitigation: EXPLAIN ANALYZE all slow queries

Cost: ~$50/month for managed Postgres (Digital Ocean) vs $0 for SQLite
Benefit: 10x faster queries, supports concurrent users, enables full-text search

Decision: Proceed with migration this weekend.
```

**Minimal Output** (for contrast):
```
Migrating to PostgreSQL. SQLite too slow at 50K users.
```

### Feature Implementation
**Detailed Explanation**:
```
Adding rate limiting to the API:

Why: We're seeing abuse from scrapers hitting /api/search 1000x/second,
causing 504 timeouts for legitimate users. Logs show 3 IPs responsible
for 80% of traffic.

Implementation approach:
- Using token bucket algorithm (allows bursts, prevents sustained abuse)
- Redis for distributed counting (we have 3 API servers)
- Limits: 100 requests/minute per IP for authenticated, 10/minute for anonymous
- Returns HTTP 429 with Retry-After header

Why these limits:
- Legitimate users average 5-10 requests/minute
- Allowing 100 gives headroom for legitimate bursts
- Anonymous users need lower limit (higher abuse potential)

Libraries considered:
- django-ratelimit: Too basic, no distributed support
- django-redis-ratelimit: ✓ Chosen - Redis-backed, battle-tested
- custom implementation: Not worth the effort for this common pattern

Configuration:
```python
RATELIMIT_ENABLE = True
RATELIMIT_USE_CACHE = 'default'  # Redis cache
RATELIMIT_VIEW = 'api.views.rate_limited'  # Custom error response

@ratelimit(key='ip', rate='100/m', method='ALL')
def search_api(request):
    # existing code
```

Testing plan:
1. Unit tests: Verify counting, limit enforcement, header values
2. Integration test: Simulate burst traffic, verify 429 responses
3. Load test: 1000 concurrent users, verify no performance regression
4. Monitor: Check Redis memory usage (estimate +50MB for rate limit counters)

Rollout:
- Deploy to staging first, test with QA team
- Monitor error rates and Redis performance
- Enable in production with high limits (1000/min) initially
- Gradually lower to target limits while monitoring

Fallback: If Redis fails, degrade gracefully (no rate limiting) rather than
blocking all traffic. Set RATELIMIT_ENABLE=False remotely if needed.
```

**Minimal Output** (for contrast):
```
Adding rate limiting: 100 req/min authenticated, 10 req/min anonymous.
Using django-redis-ratelimit with token bucket algorithm.
```

## When to Use

### Good For
- Learning environments (students, junior developers)
- Debugging complex issues
- Collaborative projects (multiple stakeholders)
- Onboarding new team members
- Documenting decisions for future reference
- Regulated environments (audit trails)
- Teaching and mentoring
- Research and exploration

### Bad For
- Rapid prototyping (explanation slows iteration)
- Experienced solo developers (know the context)
- High-velocity production fixes (speed matters more)
- Repetitive tasks (explanation becomes noise)
- Time-critical operations (focus over comprehension)

## Quotes

> "If you can't explain it simply, you don't understand it well enough." — Albert Einstein

> "Code comments should explain why, not what." — Robert C. Martin

> "Documentation is a love letter that you write to your future self." — Damian Conway

> "Programs must be written for people to read, and only incidentally for machines to execute." — Harold Abelson

## Related Patterns

- **Literate Programming**: Code and explanation intertwined
- **Self-Documenting Code**: Structure that reveals intent
- **Decision Records**: Architectural decision documentation
- **Explainable AI**: Making ML decisions interpretable
- **Rubber Duck Debugging**: Explaining reveals understanding

## Evolution

This principle doesn't mean "explain everything always." It means:

1. **Know your audience**: Adjust detail level to context
2. **Explain the non-obvious**: Focus on surprising or complex decisions
3. **Layer information**: Summary first, details available
4. **Enable learning**: Help users build mental models
5. **Build trust**: Transparency creates confidence

The right amount of explanation depends on:
- User expertise (junior vs senior)
- Task complexity (simple vs novel)
- Time constraints (urgent vs exploratory)
- Learning goals (teaching vs executing)
- Team dynamics (solo vs collaborative)

Adapt the verbosity to the situation while maintaining transparency.

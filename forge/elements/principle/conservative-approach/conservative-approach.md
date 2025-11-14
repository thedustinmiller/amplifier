# Principle: Conservative Approach

## Core Tenet
Choose proven, boring, reliable solutions. Stability and longevity matter more than being on the cutting edge. Let others absorb the risk of experimentation.

## Motivation

The software graveyard is full of projects built on exciting new technologies that became abandonware. Boring technology has a critical advantage: it works.

**Stability Matters**:
- Production systems need to stay up
- On-call engineers need sleep
- Users need reliability
- Businesses need predictability
- Teams need sustainable pace

**Proven Solutions Scale**:
- Battle-tested under load
- Edge cases already discovered
- Security vulnerabilities patched
- Performance characteristics known
- Troubleshooting resources abundant

**Longevity Pays Off**:
- 10-year-old PostgreSQL skills still valuable
- Mature ecosystems have better tooling
- Hiring is easier for common tech
- Knowledge compounds over time
- Less churn, more depth

Let others beta test. You'll ship while they debug.

## Implications

### Choose Boring
- Prefer mature over new (10+ years ideal)
- Favor widespread adoption over novelty
- Pick technologies with large communities
- Use stable versions, not beta releases
- Trust time-tested patterns

### Avoid Churn
- Minimize technology changes
- Resist framework fads
- Upgrade conservatively
- Deprecation is a feature, not a bug
- Stability > features

### Optimize for Maintenance
- Future you will maintain this
- New team members need to onboard
- Documentation and resources matter
- Debugging unknown tech is expensive
- Operational complexity is risk

### Default to Standards
- SQL over NoSQL (usually)
- REST over GraphQL (usually)
- Monolith over microservices (usually)
- Server-side rendering over SPA (often)
- Standard library over framework

## Trade-offs

### What You Gain
- **Reliability**: Fewer surprises, more uptime
- **Predictability**: Known performance characteristics
- **Resources**: Abundant docs, tutorials, Stack Overflow
- **Hiring**: Easier to find experienced developers
- **Longevity**: Tech stack survives years
- **Sleep**: Fewer 3am debugging sessions

### What You Sacrifice
- **Innovation**: Miss out on cutting-edge capabilities
- **Speed**: Newer tools may be faster
- **Excitement**: Boring can feel... boring
- **Competitive Edge**: May lag innovative competitors
- **Talent**: Some developers prefer new tech
- **Optimal Solutions**: Sometimes new is genuinely better

## Conflicts

### Incompatible Principles
- **experimental-features**: Directly opposed - favors experimental over proven
- **innovation-first**: Prioritizes novelty over stability
- **bleeding-edge**: Embraces risk for early advantage

### Compatible Principles
- **ruthless-minimalism**: Both favor boring, simple solutions
- **stability-first**: Aligned on reliability
- **user-confirmation**: Both reduce risk through caution
- **focused-refinement**: Polish existing rather than explore new

## Examples

### Database Selection
**Conservative Approach**: PostgreSQL
```sql
-- PostgreSQL (since 1996, rock solid)
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  email VARCHAR(255) UNIQUE NOT NULL,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Full-text search, JSON, arrays, CTEs, window functions
-- Battle-tested, well-understood, abundant expertise
```

**Experimental Approach**: Try Turso, SurrealDB, EdgeDB

**Why Conservative Wins**: PostgreSQL will outlive most startups. You'll never get fired for choosing Postgres.

### Web Framework
**Conservative Approach**: Django or Rails
```python
# Django (since 2005)
from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    published = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-published']

# Admin panel, ORM, auth, migrations - all built-in
# 20 years of bug fixes and optimizations
```

**Experimental Approach**: Try Astro, Qwik, Fresh

**Why Conservative Wins**: When you Google an error, the answer exists. The patterns are documented. The sharp edges are smoothed.

### Language Choice
**Conservative Approach**: Python, JavaScript, Java
```python
# Python (since 1991)
def process_data(items):
    """Simple, readable, maintainable."""
    return [
        item.upper()
        for item in items
        if item.startswith('A')
    ]

# Massive ecosystem, any library you need exists
# Hire anywhere in the world
# Will be maintained for decades
```

**Experimental Approach**: Try Gleam, Roc, Zig

**Why Conservative Wins**: Your company will still have Python expertise in 10 years. Guaranteed.

### Deployment Strategy
**Conservative Approach**: VPS or traditional cloud
```bash
# Digital Ocean droplet, traditional deployment
ssh production
cd /var/www/app
git pull
pip install -r requirements.txt
sudo systemctl restart app
sudo systemctl restart nginx

# Boring, debuggable, controllable
# SSH in and fix things
```

**Experimental Approach**: Try Cloudflare Workers, Deno Deploy, edge functions

**Why Conservative Wins**: When something breaks at 2am, you know how to fix it. Standard Linux debugging tools work.

### State Management
**Conservative Approach**: Server-side sessions
```python
# Flask session (server-side, simple)
from flask import session

@app.route('/login', methods=['POST'])
def login():
    user = authenticate(request.form)
    session['user_id'] = user.id  # Server-side storage
    return redirect('/')

# Works, understood, debuggable
# No complex client-side state
```

**Experimental Approach**: Try Zustand, Jotai, Signals, Solid.js reactivity

**Why Conservative Wins**: Server sessions have worked for 30 years. They'll work for 30 more.

### API Design
**Conservative Approach**: RESTful JSON
```python
# REST API (since 2000)
@app.route('/api/posts/<int:post_id>')
def get_post(post_id):
    post = Post.query.get_or_404(post_id)
    return jsonify({
        'id': post.id,
        'title': post.title,
        'author': post.author.name,
        'published': post.published.isoformat()
    })

# Every developer understands REST
# Curl, Postman, any HTTP client works
```

**Experimental Approach**: Try tRPC, GraphQL, gRPC

**Why Conservative Wins**: REST will never go away. It's the common denominator.

## When to Use

### Good For
- **Production systems**: Uptime matters
- **Long-term projects**: 5+ year horizons
- **Team scaling**: Need to hire easily
- **Regulated industries**: Compliance requires stability
- **Critical infrastructure**: Cannot afford downtime
- **Resource-constrained teams**: No bandwidth for troubleshooting new tech

### Bad For
- **Greenfield innovation**: Missing opportunities
- **Competitive markets**: Need every edge
- **Research projects**: Learning is the goal
- **Fast-changing domains**: Old tech may be obsolete
- **Talent attraction**: Top developers want modern tools
- **Genuinely better solutions**: Sometimes new is clearly superior

## Practices

### Technology Selection
1. **Age Test**: Is it 5+ years old?
2. **Adoption Test**: Do major companies use it?
3. **Community Test**: Is Stack Overflow full of answers?
4. **Longevity Test**: Will it exist in 10 years?
5. **Hiring Test**: Can we hire for this easily?

### Upgrade Strategy
- Stay on LTS (Long Term Support) versions
- Skip major versions if possible
- Wait 6 months after major releases
- Read changelogs carefully
- Test upgrades thoroughly
- Keep deprecation warnings clean

### Risk Management
- Avoid version 1.0 of anything
- Wait for battle-testing in production
- Let others find the bugs
- Read postmortems before adopting
- Prefer stable over features

## Anti-Patterns

### Cargo Cult Conservatism
Rejecting all change out of fear.
**Fix**: Evaluate new tech rationally, adopt when proven.

### Technical Debt Denial
"If it ain't broke, don't fix it" taken too far.
**Fix**: Conservative doesn't mean stagnant.

### Resume-Driven Development
Choosing tech for your resume, not the project.
**Fix**: Put project needs first.

### Premature Optimization
Choosing complex "enterprise" solutions too early.
**Fix**: Start simple, scale when needed.

## Quotes

> "Boring technology is not bad technology." — Dan McKinley

> "Choose boring technology." — McKinley (Choose Boring Technology essay)

> "The best technology is the one you already know." — Unknown

> "Nobody ever got fired for choosing PostgreSQL." — Programming wisdom

> "Use what you know, because what you don't know will slow you down." — Pragmatic Programmer

## Related Concepts

- **Lindy Effect** (older = likely to last longer)
- **Choose Boring Technology** (Dan McKinley)
- **Chesterton's Fence** (understand before replacing)
- **Second-Mover Advantage** (let others take the risk)
- **Innovation Tokens** (spend them wisely)

## The Boring Technology Club

Technologies that have proven their worth:

**Languages**: Python, JavaScript, Java, Go, Ruby
**Databases**: PostgreSQL, MySQL, SQLite, Redis
**Frameworks**: Django, Rails, Express, Spring
**Infrastructure**: Linux, nginx, Docker, Kubernetes
**Tools**: Git, Make, Bash, SSH

These are boring because they work.

## When to Break This Rule

Even conservative teams should occasionally adopt new tech when:

1. **Clear Superior Solution**: New tech solves problem dramatically better
2. **Industry Shift**: Old tech being deprecated
3. **Hiring Crisis**: Can't find talent for legacy stack
4. **Competitive Necessity**: Falling behind competitors
5. **Performance Wall**: Old tech can't scale to requirements

Conservative doesn't mean never change—it means change deliberately.

## Measuring Success

- **Uptime**: Are systems reliable?
- **Velocity**: Can we ship features quickly?
- **Hiring**: Can we find developers easily?
- **Incidents**: How often do we wake up at 3am?
- **Onboarding**: How fast do new devs become productive?
- **Longevity**: Is our stack still relevant in 5 years?

Success is shipping and sleeping.

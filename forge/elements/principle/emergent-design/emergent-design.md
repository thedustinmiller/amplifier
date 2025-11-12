# Emergent Design

**Core Tenet**: Design emerges from implementation rather than being fully specified upfront. Architecture evolves as you learn from building.

## Philosophy

Traditional software development often demands comprehensive upfront design. This principle challenges that assumption: **you cannot fully know the right design until you've built something**.

Emergent design embraces uncertainty and learning:
- Start with the simplest design that could work
- Let implementation reveal better structures
- Refactor continuously as patterns emerge
- Trust that good design will emerge from good code

## Core Practices

### 1. Start Simple, Refactor Toward Patterns

Don't predict patterns. Discover them.

**Instead of:**
```python
# Upfront: "We'll need a Strategy pattern for payment processing"
class PaymentStrategy(ABC):
    @abstractmethod
    def process_payment(self, amount: float) -> bool:
        pass

class CreditCardStrategy(PaymentStrategy):
    def process_payment(self, amount: float) -> bool:
        # Implementation
        pass

class PayPalStrategy(PaymentStrategy):
    def process_payment(self, amount: float) -> bool:
        # Implementation
        pass

class PaymentProcessor:
    def __init__(self, strategy: PaymentStrategy):
        self.strategy = strategy

    def process(self, amount: float) -> bool:
        return self.strategy.process_payment(amount)
```

**Start with:**
```python
# Day 1: Just make it work
def process_credit_card(amount: float) -> bool:
    # Charge the card
    return True

# Day 5: Need PayPal, duplicate but ship
def process_paypal(amount: float) -> bool:
    # PayPal integration
    return True

# Day 10: Pattern emerges, now refactor
def process_payment(method: str, amount: float) -> bool:
    if method == "credit_card":
        return process_credit_card(amount)
    elif method == "paypal":
        return process_paypal(amount)

# Day 20: More methods added, Strategy pattern NOW makes sense
# Refactor when the pattern is obvious, not when you predict it might be needed
```

### 2. Refactoring Triggers

Refactor when you see these signals:

**Duplication (Rule of Three)**
- First time: just write it
- Second time: duplicate but notice
- Third time: refactor to eliminate duplication

**Complexity**
- Function > 20 lines? Consider splitting
- Class > 200 lines? Look for cohesive subsets
- Too many parameters? Look for object groupings

**Change Patterns**
- Same files always change together? Maybe they should be one module
- Same reason for changes? Extract a boundary
- Hard to test? Refactor for testability

**Understanding**
- Can't explain it in 30 seconds? Simplify
- Names don't match reality? Rename
- Comments explain "how"? Code should be self-explanatory

### 3. Simplicity Bias

When uncertain, choose simpler:
- One file vs multiple modules → one file
- Plain function vs class → function
- Inline vs abstraction → inline
- Specific vs generic → specific

You can always refactor toward complexity. You rarely refactor toward simplicity.

### 4. Evolutionary Architecture

Design evolves in response to forces:

**Performance pressure** → Caching, optimization
**Scale pressure** → Distribution, partitioning
**Change pressure** → Modularity, abstraction
**Test pressure** → Dependency injection, interfaces

Don't add these preemptively. Add them when pressure is real.

## Examples

### Example 1: Data Storage Evolution

**Day 1: In-memory dictionary**
```python
users = {}  # That's it. Ship it.
```

**Week 2: Need persistence**
```python
import json

def save_users():
    with open('users.json', 'w') as f:
        json.dump(users, f)

def load_users():
    with open('users.json') as f:
        return json.load(f)
```

**Month 2: JSON too slow**
```python
import sqlite3

class UserStore:
    def __init__(self):
        self.db = sqlite3.connect('users.db')

    def get(self, user_id: str):
        # SQLite query
        pass
```

**Month 6: Need real database**
```python
# Now migrate to PostgreSQL with proper ORM
# The evolution taught you what you actually need
```

Each step was the right design **for that moment**. Predicting PostgreSQL on Day 1 would have been premature.

### Example 2: API Evolution

**Version 1: Single endpoint**
```python
@app.post("/process")
def process(data: dict):
    # Do everything in one place
    return {"result": "ok"}
```

**Version 2: Patterns emerge**
```python
@app.post("/users")
def create_user(data: dict): pass

@app.post("/orders")
def create_order(data: dict): pass

# Now you see the pattern → refactor
```

**Version 3: Extract common logic**
```python
class ResourceHandler:
    def create(self, data: dict): pass
    def update(self, id: str, data: dict): pass
    # Pattern is obvious now
```

## When to Use

**Emergent design works best for:**
- ✅ Greenfield projects (learn as you build)
- ✅ Uncertain requirements (design follows reality)
- ✅ Rapid prototypes (don't over-design)
- ✅ Small teams (easy to refactor)
- ✅ Explorative work (design space is unknown)

## When NOT to Use

**Avoid emergent design when:**
- ❌ Safety-critical systems (need upfront verification)
- ❌ Fixed architecture contracts (client expects specific design)
- ❌ Large distributed teams (need coordination through design)
- ❌ Highly regulated domains (design must be documented/approved)
- ❌ Known domain with proven patterns (don't rediscover the wheel)

## Trade-offs

**Benefits:**
- Lower initial complexity
- Design matches actual needs
- Learn from implementation
- Easier to change early
- Less upfront time

**Costs:**
- May need refactoring (plan for it)
- Can accumulate technical debt (address continuously)
- Requires discipline (know when to refactor)
- Team must embrace change
- Less predictable timeline

## Integration with Other Principles

**Pairs well with:**
- **ruthless-minimalism**: Start simple, refactor when needed
- **coevolution**: Let implementation teach you the design
- **analysis-first**: Quick analysis informs starting point

**Tension with:**
- **specification-driven**: Specs often imply fixed design
- **formal-verification**: Needs stable design to verify

## Anti-patterns

**1. Never Refactoring**
Emergent design ≠ no design. Refactor when patterns emerge.

**2. Over-refactoring**
Don't refactor on speculation. Refactor on evidence (duplication, complexity).

**3. Ignoring Performance**
Emergent design doesn't mean ignore scale. Monitor and refactor when pressure is real.

**4. No Tests**
Refactoring requires tests. Emergent design without tests = technical debt accumulation.

## Metrics

**Health indicators:**
- Regular refactoring commits (weekly)
- Decreasing complexity over time
- High test coverage (enables refactoring)
- Short feedback cycles (< 1 day)

**Warning signs:**
- No refactoring in weeks (debt building)
- Increasing complexity metrics
- Fear of changing code
- "We can't touch that module"

## Summary

Emergent design is about **learning from building** rather than predicting the future.

Start simple. Let patterns emerge. Refactor continuously. Trust the process.

The best design is the one that emerges from real code solving real problems.

---

**Related Elements:**
- `ruthless-minimalism` - Provides starting simplicity
- `coevolution` - Specs and code inform design together
- `analysis-first` - Quick upfront thinking guides starting point

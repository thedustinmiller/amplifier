# Principle: Code as Documentation

## Core Tenet
Code should be so clear that separate documentation is unnecessary. Invest in readable, self-explanatory code rather than maintaining external docs that drift from reality.

## Motivation

Documentation lies. Not intentionally—it just falls out of sync. Code is the only source of truth that's guaranteed to reflect reality:

**The Documentation Problem**:
- Docs get stale when code changes
- Maintaining both code and docs doubles work
- Inconsistency between code and docs breeds confusion
- Comments describe what code should do, not what it does
- Documentation is a form of duplication

**Code as Truth**:
- Code always reflects current behavior
- Tests document expected behavior
- Types document contracts
- Names document purpose
- Structure documents architecture

**Quality Investment**:
- Time spent on clear code compounds
- Refactoring improves understanding
- Good names eliminate comments
- Clear structure beats diagrams
- Expressive code reads like prose

If you need comments to explain code, improve the code instead.

## Implications

### Write for Readers
- Choose meaningful names
- Keep functions small and focused
- Make intent explicit
- Avoid clever tricks
- Structure reveals purpose

### Let Code Speak
- Variable names explain what
- Function names explain why
- Type signatures explain contracts
- Tests explain behavior
- Structure explains relationships

### Refactor Relentlessly
- Extract methods for clarity
- Rename for precision
- Simplify complex logic
- Remove dead code
- Consolidate duplication

### Minimal Comments
- Comment WHY when non-obvious
- Never comment WHAT (code shows that)
- Delete outdated comments
- Prefer code changes over comments
- Comments are code smell

## Trade-offs

### What You Gain
- **Accuracy**: Code never lies about behavior
- **Velocity**: No separate docs to maintain
- **Refactoring**: Code changes don't require doc updates
- **Trust**: Single source of truth
- **Quality**: Forces better code design
- **Simplicity**: Less to maintain

### What You Sacrifice
- **Context**: Historical decisions not preserved
- **Onboarding**: Steeper learning curve initially
- **Architecture**: High-level view harder
- **Domain Knowledge**: Business rules less explicit
- **Why vs What**: Rationale not captured
- **Non-Technical Audience**: Code intimidates non-coders

## Conflicts

### Incompatible Principles
- **comprehensive-documentation**: Directly opposed - values extensive docs
- **documentation-first**: Requires docs before code
- **spec-driven**: Heavy upfront documentation

### Compatible Principles
- **ruthless-minimalism**: Both minimize artifacts
- **emergent-design**: Let structure emerge from code
- **refactoring-culture**: Continuous code improvement
- **test-driven**: Tests as living documentation

## Examples

### Self-Documenting Names
**Code as Documentation**:
```python
# Good - names explain everything
def calculate_total_price_with_tax(
    items: list[LineItem],
    tax_rate: Decimal,
    shipping_cost: Decimal
) -> Decimal:
    subtotal = sum(item.price * item.quantity for item in items)
    tax = subtotal * tax_rate
    return subtotal + tax + shipping_cost

# Usage is obvious
total = calculate_total_price_with_tax(
    items=cart.items,
    tax_rate=Decimal("0.0875"),  # 8.75%
    shipping_cost=Decimal("5.99")
)
```

**Requires Documentation**:
```python
# Bad - needs comments
def calc(items, rate, ship):
    """Calculate total.

    Args:
        items: List of items
        rate: Tax rate
        ship: Shipping cost

    Returns:
        Total price
    """
    st = sum(i.p * i.q for i in items)
    t = st * rate
    return st + t + ship
```

**Why Code-as-Doc Wins**: First version needs no comments. Names are documentation.

### Small, Focused Functions
**Code as Documentation**:
```typescript
// Each function documents its purpose
function processOrder(order: Order): ProcessedOrder {
  validateOrderItems(order.items);
  const inventory = reserveInventory(order.items);
  const payment = processPayment(order.paymentMethod, order.total);
  const shipment = createShipment(order.shippingAddress, inventory);
  const confirmation = sendConfirmationEmail(order.customer, payment, shipment);

  return {
    orderId: order.id,
    payment,
    shipment,
    confirmation
  };
}

// Each step is obvious
// No comments needed
// Easy to test each piece
// Structure shows workflow
```

**Requires Documentation**:
```typescript
// Bad - complex function needs explanation
function processOrder(order: Order): ProcessedOrder {
  // Check if all items are in stock and valid
  for (const item of order.items) {
    if (!item.sku || item.quantity <= 0) {
      throw new Error("Invalid item");
    }
    const stock = inventory.get(item.sku);
    if (!stock || stock < item.quantity) {
      throw new Error("Insufficient stock");
    }
  }

  // Reserve inventory and process payment...
  // (100 more lines of intertwined logic)
}
```

**Why Code-as-Doc Wins**: Small functions are self-explanatory. No mental load.

### Type Systems as Documentation
**Code as Documentation**:
```typescript
// Types document the contract
type OrderStatus =
  | 'draft'
  | 'pending_payment'
  | 'processing'
  | 'shipped'
  | 'delivered'
  | 'cancelled';

interface Order {
  id: string;
  customer: Customer;
  items: LineItem[];
  status: OrderStatus;
  createdAt: Date;
  total: Money;
}

function shipOrder(order: Order): ShippedOrder {
  // Compiler enforces: only valid order states
  // Return type documents what you get back
  // Types never lie
}

// Usage is type-safe and obvious
const shipped = shipOrder(order);
// shipped.trackingNumber available (type says so)
```

**Requires Documentation**:
```javascript
// Bad - needs documentation
function shipOrder(order) {
  // order: Object with id, customer, items, status, createdAt, total
  // returns: Object with trackingNumber and estimatedDelivery
  // throws: Error if order is not in 'processing' state
}
```

**Why Code-as-Doc Wins**: Types are documentation that the compiler validates.

### Tests as Documentation
**Code as Documentation**:
```python
# Tests document behavior
class TestOrderProcessing:
    def test_successful_order_creates_shipment(self):
        # Arrange: Given valid order
        order = create_test_order(
            items=[LineItem(sku="WIDGET", quantity=2, price=10)],
            payment_method=valid_credit_card()
        )

        # Act: When processing order
        result = process_order(order)

        # Assert: Then shipment is created
        assert result.shipment is not None
        assert result.shipment.tracking_number is not None
        assert result.shipment.status == ShipmentStatus.PENDING

    def test_insufficient_inventory_prevents_order(self):
        # Given order with out-of-stock item
        order = create_test_order(
            items=[LineItem(sku="RARE", quantity=100, price=10)]
        )

        # When processing order
        # Then raises insufficient inventory error
        with pytest.raises(InsufficientInventoryError):
            process_order(order)

    def test_failed_payment_releases_inventory(self):
        # Test documents rollback behavior
        # ...

# Test names document requirements
# Test bodies document examples
# No separate specification needed
```

**Requires Documentation**:
```
Separate spec document describing all edge cases
```

**Why Code-as-Doc Wins**: Tests are executable documentation. Always up to date.

### Domain-Driven Design
**Code as Documentation**:
```python
# Domain model documents business rules
class Order:
    def __init__(self, customer: Customer, items: list[LineItem]):
        if not items:
            raise EmptyOrderError("Order must have at least one item")

        self.customer = customer
        self.items = items
        self.status = OrderStatus.DRAFT
        self.created_at = datetime.now()

    def submit_for_payment(self) -> PendingPaymentOrder:
        """Transition from draft to pending payment."""
        if self.status != OrderStatus.DRAFT:
            raise InvalidStateTransition(
                f"Cannot submit order in {self.status} state"
            )

        self._reserve_inventory()
        return PendingPaymentOrder(self)

    def cancel(self) -> CancelledOrder:
        """Cancel order and release resources."""
        if self.status in [OrderStatus.SHIPPED, OrderStatus.DELIVERED]:
            raise InvalidStateTransition(
                f"Cannot cancel {self.status} order. Use return process."
            )

        self._release_inventory()
        self._refund_payment()
        return CancelledOrder(self, reason=CancellationReason.USER_REQUESTED)

# Business rules enforced in code
# State transitions explicit
# Errors document invalid operations
```

**Requires Documentation**:
```
Separate state machine diagram and business rules document
```

**Why Code-as-Doc Wins**: Code enforces rules. Can't get out of sync with reality.

### Fluent Interfaces
**Code as Documentation**:
```java
// API that reads like English
Order order = new OrderBuilder()
    .forCustomer(customer)
    .addItem("WIDGET", quantity: 2)
    .addItem("GADGET", quantity: 1)
    .withShipping(expedited: true)
    .withDiscount("SAVE10")
    .build();

// Usage is self-documenting
// No manual needed
```

**Requires Documentation**:
```java
// Bad - needs explanation
Order order = new Order(
    customer,
    Arrays.asList(new Item("WIDGET", 2), new Item("GADGET", 1)),
    true,
    "SAVE10"
);
// What does 'true' mean? Need docs.
```

**Why Code-as-Doc Wins**: Reads like a sentence. Self-explanatory.

### Directory Structure as Architecture
**Code as Documentation**:
```
src/
  domain/          # Business logic (no dependencies)
    models/
    services/
    repositories/  # Interfaces only

  infrastructure/  # External dependencies
    database/
    email/
    payment/

  application/     # Use cases
    orders/
    users/
    inventory/

  presentation/    # UI layer
    api/
    web/
    cli/

# Structure documents clean architecture
# Dependencies flow inward
# No comments needed to explain layering
```

**Requires Documentation**:
```
src/
  stuff/
  things/
  utils/
  helpers/

# Needs architecture doc to explain organization
```

**Why Code-as-Doc Wins**: Structure reveals intent. Onboarding through exploration.

## When to Use

### Good For
- **Small teams**: Code review is communication
- **Experienced developers**: Can read code effectively
- **Fast-moving projects**: Docs would be stale anyway
- **Clear domains**: Business logic is straightforward
- **Modern languages**: Strong type systems help
- **Good testing culture**: Tests document behavior

### Bad For
- **Complex domains**: Business rules need extensive explanation
- **Large teams**: Onboarding burden too high
- **Regulated industries**: Audit trail required
- **Non-technical stakeholders**: Need readable specs
- **Legacy systems**: Historical context matters
- **Distributed teams**: Async communication needs docs

## Practices

### Naming Conventions
- **Variables**: Describe what they hold (`totalPrice`, not `tp`)
- **Functions**: Describe what they do (`calculateTax`, not `calc`)
- **Classes**: Describe what they represent (`ShoppingCart`, not `SC`)
- **Booleans**: Ask questions (`isValid`, `hasShipped`, `canCancel`)

### Function Design
- **Single Responsibility**: One thing, well-named
- **Small**: 10-20 lines max
- **Few Parameters**: 3 or fewer (use objects if more)
- **Pure When Possible**: Same input → same output
- **Obvious**: Intent clear from name and signature

### Comment Guidelines
Only comment when:
- Explaining non-obvious algorithms
- Documenting workarounds for third-party bugs
- Clarifying business rules from domain experts
- Linking to external resources (RFCs, tickets)

Never comment:
- What the code does (name it better)
- Obvious operations
- Dead code (delete it instead)
- Historical changes (use git)

### Refactoring Habits
- Extract method when logic is complex
- Rename when better name found
- Inline when abstraction adds no value
- Delete unused code immediately
- Simplify conditionals

## Anti-Patterns

### Comment-Driven Development
Writing comments instead of fixing unclear code.
**Fix**: Rename, extract, simplify.

### Clever Code
Writing terse, clever code that needs explanation.
**Fix**: Write obvious code.

### Comment Noise
```python
# Bad: Comments that add no value
# Increment counter
counter += 1

# Loop through items
for item in items:
    # Process the item
    process(item)
```
**Fix**: Delete obvious comments.

### Orphaned Comments
Comments that became outdated.
**Fix**: Delete or update during code changes.

## Quotes

> "Code never lies, comments sometimes do." — Ron Jeffries

> "Clean code is simple and direct. Clean code reads like well-written prose." — Grady Booch

> "Indeed, the ratio of time spent reading versus writing is well over 10 to 1. We are constantly reading old code as part of the effort to write new code." — Robert C. Martin

> "Any fool can write code that a computer can understand. Good programmers write code that humans can understand." — Martin Fowler

> "Programs must be written for people to read, and only incidentally for machines to execute." — Harold Abelson

## Related Concepts

- **Clean Code** (Robert C. Martin)
- **Self-Documenting Code**
- **Domain-Driven Design** (Eric Evans)
- **Test-Driven Development**
- **Refactoring** (Martin Fowler)
- **SOLID Principles**

## Code Smells That Need Documentation

If you need extensive comments to explain:
- **Complex conditionals** → Extract to well-named function
- **Magic numbers** → Named constants
- **Unclear variable names** → Better names
- **Long functions** → Extract smaller functions
- **Deep nesting** → Guard clauses, early returns
- **Obscure algorithms** → Maybe okay to comment, or extract

Comment is a code smell. Refactor instead.

## When Comments Are Acceptable

**Algorithm Explanation**:
```python
# Binary search implementation (O(log n))
# See: https://en.wikipedia.org/wiki/Binary_search_algorithm
def binary_search(arr: list[int], target: int) -> int:
    # ...
```

**Business Rule Citation**:
```python
# Per tax code §1234.5, charitable contributions
# are deductible up to 60% of adjusted gross income
def calculate_deduction(agi: Decimal, donation: Decimal) -> Decimal:
    # ...
```

**Workaround Documentation**:
```python
# Workaround for SQLAlchemy bug #5678
# Remove when upgrading to version 2.0
session.expire_on_commit = False
```

**TODO with Context**:
```python
# TODO(alice): Migrate to new API when available (Q2 2025)
# Current API deprecated: https://api.example.com/v1/docs
```

## Evolution

Even code-as-documentation projects evolve:

**Phase 1**: Pure code (small, simple)
**Phase 2**: Add README (setup, overview)
**Phase 3**: Add API docs (public interfaces)
**Phase 4**: Add architecture decision records (major choices)
**Phase 5**: Maybe add more docs (if complexity demands)

Start minimal. Add docs only when code alone isn't sufficient.

## Success Metrics

- **Code Review Time**: How fast do reviewers understand code?
- **Bug Rate**: Clear code → fewer bugs
- **Onboarding Speed**: Can new devs read and contribute?
- **Refactoring Frequency**: Is code easy to change?
- **Test Coverage**: Do tests document behavior?
- **Comment Ratio**: Lines of comments / lines of code (lower is better)

Success is code that explains itself.

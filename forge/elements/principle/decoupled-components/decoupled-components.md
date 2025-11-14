# Principle: Decoupled Components

## Core Tenet
Build independent, composable components that communicate through well-defined interfaces. Optimize for autonomy, replaceability, and independent evolution.

## Motivation

Systems grow in complexity and scale. Decoupling enables evolution without coordination overhead:

**Independence Advantages**:
- Components evolve at different rates
- Teams work autonomously
- Scale components independently
- Replace without rewriting entire system
- Technology choices per component

**Resilience Benefits**:
- Failure isolation (one component down ≠ system down)
- Independent deployment reduces risk
- Gradual rollouts component by component
- A/B testing at component level
- Rollback individual pieces

**Organizational Scaling**:
- Teams own components end-to-end
- Clear ownership boundaries
- Parallel development
- Reduced coordination overhead
- Conway's Law works for you

Loose coupling is not a cost—it's an investment in future flexibility.

## Implications

### Design for Independence
- Separate databases per component
- API-based communication
- Async messaging over direct calls
- Event-driven architecture
- No shared state

### Enforce Boundaries
- Versioned interfaces
- Contract testing
- API gateways
- Service mesh
- Clear ownership

### Enable Composition
- Small, focused services
- Well-defined responsibilities
- Pluggable architecture
- Standard protocols
- Interchangeable components

### Accept Complexity
- Distributed systems challenges
- Network unreliability
- Eventual consistency
- Monitoring across services
- Distributed debugging

## Trade-offs

### What You Gain
- **Autonomy**: Teams work independently
- **Scalability**: Scale components separately
- **Resilience**: Failures isolated
- **Technology Freedom**: Choose best tool per component
- **Replaceability**: Swap components without rewrite
- **Team Scaling**: Parallel development

### What You Sacrifice
- **Performance**: Network calls vs. function calls
- **Consistency**: Eventual rather than immediate
- **Simplicity**: Distributed systems are complex
- **Debugging**: Spans multiple services
- **Transactions**: No global ACID
- **Operations**: More moving parts

## Conflicts

### Incompatible Principles
- **integrated-solutions**: Directly opposed - favors integration over separation
- **monolith-first**: Prioritizes cohesion over modularity
- **simplicity-above-all**: Distributed systems are inherently complex

### Compatible Principles
- **autonomous-execution**: Both value independence
- **wide-search**: Exploring different solutions per component
- **experimental-features**: Freedom to experiment per component
- **team-autonomy**: Clear ownership enables independence

## Examples

### Microservices Architecture
**Decoupled Approach**: Independent services
```yaml
# docker-compose.yml - separate services
services:
  user-service:
    image: user-service:latest
    environment:
      - DATABASE_URL=postgres://users-db:5432/users
    depends_on: [users-db]

  order-service:
    image: order-service:latest
    environment:
      - DATABASE_URL=postgres://orders-db:5432/orders
      - USER_SERVICE_URL=http://user-service:3000
    depends_on: [orders-db]

  inventory-service:
    image: inventory-service:latest
    environment:
      - DATABASE_URL=postgres://inventory-db:5432/inventory
    depends_on: [inventory-db]

  # Each service: separate DB, separate deploy, independent scaling
```

**Communication via APIs**:
```python
# order-service calls user-service via API
async def create_order(user_id, items):
    # Call user service to verify user
    user = await http.get(f"{USER_SERVICE_URL}/users/{user_id}")

    # Call inventory service to reserve items
    reservation = await http.post(
        f"{INVENTORY_SERVICE_URL}/reservations",
        json={"items": items}
    )

    # Create order in local database
    order = await db.orders.create({
        "user_id": user_id,
        "items": items,
        "reservation_id": reservation["id"]
    })

    # Publish event for other services
    await events.publish("order.created", order)

    return order

# No shared database, no shared state
# Each service owns its data
```

**Integrated Approach**: Single monolith with shared database

**Why Decoupling Wins**: Scale inventory service independently during peak load. Update user service without touching orders. Different teams own different services.

### Plugin Architecture
**Decoupled Approach**: VSCode extensions
```typescript
// Extension API - well-defined contract
import * as vscode from 'vscode';

export function activate(context: vscode.ExtensionContext) {
    // Extension communicates via stable API
    let disposable = vscode.commands.registerCommand(
        'myextension.doSomething',
        () => {
            vscode.window.showInformationMessage('Hello!');
        }
    );

    context.subscriptions.push(disposable);
}

// VSCode doesn't know about this extension
// Extension doesn't know VSCode internals
// Versioned API, backward compatible
// Can install/uninstall without restarting
```

**Integrated Approach**: Features built directly into IDE

**Why Decoupling Wins**: Thousands of extensions, community-driven, install what you need, third-party innovation.

### Event-Driven System
**Decoupled Approach**: Event bus
```python
# Publisher doesn't know about subscribers
class OrderService:
    async def create_order(self, order_data):
        order = await self.db.create(order_data)

        # Publish event - don't care who listens
        await events.publish('order.created', {
            'order_id': order.id,
            'user_id': order.user_id,
            'total': order.total
        })

        return order

# Subscribers don't know about publisher
class EmailService:
    async def on_order_created(self, event):
        await self.send_confirmation(event['user_id'], event['order_id'])

class AnalyticsService:
    async def on_order_created(self, event):
        await self.track_conversion(event['total'])

class InventoryService:
    async def on_order_created(self, event):
        await self.update_stock(event['order_id'])

# Add new subscribers without touching publisher
# Temporal decoupling - can be async
```

**Integrated Approach**: Direct function calls between modules

**Why Decoupling Wins**: Add new features (analytics, warehousing, fraud detection) without modifying order service.

### Frontend Microfrontends
**Decoupled Approach**: Module federation
```javascript
// webpack.config.js - Host application
module.exports = {
  plugins: [
    new ModuleFederationPlugin({
      name: 'host',
      remotes: {
        productCatalog: 'productCatalog@http://localhost:3001/remoteEntry.js',
        shoppingCart: 'shoppingCart@http://localhost:3002/remoteEntry.js',
        userProfile: 'userProfile@http://localhost:3003/remoteEntry.js',
      },
    }),
  ],
};

// App.jsx - Compose independent frontends
import React, { lazy, Suspense } from 'react';

const ProductCatalog = lazy(() => import('productCatalog/Catalog'));
const ShoppingCart = lazy(() => import('shoppingCart/Cart'));
const UserProfile = lazy(() => import('userProfile/Profile'));

function App() {
  return (
    <div>
      <Suspense fallback="Loading...">
        <UserProfile />
        <ProductCatalog />
        <ShoppingCart />
      </Suspense>
    </div>
  );
}

// Each microfrontend: separate repo, separate deploy, independent teams
```

**Integrated Approach**: Single SPA with all features

**Why Decoupling Wins**: Different teams ship different features independently. Catalog team can use Vue, Cart team uses React.

### Database per Service
**Decoupled Approach**: Separate databases
```python
# user-service
class UserService:
    def __init__(self):
        self.db = connect('postgres://users-db/users')

    def get_user(self, user_id):
        return self.db.query('SELECT * FROM users WHERE id = ?', user_id)

# order-service
class OrderService:
    def __init__(self):
        self.db = connect('postgres://orders-db/orders')
        self.user_client = UserServiceClient()

    async def get_order_with_user(self, order_id):
        order = self.db.query('SELECT * FROM orders WHERE id = ?', order_id)
        # Call user service via API
        user = await self.user_client.get_user(order.user_id)
        return {'order': order, 'user': user}

# Each service owns its data
# No shared tables
# Communication via APIs
```

**Integrated Approach**: Shared database with joins

**Why Decoupling Wins**: Scale databases independently. Use different databases (Postgres for users, MongoDB for orders). Migrate one without affecting others.

### API Gateway Pattern
**Decoupled Approach**: Gateway routes to services
```yaml
# API Gateway configuration
routes:
  - path: /users/*
    service: user-service
    methods: [GET, POST, PUT, DELETE]

  - path: /orders/*
    service: order-service
    methods: [GET, POST]
    rate_limit: 100/minute

  - path: /inventory/*
    service: inventory-service
    methods: [GET, POST]
    auth: required

  - path: /analytics/*
    service: analytics-service
    methods: [GET]
    cache: 5m

# Gateway handles: routing, auth, rate limiting, caching
# Services focus on business logic
# Can swap service implementations
```

**Integrated Approach**: Single application handles all routes

**Why Decoupling Wins**: Replace analytics service without touching others. Add authentication at gateway level. Scale services independently.

## When to Use

### Good For
- **Large teams**: Multiple teams need autonomy
- **Different scaling needs**: Some components need more resources
- **Independent evolution**: Features change at different rates
- **Technology diversity**: Different tools for different problems
- **Third-party integration**: External systems must plug in
- **High availability**: Failure isolation critical

### Bad For
- **Small teams**: Coordination overhead low, decoupling overhead high
- **Simple applications**: Distributed complexity not worth it
- **Tight coupling inherent**: Features deeply interconnected
- **Resource constrained**: Limited ops capacity
- **Performance critical**: Network latency matters
- **ACID requirements**: Need transactional consistency

## Practices

### Define Clear Contracts
- API versioning (v1, v2)
- OpenAPI/GraphQL schemas
- Contract testing
- Backward compatibility
- Deprecation policies

### Manage Dependencies
- Service discovery
- Circuit breakers
- Retry policies
- Timeout handling
- Graceful degradation

### Monitor Distributed System
- Distributed tracing
- Correlation IDs
- Centralized logging
- Service mesh
- Health checks

### Handle Failure
- Bulkheads (isolation)
- Fallbacks
- Idempotency
- Eventual consistency
- Compensating transactions

## Anti-Patterns

### Distributed Monolith
Microservices that all depend on each other.
**Fix**: Clear boundaries, minimize inter-service calls.

### Chatty Services
Too many network calls for simple operations.
**Fix**: Batch operations, aggregate services, consider boundaries.

### Shared Database
Microservices sharing same database.
**Fix**: Database per service, API communication.

### No Versioning
Breaking API changes without versioning.
**Fix**: Semantic versioning, backward compatibility.

## Quotes

> "The best writing is rewriting." — E.B. White (applies to refactoring toward modularity)

> "Services should be loosely coupled and highly cohesive." — Sam Newman

> "You must be able to deploy each service independently." — Martin Fowler

> "Microservices are not a free lunch. You pay in operational complexity." — Martin Fowler

> "Make each program do one thing well." — Unix Philosophy

## Related Concepts

- **Microservices Architecture**
- **Service-Oriented Architecture (SOA)**
- **Plugin Systems**
- **Event-Driven Architecture**
- **Domain-Driven Design (Bounded Contexts)**
- **Unix Philosophy**

## Implementation Patterns

### Communication Patterns
- **Synchronous**: REST, GraphQL, gRPC
- **Asynchronous**: Message queues, event streams
- **Hybrid**: Command Query Responsibility Segregation (CQRS)

### Data Patterns
- **Database per Service**: Own your data
- **Event Sourcing**: Log of changes
- **Saga Pattern**: Distributed transactions
- **API Composition**: Join data via APIs

### Deployment Patterns
- **Containerization**: Docker, Kubernetes
- **Service Mesh**: Istio, Linkerd
- **API Gateway**: Kong, Traefik
- **Observability**: Prometheus, Jaeger

## Evolution Path

Progressive decoupling:

1. **Monolith**: Start simple
2. **Modular Monolith**: Clear internal boundaries
3. **Extract Critical Services**: Pull out what must scale
4. **Selective Decomposition**: Strategic microservices
5. **Full Decoupling**: When organization demands it

Don't start with microservices—earn them.

## Success Metrics

- **Deploy Independence**: Can we deploy without coordination?
- **Team Velocity**: Are teams moving faster?
- **Failure Isolation**: Do failures cascade?
- **Scaling Efficiency**: Can we scale components independently?
- **Time to Market**: Are we shipping faster?
- **Operational Complexity**: Is it manageable?

Success is autonomy without chaos.

# Common Workflows

Practical workflows for using Forge in real-world development scenarios.

## Table of Contents

- [Getting Started Workflows](#getting-started-workflows)
- [Development Workflows](#development-workflows)
- [Team Workflows](#team-workflows)
- [Maintenance Workflows](#maintenance-workflows)
- [Advanced Workflows](#advanced-workflows)

---

## Getting Started Workflows

### Workflow 1: Create Your First Project

**Goal:** Set up a new Forge project from scratch.

**Duration:** 5 minutes

**Steps:**

```bash
# 1. Run the wizard
forge init

# 2. Follow prompts
# - Project name: my-app
# - Principles: ruthless-minimalism, coevolution
# - Memory provider: file
# - Storage path: .forge/memory

# 3. Navigate to project
cd my-app

# 4. Review composition
cat .forge/composition.yaml

# 5. Generate Claude Code integration
forge generate claude-code

# 6. Validate
forge validate claude-code
```

**Result:**
- Project structure created
- Composition configured
- Claude Code integration ready
- Ready to start developing

---

### Workflow 2: Start from Example Composition

**Goal:** Use a pre-built composition as starting point.

**Duration:** 3 minutes

**Steps:**

```bash
# 1. Create project directory
mkdir my-rapid-prototype && cd my-rapid-prototype

# 2. Create .forge directory
mkdir -p .forge

# 3. Copy example composition
cp /path/to/forge/examples/rapid-prototype.yaml .forge/composition.yaml

# 4. Review and customize
nano .forge/composition.yaml

# 5. Generate integration
forge generate claude-code

# 6. Start coding
```

**Result:**
- Quick setup with proven composition
- Customizable foundation
- Ready for rapid prototyping

---

## Development Workflows

### Workflow 3: Rapid Prototyping

**Goal:** Ship working code fast, iterate based on feedback.

**Composition:**

```yaml
elements:
  principles:
    - ruthless-minimalism
    - coevolution
  tools:
    - scaffold
  agents:
    - zen-architect
```

**Development Cycle:**

```bash
# 1. Start with rough spec
echo "Build a REST API for todo items" > spec.md

# 2. Generate Claude Code files
forge generate claude-code

# 3. Open in Claude Code and ask:
# "Scaffold a minimal REST API for todo items following ruthless-minimalism"

# 4. Claude generates minimal implementation
# - Simple SQLite database
# - Basic CRUD endpoints
# - No authentication (defer until needed)
# - Plain JSON responses (no fancy formatting)

# 5. Test immediately
python app.py

# 6. Discover gaps
# "Authentication needed for production"

# 7. Update spec
echo "- [ ] Add authentication when deployed" >> spec.md

# 8. Keep iterating
```

**Memory Usage:**

```bash
# Store decisions in memory
# Claude can write to memory via composition

# Example memory entries:
# decision:database = "Using SQLite until 10K users"
# decision:auth = "Deferring until first production user"
# learning:minimal-api = "3 endpoints sufficient for v1"
```

**Outcome:**
- Working prototype in hours, not days
- Clear decisions tracked
- Easy to iterate and adapt

---

### Workflow 4: Test-Driven Development

**Goal:** Ensure quality through comprehensive testing.

**Composition:**

```yaml
elements:
  principles:
    - test-first
    - coevolution
  tools:
    - test-runner
    - coverage-check
  templates:
    - test-template
```

**Development Cycle:**

```bash
# 1. Write spec with test criteria
cat > spec.md <<EOF
# Feature: User Authentication

## Requirements
- Users can register with email/password
- Passwords must be hashed
- Login returns JWT token

## Test Criteria
- Registration creates user in database
- Duplicate emails rejected
- Invalid passwords rejected
- Login with valid credentials succeeds
- Login with invalid credentials fails
EOF

# 2. Generate integration
forge generate claude-code

# 3. Open in Claude Code
# "Write tests first for user authentication feature"

# 4. Claude generates test suite
# Following test-first principle

# 5. Run tests (all failing)
pytest tests/test_auth.py

# 6. Implement to pass tests
# "Implement authentication to pass these tests"

# 7. Run tests until green
pytest tests/test_auth.py

# 8. Check coverage
pytest --cov=app tests/

# 9. Refine spec based on implementation
# Update spec.md with discovered edge cases
```

**Outcome:**
- High confidence in correctness
- Comprehensive test coverage
- Specs stay aligned with reality

---

### Workflow 5: Specification-Driven Development

**Goal:** Align team around detailed specifications.

**Composition:**

```yaml
elements:
  principles:
    - spec-driven
    - coevolution
  templates:
    - spec-template
    - decision-log
  tools:
    - doc-generator
```

**Development Cycle:**

```bash
# 1. Write detailed spec
cat > specs/payment-system.md <<EOF
# Payment System Specification

## Overview
Process credit card payments for orders.

## Requirements
1. Accept Visa, Mastercard, Amex
2. Validate card numbers
3. Handle declined transactions
4. Store transaction history
5. Comply with PCI-DSS

## API Design
POST /payments
{
  "order_id": "...",
  "card": {...},
  "amount": 99.99
}

## Error Handling
- Invalid card: 400 Bad Request
- Declined: 402 Payment Required
- Server error: 500 Internal Server Error

## Security
- Use Stripe API (PCI compliant)
- Never store full card numbers
- Use HTTPS only
EOF

# 2. Generate integration
forge generate claude-code

# 3. Have Claude review spec
# "Review this payment spec for gaps and issues"

# 4. Claude identifies issues
# - Missing: Refund handling
# - Missing: Webhook for async processing
# - Security: Add rate limiting

# 5. Update spec
nano specs/payment-system.md

# 6. Implement against refined spec
# "Implement payment system according to spec"

# 7. Discover implementation insights
# "Stripe webhooks require special handling"

# 8. Update spec with learnings
echo "## Webhooks..." >> specs/payment-system.md

# 9. Keep spec and code in sync
```

**Outcome:**
- Team alignment on requirements
- Fewer surprises during implementation
- Living documentation that evolves

---

### Workflow 6: Coevolution in Practice

**Goal:** Let specs and code inform each other naturally.

**Composition:**

```yaml
elements:
  principles:
    - coevolution
    - ruthless-minimalism
  templates:
    - spec-template
    - plan-template
```

**Coevolution Cycle:**

```bash
# Iteration 1: Sketch and Prototype

# 1. Rough spec (5 minutes)
cat > spec.md <<EOF
# File Upload Feature
Users can upload images.
Max size: 5MB
Formats: JPG, PNG
EOF

# 2. Quick implementation (30 minutes)
# "Build simple file upload based on spec"

# 3. Discover constraints
# - Need to validate file types
# - Need to handle large files
# - Need to prevent malicious uploads

# Iteration 2: Refine Based on Reality

# 4. Update spec with discoveries
cat >> spec.md <<EOF

## Technical Details
- Validate file signature (not just extension)
- Stream large files to prevent memory issues
- Scan for malware before storage
- Generate thumbnails asynchronously
EOF

# 5. Improve implementation
# "Add file validation and streaming"

# 6. Discover more requirements
# - Users want progress indication
# - Need resumable uploads for slow connections

# Iteration 3: Converge

# 7. Final spec update
cat >> spec.md <<EOF

## User Experience
- Show upload progress
- Support resume after disconnect
- Display thumbnail immediately
EOF

# 8. Final implementation
# "Add upload progress and resume support"

# 9. Spec and code now coherent
# Both reflect reality, inform future changes
```

**Memory Tracking:**

```bash
# Store the evolution
# decision:file-validation = "Using file signature, not extension"
# learning:streaming = "Streaming essential for files > 1MB"
# decision:thumbnails = "Async generation to avoid blocking"
```

**Outcome:**
- Spec reflects reality, not fantasy
- Implementation informed by real constraints
- Continuous improvement loop

---

## Team Workflows

### Workflow 7: Onboarding New Team Member

**Goal:** Get new developer productive quickly.

**Steps:**

```bash
# 1. Clone project
git clone https://github.com/team/project.git
cd project

# 2. Install Forge
cd forge
uv pip install -e .
cd ../project

# 3. Review composition
cat .forge/composition.yaml
# Shows team's principles, tools, agents

# 4. Read active principles
cat .forge/elements/principle/*/README.md
# Understand team values and approach

# 5. Review memory
ls .forge/memory/project/
# See past decisions and learnings

# 6. Generate integration
forge generate claude-code

# 7. Start contributing
# Claude guides new developer based on team's composition
```

**Outcome:**
- New team member understands team methodology
- Consistent approach across team
- Principles guide Claude's assistance

---

### Workflow 8: Sharing Custom Elements

**Goal:** Share proven elements across team/projects.

**Steps:**

```bash
# Developer A creates useful principle
mkdir -p .forge/elements/principle/api-design-first
cat > .forge/elements/principle/api-design-first/element.yaml <<EOF
metadata:
  name: api-design-first
  type: principle
  version: 1.0.0
  description: Design API contract before implementation
  author: developer-a
  tags: [api, design, contracts]

dependencies:
  principles: []
EOF

cat > .forge/elements/principle/api-design-first/api-design-first.md <<EOF
# Principle: API Design First

## Core Tenet
Design and document API contracts before implementing.

## Motivation
Clear contracts prevent integration issues and enable parallel work.

## Implications
- Write OpenAPI/Swagger specs first
- Review API design with team
- Generate client code from specs
- Validate implementation against spec
EOF

# Commit and push
git add .forge/elements/
git commit -m "Add api-design-first principle"
git push

# Developer B uses it
git pull
cat >> .forge/composition.yaml <<EOF
  principles:
    - api-design-first
EOF

forge update claude-code
```

**Outcome:**
- Team knowledge codified
- Reusable across projects
- Continuous improvement

---

## Maintenance Workflows

### Workflow 9: Updating Elements

**Goal:** Incorporate element updates without breaking project.

**Steps:**

```bash
# 1. Check current elements
cat .forge/composition.yaml

# 2. Update Forge package
cd /path/to/forge
git pull
uv pip install -e .

# 3. Back to project
cd /path/to/project

# 4. Update integration (preserves composition)
forge update claude-code

# 5. Review changes
git diff .claude/

# 6. Test with updated elements
# Use Claude Code with updated principles/tools

# 7. If issues, pin to specific version
cat >> .forge/composition.yaml <<EOF
elements:
  principles:
    - name: coevolution
      version: 1.0.0  # Pin to version
EOF

forge update claude-code
```

**Outcome:**
- Benefit from element improvements
- Control when to adopt changes
- Safe upgrades

---

### Workflow 10: Migrating Between Memory Providers

**Goal:** Scale from file-based to database memory.

**Steps:**

```bash
# Starting with file provider
cat .forge/composition.yaml
# settings:
#   memory:
#     provider: file

# 1. Set up PostgreSQL
docker run -d \
  --name forge-db \
  -e POSTGRES_PASSWORD=secret \
  -p 5432:5432 \
  postgres:15

# 2. Create database
psql -h localhost -U postgres -c "CREATE DATABASE forge_memory;"

# 3. Export existing memory
mkdir memory-backup
cp -r .forge/memory/* memory-backup/

# 4. Update composition
cat >> .forge/composition.yaml <<EOF
settings:
  memory:
    provider: relational
    config:
      url: postgresql://postgres:secret@localhost:5432/forge_memory
EOF

# 5. Migrate data (future: automated migration tool)
# For now: manual import of key entries

# 6. Test new provider
# Use Claude Code, verify memory persists

# 7. Once validated, remove backup
rm -rf memory-backup
```

**Outcome:**
- Scalable memory system
- Preserved historical data
- Better query performance

---

## Advanced Workflows

### Workflow 11: Multi-Project Shared Memory

**Goal:** Share learnings across multiple projects.

**Architecture:**

```
Global memory (shared)
├── Project A (local memory)
├── Project B (local memory)
└── Project C (local memory)
```

**Setup:**

```bash
# 1. Configure shared global memory
mkdir -p ~/.forge/global-memory

# Each project composition
cat > .forge/composition.yaml <<EOF
settings:
  memory:
    provider: file
    config:
      base_path: .forge/memory
      global_path: ~/.forge/global-memory
EOF

# 2. Store global learnings
# From Project A
# memory.set("learning:postgres-tuning", "...", scope=GLOBAL)

# 3. Access in Project B
# memory.get("learning:postgres-tuning", scope=GLOBAL)
```

**Outcome:**
- Cross-project knowledge sharing
- Team-wide learnings persist
- Faster problem solving

---

### Workflow 12: Custom Tool Development

**Goal:** Create project-specific automation.

**Steps:**

```bash
# 1. Identify repetitive task
# "We keep writing similar database migrations"

# 2. Create custom tool
mkdir -p .forge/elements/tool/migration-generator

cat > .forge/elements/tool/migration-generator/element.yaml <<EOF
metadata:
  name: migration-generator
  type: tool
  version: 1.0.0
  description: Generate database migration from model changes
  tags: [database, migration, automation]

dependencies:
  tools: []

interface:
  inputs:
    - model_file: Path to model file
    - migration_name: Name for migration
  outputs:
    - migration_file: Generated migration file
EOF

cat > .forge/elements/tool/migration-generator/migration-generator.md <<EOF
# Tool: Migration Generator

## Purpose
Automatically generate database migrations from model changes.

## Usage
\`\`\`bash
# Compare current models to database
python tools/migration-generator.py compare

# Generate migration
python tools/migration-generator.py generate "add_user_avatar"
\`\`\`

## Implementation
See tools/migration-generator.py
EOF

# 3. Implement tool
cat > tools/migration-generator.py <<EOF
#!/usr/bin/env python3
"""Database migration generator."""

import sys

def compare_models():
    """Compare models to database schema."""
    # Implementation...
    pass

def generate_migration(name):
    """Generate migration file."""
    # Implementation...
    pass

if __name__ == "__main__":
    if sys.argv[1] == "compare":
        compare_models()
    elif sys.argv[1] == "generate":
        generate_migration(sys.argv[2])
EOF

chmod +x tools/migration-generator.py

# 4. Add to composition
cat >> .forge/composition.yaml <<EOF
  tools:
    - migration-generator
EOF

# 5. Update integration
forge update claude-code

# 6. Use tool via Claude Code
# "Generate a migration to add avatar field to users"
```

**Outcome:**
- Project-specific automation
- Reusable across team
- Part of composition, not ad-hoc scripts

---

### Workflow 13: A/B Testing Compositions

**Goal:** Compare different methodologies for your project.

**Steps:**

```bash
# 1. Create branch for experiment
git checkout -b experiment/spec-driven-approach

# 2. Modify composition
cat > .forge/composition.yaml <<EOF
composition:
  name: my-project-spec-driven
  type: preset

elements:
  principles:
    - spec-driven
    - formal-verification
  templates:
    - spec-template
    - test-template
EOF

# 3. Update integration
forge update claude-code

# 4. Develop feature with this approach
# Build feature following spec-driven methodology

# 5. Measure results
# - Time to implement
# - Bug count
# - Team satisfaction

# 6. Compare with main branch approach
git checkout main
git checkout -b experiment/rapid-prototype-approach

cat > .forge/composition.yaml <<EOF
elements:
  principles:
    - ruthless-minimalism
    - coevolution
EOF

forge update claude-code

# Implement same feature with rapid-prototype approach

# 7. Choose best approach or hybrid
git checkout main
# Update composition based on learnings
```

**Outcome:**
- Data-driven methodology choice
- Team learns what works for them
- Continuous methodology improvement

---

### Workflow 14: Documentation-First Projects

**Goal:** Use comprehensive docs to drive development.

**Composition:**

```yaml
elements:
  principles:
    - coevolution
  templates:
    - spec-template
    - architecture-doc
    - decision-log
  tools:
    - doc-generator
```

**Workflow:**

```bash
# 1. Document architecture
cat > docs/architecture.md <<EOF
# System Architecture

## Overview
Microservices architecture with event-driven communication.

## Services
- API Gateway (Node.js)
- User Service (Python)
- Payment Service (Go)
- Notification Service (Python)

## Communication
- REST APIs for synchronous
- RabbitMQ for async events

## Data Stores
- PostgreSQL (users, payments)
- Redis (sessions, cache)
EOF

# 2. Document each service spec
mkdir -p docs/services
cat > docs/services/user-service.md <<EOF
# User Service Specification
...
EOF

# 3. Log architectural decisions
cat > docs/decisions/001-microservices.md <<EOF
# ADR 001: Use Microservices Architecture

## Context
Need to scale different parts of system independently.

## Decision
Adopt microservices with clear service boundaries.

## Consequences
- More operational complexity
- Better scalability
- Team can work independently
EOF

# 4. Generate code from specs
# "Implement user-service based on specification"

# 5. Update docs as you discover constraints
# Coevolution between docs and code

# 6. Generate API documentation
python tools/doc-generator.py --output api-docs/
```

**Outcome:**
- Comprehensive project documentation
- Clear team alignment
- Docs evolve with system

---

## Workflow Patterns Summary

### Choose Your Workflow Based On

| Goal | Recommended Workflow | Key Principles |
|------|---------------------|----------------|
| **Ship fast** | Rapid Prototyping | ruthless-minimalism, coevolution |
| **Ensure quality** | Test-Driven Development | test-first, coevolution |
| **Team alignment** | Specification-Driven | spec-driven, coevolution |
| **Learning system** | Coevolution Practice | coevolution |
| **New team member** | Onboarding | (use existing composition) |
| **Scale memory** | Provider Migration | (technical) |
| **Share knowledge** | Custom Elements | (team collaboration) |
| **Experiment** | A/B Testing | (methodology research) |

### Universal Patterns

1. **Always Use Memory**
   - Store decisions
   - Track learnings
   - Document "why"

2. **Update Regularly**
   - After composition changes
   - After element updates
   - Before major milestones

3. **Validate Often**
   - After manual edits
   - Before git commits
   - After updates

4. **Iterate Compositions**
   - Start simple
   - Add elements as needed
   - Remove what doesn't work

---

For more information:
- [COMMANDS.md](COMMANDS.md) - Detailed command reference
- [element-types.md](element-types.md) - Element documentation
- [memory-system.md](memory-system.md) - Memory system guide
- [../README.md](../README.md) - Project overview

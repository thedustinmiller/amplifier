# Default Profile: Ruthless Minimalism & Emergent Design

## Philosophy at a Glance

**This profile embodies a zen-like approach to software development: start minimal, trust emergence, and let complexity arise only when absolutely necessary.**

### Core Tenets

1. **Ruthless Simplicity**
   - KISS principle as a forcing function
   - Minimize abstractions until they prove essential
   - Start with the most direct solution
   - Every line of code is a liability

2. **Emergent Design**
   - Trust that structure will emerge from solving real problems
   - Don't architect for hypothetical futures
   - Let patterns reveal themselves through iteration
   - Resist premature abstraction

3. **Bricks & Studs Architecture**
   - Build self-contained "bricks" (directories with everything inside)
   - Define clear "studs" (public contracts/interfaces)
   - Start with the contract: purpose, inputs, outputs, dependencies
   - Build bricks in isolation with all code, tests, fixtures together
   - Regenerate rather than patch when changes are needed

4. **Human ↔ AI Handshake**
   - Humans write specifications and make decisions
   - AI generates implementations from specs
   - Continuous iteration based on real use
   - Preserve decisions to prevent uninformed reversals

### When to Use This Profile

**Use this profile when:**
- Building new tools or systems from scratch
- You want to stay nimble and avoid over-engineering
- The problem space is not fully understood yet
- You value code simplicity over clever solutions
- You're working with AI to generate implementations

**Consider alternatives when:**
- You're in a regulated domain requiring upfront design (try `waterfall`)
- You need formal verification or proofs (try `mathematical-elegance`)
- You're working with legacy systems requiring incremental change
- Team size or compliance demands more process

### Key Commands

This profile emphasizes document-driven development (DDD):
- `/ddd:1-plan` - Create high-level plan
- `/ddd:2-contract` - Define module contracts
- `/ddd:3-implement` - Generate implementation
- `/ddd:4-verify` - Test and validate
- `/ddd:5-finish` - Finalize and document

### Key Agents

- **zen-architect** - Analyzes problems with minimalist lens
- **modular-builder** - Implements bricks from contracts
- **bug-hunter** - Finds and fixes issues
- **test-coverage** - Ensures behavior is verified

### Philosophy Documents

This profile loads:
1. `IMPLEMENTATION_PHILOSOPHY.md` - Core principles and decision framework
2. `MODULAR_DESIGN_PHILOSOPHY.md` - Bricks & studs approach
3. This `PROFILE.md` - Quick reference

### Design Principles

- **Code over configuration** - Prefer explicit code to magic configs
- **Tests verify behavior** - Not implementation details
- **60/30/10 testing** - 60% unit, 30% integration, 10% e2e
- **Fail fast and visibly** - During development, not production
- **One concern per module** - High cohesion, loose coupling

### Cultural Notes

This profile draws inspiration from:
- **Wabi-sabi** - Finding beauty in imperfection and simplicity
- **Unix philosophy** - Do one thing well, compose tools
- **Extreme Programming** - Simplest thing that could work
- **Lean Startup** - Build, measure, learn

### Anti-patterns to Avoid

- Gold-plating and premature optimization
- Frameworks for one-off needs
- Complex inheritance hierarchies
- Clever code that requires comments
- Testing implementation instead of behavior
- Solving problems you don't have yet

---

## How This Profile Works

When this profile is active:
1. Session starts by loading philosophy documents
2. Commands guide you through document-driven development
3. Agents make decisions through the minimalist lens
4. Hooks enforce code quality automatically
5. Discoveries feed back to improve the process

This creates a **cognitive prosthesis** that helps you think and build in a ruthlessly simple way, using AI to handle implementation while you focus on vision and judgment.

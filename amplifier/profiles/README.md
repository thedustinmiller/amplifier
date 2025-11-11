# Development Profiles: Metacognitive Process Design

## What Are Profiles?

**Profiles are not just configurations - they are cognitive prostheses that shape how you think about and approach development.**

Rather than forcing a single prescriptive methodology, the profiles system makes the development process itself:
- **Explicit** - Philosophy is documented, not implicit
- **Mutable** - You can switch or create approaches
- **Compositional** - Profiles reuse and combine components
- **Self-improving** - The profile-editor profile makes the system subject to its own processes

This transforms the toolkit from a set of tools into a **system for externalizing and evolving your entire development methodology**.

## Quick Start

### See Available Profiles
```bash
/profile-list
```

### Switch Profiles
```bash
/profile-switch waterfall              # Switch to phase-gate development
/profile-switch mathematical-elegance  # Switch to formal methods
/profile-switch default                # Return to minimalist approach
```

### Create New Profile
```bash
/profile-create my-approach
```

### Edit Profiles (Meta!)
```bash
/profile-switch profile-editor
/profile-analyze default
/profile-refine
```

## Architecture

### Directory Structure

```
profiles/
├── default/                    # Ruthless minimalism & emergent design
│   ├── PROFILE.md             # Philosophy "pitch" (what's this about?)
│   ├── config.yaml            # Technical configuration
│   ├── commands/              # Profile-specific commands
│   └── agents/                # Profile-specific agents
│
├── profile-editor/            # Meta-profile for editing profiles
│   ├── PROFILE.md
│   ├── config.yaml
│   ├── PROFILE_DESIGN_PRINCIPLES.md
│   └── ...
│
├── waterfall/                 # Traditional phase-gate development
├── mathematical-elegance/     # Formal methods & proofs
└── README.md                  # This file

.claude/
├── active-profile -> ../profiles/default/  # Symlink to active profile
├── commands/                  # Shared command library
└── agents/                    # Shared agent library
```

### How Profiles Work

1. **Active Profile** - `.claude/active-profile` symlink points to current profile
2. **Configuration** - Each profile's `config.yaml` defines:
   - Imported commands and agents (from shared library)
   - Local commands and agents (profile-specific)
   - Philosophy documents to load
   - Settings and preferences
3. **Philosophy Loading** - On session start, philosophy documents shape AI's thinking
4. **Compositional** - Profiles reference shared resources, don't duplicate them

## Included Profiles

### default - Ruthless Minimalism & Emergent Design

**Philosophy**: Start minimal, trust emergence, let complexity arise only when necessary.

**Core Tenets**:
- KISS principle as a forcing function
- Trust that structure emerges from solving real problems
- Bricks & studs architecture (self-contained modules with clear contracts)
- Human ↔ AI handshake (humans write specs, AI generates code)

**When to Use**:
- Building new tools from scratch
- Want to stay nimble and avoid over-engineering
- Problem space not fully understood
- Working with AI to generate implementations

**Key Commands**: `/ddd:1-plan` through `/ddd:5-finish`

**Tradeoffs**:
- Gains: Nimbleness, simplicity, adaptability
- Sacrifices: Upfront certainty, comprehensive planning

---

### profile-editor - Meta-Cognitive Process Design

**Philosophy**: Development methodology itself is mutable, explorable, and subject to rigor.

**Core Tenets**:
- Process as code (version-controlled, testable, iterable)
- Meta-cognitive awareness (observe how process affects outcomes)
- Compositional thinking (compose from smaller patterns)
- Empirical improvement (base changes on actual pain points)

**When to Use**:
- Creating a new development profile
- Refining an existing profile based on experience
- Analyzing why current process isn't working
- Exploring alternative methodologies

**Key Commands**: `/profile-analyze`, `/profile-compare`, `/profile-create`, `/profile-refine`

**Warning**: Easy to get lost in abstraction. Use intermittently, then return to building.

---

### waterfall - Sequential Phase-Based Development

**Philosophy**: Thorough upfront planning, sequential phases with gates, comprehensive documentation.

**Core Tenets**:
- Requirements first - Fully specify before design
- Phase-gate structure - Complete each phase before next
- Comprehensive documentation - Mandatory deliverables
- Risk through planning - Minimize surprises

**When to Use**:
- Requirements are well-understood and stable
- In regulated domains (medical, aerospace, defense)
- Cost of changes is very high
- Multiple teams need detailed coordination
- Fixed-price contracts demand upfront estimates

**Key Commands**: `/waterfall:1-requirements` through `/waterfall:5-deploy`, `/gate-review`

**Tradeoffs**:
- Gains: Predictability, coordination, documentation, regulatory compliance
- Sacrifices: Adaptability, speed, learning from implementation

---

### mathematical-elegance - Formal Methods & Provable Correctness

**Philosophy**: Mathematical rigor, formal specifications, type-driven design, provable correctness.

**Core Tenets**:
- Correctness over convenience
- Types encode invariants ("make illegal states unrepresentable")
- Specifications as mathematics (pre/post-conditions, formal proofs)
- Elegant abstractions (category theory, algebraic structures)

**When to Use**:
- Correctness more important than time to market
- Safety-critical systems (bugs have catastrophic consequences)
- Building foundational libraries or protocols
- Long-term maintainability outweighs initial effort
- Team has mathematical sophistication

**Key Commands**: `/formal:specify`, `/formal:prove`, `/type:design`, `/property:test`

**Tradeoffs**:
- Gains: Provable correctness, confidence, deep understanding
- Sacrifices: Time to first version, accessibility, pragmatism

---

## Creating Your Own Profile

### Option 1: From Archetype
```bash
/profile-create my-profile --archetype iterative
```

Available archetypes:
- `minimalist` - Start small, let complexity emerge
- `formal` - Proofs, specifications, verification
- `sequential` - Phases, gates, upfront design
- `iterative` - Sprints, stories, continuous delivery
- `exploratory` - Hypothesis, experiment, learn
- `safety-critical` - Compliance, validation, traceability

### Option 2: From Existing Profile
```bash
/profile-create my-profile --from-template default
```

### Option 3: From Scratch
```bash
/profile-switch profile-editor
/profile-create my-profile
```

The profile-editor will guide you through:
1. What is this profile optimizing for?
2. What are the core principles?
3. What commands embody this approach?
4. What agents think this way?
5. What are the key tradeoffs?
6. When should someone use this profile?

## Compositional Design

Profiles are **compositional** - they reference and combine rather than duplicate.

### Shared Resources

Located in `.claude/`:
- `commands/` - Shared command library (ultrathink-task, prime, etc.)
- `agents/` - Shared agent library (zen-architect, modular-builder, etc.)

### Profile-Specific Resources

Located in each `profiles/<name>/`:
- `commands/` - Commands unique to this profile
- `agents/` - Agents specific to this approach

### Reference Syntax

In `config.yaml`:
```yaml
imports:
  commands:
    - "@commands/ultrathink-task"  # From shared library
  agents:
    - "@agents/zen-architect"      # From shared library

local:
  commands:
    - "ddd:1-plan"                 # From this profile's commands/
  agents:
    - "bricks-builder"             # From this profile's agents/
```

This enables:
- **Reuse** - Improvements benefit all profiles
- **Clarity** - Easy to see what's shared vs. profile-specific
- **Experimentation** - Try new profiles without massive duplication

## Philosophy Documents

Each profile defines philosophy documents that are loaded on session start. These shape how the AI thinks about development.

Example from `default/config.yaml`:
```yaml
philosophy:
  - "../../ai_context/IMPLEMENTATION_PHILOSOPHY.md"  # Core principles
  - "../../ai_context/MODULAR_DESIGN_PHILOSOPHY.md"  # Bricks & studs
  - "./PROFILE.md"                                   # Quick reference
```

Philosophy documents should:
1. Be explicit about what you're optimizing for
2. Explain reasoning, not just rules
3. Make tradeoffs visible
4. Guide decisions, not script them
5. Leave room for judgment

## Profile Lifecycle

### 1. Creation
```bash
/profile-create my-profile
```

### 2. Activation
```bash
/profile-switch my-profile
```

### 3. Use
Build things! The profile shapes how AI assists.

### 4. Observation
Notice pain points, what works, what doesn't.

### 5. Reflection
```bash
/profile-switch profile-editor
/profile-analyze my-profile
```

### 6. Refinement
```bash
/profile-refine
```

### 7. Iteration
Return to step 2. Profiles evolve with use.

## Meta-Cognitive Loop

The profiles system creates a **meta-cognitive loop**:

1. **Work in a profile** - Use default, waterfall, whatever fits
2. **Notice patterns** - What works? What creates friction?
3. **Switch to profile-editor** - Meta-cognitive mode
4. **Analyze and refine** - Improve the process
5. **Switch back** - Apply learnings
6. **Repeat** - Continuous process improvement

This makes your development methodology **subject to the same rigor as your code**.

## Design Principles

### For Profile Designers

When creating or refining profiles:

1. **Be explicit about optimization targets** - Every methodology makes tradeoffs
2. **Make philosophy executable** - Abstract principles → concrete tools
3. **Design for composability** - Reference, don't duplicate
4. **Document the why** - Future you needs context
5. **Embrace appropriate incompleteness** - Leave room for judgment
6. **Design for user's mental model** - Match how people think
7. **Include "when to use" guidance** - Prevent cargo-culting
8. **Make tradeoffs visible** - Name what you sacrifice

See `profile-editor/PROFILE_DESIGN_PRINCIPLES.md` for deep dive.

### Anti-Patterns to Avoid

- **Cargo culting** - Copying process without understanding why
- **Process maximalism** - Adding ceremony for ceremony's sake
- **Philosophy drift** - Practice diverges from stated principles
- **Premature standardization** - Locking in before understanding needs
- **Meta-work as procrastination** - Refining process instead of building

## Advanced Usage

### Invoking Subagents with Specific Profiles

One of the key benefits of the profiles system is the ability to invoke subagents with specific cognitive approaches, regardless of your currently active profile.

#### Pattern 1: Explicit Profile Context in Task Description

When using the Task tool or invoking subagents, you can specify the desired cognitive approach in the task description:

```
Use the zen-architect agent with minimalist philosophy to design a caching layer
```

```
Deploy the requirements-analyst agent using waterfall methodology to gather requirements
```

```
Invoke the proof-architect agent with formal methods approach to verify this algorithm
```

#### Pattern 2: Profile-Specific Agents

Create agents specifically designed for a profile by placing them in `profiles/<name>/agents/`:

```
profiles/
├── waterfall/
│   └── agents/
│       ├── requirements-analyst.md    # Waterfall-specific
│       └── gate-reviewer.md          # Waterfall-specific
├── mathematical-elegance/
│   └── agents/
│       ├── proof-architect.md        # Formal methods-specific
│       └── type-designer.md          # Type-driven design
└── default/
    └── agents/
        └── bricks-builder.md         # Minimalist-specific
```

These agents automatically inherit their profile's philosophy when invoked.

#### Pattern 3: Temporary Profile Switching for Specific Tasks

For complex workflows, you can switch profiles temporarily:

```bash
# Currently in default profile
/profile-switch waterfall
# Work with waterfall methodology
# ... use agents, commands, etc.
/profile-switch default  # Return to default
```

#### Pattern 4: Parallel Agents with Different Profiles

Use multiple agents in parallel, each with different profiles, to explore approaches:

```
Launch three parallel agents:
1. Use zen-architect with minimalist approach
2. Use requirements-analyst with waterfall methodology
3. Use proof-architect with formal methods

Compare their recommendations.
```

### Comparing Profiles
```bash
/profile-compare default waterfall
```

### Extracting Philosophy from Code
```bash
/philosophy-extract --from-code src/
```

### Analyzing Pain Points
```bash
/process-pain-points --profile default
```

### Profile Composition (Future)
Potential future feature: Compose profiles from other profiles
```yaml
extends:
  - "@profiles/default"
overrides:
  testingStrategy: "TDD"
```

## Integration with Existing System

Profiles integrate with existing Amplifier components:

- **Commands** - Both shared (.claude/commands/) and profile-specific (profiles/*/commands/)
- **Agents** - Both shared (.claude/agents/) and profile-specific (profiles/*/agents/)
- **Hooks** - Profiles can define custom hooks in config.yaml
- **Philosophy** - Profiles load philosophy documents that guide AI reasoning
- **MCP Servers** - Profiles can specify which MCP servers they use

The profiles system is **additive** - it makes the existing system more flexible without breaking anything.

## Technical Details

### Symlink Mechanism
```bash
.claude/active-profile -> ../profiles/default/
```

The symlink determines which profile is active. Change it to switch profiles:
```bash
ln -sfn ../profiles/waterfall .claude/active-profile
```

### Config.yaml Schema
```yaml
name: string                    # Profile identifier
description: string             # One-line summary
version: string                 # Semantic version

imports:                        # From shared library
  commands: string[]            # @commands/name
  agents: string[]              # @agents/name

local:                          # Profile-specific
  commands: string[]            # Local command names
  agents: string[]              # Local agent names

philosophy: string[]            # Paths to philosophy docs

hooks:                          # Profile-specific hooks
  SessionStart: string
  PostToolUse: string
  # etc.

settings:                       # Profile-specific settings
  [key]: [value]

tags: string[]                  # For discovery
```

### Loading Process

1. Session starts
2. Hook reads `.claude/active-profile` symlink
3. Loads `profiles/<active>/config.yaml`
4. Resolves imports (@commands/*, @agents/*)
5. Loads philosophy documents in order
6. Applies settings
7. Makes commands and agents available

## Philosophy

The profiles system embodies several key insights:

1. **Development methodology is a first-class artifact** - It should be as carefully designed as code

2. **One size does NOT fit all** - Different contexts demand different approaches

3. **Process should be explicit, not implicit** - If you can't articulate why you work a certain way, you can't improve it

4. **Metacognition is a tool** - The ability to reflect on and improve your process is valuable

5. **Composition over inheritance** - Reuse and combine rather than duplicate

6. **The system should eat its own dogfood** - The profile-editor profile makes the system subject to its own processes

## Future Directions

Potential enhancements:

- **Profile analytics** - Measure which profiles lead to better outcomes
- **Profile composition** - Profiles that extend other profiles
- **Dynamic profile switching** - Auto-switch based on context
- **Profile marketplace** - Share profiles across teams/organizations
- **Profile versioning** - Track evolution of methodologies over time
- **Empirical validation** - A/B test development approaches

## Contributing New Profiles

To contribute a new profile:

1. Create the profile using `/profile-create`
2. Use it for real work - profiles should solve actual problems
3. Document the philosophy clearly
4. Include "when to use" and "when NOT to use" guidance
5. Make tradeoffs explicit
6. Submit PR with profile in `profiles/<name>/`

Good profiles:
- Embody a coherent philosophy
- Solve real problems
- Make tradeoffs explicit
- Are honest about limitations
- Provide clear guidance on when to use

## Questions?

The profile system is designed to be discoverable:

- `/profile-list` - See all available profiles
- `/profile-switch profile-editor` - Enter meta-cognitive mode
- `/profile-analyze <name>` - Deep dive on a profile
- `profiles/<name>/PROFILE.md` - Read the philosophy

## The Big Picture

This system is about **making thought processes explicit and improvable**.

Instead of:
- Implicit methodology that varies by person
- Process that's "just how we do things"
- Inflexible one-size-fits-all approaches
- Development as a black art

You get:
- Explicit methodologies that can be compared
- Process as code that evolves
- Flexible approaches that adapt to context
- Development as a discipline

The goal is to create a **cognitive prosthesis** that helps you think more clearly about how you build software, while making that thinking process itself subject to continuous improvement.

Use it wisely. Build great things.

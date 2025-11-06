# Profiles System: Metacognitive Development Framework

## What Changed?

Amplifier has evolved from a prescriptive toolkit into a **metacognitive system** where the development process itself is:
- **Explicit** - Philosophy is documented
- **Mutable** - You can switch approaches
- **Compositional** - Profiles reuse components
- **Self-improving** - Subject to its own processes

## TL;DR

```bash
# See available development profiles
/profile-list

# Switch to different development approach
/profile-switch waterfall              # Traditional phase-gate
/profile-switch mathematical-elegance  # Formal methods
/profile-switch default                # Minimalist (current)

# Create your own profile
/profile-create my-approach

# Meta: Edit profiles themselves
/profile-switch profile-editor
```

## The Problem

Previously, Amplifier encoded a single development philosophy:
- Ruthless minimalism
- Emergent design
- Bricks & studs architecture

This is powerful but **prescriptive**. It assumes:
- You're building greenfield projects
- You value nimbleness over certainty
- You're okay with minimal upfront planning

But what if you're:
- Working in a regulated domain requiring formal validation?
- Building safety-critical systems needing proofs?
- On a team that thinks in phases and gates?
- Exploring mathematical elegance over pragmatism?

**One size does not fit all.**

## The Solution: Profiles

**Profiles** are complete development methodologies that you can switch between:

### Included Profiles

1. **default** - Ruthless minimalism & emergent design (current philosophy)
2. **profile-editor** - Meta-profile for editing profiles themselves
3. **waterfall** - Sequential phase-gate development
4. **mathematical-elegance** - Formal methods & provable correctness

Each profile includes:
- Philosophy documents that shape AI's thinking
- Commands appropriate for that methodology
- Agents that embody the approach
- Clear guidance on when to use it

## Architecture

### Before (Prescriptive)
```
.claude/
├── commands/      # All commands (DDD workflow baked in)
├── agents/        # All agents (minimalist lens baked in)
└── settings.json

ai_context/
├── IMPLEMENTATION_PHILOSOPHY.md    # Ruthless minimalism
└── MODULAR_DESIGN_PHILOSOPHY.md   # Bricks & studs
```

Every session loaded the same philosophy, used the same commands, thought the same way.

### After (Metacognitive)
```
profiles/
├── default/                        # Minimalist approach
│   ├── PROFILE.md                 # Philosophy "pitch"
│   ├── config.yaml                # Configuration
│   ├── commands/                  # Profile-specific commands
│   └── agents/                    # Profile-specific agents
│
├── profile-editor/                # Meta-profile
├── waterfall/                     # Phase-gate approach
└── mathematical-elegance/         # Formal methods

.claude/
├── active-profile -> ../profiles/default/  # Symlink to active
├── commands/      # Shared command library
└── agents/        # Shared agent library
```

Profiles compose by referencing shared resources:
```yaml
imports:
  commands:
    - "@commands/ultrathink-task"  # Shared
  agents:
    - "@agents/zen-architect"      # Shared

local:
  commands:
    - "ddd:1-plan"                 # Profile-specific
```

## Key Concepts

### 1. Profiles as Cognitive Prostheses

A profile isn't just settings - it's a **cognitive prosthesis** that shapes how you think:
- Philosophy documents guide AI's reasoning
- Commands embody the methodology
- Agents think through that lens
- Settings enforce preferences

Switching profiles changes the **cognitive affordances** - what's easy vs. hard.

### 2. Compositional Design

Profiles don't duplicate - they **compose**:
- Reference shared commands and agents with `@commands/name`, `@agents/name`
- Add profile-specific commands/agents locally
- Improvements to shared resources benefit all profiles

This enables experimentation without massive duplication.

### 3. Meta-Cognitive Loop

The `profile-editor` profile creates a **meta-cognitive loop**:

1. Work in your normal profile (default, waterfall, etc.)
2. Notice pain points or process questions
3. Switch to `profile-editor`
4. Analyze, refine, or create profiles
5. Switch back and apply learnings

This makes your development process **subject to the same rigor as your code**.

### 4. Explicit Tradeoffs

Every profile is honest about tradeoffs:

**default**:
- Gains: Nimbleness, simplicity, adaptability
- Sacrifices: Upfront certainty, comprehensive planning

**waterfall**:
- Gains: Predictability, coordination, compliance
- Sacrifices: Adaptability, speed, learning from building

**mathematical-elegance**:
- Gains: Provable correctness, deep understanding
- Sacrifices: Time to first version, accessibility

This prevents cargo-culting and enables informed choice.

## Migration Path

### Nothing Breaks

The profiles system is **additive**:
- Default profile preserves existing philosophy
- Existing commands and agents work unchanged
- Current workflows continue as-is

### To Adopt Profiles

1. **Explore**: `/profile-list` to see what's available
2. **Experiment**: `/profile-switch <name>` to try different approaches
3. **Create**: `/profile-create` when you need something new
4. **Refine**: `/profile-switch profile-editor` to improve profiles

Start by just being aware profiles exist. Switch when context demands it.

## Use Cases

### Regulated Development
```bash
/profile-switch waterfall
/waterfall:1-requirements  # Formal requirements gathering
/gate-review              # Phase gate approval
```

Perfect for medical devices, aerospace, regulated domains.

### Formal Verification
```bash
/profile-switch mathematical-elegance
/formal:specify           # Write formal specification
/type:design             # Design type system
/formal:prove            # Construct proof
```

Perfect for safety-critical systems, cryptography, foundational libraries.

### Exploratory Work
```bash
/profile-switch default
/ddd:1-plan              # Minimal planning
/ddd:3-implement         # Start building
# Let structure emerge through iteration
```

Perfect for greenfield projects, rapid prototyping, AI-assisted development.

### Process Improvement
```bash
/profile-switch profile-editor
/profile-analyze default
/profile-compare default waterfall
/profile-refine
```

Perfect for teams wanting to articulate and improve their process.

## Philosophy

The profiles system embodies several insights:

### 1. Process is a First-Class Artifact
Your development methodology should be as carefully designed as your code.

### 2. Context Matters
Different situations demand different approaches. Flexibility beats rigidity.

### 3. Explicit Beats Implicit
If you can't articulate why you work a certain way, you can't improve it.

### 4. The System Should Eat Its Own Dogfood
The profile-editor makes the system subject to its own processes. Recursive, but bounded.

### 5. Composition Over Duplication
Reuse and combine rather than copy. DRY applies to process too.

## For Power Users

### Creating Custom Profiles

```bash
/profile-switch profile-editor
/profile-create my-team-process --archetype iterative
```

Guide you through:
- What are you optimizing for?
- Core principles?
- Key tradeoffs?
- When to use?

### Profile Anatomy

Each profile directory contains:
```
my-profile/
├── PROFILE.md           # Philosophy "pitch" (required)
├── config.yaml          # Technical config (required)
├── commands/            # Profile-specific commands (optional)
├── agents/              # Profile-specific agents (optional)
└── *.md                # Additional philosophy docs (optional)
```

### Config.yaml Structure

```yaml
name: my-profile
description: "One-line summary"
version: "1.0.0"

imports:                  # From shared library
  commands: ["@commands/ultrathink-task"]
  agents: ["@agents/zen-architect"]

local:                    # Profile-specific
  commands: ["my-cmd"]
  agents: ["my-agent"]

philosophy:               # Docs to load
  - "./PROFILE.md"
  - "../../ai_context/SOME_DOC.md"

settings:                 # Profile preferences
  testingStrategy: "TDD"

tags: ["agile", "iterative"]
```

### Profile Switching

Mechanically:
```bash
ln -sfn ../profiles/<name> .claude/active-profile
```

Session restart loads new profile's config and philosophy.

## Advanced Topics

### Profile Composition (Future)
Potential: Profiles that extend other profiles
```yaml
extends: "@profiles/default"
overrides:
  testingStrategy: "property-based"
```

### Profile Analytics (Future)
Measure which profiles lead to better outcomes. Empirical process improvement.

### Dynamic Switching (Future)
Auto-switch based on context (file type, git branch, time of day, etc.)

## Implementation Notes

### For Claude Code

The profiles system integrates with Claude Code's existing features:
- Philosophy documents loaded on session start
- Commands discovered from both shared and profile directories
- Agents available from both pools
- Hooks can be profile-specific

### For Hook Authors

Session start hook should:
1. Read `.claude/active-profile` symlink
2. Load profile's `config.yaml`
3. Resolve imports (@commands/*, @agents/*)
4. Load philosophy documents in order
5. Apply profile settings

See `.claude/tools/hook_session_start.py` for implementation.

## Documentation

- `profiles/README.md` - Comprehensive profiles documentation
- `profiles/<name>/PROFILE.md` - Individual profile philosophy
- `profile-editor/PROFILE_DESIGN_PRINCIPLES.md` - How to design profiles
- This file - Overview and migration guide

## Questions & Feedback

The profiles system is an experiment in **making development methodology itself subject to tooling**.

Questions:
- What profiles would be useful for your work?
- What makes this system more/less powerful?
- Where does the abstraction help/hurt?

Feedback welcome. This is v1.0 - expect iteration.

## The Big Picture

Amplifier started as a toolkit for building AI-powered CLI tools.

With profiles, it becomes a **metacognitive system**:
- Tools for building tools (ccsdk_toolkit)
- Agents for specialized thinking
- Commands for workflows
- **Profiles for shaping the development process itself**

The goal: Create a **cognitive prosthesis** that helps you think more clearly about building software, while making that thinking process subject to continuous improvement.

The system has become powerful enough to improve itself.

Use it wisely.

## Usage
/profile-list [--detailed]

## Context
- Shows all available development profiles
- Displays which profile is currently active
- Optional detailed view shows full profile information
- Helps users discover and understand different development approaches

## Process

### 1. Read Active Profile
- Check the `.claude/active-profile` symlink to determine current profile
- Read the target of the symlink to identify active profile name

### 2. Discover All Profiles
- Scan the `profiles/` directory for subdirectories
- Each subdirectory is a profile
- Read each profile's `PROFILE.md` and `config.yaml`

### 3. Display Profile List
For each profile, show:
- **Name** - Profile identifier
- **Description** - One-line summary from config.yaml
- **Status** - [ACTIVE] or [ ] indicator
- **Tags** - Key characteristics (minimalist, formal, sequential, etc.)
- **When to use** - Brief guidance from PROFILE.md

### 4. If --detailed flag provided
Show additional information for each profile:
- Full philosophy summary
- Imported commands and agents
- Local (profile-specific) commands and agents
- Key tradeoffs
- Related profiles

## Output Format

### Basic View

```
Available Profiles:

[ACTIVE] default - Ruthless minimalism with emergent design
         Tags: minimalism, emergent-design, modular, document-driven
         Use when: Building new tools, staying nimble, avoiding over-engineering

[ ] profile-editor - Meta-cognitive profile for analyzing and refining processes
    Tags: meta-cognitive, process-design, methodology, reflection
    Use when: Creating/refining profiles, analyzing development approaches

[ ] waterfall - Sequential phase-based development with formal gates
    Tags: waterfall, sequential, phase-gate, predictive, formal
    Use when: Stable requirements, regulated domains, need predictability

[ ] mathematical-elegance - Formal methods and provable correctness
    Tags: formal-methods, type-driven, mathematical, correctness, proofs
    Use when: Correctness critical, safety-critical systems, foundational libraries

To switch profiles: /profile-switch <name>
To see detailed info: /profile-list --detailed
To create a new profile: /profile-create <name>
```

### Detailed View

For each profile, additionally show:
```
Profile: default
Description: Ruthless minimalism with emergent design
Status: ACTIVE
Version: 1.0.0

Philosophy:
  - Ruthless simplicity - KISS principle as forcing function
  - Emergent design - Trust structure will emerge from solving real problems
  - Bricks & studs architecture - Self-contained modules with clear contracts

Imports:
  Commands: @commands/ultrathink-task, @commands/prime, @commands/transcripts, ...
  Agents: @agents/zen-architect, @agents/modular-builder, @agents/bug-hunter, ...

Local Commands: ddd:1-plan, ddd:2-contract, ddd:3-implement, ddd:4-verify, ddd:5-finish
Local Agents: (none)

Key Tradeoffs:
  Gains: Nimbleness, simplicity, adaptability, emergence
  Sacrifices: Upfront certainty, comprehensive planning, formal validation

When to use:
  - Building new tools or systems from scratch
  - You want to stay nimble and avoid over-engineering
  - Problem space is not fully understood yet

Consider alternatives when:
  - In regulated domain requiring upfront design (try waterfall)
  - Need formal verification or proofs (try mathematical-elegance)

---
```

## Notes
- This command is available in all profiles (it's a shared command)
- Helps users navigate the profile system
- Encourages exploration of different development approaches
- Makes the profile system discoverable

## Implementation Details
- Read from `profiles/` directory to discover profiles
- Parse YAML configs for metadata
- Read PROFILE.md for philosophy summaries
- Check symlink at `.claude/active-profile` for active status

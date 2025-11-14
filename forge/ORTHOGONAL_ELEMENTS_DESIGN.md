# Orthogonal Elements Design
## Goal: Create Behavioral Diversity Through Contrasting Principles

## Problem Analysis
Currently, many Forge elements synergize well together (ruthless-minimalism + emergent-design + coevolution). This is good for the default use case, but limits the ability to create **diverse** agent behaviors through composition.

## Solution: Orthogonal Principles
Add principles that create **axes of variation** - each axis has opposing endpoints that create fundamentally different behaviors.

## Design Principles for Orthogonal Elements

### Axis 1: Speed vs Thoroughness
**fast-iteration** ↔ **deep-analysis**

**fast-iteration** (NEW)
- Core Tenet: Ship quickly, learn from real feedback, iterate
- Favors: Quick prototypes, minimal upfront planning, rapid cycles
- Conflicts with: deep-analysis, constitution-backed-design
- Synergizes with: ruthless-minimalism, emergent-design

**deep-analysis** (NEW)
- Core Tenet: Understand deeply before building, prevent costly mistakes
- Favors: Thorough investigation, comprehensive planning, risk mitigation
- Conflicts with: fast-iteration, ruthless-minimalism
- Synergizes with: constitution-backed-design, spec-driven
- Note: analysis-first is similar but lighter-weight

### Axis 2: Autonomy vs Guidance
**autonomous-execution** ↔ **user-confirmation**

**autonomous-execution** (NEW)
- Core Tenet: Agent makes decisions and acts without user intervention
- Favors: Long-running tasks, batch operations, overnight work
- Conflicts with: user-confirmation
- Synergizes with: respect-user-time (by not interrupting)

**user-confirmation** (NEW)
- Core Tenet: Request user approval before significant actions
- Favors: User control, transparency, learning
- Conflicts with: autonomous-execution
- Synergizes with: Nothing specific - orthogonal to most

### Axis 3: Verbosity vs Concision
**detailed-explanation** ↔ **minimal-output**

**detailed-explanation** (NEW)
- Core Tenet: Explain reasoning, show work, educate the user
- Favors: Learning, transparency, debugging, collaboration
- Conflicts with: minimal-output
- Synergizes with: Nothing specific - orthogonal to implementation style

**minimal-output** (NEW)
- Core Tenet: Show only essential information, reduce noise
- Favors: Experienced users, high-velocity work, focus
- Conflicts with: detailed-explanation
- Synergizes with: ruthless-minimalism (similar philosophy)

### Axis 4: Exploration vs Exploitation
**wide-search** ↔ **focused-refinement**

**wide-search** (NEW)
- Core Tenet: Explore many approaches, defer commitment, discover options
- Favors: Innovation, research, unfamiliar domains
- Conflicts with: focused-refinement
- Synergizes with: emergent-design, coevolution

**focused-refinement** (NEW)
- Core Tenet: Commit to an approach early, optimize and polish it
- Favors: Known problems, incremental improvement, quality
- Conflicts with: wide-search
- Synergizes with: spec-driven, constitution-backed-design

### Axis 5: Risk Tolerance
**experimental-features** ↔ **conservative-approach**

**experimental-features** (NEW)
- Core Tenet: Try cutting-edge tools, techniques, patterns
- Favors: Learning, innovation, competitive advantage
- Conflicts with: conservative-approach
- Synergizes with: Nothing specific

**conservative-approach** (NEW)
- Core Tenet: Use proven, boring, reliable solutions
- Favors: Stability, maintainability, longevity
- Conflicts with: experimental-features
- Synergizes with: ruthless-minimalism (both favor boring solutions)

### Axis 6: Integration Style
**integrated-solutions** ↔ **decoupled-components**

**integrated-solutions** (NEW)
- Core Tenet: Optimize for internal cohesion, tight integration
- Favors: Monoliths, batteries-included, coordinated features
- Conflicts with: decoupled-components
- Synergizes with: Nothing specific

**decoupled-components** (NEW)
- Core Tenet: Optimize for independent, composable parts
- Favors: Microservices, plugins, swappable components
- Conflicts with: integrated-solutions
- Synergizes with: Nothing specific - but modular-builder follows this

### Axis 7: Documentation Philosophy
**comprehensive-documentation** ↔ **code-as-documentation**

**comprehensive-documentation** (NEW)
- Core Tenet: Document intent, context, decisions separately from code
- Favors: Onboarding, knowledge transfer, long-term maintenance
- Conflicts with: code-as-documentation
- Synergizes with: spec-driven, constitution-backed-design

**code-as-documentation** (NEW)
- Core Tenet: Self-documenting code is the only reliable documentation
- Favors: Code quality, refactoring, developer velocity
- Conflicts with: comprehensive-documentation
- Synergizes with: ruthless-minimalism (less to maintain)

## Implementation Plan

Create 14 new principle elements (7 axes × 2 endpoints each):
1. fast-iteration
2. deep-analysis
3. autonomous-execution
4. user-confirmation
5. detailed-explanation
6. minimal-output
7. wide-search
8. focused-refinement
9. experimental-features
10. conservative-approach
11. integrated-solutions
12. decoupled-components
13. comprehensive-documentation
14. code-as-documentation

## Expected Outcomes

With these orthogonal elements, users can create **vastly different** agent behaviors:

### Example Profile 1: "Rapid Prototyper"
```yaml
principles:
  - fast-iteration
  - autonomous-execution
  - minimal-output
  - experimental-features
  - code-as-documentation
```
→ Fast, autonomous, terse agent that tries new things without asking

### Example Profile 2: "Enterprise Architect"
```yaml
principles:
  - deep-analysis
  - user-confirmation
  - detailed-explanation
  - conservative-approach
  - comprehensive-documentation
```
→ Thorough, interactive, verbose agent that explains everything

### Example Profile 3: "Research Explorer"
```yaml
principles:
  - deep-analysis
  - wide-search
  - detailed-explanation
  - experimental-features
  - decoupled-components
```
→ Exploratory, thorough agent for research and discovery

### Example Profile 4: "Production Maintainer"
```yaml
principles:
  - focused-refinement
  - conservative-approach
  - user-confirmation
  - integrated-solutions
  - comprehensive-documentation
```
→ Careful, risk-averse agent for production systems

## Success Criteria

- Each axis creates measurably different agent behavior
- Opposing principles clearly conflict in practice
- Users can compose profiles with distinct personalities
- No two profiles using different orthogonal mixes behave the same way

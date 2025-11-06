# Profile Design Principles

## What Makes a Good Profile?

A good profile is a **cognitive prosthesis** - it helps you think in a particular way about development. It's not just a collection of commands and settings, but an embodiment of a coherent development philosophy.

## Core Design Principles

### 1. Be Explicit About What You're Optimizing For

Every development methodology makes tradeoffs. A good profile names these explicitly:

- **Speed vs. Correctness** - Move fast vs. get it right
- **Flexibility vs. Structure** - Adapt quickly vs. follow process
- **Exploration vs. Execution** - Discover vs. deliver
- **Individual vs. Team** - Optimize for one person vs. coordination
- **Short-term vs. Long-term** - Ship now vs. maintainability

**Example**: The `default` profile optimizes for *nimbleness and emergence* at the cost of *upfront certainty*. It chooses *simplicity over comprehensiveness*, betting that the right structure will emerge through iteration.

### 2. Make Philosophy Executable

Abstract principles should translate to concrete tools:

```
Philosophy → Commands → Agents → Code
```

**Bad**: "We value simplicity" (stated but not enforced)

**Good**:
- Philosophy document explains *why* simplicity matters
- Commands guide minimal-first development (ddd:1-plan starts small)
- Agents (zen-architect) analyze complexity and suggest simplification
- Hooks enforce complexity metrics

The philosophy should be **discoverable in the artifacts** - someone reading your code or using your commands should be able to infer the underlying philosophy.

### 3. Design for Composability

Profiles should compose, not duplicate:

**Reuse through references**:
```yaml
imports:
  commands:
    - "@commands/ultrathink-task"
  agents:
    - "@agents/zen-architect"
```

**Not through duplication**:
```yaml
# DON'T copy the entire command/agent definition
local:
  commands:
    - ultrathink-task: [entire definition copied]
```

**Benefits of compositional design**:
- Improvements to shared commands benefit all profiles
- Clear boundaries between profile-specific and universal tools
- Easier to understand what makes each profile unique
- Enables profile experimentation without massive duplication

### 4. Document the Why, Not Just the What

Future you (and others) need context:

**Bad**:
```yaml
# Use test-driven development
testingStrategy: "TDD"
```

**Good**:
```markdown
## Testing Philosophy

We use test-driven development because:
1. This profile targets regulated domains requiring validation
2. Upfront test design clarifies requirements
3. Red-green-refactor matches our incremental approval process
4. Tests become acceptance criteria for compliance

We DON'T mandate TDD when:
- Exploring unknown problem spaces (spike first)
- Prototyping UI/UX (need visual feedback)
- Writing throwaway scripts (test effort > value)
```

### 5. Embrace Appropriate Incompleteness

Not everything needs to be specified. Good profiles leave room for:

- **Judgment** - Human decision-making where context matters
- **Adaptation** - Situational adjustments
- **Learning** - Process improvement through experience
- **Emergence** - Patterns that reveal themselves over time

**Over-specification kills agency**. If you script every decision, you create robots, not developers.

**Example**: The `default` profile doesn't specify *when* to extract an abstraction - it provides principles (KISS, YAGNI) and trusts developers to apply judgment.

### 6. Design for the User's Mental Model

A profile should match how people actually think about the work:

- **Waterfall** - Sequential phases match upfront planning mindset
- **Agile** - Iterations match incremental delivery mindset
- **Mathematical-elegance** - Proofs match formal reasoning mindset

If your profile's structure fights the user's mental model, it creates friction.

### 7. Include Clear "When to Use" Guidance

Help people choose the right profile:

```markdown
## When to Use This Profile

Use this profile when:
- [Specific contexts where it excels]

Consider alternatives when:
- [Specific contexts where it struggles]
```

This prevents cargo-culting and helps teams adapt process to context.

### 8. Make Tradeoffs Visible

Every methodology sacrifices something. Name it:

- **Waterfall** - Sacrifices adaptability for predictability
- **Agile** - Sacrifices upfront certainty for responsiveness
- **Formal methods** - Sacrifices speed for correctness
- **Minimalism** - Sacrifices completeness for simplicity

Acknowledging tradeoffs builds trust and enables informed choice.

## Profile Structure Guidelines

### Essential Components

Every profile should have:

1. **PROFILE.md** - The "pitch" - what's this about at a glance?
2. **config.yaml** - Technical definition of imports and settings
3. **Clear archetype** - What category of approach is this?

### Optional Components

Add when needed:

4. **Philosophy documents** - Detailed reasoning and principles
5. **Local commands** - Profile-specific workflows
6. **Local agents** - Profile-specific specialists
7. **Examples** - Concrete demonstrations of the profile in action
8. **Anti-patterns** - What NOT to do with this profile

### Naming Conventions

- **Profile names** - Descriptive, memorable, lowercase-with-hyphens
  - Good: `mathematical-elegance`, `test-first`, `continuous-discovery`
  - Bad: `profile1`, `new-profile`, `jacks-special-profile`

- **Commands** - Action verbs, namespace if profile-specific
  - Good: `/ddd:plan`, `/formal:prove`, `/explore:spike`
  - Bad: `/do-the-thing`, `/x`, `/command1`

- **Agents** - Role-based, descriptive
  - Good: `process-philosopher`, `proof-checker`, `ux-researcher`
  - Bad: `agent-helper`, `thing-doer`, `assistant`

## Common Pitfalls

### 1. Cargo Culting

Copying a process without understanding *why* it exists.

**Symptoms**: "We do TDD because that's what Agile says" rather than "We do TDD because it clarifies our requirements"

**Fix**: Force yourself to articulate the reasoning. If you can't explain why, don't include it.

### 2. Process Maximalism

Adding ceremony for ceremony's sake.

**Symptoms**: Profiles with 50 commands, 100 agents, and 20 required steps for simple changes

**Fix**: Apply the minimalist test - what happens if you remove this? If nothing bad, remove it.

### 3. Philosophy Drift

The stated principles diverge from actual practice.

**Symptoms**: Profile says "value simplicity" but enforces complex approval chains

**Fix**: Regular audits - does our practice match our philosophy? Update one or the other.

### 4. Hidden Assumptions

Implicit assumptions about context, team, or problem space.

**Symptoms**: Profile works great for one team, fails mysteriously for another

**Fix**: Make assumptions explicit in "When to Use" section

### 5. Overspecification

Scripting every decision, leaving no room for judgment.

**Symptoms**: People follow process mechanically without understanding

**Fix**: Specify principles and outcomes, not every step

## Testing Your Profile

Good tests for a profile:

### 1. The Pitch Test
Can you explain this profile's philosophy in 2 minutes? If not, it's too complex or unclear.

### 2. The Archetype Test
Does this profile fit a recognizable development archetype? If it's totally novel, you may be over-engineering.

### 3. The Tradeoff Test
Can you name 3 things this profile sacrifices? If not, you haven't thought through the costs.

### 4. The User Test
Would someone unfamiliar with this profile understand when to use it? If not, add guidance.

### 5. The Consistency Test
Do the commands and agents embody the stated philosophy? If not, there's drift.

### 6. The Minimalism Test
What happens if you remove each component? If nothing bad, remove it.

## Evolution Over Dogma

Good profiles evolve:

- **Track pain points** - Where does current process create friction?
- **Measure outcomes** - Does this profile achieve its goals?
- **Iterate based on evidence** - Change what doesn't work
- **Document evolution** - Why did we change this?

A profile should be version-controlled, with meaningful commit messages explaining process changes.

## Meta-Cognitive Hygiene

When working on profiles:

- **Set time limits** - Don't get lost in abstraction
- **Return to building** - The best test is actual use
- **Question recursion** - Do you really need a profile for editing profiles for editing profiles?
- **Stay grounded** - Process exists to serve building, not the reverse

Remember: The goal is to make development processes mutable and improvable, not to create infinite layers of meta-process.

---

## Further Reading

- `PROCESS_PATTERNS_LIBRARY.md` - Common development patterns
- `COGNITIVE_AFFORDANCES.md` - How process shapes thought
- Individual profile `PROFILE.md` files - Examples in practice

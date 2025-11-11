## Usage
/profile-create <profile-name> [--from-template <template>] [--archetype <archetype>]

## Context
- Creates a new development profile from scratch or template
- Guides user through defining philosophy, commands, agents
- Sets up proper directory structure
- Helps articulate development process explicitly
- Best used from the `profile-editor` profile

## Process

### 1. Validate Profile Name
- Check that `profiles/<profile-name>/` does NOT already exist
- Verify name follows conventions: lowercase-with-hyphens
- Reject if name conflicts with existing profile
- Good names: `agile-sprint`, `exploratory-research`, `microservices-first`
- Bad names: `Profile1`, `new_profile`, `MYPROFILE`

### 2. Choose Creation Mode

#### Mode A: From Archetype
If `--archetype` flag provided, use predefined archetype:
- `minimalist` - Start small, let complexity emerge
- `formal` - Proofs, specifications, verification
- `sequential` - Phases, gates, upfront design
- `iterative` - Sprints, stories, continuous delivery
- `exploratory` - Hypothesis, experiment, learn
- `safety-critical` - Compliance, validation, traceability

Each archetype has a template with typical commands, agents, and philosophy.

#### Mode B: From Existing Profile
If `--from-template` flag provided, copy structure from existing profile:
- Copy PROFILE.md as starting point
- Copy config.yaml structure
- Modify for new context
- Keep references to shared commands/agents

#### Mode C: From Scratch
If no flags, guide user through defining:
- What is this profile optimizing for?
- What are the core principles?
- What commands make sense?
- What agents embody the philosophy?
- What tradeoffs does it make?

### 3. Create Directory Structure
```
profiles/<profile-name>/
├── PROFILE.md            # Philosophy pitch (created)
├── config.yaml           # Configuration (created)
├── commands/             # Profile-specific commands (empty)
└── agents/               # Profile-specific agents (empty)
```

### 4. Generate PROFILE.md

Guide user through sections:

```markdown
# <Profile Name>: <One-line Description>

## Philosophy at a Glance
[What is this profile about? What mindset does it embody?]

### Core Tenets
1. [Principle 1]
2. [Principle 2]
3. [Principle 3]

### When to Use This Profile
**Use this profile when:**
- [Context 1]
- [Context 2]

**Consider alternatives when:**
- [Context where it doesn't fit]

### Key Commands
- [Command 1] - [Purpose]
- [Command 2] - [Purpose]

### Key Agents
- [Agent 1] - [Role]
- [Agent 2] - [Role]

### Design Principles
- [Principle 1]
- [Principle 2]

### Tradeoffs This Profile Makes
**Gains**: [What you get]
**Sacrifices**: [What you give up]

### Cultural Notes
This profile draws from: [Influences]

### Anti-patterns to Avoid
- [Anti-pattern 1]
- [Anti-pattern 2]
```

### 5. Generate config.yaml

Create configuration:

```yaml
name: <profile-name>
description: "<one-line-description>"
version: "1.0.0"

imports:
  commands:
    # Shared commands this profile uses
    - "@commands/ultrathink-task"
    - "@commands/prime"

  agents:
    # Shared agents this profile uses
    - "@agents/zen-architect"

local:
  commands: []  # Profile-specific commands
  agents: []    # Profile-specific agents

philosophy:
  - "./PROFILE.md"

hooks:
  SessionStart: "hook_session_start.py"

settings:
  enableTodoList: true
  trackDecisions: true

tags:
  - "<tag1>"
  - "<tag2>"
```

### 6. Interview User for Content

Ask key questions to populate the profile:

1. **What is this profile optimizing for?**
   - Speed? Correctness? Learning? Collaboration?
   - This becomes the core philosophy

2. **What are 3-5 core principles?**
   - These guide all decisions in this profile
   - Should be actionable, not platitudes

3. **What commands would embody this approach?**
   - What workflows make sense?
   - Import shared commands or define new ones?

4. **What agents would think this way?**
   - What specialized roles are needed?
   - Can you reuse existing agents?

5. **What are the key tradeoffs?**
   - What do you gain?
   - What do you sacrifice?
   - Be honest about costs

6. **When should someone use this profile?**
   - What contexts is it designed for?
   - When is it the wrong choice?

7. **What influences or methodologies inspired this?**
   - Agile? XP? TDD? FP? Mathematics?
   - Cultural context matters

### 7. Create Supporting Documents

Optionally create:
- `PHILOSOPHY_DETAILED.md` - Deep dive into principles
- `WORKFLOW_GUIDE.md` - Step-by-step workflows
- `EXAMPLES.md` - Concrete examples of profile in use
- Command templates in `commands/`
- Agent templates in `agents/`

### 8. Register Profile

- Profile is automatically discovered (directory exists in `profiles/`)
- Add to documentation
- Test that it can be activated with `/profile-switch`

### 9. Next Steps

Suggest:
```
✓ Profile created: <profile-name>

Next steps:
1. Review and refine: /profile-switch profile-editor, then /profile-analyze <profile-name>
2. Create profile-specific commands in: profiles/<profile-name>/commands/
3. Create profile-specific agents in: profiles/<profile-name>/agents/
4. Test the profile: /profile-switch <profile-name>
5. Iterate based on use: Does it embody the philosophy?

To activate: /profile-switch <profile-name>
To refine: /profile-switch profile-editor
```

## Output Format

```
=== Creating New Profile: agile-sprint ===

Let's define this profile through key questions...

Q: What is this profile optimizing for?
A: [User: Rapid iteration and continuous delivery]

Q: What are the core principles (3-5)?
A: [User:
    1. Time-boxed iterations
    2. User stories over specs
    3. Working software over documentation
    4. Respond to change over following plan]

Q: Key tradeoffs?
A: [User:
    Gains: Speed, adaptability, frequent feedback
    Sacrifices: Long-term planning, comprehensive docs, upfront certainty]

Q: When should someone use this profile?
A: [User: Product development with evolving requirements,
    small to medium teams, need to show progress frequently]

Q: Influences?
A: [User: Agile Manifesto, Scrum, XP]

Generating profile structure...

✓ Created: profiles/agile-sprint/
✓ Created: profiles/agile-sprint/PROFILE.md
✓ Created: profiles/agile-sprint/config.yaml
✓ Created: profiles/agile-sprint/commands/
✓ Created: profiles/agile-sprint/agents/

Profile summary:
  Name: agile-sprint
  Optimizes for: Rapid iteration and continuous delivery
  Core principles: 4 defined
  Imports: 2 commands, 3 agents
  Local: 0 commands, 0 agents (add as needed)

Next: /profile-switch agile-sprint
Refine: /profile-switch profile-editor, then /profile-analyze agile-sprint
```

## Notes
- Best used from `profile-editor` profile for meta-cognitive context
- Creating a good profile requires clear thinking about tradeoffs
- Start simple - you can always add commands/agents later
- Test by actually using the profile
- Iterate based on experience

## Implementation Details
- Create directory: `mkdir -p profiles/<profile-name>/{commands,agents}`
- Generate PROFILE.md from template with user's answers
- Generate config.yaml with appropriate imports
- Validate structure before marking complete
- Add to profile registry (automatic via directory existence)

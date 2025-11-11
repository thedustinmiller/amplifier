## Usage
/profile-switch <profile-name>

## Context
- Switches from current development profile to a different one
- Updates the active profile symlink
- Reloads philosophy documents and configuration
- Changes the cognitive lens through which AI assists development
- Critical for adapting process to context

## Process

### 1. Validate Target Profile
- Check that `profiles/<profile-name>/` exists
- Verify it has required files: `PROFILE.md`, `config.yaml`
- If profile doesn't exist, suggest using `/profile-list` to see available profiles
- If validation fails, do not proceed

### 2. Show Current and Target Profile
Display comparison:
```
Current profile: default (Ruthless minimalism with emergent design)
Target profile:  waterfall (Sequential phase-based development)

This will change:
- Philosophy: Minimalism → Formal planning
- Commands: DDD workflow → Phase-gate workflow
- Agents: Zen-architect → Requirements-analyst, Systems-architect
- Approach: Emergent → Predictive

Do you want to proceed? [Y/n]
```

### 3. Get User Confirmation
- This is a significant cognitive shift
- Explain what will change
- Require explicit confirmation before proceeding

### 4. Update Active Profile Symlink
- Remove existing `.claude/active-profile` symlink if it exists
- Create new symlink: `.claude/active-profile -> ../profiles/<profile-name>`
- Verify symlink was created successfully

### 5. Load New Profile
- Read `profiles/<profile-name>/config.yaml`
- Parse the configuration:
  - Resolve imported commands (@commands/...)
  - Resolve imported agents (@agents/...)
  - Identify local commands and agents
  - Load philosophy documents in order
  - Apply profile-specific settings

### 6. Display New Profile Summary
Show what's now active:
```
✓ Profile switched to: waterfall

Philosophy loaded:
  - WATERFALL_METHODOLOGY.md
  - PHASE_GATE_CHECKLIST.md
  - CHANGE_MANAGEMENT_PROCESS.md
  - PROFILE.md

Available commands:
  Shared: /ultrathink-task, /prime
  Profile: /waterfall:1-requirements, /waterfall:2-design, /waterfall:3-implement, ...

Available agents:
  Shared: zen-architect, modular-builder, bug-hunter, ...
  Profile: requirements-analyst, systems-architect, qa-planner, ...

Settings applied:
  - phaseGatesRequired: true
  - requireDocumentation: comprehensive
  - changeControlProcess: formal

You're now in waterfall mode. This profile emphasizes:
  - Thorough upfront planning
  - Sequential phase progression
  - Formal gate reviews
  - Comprehensive documentation

To see full philosophy: /prime
To return to default: /profile-switch default
```

### 7. Suggest Next Steps
Based on the new profile, suggest appropriate next commands:
- For waterfall: "Start with /waterfall:1-requirements to begin requirements gathering"
- For mathematical-elegance: "Use /formal:specify to write formal specifications"
- For profile-editor: "Use /profile-analyze to analyze a profile"

## Output Format

```
=== Profile Switch: default → waterfall ===

Current: default - Ruthless minimalism with emergent design
Target:  waterfall - Sequential phase-based development

Changes:
  Philosophy:     Emergent design → Formal planning
  Development:    Iterative → Phase-gated
  Documentation:  Minimal → Comprehensive
  Testing:        60/30/10 → Test plans upfront

This is a significant change in development approach.
Proceed with switch? [Y/n]

> Y

Switching profile...

✓ Symlink updated: .claude/active-profile → ../profiles/waterfall
✓ Configuration loaded: waterfall/config.yaml
✓ Philosophy documents loaded (4 files)
✓ Commands registered: 8 profile-specific, 2 shared
✓ Agents registered: 6 profile-specific, 5 shared

=== Now Active: waterfall ===

Phase-based development with formal gates and comprehensive documentation.

Key principles:
  • Requirements first - Fully specify before design
  • Phase-gate structure - Complete each phase before next
  • Comprehensive documentation - Mandatory deliverables
  • Risk through planning - Minimize surprises

Start here: /waterfall:1-requirements
View philosophy: /prime
Return to default: /profile-switch default
```

## Notes
- Profile switching is a cognitive shift, not just a config change
- Explain the change clearly before and after
- Make it reversible - show how to switch back
- Different profiles embody different development philosophies
- Use this when context changes (e.g., moving from greenfield to regulated)

## Implementation Details
- Validate profile exists: `test -d profiles/<profile-name>`
- Update symlink: `ln -sfn ../profiles/<profile-name> .claude/active-profile`
- Parse config.yaml for imports and settings
- Load philosophy documents in order specified
- Display helpful context about new profile

## Safety Considerations
- Always confirm before switching
- Show what will change
- Don't switch in the middle of active work
- Suggest completing current tasks first
- Profile switch should be intentional, not accidental

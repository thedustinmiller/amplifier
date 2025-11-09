# File Organization Analysis & Refactoring Plan

## Executive Summary

This document analyzes the current markdown file structure in the Amplifier project after the profiles system refactoring. It identifies purposes, redundancies, and proposes a cleaned-up organization optimized for:

1. **Profile-based development** - Making it easy to compose and deploy subagents with specific profiles
2. **Clear separation of concerns** - Each file serves a single, well-defined purpose
3. **Symlink-based composition** - Using symlinks to make it easy to swap out or deploy subagents
4. **Externalizing the development process** - Making the system about grasping and externalizing metacognitive workflows

## Current File Inventory

### Root Level Documentation (`/working/`)

| File | Purpose | Issues | Recommendation |
|------|---------|--------|----------------|
| `README.md` | Main entry point for the project | Good - user-facing | **KEEP** |
| `AGENTS.md` | General AI assistant guidance (build commands, style, philosophy) | **DUPLICATES** content from ai_context files | **CONSOLIDATE** - This should be the SINGLE source for agent guidance |
| `CLAUDE.md` | Claude Code-specific entry point | Imports many files, acts as router | **REFACTOR** - Should be minimal, pointing to profile system |
| `AMPLIFIER_VISION.md` | High-level vision and goals | Good - strategic document | **KEEP** |
| `PROFILES_SYSTEM.md` | Overview of profiles system | Good - explains new architecture | **KEEP** |
| `PROFILES_TESTING_RESULTS.md` | Testing validation of profiles | Good - evidence of system working | **KEEP** (or **ARCHIVE**) |
| `ROADMAP.md` | Project roadmap | Good | **KEEP** |
| `DISCOVERIES.md` | Problem/solution knowledge base | Good - learning accumulation | **KEEP** |
| `DOCKER_README.md` | Docker-specific instructions | Good | **KEEP** |
| `CODE_OF_CONDUCT.md` | Community guidelines | Standard | **KEEP** |
| `SECURITY.md` | Security policy | Standard | **KEEP** |
| `SUPPORT.md` | Support policy | Standard | **KEEP** |

### AI Context Directory (`/working/ai_context/`)

| File/Dir | Purpose | Issues | Recommendation |
|----------|---------|--------|----------------|
| `IMPLEMENTATION_PHILOSOPHY.md` | Core implementation principles | **OVERLAPS** with AGENTS.md | **CONSOLIDATE** into AGENTS.md |
| `MODULAR_DESIGN_PHILOSOPHY.md` | Bricks & studs architecture | **OVERLAPS** with AGENTS.md | **CONSOLIDATE** into AGENTS.md |
| `DESIGN-PHILOSOPHY.md` | Design approach philosophy | Separate concern (design vs dev) | **KEEP** but organize |
| `DESIGN-PRINCIPLES.md` | Design principles | Separate concern (design vs dev) | **KEEP** but organize |
| `AMPLIFIER_CLAUDE_CODE_LEVERAGE.md` | How to leverage Claude Code features | Good reference | **KEEP** |
| `claude_code/` | Claude Code documentation copies | Reference material | **KEEP** organized |
| `design/` | Design framework docs | Design-specific | **KEEP** organized |
| `git_collector/` | External library docs | Reference material | **KEEP** |
| `module_generator/` | Module generation specs | Tool-specific | **KEEP** |
| `generated/` | Auto-generated content | Build artifact | **KEEP** |
| `README.md` | Directory explanation | Too minimal | **IMPROVE** |

### Claude Config Directory (`/working/.claude/`)

| File/Dir | Purpose | Issues | Recommendation |
|----------|---------|--------|----------------|
| `README.md` | Explains .claude architecture | Good | **KEEP** |
| `AGENT_PROMPT_INCLUDE.md` | **MISSING** (listed in ls output earlier but doesn't exist) | Confusion | **REMOVE** reference |
| `README_LOGS.md` | Log file documentation | Good | **KEEP** |
| `agents/` | Shared agent library | Core functionality | **KEEP** |
| `commands/` | Shared command library | Core functionality | **KEEP** |
| `tools/` | Automation scripts | Core functionality | **KEEP** |
| `settings.json` | Configuration | Core functionality | **KEEP** |
| `active-profile` | Symlink to active profile | Core functionality | **KEEP** |

### Profiles Directory (`/working/profiles/`)

| Profile | Purpose | Issues | Recommendation |
|---------|---------|--------|----------------|
| `default/` | Minimalist approach | Good | **KEEP** |
| `profile-editor/` | Meta-profile for editing profiles | Good | **KEEP** |
| `waterfall/` | Sequential phase-gate | Good | **KEEP** |
| `mathematical-elegance/` | Formal methods | Good | **KEEP** |
| `README.md` | Comprehensive profiles guide | Excellent | **KEEP** |

## Key Redundancies Identified

### 1. AGENTS.md vs ai_context Philosophy Files

**Problem**: The same principles appear in multiple files:
- `AGENTS.md` - Lines 419-714 contain implementation & modular design philosophy
- `ai_context/IMPLEMENTATION_PHILOSOPHY.md` - Contains similar content
- `ai_context/MODULAR_DESIGN_PHILOSOPHY.md` - Contains similar content

**Impact**: Updates must be made in 3 places, causing drift

**Solution**: Make `AGENTS.md` the SINGLE authoritative source, symlink from ai_context

### 2. Claude Code Documentation Duplication

**Problem**: Claude Code docs are cached in `ai_context/claude_code/`
**Impact**: May become stale
**Solution**: Keep for offline reference, but add date stamps and update process

### 3. Entry Point Confusion

**Problem**: Multiple entry points for AI:
- `CLAUDE.md` - Claude Code specific
- `AGENTS.md` - General AI guidance
- Profile PROFILE.md files - Profile-specific philosophy

**Impact**: Unclear what gets loaded when
**Solution**: Clear hierarchy and explicit loading order

## Proposed Organization Structure

### Core Principle: Profiles are the Primary Organizing Mechanism

```
working/
├── README.md                           # User-facing entry point
├── AGENTS.md                          # SINGLE SOURCE: AI agent guidance & philosophy
├── CLAUDE.md                          # Minimal: "Load profiles system, see AGENTS.md"
├── AMPLIFIER_VISION.md               # Strategic vision
├── PROFILES_SYSTEM.md                # Profiles system overview
├── ROADMAP.md                        # Project roadmap
├── DISCOVERIES.md                    # Learning accumulation
├── [standard files: CODE_OF_CONDUCT, SECURITY, SUPPORT, etc.]
│
├── .claude/
│   ├── README.md                      # Platform architecture
│   ├── settings.json                  # Configuration
│   ├── active-profile -> ../profiles/default/  # Current profile
│   ├── agents/                        # Shared agent library
│   ├── commands/                      # Shared command library
│   └── tools/                         # Automation scripts
│
├── profiles/                          # Profile system (NEW FOCUS)
│   ├── README.md                      # Comprehensive guide
│   ├── default/
│   │   ├── PROFILE.md                # Profile philosophy
│   │   ├── config.yaml               # Profile configuration
│   │   ├── agents/                   # Profile-specific agents
│   │   └── commands/                 # Profile-specific commands
│   ├── profile-editor/
│   ├── waterfall/
│   └── mathematical-elegance/
│
└── ai_context/                        # Reference & Supporting Materials
    ├── README.md                      # Improved: Explains organization
    ├── core/                          # NEW: Core philosophy (symlinked)
    │   ├── AGENTS.md -> ../../AGENTS.md           # Symlink to single source
    │   ├── IMPLEMENTATION_PHILOSOPHY.md -> ../../AGENTS.md  # Symlink for backwards compat
    │   └── MODULAR_DESIGN_PHILOSOPHY.md -> ../../AGENTS.md  # Symlink for backwards compat
    ├── design/                        # Design-specific philosophy
    │   ├── DESIGN-FRAMEWORK.md
    │   ├── DESIGN-VISION.md
    │   ├── DESIGN-PHILOSOPHY.md
    │   └── DESIGN-PRINCIPLES.md
    ├── claude_code/                   # Claude Code reference docs
    │   ├── README.md                  # Updated: When cached, update process
    │   ├── [docs...]
    │   └── sdk/
    ├── reference/                     # NEW: Renamed from git_collector
    │   └── [external library docs]
    └── tools/                         # NEW: Tool-specific context
        └── module_generator/
```

## Refactoring Plan

### Phase 1: Consolidate Philosophy Files

**Goal**: Single source of truth for core development philosophy

**Actions**:
1. ✅ Keep `AGENTS.md` as the authoritative source
2. ✅ Create `ai_context/core/` directory
3. ✅ Create symlinks from ai_context/core/ to AGENTS.md
4. ✅ Update all references to use AGENTS.md
5. ✅ Update CLAUDE.md to simplify imports

### Phase 2: Organize ai_context by Purpose

**Goal**: Clear organization of supporting materials

**Actions**:
1. ✅ Create `ai_context/core/` - Core philosophy (symlinks)
2. ✅ Move design files to `ai_context/design/`
3. ✅ Rename `git_collector/` to `reference/`
4. ✅ Move `module_generator/` to `ai_context/tools/`
5. ✅ Update `ai_context/README.md` with clear organization

### Phase 3: Simplify Entry Points

**Goal**: Clear loading hierarchy

**Actions**:
1. ✅ Simplify `CLAUDE.md` - Point to profiles system
2. ✅ Add clear comments explaining load order
3. ✅ Document in `AGENTS.md` what loads when

### Phase 4: Profile-Centric Agent Deployment

**Goal**: Make it easy to call subagents with specific profiles

**Current State**:
- Profiles load philosophy documents that shape thinking
- Subagents inherit the active profile's context
- No easy way to call a subagent with a DIFFERENT profile than active

**Enhancement**:
1. ✅ Create profile-specific agent invocation patterns
2. ✅ Document how to invoke agents with explicit profiles
3. ✅ Add examples to profiles/README.md
4. ✅ Consider: Allow Task tool to specify profile override

**Example Pattern**:
```markdown
# In a command or workflow:

# Call subagent with default profile's philosophy
Use the zen-architect agent with minimalist approach

# Call subagent with waterfall profile's philosophy
Use the requirements-analyst agent with waterfall methodology

# Call subagent with mathematical-elegance profile
Use the proof-architect agent with formal methods approach
```

## Benefits of New Organization

### 1. Single Source of Truth
- `AGENTS.md` is the authoritative source for development philosophy
- Changes propagate automatically via symlinks
- No drift between files

### 2. Clear Purpose Hierarchy
- Root: User-facing docs and strategic vision
- `.claude/`: Platform configuration and shared resources
- `profiles/`: Development methodology system
- `ai_context/`: Reference materials and supporting docs

### 3. Profile-First Mental Model
- Profiles are the primary way to shape AI behavior
- Easy to understand what philosophy is active
- Clear how to switch contexts

### 4. Easy Composition
- Symlinks enable flexible composition
- Profile-specific agents can override shared agents
- Commands can reference specific profiles

### 5. Subagent Deployment Flexibility
- Clear patterns for invoking agents with specific profiles
- Documentation of how profiles shape agent behavior
- Easy to experiment with different approaches

## Migration Checklist

- [ ] Phase 1: Consolidate Philosophy
  - [x] Create ai_context/core/
  - [x] Create symlinks to AGENTS.md
  - [ ] Update all imports in CLAUDE.md
  - [ ] Test that everything loads correctly

- [ ] Phase 2: Reorganize ai_context
  - [ ] Rename git_collector/ to reference/
  - [ ] Move module_generator/ to ai_context/tools/
  - [ ] Update ai_context/README.md
  - [ ] Update any references

- [ ] Phase 3: Simplify Entry Points
  - [ ] Simplify CLAUDE.md
  - [ ] Add loading order documentation to AGENTS.md
  - [ ] Test Claude Code session startup

- [ ] Phase 4: Document Profile-Agent Patterns
  - [ ] Add examples to profiles/README.md
  - [ ] Create usage guide for profile-specific agents
  - [ ] Update AGENTS.md with patterns

- [ ] Phase 5: Validation
  - [ ] Start fresh Claude Code session
  - [ ] Verify all documents load
  - [ ] Test profile switching
  - [ ] Test agent invocation with different profiles
  - [ ] Update documentation

## Success Criteria

- ✅ Zero duplicate content across files
- ✅ Clear, documented purpose for each file
- ✅ Obvious where to make changes
- ✅ Profile system is primary organizing mechanism
- ✅ Easy to understand what gets loaded when
- ✅ Simple patterns for invoking agents with specific profiles
- ✅ All symlinks work correctly
- ✅ Claude Code loads correctly with new organization

## Notes

- This refactoring aligns with the shift to "externalizing and grasping the development process"
- Focus on composition via profiles and symlinks
- Prioritize calling subagents of a given profile over hot-swapping
- Keep user-facing documentation simple and clear
- Internal organization optimized for AI consumption

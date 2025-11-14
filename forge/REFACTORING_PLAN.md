# Forge Refactoring Plan
## Date: 2025-11-14

## Project Scope Clarification
Forge is a **preprocessor/compiler** that:
1. Takes element specifications as input
2. Compiles specified elements into usable profiles
3. Enables launching agents and subagents with those profiles
4. Generates platform-specific artifacts (e.g., Claude Code `.claude/` files)

## Major Changes

### 1. Remove Constitutions Concept
- **Current State**: Constitutions defined in docs but never implemented
- **Action**: Remove from element type hierarchy, replace with principle
- **New Element**: `constitution-backed-design` principle
- **Rationale**: Lighter-weight, more composable than full constitutions

### 2. Clarify Coevolution
- **Current State**: Coevolution already exists as principle (correctly)
- **Action**: Keep as-is, update docs to emphasize it's a principle element
- **Note**: No "coevolution language" exists or needs to be created

### 3. Add AI/Agent Distinction for Tools
- **Current State**: Tools exist but purpose not explicitly stated
- **Action**: Document that tools are for AI/agent use
- **Update**: Tool element type spec and all tool elements

### 4. Create Command Element Type
- **Purpose**: User-facing commands that execute pipelines
- **Example**: `/ultrathink-task` - carries out pipeline per current profile
- **Distinction**: Commands are for users, tools are for agents
- **Format**: Similar to Claude Code slash commands

### 5. Add Orthogonal Elements
- **Goal**: Enable diverse, contrasting behaviors through composition
- **Current Problem**: Many elements synergize but lack orthogonal options
- **Target**: 5-7 new elements that create different behavior axes

## Implementation Phases

### Phase 1: Documentation Foundation (Tasks 3-4)
- Update README.md with preprocessor/compiler model
- Update element-types.md to remove constitutions, add commands
- Update hierarchy diagrams

### Phase 2: Constitution Changes (Task 5-6)
- Create `constitution-backed-design` principle
- Update catalog and cross-references
- Archive old constitution documentation

### Phase 3: Tools Clarification (Task 7)
- Update tool element type documentation
- Add "AI/Agent Use" section to each tool element
- Update tool descriptions in catalog

### Phase 4: Command Element Type (Tasks 8-9)
- Design command element specification
- Create `/ultrathink-task` command as reference
- Update Python core to support commands
- Update CLI to handle command generation

### Phase 5: Orthogonal Elements (Tasks 10-11)
- Design 5-7 new orthogonal elements
- Implement elements with full metadata
- Create example compositions showing diversity

### Phase 6: Integration (Tasks 12-13)
- Update ELEMENT_CATALOG.md
- Update all cross-references
- Validate consistency
- Run test suite
- Commit and push

## Orthogonal Element Ideas (To Be Refined)

### Behavior Axes to Create:
1. **Speed vs Thoroughness**: fast-iteration vs deep-analysis
2. **Autonomy vs Guidance**: autonomous-execution vs user-confirmation
3. **Verbosity vs Concision**: detailed-explanation vs minimal-output
4. **Exploration vs Exploitation**: wide-search vs focused-refinement
5. **Risk vs Safety**: experimental-features vs conservative-approach
6. **Monolithic vs Modular**: integrated-solutions vs decoupled-components
7. **Documentation**: verbose-documentation vs code-as-documentation

## Success Criteria
- [ ] Preprocessor/compiler model clearly documented
- [ ] No references to constitutions as element type
- [ ] `constitution-backed-design` principle exists
- [ ] All tools marked for AI/agent use
- [ ] Command element type fully specified
- [ ] `/ultrathink-task` command implemented
- [ ] 5-7 orthogonal elements created
- [ ] All documentation updated and consistent
- [ ] Tests pass
- [ ] Changes committed and pushed

## Subagent Strategy
- Use specialized agents for:
  - Python code updates (CLI/core)
  - Element creation (repetitive structure)
  - Documentation consistency checks
  - Catalog updates

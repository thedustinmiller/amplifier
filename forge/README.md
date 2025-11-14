# Forge: A Composable AI Development System

**Forge** is a **preprocessor/compiler for AI agent profiles**. It compiles specified elements into usable configurations that launch agents and subagents with tailored behaviors.

Think of Forge as:
- **Input**: Element specifications (principles, tools, commands, agents, templates)
- **Process**: Composition and compilation into platform-specific profiles
- **Output**: Agent configurations ready for execution (e.g., Claude Code `.claude/` directories)

Forge learns from both Amplifier and Spec-Kit while embracing a fundamental truth: **specifications and code coevolve**. Neither is purely authoritative—requirements crystallize through the act of implementation.

## Core Philosophy

### 1. Coevolution, Not Dichotomy
Traditional approaches force a false choice:
- **Code-first**: Specs become stale documentation
- **Spec-first**: Reality diverges from the plan

**Forge's approach**: Specs and code are **conversation partners**. Each informs the other. The project emerges from their dialogue.

### 2. Radical Composition
Everything is an element. Elements combine into compositions. Compositions can become elements. There's no "core" that can't be replaced.

### 3. Hierarchy of Influence
```
Foundations (Why)
    ↓ constrain
Elements (What)
    ↓ assemble into
Compositions (How)
    ↓ observed by
Meta (Improve)
```

### 4. Non-Prescriptive by Design
- No default profile
- No recommended workflow
- No "best practices" enshrined
- Users compose their own methodology from elements

### 5. Agent-Agnostic Architecture
Implements for Claude Code today. Works with any AI tomorrow. Knowledge outlives platforms.

### 6. Pluggable Everything
Memory, agents, tools, templates—all pluggable. Start simple, scale to production.

## Architecture

### Compilation Model

Forge operates as a **preprocessor/compiler**:
1. **Load** element specifications from library
2. **Compose** elements according to user selection
3. **Resolve** dependencies and detect conflicts
4. **Compile** into platform-specific artifacts
5. **Deploy** as agent profiles ready for execution

### Element Hierarchy

#### Layer 1: Foundations
**Principles - Philosophical Stances**
- Define "why" and high-level constraints
- Constrain decision-making without prescribing implementation
- Examples:
  - `ruthless-minimalism.md` - Ship fast, adapt
  - `constitution-backed-design.md` - Governance through immutable rules
  - `specification-driven.md` - Specs as source of truth
  - `coevolution.md` - Specs and code dialogue

#### Layer 2: Elements
**Atomic, Reusable Building Blocks**
- **Principles**: Philosophical guidelines that constrain decisions
- **Tools**: Executable capabilities for AI/agent use
- **Commands**: User-facing executable pipelines (e.g., slash commands)
- **Agents**: Specialized AI intelligences
- **Templates**: Structured documents and formats
- **Hooks**: Event-driven automation triggers
- **Queries**: Memory interaction patterns

Each element:
- Self-contained
- Declares dependencies
- Exposes clear interface
- Can be composed freely

#### Layer 3: Compositions
**Assemblies of Elements**
- **Presets**: Pre-configured element bundles (like profiles)
- **Workflows**: Ordered sequences of tools
- **Orchestrations**: Agent coordination patterns
- **Methodologies**: Complete development approaches

Compositions are **just elements** that reference other elements. No special status.

#### Layer 4: Meta
**System for Creating and Evolving**
- **Composer**: Interactive element assembly
- **Analyzer**: Evaluate effectiveness
- **Generator**: Create new elements from patterns
- **Evolver**: Suggest improvements

### Memory System

#### Abstract Interface
```python
class MemoryProvider(Protocol):
    async def get(self, key: str, scope: Scope) -> Optional[str]
    async def set(self, key: str, value: str, scope: Scope) -> None
    async def query(self, pattern: str, scope: Scope) -> List[str]
    async def search(self, semantic: str, scope: Scope) -> List[tuple[str, float]]
```

#### Scopes
- **Session**: Current working context (ephemeral)
- **Project**: Project-specific memory (persistent)
- **Global**: Cross-project learnings (permanent)

#### Providers
- **FileProvider**: Simple file-based (start here)
- **GraphProvider**: Relationships between concepts
- **VectorProvider**: Semantic search (embeddings)
- **RelationalProvider**: Structured queries (SQL)
- **HybridProvider**: Combine multiple backends

### Composition System

#### Element Declaration (`element.yaml`)
```yaml
element:
  name: zen-architect
  type: agent
  version: 1.0.0

dependencies:
  principles:
    - ruthless-minimalism
    - emergent-design
  tools:
    - code-review
  templates:
    - minimal-plan

interface:
  inputs:
    - problem_description
    - constraints
  outputs:
    - architectural_direction
    - minimal_implementation_plan

metadata:
  author: community
  tags: [design, minimalism, architecture]
  license: MIT
```

#### Composition Declaration (`composition.yaml`)
```yaml
composition:
  name: rapid-prototype
  type: preset
  description: "Fast iteration with emergent design"

elements:
  principles:
    - ruthless-minimalism
    - coevolution
    - test-when-needed

  tools:
    - quick-scaffold
    - live-reload
    - commit

  commands:
    - ultrathink-task
    - rapid-iterate

  agents:
    - zen-architect
    - bug-hunter

  hooks:
    - session-start: load-context
    - pre-commit: quick-check

settings:
  memory_provider: file
  memory_scopes: [session, project]
  agent_orchestration: sequential
```

#### Dynamic Assembly
Users can:
```bash
# Start with a preset
forge init --preset rapid-prototype

# Add elements on the fly
forge add principle formal-verification
forge add agent test-coverage

# Remove elements
forge remove tool live-reload

# Save as new preset
forge save-preset my-hybrid-approach

# Mix multiple presets
forge compose rapid-prototype + specification-driven - waterfall

# Query what's active
forge active
```

## Coevolution in Practice

### The Dialogue Pattern
1. **Sketch Spec**: Write rough specification (WHAT)
2. **Prototype**: Implement quickly (HOW)
3. **Discover**: Find gaps, ambiguities, impossibilities
4. **Refine Spec**: Update based on reality
5. **Improve Code**: Incorporate learnings
6. **Repeat**: Spiral toward coherence

### Memory Captures Both
- **Specs**: Intentions, goals, requirements
- **Code**: Implementations, constraints, solutions
- **Decisions**: Why something was chosen
- **Learnings**: What worked, what didn't

Neither is authoritative. Both inform future decisions.

## Implementation Strategy

### Phase 1: Core Abstractions
- [ ] Element system (declaration, loading, validation)
- [ ] Memory provider interface
- [ ] File-based memory implementation
- [ ] Composition engine

### Phase 2: Essential Elements
Decompose amplifier defaults:
- [ ] Principles: ruthless-minimalism, emergent-design, coevolution
- [ ] Tools: scaffold, commit, review
- [ ] Agents: zen-architect, bug-hunter
- [ ] Templates: minimal-spec, quick-plan

### Phase 3: Claude Code Integration (Compilation Target)
- [ ] Compile compositions to `.claude/` directories
- [ ] Generate slash commands from command elements
- [ ] Generate agent prompts from agent elements
- [ ] Generate tool scripts for AI/agent use
- [ ] Implement hooks as event triggers

### Phase 4: Meta System
- [ ] Composer for interactive assembly
- [ ] Analyzer for effectiveness evaluation
- [ ] Generator for new elements

### Phase 5: Advanced Providers
- [ ] Graph memory (relationships)
- [ ] Vector memory (semantic search)
- [ ] Hybrid memory (best of all)

## Design Decisions

### Why "Forge"?
A forge is where raw materials are shaped through heat and pressure. This system **forges** software through the creative tension between intention (specs) and reality (code).

### Why No Default Preset?
Prescribing a default methodology undermines the core philosophy. Users must consciously choose or compose their approach.

### Why Decompose Everything?
Maximum reuse. Minimal duplication. Easy experimentation. Clear understanding.

### Why Pluggable Memory?
Start simple (files). Scale when needed (graphs, vectors). Different projects have different needs. One size doesn't fit all.

## Getting Started

```bash
# Initialize a new project
forge init

# You'll be prompted to compose your approach:
# "What principles guide your work?"
# "What tools do you need?"
# "Which agents assist you?"

# Or compose manually:
forge add principle coevolution
forge add tool scaffold
forge add agent zen-architect

# Start working:
forge session start

# Elements guide the AI based on your composition
# Memory accumulates across sessions
# Meta-tools help you evolve your approach
```

## Differences from Amplifier and Spec-Kit

### vs Amplifier
- **No profiles**: Everything is elements + compositions
- **No defaults**: User composes from scratch
- **Pluggable memory**: Not just file-based
- **Meta generates**: Don't just analyze, create new elements

### vs Spec-Kit
- **Coevolution**: Not spec-first, but spec-code dialogue
- **No prescribed workflow**: 5 steps is ONE composition, not THE way
- **Agent-agnostic**: Like Spec-Kit, but compositional

### Synthesis
- **From Amplifier**: Meta-development, memory system, agent orchestration
- **From Spec-Kit**: Constitutional governance, templates, multi-agent support
- **New**: Radical composition, pluggable memory, coevolution philosophy

## License

MIT - Use freely, modify wildly, share openly.

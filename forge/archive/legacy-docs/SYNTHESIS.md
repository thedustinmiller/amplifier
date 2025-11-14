# Forge: Synthesis of Amplifier and Spec-Kit

## Overview

Forge is a greenfield project that synthesizes learnings from both Amplifier and Spec-Kit while addressing key philosophical insights:

1. **Specs and code coevolve** - Neither is purely authoritative
2. **Radical composition** - Everything is decomposed into reusable elements
3. **Non-prescriptive by design** - No default methodology
4. **Hierarchy of influence** - Clear levels from principles to meta-tools
5. **Agent-agnostic** - Works with any AI platform
6. **Pluggable everything** - Memory, tools, agents all swappable

## Key Differences from Previous Approaches

### From Amplifier

**What We Kept**:
- ✅ Meta-development philosophy (system improves itself)
- ✅ Memory system with scopes (session/project/global)
- ✅ Agent orchestration patterns
- ✅ Hub-and-spoke architecture
- ✅ Non-prescriptive approach

**What We Changed**:
- ❌ Profiles → Elements + Compositions (more granular)
- ❌ File-only memory → Pluggable providers
- ❌ Claude Code specific → Agent-agnostic core
- ❌ Implicit defaults → Everything explicit

**Why**:
- More composable (mix individual elements, not just profiles)
- More scalable (plug in databases when needed)
- More portable (works with any AI)
- More honest (no hidden assumptions)

### From Spec-Kit

**What We Kept**:
- ✅ Constitutional governance (immutable principles)
- ✅ Template-driven quality
- ✅ Multi-agent support
- ✅ Structured artifacts

**What We Changed**:
- ❌ Specs as source of truth → Coevolution (specs ↔ code dialogue)
- ❌ 5-step workflow → One composition among many
- ❌ Prescriptive process → Composable elements

**Why**:
- More pragmatic (acknowledges reality of software development)
- More flexible (no forced workflow)
- More honest (requirements often emerge through implementation)

## Core Innovations

### 1. Coevolution Principle

**Traditional approaches force a choice**:
- Code-first: Specs become stale
- Spec-first: Reality diverges from plan

**Forge recognizes**:
- Most projects don't start with clarity
- Requirements crystallize through implementation
- Specs and code are conversation partners
- Both inform future decisions

**In practice**:
```
Sketch Spec → Prototype → Discover gaps → Refine Spec → Improve Code → Repeat
```

### 2. Element Hierarchy

```
Layer 1: Foundations (Why)
  - Principles: Core values and constraints
  - Constitutions: Immutable governance rules

Layer 2: Elements (What)
  - Tools: Executable capabilities
  - Agents: Specialized intelligence
  - Templates: Structured documents
  - Hooks: Event-driven automation
  - Queries: Memory patterns

Layer 3: Compositions (How)
  - Presets: Pre-configured bundles
  - Workflows: Ordered sequences
  - Orchestrations: Agent patterns
  - Methodologies: Complete approaches

Layer 4: Meta (Improve)
  - Composer: Assemble elements
  - Analyzer: Evaluate effectiveness
  - Generator: Create new elements
  - Evolver: Suggest improvements
```

### 3. Pluggable Memory

**Why pluggable?**
Different projects need different backends:
- Prototype → File storage
- Production → Relational database
- AI-heavy → Vector store
- Complex domain → Graph database

**Interface**:
```python
class MemoryProvider(Protocol):
    async def get(key, scope) -> Entry
    async def set(key, value, scope) -> None
    async def query(pattern, scope) -> List[Entry]
    async def search(semantic, scope) -> List[(Entry, score)]
```

**Providers**:
- `FileProvider`: Simple JSON files
- `GraphProvider`: Neo4j relationships
- `VectorProvider`: Semantic search
- `RelationalProvider`: PostgreSQL
- `HybridProvider`: Best of all

### 4. Radical Composition

**Everything is composable**:
- Elements declare dependencies
- Compositions assemble elements
- No "core" that can't be replaced
- Mix and match freely

**Example**:
```yaml
composition:
  name: my-approach
  elements:
    principles:
      - ruthless-minimalism  # From amplifier
      - coevolution          # New
      - test-first           # Custom
    tools:
      - scaffold
      - commit
    agents:
      - zen-architect
```

### 5. No Defaults

**Why no default preset?**
- Prescribing a methodology undermines the philosophy
- Users must consciously choose
- Forces thinking about what you actually need
- No hidden assumptions

**In practice**:
```bash
# Must explicitly compose
forge init  # Prompts: "What principles guide you?"

# Or use a preset
forge init --preset rapid-prototype

# Or compose manually
forge add principle coevolution
forge add tool scaffold
```

## Relationship to Original Projects

### Amplifier Evolution

Forge is **Amplifier 2.0** - learning from v1:

**What worked**:
- Non-prescriptive philosophy
- Memory system
- Meta-development

**What needed improvement**:
- Too Claude Code specific
- Profiles too coarse-grained
- Memory too simple (files only)
- Some implicit defaults

**Forge addresses**:
- Agent-agnostic core
- Fine-grained elements
- Pluggable memory
- Everything explicit

### Spec-Kit Integration

Spec-Kit's methodology becomes **one composition**:

`presets/specification-driven/composition.yaml`:
```yaml
composition:
  name: specification-driven
  description: Spec-Kit's 5-step workflow

elements:
  constitutions:
    - test-first-mandatory
  tools:
    - speckit-constitution
    - speckit-specify
    - speckit-plan
    - speckit-tasks
    - speckit-implement
  templates:
    - spec-template
    - plan-template
    - tasks-template
```

**Key difference**: `coevolution` replaces `specs-as-source-of-truth`:
```yaml
  principles:
    - coevolution  # Specs and code inform each other
    # NOT: spec-driven-absolute
```

## Usage Patterns

### Pattern 1: Rapid Prototyping

```yaml
composition:
  name: rapid-prototype
  elements:
    principles: [ruthless-minimalism, coevolution]
    tools: [scaffold, commit]
    agents: [zen-architect]
  settings:
    memory: {provider: file}
```

Use when:
- Greenfield exploration
- Solo developer
- Fast iteration

### Pattern 2: Structured Development

```yaml
composition:
  name: structured-dev
  elements:
    principles: [coevolution, test-first]
    constitutions: [mandatory-tests]
    tools: [speckit-specify, speckit-plan, speckit-implement]
    templates: [spec-template, plan-template]
  settings:
    memory: {provider: relational}
```

Use when:
- Team project
- Need coordination
- Quality gates

### Pattern 3: Hybrid Approach

```yaml
composition:
  name: hybrid
  elements:
    principles: [ruthless-minimalism, coevolution, test-first]
    tools: [scaffold, speckit-specify, commit]
    agents: [zen-architect]
```

Mix rapid prototyping with structured specs.

## Migration Path

### From Amplifier

1. **Elements**: Extract from profiles
   ```
   profiles/default/ → elements/principle/ruthless-minimalism/
   ```

2. **Compositions**: Convert profiles
   ```
   profiles/default/config.yaml → presets/rapid-prototype/composition.yaml
   ```

3. **Memory**: Use file provider initially
   ```yaml
   memory: {provider: file, config: {base_path: .forge/memory}}
   ```

### From Spec-Kit

1. **Constitution**: Becomes element
   ```
   memory/constitution.md → elements/constitution/test-first-mandatory/
   ```

2. **Workflow**: Becomes composition
   ```
   5-step workflow → presets/specification-driven/composition.yaml
   ```

3. **Templates**: Become elements
   ```
   templates/spec-template.md → elements/template/spec-template/
   ```

## Design Decisions

### Why "Forge"?

A forge shapes raw materials through heat and pressure. This system **forges** software through creative tension between intention (specs) and reality (code).

### Why Coevolution over Spec-First?

Reality: Most projects don't have clear requirements upfront. Requirements emerge through implementation. Acknowledging this makes us more pragmatic.

### Why No Default Preset?

Prescribing a default undermines the core philosophy. Users must consciously choose their approach. Forces thinking.

### Why Pluggable Memory?

Start simple (files). Scale when needed (graphs, vectors). Different projects have different needs. No one-size-fits-all.

### Why Element Hierarchy?

Clear levels of influence:
- Principles constrain elements
- Elements assemble into compositions
- Compositions are observed by meta-tools
- Meta-tools improve principles

Loop closes.

## Future Evolution

### Phase 1: Core (Completed)
- ✅ Element system
- ✅ Composition system
- ✅ File memory provider
- ✅ Core principles (ruthless-minimalism, coevolution)

### Phase 2: Elements (Next)
- [ ] More principles (emergent-design, test-first, etc.)
- [ ] Core tools (scaffold, commit, review)
- [ ] Core agents (zen-architect, bug-hunter)
- [ ] Core templates (minimal-spec, quick-plan)

### Phase 3: Providers (Future)
- [ ] Graph memory provider (Neo4j)
- [ ] Vector memory provider (Pinecone/Chroma)
- [ ] Relational memory provider (PostgreSQL)
- [ ] Hybrid memory provider

### Phase 4: Meta (Future)
- [ ] Composer (interactive element assembly)
- [ ] Analyzer (evaluate effectiveness)
- [ ] Generator (create new elements)
- [ ] Evolver (suggest improvements)

### Phase 5: Integration (Future)
- [ ] Claude Code integration
- [ ] Cursor integration
- [ ] GitHub Copilot integration
- [ ] Multi-agent workflows

## Success Criteria

We'll know Forge succeeds when:

1. ✓ Users compose custom methodologies easily
2. ✓ No one asks "what's the default?" (wrong question)
3. ✓ Elements are shared and remixed
4. ✓ Memory providers are swapped based on needs
5. ✓ System improves itself (meta-loop working)
6. ✓ Works across AI platforms (agent-agnostic)
7. ✓ Users say: "I can't imagine building without composing"

## Philosophy Statement

**Forge provides building blocks, not prescriptions.**

- We don't tell you how to develop software
- We give you elements to compose your own way
- We make the development process explicit and mutable
- We embrace uncertainty (coevolution)
- We start simple (files, minimalism)
- We scale when needed (graphs, vectors, relations)
- We improve continuously (meta-development)

**The system practices what it preaches**: coevolution (design emerges through use), minimalism (start simple), composition (build from parts), meta-development (improve itself).

## License

MIT - Use freely, modify wildly, share openly.

## Acknowledgments

This project stands on the shoulders of:
- **Amplifier**: Meta-development philosophy, memory system, non-prescriptive approach
- **Spec-Kit**: Constitutional governance, templates, multi-agent support
- **The pragmatic reality**: That most projects don't start with clarity, and that's okay

Thank you to the authors of both projects for showing different paths. Forge attempts to synthesize the best of both while adding new insights.

# Element Types

Elements are the atomic building blocks of Forge. Each type serves a specific purpose in the hierarchy.

## Hierarchy Visualization

```
┌─────────────────────────────────────────────┐
│ FOUNDATIONS (Layer 1: Why)                  │
│ - Principles: Core values and constraints   │
│ - Constitutions: Immutable governance rules │
├─────────────────────────────────────────────┤
│ ELEMENTS (Layer 2: What)                    │
│ - Tools: Executable capabilities            │
│ - Agents: Specialized intelligence          │
│ - Templates: Structured documents           │
│ - Hooks: Event-driven automation            │
│ - Queries: Memory interaction patterns      │
├─────────────────────────────────────────────┤
│ COMPOSITIONS (Layer 3: How)                 │
│ - Presets: Bundled elements                 │
│ - Workflows: Sequenced tools                │
│ - Orchestrations: Agent patterns            │
│ - Methodologies: Complete approaches        │
├─────────────────────────────────────────────┤
│ META (Layer 4: Improve)                     │
│ - Composer: Assemble elements               │
│ - Analyzer: Evaluate effectiveness          │
│ - Generator: Create new elements            │
│ - Evolver: Suggest improvements             │
└─────────────────────────────────────────────┘
```

## Layer 1: Foundations

### Principles
**Purpose**: Define core values and philosophical stances that guide decision-making.

**Format**: Markdown document with structured sections.

**Structure**:
```markdown
# Principle: {Name}

## Core Tenet
One-sentence summary of the principle.

## Motivation
Why this principle matters.

## Implications
What this principle means in practice.

## Trade-offs
What you sacrifice by following this principle.

## Conflicts
Which other principles this might conflict with.

## Examples
Concrete scenarios where this principle applies.
```

**Example: `ruthless-minimalism.md`**
```markdown
# Principle: Ruthless Minimalism

## Core Tenet
Ship the simplest thing that could possibly work, then adapt based on real needs.

## Motivation
Complexity is expensive. Time spent building features nobody needs is wasted.
The best way to discover what's actually needed is to ship fast and learn.

## Implications
- Defer features until pain is real
- Delete code aggressively
- Reject abstractions until duplication hurts
- Measure in hours, not weeks

## Trade-offs
- Less upfront planning
- May require rewrites
- Reduced predictability
- Not suitable for safety-critical systems

## Conflicts
- Conflicts with: formal-verification, waterfall, predictability
- Synergizes with: emergent-design, coevolution, rapid-feedback

## Examples
- MVP: User auth with email/password only (defer OAuth until requested)
- Data: SQLite file (defer to PostgreSQL when scale demands it)
- UI: Plain HTML forms (defer to React when interactivity needed)
```

### Constitutions
**Purpose**: Immutable governance rules that apply across entire project.

**Format**: Numbered articles with clear violation criteria.

**Structure**:
```markdown
# Constitution: {Name}

## Preamble
Why this constitution exists.

## Article I: {Rule Name}
**Rule**: Clear statement
**Rationale**: Why this rule
**Validation**: How to check compliance
**Exceptions**: When allowed (if ever)
**Penalty**: What happens on violation

## Article II: ...
```

**Example: `article-test-first.md`**
```markdown
# Constitution: Test-First Development

## Preamble
Tests written after implementation are biased by the implementation.
Test-first ensures we think about contracts before coding.

## Article I: Test-First Mandatory
**Rule**: All functionality must have failing tests before implementation.

**Rationale**:
- Forces API thinking before coding
- Prevents untestable designs
- Provides regression protection from day 1

**Validation**:
- Commit history shows test file before implementation
- Pre-commit hook verifies test existence
- No implementation PR accepted without tests

**Exceptions**:
- Exploratory spikes (must be deleted or retroactively tested)
- Generated code (tests apply to generator)

**Penalty**:
- CI fails
- PR blocked
- Implementation must be revised
```

## Layer 2: Elements

### Tools
**Purpose**: Executable capabilities that perform specific tasks.

**Types**:
- **Commands**: User-invoked operations (e.g., `/commit`, `/scaffold`)
- **Scripts**: Automation scripts (e.g., `pre-commit`, `deploy`)
- **Utilities**: Helper functions (e.g., `parse-yaml`, `validate-markdown`)

**Declaration** (`tool.yaml`):
```yaml
tool:
  name: quick-scaffold
  type: command
  version: 1.0.0

dependencies:
  principles:
    - ruthless-minimalism
  templates:
    - minimal-structure

interface:
  inputs:
    - project_name: string
    - language: string (optional, default: python)
  outputs:
    - directory_path: string
    - files_created: list[string]

implementation:
  type: python
  entry_point: tools/scaffold/main.py

metadata:
  description: "Create minimal project structure"
  usage: "forge tool quick-scaffold --name myproject"
  author: core
  tags: [scaffolding, initialization]
```

**Implementation** (`tools/scaffold/main.py`):
```python
"""Quick scaffolding tool."""
from forge.core import Tool, Context

class QuickScaffold(Tool):
    """Create minimal project structure."""

    async def execute(self, ctx: Context, name: str, language: str = "python"):
        """Execute scaffolding."""
        # Check principles
        minimalism = await ctx.principles.get("ruthless-minimalism")

        # Use template
        template = await ctx.templates.get("minimal-structure")

        # Generate structure
        structure = template.render(name=name, language=language)

        # Write files
        files = await ctx.files.write_tree(structure)

        # Log to memory
        await ctx.memory.set(
            key=f"projects/{name}/scaffold",
            value=f"Created with {len(files)} files",
            scope="global"
        )

        return {
            "directory_path": f"./{name}",
            "files_created": files
        }
```

### Agents
**Purpose**: Specialized intelligence that provides perspective or performs complex reasoning.

**Declaration** (`agent.yaml`):
```yaml
agent:
  name: zen-architect
  type: perspective
  version: 1.0.0

dependencies:
  principles:
    - ruthless-minimalism
    - emergent-design
  tools:
    - code-review

interface:
  role: |
    You are a minimalist architect. You see complexity as the enemy.
    You always ask: "What's the simplest thing that could work?"

  inputs:
    - problem_description: string
    - current_solution: string (optional)

  outputs:
    - architectural_direction: string
    - simplification_suggestions: list[string]
    - minimal_implementation_plan: string

prompts:
  system: |
    You are the Zen Architect. Your core principles:

    {{load_principle("ruthless-minimalism")}}
    {{load_principle("emergent-design")}}

    When presented with a problem:
    1. Identify the absolute minimum needed
    2. Defer everything else
    3. Suggest the simplest possible implementation
    4. Point out unnecessary complexity

  constraints: |
    - Never suggest frameworks unless absolutely necessary
    - Prefer boring, proven solutions
    - Avoid abstractions until duplication hurts
    - Think in hours, not weeks

metadata:
  description: "Minimalist design perspective"
  author: core
  tags: [design, minimalism, architecture]
```

**Usage**:
```bash
# Invoke via CLI
forge agent zen-architect "Design user authentication"

# Use in composition
# Agent automatically loaded based on active preset
```

### Templates
**Purpose**: Structured documents that guide content creation.

**Declaration** (`template.yaml`):
```yaml
template:
  name: minimal-spec
  type: document
  version: 1.0.0

dependencies:
  principles:
    - coevolution
    - ruthless-minimalism

interface:
  inputs:
    - feature_name: string
    - priority: string (p0|p1|p2)

  outputs:
    - spec_document: string

metadata:
  description: "Minimal specification template"
  author: core
  tags: [documentation, specification]
```

**Content** (`templates/minimal-spec/template.md`):
```markdown
# Spec: {{feature_name}}

**Priority**: {{priority}}
**Status**: Draft
**Updated**: {{now}}

## Problem
What problem are we solving? (2-3 sentences max)

## Solution
What's the simplest thing that could work? (1 paragraph)

## Non-Goals
What are we explicitly NOT building? (bullet list)

## Open Questions
What don't we know yet? (will be answered through implementation)

## Success
How do we know it works? (1-2 concrete tests)

---

*This spec will evolve as we implement. Code and spec inform each other.*
```

### Hooks
**Purpose**: Event-driven automation that responds to system events.

**Types**:
- **Lifecycle**: `session-start`, `session-end`
- **Interaction**: `pre-tool`, `post-tool`, `pre-commit`, `post-commit`
- **Memory**: `memory-write`, `memory-query`
- **Custom**: User-defined events

**Declaration** (`hook.yaml`):
```yaml
hook:
  name: load-context
  type: session-start
  version: 1.0.0

dependencies:
  tools:
    - memory-query

interface:
  events:
    - session-start

  inputs:
    - session_id: string
    - project_path: string

  outputs:
    - context_loaded: bool
    - principles_active: list[string]
    - tools_available: list[string]

implementation:
  type: python
  entry_point: hooks/load_context.py

metadata:
  description: "Load project context at session start"
  author: core
  tags: [lifecycle, context]
```

**Implementation** (`hooks/load_context.py`):
```python
"""Load context hook."""
from forge.core import Hook, Context

class LoadContext(Hook):
    """Load project context at session start."""

    async def on_session_start(self, ctx: Context, session_id: str, project_path: str):
        """Load active composition and memory."""
        # Load composition
        composition = await ctx.files.read_yaml(f"{project_path}/.forge/active.yaml")

        # Activate elements
        for principle in composition.get("elements", {}).get("principles", []):
            await ctx.principles.load(principle)

        for tool in composition.get("elements", {}).get("tools", []):
            await ctx.tools.register(tool)

        # Load memory
        memory_config = composition.get("settings", {}).get("memory", {})
        provider_type = memory_config.get("provider", "file")
        await ctx.memory.initialize(provider_type, project_path)

        # Query recent context
        recent = await ctx.memory.query("session:*", scope="project", limit=5)

        # Make available to AI
        await ctx.ai.add_context({
            "active_principles": composition.get("elements", {}).get("principles", []),
            "active_tools": composition.get("elements", {}).get("tools", []),
            "recent_sessions": recent
        })

        return {
            "context_loaded": True,
            "principles_active": composition.get("elements", {}).get("principles", []),
            "tools_available": composition.get("elements", {}).get("tools", [])
        }
```

### Queries
**Purpose**: Patterns for interacting with memory.

**Declaration** (`query.yaml`):
```yaml
query:
  name: recent-decisions
  type: pattern
  version: 1.0.0

interface:
  inputs:
    - days_back: int (default: 7)

  outputs:
    - decisions: list[Decision]

implementation:
  type: template
  pattern: |
    SELECT * FROM memory
    WHERE key LIKE 'decision:%'
    AND timestamp > NOW() - INTERVAL '{{days_back}} days'
    ORDER BY timestamp DESC

metadata:
  description: "Query recent project decisions"
  author: core
  tags: [memory, decision]
```

## Layer 3: Compositions

### Presets
**Purpose**: Pre-configured bundles of elements.

**Declaration** (`composition.yaml`):
```yaml
composition:
  name: rapid-prototype
  type: preset
  version: 1.0.0
  description: "Fast iteration with emergent design"

elements:
  principles:
    - ruthless-minimalism
    - coevolution
    - emergent-design

  tools:
    - quick-scaffold
    - live-reload
    - commit

  agents:
    - zen-architect
    - bug-hunter

  templates:
    - minimal-spec
    - quick-plan

  hooks:
    - load-context: session-start
    - quick-check: pre-commit

  queries:
    - recent-decisions
    - session-context

settings:
  memory:
    provider: file
    scopes: [session, project]

  agent_orchestration:
    mode: sequential
    max_parallel: 3

  tool_defaults:
    commit:
      auto_message: true
    scaffold:
      language: python

metadata:
  description: "Ship fast, adapt based on reality"
  author: core
  tags: [rapid, prototyping, minimalism]
  recommended_for:
    - Greenfield projects
    - Exploration phase
    - Solo developers
```

### Workflows
**Purpose**: Ordered sequences of tools.

**Declaration** (`workflow.yaml`):
```yaml
workflow:
  name: quick-feature
  type: sequence
  version: 1.0.0

dependencies:
  tools:
    - quick-scaffold
    - commit
  agents:
    - zen-architect
  templates:
    - minimal-spec

steps:
  - name: sketch_spec
    tool: template
    args:
      template: minimal-spec
      feature_name: "{{input.feature}}"

  - name: get_perspective
    agent: zen-architect
    args:
      problem: "{{steps.sketch_spec.output}}"

  - name: prototype
    tool: quick-scaffold
    args:
      name: "{{input.feature}}"
      guidance: "{{steps.get_perspective.output}}"

  - name: commit_work
    tool: commit
    args:
      message: "Prototype {{input.feature}}"

metadata:
  description: "Quickly prototype a feature"
  author: core
  tags: [workflow, rapid, feature]
```

## Layer 4: Meta

### Composer
**Purpose**: Interactive element assembly.

**Capabilities**:
- Browse available elements
- Preview combinations
- Resolve conflicts
- Save as presets

### Analyzer
**Purpose**: Evaluate effectiveness.

**Capabilities**:
- Track tool usage
- Measure velocity
- Identify patterns
- Suggest optimizations

### Generator
**Purpose**: Create new elements from patterns.

**Capabilities**:
- Extract common patterns
- Generate element declarations
- Create implementations
- Test and validate

### Evolver
**Purpose**: Suggest improvements.

**Capabilities**:
- Analyze outcomes
- Compare approaches
- Recommend changes
- Auto-update elements

## Element Lifecycle

### Creation
1. Author declares element (YAML)
2. Implement if needed (code/markdown)
3. Tag with metadata
4. Submit for inclusion

### Discovery
1. User searches/browses elements
2. System suggests relevant elements
3. Dependencies automatically resolved

### Activation
1. User adds element to composition
2. System loads dependencies
3. Element becomes available
4. Context updated

### Evolution
1. Usage tracked
2. Effectiveness measured
3. Improvements suggested
4. New version released

## Dependencies and Conflicts

### Dependency Resolution
Elements declare dependencies. System ensures all are available:
```yaml
dependencies:
  principles:
    - ruthless-minimalism  # Must be present
  tools:
    - quick-scaffold       # Must be present
  suggests:
    - commit              # Optional but recommended
```

### Conflict Detection
Elements can declare conflicts:
```yaml
conflicts:
  principles:
    - waterfall           # Cannot coexist
    - formal-verification # Incompatible philosophy
```

System alerts user when conflicts detected:
```
Warning: 'ruthless-minimalism' conflicts with 'waterfall'
These principles have incompatible trade-offs.

Resolution options:
1. Remove 'waterfall'
2. Remove 'ruthless-minimalism'
3. Continue anyway (not recommended)
```

## Versioning

All elements use semantic versioning: `MAJOR.MINOR.PATCH`

- **MAJOR**: Breaking changes (incompatible interface)
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

Compositions can pin versions:
```yaml
elements:
  principles:
    - ruthless-minimalism@1.0.0    # Exact version
    - coevolution@^1.2.0            # Compatible with 1.2.x
    - emergent-design@~2.0          # Latest 2.x
```

## Distribution

Elements can be:
- **Core**: Shipped with Forge
- **Community**: Shared repository
- **Private**: Organization-specific
- **Local**: Project-only

```yaml
sources:
  - type: core
    priority: 1
  - type: community
    url: https://forge-elements.dev
    priority: 2
  - type: private
    url: https://company.com/forge-elements
    priority: 3
  - type: local
    path: ./.forge/elements
    priority: 4
```

## Summary

Elements are the atoms of Forge. By decomposing everything into elements and providing powerful composition primitives, users can:
- Mix and match freely
- Create custom approaches
- Share discoveries
- Evolve continuously

No prescribed methodology. Just building blocks and composition rules.

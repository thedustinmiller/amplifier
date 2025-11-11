# Forge Quickstart

This guide shows you how to use Forge to create a composable AI development environment.

## Installation

```bash
cd forge
pip install -e .
```

## Core Concepts

### Elements
Atomic, reusable building blocks:
- **Principles**: Core values (ruthless-minimalism, coevolution)
- **Tools**: Executable capabilities (scaffold, commit)
- **Agents**: Specialized intelligence (zen-architect, bug-hunter)
- **Templates**: Structured documents (minimal-spec, quick-plan)
- **Hooks**: Event-driven automation (session-start, pre-commit)

### Compositions
Assemblies of elements:
- **Presets**: Pre-configured bundles (rapid-prototype, specification-driven)
- **Workflows**: Ordered sequences
- **Methodologies**: Complete approaches

### Memory
Pluggable storage:
- **Scopes**: Session (ephemeral), Project (persistent), Global (permanent)
- **Providers**: File (simple), Graph (relationships), Vector (semantic), Relational (structured)

## Example 1: Using Memory

```python
import asyncio
from forge.memory import FileProvider, Scope

async def main():
    # Initialize file provider
    memory = FileProvider()
    await memory.initialize({
        "base_path": ".forge/memory",
        "session_id": "demo"
    })

    # Store a decision
    await memory.set(
        key="decision:auth-strategy",
        value="Using JWT tokens because simplest for MVP",
        scope=Scope.PROJECT,
        tags=["decision", "authentication"]
    )

    # Query all decisions
    decisions = await memory.query("decision:*", Scope.PROJECT)
    for entry in decisions:
        print(f"{entry.key}: {entry.value}")

    # Store a learning
    await memory.set(
        key="learning:async-files",
        value="Always use aiofiles for async file operations",
        scope=Scope.GLOBAL,
        tags=["python", "async", "io"]
    )

    # Clean up
    await memory.close()

asyncio.run(main())
```

## Example 2: Loading Elements

```python
from pathlib import Path
from forge.core.element import ElementLoader, ElementType

# Create loader
loader = ElementLoader(search_paths=[
    Path("./elements"),
    Path("~/.forge/elements").expanduser(),
])

# Load a principle
minimalism = loader.load("ruthless-minimalism", ElementType.PRINCIPLE)
print(f"Principle: {minimalism.name}")
print(f"Description: {minimalism.metadata.description}")
print(f"\nContent:\n{minimalism.content}")

# List all principles
principles = loader.list_elements(ElementType.PRINCIPLE)
print(f"\nAvailable principles: {[p.name for p in principles]}")
```

## Example 3: Loading Compositions

```python
from pathlib import Path
from forge.core.element import ElementLoader
from forge.core.composition import CompositionLoader

# Setup
element_loader = ElementLoader(search_paths=[Path("./elements")])
composition_loader = CompositionLoader(element_loader)

# Load a preset
preset_path = Path("./presets/rapid-prototype/composition.yaml")
loaded = composition_loader.load(preset_path)

# Inspect composition
print(f"Composition: {loaded.composition.name}")
print(f"Description: {loaded.composition.description}")

# Get principles
principles = loaded.get_principles()
print(f"\nPrinciples:")
for p in principles:
    print(f"  - {p.name}: {p.metadata.description}")

# Get all elements
print(f"\nAll elements: {len(loaded.elements)}")
```

## Example 4: Using Context

```python
import asyncio
from pathlib import Path
from forge.memory import FileProvider, Scope
from forge.core.element import ElementLoader
from forge.core.composition import CompositionLoader
from forge.core.context import Context

async def main():
    # Initialize memory
    memory = FileProvider()
    await memory.initialize({
        "base_path": ".forge/memory",
        "session_id": "demo"
    })

    # Load composition
    element_loader = ElementLoader(search_paths=[Path("./elements")])
    composition_loader = CompositionLoader(element_loader)
    loaded = composition_loader.load(Path("./presets/rapid-prototype/composition.yaml"))

    # Create context
    ctx = Context(
        memory=memory,
        composition=loaded,
        project_path=Path("."),
        session_id="demo"
    )

    # Use context
    print("Active principles:")
    for name in ctx.principles.list():
        content = await ctx.principles.get(name)
        print(f"  - {name}")

    # Store in memory
    await ctx.memory.set(
        key="context:initialized",
        value="Context created successfully",
        scope=Scope.SESSION
    )

    # Clean up
    await memory.close()

asyncio.run(main())
```

## Example 5: Creating Custom Elements

### Create a New Principle

```bash
mkdir -p elements/principle/test-first
```

`elements/principle/test-first/element.yaml`:
```yaml
metadata:
  name: test-first
  type: principle
  version: 1.0.0
  description: Write tests before implementation
  author: you
  tags: [testing, tdd, quality]
  license: MIT

dependencies:
  principles: []
  suggests: [ruthless-minimalism]

conflicts:
  principles: []

interface:
  inputs: {}
  outputs: {}
```

`elements/principle/test-first/test-first.md`:
```markdown
# Principle: Test-First

## Core Tenet
Write tests before implementation to ensure testable design.

## Motivation
Tests written after implementation are biased by the implementation.
Test-first forces you to think about the interface first.

... (rest of content)
```

### Create a Custom Preset

```bash
mkdir -p presets/my-approach
```

`presets/my-approach/composition.yaml`:
```yaml
composition:
  name: my-approach
  type: preset
  version: 1.0.0
  description: My custom development approach

elements:
  principles:
    - ruthless-minimalism
    - coevolution
    - test-first  # Your new principle

settings:
  memory:
    provider: file
```

## Example 6: Claude Code Integration

For Claude Code integration, create `.claude/` directory:

`.claude/system.md`:
```markdown
# Active Composition: {{composition.name}}

## Principles

{{#each principles}}
### {{name}}
{{content}}
{{/each}}

## Memory

Recent context:
{{memory.query("*", "session", limit=5)}}
```

`.claude/commands/init.md`:
```markdown
# Initialize Project

Load the active composition and set up memory.

Steps:
1. Load composition from .forge/active.yaml
2. Initialize memory provider
3. Load all principles into context
4. Display active elements
```

## Next Steps

1. **Explore Elements**: Browse `elements/` directory
2. **Try Presets**: Load different presets to see different philosophies
3. **Create Custom**: Make your own elements and compositions
4. **Integrate**: Connect with Claude Code or other AI agents

## Philosophy

Forge provides building blocks, not prescriptions. You compose your own methodology from elements. Start simple (file memory, few principles), scale when needed (vector memory, many elements).

The system itself follows the principles it enables: coevolution (design emerges through use), minimalism (start simple), composition (build from parts).

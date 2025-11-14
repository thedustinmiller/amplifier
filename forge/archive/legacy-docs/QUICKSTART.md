# Forge Quickstart Guide

Get up and running with Forge in 5 minutes!

## What is Forge?

Forge is a composable AI development system that lets you:
- **Choose your principles** - ruthless-minimalism, coevolution, test-first, etc.
- **Compose your methodology** - Mix and match elements to create your workflow
- **Store context** - Memory system that persists across sessions
- **Stay agent-agnostic** - Works with Claude Code, Cursor, Copilot, and more

## Installation

### Prerequisites

- Python 3.10 or higher
- [uv](https://docs.astral.sh/uv/) (recommended) or pip

### Install uv (if needed)

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Install Forge

```bash
# Clone the repository (or download the forge directory)
cd forge

# Create virtual environment
uv venv

# Activate virtual environment
source .venv/bin/activate  # On Unix/macOS
# or
.venv\Scripts\activate  # On Windows

# Install Forge
uv pip install -e .
```

### Verify Installation

```bash
forge version
# Output: Forge version 0.1.0
```

## Quick Start: Interactive Wizard

The easiest way to get started is with the interactive wizard:

```bash
forge init
```

This will guide you through:

1. **Project setup** - Choose a project name
2. **Select principles** - Pick guiding values (e.g., ruthless-minimalism, coevolution)
3. **Configure memory** - Choose storage backend (file, graph, vector, relational)
4. **Create composition** - Your custom methodology

### Example Session

```
🔨 Forge Project Wizard
============================================================

Welcome to Forge!

Forge is a composable AI development system. This wizard will help you:
  • Choose guiding principles for your project
  • Select development tools
  • Configure memory storage
  • Create your first composition

Let's get started!


▶ Project Information

Project name [my-project]: hello-forge
✓ Created project directory: /path/to/hello-forge


▶ Loading Available Elements

✓ Found 2 principles


▶ Choose Guiding Principles

Principles define your project's philosophy and values.
They guide decision-making throughout development.

Select principles to guide your project:
(Select as many as you like)
Enter numbers separated by spaces (e.g., '1 3 4') or 'all' for all options:

  1. ruthless-minimalism
     Ship the simplest thing that could possibly work, then adapt based on real needs

  2. coevolution
     Specifications and code are conversation partners that inform each other

Your selection: 1 2
✓ Selected 2 principles: ruthless-minimalism, coevolution


▶ Memory Configuration

Memory stores context across sessions.

Available providers:
  • file - Simple JSON files (recommended for getting started)
  • graph - Graph database for relationships (requires Neo4j)
  • vector - Semantic search (requires vector database)
  • relational - SQL database (requires PostgreSQL)

Memory provider [file]:
Memory storage path [.forge/memory]:
✓ Configured file memory at .forge/memory


▶ Creating Composition

Composition name [hello-forge]:
Description [Development composition for hello-forge]: My first Forge project
✓ Saved composition to .forge/composition.yaml


▶ Initializing Memory

✓ Memory initialized successfully


▶ Creating Documentation

✓ Created README.md


🎉 Project Initialized!
============================================================

Your Forge project is ready!

📁 Project: /path/to/hello-forge
📝 Composition: hello-forge
💾 Memory: file (.forge/memory)
🎯 Principles: ruthless-minimalism, coevolution

Next steps:

  1. cd hello-forge
  2. Review README.md for more information
  3. Customize .forge/composition.yaml as needed
  4. Start building!

Happy forging! 🔨
```

## Your First Forge Project

After running `forge init`, you'll have a project structure like this:

```
hello-forge/
├── .forge/
│   ├── composition.yaml     # Your methodology
│   └── memory/              # Context storage
│       └── project/
│           ├── project:initialized.json
│           └── composition:active.json
└── README.md                # Project documentation
```

### Explore Your Composition

```bash
cd hello-forge
cat .forge/composition.yaml
```

You'll see something like:

```yaml
composition:
  name: hello-forge
  type: preset
  version: 1.0.0
  description: My first Forge project

elements:
  principles:
    - ruthless-minimalism
    - coevolution
  constitutions: []
  tools: []
  agents: []
  templates: []
  hooks: {}
  queries: []

settings:
  memory:
    provider: file
    config:
      base_path: .forge/memory
  agent_orchestration:
    mode: sequential
    max_parallel: 3
  tool_defaults: {}
```

### Explore Memory

Memory is stored as JSON files:

```bash
ls .forge/memory/project/
# project:initialized.json  composition:active.json  _index.json

cat .forge/memory/project/project\:initialized.json
```

Output:

```json
{
  "key": "project:initialized",
  "value": "Project 'hello-forge' initialized with Forge wizard",
  "scope": "project",
  "timestamp": 1234567890,
  "tags": ["initialization", "wizard"],
  "metadata": {}
}
```

## Adding More Elements

You can add more elements to your project:

```bash
forge add
```

This will prompt you to select:
- Principles
- Tools
- Agents
- Templates

## Manual Customization

You can also manually edit `.forge/composition.yaml`:

```yaml
composition:
  name: hello-forge
  type: preset
  version: 1.0.0
  description: My first Forge project

elements:
  principles:
    - ruthless-minimalism
    - coevolution
    - test-first              # Add manually

  tools:
    - scaffold                # Add tools
    - commit

  agents:
    - zen-architect           # Add agents

  templates:
    - minimal-spec            # Add templates
```

## Using Forge with Python

### Load and Use Memory

```python
import asyncio
from pathlib import Path
from forge.memory import FileProvider, Scope

async def main():
    # Initialize memory
    memory = FileProvider()
    await memory.initialize({
        "base_path": ".forge/memory",
        "session_id": "demo"
    })

    # Store a decision
    await memory.set(
        key="decision:use-sqlite",
        value="Using SQLite for simplicity, will migrate to PostgreSQL when we hit 10K users",
        scope=Scope.PROJECT,
        tags=["decision", "database"]
    )

    # Query all decisions
    decisions = await memory.query("decision:*", Scope.PROJECT)
    for entry in decisions:
        print(f"{entry.key}: {entry.value}")

    # Store a global learning
    await memory.set(
        key="learning:async-patterns",
        value="Always use asyncio.gather() for parallel operations",
        scope=Scope.GLOBAL,
        tags=["python", "async"]
    )

    await memory.close()

asyncio.run(main())
```

### Load a Composition

```python
from pathlib import Path
from forge.core.element import ElementLoader
from forge.core.composition import CompositionLoader, Composition

# Load composition
composition = Composition.load_from_file(Path(".forge/composition.yaml"))

print(f"Composition: {composition.name}")
print(f"Principles: {composition.elements.principles}")
print(f"Memory provider: {composition.settings.memory['provider']}")

# Load and resolve with elements
element_loader = ElementLoader(search_paths=[Path("../elements")])
composition_loader = CompositionLoader(element_loader)

loaded = composition_loader.load(Path(".forge/composition.yaml"))

# Get all active principles
for principle in loaded.get_principles():
    print(f"\n{principle.name}:")
    print(principle.content)
```

## Next Steps

### 1. Explore Available Elements

Browse the `elements/` directory in the Forge repository:

```
forge/elements/
├── principle/
│   ├── ruthless-minimalism/
│   │   ├── element.yaml
│   │   └── ruthless-minimalism.md
│   └── coevolution/
│       ├── element.yaml
│       └── coevolution.md
├── tool/
├── agent/
└── template/
```

### 2. Create Custom Elements

Create your own principles, tools, or agents:

```bash
mkdir -p .forge/elements/principle/my-principle
```

`.forge/elements/principle/my-principle/element.yaml`:
```yaml
metadata:
  name: my-principle
  type: principle
  version: 1.0.0
  description: My custom principle
  tags: [custom]

dependencies:
  principles: []
```

`.forge/elements/principle/my-principle/my-principle.md`:
```markdown
# Principle: My Custom Principle

## Core Tenet
Your guiding philosophy...

## Motivation
Why this matters...
```

### 3. Try Different Presets

Forge comes with example presets:

```bash
# Copy a preset to your project
cp ../presets/rapid-prototype/composition.yaml .forge/
```

### 4. Scale Your Memory

When your project grows, upgrade from file-based memory:

```yaml
# In .forge/composition.yaml
settings:
  memory:
    provider: relational  # or graph, vector
    config:
      url: postgresql://user:pass@localhost/mydb
```

### 5. Integrate with AI Agents

Forge works with any AI coding assistant:

- **Claude Code**: Create `.claude/` directory
- **Cursor**: Create `.cursor/` directory
- **GitHub Copilot**: Create `.github/prompts/` directory

Example for Claude Code (`.claude/system.md`):

```markdown
# Project: {{ project.name }}

## Active Principles

{{ load_principles() }}

## Recent Context

{{ memory.query("*", "session", limit=5) }}
```

## Common Patterns

### Pattern 1: Rapid Prototyping

```yaml
elements:
  principles: [ruthless-minimalism, coevolution]
  tools: [scaffold, commit]
  agents: [zen-architect]
```

### Pattern 2: Quality-Focused

```yaml
elements:
  principles: [test-first, coevolution]
  constitutions: [mandatory-tests]
  tools: [test-runner, coverage-check]
```

### Pattern 3: Documentation-Heavy

```yaml
elements:
  principles: [coevolution]
  templates: [spec-template, plan-template, decision-log]
  tools: [doc-generator]
```

## Troubleshooting

### "Not in a Forge project directory"

Run `forge init` first to create a project, or navigate to an existing Forge project directory.

### "No composition.yaml found"

Your `.forge/` directory is missing the composition file. Run `forge init` to create one.

### Memory provider errors

Make sure the memory directory exists and is writable:

```bash
mkdir -p .forge/memory
chmod 755 .forge/memory
```

## Getting Help

- **Documentation**: Browse `docs/` directory
- **Examples**: Check `examples/quickstart.md`
- **Issues**: Report bugs or request features on GitHub

## Learn More

- [Element Types](docs/element-types.md) - Deep dive into all element types
- [Memory System](docs/memory-system.md) - Understanding memory providers
- [SYNTHESIS.md](SYNTHESIS.md) - Relationship to Amplifier and Spec-Kit
- [README.md](README.md) - Project overview and philosophy

---

**Happy Forging! 🔨**

Start simple. Compose freely. Scale when needed.

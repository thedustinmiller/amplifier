# Amplifier

A composable AI development system that enables specification-driven development through modular elements and persistent memory.

## Overview

Amplifier consists of two complementary systems:

### 1. Forge - Composable Element System

**Forge** is a greenfield AI development system that learns from both past approaches while embracing a fundamental truth: **specifications and code coevolve**. It provides a compositional framework where everything is an element that can be combined, replaced, and evolved.

**Core Philosophy:**
- **Coevolution, Not Dichotomy**: Specs and code are conversation partners that inform each other
- **Radical Composition**: Everything is an element; elements combine into compositions; compositions can become elements
- **Non-Prescriptive Design**: No defaults, no "best practices" - users compose their own methodology
- **Agent-Agnostic**: Works with Claude Code, Cursor, Copilot, and any AI assistant
- **Pluggable Everything**: Memory, agents, tools, templates - all pluggable and extensible

**Key Features:**
- Element-based architecture (principles, tools, agents, templates, hooks, queries)
- Multi-scope memory system (session, project, global)
- Pluggable memory providers (file, graph, vector, relational)
- Composition engine for creating custom methodologies
- Meta-system for generating and evolving elements
- Full integration with Claude Code via `.claude/` directory

### 2. Spec-Kit - Specification-Driven Development

**Spec-Kit** provides structured templates and workflows for specification-driven development, enabling teams to align around clear requirements before implementation.

## Project Structure

```
amplifier/
├── forge/                      # Composable element system
│   ├── src/forge/             # Core Forge implementation
│   │   ├── cli/               # Command-line interface
│   │   ├── core/              # Element and composition engine
│   │   ├── memory/            # Memory provider system
│   │   ├── providers/         # Platform integrations (Claude Code, etc.)
│   │   └── testing/           # Testing utilities
│   ├── elements/              # Curated element library
│   │   ├── principle/         # Guiding principles
│   │   ├── tool/              # Executable tools
│   │   ├── agent/             # Specialized agents
│   │   └── template/          # Document templates
│   ├── docs/                  # Detailed documentation
│   ├── examples/              # Example compositions
│   ├── presets/               # Pre-configured compositions
│   └── tests/                 # Test suite
├── spec-kit/                  # Specification templates and tools
│   ├── elements/              # Spec-Kit specific elements
│   └── templates/             # Specification templates
└── docs/                      # Root documentation
```

## Quick Start

### Prerequisites

- Python 3.10 or higher
- [uv](https://docs.astral.sh/uv/) (recommended) or pip

### Installation

```bash
# Navigate to forge directory
cd forge

# Create and activate virtual environment
uv venv
source .venv/bin/activate  # Unix/macOS
# or: .venv\Scripts\activate  # Windows

# Install Forge
uv pip install -e .

# Verify installation
forge version
```

### Initialize Your First Project

```bash
# Run interactive wizard
forge init

# Or create manually
mkdir my-project && cd my-project
mkdir -p .forge

# Create composition.yaml
cat > .forge/composition.yaml <<'EOF'
composition:
  name: my-project
  type: preset
  version: 1.0.0

elements:
  principles:
    - ruthless-minimalism
    - coevolution
  tools:
    - scaffold
  agents:
    - code-reviewer

settings:
  memory:
    provider: file
    config:
      base_path: .forge/memory
EOF

# Generate Claude Code integration
forge generate claude-code
```

For detailed step-by-step instructions, see [QUICKSTART.md](QUICKSTART.md).

## Core Concepts

### Elements

Elements are the atomic building blocks of Forge:

- **Principles**: Philosophical guidelines that shape decision-making
- **Constitutions**: Immutable governance rules
- **Tools**: Executable capabilities (commands, scripts)
- **Agents**: Specialized AI assistants
- **Templates**: Structured document patterns
- **Hooks**: Event-driven automation
- **Queries**: Memory interaction patterns

### Compositions

Compositions assemble elements into cohesive methodologies:

- **Presets**: Pre-configured element bundles
- **Workflows**: Ordered sequences of tools
- **Orchestrations**: Agent coordination patterns
- **Methodologies**: Complete development approaches

### Memory System

Persistent context across sessions:

- **Scopes**: Session (ephemeral), Project (persistent), Global (cross-project)
- **Providers**: File (simple), Graph (relationships), Vector (semantic), Relational (structured)
- **Operations**: Store, retrieve, query, search

### Coevolution Pattern

The core workflow philosophy:

1. **Sketch Spec**: Write rough specification
2. **Prototype**: Implement quickly
3. **Discover**: Find gaps and impossibilities
4. **Refine Spec**: Update based on reality
5. **Improve Code**: Incorporate learnings
6. **Repeat**: Spiral toward coherence

## Available Commands

```bash
forge                    # Show help and available commands
forge version            # Display version information
forge init               # Interactive wizard for new projects
forge generate <target>  # Generate platform integration
forge validate <target>  # Validate generated files
forge update <target>    # Update generated files
forge clean <target>     # Remove generated files
forge test               # Run test suite
```

Supported targets: `claude-code` (more coming soon)

## Common Use Cases

### Rapid Prototyping

```yaml
elements:
  principles: [ruthless-minimalism, coevolution]
  tools: [scaffold, commit]
  agents: [zen-architect]
```

### Quality-Focused Development

```yaml
elements:
  principles: [test-first, coevolution]
  constitutions: [mandatory-tests]
  tools: [test-runner, coverage-check]
```

### Documentation-Heavy Projects

```yaml
elements:
  principles: [coevolution, spec-driven]
  templates: [spec-template, plan-template, decision-log]
  tools: [doc-generator]
```

## Documentation

- **[QUICKSTART.md](QUICKSTART.md)** - Step-by-step guide to get started
- **[TESTING.md](TESTING.md)** - Testing structure and methodology
- **[forge/docs/](forge/docs/)** - Detailed command reference and workflows
- **[forge/README.md](forge/README.md)** - Forge system deep dive
- **[forge/ELEMENT_CATALOG.md](forge/ELEMENT_CATALOG.md)** - Available elements

## Philosophy

### Why Coevolution?

Traditional development forces a false choice between code-first (specs become stale) and spec-first (reality diverges from plan). Forge embraces the truth that **specifications and code inform each other** through continuous dialogue.

### Why Composable?

Every project is unique. One-size-fits-all methodologies fail because they can't adapt to your specific context, constraints, and values. Forge provides building blocks you compose into your own approach.

### Why Agent-Agnostic?

AI platforms will evolve and change. Your knowledge, principles, and processes should outlive any specific tool. Forge works with any AI assistant through standard integration patterns.

### Why Pluggable Memory?

Different projects have different needs. Start simple with file-based memory. Scale to graph databases for complex relationships, vector stores for semantic search, or relational databases for structured queries.

## Development Status

**Current Version**: 0.1.0 (Alpha)

**Test Coverage**:
- 23 automated tests (100% passing)
- Provider tests: 14/14 ✓
- End-to-end tests: 9/9 ✓
- Element system validated
- Memory system validated
- Composition system validated

**Platform Support**:
- ✅ Claude Code
- 🚧 Cursor (planned)
- 🚧 GitHub Copilot (planned)

## Contributing

Forge is designed to be extended by the community:

1. **Create Elements**: Add new principles, tools, agents, or templates
2. **Build Compositions**: Share effective element combinations
3. **Develop Providers**: Integrate new platforms or memory systems
4. **Improve Meta-System**: Enhance element generation and analysis

## License

MIT - Use freely, modify wildly, share openly.

## Getting Help

- **Documentation**: See [forge/docs/](forge/docs/) for detailed guides
- **Examples**: Browse [forge/examples/](forge/examples/) for working examples
- **Issues**: Report bugs or request features on GitHub

---

**Start simple. Compose freely. Scale when needed.**

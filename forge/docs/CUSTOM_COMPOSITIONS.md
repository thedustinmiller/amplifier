# Creating Custom Forge Compositions

A guide to creating, testing, and using custom Forge compositions.

## Quick Start

### 1. Create a Composition Programmatically

```python
from forge.core.composition import (
    Composition,
    CompositionElements,
    CompositionSettings,
)

# Create custom composition
composition = Composition(
    name="my-composition",
    type="preset",
    version="1.0.0",
    description="My custom development approach",
    elements=CompositionElements(
        principles=["ruthless-minimalism", "coevolution"],
        tools=["linter", "formatter"],
        agents=[],
    ),
    settings=CompositionSettings(
        memory={
            "provider": "file",
            "config": {"base_path": ".forge/memory"},
        },
    ),
    metadata={
        "author": "your-name",
        "tags": ["custom", "experimental"],
    },
)

# Save to file
composition.save_to_file(Path("my-composition.yaml"))
```

### 2. Create a Composition via YAML

```yaml
composition:
  name: my-composition
  type: preset
  version: 1.0.0
  description: My custom development approach

elements:
  principles:
    - ruthless-minimalism
    - coevolution
  tools:
    - linter
  agents: []

settings:
  memory:
    provider: file
    config:
      base_path: .forge/memory

metadata:
  author: your-name
  tags: [custom, experimental]
```

### 3. Load and Use a Composition

```python
from pathlib import Path
from forge.core.composition import Composition, CompositionLoader
from forge.core.element import ElementLoader
from forge.core.context import Context
from forge.memory.file_provider import FileProvider

# Load composition
element_loader = ElementLoader(search_paths=[Path("elements")])
composition_loader = CompositionLoader(element_loader)
loaded_composition = composition_loader.load(Path("my-composition.yaml"))

# Initialize memory
memory = FileProvider()
await memory.initialize({
    "base_path": ".forge/memory",
    "session_id": "my-session",
})

# Create context
context = Context(
    memory=memory,
    composition=loaded_composition,
    project_path=Path.cwd(),
    session_id="my-session",
)

# Use context
principles = context.principles.list()
content = await context.principles.get("ruthless-minimalism")
await context.memory.set("key", "value", Scope.PROJECT)
```

## Composition Structure

### Required Fields

```yaml
composition:
  name: string          # Unique identifier
  type: string          # preset|workflow|orchestration|methodology
  version: string       # Semantic version (e.g., "1.0.0")
```

### Optional Fields

```yaml
composition:
  description: string   # Human-readable description

elements:
  principles: []        # List of principle names
  constitutions: []     # List of constitution names
  tools: []            # List of tool names
  agents: []           # List of agent names
  templates: []        # List of template names
  hooks: {}            # Map of event -> hook name
  queries: []          # List of saved query names

settings:
  memory: {}           # Memory provider configuration
  agent_orchestration: {}  # Agent coordination settings
  tool_defaults: {}    # Default tool configurations

metadata: {}           # Arbitrary metadata (fully extensible)
```

## Element Types

### Principles
Guiding philosophies and development approaches.

```yaml
elements:
  principles:
    - ruthless-minimalism  # Ship simplest thing first
    - coevolution          # Specs and code coevolve
    - test-driven          # Tests before implementation
```

### Constitutions
Rules, constraints, and governance policies.

```yaml
elements:
  constitutions:
    - no-external-deps    # Dependency restrictions
    - security-first      # Security requirements
```

### Tools
Executable tools and utilities.

```yaml
elements:
  tools:
    - linter             # Code quality checking
    - formatter          # Code formatting
    - type-checker       # Static type analysis
```

### Agents
AI agents for automation.

```yaml
elements:
  agents:
    - code-reviewer      # Automated code review
    - test-generator     # Test generation
```

### Templates
Code generation templates.

```yaml
elements:
  templates:
    - api-endpoint       # REST API endpoint template
    - component          # UI component template
```

### Hooks
Lifecycle event handlers.

```yaml
elements:
  hooks:
    pre_commit: linter-hook      # Run before commit
    post_generate: formatter     # Run after code generation
    pre_push: test-runner        # Run before push
```

### Queries
Saved memory queries.

```yaml
elements:
  queries:
    - recent-decisions   # Last 10 architecture decisions
    - active-tasks       # Current work items
```

## Settings

### Memory Configuration

```yaml
settings:
  memory:
    provider: file  # file|vector|graph|relational
    config:
      base_path: .forge/memory
      compression: false
      session_id: auto  # or explicit ID
```

**Available Providers:**
- `file` - JSON file-based storage (simple, no dependencies)
- `vector` - Embeddings-based semantic search (future)
- `graph` - Relationship-based storage (future)
- `relational` - SQL database storage (future)

### Agent Orchestration

```yaml
settings:
  agent_orchestration:
    mode: sequential  # sequential|parallel|priority|round-robin
    max_parallel: 3   # Max concurrent agents
    timeout: 300      # Operation timeout (seconds)
```

**Orchestration Modes:**
- `sequential` - Run agents one at a time, in order
- `parallel` - Run multiple agents concurrently
- `priority` - Run agents based on priority scores
- `round-robin` - Distribute work evenly across agents

### Tool Defaults

```yaml
settings:
  tool_defaults:
    linter:
      strict: true
      config: .pylintrc
    formatter:
      style: black
      line_length: 88
```

## Metadata

Metadata is fully extensible. Add any fields you need:

```yaml
metadata:
  # Common fields
  description: string
  author: string
  tags: [string]

  # Custom fields (examples)
  team: platform-engineering
  maturity: experimental|beta|stable
  last_updated: 2025-11-11
  license: MIT
  repository: https://github.com/org/repo
  documentation: https://docs.example.com

  # Structured custom fields
  recommended_for:
    - Use case 1
    - Use case 2

  compatibility:
    python: ">=3.10"
    forge: ">=1.0.0"

  changelog:
    - version: 1.0.0
      date: 2025-11-11
      changes: Initial release
```

## Composition Types

### Preset
Pre-configured development approach.

```yaml
composition:
  type: preset

# Example: rapid-prototype preset
elements:
  principles: [ruthless-minimalism, coevolution]
settings:
  agent_orchestration:
    mode: sequential
```

### Workflow
Step-by-step process.

```yaml
composition:
  type: workflow

# Example: test-driven workflow
elements:
  templates: [test-template, implementation-template]
  hooks:
    pre_commit: test-runner
```

### Orchestration
Agent coordination pattern.

```yaml
composition:
  type: orchestration

# Example: multi-agent orchestration
elements:
  agents: [planner, implementer, reviewer]
settings:
  agent_orchestration:
    mode: priority
    max_parallel: 2
```

### Methodology
Comprehensive development methodology.

```yaml
composition:
  type: methodology

# Example: full-stack methodology
elements:
  principles: [...]
  constitutions: [...]
  tools: [...]
  agents: [...]
  templates: [...]
```

## Testing Compositions

### Basic Validation

```python
# Load and validate
composition = Composition.load_from_file(Path("composition.yaml"))
loaded = composition_loader.load(Path("composition.yaml"))

# Check integrity
assert loaded.composition.name == "my-composition"
assert len(loaded.get_principles()) == 2
```

### Memory Testing

```python
# Test memory operations
await context.memory.set("test", "value", Scope.PROJECT)
entry = await context.memory.get("test", Scope.PROJECT)
assert entry.value == "value"

# Test queries
entries = await context.memory.query("test:*", Scope.PROJECT)
assert len(entries) > 0
```

### Element Access

```python
# Test principle access
principles = context.principles.list()
assert "ruthless-minimalism" in principles

content = await context.principles.get("ruthless-minimalism")
assert content is not None
```

## Examples

### Minimal Composition
```yaml
composition:
  name: minimal
  type: preset
  version: 1.0.0

elements:
  principles: [ruthless-minimalism]
```

### Full-Featured Composition
```yaml
composition:
  name: full-featured
  type: methodology
  version: 1.0.0
  description: Complete development methodology

elements:
  principles:
    - ruthless-minimalism
    - coevolution
    - test-driven

  tools:
    - linter
    - formatter
    - type-checker

  agents:
    - code-reviewer
    - test-generator

  templates:
    - api-endpoint
    - test-suite

  hooks:
    pre_commit: linter-hook
    post_generate: formatter-hook

settings:
  memory:
    provider: file
    config:
      base_path: .forge/memory

  agent_orchestration:
    mode: priority
    max_parallel: 3

  tool_defaults:
    linter:
      strict: true
    formatter:
      style: black

metadata:
  author: platform-team
  tags: [methodology, full-stack]
  maturity: stable
  recommended_for:
    - Team projects
    - Production systems
```

## Best Practices

### 1. Start Simple
Begin with a minimal composition and add complexity as needed.

```yaml
# Start here
elements:
  principles: [ruthless-minimalism]

# Add more later
elements:
  principles: [ruthless-minimalism, coevolution]
  tools: [linter]
```

### 2. Use Meaningful Names
Choose descriptive names for your compositions.

```yaml
# Good
name: rapid-prototype-with-testing

# Less good
name: comp1
```

### 3. Version Your Compositions
Use semantic versioning to track changes.

```yaml
version: 1.0.0  # Initial release
version: 1.1.0  # Add new element
version: 2.0.0  # Breaking change
```

### 4. Document in Metadata
Use metadata to explain your composition.

```yaml
metadata:
  description: |
    This composition emphasizes rapid prototyping with minimal upfront
    planning. It's designed for solo developers working on greenfield
    projects where requirements are uncertain.

  recommended_for:
    - Prototypes and MVPs
    - Solo developers
    - Exploration phase

  not_recommended_for:
    - Safety-critical systems
    - Large teams
    - Well-understood domains
```

### 5. Test Before Committing
Always validate your composition works before committing.

```bash
python test_custom_composition.py
```

### 6. Use Element Dependencies
Let elements declare their dependencies to ensure compatibility.

```yaml
# In element.yaml
dependencies:
  principles:
    - ruthless-minimalism  # This element requires this principle

conflicts:
  principles:
    - waterfall  # This element conflicts with waterfall
```

## Common Patterns

### Pattern: Principle-Only Development
Focus on philosophy without tooling.

```yaml
elements:
  principles: [ruthless-minimalism, coevolution]
  # No tools, agents, or other automation
```

### Pattern: Test-First Workflow
Emphasize testing at every stage.

```yaml
elements:
  principles: [test-driven]
  templates: [test-template]
  hooks:
    pre_commit: test-runner
    pre_push: test-runner
```

### Pattern: Multi-Agent Collaboration
Coordinate multiple AI agents.

```yaml
elements:
  agents: [planner, implementer, reviewer, tester]
settings:
  agent_orchestration:
    mode: priority
    max_parallel: 2
```

### Pattern: Memory-Heavy Composition
Emphasize knowledge accumulation.

```yaml
settings:
  memory:
    provider: file
    config:
      base_path: .forge/memory

elements:
  queries:
    - architecture-decisions
    - lessons-learned
    - known-issues
```

## Troubleshooting

### Issue: "Element not found"
**Cause:** Element doesn't exist in search paths.
**Solution:** Verify element exists in `elements/` directory.

```bash
ls elements/principle/ruthless-minimalism/element.yaml
```

### Issue: "Missing dependencies"
**Cause:** Element requires another element that's not included.
**Solution:** Add required elements to composition.

```yaml
elements:
  principles:
    - coevolution          # Requires...
    - ruthless-minimalism  # ...this principle
```

### Issue: "Conflicts detected"
**Cause:** Two elements explicitly conflict.
**Solution:** Remove one of the conflicting elements.

```yaml
# Remove one of these
elements:
  principles:
    - waterfall           # Conflicts with...
    - ruthless-minimalism # ...this principle
```

### Issue: "Memory provider not initialized"
**Cause:** Context created without initializing memory.
**Solution:** Initialize memory provider first.

```python
memory = FileProvider()
await memory.initialize(config)  # Must call this
context = Context(memory=memory, ...)
```

## Reference

### Complete Composition Example
See: `/home/user/amplifier/forge/examples/custom-composition-example.yaml`

### Test Results
See: `/home/user/amplifier/forge/CUSTOM_COMPOSITION_TEST_RESULTS.md`

### Test Script
See: `/home/user/amplifier/forge/test_custom_composition.py`

### Existing Compositions
- `presets/rapid-prototype/composition.yaml` - Fast iteration preset

### Element Directories
- `elements/principle/` - Development principles
- `elements/constitution/` - Governance rules
- `elements/tool/` - Executable tools
- `elements/agent/` - AI agents
- `elements/template/` - Code templates

## Further Reading

- [Forge README](../README.md) - System overview
- [Quickstart Guide](../QUICKSTART.md) - Getting started
- [Synthesis Document](../SYNTHESIS.md) - Architecture and design

## Support

For questions or issues:
1. Check this guide first
2. Review test results document
3. Examine example compositions
4. Consult the test script for usage patterns

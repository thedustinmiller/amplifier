# Claude Code Provider

The Claude Code Provider enables seamless integration between Forge compositions and Claude Code's `.claude/` directory structure.

## Overview

The Claude Code Provider automatically generates:

- **Agent files** (`.claude/agents/*.md`) - AI agents for specialized tasks
- **Command files** (`.claude/commands/*.md`) - Slash commands for workflows
- **Tool scripts** (`.claude/tools/*.py`) - Automation scripts and hooks
- **Settings** (`settings.json`) - Claude Code configuration and hooks

## Installation

The Claude Code provider is included with Forge by default.

```python
from forge.providers import ClaudeCodeProvider
```

## Usage

### Generate Claude Code Files

Generate `.claude/` structure from a Forge composition:

```bash
forge generate claude-code
```

Or from Python:

```python
import asyncio
from pathlib import Path
from forge.core.element import ElementLoader
from forge.core.composition import CompositionLoader
from forge.providers import ClaudeCodeProvider

async def generate():
    element_loader = ElementLoader(search_paths=[Path("elements")])
    composition_loader = CompositionLoader(element_loader)

    composition = composition_loader.load(Path(".forge/composition.yaml"))

    provider = ClaudeCodeProvider()
    result = await provider.generate(composition, Path("."), force=True)

    if result.success:
        print(f"Generated {len(result.files_created)} files")
    else:
        print(f"Errors: {result.errors}")

asyncio.run(generate())
```

### Validate Integration

Check if `.claude/` files match the composition:

```bash
forge validate claude-code
```

Or from Python:

```python
result = await provider.validate(composition, Path("."))

if result.valid:
    print("✓ Validation passed")
else:
    print(f"✗ Errors: {result.errors}")
    print(f"⚠ Warnings: {result.warnings}")
```

### Update After Changes

Update Claude Code files when composition changes:

```bash
forge update claude-code
```

Or:

```python
result = await provider.update(composition, Path("."))
```

### Clean Generated Files

Remove all generated `.claude/` files:

```bash
forge clean claude-code
```

Or:

```python
result = await provider.clean(Path("."))
```

## Element Mapping

### Forge Agent → Claude Code Agent

**Forge element** (`elements/agent/code-reviewer/element.yaml`):

```yaml
metadata:
  name: code-reviewer
  type: agent
  description: Reviews code for quality

interface:
  role: code_reviewer

implementation:
  model: inherit
  prompt: |
    You are an expert code reviewer...
```

**Generated Claude Code** (`.claude/agents/code-reviewer.md`):

```markdown
---
name: code-reviewer
description: "Reviews code for quality"
model: inherit
role: "code_reviewer"
---

You are an expert code reviewer...
```

### Forge Tool → Claude Code Command

**Forge element** (`elements/tool/scaffold/element.yaml`):

```yaml
metadata:
  name: scaffold
  type: tool
  description: Scaffolds project structures
  tags: [scaffolding]

implementation:
  instructions: |
    # Scaffold Command
    ...
  allowed_tools:
    - Bash
    - Write
```

**Generated Claude Code** (`.claude/commands/scaffold.md`):

```markdown
---
description: "Scaffolds project structures"
category: scaffolding
allowed-tools: Bash, Write
---

# Scaffold Command
...
```

### Forge Hook → Claude Code Hook

**Forge element** (`elements/hook/session-logger/element.yaml`):

```yaml
metadata:
  name: session-logger
  type: hook

interface:
  events:
    - SessionStart
    - Stop

implementation:
  script: |
    #!/usr/bin/env python3
    ...
  script_type: py
  matcher: "*"
  timeout: 3000
```

**Generated files**:

1. **Script** (`.claude/tools/hook_sessionstart.py`):
   ```python
   #!/usr/bin/env python3
   ...
   ```

2. **Settings** (`settings.json`):
   ```json
   {
     "hooks": {
       "SessionStart": [{
         "matcher": "*",
         "hooks": [{
           "type": "command",
           "command": "$CLAUDE_PROJECT_DIR/.claude/tools/hook_sessionstart.py",
           "timeout": 3000
         }]
       }]
     }
   }
   ```

## Directory Structure

After generation, your project will have:

```
project-root/
├── .forge/
│   ├── composition.yaml
│   └── elements/
└── .claude/
    ├── agents/
    │   └── code-reviewer.md
    ├── commands/
    │   └── scaffold.md
    ├── tools/
    │   └── hook_sessionstart.py
    ├── settings.json
    └── README.md
```

## Composition Settings

Configure Claude Code-specific settings in your composition:

```yaml
settings:
  memory:
    provider: file
    config:
      base_path: .forge/memory

  agent_orchestration:
    mode: sequential
    max_parallel: 3
```

## Advanced Usage

### Custom Provider Configuration

Create a custom provider with additional capabilities:

```python
from forge.providers.claude_code import ClaudeCodeProvider

class CustomClaudeProvider(ClaudeCodeProvider):
    async def _generate_agents(self, composition, claude_dir):
        # Custom agent generation logic
        files = await super()._generate_agents(composition, claude_dir)
        # Additional processing
        return files
```

### Bidirectional Sync

Sync changes from `.claude/` back to Forge elements:

```python
result = await provider.sync(composition, Path("."))
```

This detects changes in `.claude/` files and suggests updates to Forge elements.

## Best Practices

1. **Version Control**: Commit both `.forge/` and `.claude/` directories
2. **Regenerate on Changes**: Run `forge update claude-code` after modifying compositions
3. **Validate Regularly**: Use `forge validate claude-code` to catch drift
4. **Use Force Sparingly**: The `--force` flag overwrites customizations

## Troubleshooting

### Generation Fails with "Directory Already Exists"

**Problem**: `.claude/` directory exists without `force=True`

**Solution**:
```bash
forge generate claude-code --force
```

Or remove `.claude/` first:
```bash
forge clean claude-code
forge generate claude-code
```

### Validation Warnings After Manual Edits

**Problem**: Manually edited `.claude/` files don't match composition

**Solution**: Either:
1. Update composition to match: Edit `.forge/composition.yaml`
2. Regenerate files: `forge update claude-code --force`

### Hook Scripts Not Executable

**Problem**: Hook scripts (`.sh` files) lack execute permissions

**Solution**: Provider automatically sets execute permissions for `.sh` files. If issues persist:
```bash
chmod +x .claude/tools/*.sh
```

## Provider API

### Methods

#### `generate(composition, output_dir, force=False)`

Generate `.claude/` structure from composition.

**Returns**: `GenerationResult`
- `success`: Whether generation succeeded
- `files_created`: List of created files
- `files_updated`: List of updated files
- `errors`: List of error messages
- `warnings`: List of warnings

#### `validate(composition, output_dir)`

Validate `.claude/` files against composition.

**Returns**: `ValidationResult`
- `valid`: Whether validation passed
- `errors`: List of validation errors
- `warnings`: List of warnings
- `suggestions`: List of suggested fixes

#### `update(composition, output_dir)`

Update `.claude/` files after composition changes.

**Returns**: `GenerationResult`

#### `clean(output_dir)`

Remove all generated `.claude/` files.

**Returns**: `GenerationResult`

## Examples

### Example 1: Simple Workflow

Create a composition with basic elements:

```yaml
# .forge/composition.yaml
composition:
  name: my-workflow
  type: preset
  version: 1.0.0

elements:
  principles:
    - ruthless-minimalism
  agents:
    - code-reviewer
  tools:
    - scaffold
```

Generate Claude Code files:

```bash
forge generate claude-code
```

### Example 2: Multi-Hook Setup

Configure multiple hooks for different events:

```yaml
elements:
  hooks:
    SessionStart: session-logger
    PostToolUse: code-formatter
    PreCompact: transcript-saver
```

Generates hook scripts for each event with proper configuration.

### Example 3: Custom Agent Models

Specify different models for agents:

```yaml
# elements/agent/architect/element.yaml
implementation:
  model: opus  # or sonnet, haiku
  prompt: |
    You are a system architect...
```

Generates agent with specified model in frontmatter.

## See Also

- [Forge README](../../README.md)
- [Element Types](../element-types.md)
- [Memory System](../memory-system.md)
- [Claude Code Documentation](https://code.claude.com/docs)

# Forge Providers

Providers enable Forge to integrate with different AI coding platforms by converting Forge compositions into platform-specific formats.

## Overview

Forge uses a **provider plugin architecture** that allows compositions to be:

1. **Generated**: Convert Forge compositions to platform files
2. **Validated**: Check platform files match composition
3. **Synced**: Keep composition and platform files in sync
4. **Updated**: Regenerate files when composition changes
5. **Cleaned**: Remove generated files

## Available Providers

### Claude Code Provider

Generates `.claude/` directory structure for Anthropic's Claude Code.

- **Status**: Stable
- **Documentation**: [claude-code.md](./claude-code.md)
- **Capabilities**: Agents, Commands, Hooks, Tools, Settings

### Future Providers

Additional providers planned:

- **Cursor Provider** - `.cursor/` directory integration
- **GitHub Copilot Provider** - `.github/prompts/` integration
- **Windsurf Provider** - `.windsurf/workflows/` integration

## Provider Architecture

### Base Protocol

All providers implement the `Provider` protocol:

```python
from forge.providers.protocol import Provider, ProviderCapability

class MyProvider:
    @property
    def name(self) -> str:
        """Provider name (e.g., 'claude-code')."""
        ...

    @property
    def capabilities(self) -> List[ProviderCapability]:
        """Supported capabilities."""
        ...

    async def generate(self, composition, output_dir, force=False):
        """Generate platform files from composition."""
        ...

    async def validate(self, composition, output_dir):
        """Validate platform files against composition."""
        ...

    async def update(self, composition, output_dir):
        """Update platform files when composition changes."""
        ...

    async def clean(self, output_dir):
        """Remove all generated platform files."""
        ...
```

### Provider Capabilities

Providers declare supported capabilities:

```python
from forge.providers.protocol import ProviderCapability

class ClaudeCodeProvider:
    @property
    def capabilities(self):
        return [
            ProviderCapability.AGENTS,
            ProviderCapability.COMMANDS,
            ProviderCapability.HOOKS,
            ProviderCapability.TOOLS,
            ProviderCapability.SETTINGS,
        ]
```

Available capabilities:
- `AGENTS` - AI agent support
- `COMMANDS` - Custom commands/workflows
- `HOOKS` - Event-driven automation
- `TOOLS` - Executable tools/scripts
- `TEMPLATES` - Document templates
- `SETTINGS` - Platform configuration

### Provider Registry

Register and discover providers:

```python
from forge.providers.protocol import ProviderRegistry
from forge.providers import ClaudeCodeProvider

registry = ProviderRegistry()
registry.register(ClaudeCodeProvider())

provider = registry.get("claude-code")

available = registry.list_providers()
with_agents = registry.list_providers_with_capability(
    ProviderCapability.AGENTS
)
```

## Usage

### Command Line

Generate files for a specific provider:

```bash
forge generate <provider-name>
```

Options:
- `--force` / `-f` - Overwrite existing files
- `--project-dir` / `-d` - Specify project directory

Examples:

```bash
forge generate claude-code
forge generate claude-code --force
forge generate cursor --project-dir /path/to/project
```

Validate integration:

```bash
forge validate <provider-name>
```

Update after changes:

```bash
forge update <provider-name>
```

Clean generated files:

```bash
forge clean <provider-name>
```

### Python API

```python
import asyncio
from pathlib import Path
from forge.core.element import ElementLoader
from forge.core.composition import CompositionLoader
from forge.providers import ClaudeCodeProvider

async def main():
    element_loader = ElementLoader(search_paths=[Path("elements")])
    composition_loader = CompositionLoader(element_loader)

    composition = composition_loader.load(Path(".forge/composition.yaml"))

    provider = ClaudeCodeProvider()

    result = await provider.generate(composition, Path("."), force=True)

    if result.success:
        print(f"✓ Generated {len(result.files_created)} files")
        for file in result.files_created:
            print(f"  • {file}")
    else:
        print("✗ Generation failed")
        for error in result.errors:
            print(f"  {error}")

asyncio.run(main())
```

## Creating a Custom Provider

### Step 1: Implement Provider Protocol

```python
from typing import List
from pathlib import Path
from forge.providers.protocol import (
    Provider,
    ProviderCapability,
    GenerationResult,
    ValidationResult,
)

class MyCustomProvider:
    @property
    def name(self) -> str:
        return "my-platform"

    @property
    def capabilities(self) -> List[ProviderCapability]:
        return [
            ProviderCapability.AGENTS,
            ProviderCapability.COMMANDS,
        ]

    async def generate(self, composition, output_dir, force=False):
        files_created = []
        errors = []

        platform_dir = output_dir / ".myplatform"
        platform_dir.mkdir(parents=True, exist_ok=True)

        try:
            agents = composition.get_agents()
            for agent in agents:
                agent_file = platform_dir / f"{agent.name}.config"
                content = self._format_agent(agent)
                agent_file.write_text(content)
                files_created.append(agent_file)

        except Exception as e:
            errors.append(str(e))

        return GenerationResult(
            success=len(errors) == 0,
            files_created=files_created,
            files_updated=[],
            errors=errors,
            warnings=[],
        )

    def _format_agent(self, agent):
        return f"""
        [agent]
        name = "{agent.name}"
        description = "{agent.metadata.description}"
        prompt = '''
        {agent.content}
        '''
        """

    async def validate(self, composition, output_dir):
        # Implementation
        ...

    async def update(self, composition, output_dir):
        return await self.generate(composition, output_dir, force=True)

    async def clean(self, output_dir):
        # Implementation
        ...
```

### Step 2: Register Provider

```python
from forge.providers.protocol import ProviderRegistry

registry = ProviderRegistry()
registry.register(MyCustomProvider())
```

### Step 3: Test Provider

```python
import pytest

@pytest.mark.asyncio
async def test_my_provider_generates_files(composition, temp_dir):
    provider = MyCustomProvider()

    result = await provider.generate(composition, temp_dir)

    assert result.success
    assert len(result.files_created) > 0

    config_file = temp_dir / ".myplatform" / "agent.config"
    assert config_file.exists()
```

## Best Practices

### 1. Idempotent Generation

Ensure `generate()` can be run multiple times safely:

```python
async def generate(self, composition, output_dir, force=False):
    platform_dir = output_dir / ".myplatform"

    if platform_dir.exists() and not force:
        return GenerationResult(
            success=False,
            errors=[f"{platform_dir} already exists. Use force=True"],
            ...
        )

    # Proceed with generation
```

### 2. Detailed Error Reporting

Provide clear error messages and context:

```python
try:
    agent_file.write_text(content)
except Exception as e:
    errors.append(
        f"Failed to write agent '{agent.name}' to {agent_file}: {str(e)}"
    )
```

### 3. Atomic Operations

Use temp files and rename for atomic writes:

```python
import tempfile
import shutil

temp_file = Path(tempfile.mktemp())
temp_file.write_text(content)
shutil.move(temp_file, target_file)
```

### 4. Validation Feedback

Provide actionable suggestions in validation:

```python
async def validate(self, composition, output_dir):
    suggestions = []

    if not config_file.exists():
        suggestions.append(
            f"Run 'forge generate {self.name}' to create missing files"
        )

    return ValidationResult(
        valid=len(errors) == 0,
        errors=errors,
        warnings=warnings,
        suggestions=suggestions,
    )
```

### 5. Preserve Platform-Specific Features

Allow platform-specific customizations:

```python
async def generate(self, composition, output_dir, force=False):
    # Check for existing customizations
    custom_settings = self._load_custom_settings(output_dir)

    # Generate files
    ...

    # Merge custom settings back
    if custom_settings:
        self._merge_custom_settings(output_dir, custom_settings)
```

## Provider Patterns

### Pattern 1: Frontmatter + Content

Separate metadata from content (Markdown, YAML):

```python
def _format_agent(self, agent):
    frontmatter = self._build_frontmatter(agent)
    content = agent.content or "Default prompt"

    return f"""---
{frontmatter}---

{content}
"""
```

### Pattern 2: Configuration Files

Generate platform-specific config files (JSON, TOML):

```python
import json

def _generate_config(self, composition):
    config = {
        "version": composition.version,
        "agents": [a.name for a in composition.get_agents()],
        "settings": composition.settings.to_dict(),
    }

    return json.dumps(config, indent=2)
```

### Pattern 3: Script Generation

Generate executable scripts with proper permissions:

```python
def _generate_hook_script(self, hook):
    script = hook.implementation.get("script")
    script_type = hook.implementation.get("script_type", "py")

    script_file = output_dir / f"hook_{hook.name}.{script_type}"
    script_file.write_text(script)

    if script_type == "sh":
        script_file.chmod(0o755)

    return script_file
```

## Testing Providers

### Unit Tests

Test individual provider methods:

```python
@pytest.mark.asyncio
async def test_format_agent():
    provider = MyProvider()
    agent = create_test_agent()

    formatted = provider._format_agent(agent)

    assert agent.name in formatted
    assert agent.content in formatted
```

### Integration Tests

Test full generation workflow:

```python
@pytest.mark.asyncio
async def test_full_generation_workflow(composition, temp_dir):
    provider = MyProvider()

    # Generate
    result = await provider.generate(composition, temp_dir)
    assert result.success

    # Validate
    validation = await provider.validate(composition, temp_dir)
    assert validation.valid

    # Update
    update_result = await provider.update(composition, temp_dir)
    assert update_result.success

    # Clean
    clean_result = await provider.clean(temp_dir)
    assert clean_result.success
    assert not (temp_dir / ".myplatform").exists()
```

### Fixture Patterns

```python
@pytest.fixture
def temp_project_dir():
    temp_dir = Path(tempfile.mkdtemp())
    yield temp_dir
    shutil.rmtree(temp_dir)

@pytest.fixture
def element_loader():
    return ElementLoader(search_paths=[Path("elements")])

@pytest.fixture
def test_composition(element_loader):
    loader = CompositionLoader(element_loader)
    return loader.load(Path("test-composition.yaml"))
```

## See Also

- [Claude Code Provider](./claude-code.md)
- [Element Types](../element-types.md)
- [Composition System](../CUSTOM_COMPOSITIONS.md)
- [Forge README](../../README.md)

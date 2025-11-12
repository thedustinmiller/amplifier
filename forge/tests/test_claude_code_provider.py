"""
Tests for Claude Code provider.
"""

import asyncio
import json
from pathlib import Path
import tempfile
import shutil
import pytest

from forge.core.element import ElementLoader, ElementType
from forge.core.composition import CompositionLoader
from forge.providers.claude_code import ClaudeCodeProvider


@pytest.fixture
def temp_project_dir():
    """Create temporary project directory."""
    temp_dir = Path(tempfile.mkdtemp())
    yield temp_dir
    shutil.rmtree(temp_dir)


@pytest.fixture
def element_loader():
    """Create element loader."""
    forge_root = Path(__file__).parent.parent
    return ElementLoader(search_paths=[forge_root / "elements"])


@pytest.fixture
def example_composition(element_loader):
    """Load example composition."""
    forge_root = Path(__file__).parent.parent
    composition_file = forge_root / "examples" / "example-composition.yaml"

    loader = CompositionLoader(element_loader)
    return loader.load(composition_file)


@pytest.mark.asyncio
async def test_provider_properties():
    """Test provider basic properties."""
    provider = ClaudeCodeProvider()

    assert provider.name == "claude-code"
    assert len(provider.capabilities) > 0


@pytest.mark.asyncio
async def test_generate_creates_directory_structure(
    example_composition, temp_project_dir
):
    """Test that generate creates .claude/ directory structure."""
    provider = ClaudeCodeProvider()

    result = await provider.generate(example_composition, temp_project_dir)

    assert result.success
    assert len(result.errors) == 0

    claude_dir = temp_project_dir / ".claude"
    assert claude_dir.exists()
    assert (claude_dir / "agents").exists()
    assert (claude_dir / "commands").exists()
    assert (claude_dir / "tools").exists()


@pytest.mark.asyncio
async def test_generate_creates_agent_files(example_composition, temp_project_dir):
    """Test that agents are generated correctly."""
    provider = ClaudeCodeProvider()

    result = await provider.generate(example_composition, temp_project_dir)

    assert result.success

    agent_file = temp_project_dir / ".claude" / "agents" / "code-reviewer.md"
    assert agent_file.exists()

    content = agent_file.read_text()
    assert "name: code-reviewer" in content
    assert "---" in content
    assert "code reviewer" in content.lower()


@pytest.mark.asyncio
async def test_generate_creates_command_files(example_composition, temp_project_dir):
    """Test that commands are generated correctly."""
    provider = ClaudeCodeProvider()

    result = await provider.generate(example_composition, temp_project_dir)

    assert result.success

    command_file = temp_project_dir / ".claude" / "commands" / "scaffold.md"
    assert command_file.exists()

    content = command_file.read_text()
    assert "description:" in content
    assert "scaffold" in content.lower()


@pytest.mark.asyncio
async def test_generate_creates_hook_scripts(example_composition, temp_project_dir):
    """Test that hook scripts are generated correctly."""
    provider = ClaudeCodeProvider()

    result = await provider.generate(example_composition, temp_project_dir)

    assert result.success

    hook_file = temp_project_dir / ".claude" / "tools" / "hook_sessionstart.py"
    assert hook_file.exists()

    content = hook_file.read_text()
    assert "#!/usr/bin/env python3" in content


@pytest.mark.asyncio
async def test_generate_creates_settings_json(example_composition, temp_project_dir):
    """Test that settings.json is generated correctly."""
    provider = ClaudeCodeProvider()

    result = await provider.generate(example_composition, temp_project_dir)

    assert result.success

    settings_file = temp_project_dir / ".claude" / "settings.json"
    assert settings_file.exists()

    settings = json.loads(settings_file.read_text())
    assert "permissions" in settings
    assert "hooks" in settings
    assert "SessionStart" in settings["hooks"]


@pytest.mark.asyncio
async def test_generate_creates_readme(example_composition, temp_project_dir):
    """Test that README is generated."""
    provider = ClaudeCodeProvider()

    result = await provider.generate(example_composition, temp_project_dir)

    assert result.success

    readme_file = temp_project_dir / ".claude" / "README.md"
    assert readme_file.exists()

    content = readme_file.read_text()
    assert "example-workflow" in content
    assert "Forge" in content


@pytest.mark.asyncio
async def test_generate_fails_if_directory_exists(
    example_composition, temp_project_dir
):
    """Test that generate fails if .claude/ exists without force."""
    provider = ClaudeCodeProvider()

    await provider.generate(example_composition, temp_project_dir)

    result = await provider.generate(example_composition, temp_project_dir, force=False)

    assert not result.success
    assert len(result.errors) > 0
    assert ".claude/" in result.errors[0]


@pytest.mark.asyncio
async def test_generate_with_force_overwrites(example_composition, temp_project_dir):
    """Test that generate with force=True overwrites files."""
    provider = ClaudeCodeProvider()

    await provider.generate(example_composition, temp_project_dir)

    result = await provider.generate(example_composition, temp_project_dir, force=True)

    assert result.success


@pytest.mark.asyncio
async def test_validate_detects_missing_directory(
    example_composition, temp_project_dir
):
    """Test that validate detects missing .claude/ directory."""
    provider = ClaudeCodeProvider()

    result = await provider.validate(example_composition, temp_project_dir)

    assert not result.valid
    assert len(result.errors) > 0


@pytest.mark.asyncio
async def test_validate_detects_missing_files(example_composition, temp_project_dir):
    """Test that validate detects missing files."""
    provider = ClaudeCodeProvider()

    (temp_project_dir / ".claude").mkdir()
    (temp_project_dir / ".claude" / "agents").mkdir()
    (temp_project_dir / ".claude" / "commands").mkdir()
    (temp_project_dir / ".claude" / "tools").mkdir()

    result = await provider.validate(example_composition, temp_project_dir)

    assert result.valid
    assert len(result.warnings) > 0


@pytest.mark.asyncio
async def test_validate_passes_after_generate(example_composition, temp_project_dir):
    """Test that validate passes after successful generate."""
    provider = ClaudeCodeProvider()

    await provider.generate(example_composition, temp_project_dir)

    result = await provider.validate(example_composition, temp_project_dir)

    assert result.valid


@pytest.mark.asyncio
async def test_clean_removes_directory(example_composition, temp_project_dir):
    """Test that clean removes .claude/ directory."""
    provider = ClaudeCodeProvider()

    await provider.generate(example_composition, temp_project_dir)

    claude_dir = temp_project_dir / ".claude"
    assert claude_dir.exists()

    result = await provider.clean(temp_project_dir)

    assert result.success
    assert not claude_dir.exists()


@pytest.mark.asyncio
async def test_update_regenerates_files(example_composition, temp_project_dir):
    """Test that update regenerates files."""
    provider = ClaudeCodeProvider()

    await provider.generate(example_composition, temp_project_dir)

    agent_file = temp_project_dir / ".claude" / "agents" / "code-reviewer.md"
    agent_file.write_text("modified content")

    result = await provider.update(example_composition, temp_project_dir)

    assert result.success

    content = agent_file.read_text()
    assert "modified content" not in content
    assert "code reviewer" in content.lower()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

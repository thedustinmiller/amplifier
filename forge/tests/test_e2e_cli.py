"""
End-to-end integration tests for Forge CLI.

Tests the complete user workflow as it would be used in practice.
"""

import asyncio
import tempfile
import shutil
from pathlib import Path
import subprocess
import pytest


class TestForgeEndToEnd:
    """End-to-end tests for Forge CLI commands."""

    @pytest.fixture
    def temp_workspace(self):
        """Create temporary workspace for testing."""
        temp_dir = Path(tempfile.mkdtemp())
        yield temp_dir
        shutil.rmtree(temp_dir)

    def run_forge(self, args, cwd=None):
        """Run forge command and return result."""
        result = subprocess.run(
            ["forge"] + args,
            cwd=cwd or Path.cwd(),
            capture_output=True,
            text=True,
        )
        return result

    def test_forge_help(self):
        """Test forge help command."""
        result = self.run_forge([])

        assert result.returncode == 0
        assert "Forge CLI" in result.stdout
        assert "forge init" in result.stdout
        assert "forge generate" in result.stdout
        assert "forge validate" in result.stdout

    def test_forge_version(self):
        """Test forge version command."""
        result = self.run_forge(["version"])

        assert result.returncode == 0
        assert "Forge" in result.stdout
        assert "0.1.0" in result.stdout

    def test_complete_workflow(self, temp_workspace):
        """Test complete workflow: init -> generate -> validate -> clean."""
        project_dir = temp_workspace / "test-project"
        project_dir.mkdir()

        composition_content = """composition:
  name: test-project
  type: preset
  version: 1.0.0
  description: Test project

elements:
  principles:
    - ruthless-minimalism
    - coevolution
  agents:
    - code-reviewer
  tools:
    - scaffold
  hooks:
    SessionStart: session-logger

settings:
  memory:
    provider: file
    config:
      base_path: .forge/memory
"""

        forge_dir = project_dir / ".forge"
        forge_dir.mkdir()
        (forge_dir / "composition.yaml").write_text(composition_content)

        result = self.run_forge(["generate", "claude-code"], cwd=project_dir)

        assert result.returncode == 0, f"Generate failed: {result.stderr}"
        assert "Generation complete!" in result.stdout
        assert "Created" in result.stdout

        claude_dir = project_dir / ".claude"
        assert claude_dir.exists()
        assert (claude_dir / "settings.json").exists()
        assert (claude_dir / "README.md").exists()
        assert (claude_dir / "agents" / "code-reviewer.md").exists()
        assert (claude_dir / "commands" / "scaffold.md").exists()
        assert (claude_dir / "tools" / "hook_sessionstart.py").exists()

        result = self.run_forge(["validate", "claude-code"], cwd=project_dir)

        assert result.returncode == 0, f"Validate failed: {result.stderr}"
        assert "Validation passed!" in result.stdout

        result = self.run_forge(
            ["clean", "claude-code", "--force"], cwd=project_dir
        )

        assert result.returncode == 0, f"Clean failed: {result.stderr}"
        assert "Clean complete!" in result.stdout
        assert not claude_dir.exists()

    def test_generate_force_overwrite(self, temp_workspace):
        """Test generate with --force flag."""
        project_dir = temp_workspace / "test-project"
        project_dir.mkdir()

        composition_content = """composition:
  name: test-project
  type: preset
  version: 1.0.0

elements:
  principles: []
  agents: []
  tools: []
  hooks: {}

settings:
  memory:
    provider: file
"""

        forge_dir = project_dir / ".forge"
        forge_dir.mkdir()
        (forge_dir / "composition.yaml").write_text(composition_content)

        result = self.run_forge(["generate", "claude-code"], cwd=project_dir)
        assert result.returncode == 0

        result = self.run_forge(["generate", "claude-code"], cwd=project_dir)
        assert result.returncode == 1
        assert "already exists" in result.stderr

        result = self.run_forge(
            ["generate", "claude-code", "--force"], cwd=project_dir
        )
        assert result.returncode == 0
        assert "Generation complete!" in result.stdout

    def test_generate_without_composition(self, temp_workspace):
        """Test generate fails gracefully without composition."""
        result = self.run_forge(["generate", "claude-code"], cwd=temp_workspace)

        assert result.returncode == 1
        assert "Composition not found" in result.stderr

    def test_validate_without_files(self, temp_workspace):
        """Test validate detects missing files."""
        project_dir = temp_workspace / "test-project"
        project_dir.mkdir()

        composition_content = """composition:
  name: test-project
  type: preset
  version: 1.0.0

elements:
  principles: []
  agents: []
  tools: []
  hooks: {}

settings:
  memory:
    provider: file
"""

        forge_dir = project_dir / ".forge"
        forge_dir.mkdir()
        (forge_dir / "composition.yaml").write_text(composition_content)

        result = self.run_forge(["validate", "claude-code"], cwd=project_dir)

        assert result.returncode == 1
        assert "not found" in result.stderr or "Validation failed" in result.stderr

    def test_update_regenerates_files(self, temp_workspace):
        """Test update command regenerates files."""
        project_dir = temp_workspace / "test-project"
        project_dir.mkdir()

        composition_content = """composition:
  name: test-project
  type: preset
  version: 1.0.0

elements:
  principles:
    - ruthless-minimalism
  agents:
    - code-reviewer
  tools: []
  hooks: {}

settings:
  memory:
    provider: file
"""

        forge_dir = project_dir / ".forge"
        forge_dir.mkdir()
        (forge_dir / "composition.yaml").write_text(composition_content)

        result = self.run_forge(["generate", "claude-code"], cwd=project_dir)
        assert result.returncode == 0

        agent_file = project_dir / ".claude" / "agents" / "code-reviewer.md"
        original_content = agent_file.read_text()

        agent_file.write_text("MODIFIED CONTENT")

        result = self.run_forge(["update", "claude-code"], cwd=project_dir)
        assert result.returncode == 0
        assert "Update complete!" in result.stdout

        new_content = agent_file.read_text()
        assert "MODIFIED CONTENT" not in new_content
        assert "code reviewer" in new_content.lower()

    def test_element_discovery(self, temp_workspace):
        """Test that elements can be discovered from package."""
        from forge.utils import get_element_search_paths
        from forge.core.element import ElementLoader, ElementType

        search_paths = get_element_search_paths()

        assert len(search_paths) > 0, "No element search paths found"

        loader = ElementLoader(search_paths=search_paths)

        principles = loader.list_elements(ElementType.PRINCIPLE)
        assert len(principles) > 0, "No principles found"

        agents = loader.list_elements(ElementType.AGENT)
        assert len(agents) > 0, "No agents found"

        tools = loader.list_elements(ElementType.TOOL)
        assert len(tools) > 0, "No tools found"

    def test_project_local_elements_override(self, temp_workspace):
        """Test that project-local elements take precedence."""
        project_dir = temp_workspace / "test-project"
        project_dir.mkdir()

        forge_dir = project_dir / ".forge"
        forge_dir.mkdir()

        local_elements = forge_dir / "elements" / "agent" / "custom-agent"
        local_elements.mkdir(parents=True)

        element_yaml = local_elements / "element.yaml"
        element_yaml.write_text(
            """metadata:
  name: custom-agent
  type: agent
  version: 1.0.0
  description: Custom local agent

dependencies:
  principles: []
  tools: []
  agents: []

interface:
  inputs: {}
  outputs: {}

implementation:
  model: inherit
  prompt: "Custom agent prompt"

settings: {}
"""
        )

        from forge.utils import get_element_search_paths
        from forge.core.element import ElementLoader, ElementType

        search_paths = get_element_search_paths(project_dir)

        assert str(forge_dir / "elements") in [str(p) for p in search_paths]

        loader = ElementLoader(search_paths=search_paths)
        custom_agent = loader.load("custom-agent", ElementType.AGENT)

        assert custom_agent.name == "custom-agent"
        assert custom_agent.metadata.description == "Custom local agent"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

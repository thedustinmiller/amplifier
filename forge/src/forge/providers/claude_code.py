"""
Claude Code provider for Forge.

Generates .claude/ directory structure from Forge compositions.
"""

import json
from pathlib import Path
from typing import Dict, List, Any, Optional
import logging

from forge.core.composition import LoadedComposition
from forge.core.element import Element, ElementType
from forge.providers.protocol import (
    Provider,
    ProviderCapability,
    GenerationResult,
    ValidationResult,
)

logger = logging.getLogger(__name__)


class ClaudeCodeProvider:
    """Claude Code provider implementation.

    Converts Forge compositions to Claude Code format:
    - Agents → .claude/agents/[name].md
    - Commands → .claude/commands/[name].md
    - Tools → .claude/tools/[name].py
    - Hooks → settings.json
    """

    @property
    def name(self) -> str:
        """Provider name."""
        return "claude-code"

    @property
    def capabilities(self) -> List[ProviderCapability]:
        """Supported capabilities."""
        return [
            ProviderCapability.AGENTS,
            ProviderCapability.COMMANDS,
            ProviderCapability.HOOKS,
            ProviderCapability.TOOLS,
            ProviderCapability.SETTINGS,
        ]

    async def generate(
        self, composition: LoadedComposition, output_dir: Path, force: bool = False
    ) -> GenerationResult:
        """Generate .claude/ structure from composition."""
        files_created = []
        files_updated = []
        errors = []
        warnings = []

        claude_dir = output_dir / ".claude"

        if claude_dir.exists() and not force:
            errors.append(
                f".claude/ directory already exists at {claude_dir}. Use force=True to overwrite."
            )
            return GenerationResult(
                success=False,
                files_created=files_created,
                files_updated=files_updated,
                errors=errors,
                warnings=warnings,
            )

        claude_dir.mkdir(parents=True, exist_ok=True)

        (claude_dir / "agents").mkdir(exist_ok=True)
        (claude_dir / "commands").mkdir(exist_ok=True)
        (claude_dir / "tools").mkdir(exist_ok=True)

        try:
            agent_files = await self._generate_agents(composition, claude_dir)
            files_created.extend(agent_files)

            command_files = await self._generate_commands(composition, claude_dir)
            files_created.extend(command_files)

            tool_files = await self._generate_tools(composition, claude_dir)
            files_created.extend(tool_files)

            settings_file = await self._generate_settings(composition, claude_dir)
            if settings_file:
                files_created.append(settings_file)

            readme_file = await self._generate_readme(composition, claude_dir)
            if readme_file:
                files_created.append(readme_file)

        except Exception as e:
            errors.append(f"Generation failed: {str(e)}")
            logger.exception("Generation failed")
            return GenerationResult(
                success=False,
                files_created=files_created,
                files_updated=files_updated,
                errors=errors,
                warnings=warnings,
            )

        return GenerationResult(
            success=True,
            files_created=files_created,
            files_updated=files_updated,
            errors=errors,
            warnings=warnings,
        )

    async def _generate_agents(
        self, composition: LoadedComposition, claude_dir: Path
    ) -> List[Path]:
        """Generate agent files."""
        files = []
        agents = composition.get_agents()

        for agent in agents:
            agent_file = claude_dir / "agents" / f"{agent.name}.md"
            content = self._format_agent(agent)
            agent_file.write_text(content)
            files.append(agent_file)
            logger.info(f"Generated agent: {agent_file}")

        return files

    def _format_agent(self, agent: Element) -> str:
        """Format agent as Claude Code markdown."""
        frontmatter = self._build_agent_frontmatter(agent)
        system_prompt = agent.content or "You are a helpful AI assistant."

        if agent.implementation and "prompt" in agent.implementation:
            system_prompt = agent.implementation["prompt"]

        return f"""---
{frontmatter}---

{system_prompt}
"""

    def _build_agent_frontmatter(self, agent: Element) -> str:
        """Build agent frontmatter."""
        lines = []

        lines.append(f"name: {agent.name}")

        if agent.metadata.description:
            description = agent.metadata.description.replace('"', '\\"')
            lines.append(f'description: "{description}"')

        model = "inherit"
        if agent.implementation and "model" in agent.implementation:
            model = agent.implementation["model"]
        lines.append(f"model: {model}")

        if agent.interface.role:
            lines.append(f'role: "{agent.interface.role}"')

        return "\n".join(lines)

    async def _generate_commands(
        self, composition: LoadedComposition, claude_dir: Path
    ) -> List[Path]:
        """Generate command files."""
        files = []
        commands = composition.get_commands()

        for command in commands:
            command_file = claude_dir / "commands" / f"{command.name}.md"
            content = self._format_command(command)
            command_file.write_text(content)
            files.append(command_file)
            logger.info(f"Generated command: {command_file}")

        return files

    def _format_command(self, command: Element) -> str:
        """Format command as Claude Code command."""
        frontmatter = self._build_command_frontmatter(command)

        instructions = command.content or f"Execute {command.name} command."
        if command.implementation and "instructions" in command.implementation:
            instructions = command.implementation["instructions"]

        return f"""---
{frontmatter}---

{instructions}
"""

    def _build_command_frontmatter(self, command: Element) -> str:
        """Build command frontmatter."""
        lines = []

        if command.metadata.description:
            description = command.metadata.description.replace('"', '\\"')
            lines.append(f'description: "{description}"')

        if command.metadata.tags:
            category = command.metadata.tags[0]
            lines.append(f"category: {category}")

        allowed_tools = ["Bash", "Read", "Write", "Edit", "Glob", "Grep"]
        if command.implementation and "allowed_tools" in command.implementation:
            allowed_tools = command.implementation["allowed_tools"]

        lines.append(f"allowed-tools: {', '.join(allowed_tools)}")

        return "\n".join(lines)

    async def _generate_tools(
        self, composition: LoadedComposition, claude_dir: Path
    ) -> List[Path]:
        """Generate tool scripts."""
        files = []

        hooks = composition.get_hooks()
        for event, hook in hooks.items():
            if not hook.implementation or "script" not in hook.implementation:
                continue

            script_content = hook.implementation["script"]
            script_ext = hook.implementation.get("script_type", "py")
            tool_file = claude_dir / "tools" / f"hook_{event.lower()}.{script_ext}"

            tool_file.write_text(script_content)
            if script_ext == "sh":
                tool_file.chmod(0o755)

            files.append(tool_file)
            logger.info(f"Generated tool: {tool_file}")

        return files

    async def _generate_settings(
        self, composition: LoadedComposition, claude_dir: Path
    ) -> Optional[Path]:
        """Generate settings.json with hooks configuration."""
        settings = {
            "permissions": {
                "allow": ["Bash", "TodoWrite", "WebFetch"],
                "deny": [],
                "defaultMode": "bypassPermissions",
                "additionalDirectories": [".forge", ".data"],
            },
            "enableAllProjectMcpServers": False,
            "enabledMcpjsonServers": [],
            "hooks": {},
        }

        hooks = composition.get_hooks()
        for event, hook in hooks.items():
            hook_config = self._build_hook_config(event, hook, claude_dir)
            if hook_config:
                settings["hooks"][event] = hook_config

        settings_file = claude_dir / "settings.json"
        settings_file.write_text(json.dumps(settings, indent=2))
        logger.info(f"Generated settings: {settings_file}")

        return settings_file

    def _build_hook_config(
        self, event: str, hook: Element, claude_dir: Path
    ) -> Optional[List[Dict[str, Any]]]:
        """Build hook configuration for settings.json."""
        if not hook.implementation:
            return None

        config = []

        matcher = hook.implementation.get("matcher", "*")
        script_type = hook.implementation.get("script_type", "py")
        timeout = hook.implementation.get("timeout", 5000)

        tool_file = claude_dir / "tools" / f"hook_{event.lower()}.{script_type}"

        hook_entry = {
            "hooks": [
                {
                    "type": "command",
                    "command": f"$CLAUDE_PROJECT_DIR/.claude/tools/{tool_file.name}",
                    "timeout": timeout,
                }
            ]
        }

        if matcher != "*":
            hook_entry["matcher"] = matcher

        config.append(hook_entry)

        return config

    async def _generate_readme(
        self, composition: LoadedComposition, claude_dir: Path
    ) -> Optional[Path]:
        """Generate README.md for .claude/ directory."""
        readme_content = f"""# Claude Code Configuration for {composition.composition.name}

Generated by Forge from composition: `{composition.composition.name}`

## Composition Overview

**Type**: {composition.composition.type}
**Version**: {composition.composition.version}

{composition.composition.description or 'No description provided.'}

## Active Elements

### Principles
{self._format_element_list(composition.get_principles())}

### Constitutions
{self._format_element_list(composition.get_constitutions())}

### Agents
{self._format_element_list(composition.get_agents())}

### Commands
{self._format_element_list(composition.get_commands())}

### Tools
{self._format_element_list(composition.get_tools())}

### Hooks
{self._format_hook_list(composition.get_hooks())}

## Memory Configuration

**Provider**: {composition.composition.settings.memory.get('provider', 'file')}

## Directory Structure

```
.claude/
├── agents/           # AI agents for specialized tasks
├── commands/         # Slash commands
├── tools/            # Automation scripts and hooks
├── settings.json     # Claude Code settings and hooks
└── README.md         # This file
```

## Usage

This configuration is automatically loaded by Claude Code when you work in this project.

- **Agents**: Invoked via Task tool with subagent_type parameter
- **Commands**: Available as `/command-name` in Claude Code
- **Hooks**: Triggered automatically on events (session start, tool use, etc.)

## Updating Configuration

To update this configuration:

1. Modify your Forge composition in `.forge/composition.yaml`
2. Run: `forge generate claude-code`

This will regenerate all Claude Code files from your composition.

---

*Generated by Forge v{composition.composition.version}*
"""

        readme_file = claude_dir / "README.md"
        readme_file.write_text(readme_content)
        logger.info(f"Generated README: {readme_file}")

        return readme_file

    def _format_element_list(self, elements: List[Element]) -> str:
        """Format element list for README."""
        if not elements:
            return "*None*"

        lines = []
        for elem in elements:
            desc = elem.metadata.description or "No description"
            lines.append(f"- **{elem.name}**: {desc}")

        return "\n".join(lines)

    def _format_hook_list(self, hooks: Dict[str, Element]) -> str:
        """Format hook list for README."""
        if not hooks:
            return "*None*"

        lines = []
        for event, hook in hooks.items():
            desc = hook.metadata.description or "No description"
            lines.append(f"- **{event}**: {hook.name} - {desc}")

        return "\n".join(lines)

    async def sync(
        self, composition: LoadedComposition, output_dir: Path
    ) -> GenerationResult:
        """Sync changes bidirectionally."""
        return await self.update(composition, output_dir)

    async def validate(
        self, composition: LoadedComposition, output_dir: Path
    ) -> ValidationResult:
        """Validate .claude/ structure against composition."""
        errors = []
        warnings = []
        suggestions = []

        claude_dir = output_dir / ".claude"

        if not claude_dir.exists():
            errors.append(f".claude/ directory not found at {claude_dir}")
            return ValidationResult(
                valid=False, errors=errors, warnings=warnings, suggestions=suggestions
            )

        agents = composition.get_agents()
        for agent in agents:
            agent_file = claude_dir / "agents" / f"{agent.name}.md"
            if not agent_file.exists():
                warnings.append(f"Agent file missing: {agent_file.name}")

        commands = composition.get_commands()
        for command in commands:
            command_file = claude_dir / "commands" / f"{command.name}.md"
            if not command_file.exists():
                warnings.append(f"Command file missing: {command_file.name}")

        settings_file = claude_dir / "settings.json"
        if not settings_file.exists():
            warnings.append("settings.json not found")

        if warnings:
            suggestions.append("Run 'forge generate claude-code' to sync files")

        valid = len(errors) == 0

        return ValidationResult(
            valid=valid, errors=errors, warnings=warnings, suggestions=suggestions
        )

    async def update(
        self, composition: LoadedComposition, output_dir: Path
    ) -> GenerationResult:
        """Update .claude/ files when composition changes."""
        return await self.generate(composition, output_dir, force=True)

    async def clean(self, output_dir: Path) -> GenerationResult:
        """Remove .claude/ directory."""
        import shutil

        files_removed = []
        errors = []

        claude_dir = output_dir / ".claude"

        if not claude_dir.exists():
            return GenerationResult(
                success=True,
                files_created=[],
                files_updated=[],
                errors=errors,
                warnings=[f".claude/ directory not found at {claude_dir}"],
            )

        try:
            for item in claude_dir.rglob("*"):
                if item.is_file():
                    files_removed.append(item)

            shutil.rmtree(claude_dir)
            logger.info(f"Removed .claude/ directory: {claude_dir}")

        except Exception as e:
            errors.append(f"Failed to remove .claude/: {str(e)}")
            logger.exception("Clean failed")
            return GenerationResult(
                success=False,
                files_created=[],
                files_updated=files_removed,
                errors=errors,
                warnings=[],
            )

        return GenerationResult(
            success=True,
            files_created=[],
            files_updated=files_removed,
            errors=errors,
            warnings=[],
        )

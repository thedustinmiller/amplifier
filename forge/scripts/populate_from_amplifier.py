#!/usr/bin/env python3
"""
Extract and convert elements from amplifier to Forge format.
"""

from pathlib import Path
import re
import yaml


def extract_agent_frontmatter(content: str) -> dict:
    """Extract frontmatter from Claude Code agent file."""
    if not content.startswith('---'):
        return {}

    parts = content.split('---', 2)
    if len(parts) < 3:
        return {}

    try:
        return yaml.safe_load(parts[1])
    except:
        return {}


def extract_agent_content(content: str) -> str:
    """Extract main content from agent file (after frontmatter)."""
    if not content.startswith('---'):
        return content

    parts = content.split('---', 2)
    if len(parts) < 3:
        return content

    return parts[2].strip()


def create_agent_element(agent_path: Path, output_dir: Path, dependencies: list = None):
    """Convert Claude Code agent to Forge element."""
    content = agent_path.read_text()
    frontmatter = extract_agent_frontmatter(content)
    agent_content = extract_agent_content(content)

    name = agent_path.stem
    element_dir = output_dir / "agent" / name
    element_dir.mkdir(parents=True, exist_ok=True)

    element_yaml = {
        "metadata": {
            "name": name,
            "type": "agent",
            "version": "1.0.0",
            "description": frontmatter.get("description", f"{name} agent"),
            "author": "amplifier",
            "tags": ["development", "ai-agent"],
            "license": "MIT"
        },
        "dependencies": {
            "principles": dependencies or [],
            "constitutions": [],
            "tools": [],
            "agents": [],
            "templates": [],
            "suggests": []
        },
        "conflicts": {
            "principles": [],
            "tools": [],
            "agents": [],
            "reason": None
        },
        "interface": {
            "inputs": {},
            "outputs": {},
            "role": name.replace("-", "_"),
            "events": []
        },
        "implementation": {
            "model": frontmatter.get("model", "inherit"),
            "prompt": agent_content
        },
        "settings": {}
    }

    with open(element_dir / "element.yaml", "w") as f:
        yaml.dump(element_yaml, f, default_flow_style=False, sort_keys=False)

    print(f"✓ Created agent: {name}")
    return element_dir


def create_tool_element(command_path: Path, output_dir: Path, dependencies: list = None):
    """Convert Claude Code command to Forge tool."""
    content = command_path.read_text()
    frontmatter = extract_agent_frontmatter(content)
    tool_content = extract_agent_content(content)

    name = command_path.stem
    element_dir = output_dir / "tool" / name
    element_dir.mkdir(parents=True, exist_ok=True)

    element_yaml = {
        "metadata": {
            "name": name,
            "type": "tool",
            "version": "1.0.0",
            "description": frontmatter.get("description", f"{name} command"),
            "author": "amplifier",
            "tags": ["workflow", "command"],
            "license": "MIT"
        },
        "dependencies": {
            "principles": dependencies or [],
            "constitutions": [],
            "tools": [],
            "agents": [],
            "templates": [],
            "suggests": []
        },
        "conflicts": {
            "principles": [],
            "tools": [],
            "agents": [],
            "reason": None
        },
        "interface": {
            "inputs": {"arguments": "Command arguments"},
            "outputs": {"result": "Command result"},
            "role": None,
            "events": []
        },
        "implementation": {
            "instructions": tool_content,
            "allowed_tools": frontmatter.get("allowed-tools", "Bash, Read, Write, Edit").split(", ")
        },
        "settings": {}
    }

    with open(element_dir / "element.yaml", "w") as f:
        yaml.dump(element_yaml, f, default_flow_style=False, sort_keys=False)

    print(f"✓ Created tool: {name}")
    return element_dir


def main():
    """Main extraction script."""
    amplifier_root = Path("/home/user/amplifier/amplifier")
    forge_root = Path("/home/user/amplifier/forge")
    elements_dir = forge_root / "elements"

    # Key agents to extract
    agents = [
        "zen-architect",
        "modular-builder",
        "bug-hunter",
        "test-coverage",
        "security-guardian",
        "post-task-cleanup"
    ]

    # Key commands to extract
    commands = [
        "commit",
        "review-changes",
        "modular-build",
        "create-plan"
    ]

    print("🔨 Extracting elements from amplifier...\n")

    print("📦 Creating agents:")
    for agent in agents:
        agent_path = amplifier_root / ".claude" / "agents" / f"{agent}.md"
        if agent_path.exists():
            create_agent_element(
                agent_path,
                elements_dir,
                dependencies=["ruthless-minimalism", "analysis-first"]
            )
        else:
            print(f"✗ Not found: {agent}")

    print("\n📦 Creating tools:")
    for command in commands:
        command_path = amplifier_root / ".claude" / "commands" / f"{command}.md"
        if command_path.exists():
            create_tool_element(
                command_path,
                elements_dir,
                dependencies=["respect-user-time"]
            )
        else:
            print(f"✗ Not found: {command}")

    print("\n✅ Done! Elements created in:", elements_dir)


if __name__ == "__main__":
    main()

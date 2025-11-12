"""
Forge CLI - Interactive wizard for project setup.
"""

import asyncio
import sys
from pathlib import Path
from typing import List, Optional

from forge.core.element import ElementLoader, ElementType
from forge.core.composition import Composition, CompositionElements, CompositionSettings
from forge.memory import FileProvider, Scope


class Colors:
    """ANSI color codes for terminal output."""
    RESET = "\033[0m"
    BOLD = "\033[1m"
    GREEN = "\033[92m"
    BLUE = "\033[94m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    CYAN = "\033[96m"


def print_header(text: str):
    """Print a colored header."""
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'=' * 60}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}{text:^60}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'=' * 60}{Colors.RESET}\n")


def print_section(text: str):
    """Print a section header."""
    print(f"\n{Colors.BOLD}{Colors.BLUE}▶ {text}{Colors.RESET}\n")


def print_success(text: str):
    """Print a success message."""
    print(f"{Colors.GREEN}✓ {text}{Colors.RESET}")


def print_error(text: str):
    """Print an error message."""
    print(f"{Colors.RED}✗ {text}{Colors.RESET}")


def print_info(text: str):
    """Print an info message."""
    print(f"{Colors.YELLOW}ℹ {text}{Colors.RESET}")


def get_input(prompt: str, default: Optional[str] = None) -> str:
    """Get user input with optional default."""
    if default:
        full_prompt = f"{prompt} [{Colors.YELLOW}{default}{Colors.RESET}]: "
    else:
        full_prompt = f"{prompt}: "

    value = input(full_prompt).strip()
    return value if value else (default or "")


def get_multiselect(prompt: str, options: List[tuple[str, str]], max_selections: Optional[int] = None) -> List[str]:
    """Get multiple selections from user.

    Args:
        prompt: Prompt to display
        options: List of (value, description) tuples
        max_selections: Maximum number of selections allowed

    Returns:
        List of selected values
    """
    print(f"\n{Colors.BOLD}{prompt}{Colors.RESET}")
    if max_selections:
        print(f"{Colors.YELLOW}(Select up to {max_selections} options){Colors.RESET}")
    else:
        print(f"{Colors.YELLOW}(Select as many as you like){Colors.RESET}")
    print(f"\n{Colors.CYAN}Enter numbers separated by spaces (e.g., '1 3 4') or 'all' for all options:{Colors.RESET}\n")

    for i, (value, description) in enumerate(options, 1):
        print(f"  {Colors.BOLD}{i}.{Colors.RESET} {Colors.GREEN}{value}{Colors.RESET}")
        print(f"     {description}")

    while True:
        response = input(f"\n{Colors.BOLD}Your selection:{Colors.RESET} ").strip().lower()

        if response == "all":
            if max_selections and len(options) > max_selections:
                print_error(f"Cannot select all - maximum {max_selections} allowed")
                continue
            return [value for value, _ in options]

        if not response:
            return []

        try:
            indices = [int(x.strip()) for x in response.split()]

            if any(i < 1 or i > len(options) for i in indices):
                print_error("Invalid selection - numbers must be between 1 and {}".format(len(options)))
                continue

            if max_selections and len(indices) > max_selections:
                print_error(f"Too many selections - maximum {max_selections} allowed")
                continue

            return [options[i - 1][0] for i in indices]

        except ValueError:
            print_error("Invalid input - please enter numbers separated by spaces")


def get_yes_no(prompt: str, default: bool = False) -> bool:
    """Get yes/no input from user."""
    default_str = "Y/n" if default else "y/N"
    response = input(f"{prompt} [{Colors.YELLOW}{default_str}{Colors.RESET}]: ").strip().lower()

    if not response:
        return default

    return response in ("y", "yes")


async def wizard_init():
    """Interactive wizard for initializing a Forge project."""
    print_header("🔨 Forge Project Wizard")

    print(f"""
{Colors.CYAN}Welcome to Forge!{Colors.RESET}

Forge is a composable AI development system. This wizard will help you:
  • Choose guiding principles for your project
  • Select development tools
  • Configure memory storage
  • Create your first composition

Let's get started!
""")

    # Project name
    print_section("Project Information")
    project_name = get_input("Project name", "my-project")
    project_path = Path.cwd() / project_name

    if project_path.exists():
        if not get_yes_no(f"Directory '{project_name}' already exists. Continue?", False):
            print_info("Aborted.")
            return

    # Create project directory
    project_path.mkdir(parents=True, exist_ok=True)
    forge_dir = project_path / ".forge"
    forge_dir.mkdir(exist_ok=True)

    print_success(f"Created project directory: {project_path}")

    # Load available elements
    print_section("Loading Available Elements")

    forge_root = Path(__file__).parent.parent.parent
    element_loader = ElementLoader(search_paths=[forge_root / "elements"])

    try:
        available_principles = element_loader.list_elements(ElementType.PRINCIPLE)
        print_success(f"Found {len(available_principles)} principles")
    except Exception as e:
        print_error(f"Error loading elements: {e}")
        available_principles = []

    # Select principles
    print_section("Choose Guiding Principles")

    print(f"""
{Colors.CYAN}Principles define your project's philosophy and values.{Colors.RESET}
They guide decision-making throughout development.
""")

    principle_options = []
    for p in available_principles:
        principle_options.append((p.name, p.metadata.description or "No description"))

    if principle_options:
        selected_principles = get_multiselect(
            "Select principles to guide your project:",
            principle_options,
            max_selections=5
        )
    else:
        print_info("No principles available. You can add them later.")
        selected_principles = []

    if selected_principles:
        print_success(f"Selected {len(selected_principles)} principles: {', '.join(selected_principles)}")

    # Memory configuration
    print_section("Memory Configuration")

    print(f"""
{Colors.CYAN}Memory stores context across sessions.{Colors.RESET}

Available providers:
  • {Colors.GREEN}file{Colors.RESET} - Simple JSON files (recommended for getting started)
  • {Colors.GREEN}graph{Colors.RESET} - Graph database for relationships (requires Neo4j)
  • {Colors.GREEN}vector{Colors.RESET} - Semantic search (requires vector database)
  • {Colors.GREEN}relational{Colors.RESET} - SQL database (requires PostgreSQL)
""")

    memory_provider = get_input("Memory provider", "file")
    memory_base_path = get_input("Memory storage path", ".forge/memory")

    print_success(f"Configured {memory_provider} memory at {memory_base_path}")

    # Create composition
    print_section("Creating Composition")

    composition_name = get_input("Composition name", project_name)
    composition_desc = get_input("Description", f"Development composition for {project_name}")

    composition = Composition(
        name=composition_name,
        type="preset",
        version="1.0.0",
        description=composition_desc,
        elements=CompositionElements(
            principles=selected_principles,
            constitutions=[],
            tools=[],
            agents=[],
            templates=[],
            hooks={},
            queries=[]
        ),
        settings=CompositionSettings(
            memory={
                "provider": memory_provider,
                "config": {
                    "base_path": memory_base_path
                }
            },
            agent_orchestration={
                "mode": "sequential",
                "max_parallel": 3
            },
            tool_defaults={}
        ),
        metadata={
            "author": "wizard",
            "tags": ["custom"],
            "created_by": "forge-wizard"
        }
    )

    # Save composition
    composition_file = forge_dir / "composition.yaml"
    composition.save_to_file(composition_file)
    print_success(f"Saved composition to {composition_file}")

    # Initialize memory
    print_section("Initializing Memory")

    try:
        memory = FileProvider()
        await memory.initialize({
            "base_path": str(project_path / memory_base_path),
            "session_id": "wizard"
        })

        # Store initialization info
        await memory.set(
            key="project:initialized",
            value=f"Project '{project_name}' initialized with Forge wizard",
            scope=Scope.PROJECT,
            tags=["initialization", "wizard"]
        )

        await memory.set(
            key="composition:active",
            value=composition_name,
            scope=Scope.PROJECT,
            tags=["composition"]
        )

        await memory.close()
        print_success("Memory initialized successfully")

    except Exception as e:
        print_error(f"Error initializing memory: {e}")

    # Create README
    print_section("Creating Documentation")

    readme_content = f"""# {project_name}

Created with Forge - A Composable AI Development System

## Composition

**Name**: {composition_name}
**Description**: {composition_desc}

### Active Principles

{chr(10).join(f"- **{p}**" for p in selected_principles) if selected_principles else "None selected"}

### Memory

- **Provider**: {memory_provider}
- **Location**: {memory_base_path}

## Getting Started

```bash
# View your composition
cat .forge/composition.yaml

# Explore memory
ls {memory_base_path}/

# Add more elements
# Edit .forge/composition.yaml and add elements to the appropriate sections
```

## Next Steps

1. Review available elements in the Forge repository
2. Customize your composition by editing `.forge/composition.yaml`
3. Add tools, agents, and templates as needed
4. Start building!

## Learn More

- [Forge README](https://github.com/yourorg/forge)
- [Element Types](https://github.com/yourorg/forge/docs/element-types.md)
- [Memory System](https://github.com/yourorg/forge/docs/memory-system.md)
"""

    readme_file = project_path / "README.md"
    with open(readme_file, 'w') as f:
        f.write(readme_content)

    print_success(f"Created README.md")

    # Summary
    print_header("🎉 Project Initialized!")

    print(f"""
{Colors.GREEN}Your Forge project is ready!{Colors.RESET}

📁 Project: {Colors.BOLD}{project_path}{Colors.RESET}
📝 Composition: {Colors.BOLD}{composition_name}{Colors.RESET}
💾 Memory: {Colors.BOLD}{memory_provider} ({memory_base_path}){Colors.RESET}
🎯 Principles: {Colors.BOLD}{', '.join(selected_principles) if selected_principles else 'None'}{Colors.RESET}

{Colors.CYAN}Next steps:{Colors.RESET}

  1. cd {project_name}
  2. Review README.md for more information
  3. Customize .forge/composition.yaml as needed
  4. Start building!

{Colors.YELLOW}Happy forging! 🔨{Colors.RESET}
""")


async def wizard_add():
    """Interactive wizard for adding elements to existing project."""
    print_header("➕ Add Elements to Project")

    # Check if we're in a Forge project
    forge_dir = Path.cwd() / ".forge"
    if not forge_dir.exists():
        print_error("Not in a Forge project directory.")
        print_info("Run 'forge init' to create a new project.")
        return

    composition_file = forge_dir / "composition.yaml"
    if not composition_file.exists():
        print_error("No composition.yaml found.")
        return

    # Load current composition
    composition = Composition.load_from_file(composition_file)
    print_success(f"Loaded composition: {composition.name}")

    # Load available elements
    forge_root = Path(__file__).parent.parent.parent
    element_loader = ElementLoader(search_paths=[forge_root / "elements"])

    print_section("What would you like to add?")

    options = [
        ("principles", "Guiding principles and values"),
        ("tools", "Executable capabilities"),
        ("agents", "Specialized AI intelligence"),
        ("templates", "Document templates"),
    ]

    element_type = get_multiselect("Select element type:", options, max_selections=1)

    if not element_type:
        print_info("No element type selected. Aborted.")
        return

    element_type = element_type[0]

    # Get available elements of selected type
    type_map = {
        "principles": ElementType.PRINCIPLE,
        "tools": ElementType.TOOL,
        "agents": ElementType.AGENT,
        "templates": ElementType.TEMPLATE,
    }

    available = element_loader.list_elements(type_map[element_type])

    # Filter out already added elements
    current_elements = getattr(composition.elements, element_type)
    available = [e for e in available if e.name not in current_elements]

    if not available:
        print_info(f"No new {element_type} available to add.")
        return

    element_options = [(e.name, e.metadata.description or "No description") for e in available]

    selected = get_multiselect(
        f"Select {element_type} to add:",
        element_options
    )

    if not selected:
        print_info("No elements selected. Aborted.")
        return

    # Add to composition
    current_list = getattr(composition.elements, element_type)
    current_list.extend(selected)

    # Save composition
    composition.save_to_file(composition_file)
    print_success(f"Added {len(selected)} {element_type} to composition")
    print_success(f"Updated {composition_file}")

    print(f"\n{Colors.CYAN}Added elements:{Colors.RESET}")
    for elem in selected:
        print(f"  • {Colors.GREEN}{elem}{Colors.RESET}")


def main():
    """Main CLI entry point."""
    if len(sys.argv) < 2:
        print(f"""
{Colors.BOLD}Forge CLI{Colors.RESET} - A Composable AI Development System

{Colors.CYAN}Usage:{Colors.RESET}
  forge init              Initialize a new Forge project (interactive wizard)
  forge add               Add elements to current project
  forge generate [PROVIDER] Generate AI platform files from composition
  forge validate [PROVIDER] Validate platform files against composition
  forge update [PROVIDER]   Update platform files when composition changes
  forge clean [PROVIDER]    Remove generated platform files
  forge version           Show version information

{Colors.CYAN}Examples:{Colors.RESET}
  forge init                      # Start the interactive wizard
  forge add                       # Add elements to project
  forge generate claude-code      # Generate .claude/ directory
  forge generate claude-code -f   # Force overwrite existing files
  forge validate claude-code      # Check if .claude/ matches composition

{Colors.CYAN}Available Providers:{Colors.RESET}
  claude-code    Claude Code integration (.claude/ directory)

{Colors.CYAN}Learn more:{Colors.RESET}
  https://github.com/yourorg/forge
""")
        return

    command = sys.argv[1]

    if command == "init":
        asyncio.run(wizard_init())
    elif command == "add":
        asyncio.run(wizard_add())
    elif command == "generate":
        from forge.cli.generate import main as generate_main
        generate_main()
    elif command == "validate":
        from forge.cli.validate import main as validate_main
        validate_main()
    elif command == "update":
        from forge.cli.update import main as update_main
        update_main()
    elif command == "clean":
        from forge.cli.clean import main as clean_main
        clean_main()
    elif command == "version":
        print(f"{Colors.BOLD}Forge{Colors.RESET} version {Colors.GREEN}0.1.0{Colors.RESET}")
    else:
        print_error(f"Unknown command: {command}")
        print_info("Run 'forge' with no arguments to see usage.")


if __name__ == "__main__":
    main()

"""
Generate AI platform files from Forge composition.
"""

import asyncio
from pathlib import Path
from typing import Optional
import sys

from forge.core.element import ElementLoader
from forge.core.composition import CompositionLoader
from forge.providers.protocol import ProviderRegistry
from forge.providers.claude_code import ClaudeCodeProvider


def print_success(msg: str) -> None:
    """Print success message."""
    print(f"✓ {msg}")


def print_error(msg: str) -> None:
    """Print error message."""
    print(f"✗ {msg}", file=sys.stderr)


def print_warning(msg: str) -> None:
    """Print warning message."""
    print(f"⚠ {msg}")


async def generate_command(
    provider_name: str = "claude-code",
    project_dir: Optional[Path] = None,
    force: bool = False,
) -> int:
    """Generate AI platform files from composition.

    Args:
        provider_name: Provider to use (default: claude-code)
        project_dir: Project directory (default: current directory)
        force: Overwrite existing files

    Returns:
        Exit code (0 = success, 1 = error)
    """
    if project_dir is None:
        project_dir = Path.cwd()

    composition_file = project_dir / ".forge" / "composition.yaml"

    if not composition_file.exists():
        print_error(f"Composition not found: {composition_file}")
        print_error("Run 'forge init' to create a new project first.")
        return 1

    print(f"📁 Project: {project_dir}")
    print(f"🔨 Provider: {provider_name}")
    print()

    registry = ProviderRegistry()
    registry.register(ClaudeCodeProvider())

    provider = registry.get(provider_name)
    if not provider:
        print_error(f"Unknown provider: {provider_name}")
        print(f"Available providers: {', '.join(registry.list_providers())}")
        return 1

    try:
        element_loader = ElementLoader(
            search_paths=[
                project_dir / ".forge" / "elements",
                Path(__file__).parent.parent.parent.parent / "elements",
            ]
        )

        composition_loader = CompositionLoader(element_loader)
        loaded = composition_loader.load(composition_file)

        print(f"▶ Loaded composition: {loaded.composition.name}")
        print(f"  • {len(loaded.get_principles())} principles")
        print(f"  • {len(loaded.get_agents())} agents")
        print(f"  • {len(loaded.get_tools())} tools")
        print(f"  • {len(loaded.get_hooks())} hooks")
        print()

        print(f"▶ Generating {provider_name} files...")
        result = await provider.generate(loaded, project_dir, force=force)

        if not result.success:
            print_error("Generation failed!")
            for error in result.errors:
                print_error(f"  {error}")
            return 1

        print()
        print_success("Generation complete!")
        print()

        if result.files_created:
            print(f"📝 Created {len(result.files_created)} files:")
            for file in result.files_created:
                rel_path = file.relative_to(project_dir)
                print(f"  • {rel_path}")

        if result.files_updated:
            print()
            print(f"🔄 Updated {len(result.files_updated)} files:")
            for file in result.files_updated:
                rel_path = file.relative_to(project_dir)
                print(f"  • {rel_path}")

        if result.warnings:
            print()
            for warning in result.warnings:
                print_warning(warning)

        print()
        print("🎉 Done! Your AI platform files are ready.")

        return 0

    except Exception as e:
        print_error(f"Generation failed: {str(e)}")
        import traceback

        traceback.print_exc()
        return 1


def main() -> None:
    """CLI entry point for generate command."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Generate AI platform files from Forge composition"
    )
    parser.add_argument(
        "provider",
        nargs="?",
        default="claude-code",
        help="Provider to use (default: claude-code)",
    )
    parser.add_argument(
        "--project-dir",
        "-d",
        type=Path,
        help="Project directory (default: current directory)",
    )
    parser.add_argument(
        "--force", "-f", action="store_true", help="Overwrite existing files"
    )

    args = parser.parse_args()

    exit_code = asyncio.run(
        generate_command(
            provider_name=args.provider, project_dir=args.project_dir, force=args.force
        )
    )

    sys.exit(exit_code)


if __name__ == "__main__":
    main()

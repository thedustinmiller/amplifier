"""
Validate AI platform files against Forge composition.
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


async def validate_command(
    provider_name: str = "claude-code",
    project_dir: Optional[Path] = None,
) -> int:
    """Validate AI platform files against composition.

    Args:
        provider_name: Provider to use (default: claude-code)
        project_dir: Project directory (default: current directory)

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

        print(f"▶ Validating {provider_name} files...")
        result = await provider.validate(loaded, project_dir)

        if result.valid:
            print()
            print_success("Validation passed!")

            if result.warnings:
                print()
                for warning in result.warnings:
                    print_warning(warning)

            return 0
        else:
            print()
            print_error("Validation failed!")

            if result.errors:
                print()
                print("Errors:")
                for error in result.errors:
                    print_error(f"  {error}")

            if result.warnings:
                print()
                print("Warnings:")
                for warning in result.warnings:
                    print_warning(f"  {warning}")

            if result.suggestions:
                print()
                print("Suggestions:")
                for suggestion in result.suggestions:
                    print(f"  💡 {suggestion}")

            return 1

    except Exception as e:
        print_error(f"Validation failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1


def main() -> None:
    """CLI entry point for validate command."""
    import argparse

    parser = argparse.ArgumentParser(
        prog="forge validate",
        description="Validate AI platform files against Forge composition"
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

    args = parser.parse_args(sys.argv[2:])

    exit_code = asyncio.run(
        validate_command(provider_name=args.provider, project_dir=args.project_dir)
    )

    sys.exit(exit_code)


if __name__ == "__main__":
    main()

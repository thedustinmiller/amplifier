"""
Clean (remove) generated AI platform files.
"""

import asyncio
from pathlib import Path
from typing import Optional
import sys

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


def get_confirmation(provider_name: str, project_dir: Path) -> bool:
    """Get user confirmation for clean operation."""
    print(f"⚠️  WARNING: This will remove all {provider_name} files from:")
    print(f"   {project_dir}")
    print()

    response = input("Are you sure? Type 'yes' to confirm: ").strip().lower()
    return response == "yes"


async def clean_command(
    provider_name: str = "claude-code",
    project_dir: Optional[Path] = None,
    force: bool = False,
) -> int:
    """Remove generated AI platform files.

    Args:
        provider_name: Provider to use (default: claude-code)
        project_dir: Project directory (default: current directory)
        force: Skip confirmation prompt

    Returns:
        Exit code (0 = success, 1 = error)
    """
    if project_dir is None:
        project_dir = Path.cwd()

    print(f"📁 Project: {project_dir}")
    print(f"🔨 Provider: {provider_name}")
    print()

    if not force and not get_confirmation(provider_name, project_dir):
        print("Aborted.")
        return 0

    registry = ProviderRegistry()
    registry.register(ClaudeCodeProvider())

    provider = registry.get(provider_name)
    if not provider:
        print_error(f"Unknown provider: {provider_name}")
        print(f"Available providers: {', '.join(registry.list_providers())}")
        return 1

    try:
        print(f"▶ Cleaning {provider_name} files...")
        result = await provider.clean(project_dir)

        if not result.success:
            print_error("Clean failed!")
            for error in result.errors:
                print_error(f"  {error}")
            return 1

        print()
        print_success("Clean complete!")
        print()

        if result.files_updated:
            print(f"🗑️  Removed {len(result.files_updated)} files:")
            for file in result.files_updated[:10]:
                rel_path = file.relative_to(project_dir) if file.is_relative_to(project_dir) else file
                print(f"  • {rel_path}")

            if len(result.files_updated) > 10:
                print(f"  ... and {len(result.files_updated) - 10} more")

        if result.warnings:
            print()
            for warning in result.warnings:
                print_warning(warning)

        print()
        print("🎉 Done! AI platform files have been removed.")

        return 0

    except Exception as e:
        print_error(f"Clean failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1


def main() -> None:
    """CLI entry point for clean command."""
    import argparse

    parser = argparse.ArgumentParser(
        prog="forge clean",
        description="Remove generated AI platform files"
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
        "--force",
        "-f",
        action="store_true",
        help="Skip confirmation prompt",
    )

    args = parser.parse_args(sys.argv[2:])

    exit_code = asyncio.run(
        clean_command(
            provider_name=args.provider,
            project_dir=args.project_dir,
            force=args.force,
        )
    )

    sys.exit(exit_code)


if __name__ == "__main__":
    main()

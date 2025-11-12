"""
Helper functions for locating Forge resources.
"""

from pathlib import Path
from typing import List
import sys


def get_element_search_paths(project_dir: Path = None) -> List[Path]:
    """Get element search paths in priority order.

    Args:
        project_dir: Optional project directory (defaults to cwd)

    Returns:
        List of paths to search for elements
    """
    if project_dir is None:
        project_dir = Path.cwd()

    search_paths = []

    project_elements = project_dir / ".forge" / "elements"
    if project_elements.exists():
        search_paths.append(project_elements)

    package_elements = _find_package_elements()
    if package_elements:
        search_paths.append(package_elements)

    repo_elements = _find_repo_elements()
    if repo_elements:
        search_paths.append(repo_elements)

    return search_paths


def _find_package_elements() -> Path:
    """Find elements directory in installed package."""
    try:
        import forge

        package_dir = Path(forge.__file__).parent
        elements_dir = package_dir.parent / "elements"

        if elements_dir.exists():
            return elements_dir

    except (ImportError, AttributeError):
        pass

    return None


def _find_repo_elements() -> Path:
    """Find elements directory in repository (for development)."""
    current = Path(__file__).parent

    for _ in range(5):
        elements_dir = current / "elements"
        if elements_dir.exists():
            return elements_dir

        parent = current.parent
        if parent == current:
            break
        current = parent

    return None


def get_forge_root() -> Path:
    """Get Forge repository root (for development/testing).

    Returns:
        Path to Forge root directory
    """
    current = Path(__file__).parent

    for _ in range(5):
        if (current / "pyproject.toml").exists():
            return current

        parent = current.parent
        if parent == current:
            break
        current = parent

    return Path.cwd()

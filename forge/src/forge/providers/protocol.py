"""
Provider protocol for AI platform integration.
"""

from typing import Protocol, Dict, List, Any, Optional
from pathlib import Path
from enum import Enum
from dataclasses import dataclass

from forge.core.composition import LoadedComposition
from forge.core.element import Element, ElementType


class ProviderCapability(Enum):
    """Capabilities supported by providers."""

    AGENTS = "agents"
    COMMANDS = "commands"
    HOOKS = "hooks"
    TOOLS = "tools"
    TEMPLATES = "templates"
    SETTINGS = "settings"


@dataclass
class GenerationResult:
    """Result of provider generation."""

    success: bool
    files_created: List[Path]
    files_updated: List[Path]
    errors: List[str]
    warnings: List[str]


@dataclass
class ValidationResult:
    """Result of provider validation."""

    valid: bool
    errors: List[str]
    warnings: List[str]
    suggestions: List[str]


class Provider(Protocol):
    """Base protocol for AI platform providers.

    Providers convert Forge compositions into platform-specific formats
    (e.g., .claude/, .cursor/, .github/prompts/, etc.)
    """

    @property
    def name(self) -> str:
        """Provider name (e.g., 'claude-code', 'cursor', 'copilot')."""
        ...

    @property
    def capabilities(self) -> List[ProviderCapability]:
        """List of supported capabilities."""
        ...

    async def generate(
        self, composition: LoadedComposition, output_dir: Path, force: bool = False
    ) -> GenerationResult:
        """Generate platform files from composition.

        Args:
            composition: Loaded composition with resolved elements
            output_dir: Project root directory
            force: Overwrite existing files

        Returns:
            GenerationResult with created/updated files and errors
        """
        ...

    async def sync(
        self, composition: LoadedComposition, output_dir: Path
    ) -> GenerationResult:
        """Sync changes bidirectionally.

        Args:
            composition: Current composition
            output_dir: Project root directory

        Returns:
            GenerationResult with changes applied
        """
        ...

    async def validate(
        self, composition: LoadedComposition, output_dir: Path
    ) -> ValidationResult:
        """Validate platform files against composition.

        Args:
            composition: Expected composition
            output_dir: Project root directory

        Returns:
            ValidationResult with validation status and issues
        """
        ...

    async def update(
        self, composition: LoadedComposition, output_dir: Path
    ) -> GenerationResult:
        """Update platform files when composition changes.

        Args:
            composition: Updated composition
            output_dir: Project root directory

        Returns:
            GenerationResult with updated files
        """
        ...

    async def clean(self, output_dir: Path) -> GenerationResult:
        """Remove all generated platform files.

        Args:
            output_dir: Project root directory

        Returns:
            GenerationResult with removed files
        """
        ...


class ProviderRegistry:
    """Registry of available providers."""

    def __init__(self):
        """Initialize registry."""
        self._providers: Dict[str, Provider] = {}

    def register(self, provider: Provider) -> None:
        """Register a provider.

        Args:
            provider: Provider instance to register
        """
        self._providers[provider.name] = provider

    def get(self, name: str) -> Optional[Provider]:
        """Get provider by name.

        Args:
            name: Provider name

        Returns:
            Provider instance or None
        """
        return self._providers.get(name)

    def list_providers(self) -> List[str]:
        """List all registered providers.

        Returns:
            List of provider names
        """
        return list(self._providers.keys())

    def list_providers_with_capability(
        self, capability: ProviderCapability
    ) -> List[str]:
        """List providers supporting a capability.

        Args:
            capability: Required capability

        Returns:
            List of provider names
        """
        return [
            name
            for name, provider in self._providers.items()
            if capability in provider.capabilities
        ]

"""
Context for Forge operations.

Provides access to memory, elements, and system state.
"""

from typing import Optional, Dict, Any
from pathlib import Path

from forge.memory import MemoryProvider, Scope
from forge.core.element import ElementLoader
from forge.core.composition import CompositionLoader, LoadedComposition


class Context:
    """Execution context for Forge.

    Provides access to memory, loaded elements, and system state.
    """

    def __init__(
        self,
        memory: MemoryProvider,
        composition: LoadedComposition,
        project_path: Path,
        session_id: str,
    ):
        """Initialize context.

        Args:
            memory: Memory provider
            composition: Loaded composition
            project_path: Path to project root
            session_id: Current session identifier
        """
        self.memory = memory
        self.composition = composition
        self.project_path = project_path
        self.session_id = session_id

    @property
    def principles(self):
        """Get principles manager."""
        return PrinciplesManager(self.composition)

    @property
    def tools(self):
        """Get tools manager."""
        return ToolsManager(self.composition)

    @property
    def agents(self):
        """Get agents manager."""
        return AgentsManager(self.composition)

    @property
    def templates(self):
        """Get templates manager."""
        return TemplatesManager(self.composition)


class PrinciplesManager:
    """Manage principles."""

    def __init__(self, composition: LoadedComposition):
        self.composition = composition

    async def get(self, name: str) -> Optional[str]:
        """Get principle content by name."""
        from forge.core.element import ElementType

        principle = self.composition.get_element(name, ElementType.PRINCIPLE)
        return principle.content if principle else None

    def list(self) -> list[str]:
        """List all principle names."""
        return [p.name for p in self.composition.get_principles()]


class ToolsManager:
    """Manage tools."""

    def __init__(self, composition: LoadedComposition):
        self.composition = composition

    def list(self) -> list[str]:
        """List all tool names."""
        return [t.name for t in self.composition.get_tools()]


class AgentsManager:
    """Manage agents."""

    def __init__(self, composition: LoadedComposition):
        self.composition = composition

    def list(self) -> list[str]:
        """List all agent names."""
        return [a.name for a in self.composition.get_agents()]


class TemplatesManager:
    """Manage templates."""

    def __init__(self, composition: LoadedComposition):
        self.composition = composition

    async def get(self, name: str) -> Optional[str]:
        """Get template content by name."""
        from forge.core.element import ElementType

        template = self.composition.get_element(name, ElementType.TEMPLATE)
        return template.content if template else None

    def list(self) -> list[str]:
        """List all template names."""
        return [t.name for t in self.composition.get_templates()]

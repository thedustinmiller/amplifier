"""
Composition system for Forge.

Compositions are assemblies of elements.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from pathlib import Path
import yaml

from forge.core.element import Element, ElementType, ElementLoader


@dataclass
class CompositionElements:
    """Elements included in a composition."""

    principles: List[str] = field(default_factory=list)
    constitutions: List[str] = field(default_factory=list)
    tools: List[str] = field(default_factory=list)
    agents: List[str] = field(default_factory=list)
    templates: List[str] = field(default_factory=list)
    hooks: Dict[str, str] = field(default_factory=dict)  # event -> hook name
    queries: List[str] = field(default_factory=list)


@dataclass
class CompositionSettings:
    """Composition-level settings."""

    memory: Dict[str, Any] = field(default_factory=dict)
    agent_orchestration: Dict[str, Any] = field(default_factory=dict)
    tool_defaults: Dict[str, Dict[str, Any]] = field(default_factory=dict)


@dataclass
class Composition:
    """A composition of elements.

    Compositions are themselves elements that can be nested.
    """

    name: str
    type: str  # preset, workflow, orchestration, methodology
    version: str
    description: Optional[str] = None
    elements: CompositionElements = field(default_factory=CompositionElements)
    settings: CompositionSettings = field(default_factory=CompositionSettings)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "composition": {
                "name": self.name,
                "type": self.type,
                "version": self.version,
                "description": self.description,
            },
            "elements": {
                "principles": self.elements.principles,
                "constitutions": self.elements.constitutions,
                "tools": self.elements.tools,
                "agents": self.elements.agents,
                "templates": self.elements.templates,
                "hooks": self.elements.hooks,
                "queries": self.elements.queries,
            },
            "settings": {
                "memory": self.settings.memory,
                "agent_orchestration": self.settings.agent_orchestration,
                "tool_defaults": self.settings.tool_defaults,
            },
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Composition":
        """Create from dictionary."""
        comp_data = data.get("composition", {})
        elements_data = data.get("elements", {})
        settings_data = data.get("settings", {})

        elements = CompositionElements(
            principles=elements_data.get("principles", []),
            constitutions=elements_data.get("constitutions", []),
            tools=elements_data.get("tools", []),
            agents=elements_data.get("agents", []),
            templates=elements_data.get("templates", []),
            hooks=elements_data.get("hooks", {}),
            queries=elements_data.get("queries", []),
        )

        settings = CompositionSettings(
            memory=settings_data.get("memory", {}),
            agent_orchestration=settings_data.get("agent_orchestration", {}),
            tool_defaults=settings_data.get("tool_defaults", {}),
        )

        return cls(
            name=comp_data.get("name", ""),
            type=comp_data.get("type", "preset"),
            version=comp_data.get("version", "1.0.0"),
            description=comp_data.get("description"),
            elements=elements,
            settings=settings,
            metadata=data.get("metadata", {}),
        )

    @classmethod
    def load_from_file(cls, path: Path) -> "Composition":
        """Load composition from YAML file."""
        with open(path, 'r') as f:
            data = yaml.safe_load(f)
        return cls.from_dict(data)

    def save_to_file(self, path: Path) -> None:
        """Save composition to YAML file."""
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'w') as f:
            yaml.dump(self.to_dict(), f, default_flow_style=False, sort_keys=False)

    def get_all_element_names(self) -> List[tuple[ElementType, str]]:
        """Get all element names with their types.

        Returns:
            List of (element_type, element_name) tuples
        """
        result = []

        for principle in self.elements.principles:
            result.append((ElementType.PRINCIPLE, principle))

        for constitution in self.elements.constitutions:
            result.append((ElementType.CONSTITUTION, constitution))

        for tool in self.elements.tools:
            result.append((ElementType.TOOL, tool))

        for agent in self.elements.agents:
            result.append((ElementType.AGENT, agent))

        for template in self.elements.templates:
            result.append((ElementType.TEMPLATE, template))

        for hook in self.elements.hooks.values():
            result.append((ElementType.HOOK, hook))

        for query in self.elements.queries:
            result.append((ElementType.QUERY, query))

        return result


class CompositionLoader:
    """Load and resolve compositions."""

    def __init__(self, element_loader: ElementLoader):
        """Initialize composition loader.

        Args:
            element_loader: Element loader instance
        """
        self.element_loader = element_loader
        self._composition_cache: Dict[str, Composition] = {}

    def load(self, path: Path) -> "LoadedComposition":
        """Load and resolve composition.

        Args:
            path: Path to composition.yaml

        Returns:
            LoadedComposition with all elements resolved

        Raises:
            ValueError: If dependencies can't be resolved or conflicts exist
        """
        # Load composition
        composition = Composition.load_from_file(path)

        # Resolve all elements
        elements = {}
        for element_type, element_name in composition.get_all_element_names():
            try:
                element = self.element_loader.load(element_name, element_type)
                elements[f"{element_type.value}:{element_name}"] = element
            except FileNotFoundError:
                raise ValueError(
                    f"Element not found: {element_type.value}/{element_name}"
                )

        # Check dependencies
        missing_deps = self._check_dependencies(elements)
        if missing_deps:
            raise ValueError(f"Missing dependencies: {missing_deps}")

        # Check conflicts
        conflicts = self._check_conflicts(elements)
        if conflicts:
            raise ValueError(f"Conflicts detected: {conflicts}")

        return LoadedComposition(composition=composition, elements=elements)

    def _check_dependencies(
        self, elements: Dict[str, Element]
    ) -> List[tuple[str, str]]:
        """Check if all dependencies are satisfied.

        Args:
            elements: Loaded elements

        Returns:
            List of (element_name, missing_dependency) tuples
        """
        missing = []

        for key, element in elements.items():
            # Check principle dependencies
            for dep in element.dependencies.principles:
                dep_key = f"principle:{dep}"
                if dep_key not in elements:
                    missing.append((element.name, dep))

            # Check tool dependencies
            for dep in element.dependencies.tools:
                dep_key = f"tool:{dep}"
                if dep_key not in elements:
                    missing.append((element.name, dep))

            # Check agent dependencies
            for dep in element.dependencies.agents:
                dep_key = f"agent:{dep}"
                if dep_key not in elements:
                    missing.append((element.name, dep))

        return missing

    def _check_conflicts(self, elements: Dict[str, Element]) -> List[tuple[str, str]]:
        """Check for conflicting elements.

        Args:
            elements: Loaded elements

        Returns:
            List of (element1_name, element2_name) tuples
        """
        conflicts = []

        # Build name -> element mapping
        by_name = {elem.name: elem for elem in elements.values()}

        for element in elements.values():
            # Check principle conflicts
            for conflict_name in element.conflicts.principles:
                if conflict_name in by_name:
                    conflicts.append((element.name, conflict_name))

            # Check tool conflicts
            for conflict_name in element.conflicts.tools:
                if conflict_name in by_name:
                    conflicts.append((element.name, conflict_name))

            # Check agent conflicts
            for conflict_name in element.conflicts.agents:
                if conflict_name in by_name:
                    conflicts.append((element.name, conflict_name))

        return conflicts


@dataclass
class LoadedComposition:
    """A composition with all elements resolved."""

    composition: Composition
    elements: Dict[str, Element]

    def get_elements_by_type(self, element_type: ElementType) -> List[Element]:
        """Get all elements of a specific type.

        Args:
            element_type: Type of elements to retrieve

        Returns:
            List of elements of that type
        """
        return [
            elem
            for key, elem in self.elements.items()
            if elem.type == element_type
        ]

    def get_element(self, name: str, element_type: ElementType) -> Optional[Element]:
        """Get specific element by name and type.

        Args:
            name: Element name
            element_type: Element type

        Returns:
            Element if found, None otherwise
        """
        key = f"{element_type.value}:{name}"
        return self.elements.get(key)

    def get_principles(self) -> List[Element]:
        """Get all principles."""
        return self.get_elements_by_type(ElementType.PRINCIPLE)

    def get_constitutions(self) -> List[Element]:
        """Get all constitutions."""
        return self.get_elements_by_type(ElementType.CONSTITUTION)

    def get_tools(self) -> List[Element]:
        """Get all tools."""
        return self.get_elements_by_type(ElementType.TOOL)

    def get_agents(self) -> List[Element]:
        """Get all agents."""
        return self.get_elements_by_type(ElementType.AGENT)

    def get_templates(self) -> List[Element]:
        """Get all templates."""
        return self.get_elements_by_type(ElementType.TEMPLATE)

    def get_hooks(self) -> Dict[str, Element]:
        """Get all hooks mapped by event.

        Returns:
            Dictionary mapping event names to hook elements
        """
        hooks = {}
        for event, hook_name in self.composition.elements.hooks.items():
            hook = self.get_element(hook_name, ElementType.HOOK)
            if hook:
                hooks[event] = hook
        return hooks

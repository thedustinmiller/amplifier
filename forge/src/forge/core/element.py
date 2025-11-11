"""
Element abstraction for Forge.

Elements are atomic, reusable building blocks.
"""

from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from pathlib import Path
import yaml


class ElementType(Enum):
    """Types of elements."""

    PRINCIPLE = "principle"
    CONSTITUTION = "constitution"
    TOOL = "tool"
    AGENT = "agent"
    TEMPLATE = "template"
    HOOK = "hook"
    QUERY = "query"
    WORKFLOW = "workflow"
    PRESET = "preset"


@dataclass
class ElementMetadata:
    """Element metadata."""

    name: str
    type: ElementType
    version: str
    description: Optional[str] = None
    author: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    license: Optional[str] = None


@dataclass
class ElementDependencies:
    """Element dependencies."""

    principles: List[str] = field(default_factory=list)
    constitutions: List[str] = field(default_factory=list)
    tools: List[str] = field(default_factory=list)
    agents: List[str] = field(default_factory=list)
    templates: List[str] = field(default_factory=list)
    suggests: List[str] = field(default_factory=list)


@dataclass
class ElementConflicts:
    """Element conflicts."""

    principles: List[str] = field(default_factory=list)
    tools: List[str] = field(default_factory=list)
    agents: List[str] = field(default_factory=list)
    reason: Optional[str] = None


@dataclass
class ElementInterface:
    """Element interface specification."""

    inputs: Dict[str, str] = field(default_factory=dict)
    outputs: Dict[str, str] = field(default_factory=dict)
    role: Optional[str] = None  # For agents
    events: List[str] = field(default_factory=list)  # For hooks


@dataclass
class Element:
    """Base element class.

    All elements (tools, agents, templates, etc.) inherit from this.
    """

    metadata: ElementMetadata
    dependencies: ElementDependencies = field(default_factory=ElementDependencies)
    conflicts: ElementConflicts = field(default_factory=ElementConflicts)
    interface: ElementInterface = field(default_factory=ElementInterface)
    content: Optional[str] = None  # For principles, constitutions
    implementation: Optional[Dict[str, Any]] = None  # For tools, agents
    settings: Dict[str, Any] = field(default_factory=dict)

    @property
    def name(self) -> str:
        """Get element name."""
        return self.metadata.name

    @property
    def type(self) -> ElementType:
        """Get element type."""
        return self.metadata.type

    @property
    def version(self) -> str:
        """Get element version."""
        return self.metadata.version

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "metadata": {
                "name": self.metadata.name,
                "type": self.metadata.type.value,
                "version": self.metadata.version,
                "description": self.metadata.description,
                "author": self.metadata.author,
                "tags": self.metadata.tags,
                "license": self.metadata.license,
            },
            "dependencies": {
                "principles": self.dependencies.principles,
                "constitutions": self.dependencies.constitutions,
                "tools": self.dependencies.tools,
                "agents": self.dependencies.agents,
                "templates": self.dependencies.templates,
                "suggests": self.dependencies.suggests,
            },
            "conflicts": {
                "principles": self.conflicts.principles,
                "tools": self.conflicts.tools,
                "agents": self.conflicts.agents,
                "reason": self.conflicts.reason,
            },
            "interface": {
                "inputs": self.interface.inputs,
                "outputs": self.interface.outputs,
                "role": self.interface.role,
                "events": self.interface.events,
            },
            "content": self.content,
            "implementation": self.implementation,
            "settings": self.settings,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Element":
        """Create from dictionary."""
        metadata = ElementMetadata(
            name=data["metadata"]["name"],
            type=ElementType(data["metadata"]["type"]),
            version=data["metadata"]["version"],
            description=data["metadata"].get("description"),
            author=data["metadata"].get("author"),
            tags=data["metadata"].get("tags", []),
            license=data["metadata"].get("license"),
        )

        dependencies = ElementDependencies(
            principles=data.get("dependencies", {}).get("principles", []),
            constitutions=data.get("dependencies", {}).get("constitutions", []),
            tools=data.get("dependencies", {}).get("tools", []),
            agents=data.get("dependencies", {}).get("agents", []),
            templates=data.get("dependencies", {}).get("templates", []),
            suggests=data.get("dependencies", {}).get("suggests", []),
        )

        conflicts = ElementConflicts(
            principles=data.get("conflicts", {}).get("principles", []),
            tools=data.get("conflicts", {}).get("tools", []),
            agents=data.get("conflicts", {}).get("agents", []),
            reason=data.get("conflicts", {}).get("reason"),
        )

        interface = ElementInterface(
            inputs=data.get("interface", {}).get("inputs", {}),
            outputs=data.get("interface", {}).get("outputs", {}),
            role=data.get("interface", {}).get("role"),
            events=data.get("interface", {}).get("events", []),
        )

        return cls(
            metadata=metadata,
            dependencies=dependencies,
            conflicts=conflicts,
            interface=interface,
            content=data.get("content"),
            implementation=data.get("implementation"),
            settings=data.get("settings", {}),
        )

    @classmethod
    def load_from_file(cls, path: Path) -> "Element":
        """Load element from YAML file.

        Args:
            path: Path to element.yaml file

        Returns:
            Element instance
        """
        with open(path, 'r') as f:
            data = yaml.safe_load(f)

        # Read content if it's a principle or constitution
        element_type = ElementType(data["metadata"]["type"])
        content = None

        if element_type in (ElementType.PRINCIPLE, ElementType.CONSTITUTION):
            # Look for content file
            content_path = path.parent / f"{data['metadata']['name']}.md"
            if content_path.exists():
                with open(content_path, 'r') as cf:
                    content = cf.read()

        data["content"] = content
        return cls.from_dict(data)

    def save_to_file(self, path: Path) -> None:
        """Save element to YAML file.

        Args:
            path: Path to save element.yaml
        """
        path.parent.mkdir(parents=True, exist_ok=True)

        # Save YAML
        with open(path, 'w') as f:
            yaml.dump(self.to_dict(), f, default_flow_style=False, sort_keys=False)

        # Save content separately if it exists
        if self.content and self.type in (
            ElementType.PRINCIPLE,
            ElementType.CONSTITUTION,
        ):
            content_path = path.parent / f"{self.name}.md"
            with open(content_path, 'w') as cf:
                cf.write(self.content)


class ElementLoader:
    """Load elements from filesystem or registry."""

    def __init__(self, search_paths: List[Path]):
        """Initialize loader.

        Args:
            search_paths: Directories to search for elements
        """
        self.search_paths = search_paths
        self._cache: Dict[str, Element] = {}

    def load(self, name: str, element_type: Optional[ElementType] = None) -> Element:
        """Load element by name.

        Args:
            name: Element name
            element_type: Optional type filter

        Returns:
            Element instance

        Raises:
            FileNotFoundError: If element not found
        """
        # Check cache
        cache_key = f"{element_type.value if element_type else 'any'}:{name}"
        if cache_key in self._cache:
            return self._cache[cache_key]

        # Search paths
        for search_path in self.search_paths:
            if element_type:
                # Look in type-specific directory
                element_dir = search_path / element_type.value / name
            else:
                # Search all type directories
                for et in ElementType:
                    element_dir = search_path / et.value / name
                    if element_dir.exists():
                        element_type = et
                        break
                else:
                    continue

            element_file = element_dir / "element.yaml"
            if element_file.exists():
                element = Element.load_from_file(element_file)
                self._cache[cache_key] = element
                return element

        raise FileNotFoundError(f"Element not found: {name}")

    def list_elements(
        self, element_type: Optional[ElementType] = None
    ) -> List[Element]:
        """List all available elements.

        Args:
            element_type: Optional type filter

        Returns:
            List of elements
        """
        elements = []

        for search_path in self.search_paths:
            if element_type:
                type_dirs = [search_path / element_type.value]
            else:
                type_dirs = [search_path / et.value for et in ElementType]

            for type_dir in type_dirs:
                if not type_dir.exists():
                    continue

                for element_dir in type_dir.iterdir():
                    if not element_dir.is_dir():
                        continue

                    element_file = element_dir / "element.yaml"
                    if element_file.exists():
                        try:
                            element = Element.load_from_file(element_file)
                            elements.append(element)
                        except Exception:
                            # Skip malformed elements
                            pass

        return elements

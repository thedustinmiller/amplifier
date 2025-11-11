"""
Forge: A Composable AI Development System

Core exports for the Forge system.
"""

__version__ = "0.1.0"

from forge.core import (
    Element,
    Composition,
    Context,
    Tool,
    Agent,
    Hook,
)

from forge.memory import (
    MemoryProvider,
    Scope,
    MemoryEntry,
    FileProvider,
)

__all__ = [
    "Element",
    "Composition",
    "Context",
    "Tool",
    "Agent",
    "Hook",
    "MemoryProvider",
    "Scope",
    "MemoryEntry",
    "FileProvider",
]

"""
Core abstractions for Forge.

Provides Element, Composition, Context, and base classes for tools, agents, and hooks.
"""

from forge.core.element import Element, ElementType
from forge.core.composition import Composition, CompositionLoader
from forge.core.context import Context
from forge.core.tool import Tool
from forge.core.agent import Agent
from forge.core.hook import Hook

__all__ = [
    "Element",
    "ElementType",
    "Composition",
    "CompositionLoader",
    "Context",
    "Tool",
    "Agent",
    "Hook",
]

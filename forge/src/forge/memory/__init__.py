"""
Memory system for Forge.

Provides pluggable memory providers with different backends.
"""

from forge.memory.protocol import (
    MemoryProvider,
    Scope,
    MemoryEntry,
)

from forge.memory.file_provider import FileProvider

__all__ = [
    "MemoryProvider",
    "Scope",
    "MemoryEntry",
    "FileProvider",
]

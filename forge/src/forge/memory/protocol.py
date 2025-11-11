"""
Memory provider protocol and core types.
"""

from typing import Protocol, Optional, List, Dict, Any
from enum import Enum
from dataclasses import dataclass, asdict
import time


class Scope(Enum):
    """Memory scopes with different lifetimes."""

    SESSION = "session"  # Current working context (ephemeral)
    PROJECT = "project"  # Project-specific (persistent)
    GLOBAL = "global"  # Cross-project (permanent)


@dataclass
class MemoryEntry:
    """Memory entry with metadata."""

    key: str
    value: str
    scope: Scope
    timestamp: int
    tags: List[str]
    metadata: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        result = asdict(self)
        result["scope"] = self.scope.value
        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "MemoryEntry":
        """Create from dictionary."""
        data["scope"] = Scope(data["scope"])
        return cls(**data)


class MemoryProvider(Protocol):
    """Abstract memory provider interface.

    All memory providers must implement this protocol.
    """

    async def initialize(self, config: Dict[str, Any]) -> None:
        """Initialize provider with configuration.

        Args:
            config: Provider-specific configuration
        """
        ...

    async def get(self, key: str, scope: Scope) -> Optional[MemoryEntry]:
        """Retrieve value by key within scope.

        Args:
            key: Unique identifier within scope
            scope: Memory scope (session/project/global)

        Returns:
            MemoryEntry if found, None otherwise
        """
        ...

    async def set(
        self,
        key: str,
        value: str,
        scope: Scope,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Store value with key in scope.

        Args:
            key: Unique identifier within scope
            value: Content to store
            scope: Memory scope (session/project/global)
            tags: Optional tags for categorization
            metadata: Optional metadata dictionary
        """
        ...

    async def query(
        self, pattern: str, scope: Scope, limit: Optional[int] = None
    ) -> List[MemoryEntry]:
        """Query entries matching pattern.

        Pattern syntax:
        - "prefix:*" - All keys starting with "prefix:"
        - "*:suffix" - All keys ending with ":suffix"
        - "key" - Exact match
        - "tag:tagname" - All entries with tag

        Args:
            pattern: Query pattern
            scope: Memory scope to search
            limit: Maximum number of results

        Returns:
            List of matching entries
        """
        ...

    async def search(
        self, semantic: str, scope: Scope, limit: int = 10, threshold: float = 0.7
    ) -> List[tuple[MemoryEntry, float]]:
        """Semantic search (requires vector support).

        Args:
            semantic: Natural language query
            scope: Memory scope to search
            limit: Maximum number of results
            threshold: Minimum similarity score (0-1)

        Returns:
            List of (entry, similarity_score) tuples

        Raises:
            NotImplementedError: If provider doesn't support semantic search
        """
        ...

    async def delete(self, key: str, scope: Scope) -> bool:
        """Delete entry by key.

        Args:
            key: Unique identifier within scope
            scope: Memory scope

        Returns:
            True if deleted, False if not found
        """
        ...

    async def clear(self, scope: Scope) -> int:
        """Clear all entries in scope.

        Args:
            scope: Memory scope to clear

        Returns:
            Number of entries deleted
        """
        ...

    async def close(self) -> None:
        """Close provider and release resources."""
        ...


class AdvancedMemoryProvider(MemoryProvider):
    """Extended capabilities for advanced providers.

    Optional interface for providers that support relationships,
    transactions, and other advanced features.
    """

    async def relate(
        self, from_key: str, to_key: str, relation_type: str, scope: Scope
    ) -> None:
        """Create relationship between entries (graph providers).

        Args:
            from_key: Source entry key
            to_key: Target entry key
            relation_type: Type of relationship (e.g., "IMPLEMENTS", "DEPENDS_ON")
            scope: Memory scope
        """
        ...

    async def traverse(
        self,
        start_key: str,
        relation_type: str,
        scope: Scope,
        max_depth: int = 3,
    ) -> List[List[MemoryEntry]]:
        """Traverse relationships (graph providers).

        Args:
            start_key: Starting entry key
            relation_type: Relationship type to follow
            scope: Memory scope
            max_depth: Maximum traversal depth

        Returns:
            List of paths (each path is list of entries)
        """
        ...

    async def transaction(self) -> "Transaction":
        """Begin transaction (relational providers).

        Returns:
            Transaction context manager
        """
        ...

    async def index(self, field: str, scope: Scope) -> None:
        """Create index for faster queries.

        Args:
            field: Field to index (key, tags, etc.)
            scope: Memory scope
        """
        ...


def create_memory_entry(
    key: str,
    value: str,
    scope: Scope,
    tags: Optional[List[str]] = None,
    metadata: Optional[Dict[str, Any]] = None,
) -> MemoryEntry:
    """Helper to create a memory entry with current timestamp.

    Args:
        key: Unique identifier
        value: Content
        scope: Memory scope
        tags: Optional tags
        metadata: Optional metadata

    Returns:
        New MemoryEntry
    """
    return MemoryEntry(
        key=key,
        value=value,
        scope=scope,
        timestamp=int(time.time()),
        tags=tags or [],
        metadata=metadata or {},
    )

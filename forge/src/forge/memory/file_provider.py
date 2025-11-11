"""
File-based memory provider implementation.

Simple, dependency-free memory storage using JSON files.
"""

import json
import re
import asyncio
from pathlib import Path
from typing import Optional, List, Dict, Any
from dataclasses import asdict

from forge.memory.protocol import MemoryProvider, Scope, MemoryEntry, create_memory_entry


class FileProvider:
    """File-based memory provider.

    Stores memory entries as JSON files in a directory structure:
    .forge/memory/
    ├── session/
    │   └── {session_id}/
    │       └── {key}.json
    ├── project/
    │   ├── {key}.json
    │   └── _index.json
    └── global/
        ├── {key}.json
        └── _index.json
    """

    def __init__(self):
        """Initialize file provider."""
        self.base_path: Optional[Path] = None
        self.session_id: Optional[str] = None
        self._index_cache: Dict[Scope, List[Dict[str, Any]]] = {}
        self._lock = asyncio.Lock()

    async def initialize(self, config: Dict[str, Any]) -> None:
        """Initialize file provider.

        Args:
            config: Configuration dictionary with:
                - base_path: Base directory for memory files
                - session_id: Current session identifier
                - compression: Whether to compress files (not implemented)
        """
        self.base_path = Path(config.get("base_path", ".forge/memory"))
        self.session_id = config.get("session_id", "default")

        # Create scope directories
        await self._ensure_directories()

        # Load indices
        await self._load_indices()

    async def _ensure_directories(self) -> None:
        """Ensure all required directories exist."""
        if not self.base_path:
            raise RuntimeError("FileProvider not initialized")

        self.base_path.mkdir(parents=True, exist_ok=True)

        for scope in Scope:
            scope_path = self._get_scope_path(scope)
            scope_path.mkdir(parents=True, exist_ok=True)

    def _get_scope_path(self, scope: Scope) -> Path:
        """Get path for a scope.

        Args:
            scope: Memory scope

        Returns:
            Path to scope directory
        """
        if scope == Scope.SESSION:
            return self.base_path / "session" / self.session_id
        else:
            return self.base_path / scope.value

    def _key_to_filename(self, key: str) -> str:
        """Convert key to safe filename.

        Args:
            key: Memory key

        Returns:
            Safe filename
        """
        # Replace unsafe characters
        safe_key = re.sub(r'[^\w\-.]', '_', key)
        return f"{safe_key}.json"

    def _get_entry_path(self, key: str, scope: Scope) -> Path:
        """Get path for an entry.

        Args:
            key: Memory key
            scope: Memory scope

        Returns:
            Path to entry file
        """
        scope_path = self._get_scope_path(scope)
        filename = self._key_to_filename(key)
        return scope_path / filename

    def _get_index_path(self, scope: Scope) -> Path:
        """Get path for scope index.

        Args:
            scope: Memory scope

        Returns:
            Path to index file
        """
        scope_path = self._get_scope_path(scope)
        return scope_path / "_index.json"

    async def _load_indices(self) -> None:
        """Load indices for all scopes."""
        for scope in Scope:
            await self._load_index(scope)

    async def _load_index(self, scope: Scope) -> List[Dict[str, Any]]:
        """Load index for a scope.

        Args:
            scope: Memory scope

        Returns:
            List of index entries
        """
        index_path = self._get_index_path(scope)

        if not index_path.exists():
            self._index_cache[scope] = []
            return []

        try:
            with open(index_path, 'r') as f:
                index_data = json.load(f)
                self._index_cache[scope] = index_data
                return index_data
        except (json.JSONDecodeError, IOError):
            self._index_cache[scope] = []
            return []

    async def _save_index(self, scope: Scope) -> None:
        """Save index for a scope.

        Args:
            scope: Memory scope
        """
        index_path = self._get_index_path(scope)
        index_data = self._index_cache.get(scope, [])

        async with self._lock:
            with open(index_path, 'w') as f:
                json.dump(index_data, f, indent=2)

    async def _update_index(self, entry: MemoryEntry) -> None:
        """Update index with entry.

        Args:
            entry: Memory entry to add/update
        """
        index = self._index_cache.get(entry.scope, [])

        # Remove existing entry with same key
        index = [e for e in index if e.get("key") != entry.key]

        # Add new entry
        index.append({
            "key": entry.key,
            "timestamp": entry.timestamp,
            "tags": entry.tags,
            "metadata": entry.metadata,
        })

        # Sort by timestamp (newest first)
        index.sort(key=lambda e: e["timestamp"], reverse=True)

        self._index_cache[entry.scope] = index
        await self._save_index(entry.scope)

    async def _remove_from_index(self, key: str, scope: Scope) -> None:
        """Remove entry from index.

        Args:
            key: Memory key
            scope: Memory scope
        """
        index = self._index_cache.get(scope, [])
        index = [e for e in index if e.get("key") != key]
        self._index_cache[scope] = index
        await self._save_index(scope)

    async def get(self, key: str, scope: Scope) -> Optional[MemoryEntry]:
        """Retrieve value by key within scope.

        Args:
            key: Unique identifier within scope
            scope: Memory scope (session/project/global)

        Returns:
            MemoryEntry if found, None otherwise
        """
        entry_path = self._get_entry_path(key, scope)

        if not entry_path.exists():
            return None

        try:
            with open(entry_path, 'r') as f:
                data = json.load(f)
                return MemoryEntry.from_dict(data)
        except (json.JSONDecodeError, IOError):
            return None

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
        entry = create_memory_entry(key, value, scope, tags, metadata)

        entry_path = self._get_entry_path(key, scope)
        entry_path.parent.mkdir(parents=True, exist_ok=True)

        # Write entry
        with open(entry_path, 'w') as f:
            json.dump(entry.to_dict(), f, indent=2)

        # Update index
        await self._update_index(entry)

    def _matches_pattern(self, key: str, pattern: str) -> bool:
        """Check if key matches pattern.

        Args:
            key: Memory key
            pattern: Query pattern

        Returns:
            True if matches, False otherwise
        """
        # Exact match
        if pattern == key:
            return True

        # Prefix match: "prefix:*"
        if pattern.endswith(":*"):
            prefix = pattern[:-2]
            return key.startswith(prefix)

        # Suffix match: "*:suffix"
        if pattern.startswith("*:"):
            suffix = pattern[2:]
            return key.endswith(suffix)

        # Contains match: "*substring*"
        if pattern.startswith("*") and pattern.endswith("*"):
            substring = pattern[1:-1]
            return substring in key

        return False

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
        # Check if it's a tag query
        if pattern.startswith("tag:"):
            tag_name = pattern[4:]
            return await self._query_by_tag(tag_name, scope, limit)

        # Load index
        index = self._index_cache.get(scope, [])

        # Match pattern
        matches = []
        for entry_data in index:
            key = entry_data["key"]
            if self._matches_pattern(key, pattern):
                entry = await self.get(key, scope)
                if entry:
                    matches.append(entry)

                if limit and len(matches) >= limit:
                    break

        return matches

    async def _query_by_tag(
        self, tag: str, scope: Scope, limit: Optional[int] = None
    ) -> List[MemoryEntry]:
        """Query entries by tag.

        Args:
            tag: Tag name
            scope: Memory scope
            limit: Maximum number of results

        Returns:
            List of matching entries
        """
        index = self._index_cache.get(scope, [])

        matches = []
        for entry_data in index:
            if tag in entry_data.get("tags", []):
                key = entry_data["key"]
                entry = await self.get(key, scope)
                if entry:
                    matches.append(entry)

                if limit and len(matches) >= limit:
                    break

        return matches

    async def search(
        self, semantic: str, scope: Scope, limit: int = 10, threshold: float = 0.7
    ) -> List[tuple[MemoryEntry, float]]:
        """Semantic search not supported in file provider.

        Args:
            semantic: Natural language query
            scope: Memory scope to search
            limit: Maximum number of results
            threshold: Minimum similarity score (0-1)

        Raises:
            NotImplementedError: FileProvider doesn't support semantic search
        """
        raise NotImplementedError(
            "FileProvider doesn't support semantic search. "
            "Use VectorProvider for semantic capabilities."
        )

    async def delete(self, key: str, scope: Scope) -> bool:
        """Delete entry by key.

        Args:
            key: Unique identifier within scope
            scope: Memory scope

        Returns:
            True if deleted, False if not found
        """
        entry_path = self._get_entry_path(key, scope)

        if not entry_path.exists():
            return False

        try:
            entry_path.unlink()
            await self._remove_from_index(key, scope)
            return True
        except IOError:
            return False

    async def clear(self, scope: Scope) -> int:
        """Clear all entries in scope.

        Args:
            scope: Memory scope to clear

        Returns:
            Number of entries deleted
        """
        scope_path = self._get_scope_path(scope)

        if not scope_path.exists():
            return 0

        count = 0
        for entry_file in scope_path.glob("*.json"):
            if entry_file.name != "_index.json":
                try:
                    entry_file.unlink()
                    count += 1
                except IOError:
                    pass

        # Clear index
        self._index_cache[scope] = []
        await self._save_index(scope)

        return count

    async def close(self) -> None:
        """Close provider and release resources."""
        # Save all indices
        for scope in Scope:
            if scope in self._index_cache:
                await self._save_index(scope)

        # Clear cache
        self._index_cache.clear()

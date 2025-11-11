"""
Tests for memory providers.
"""

import asyncio
import tempfile
from pathlib import Path
import pytest

from forge.memory import FileProvider, Scope


@pytest.mark.asyncio
async def test_file_provider_basic():
    """Test basic file provider operations."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Initialize
        memory = FileProvider()
        await memory.initialize({
            "base_path": tmpdir,
            "session_id": "test"
        })

        # Set value
        await memory.set(
            key="test:key",
            value="test value",
            scope=Scope.PROJECT,
            tags=["test"]
        )

        # Get value
        entry = await memory.get("test:key", Scope.PROJECT)
        assert entry is not None
        assert entry.key == "test:key"
        assert entry.value == "test value"
        assert "test" in entry.tags

        # Query
        results = await memory.query("test:*", Scope.PROJECT)
        assert len(results) == 1
        assert results[0].key == "test:key"

        # Delete
        deleted = await memory.delete("test:key", Scope.PROJECT)
        assert deleted is True

        # Verify deleted
        entry = await memory.get("test:key", Scope.PROJECT)
        assert entry is None

        await memory.close()


@pytest.mark.asyncio
async def test_file_provider_scopes():
    """Test different memory scopes."""
    with tempfile.TemporaryDirectory() as tmpdir:
        memory = FileProvider()
        await memory.initialize({
            "base_path": tmpdir,
            "session_id": "test"
        })

        # Store in different scopes
        await memory.set("key1", "session value", Scope.SESSION)
        await memory.set("key2", "project value", Scope.PROJECT)
        await memory.set("key3", "global value", Scope.GLOBAL)

        # Retrieve from correct scopes
        assert (await memory.get("key1", Scope.SESSION)).value == "session value"
        assert (await memory.get("key2", Scope.PROJECT)).value == "project value"
        assert (await memory.get("key3", Scope.GLOBAL)).value == "global value"

        # Keys don't cross scopes
        assert await memory.get("key1", Scope.PROJECT) is None
        assert await memory.get("key2", Scope.GLOBAL) is None

        await memory.close()


@pytest.mark.asyncio
async def test_file_provider_tags():
    """Test tag-based queries."""
    with tempfile.TemporaryDirectory() as tmpdir:
        memory = FileProvider()
        await memory.initialize({
            "base_path": tmpdir,
            "session_id": "test"
        })

        # Store with tags
        await memory.set("key1", "value1", Scope.PROJECT, tags=["tag1", "tag2"])
        await memory.set("key2", "value2", Scope.PROJECT, tags=["tag2", "tag3"])
        await memory.set("key3", "value3", Scope.PROJECT, tags=["tag3"])

        # Query by tag
        results = await memory.query("tag:tag2", Scope.PROJECT)
        assert len(results) == 2
        keys = {r.key for r in results}
        assert "key1" in keys
        assert "key2" in keys

        await memory.close()


@pytest.mark.asyncio
async def test_file_provider_clear():
    """Test clearing a scope."""
    with tempfile.TemporaryDirectory() as tmpdir:
        memory = FileProvider()
        await memory.initialize({
            "base_path": tmpdir,
            "session_id": "test"
        })

        # Store multiple entries
        await memory.set("key1", "value1", Scope.PROJECT)
        await memory.set("key2", "value2", Scope.PROJECT)
        await memory.set("key3", "value3", Scope.PROJECT)

        # Clear scope
        count = await memory.clear(Scope.PROJECT)
        assert count == 3

        # Verify cleared
        assert await memory.get("key1", Scope.PROJECT) is None
        assert await memory.get("key2", Scope.PROJECT) is None
        assert await memory.get("key3", Scope.PROJECT) is None

        await memory.close()


def test_import():
    """Test that imports work."""
    from forge.memory import MemoryProvider, Scope, MemoryEntry, FileProvider
    assert MemoryProvider is not None
    assert Scope is not None
    assert MemoryEntry is not None
    assert FileProvider is not None

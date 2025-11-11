#!/usr/bin/env python3
"""
Comprehensive memory system test script.

Tests all FileProvider operations across all scopes with detailed verification.
"""

import asyncio
import tempfile
import json
from pathlib import Path
from datetime import datetime
import sys
import time

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from forge.memory import FileProvider, Scope


class TestResults:
    """Track test results and timing."""

    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors = []
        self.timings = {}

    def record_pass(self, test_name: str, duration: float):
        self.passed += 1
        self.timings[test_name] = duration
        print(f"✓ {test_name} ({duration:.3f}s)")

    def record_fail(self, test_name: str, error: str):
        self.failed += 1
        self.errors.append((test_name, error))
        print(f"✗ {test_name}: {error}")

    def summary(self):
        print("\n" + "="*70)
        print(f"Test Results: {self.passed} passed, {self.failed} failed")
        print(f"Total time: {sum(self.timings.values()):.3f}s")
        if self.errors:
            print("\nFailures:")
            for name, error in self.errors:
                print(f"  - {name}: {error}")
        print("="*70)


async def test_initialization(tmpdir: Path, results: TestResults):
    """Test FileProvider initialization."""
    test_name = "Initialization"
    start = time.time()

    try:
        test_dir = tmpdir / "init_test"
        memory = FileProvider()
        await memory.initialize({
            "base_path": str(test_dir),
            "session_id": "test_session_123"
        })

        # Verify directories created
        assert (test_dir / "session" / "test_session_123").exists(), "Session dir not created"
        assert (test_dir / "project").exists(), "Project dir not created"
        assert (test_dir / "global").exists(), "Global dir not created"

        await memory.close()
        results.record_pass(test_name, time.time() - start)
        return True
    except Exception as e:
        results.record_fail(test_name, str(e))
        return False


async def test_set_operations(tmpdir: Path, results: TestResults):
    """Test set() operations in all scopes."""
    test_name = "Set Operations (All Scopes)"
    start = time.time()

    try:
        test_dir = tmpdir / "set_test"
        memory = FileProvider()
        await memory.initialize({
            "base_path": str(test_dir),
            "session_id": "test_session"
        })

        # Test SESSION scope
        await memory.set(
            key="session:user",
            value="Alice",
            scope=Scope.SESSION,
            tags=["user", "session"],
            metadata={"role": "developer"}
        )

        # Test PROJECT scope
        await memory.set(
            key="project:config",
            value='{"theme": "dark", "lang": "en"}',
            scope=Scope.PROJECT,
            tags=["config", "project"],
            metadata={"version": "1.0"}
        )

        # Test GLOBAL scope
        await memory.set(
            key="global:api_key",
            value="sk-test-key-123",
            scope=Scope.GLOBAL,
            tags=["auth", "global"],
            metadata={"created": "2025-11-11"}
        )

        # Verify files exist
        session_file = test_dir / "session" / "test_session" / "session_user.json"
        project_file = test_dir / "project" / "project_config.json"
        global_file = test_dir / "global" / "global_api_key.json"

        assert session_file.exists(), f"Session file not created: {session_file}"
        assert project_file.exists(), f"Project file not created: {project_file}"
        assert global_file.exists(), f"Global file not created: {global_file}"

        await memory.close()
        results.record_pass(test_name, time.time() - start)
        return memory, tmpdir
    except Exception as e:
        results.record_fail(test_name, str(e))
        return None, None


async def test_get_operations(tmpdir: Path, results: TestResults):
    """Test get() operations."""
    test_name = "Get Operations"
    start = time.time()

    try:
        test_dir = tmpdir / "get_test"
        memory = FileProvider()
        await memory.initialize({
            "base_path": str(test_dir),
            "session_id": "test_session"
        })

        # Store test data
        await memory.set("test:key1", "value1", Scope.PROJECT, tags=["test"])
        await memory.set("test:key2", "value2", Scope.SESSION, tags=["test"])
        await memory.set("test:key3", "value3", Scope.GLOBAL, tags=["test"])

        # Test retrievals
        entry1 = await memory.get("test:key1", Scope.PROJECT)
        entry2 = await memory.get("test:key2", Scope.SESSION)
        entry3 = await memory.get("test:key3", Scope.GLOBAL)

        assert entry1 is not None, "Failed to get PROJECT entry"
        assert entry1.value == "value1", f"Wrong value: {entry1.value}"
        assert entry1.key == "test:key1", f"Wrong key: {entry1.key}"
        assert "test" in entry1.tags, f"Missing tag: {entry1.tags}"

        assert entry2 is not None, "Failed to get SESSION entry"
        assert entry2.value == "value2"

        assert entry3 is not None, "Failed to get GLOBAL entry"
        assert entry3.value == "value3"

        # Test non-existent key
        missing = await memory.get("nonexistent", Scope.PROJECT)
        assert missing is None, "Should return None for missing key"

        # Test scope isolation
        wrong_scope = await memory.get("test:key1", Scope.SESSION)
        assert wrong_scope is None, "Keys should not cross scopes"

        await memory.close()
        results.record_pass(test_name, time.time() - start)
    except Exception as e:
        results.record_fail(test_name, str(e))


async def test_query_patterns(tmpdir: Path, results: TestResults):
    """Test query() with various patterns."""
    test_name = "Query Patterns"
    start = time.time()

    try:
        test_dir = tmpdir / "query_test"
        memory = FileProvider()
        await memory.initialize({
            "base_path": str(test_dir),
            "session_id": "test_session"
        })

        # Store test data with various keys
        await memory.set("user:alice", "Alice Data", Scope.PROJECT, tags=["user"])
        await memory.set("user:bob", "Bob Data", Scope.PROJECT, tags=["user"])
        await memory.set("config:theme", "dark", Scope.PROJECT, tags=["config"])
        await memory.set("config:lang", "en", Scope.PROJECT, tags=["config"])
        await memory.set("data:important", "Important", Scope.PROJECT, tags=["important"])

        # Test prefix pattern: "user:*"
        user_results = await memory.query("user:*", Scope.PROJECT)
        assert len(user_results) == 2, f"Expected 2 user results, got {len(user_results)}"
        user_keys = {r.key for r in user_results}
        assert "user:alice" in user_keys
        assert "user:bob" in user_keys

        # Test prefix pattern: "config:*"
        config_results = await memory.query("config:*", Scope.PROJECT)
        assert len(config_results) == 2, f"Expected 2 config results, got {len(config_results)}"

        # Test exact match
        exact_results = await memory.query("user:alice", Scope.PROJECT)
        assert len(exact_results) == 1, f"Expected 1 exact result, got {len(exact_results)}"
        assert exact_results[0].key == "user:alice"

        # Test tag query: "tag:user"
        tag_results = await memory.query("tag:user", Scope.PROJECT)
        assert len(tag_results) == 2, f"Expected 2 tagged results, got {len(tag_results)}"

        # Test tag query: "tag:config"
        config_tag_results = await memory.query("tag:config", Scope.PROJECT)
        assert len(config_tag_results) == 2

        # Test limit parameter
        limited_results = await memory.query("config:*", Scope.PROJECT, limit=1)
        assert len(limited_results) == 1, f"Limit not working: got {len(limited_results)}"

        await memory.close()
        results.record_pass(test_name, time.time() - start)
    except Exception as e:
        results.record_fail(test_name, str(e))


async def test_suffix_and_contains_patterns(tmpdir: Path, results: TestResults):
    """Test suffix and contains query patterns."""
    test_name = "Suffix & Contains Patterns"
    start = time.time()

    try:
        test_dir = tmpdir / "suffix_test"
        memory = FileProvider()
        await memory.initialize({
            "base_path": str(test_dir),
            "session_id": "test_session"
        })

        # Store test data
        await memory.set("alpha:config", "Config 1", Scope.PROJECT)
        await memory.set("beta:config", "Config 2", Scope.PROJECT)
        await memory.set("gamma:setting", "Setting 1", Scope.PROJECT)
        await memory.set("test_important_data", "Important", Scope.PROJECT)

        # Test suffix pattern: "*:config"
        suffix_results = await memory.query("*:config", Scope.PROJECT)
        assert len(suffix_results) == 2, f"Expected 2 suffix results, got {len(suffix_results)}"
        keys = {r.key for r in suffix_results}
        assert "alpha:config" in keys
        assert "beta:config" in keys

        # Test contains pattern: "*important*"
        contains_results = await memory.query("*important*", Scope.PROJECT)
        assert len(contains_results) == 1, f"Expected 1 contains result, got {len(contains_results)}"
        assert contains_results[0].key == "test_important_data"

        await memory.close()
        results.record_pass(test_name, time.time() - start)
    except Exception as e:
        results.record_fail(test_name, str(e))


async def test_delete_operations(tmpdir: Path, results: TestResults):
    """Test delete() operations."""
    test_name = "Delete Operations"
    start = time.time()

    try:
        test_dir = tmpdir / "delete_test"
        memory = FileProvider()
        await memory.initialize({
            "base_path": str(test_dir),
            "session_id": "test_session"
        })

        # Store test data
        await memory.set("delete:test1", "Value 1", Scope.PROJECT)
        await memory.set("delete:test2", "Value 2", Scope.PROJECT)

        # Verify exists
        entry = await memory.get("delete:test1", Scope.PROJECT)
        assert entry is not None, "Entry should exist before delete"

        # Delete entry
        deleted = await memory.delete("delete:test1", Scope.PROJECT)
        assert deleted is True, "Delete should return True"

        # Verify deleted
        entry = await memory.get("delete:test1", Scope.PROJECT)
        assert entry is None, "Entry should not exist after delete"

        # Verify file removed
        file_path = test_dir / "project" / "delete_test1.json"
        assert not file_path.exists(), "File should be removed"

        # Verify other entry still exists
        entry2 = await memory.get("delete:test2", Scope.PROJECT)
        assert entry2 is not None, "Other entries should not be affected"

        # Test deleting non-existent key
        deleted = await memory.delete("nonexistent", Scope.PROJECT)
        assert deleted is False, "Delete of non-existent should return False"

        await memory.close()
        results.record_pass(test_name, time.time() - start)
    except Exception as e:
        results.record_fail(test_name, str(e))


async def test_clear_operations(tmpdir: Path, results: TestResults):
    """Test clear() operations."""
    test_name = "Clear Operations"
    start = time.time()

    try:
        test_dir = tmpdir / "clear_test"
        memory = FileProvider()
        await memory.initialize({
            "base_path": str(test_dir),
            "session_id": "test_session"
        })

        # Store test data in multiple scopes
        await memory.set("key1", "value1", Scope.PROJECT)
        await memory.set("key2", "value2", Scope.PROJECT)
        await memory.set("key3", "value3", Scope.PROJECT)
        await memory.set("session1", "value1", Scope.SESSION)
        await memory.set("session2", "value2", Scope.SESSION)

        # Clear PROJECT scope
        count = await memory.clear(Scope.PROJECT)
        assert count == 3, f"Expected 3 cleared, got {count}"

        # Verify PROJECT scope is empty
        entry = await memory.get("key1", Scope.PROJECT)
        assert entry is None, "PROJECT scope should be empty"

        # Verify SESSION scope unaffected
        entry = await memory.get("session1", Scope.SESSION)
        assert entry is not None, "SESSION scope should be unaffected"

        # Clear SESSION scope
        count = await memory.clear(Scope.SESSION)
        assert count == 2, f"Expected 2 cleared, got {count}"

        # Verify SESSION scope is empty
        entry = await memory.get("session1", Scope.SESSION)
        assert entry is None, "SESSION scope should be empty"

        await memory.close()
        results.record_pass(test_name, time.time() - start)
    except Exception as e:
        results.record_fail(test_name, str(e))


async def test_index_maintenance(tmpdir: Path, results: TestResults):
    """Test that _index.json files are properly maintained."""
    test_name = "Index Maintenance"
    start = time.time()

    try:
        test_dir = tmpdir / "index_test"
        memory = FileProvider()
        await memory.initialize({
            "base_path": str(test_dir),
            "session_id": "test_session"
        })

        # Store entries
        await memory.set("idx:key1", "value1", Scope.PROJECT, tags=["tag1"])
        await memory.set("idx:key2", "value2", Scope.PROJECT, tags=["tag2"])
        await memory.set("idx:key3", "value3", Scope.GLOBAL, tags=["tag3"])

        # Check index files exist
        project_index = test_dir / "project" / "_index.json"
        global_index = test_dir / "global" / "_index.json"

        assert project_index.exists(), "Project index not created"
        assert global_index.exists(), "Global index not created"

        # Verify index contents
        with open(project_index) as f:
            project_idx = json.load(f)

        assert len(project_idx) == 2, f"Expected 2 entries in index, got {len(project_idx)}"

        # Check index entries have required fields
        for entry in project_idx:
            assert "key" in entry, "Index entry missing key"
            assert "timestamp" in entry, "Index entry missing timestamp"
            assert "tags" in entry, "Index entry missing tags"
            assert "metadata" in entry, "Index entry missing metadata"

        # Verify index is sorted by timestamp (newest first)
        if len(project_idx) > 1:
            for i in range(len(project_idx) - 1):
                assert project_idx[i]["timestamp"] >= project_idx[i+1]["timestamp"], \
                    "Index not sorted by timestamp"

        # Test index updates on delete
        await memory.delete("idx:key1", Scope.PROJECT)

        with open(project_index) as f:
            project_idx = json.load(f)

        assert len(project_idx) == 1, "Index not updated after delete"
        remaining_keys = [e["key"] for e in project_idx]
        assert "idx:key1" not in remaining_keys, "Deleted key still in index"
        assert "idx:key2" in remaining_keys, "Other key removed from index"

        # Test index cleared
        await memory.clear(Scope.PROJECT)

        with open(project_index) as f:
            project_idx = json.load(f)

        assert len(project_idx) == 0, "Index not cleared"

        await memory.close()
        results.record_pass(test_name, time.time() - start)
    except Exception as e:
        results.record_fail(test_name, str(e))


async def test_persistence(tmpdir: Path, results: TestResults):
    """Test that data persists across provider instances."""
    test_name = "Data Persistence"
    start = time.time()

    try:
        test_dir = tmpdir / "persist_test"
        # Create first provider instance
        memory1 = FileProvider()
        await memory1.initialize({
            "base_path": str(test_dir),
            "session_id": "persist_test"
        })

        # Store data
        await memory1.set("persist:key", "persistent value", Scope.PROJECT, tags=["persist"])
        await memory1.close()

        # Create second provider instance
        memory2 = FileProvider()
        await memory2.initialize({
            "base_path": str(test_dir),
            "session_id": "persist_test"
        })

        # Retrieve data
        entry = await memory2.get("persist:key", Scope.PROJECT)
        assert entry is not None, "Data did not persist"
        assert entry.value == "persistent value", "Value changed after reload"
        assert "persist" in entry.tags, "Tags not persisted"

        # Verify query works after reload
        results_query = await memory2.query("persist:*", Scope.PROJECT)
        assert len(results_query) == 1, "Query failed after reload"

        await memory2.close()
        results.record_pass(test_name, time.time() - start)
    except Exception as e:
        results.record_fail(test_name, str(e))


async def test_metadata_handling(tmpdir: Path, results: TestResults):
    """Test metadata storage and retrieval."""
    test_name = "Metadata Handling"
    start = time.time()

    try:
        test_dir = tmpdir / "metadata_test"
        memory = FileProvider()
        await memory.initialize({
            "base_path": str(test_dir),
            "session_id": "test_session"
        })

        # Store with complex metadata
        metadata = {
            "author": "Alice",
            "version": 2,
            "created": "2025-11-11",
            "nested": {
                "field1": "value1",
                "field2": 123
            }
        }

        await memory.set(
            "meta:test",
            "value with metadata",
            Scope.PROJECT,
            tags=["meta", "test"],
            metadata=metadata
        )

        # Retrieve and verify metadata
        entry = await memory.get("meta:test", Scope.PROJECT)
        assert entry is not None, "Entry not found"
        assert entry.metadata == metadata, f"Metadata mismatch: {entry.metadata}"
        assert entry.metadata["author"] == "Alice"
        assert entry.metadata["nested"]["field2"] == 123

        await memory.close()
        results.record_pass(test_name, time.time() - start)
    except Exception as e:
        results.record_fail(test_name, str(e))


async def test_special_characters_in_keys(tmpdir: Path, results: TestResults):
    """Test handling of special characters in keys."""
    test_name = "Special Characters in Keys"
    start = time.time()

    try:
        test_dir = tmpdir / "special_chars_test"
        memory = FileProvider()
        await memory.initialize({
            "base_path": str(test_dir),
            "session_id": "test_session"
        })

        # Test keys with special characters
        special_keys = [
            "key:with:colons",
            "key-with-dashes",
            "key.with.dots",
            "key_with_underscores",
            "key with spaces",  # Will be sanitized
            "key@with#special$chars",  # Will be sanitized
        ]

        for key in special_keys:
            await memory.set(key, f"value for {key}", Scope.PROJECT)

        # Verify all can be retrieved
        for key in special_keys:
            entry = await memory.get(key, Scope.PROJECT)
            assert entry is not None, f"Failed to retrieve key: {key}"
            assert entry.key == key, f"Key mismatch: {entry.key} != {key}"

        await memory.close()
        results.record_pass(test_name, time.time() - start)
    except Exception as e:
        results.record_fail(test_name, str(e))


async def verify_file_structure(tmpdir: Path, results: TestResults):
    """Verify the complete file structure."""
    test_name = "File Structure Verification"
    start = time.time()

    try:
        test_dir = tmpdir / "struct_test"
        memory = FileProvider()
        await memory.initialize({
            "base_path": str(test_dir),
            "session_id": "struct_test"
        })

        # Create comprehensive structure
        await memory.set("s1", "session value", Scope.SESSION)
        await memory.set("p1", "project value", Scope.PROJECT)
        await memory.set("g1", "global value", Scope.GLOBAL)
        await memory.close()

        # Verify directory structure
        expected_structure = {
            "session/struct_test": ["s1.json"],
            "project": ["p1.json", "_index.json"],
            "global": ["g1.json", "_index.json"],
        }

        for path, files in expected_structure.items():
            dir_path = test_dir / path
            assert dir_path.exists(), f"Directory not found: {path}"

            for filename in files:
                file_path = dir_path / filename
                assert file_path.exists(), f"File not found: {path}/{filename}"

        # Verify JSON structure
        with open(test_dir / "project" / "p1.json") as f:
            entry_data = json.load(f)
            assert "key" in entry_data
            assert "value" in entry_data
            assert "scope" in entry_data
            assert "timestamp" in entry_data
            assert "tags" in entry_data
            assert "metadata" in entry_data
            assert entry_data["key"] == "p1"
            assert entry_data["value"] == "project value"
            assert entry_data["scope"] == "project"

        results.record_pass(test_name, time.time() - start)
    except Exception as e:
        results.record_fail(test_name, str(e))


async def main():
    """Run comprehensive memory system tests."""
    print("="*70)
    print("FORGE MEMORY SYSTEM - COMPREHENSIVE TEST SUITE")
    print("="*70)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    results = TestResults()

    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)
        print(f"Test directory: {tmpdir}\n")

        # Run all tests
        await test_initialization(tmpdir, results)
        await test_set_operations(tmpdir, results)
        await test_get_operations(tmpdir, results)
        await test_query_patterns(tmpdir, results)
        await test_suffix_and_contains_patterns(tmpdir, results)
        await test_delete_operations(tmpdir, results)
        await test_clear_operations(tmpdir, results)
        await test_index_maintenance(tmpdir, results)
        await test_persistence(tmpdir, results)
        await test_metadata_handling(tmpdir, results)
        await test_special_characters_in_keys(tmpdir, results)
        await verify_file_structure(tmpdir, results)

        # Display file structure
        print("\n" + "="*70)
        print("FINAL FILE STRUCTURE")
        print("="*70)

        # Create a new provider for final structure demo
        memory = FileProvider()
        await memory.initialize({
            "base_path": str(tmpdir / "demo"),
            "session_id": "demo_session"
        })

        await memory.set("user:alice", "Alice", Scope.SESSION, tags=["user"])
        await memory.set("user:bob", "Bob", Scope.SESSION, tags=["user"])
        await memory.set("config:theme", "dark", Scope.PROJECT, tags=["config"])
        await memory.set("config:lang", "en", Scope.PROJECT, tags=["config"])
        await memory.set("api:key", "secret", Scope.GLOBAL, tags=["secret"])
        await memory.close()

        # Display structure
        demo_dir = tmpdir / "demo"
        for root, dirs, files in sorted(os.walk(demo_dir)):
            level = root.replace(str(demo_dir), '').count(os.sep)
            indent = '  ' * level
            rel_path = Path(root).relative_to(demo_dir)
            print(f"{indent}{rel_path}/")

            sub_indent = '  ' * (level + 1)
            for file in sorted(files):
                file_path = Path(root) / file
                size = file_path.stat().st_size
                print(f"{sub_indent}{file} ({size} bytes)")

        # Sample index content
        print("\n" + "="*70)
        print("SAMPLE INDEX FILE (_index.json)")
        print("="*70)
        index_path = demo_dir / "project" / "_index.json"
        if index_path.exists():
            with open(index_path) as f:
                index_data = json.load(f)
                print(json.dumps(index_data, indent=2))

        # Sample entry file
        print("\n" + "="*70)
        print("SAMPLE ENTRY FILE (config_theme.json)")
        print("="*70)
        entry_path = demo_dir / "project" / "config_theme.json"
        if entry_path.exists():
            with open(entry_path) as f:
                entry_data = json.load(f)
                print(json.dumps(entry_data, indent=2))

    # Final summary
    print()
    results.summary()

    # Performance observations
    print("\n" + "="*70)
    print("PERFORMANCE OBSERVATIONS")
    print("="*70)
    avg_time = sum(results.timings.values()) / len(results.timings) if results.timings else 0
    fastest = min(results.timings.items(), key=lambda x: x[1]) if results.timings else (None, 0)
    slowest = max(results.timings.items(), key=lambda x: x[1]) if results.timings else (None, 0)

    print(f"Average test time: {avg_time:.3f}s")
    print(f"Fastest test: {fastest[0]} ({fastest[1]:.3f}s)")
    print(f"Slowest test: {slowest[0]} ({slowest[1]:.3f}s)")
    print()

    return results.failed == 0


if __name__ == "__main__":
    import os
    success = asyncio.run(main())
    sys.exit(0 if success else 1)

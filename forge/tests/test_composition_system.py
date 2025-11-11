"""
Comprehensive test suite for Forge composition loading and validation system.
"""

import sys
from pathlib import Path
import tempfile
import shutil

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from forge.core.composition import (
    Composition,
    CompositionElements,
    CompositionSettings,
    CompositionLoader,
    LoadedComposition,
)
from forge.core.element import (
    Element,
    ElementType,
    ElementMetadata,
    ElementDependencies,
    ElementConflicts,
    ElementInterface,
    ElementLoader,
)


class TestResults:
    """Track test results."""

    def __init__(self):
        self.passed = []
        self.failed = []
        self.errors = []

    def record_pass(self, test_name: str, details: str = ""):
        self.passed.append((test_name, details))
        print(f"✓ PASS: {test_name}")
        if details:
            print(f"  {details}")

    def record_fail(self, test_name: str, reason: str):
        self.failed.append((test_name, reason))
        print(f"✗ FAIL: {test_name}")
        print(f"  Reason: {reason}")

    def record_error(self, test_name: str, error: Exception):
        self.errors.append((test_name, str(error)))
        print(f"✗ ERROR: {test_name}")
        print(f"  Error: {error}")

    def summary(self):
        total = len(self.passed) + len(self.failed) + len(self.errors)
        print("\n" + "=" * 80)
        print("TEST SUMMARY")
        print("=" * 80)
        print(f"Total Tests: {total}")
        print(f"Passed: {len(self.passed)} ({len(self.passed)/total*100:.1f}%)")
        print(f"Failed: {len(self.failed)}")
        print(f"Errors: {len(self.errors)}")
        print("=" * 80)
        return len(self.failed) == 0 and len(self.errors) == 0


def test_load_rapid_prototype(results: TestResults):
    """Test 1: Load the existing rapid-prototype preset."""
    print("\n" + "=" * 80)
    print("TEST 1: Load rapid-prototype composition")
    print("=" * 80)

    try:
        composition_path = (
            Path(__file__).parent.parent
            / "presets"
            / "rapid-prototype"
            / "composition.yaml"
        )

        if not composition_path.exists():
            results.record_fail(
                "Load rapid-prototype", f"File not found: {composition_path}"
            )
            return

        composition = Composition.load_from_file(composition_path)

        # Verify basic metadata
        assert composition.name == "rapid-prototype"
        assert composition.type == "preset"
        assert composition.version == "1.0.0"
        assert composition.description is not None

        results.record_pass(
            "Load rapid-prototype",
            f"Successfully loaded {composition.name} v{composition.version}",
        )

        # Verify elements
        assert len(composition.elements.principles) == 2
        assert "ruthless-minimalism" in composition.elements.principles
        assert "coevolution" in composition.elements.principles

        results.record_pass(
            "Parse principles", f"Found {len(composition.elements.principles)} principles"
        )

        # Verify settings
        assert composition.settings.memory.get("provider") == "file"
        assert composition.settings.agent_orchestration.get("mode") == "sequential"

        results.record_pass("Parse settings", "Memory and orchestration settings parsed")

        # Verify metadata
        assert "tags" in composition.metadata
        assert "rapid" in composition.metadata["tags"]

        results.record_pass("Parse metadata", f"Found {len(composition.metadata['tags'])} tags")

    except Exception as e:
        results.record_error("Load rapid-prototype", e)


def test_composition_serialization(results: TestResults):
    """Test 2: Test composition to_dict and from_dict."""
    print("\n" + "=" * 80)
    print("TEST 2: Composition serialization")
    print("=" * 80)

    try:
        # Create a composition
        elements = CompositionElements(
            principles=["test-principle-1", "test-principle-2"],
            tools=["test-tool"],
            hooks={"on_start": "init-hook"},
        )

        settings = CompositionSettings(
            memory={"provider": "memory"},
            agent_orchestration={"mode": "parallel"},
        )

        composition = Composition(
            name="test-composition",
            type="workflow",
            version="0.1.0",
            description="Test composition",
            elements=elements,
            settings=settings,
            metadata={"author": "test"},
        )

        # Convert to dict
        data = composition.to_dict()
        assert data["composition"]["name"] == "test-composition"
        assert len(data["elements"]["principles"]) == 2
        assert data["elements"]["hooks"]["on_start"] == "init-hook"

        results.record_pass("to_dict", "Composition serialized to dictionary")

        # Convert back from dict
        composition2 = Composition.from_dict(data)
        assert composition2.name == composition.name
        assert composition2.elements.principles == composition.elements.principles
        assert composition2.settings.memory == composition.settings.memory

        results.record_pass("from_dict", "Composition deserialized from dictionary")

        # Verify round-trip
        data2 = composition2.to_dict()
        assert data == data2

        results.record_pass("Round-trip", "Dictionary round-trip successful")

    except Exception as e:
        results.record_error("Composition serialization", e)


def test_element_loader(results: TestResults):
    """Test 3: Test ElementLoader with existing elements."""
    print("\n" + "=" * 80)
    print("TEST 3: ElementLoader")
    print("=" * 80)

    try:
        elements_path = Path(__file__).parent.parent / "elements"
        loader = ElementLoader([elements_path])

        # Load ruthless-minimalism principle
        element = loader.load("ruthless-minimalism", ElementType.PRINCIPLE)
        assert element.name == "ruthless-minimalism"
        assert element.type == ElementType.PRINCIPLE
        assert element.content is not None

        results.record_pass(
            "Load ruthless-minimalism",
            f"Loaded principle v{element.version}",
        )

        # Load coevolution principle
        element2 = loader.load("coevolution", ElementType.PRINCIPLE)
        assert element2.name == "coevolution"
        assert element2.type == ElementType.PRINCIPLE

        results.record_pass(
            "Load coevolution",
            f"Loaded principle v{element2.version}",
        )

        # Test cache
        element3 = loader.load("ruthless-minimalism", ElementType.PRINCIPLE)
        assert element3 is element  # Should be same object from cache

        results.record_pass("Cache", "Element caching working")

        # Test list elements
        principles = loader.list_elements(ElementType.PRINCIPLE)
        assert len(principles) >= 2

        results.record_pass(
            "List elements",
            f"Found {len(principles)} principle elements",
        )

    except Exception as e:
        results.record_error("ElementLoader", e)


def test_composition_loader_valid(results: TestResults):
    """Test 4: Test CompositionLoader with valid composition."""
    print("\n" + "=" * 80)
    print("TEST 4: CompositionLoader with valid composition")
    print("=" * 80)

    try:
        elements_path = Path(__file__).parent.parent / "elements"
        composition_path = (
            Path(__file__).parent.parent
            / "presets"
            / "rapid-prototype"
            / "composition.yaml"
        )

        element_loader = ElementLoader([elements_path])
        composition_loader = CompositionLoader(element_loader)

        # Load and resolve composition
        loaded = composition_loader.load(composition_path)
        assert isinstance(loaded, LoadedComposition)
        assert loaded.composition.name == "rapid-prototype"

        results.record_pass(
            "Load composition",
            f"Loaded composition with {len(loaded.elements)} elements",
        )

        # Verify elements are resolved
        assert len(loaded.elements) == 2  # Two principles

        results.record_pass(
            "Resolve elements",
            f"Resolved {len(loaded.elements)} elements",
        )

        # Get principles
        principles = loaded.get_principles()
        assert len(principles) == 2
        principle_names = [p.name for p in principles]
        assert "ruthless-minimalism" in principle_names
        assert "coevolution" in principle_names

        results.record_pass(
            "Get principles",
            f"Retrieved {len(principles)} principles",
        )

        # Get specific element
        rm = loaded.get_element("ruthless-minimalism", ElementType.PRINCIPLE)
        assert rm is not None
        assert rm.name == "ruthless-minimalism"

        results.record_pass(
            "Get specific element",
            "Retrieved ruthless-minimalism principle",
        )

    except Exception as e:
        results.record_error("CompositionLoader valid", e)


def test_invalid_dependencies(results: TestResults):
    """Test 5: Test composition with invalid dependencies."""
    print("\n" + "=" * 80)
    print("TEST 5: Invalid dependencies detection")
    print("=" * 80)

    temp_dir = None
    try:
        # Create temporary directory structure
        temp_dir = Path(tempfile.mkdtemp())
        elements_dir = temp_dir / "elements"
        compositions_dir = temp_dir / "compositions"
        elements_dir.mkdir()
        compositions_dir.mkdir()

        # Create a principle that depends on non-existent principle
        principle_dir = elements_dir / "principle" / "dependent-principle"
        principle_dir.mkdir(parents=True)

        principle = Element(
            metadata=ElementMetadata(
                name="dependent-principle",
                type=ElementType.PRINCIPLE,
                version="1.0.0",
                description="Principle with dependencies",
            ),
            dependencies=ElementDependencies(
                principles=["non-existent-principle"]
            ),
            content="# Dependent Principle\nDepends on something that doesn't exist.",
        )
        principle.save_to_file(principle_dir / "element.yaml")

        # Create composition that uses this principle
        composition = Composition(
            name="invalid-composition",
            type="workflow",
            version="1.0.0",
            description="Composition with invalid dependencies",
            elements=CompositionElements(
                principles=["dependent-principle"]
            ),
        )
        composition_path = compositions_dir / "composition.yaml"
        composition.save_to_file(composition_path)

        # Try to load with CompositionLoader
        element_loader = ElementLoader([elements_dir])
        composition_loader = CompositionLoader(element_loader)

        try:
            loaded = composition_loader.load(composition_path)
            results.record_fail(
                "Detect invalid dependencies",
                "Should have raised ValueError for missing dependencies",
            )
        except ValueError as e:
            if "dependencies" in str(e).lower():
                results.record_pass(
                    "Detect invalid dependencies",
                    f"Correctly detected missing dependency: {e}",
                )
            else:
                results.record_fail(
                    "Detect invalid dependencies",
                    f"Wrong error: {e}",
                )

    except Exception as e:
        results.record_error("Invalid dependencies", e)
    finally:
        if temp_dir and temp_dir.exists():
            shutil.rmtree(temp_dir)


def test_conflicting_elements(results: TestResults):
    """Test 6: Test composition with conflicting elements."""
    print("\n" + "=" * 80)
    print("TEST 6: Conflicting elements detection")
    print("=" * 80)

    temp_dir = None
    try:
        # Create temporary directory structure
        temp_dir = Path(tempfile.mkdtemp())
        elements_dir = temp_dir / "elements"
        compositions_dir = temp_dir / "compositions"
        elements_dir.mkdir()
        compositions_dir.mkdir()

        # Create two conflicting principles
        principle1_dir = elements_dir / "principle" / "principle-a"
        principle1_dir.mkdir(parents=True)

        principle1 = Element(
            metadata=ElementMetadata(
                name="principle-a",
                type=ElementType.PRINCIPLE,
                version="1.0.0",
                description="First principle",
            ),
            conflicts=ElementConflicts(
                principles=["principle-b"],
                reason="These principles are mutually exclusive",
            ),
            content="# Principle A",
        )
        principle1.save_to_file(principle1_dir / "element.yaml")

        principle2_dir = elements_dir / "principle" / "principle-b"
        principle2_dir.mkdir(parents=True)

        principle2 = Element(
            metadata=ElementMetadata(
                name="principle-b",
                type=ElementType.PRINCIPLE,
                version="1.0.0",
                description="Second principle",
            ),
            content="# Principle B",
        )
        principle2.save_to_file(principle2_dir / "element.yaml")

        # Create composition that uses both conflicting principles
        composition = Composition(
            name="conflicting-composition",
            type="workflow",
            version="1.0.0",
            description="Composition with conflicting elements",
            elements=CompositionElements(
                principles=["principle-a", "principle-b"]
            ),
        )
        composition_path = compositions_dir / "composition.yaml"
        composition.save_to_file(composition_path)

        # Try to load with CompositionLoader
        element_loader = ElementLoader([elements_dir])
        composition_loader = CompositionLoader(element_loader)

        try:
            loaded = composition_loader.load(composition_path)
            results.record_fail(
                "Detect conflicts",
                "Should have raised ValueError for conflicting elements",
            )
        except ValueError as e:
            if "conflict" in str(e).lower():
                results.record_pass(
                    "Detect conflicts",
                    f"Correctly detected conflict: {e}",
                )
            else:
                results.record_fail(
                    "Detect conflicts",
                    f"Wrong error: {e}",
                )

    except Exception as e:
        results.record_error("Conflicting elements", e)
    finally:
        if temp_dir and temp_dir.exists():
            shutil.rmtree(temp_dir)


def test_save_and_reload(results: TestResults):
    """Test 7: Test saving and reloading compositions."""
    print("\n" + "=" * 80)
    print("TEST 7: Save and reload composition")
    print("=" * 80)

    temp_dir = None
    try:
        # Create temporary directory
        temp_dir = Path(tempfile.mkdtemp())
        composition_path = temp_dir / "test-composition.yaml"

        # Create a composition
        elements = CompositionElements(
            principles=["test-principle"],
            tools=["tool-1", "tool-2"],
            agents=["agent-1"],
            hooks={"on_start": "init-hook", "on_end": "cleanup-hook"},
            queries=["query-1"],
        )

        settings = CompositionSettings(
            memory={
                "provider": "file",
                "config": {"path": ".forge/memory"},
            },
            agent_orchestration={
                "mode": "parallel",
                "max_parallel": 5,
            },
            tool_defaults={
                "tool-1": {"timeout": 30},
                "tool-2": {"retries": 3},
            },
        )

        composition = Composition(
            name="test-composition",
            type="workflow",
            version="2.1.0",
            description="A test composition for validation",
            elements=elements,
            settings=settings,
            metadata={
                "author": "test-suite",
                "tags": ["test", "validation"],
                "license": "MIT",
            },
        )

        # Save composition
        composition.save_to_file(composition_path)
        assert composition_path.exists()

        results.record_pass("Save composition", f"Saved to {composition_path}")

        # Reload composition
        loaded = Composition.load_from_file(composition_path)

        # Verify all fields
        assert loaded.name == composition.name
        assert loaded.type == composition.type
        assert loaded.version == composition.version
        assert loaded.description == composition.description

        results.record_pass("Reload composition", "Basic metadata matches")

        # Verify elements
        assert loaded.elements.principles == composition.elements.principles
        assert loaded.elements.tools == composition.elements.tools
        assert loaded.elements.agents == composition.elements.agents
        assert loaded.elements.hooks == composition.elements.hooks
        assert loaded.elements.queries == composition.elements.queries

        results.record_pass("Verify elements", "All elements preserved")

        # Verify settings
        assert loaded.settings.memory == composition.settings.memory
        assert (
            loaded.settings.agent_orchestration
            == composition.settings.agent_orchestration
        )
        assert loaded.settings.tool_defaults == composition.settings.tool_defaults

        results.record_pass("Verify settings", "All settings preserved")

        # Verify metadata
        assert loaded.metadata == composition.metadata

        results.record_pass("Verify metadata", "All metadata preserved")

        # Test get_all_element_names
        element_names = loaded.get_all_element_names()
        assert len(element_names) == 7  # 1 principle + 2 tools + 1 agent + 2 hooks + 1 query

        principle_count = sum(1 for t, n in element_names if t == ElementType.PRINCIPLE)
        tool_count = sum(1 for t, n in element_names if t == ElementType.TOOL)
        agent_count = sum(1 for t, n in element_names if t == ElementType.AGENT)
        hook_count = sum(1 for t, n in element_names if t == ElementType.HOOK)
        query_count = sum(1 for t, n in element_names if t == ElementType.QUERY)

        assert principle_count == 1
        assert tool_count == 2
        assert agent_count == 1
        assert hook_count == 2
        assert query_count == 1

        results.record_pass(
            "get_all_element_names",
            f"Found {len(element_names)} elements correctly categorized",
        )

    except Exception as e:
        results.record_error("Save and reload", e)
    finally:
        if temp_dir and temp_dir.exists():
            shutil.rmtree(temp_dir)


def test_valid_with_dependencies(results: TestResults):
    """Test 8: Test composition with valid dependencies."""
    print("\n" + "=" * 80)
    print("TEST 8: Valid dependencies resolution")
    print("=" * 80)

    temp_dir = None
    try:
        # Create temporary directory structure
        temp_dir = Path(tempfile.mkdtemp())
        elements_dir = temp_dir / "elements"
        compositions_dir = temp_dir / "compositions"
        elements_dir.mkdir()
        compositions_dir.mkdir()

        # Create base principle
        base_principle_dir = elements_dir / "principle" / "base-principle"
        base_principle_dir.mkdir(parents=True)

        base_principle = Element(
            metadata=ElementMetadata(
                name="base-principle",
                type=ElementType.PRINCIPLE,
                version="1.0.0",
                description="Base principle with no dependencies",
            ),
            content="# Base Principle\nFundamental principle.",
        )
        base_principle.save_to_file(base_principle_dir / "element.yaml")

        # Create dependent principle
        dependent_principle_dir = elements_dir / "principle" / "dependent-principle"
        dependent_principle_dir.mkdir(parents=True)

        dependent_principle = Element(
            metadata=ElementMetadata(
                name="dependent-principle",
                type=ElementType.PRINCIPLE,
                version="1.0.0",
                description="Principle with valid dependencies",
            ),
            dependencies=ElementDependencies(
                principles=["base-principle"]
            ),
            content="# Dependent Principle\nBuilds on base-principle.",
        )
        dependent_principle.save_to_file(dependent_principle_dir / "element.yaml")

        # Create composition that includes both
        composition = Composition(
            name="valid-composition",
            type="workflow",
            version="1.0.0",
            description="Composition with valid dependencies",
            elements=CompositionElements(
                principles=["base-principle", "dependent-principle"]
            ),
        )
        composition_path = compositions_dir / "composition.yaml"
        composition.save_to_file(composition_path)

        # Load with CompositionLoader - should succeed
        element_loader = ElementLoader([elements_dir])
        composition_loader = CompositionLoader(element_loader)

        loaded = composition_loader.load(composition_path)
        assert isinstance(loaded, LoadedComposition)
        assert len(loaded.elements) == 2

        results.record_pass(
            "Valid dependencies",
            f"Successfully resolved {len(loaded.elements)} elements with dependencies",
        )

        # Verify both principles are loaded
        principles = loaded.get_principles()
        assert len(principles) == 2
        principle_names = [p.name for p in principles]
        assert "base-principle" in principle_names
        assert "dependent-principle" in principle_names

        results.record_pass(
            "Verify resolved elements",
            "Both base and dependent principles loaded",
        )

    except Exception as e:
        results.record_error("Valid dependencies", e)
    finally:
        if temp_dir and temp_dir.exists():
            shutil.rmtree(temp_dir)


def test_missing_element_in_composition(results: TestResults):
    """Test 9: Test composition referencing non-existent element."""
    print("\n" + "=" * 80)
    print("TEST 9: Missing element detection")
    print("=" * 80)

    temp_dir = None
    try:
        # Create temporary directory structure
        temp_dir = Path(tempfile.mkdtemp())
        elements_dir = temp_dir / "elements"
        compositions_dir = temp_dir / "compositions"
        elements_dir.mkdir()
        compositions_dir.mkdir()

        # Create composition referencing non-existent element
        composition = Composition(
            name="invalid-refs-composition",
            type="workflow",
            version="1.0.0",
            description="Composition with missing element references",
            elements=CompositionElements(
                principles=["non-existent-principle"],
                tools=["non-existent-tool"],
            ),
        )
        composition_path = compositions_dir / "composition.yaml"
        composition.save_to_file(composition_path)

        # Try to load with CompositionLoader
        element_loader = ElementLoader([elements_dir])
        composition_loader = CompositionLoader(element_loader)

        try:
            loaded = composition_loader.load(composition_path)
            results.record_fail(
                "Detect missing elements",
                "Should have raised ValueError for missing elements",
            )
        except ValueError as e:
            if "not found" in str(e).lower():
                results.record_pass(
                    "Detect missing elements",
                    f"Correctly detected missing element: {e}",
                )
            else:
                results.record_fail(
                    "Detect missing elements",
                    f"Wrong error: {e}",
                )

    except Exception as e:
        results.record_error("Missing element detection", e)
    finally:
        if temp_dir and temp_dir.exists():
            shutil.rmtree(temp_dir)


def test_complex_composition(results: TestResults):
    """Test 10: Test complex composition with multiple element types."""
    print("\n" + "=" * 80)
    print("TEST 10: Complex composition")
    print("=" * 80)

    temp_dir = None
    try:
        # Create temporary directory structure
        temp_dir = Path(tempfile.mkdtemp())
        elements_dir = temp_dir / "elements"
        compositions_dir = temp_dir / "compositions"
        elements_dir.mkdir()
        compositions_dir.mkdir()

        # Create various elements

        # Principle
        principle_dir = elements_dir / "principle" / "test-principle"
        principle_dir.mkdir(parents=True)
        principle = Element(
            metadata=ElementMetadata(
                name="test-principle",
                type=ElementType.PRINCIPLE,
                version="1.0.0",
            ),
            content="# Test Principle",
        )
        principle.save_to_file(principle_dir / "element.yaml")

        # Tool
        tool_dir = elements_dir / "tool" / "test-tool"
        tool_dir.mkdir(parents=True)
        tool = Element(
            metadata=ElementMetadata(
                name="test-tool",
                type=ElementType.TOOL,
                version="1.0.0",
            ),
            implementation={"type": "function", "handler": "test_handler"},
        )
        tool.save_to_file(tool_dir / "element.yaml")

        # Agent
        agent_dir = elements_dir / "agent" / "test-agent"
        agent_dir.mkdir(parents=True)
        agent = Element(
            metadata=ElementMetadata(
                name="test-agent",
                type=ElementType.AGENT,
                version="1.0.0",
            ),
            dependencies=ElementDependencies(
                tools=["test-tool"],
                principles=["test-principle"],
            ),
            interface=ElementInterface(role="coordinator"),
        )
        agent.save_to_file(agent_dir / "element.yaml")

        # Hook
        hook_dir = elements_dir / "hook" / "test-hook"
        hook_dir.mkdir(parents=True)
        hook = Element(
            metadata=ElementMetadata(
                name="test-hook",
                type=ElementType.HOOK,
                version="1.0.0",
            ),
            interface=ElementInterface(events=["on_start"]),
        )
        hook.save_to_file(hook_dir / "element.yaml")

        # Create complex composition
        composition = Composition(
            name="complex-composition",
            type="workflow",
            version="1.0.0",
            description="Complex composition with multiple element types",
            elements=CompositionElements(
                principles=["test-principle"],
                tools=["test-tool"],
                agents=["test-agent"],
                hooks={"on_start": "test-hook"},
            ),
        )
        composition_path = compositions_dir / "composition.yaml"
        composition.save_to_file(composition_path)

        # Load with CompositionLoader
        element_loader = ElementLoader([elements_dir])
        composition_loader = CompositionLoader(element_loader)

        loaded = composition_loader.load(composition_path)
        assert isinstance(loaded, LoadedComposition)

        results.record_pass(
            "Load complex composition",
            f"Loaded composition with {len(loaded.elements)} elements",
        )

        # Verify each type
        principles = loaded.get_principles()
        assert len(principles) == 1
        assert principles[0].name == "test-principle"

        tools = loaded.get_tools()
        assert len(tools) == 1
        assert tools[0].name == "test-tool"

        agents = loaded.get_agents()
        assert len(agents) == 1
        assert agents[0].name == "test-agent"

        hooks = loaded.get_hooks()
        assert len(hooks) == 1
        assert "on_start" in hooks
        assert hooks["on_start"].name == "test-hook"

        results.record_pass(
            "Verify all element types",
            "All element types (principles, tools, agents, hooks) loaded correctly",
        )

        # Verify agent dependencies are satisfied
        agent_elem = loaded.get_element("test-agent", ElementType.AGENT)
        assert agent_elem is not None
        assert "test-tool" in agent_elem.dependencies.tools
        assert "test-principle" in agent_elem.dependencies.principles

        results.record_pass(
            "Verify dependencies",
            "Agent dependencies correctly satisfied",
        )

    except Exception as e:
        results.record_error("Complex composition", e)
    finally:
        if temp_dir and temp_dir.exists():
            shutil.rmtree(temp_dir)


def main():
    """Run all tests."""
    print("=" * 80)
    print("FORGE COMPOSITION SYSTEM TEST SUITE")
    print("=" * 80)

    results = TestResults()

    # Run all tests
    test_load_rapid_prototype(results)
    test_composition_serialization(results)
    test_element_loader(results)
    test_composition_loader_valid(results)
    test_invalid_dependencies(results)
    test_conflicting_elements(results)
    test_save_and_reload(results)
    test_valid_with_dependencies(results)
    test_missing_element_in_composition(results)
    test_complex_composition(results)

    # Print summary
    success = results.summary()

    return 0 if success else 1


if __name__ == "__main__":
    exit(main())

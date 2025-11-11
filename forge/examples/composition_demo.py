"""
Demonstration of Forge composition system usage.

This script shows practical examples of:
- Loading compositions from files
- Creating compositions programmatically
- Working with loaded compositions
- Accessing elements by type
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from forge.core.composition import (
    Composition,
    CompositionElements,
    CompositionSettings,
    CompositionLoader,
)
from forge.core.element import ElementType, ElementLoader


def demo_load_preset():
    """Demonstrate loading the rapid-prototype preset."""
    print("=" * 80)
    print("DEMO 1: Loading rapid-prototype preset")
    print("=" * 80)

    # Setup paths
    elements_path = Path(__file__).parent.parent / "elements"
    preset_path = (
        Path(__file__).parent.parent
        / "presets"
        / "rapid-prototype"
        / "composition.yaml"
    )

    # Load composition
    element_loader = ElementLoader([elements_path])
    composition_loader = CompositionLoader(element_loader)

    loaded = composition_loader.load(preset_path)

    print(f"\nComposition: {loaded.composition.name}")
    print(f"Type: {loaded.composition.type}")
    print(f"Version: {loaded.composition.version}")
    print(f"Description: {loaded.composition.description}")

    # Get principles
    principles = loaded.get_principles()
    print(f"\nPrinciples ({len(principles)}):")
    for principle in principles:
        print(f"  - {principle.name} v{principle.version}")
        print(f"    {principle.metadata.description}")
        if principle.dependencies.suggests:
            print(f"    Suggests: {', '.join(principle.dependencies.suggests)}")
        if principle.conflicts.principles:
            print(f"    Conflicts: {', '.join(principle.conflicts.principles)}")

    # Settings
    print(f"\nSettings:")
    print(f"  Memory Provider: {loaded.composition.settings.memory.get('provider')}")
    print(
        f"  Orchestration Mode: {loaded.composition.settings.agent_orchestration.get('mode')}"
    )

    # Metadata tags
    print(f"\nTags: {', '.join(loaded.composition.metadata.get('tags', []))}")


def demo_create_composition():
    """Demonstrate creating a composition programmatically."""
    print("\n" + "=" * 80)
    print("DEMO 2: Creating composition programmatically")
    print("=" * 80)

    # Create composition elements
    elements = CompositionElements(
        principles=["test-driven-development", "clean-architecture"],
        tools=["linter", "formatter", "test-runner"],
        agents=["code-reviewer", "documentation-generator"],
        hooks={
            "on_start": "setup-environment",
            "on_test": "coverage-reporter",
            "on_commit": "pre-commit-checks",
        },
        queries=["find-todos", "analyze-complexity"],
    )

    # Create settings
    settings = CompositionSettings(
        memory={
            "provider": "file",
            "config": {
                "base_path": ".forge/memory",
                "compression": True,
                "retention_days": 30,
            },
        },
        agent_orchestration={
            "mode": "parallel",
            "max_parallel": 5,
            "timeout_seconds": 300,
        },
        tool_defaults={
            "linter": {"strict": True, "auto_fix": False},
            "formatter": {"line_length": 88},
            "test-runner": {"coverage_threshold": 80},
        },
    )

    # Create composition
    composition = Composition(
        name="quality-assurance",
        type="workflow",
        version="1.0.0",
        description="Comprehensive quality assurance workflow with TDD and clean architecture",
        elements=elements,
        settings=settings,
        metadata={
            "author": "development-team",
            "tags": ["quality", "tdd", "architecture", "automation"],
            "license": "MIT",
            "recommended_for": [
                "Production applications",
                "Team projects",
                "Quality-critical systems",
            ],
        },
    )

    # Display composition
    print(f"\nCreated Composition: {composition.name}")
    print(f"Type: {composition.type}")
    print(f"Version: {composition.version}")

    print(f"\nElements:")
    print(f"  Principles: {len(composition.elements.principles)}")
    print(f"  Tools: {len(composition.elements.tools)}")
    print(f"  Agents: {len(composition.elements.agents)}")
    print(f"  Hooks: {len(composition.elements.hooks)}")
    print(f"  Queries: {len(composition.elements.queries)}")

    # Get all element names with types
    all_elements = composition.get_all_element_names()
    print(f"\nAll Elements ({len(all_elements)}):")
    for element_type, element_name in all_elements:
        print(f"  - {element_type.value}: {element_name}")

    # Convert to dictionary for inspection
    data = composition.to_dict()
    print(f"\nSerialized to dictionary with {len(data)} top-level keys")
    print(f"Keys: {', '.join(data.keys())}")

    return composition


def demo_save_and_load():
    """Demonstrate saving and loading compositions."""
    print("\n" + "=" * 80)
    print("DEMO 3: Save and reload composition")
    print("=" * 80)

    import tempfile

    # Create a simple composition
    composition = Composition(
        name="demo-composition",
        type="preset",
        version="0.1.0",
        description="Demo composition for save/load example",
        elements=CompositionElements(
            principles=["simplicity", "clarity"],
            tools=["analyzer"],
        ),
        settings=CompositionSettings(
            memory={"provider": "memory"},
        ),
    )

    # Save to temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        temp_path = Path(f.name)

    composition.save_to_file(temp_path)
    print(f"Saved composition to: {temp_path}")

    # Load it back
    loaded = Composition.load_from_file(temp_path)
    print(f"\nReloaded composition: {loaded.name}")
    print(f"Elements match: {loaded.elements.principles == composition.elements.principles}")
    print(f"Settings match: {loaded.settings.memory == composition.settings.memory}")

    # Clean up
    temp_path.unlink()
    print(f"\nCleaned up temporary file")


def demo_element_access():
    """Demonstrate different ways to access elements."""
    print("\n" + "=" * 80)
    print("DEMO 4: Accessing elements from loaded composition")
    print("=" * 80)

    # Setup
    elements_path = Path(__file__).parent.parent / "elements"
    preset_path = (
        Path(__file__).parent.parent
        / "presets"
        / "rapid-prototype"
        / "composition.yaml"
    )

    element_loader = ElementLoader([elements_path])
    composition_loader = CompositionLoader(element_loader)
    loaded = composition_loader.load(preset_path)

    print(f"Loaded composition: {loaded.composition.name}")
    print(f"Total elements: {len(loaded.elements)}")

    # Access by type
    print("\n1. Get all principles:")
    principles = loaded.get_principles()
    for p in principles:
        print(f"   - {p.name}: {p.metadata.description}")

    # Access specific element
    print("\n2. Get specific element:")
    rm = loaded.get_element("ruthless-minimalism", ElementType.PRINCIPLE)
    if rm:
        print(f"   Found: {rm.name}")
        print(f"   Tags: {', '.join(rm.metadata.tags)}")
        print(f"   Suggests: {', '.join(rm.dependencies.suggests)}")

    # Access all element types
    print("\n3. Element counts by type:")
    print(f"   Principles: {len(loaded.get_principles())}")
    print(f"   Constitutions: {len(loaded.get_constitutions())}")
    print(f"   Tools: {len(loaded.get_tools())}")
    print(f"   Agents: {len(loaded.get_agents())}")
    print(f"   Hooks: {len(loaded.get_hooks())}")
    print(f"   Templates: {len(loaded.get_templates())}")

    # Access raw elements dictionary
    print("\n4. Raw elements dictionary:")
    for key, element in loaded.elements.items():
        print(f"   {key} -> {element.name} v{element.version}")


def main():
    """Run all demonstrations."""
    print("\n")
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 20 + "FORGE COMPOSITION SYSTEM DEMO" + " " * 29 + "║")
    print("╚" + "=" * 78 + "╝")

    try:
        # Run demos
        demo_load_preset()
        demo_create_composition()
        demo_save_and_load()
        demo_element_access()

        print("\n" + "=" * 80)
        print("All demonstrations completed successfully!")
        print("=" * 80)

    except Exception as e:
        print(f"\nError during demonstration: {e}")
        import traceback

        traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    exit(main())

#!/usr/bin/env python3
"""
Test custom Forge composition creation and interaction.

This script creates a custom composition from scratch, saves it,
reloads it, and tests all composition features including:
- Principles
- Memory (file-based)
- Context interaction
- Validation and integrity
"""

import asyncio
import sys
import tempfile
import shutil
from pathlib import Path
from typing import Dict, Any

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from forge.core.composition import (
    Composition,
    CompositionElements,
    CompositionSettings,
    CompositionLoader,
)
from forge.core.element import ElementLoader, ElementType
from forge.core.context import Context
from forge.memory.file_provider import FileProvider
from forge.memory.protocol import Scope


class TestResults:
    """Track test results."""

    def __init__(self):
        self.results = []
        self.failures = 0
        self.successes = 0

    def add(self, test_name: str, passed: bool, details: str = ""):
        """Add test result."""
        status = "✓ PASS" if passed else "✗ FAIL"
        self.results.append(f"{status}: {test_name}")
        if details:
            self.results.append(f"  └─ {details}")

        if passed:
            self.successes += 1
        else:
            self.failures += 1

    def print_results(self):
        """Print all results."""
        print("\n" + "=" * 80)
        print("TEST RESULTS")
        print("=" * 80)
        for result in self.results:
            print(result)
        print("\n" + "-" * 80)
        print(f"Total: {self.successes + self.failures} | "
              f"Passed: {self.successes} | Failed: {self.failures}")
        print("=" * 80)


async def main():
    """Run comprehensive composition test."""

    results = TestResults()
    temp_dir = None

    try:
        # Setup
        print("=" * 80)
        print("FORGE CUSTOM COMPOSITION TEST")
        print("=" * 80)

        # Get paths
        forge_dir = Path(__file__).parent
        elements_dir = forge_dir / "elements"
        temp_dir = Path(tempfile.mkdtemp(prefix="forge-test-"))

        print(f"\n📁 Forge directory: {forge_dir}")
        print(f"📁 Test directory: {temp_dir}")

        # =====================================================================
        # STEP 1: Create Custom Composition
        # =====================================================================
        print("\n" + "=" * 80)
        print("STEP 1: Creating Custom Composition")
        print("=" * 80)

        # Create composition with both principles and file-based memory
        composition = Composition(
            name="test-composition",
            type="preset",
            version="1.0.0",
            description="Custom test composition with both principles and file memory",
            elements=CompositionElements(
                principles=["ruthless-minimalism", "coevolution"],
                constitutions=[],
                tools=[],
                agents=[],
                templates=[],
                hooks={},
                queries=[],
            ),
            settings=CompositionSettings(
                memory={
                    "provider": "file",
                    "config": {
                        "base_path": str(temp_dir / ".forge" / "memory"),
                        "compression": False,
                    },
                },
                agent_orchestration={
                    "mode": "sequential",
                    "max_parallel": 2,
                },
                tool_defaults={},
            ),
            metadata={
                "description": "Test composition for validation",
                "author": "test-suite",
                "tags": ["test", "custom", "minimalism", "coevolution"],
                "recommended_for": [
                    "Testing composition system",
                    "Validating element loading",
                    "Memory integration testing",
                ],
                "use_cases": {
                    "primary": "End-to-end composition testing",
                    "secondary": "Flexibility demonstration",
                },
            },
        )

        # Convert to dict for display
        comp_dict = composition.to_dict()
        print("\n📝 Composition structure:")
        print(f"  Name: {comp_dict['composition']['name']}")
        print(f"  Type: {comp_dict['composition']['type']}")
        print(f"  Version: {comp_dict['composition']['version']}")
        print(f"  Principles: {comp_dict['elements']['principles']}")
        print(f"  Memory provider: {comp_dict['settings']['memory']['provider']}")

        results.add(
            "Create composition object",
            True,
            f"Created {composition.name} v{composition.version}",
        )

        # =====================================================================
        # STEP 2: Save Composition to File
        # =====================================================================
        print("\n" + "=" * 80)
        print("STEP 2: Saving Composition to File")
        print("=" * 80)

        composition_file = temp_dir / "composition.yaml"
        composition.save_to_file(composition_file)

        print(f"\n💾 Saved to: {composition_file}")
        print(f"   File exists: {composition_file.exists()}")
        print(f"   File size: {composition_file.stat().st_size} bytes")

        results.add(
            "Save composition to file",
            composition_file.exists(),
            f"Saved to {composition_file}",
        )

        # Display YAML content
        print("\n📄 Composition YAML content:")
        print("-" * 80)
        with open(composition_file, "r") as f:
            yaml_content = f.read()
            print(yaml_content)
        print("-" * 80)

        # =====================================================================
        # STEP 3: Reload and Validate Composition
        # =====================================================================
        print("\n" + "=" * 80)
        print("STEP 3: Reloading and Validating Composition")
        print("=" * 80)

        # Load from file
        reloaded_composition = Composition.load_from_file(composition_file)

        print(f"\n✓ Reloaded composition: {reloaded_composition.name}")
        print(f"  Principles: {reloaded_composition.elements.principles}")
        print(f"  Settings: {list(reloaded_composition.settings.memory.keys())}")

        # Validate integrity
        integrity_checks = {
            "name": reloaded_composition.name == composition.name,
            "version": reloaded_composition.version == composition.version,
            "principles": (
                reloaded_composition.elements.principles
                == composition.elements.principles
            ),
            "memory_provider": (
                reloaded_composition.settings.memory.get("provider")
                == composition.settings.memory.get("provider")
            ),
            "metadata_tags": (
                reloaded_composition.metadata.get("tags")
                == composition.metadata.get("tags")
            ),
        }

        all_checks_passed = all(integrity_checks.values())
        print("\n🔍 Integrity checks:")
        for check, passed in integrity_checks.items():
            status = "✓" if passed else "✗"
            print(f"  {status} {check}: {passed}")

        results.add(
            "Reload composition from file",
            True,
            f"Successfully reloaded {reloaded_composition.name}",
        )
        results.add(
            "Validate composition integrity",
            all_checks_passed,
            f"{sum(integrity_checks.values())}/{len(integrity_checks)} checks passed",
        )

        # =====================================================================
        # STEP 4: Load Elements and Create Context
        # =====================================================================
        print("\n" + "=" * 80)
        print("STEP 4: Loading Elements and Creating Context")
        print("=" * 80)

        # Initialize element loader
        element_loader = ElementLoader(search_paths=[elements_dir])
        composition_loader = CompositionLoader(element_loader)

        # Load composition with elements
        print("\n📦 Loading elements...")
        loaded_composition = composition_loader.load(composition_file)

        print(f"✓ Loaded {len(loaded_composition.elements)} elements:")
        for key, element in loaded_composition.elements.items():
            print(f"  - {key}: {element.metadata.description}")

        results.add(
            "Load elements",
            len(loaded_composition.elements) == 2,
            f"Loaded {len(loaded_composition.elements)} principle elements",
        )

        # Initialize memory provider
        print("\n💾 Initializing file-based memory provider...")
        memory = FileProvider()
        await memory.initialize(
            {
                "base_path": str(temp_dir / ".forge" / "memory"),
                "session_id": "test-session-001",
            }
        )

        results.add("Initialize memory provider", True, "FileProvider initialized")

        # Create context
        context = Context(
            memory=memory,
            composition=loaded_composition,
            project_path=temp_dir,
            session_id="test-session-001",
        )

        print(f"✓ Context created with session: {context.session_id}")

        results.add("Create context", True, f"Context with session {context.session_id}")

        # =====================================================================
        # STEP 5: Test Context - Access Principles
        # =====================================================================
        print("\n" + "=" * 80)
        print("STEP 5: Testing Context - Access Principles")
        print("=" * 80)

        # List principles
        principles_list = context.principles.list()
        print(f"\n📋 Available principles: {principles_list}")

        # Get principle content
        for principle_name in principles_list:
            content = await context.principles.get(principle_name)
            status = "✓" if content is not None else "✗"
            print(f"\n{status} Principle: {principle_name}")
            if content:
                print(f"  Content: {content[:100] if len(content) > 100 else content}...")

        results.add(
            "List principles",
            len(principles_list) == 2,
            f"Found {len(principles_list)} principles",
        )

        # Verify both principles are accessible
        minimalism = await context.principles.get("ruthless-minimalism")
        coevolution = await context.principles.get("coevolution")

        results.add(
            "Access ruthless-minimalism principle",
            minimalism is not None,  # Content should exist (.md file)
            f"Principle loaded ({len(minimalism) if minimalism else 0} chars)" if minimalism else "No content",
        )
        results.add(
            "Access coevolution principle",
            coevolution is not None,  # Content should exist (.md file)
            f"Principle loaded ({len(coevolution) if coevolution else 0} chars)" if coevolution else "No content",
        )

        # =====================================================================
        # STEP 6: Test Context - Memory Operations
        # =====================================================================
        print("\n" + "=" * 80)
        print("STEP 6: Testing Context - Memory Operations")
        print("=" * 80)

        # Test SESSION scope
        print("\n📝 Testing SESSION scope memory...")
        await context.memory.set(
            "test:session:key1",
            "Session value 1",
            Scope.SESSION,
            tags=["test", "session"],
            metadata={"type": "test", "index": 1},
        )
        await context.memory.set(
            "test:session:key2",
            "Session value 2",
            Scope.SESSION,
            tags=["test", "session"],
        )

        session_entry = await context.memory.get("test:session:key1", Scope.SESSION)
        print(f"  ✓ Stored and retrieved: {session_entry.key} = {session_entry.value}")

        results.add(
            "Store/retrieve SESSION memory",
            session_entry is not None and session_entry.value == "Session value 1",
            f"Key: {session_entry.key if session_entry else 'None'}",
        )

        # Test PROJECT scope
        print("\n📝 Testing PROJECT scope memory...")
        await context.memory.set(
            "project:config:theme",
            "dark-mode",
            Scope.PROJECT,
            tags=["config", "ui"],
            metadata={"category": "appearance"},
        )

        project_entry = await context.memory.get("project:config:theme", Scope.PROJECT)
        print(f"  ✓ Stored and retrieved: {project_entry.key} = {project_entry.value}")

        results.add(
            "Store/retrieve PROJECT memory",
            project_entry is not None and project_entry.value == "dark-mode",
            f"Key: {project_entry.key if project_entry else 'None'}",
        )

        # Test GLOBAL scope
        print("\n📝 Testing GLOBAL scope memory...")
        await context.memory.set(
            "global:user:preference",
            "minimalist-workflow",
            Scope.GLOBAL,
            tags=["global", "user"],
        )

        global_entry = await context.memory.get("global:user:preference", Scope.GLOBAL)
        print(f"  ✓ Stored and retrieved: {global_entry.key} = {global_entry.value}")

        results.add(
            "Store/retrieve GLOBAL memory",
            global_entry is not None and global_entry.value == "minimalist-workflow",
            f"Key: {global_entry.key if global_entry else 'None'}",
        )

        # =====================================================================
        # STEP 7: Test Memory Queries
        # =====================================================================
        print("\n" + "=" * 80)
        print("STEP 7: Testing Memory Queries")
        print("=" * 80)

        # Query by pattern
        print("\n🔍 Query by pattern: 'test:session:*'")
        session_entries = await context.memory.query("test:session:*", Scope.SESSION)
        print(f"  Found {len(session_entries)} entries:")
        for entry in session_entries:
            print(f"    - {entry.key}: {entry.value}")

        results.add(
            "Query by pattern",
            len(session_entries) == 2,
            f"Found {len(session_entries)} entries matching 'test:session:*'",
        )

        # Query by tag
        print("\n🔍 Query by tag: 'tag:test'")
        tagged_entries = await context.memory.query("tag:test", Scope.SESSION)
        print(f"  Found {len(tagged_entries)} entries with tag 'test':")
        for entry in tagged_entries:
            print(f"    - {entry.key}: {entry.value} (tags: {entry.tags})")

        results.add(
            "Query by tag",
            len(tagged_entries) == 2,
            f"Found {len(tagged_entries)} entries with tag 'test'",
        )

        # =====================================================================
        # STEP 8: Verify Composition Elements
        # =====================================================================
        print("\n" + "=" * 80)
        print("STEP 8: Verifying All Composition Elements")
        print("=" * 80)

        # Check principles
        principles = loaded_composition.get_principles()
        print(f"\n✓ Principles ({len(principles)}):")
        for principle in principles:
            print(f"  - {principle.name} (v{principle.version})")
            print(f"    Description: {principle.metadata.description}")
            print(f"    Tags: {', '.join(principle.metadata.tags)}")

        results.add(
            "Verify all principles loaded",
            len(principles) == 2,
            f"{len(principles)} principles available",
        )

        # Check memory configuration
        memory_config = loaded_composition.composition.settings.memory
        print(f"\n✓ Memory configuration:")
        print(f"  Provider: {memory_config.get('provider')}")
        print(f"  Config: {memory_config.get('config')}")

        results.add(
            "Verify memory configuration",
            memory_config.get("provider") == "file",
            f"Provider: {memory_config.get('provider')}",
        )

        # =====================================================================
        # STEP 9: Test End-to-End Workflow
        # =====================================================================
        print("\n" + "=" * 80)
        print("STEP 9: Testing End-to-End Workflow")
        print("=" * 80)

        # Simulate a workflow using the composition
        print("\n🔄 Simulating workflow...")

        # Step 1: Store design decision (aligned with ruthless-minimalism)
        await context.memory.set(
            "decision:001",
            "Start with simplest implementation, defer optimization",
            Scope.PROJECT,
            tags=["decision", "minimalism"],
            metadata={"principle": "ruthless-minimalism", "priority": "high"},
        )

        # Step 2: Store coevolution note
        await context.memory.set(
            "coevolution:note:001",
            "Code revealed need for simpler API - updating spec accordingly",
            Scope.PROJECT,
            tags=["coevolution", "spec"],
            metadata={"principle": "coevolution", "iteration": 1},
        )

        # Step 3: Query all decisions
        decisions = await context.memory.query("decision:*", Scope.PROJECT)
        coevolution_notes = await context.memory.query(
            "coevolution:note:*", Scope.PROJECT
        )

        print(f"  ✓ Stored {len(decisions)} design decision(s)")
        print(f"  ✓ Stored {len(coevolution_notes)} coevolution note(s)")

        workflow_successful = len(decisions) == 1 and len(coevolution_notes) == 1

        results.add(
            "End-to-end workflow test",
            workflow_successful,
            f"Workflow completed: {len(decisions) + len(coevolution_notes)} entries created",
        )

        # =====================================================================
        # STEP 10: Composition Flexibility Test
        # =====================================================================
        print("\n" + "=" * 80)
        print("STEP 10: Testing Composition Flexibility")
        print("=" * 80)

        # Demonstrate that composition can be modified
        print("\n🔧 Testing composition modifications...")

        # Create a modified version
        modified_composition = Composition.from_dict(composition.to_dict())
        modified_composition.metadata["tags"].append("modified")
        modified_composition.settings.agent_orchestration["max_parallel"] = 5

        print(f"  Original max_parallel: 2")
        print(f"  Modified max_parallel: 5")
        print(f"  Original tags: {composition.metadata['tags']}")
        print(f"  Modified tags: {modified_composition.metadata['tags']}")

        results.add(
            "Composition flexibility",
            modified_composition.settings.agent_orchestration["max_parallel"] == 5,
            "Successfully modified composition settings",
        )

        # =====================================================================
        # Cleanup
        # =====================================================================
        print("\n" + "=" * 80)
        print("CLEANUP")
        print("=" * 80)

        await memory.close()
        print("\n✓ Memory provider closed")

        print(f"✓ Test directory preserved: {temp_dir}")
        print(f"  - Composition file: {composition_file}")
        print(f"  - Memory directory: {temp_dir / '.forge' / 'memory'}")

    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback

        traceback.print_exc()
        results.add("Overall test execution", False, str(e))
    finally:
        # Print final results
        results.print_results()

        # Return exit code
        return 0 if results.failures == 0 else 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)

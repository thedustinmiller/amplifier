#!/usr/bin/env python3
"""
Test the Forge element discovery and loading system.

Tests:
1. Element discovery in elements/ directory
2. List all principles
3. Load each principle with validation
4. Verify element.yaml structure
5. Test loading non-existent elements (error handling)
"""

import sys
from pathlib import Path
from typing import List, Dict, Any
import json

# Add src to path
forge_root = Path(__file__).parent
sys.path.insert(0, str(forge_root / "src"))

from forge.core.element import ElementLoader, Element, ElementType


class ElementSystemTester:
    """Test the element loading system."""

    def __init__(self, elements_dir: Path):
        """Initialize tester.

        Args:
            elements_dir: Path to elements directory
        """
        self.elements_dir = elements_dir
        self.loader = ElementLoader([elements_dir])
        self.results = {
            "discovery": {},
            "principles": [],
            "loading_tests": {},
            "error_handling": {},
            "health_status": "unknown"
        }

    def test_discovery(self) -> Dict[str, Any]:
        """Test element discovery."""
        print("=" * 80)
        print("TEST 1: Element Discovery")
        print("=" * 80)

        try:
            all_elements = self.loader.list_elements()
            print(f"\n✓ Discovered {len(all_elements)} total elements")

            # Group by type
            by_type = {}
            for element in all_elements:
                type_name = element.type.value
                if type_name not in by_type:
                    by_type[type_name] = []
                by_type[type_name].append(element.name)

            self.results["discovery"] = {
                "total_count": len(all_elements),
                "by_type": by_type,
                "elements": [e.name for e in all_elements]
            }

            print("\nElements by type:")
            for element_type, names in by_type.items():
                print(f"  {element_type}: {len(names)} element(s)")
                for name in names:
                    print(f"    - {name}")

            return {"status": "success", "count": len(all_elements)}

        except Exception as e:
            print(f"\n✗ Discovery failed: {e}")
            return {"status": "error", "error": str(e)}

    def test_list_principles(self) -> Dict[str, Any]:
        """Test listing all principles."""
        print("\n" + "=" * 80)
        print("TEST 2: List All Principles")
        print("=" * 80)

        try:
            principles = self.loader.list_elements(ElementType.PRINCIPLE)
            print(f"\n✓ Found {len(principles)} principle(s)")

            principle_data = []
            for principle in principles:
                info = {
                    "name": principle.name,
                    "version": principle.version,
                    "description": principle.metadata.description,
                    "tags": principle.metadata.tags,
                    "author": principle.metadata.author
                }
                principle_data.append(info)

                print(f"\nPrinciple: {principle.name}")
                print(f"  Version: {principle.version}")
                print(f"  Description: {principle.metadata.description}")
                print(f"  Tags: {', '.join(principle.metadata.tags)}")
                print(f"  Author: {principle.metadata.author}")

            self.results["principles"] = principle_data
            return {"status": "success", "count": len(principles)}

        except Exception as e:
            print(f"\n✗ Listing principles failed: {e}")
            return {"status": "error", "error": str(e)}

    def test_load_element(self, name: str, element_type: ElementType) -> Dict[str, Any]:
        """Test loading a specific element.

        Args:
            name: Element name
            element_type: Element type

        Returns:
            Test results
        """
        print(f"\n{'-' * 80}")
        print(f"Loading element: {name} (type: {element_type.value})")
        print(f"{'-' * 80}")

        result = {
            "name": name,
            "type": element_type.value,
            "tests": {}
        }

        try:
            # Load the element
            element = self.loader.load(name, element_type)
            print(f"✓ Successfully loaded element: {name}")

            # Test 1: Metadata validation
            print("\n[1] Metadata Validation:")
            metadata_valid = (
                element.metadata.name == name and
                element.metadata.type == element_type and
                element.metadata.version is not None
            )
            if metadata_valid:
                print(f"  ✓ Metadata is valid")
                print(f"    - Name: {element.metadata.name}")
                print(f"    - Type: {element.metadata.type.value}")
                print(f"    - Version: {element.metadata.version}")
                print(f"    - Description: {element.metadata.description}")
                print(f"    - Tags: {element.metadata.tags}")
                print(f"    - License: {element.metadata.license}")
            else:
                print(f"  ✗ Metadata validation failed")

            result["tests"]["metadata"] = {
                "valid": metadata_valid,
                "name": element.metadata.name,
                "type": element.metadata.type.value,
                "version": element.metadata.version,
                "description": element.metadata.description,
                "tags": element.metadata.tags,
                "license": element.metadata.license
            }

            # Test 2: Content loading (for principles)
            print("\n[2] Content Loading:")
            if element_type in (ElementType.PRINCIPLE, ElementType.CONSTITUTION):
                if element.content:
                    content_length = len(element.content)
                    content_preview = element.content[:200] if len(element.content) > 200 else element.content
                    print(f"  ✓ Content loaded ({content_length} chars)")
                    print(f"    Preview: {content_preview}...")
                    result["tests"]["content"] = {
                        "loaded": True,
                        "length": content_length,
                        "preview": content_preview
                    }
                else:
                    print(f"  ✗ Content not loaded")
                    result["tests"]["content"] = {"loaded": False}
            else:
                print(f"  - Content not applicable for {element_type.value}")
                result["tests"]["content"] = {"applicable": False}

            # Test 3: Dependencies parsing
            print("\n[3] Dependencies Parsing:")
            deps = element.dependencies
            has_deps = any([
                deps.principles,
                deps.constitutions,
                deps.tools,
                deps.agents,
                deps.templates,
                deps.suggests
            ])

            if has_deps or deps.suggests:
                print(f"  ✓ Dependencies parsed:")
                if deps.principles:
                    print(f"    - Principles: {deps.principles}")
                if deps.constitutions:
                    print(f"    - Constitutions: {deps.constitutions}")
                if deps.tools:
                    print(f"    - Tools: {deps.tools}")
                if deps.agents:
                    print(f"    - Agents: {deps.agents}")
                if deps.templates:
                    print(f"    - Templates: {deps.templates}")
                if deps.suggests:
                    print(f"    - Suggests: {deps.suggests}")
            else:
                print(f"  - No dependencies declared")

            result["tests"]["dependencies"] = {
                "principles": deps.principles,
                "constitutions": deps.constitutions,
                "tools": deps.tools,
                "agents": deps.agents,
                "templates": deps.templates,
                "suggests": deps.suggests
            }

            # Test 4: Conflicts identification
            print("\n[4] Conflicts Identification:")
            conflicts = element.conflicts
            has_conflicts = any([
                conflicts.principles,
                conflicts.tools,
                conflicts.agents
            ])

            if has_conflicts:
                print(f"  ✓ Conflicts identified:")
                if conflicts.principles:
                    print(f"    - Conflicting principles: {conflicts.principles}")
                if conflicts.tools:
                    print(f"    - Conflicting tools: {conflicts.tools}")
                if conflicts.agents:
                    print(f"    - Conflicting agents: {conflicts.agents}")
                if conflicts.reason:
                    print(f"    - Reason: {conflicts.reason}")
            else:
                print(f"  - No conflicts declared")

            result["tests"]["conflicts"] = {
                "principles": conflicts.principles,
                "tools": conflicts.tools,
                "agents": conflicts.agents,
                "reason": conflicts.reason
            }

            # Test 5: element.yaml structure
            print("\n[5] element.yaml Structure:")
            element_file = (
                self.elements_dir /
                element_type.value /
                name /
                "element.yaml"
            )

            if element_file.exists():
                print(f"  ✓ element.yaml exists at: {element_file}")
                result["tests"]["yaml_structure"] = {
                    "exists": True,
                    "path": str(element_file)
                }
            else:
                print(f"  ✗ element.yaml not found")
                result["tests"]["yaml_structure"] = {"exists": False}

            result["status"] = "success"
            print(f"\n✓ All tests passed for {name}")

        except Exception as e:
            print(f"\n✗ Loading failed: {e}")
            import traceback
            traceback.print_exc()
            result["status"] = "error"
            result["error"] = str(e)

        return result

    def test_error_handling(self) -> Dict[str, Any]:
        """Test error handling for non-existent elements."""
        print("\n" + "=" * 80)
        print("TEST 3: Error Handling (Non-existent Elements)")
        print("=" * 80)

        test_cases = [
            ("nonexistent-principle", ElementType.PRINCIPLE),
            ("fake-tool", ElementType.TOOL),
            ("missing-agent", ElementType.AGENT),
        ]

        results = {}

        for name, element_type in test_cases:
            print(f"\nTrying to load non-existent element: {name} ({element_type.value})")
            try:
                element = self.loader.load(name, element_type)
                print(f"  ✗ Should have raised FileNotFoundError but got: {element}")
                results[name] = {"status": "unexpected_success"}
            except FileNotFoundError as e:
                print(f"  ✓ Correctly raised FileNotFoundError: {e}")
                results[name] = {"status": "correct_error", "error": str(e)}
            except Exception as e:
                print(f"  ⚠ Raised unexpected error: {e}")
                results[name] = {"status": "wrong_error", "error": str(e)}

        self.results["error_handling"] = results
        return results

    def run_all_tests(self) -> Dict[str, Any]:
        """Run all tests and generate report."""
        print("\n" + "=" * 80)
        print("FORGE ELEMENT SYSTEM TEST SUITE")
        print("=" * 80)
        print(f"Elements directory: {self.elements_dir}")
        print()

        # Test 1: Discovery
        discovery_result = self.test_discovery()

        # Test 2: List principles
        principles_result = self.test_list_principles()

        # Test 3: Load each principle with full validation
        print("\n" + "=" * 80)
        print("TEST 3: Load and Validate Each Principle")
        print("=" * 80)

        all_elements = self.loader.list_elements(ElementType.PRINCIPLE)
        for element in all_elements:
            load_result = self.test_load_element(element.name, ElementType.PRINCIPLE)
            self.results["loading_tests"][element.name] = load_result

        # Test 4: Error handling
        error_result = self.test_error_handling()

        # Determine health status
        all_successful = (
            discovery_result.get("status") == "success" and
            principles_result.get("status") == "success" and
            all(r.get("status") == "success"
                for r in self.results["loading_tests"].values()) and
            all(r.get("status") == "correct_error"
                for r in error_result.values())
        )

        self.results["health_status"] = "healthy" if all_successful else "degraded"

        # Print summary
        self.print_summary()

        return self.results

    def print_summary(self):
        """Print test summary."""
        print("\n" + "=" * 80)
        print("TEST SUMMARY")
        print("=" * 80)

        print(f"\nElement Discovery: {self.results['discovery'].get('total_count', 0)} elements found")
        print(f"Principles Found: {len(self.results['principles'])}")
        print(f"Loading Tests: {len(self.results['loading_tests'])} elements tested")

        # Count successes
        successful_loads = sum(
            1 for r in self.results["loading_tests"].values()
            if r.get("status") == "success"
        )
        print(f"  - Successful: {successful_loads}")
        print(f"  - Failed: {len(self.results['loading_tests']) - successful_loads}")

        print(f"\nError Handling Tests: {len(self.results['error_handling'])}")
        correct_errors = sum(
            1 for r in self.results["error_handling"].values()
            if r.get("status") == "correct_error"
        )
        print(f"  - Correct error handling: {correct_errors}")
        print(f"  - Incorrect: {len(self.results['error_handling']) - correct_errors}")

        print(f"\n{'=' * 80}")
        print(f"OVERALL HEALTH STATUS: {self.results['health_status'].upper()}")
        print(f"{'=' * 80}")

    def save_results(self, output_file: Path):
        """Save test results to JSON file.

        Args:
            output_file: Path to output JSON file
        """
        with open(output_file, 'w') as f:
            json.dump(self.results, f, indent=2)
        print(f"\n✓ Results saved to: {output_file}")


def main():
    """Main entry point."""
    # Setup paths
    forge_root = Path(__file__).parent
    elements_dir = forge_root / "elements"

    if not elements_dir.exists():
        print(f"Error: Elements directory not found: {elements_dir}")
        sys.exit(1)

    # Run tests
    tester = ElementSystemTester(elements_dir)
    results = tester.run_all_tests()

    # Save results
    output_file = forge_root / "test_results_element_loader.json"
    tester.save_results(output_file)

    # Exit with appropriate code
    sys.exit(0 if results["health_status"] == "healthy" else 1)


if __name__ == "__main__":
    main()

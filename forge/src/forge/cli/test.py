"""
CLI command for running Forge tests.
"""

import sys
from pathlib import Path
import json

from forge.testing import TestRunner, TestScenario, ScenarioType


def run_tests(args):
    """Run Forge tests."""
    # Parse arguments
    test_type = getattr(args, 'type', 'all')
    output_dir = Path(getattr(args, 'output', './forge_test_results'))
    scenarios_dir = Path(getattr(args, 'scenarios', './testing/profile_evaluation'))

    print(f"Forge Test Runner")
    print(f"=================")
    print(f"Test type: {test_type}")
    print(f"Output dir: {output_dir}")
    print(f"Scenarios dir: {scenarios_dir}")
    print()

    # Create test runner
    runner = TestRunner(output_dir)

    # Load scenarios based on type
    if test_type == 'all' or test_type == 'scenarios':
        if scenarios_dir.exists():
            runner.load_scenarios_from_dir(scenarios_dir)
            print(f"Loaded {len(runner.scenarios)} scenarios")

    # Run tests
    if runner.scenarios:
        print("\nRunning scenarios...")
        summary = runner.run_all()

        print("\n" + "="*50)
        print("Test Summary")
        print("="*50)
        print(f"Total scenarios: {summary['total_scenarios']}")
        print(f"Successful: {summary['successful']}")
        print(f"Failed: {summary['failed']}")
        print(f"Success rate: {summary['success_rate']:.1f}%")
        print(f"\nResults saved to: {output_dir}")

        # Save detailed summary
        summary_file = output_dir / "summary.json"
        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2)

        return 0 if summary['failed'] == 0 else 1
    else:
        print("No scenarios loaded. Check scenarios directory.")
        return 1


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description='Run Forge tests')
    parser.add_argument(
        '--type',
        choices=['all', 'scenarios', 'elements', 'compositions'],
        default='all',
        help='Type of tests to run'
    )
    parser.add_argument(
        '--output',
        default='./forge_test_results',
        help='Output directory for test results'
    )
    parser.add_argument(
        '--scenarios',
        default='./testing/profile_evaluation',
        help='Directory containing test scenarios'
    )

    args = parser.parse_args()
    sys.exit(run_tests(args))


if __name__ == '__main__':
    main()

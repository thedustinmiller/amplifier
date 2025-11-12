#!/usr/bin/env python3
"""
Test orchestrator for running iterative tests with child Claude Code instances.

This script coordinates testing of:
1. Individual elements
2. Element compositions
3. The overall Forge process

Uses child Claude Code instances via Task tool integration.
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Any

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from forge.testing import TestRunner, TestScenario, ScenarioType, TestLogger, MetricsCollector


class TestOrchestrator:
    """
    Orchestrates comprehensive testing with child instances.

    This class manages:
    - Test plan generation
    - Child instance coordination
    - Result aggregation
    - Iterative improvement
    """

    def __init__(self, output_dir: Path):
        """Initialize orchestrator."""
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.test_results: Dict[str, Any] = {}
        self.iterations: List[Dict[str, Any]] = []

    def generate_element_tests(self, elements_dir: Path) -> List[TestScenario]:
        """
        Generate test scenarios for individual elements.

        Args:
            elements_dir: Directory containing elements

        Returns:
            List of element test scenarios
        """
        scenarios = []

        # Find all elements
        for element_file in elements_dir.rglob("element.yaml"):
            element_name = element_file.parent.name

            scenario = TestScenario(
                name=f"element_{element_name}",
                scenario_type=ScenarioType.ELEMENT_TEST,
                description=f"Test element: {element_name}",
                elements_to_test=[element_name],
                metadata={
                    "element_path": str(element_file.parent),
                    "element_file": str(element_file),
                }
            )

            scenarios.append(scenario)

        return scenarios

    def generate_composition_tests(self) -> List[TestScenario]:
        """
        Generate test scenarios for element compositions.

        Returns:
            List of composition test scenarios
        """
        scenarios = []

        # Define key compositions to test
        compositions = [
            {
                "name": "minimal_workflow",
                "elements": ["file-analyzer", "code-generator", "test-runner"],
                "description": "Test minimal development workflow",
            },
            {
                "name": "full_cycle",
                "elements": ["spec-writer", "architect", "implementer", "tester", "documenter"],
                "description": "Test full development cycle",
            },
            {
                "name": "spec_driven",
                "elements": ["spec-writer", "spec-validator", "spec-implementer"],
                "description": "Test specification-driven development",
            },
        ]

        for comp in compositions:
            scenario = TestScenario(
                name=f"composition_{comp['name']}",
                scenario_type=ScenarioType.COMPOSITION_TEST,
                description=comp["description"],
                elements_to_test=comp["elements"],
                composition_config=comp,
            )
            scenarios.append(scenario)

        return scenarios

    def generate_workflow_tests(self) -> List[TestScenario]:
        """
        Generate test scenarios for complete workflows.

        Returns:
            List of workflow test scenarios
        """
        scenarios = []

        # Define workflow tests based on common development scenarios
        workflows = [
            {
                "name": "greenfield_project",
                "description": "Create a new project from scratch",
                "phases": ["ideation", "specification", "architecture", "implementation", "testing"],
            },
            {
                "name": "feature_addition",
                "description": "Add a feature to existing code",
                "phases": ["analysis", "design", "implementation", "integration", "testing"],
            },
            {
                "name": "bug_fix",
                "description": "Debug and fix an issue",
                "phases": ["reproduction", "investigation", "fix", "verification", "documentation"],
            },
        ]

        for workflow in workflows:
            scenario = TestScenario(
                name=f"workflow_{workflow['name']}",
                scenario_type=ScenarioType.WORKFLOW_TEST,
                description=workflow["description"],
                metadata=workflow,
            )
            scenarios.append(scenario)

        return scenarios

    def create_test_plan(self) -> Dict[str, Any]:
        """
        Create comprehensive test plan.

        Returns:
            Test plan dictionary
        """
        # Get elements directory
        elements_dir = Path(__file__).parent.parent / "elements"

        # Generate all test types
        element_tests = self.generate_element_tests(elements_dir) if elements_dir.exists() else []
        composition_tests = self.generate_composition_tests()
        workflow_tests = self.generate_workflow_tests()

        all_scenarios = element_tests + composition_tests + workflow_tests

        plan = {
            "version": "1.0",
            "total_scenarios": len(all_scenarios),
            "breakdown": {
                "element_tests": len(element_tests),
                "composition_tests": len(composition_tests),
                "workflow_tests": len(workflow_tests),
            },
            "scenarios": [
                {
                    "name": s.name,
                    "type": s.scenario_type.value,
                    "description": s.description,
                }
                for s in all_scenarios
            ],
        }

        # Save plan
        plan_file = self.output_dir / "test_plan.json"
        with open(plan_file, "w") as f:
            json.dump(plan, f, indent=2)

        print(f"Test plan created: {plan_file}")
        print(f"Total scenarios: {plan['total_scenarios']}")
        print(f"  - Element tests: {plan['breakdown']['element_tests']}")
        print(f"  - Composition tests: {plan['breakdown']['composition_tests']}")
        print(f"  - Workflow tests: {plan['breakdown']['workflow_tests']}")

        return plan

    def prepare_child_task(self, scenario: TestScenario) -> str:
        """
        Prepare task prompt for child Claude Code instance.

        Args:
            scenario: Test scenario to execute

        Returns:
            Task prompt string
        """
        prompt = f"""
Execute test scenario: {scenario.name}

Type: {scenario.scenario_type.value}
Description: {scenario.description}

"""

        if scenario.task_file:
            prompt += f"""
Task File: {scenario.task_file}

Read the task file and execute according to the requirements.
"""

        if scenario.requirements:
            prompt += f"""
Requirements:
"""
            for req in scenario.requirements:
                prompt += f"- {req}\n"

        if scenario.elements_to_test:
            prompt += f"""
Elements to test: {', '.join(scenario.elements_to_test)}
"""

        if scenario.composition_config:
            prompt += f"""
Composition config:
{json.dumps(scenario.composition_config, indent=2)}
"""

        prompt += f"""

Execute this scenario systematically:
1. Review requirements and constraints
2. Execute the task according to the scenario type
3. Document your approach and decisions
4. Track metrics (time, quality, process)
5. Generate artifacts

Report back with:
- Success/failure status
- Key metrics
- Observations
- Artifacts produced
- Recommendations for improvement
"""

        return prompt

    def execute_iteration(self, iteration_num: int) -> Dict[str, Any]:
        """
        Execute one iteration of testing.

        Args:
            iteration_num: Iteration number

        Returns:
            Iteration results
        """
        print(f"\n{'='*60}")
        print(f"ITERATION {iteration_num}")
        print(f"{'='*60}\n")

        iteration_dir = self.output_dir / f"iteration_{iteration_num}"
        iteration_dir.mkdir(parents=True, exist_ok=True)

        # Create test plan
        plan = self.create_test_plan()

        # For this implementation, we'll prepare the scenarios
        # Actual child instance execution would happen via Claude Code Task tool
        # This script prepares everything for that

        iteration_result = {
            "iteration": iteration_num,
            "plan": plan,
            "output_dir": str(iteration_dir),
            "scenarios_prepared": plan["total_scenarios"],
        }

        # Save iteration result
        result_file = iteration_dir / "iteration_result.json"
        with open(result_file, "w") as f:
            json.dump(iteration_result, f, indent=2)

        self.iterations.append(iteration_result)

        return iteration_result

    def analyze_and_improve(self) -> List[str]:
        """
        Analyze results and generate improvement recommendations.

        Returns:
            List of improvement recommendations
        """
        recommendations = []

        # Analyze patterns across iterations
        if len(self.iterations) > 0:
            latest = self.iterations[-1]
            recommendations.append(
                f"Review iteration {latest['iteration']} results"
            )

        recommendations.extend([
            "Identify failing test patterns",
            "Review element effectiveness",
            "Optimize composition strategies",
            "Update elements based on learnings",
            "Add missing elements for common patterns",
            "Improve documentation based on observations",
        ])

        return recommendations

    def generate_report(self) -> Dict[str, Any]:
        """
        Generate comprehensive test report.

        Returns:
            Report dictionary
        """
        report = {
            "total_iterations": len(self.iterations),
            "iterations": self.iterations,
            "recommendations": self.analyze_and_improve(),
            "output_dir": str(self.output_dir),
        }

        report_file = self.output_dir / "comprehensive_report.json"
        with open(report_file, "w") as f:
            json.dump(report, f, indent=2)

        print(f"\nComprehensive report generated: {report_file}")

        return report


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Orchestrate comprehensive Forge testing"
    )
    parser.add_argument(
        "--output",
        default="./forge_test_orchestration",
        help="Output directory for test results",
    )
    parser.add_argument(
        "--iterations",
        type=int,
        default=1,
        help="Number of test iterations to run",
    )

    args = parser.parse_args()

    # Create orchestrator
    orchestrator = TestOrchestrator(Path(args.output))

    print("Forge Test Orchestrator")
    print("="*60)
    print(f"Output directory: {args.output}")
    print(f"Planned iterations: {args.iterations}")
    print()

    # Execute iterations
    for i in range(1, args.iterations + 1):
        orchestrator.execute_iteration(i)

    # Generate final report
    report = orchestrator.generate_report()

    print("\n" + "="*60)
    print("ORCHESTRATION COMPLETE")
    print("="*60)
    print(f"Total iterations: {report['total_iterations']}")
    print(f"\nRecommendations:")
    for rec in report['recommendations']:
        print(f"  - {rec}")

    return 0


if __name__ == "__main__":
    sys.exit(main())

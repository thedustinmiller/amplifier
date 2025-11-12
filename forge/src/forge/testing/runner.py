"""
Test runner for executing test scenarios.
"""

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Callable
from enum import Enum

from .logger import TestLogger
from .metrics import MetricsCollector


class ScenarioType(Enum):
    """Types of test scenarios."""
    ELEMENT_TEST = "element_test"
    COMPOSITION_TEST = "composition_test"
    WORKFLOW_TEST = "workflow_test"
    INTEGRATION_TEST = "integration_test"
    PROFILE_EVALUATION = "profile_evaluation"


@dataclass
class TestScenario:
    """A test scenario to execute."""

    name: str
    scenario_type: ScenarioType
    description: str
    task_file: Optional[Path] = None
    requirements: List[str] = field(default_factory=list)
    success_criteria: Dict[str, Any] = field(default_factory=dict)
    elements_to_test: List[str] = field(default_factory=list)
    composition_config: Optional[Dict[str, Any]] = None
    setup_commands: List[str] = field(default_factory=list)
    timeout_seconds: int = 3600
    metadata: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_task_file(cls, task_file: Path) -> "TestScenario":
        """Create scenario from a task markdown file."""
        # Parse task file to extract requirements
        content = task_file.read_text()

        # Extract task name from file
        name = task_file.stem.replace("task_", "").replace("_", " ").title()

        # Simple parsing - could be enhanced
        requirements = []
        in_requirements = False
        for line in content.split("\n"):
            if "## Requirements" in line or "### Functional Requirements" in line:
                in_requirements = True
                continue
            if in_requirements and line.startswith("- "):
                requirements.append(line[2:].strip())
            if in_requirements and line.startswith("##"):
                in_requirements = False

        return cls(
            name=name,
            scenario_type=ScenarioType.PROFILE_EVALUATION,
            description=f"Test from {task_file.name}",
            task_file=task_file,
            requirements=requirements,
            metadata={"source": str(task_file)},
        )


class TestRunner:
    """
    Orchestrates test execution.

    Provides:
    - Test scenario execution
    - Child agent coordination
    - Result collection
    - Progress tracking
    """

    def __init__(self, output_dir: Path):
        """
        Initialize test runner.

        Args:
            output_dir: Base directory for test outputs
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.scenarios: List[TestScenario] = []
        self.results: Dict[str, Dict[str, Any]] = {}

    def add_scenario(self, scenario: TestScenario):
        """Add a test scenario."""
        self.scenarios.append(scenario)

    def load_scenarios_from_dir(self, scenarios_dir: Path, pattern: str = "task_*.md"):
        """Load scenarios from directory of task files."""
        for task_file in scenarios_dir.glob(pattern):
            if task_file.name == "task_template.md":
                continue
            scenario = TestScenario.from_task_file(task_file)
            self.add_scenario(scenario)

    def run_scenario(
        self,
        scenario: TestScenario,
        executor: Optional[Callable] = None
    ) -> Dict[str, Any]:
        """
        Run a single test scenario.

        Args:
            scenario: The scenario to run
            executor: Optional custom executor function

        Returns:
            Test results dictionary
        """
        # Create output directory for this scenario
        scenario_dir = self.output_dir / scenario.name.lower().replace(" ", "_")
        scenario_dir.mkdir(parents=True, exist_ok=True)

        # Initialize logger and metrics
        logger = TestLogger(scenario.name, scenario_dir)
        metrics = MetricsCollector()

        logger.start()
        metrics.start_test()

        try:
            # Log scenario info
            logger.observe(
                "scenario",
                f"Starting scenario: {scenario.name}",
                {
                    "type": scenario.scenario_type.value,
                    "description": scenario.description,
                    "requirements": scenario.requirements,
                }
            )

            # Execute scenario
            if executor:
                result = executor(scenario, logger, metrics)
            else:
                result = self._default_executor(scenario, logger, metrics)

            # Record success
            success = result.get("success", False)
            metrics.record_success(success)

            logger.end(success, f"Scenario completed: {scenario.name}")
            metrics.end_test()

            # Save metrics
            metrics.get_metrics().save(scenario_dir / "metrics.json")

            # Store results
            test_result = {
                "scenario": scenario.name,
                "success": success,
                "metrics": metrics.get_summary(),
                "output_dir": str(scenario_dir),
                **result,
            }

            self.results[scenario.name] = test_result

            return test_result

        except Exception as e:
            logger.error(f"Scenario failed with exception: {str(e)}", e)
            metrics.record_success(False)
            logger.end(False, f"Scenario failed: {str(e)}")
            metrics.end_test()

            test_result = {
                "scenario": scenario.name,
                "success": False,
                "error": str(e),
                "metrics": metrics.get_summary(),
                "output_dir": str(scenario_dir),
            }

            self.results[scenario.name] = test_result

            return test_result

    def _default_executor(
        self,
        scenario: TestScenario,
        logger: TestLogger,
        metrics: MetricsCollector
    ) -> Dict[str, Any]:
        """Default scenario executor."""
        # This is a placeholder - actual execution happens via child agents
        logger.observe(
            "execution",
            "Default executor - scenario prepared for manual or agent execution",
            {"scenario_type": scenario.scenario_type.value}
        )

        return {
            "success": True,
            "message": "Scenario prepared",
            "task_file": str(scenario.task_file) if scenario.task_file else None,
        }

    def run_all(self, executor: Optional[Callable] = None) -> Dict[str, Any]:
        """
        Run all scenarios.

        Args:
            executor: Optional custom executor function

        Returns:
            Summary of all results
        """
        results = []

        for scenario in self.scenarios:
            result = self.run_scenario(scenario, executor)
            results.append(result)

        # Generate summary
        total = len(results)
        successful = sum(1 for r in results if r.get("success"))

        summary = {
            "total_scenarios": total,
            "successful": successful,
            "failed": total - successful,
            "success_rate": (successful / total * 100) if total > 0 else 0,
            "results": results,
        }

        # Save summary
        summary_path = self.output_dir / "test_summary.json"
        with open(summary_path, "w") as f:
            json.dump(summary, f, indent=2)

        return summary

    def get_results(self) -> Dict[str, Dict[str, Any]]:
        """Get all test results."""
        return self.results

    def get_summary(self) -> Dict[str, Any]:
        """Get results summary."""
        if not self.results:
            return {
                "total_scenarios": 0,
                "successful": 0,
                "failed": 0,
                "success_rate": 0,
            }

        total = len(self.results)
        successful = sum(1 for r in self.results.values() if r.get("success"))

        return {
            "total_scenarios": total,
            "successful": successful,
            "failed": total - successful,
            "success_rate": (successful / total * 100) if total > 0 else 0,
        }


def create_test_plan(
    name: str,
    scenarios: List[TestScenario],
    output_dir: Path
) -> Dict[str, Any]:
    """
    Create a test plan document.

    Args:
        name: Name of test plan
        scenarios: List of scenarios to include
        output_dir: Directory for output

    Returns:
        Test plan metadata
    """
    plan = {
        "name": name,
        "total_scenarios": len(scenarios),
        "scenarios": [
            {
                "name": s.name,
                "type": s.scenario_type.value,
                "description": s.description,
                "requirements_count": len(s.requirements),
            }
            for s in scenarios
        ],
        "output_dir": str(output_dir),
    }

    plan_path = output_dir / "test_plan.json"
    with open(plan_path, "w") as f:
        json.dump(plan, f, indent=2)

    return plan

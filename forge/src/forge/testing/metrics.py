"""
Metrics collection for test evaluation.
"""

import time
from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional
from pathlib import Path
import json


@dataclass
class TestMetrics:
    """Comprehensive test metrics."""

    # Time metrics
    total_time_seconds: float = 0.0
    time_to_first_code: Optional[float] = None
    time_to_first_test: Optional[float] = None
    planning_time: float = 0.0
    implementation_time: float = 0.0
    testing_time: float = 0.0
    documentation_time: float = 0.0

    # Process metrics
    phases_count: int = 0
    decisions_made: int = 0
    observations_recorded: int = 0
    iterations_count: int = 0

    # Code metrics
    files_created: int = 0
    files_modified: int = 0
    lines_of_code: int = 0
    lines_of_tests: int = 0
    lines_of_docs: int = 0

    # Quality metrics
    tests_written: int = 0
    tests_passed: int = 0
    tests_failed: int = 0
    test_coverage_percent: Optional[float] = None
    linting_issues: int = 0

    # Element metrics
    elements_used: List[str] = field(default_factory=list)
    tools_invoked: List[str] = field(default_factory=list)
    agents_spawned: int = 0

    # Outcome metrics
    success: bool = False
    requirements_met: int = 0
    requirements_total: int = 0
    features_implemented: List[str] = field(default_factory=list)
    features_deferred: List[str] = field(default_factory=list)

    # Custom metrics
    custom: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)

    def save(self, path: Path):
        """Save metrics to file."""
        with open(path, "w") as f:
            json.dump(self.to_dict(), f, indent=2)

    @classmethod
    def load(cls, path: Path) -> "TestMetrics":
        """Load metrics from file."""
        with open(path) as f:
            data = json.load(f)
        return cls(**data)


class MetricsCollector:
    """
    Collects and aggregates test metrics.

    Tracks various aspects of test execution including time, quality, and outcomes.
    """

    def __init__(self):
        """Initialize metrics collector."""
        self.metrics = TestMetrics()
        self._phase_start_times: Dict[str, float] = {}
        self._test_start_time: Optional[float] = None

    def start_test(self):
        """Mark test start."""
        self._test_start_time = time.time()

    def end_test(self):
        """Mark test end and calculate total time."""
        if self._test_start_time:
            self.metrics.total_time_seconds = time.time() - self._test_start_time

    def start_phase(self, phase_name: str):
        """Mark phase start."""
        self._phase_start_times[phase_name] = time.time()
        self.metrics.phases_count += 1

    def end_phase(self, phase_name: str):
        """Mark phase end and update phase time."""
        if phase_name in self._phase_start_times:
            duration = time.time() - self._phase_start_times[phase_name]

            # Map phase names to metrics
            if "plan" in phase_name.lower() or "design" in phase_name.lower():
                self.metrics.planning_time += duration
            elif "implement" in phase_name.lower() or "code" in phase_name.lower():
                self.metrics.implementation_time += duration
            elif "test" in phase_name.lower():
                self.metrics.testing_time += duration
            elif "doc" in phase_name.lower():
                self.metrics.documentation_time += duration

            del self._phase_start_times[phase_name]

    def record_first_code(self):
        """Record time to first code."""
        if self._test_start_time and self.metrics.time_to_first_code is None:
            self.metrics.time_to_first_code = time.time() - self._test_start_time

    def record_first_test(self):
        """Record time to first test."""
        if self._test_start_time and self.metrics.time_to_first_test is None:
            self.metrics.time_to_first_test = time.time() - self._test_start_time

    def record_decision(self):
        """Increment decision count."""
        self.metrics.decisions_made += 1

    def record_observation(self):
        """Increment observation count."""
        self.metrics.observations_recorded += 1

    def record_iteration(self):
        """Increment iteration count."""
        self.metrics.iterations_count += 1

    def record_file_created(self, path: str):
        """Record file creation."""
        self.metrics.files_created += 1

    def record_file_modified(self, path: str):
        """Record file modification."""
        self.metrics.files_modified += 1

    def record_code_metrics(self, loc: int, test_loc: int = 0, doc_loc: int = 0):
        """Record lines of code metrics."""
        self.metrics.lines_of_code += loc
        self.metrics.lines_of_tests += test_loc
        self.metrics.lines_of_docs += doc_loc

    def record_test_results(self, passed: int, failed: int):
        """Record test results."""
        self.metrics.tests_written += (passed + failed)
        self.metrics.tests_passed += passed
        self.metrics.tests_failed += failed

    def record_coverage(self, coverage_percent: float):
        """Record test coverage."""
        self.metrics.test_coverage_percent = coverage_percent

    def record_linting_issues(self, count: int):
        """Record linting issues."""
        self.metrics.linting_issues += count

    def record_element_used(self, element_name: str):
        """Record element usage."""
        if element_name not in self.metrics.elements_used:
            self.metrics.elements_used.append(element_name)

    def record_tool_invoked(self, tool_name: str):
        """Record tool invocation."""
        self.metrics.tools_invoked.append(tool_name)

    def record_agent_spawned(self):
        """Increment agent spawn count."""
        self.metrics.agents_spawned += 1

    def record_requirement_met(self):
        """Increment requirements met."""
        self.metrics.requirements_met += 1

    def set_total_requirements(self, count: int):
        """Set total requirements."""
        self.metrics.requirements_total = count

    def record_feature_implemented(self, feature: str):
        """Record implemented feature."""
        if feature not in self.metrics.features_implemented:
            self.metrics.features_implemented.append(feature)

    def record_feature_deferred(self, feature: str):
        """Record deferred feature."""
        if feature not in self.metrics.features_deferred:
            self.metrics.features_deferred.append(feature)

    def record_success(self, success: bool):
        """Record overall success."""
        self.metrics.success = success

    def record_custom(self, key: str, value: Any):
        """Record custom metric."""
        self.metrics.custom[key] = value

    def get_metrics(self) -> TestMetrics:
        """Get current metrics."""
        return self.metrics

    def get_summary(self) -> Dict[str, Any]:
        """Get metrics summary."""
        total_tests = self.metrics.tests_passed + self.metrics.tests_failed
        test_pass_rate = (
            (self.metrics.tests_passed / total_tests * 100)
            if total_tests > 0
            else 0
        )

        req_completion_rate = (
            (self.metrics.requirements_met / self.metrics.requirements_total * 100)
            if self.metrics.requirements_total > 0
            else 0
        )

        return {
            "total_time_minutes": round(self.metrics.total_time_seconds / 60, 2),
            "test_pass_rate": round(test_pass_rate, 2),
            "requirement_completion": round(req_completion_rate, 2),
            "code_to_test_ratio": (
                round(self.metrics.lines_of_code / self.metrics.lines_of_tests, 2)
                if self.metrics.lines_of_tests > 0
                else 0
            ),
            "success": self.metrics.success,
        }

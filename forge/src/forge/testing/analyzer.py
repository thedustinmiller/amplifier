"""
Result analysis and comparison tools.
"""

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional
from collections import defaultdict


@dataclass
class ComparisonResult:
    """Result of comparing multiple test runs."""

    metric_name: str
    values: Dict[str, Any]
    best: str
    worst: str
    variance: float


class ResultAnalyzer:
    """
    Analyzes and compares test results.

    Provides:
    - Cross-run comparison
    - Trend analysis
    - Pattern identification
    - Recommendation generation
    """

    def __init__(self):
        """Initialize analyzer."""
        self.results: List[Dict[str, Any]] = []

    def load_result(self, result_path: Path):
        """Load a test result file."""
        with open(result_path) as f:
            result = json.load(f)
        self.results.append(result)

    def load_results_from_dir(self, results_dir: Path):
        """Load all results from a directory."""
        for result_file in results_dir.rglob("metrics.json"):
            self.load_result(result_file)

    def compare_metrics(
        self,
        metric_paths: List[str],
        result_filter: Optional[Dict[str, Any]] = None
    ) -> List[ComparisonResult]:
        """
        Compare specific metrics across results.

        Args:
            metric_paths: Dot-notation paths to metrics (e.g., "total_time_seconds")
            result_filter: Optional filter for results

        Returns:
            List of comparison results
        """
        comparisons = []

        for metric_path in metric_paths:
            values = {}

            for result in self.results:
                # Apply filter if provided
                if result_filter:
                    if not all(
                        result.get(k) == v for k, v in result_filter.items()
                    ):
                        continue

                # Extract metric value using dot notation
                value = self._get_nested_value(result, metric_path)
                if value is not None:
                    result_id = result.get("scenario", "unknown")
                    values[result_id] = value

            if not values:
                continue

            # Calculate statistics
            numeric_values = [v for v in values.values() if isinstance(v, (int, float))]

            if numeric_values:
                best_id = min(values, key=values.get)
                worst_id = max(values, key=values.get)
                variance = max(numeric_values) - min(numeric_values)
            else:
                best_id = worst_id = list(values.keys())[0]
                variance = 0

            comparisons.append(
                ComparisonResult(
                    metric_name=metric_path,
                    values=values,
                    best=best_id,
                    worst=worst_id,
                    variance=variance
                )
            )

        return comparisons

    def _get_nested_value(self, data: Dict, path: str) -> Any:
        """Get nested value using dot notation."""
        keys = path.split(".")
        value = data

        for key in keys:
            if isinstance(value, dict):
                value = value.get(key)
            else:
                return None

        return value

    def identify_patterns(self) -> Dict[str, List[str]]:
        """
        Identify patterns across results.

        Returns:
            Dictionary of pattern categories and observations
        """
        patterns = defaultdict(list)

        # Analyze time patterns
        time_metrics = ["total_time_seconds", "planning_time", "implementation_time"]
        for metric in time_metrics:
            values = []
            for result in self.results:
                value = self._get_nested_value(result, metric)
                if value is not None:
                    values.append(value)

            if values:
                avg = sum(values) / len(values)
                patterns["time"].append(
                    f"Average {metric}: {avg:.2f}s"
                )

        # Analyze success patterns
        success_count = sum(
            1 for r in self.results
            if self._get_nested_value(r, "success")
        )
        success_rate = (success_count / len(self.results) * 100) if self.results else 0
        patterns["success"].append(
            f"Success rate: {success_rate:.1f}% ({success_count}/{len(self.results)})"
        )

        # Analyze element usage
        element_usage = defaultdict(int)
        for result in self.results:
            elements = self._get_nested_value(result, "elements_used") or []
            for element in elements:
                element_usage[element] += 1

        if element_usage:
            most_used = max(element_usage.items(), key=lambda x: x[1])
            patterns["elements"].append(
                f"Most used element: {most_used[0]} ({most_used[1]} times)"
            )

        return dict(patterns)

    def generate_recommendations(self) -> List[str]:
        """
        Generate recommendations based on analysis.

        Returns:
            List of recommendations
        """
        recommendations = []

        # Analyze failure patterns
        failures = [
            r for r in self.results
            if not self._get_nested_value(r, "success")
        ]

        if failures:
            recommendations.append(
                f"Investigate {len(failures)} failed scenarios to identify common issues"
            )

        # Analyze time efficiency
        time_values = [
            self._get_nested_value(r, "total_time_seconds")
            for r in self.results
            if self._get_nested_value(r, "total_time_seconds") is not None
        ]

        if time_values:
            avg_time = sum(time_values) / len(time_values)
            slow_results = [
                r for r in self.results
                if (self._get_nested_value(r, "total_time_seconds") or 0) > avg_time * 1.5
            ]

            if slow_results:
                recommendations.append(
                    f"Optimize {len(slow_results)} slow scenarios "
                    f"(>{avg_time * 1.5:.1f}s vs {avg_time:.1f}s avg)"
                )

        # Analyze test coverage
        coverage_values = [
            self._get_nested_value(r, "test_coverage_percent")
            for r in self.results
            if self._get_nested_value(r, "test_coverage_percent") is not None
        ]

        if coverage_values:
            avg_coverage = sum(coverage_values) / len(coverage_values)
            if avg_coverage < 80:
                recommendations.append(
                    f"Improve test coverage (current avg: {avg_coverage:.1f}%, target: 80%)"
                )

        return recommendations

    def generate_report(self, output_path: Path):
        """
        Generate comprehensive analysis report.

        Args:
            output_path: Path to save report
        """
        patterns = self.identify_patterns()
        recommendations = self.generate_recommendations()

        # Compare key metrics
        key_metrics = [
            "total_time_seconds",
            "tests_passed",
            "tests_failed",
            "lines_of_code",
            "requirements_met",
        ]

        comparisons = self.compare_metrics(key_metrics)

        report = {
            "total_results_analyzed": len(self.results),
            "patterns": patterns,
            "recommendations": recommendations,
            "metric_comparisons": [
                {
                    "metric": c.metric_name,
                    "best": c.best,
                    "worst": c.worst,
                    "variance": c.variance,
                    "values": c.values,
                }
                for c in comparisons
            ],
        }

        with open(output_path, "w") as f:
            json.dump(report, f, indent=2)

        return report

    def get_summary(self) -> Dict[str, Any]:
        """Get analysis summary."""
        patterns = self.identify_patterns()
        recommendations = self.generate_recommendations()

        return {
            "total_results": len(self.results),
            "patterns": patterns,
            "recommendations": recommendations,
        }

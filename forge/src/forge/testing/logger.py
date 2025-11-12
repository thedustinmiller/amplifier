"""
Test logging system for systematic observation and result tracking.
"""

import json
import time
from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Optional, List, Dict
from contextlib import contextmanager


class EventType(Enum):
    """Types of test events."""
    TEST_START = "test_start"
    TEST_END = "test_end"
    PHASE_START = "phase_start"
    PHASE_END = "phase_end"
    OBSERVATION = "observation"
    METRIC = "metric"
    ERROR = "error"
    DECISION = "decision"
    ARTIFACT = "artifact"


class Severity(Enum):
    """Severity levels for observations."""
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


@dataclass
class TestEvent:
    """A single event in the test execution."""
    timestamp: float
    event_type: EventType
    message: str
    data: Dict[str, Any] = field(default_factory=dict)
    severity: Severity = Severity.INFO

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "timestamp": self.timestamp,
            "datetime": datetime.fromtimestamp(self.timestamp).isoformat(),
            "event_type": self.event_type.value,
            "message": self.message,
            "data": self.data,
            "severity": self.severity.value,
        }


@dataclass
class Observation:
    """A structured observation during testing."""
    category: str
    observation: str
    context: Dict[str, Any] = field(default_factory=dict)
    timestamp: float = field(default_factory=time.time)
    tags: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "timestamp": self.timestamp,
            "datetime": datetime.fromtimestamp(self.timestamp).isoformat(),
            "category": self.category,
            "observation": self.observation,
            "context": self.context,
            "tags": self.tags,
        }


class TestLogger:
    """
    Systematic test logging with structured events and observations.

    Provides:
    - Event logging with timestamps
    - Observation tracking
    - Metrics collection
    - Result serialization
    - Context management
    """

    def __init__(self, test_name: str, output_dir: Path):
        """
        Initialize test logger.

        Args:
            test_name: Name of the test
            output_dir: Directory for output files
        """
        self.test_name = test_name
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.events: List[TestEvent] = []
        self.observations: List[Observation] = []
        self.metrics: Dict[str, Any] = {}
        self.start_time: Optional[float] = None
        self.end_time: Optional[float] = None
        self.current_phase: Optional[str] = None

        # Create log files
        self.events_file = self.output_dir / "events.jsonl"
        self.observations_file = self.output_dir / "observations.jsonl"
        self.summary_file = self.output_dir / "summary.json"

    def start(self):
        """Start test logging."""
        self.start_time = time.time()
        self.log_event(
            EventType.TEST_START,
            f"Starting test: {self.test_name}",
            {"test_name": self.test_name}
        )

    def end(self, success: bool = True, message: str = ""):
        """End test logging."""
        self.end_time = time.time()
        duration = self.end_time - (self.start_time or self.end_time)

        self.log_event(
            EventType.TEST_END,
            message or f"Test completed: {self.test_name}",
            {
                "test_name": self.test_name,
                "success": success,
                "duration_seconds": duration,
            }
        )

        # Write summary
        self._write_summary()

    def log_event(
        self,
        event_type: EventType,
        message: str,
        data: Optional[Dict[str, Any]] = None,
        severity: Severity = Severity.INFO
    ):
        """Log a test event."""
        event = TestEvent(
            timestamp=time.time(),
            event_type=event_type,
            message=message,
            data=data or {},
            severity=severity
        )
        self.events.append(event)

        # Write to events log
        with open(self.events_file, "a") as f:
            f.write(json.dumps(event.to_dict()) + "\n")

        # Also print to console
        time_str = datetime.fromtimestamp(event.timestamp).strftime("%H:%M:%S")
        print(f"[{time_str}] {event_type.value}: {message}")

    def observe(
        self,
        category: str,
        observation: str,
        context: Optional[Dict[str, Any]] = None,
        tags: Optional[List[str]] = None
    ):
        """Record an observation."""
        obs = Observation(
            category=category,
            observation=observation,
            context=context or {},
            tags=tags or []
        )
        self.observations.append(obs)

        # Write to observations log
        with open(self.observations_file, "a") as f:
            f.write(json.dumps(obs.to_dict()) + "\n")

        # Log as event too
        self.log_event(
            EventType.OBSERVATION,
            f"{category}: {observation}",
            {"observation": obs.to_dict()}
        )

    def record_metric(self, key: str, value: Any):
        """Record a metric."""
        self.metrics[key] = value
        self.log_event(
            EventType.METRIC,
            f"Metric recorded: {key} = {value}",
            {"metric": key, "value": value}
        )

    def record_decision(self, decision: str, reasoning: str, alternatives: Optional[List[str]] = None):
        """Record a decision point."""
        self.log_event(
            EventType.DECISION,
            f"Decision: {decision}",
            {
                "decision": decision,
                "reasoning": reasoning,
                "alternatives": alternatives or []
            }
        )

    def record_artifact(self, name: str, path: str, description: str = ""):
        """Record an artifact produced during testing."""
        self.log_event(
            EventType.ARTIFACT,
            f"Artifact created: {name}",
            {
                "artifact_name": name,
                "path": path,
                "description": description
            }
        )

    @contextmanager
    def phase(self, phase_name: str):
        """Context manager for test phases."""
        phase_start = time.time()
        self.current_phase = phase_name
        self.log_event(
            EventType.PHASE_START,
            f"Starting phase: {phase_name}",
            {"phase": phase_name}
        )

        try:
            yield
        finally:
            phase_end = time.time()
            duration = phase_end - phase_start
            self.log_event(
                EventType.PHASE_END,
                f"Completed phase: {phase_name}",
                {
                    "phase": phase_name,
                    "duration_seconds": duration
                }
            )
            self.current_phase = None

    def error(self, message: str, exception: Optional[Exception] = None):
        """Log an error."""
        error_data = {"message": message}
        if exception:
            error_data["exception"] = str(exception)
            error_data["exception_type"] = type(exception).__name__

        self.log_event(
            EventType.ERROR,
            message,
            error_data,
            Severity.ERROR
        )

    def _write_summary(self):
        """Write summary file."""
        summary = {
            "test_name": self.test_name,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "duration_seconds": (self.end_time or 0) - (self.start_time or 0),
            "total_events": len(self.events),
            "total_observations": len(self.observations),
            "metrics": self.metrics,
            "output_dir": str(self.output_dir),
        }

        with open(self.summary_file, "w") as f:
            json.dumps(summary, f, indent=2)

    def get_summary(self) -> Dict[str, Any]:
        """Get current test summary."""
        duration = 0
        if self.start_time:
            end = self.end_time or time.time()
            duration = end - self.start_time

        return {
            "test_name": self.test_name,
            "duration_seconds": duration,
            "total_events": len(self.events),
            "total_observations": len(self.observations),
            "metrics": self.metrics.copy(),
            "current_phase": self.current_phase,
        }

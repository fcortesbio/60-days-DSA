#!/usr/bin/env python3
"""
Data structures for 60-days DSA implementations.

This module provides dataclasses and type definitions used across different
algorithm implementations for consistent data handling.

Author: Andres
Date: October 2025
"""

from dataclasses import dataclass
from typing import Callable, Any, Optional, Union


@dataclass
class TestCase:
    """Structure for algorithm test case data."""

    array: list[int]
    expected: Union[int, float, list, Any]
    name: str
    description: Optional[str] = None

    def __post_init__(self):
        """Validate test case data after initialization."""
        if not self.name:
            raise ValueError("Test case name cannot be empty")


@dataclass
class BenchmarkResult:
    """Structure for algorithm benchmark results."""

    function: Callable
    time: float
    memory_usage: Optional[float] = None
    iterations: Optional[int] = None

    @property
    def function_name(self) -> str:
        """Get the function name for display purposes."""
        return self.function.__name__

    @property
    def avg_time_per_call(self) -> float:
        """Calculate average time per call if iterations are available."""
        if self.iterations and self.iterations > 0:
            return self.time / self.iterations
        return self.time


@dataclass
class PerformanceComparison:
    """Structure for comparing multiple algorithm implementations."""

    algorithm_name: str
    complexity: str
    benchmark_results: list[BenchmarkResult]
    best_case_time: Optional[float] = None
    worst_case_time: Optional[float] = None
    average_time: Optional[float] = None

    def __post_init__(self):
        """Calculate statistics from benchmark results."""
        if self.benchmark_results:
            times = [result.time for result in self.benchmark_results]
            self.best_case_time = min(times)
            self.worst_case_time = max(times)
            self.average_time = sum(times) / len(times)


@dataclass
class ValidationResult:
    """Structure for algorithm validation results."""

    function_name: str
    test_case: TestCase
    actual_result: Any
    passed: bool
    error_message: Optional[str] = None
    execution_time: Optional[float] = None

    @property
    def status_emoji(self) -> str:
        """Get emoji representation of test status."""
        return "✅" if self.passed else "❌"

    @property
    def status_text(self) -> str:
        """Get text representation of test status."""
        return "PASS" if self.passed else "FAIL"


# Type aliases for common use cases
AlgorithmFunction = Callable[[list[int]], Union[int, float, list]]
TestSuite = list[TestCase]
BenchmarkSuite = list[BenchmarkResult]
ValidationSuite = list[ValidationResult]

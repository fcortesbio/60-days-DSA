#!/usr/bin/env python3
"""
60-days DSA Utilities Package

Common utilities and structures for Data Structures and Algorithms implementations.
Provides reusable components for testing, benchmarking, and analysis across all days.

Author: Andres
Date: October 2025
"""

# Import commonly used components for convenience
from .models import TestCase, BenchmarkResult
from .config import *
from .benchmark import format_time, benchmark_functions, analyze_performance
from .testing import run_validation_tests

__version__ = "1.0.0"
__all__ = [
    "TestCase", 
    "BenchmarkResult",
    "format_time",
    "benchmark_functions", 
    "analyze_performance",
    "run_validation_tests",
    # Configuration constants will be imported via *
]
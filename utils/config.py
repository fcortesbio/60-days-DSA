#!/usr/bin/env python3
"""
Configuration constants for 60-days DSA implementations.

This module contains shared configuration values used across different
algorithm implementations for consistent testing and benchmarking.

Author: Andres
Date: October 2025
"""

# Array sizes for testing
STANDARD_ARRAY_SIZE = 100
LARGE_ARRAY_SIZE = 1500
EXTRA_LARGE_ARRAY_SIZE = 30000

# Benchmarking parameters
STANDARD_REPLICAS = 1000
LARGE_REPLICAS = 100
EXTRA_LARGE_REPLICAS = 10

# Display formatting
SECTION_WIDTH = 70
SUBSECTION_WIDTH = 50
FUNCTION_NAME_WIDTH = 30
LARGE_FUNCTION_NAME_WIDTH = 40

# Performance thresholds (in seconds)
SLOW_THRESHOLD = 1.0
MEDIUM_THRESHOLD = 0.001

# Default test arrays for quick validation
DEFAULT_TEST_ARRAYS = {
    "small": [1, 2, 3],
    "medium": [2, 1, 3, 4],
    "negative": [-1, 2, -3],
    "zeros": [0, 1, 0, 2],
    "single": [42],
    "empty": [],
}

# Algorithm complexity categories for analysis
COMPLEXITY_MAP = {
    # Time complexities
    "O(1)": "Constant",
    "O(log n)": "Logarithmic", 
    "O(n)": "Linear",
    "O(n log n)": "Linearithmic",
    "O(n²)": "Quadratic",
    "O(n³)": "Cubic",
    "O(2^n)": "Exponential",
    "O(n!)": "Factorial",
}

# Medal emojis for rankings
RANKING_MEDALS = ["🥇", "🥈", "🥉"]
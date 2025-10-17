#!/usr/bin/env python3
from __future__ import annotations  # For Python 3.9+ list[int] syntax
import numpy as np
import sys
import os

# Add parent directory to path for utils import
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import (
    TestCase,
    BenchmarkResult,
    STANDARD_ARRAY_SIZE,
    LARGE_ARRAY_SIZE,
    STANDARD_REPLICAS,
    LARGE_REPLICAS,
    benchmark_functions,
    analyze_performance,
    run_validation_tests,
)

"""
Day 1: Subarray Sums & Range Queries
Python Implementation

Author: Andres
Date: October 2025
"""


def naive_brute_force(arr: list[int]) -> int:
    """
    Calculates sum of all subarray sums using triple nested loops.

    Args:
        arr: List of integers

    Returns:
        int: Sum of all possible subarray sums

    Time Complexity: O(n³)
    Space Complexity: O(1)
    """
    n: int = len(arr)
    total_sum: int = 0
    for i in range(n):
        for j in range(i, n):
            # Explicit third loop for consistency with JS/Java
            subarray_sum: int = 0
            for k in range(i, j + 1):
                subarray_sum += arr[k]
            total_sum += subarray_sum
    return total_sum


def optimized_brute_force(arr: list[int]) -> int:
    """
    Calculates sum of all subarray sums using running sum technique.

    Args:
        arr: List of integers

    Returns:
        int: Sum of all possible subarray sums

    Time Complexity: O(n²)
    Space Complexity: O(1)
    """
    n: int = len(arr)
    total_sum: int = 0
    for i in range(n):
        current_subarray_sum: int = 0
        for j in range(i, n):
            current_subarray_sum += arr[j]
            total_sum += current_subarray_sum
    return total_sum


def contribution_technique(arr: list[int]) -> int:
    """
    Calculates sum of all subarray sums using element contribution method.

    For each element at position i, counts how many subarrays contain it:
    (i + 1) choices for start position × (n - i) choices for end position

    Args:
        arr: List of integers

    Returns:
        int: Sum of all possible subarray sums

    Time Complexity: O(n)
    Space Complexity: O(1)
    """
    n: int = len(arr)
    total_sum: int = 0
    for i in range(n):
        contribution: int = arr[i] * (i + 1) * (n - i)
        total_sum += contribution
    return total_sum


def vectorized_contribution(arr: list[int]) -> int:
    """
    Calculates sum of all subarray sums using precomputed contributions array.

    Args:
        arr: List of integers

    Returns:
        int: Sum of all possible subarray sums

    Time Complexity: O(n)
    Space Complexity: O(n) for contributions array
    """
    n: int = len(arr)
    contributions: list[int] = [(k + 1) * (n - k) for k in range(n)]
    return sum(arr[i] * contributions[i] for i in range(n))


def vector_half_contribution(arr: list[int]) -> int:
    """
    Calculates sum of all subarray sums using symmetric contributions optimization.

    Exploits the symmetric pattern of contribution coefficients to compute only
    half the array and mirror it, then calculates dot product with input array.

    Args:
        arr: List of integers

    Returns:
        int: Sum of all possible subarray sums

    Time Complexity: O(n)
    Space Complexity: O(n) for contributions array
    """
    n: int = len(arr)
    m: int = (n + 1) // 2  # ceiling division for midpoint

    # Compute first half of contributions using list comprehension
    first_half: list[int] = [(k + 1) * (n - k) for k in range(m)]

    # Create mirror based on array length parity
    mirror: list[int] = first_half[::-1] if n % 2 == 0 else first_half[:-1][::-1]
    contributions: list[int] = first_half + mirror

    return sum(arr[i] * contributions[i] for i in range(n))


def _numpy_contribution(
    arr: list[int] | np.ndarray, use_half_optimization: bool = False
) -> int:
    """
    Helper function for NumPy-based subarray sum calculations.

    Args:
        arr: List or NumPy array of integers
        use_half_optimization: Whether to use symmetric optimization

    Returns:
        int: Sum of all possible subarray sums
    """
    arr = np.array(arr, dtype=np.int64)
    n = len(arr)

    if use_half_optimization:
        m = (n + 1) // 2  # ceiling division
        # Compute first half contributions directly as a vector
        k = np.arange(m)
        first_half = (k + 1) * (n - k)

        # Build the symmetric full contribution array
        mirror = first_half[::-1] if n % 2 == 0 else first_half[:-1][::-1]
        contributions = np.concatenate((first_half, mirror))
    else:
        # Compute full contributions array directly as vector operation
        k = np.arange(n)
        contributions = (k + 1) * (n - k)

    # Compute the dot product (arr · contributions)
    return int(np.dot(arr, contributions))


def vector_numpy_half_contribution(arr: list[int] | np.ndarray) -> int:
    """
    Calculates sum of all subarray sums using NumPy with symmetric optimization.

    Time Complexity: O(n)
    Space Complexity: O(n)
    """
    return _numpy_contribution(arr, use_half_optimization=True)


def vector_numpy_full_contribution(arr: list[int] | np.ndarray) -> int:
    """
    Calculates sum of all subarray sums using full NumPy vectorization.

    Time Complexity: O(n)
    Space Complexity: O(n)
    """
    return _numpy_contribution(arr, use_half_optimization=False)


# ----------------------------------------------------------------------


def main() -> None:
    """Main execution function for testing - consistent with JS/Java."""
    # Define core algorithm functions (same 5 as JS/Java)
    functions = [
        naive_brute_force,
        optimized_brute_force,
        contribution_technique,
        vectorized_contribution,
        vector_half_contribution,
    ]

    # Define test cases (same as JS/Java)
    test_cases = [
        TestCase(array=[1, 2, 3], expected=20, name="Basic example [1,2,3]"),
        TestCase(array=[2, 1, 3], expected=19, name="Reordered [2,1,3]"),
        TestCase(array=[5], expected=5, name="Single element [5]"),
        TestCase(array=[], expected=0, name="Empty array"),
        TestCase(array=[-1, 2, -3], expected=-4, name="Mixed signs [-1,2,-3]"),
        TestCase(array=[3, 3, 3], expected=30, name="Repeated elements [3,3,3]"),
    ]

    print("🧪 Running DSA Solution Tests...")
    print("=" * 50)
    
    # Run validation tests only (like JS/Java)
    run_validation_tests(functions, test_cases, verbose=True)
    


    # Smaller arrays for benchmarking to avoid performance issues
    print("⚡ Performance Benchmarking...")
    print("=" * 50)
    
    # Small-scale benchmarking
    small_array = list(range(100))  # Reduced from 500
    small_results = benchmark_functions(functions, small_array, 100)  # Reduced replicas
    analyze_performance(small_results, len(small_array))

    # Large-scale benchmarking (contribution algorithms only)
    contribution_functions = [
        contribution_technique,
        vectorized_contribution,
        vector_half_contribution,
        vector_numpy_full_contribution,
        vector_numpy_half_contribution,
    ]

    large_array = list(range(10000))  # Reduced from 50000
    large_results = benchmark_functions(
        contribution_functions, large_array, 50  # Reduced replicas
    )
    analyze_performance(large_results, len(large_array))


if __name__ == "__main__":
    main()


# ----------------------------------------------------------------------

# Concept 2 (Pending): Range Sum Queries

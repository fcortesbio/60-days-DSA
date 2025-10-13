#!/usr/bin/env python3
from __future__ import annotations  # For Python 3.9+ list[int] syntax
import numpy as np
import timeit
import time
from dataclasses import dataclass
from typing import Callable

"""
Day 1: Subarray Sums & Range Queries
Python Implementation

Author: Andres
Date: October 2025
"""

# Configuration constants
STANDARD_ARRAY_SIZE = 99
LARGE_ARRAY_SIZE = 1000
STANDARD_REPLICAS = 1000
LARGE_REPLICAS = 100
SECTION_WIDTH = 70

@dataclass
class TestCase:
    """Structure for test case data"""
    array: list[int]
    expected: int
    name: str

@dataclass
class BenchmarkResult:
    """Structure for benchmark results"""
    function: Callable
    time: float


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
            # Third loop implicit in sum() function
            subarray_sum: int = sum(arr[i : j + 1])
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
        left_choices: int = i + 1  # positions where subarray can start
        right_choices: int = n - i  # positions where subarray can end
        contribution: int = arr[i] * left_choices * right_choices
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


def _numpy_contribution(arr: list[int] | np.ndarray, use_half_optimization: bool = False) -> int:
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


# Utility functions
def format_time(seconds: float) -> str:
    """Convert seconds to human-readable format."""
    if seconds >= 1.0:
        return f"{seconds:.3f} s"
    elif seconds >= 0.001:
        return f"{seconds * 1000:.2f} ms"
    else:
        return f"{seconds * 1000000:.1f} μs"


def run_validation_tests(functions: list[Callable], test_cases: list[TestCase]) -> bool:
    """Run validation tests for all functions."""
    print("=" * SECTION_WIDTH)
    print("🔬 SUBARRAY SUMS ALGORITHM VALIDATION & BENCHMARKING")
    print("=" * SECTION_WIDTH)
    
    all_tests_passed = True
    
    for test_case in test_cases:
        print(f"\n📋 {test_case.name} → Expected: {test_case.expected}")
        print("-" * 50)
        
        test_passed = True
        for function in functions:
            result = function(test_case.array)
            status = "✅ PASS" if result == test_case.expected else "❌ FAIL"
            print(f"{function.__name__:25} : {result:6d} {status}")
            if result != test_case.expected:
                test_passed = False
                all_tests_passed = False
        
        print(f"\n🎯 Overall: {'✅ ALL TESTS PASSED' if test_passed else '❌ SOME TESTS FAILED'}")
        time.sleep(0.5)
    
    return all_tests_passed


def benchmark_functions(functions: list[Callable], test_array: list[int], replicas: int) -> list[BenchmarkResult]:
    """Benchmark all functions and return results."""
    print("\n" + "=" * SECTION_WIDTH)
    print("⚡ PERFORMANCE BENCHMARKING")
    print("=" * SECTION_WIDTH)
    
    print(f"\n📊 Testing with array size: {len(test_array)} elements")
    print(f"🔄 Replications per test: {replicas:,}")
    print(f"⏱️  Timer: {time.perf_counter.__name__}")
    print("-" * SECTION_WIDTH)
    
    results = []
    for function in functions:
        timing = timeit.timeit(
            lambda f=function: f(test_array), 
            number=replicas, 
            timer=time.perf_counter
        )
        results.append(BenchmarkResult(function=function, time=timing))
        avg_per_call = timing / replicas
        print(
            f"{function.__name__:25} : {format_time(timing):>10} total | {format_time(avg_per_call):>10} avg"
        )
    
    return results


def analyze_performance(results: list[BenchmarkResult], array_size: int) -> None:
    """Analyze and display performance results."""
    print("\n" + "=" * SECTION_WIDTH)
    print("📈 PERFORMANCE ANALYSIS")
    print("=" * SECTION_WIDTH)
    
    # Sort by performance (fastest first)
    results.sort(key=lambda x: x.time)
    fastest = results[0].time
    
    print(f"\n🏆 Performance Ranking (fastest to slowest):")
    print("-" * 50)
    
    complexity_map = {
        "naive_brute_force": "O(n³)",
        "optimized_brute_force": "O(n²)",
        "contribution_technique": "O(n)",
        "vectorized_contribution": "O(n)",
        "vector_half_contribution": "O(n)",
        "vector_numpy_full_contribution": "O(n)",
        "vector_numpy_half_contribution": "O(n)",
    }
    
    for i, result in enumerate(results, 1):
        func = result.function
        timing = result.time
        speedup = timing / fastest
        complexity = complexity_map.get(func.__name__, "O(?)")
        medal = ["🥇", "🥈", "🥉"][i - 1] if i <= 3 else f"{i}."
        
        print(
            f"{medal} {func.__name__:25} | {complexity:>6} | {speedup:5.1f}x slower | {format_time(timing)}"
        )
    
    # Key insights
    print(f"\n💡 Key Insights:")
    print(f"   • Fastest algorithm: {results[0].function.__name__}")
    print(f"   • O(n) algorithms perform {results[-1].time / fastest:.0f}x faster than O(n³)")
    print(f"   • NumPy overhead dominates for small arrays (n={array_size})")


# ----------------------------------------------------------------------


def main() -> None:
    """Main execution function."""
    # Define test data and functions
    functions = [
        naive_brute_force,
        optimized_brute_force,
        contribution_technique,
        vectorized_contribution,
        vector_half_contribution,
        vector_numpy_full_contribution,
        vector_numpy_half_contribution,
    ]
    
    test_cases = [
        TestCase(array=[1, 2, 3], expected=20, name="Test 1: [1, 2, 3]"),
        TestCase(array=[2, 1, 3], expected=19, name="Test 2: [2, 1, 3]"),
    ]
    
    # Run validation tests
    run_validation_tests(functions, test_cases)
    
    # Standard benchmarking
    standard_array = list(range(STANDARD_ARRAY_SIZE))
    standard_results = benchmark_functions(functions, standard_array, STANDARD_REPLICAS)
    analyze_performance(standard_results, STANDARD_ARRAY_SIZE)
    
    # Large-scale benchmarking (contribution algorithms only)
    contribution_functions = [
        contribution_technique,
        vectorized_contribution,
        vector_half_contribution,
        vector_numpy_full_contribution,
        vector_numpy_half_contribution,
    ]
    
    large_array = list(range(LARGE_ARRAY_SIZE))
    large_results = benchmark_functions(contribution_functions, large_array, LARGE_REPLICAS)
    analyze_performance(large_results, LARGE_ARRAY_SIZE)


if __name__ == "__main__":
    main()


# ----------------------------------------------------------------------

# Concept 2 (Pending): Range Sum Queries

#!/usr/bin/env python3
from __future__ import annotations  # For Python 3.9+ list[int] syntax
import numpy as np
import timeit
import time

"""
Day 1: Subarray Sums & Range Queries
Python Implementation

Author: Andres
Date: October 2024
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
    Calculates sum of all subarray sums using precomputed symmetric contributions array.

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
    contributions: list[int] = []

    for k in range(n):
        contributions.append((k + 1) * (n - k))

    # Calculate dot product
    total_sum: int = 0
    for i in range(n):
        total_sum += arr[i] * contributions[i]

    return total_sum


def vector_half_contribution(arr: list[int]) -> int:
    """
    Calculates sum of all subarray sums using precomputed symmetric contributions array.

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

    # Compute first half of contributions
    first_half: list[int] = []
    for k in range(m):
        first_half.append((k + 1) * (n - k))

    # Create mirror based on array length parity
    if n % 2 == 0:
        # Even: mirror entire first half
        mirror: list[int] = first_half[::-1]
    else:
        # Odd: mirror all except center element (last in first_half)
        mirror: list[int] = first_half[:-1][::-1]

    contributions: list[int] = first_half + mirror

    # Calculate dot product
    total_sum: int = 0
    for i in range(n):
        total_sum += arr[i] * contributions[i]

    return total_sum


def vector_numpy_half_contribution(arr: list[int] | np.ndarray) -> int:
    """
    Calculates sum of all subarray sums using NumPy with symmetric optimization.

    Uses symmetric pattern to compute only half the contributions array,
    then mirrors it. This tests the cost of array operations vs computation.

    Args:
        arr: List or NumPy array of integers

    Returns:
        int: Sum of all possible subarray sums

    Time Complexity: O(n)
    Space Complexity: O(n)
    """
    arr = np.array(arr, dtype=np.int64)
    n = len(arr)
    m = (n + 1) // 2  # ceiling division

    # Compute first half contributions directly as a vector
    k = np.arange(m)  # [0, 1, 2, ...]
    first_half = (k + 1) * (n - k)

    # Build the symmetric full contribution array
    if n % 2 == 0:
        mirror = first_half[::-1]
    else:
        mirror = first_half[:-1][::-1]

    contributions = np.concatenate((first_half, mirror))

    # Compute the dot product (arr · contributions)
    total_sum = np.dot(arr, contributions)
    return int(total_sum)


def vector_numpy_full_contribution(arr: list[int] | np.ndarray) -> int:
    """
    Calculates sum of all subarray sums using full NumPy vectorization.

    Computes the entire contributions array directly without symmetric
    optimization to test pure NumPy vectorization performance.

    Args:
        arr: List or NumPy array of integers

    Returns:
        int: Sum of all possible subarray sums

    Time Complexity: O(n)
    Space Complexity: O(n)
    """
    arr = np.array(arr, dtype=np.int64)
    n = len(arr)

    # Compute full contributions array directly as vector operation
    k = np.arange(n)  # [0, 1, 2, ..., n-1]
    contributions = (k + 1) * (n - k)

    # Compute the dot product (arr · contributions)
    total_sum = np.dot(arr, contributions)
    return int(total_sum)


# ----------------------------------------------------------------------


if __name__ == "__main__":
    # Test data
    input_array_1: list[int] = [1, 2, 3]
    input_array_2: list[int] = [2, 1, 3]
    input_array_bulk: list[int] = [i for i in range(0, 99)]

    functions = [
        naive_brute_force,
        optimized_brute_force,
        contribution_technique,
        vectorized_contribution,  # Full array computation (Python)
        vector_half_contribution,  # Half + mirror optimization (Python)
        vector_numpy_full_contribution,  # Full array computation (NumPy)
        vector_numpy_half_contribution,  # Half + mirror optimization (NumPy)
    ]

    print("=" * 70)
    print("🔬 SUBARRAY SUMS ALGORITHM VALIDATION & BENCHMARKING")
    print("=" * 70)

    # Test cases with validation
    test_cases = [
        {"array": input_array_1, "expected": 20, "name": "Test 1: [1, 2, 3]"},
        {
            "array": input_array_2,
            "expected": 19,
            "name": "Test 2: [2, 1, 3]",
        },  # Fixed expected value
    ]

    for test_case in test_cases:
        print(f"\n📋 {test_case['name']} → Expected: {test_case['expected']}")
        print("-" * 50)

        all_passed = True
        for function in functions:
            result = function(test_case["array"])
            status = "✅ PASS" if result == test_case["expected"] else "❌ FAIL"
            print(f"{function.__name__:25} : {result:6d} {status}")
            if result != test_case["expected"]:
                all_passed = False

        print(
            f"\n🎯 Overall: {'✅ ALL TESTS PASSED' if all_passed else '❌ SOME TESTS FAILED'}"
        )
        time.sleep(0.5)

    print("\n" + "=" * 70)
    print("⚡ PERFORMANCE BENCHMARKING")
    print("=" * 70)

    # Benchmarking setup
    test_timer = time.perf_counter
    replicas = 1000
    array_size = len(input_array_bulk)

    def test_implementation(function, array):
        return timeit.timeit(lambda: function(array), number=replicas, timer=test_timer)

    def format_time(seconds: float) -> str:
        """Convert seconds to human-readable format"""
        if seconds >= 1.0:
            return f"{seconds:.3f} s"
        elif seconds >= 0.001:
            return f"{seconds * 1000:.2f} ms"
        else:
            return f"{seconds * 1000000:.1f} μs"

    print(f"\n📊 Testing with array size: {array_size} elements")
    print(f"🔄 Replications per test: {replicas:,}")
    print(f"⏱️  Timer: {test_timer.__name__}")
    print("-" * 70)

    # Collect timing results
    results = []
    for function in functions:
        timing = test_implementation(function, input_array_bulk)
        results.append({"function": function, "time": timing})
        avg_per_call = timing / replicas
        print(
            f"{function.__name__:25} : {format_time(timing):>10} total | {format_time(avg_per_call):>10} avg"
        )

    # Performance analysis
    print("\n" + "=" * 70)
    print("📈 PERFORMANCE ANALYSIS")
    print("=" * 70)

    # Sort by performance (fastest first)
    results.sort(key=lambda x: x["time"])
    fastest = results[0]["time"]

    print(f"\n🏆 Performance Ranking (fastest to slowest):")
    print("-" * 50)

    for i, result in enumerate(results, 1):
        func = result["function"]
        timing = result["time"]
        speedup = timing / fastest

        complexity = {
            "naive_brute_force": "O(n³)",
            "optimized_brute_force": "O(n²)",
            "contribution_technique": "O(n)",
            "vectorized_contribution": "O(n)",
            "vector_half_contribution": "O(n)",
            "vector_numpy_full_contribution": "O(n)",
            "vector_numpy_half_contribution": "O(n)",
        }.get(func.__name__, "O(?)")

        medal = ["🥇", "🥈", "🥉"][i - 1] if i <= 3 else f"{i}."

        print(
            f"{medal} {func.__name__:25} | {complexity:>6} | {speedup:5.1f}x slower | {format_time(timing)}"
        )

    print(f"\n💡 Key Insights:")
    print(f"   • Fastest algorithm: {results[0]['function'].__name__}")
    print(
        f"   • O(n) algorithms perform {results[-1]['time'] / fastest:.0f}x faster than O(n³)"
    )
    print(f"   • NumPy overhead dominates for small arrays (n={array_size})")

    # Find Python vs NumPy implementations for comparison
    python_algos = [
        r
        for r in results
        if "numpy" not in r["function"].__name__
        and r["function"].__name__ != "naive_brute_force"
        and r["function"].__name__ != "optimized_brute_force"
    ]
    numpy_algos = [r for r in results if "numpy" in r["function"].__name__]

    if python_algos and numpy_algos:
        fastest_python = min(python_algos, key=lambda x: x["time"])
        fastest_numpy = min(numpy_algos, key=lambda x: x["time"])
        overhead = fastest_numpy["time"] / fastest_python["time"]
        print(
            f"   • NumPy adds {overhead:.1f}x overhead vs pure Python for this problem size"
        )

    # Compare optimization strategies
    full_algos = [
        r
        for r in results
        if "vectorized_contribution" in r["function"].__name__
        or "numpy_full" in r["function"].__name__
    ]
    half_algos = [r for r in results if "half" in r["function"].__name__]

    if full_algos and half_algos:
        avg_full = sum(r["time"] for r in full_algos) / len(full_algos)
        avg_half = sum(r["time"] for r in half_algos) / len(half_algos)
        if avg_half < avg_full:
            print(
                f"   • Half-array + mirror optimization saves {(1 - avg_half / avg_full) * 100:.1f}% computation time"
            )
        else:
            print(
                f"   • Full computation is {(1 - avg_full / avg_half) * 100:.1f}% faster than half + mirror approach"
            )

    print(
        f"   • Python 3.13+ JIT compilation may favor simple loops over NumPy for small data"
    )

    # Large-scale benchmark for contribution algorithms only
    print("\n" + "=" * 70)
    print("🚀 LARGE-SCALE BENCHMARK: Contribution Algorithms")
    print("=" * 70)

    # Test with larger array to see NumPy crossover point
    large_array: list[int] = list(range(1000))
    large_replicas = 100  # Fewer replicas due to larger computation

    contribution_functions = [
        contribution_technique,
        vectorized_contribution,
        vector_half_contribution,
        vector_numpy_full_contribution,
        vector_numpy_half_contribution,
    ]

    print(f"\n📊 Large-scale testing:")
    print(f"   Array size: {len(large_array):,} elements")
    print(f"   Replications: {large_replicas} (reduced for larger computation)")
    print(f"   Focus: O(n) contribution algorithms only")
    print("-" * 70)

    # Collect large-scale results
    large_results = []
    for function in contribution_functions:
        timing = timeit.timeit(
            lambda f=function: f(large_array), number=large_replicas, timer=test_timer
        )
        large_results.append({"function": function, "time": timing})
        avg_per_call = timing / large_replicas
        print(
            f"{function.__name__:30} : {format_time(timing):>10} total | {format_time(avg_per_call):>10} avg"
        )

    # Large-scale analysis
    print("\n" + "=" * 70)
    print("📈 LARGE-SCALE PERFORMANCE ANALYSIS")
    print("=" * 70)

    # Sort by performance (fastest first)
    large_results.sort(key=lambda x: x["time"])
    fastest_large = large_results[0]["time"]

    print(f"\n🏆 Large-scale Performance Ranking:")
    print("-" * 50)

    for i, result in enumerate(large_results, 1):
        func = result["function"]
        timing = result["time"]
        speedup = timing / fastest_large

        medal = ["🥇", "🥈", "🥉"][i - 1] if i <= 3 else f"{i}."
        impl_type = "NumPy" if "numpy" in func.__name__ else "Python"
        opt_type = (
            "Half+Mirror"
            if "half" in func.__name__
            else "Full Compute"
            if "vectorized" in func.__name__
            else "Direct"
        )

        print(
            f"{medal} {func.__name__:30} | {impl_type:6} | {opt_type:11} | {speedup:4.1f}x | {format_time(timing)}"
        )

    # Compare small vs large scale performance
    print(f"\n🔍 Scale Comparison Analysis:")
    print("-" * 50)

    # Find matching algorithms in both scales
    small_dict = {r["function"].__name__: r["time"] for r in results}
    large_dict = {r["function"].__name__: r["time"] for r in large_results}

    print(
        f"{'Algorithm':30} | {'Small (n=99)':12} | {'Large (n=1000)':13} | {'Scale Factor':12}"
    )
    print("-" * 70)

    for func_name in ["contribution_technique", "vector_numpy_full_contribution"]:
        if func_name in small_dict and func_name in large_dict:
            small_time = small_dict[func_name] / replicas  # per-call time
            large_time = large_dict[func_name] / large_replicas  # per-call time
            scale_factor = large_time / small_time

            print(
                f"{func_name:30} | {format_time(small_time):>10} | {format_time(large_time):>11} | {scale_factor:>10.1f}x"
            )

    # Final insights for large scale
    print(f"\n💡 Large-Scale Insights:")
    fastest_large_name = large_results[0]["function"].__name__
    print(f"   • Winner at n=1000: {fastest_large_name}")

    # Compare Python vs NumPy at large scale
    python_large = [r for r in large_results if "numpy" not in r["function"].__name__]
    numpy_large = [r for r in large_results if "numpy" in r["function"].__name__]

    if python_large and numpy_large:
        best_python_large = min(python_large, key=lambda x: x["time"])
        best_numpy_large = min(numpy_large, key=lambda x: x["time"])

        if best_numpy_large["time"] < best_python_large["time"]:
            speedup = best_python_large["time"] / best_numpy_large["time"]
            print(f"   • NumPy is {speedup:.2f}x faster than Python at n=1,000")
        else:
            speedup = best_numpy_large["time"] / best_python_large["time"]
            print(f"   • Python is still {speedup:.2f}x faster than NumPy at n=1,000")

    print(f"   • Crossover point: NumPy becomes advantageous around n=1,000")
    print(f"   • Algorithm choice depends on both complexity AND data size")
    print(f"   • Modern Python JIT compilation is remarkably effective")


# ----------------------------------------------------------------------

# Concept 2 (Pending): Range Sum Queries

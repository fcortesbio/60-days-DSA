#!/usr/bin/env python3
"""
Benchmarking utilities for 60-days DSA implementations.

This module provides functions for measuring and analyzing algorithm performance
across different implementations and data sizes.

Author: Andres
Date: October 2025
"""

import time
import timeit
from typing import Callable, Optional

from .models import BenchmarkResult, AlgorithmFunction
from .config import (
    SECTION_WIDTH, FUNCTION_NAME_WIDTH, RANKING_MEDALS,
    SLOW_THRESHOLD, MEDIUM_THRESHOLD
)


def format_time(seconds: float) -> str:
    """
    Convert seconds to human-readable format.
    
    Args:
        seconds: Time in seconds
        
    Returns:
        Formatted time string with appropriate units
    """
    if seconds >= 1.0:
        return f"{seconds:.3f} s"
    elif seconds >= MEDIUM_THRESHOLD:
        return f"{seconds * 1000:.2f} ms"
    else:
        return f"{seconds * 1000000:.1f} μs"


def benchmark_functions(
    functions: list[AlgorithmFunction], 
    test_array: list[int], 
    replicas: int,
    timer: Optional[Callable] = None
) -> list[BenchmarkResult]:
    """
    Benchmark multiple functions and return performance results.
    
    Args:
        functions: List of functions to benchmark
        test_array: Array to test functions with
        replicas: Number of times to run each function
        timer: Timer function to use (defaults to time.perf_counter)
        
    Returns:
        List of BenchmarkResult objects with timing data
    """
    if timer is None:
        timer = time.perf_counter
    
    print("\n" + "=" * SECTION_WIDTH)
    print("⚡ PERFORMANCE BENCHMARKING")
    print("=" * SECTION_WIDTH)
    
    print(f"\n📊 Testing with array size: {len(test_array)} elements")
    print(f"🔄 Replications per test: {replicas:,}")
    print(f"⏱️  Timer: {timer.__name__}")
    print("-" * SECTION_WIDTH)
    
    results = []
    for function in functions:
        try:
            timing = timeit.timeit(
                lambda f=function: f(test_array), 
                number=replicas, 
                timer=timer
            )
            result = BenchmarkResult(
                function=function, 
                time=timing,
                iterations=replicas
            )
            results.append(result)
            
            avg_per_call = timing / replicas
            print(
                f"{function.__name__:{FUNCTION_NAME_WIDTH}} : "
                f"{format_time(timing):>10} total | "
                f"{format_time(avg_per_call):>10} avg"
            )
            
        except Exception as e:
            print(f"{function.__name__:{FUNCTION_NAME_WIDTH}} : ERROR - {str(e)}")
            # Still add a result with error information
            results.append(BenchmarkResult(
                function=function, 
                time=float('inf'),
                iterations=replicas
            ))
    
    return results


def analyze_performance(
    results: list[BenchmarkResult], 
    array_size: int,
    complexity_map: Optional[dict[str, str]] = None
) -> None:
    """
    Analyze and display performance results with detailed insights.
    
    Args:
        results: List of benchmark results
        array_size: Size of array used in testing
        complexity_map: Optional mapping of function names to complexity strings
    """
    if not results:
        print("No results to analyze")
        return
    
    print("\n" + "=" * SECTION_WIDTH)
    print("📈 PERFORMANCE ANALYSIS")
    print("=" * SECTION_WIDTH)
    
    # Filter out failed results and sort by performance
    valid_results = [r for r in results if r.time != float('inf')]
    failed_results = [r for r in results if r.time == float('inf')]
    
    if not valid_results:
        print("❌ No valid results to analyze")
        return
    
    valid_results.sort(key=lambda x: x.time)
    fastest = valid_results[0].time
    
    print(f"\n🏆 Performance Ranking (fastest to slowest):")
    print("-" * 50)
    
    # Default complexity mapping
    if complexity_map is None:
        complexity_map = {
            "naive_brute_force": "O(n³)",
            "optimized_brute_force": "O(n²)",
            "contribution_technique": "O(n)",
            "vectorized_contribution": "O(n)",
            "vector_half_contribution": "O(n)",
            "vector_numpy_full_contribution": "O(n)",
            "vector_numpy_half_contribution": "O(n)",
        }
    
    for i, result in enumerate(valid_results, 1):
        func = result.function
        timing = result.time
        speedup = timing / fastest if fastest > 0 else 1
        complexity = complexity_map.get(func.__name__, "O(?)")
        
        # Assign medal or number
        if i <= len(RANKING_MEDALS):
            medal = RANKING_MEDALS[i - 1]
        else:
            medal = f"{i}."
        
        print(
            f"{medal} {func.__name__:{FUNCTION_NAME_WIDTH}} | "
            f"{complexity:>6} | {speedup:5.1f}x slower | "
            f"{format_time(timing)}"
        )
    
    # Show failed functions
    if failed_results:
        print(f"\n❌ Failed Functions:")
        for result in failed_results:
            print(f"   • {result.function.__name__}: Execution error")
    
    # Performance insights
    print(f"\n💡 Key Insights:")
    if len(valid_results) > 1:
        fastest_name = valid_results[0].function.__name__
        slowest = valid_results[-1]
        slowest_speedup = slowest.time / fastest
        
        print(f"   • Fastest algorithm: {fastest_name}")
        print(f"   • Performance range: {slowest_speedup:.0f}x difference")
        print(f"   • Array size impact: n={array_size}")
        
        # Categorize by speed
        fast_count = sum(1 for r in valid_results if r.time < MEDIUM_THRESHOLD)
        slow_count = sum(1 for r in valid_results if r.time > SLOW_THRESHOLD)
        
        if fast_count > 0:
            print(f"   • Fast algorithms (< {format_time(MEDIUM_THRESHOLD)}): {fast_count}")
        if slow_count > 0:
            print(f"   • Slow algorithms (> {format_time(SLOW_THRESHOLD)}): {slow_count}")
    
    # Algorithm category analysis
    _analyze_algorithm_categories(valid_results, complexity_map)


def _analyze_algorithm_categories(
    results: list[BenchmarkResult], 
    complexity_map: dict[str, str]
) -> None:
    """
    Analyze performance by algorithm categories (internal helper).
    
    Args:
        results: Valid benchmark results
        complexity_map: Mapping of function names to complexities
    """
    # Group by implementation type
    python_algos = [
        r for r in results 
        if "numpy" not in r.function.__name__ 
        and "brute_force" not in r.function.__name__
    ]
    numpy_algos = [r for r in results if "numpy" in r.function.__name__]
    brute_force_algos = [r for r in results if "brute_force" in r.function.__name__]
    
    # Compare Python vs NumPy
    if python_algos and numpy_algos:
        fastest_python = min(python_algos, key=lambda x: x.time)
        fastest_numpy = min(numpy_algos, key=lambda x: x.time)
        
        if fastest_numpy.time < fastest_python.time:
            speedup = fastest_python.time / fastest_numpy.time
            print(f"   • NumPy advantage: {speedup:.1f}x faster than pure Python")
        else:
            overhead = fastest_numpy.time / fastest_python.time
            print(f"   • Python advantage: NumPy adds {overhead:.1f}x overhead")
    
    # Complexity analysis
    if brute_force_algos:
        linear_algos = [
            r for r in results 
            if complexity_map.get(r.function.__name__, "").startswith("O(n)")
            and "O(n²)" not in complexity_map.get(r.function.__name__, "")
            and "O(n³)" not in complexity_map.get(r.function.__name__, "")
        ]
        
        if linear_algos and brute_force_algos:
            fastest_linear = min(linear_algos, key=lambda x: x.time)
            slowest_brute = max(brute_force_algos, key=lambda x: x.time)
            improvement = slowest_brute.time / fastest_linear.time
            print(f"   • Algorithmic improvement: {improvement:.0f}x faster with optimal complexity")


def compare_scale_performance(
    small_results: list[BenchmarkResult],
    large_results: list[BenchmarkResult],
    small_size: int,
    large_size: int
) -> None:
    """
    Compare performance across different data sizes.
    
    Args:
        small_results: Results from small array testing
        large_results: Results from large array testing  
        small_size: Size of small test array
        large_size: Size of large test array
    """
    print(f"\n🔍 Scale Comparison Analysis:")
    print("-" * 50)
    
    # Create dictionaries for easy lookup
    small_dict = {r.function.__name__: r for r in small_results}
    large_dict = {r.function.__name__: r for r in large_results}
    
    # Find common functions
    common_functions = set(small_dict.keys()) & set(large_dict.keys())
    
    if not common_functions:
        print("No common functions found for comparison")
        return
    
    print(
        f"{'Algorithm':{FUNCTION_NAME_WIDTH}} | "
        f"{'Small (n=' + str(small_size) + ')':12} | "
        f"{'Large (n=' + str(large_size) + ')':13} | "
        f"{'Scale Factor':12}"
    )
    print("-" * SECTION_WIDTH)
    
    for func_name in sorted(common_functions):
        small_result = small_dict[func_name]
        large_result = large_dict[func_name]
        
        if (small_result.iterations and large_result.iterations and 
            small_result.iterations > 0 and large_result.iterations > 0):
            small_avg = small_result.time / small_result.iterations
            large_avg = large_result.time / large_result.iterations
            scale_factor = large_avg / small_avg if small_avg > 0 else float('inf')
            
            print(
                f"{func_name:{FUNCTION_NAME_WIDTH}} | "
                f"{format_time(small_avg):>10} | "
                f"{format_time(large_avg):>11} | "
                f"{scale_factor:>10.1f}x"
            )
    
    print(f"\n💡 Scale Analysis Insights:")
    print(f"   • Data size increased {large_size/small_size:.1f}x")
    print(f"   • Theoretical O(n) should scale linearly")
    print(f"   • Theoretical O(n²) should scale quadratically ({(large_size/small_size)**2:.0f}x)")
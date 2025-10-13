#!/usr/bin/env python3
"""
Example Usage of 60-days DSA Utilities

This file demonstrates how to use the shared utilities package
in future day implementations. Copy and modify as needed.

Author: Andres
Date: October 2025
"""

import sys
import os

# Add parent directory to path for utils import (if not in root)
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
from utils.testing import create_standard_test_cases


# Example algorithms for demonstration
def example_sum(arr: list[int]) -> int:
    """Example: Simple array sum - O(n)"""
    return sum(arr)


def example_sum_squares(arr: list[int]) -> int:
    """Example: Sum of squares - O(n)"""
    return sum(x * x for x in arr)


def example_nested_sum(arr: list[int]) -> int:
    """Example: Nested sum - O(n²)"""
    total = 0
    n = len(arr)
    for i in range(n):
        for j in range(i, n):
            total += arr[j]
    return total


def main() -> None:
    """Main execution function demonstrating utils usage."""

    # Step 1: Define your algorithms
    functions = [
        example_sum,
        example_sum_squares,
        example_nested_sum,
    ]

    # Step 2: Create test cases
    # Option A: Manual test cases
    manual_test_cases = [
        TestCase(array=[1, 2, 3], expected=6, name="Sum test [1,2,3]"),
        TestCase(array=[1, 2, 3], expected=14, name="Sum squares [1,2,3]"),
        TestCase(array=[1, 2, 3], expected=10, name="Nested sum [1,2,3]"),
    ]

    # Option B: Use standard test cases (for specific problem types)
    # standard_test_cases = create_standard_test_cases("subarray_sum")

    # Step 3: Validate algorithm correctness
    print("🧪 VALIDATION PHASE")
    validation_results = run_validation_tests(functions, manual_test_cases)

    # Check if validation passed
    all_passed = all(r.passed for r in validation_results)
    if not all_passed:
        print("❌ Some tests failed - fix algorithms before benchmarking")
        return

    # Step 4: Benchmark performance
    print("\n" + "=" * 70)
    print("🚀 BENCHMARKING PHASE")
    print("=" * 70)

    # Small-scale benchmarking
    small_array = list(range(STANDARD_ARRAY_SIZE))
    small_results = benchmark_functions(functions, small_array, STANDARD_REPLICAS)
    analyze_performance(small_results, len(small_array))

    # Large-scale benchmarking (optional)
    print(f"\n{'=' * 70}")
    print("🔥 LARGE-SCALE BENCHMARKING")
    print(f"{'=' * 70}")

    large_array = list(range(LARGE_ARRAY_SIZE))
    large_results = benchmark_functions(functions, large_array, LARGE_REPLICAS)
    analyze_performance(large_results, len(large_array))

    # Step 5: Compare scaling behavior (optional)
    from utils.benchmark import compare_scale_performance

    compare_scale_performance(
        small_results, large_results, len(small_array), len(large_array)
    )

    print(f"\n{'=' * 70}")
    print("✅ ANALYSIS COMPLETE")
    print(f"{'=' * 70}")
    print("📝 Summary:")
    print(f"   • {len(functions)} algorithms tested")
    print(f"   • {len(validation_results)} validation tests passed")
    print(f"   • Small-scale benchmark: n={len(small_array)}")
    print(f"   • Large-scale benchmark: n={len(large_array)}")
    print("🎯 All algorithms validated and benchmarked successfully!")


# Additional utility function examples
def demo_advanced_features():
    """Demonstrate advanced features of the utils package."""

    # Custom test case validation
    from utils.testing import validate_test_cases

    test_cases = [
        TestCase(array=[1, 2], expected=3, name="Valid test"),
        # TestCase(array=None, expected=0, name="Invalid test"),  # Would fail validation
    ]

    print("🔍 Test Case Validation:")
    is_valid = validate_test_cases(test_cases)
    print(f"   • Test cases valid: {is_valid}")

    # Access configuration constants
    from utils.config import DEFAULT_TEST_ARRAYS, COMPLEXITY_MAP

    print(f"\n⚙️ Configuration Access:")
    print(f"   • Default arrays available: {list(DEFAULT_TEST_ARRAYS.keys())}")
    print(f"   • Complexity categories: {len(COMPLEXITY_MAP)}")

    # Create different problem types
    search_tests = create_standard_test_cases("search")
    print(f"\n🔎 Problem Type Examples:")
    print(f"   • Search test cases: {len(search_tests)}")


if __name__ == "__main__":
    main()
    print("\n" + "-" * 50)
    demo_advanced_features()

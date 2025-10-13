#!/usr/bin/env python3
"""
Testing utilities for 60-days DSA implementations.

This module provides functions for validating algorithm correctness
across different implementations and test cases.

Author: Andres
Date: October 2025
"""

import time
from typing import List, Optional

from .models import TestCase, ValidationResult, AlgorithmFunction
from .config import SECTION_WIDTH, FUNCTION_NAME_WIDTH


def run_validation_tests(
    functions: List[AlgorithmFunction], 
    test_cases: List[TestCase],
    verbose: bool = True
) -> List[ValidationResult]:
    """
    Run validation tests for multiple functions against test cases.
    
    Args:
        functions: List of functions to test
        test_cases: List of test cases to validate against
        verbose: Whether to print detailed results
        
    Returns:
        List of ValidationResult objects with test outcomes
    """
    if verbose:
        print("=" * SECTION_WIDTH)
        print("🔬 ALGORITHM VALIDATION & TESTING")
        print("=" * SECTION_WIDTH)
    
    all_results = []
    overall_passed = True
    
    for test_case in test_cases:
        if verbose:
            print(f"\n📋 {test_case.name} → Expected: {test_case.expected}")
            print("-" * 50)
        
        test_case_passed = True
        
        for function in functions:
            result = _run_single_test(function, test_case)
            all_results.append(result)
            
            if verbose:
                print(f"{result.function_name:{FUNCTION_NAME_WIDTH}} : "
                      f"{result.actual_result:6} {result.status_emoji} {result.status_text}")
            
            if not result.passed:
                test_case_passed = False
                overall_passed = False
        
        if verbose:
            status_text = "✅ ALL TESTS PASSED" if test_case_passed else "❌ SOME TESTS FAILED"
            print(f"\n🎯 Test Case Result: {status_text}")
            time.sleep(0.1)  # Brief pause for readability
    
    if verbose:
        _print_validation_summary(all_results, overall_passed)
    
    return all_results


def _run_single_test(function: AlgorithmFunction, test_case: TestCase) -> ValidationResult:
    """
    Run a single test case against a function.
    
    Args:
        function: Function to test
        test_case: Test case to run
        
    Returns:
        ValidationResult with test outcome
    """
    start_time = time.perf_counter()
    
    try:
        # Execute the function
        actual_result = function(test_case.array)
        execution_time = time.perf_counter() - start_time
        
        # Check if result matches expected
        passed = _compare_results(actual_result, test_case.expected)
        
        return ValidationResult(
            function_name=function.__name__,
            test_case=test_case,
            actual_result=actual_result,
            passed=passed,
            execution_time=execution_time
        )
        
    except Exception as e:
        execution_time = time.perf_counter() - start_time
        
        return ValidationResult(
            function_name=function.__name__,
            test_case=test_case,
            actual_result=None,
            passed=False,
            error_message=str(e),
            execution_time=execution_time
        )


def _compare_results(actual, expected) -> bool:
    """
    Compare actual and expected results with appropriate tolerance.
    
    Args:
        actual: Actual result from function
        expected: Expected result
        
    Returns:
        True if results match within tolerance
    """
    # Handle None/error cases
    if actual is None:
        return False
    
    # Handle numeric comparisons with floating point tolerance
    if isinstance(actual, (int, float)) and isinstance(expected, (int, float)):
        if isinstance(actual, float) or isinstance(expected, float):
            return abs(actual - expected) < 1e-9
        else:
            return actual == expected
    
    # Handle list/array comparisons
    if isinstance(actual, list) and isinstance(expected, list):
        if len(actual) != len(expected):
            return False
        return all(_compare_results(a, e) for a, e in zip(actual, expected))
    
    # Default comparison
    return actual == expected


def _print_validation_summary(results: List[ValidationResult], overall_passed: bool) -> None:
    """
    Print a summary of validation results.
    
    Args:
        results: List of all validation results
        overall_passed: Whether all tests passed
    """
    print("\n" + "=" * SECTION_WIDTH)
    print("📊 VALIDATION SUMMARY")
    print("=" * SECTION_WIDTH)
    
    # Count results by function
    function_stats = {}
    for result in results:
        func_name = result.function_name
        if func_name not in function_stats:
            function_stats[func_name] = {"passed": 0, "failed": 0, "total": 0}
        
        function_stats[func_name]["total"] += 1
        if result.passed:
            function_stats[func_name]["passed"] += 1
        else:
            function_stats[func_name]["failed"] += 1
    
    # Print function-wise summary
    print(f"\n🎯 Results by Function:")
    print("-" * 50)
    
    for func_name, stats in function_stats.items():
        passed_pct = (stats["passed"] / stats["total"]) * 100 if stats["total"] > 0 else 0
        status = "✅" if stats["failed"] == 0 else "❌"
        
        print(f"{status} {func_name:{FUNCTION_NAME_WIDTH}} : "
              f"{stats['passed']:2d}/{stats['total']:2d} passed ({passed_pct:5.1f}%)")
    
    # Overall summary
    total_tests = len(results)
    total_passed = sum(1 for r in results if r.passed)
    overall_pct = (total_passed / total_tests) * 100 if total_tests > 0 else 0
    
    print(f"\n🏆 Overall Results:")
    print(f"   • Total tests: {total_tests}")
    print(f"   • Passed: {total_passed} ({overall_pct:.1f}%)")
    print(f"   • Failed: {total_tests - total_passed}")
    print(f"   • Status: {'✅ ALL PASSED' if overall_passed else '❌ SOME FAILED'}")
    
    # Show errors if any
    error_results = [r for r in results if not r.passed and r.error_message]
    if error_results:
        print(f"\n❌ Error Details:")
        for result in error_results:
            print(f"   • {result.function_name}: {result.error_message}")


def create_standard_test_cases(problem_type: str = "subarray_sum") -> List[TestCase]:
    """
    Create a standard set of test cases for common problem types.
    
    Args:
        problem_type: Type of problem ("subarray_sum", "search", etc.)
        
    Returns:
        List of standard test cases for the problem type
    """
    if problem_type == "subarray_sum":
        return [
            TestCase(
                array=[1, 2, 3], 
                expected=20, 
                name="Basic case [1, 2, 3]",
                description="Simple positive integers"
            ),
            TestCase(
                array=[2, 1, 3], 
                expected=19, 
                name="Reordered [2, 1, 3]",
                description="Different order, different result"
            ),
            TestCase(
                array=[1], 
                expected=1, 
                name="Single element [1]",
                description="Edge case: single element"
            ),
            TestCase(
                array=[0, 0], 
                expected=0, 
                name="All zeros [0, 0]",
                description="Edge case: all zeros"
            ),
            TestCase(
                array=[-1, 2], 
                expected=1, 
                name="Mixed signs [-1, 2]",
                description="Negative and positive values"
            ),
        ]
    
    elif problem_type == "search":
        return [
            TestCase(
                array=[1, 2, 3, 4, 5], 
                expected=2, 
                name="Find 3 in [1, 2, 3, 4, 5]",
                description="Target exists in middle"
            ),
            TestCase(
                array=[1, 2, 3, 4, 5], 
                expected=-1, 
                name="Find 6 in [1, 2, 3, 4, 5]",
                description="Target doesn't exist"
            ),
        ]
    
    else:
        # Return basic test cases for unknown problem types
        return [
            TestCase(
                array=[1, 2, 3], 
                expected=None, 
                name="Generic test [1, 2, 3]",
                description="Basic test case - update expected value"
            ),
        ]


def validate_test_cases(test_cases: List[TestCase]) -> bool:
    """
    Validate that all test cases are properly formed.
    
    Args:
        test_cases: List of test cases to validate
        
    Returns:
        True if all test cases are valid
    """
    for i, test_case in enumerate(test_cases):
        try:
            # Check required fields
            if not test_case.name:
                print(f"❌ Test case {i}: name is required")
                return False
            
            if test_case.array is None:
                print(f"❌ Test case {i} ({test_case.name}): array is required")
                return False
            
            if test_case.expected is None:
                print(f"⚠️  Test case {i} ({test_case.name}): expected value is None")
            
        except Exception as e:
            print(f"❌ Test case {i}: validation error - {e}")
            return False
    
    print(f"✅ All {len(test_cases)} test cases are valid")
    return True
#!/usr/bin/env python
from __future__ import annotations
"""
Day 1: Range Sum Queries
Python Implementation

Author: Andres
Date: October 2025
"""

def rangeSumQuery(A: list[int], B: list[list[int]], method: str = "brute") -> list[int]:
    """
    Calculates the sum of all elements from L to R indices in the A array (0-indexed)
    
    Args: 
        A: list of integers
        B: 2D integer array with the query limits [L, R]
        method: "brute" or "optimized" 
    Returns: 
        list[int]: Sum of elements in the selected range for each query
    """
    # check for malformed inputs
    if not A or not B:
        raise ValueError("Input Arrays A and B cannot be empty")
    
    # Validate queries
    for query in B:
        if len(query) != 2:
            raise ValueError("Each query must have exactly 2 elements [L, R]")
        L, R = query
        if L < 0 or R >= len(A) or L > R:
            raise ValueError(f"Invalid query [{L}, {R}] for array of length {len(A)}")
    
    # === Method selection ===
    normalized_method = method.lower().strip()
    if normalized_method == "brute":
        results = brute_force_rsq(A, B)
    elif normalized_method == "optimized":
        results = optimized_rsq(A, B)
    else:
        raise ValueError("Method must be either 'brute' or 'optimized'")
    
    return results

def brute_force_rsq(A: list[int], B: list[list[int]]) -> list[int]:
    """
    Brute force approach: For each query, iterate through the range and calculate sum.
    Time Complexity: O(N × Q) where N = array length, Q = number of queries
    Space Complexity: O(1)
    """
    results = []
    for query in B:
        L, R = query
        range_sum = 0
        for i in range(L, R + 1):
            range_sum += A[i]
        results.append(range_sum)
    return results

def optimized_rsq(A: list[int], B: list[list[int]]) -> list[int]:
    """
    Optimized approach using prefix sums: Preprocess once, answer queries in O(1)
    Time Complexity: O(N + Q) where N = array length, Q = number of queries  
    Space Complexity: O(N) for prefix array
    
    Key insight: sum[L:R] = prefix[R+1] - prefix[L]
    """
    n = len(A)
    # Build prefix sum array where prefix[i] = sum of first i elements
    prefix = [0] * (n + 1)
    for i in range(n):
        prefix[i + 1] = prefix[i] + A[i]
    
    results = []
    for query in B:
        L, R = query
        # Sum from L to R (inclusive) = prefix[R+1] - prefix[L]
        range_sum = prefix[R + 1] - prefix[L]
        results.append(range_sum)
    
    return results

# Test cases
if __name__ == "__main__":
    # Test case 1: [1, 2, 3, 4, 5] with queries [[0, 3], [1, 2]]
    A1 = [1, 2, 3, 4, 5]
    B1 = [[0, 3], [1, 2]]
    
    print("Test case 1:")
    print(f"Array: {A1}")
    print(f"Queries: {B1}")
    print(f"Brute force result: {rangeSumQuery(A1, B1, 'brute')}")
    print(f"Optimized result: {rangeSumQuery(A1, B1, 'optimized')}")
    print(f"Expected: [10, 5]")
    print()
    
    # Test case 2: [2, 2, 2] with queries [[0, 0], [1, 2]]
    A2 = [2, 2, 2]
    B2 = [[0, 0], [1, 2]]
    
    print("Test case 2:")
    print(f"Array: {A2}")
    print(f"Queries: {B2}")
    print(f"Brute force result: {rangeSumQuery(A2, B2, 'brute')}")
    print(f"Optimized result: {rangeSumQuery(A2, B2, 'optimized')}")
    print(f"Expected: [2, 4]")

#!/usr/bin/env python3
"""
Day 1: Subarray Sums & Range Queries
Python Implementation

Author: Andres
Date: October 2024
"""

# TODO: Implement solutions for both problems
# (Currently only Concept 1's brute force is implemented.)
# ----------------------------------------------------------------------

"""
Concept 1: Sum of All Subarray Sums

You are given an integer array A of length N. You have to find the sum of all
subarray sums of A. More formally, a subarray is defined as a contiguous part of
an array which we can obtain by deleting zero or more elements from either end of
the array. A subarray sum denotes the sum of all the elements of that subarray.
"""

# Brute force solution: Generate all possible subarrays and calculate their sums.

# Algorithm:
# 1. Use nested loops
# 2. Outer loop generates subarray boundaries
# 3. Inner loop calculates sum

# Complexity:
# - Time: O(n³)  # This is the complexity for the brute_force implementation shown below.

# ----------------------------------------------------------------------


def brute_force(arr):
    """
    Calculates the sum of all subarray sums in O(n³) time.
    """
    n = len(arr)
    total_sum = 0
    for i in range(n):
        for j in range(i, n):
            # arr[i:j+1] creates a new list, and sum() iterates over it.
            subarray_sum = sum(arr[i:j+1])
            total_sum += subarray_sum

    return total_sum

# ----------------------------------------------------------------------

# Brute force optimized solution (O n²):

# The initial brute foce implementation has a time complexity of O(n³) because:
# 1. The outer loop runs n times (for starting index j)

# Algorithm:
# TO-DO


# ----------------------------------------------------------------------


if __name__ == "__main__":
    # TODO: Add more comprehensive test cases and run solutions
    # The expected sum for [1, 2, 3] is:
    # [1] -> 1
    # [2] -> 2
    # [3] -> 3
    # [1, 2] -> 3
    # [2, 3] -> 5
    # [1, 2, 3] -> 6
    # Total sum = 1 + 2 + 3 + 3 + 5 + 6 = 20
    input_array_1 = [1, 2, 3]

    # The expected sum for [2, 1, 3] is:
    # [2] -> 2
    # [1] -> 1
    # [3] -> 3
    # [2, 1] -> 3
    # [1, 3] -> 4
    # [2, 1, 3] -> 6
    # Total sum = 2 + 1 + 3 + 3 + 4 + 6 = 19
    input_array_2 = [2, 1, 3]
    input_array_bulk = [i for i in range(0, 99)]

    print(
        f"Input: {input_array_1} | Brute Force O(n³): {brute_force(input_array_1)} (Expected: 20)")
    print(
        f"Input: {input_array_2} | Brute Force O(n³): {brute_force(input_array_2)} (Expected: 19)")
    
    # here we check how much does it take to calculates the sum of all subarrays for the bulk list

    print("Day 1: Ready to implement!")

# ----------------------------------------------------------------------

# Concept 2 (Pending): Range Seum Queries

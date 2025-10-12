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
            subarray_sum: int = sum(arr[i:j+1])
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
        left_choices: int = i + 1        # positions where subarray can start
        right_choices: int = n - i       # positions where subarray can end
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


def brute_force_O_n_squared(arr):
    """
    Calculates the sum of all subarray sums in O(n^2) time.
    """
    n = len(arr)
    total_sum = 0
    for i in range(n):
        current_subarray_sum = 0
        for j in range(i, n):
            # Calculate the sum for arr[i...j] by adding arr[j] to the previous sum
            current_subarray_sum += arr[j]
            # Add the current subarray sum to the total
            total_sum += current_subarray_sum

    return total_sum


def vector_numpy_contribution(arr: list[int] | np.ndarray) -> int:
    """
    Calculates sum of all subarray sums using a fully vectorized NumPy approach.
    
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


# ----------------------------------------------------------------------


if __name__ == "__main__":
    input_array_1: list[int] = [1, 2, 3]
    input_array_2: list[int] = [2, 1, 3]
    input_array_bulk: list[int] = [i for i in range(0, 99)]
    
    functions = [naive_brute_force, optimized_brute_force, contribution_technique, vectorized_contribution, vector_numpy_contribution]
       
    print("Array 1: [1, 2, 3], expected sum: 20")
    for function in functions:
        print(function.__name__, ":", function(input_array_1))
    print("\n"); time.sleep(1)
    
    print("Array 2: [2, 1, 3], expected sum: 20")
    for function in functions:
        print(function.__name__, ":", function(input_array_2))
    print("\n"); time.sleep(1)
    
    ## Benchmarking with timeit
    test_timer = time.perf_counter
    replicas = 1000
    
    def test_implementation(function, array):
        return timeit.timeit(
            lambda: function(array),
            number=replicas,
            timer=test_timer)
    
    for function in functions:
        print("Testing", function.__name__, "with 100 elements, ${replicas} replicas: ", test_implementation(function, input_array_bulk))
    


    
# ----------------------------------------------------------------------

# Concept 2 (Pending): Range Sum Queries

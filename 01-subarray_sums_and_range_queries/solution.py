#!/usr/bin/env python3
"""
Day 1: Subarray Sums & Range Queries
Python Implementation

Author: Andres
Date: October 2024
"""
def naive_brute_force(arr):
    """
    Calculates sum of all subarray sums using triple nested loops.
    
    Args:
        arr: List of integers
        
    Returns:
        int: Sum of all possible subarray sums
        
    Time Complexity: O(n³)
    Space Complexity: O(1)
    """
    n = len(arr)
    total_sum = 0
    for i in range(n):
        for j in range(i, n):
            # Third loop implicit in sum() function
            subarray_sum = sum(arr[i:j+1])
            total_sum += subarray_sum
    return total_sum

def optimized_brute_force(arr):
    """
    Calculates sum of all subarray sums using running sum technique.
    
    Args:
        arr: List of integers
        
    Returns:
        int: Sum of all possible subarray sums
        
    Time Complexity: O(n²)
    Space Complexity: O(1)
    """
    n = len(arr)
    total_sum = 0
    for i in range(n):
        current_subarray_sum = 0
        for j in range(i, n):
            current_subarray_sum += arr[j]
            total_sum += current_subarray_sum
    return total_sum

def contribution_technique(arr):
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
    n = len(arr)
    total_sum = 0
    for i in range(n):
        left_choices = i + 1        # positions where subarray can start
        right_choices = n - i       # positions where subarray can end
        contribution = arr[i] * left_choices * right_choices
        total_sum += contribution
    return total_sum

def vectorized_contribution(arr):
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
    n = len(arr)
    m = (n + 1) // 2  # ceiling division for midpoint
    
    # Compute first half of contributions
    first_half = []
    for k in range(m):
        first_half.append((k + 1) * (n - k))
    
    # Create mirror based on array length parity
    if n % 2 == 0:
        # Even: mirror entire first half
        mirror = first_half[::-1]
    else:
        # Odd: mirror all except center element (last in first_half)
        mirror = first_half[:-1][::-1]
    
    contributions = first_half + mirror
    
    # Calculate dot product
    total_sum = 0
    for i in range(n):
        total_sum += arr[i] * contributions[i]
    
    return total_sum

# ----------------------------------------------------------------------


if __name__ == "__main__":
    input_array_1 = [1, 2, 3]
    input_array_2 = [2, 1, 3]
    input_array_bulk = [i for i in range(0, 99)]
    

    


    
# ----------------------------------------------------------------------

# Concept 2 (Pending): Range Sum Queries

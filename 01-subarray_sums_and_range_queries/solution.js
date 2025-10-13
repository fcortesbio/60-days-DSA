#!/usr/bin/env node
/**
 * Day 1: Subarray Sums & Range Queries
 * JavaScript/Node.js Implementation
 *
 * Author: Andres
 * Date: October 2025
 */

// TODO: Implement solutions for both problems
// naive_brute_force

function naive_brute_force(arr) {
  const n = arr.length;
  let total_sum = 0;

  for (let i = 0; i < n; i++) {
    for (let j = i; j < n; j++) {
      let subarray_sum = 0;
      for (let k = i; k <= j; k++) {
        subarray_sum += arr[k];
      }
      total_sum += subarray_sum;
    }
  }
  return total_sum;
}

// optimized_brute_force
function optimized_brute_force(arr) {
  const n = arr.length;
  let total_sum = 0;

  for (let i = 0; i < n; i++) {
    let current_subarray_sum = 0;

    for (let j = i; j < n; j++) {
      current_subarray_sum += arr[j];
      total_sum += current_subarray_sum;
    }
  }
  return total_sum;
}

// contribution_technique
function contribution_technique(arr) {
  const n = arr.length;
  let contribution = (k, n) => (k + 1) * (n - k);
  let total_sum = 0;
  for (let k = 0; k < n; k++) {
    total_sum += arr[k] * contribution(k, n);
  }
  return total_sum;
}

// vectorized_contribution
function vectorized_contribution(arr) {
  const n = arr.length;
  const contribution = (k, n) => (k + 1) * (n - k);
  let contributions = [];
  for (let k = 0; k < n; k++) {
    contributions.push(contribution(k, n));
  }
  let total_sum = 0;
  for (let i = 0; i < n; i++) {
    total_sum += arr[i] * contributions[i];
  }
  return total_sum;
}

// vector_half_contribution
function vector_half_contribution(arr) {
  const n = arr.length;
  const contribution = (k, n) => (k + 1) * (n - k);
  const m = Math.ceil(n / 2);
  // compute half of the contribution array
  let first_half = [];
  for (let k = 0; k < m; k++) {
    first_half.push(contribution(k, n));
  }
  let mirror =
    n % 2 == 0
      ? first_half.slice().reverse()
      : first_half.slice(0, m - 1).reverse();

  let contributions = first_half.concat(mirror);
  let total_sum = 0;
  for (let i = 0; i < n; i++) {
    total_sum += arr[i] * contributions[i];
  }
  return total_sum;
}

// m = (n + 1) // 2 ; // ceiling division for midpoint

// Run tests if this file is executed directly
if (require.main === module) {
  // TODO: Add test cases and run solutions
  console.log("Day 1: Ready to implement!");
}

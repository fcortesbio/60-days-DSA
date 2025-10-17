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

// Export functions for testing
module.exports = {
  naive_brute_force,
  optimized_brute_force,
  contribution_technique,
  vectorized_contribution,
  vector_half_contribution
};

// Run tests if this file is executed directly
if (require.main === module) {
  // Simple assertion-based tests
  const assert = (actual, expected, description) => {
    if (actual === expected) {
      console.log(`✅ ${description}: ${actual}`);
    } else {
      console.log(`❌ ${description}: expected ${expected}, got ${actual}`);
      process.exit(1);
    }
  };

  const algorithms = [
    { name: 'naive_brute_force', func: naive_brute_force },
    { name: 'optimized_brute_force', func: optimized_brute_force },
    { name: 'contribution_technique', func: contribution_technique },
    { name: 'vectorized_contribution', func: vectorized_contribution },
    { name: 'vector_half_contribution', func: vector_half_contribution }
  ];

  const testCases = [
    { input: [1, 2, 3], expected: 20, name: "Basic example [1,2,3]" },
    { input: [2, 1, 3], expected: 19, name: "Reordered [2,1,3]" },
    { input: [5], expected: 5, name: "Single element [5]" },
    { input: [], expected: 0, name: "Empty array" },
    { input: [-1, 2, -3], expected: -4, name: "Mixed signs [-1,2,-3]" },
    { input: [3, 3, 3], expected: 30, name: "Repeated elements [3,3,3]" }
  ];

  console.log('🧪 Running DSA Solution Tests...');
  console.log('='.repeat(50));
  
  let totalTests = 0;
  let passedTests = 0;
  
  algorithms.forEach(algorithm => {
    console.log(`\n📋 Testing ${algorithm.name}:`);
    testCases.forEach(testCase => {
      try {
        const result = algorithm.func(testCase.input);
        assert(result, testCase.expected, `${testCase.name}`);
        passedTests++;
      } catch (error) {
        console.log(`❌ ${testCase.name}: ${error.message}`);
      }
      totalTests++;
    });
  });
  
  console.log(`\n📊 Results: ${passedTests}/${totalTests} tests passed`);
  console.log(passedTests === totalTests ? '🎉 All tests passed!' : '💥 Some tests failed!');
}

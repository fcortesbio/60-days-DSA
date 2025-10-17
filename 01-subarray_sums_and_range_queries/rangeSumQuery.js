/**
 * Day 1: Range Sum Queries
 * JavaScript Implementation
 * 
 * Author: Andres
 * Date: October 2025
 */

/**
 * Calculates the sum of all elements from L to R indices in the A array (0-indexed)
 * 
 * @param {number[]} A - array of integers
 * @param {number[][]} B - 2D integer array with the query limits [L, R]
 * @param {string} method - "brute" or "optimized"
 * @returns {number[]} - Sum of elements in the selected range for each query
 * @throws {Error} - for invalid inputs
 */
function rangeSumQuery(A, B, method = "brute") {
    // Check for malformed inputs
    if (!A || A.length === 0 || !B || B.length === 0) {
        throw new Error("Input Arrays A and B cannot be empty");
    }
    
    // Validate queries
    for (const query of B) {
        if (query.length !== 2) {
            throw new Error("Each query must have exactly 2 elements [L, R]");
        }
        const [L, R] = query;
        if (L < 0 || R >= A.length || L > R) {
            throw new Error(`Invalid query [${L}, ${R}] for array of length ${A.length}`);
        }
    }
    
    // Method selection
    const normalizedMethod = method.toLowerCase().trim();
    switch (normalizedMethod) {
        case "brute":
            return bruteForceRSQ(A, B);
        case "optimized":
            return optimizedRSQ(A, B);
        default:
            throw new Error("Method must be either 'brute' or 'optimized'");
    }
}

/**
 * Brute force approach: For each query, iterate through the range and calculate sum.
 * Time Complexity: O(N × Q) where N = array length, Q = number of queries
 * Space Complexity: O(1)
 * 
 * @param {number[]} A - input array
 * @param {number[][]} B - queries array
 * @returns {number[]} - list of range sums
 */
function bruteForceRSQ(A, B) {
    const results = [];
    
    for (const query of B) {
        const [L, R] = query;
        let rangeSum = 0;
        
        for (let i = L; i <= R; i++) {
            rangeSum += A[i];
        }
        
        results.push(rangeSum);
    }
    
    return results;
}

/**
 * Optimized approach using prefix sums: Preprocess once, answer queries in O(1)
 * Time Complexity: O(N + Q) where N = array length, Q = number of queries
 * Space Complexity: O(N) for prefix array
 * 
 * Key insight: sum[L:R] = prefix[R+1] - prefix[L]
 * 
 * @param {number[]} A - input array
 * @param {number[][]} B - queries array
 * @returns {number[]} - list of range sums
 */
function optimizedRSQ(A, B) {
    const n = A.length;
    
    // Build prefix sum array where prefix[i] = sum of first i elements
    const prefix = new Array(n + 1).fill(0);
    for (let i = 0; i < n; i++) {
        prefix[i + 1] = prefix[i] + A[i];
    }
    
    const results = [];
    
    for (const query of B) {
        const [L, R] = query;
        // Sum from L to R (inclusive) = prefix[R+1] - prefix[L]
        const rangeSum = prefix[R + 1] - prefix[L];
        results.push(rangeSum);
    }
    
    return results;
}

// Test cases and demonstration
if (require.main === module) {
    // Test case 1: [1, 2, 3, 4, 5] with queries [[0, 3], [1, 2]]
    const A1 = [1, 2, 3, 4, 5];
    const B1 = [[0, 3], [1, 2]];
    
    console.log("Test case 1:");
    console.log("Array:", A1);
    console.log("Queries:", B1);
    console.log("Brute force result:", rangeSumQuery(A1, B1, "brute"));
    console.log("Optimized result:", rangeSumQuery(A1, B1, "optimized"));
    console.log("Expected: [10, 5]");
    console.log();
    
    // Test case 2: [2, 2, 2] with queries [[0, 0], [1, 2]]
    const A2 = [2, 2, 2];
    const B2 = [[0, 0], [1, 2]];
    
    console.log("Test case 2:");
    console.log("Array:", A2);
    console.log("Queries:", B2);
    console.log("Brute force result:", rangeSumQuery(A2, B2, "brute"));
    console.log("Optimized result:", rangeSumQuery(A2, B2, "optimized"));
    console.log("Expected: [2, 4]");
    console.log();
    
    // Performance comparison for larger input
    console.log("Performance comparison:");
    const largeArray = Array.from({length: 10000}, (_, i) => i + 1);
    const largeQueries = Array.from({length: 1000}, (_, i) => [
        i * 10, 
        Math.min(i * 10 + 50, largeArray.length - 1)
    ]);
    
    const startTime1 = process.hrtime.bigint();
    const bruteResult = rangeSumQuery(largeArray, largeQueries, "brute");
    const bruteTime = Number(process.hrtime.bigint() - startTime1) / 1_000_000;
    
    const startTime2 = process.hrtime.bigint();
    const optimizedResult = rangeSumQuery(largeArray, largeQueries, "optimized");
    const optimizedTime = Number(process.hrtime.bigint() - startTime2) / 1_000_000;
    
    console.log(`Brute force time: ${bruteTime.toFixed(2)} ms`);
    console.log(`Optimized time: ${optimizedTime.toFixed(2)} ms`);
    console.log(`Speedup: ${(bruteTime / optimizedTime).toFixed(2)}x`);
    
    // Check if results match
    const resultsMatch = JSON.stringify(bruteResult) === JSON.stringify(optimizedResult);
    console.log("Results match:", resultsMatch);
}

// Export for use in other modules
module.exports = { rangeSumQuery, bruteForceRSQ, optimizedRSQ };
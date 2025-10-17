import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

/**
 * Day 1: Range Sum Queries
 * Java Implementation
 * 
 * Author: Andres
 * Date: October 2025
 */
public class RangeSumQuery {
    
    /**
     * Calculates the sum of all elements from L to R indices in the A array (0-indexed)
     * 
     * @param A      array of integers
     * @param B      2D integer array with the query limits [L, R]
     * @param method "brute" or "optimized"
     * @return list of sums for each query
     * @throws IllegalArgumentException for invalid inputs
     */
    public static List<Integer> rangeSumQuery(int[] A, int[][] B, String method) {
        // Check for malformed inputs
        if (A == null || A.length == 0 || B == null || B.length == 0) {
            throw new IllegalArgumentException("Input Arrays A and B cannot be empty");
        }
        
        // Validate queries
        for (int[] query : B) {
            if (query.length != 2) {
                throw new IllegalArgumentException("Each query must have exactly 2 elements [L, R]");
            }
            int L = query[0], R = query[1];
            if (L < 0 || R >= A.length || L > R) {
                throw new IllegalArgumentException(
                    String.format("Invalid query [%d, %d] for array of length %d", L, R, A.length)
                );
            }
        }
        
        // Method selection
        String normalizedMethod = method.toLowerCase().trim();
        switch (normalizedMethod) {
            case "brute":
                return bruteForceRSQ(A, B);
            case "optimized":
                return optimizedRSQ(A, B);
            default:
                throw new IllegalArgumentException("Method must be either 'brute' or 'optimized'");
        }
    }
    
    /**
     * Brute force approach: For each query, iterate through the range and calculate sum.
     * Time Complexity: O(N × Q) where N = array length, Q = number of queries
     * Space Complexity: O(1)
     * 
     * @param A input array
     * @param B queries array
     * @return list of range sums
     */
    private static List<Integer> bruteForceRSQ(int[] A, int[][] B) {
        List<Integer> results = new ArrayList<>();
        
        for (int[] query : B) {
            int L = query[0], R = query[1];
            int rangeSum = 0;
            
            for (int i = L; i <= R; i++) {
                rangeSum += A[i];
            }
            
            results.add(rangeSum);
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
     * @param A input array
     * @param B queries array
     * @return list of range sums
     */
    private static List<Integer> optimizedRSQ(int[] A, int[][] B) {
        int n = A.length;
        
        // Build prefix sum array where prefix[i] = sum of first i elements
        long[] prefix = new long[n + 1];
        for (int i = 0; i < n; i++) {
            prefix[i + 1] = prefix[i] + A[i];
        }
        
        List<Integer> results = new ArrayList<>();
        
        for (int[] query : B) {
            int L = query[0], R = query[1];
            // Sum from L to R (inclusive) = prefix[R+1] - prefix[L]
            long rangeSum = prefix[R + 1] - prefix[L];
            results.add((int) rangeSum);
        }
        
        return results;
    }
    
    /**
     * Convenience method with default "optimized" approach
     */
    public static List<Integer> rangeSumQuery(int[] A, int[][] B) {
        return rangeSumQuery(A, B, "optimized");
    }
    
    /**
     * Test cases and demonstration
     */
    public static void main(String[] args) {
        // Test case 1: [1, 2, 3, 4, 5] with queries [[0, 3], [1, 2]]
        int[] A1 = {1, 2, 3, 4, 5};
        int[][] B1 = {{0, 3}, {1, 2}};
        
        System.out.println("Test case 1:");
        System.out.println("Array: " + Arrays.toString(A1));
        System.out.println("Queries: " + Arrays.deepToString(B1));
        System.out.println("Brute force result: " + rangeSumQuery(A1, B1, "brute"));
        System.out.println("Optimized result: " + rangeSumQuery(A1, B1, "optimized"));
        System.out.println("Expected: [10, 5]");
        System.out.println();
        
        // Test case 2: [2, 2, 2] with queries [[0, 0], [1, 2]]
        int[] A2 = {2, 2, 2};
        int[][] B2 = {{0, 0}, {1, 2}};
        
        System.out.println("Test case 2:");
        System.out.println("Array: " + Arrays.toString(A2));
        System.out.println("Queries: " + Arrays.deepToString(B2));
        System.out.println("Brute force result: " + rangeSumQuery(A2, B2, "brute"));
        System.out.println("Optimized result: " + rangeSumQuery(A2, B2, "optimized"));
        System.out.println("Expected: [2, 4]");
        System.out.println();
        
        // Performance comparison for larger input
        System.out.println("Performance comparison:");
        int[] largeArray = new int[10000];
        for (int i = 0; i < largeArray.length; i++) {
            largeArray[i] = i + 1;
        }
        
        int[][] largeQueries = new int[1000][2];
        for (int i = 0; i < 1000; i++) {
            largeQueries[i][0] = i * 10;
            largeQueries[i][1] = Math.min(i * 10 + 50, largeArray.length - 1);
        }
        
        long startTime = System.nanoTime();
        List<Integer> bruteResult = rangeSumQuery(largeArray, largeQueries, "brute");
        long bruteTime = System.nanoTime() - startTime;
        
        startTime = System.nanoTime();
        List<Integer> optimizedResult = rangeSumQuery(largeArray, largeQueries, "optimized");
        long optimizedTime = System.nanoTime() - startTime;
        
        System.out.printf("Brute force time: %.2f ms%n", bruteTime / 1_000_000.0);
        System.out.printf("Optimized time: %.2f ms%n", optimizedTime / 1_000_000.0);
        System.out.printf("Speedup: %.2fx%n", (double) bruteTime / optimizedTime);
        System.out.println("Results match: " + bruteResult.equals(optimizedResult));
    }
}

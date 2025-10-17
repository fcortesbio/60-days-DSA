/**
 * Day 1: Subarray Sums & Range Queries
 * Java Implementation
 *
 * Author: Andres
 * Date: October 2025
 */

public class SubArraySum{

    /**
     * Main method to run tests
     */
    public static void main(String[] args) {
        System.out.println("🧪 Running DSA Solution Tests...");
        System.out.println("=".repeat(50));
        
        runTests();
    }
    
    /**
     * Simple assertion method for testing
     */
    private static void assertEquals(int actual, int expected, String testName) {
        if (actual == expected) {
            System.out.println("✅ " + testName + ": " + actual);
        } else {
            System.out.println("❌ " + testName + ": expected " + expected + ", got " + actual);
            System.exit(1);
        }
    }
    
    /**
     * Run all tests for the implemented algorithms
     */
    private static void runTests() {
        // Test cases with expected results
        TestCase[] testCases = {
            new TestCase(new int[]{1, 2, 3}, 20, "Basic example [1,2,3]"),
            new TestCase(new int[]{2, 1, 3}, 19, "Reordered [2,1,3]"),
            new TestCase(new int[]{5}, 5, "Single element [5]"),
            new TestCase(new int[]{}, 0, "Empty array"),
            new TestCase(new int[]{-1, 2, -3}, -4, "Mixed signs [-1,2,-3]"),
            new TestCase(new int[]{3, 3, 3}, 30, "Repeated elements [3,3,3]")
        };
        
        String[] algorithmNames = {
            "naive_brute_force",
            "optimized_brute_force", 
            "contribution_technique",
            "vectorized_contribution",
            "vector_half_contribution"
        };
        
        int totalTests = 0;
        int passedTests = 0;
        
        for (String algorithm : algorithmNames) {
            System.out.println("\n📋 Testing " + algorithm + ":");
            
            for (TestCase testCase : testCases) {
                try {
                    int result = runAlgorithm(algorithm, testCase.input);
                    assertEquals(result, testCase.expected, testCase.name);
                    passedTests++;
                } catch (Exception e) {
                    System.out.println("❌ " + testCase.name + ": " + e.getMessage());
                }
                totalTests++;
            }
        }
        
        System.out.println("\n📊 Results: " + passedTests + "/" + totalTests + " tests passed");
        System.out.println(passedTests == totalTests ? "🎉 All tests passed!" : "💥 Some tests failed!");
    }
    
    /**
     * Helper method to run specific algorithm by name
     */
    private static int runAlgorithm(String algorithmName, int[] arr) {
        switch (algorithmName) {
            case "naive_brute_force":
                return SubarraySum.naive_brute_force(arr);
            case "optimized_brute_force":
                return SubarraySum.optimized_brute_force(arr);
            case "contribution_technique":
                return SubarraySum.contribution_technique(arr);
            case "vectorized_contribution":
                return SubarraySum.vectorized_contribution(arr);
            case "vector_half_contribution":
                return SubarraySum.vector_half_contribution(arr);
            default:
                throw new IllegalArgumentException("Unknown algorithm: " + algorithmName);
        }
    }
    
    /**
     * Test case data structure
     */
    private static class TestCase {
        int[] input;
        int expected;
        String name;
        
        TestCase(int[] input, int expected, String name) {
            this.input = input;
            this.expected = expected;
            this.name = name;
        }
    }

    /**
     * Static inner class containing all subarray sum algorithms
     */
    public static class SubarraySum {

        /**
         * Naive brute force approach - O(n³) time complexity
         * Generates all subarrays and calculates their sums
         */
        public static int naive_brute_force(int[] arr) {
            int totalSum = 0;
            int n = arr.length;

            // Triple nested loop to generate all subarrays
            for (int i = 0; i < n; i++) {              // Start index
                for (int j = i; j < n; j++) {          // End index
                    for (int k = i; k <= j; k++) {     // Sum elements in subarray [i,j]
                        totalSum += arr[k];
                    }
                }
            }
            return totalSum;
        }

        /**
         * Optimized brute force approach - O(n²) time complexity
         * Uses running sum to avoid recalculating subarray sums
         */
        public static int optimized_brute_force(int[] arr) {
            int n = arr.length;
            int totalSum = 0;

            for (int i = 0; i < n; i++) {
                int currentSum = 0;
                for (int j = i; j < n; j++) {
                    currentSum += arr[j];     // Add current element to running sum
                    totalSum += currentSum;   // Add this subarray sum to total
                }
            }
            return totalSum;
        }

        /**
         * Contribution technique - O(n) time complexity
         * Calculates how many times each element appears in all subarrays
         */
        public static int contribution_technique(int[] arr) {
            int n = arr.length;
            int totalSum = 0;
            
            for (int k = 0; k < n; k++) {
                // Element at index k appears in (k+1) * (n-k) subarrays
                int contribution = (k + 1) * (n - k);
                totalSum += arr[k] * contribution;
            }
            return totalSum;
        }

        /**
         * Vectorized contribution approach - O(n) time complexity
         * Precomputes contribution values then calculates final sum
         */
        public static int vectorized_contribution(int[] arr) {
            int n = arr.length;
            
            if (n == 0) return 0;
            
            // Precompute contribution values for each position
            int[] contributions = new int[n];
            for (int i = 0; i < n; i++) {
                contributions[i] = (i + 1) * (n - i);
            }
            
            // Calculate total sum using contributions
            int totalSum = 0;
            for (int i = 0; i < n; i++) {
                totalSum += arr[i] * contributions[i];
            }
            
            return totalSum;
        }
        
        /**
         * Vector half contribution approach - O(n) time complexity
         * Uses symmetric property of contributions to compute only half
         */
        public static int vector_half_contribution(int[] arr) {
            int n = arr.length;
            
            if (n == 0) return 0;
            
            int m = (n + 1) / 2; // ceiling division
            
            // Compute first half of contributions
            int[] firstHalf = new int[m];
            for (int k = 0; k < m; k++) {
                firstHalf[k] = (k + 1) * (n - k);
            }
            
            // Create mirror based on array length parity
            int[] contributions = new int[n];
            System.arraycopy(firstHalf, 0, contributions, 0, m);
            
            if (n % 2 == 0) {
                // Even length: mirror entire first half
                for (int i = 0; i < m; i++) {
                    contributions[m + i] = firstHalf[m - 1 - i];
                }
            } else {
                // Odd length: mirror all except center element
                for (int i = 0; i < m - 1; i++) {
                    contributions[m + i] = firstHalf[m - 2 - i];
                }
            }
            
            // Calculate total sum using contributions
            int totalSum = 0;
            for (int i = 0; i < n; i++) {
                totalSum += arr[i] * contributions[i];
            }
            
            return totalSum;
        }
    }
}

/**
 * Day 1: Subarray Sums & Range Queries
 * Java Implementation
 *
 * Author: Andres
 * Date: October 2025
 */

public class Solution {

    // TODO: Implement solutions for both problems

    /**
     * Main method to run tests
     */
    public static void main(String[] args) {
        // TODO: Add test cases and run solutions
        System.out.println("Day 1: Ready to implement!");
    }

    public class SubarraySum {
        /**
         * Calculates the sum of all subarray sums using a naive, triple-loop approach
         * @param arr The input array of integers
         * @return The sum of all possible subarray sums
         */
        public static int naiveBruteForce(int[] arr){
            int totalSum = 0;
            int n = arr.length;

            // first loop sets the starting point of the subarray
            for (int i = 0; i < n ; i++){
                // second loop sets the ending point of the subarray
                for (int j = i; j < n; j++){
                    // third loop calculates the sum of the subarray
                    for (int k = i; k <= j; k++){
                        totalSum += arr[k];
                    }
                }
            }
            return totalSum;
        }

    }
}

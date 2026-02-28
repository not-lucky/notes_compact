# Lessons Learned

## Coin Change DP Notes
- Ensure explicit separation between combinations (Coin Change II) and permutations (Combination Sum IV) in explanation since loop ordering causes frequent confusion.
- Always initialize DP arrays with `float('inf')` for "minimum" problems to prevent `min()` from defaulting to `0` incorrectly.
- When doing counting/ways DP, the base case `dp[0] = 1` is critical because it acts as the foundation for the sum.
- Make it clear why greedy doesn't work for arbitrary coins.

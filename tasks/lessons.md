# Lessons Learned

## Dynamic Programming
- **Combinations vs. Permutations (Coin Change II / Combination Sum IV)**: Emphasize *why* loop ordering changes the result. Explicitly connect the "coins in outer loop" approach to a space-optimized 2D DP. This makes the `(2, 1)` vs `(1, 2)` duplicate prevention completely obvious to learners.
- **Base Case Initialization**: Explicitly contrast `0` vs `float('inf')` initialization. `min()` DP problems need `inf`, but counting/ways DP problems need `0` (with `dp[0] = 1`).
- **Greedy Counter-Examples**: Always provide concrete counter-examples for why Greedy algorithms fail on DP problems (e.g., `coins = [1, 3, 4]`, `amount = 6` or `nums = [2, 7, 9, 3, 1]`).
- **House Robber Complexity**: Ensure explanation for House Robber emphasizes the state transitions avoiding adjacent elements clearly.
- **House Robber II Logic**: Explain how separating the problem into `nums[:-1]` and `nums[1:]` transforms the circular constraint into two simple linear problems.
- **House Robber III DP on Trees**: Clarify that it's just post-order traversal where each step returns `(max_if_robbed, max_if_skipped)`, and taking the current node STRICTLY means skipping children, while skipping the current node allows taking the MAX of robbing or skipping each child.
- **First/Last Occurrence Tracking**: When writing documentation or guides, prefer strict bounds tracing.
- **Edit Distance Recurrence Intuition**: Prefix lengths vs array indices are a massive source of confusion for learners. Always clearly distinguish between "length of prefix `i`" and "character index `i-1`".
- **Edit Distance 1D Optimization**: The logic for maintaining the `prev_diagonal` (which represents `dp[i-1][j-1]`) in the 1D space-optimized DP matrix is notoriously tricky to understand and explain. Break it down explicitly.
- **Burst Balloons Interval Boundaries**: Using exclusive bounds (e.g. `strictly between left and right`) and tracking `length = right - left` makes interval DP logic, tabulation iterations, and visual walkthroughs vastly clearer for learners than using inclusive bounds.

## Python DP Style
- Add explicit type hints (e.g., `coins: list[int]`).
- Clean docstrings specifying Time/Space complexity.
- Optimize inner loops (e.g., `for i in range(coin, amount + 1):`) instead of adding `if i - coin >= 0:` when traversing forward.

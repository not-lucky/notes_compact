# Chapter 09: Dynamic Programming

Dynamic Programming (DP) is often considered one of the most challenging topics in technical interviews. It is a method for solving complex problems by breaking them down into simpler subproblems. Mastering DP patterns is essential for success at top tech companies.

## Why DP Matters for Interviews

1. **High Interview Frequency**: DP is heavily tested; a significant percentage of coding interviews at FANG+ companies feature DP problems.
2. **Demonstrates Problem-Solving**: It shows your ability to break down complex problems into manageable, overlapping subproblems.
3. **Highlights Optimization Skills**: It proves your understanding of time-space tradeoffs, recursion, and algorithmic efficiency.
4. **Tests Pattern Recognition**: Many seemingly unique or difficult problems are actually variations of a few core DP patterns.

---

## The Two Key Properties of DP

For Dynamic Programming to be applicable, a problem must exhibit two key properties:

1. **Optimal Substructure**: The optimal solution to a problem can be constructed from the optimal solutions of its subproblems. If you have the best answers for the smaller pieces, you can combine them to get the best answer for the whole.
2. **Overlapping Subproblems**: The problem can be broken down into subproblems which are reused several times. Instead of recomputing these subproblems every time, DP stores their results (memoization/tabulation) to avoid redundant work.

If a problem has optimal substructure but *no* overlapping subproblems, a **Divide and Conquer** approach (like Merge Sort) is used instead.

---

## Top-Down vs. Bottom-Up

There are two primary ways to implement a DP solution:

1. **Top-Down (Memoization)**:
   - Starts with the main problem and recursively breaks it down into subproblems.
   - Caches the results of subproblems in a hash map or array as they are computed.
   - **Pros**: Easy to write if you understand recursion; only computes needed subproblems.
   - **Cons**: Overhead from recursive function calls; risk of stack overflow for deep recursion.

2. **Bottom-Up (Tabulation)**:
   - Solves all subproblems first, starting from the smallest (base cases), and builds up to the main problem.
   - Uses a table (array/matrix) to store results.
   - **Pros**: No recursion overhead; easy to optimize space complexity.
   - **Cons**: Can be unintuitive to figure out the iteration order; computes all subproblems even if some aren't strictly necessary.

---

## The DP Problem-Solving Framework

When faced with a DP problem, follow these 5 steps systematically:

1. **Define the State**: What does `dp[i]` or `dp[i][j]` represent? Clearly articulate what the variables track (e.g., "the maximum profit up to day `i`").
2. **Define the Recurrence Relation**: How does the current state relate to previous states? (e.g., `dp[i] = dp[i-1] + dp[i-2]`). This is the hardest and most important step.
3. **Define Base Cases**: What are the initial, simplest values that bootstrap the recurrence? (e.g., `dp[0] = 0`, `dp[1] = 1`).
4. **Define the Final Answer**: Where is the final answer stored? Is it `dp[n]`, the `max` of the entire `dp` array, or something else?
5. **Optimize Space**: Can we reduce the space complexity? If `dp[i]` only depends on `dp[i-1]` and `dp[i-2]`, we can often reduce $O(N)$ space to $O(1)$ by just keeping track of the last two values.

---

## DP Patterns Overview

| Pattern | Examples | Key Insight | Typical Space Opt. |
| :--- | :--- | :--- | :--- |
| **1D Linear** | Climbing Stairs, House Robber | State depends on 1-2 previous states | $O(N) \rightarrow O(1)$ |
| **2D Grid** | Unique Paths, Min Path Sum | State depends on up/left adjacent cells | $O(M \times N) \rightarrow O(N)$ |
| **Knapsack (0/1)** | Subset Sum, Partition Equal | Decide to include or exclude an item | $O(N \times W) \rightarrow O(W)$ |
| **Unbounded Knapsack** | Coin Change | Items can be used multiple times | $O(N \times W) \rightarrow O(W)$ |
| **String / Sequences** | LCS, Edit Distance | Compare characters of two strings/arrays | $O(M \times N) \rightarrow O(\min(M, N))$ |
| **Interval** | Burst Balloons, Matrix Chain | Merge ranges, `dp[i][j]` represents interval | $O(N^2)$, rarely optimized further |
| **State Machine** | Buy & Sell Stock with Cooldown | Finite states (e.g., hold, empty, cooldown) | $O(N \times \text{states}) \rightarrow O(\text{states})$ |
| **Bitmask DP** | TSP, Matchsticks to Square | Represent small sets of items using integers | $O(2^N \times N)$ |

---

## Time Complexity Guidelines

| DP Type | Typical Time Complexity | Typical Space Complexity |
| :--- | :--- | :--- |
| **1D DP** | $O(N)$ | $O(N)$ or $O(1)$ |
| **2D DP** | $O(M \times N)$ | $O(M \times N)$ or $O(\min(M, N))$ |
| **Interval DP** | $O(N^3)$ | $O(N^2)$ |
| **DP + Binary Search**| $O(N \log N)$ | $O(N)$ |
| **Bitmask DP** | $O(2^N \cdot N)$ | $O(2^N)$ |

---

## Quick Reference: Common State Transitions

```python
# 1D Linear (e.g., Fibonacci, Climbing Stairs)
dp[i] = dp[i-1] + dp[i-2]

# 2D Grid (e.g., Unique Paths)
dp[i][j] = dp[i-1][j] + dp[i][j-1]

# 0/1 Knapsack (Wt array for weights, Val array for values)
# dp[i][w] = max value using first i items with capacity w
dp[i][w] = max(dp[i-1][w], dp[i-1][w-wt[i-1]] + val[i-1])

# Unbounded Knapsack (e.g., Coin Change)
# dp[i][w] = min coins to make amount w using first i coin denominations
dp[i][w] = min(dp[i-1][w], dp[i][w-coins[i-1]] + 1)

# String DP (e.g., Longest Common Subsequence)
if s1[i-1] == s2[j-1]:
    dp[i][j] = dp[i-1][j-1] + 1
else:
    dp[i][j] = max(dp[i-1][j], dp[i][j-1])

# Interval DP (e.g., Matrix Chain Multiplication)
# Cost of combining intervals [i...k] and [k+1...j]
dp[i][j] = min(dp[i][k] + dp[k+1][j] + cost(i, k, j) for k in range(i, j))
```

---

## Common Interview Problems by Company

| Company | Favorite DP Problems |
| :--- | :--- |
| **Google** | Word Break, Coin Change, Longest Increasing Subsequence (LIS), Maximize/Minimize Paths |
| **Meta** | Edit Distance, Decode Ways, Buy & Sell Stock variants, Valid Palindrome III |
| **Amazon** | House Robber, Coin Change, Knapsack variations, Word Break |
| **Microsoft** | Longest Common Subsequence (LCS), Unique Paths, Min Path Sum, Wildcard Matching |
| **Apple** | Palindrome DP, Word Break, Maximum Subarray |

---

## Chapter Contents

| # | Topic | Key Concepts |
| :--- | :--- | :--- |
| 01 | [DP Fundamentals](./01-dp-fundamentals.md) | Core properties, recognition, Top-down vs Bottom-up |
| 02 | [Memoization vs Tabulation](./02-memoization-vs-tabulation.md) | Practical differences and tradeoffs |
| 03 | [1D DP Basics](./03-1d-dp-basics.md) | Fibonacci, Climbing Stairs, Min Cost Climbing Stairs |
| 04 | [House Robber](./04-house-robber.md) | Linear DP variants, handling circular arrays |
| 05 | [Coin Change](./05-coin-change.md) | Unbounded knapsack, minimization vs maximization |
| 06 | [Longest Increasing Subsequence](./06-longest-increasing-subsequence.md) | Standard $O(N^2)$ DP, optimized $O(N \log N)$ with Binary Search |
| 07 | [2D DP Basics](./07-2d-dp-basics.md) | Grid traversal, Unique Paths, Obstacles, Space optimization |
| 08 | [Longest Common Subsequence](./08-longest-common-subsequence.md) | String comparison, building the 2D DP table |
| 09 | [Edit Distance](./09-edit-distance.md) | Levenshtein distance, insert/delete/replace operations |
| 10 | [0/1 Knapsack](./10-knapsack-01.md) | Include/exclude pattern, 2D to 1D space optimization |
| 11 | [Unbounded Knapsack](./11-knapsack-unbounded.md) | Unlimited item usage, comparison with 0/1 Knapsack |
| 12 | [Palindrome DP](./12-palindrome-dp.md) | Longest Palindromic Substring vs Subsequence |
| 13 | [Word Break](./13-word-break.md) | Dictionary problems, string partitioning |
| 14 | [Regex Matching](./14-regex-matching.md) | Pattern matching, handling '*' and '.' |
| 15 | [Buy & Sell Stock](./15-buy-sell-stock.md) | State machine approach, handling cooldowns/fees |
| 16 | [Matrix Chain](./16-matrix-chain.md) | Optimal multiplication, interval DP basics |
| 17 | [Burst Balloons](./17-burst-balloons.md) | Advanced interval DP, thinking in reverse |
| 18 | [DP on Strings](./18-dp-on-strings.md) | Advanced string manipulation, distinct subsequences |

---

## Start: [01-dp-fundamentals.md](./01-dp-fundamentals.md)

Begin with understanding the core principles of Dynamic Programming.

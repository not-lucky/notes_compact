# Chapter 09: Dynamic Programming

Dynamic Programming is the most heavily tested topic in FANG+ interviews. Mastering DP patterns is essential for success.

## Why DP Matters

1. **Interview frequency**: 30-40% of coding questions involve DP
2. **Problem-solving skill**: Shows ability to break down complex problems
3. **Optimization thinking**: Demonstrates understanding of time-space tradeoffs
4. **Pattern recognition**: Many problems are variations of core patterns

---

## The Two Key Properties

For DP to apply, a problem must have:

1. **Optimal Substructure**: Optimal solution contains optimal solutions to subproblems
2. **Overlapping Subproblems**: Same subproblems solved multiple times

---

## DP Patterns Overview

| Pattern       | Problems                      | Key Insight                          |
| ------------- | ----------------------------- | ------------------------------------ |
| 1D Linear     | Climbing stairs, House Robber | State depends on previous 1-2 states |
| 2D Grid       | Unique Paths, Min Path Sum    | State depends on up/left cells       |
| Knapsack      | Subset Sum, Coin Change       | Include/exclude decisions            |
| String DP     | LCS, Edit Distance            | Compare characters                   |
| Interval DP   | Burst Balloons, Matrix Chain  | Merge ranges                         |
| State Machine | Stock Problems                | Finite states with transitions       |
| Subsequence   | LIS, Palindrome               | Character inclusion decisions        |

---

## Chapter Contents

| #   | Topic                                                                    | Key Concepts                 |
| --- | ------------------------------------------------------------------------ | ---------------------------- |
| 01  | [DP Fundamentals](./01-dp-fundamentals.md)                               | Core properties, recognition |
| 02  | [Memoization vs Tabulation](./02-memoization-vs-tabulation.md)           | Top-down vs bottom-up        |
| 03  | [1D DP Basics](./03-1d-dp-basics.md)                                     | Fibonacci, Climbing Stairs   |
| 04  | [House Robber](./04-house-robber.md)                                     | Linear DP variants           |
| 05  | [Coin Change](./05-coin-change.md)                                       | Unbounded knapsack pattern   |
| 06  | [Longest Increasing Subsequence](./06-longest-increasing-subsequence.md) | LIS with O(n log n)          |
| 07  | [2D DP Basics](./07-2d-dp-basics.md)                                     | Grid traversal DP            |
| 08  | [Longest Common Subsequence](./08-longest-common-subsequence.md)         | String comparison            |
| 09  | [Edit Distance](./09-edit-distance.md)                                   | Levenshtein distance         |
| 10  | [0/1 Knapsack](./10-knapsack-01.md)                                      | Include/exclude pattern      |
| 11  | [Unbounded Knapsack](./11-knapsack-unbounded.md)                         | Unlimited items              |
| 12  | [Palindrome DP](./12-palindrome-dp.md)                                   | Substring/subsequence        |
| 13  | [Word Break](./13-word-break.md)                                         | Dictionary problems          |
| 14  | [Regex Matching](./14-regex-matching.md)                                 | Pattern matching DP          |
| 15  | [Buy & Sell Stock](./15-buy-sell-stock.md)                               | State machine DP             |
| 16  | [Matrix Chain](./16-matrix-chain.md)                                     | Optimal multiplication       |
| 17  | [Burst Balloons](./17-burst-balloons.md)                                 | Interval DP                  |
| 18  | [DP on Strings](./18-dp-on-strings.md)                                   | Advanced string DP           |

---

## The DP Problem-Solving Framework

```
1. Define state: What does dp[i] or dp[i][j] represent?
2. Define recurrence: How does current state relate to previous?
3. Define base cases: What are the initial values?
4. Define answer: Where is the final answer?
5. Optimize space: Can we reduce from O(n²) to O(n)?
```

---

## Time Complexity Patterns

| DP Type            | Typical Time | Typical Space    |
| ------------------ | ------------ | ---------------- |
| 1D DP              | O(n)         | O(n) or O(1)     |
| 2D DP              | O(n × m)     | O(n × m) or O(m) |
| Interval DP        | O(n³)        | O(n²)            |
| DP + Binary Search | O(n log n)   | O(n)             |
| Bitmask DP         | O(2ⁿ × n)    | O(2ⁿ)            |

---

## Common Interview Problems by Company

| Company   | Favorite DP Problems                |
| --------- | ----------------------------------- |
| Google    | Word Break, Coin Change, LIS        |
| Meta      | Edit Distance, Decode Ways, Stock   |
| Amazon    | House Robber, Coin Change, Knapsack |
| Microsoft | LCS, Unique Paths, Min Path Sum     |
| Apple     | Palindrome DP, Word Break           |

---

## Quick Reference: State Transitions

```python
# 1D Linear
dp[i] = dp[i-1] + dp[i-2]          # Fibonacci-like

# 2D Grid
dp[i][j] = dp[i-1][j] + dp[i][j-1] # Path counting

# Knapsack
dp[i][w] = max(dp[i-1][w], dp[i-1][w-wt[i]] + val[i])

# String DP
dp[i][j] = dp[i-1][j-1] + 1 if match else max(dp[i-1][j], dp[i][j-1])

# Interval DP
dp[i][j] = min(dp[i][k] + dp[k+1][j] + cost for k in range(i, j))
```

---

## Start: [01-dp-fundamentals.md](./01-dp-fundamentals.md)

Begin with understanding the core principles of Dynamic Programming.

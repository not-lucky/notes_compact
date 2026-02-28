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
2. **Define the Recurrence Relation**: How does the current state relate to previous states? (e.g., `dp[i] = max(dp[i-1], dp[i-2] + nums[i])`). This is the hardest and most important step.
3. **Define Base Cases**: What are the initial, simplest values that bootstrap the recurrence? (e.g., `dp[0] = 0`, `dp[1] = nums[0]`).
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
| **Interval** | Burst Balloons, Palindromes | Solve sub-intervals and expand outward | $O(N^2)$, rarely optimized further |
| **State Machine** | Buy & Sell Stock series | Finite states (e.g., hold, empty, cooldown) | $O(N \times \text{states}) \rightarrow O(\text{states})$ |

---

## Time/Space Complexity Guidelines

| DP Pattern | Typical Time | Typical Space | Space Optimized |
| :--- | :--- | :--- | :--- |
| **1D DP** | $O(N)$ | $O(N)$ | $O(1)$ |
| **2D Grid DP** | $O(M \times N)$ | $O(M \times N)$ | $O(N)$ |
| **0/1 Knapsack** | $O(N \times W)$ | $O(N \times W)$ | $O(W)$ |
| **String DP** | $O(M \times N)$ | $O(M \times N)$ | $O(\min(M, N))$ |
| **Interval DP** | $O(N^3)$ | $O(N^2)$ | N/A |
| **State Machine** | $O(N)$ | $O(N)$ | $O(1)$ |

---

## Chapter Contents

This chapter is structured progressively. Master the early concepts before tackling the harder patterns.

### Core Foundations
| File | Topic | Focus |
| :--- | :--- | :--- |
| [01-dp-fundamentals.md](./01-dp-fundamentals.md) | **DP Fundamentals** | Core properties, recognition, Top-down vs Bottom-up |
| [02-memoization-vs-tabulation.md](./02-memoization-vs-tabulation.md) | **Memoization vs Tabulation** | Practical differences, tradeoffs, translation |

### Linear & Grid Patterns
| File | Topic | Focus |
| :--- | :--- | :--- |
| [03-1d-dp-basics.md](./03-1d-dp-basics.md) | **1D DP Basics** | Fibonacci, Climbing Stairs, State transitions |
| [04-house-robber.md](./04-house-robber.md) | **House Robber** | Adjacent element constraints, Circular arrays |
| [07-2d-dp-basics.md](./07-2d-dp-basics.md) | **2D DP Basics** | Grid traversal, Obstacles, Array padding |
| [15-buy-sell-stock.md](./15-buy-sell-stock.md) | **State Machine DP** | Modeling multiple states (Buy, Sell, Cooldown) |

### Knapsack & Combinatorics
| File | Topic | Focus |
| :--- | :--- | :--- |
| [10-knapsack-01.md](./10-knapsack-01.md) | **0/1 Knapsack** | Include/exclude pattern, Target Sum |
| [11-knapsack-unbounded.md](./11-knapsack-unbounded.md) | **Unbounded Knapsack** | Unlimited item usage, Coin Change II |
| [05-coin-change.md](./05-coin-change.md) | **Coin Change** | Minimization knapsack, Combinations vs Permutations |

### String & Sequence Patterns
| File | Topic | Focus |
| :--- | :--- | :--- |
| [08-longest-common-subsequence.md](./08-longest-common-subsequence.md) | **LCS** | Subsequence comparison, 2D to 1D space opt |
| [09-edit-distance.md](./09-edit-distance.md) | **Edit Distance** | Insert/delete/replace operations |
| [18-dp-on-strings.md](./18-dp-on-strings.md) | **DP on Strings** | Decodings, Distinct Subsequences, Interleaving |
| [13-word-break.md](./13-word-break.md) | **Word Break** | Dictionary partitioning, Recursion with Memo |
| [14-regex-matching.md](./14-regex-matching.md) | **Regex Matching** | Branching decisions, handling `*` and `?` |

### Advanced Interval DP
| File | Topic | Focus |
| :--- | :--- | :--- |
| [06-longest-increasing-subsequence.md](./06-longest-increasing-subsequence.md) | **LIS** | $O(N^2)$ DP, optimized $O(N \log N)$ with Binary Search |
| [12-palindrome-dp.md](./12-palindrome-dp.md) | **Palindrome DP** | Interval expanding, LPS vs Longest Substring |
| [16-matrix-chain.md](./16-matrix-chain.md) | **Matrix Chain** | Splitting intervals, the $O(N^3)$ pattern |
| [17-burst-balloons.md](./17-burst-balloons.md) | **Burst Balloons** | Reverse interval thinking, Virtual boundaries |

---

## Start Here
Begin your journey with [**01 DP Fundamentals**](./01-dp-fundamentals.md).
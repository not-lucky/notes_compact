# Chapter 09: Dynamic Programming

Dynamic Programming (DP) is often considered one of the most intimidating topics in technical interviews. At its core, DP is an algorithmic paradigm that solves complex problems by breaking them down into simpler, overlapping subproblems.

Rather than computing the same subproblem multiple times, DP solves each subproblem once and saves its answer (a technique known as **memoization** or **tabulation**). Mastering DP patterns is an essential step for succeeding in technical interviews at top-tier companies.

## Why DP Matters

1. **High Interview Frequency**: DP problems are heavily tested in coding interviews.
2. **Demonstrates Optimization Skills**: It proves your understanding of time-space tradeoffs, recursion depth, and computational efficiency.
3. **Highlights Problem Solving**: Successfully modeling a problem's state and transitions demonstrates strong analytical capabilities.
4. **Pattern Recognition**: The vast majority of DP problems are variations of a few foundational patterns. Once you learn the patterns, you can solve hundreds of problems.

---

## The Two Key Properties of DP

For Dynamic Programming to be applicable, a problem must exhibit two specific mathematical properties:

1. **Optimal Substructure**:
   The optimal solution to the overall problem can be constructed from the optimal solutions of its subproblems. If you have the best answers for the smaller pieces, you can combine them to derive the best answer for the entire problem.
   *(Example: The shortest path from A to C through B consists of the shortest path from A to B, and the shortest path from B to C.)*

2. **Overlapping Subproblems**:
   The problem can be broken down into subproblems which are reused multiple times. Instead of recomputing these subproblems every time they are encountered, DP stores their results to avoid redundant work.
   *(Example: In the recursive Fibonacci sequence calculation, `fib(3)` is computed multiple times if we don't cache the results).*

> **Note:** If a problem has an optimal substructure but *no* overlapping subproblems, a **Divide and Conquer** approach (like Merge Sort or Quick Sort) is used instead of DP.

---

## Top-Down vs. Bottom-Up Approaches

There are two primary paradigms for implementing a Dynamic Programming solution:

### 1. Top-Down (Memoization)
- **Concept**: Starts with the main problem and recursively breaks it down into smaller subproblems.
- **Mechanism**: Caches the results of subproblems in a data structure (like a hash map or an array) as they are computed. When a subproblem is encountered again, the cached result is returned.
- **Pros**: Intuitive to write if you understand the recursive mathematical recurrence. It naturally only computes the subproblems that are strictly necessary.
- **Cons**: Overhead from recursive function calls. It carries a risk of stack overflow for very deep recursion limits in certain languages (like Python).

### 2. Bottom-Up (Tabulation)
- **Concept**: Solves all subproblems first, starting from the smallest (the base cases), and builds up iteratively to the main problem.
- **Mechanism**: Uses a table (usually a 1D or 2D array) to store results. Loops are used to fill the table.
- **Pros**: No recursion overhead or stack overflow risk. It is often easier to apply space complexity optimization.
- **Cons**: Can be unintuitive to figure out the correct iteration order. It may compute all subproblems, even if some aren't strictly necessary for the final answer.

---

## The 6-Step DP Problem-Solving Framework

When faced with a DP problem, follow this systematic framework to derive the solution:

1. **Define the State (The Variables)**
   What does your state represent? What variables do you need to uniquely identify a subproblem?
   *Example: Let `dp[i]` represent the maximum profit we can make by robbing houses up to index `i`.*

2. **Formulate the Recurrence Relation (The Transitions)**
   How does the current state relate to previous states? This is the core logic of the problem.
   *Example: To maximize profit at house `i`, we either rob it (adding its value to the profit from house `i-2`) or skip it (taking the profit from house `i-1`). Thus, `dp[i] = max(dp[i-1], dp[i-2] + nums[i])`.*

3. **Establish the Base Cases**
   What are the simplest subproblems that bootstrap the recurrence?
   *Example: `dp[0] = nums[0]` (only one house to rob), and `dp[1] = max(nums[0], nums[1])` (rob the better of the first two).*

4. **Determine the Iteration Order (For Tabulation)**
   In what order should you compute the states so that when you calculate state `dp[i]`, all necessary previous states have already been computed?
   *Example: Loop `i` from `2` to `n-1`.*

5. **Identify the Final Answer**
   Where is the final answer stored after all computations?
   *Example: Is it `dp[n-1]`, the `max` value in the entire `dp` array, or `dp[n][W]`?*

6. **Optimize Space (Optional but Recommended)**
   Can we reduce the space complexity? If `dp[i]` only depends on a few previous states (e.g., `dp[i-1]` and `dp[i-2]`), we can often reduce $O(N)$ space to $O(1)$ by just maintaining pointers to the last few values.

---

## DP Patterns & Complexity Guidelines

Recognizing the pattern is 90% of the battle. Below are the most common DP patterns, their identifying traits, and typical complexities.

| DP Pattern | Key Insight / Strategy | Time Complexity | Space Complexity | Space Optimized |
| :--- | :--- | :--- | :--- | :--- |
| **1D Linear** | State depends on 1 or 2 previous states (e.g., Fibonacci, House Robber). | $O(N)$ | $O(N)$ | $O(1)$ |
| **2D Grid** | State depends on adjacent cells, usually up/left or down/right (e.g., Unique Paths). | $O(M \times N)$ | $O(M \times N)$ | $O(N)$ |
| **0/1 Knapsack** | Decide to include or exclude each item exactly once (e.g., Partition Equal Subset Sum). | $O(N \times W)$ | $O(N \times W)$ | $O(W)$ |
| **Unbounded Knapsack** | Items can be used an unlimited number of times (e.g., Coin Change). | $O(N \times W)$ | $O(N \times W)$ | $O(W)$ |
| **Strings & Sequences** | Compare characters of two strings/arrays (e.g., Longest Common Subsequence). | $O(M \times N)$ | $O(M \times N)$ | $O(\min(M, N))$ |
| **State Machine** | Manage multiple interwoven states like Buy, Sell, and Cooldown (e.g., Stock problems). | $O(N)$ | $O(N)$ | $O(1)$ |
| **Interval DP** | Solve for smaller sub-intervals and expand outwards (e.g., Burst Balloons, Palindromes). | $O(N^2)$ to $O(N^3)$ | $O(N^2)$ | N/A |

> *Note: $N$ typically represents the number of items or length of the array, $W$ represents the target capacity, and $M$ represents the secondary dimension.*

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

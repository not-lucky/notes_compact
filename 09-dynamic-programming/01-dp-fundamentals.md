# DP Fundamentals

## Overview

Dynamic Programming (DP) is a powerful algorithmic technique that solves complex problems by breaking them down into simpler, overlapping subproblems. It stores the solutions to these subproblems to avoid redundant computation, effectively trading space for time.

Think of DP as **"smart recursion with memory."**

## The Core Problem DP Solves

### The Redundancy Problem
In naive recursion, we often solve the exact same subproblems exponentially many times.
For example, computing `Fibonacci(50)` naively would calculate `Fibonacci(25)` over 75,000 times! The time complexity becomes $O(2^N)$.

### The Memory Solution
If we store (memoize) the answer to each subproblem the *first* time we compute it, subsequent lookups take $O(1)$ time. This "state compression" transforms exponential-time algorithms into polynomial-time ones (like $O(N)$ or $O(N^2)$).

## The Two Essential Properties of DP

A problem must have these two properties to be solvable with Dynamic Programming:

### 1. Optimal Substructure
The optimal solution to the main problem can be constructed from the optimal solutions of its subproblems.

*Example (Shortest Path):* If the shortest path from city A to city C goes through city B, then the path from A to B must be the shortest possible path from A to B, and the path from B to C must be the shortest possible path from B to C.

### 2. Overlapping Subproblems
The problem can be broken down into subproblems which are reused multiple times.

*Example (Fibonacci):*
```text
           fib(5)
         /        \
    fib(4)        fib(3)
    /    \        /    \
fib(3)  fib(2)  fib(2) fib(1)
```
Notice how `fib(3)` and `fib(2)` are evaluated multiple times. This is where DP shines by caching the results.

---

## When NOT to Use DP

DP is powerful but not a silver bullet. Avoid it when:

1. **No Overlapping Subproblems (Use Divide & Conquer):**
   If subproblems are completely independent, caching doesn't help.
   *Example:* Merge Sort splits an array in half, but sorting the left half shares no work with sorting the right half.

2. **Greedy is Optimal:**
   If making the locally optimal choice at each step guarantees a globally optimal solution, a Greedy algorithm is simpler and often faster ($O(N)$ or $O(N \log N)$ vs DP's $O(N^2)$).
   *Example:* Activity selection (finding max non-overlapping intervals) can be solved optimally in $O(N \log N)$ by sorting by end times and picking greedily.

3. **State Space Explodes:**
   If tracking the state requires exponential memory (e.g., tracking subsets, bitmasks, or permutations of large sets), DP becomes unfeasible.
   *Example:* Traveling Salesperson Problem on 100 cities. Tracking the set of visited cities requires $2^{100}$ states.

4. **No Optimal Substructure:**
   If combining optimal subproblem solutions doesn't yield the global optimal.
   *Example:* Finding the *longest simple path* in a graph. The longest path from A to B and B to C might share vertices, making them impossible to combine into a valid simple path.

---

## The DP Problem-Solving Template (The FAST Method)

When tackling a DP problem, follow this structured framework:

### 1. **F**ind the State
What variables define a specific subproblem? How do you uniquely identify a subproblem?
*   **1D Array:** `dp[i]` represents the answer for the subarray `arr[0...i]`.
*   **2D Array:** `dp[i][j]` represents the answer using the first `i` items with capacity `j` (e.g., Knapsack).

### 2. **A**nalyze the Recurrence (The Transition)
How does the current state depend on previously computed states? What choices are available at this step?
*   *Example (Climbing Stairs):* To reach step `i`, you either came from step `i-1` or step `i-2`.
*   `dp[i] = dp[i-1] + dp[i-2]`

### 3. **S**et the Base Cases
What are the trivial subproblems that can be answered immediately without further calculation?
*   *Example (Fibonacci):* `dp[0] = 0`, `dp[1] = 1`.

### 4. **T**hink about the Answer
Where will the final answer be stored once the computation is complete?
*   Usually `dp[n]`, `dp[n][m]`, or `max(dp)`.

---

## The Four Stages of DP Solutions (Fibonacci Example)

Most DP problems can be solved in these four stages. In an interview, progressing through these shows deep understanding.

### Stage 1: Naive Recursion (Top-Down)
Translate the recurrence relation directly into code. Usually times out (TLE) due to overlapping subproblems.

```python
def fib_naive(n: int) -> int:
    # Base cases
    if n <= 1:
        return n
    # Recurrence
    return fib_naive(n - 1) + fib_naive(n - 2)

# Time Complexity: O(2^n) - Exponential branching
# Space Complexity: O(n) - Call stack depth
```

### Stage 2: Memoization (Top-Down DP)
Add a cache (dictionary or array) to the recursive function. Check the cache before computing, and save the result before returning.

```python
def fib_memo(n: int, memo: dict = None) -> int:
    if memo is None:
        memo = {}

    # Check cache
    if n in memo:
        return memo[n]

    # Base cases
    if n <= 1:
        return n

    # Compute and save to cache
    memo[n] = fib_memo(n - 1, memo) + fib_memo(n - 2, memo)
    return memo[n]

# Time Complexity: O(n) - Each state computed once
# Space Complexity: O(n) - Call stack + Memo dictionary
```

### Stage 3: Tabulation (Bottom-Up DP)
Eliminate recursion overhead by building a table (array) iteratively from the base cases up to `n`.

```python
def fib_tab(n: int) -> int:
    if n <= 1:
        return n

    # Initialize DP table
    dp = [0] * (n + 1)

    # Base cases
    dp[0] = 0
    dp[1] = 1

    # Build bottom-up
    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]

    return dp[n]

# Time Complexity: O(n) - Single loop
# Space Complexity: O(n) - DP array
```

### Stage 4: Space Optimization
Look at the recurrence. If `dp[i]` only depends on a few previous states (e.g., `dp[i-1]` and `dp[i-2]`), we don't need the entire array. We can just keep track of the required previous states.

```python
def fib_optimized(n: int) -> int:
    if n <= 1:
        return n

    # Only store the two previous states needed
    prev2 = 0 # dp[i-2]
    prev1 = 1 # dp[i-1]

    for _ in range(2, n + 1):
        curr = prev1 + prev2
        prev2 = prev1
        prev1 = curr

    return prev1

# Time Complexity: O(n)
# Space Complexity: O(1) - Constant variables only
```

---

## How to Recognize a DP Problem in Interviews

Look for these strong signals:

1. **The problem asks for an extreme value:**
   - "Find the **minimum/maximum** number of..."
   - "Find the **longest/shortest**..."
2. **The problem asks for counting:**
   - "Find the **total number of ways** to..."
   - "**Count all possible** valid..."
3. **The problem asks for feasibility:**
   - "**Is it possible** to reach/make/partition..."
4. **Constraints:**
   - Array/String length is typically $1000 \le N \le 10^5$ (pointing to $O(N)$ or $O(N \log N)$ DP) or $10 \le N \le 1000$ (pointing to $O(N^2)$ or $O(N^3)$ DP).

---

## Common Debugging Pitfalls

If your DP solution is failing, check these common mistakes:

1. **Incorrect Base Cases:** Are you starting with the right values? Did you account for `i=0` or empty string cases?
2. **Off-by-One Array Bounds:** When defining a DP array `dp = [0] * n`, remember the indices are `0` to `n-1`. Often, it's easier to use `dp = [0] * (n + 1)` so `dp[n]` represents the answer for length `n`.
3. **Missing State Transitions:** Did you consider *all* possible choices at the current state?
4. **Initialization:** Is your DP array initialized with `0`, `-1`, `float('inf')`, or `float('-inf')`? Choosing the wrong initial value (e.g., initializing with `0` when looking for a minimum) will break the logic.

## Summary

1. **Identify:** Optimal substructure + Overlapping subproblems.
2. **State:** Define what a subproblem represents.
3. **Transition:** Figure out how to build the current state from previous states.
4. **Optimize:** Recursion $\to$ Memoization $\to$ Tabulation $\to$ Space Optimization.
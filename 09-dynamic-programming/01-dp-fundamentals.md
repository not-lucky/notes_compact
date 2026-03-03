# Chapter 09: DP Fundamentals

## Overview

Dynamic Programming (DP) is a powerful algorithmic technique that solves complex problems by breaking them down into simpler, overlapping subproblems. It stores the solutions to these subproblems to avoid redundant computation, effectively trading space for time.

Think of DP as **"smart recursion with memory."**

## The Core Problem DP Solves

### The Redundancy Problem
In naive recursion, we often solve the exact same subproblems exponentially many times.
For example, computing `Fibonacci(50)` naively would calculate `Fibonacci(25)` over 75,000 times! The time complexity becomes $O(2^n)$.

### The Memory Solution
If we store (memoize) the answer to each subproblem the *first* time we compute it, subsequent lookups take $O(1)$ time. This "state compression" transforms exponential-time algorithms into polynomial-time ones (like $O(n)$ or $O(n^2)$).

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
   If making the locally optimal choice at each step guarantees a globally optimal solution, a Greedy algorithm is simpler and often faster ($O(n)$ or $O(n \log n)$ vs DP's $O(n^2)$).
   *Example:* Activity selection (finding max non-overlapping intervals) can be solved optimally in $O(n \log n)$ by sorting by end times and picking greedily.

3. **State Space Explodes:**
   If tracking the state requires exponential memory (e.g., tracking subsets, bitmasks, or permutations of large sets), standard DP might become unfeasible without advanced techniques or might not be the right approach.
   *Example:* Traveling Salesperson Problem on 100 cities. Tracking the set of visited cities requires $2^{100}$ states, which is computationally impossible to store.

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


## Example Walkthrough: Climbing Stairs

**Problem:** You are climbing a staircase. It takes `n` steps to reach the top. Each time you can either climb 1 or 2 steps. In how many distinct ways can you climb to the top?

### 1. Identify the State
`dp(i)` will represent the total number of distinct ways to reach step `i`.

### 2. Recurrence Relation
To reach step `i`, you must have come from either step `i-1` (by taking 1 step) or step `i-2` (by taking 2 steps).
Therefore, `dp(i) = dp(i-1) + dp(i-2)`.

### 3. Base Cases
- `dp(0) = 1` (1 way to stay at the ground: do nothing)
- `dp(1) = 1` (1 way to reach the first step: take 1 step)

### Solution: Top-Down Memoization
This is the required approach that solves the problem efficiently using recursion and caching.

```python
def climbStairs(n: int) -> int:
    memo = {}
    
    def dp(i: int) -> int:
        # Base cases
        if i <= 1:
            return 1
            
        # Check cache
        if i in memo:
            return memo[i]
            
        # Compute and memoize
        memo[i] = dp(i - 1) + dp(i - 2)
        return memo[i]
        
    return dp(n)
```

### Solution: Bottom-Up Tabulation
```python
def climbStairsTab(n: int) -> int:
    if n <= 1:
        return 1
        
    dp = [0] * (n + 1)
    dp[0] = 1
    dp[1] = 1
    
    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]
        
    return dp[n]
```

## The Four Stages of DP Solutions (Fibonacci Example)

Most DP problems can be solved by progressing through these four stages. In an interview, explaining this progression demonstrates a deep understanding of the concepts.

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
def fib_memo(n: int, memo: dict[int, int] | None = None) -> int:
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

# Time Complexity: O(n) - Each state computed exactly once
# Space Complexity: O(n) - Call stack + Memo dictionary
```
*Note: In modern Python, you can achieve this easily using `@functools.cache` or `@functools.lru_cache(maxsize=None)`, but understanding the underlying mechanism is crucial for interviews.*

### Stage 3: Tabulation (Bottom-Up DP)
Eliminate recursion overhead by building a table (array) iteratively from the base cases up to `n`.

```python
def fib_tab(n: int) -> int:
    if n <= 1:
        return n

    # Initialize DP table (size n + 1 to include index n)
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
    prev2 = 0  # Represents dp[i-2]
    prev1 = 1  # Represents dp[i-1]

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
   - Array/String length is typically $1000 \le n \le 10^5$ (pointing to $O(n)$ or $O(n \log n)$ DP) or $10 \le n \le 1000$ (pointing to $O(n^2)$ or $O(n^3)$ DP).

---

## Common Debugging Pitfalls

If your DP solution is failing, check these common mistakes:

1. **Incorrect Base Cases:** Are you starting with the right values? Did you account for `i=0` or empty string cases? Ensure your base cases cover all scenarios required by your recurrence.
2. **Off-by-One Array Bounds:** When defining a DP array `dp = [0] * n`, remember the indices are `0` to `n-1`. Often, it's easier to use `dp = [0] * (n + 1)` so `dp[n]` represents the answer for length `n`.
3. **Missing State Transitions:** Did you consider *all* possible choices at the current state? Make sure your recurrence handles every option.
4. **Initialization Values:** Is your DP array initialized with `0`, `-1`, `float('inf')`, or `float('-inf')`? Choosing the wrong initial value (e.g., initializing with `0` when looking for a minimum) will break the logic. For minimums, use `float('inf')`; for maximums, use `float('-inf')`.


## Progressive Problems to Master DP Fundamentals

To build a solid intuition for Dynamic Programming, solve these problems in order. They gradually introduce new concepts.

### 1. 1D Array / Sequence (Fibonacci Style)
These problems depend only on 1 or 2 previous states.

#### Min Cost Climbing Stairs (Easy)
Introduces choosing between costs at each step. You can start at step 0 or 1.
**Problem:** You are given an integer array `cost` where `cost[i]` is the cost of `i`th step on a staircase. Once you pay the cost, you can either climb one or two steps. You can either start from the step with index 0, or the step with index 1. Return the minimum cost to reach the top of the floor.

**Top-Down Memoization:**
```python
def minCostClimbingStairsMemo(cost: list[int]) -> int:
    memo = {}
    
    def dp(i: int) -> int:
        # Base case: we reached or passed the top step
        if i >= len(cost):
            return 0
            
        if i in memo:
            return memo[i]
            
        # Decision: take 1 step or 2 steps
        memo[i] = cost[i] + min(dp(i + 1), dp(i + 2))
        return memo[i]
        
    return min(dp(0), dp(1))
```

**Bottom-Up Tabulation:**
```python
def minCostClimbingStairsTab(cost: list[int]) -> int:
    n = len(cost)
    if n == 0:
        return 0
    if n == 1:
        return cost[0]

    dp = [0] * (n + 1)

    for i in range(2, n + 1):
        dp[i] = min(dp[i - 1] + cost[i - 1], dp[i - 2] + cost[i - 2])

    return dp[n]
```

#### House Robber (Medium)
Classic DP. You can't take adjacent items. `dp(i) = max(dp(i+1), nums[i] + dp(i+2))`
**Problem:** You are a professional robber planning to rob houses along a street. Each house has a certain amount of money stashed, the only constraint stopping you from robbing each of them is that adjacent houses have security systems connected and it will automatically contact the police if two adjacent houses were broken into on the same night. Given an integer array `nums` representing the amount of money of each house, return the maximum amount of money you can rob tonight without alerting the police.

**Top-Down Memoization:**
```python
def robMemo(nums: list[int]) -> int:
    memo = {}
    
    def dp(i: int) -> int:
        if i >= len(nums):
            return 0
            
        if i in memo:
            return memo[i]
            
        # Decision: Rob this house (and skip next), or skip this house
        rob_current = nums[i] + dp(i + 2)
        skip_current = dp(i + 1)
        
        memo[i] = max(rob_current, skip_current)
        return memo[i]
        
    return dp(0)
```

**Bottom-Up Tabulation:**
```python
def robTab(nums: list[int]) -> int:
    if not nums:
        return 0
    if len(nums) == 1:
        return nums[0]

    dp = [0] * len(nums)
    dp[0] = nums[0]
    dp[1] = max(nums[0], nums[1])

    for i in range(2, len(nums)):
        dp[i] = max(dp[i - 1], dp[i - 2] + nums[i])

    return dp[-1]
```

### 2. 1D Array (Longest Increasing Subsequence Style)
These problems depend on *all* previous states, not just the last few.

#### Longest Increasing Subsequence (Medium)
Core pattern. `dp(i)` finds the longest increasing subsequence starting at index `i`.
**Problem:** Given an integer array `nums`, return the length of the longest strictly increasing subsequence. A subsequence is a sequence that can be derived from an array by deleting some or no elements without changing the order of the remaining elements.

**Top-Down Memoization:**
```python
def lengthOfLISMemo(nums: list[int]) -> int:
    memo = {}
    
    def dp(i: int) -> int:
        if i in memo:
            return memo[i]
            
        # Minimum length is 1 (the element itself)
        max_len = 1
        
        # Look ahead at all valid next elements
        for j in range(i + 1, len(nums)):
            if nums[j] > nums[i]:
                max_len = max(max_len, 1 + dp(j))
                
        memo[i] = max_len
        return memo[i]
        
    # We can start the LIS from any index
    if not nums: return 0
    return max(dp(i) for i in range(len(nums)))
```

**Bottom-Up Tabulation:**
```python
def lengthOfLISTab(nums: list[int]) -> int:
    if not nums:
        return 0

    dp = [1] * len(nums)

    for i in range(1, len(nums)):
        for j in range(i):
            if nums[i] > nums[j]:
                dp[i] = max(dp[i], dp[j] + 1)

    return max(dp)
```

### 3. 2D DP (Grid Style)
The state depends on coordinates `(r, c)` and transitions usually involve moving right/down.

#### Unique Paths (Medium)
Count ways to reach bottom-right.
**Problem:** There is a robot on an `m x n` grid. The robot is initially located at the top-left corner (i.e., `grid[0][0]`). The robot tries to move to the bottom-right corner (i.e., `grid[m - 1][n - 1]`). The robot can only move either down or right at any point in time. Given the two integers `m` and `n`, return the number of possible unique paths that the robot can take to reach the bottom-right corner.

**Top-Down Memoization:**
```python
def uniquePathsMemo(m: int, n: int) -> int:
    memo = {}
    
    def dp(r: int, c: int) -> int:
        # Out of bounds
        if r >= m or c >= n:
            return 0
        # Reached bottom-right corner
        if r == m - 1 and c == n - 1:
            return 1
            
        state = (r, c)
        if state in memo:
            return memo[state]
            
        # Move right + move down
        memo[state] = dp(r, c + 1) + dp(r + 1, c)
        return memo[state]
        
    return dp(0, 0)
```

**Bottom-Up Tabulation:**
```python
def uniquePathsTab(m: int, n: int) -> int:
    dp = [[1] * n for _ in range(m)]

    for r in range(1, m):
        for c in range(1, n):
            dp[r][c] = dp[r - 1][c] + dp[r][c - 1]

    return dp[m - 1][n - 1]
```

### 4. 2D DP (Knapsack Style)
The state depends on an `index` in the array and a `capacity` constraint.

#### Coin Change (Medium)
Unbounded Knapsack problem. You can reuse the same coin multiple times.
**Problem:** You are given an integer array `coins` representing coins of different denominations and an integer `amount` representing a total amount of money. Return the fewest number of coins that you need to make up that amount. If that amount of money cannot be made up by any combination of the coins, return `-1`. You may assume that you have an infinite number of each kind of coin.

**Top-Down Memoization:**
```python
def coinChangeMemo(coins: list[int], amount: int) -> int:
    memo = {}
    
    def dp(rem: int) -> int:
        if rem < 0:
            return -1
        if rem == 0:
            return 0
            
        if rem in memo:
            return memo[rem]
            
        min_coins = float('inf')
        
        for coin in coins:
            res = dp(rem - coin)
            if res >= 0 and res < min_coins:
                min_coins = 1 + res
                
        memo[rem] = min_coins if min_coins != float('inf') else -1
        return memo[rem]
        
    return dp(amount)
```

**Bottom-Up Tabulation:**
```python
def coinChangeTab(coins: list[int], amount: int) -> int:
    # dp[i] represents the minimum number of coins to make amount i
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0

    for i in range(1, amount + 1):
        for coin in coins:
            if i - coin >= 0:
                dp[i] = min(dp[i], dp[i - coin] + 1)

    return dp[amount] if dp[amount] != float('inf') else -1
```

## Summary

1. **Identify:** Optimal substructure and overlapping subproblems.
2. **State:** Define what a subproblem represents.
3. **Transition:** Figure out how to build the current state from previous states.
4. **Optimize:** Recursion $\to$ Memoization $\to$ Tabulation $\to$ Space Optimization.

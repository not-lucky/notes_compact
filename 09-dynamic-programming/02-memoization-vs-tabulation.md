# Memoization vs Tabulation

> **Prerequisites:** [01-dp-fundamentals](./01-dp-fundamentals.md)

## Overview

Both memoization (top-down) and tabulation (bottom-up) are techniques for implementing DP. They achieve the same asymptotic complexity but differ in implementation style, space optimization potential, and debugging ease.

## Building Intuition

**Why do two approaches exist?**

1. **Memoization mirrors human thinking**: When you think about Fibonacci(10), you naturally think "I need Fibonacci(9) and Fibonacci(8) first." This top-down, recursive decomposition is intuitive. Memoization simply adds caching to avoid recomputation.

2. **Tabulation mirrors computation order**: Computers execute sequentially. Tabulation explicitly builds solutions from smallest subproblems up, making dependencies clear and enabling space optimization.

3. **The Trade-off**:
   - **Memoization**: Easier to write (just add caching to recursion), only solves needed subproblems, but uses call stack and is harder to space-optimize.
   - **Tabulation**: Requires understanding dependency order upfront, solves all subproblems, but avoids stack overflow and enables O(1) space optimizations.

4. **Mental Model**: Think of memoization as "lazy evaluation with caching"—you only compute what you need. Tabulation is "eager evaluation"—you systematically build the entire solution table.

5. **When each shines**:
   - Memoization: When many subproblems are never needed (sparse state space), or when the recursive structure is complex.
   - Tabulation: When you need space optimization, or when the iteration order is straightforward.

## Interview Context

Understanding both approaches is essential because:

1. **Different problems favor different approaches**: Some easier top-down, others bottom-up
2. **Space optimization**: Tabulation often easier to optimize
3. **Interview flexibility**: Solve both ways to impress
4. **Debugging**: Memoization easier to debug initially

---

## When NOT to Use Each

### When NOT to Use Memoization

1. **Deep Recursion Risk**: Python has a default recursion limit of ~1000. For n = 10,000, memoization will stack overflow. Use `sys.setrecursionlimit()` cautiously or switch to tabulation.

2. **Space Optimization Needed**: When you only need the last few states (like Fibonacci needing only prev2 and prev1), tabulation allows O(1) space. Memoization inherently stores all computed states.

3. **Cache Overhead Matters**: Hash table lookups (O(1) average) have constant overhead. For very tight time constraints or simple recurrences, tabulation's array indexing is faster.

4. **Predictable Memory Usage**: Memoization's cache grows unpredictably. Tabulation allocates exactly what's needed upfront.

### When NOT to Use Tabulation

1. **Sparse State Space**: If only a small fraction of states are actually needed (e.g., subset sum with large capacity but few items), memoization avoids wasted computation.

2. **Complex Dependency Order**: When it's hard to determine which states to fill first (e.g., recursive tree structures), memoization's natural recursion handles dependencies automatically.

3. **Quick Prototyping**: Memoization is faster to write and debug. Use it first, then convert to tabulation if needed.

4. **Multi-dimensional States**: With 3+ dimensions, figuring out the correct loop nesting for tabulation is error-prone. Memoization handles this naturally.

---

## Overview Comparison

| Aspect | Memoization (Top-Down) | Tabulation (Bottom-Up) |
|--------|------------------------|------------------------|
| Direction | Start from problem, recurse down | Start from base, build up |
| Implementation | Recursive + cache | Iterative + table |
| Subproblems | Solves only needed ones | Solves all subproblems |
| Stack | Uses call stack (recursion limit) | No stack issues |
| Space optimization | Harder | Easier |
| Debugging | Often easier | State transitions clearer |

---

## Memoization (Top-Down)

### How It Works

1. Start with the original problem
2. Recursively break into subproblems
3. Before computing, check if already solved
4. Store result after computing

### Template

```python
def solve_memo(params):
    """
    Top-down DP with memoization.
    """
    memo = {}

    def dp(state):
        # Base case
        if is_base_case(state):
            return base_value

        # Check cache
        if state in memo:
            return memo[state]

        # Compute and cache
        result = compute_from_subproblems(state)
        memo[state] = result
        return result

    return dp(initial_state)
```

### Example: Fibonacci

```python
def fib_memo(n: int) -> int:
    """
    Memoized Fibonacci.

    Time: O(n)
    Space: O(n) for memo + O(n) for call stack
    """
    memo = {}

    def dp(i: int) -> int:
        if i <= 1:
            return i

        if i in memo:
            return memo[i]

        memo[i] = dp(i - 1) + dp(i - 2)
        return memo[i]

    return dp(n)
```

### Using @lru_cache (Python)

```python
from functools import lru_cache

def fib_lru(n: int) -> int:
    """
    Python's built-in memoization.

    Note: Clear cache with fib.cache_clear() if needed.
    """
    @lru_cache(maxsize=None)
    def dp(i: int) -> int:
        if i <= 1:
            return i
        return dp(i - 1) + dp(i - 2)

    return dp(n)
```

---

## Tabulation (Bottom-Up)

### How It Works

1. Create a table to store all subproblem solutions
2. Fill table starting from base cases
3. Use previously computed values for new entries
4. Final answer is in a specific table position

### Template

```python
def solve_tab(params):
    """
    Bottom-up DP with tabulation.
    """
    # Initialize table
    dp = [initial_value] * (size + 1)

    # Base cases
    dp[0] = base_value_0
    # dp[1] = base_value_1, etc.

    # Fill table
    for i in range(start, end + 1):
        dp[i] = compute_from_previous(dp, i)

    return dp[answer_index]
```

### Example: Fibonacci

```python
def fib_tab(n: int) -> int:
    """
    Tabulated Fibonacci.

    Time: O(n)
    Space: O(n)
    """
    if n <= 1:
        return n

    dp = [0] * (n + 1)
    dp[0] = 0
    dp[1] = 1

    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]

    return dp[n]
```

---

## Space Optimization

Tabulation often allows space reduction when only recent states are needed.

### Fibonacci: O(n) → O(1) Space

```python
def fib_optimized(n: int) -> int:
    """
    Only need last two values.

    Time: O(n)
    Space: O(1)
    """
    if n <= 1:
        return n

    prev2, prev1 = 0, 1

    for i in range(2, n + 1):
        curr = prev1 + prev2
        prev2 = prev1
        prev1 = curr

    return prev1
```

### 2D to 1D: Row-by-Row Processing

```python
# Original: O(n × m) space
dp = [[0] * m for _ in range(n)]
for i in range(n):
    for j in range(m):
        dp[i][j] = dp[i-1][j] + dp[i][j-1]

# Optimized: O(m) space
dp = [0] * m
for i in range(n):
    for j in range(m):
        dp[j] = dp[j] + dp[j-1]  # dp[j] is previous row's value
```

---

## When to Use Which?

### Use Memoization When:

1. **Not all subproblems needed**: Only computes what's required
2. **Natural recursive structure**: Problem is naturally recursive
3. **Quick prototyping**: Easier to implement and debug
4. **Sparse subproblem space**: Many subproblems unused

### Use Tabulation When:

1. **All subproblems needed**: No waste in computing all
2. **Space optimization needed**: Easier to reduce space
3. **Avoiding stack overflow**: Large n causes recursion limits
4. **Clear iteration order**: Natural left-to-right or top-to-bottom

---

## Side-by-Side Comparison: Unique Paths

### Problem

Count paths from top-left to bottom-right in m×n grid, moving only right or down.

### Memoization

```python
def unique_paths_memo(m: int, n: int) -> int:
    """
    Top-down with memoization.
    """
    memo = {}

    def dp(i: int, j: int) -> int:
        # Base cases
        if i == 0 or j == 0:
            return 1

        if (i, j) in memo:
            return memo[(i, j)]

        # Recurrence
        memo[(i, j)] = dp(i - 1, j) + dp(i, j - 1)
        return memo[(i, j)]

    return dp(m - 1, n - 1)
```

### Tabulation

```python
def unique_paths_tab(m: int, n: int) -> int:
    """
    Bottom-up with tabulation.
    """
    dp = [[1] * n for _ in range(m)]

    for i in range(1, m):
        for j in range(1, n):
            dp[i][j] = dp[i - 1][j] + dp[i][j - 1]

    return dp[m - 1][n - 1]
```

### Space Optimized

```python
def unique_paths_opt(m: int, n: int) -> int:
    """
    O(n) space.
    """
    dp = [1] * n

    for i in range(1, m):
        for j in range(1, n):
            dp[j] = dp[j] + dp[j - 1]

    return dp[n - 1]
```

---

## Handling Recursion Limits (Python)

```python
import sys
sys.setrecursionlimit(10000)  # Increase if needed

# Or use tabulation for very large n
```

---

## Common Pitfalls

### Memoization

```python
# WRONG: Mutable default argument
def dp(n, memo={}):  # Shared across calls!
    ...

# CORRECT: Initialize inside or pass explicitly
def dp(n, memo=None):
    if memo is None:
        memo = {}
    ...
```

### Tabulation

```python
# WRONG: Off-by-one in loop bounds
for i in range(n):  # Missing dp[n]!
    dp[i] = ...

# CORRECT: Include the target
for i in range(n + 1):
    dp[i] = ...
```

---

## Converting Between Approaches

### Memoization → Tabulation

1. Identify all unique states from memoization keys
2. Determine the order states should be filled (dependencies)
3. Create table of appropriate dimensions
4. Fill base cases
5. Iterate in dependency order

### Tabulation → Memoization

1. Identify the recurrence relation
2. Convert to recursive function
3. Add memoization cache
4. Handle base cases in recursion

---

## Performance Comparison

```python
import time

def benchmark(func, n):
    start = time.time()
    result = func(n)
    elapsed = time.time() - start
    return result, elapsed

# For n = 35:
# Naive recursion: ~3.5 seconds
# Memoization: ~0.00005 seconds
# Tabulation: ~0.00003 seconds
```

---

## Interview Tips

1. **Start with memoization**: Easier to derive from recursion
2. **Optimize if asked**: Convert to tabulation, then space-optimize
3. **Know both**: Some problems easier one way or another
4. **Mention tradeoffs**: Shows depth of understanding
5. **Watch recursion limits**: Mention when tabulation is necessary

---

## Key Takeaways

1. **Memoization**: Recursive, cache results, natural thinking
2. **Tabulation**: Iterative, build table, easier to optimize
3. **Both achieve same time complexity**: Just different approaches
4. **Space optimization**: Usually only with tabulation
5. **Choose based on problem**: Not one-size-fits-all

---

## Next: [03-1d-dp-basics.md](./03-1d-dp-basics.md)

Learn the fundamental 1D DP patterns with classic problems.

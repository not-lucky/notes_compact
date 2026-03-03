# Chapter 09: Memoization vs Tabulation

> **Prerequisites:** [01-dp-fundamentals](./01-dp-fundamentals.md)

## Overview

Dynamic Programming can be implemented using two main techniques: **Memoization (Top-Down)** and **Tabulation (Bottom-Up)**. Both approaches solve problems by breaking them into overlapping subproblems and storing the results to avoid redundant work. While they achieve the same asymptotic time complexity, they differ significantly in implementation style, memory usage, and potential for space optimization.

Understanding when and how to use each approach is critical for technical interviews.

---

## 1. Memoization (Top-Down)

### "Lazy Evaluation with Caching"
Start from the "top" (target problem) and recursively break it down. Solve subproblems only as needed and store results in a cache (array or dict). Return cached results to avoid re-computation.

### Use Cases & Tradeoffs
*   **Pros**:
    *   **Sparse State Spaces**: Computes only necessary subproblems.
    *   **Complex Dependencies**: Easier for trees, graphs, and complex state transitions.
    *   **Interview Velocity**: Faster to write and debug since it mirrors the mathematical recurrence directly.
*   **Cons**:
    *   **Overhead**: Recursion call stack overhead.
    *   **Stack Overflow**: Risk of hitting recursion limits (e.g., Python's 1000 frame limit).
    *   **Space Limits**: Difficult to space-optimize below $O(n)$ due to the call stack.

### Example: Fibonacci Sequence

**Mathematical Recurrence:**
$$
F(n) = \begin{cases}
0 & \text{if } n = 0 \\
1 & \text{if } n = 1 \\
F(n-1) + F(n-2) & \text{if } n \ge 2
\end{cases}
$$

**Python Implementation:**
```python
def fib_memo(n: int) -> int:
    """
    Top-Down DP with Memoization.
    Time: O(n) | Space: O(n) for cache + O(n) for call stack = O(n)
    """
    # Using an array for the cache is often faster than a dictionary
    # if the state space is dense and integer-based (0 to n)
    # Initialize with -1 to indicate uncomputed states
    memo = [-1] * (n + 1)

    def dp(i: int) -> int:
        # 1. Base cases
        if i <= 1:
            return i

        # 2. Check cache
        if memo[i] != -1:
            return memo[i]

        # 3. Compute, store, and return
        memo[i] = dp(i - 1) + dp(i - 2)
        return memo[i]

    return dp(n)
```

*(Note: In Python, you can also use `@functools.cache` or `@functools.lru_cache(None)` to automatically memoize a recursive function, which is great for competitive programming but often forbidden in interviews).*

---

## 2. Tabulation (Bottom-Up)

### "Eager Evaluation"
Start from the "bottom" (base cases) and build up iteratively to the target state. Fill an array/matrix systematically so all dependencies are computed before they are needed.

### Use Cases & Tradeoffs
*   **Pros**:
    *   **Dense State Spaces**: Optimal when almost all subproblems must be computed (common in arrays/strings).
    *   **Performance**: Iteration is faster than recursion.
    *   **Safety**: No call stack, so no stack overflow risk.
    *   **Space Optimization**: Allows massive space savings (e.g., $O(n) \rightarrow O(1)$).
*   **Cons**:
    *   **Computes Everything**: May evaluate unnecessary states if the space is sparse.
    *   **Harder to Formulate**: Loop order and state dependencies can be tricky to define initially.

### Example: Fibonacci Sequence

**Python Implementation:**
```python
def fib_tab(n: int) -> int:
    """
    Bottom-Up DP with Tabulation.
    Time: O(n) | Space: O(n)
    """
    if n <= 1:
        return n

    # 1. Initialize table (size n + 1 to include 0 through n)
    dp = [0] * (n + 1)

    # 2. Base cases
    dp[0] = 0
    dp[1] = 1

    # 3. Fill the table iteratively
    # Dependency order: to solve i, we need i-1 and i-2.
    # Looping 2 to n guarantees i-1 and i-2 are already solved.
    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]

    # 4. Return final answer
    return dp[n]
```

---

## 3. The Power of Space Optimization

If computing state `i` only requires states `i-1` and `i-2`, we don't need an array of size $N$. We can use a sliding window of constant variables.

```python
def fib_optimized(n: int) -> int:
    # Time: O(n) | Space: O(1)
    if n <= 1: return n
    prev2, prev1 = 0, 1
    for _ in range(2, n + 1):
        prev2, prev1 = prev1, prev1 + prev2
    return prev1
```

### 2D DP: $O(m \times n)$ Space $\rightarrow$ $O(n)$ Space

A similar logic applies to 2D DP problems (like grids or string comparisons). If computing a cell `dp[r][c]` only requires values from the *current row* `dp[r]` and the *previous row* `dp[r-1]`, we don't need an $m \times n$ matrix. We only need two rows of size $n$ (or sometimes just a single 1D array of size $n$ updated in-place). We will explore this further in the 2D DP sections.

---

## 4. Side-by-Side Comparison: Unique Paths

To see how the approaches differ on a real 2D problem, let's look at counting paths from the top-left to the bottom-right in an $m \times n$ grid, moving only right or down.

**Recurrence:**
$$
dp[r][c] = \begin{cases}
1 & \text{if } r = 0 \text{ or } c = 0 \\
dp[r-1][c] + dp[r][c-1] & \text{if } r > 0 \text{ and } c > 0
\end{cases}
$$

### Top-Down (Memoization)
Start at the destination `(m-1, n-1)` and ask: "How many ways to get here from the cell above, plus the cell to the left?"

```python
def unique_paths_memo(m: int, n: int) -> int:
    # Initialize cache with -1 to indicate uncomputed states
    memo = [[-1] * n for _ in range(m)]

    def dp(r, c):
        # Base case: top row or left column only has 1 straight path
        if r == 0 or c == 0:
            return 1

        # Check cache
        if memo[r][c] != -1:
            return memo[r][c]

        # Recursive step: sum of paths from cell above and cell to the left
        memo[r][c] = dp(r - 1, c) + dp(r, c - 1)
        return memo[r][c]

    # Start from bottom-right, recurse up to top-left
    return dp(m - 1, n - 1)
```

### Bottom-Up (Tabulation)
Start at `(0, 0)` and build the grid forwards. To compute cell `(r, c)`, we need the cell above it `(r-1, c)` and left of it `(r, c-1)`. Iterating row by row, column by column ensures these are always ready.

```python
def unique_paths_tab(m: int, n: int) -> int:
    # Initialize full table with 1s.
    # This cleverly handles the base cases (r=0 and c=0 are already 1)
    dp = [[1] * n for _ in range(m)]

    # Fill iteratively starting from 1 (since row 0 and col 0 are bases)
    for r in range(1, m):
        for c in range(1, n):
            dp[r][c] = dp[r - 1][c] + dp[r][c - 1]

    # Return bottom-right corner
    return dp[m - 1][n - 1]
```

### Space-Optimized Tabulation
Since `dp[r][c]` only depends on `dp[r-1][c]` (the cell directly above) and `dp[r][c-1]` (the cell directly to the left), we only need to keep the previous row's values. We can optimize the $O(m \times n)$ space to $O(n)$ by using a 1D array.

```python
def unique_paths_optimized(m: int, n: int) -> int:
    # Initialize a 1D array to represent the current row
    # The first row is all 1s
    dp = [1] * n

    for r in range(1, m):
        for c in range(1, n):
            # dp[c] is currently the value from the row above (dp[r-1][c])
            # dp[c-1] is the value from the current row, just computed (dp[r][c-1])
            dp[c] = dp[c] + dp[c - 1]

    return dp[n - 1]
```

---

## 5. Summary Cheat Sheet

| Feature | Memoization (Top-Down) | Tabulation (Bottom-Up) |
| :--- | :--- | :--- |
| **Strategy** | Start at target, break into subproblems. | Start at bases, build up to target. |
| **Implementation** | Recursion + Caching (Array/Hash map) | Iteration (Loops) + Array/Matrix |
| **Evaluation** | **Lazy**: Computes only needed states. | **Eager**: Computes all states. |
| **Speed** | Fast, but has recursion overhead. | Faster (no call stack overhead, better cache locality). |
| **Space** | $O(n)$ (Cache + Call Stack). | $O(n)$, but easily optimized to $O(1)$ or $O(m)$. |
| **Stack Overflow?** | Yes, risk for large inputs. | No. |
| **Ease of Writing** | Very intuitive, mimics math formula. | Harder to define state dependencies and loop bounds. |

---

## Interview Strategy Guide

1. **Start Top-Down:** In an interview, it is almost always best to start by discovering the recursive relation and writing the Memoized solution. It is faster to write, easier to reason about, and easier to verify correctness.
2. **Discuss Trade-offs:** Always mention to the interviewer: *"This top-down approach is $O(n)$ space due to the call stack. For massive inputs, we could hit recursion limits. We could convert this to bottom-up tabulation."*
3. **Convert to Bottom-Up (If Asked):** If the interviewer asks to optimize for stack space, rewrite it iteratively.
4. **Always Look for Space Optimization:** If you write a tabulated solution, always look for space optimization. If your loop only looks back $k$ steps, reduce your $O(n)$ array to $k$ variables! Tell the interviewer: *"I notice we only need the last two states, so we don't need to store the whole array."*

---

## Common Pitfalls & Mistakes

- **Python Default Arguments for Memo:** Never use `def dp(n, memo={}):`. Default mutable arguments in Python persist across completely separate function calls! If you must pass it as an argument, use `def dp(n, memo=None):` and then initialize `if memo is None: memo = {}`. Or better yet, initialize `memo = {}` *inside* the outer wrapper function.
- **Index Out of Bounds in Tabulation:** When writing tabulation loops, pay close attention to `range(n)` vs `range(n + 1)`. Often, DP arrays are sized `n + 1` to account for a base case at index 0 or similar boundary conditions.
- **Cache Initialization:** When using arrays for memoization, make sure to initialize them with a value that cannot be a valid answer (like `-1` or `float('inf')`), not `0` (if `0` can be a valid answer).

---


## Progressive Problems

To practice recognizing when to use Memoization vs Tabulation and space optimization, try these:

1. [Fibonacci Number](https://leetcode.com/problems/fibonacci-number/) (Easy) - Write it both top-down and bottom-up.
2. [Climbing Stairs](https://leetcode.com/problems/climbing-stairs/) (Easy) - Optimize bottom-up to O(1) space.
3. [N-th Tribonacci Number](https://leetcode.com/problems/n-th-tribonacci-number/) (Easy) - Good practice for tracking 3 previous states instead of 2.
4. [Unique Paths](https://leetcode.com/problems/unique-paths/) (Medium) - Practice 2D tabulation and converting it to O(n) space.

---

## Next Steps

Now that you understand the two core implementations of DP, we will apply them to real patterns.

**Next:** [03-1d-dp-basics](./03-1d-dp-basics.md)

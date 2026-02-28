# Memoization vs Tabulation

> **Prerequisites:** [01-dp-fundamentals](./01-dp-fundamentals.md)

## Overview

Dynamic Programming can be implemented using two main techniques: **Memoization (Top-Down)** and **Tabulation (Bottom-Up)**. Both approaches solve problems by breaking them into overlapping subproblems and storing the results to avoid redundant work. While they achieve the same asymptotic time complexity, they differ significantly in implementation style, memory usage, and potential for space optimization.

Understanding when and how to use each approach is critical for technical interviews.

---

## 1. Memoization (Top-Down DP)

### Mental Model: "Lazy Evaluation with Caching"
Memoization starts with the original, large problem and recursively breaks it down into smaller subproblems. Whenever a subproblem is solved, its result is stored in a cache (usually a hash map or an array). Before computing any subproblem, we check the cache; if the result is already there, we return it immediately.

It is called **"top-down"** because we start from the "top" (the target state we want to solve) and move down towards the base cases recursively. It uses **"lazy evaluation"** because it only computes the specific subproblems that are strictly necessary to solve the target problem.

### How It Works
1. Write a standard recursive solution.
2. Add a cache data structure (array or hash map) to store results.
3. Before doing any computation in the recursive function, check if the state's result is in the cache.
4. After computing a result, save it in the cache before returning.

### When to Use Memoization
- **Sparse State Space:** When you don't need to evaluate all possible subproblems to find the answer. Memoization only computes exactly what is needed.
- **Complex Transitions/Dependencies:** When the sequence of subproblems is hard to define iteratively (e.g., recursive operations on trees, graphs, or complicated game states).
- **Prototyping & Interviews:** It is usually much faster to write and debug because it closely follows the natural recursive mathematical definition of the problem.

### Drawbacks
- **Recursion Overhead:** Function calls add overhead to the call stack, making it slightly slower than iteration by a constant factor.
- **Stack Overflow:** Deep recursion can exceed the maximum recursion depth limits in languages like Python (which defaults to exactly 1000 frames).
- **Harder to Space-Optimize:** Because the recursion stack and cache persist throughout the execution, it's very difficult to reduce the memory complexity below $O(N)$.

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

## 2. Tabulation (Bottom-Up DP)

### Mental Model: "Eager Evaluation"
Tabulation starts at the base cases and systematically builds up to the target problem. It uses an iterative approach (loops) to fill a table (array or matrix) with solutions to subproblems, ensuring that by the time you need to compute a state, all its dependencies have already been computed.

It is called **"bottom-up"** because we start at the "bottom" (base cases) and work our way up to the target state. It uses **"eager evaluation"** because it computes the answer for *every single subproblem* along the way, whether it ends up being part of the final optimal path or not.

### How It Works
1. Initialize a table (array/matrix) to hold the results of all subproblems.
2. Initialize the base cases directly in the table.
3. Use loops to iterate through the remaining states in the correct topological order.
4. Compute the current state using the previously computed values in the table.
5. Return the final answer, usually located at the end of the table.

### When to Use Tabulation
- **Dense State Space:** When you know you will have to compute almost all subproblems anyway (which is true for most array/string DP problems).
- **Strict Performance Limits:** Iteration is generally faster than recursion because there is no function call overhead.
- **Avoiding Stack Overflow:** Iteration does not use the call stack, allowing it to handle massive inputs safely.
- **Space Optimization:** Tabulation often allows for dramatic space optimization (e.g., reducing $O(N)$ space to $O(1)$) by discarding old states that are no longer needed.

### Drawbacks
- **Computes Unnecessary States:** Tabulation evaluates *every* state up to the target. If the problem space is sparse, this wastes time.
- **Harder to Formulate:** Determining the correct loop order to fill the table (especially for multi-dimensional DP) can be tricky. You must ensure dependencies are solved before they are needed.

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

## 3. The Power of Tabulation: Space Optimization

One of the biggest advantages of tabulation is the ability to optimize space.

**The Core Concept:** If calculating the current state `dp[i]` only requires looking back a fixed number of steps (e.g., `dp[i-1]` and `dp[i-2]`), we don't need to store the entire `dp` array. We only need to keep track of a "sliding window" of the most recent steps.

### Fibonacci: $O(N)$ Space $\rightarrow$ $O(1)$ Space

In Fibonacci, `dp[i]` only depends on `dp[i-1]` and `dp[i-2]`. Once `dp[i]` is computed, `dp[i-2]` is never needed again. We can replace the $O(N)$ array with just two variables that update as we iterate.

```python
def fib_optimized(n: int) -> int:
    """
    Space-Optimized Bottom-Up DP.
    Time: O(n) | Space: O(1)
    """
    if n <= 1:
        return n

    # We only need to track the last two states
    prev2 = 0  # represents dp[i-2] initially dp[0]
    prev1 = 1  # represents dp[i-1] initially dp[1]

    for i in range(2, n + 1):
        # Calculate current state
        curr = prev1 + prev2

        # Shift our window forward for the next iteration
        prev2 = prev1
        prev1 = curr

    return prev1
```

### 2D DP: $O(M \times N)$ Space $\rightarrow$ $O(N)$ Space

A similar logic applies to 2D DP problems (like grids or string comparisons). If computing a cell `dp[r][c]` only requires values from the *current row* `dp[r]` and the *previous row* `dp[r-1]`, we don't need an $M \times N$ matrix. We only need two rows of size $N$ (or sometimes just a single 1D array of size $N$ updated in-place). We will explore this further in the 2D DP sections.

---

## 4. Side-by-Side Comparison: Unique Paths

To see how the approaches differ on a real 2D problem, let's look at counting paths from the top-left to the bottom-right in an $M \times N$ grid, moving only right or down.

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

---

## 5. Summary Cheat Sheet

| Feature | Memoization (Top-Down) | Tabulation (Bottom-Up) |
| :--- | :--- | :--- |
| **Strategy** | Start at target, break into subproblems. | Start at bases, build up to target. |
| **Implementation** | Recursion + Caching (Array/Hash map) | Iteration (Loops) + Array/Matrix |
| **Evaluation** | **Lazy**: Computes only needed states. | **Eager**: Computes all states. |
| **Speed** | Fast, but has recursion overhead. | Faster (no call stack overhead, better cache locality). |
| **Space** | $O(N)$ (Cache + Call Stack). | $O(N)$, but easily optimized to $O(1)$ or $O(M)$. |
| **Stack Overflow?** | Yes, risk for large inputs. | No. |
| **Ease of Writing** | Very intuitive, mimics math formula. | Harder to define state dependencies and loop bounds. |

---

## Interview Strategy Guide

1. **Start Top-Down:** In an interview, it is almost always best to start by discovering the recursive relation and writing the Memoized solution. It is faster to write, easier to reason about, and easier to verify correctness.
2. **Discuss Trade-offs:** Always mention to the interviewer: *"This top-down approach is $O(N)$ space due to the call stack. For massive inputs, we could hit recursion limits. We could convert this to bottom-up tabulation."*
3. **Convert to Bottom-Up (If Asked):** If the interviewer asks to optimize for stack space, rewrite it iteratively.
4. **Always Look for Space Optimization:** If you write a tabulated solution, always look for space optimization. If your loop only looks back $k$ steps, reduce your $O(N)$ array to $k$ variables! Tell the interviewer: *"I notice we only need the last two states, so we don't need to store the whole array."*

---

## Common Pitfalls & Mistakes

- **Python Default Arguments for Memo:** Never use `def dp(n, memo={}):`. Default mutable arguments in Python persist across completely separate function calls! Always initialize `memo = {}` *inside* the outer wrapper function.
- **Index Out of Bounds in Tabulation:** When writing tabulation loops, pay close attention to `range(n)` vs `range(n + 1)`. Often, DP arrays are sized `n + 1` to account for a base case at index 0.
- **Cache Initialization:** When using arrays for memoization, make sure to initialize them with a value that cannot be a valid answer (like `-1` or `float('inf')`), not `0` (if `0` can be a valid answer).

---

## Next Steps

Now that you understand the two core implementations of DP, we will apply them to real patterns.

**Next:** [03-1d-dp-basics](./03-1d-dp-basics.md)

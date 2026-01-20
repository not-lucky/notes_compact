# DP Fundamentals

## Overview

Dynamic Programming (DP) is an algorithmic technique that solves complex problems by breaking them into simpler overlapping subproblems and storing their solutions to avoid redundant computation.

## Building Intuition

**Why does DP work?**

Think of DP as "smart recursion with memory." The key insight is that many problems have a recursive structure where the same smaller problems appear repeatedly:

1. **The Redundancy Problem**: In naive recursion, we solve the same subproblems exponentially many times. For Fibonacci(50), naive recursion would compute Fibonacci(25) over 75,000 times!

2. **The Memory Solution**: If we store (memoize) each subproblem's answer the first time we compute it, subsequent lookups are O(1). This transforms exponential algorithms into polynomial ones.

3. **The Key Mental Model**: Imagine you're climbing a staircase with numbered steps. To reach step N, you must first reach step N-1 or N-2. The number of ways to reach N depends only on the number of ways to reach those earlier steps—not on HOW you reached them. This "state compression" is the essence of DP.

4. **When DP "Clicks"**: DP works when the problem has "optimal substructure" (the best solution contains best solutions to subproblems) and "overlapping subproblems" (same subproblems recur). If subproblems don't overlap, you have Divide & Conquer instead.

## Interview Context

Dynamic Programming is tested heavily because:

1. **Problem decomposition**: Shows ability to break complex problems into subproblems
2. **Optimization skill**: Finding optimal solutions efficiently
3. **Pattern recognition**: Same patterns appear across different problems
4. **Time-space tradeoffs**: Understanding memoization vs space optimization

---

## When NOT to Use DP

DP is powerful but not always appropriate. Avoid DP when:

1. **No Overlapping Subproblems**: If each subproblem is unique (like in merge sort or binary search), use Divide & Conquer instead. DP's memoization provides no benefit.

2. **Greedy Works**: If locally optimal choices lead to globally optimal solutions (like in activity selection or Huffman coding), greedy is simpler and often faster. DP is overkill.

3. **State Space Explodes**: If the number of unique states is exponential (e.g., tracking subsets or permutations), even memoized DP may be too slow. Consider approximation algorithms or heuristics.

4. **No Optimal Substructure**: If the optimal solution doesn't contain optimal solutions to subproblems, DP won't work. Example: Longest simple path in a graph (taking the longest path to an intermediate node may block the remaining path).

5. **Problem Asks for "Any" Solution**: If you just need any valid solution (not optimal), BFS/DFS often suffices without DP overhead.

**Red Flags That DP Won't Help:**
- The problem involves graphs with cycles (except shortest path problems)
- You need to track the actual path/sequence, not just the count/optimal value (reconstruction requires extra space)
- The constraints are tiny (n ≤ 10)—brute force may be cleaner

---

## The Two Essential Properties

### 1. Optimal Substructure

The optimal solution to the problem contains optimal solutions to subproblems.

```
Example: Shortest path A → C via B
If A → B → C is shortest, then:
- A → B must be the shortest path from A to B
- B → C must be the shortest path from B to C
```

### 2. Overlapping Subproblems

The same subproblems are solved multiple times.

```
Fibonacci: fib(5)
           /      \
        fib(4)   fib(3)
        /   \     /   \
     fib(3) fib(2) fib(2) fib(1)
     ...

fib(2) and fib(3) computed multiple times!
```

---

## Recognizing DP Problems

Ask yourself these questions:

1. **Can I break this into smaller subproblems?**
2. **Do subproblems overlap (same calculation repeated)?**
3. **Is there an optimal choice at each step?**
4. **Does the problem ask for min/max/count/feasibility?**

Common DP keywords:
- "Minimum/maximum number of..."
- "Count all ways to..."
- "Is it possible to..."
- "Longest/shortest..."

---

## Fibonacci: The Classic Example

### Naive Recursion - O(2ⁿ)

```python
def fib_naive(n: int) -> int:
    """
    Exponential time - overlapping subproblems not reused.
    """
    if n <= 1:
        return n
    return fib_naive(n - 1) + fib_naive(n - 2)
```

### Memoization (Top-Down) - O(n)

```python
def fib_memo(n: int, memo: dict = None) -> int:
    """
    Store computed results to avoid recomputation.

    Time: O(n)
    Space: O(n)
    """
    if memo is None:
        memo = {}

    if n <= 1:
        return n

    if n not in memo:
        memo[n] = fib_memo(n - 1, memo) + fib_memo(n - 2, memo)

    return memo[n]
```

### Tabulation (Bottom-Up) - O(n)

```python
def fib_tab(n: int) -> int:
    """
    Build solution iteratively from base cases.

    Time: O(n)
    Space: O(n)
    """
    if n <= 1:
        return n

    dp = [0] * (n + 1)
    dp[1] = 1

    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]

    return dp[n]
```

### Space Optimized - O(1)

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

    for _ in range(2, n + 1):
        curr = prev1 + prev2
        prev2 = prev1
        prev1 = curr

    return prev1
```

---

## The DP Problem-Solving Template

### Step 1: Define the State

What does `dp[i]` or `dp[i][j]` represent?

```python
# 1D: dp[i] = answer for first i elements
# 2D: dp[i][j] = answer for subproblem (i, j)
```

### Step 2: Define the Recurrence

How does current state depend on previous states?

```python
# Example: Fibonacci
# dp[i] = dp[i-1] + dp[i-2]
```

### Step 3: Define Base Cases

What are the initial values?

```python
# dp[0] = 0, dp[1] = 1
```

### Step 4: Define the Answer

Where do we find the final answer?

```python
# return dp[n]
```

### Step 5: Consider Optimization

Can we reduce space complexity?

---

## DP vs Greedy vs Divide & Conquer

| Approach | Subproblems | Choice | Example |
|----------|-------------|--------|---------|
| DP | Overlapping | Consider all | Fibonacci |
| Greedy | N/A | Local optimal | Activity Selection |
| D&C | Non-overlapping | Combine | Merge Sort |

---

## Common DP State Definitions

### 1D States

```python
dp[i] = # solution for elements 0..i
dp[i] = # solution ending at index i
dp[i] = # solution using first i items
```

### 2D States

```python
dp[i][j] = # solution for elements i..j
dp[i][j] = # solution for strings s1[0..i] and s2[0..j]
dp[i][j] = # solution with i items and capacity j
```

### State Machine

```python
dp[i][state] = # solution at index i in given state
# Example: Stock problems with hold/not-hold states
```

---

## Example: Climbing Stairs

```python
def climb_stairs(n: int) -> int:
    """
    Count ways to climb n stairs (1 or 2 steps at a time).

    State: dp[i] = ways to reach step i
    Recurrence: dp[i] = dp[i-1] + dp[i-2]
    Base: dp[0] = 1, dp[1] = 1
    Answer: dp[n]

    Time: O(n)
    Space: O(1) after optimization
    """
    if n <= 2:
        return n

    prev2, prev1 = 1, 2

    for _ in range(3, n + 1):
        curr = prev1 + prev2
        prev2 = prev1
        prev1 = curr

    return prev1
```

---

## Debugging DP Solutions

Common issues:

1. **Wrong base case**: Double-check edge cases
2. **Off-by-one errors**: Verify loop bounds
3. **Wrong recurrence**: Trace through small example
4. **Missing states**: Ensure all cases covered
5. **Integer overflow**: Use modulo if needed

Debugging technique:
```python
# Print DP table for small inputs
for i in range(n + 1):
    print(f"dp[{i}] = {dp[i]}")
```

---

## Interview Tips

1. **Start with brute force**: Show you understand the problem
2. **Identify overlapping subproblems**: Draw recursion tree
3. **Define state clearly**: Write it in comments
4. **Build incrementally**: Start with memoization, then optimize
5. **Trace small example**: Verify your solution works

---

## Complexity Cheat Sheet

| Problem Type | Time | Space | Space-Optimized |
|--------------|------|-------|-----------------|
| 1D DP | O(n) | O(n) | O(1) |
| 2D DP | O(n²) or O(nm) | O(n²) or O(nm) | O(n) or O(m) |
| Interval DP | O(n³) | O(n²) | N/A |
| DP + Binary Search | O(n log n) | O(n) | O(n) |

---

## Key Takeaways

1. **Two properties**: Optimal substructure + overlapping subproblems
2. **Define state first**: Everything else follows
3. **Start simple**: Recursion → memoization → tabulation → optimization
4. **Practice patterns**: Most problems are pattern variations
5. **Trace through**: Always verify with small examples

---

## Next: [02-memoization-vs-tabulation.md](./02-memoization-vs-tabulation.md)

Compare top-down and bottom-up approaches in detail.

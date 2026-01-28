# Matrix Chain Multiplication

> **Prerequisites:** [07-2d-dp-basics](./07-2d-dp-basics.md)

## Overview

Matrix Chain Multiplication is the canonical interval DP problem where you find the optimal way to parenthesize a sequence of operations.

## Building Intuition

**Why is interval DP needed for matrix chain?**

1. **Order Matters, But Not Linearly**: Matrix multiplication is associative (result is same), but the COST depends on parenthesization. We're not choosing a sequence—we're choosing a STRUCTURE (binary tree of operations).

2. **Interval = Subchain**: dp[i][j] represents the best way to multiply matrices i through j. Every subchain can be split at some point k, giving (i..k) and (k+1..j).

3. **The Split Point Insight**: To multiply matrices i to j, we must eventually do ONE final multiplication that combines two groups. That multiplication has dimensions p[i-1] × p[k] × p[j]. We try all possible k and take the minimum.

4. **Why Iterate by Length**: dp[i][j] depends on dp[i][k] and dp[k+1][j], which are shorter chains. So we must solve shorter chains first. Iterating by length (1, 2, 3, ...) ensures this.

5. **O(n³) Breakdown**: n² subproblems (all i,j pairs), each taking O(n) to solve (trying all split points k). Total: O(n³).

6. **Mental Model**: Think of grouping expressions like ((A×B)×C) vs (A×(B×C)). The binary tree of multiplications can have many shapes. We're finding the tree with minimum total cost.

## Interview Context

Matrix Chain Multiplication introduces **interval DP**:

1. **Parenthesization problems**: Optimal way to combine
2. **O(n³) pattern**: Iterate by length, split points
3. **Foundation for harder**: Burst balloons, merge stones
4. **Classic optimization**: Minimize/maximize over splits

---

## When NOT to Use Interval DP

1. **Linear Dependencies**: If dp[i] only depends on dp[i-1] and dp[i-2], use 1D DP. Interval DP is for range-based dependencies.

2. **O(n³) Is Too Slow**: For n > 500, O(n³) may time out. Some problems have Knuth's optimization reducing to O(n²).

3. **Non-Associative Operations**: Interval DP assumes combining (i..k) and (k+1..j) gives (i..j). If merging isn't associative or has side effects, the model breaks.

4. **Greedy Works**: Some parenthesization problems have greedy solutions (e.g., Huffman coding for optimal merge). Check before using DP.

5. **Graph Structure, Not Interval**: If the problem involves graphs rather than linear sequences, interval DP doesn't apply.

**Recognize Interval DP When:**

- Combine contiguous ranges optimally
- Split a range into two subranges
- Order of operations affects cost but not result

---

## Problem Statement

Given dimensions of n matrices, find minimum multiplications to compute their product.

Matrix i has dimensions p[i-1] × p[i].

```
Example:
p = [10, 30, 5, 60]
Matrices: A(10×30), B(30×5), C(5×60)

(A×B)×C = 10×30×5 + 10×5×60 = 1500 + 3000 = 4500
A×(B×C) = 30×5×60 + 10×30×60 = 9000 + 18000 = 27000

Optimal: (A×B)×C = 4500
```

---

## Solution

```python
def matrix_chain_order(p: list[int]) -> int:
    """
    Minimum scalar multiplications to multiply chain of matrices.

    State: dp[i][j] = min cost to multiply matrices i through j
    Recurrence: dp[i][j] = min(dp[i][k] + dp[k+1][j] + p[i-1]*p[k]*p[j])
                for all k in [i, j-1]

    Time: O(n³)
    Space: O(n²)
    """
    n = len(p) - 1  # Number of matrices

    if n <= 1:
        return 0

    # dp[i][j] = min cost for matrices i to j (1-indexed)
    dp = [[0] * (n + 1) for _ in range(n + 1)]

    # Fill by increasing chain length
    for length in range(2, n + 1):  # length of chain
        for i in range(1, n - length + 2):
            j = i + length - 1
            dp[i][j] = float('inf')

            for k in range(i, j):
                cost = dp[i][k] + dp[k + 1][j] + p[i - 1] * p[k] * p[j]
                dp[i][j] = min(dp[i][j], cost)

    return dp[1][n]
```

---

## With Parenthesization

```python
def matrix_chain_with_solution(p: list[int]) -> tuple[int, str]:
    """
    Return min cost and optimal parenthesization.
    """
    n = len(p) - 1

    if n <= 1:
        return 0, "A1" if n == 1 else ""

    dp = [[0] * (n + 1) for _ in range(n + 1)]
    split = [[0] * (n + 1) for _ in range(n + 1)]

    for length in range(2, n + 1):
        for i in range(1, n - length + 2):
            j = i + length - 1
            dp[i][j] = float('inf')

            for k in range(i, j):
                cost = dp[i][k] + dp[k + 1][j] + p[i - 1] * p[k] * p[j]
                if cost < dp[i][j]:
                    dp[i][j] = cost
                    split[i][j] = k

    def build_parens(i: int, j: int) -> str:
        if i == j:
            return f"A{i}"
        k = split[i][j]
        left = build_parens(i, k)
        right = build_parens(k + 1, j)
        return f"({left} × {right})"

    return dp[1][n], build_parens(1, n)
```

---

## Visual Walkthrough

```
p = [10, 30, 5, 60]
Matrices: A1(10×30), A2(30×5), A3(5×60)

Step 1: Length 2 chains
dp[1][2] = p[0]*p[1]*p[2] = 10*30*5 = 1500   (A1×A2)
dp[2][3] = p[1]*p[2]*p[3] = 30*5*60 = 9000   (A2×A3)

Step 2: Length 3 chain
dp[1][3] = min of:
  k=1: dp[1][1] + dp[2][3] + p[0]*p[1]*p[3] = 0 + 9000 + 10*30*60 = 27000
  k=2: dp[1][2] + dp[3][3] + p[0]*p[2]*p[3] = 1500 + 0 + 10*5*60 = 4500 ✓

Answer: 4500, ((A1 × A2) × A3)
```

---

## Memoization Version

```python
from functools import lru_cache

def matrix_chain_memo(p: list[int]) -> int:
    """
    Top-down memoized version.
    """
    n = len(p) - 1

    @lru_cache(maxsize=None)
    def dp(i: int, j: int) -> int:
        if i == j:
            return 0

        min_cost = float('inf')
        for k in range(i, j):
            cost = dp(i, k) + dp(k + 1, j) + p[i - 1] * p[k] * p[j]
            min_cost = min(min_cost, cost)

        return min_cost

    return dp(1, n)
```

---

## Related: Minimum Cost to Merge Stones

```python
def merge_stones(stones: list[int], k: int) -> int:
    """
    Merge k consecutive piles into one, minimize total cost.

    Time: O(n³)
    Space: O(n²)
    """
    n = len(stones)

    if (n - 1) % (k - 1) != 0:
        return -1  # Impossible

    # Prefix sums for range sum
    prefix = [0] * (n + 1)
    for i in range(n):
        prefix[i + 1] = prefix[i] + stones[i]

    def range_sum(i: int, j: int) -> int:
        return prefix[j + 1] - prefix[i]

    # dp[i][j] = min cost to merge stones[i..j] as much as possible
    dp = [[0] * n for _ in range(n)]

    for length in range(k, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            dp[i][j] = float('inf')

            for mid in range(i, j, k - 1):
                dp[i][j] = min(dp[i][j], dp[i][mid] + dp[mid + 1][j])

            # If can merge to single pile
            if (j - i) % (k - 1) == 0:
                dp[i][j] += range_sum(i, j)

    return dp[0][n - 1]
```

---

## Related: Optimal BST

```python
def optimal_bst(keys: list[int], freq: list[int]) -> int:
    """
    Construct BST with minimum search cost.

    Time: O(n³)
    Space: O(n²)
    """
    n = len(keys)

    # dp[i][j] = min cost for keys[i..j]
    dp = [[0] * n for _ in range(n)]

    # Frequency sum for range
    prefix = [0] * (n + 1)
    for i in range(n):
        prefix[i + 1] = prefix[i] + freq[i]

    def freq_sum(i: int, j: int) -> int:
        return prefix[j + 1] - prefix[i]

    # Single keys
    for i in range(n):
        dp[i][i] = freq[i]

    # Fill by length
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            dp[i][j] = float('inf')

            # Try each root
            for r in range(i, j + 1):
                left = dp[i][r - 1] if r > i else 0
                right = dp[r + 1][j] if r < j else 0
                cost = left + right + freq_sum(i, j)
                dp[i][j] = min(dp[i][j], cost)

    return dp[0][n - 1]
```

---

## Interval DP Template

```python
def interval_dp_template(arr: list) -> int:
    """
    General interval DP template.
    """
    n = len(arr)
    dp = [[0] * n for _ in range(n)]

    # Base case: single elements
    for i in range(n):
        dp[i][i] = base_case(arr[i])

    # Fill by increasing length
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1

            dp[i][j] = initial_value  # inf or -inf

            # Try all split points
            for k in range(i, j):  # or range(i, j + 1)
                dp[i][j] = optimize(
                    dp[i][j],
                    dp[i][k] + dp[k + 1][j] + merge_cost(i, k, j)
                )

    return dp[0][n - 1]
```

---

## Edge Cases

```python
# 1. Single matrix
p = [10, 20]  # One matrix, no multiplication
# Return 0

# 2. Two matrices
p = [10, 20, 30]  # A1(10×20) × A2(20×30)
# Return 10 * 20 * 30 = 6000

# 3. Identity dimension
p = [1, 1, 1, 1]  # All 1×1 matrices
# Return 1 + 1 = 2
```

---

## Common Mistakes

```python
# WRONG: Wrong loop order
for i in range(n):
    for j in range(i, n):  # dp[i+1][j] not computed yet!
        ...

# CORRECT: Loop by length
for length in range(2, n + 1):
    for i in range(n - length + 1):
        j = i + length - 1
        ...


# WRONG: Wrong dimension indexing
cost = p[i] * p[k] * p[j]  # Off by one!

# CORRECT:
cost = p[i-1] * p[k] * p[j]  # p is 0-indexed dimensions


# WRONG: Not initializing with inf
dp[i][j] = dp[i][k] + dp[k+1][j] + cost  # First iteration uses 0!

# CORRECT:
dp[i][j] = float('inf')
for k in range(...):
    dp[i][j] = min(dp[i][j], ...)
```

---

## Complexity

| Problem             | Time  | Space |
| ------------------- | ----- | ----- |
| Matrix Chain        | O(n³) | O(n²) |
| Merge Stones        | O(n³) | O(n²) |
| Optimal BST         | O(n³) | O(n²) |
| General Interval DP | O(n³) | O(n²) |

Note: Some can be optimized to O(n²) with Knuth's optimization.

---

## Interview Tips

1. **Recognize interval pattern**: "Combine ranges optimally"
2. **Loop by length**: Not by endpoints
3. **Split point k**: What it represents
4. **Merge cost**: How to compute efficiently
5. **Reconstruct solution**: Keep track of split points

---

## Practice Problems

| #   | Problem                     | Difficulty | Variation         |
| --- | --------------------------- | ---------- | ----------------- |
| 1   | Matrix Chain Multiplication | Medium     | Classic           |
| 2   | Burst Balloons              | Hard       | Reverse thinking  |
| 3   | Merge Stones                | Hard       | K-way merge       |
| 4   | Optimal BST                 | Hard       | Tree construction |
| 5   | Minimum Score Triangulation | Medium     | Polygon           |

---

## Key Takeaways

1. **Interval DP**: dp[i][j] for ranges
2. **Loop by length**: Ensures dependencies solved
3. **Try all splits**: O(n) per subproblem
4. **O(n³) typical**: But O(n²) possible with optimizations
5. **Foundation for harder**: Burst balloons, etc.

---

## Next: [17-burst-balloons.md](./17-burst-balloons.md)

Apply interval DP to the Burst Balloons problem.

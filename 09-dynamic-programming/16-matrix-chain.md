# Matrix Chain Multiplication & Interval DP

> **Prerequisites:** [07-2d-dp-basics](./07-2d-dp-basics.md)

## Overview

Matrix Chain Multiplication is the canonical **interval DP** problem. The goal is to find the optimal way to parenthesize a sequence of operations to minimize the total cost. Interval DP is used when a problem asks you to combine adjacent elements or split an array into pieces optimally.

## Building Intuition

**Why is interval DP needed for matrix chain?**

1. **Order Matters, But Not Linearly**: Matrix multiplication is associative (the final matrix is the same regardless of parenthesization), but the computational COST depends heavily on the parenthesization. We are not choosing a sequence—we are choosing a STRUCTURE (a binary tree of operations).
2. **Interval = Subchain**: `dp[i][j]` represents the optimal cost to multiply the sequence of matrices from index `i` through index `j` inclusive. Every subchain can be split at some point `k`, creating two smaller subchains: `(i..k)` and `(k+1..j)`.
3. **The Split Point Insight**: To combine the matrices `i` to `j`, we must eventually perform ONE final multiplication that combines the optimal result of the left group with the right group. That multiplication has dimensions $p_i \times p_{k+1} \times p_{j+1}$. We try all possible split points `k` and take the minimum.
4. **Why Iterate by Length**: `dp[i][j]` depends on `dp[i][k]` and `dp[k+1][j]`, which represent *shorter* chains. To ensure we have the answers for smaller subproblems before we need them, we must iterate over the **length of the interval**, building up from length 1, to 2, to 3, etc.
5. **O(n³) Breakdown**: There are $O(n^2)$ subproblems (all `i, j` pairs), and each takes $O(n)$ time to solve because we try all split points `k` between `i` and `j`. Total time: $O(n^3)$.

---

## Recognizing Interval DP

Interval DP is appropriate when:
- You need to combine contiguous ranges optimally (e.g., merging adjacent files/stones).
- You need to split a contiguous range into two subranges optimally.
- The operations form a tree structure over adjacent elements.

**When NOT to Use Interval DP:**

1. **Linear Dependencies**: If `dp[i]` only depends on `dp[i-1]` or `dp[i-2]`, use 1D DP. Interval DP is for range-based dependencies.
2. **O(n³) Is Too Slow**: For $n > 500$, an $O(n^3)$ solution will usually time out. Some problems have Knuth's optimization, which reduces the time complexity to $O(n^2)$.
3. **Greedy Works**: Some parenthesization or merging problems have greedy solutions (e.g., Huffman coding for optimal merge cost of items where any two can be merged, not just adjacent ones). If you can merge *any* two items, sort or use a Priority Queue in $O(n \log n)$. Interval DP strictly requires combining *adjacent* elements.
4. **Graph Structure**: If the problem involves graphs rather than a linear sequence of elements that can be partitioned, interval DP doesn't apply (e.g., Traveling Salesperson).

---

## Problem Statement

Given an array `p` of dimensions for $n$ matrices, find the minimum number of scalar multiplications needed to compute the matrix product.

- Matrix `i` (0-indexed) has dimensions `p[i] × p[i+1]`.
- Note: The array `p` has length $n + 1$.

```text
Example:
p = [10, 30, 5, 60]
Matrices: A(10×30), B(30×5), C(5×60)

(A×B)×C = (10×30×5) + (10×5×60) = 1500 + 3000 = 4500
A×(B×C) = (30×5×60) + (10×30×60) = 9000 + 18000 = 27000

Optimal cost is 4500.
```

---

## Solution

### Recurrence Relation

Let $dp[i][j]$ be the minimum number of multiplications to compute the product of matrices $A_i \dots A_j$ (0-indexed). The dimensions of matrix $A_m$ are $p_m \times p_{m+1}$.

$$
dp[i][j] =
\begin{cases}
0 & \text{if } i = j \\
\min\limits_{i \le k < j} \left\{ dp[i][k] + dp[k+1][j] + p_i \cdot p_{k+1} \cdot p_{j+1} \right\} & \text{if } i < j
\end{cases}
$$

### Bottom-Up DP (Tabulation)

It is highly recommended to use **0-indexed matrices** in Python. If `p` has length $N$, there are $n = N - 1$ matrices. We use a 2D array of size $n \times n$.

```python
def matrix_chain_order(p: list[int]) -> int:
    """
    Minimum scalar multiplications to multiply a chain of matrices.

    Time: O(n³)
    Space: O(n²)
    """
    n = len(p) - 1  # Number of matrices
    if n <= 1:
        return 0

    # dp[i][j] = min cost to multiply matrices i through j (inclusive)
    dp = [[0] * n for _ in range(n)]

    # Loop by length of the chain (from 2 up to n)
    for length in range(2, n + 1):
        # i is the start index
        for i in range(n - length + 1):
            j = i + length - 1  # j is the end index
            dp[i][j] = float('inf')

            # k is the split point: we split into (i..k) and (k+1..j)
            for k in range(i, j):
                # Cost = cost of left + cost of right + cost of multiplying left and right
                # Left matrix result is p[i] x p[k+1]
                # Right matrix result is p[k+1] x p[j+1]
                cost = dp[i][k] + dp[k+1][j] + p[i] * p[k+1] * p[j+1]
                dp[i][j] = min(dp[i][j], cost)

    return dp[0][n - 1]
```

### With Parenthesization Reconstruction

If you need to reconstruct the optimal parenthesization, keep a separate `split` table to record the `k` that yielded the minimum cost for `dp[i][j]`.

```python
def matrix_chain_with_solution(p: list[int]) -> tuple[int, str]:
    n = len(p) - 1
    if n <= 1:
        return 0, "A0" if n == 1 else ""

    dp = [[0] * n for _ in range(n)]
    split = [[0] * n for _ in range(n)]

    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            dp[i][j] = float('inf')

            for k in range(i, j):
                cost = dp[i][k] + dp[k+1][j] + p[i] * p[k+1] * p[j+1]
                if cost < dp[i][j]:
                    dp[i][j] = cost
                    split[i][j] = k  # Store the optimal split point

    # Recursive function to build the string
    def build_parens(i: int, j: int) -> str:
        if i == j:
            return f"A{i}"
        k = split[i][j]
        left = build_parens(i, k)
        right = build_parens(k + 1, j)
        return f"({left} × {right})"

    return dp[0][n - 1], build_parens(0, n - 1)
```

---

## Top-Down DP (Memoization)

Many people find the top-down memoization approach more intuitive for interval DP because you don't have to worry about the complex loop ordering (iterating by length). The recursion automatically solves the smaller dependencies first.

```python
from functools import lru_cache

def matrix_chain_memo(p: list[int]) -> int:
    n = len(p) - 1

    @lru_cache(maxsize=None)
    def dp(i: int, j: int) -> int:
        # Base case: A single matrix costs 0 to multiply
        if i == j:
            return 0

        min_cost = float('inf')
        # Try all possible split points k
        for k in range(i, j):
            cost = dp(i, k) + dp(k + 1, j) + p[i] * p[k+1] * p[j+1]
            min_cost = min(min_cost, cost)

        return min_cost

    return dp(0, n - 1)
```

---

## Standard Interval DP Template

Most interval DP problems follow this exact structure:

```python
def interval_dp_template(arr: list) -> int:
    n = len(arr)
    dp = [[0] * n for _ in range(n)]

    # Base cases: intervals of length 1
    for i in range(n):
        dp[i][i] = base_case(arr[i])

    # Iterate over interval lengths
    for length in range(2, n + 1):
        # Iterate over start index
        for i in range(n - length + 1):
            j = i + length - 1  # Calculate end index

            dp[i][j] = float('inf')  # Or float('-inf') if maximizing

            # Iterate over split points
            for k in range(i, j):  # Sometimes range(i, j + 1) depending on problem
                # Transition
                cost = dp[i][k] + dp[k+1][j] + merge_cost(i, k, j)
                dp[i][j] = min(dp[i][j], cost)

    return dp[0][n - 1]
```

---

## Related: Minimum Cost to Merge Stones

This is a classic variation. You must merge `k` consecutive piles into one. The cost of a merge is the sum of the piles being merged.

Note: To merge `stones[i..j]` down to 1 pile, the jump step for `mid` is `k - 1`. This guarantees that the left partition `i..mid` can always be reduced to exactly 1 pile.

```python
def merge_stones(stones: list[int], k: int) -> int:
    """
    Merge k consecutive piles into one, minimize total cost.

    Time: O(n³ / k)
    Space: O(n²)
    """
    n = len(stones)
    # Check if a valid merge to 1 pile is mathematically possible
    if (n - 1) % (k - 1) != 0:
        return -1

    # Prefix sums to quickly get the sum of stones[i..j]
    prefix = [0] * (n + 1)
    for i in range(n):
        prefix[i + 1] = prefix[i] + stones[i]

    def range_sum(i: int, j: int) -> int:
        return prefix[j + 1] - prefix[i]

    # dp[i][j] = min cost to merge stones[i..j] as much as mathematically possible
    dp = [[0] * n for _ in range(n)]

    for length in range(k, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            dp[i][j] = float('inf')

            # Crucial optimization: step by k-1
            # We want to merge i..mid into 1 pile, and mid+1..j into some piles
            for mid in range(i, j, k - 1):
                dp[i][j] = min(dp[i][j], dp[i][mid] + dp[mid + 1][j])

            # If the entire range i..j can be compressed into exactly 1 pile
            # We add the cost of combining those final k piles together
            if (j - i) % (k - 1) == 0:
                dp[i][j] += range_sum(i, j)

    return dp[0][n - 1]
```

---

## Related: Optimal Binary Search Tree

Given sorted keys and their search frequencies, build a BST that minimizes the expected search cost. This uses interval DP because a BST on sorted keys `i` to `j` can be formed by picking any key `r` as the root, making `i..r-1` the left subtree and `r+1..j` the right subtree.

```python
def optimal_bst(keys: list[int], freq: list[int]) -> int:
    """
    Construct BST with minimum expected search cost.

    Time: O(n³)
    Space: O(n²)
    """
    n = len(keys)
    dp = [[0] * n for _ in range(n)]

    # Prefix array for O(1) range frequency sums
    prefix = [0] * (n + 1)
    for i in range(n):
        prefix[i + 1] = prefix[i] + freq[i]

    def freq_sum(i: int, j: int) -> int:
        return prefix[j + 1] - prefix[i]

    # Base case: tree with a single key
    for i in range(n):
        dp[i][i] = freq[i]

    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            dp[i][j] = float('inf')

            # Try every key in range as the root
            for r in range(i, j + 1):
                # Cost is left subtree + right subtree + sum of all frequencies in tree
                # (because when this becomes a subtree, every node goes 1 level deeper)
                left_cost = dp[i][r - 1] if r > i else 0
                right_cost = dp[r + 1][j] if r < j else 0

                cost = left_cost + right_cost + freq_sum(i, j)
                dp[i][j] = min(dp[i][j], cost)

    return dp[0][n - 1]
```

---

## Common Mistakes

1. **Iterating by end indices instead of length**:
   ```python
   # WRONG: Will read dp[k+1][j] before it's computed!
   for i in range(n):
       for j in range(i + 1, n):
           for k in range(i, j): ...

   # CORRECT: Iterate by length
   for length in range(2, n + 1):
       for i in range(n - length + 1):
           j = i + length - 1
   ```
2. **Indexing errors with dimensions**:
   If using 0-indexed matrices, matrix `i` has size `p[i] x p[i+1]`. The cost to merge `i..k` and `k+1..j` is `p[i] * p[k+1] * p[j+1]`. Off-by-one errors here are very common.
3. **Not initializing DP table properly**:
   Always initialize `dp[i][j] = float('inf')` inside the length/start loops *before* the inner `k` loop. Otherwise, `min()` will just keep `0`.

---

## Complexity Profile

| Problem             | Time  | Space | Notes |
| ------------------- | ----- | ----- | ----- |
| Matrix Chain        | O(n³) | O(n²) | Can be mapped to polygon triangulation. |
| Merge Stones        | O(n³) | O(n²) | `dp[i][j][m]` optimized to 2D DP. |
| Optimal BST         | O(n³) | O(n²) | Can be optimized to O(n²) with Knuth's. |

---

## Next: [17-burst-balloons.md](./17-burst-balloons.md)

Apply interval DP to the notoriously tricky Burst Balloons problem.

# Burst Balloons

> **Prerequisites:** [16-matrix-chain](./16-matrix-chain.md)

## Problem Statement

You are given `n` balloons, indexed from `0` to `n - 1`. Each balloon is painted with a number on it represented by an array `nums`. You are asked to burst all the balloons.

If you burst the $i$-th balloon, you will get `nums[i - 1] * nums[i] * nums[i + 1]` coins. If `i - 1` or `i + 1` goes out of bounds of the array, then treat it as if there is a balloon with a `1` painted on it.

Return the maximum coins you can collect by bursting the balloons wisely.

## Overview

Burst Balloons (LeetCode 312) is a classic and notoriously difficult Interval DP problem. It requires a counterintuitive insight: **thinking about the LAST element to process rather than the first**.

When dealing with arrays where removing an element changes the adjacency (neighbors) of the remaining elements, standard DP approaches often fail due to chaotic state dependencies. The Burst Balloons pattern solves this by working backwards.

---

## Building Intuition: Why Think Backwards?

Imagine we have balloons `[A, B, C, D]`.

### The Problem with "First Burst" (Forward Thinking)
If we burst `B` first, its neighbors `A` and `C` are involved in the score. After `B` pops, `A` and `C` become adjacent.
The new array is `[A, C, D]`.

If we then burst `C`, its neighbors are now `A` and `D`. The score for bursting `C` depends on the fact that `B` was already burst. This means our subproblems are not independent—they depend on the exact sequence of previous bursts. Tracking all possible remaining configurations requires $O(2^n)$ states, which is far too slow for $n=300$.

### The "Last Burst" Insight (Backward Thinking)
Instead of asking "Which balloon should I burst first?", ask: **"Which balloon should I burst LAST?"**

Suppose we decide `C` will be the **very last** balloon we burst in the range `[A, B, C, D]`.
What do we know at the exact moment we burst `C`?
1. All other balloons in the range (`A`, `B`, and `D`) have **already been burst**.
2. Therefore, `C` is completely isolated within this range.
3. When `C` is finally burst, its neighbors will be whatever balloons are strictly **outside** our current range (in this case, the virtual `1`s at the boundaries).

This incredibly clever insight completely decouples the left side of `C` from the right side. The subproblem of bursting `[A, B]` is now completely independent of the subproblem of bursting `[D]`.

---

## The Core Pattern

### 1. Virtual Boundaries
The problem states that out-of-bounds indices are treated as if they have a balloon with value `1`. To avoid messy edge cases and `if` statements inside our tight loops, we explicitly add these virtual `1`s to our array:

`padded_nums = [1] + original_nums + [1]`

These boundaries also serve a crucial mathematical purpose: they represent the indestructible "walls" that remain when all actual balloons between them have been burst.

### 2. State Definition
We use an **exclusive** range definition. This is the secret to making the math clean.

Let `dp[left][right]` be the maximum coins obtained by bursting ALL balloons **strictly between** index `left` and index `right`.

*Crucial Note: Balloons at index `left` and index `right` are **NOT** burst in this subproblem. They act as the indestructible walls (the final neighbors) for the very last balloon to burst in the range `(left, right)`. They represent the balloons that will be adjacent to `k` precisely because everything between `left` and `k`, and everything between `k` and `right`, has already been removed.*

### 3. Transitions
To find `dp[left][right]`, we guess which balloon `k` (where `left < k < right`) is the **last** to burst.
If `k` is the last to burst in this range:
1. We must first burst all balloons between `left` and `k`: this gives us `dp[left][k]` coins.
2. We must also burst all balloons between `k` and `right`: this gives us `dp[k][right]` coins.
3. Finally, we burst `k`. Since all balloons strictly between `left` and `right` except `k` are gone, `k`'s neighbors are exactly `left` and `right`. The coins gained for bursting `k` are: `nums[left] * nums[k] * nums[right]`.

$$
dp[left][right] = \max_{left < k < right} \left( dp[left][k] + dp[k][right] + nums[left] \cdot nums[k] \cdot nums[right] \right)
$$

### 4. Base Case
If there are no balloons strictly between `left` and `right` (i.e., `left + 1 == right`), then there is nothing to burst.
`dp[left][left+1] = 0`.

---

## Implementations

### Top-Down (Memoization)
Memoization is often much easier to write for Interval DP because you don't have to manually manage the loop order. The recursion naturally processes smaller intervals first.

```python
from typing import List

def maxCoins_memo(nums: List[int]) -> int:
    """
    Time Complexity: O(n^3)
    Space Complexity: O(n^2) for the memoization dictionary
    """
    # 1. Add virtual boundaries
    nums = [1] + nums + [1]
    n = len(nums)
    memo = {}

    def dfs(left: int, right: int) -> int:
        """
        Returns max coins obtained by bursting all balloons
        strictly between index 'left' and 'right'.
        'left' and 'right' are the boundaries and are NOT burst.
        """
        # Base case: no balloons strictly between left and right
        if left + 1 == right:
            return 0

        if (left, right) in memo:
            return memo[(left, right)]

        max_coins = 0
        # Try bursting every balloon k LAST in the range (left, right)
        for k in range(left + 1, right):
            # Coins from bursting k last: nums[left] * nums[k] * nums[right]
            # Plus coins from bursting everything in the left half: (left, k)
            # Plus coins from bursting everything in the right half: (k, right)
            coins = nums[left] * nums[k] * nums[right]
            total = coins + dfs(left, k) + dfs(k, right)
            max_coins = max(max_coins, total)

        memo[(left, right)] = max_coins
        return max_coins

    # We want to burst all original balloons,
    # which are strictly between index 0 and index n-1
    return dfs(0, n - 1)
```

### Bottom-Up (Tabulation)
For Tabulation, **loop order is critical**. `dp[left][right]` depends on `dp[left][k]` and `dp[k][right]`. Notice that the intervals `(left, k)` and `(k, right)` are strictly **shorter** than `(left, right)`.

Therefore, we must solve subproblems ordered by **interval length**, or by moving `left` backwards and `right` forwards.

```python
def maxCoins_tabulation(nums: List[int]) -> int:
    """
    Time Complexity: O(n^3)
    Space Complexity: O(n^2) for the DP table
    """
    nums = [1] + nums + [1]
    n = len(nums)

    # dp[left][right] = max coins from bursting balloons strictly between left and right
    dp = [[0] * n for _ in range(n)]

    # Iterate left backwards from the second to last element
    for left in range(n - 2, -1, -1):
        # Iterate right forwards from left + 2 (ensures at least one balloon is between)
        for right in range(left + 2, n):

            # Try every possible last balloon k to burst in (left, right)
            for k in range(left + 1, right):
                # We calculate the score of bursting k last, plus the optimal
                # scores of bursting the sub-intervals (left, k) and (k, right)
                coins = nums[left] * nums[k] * nums[right]
                dp[left][right] = max(
                    dp[left][right],
                    dp[left][k] + dp[k][right] + coins
                )

    return dp[0][n - 1]
```

*Note on loop order:* Iterating `left` backwards and `right` forwards guarantees that when evaluating `dp[left][right]`, all strictly shorter intervals (like `dp[left][k]` and `dp[k][right]`) have already been computed.

---

## Visual Walkthrough

Let `nums = [3, 1, 5, 8]`.
Add boundaries: `padded_nums = [1, 3, 1, 5, 8, 1]`. Let $n=6$.
Indices: `0  1  2  3  4  5`

**Length 2 (right - left = 1):**
No balloons strictly between `left` and `right`. All `dp[left][left+1] = 0`.
*(This is implicitly handled by the matrix initialization).*

**Length 3 (right - left = 2, exactly one balloon between):**

| Interval `[left][right]` | Balloon $k$ (index) | Value $nums[k]$ | Calculation $nums[left] \times nums[k] \times nums[right]$ | Coins |
| :--- | :--- | :--- | :--- | :--- |
| `dp[0][2]` | 1 | 3 | $1 \times 3 \times 1$ | 3 |
| `dp[1][3]` | 2 | 1 | $3 \times 1 \times 5$ | 15 |
| `dp[2][4]` | 3 | 5 | $1 \times 5 \times 8$ | 40 |
| `dp[3][5]` | 4 | 8 | $5 \times 8 \times 1$ | 40 |

**Length 4 (right - left = 3, exactly two balloons between):**

Calculate `dp[0][3]` (range contains index 1 and 2, values `3` and `1`). We evaluate two choices for the **last** balloon to burst $k$:

1.  **Try bursting index 1 (value 3) last ($k=1$):**
    *   $dp[0][1] + dp[1][3] + (nums[0] \times nums[1] \times nums[3])$
    *   $0 + 15 + (1 \times 3 \times 5) = 15 + 15 = 30$

2.  **Try bursting index 2 (value 1) last ($k=2$):**
    *   $dp[0][2] + dp[2][3] + (nums[0] \times nums[2] \times nums[3])$
    *   $3 + 0 + (1 \times 1 \times 5) = 3 + 5 = 8$

Therefore, the maximum for `dp[0][3]` is **`30`**.

We continue expanding the interval until we calculate `dp[0][5]`, which covers all original balloons and gives the final answer: **`167`**.

---

## Comparison with Matrix Chain Multiplication

Burst Balloons is structurally identical to Matrix Chain Multiplication (MCM). Recognizing this helps you map the problem to a known solution framework immediately.

| Aspect | Matrix Chain Multiplication | Burst Balloons |
|--------|-----------------------------|----------------|
| **Goal** | Minimize multiplication cost | Maximize burst coins |
| **State $dp[left][right]$** | Cost to multiply matrices $left$ to $right$ | Coins from bursting balloons between $left$ and $right$ |
| **Split point $k$** | Where to make the *last* matrix multiplication | Which balloon to burst *last* |
| **Merge calculation**| $p[left-1] \cdot p[k] \cdot p[right]$ | $nums[left] \cdot nums[k] \cdot nums[right]$ |
| **Boundaries** | Array of dimension sizes | Explicit virtual `1`s at ends |

---

## Related Problem: Minimum Score Triangulation

Given a convex polygon with $n$ vertices (represented by an array `v` of values), find the minimum score to triangulate it. The score of a triangle is the product of its 3 vertices. (LeetCode 1039)

**Insight:**
Any triangulation of a polygon $[left \dots right]$ must contain exactly one triangle that uses the base edge $(left, right)$. Let the third vertex of this triangle be $k$. This triangle splits the remaining polygon into two smaller, independent polygons: $[left \dots k]$ and $[k \dots right]$.

**Recurrence:**
$$
dp[left][right] = \min_{left < k < right} \left( dp[left][k] + dp[k][right] + v[left] \cdot v[k] \cdot v[right] \right)
$$

Notice this is **exactly the same recurrence** as Burst Balloons, just minimizing instead of maximizing! Once you understand the "Interval DP with a $k$ split" pattern, these hard problems become trivial to model.

---

## Advanced Variation: Remove Boxes (3D State)

Remove Boxes (LeetCode 546) is a FANG-favorite Hard problem that *looks* like Burst Balloons but requires a **3D State**.

**Problem:** Given an array of colors, remove consecutive boxes of the same color to get points equal to `(count)^2`.
Example: `[1, 3, 2, 2, 2, 3, 4, 3, 1]`

**Why 2D DP Fails Here:**
In Burst Balloons, when a balloon bursts, the score `nums[left]*nums[k]*nums[right]` only cares about the *values* of the immediate neighbors.
In Remove Boxes, when boxes are removed, separated boxes of the same color merge together (e.g., removing the `2`s above merges the `3`s into `[3, 3, 3]`). The points are `count^2`, so grouping them *before* removing yields far more points ($3^2 = 9$ instead of $1^2 + 2^2 = 5$).
A standard 2D state `dp[left][right]` cannot remember how many boxes of the same color as `boxes[left]` are waiting just outside the left boundary from previous merges.

**The 3D State Solution:**
`dp(left, right, k)` = max points for `boxes[left...right]` given that there are exactly `k` boxes of the same color as `boxes[left]` attached immediately to the left of `left`.

```python
def removeBoxes(boxes: List[int]) -> int:
    """
    Time Complexity: O(n^4)
    Space Complexity: O(n^3)
    """
    memo = {}

    def dp(left: int, right: int, k: int) -> int:
        if left > right:
            return 0

        if (left, right, k) in memo:
            return memo[(left, right, k)]

        # Optimization: Group identical consecutive boxes at the start
        # E.g., [3, 3, 3, 4] with k=0 becomes processing [3, 4] with k=2
        l, count = left, k
        while l < right and boxes[l] == boxes[l + 1]:
            l += 1
            count += 1

        # Option 1: Remove boxes[left] along with the 'count' attached boxes right now.
        # This gives us (count + 1)^2 points, and we recursively solve the remaining boxes[l+1...right].
        # We reset k to 0 for the subproblem because there are no boxes attached to l+1.
        res = (count + 1) ** 2 + dp(l + 1, right, 0)

        # Option 2: Try to merge boxes[l] with another box of the same color later in the array.
        # We look for a box boxes[m] == boxes[l].
        # If we remove everything strictly between l and m (i.e., boxes[l+1...m-1]),
        # then boxes[l] and its 'count' attached boxes will touch boxes[m].
        for m in range(l + 1, right + 1):
            if boxes[m] == boxes[l]:
                # Cost to remove the middle + cost of the merged remainder
                # The remaining boxes starting at 'm' now have 'count + 1' boxes attached to their left
                res = max(res, dp(l + 1, m - 1, 0) + dp(m, right, count + 1))

        memo[(left, right, k)] = res
        return res

    return dp(0, len(boxes) - 1, 0)
```

---

## Common Mistakes & Pitfalls

1. **Forgetting Virtual Boundaries:**
   If you don't add `[1]` to the ends of the array, calculating `nums[left] * nums[k] * nums[right]` will throw index out of bounds errors when bursting the original edge balloons.

2. **Wrong Loop Order in Tabulation:**
   If you iterate `left` from `0` to `n` and `right` from `left` to `n`, you will calculate `dp[left][right]` before `dp[k][right]` is ready. **Interval DP tabulation must loop backwards for the left pointer and forwards for the right pointer**.

3. **Inclusive vs Exclusive Bounds Confusion:**
   Our state definition makes `left` and `right` **exclusive** bounds.
   - Size of the dp array must be `(n+2) x (n+2)` (where $n$ is original length, before padding).
   - $k$ must range strictly between: `for k in range(left + 1, right)`.

## Summary Checklist for Burst Balloons Pattern
- [ ] Does removing an element merge its left and right neighbors?
- [ ] Does the score depend on these new neighbors?
- [ ] **Action:** Think about the LAST element removed.
- [ ] **Action:** Add virtual boundaries to the input array.
- [ ] **Action:** Use $O(n^3)$ Interval DP mapping out `dp[left][right]` exclusively.

# Burst Balloons

> **Prerequisites:** [16-matrix-chain](./16-matrix-chain.md)

## Problem Statement

You are given `n` balloons, indexed from `0` to `n - 1`. Each balloon is painted with a number on it represented by an array `nums`. You are asked to burst all the balloons.

If you burst the $i$-th balloon, you will get `nums[i - 1] * nums[i] * nums[i + 1]` coins. If `i - 1` or `i + 1` goes out of bounds of the array, then treat it as if there is a balloon with a `1` painted on it.

Return the maximum coins you can collect by bursting the balloons wisely.

## Overview

Burst Balloons is a classic and notoriously difficult Interval DP problem. It requires a counterintuitive insight: **thinking about the LAST element to process rather than the first**.

When dealing with arrays where removing an element changes the adjacency (neighbors) of the remaining elements, standard DP approaches often fail due to chaotic state dependencies. The Burst Balloons pattern solves this by working backwards.

---

## Building Intuition: Why Think Backwards?

Imagine we have balloons `[A, B, C, D]`.

### The Problem with "First Burst" (Forward Thinking)
If we burst `B` first, its neighbors `A` and `C` are involved in the score. After `B` pops, `A` and `C` become adjacent.
The new array is `[A, C, D]`.

If we then burst `C`, its neighbors are now `A` and `D`. The score for bursting `C` depends on the fact that `B` was already burst. This means our subproblems are not independent—they depend on the exact sequence of previous bursts. Tracking all possible remaining configurations requires $O(2^n)$ states, which is too slow.

### The "Last Burst" Insight (Backward Thinking)
Instead of asking "Which balloon should I burst first?", ask: **"Which balloon should I burst LAST?"**

Suppose we decide `C` will be the **very last** balloon we burst in the range `[A, B, C, D]`.
What do we know at the exact moment we burst `C`?
- All other balloons in the range (`A`, `B`, and `D`) have **already been burst**.
- Therefore, `C` is completely isolated within this range.
- When `C` is finally burst, its neighbors will be whatever is strictly **outside** our current range.

This completely decouples the left side of `C` from the right side. The subproblem of bursting `[A, B]` is now completely independent of the subproblem of bursting `[D]`.

---

## The Core Pattern

### 1. Virtual Boundaries
The problem states that bursting balloon `i` gives `nums[i-1] * nums[i] * nums[i+1]` coins. Out-of-bounds indices are treated as if they have a balloon with value `1`.

To avoid messy edge cases, we explicitly add these virtual `1`s to our array:
`padded_nums = [1] + original_nums + [1]`

### 2. State Definition
We use an **exclusive** range definition.

Let `dp[left][right]` be the maximum coins obtained by bursting ALL balloons **strictly between** index `left` and index `right`.

*Note: Balloons `left` and `right` themselves are NOT burst in this subproblem. They act as the indestructible walls (neighbors) for the last balloon burst in the range.*

### 3. Transitions
To find `dp[left][right]`, we guess which balloon `k` (where `left < k < right`) is the **last** to burst.
If `k` is the last to burst:
1. We must first burst all balloons between `left` and `k`: cost is `dp[left][k]`
2. We must also burst all balloons between `k` and `right`: cost is `dp[k][right]`
3. Finally, we burst `k`. Since all balloons strictly between `left` and `right` except `k` are gone, `k`'s neighbors are exactly `left` and `right`. The coins gained are: `nums[left] * nums[k] * nums[right]`.

$$
dp[left][right] = \max_{left < k < right} \left( dp[left][k] + dp[k][right] + nums[left] \cdot nums[k] \cdot nums[right] \right)
$$

### 4. Base Case
If there are no balloons strictly between `left` and `right` (i.e., `left + 1 == right`), then `dp[left][right] = 0`.

---

## Implementations

### Top-Down (Memoization)
Memoization is often much easier to write for Interval DP because you don't have to manually manage the loop order. The recursion naturally processes smaller intervals first.

```python
from functools import lru_cache
from typing import List

def maxCoins(nums: List[int]) -> int:
    """
    Calculates the maximum coins obtained by bursting balloons.
    Uses Top-Down DP with Memoization.
    """
    # 1. Add virtual boundaries
    padded_nums = [1] + nums + [1]

    @lru_cache(None)
    def dp(left: int, right: int) -> int:
        """
        Returns max coins obtained by bursting all balloons
        strictly between index 'left' and 'right'.
        """
        # Base case: no balloons strictly between left and right
        if left + 1 == right:
            return 0

        max_coins = 0
        # Try bursting every balloon k LAST
        for k in range(left + 1, right):
            coins = padded_nums[left] * padded_nums[k] * padded_nums[right]
            total_coins = dp(left, k) + dp(k, right) + coins
            max_coins = max(max_coins, total_coins)

        return max_coins

    # We want to burst all original balloons,
    # which are strictly between index 0 and index len(padded_nums)-1
    return dp(0, len(padded_nums) - 1)
```

**Complexity Analysis:**
- **Time Complexity:** $O(n^3)$. There are $O(n^2)$ states (`left`, `right` pairs). For each state, we iterate through $O(n)$ possible choices for `k`.
- **Space Complexity:** $O(n^2)$ to store the memoization cache.

### Bottom-Up (Tabulation)
For Tabulation, **loop order is critical**. `dp[left][right]` depends on `dp[left][k]` and `dp[k][right]`. Notice that the intervals `(left, k)` and `(k, right)` are strictly **shorter** than `(left, right)`.

Therefore, we must solve subproblems ordered by **interval length**.

```python
from typing import List

def maxCoins(nums: List[int]) -> int:
    """
    Calculates the maximum coins obtained by bursting balloons.
    Uses Bottom-Up DP with Tabulation.
    """
    padded_nums = [1] + nums + [1]
    n = len(padded_nums)

    # dp[left][right] = max coins from bursting balloons strictly between left and right
    dp = [[0] * n for _ in range(n)]

    # Iterate by length of the interval (from 2 up to n-1)
    # length represents (right - left).
    # Min length is 2 (e.g., left=0, right=2, so strictly between is index 1)
    for length in range(2, n):
        for left in range(n - length):
            right = left + length

            # Try every possible last balloon k to burst in (left, right)
            for k in range(left + 1, right):
                coins = padded_nums[left] * padded_nums[k] * padded_nums[right]
                dp[left][right] = max(dp[left][right], dp[left][k] + dp[k][right] + coins)

    return dp[0][n - 1]
```

**Complexity Analysis:**
- **Time Complexity:** $O(n^3)$. There are $O(n^2)$ states. For each state, we iterate through $O(n)$ possible choices for `k`.
- **Space Complexity:** $O(n^2)$ to store the 2D DP table. Space cannot be optimized to 1D because `dp[left][right]` depends on subproblems that span multiple lengths and starting positions.

---

## Visual Walkthrough

Let `nums = [3, 1, 5, 8]`.
Add boundaries: `padded_nums = [1, 3, 1, 5, 8, 1]`. Let $n=6$.
Indices: `0  1  2  3  4  5`

**Length 2 (Base cases, right - left = 1):**
No balloons strictly between `left` and `right`. All `dp[left][left+1] = 0`.

**Length 3 (right - left = 2, one balloon between):**
- `dp[0][2]`: Burst balloon 1 (value 3) last. Coins = $1 \cdot 3 \cdot 1 = 3$.
- `dp[1][3]`: Burst balloon 2 (value 1) last. Coins = $3 \cdot 1 \cdot 5 = 15$.
- `dp[2][4]`: Burst balloon 3 (value 5) last. Coins = $1 \cdot 5 \cdot 8 = 40$.
- `dp[3][5]`: Burst balloon 4 (value 8) last. Coins = $5 \cdot 8 \cdot 1 = 40$.

**Length 4 (right - left = 3, two balloons between):**
Calculate `dp[0][3]` (range contains index 1 and 2, which are `3` and `1`).
- Try bursting index 1 (value 3) last ($k=1$):
  `dp[0][1] + dp[1][3] + 1 * 3 * 5 = 0 + 15 + 15 = 30`
- Try bursting index 2 (value 1) last ($k=2$):
  `dp[0][2] + dp[2][3] + 1 * 1 * 5 = 3 + 0 + 5 = 8`
- Max for `dp[0][3] = 30`.

We continue expanding length until we calculate `dp[0][5]`, which covers all original balloons and gives the final answer: `167`.

---

## Comparison with Matrix Chain Multiplication

Burst Balloons is structurally identical to Matrix Chain Multiplication.

| Aspect | Matrix Chain Multiplication | Burst Balloons |
|--------|-----------------------------|----------------|
| **Goal** | Minimize multiplication cost | Maximize burst coins |
| **State $dp[left][right]$** | Cost to multiply matrices $left$ to $right$ | Coins from bursting balloons between $left$ and $right$ |
| **Split point $k$** | Where to make the *last* matrix multiplication | Which balloon to burst *last* |
| **Merge calculation**| $p[left-1] \cdot p[k] \cdot p[right]$ | $nums[left] \cdot nums[k] \cdot nums[right]$ |
| **Boundaries** | Array of dimension sizes | Explicit virtual `1`s at ends |

---

## Related Problem: Minimum Score Triangulation

Given a convex polygon with $n$ vertices, find the minimum score to triangulate it. The score of a triangle is the product of its 3 vertices.

**Insight:**
Any triangulation of a polygon $[left \dots right]$ must contain exactly one triangle that uses the base edge $(left, right)$. Let the third vertex of this triangle be $k$. This triangle splits the remaining polygon into two smaller polygons: $[left \dots k]$ and $[k \dots right]$.

**Recurrence:**
$$
dp[left][right] = \min_{left < k < right} \left( dp[left][k] + dp[k][right] + v[left] \cdot v[k] \cdot v[right] \right)
$$

Notice this is **exactly the same recurrence** as Burst Balloons, just minimizing instead of maximizing!

---

## Advanced Variation: Remove Boxes

Remove Boxes is a FANG-favorite Hard problem that looks like Burst Balloons but requires a **3D State**.

**Problem:** Given an array of colors, remove consecutive boxes of the same color to get points equal to `(count)^2`.
Example: `[1, 3, 2, 2, 2, 3, 4, 3, 1]`

**Why 2D DP Fails Here:**
In Burst Balloons, when a balloon bursts, neighbors become adjacent, but the score formula `nums[left]*nums[k]*nums[right]` only cares about the *values* of the immediate neighbors.
In Remove Boxes, when boxes are removed, separated boxes of the same color merge together (e.g., removing the `2`s above merges the `3`s into `[3, 3, 3]`). The points are `count^2`, so grouping them *before* removing yields far more points ($3^2 = 9$ instead of $1^2 + 2^2 = 5$).
A 2D state `dp[left][right]` cannot remember how many boxes of the same color as `boxes[left]` are waiting just outside the left boundary.

**The 3D State Solution:**
`dp(left, right, k)` = max points for `boxes[left...right]` given that there are exactly `k` boxes of the same color as `boxes[left]` attached immediately to the left of `left`.

```python
from functools import lru_cache
from typing import List

def removeBoxes(boxes: List[int]) -> int:
    @lru_cache(None)
    def dp(left: int, right: int, k: int) -> int:
        if left > right:
            return 0

        # Optimization: Group identical consecutive boxes at the start
        while left < right and boxes[left] == boxes[left + 1]:
            left += 1
            k += 1

        # Option 1: Remove boxes[left] along with the k attached boxes right now.
        # This gives us (k + 1)^2 points, and we recursively solve the remaining boxes[left+1...right].
        result = (k + 1) ** 2 + dp(left + 1, right, 0)

        # Option 2: Try to merge boxes[left] with another box of the same color later in the array.
        # We look for a box boxes[m] == boxes[left].
        # If we remove everything strictly between left and m (i.e., boxes[left+1...m-1]),
        # then boxes[left] and its k attached boxes will touch boxes[m].
        for m in range(left + 1, right + 1):
            if boxes[m] == boxes[left]:
                # Cost to remove the middle + cost of the merged remainder
                result = max(result, dp(left + 1, m - 1, 0) + dp(m, right, k + 1))

        return result

    return dp(0, len(boxes) - 1, 0)
```
*Time Complexity:* $O(n^4)$. Space: $O(n^3)$.

---

## Common Mistakes & Pitfalls

1. **Forgetting Virtual Boundaries:**
   If you don't add `[1]` to the ends of the array, calculating `nums[left] * nums[k] * nums[right]` will throw index out of bounds errors when bursting the original edge balloons.

2. **Wrong Loop Order in Tabulation:**
   If you iterate `left` from `0` to `n` and `right` from `left` to `n`, you will calculate `dp[left][right]` before `dp[k][right]` is ready. **Interval DP tabulation must loop by interval length first**, or loop `left` backwards (`n-1` down to `0`) and `right` forwards (`left+1` to `n`).

3. **Inclusive vs Exclusive Bounds Confusion:**
   Our state definition makes `left` and `right` **exclusive** bounds.
   - Size of the dp array must be `(n+2) x (n+2)` (where $n$ is original length).
   - $k$ must range strictly between: `for k in range(left + 1, right)`.

## Summary Checklist for Burst Balloons Pattern
- [ ] Does removing an element merge its left and right neighbors?
- [ ] Does the score depend on these new neighbors?
- [ ] **Action:** Think about the LAST element removed.
- [ ] **Action:** Add virtual boundaries to the input array.
- [ ] **Action:** Use $O(n^3)$ Interval DP mapping out `dp[left][right]` exclusively.

---

## Next: [18-dp-on-strings.md](./18-dp-on-strings.md)

Advanced string DP problems.

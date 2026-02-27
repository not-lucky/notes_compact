# Burst Balloons

> **Prerequisites:** [16-matrix-chain](./16-matrix-chain.md)

## Overview

Burst Balloons is a classic and notoriously difficult Interval DP problem. It requires a counterintuitive insight: **thinking about the LAST element to process rather than the first**.

When dealing with arrays where removing an element changes the adjacency (neighbors) of the remaining elements, standard DP approaches often fail due to chaotic state dependencies. The Burst Balloons pattern solves this by working backwards.

---

## Building Intuition: Why Think Backwards?

Imagine we have balloons `[A, B, C, D]`.

### The Problem with "First Burst" (Forward Thinking)
If we burst `B` first, its neighbors `A` and `C` are involved in the score. After `B` pops, `A` and `C` become adjacent.
The new array is `[A, C, D]`.
If we then burst `C`, its neighbors are now `A` and `D`. The score for bursting `C` depends on the fact that `B` was already burst. This means our subproblems are not independent—they depend on the exact sequence of previous bursts. Tracking all possible remaining configurations requires $O(2^n)$ states.

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
`nums = [1] + original_nums + [1]`

### 2. State Definition
We use an **exclusive** range definition.
Let $dp[i][j]$ be the maximum coins obtained by bursting ALL balloons **strictly between** index $i$ and index $j$.
*Note: Balloons $i$ and $j$ themselves are NOT burst in this subproblem. They act as the indestructible walls (neighbors) for the last balloon burst in the range.*

### 3. Transitions
To find $dp[i][j]$, we guess which balloon $k$ (where $i < k < j$) is the **last** to burst.
If $k$ is the last to burst:
1. We must first burst all balloons between $i$ and $k$: cost is $dp[i][k]$
2. We must also burst all balloons between $k$ and $j$: cost is $dp[k][j]$
3. Finally, we burst $k$. Since all balloons strictly between $i$ and $j$ except $k$ are gone, $k$'s neighbors are exactly $i$ and $j$. The coins gained are: `nums[i] * nums[k] * nums[j]`.

$$
dp[i][j] = \max_{i < k < j} \left( dp[i][k] + dp[k][j] + nums[i] \cdot nums[k] \cdot nums[j] \right)
$$

### 4. Base Case
If there are no balloons strictly between $i$ and $j$ (i.e., $i + 1 == j$), then $dp[i][j] = 0$.

---

## Implementations

### Top-Down (Memoization)
Memoization is often much easier to write for Interval DP because you don't have to manually manage the loop order. The recursion naturally processes smaller intervals first.

```python
from functools import lru_cache

def maxCoins(nums: list[int]) -> int:
    # 1. Add virtual boundaries
    nums = [1] + nums + [1]

    @lru_cache(None)
    def dp(left: int, right: int) -> int:
        # Base case: no balloons strictly between left and right
        if left + 1 == right:
            return 0

        max_coins = 0
        # Try bursting every balloon k LAST
        for k in range(left + 1, right):
            coins = nums[left] * nums[k] * nums[right]
            total = dp(left, k) + dp(k, right) + coins
            max_coins = max(max_coins, total)

        return max_coins

    # We want to burst all original balloons,
    # which are strictly between index 0 and index len(nums)-1
    return dp(0, len(nums) - 1)
```

### Bottom-Up (Tabulation)
For Tabulation, **loop order is critical**. $dp[i][j]$ depends on $dp[i][k]$ and $dp[k][j]$. Notice that the intervals $(i, k)$ and $(k, j)$ are strictly **shorter** than $(i, j)$.
Therefore, we must solve subproblems ordered by **interval length**.

```python
def maxCoins(nums: list[int]) -> int:
    nums = [1] + nums + [1]
    n = len(nums)

    # dp[i][j] = max coins from bursting balloons strictly between i and j
    dp = [[0] * n for _ in range(n)]

    # Iterate by length of the interval (from 2 up to n-1)
    # length represents (j - i).
    # Min length is 2 (e.g., i=0, j=2, so strictly between is index 1)
    for length in range(2, n):
        for i in range(n - length):
            j = i + length

            # Try every possible last balloon k to burst in (i, j)
            for k in range(i + 1, j):
                coins = nums[i] * nums[k] * nums[j]
                dp[i][j] = max(dp[i][j], dp[i][k] + dp[k][j] + coins)

    return dp[0][n - 1]
```

**Complexity Analysis:**
- **Time Complexity:** $O(n^3)$. There are $O(n^2)$ states (all pairs of $i, j$). For each state, we iterate through $O(n)$ possible choices for $k$.
- **Space Complexity:** $O(n^2)$ to store the 2D DP table. Space cannot be optimized to 1D because $dp[i][j]$ depends on $dp[i][k]$ and $dp[k][j]$ which span multiple lengths and starting positions.

---

## Visual Walkthrough

Let `nums = [3, 1, 5, 8]`.
Add boundaries: `[1, 3, 1, 5, 8, 1]`. Let $n=6$.
Indices: `0  1  2  3  4  5`

**Length 2 (Base cases, j - i = 1):**
No balloons strictly between $i$ and $j$. All $dp[i][i+1] = 0$.

**Length 3 (j - i = 2, one balloon between):**
- $dp[0][2]$: Burst balloon 1 (value 3) last. Coins = $1 \cdot 3 \cdot 1 = 3$.
- $dp[1][3]$: Burst balloon 2 (value 1) last. Coins = $3 \cdot 1 \cdot 5 = 15$.
- $dp[2][4]$: Burst balloon 3 (value 5) last. Coins = $1 \cdot 5 \cdot 8 = 40$.
- $dp[3][5]$: Burst balloon 4 (value 8) last. Coins = $5 \cdot 8 \cdot 1 = 40$.

**Length 4 (j - i = 3, two balloons between):**
Calculate $dp[0][3]$ (range contains 3, 1).
- Try bursting index 1 (value 3) last ($k=1$):
  $dp[0][1] + dp[1][3] + 1 \cdot 3 \cdot 5 = 0 + 15 + 15 = 30$
- Try bursting index 2 (value 1) last ($k=2$):
  $dp[0][2] + dp[2][3] + 1 \cdot 1 \cdot 5 = 3 + 0 + 5 = 8$
- Max for $dp[0][3] = 30$.

We continue expanding length until we calculate $dp[0][5]$, which covers all original balloons and gives the final answer: `167`.

---

## Comparison with Matrix Chain Multiplication

Burst Balloons is structurally identical to Matrix Chain Multiplication.

| Aspect | Matrix Chain Multiplication | Burst Balloons |
|--------|-----------------------------|----------------|
| **Goal** | Minimize multiplication cost | Maximize burst coins |
| **State $dp[i][j]$** | Cost to multiply matrices $i$ to $j$ | Coins from bursting balloons between $i$ and $j$ |
| **Split point $k$** | Where to make the *last* matrix multiplication | Which balloon to burst *last* |
| **Merge calculation**| $p[i-1] \cdot p[k] \cdot p[j]$ | $nums[i] \cdot nums[k] \cdot nums[j]$ |
| **Boundaries** | Array of dimension sizes | Explicit virtual `1`s at ends |

---

## Related Problem: Minimum Score Triangulation

Given a convex polygon with $n$ vertices, find the minimum score to triangulate it. The score of a triangle is the product of its 3 vertices.

**Insight:**
Any triangulation of a polygon $[i \dots j]$ must contain exactly one triangle that uses the base edge $(i, j)$. Let the third vertex of this triangle be $k$. This triangle splits the remaining polygon into two smaller polygons: $[i \dots k]$ and $[k \dots j]$.

**Recurrence:**
$$
dp[i][j] = \min_{i < k < j} \left( dp[i][k] + dp[k][j] + v[i] \cdot v[k] \cdot v[j] \right)
$$

Notice this is **exactly the same recurrence** as Burst Balloons, just minimizing instead of maximizing!

---

## Advanced Variation: Remove Boxes

Remove Boxes is a FANG-favorite Hard problem that looks like Burst Balloons but requires a **3D State**.

**Problem:** Given an array of colors, remove consecutive boxes of the same color to get points equal to `(count)^2`.
Example: `[1, 3, 2, 2, 2, 3, 4, 3, 1]`

**Why 2D DP Fails Here:**
In Burst Balloons, when a balloon bursts, neighbors become adjacent, but the score formula `nums[i]*nums[k]*nums[j]` only cares about the *values* of the immediate neighbors.
In Remove Boxes, when boxes are removed, separated boxes of the same color merge together (e.g., removing the `2`s above merges the `3`s into `[3, 3, 3]`). The points are `count^2`, so grouping them *before* removing yields far more points ($3^2 = 9$ instead of $1^2 + 2^2 = 5$).
A 2D state $dp[i][j]$ cannot remember how many boxes of the same color as `boxes[i]` are waiting just outside the left boundary.

**The 3D State Solution:**
$dp(i, j, k) =$ max points for `boxes[i...j]` given that there are exactly $k$ boxes of the same color as `boxes[i]` attached immediately to the left of $i$.

```python
def removeBoxes(boxes: list[int]) -> int:
    n = len(boxes)
    memo = {}

    def dp(i: int, j: int, k: int) -> int:
        if i > j:
            return 0
        if (i, j, k) in memo:
            return memo[(i, j, k)]

        # Optimization: Group identical consecutive boxes at the start
        while i < j and boxes[i] == boxes[i + 1]:
            i += 1
            k += 1

        # Option 1: Remove boxes[i] along with the k attached boxes right now.
        # This gives us (k + 1)^2 points, and we recursively solve the remaining boxes[i+1...j].
        result = (k + 1) ** 2 + dp(i + 1, j, 0)

        # Option 2: Try to merge boxes[i] with another box of the same color later in the array.
        # We look for a box boxes[m] == boxes[i].
        # If we remove everything strictly between i and m (i.e., boxes[i+1...m-1]),
        # then boxes[i] and its k attached boxes will touch boxes[m].
        for m in range(i + 1, j + 1):
            if boxes[m] == boxes[i]:
                # Cost to remove the middle + cost of the merged remainder
                result = max(result, dp(i + 1, m - 1, 0) + dp(m, j, k + 1))

        memo[(i, j, k)] = result
        return result

    return dp(0, n - 1, 0)
```
*Time Complexity:* $O(n^4)$. Space: $O(n^3)$.

---

## Common Mistakes & Pitfalls

1. **Forgetting Virtual Boundaries:**
   If you don't add `[1]` to the ends of the array, calculating `nums[i] * nums[k] * nums[j]` will throw index out of bounds errors when bursting the original edge balloons.

2. **Wrong Loop Order in Tabulation:**
   If you iterate $i$ from $0 \to n$ and $j$ from $i \to n$, you will calculate $dp[i][j]$ before $dp[k][j]$ is ready. **Interval DP tabulation must loop by interval length first**, or loop $i$ backwards (`n-1` down to `0`) and $j$ forwards (`i+1` to `n`).

3. **Inclusive vs Exclusive Bounds Confusion:**
   Our state definition makes $i$ and $j$ **exclusive** bounds.
   - Size of the dp array must be `(n+2) x (n+2)` (where $n$ is original length).
   - $k$ must range strictly between: `for k in range(i + 1, j)`.

## Summary Checklist for Burst Balloons Pattern
- [ ] Does removing an element merge its left and right neighbors?
- [ ] Does the score depend on these new neighbors?
- [ ] **Action:** Think about the LAST element removed.
- [ ] **Action:** Add virtual boundaries to the input array.
- [ ] **Action:** Use $O(n^3)$ Interval DP mapping out $dp[i][j]$ exclusively.

---

## Next: [18-dp-on-strings.md](./18-dp-on-strings.md)

Advanced string DP problems.
# Burst Balloons

> **Prerequisites:** [16-matrix-chain](./16-matrix-chain.md)

## Overview

Burst Balloons is a classic interval DP problem requiring the counterintuitive insight of thinking about the LAST element to process rather than the first.

## Building Intuition

**Why think backwards (last burst, not first)?**

1. **The Problem with "First Burst"**: If we burst balloon i first, its neighbors change. The next burst depends on the new configuration. Tracking all possible configurations is exponential.

2. **The "Last Burst" Insight**: If balloon k is the LAST to burst in range (i, j), then:
   - All balloons between i and k are already gone
   - All balloons between k and j are already gone
   - k's neighbors at burst time are i and j (fixed!)

   This gives a clean recurrence: dp[i][j] = max(dp[i][k] + dp[k][j] + nums[i]×nums[k]×nums[j])

3. **Virtual Boundaries**: We add 1s at both ends ([1] + nums + [1]). This handles edge balloons gracefully—their "missing" neighbors become 1.

4. **State Definition**: dp[i][j] = max coins from bursting ALL balloons strictly between i and j (i and j are NOT burst). This "exclusive" definition makes the recurrence clean.

5. **Same as Matrix Chain**: The structure is identical! In matrix chain, we pick where to make the "final" multiplication. In balloons, we pick the "last" balloon to burst. The O(n³) pattern is the same.

6. **Mental Model**: Instead of asking "what should I do first?", ask "what's the last thing I'll do?" Work backwards. The last balloon bursted sees a predictable environment.

## Interview Context

Burst Balloons is a FANG+ hard problem because:

1. **Reverse thinking**: Consider last burst, not first
2. **Interval DP mastery**: Non-obvious state definition
3. **Tricky boundaries**: Virtual balloons at ends
4. **Matrix chain connection**: Similar structure

---

## When NOT to Use Burst Balloons Pattern

1. **Order Doesn't Affect Outcome**: If the result is the same regardless of burst order (like simple sum), DP is unnecessary.
   - *Example*: Finding the sum of an array where removing an element doesn't change anything else.

2. **No Range Structure**: If removing an element doesn't affect only its range (e.g., global effects), interval DP doesn't apply.
   - *Example*: A game where bursting a balloon doubles the score of all remaining balloons globally.

3. **Forward Thinking Works**: Some problems are naturally solved by considering "first" rather than "last." Only use "last" thinking when "first" creates dependency chaos.
   - *Example*: Coin Change. Taking a coin first doesn't change the properties of the remaining coins, so we don't need "last taken" logic.

4. **Small n (Brute Force)**: For $n \le 10$, brute force all permutations ($O(n!)$) might be acceptable and simpler to implement.
   - *Example*: A game board with 8 tiles where you want to find the exact optimal sequence of removals.

5. **Different Cost Function**: If bursting depends on more than just immediate neighbors (e.g., global state, history, or parity of elements remaining), the standard recurrence breaks.
   - *Example*: Cost is based on how many balloons have already been burst. You'd need an extra state dimension for the count, complicating the recurrence.

**Recognize This Pattern When:**

- Processing elements changes their neighbors
- "First" thinking leads to complex dependencies
- Range-based problem with "last processed" insight

---

## Problem Statement

Given n balloons with numbers, burst them to maximize coins.
Bursting balloon i gives `nums[i-1] * nums[i] * nums[i+1]` coins.

```
Input: nums = [3, 1, 5, 8]
Output: 167

Explanation:
Burst balloon 1 (value 1): 3*1*5 = 15 → nums = [3,5,8]
Burst balloon 5 (value 5): 3*5*8 = 120 → nums = [3,8]
Burst balloon 3 (value 3): 1*3*8 = 24 → nums = [8]
Burst balloon 8 (value 8): 1*8*1 = 8 → nums = []
Total: 15 + 120 + 24 + 8 = 167
```

---

## Key Insight: Think Backwards

**Wrong approach**: Which balloon to burst first?

- After bursting, neighbors change, making DP hard

**Correct approach**: Which balloon to burst LAST in a range?

- If k is last burst in range [i,j], neighbors are fixed as i-1 and j+1

---

## Solution

### Recurrence Relation

Let $nums$ be the 1-indexed array of balloons with virtual balloons $nums[0] = 1$ and $nums[n+1] = 1$.
Let $dp[i][j]$ be the maximum coins obtained by bursting all balloons strictly between index $i$ and index $j$ (exclusive).

$$
dp[i][j] =
\begin{cases}
0 & \text{if } i+1 = j \\
\max\limits_{i < k < j} \left\{ dp[i][k] + dp[k][j] + nums[i] \cdot nums[k] \cdot nums[j] \right\} & \text{if } i+1 < j
\end{cases}
$$

**Space & Time Complexity Analysis:**
Because $dp$ is an $O(n) \times O(n)$ table and computing each $dp[i][j]$ requires iterating over all possible split points $k$ where $i < k < j$ (taking $O(n)$ time), the total time complexity is $O(n^3)$.
Space is $O(n^2)$ for the table. It cannot be reduced to $O(n)$ because we need to query results of all $O(n^2)$ sub-intervals.

### Bottom-Up (Tabulation)

```python
def max_coins(nums: list[int]) -> int:
    """
    Maximum coins from bursting all balloons.

    Key insight: Consider which balloon is burst LAST in each range.
    Add virtual 1s at boundaries.

    State: dp[i][j] = max coins from bursting all balloons in (i,j) exclusive
    Recurrence: dp[i][j] = max(dp[i][k] + dp[k][j] + nums[i]*nums[k]*nums[j])
                for k in (i+1, j-1)

    Time: O(n³)
    Space: O(n²)
    """
    # Add virtual 1s at boundaries
    nums = [1] + nums + [1]
    n = len(nums)

    dp = [[0] * n for _ in range(n)]

    # Fill by increasing length
    for length in range(2, n):  # length between i and j
        for i in range(n - length):
            j = i + length

            for k in range(i + 1, j):  # k is last to burst
                coins = nums[i] * nums[k] * nums[j]
                total = dp[i][k] + dp[k][j] + coins
                dp[i][j] = max(dp[i][j], total)

    return dp[0][n - 1]
```

---

## Visual Walkthrough

```
nums = [3, 1, 5, 8]
With boundaries: [1, 3, 1, 5, 8, 1]
Indices:          0  1  2  3  4  5

dp[i][j] = max coins bursting all in (i, j) exclusive

Length 2 (no balloons between): all dp = 0

Length 3 (one balloon between):
dp[0][2]: burst 1 last → 1*3*1 = 3
dp[1][3]: burst 2 last → 3*1*5 = 15
dp[2][4]: burst 3 last → 1*5*8 = 40
dp[3][5]: burst 4 last → 5*8*1 = 40

Length 4 (two balloons between):
dp[0][3]: k=1 → dp[0][1] + dp[1][3] + 1*3*5 = 0 + 15 + 15 = 30
         k=2 → dp[0][2] + dp[2][3] + 1*1*5 = 3 + 0 + 5 = 8
         max = 30

dp[1][4]: k=2 → dp[1][2] + dp[2][4] + 3*1*8 = 0 + 40 + 24 = 64
         k=3 → dp[1][3] + dp[3][4] + 3*5*8 = 15 + 0 + 120 = 135
         max = 135

...

dp[0][5]: Check all k from 1 to 4
         Eventually max = 167
```

---

## Memoization Version

Many people find the top-down memoization approach more intuitive for interval DP because you don't have to worry about the complex loop ordering (iterating by length).

```python
from functools import lru_cache

def max_coins_memo(nums: list[int]) -> int:
    """
    Top-down memoized version.
    """
    nums = [1] + nums + [1]
    n = len(nums)

    @lru_cache(maxsize=None)
    def dp(left: int, right: int) -> int:
        # Base case: No balloons between left and right
        if left + 1 == right:
            return 0

        max_coins = 0
        # Try bursting every balloon k LAST
        for k in range(left + 1, right):
            coins = nums[left] * nums[k] * nums[right]
            total = dp(left, k) + dp(k, right) + coins
            max_coins = max(max_coins, total)

        return max_coins

    return dp(0, n - 1)
```

---

## Understanding the State

```
dp[i][j] represents bursting ALL balloons strictly between i and j.
Balloons at positions i and j are NOT burst.

When we burst k last:
- All balloons in (i, k) already burst → dp[i][k]
- All balloons in (k, j) already burst → dp[k][j]
- Now k is alone between i and j → nums[i] * nums[k] * nums[j]

Why this works:
- Since k is last, its neighbors at burst time are i and j
- Not the original neighbors (they're already burst)
```

---

## Common Variation: Minimum Cost

```python
def min_cost_burst(nums: list[int]) -> int:
    """
    Minimum cost to burst all balloons.
    """
    nums = [1] + nums + [1]
    n = len(nums)

    dp = [[0] * n for _ in range(n)]

    for length in range(2, n):
        for i in range(n - length):
            j = i + length
            dp[i][j] = float('inf')

            for k in range(i + 1, j):
                cost = nums[i] * nums[k] * nums[j]
                total = dp[i][k] + dp[k][j] + cost
                dp[i][j] = min(dp[i][j], total)

    return dp[0][n - 1]
```

---

## Related: Minimum Score Triangulation

Given a convex polygon with $n$ vertices, find the minimum score to triangulate it. The score of a triangle is the product of its 3 vertices.

### Recurrence Relation

Let $v$ be the array of vertex values. Let $dp[i][j]$ be the minimum score to triangulate the polygon formed by vertices $i, i+1, \dots, j$.

$$
dp[i][j] =
\begin{cases}
0 & \text{if } i+1 = j \quad \text{(a line, not a polygon)} \\
\min\limits_{i < k < j} \left\{ dp[i][k] + dp[k][j] + v[i] \cdot v[k] \cdot v[j] \right\} & \text{if } i+1 < j
\end{cases}
$$

```python
def min_score_triangulation(values: list[int]) -> int:
    """
    Triangulate polygon with minimum total score.
    Score of triangle = product of vertices.

    Time: O(n³)
    Space: O(n²)
    """
    n = len(values)
    dp = [[0] * n for _ in range(n)]

    for length in range(2, n):
        for i in range(n - length):
            j = i + length
            dp[i][j] = float('inf')

            for k in range(i + 1, j):
                score = values[i] * values[k] * values[j]
                total = dp[i][k] + dp[k][j] + score
                dp[i][j] = min(dp[i][j], total)

    return dp[0][n - 1]
```

---

## Related: Remove Boxes

```python
def remove_boxes(boxes: list[int]) -> int:
    """
    Remove consecutive same-color boxes for points.
    Points = (count of consecutive)²

    State: dp[i][j][k] = max points for boxes[i..j] with k
           same boxes attached to left of i

    Time: O(n⁴)
    Space: O(n³)
    """
    n = len(boxes)
    memo = {}

    def dp(i: int, j: int, k: int) -> int:
        if i > j:
            return 0

        if (i, j, k) in memo:
            return memo[(i, j, k)]

        # Skip same colored boxes at start
        while i < j and boxes[i] == boxes[i + 1]:
            i += 1
            k += 1

        # Remove boxes[i] with k attached
        result = (k + 1) ** 2 + dp(i + 1, j, 0)

        # Try to find same color later and remove together
        for m in range(i + 1, j + 1):
            if boxes[m] == boxes[i]:
                # Remove boxes[i+1..m-1] first, then combine
                result = max(result, dp(i + 1, m - 1, 0) + dp(m, j, k + 1))

        memo[(i, j, k)] = result
        return result

    return dp(0, n - 1, 0)
```

---

## Comparison with Matrix Chain

| Aspect        | Matrix Chain            | Burst Balloons              |
| ------------- | ----------------------- | --------------------------- |
| State meaning | Cost to multiply        | Coins from bursting         |
| Split point k | Where to split multiply | Last balloon to burst       |
| Merge cost    | p[i-1] × p[k] × p[j]    | nums[i] × nums[k] × nums[j] |
| Boundaries    | Dimensions array        | Virtual 1s at ends          |

---

## Edge Cases

```python
# 1. Single balloon
nums = [5]
# Return 1 * 5 * 1 = 5

# 2. Two balloons
nums = [3, 5]
# Burst 3 last: 1*3*1 + 1*5*3 = 3 + 15 = 18
# Burst 5 last: 1*5*1 + 3*1*5 = 5 + 15 = 20
# Return 20

# 3. All same values
nums = [1, 1, 1]
# Any order gives same result
```

---

## Common Mistakes

```python
# WRONG: Not adding boundary 1s
nums = [3, 1, 5, 8]
# Bursting edge balloon: 3 * 1 * ? → what's the neighbor?

# CORRECT: Add virtual 1s
nums = [1, 3, 1, 5, 8, 1]


# WRONG: Thinking about first burst, not last
# If we burst i first, neighbors change and DP breaks

# CORRECT: Think about last burst
# When k is last in range, neighbors are fixed


# WRONG: dp[i][j] includes i and j
for k in range(i, j + 1):  # Wrong range!

# CORRECT: dp[i][j] excludes i and j, k is strictly between
for k in range(i + 1, j):
```

---

## Complexity

| Metric      | Value          |
| ----------- | -------------- |
| Time        | O(n³)          |
| Space       | O(n²)          |
| States      | O(n²)          |
| Transitions | O(n) per state |

---

## Interview Tips

1. **Explain the insight**: "Consider last balloon burst"
2. **Add boundaries first**: Mention virtual 1s immediately
3. **Define state clearly**: What dp[i][j] means
4. **Walk through example**: Show understanding
5. **Know related problems**: Matrix chain, triangulation

---

## Practice Problems

| #   | Problem                 | Difficulty | Similar Pattern |
| --- | ----------------------- | ---------- | --------------- |
| 1   | Burst Balloons          | Hard       | Core problem    |
| 2   | Min Score Triangulation | Medium     | Same structure  |
| 3   | Remove Boxes            | Hard       | 3D state        |
| 4   | Strange Printer         | Hard       | Similar         |

---

## Key Takeaways

1. **Think backwards**: Last burst, not first
2. **Add virtual boundaries**: Simplifies edge cases
3. **Interval DP**: dp[i][j] for ranges
4. **k is last burst**: Neighbors fixed as i, j
5. **Same as matrix chain**: Just different meaning

---

## Next: [18-dp-on-strings.md](./18-dp-on-strings.md)

Advanced string DP problems.

# 1D DP Basics

> **Prerequisites:** [01-dp-fundamentals](./01-dp-fundamentals.md), [02-memoization-vs-tabulation](./02-memoization-vs-tabulation.md)

## Overview

1D DP uses a single-dimensional state (dp[i]) representing the answer for position i, the first i elements, or elements ending at i.

## Building Intuition

**Why does 1D DP work for so many problems?**

1. **Sequential Decision Making**: Many problems involve processing elements one at a time, making a decision at each step. The state only needs to track "where we are" (index i), not "how we got here."

2. **State Compression**: Even if multiple paths lead to position i, the optimal answer at i is the same. We don't care about the path—only the result. This is the "principle of optimality."

3. **Pattern Recognition**: Most 1D DP problems fall into a few patterns:
   - **Fibonacci-like**: dp[i] depends on dp[i-1] and dp[i-2]
   - **Take/Skip**: At each position, choose to include or exclude
   - **Best Ending Here**: Track the best subarray/subsequence ending at i
   - **Prefix Accumulation**: Build answer from left to right

4. **Space Optimization Insight**: If dp[i] only depends on a constant number of previous states (not all of dp[0..i-1]), we can reduce from O(n) to O(1) space by only keeping those states.

5. **Mental Model**: Think of 1D DP as filling a row of boxes from left to right, where each box's value is computed from previous boxes using a fixed formula.

## Interview Context

1D DP problems are the building blocks:

1. **Foundation**: Master these before 2D DP
2. **Common patterns**: Same structure appears in many problems
3. **Quick to solve**: Often warm-up or first questions
4. **Space optimization**: Usually reducible to O(1) space

---

## When NOT to Use 1D DP

1. **Problem Requires Multiple Dimensions**: If the state needs to track two variables (e.g., position AND remaining capacity), you need 2D DP. Forcing 1D won't work.

2. **All Pairs/Substrings Needed**: Problems like LCS or edit distance inherently need dp[i][j] for all pairs. 1D DP can't express this directly (though space optimization can reduce storage).

3. **Non-Linear Dependencies**: If dp[i] depends on all previous dp[j] values (not just a constant number), you still get O(n²) time even with 1D space.

4. **State Includes More Than Position**: If the optimal answer at position i depends on additional information (like which items were taken), you need more dimensions or a different approach.

5. **Graph Structure**: Grid/tree problems with branching paths often require 2D or tree DP, not linear 1D.

**Signs 1D DP is Appropriate:**
- Input is a single array/string processed linearly
- Decision at position i only depends on a constant number of previous positions
- No "knapsack-like" capacity constraint

---

## Pattern 1: Fibonacci-like

State depends on previous 1-2 states.

### Template

```python
def fibonacci_pattern(n: int) -> int:
    if n <= 1:
        return base_cases[n]

    prev2, prev1 = base_cases[0], base_cases[1]

    for i in range(2, n + 1):
        curr = f(prev1, prev2)  # Some function
        prev2 = prev1
        prev1 = curr

    return prev1
```

### Climbing Stairs

```python
def climb_stairs(n: int) -> int:
    """
    Count ways to climb n stairs (1 or 2 steps at a time).

    State: dp[i] = ways to reach step i
    Recurrence: dp[i] = dp[i-1] + dp[i-2]

    Time: O(n)
    Space: O(1)
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

### Min Cost Climbing Stairs

```python
def min_cost_climbing_stairs(cost: list[int]) -> int:
    """
    Minimum cost to reach top. Can start at step 0 or 1.

    State: dp[i] = min cost to reach step i
    Recurrence: dp[i] = cost[i] + min(dp[i-1], dp[i-2])

    Time: O(n)
    Space: O(1)
    """
    n = len(cost)

    # Can start at 0 or 1
    prev2, prev1 = cost[0], cost[1]

    for i in range(2, n):
        curr = cost[i] + min(prev1, prev2)
        prev2 = prev1
        prev1 = curr

    # Can end at n-1 or n-2
    return min(prev1, prev2)
```

---

## Pattern 2: Take or Skip

At each position, decide whether to take or skip the current element.

### House Robber

```python
def rob(nums: list[int]) -> int:
    """
    Maximum sum of non-adjacent elements.

    State: dp[i] = max money robbing houses 0..i
    Recurrence: dp[i] = max(dp[i-1], dp[i-2] + nums[i])

    Time: O(n)
    Space: O(1)
    """
    if not nums:
        return 0
    if len(nums) == 1:
        return nums[0]

    prev2, prev1 = nums[0], max(nums[0], nums[1])

    for i in range(2, len(nums)):
        curr = max(prev1, prev2 + nums[i])
        prev2 = prev1
        prev1 = curr

    return prev1
```

### Delete and Earn

```python
def delete_and_earn(nums: list[int]) -> int:
    """
    Pick num, earn num points, delete all num-1 and num+1.

    Key insight: Transform to House Robber!

    Time: O(n + max(nums))
    Space: O(max(nums))
    """
    if not nums:
        return 0

    max_num = max(nums)
    points = [0] * (max_num + 1)

    for num in nums:
        points[num] += num

    # Now it's House Robber on points array
    prev2, prev1 = 0, 0

    for i in range(max_num + 1):
        curr = max(prev1, prev2 + points[i])
        prev2 = prev1
        prev1 = curr

    return prev1
```

---

## Pattern 3: Prefix/Suffix Optimization

Use prefix sums or precomputed values.

### Maximum Subarray (Kadane's Algorithm)

```python
def max_subarray(nums: list[int]) -> int:
    """
    Find contiguous subarray with largest sum.

    State: dp[i] = max sum subarray ending at i
    Recurrence: dp[i] = max(nums[i], dp[i-1] + nums[i])

    Time: O(n)
    Space: O(1)
    """
    max_sum = curr_sum = nums[0]

    for i in range(1, len(nums)):
        curr_sum = max(nums[i], curr_sum + nums[i])
        max_sum = max(max_sum, curr_sum)

    return max_sum
```

### Maximum Product Subarray

```python
def max_product(nums: list[int]) -> int:
    """
    Find contiguous subarray with largest product.

    Track both max and min (negative can become positive).

    Time: O(n)
    Space: O(1)
    """
    max_prod = min_prod = result = nums[0]

    for i in range(1, len(nums)):
        if nums[i] < 0:
            max_prod, min_prod = min_prod, max_prod

        max_prod = max(nums[i], max_prod * nums[i])
        min_prod = min(nums[i], min_prod * nums[i])

        result = max(result, max_prod)

    return result
```

---

## Pattern 4: Counting Ways

Count number of ways to achieve something.

### Decode Ways

```python
def num_decodings(s: str) -> int:
    """
    Count ways to decode '1'-'26' to 'A'-'Z'.

    State: dp[i] = ways to decode s[0..i-1]

    Time: O(n)
    Space: O(1)
    """
    if not s or s[0] == '0':
        return 0

    n = len(s)
    prev2, prev1 = 1, 1  # dp[0] = 1, dp[1] = 1

    for i in range(2, n + 1):
        curr = 0

        # Single digit (1-9)
        if s[i - 1] != '0':
            curr += prev1

        # Two digits (10-26)
        two_digit = int(s[i - 2:i])
        if 10 <= two_digit <= 26:
            curr += prev2

        prev2 = prev1
        prev1 = curr

    return prev1
```

### Perfect Squares

```python
def num_squares(n: int) -> int:
    """
    Minimum perfect squares that sum to n.

    State: dp[i] = min squares for sum i
    Recurrence: dp[i] = min(dp[i - j*j] + 1) for all valid j

    Time: O(n√n)
    Space: O(n)
    """
    dp = [float('inf')] * (n + 1)
    dp[0] = 0

    for i in range(1, n + 1):
        j = 1
        while j * j <= i:
            dp[i] = min(dp[i], dp[i - j * j] + 1)
            j += 1

    return dp[n]
```

---

## Pattern 5: Optimization with Constraints

### Jump Game

```python
def can_jump(nums: list[int]) -> bool:
    """
    Can reach the last index?

    Greedy approach is better here, but DP works.

    Time: O(n)
    Space: O(1)
    """
    max_reach = 0

    for i in range(len(nums)):
        if i > max_reach:
            return False
        max_reach = max(max_reach, i + nums[i])

    return True
```

### Jump Game II

```python
def jump(nums: list[int]) -> int:
    """
    Minimum jumps to reach last index.

    BFS-like approach.

    Time: O(n)
    Space: O(1)
    """
    n = len(nums)
    if n <= 1:
        return 0

    jumps = 0
    curr_end = 0
    farthest = 0

    for i in range(n - 1):
        farthest = max(farthest, i + nums[i])

        if i == curr_end:
            jumps += 1
            curr_end = farthest

            if curr_end >= n - 1:
                break

    return jumps
```

---

## Visual: 1D DP State Transitions

```
Climbing Stairs:
dp[i] = dp[i-1] + dp[i-2]

    dp[0]  dp[1]  dp[2]  dp[3]  dp[4]  dp[5]
      1      1      2      3      5      8
             ↘    ↗  ↘    ↗  ↘    ↗  ↘    ↗
              ↘  ↗    ↘  ↗    ↘  ↗    ↘  ↗
               ↘↗      ↘↗      ↘↗      ↘↗


House Robber:
dp[i] = max(dp[i-1], dp[i-2] + nums[i])

    nums:  2    7    9    3    1
    dp[i]: 2    7   11   11   12
              skip→  ↗    ↗    ↗
                 ↘  rob  skip  rob
                   ↘  ↗
```

---

## Common Mistakes

```python
# WRONG: Forgetting edge cases
def climb_stairs(n):
    prev2, prev1 = 1, 2
    for _ in range(3, n + 1):  # Fails for n=1
        ...

# CORRECT: Handle small n
def climb_stairs(n):
    if n <= 2:
        return n
    ...


# WRONG: Wrong recurrence
def rob(nums):
    for i in range(len(nums)):
        dp[i] = dp[i-1] + nums[i]  # Wrong! Can't rob adjacent

# CORRECT:
dp[i] = max(dp[i-1], dp[i-2] + nums[i])
```

---

## Practice Problems

| # | Problem | Difficulty | Pattern |
|---|---------|------------|---------|
| 1 | Climbing Stairs | Easy | Fibonacci |
| 2 | Min Cost Climbing | Easy | Fibonacci + min |
| 3 | House Robber | Medium | Take/skip |
| 4 | House Robber II | Medium | Circular array |
| 5 | Maximum Subarray | Medium | Kadane's |
| 6 | Decode Ways | Medium | Counting |
| 7 | Perfect Squares | Medium | Unbounded |
| 8 | Jump Game | Medium | Optimization |

---

## Key Takeaways

1. **Most 1D DP needs only O(1) space**: Just track last 1-2 values
2. **Identify the recurrence**: What does current state depend on?
3. **Handle edge cases**: Small n often special
4. **Pattern recognition**: Fibonacci-like, take/skip, prefix optimization
5. **Transform if needed**: Delete and Earn → House Robber

---

## Next: [04-house-robber.md](./04-house-robber.md)

Deep dive into House Robber variants.

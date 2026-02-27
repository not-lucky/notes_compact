# 1D DP Basics

> **Prerequisites:** [01-dp-fundamentals](./01-dp-fundamentals.md), [02-memoization-vs-tabulation](./02-memoization-vs-tabulation.md)

## Overview

1D Dynamic Programming involves solving problems where the state can be represented by a single variable, typically an index `i`. This state, `dp[i]`, usually represents the optimal solution for the problem up to index `i`, the solution starting at index `i`, or the solution specifically ending at index `i`.

## Building Intuition

**Why does 1D DP work for so many problems?**

1. **Sequential Decision Making**: Many problems involve processing elements one at a time from left to right, making a decision at each step. The state only needs to track "where we are" (index `i`), not the entire history of "how we got here."
2. **State Compression (Optimal Substructure)**: Even if multiple paths or combinations lead to position `i`, we only care about the *best* result at `i`. We discard suboptimal paths. This allows us to build global optimums from local optimums.
3. **Overlapping Subproblems**: Calculating the answer for `i` requires the answers for `i-1`, `i-2`, etc. We store these smaller answers to avoid redundant work.
4. **Pattern Recognition**: Most 1D DP problems fall into recognizable patterns:
   - **Fibonacci-style**: `dp[i]` depends strictly on a fixed number of previous states (like `dp[i-1]` and `dp[i-2]`).
   - **Take/Skip (Include/Exclude)**: At each position, decide whether to include the current element in the optimal solution or skip it.
   - **Best Ending Here**: The state *must* include the element at index `i`. Used for contiguous subarrays.
5. **Space Optimization**: If `dp[i]` only depends on a constant number of previous states (e.g., just `i-1` and `i-2`), we don't need an array of size $O(N)$. We can maintain just a few variables, reducing space complexity from $O(N)$ to $O(1)$.

## When NOT to Use 1D DP

Recognizing when 1D DP will fail saves a lot of time:

1. **Multiple Constraining Variables**: If your decision depends on the current position *and* another factor (like remaining capacity in a knapsack, or a secondary string), you need 2D DP.
2. **All Pairs/Substrings Required**: Problems asking about palindromes within a string or comparing two strings (Longest Common Subsequence) inherently need to track a start and end point, requiring `dp[i][j]` (2D).
3. **Graph/Tree Structures**: If the problem involves moving through a grid, a tree, or an arbitrary graph, a simple 1D array isn't enough to capture the state transitions.

**Signs 1D DP is Appropriate:**
- The input is a single array, string, or integer $N$.
- You process the input linearly (left-to-right or right-to-left).
- There is no secondary capacity constraint.
- The problem asks for a maximum, minimum, or total number of ways.

---

## Pattern 1: Fibonacci-style (Constant Lookback)

The current state depends on a fixed number of immediately preceding states.

### Climbing Stairs
You are climbing a staircase. It takes `n` steps to reach the top. Each time you can either climb 1 or 2 steps. In how many distinct ways can you climb to the top?

**Recurrence Relation:**
To reach step `i`, you must have come from either step `i-1` (taking a 1-step) or step `i-2` (taking a 2-step).
Therefore, the total ways to reach `i` is the sum of ways to reach `i-1` and `i-2`.
$$dp[i] = dp[i-1] + dp[i-2]$$

*Base Cases:*
$dp[1] = 1$ (1 way: [1])
$dp[2] = 2$ (2 ways: [1,1], [2])

**Space Optimization:** We only ever need the last two values.

```python
def climb_stairs(n: int) -> int:
    """
    Time: O(n) | Space: O(1)
    """
    if n <= 2:
        return n

    # prev2 represents dp[i-2], prev1 represents dp[i-1]
    prev2, prev1 = 1, 2

    for _ in range(3, n + 1):
        curr = prev1 + prev2
        # Shift the window forward
        prev2 = prev1
        prev1 = curr

    return prev1
```

### Min Cost Climbing Stairs
You are given an integer array `cost` where `cost[i]` is the cost of $i^{th}$ step. Once you pay the cost, you can climb one or two steps. You can start from step 0 or step 1. Return the minimum cost to reach the top of the floor (beyond the last element).

**Recurrence Relation:**
Let `dp[i]` be the minimum cost to *reach* step `i`.
To reach step `i`, you came from `i-1` (and paid `cost[i-1]`) OR from `i-2` (and paid `cost[i-2]`).
$$dp[i] = \min(dp[i-1] + cost[i-1], dp[i-2] + cost[i-2])$$

*Base Cases:*
$dp[0] = 0$ (Start here for free)
$dp[1] = 0$ (Start here for free)

```python
def min_cost_climbing_stairs(cost: list[int]) -> int:
    """
    Time: O(n) | Space: O(1)
    """
    n = len(cost)

    # prev2 represents dp[i-2], prev1 represents dp[i-1]
    prev2, prev1 = 0, 0

    # We want to reach the "top", which is index n
    for i in range(2, n + 1):
        curr = min(prev1 + cost[i-1], prev2 + cost[i-2])
        prev2 = prev1
        prev1 = curr

    return prev1
```

---

## Pattern 2: Take or Skip (Include / Exclude)

At each position, you decide whether including the current element yields a better result than excluding it, often constrained by rules (e.g., cannot take adjacent elements).

### House Robber
You are a robber planning to rob houses. `nums[i]` is the amount of money in the $i^{th}$ house. You cannot rob adjacent houses. Return the maximum amount of money you can rob.

**Recurrence Relation:**
At house `i`, you have two choices:
1. **Skip it**: Keep the max profit up to house `i-1`. ($dp[i-1]$)
2. **Take it**: Add its value to the max profit up to house `i-2` (since you can't rob `i-1`). ($dp[i-2] + nums[i]$)

$$dp[i] = \max(dp[i-1], dp[i-2] + nums[i])$$

```python
def rob(nums: list[int]) -> int:
    """
    Time: O(n) | Space: O(1)
    """
    # rob1 = dp[i-2], rob2 = dp[i-1]
    rob1, rob2 = 0, 0

    for amount in nums:
        # dp[i] = max(skip, take)
        curr = max(rob2, rob1 + amount)
        # Shift variables
        rob1 = rob2
        rob2 = curr

    return rob2
```

### Delete and Earn
Given an integer array `nums`, you can pick an element `x`, earn `x` points, but you must delete *all* occurrences of `x - 1` and `x + 1`. Maximize points.

**Insight:** This is House Robber in disguise! If we transform the input into an array where the index is the number and the value is the total sum of that number, the rule "deleting `x-1` and `x+1`" is identical to "cannot rob adjacent houses".

```python
def delete_and_earn(nums: list[int]) -> int:
    """
    Time: O(N + M) where N=len(nums), M=max(nums)
    Space: O(M)
    """
    if not nums:
        return 0

    max_num = max(nums)
    # sum_array[i] will hold the total sum of all occurrences of number i
    sum_array = [0] * (max_num + 1)

    for num in nums:
        sum_array[num] += num

    # Standard House Robber logic on sum_array
    rob1, rob2 = 0, 0
    for amount in sum_array:
        curr = max(rob2, rob1 + amount)
        rob1 = rob2
        rob2 = curr

    return rob2
```

---

## Pattern 3: "Best Ending Here" (Kadane's)

Used for contiguous subarrays. The state `dp[i]` represents the optimal subarray that *must end at index `i`*.

### Maximum Subarray
Given an integer array `nums`, find the contiguous subarray with the largest sum.

**Recurrence Relation:**
At index `i`, you have a choice:
1. Extend the previous best subarray ending at `i-1` by adding `nums[i]`. ($dp[i-1] + nums[i]$)
2. Start a completely new subarray at `i`. ($nums[i]$)

You choose the maximum of these two.
$$dp[i] = \max(nums[i], dp[i-1] + nums[i])$$

The global maximum is the maximum value found in the entire `dp` array.

```python
def max_subarray(nums: list[int]) -> int:
    """
    Time: O(n) | Space: O(1)
    """
    # Initialize both to the first element
    max_sum = nums[0]
    curr_sum = nums[0]

    for i in range(1, len(nums)):
        # Decide: Extend existing subarray or start a new one
        curr_sum = max(nums[i], curr_sum + nums[i])
        # Update global max
        max_sum = max(max_sum, curr_sum)

    return max_sum
```

### Maximum Product Subarray
Like max subarray, but tracking the largest product.

**Insight:** Because multiplying two negative numbers yields a positive number, a very small (negative) product can instantly become the largest product if the current number is negative. Therefore, we must track *both* the maximum and minimum products ending at `i`.

```python
def max_product(nums: list[int]) -> int:
    """
    Time: O(n) | Space: O(1)
    """
    if not nums:
        return 0

    # global max
    res = nums[0]
    # local min and max ending at current index
    curr_min, curr_max = nums[0], nums[0]

    for i in range(1, len(nums)):
        num = nums[i]

        # We need to compute candidates before reassigning
        # The candidates are:
        # 1. The number itself (starting a new subarray)
        # 2. Extend the max product so far
        # 3. Extend the min product so far (if num is negative)

        tmp_max = max(num, curr_max * num, curr_min * num)
        curr_min = min(num, curr_max * num, curr_min * num)
        curr_max = tmp_max

        res = max(res, curr_max)

    return res
```

---

## Pattern 4: Combinatorics (Counting Ways)

Counting the total number of ways to reach a state.

### Decode Ways
A message containing letters 'A'-'Z' is encoded as '1'-'26'. Given a string `s` of digits, return the number of ways to decode it.

**Recurrence Relation:**
At index `i` (representing string length `i`):
`dp[i]` = ways to decode string of length `i`.
- If the single character at `s[i-1]` is valid ('1'-'9'), we can append it to all decodings of length `i-1`. Add `dp[i-1]`.
- If the two characters ending at `s[i-1]` form a valid number ('10'-'26'), we can append it to all decodings of length `i-2`. Add `dp[i-2]`.

```python
def num_decodings(s: str) -> int:
    """
    Time: O(n) | Space: O(1)
    """
    if not s or s[0] == '0':
        return 0

    # prev2 = dp[i-2], prev1 = dp[i-1]
    # Base cases for empty string and length 1
    prev2, prev1 = 1, 1

    for i in range(2, len(s) + 1):
        curr = 0

        # Single digit decode (1-9)
        # s is 0-indexed, so s[i-1] is the current character
        if s[i-1] != '0':
            curr += prev1

        # Two digit decode (10-26)
        two_digit = int(s[i-2:i])
        if 10 <= two_digit <= 26:
            curr += prev2

        prev2 = prev1
        prev1 = curr

    return prev1
```

---

## Pattern 5: Unbounded Lookback

Sometimes `dp[i]` depends on all previous states `dp[0]...dp[i-1]`, not just a constant number. This means $O(n)$ space is required, and time complexity is usually $O(n^2)$ or $O(n\sqrt{n})$.

### Perfect Squares
Given `n`, return the least number of perfect square numbers that sum to `n`.

**Recurrence Relation:**
To find `dp[i]`, we can try subtracting every valid perfect square $j^2 \le i$. The answer is 1 (for the square we just subtracted) plus the optimal answer for the remainder $i - j^2$.
$$dp[i] = 1 + \min_{j^2 \le i}(dp[i - j^2])$$

```python
def num_squares(n: int) -> int:
    """
    Time: O(n * sqrt(n)) | Space: O(n)
    """
    # Initialize with worst case: sum of 1s (e.g., n=4 -> 1+1+1+1)
    dp = [i for i in range(n + 1)]

    for target in range(1, n + 1):
        # Check all possible squares less than or equal to current target
        j = 1
        while j * j <= target:
            dp[target] = min(dp[target], 1 + dp[target - j*j])
            j += 1

    return dp[n]
```

---

## Visual: 1D DP State Transitions

**House Robber DP Table:**
`nums = [2, 7, 9, 3, 1]`

| i | House Value | Choice 1: Skip (take `dp[i-1]`) | Choice 2: Take (`dp[i-2] + val`) | Best `dp[i]` |
| :--- | :--- | :--- | :--- | :--- |
| **0** | `2` | 0 | 0 + 2 | **2** |
| **1** | `7` | 2 | 0 + 7 | **7** |
| **2** | `9` | 7 | 2 + 9 | **11** |
| **3** | `3` | 11 | 7 + 3 | **11** |
| **4** | `1` | 11 | 11 + 1 | **12** |

---

## Key Takeaways

1. **State Definition is King**: Clearly define what `dp[i]` represents in plain English before writing code. (e.g., "The max profit robbing houses up to index i").
2. **Find the Recurrence**: Ask yourself, "If I already knew the answers for smaller subproblems, how would I calculate the answer for the current step?"
3. **Check Space Optimization**: If your `for` loop only looks at `dp[i-1]` and `dp[i-2]`, throw away the array and use variables.
4. **Identify the Base Cases**: What are the trivial answers for `n=0`, `n=1`, etc.?
5. **Beware "Best Ending Here"**: For contiguous subarrays, the state *must* include the current element, and you track a separate global variable for the overall best answer.

---

## Next: [04-house-robber.md](./04-house-robber.md)

Deep dive into House Robber variants.

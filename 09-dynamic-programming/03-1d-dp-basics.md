# 1D DP Basics

> **Prerequisites:** [01-dp-fundamentals](./01-dp-fundamentals.md), [02-memoization-vs-tabulation](./02-memoization-vs-tabulation.md)

## Overview

1D Dynamic Programming solves problems where the state is defined by a single variable, usually an index `i`. The value `dp[i]` represents the optimal solution up to, starting at, or ending at index `i`.

## Building Intuition

1D DP is used when problems involve **sequential decision making** (processing elements left-to-right). The state compresses the history of decisions into a single optimal value at position `i`.

**Common Patterns:**
- **Constant Lookback (Fibonacci)**: `dp[i]` depends on a fixed number of previous states (e.g., `dp[i-1]` and `dp[i-2]`). easily space-optimized to $O(1)$.
- **Take/Skip**: Decide whether to include the current element or skip it.
- **Best Ending Here (Kadane's)**: State *must* include the element at index `i` (contiguous subarrays).
- **Combinatorics**: Counting the total ways to reach a state.

**When NOT to Use 1D DP:**
- Multiple constraining variables (needs 2D DP, like Knapsack capacity).
- Need to evaluate all pairs/substrings (needs 2D DP, like Palindromes or LCS).
- Graph/Tree structures (needs specialized traversal/state).

---

## Pattern 1: Fibonacci-style (Constant Lookback)

The current state depends on a fixed number of immediately preceding states.

### Climbing Stairs
You are climbing a staircase. It takes `n` steps to reach the top. Each time you can either climb 1 or 2 steps. In how many distinct ways can you climb to the top?

**State Definition:**
Let `dp[i]` be the total number of distinct ways to reach step `i`.

**Recurrence Relation:**
To reach step `i`, you must have come from either step `i-1` (taking a 1-step) or step `i-2` (taking a 2-step).
Therefore, the total ways to reach `i` is the sum of ways to reach `i-1` and `i-2`.
$$dp[i] = dp[i-1] + dp[i-2]$$

*Base Cases:*
- $dp[0] = 1$ (1 way to stay at the ground: do nothing)
- $dp[1] = 1$ (1 way to reach the first step: take 1 step)

**Space Optimization:** 
**Top-Down (Memoization):**
```python
def climb_stairs_memo(n: int) -> int:
    memo = {}
    
    def dfs(i: int) -> int:
        if i <= 1:
            return 1
        if i in memo:
            return memo[i]
            
        memo[i] = dfs(i - 1) + dfs(i - 2)
        return memo[i]
        
    return dfs(n)
```

**Bottom-Up (Tabulation - Optimized Space):**


```python
def climb_stairs(n: int) -> int:
    """
    Time: O(n) | Space: O(1)
    """
    if n <= 1:
        return 1

    # prev2 represents dp[i-2], prev1 represents dp[i-1]
    # Starting from step 2, dp[0] = 1, dp[1] = 1
    prev2, prev1 = 1, 1

    for i in range(2, n + 1):
        # Shift the window forward
        prev2, prev1 = prev1, prev1 + prev2

    return prev1
```

### Min Cost Climbing Stairs
You are given an integer array `cost` where `cost[i]` is the cost of $i^{th}$ step. Once you pay the cost, you can climb one or two steps. You can start from step 0 or step 1. Return the minimum cost to reach the top of the floor (beyond the last element).

**State Definition:**
Let `dp[i]` be the minimum cost to *reach* step `i`.

**Recurrence Relation:**
To reach step `i`, you came from `i-1` (and paid `cost[i-1]`) OR from `i-2` (and paid `cost[i-2]`). We want the minimum of these two paths.
$$dp[i] = \min(dp[i-1] + cost[i-1], dp[i-2] + cost[i-2])$$

*Base Cases:*
- $dp[0] = 0$ (Start here for free)
- $dp[1] = 0$ (Start here for free)


**Top-Down (Memoization):**
```python
def min_cost_climbing_stairs_memo(cost: list[int]) -> int:
    memo = {}
    n = len(cost)
    
    def dfs(i: int) -> int:
        if i <= 1:
            return 0
        if i in memo:
            return memo[i]
            
        # Cost to reach step i is the min of reaching i-1 + cost[i-1] 
        # or reaching i-2 + cost[i-2]
        memo[i] = min(dfs(i - 1) + cost[i - 1], dfs(i - 2) + cost[i - 2])
        return memo[i]
        
    return dfs(n)
```

**Bottom-Up (Tabulation - Optimized Space):**
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
        # Shift variables
        prev2, prev1 = prev1, min(prev1 + cost[i-1], prev2 + cost[i-2])

    return prev1
```

---

## Pattern 2: Take or Skip (Include / Exclude)

At each position, you decide whether including the current element yields a better result than excluding it, often constrained by rules (e.g., cannot take adjacent elements).

### House Robber
You are a robber planning to rob houses. `nums[i]` is the amount of money in the $i^{th}$ house. You cannot rob adjacent houses. Return the maximum amount of money you can rob.

**State Definition:**
Let `dp[i]` be the maximum profit you can rob from the first `i` houses.

**Recurrence Relation:**
At house `i`, you have two choices:
1. **Skip it**: Keep the max profit up to house `i-1`. ($dp[i-1]$)
2. **Take it**: Add its value to the max profit up to house `i-2` (since you can't rob `i-1`). ($dp[i-2] + nums[i]$)

We take the maximum of these choices:
$$dp[i] = \max(dp[i-1], dp[i-2] + nums[i])$$

**Visual: State Transitions**
`nums = [2, 7, 9, 3, 1]`

| i | House Value | Choice 1: Skip (take `dp[i-1]`) | Choice 2: Take (`dp[i-2] + val`) | Best `dp[i]` |
| :--- | :--- | :--- | :--- | :--- |
| **0** | `2` | 0 | 0 + 2 | **2** |
| **1** | `7` | 2 | 0 + 7 | **7** |
| **2** | `9` | 7 | 2 + 9 | **11** |
| **3** | `3` | 11 | 7 + 3 | **11** |
| **4** | `1` | 11 | 11 + 1 | **12** |


**Top-Down (Memoization):**
```python
def rob_memo(nums: list[int]) -> int:
    memo = {}
    
    def dfs(i: int) -> int:
        if i < 0:
            return 0
        if i in memo:
            return memo[i]
            
        # Max of skipping this house or taking this house + house i-2
        memo[i] = max(dfs(i - 1), dfs(i - 2) + nums[i])
        return memo[i]
        
    return dfs(len(nums) - 1)
```

**Bottom-Up (Tabulation - Optimized Space):**
```python
def rob(nums: list[int]) -> int:
    """
    Time: O(n) | Space: O(1)
    """
    # rob1 = dp[i-2], rob2 = dp[i-1]
    rob1, rob2 = 0, 0

    for amount in nums:
        # dp[i] = max(skip, take)
        # Shift variables forward
        rob1, rob2 = rob2, max(rob2, rob1 + amount)

    return rob2
```

### Delete and Earn
**Problem Statement:** You are given an integer array `nums`. You want to maximize the number of points you get by performing the following operation any number of times: Pick any `nums[i]` and delete it to earn `nums[i]` points. Afterwards, you must delete every element equal to `nums[i] - 1` and every element equal to `nums[i] + 1`. Return the maximum number of points you can earn by applying the above operation some number of times.

**Insight:** This is House Robber in disguise! If we transform the input into an array where the index is the number itself and the value is the total sum of that number in `nums`, the rule "deleting `x-1` and `x+1`" is identical to the House Robber rule "cannot rob adjacent houses".


**Top-Down (Memoization):**
```python
def delete_and_earn_memo(nums: list[int]) -> int:
    from collections import Counter
    if not nums:
        return 0
        
    counts = Counter(nums)
    # Get unique sorted keys to avoid iterating over empty values
    unique_nums = sorted(counts.keys())
    memo = {}
    
    def dfs(i: int) -> int:
        if i < 0:
            return 0
        if i in memo:
            return memo[i]
            
        num = unique_nums[i]
        earn = num * counts[num]
        
        # If previous number is num - 1, we can't take it
        if i > 0 and unique_nums[i - 1] == num - 1:
            memo[i] = max(dfs(i - 1), dfs(i - 2) + earn)
        else:
            # We can take both since they aren't adjacent in value
            memo[i] = dfs(i - 1) + earn
            
        return memo[i]
        
    return dfs(len(unique_nums) - 1)
```

**Bottom-Up (Tabulation with Array):**
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
        rob1, rob2 = rob2, max(rob2, rob1 + amount)

    return rob2
```

*(Note: If `max(nums)` is extremely large and the array is sparse, you can use a Hash Map to count sums, sort the unique keys, and adjust the transition logic to check if `keys[i] == keys[i-1] + 1`.)*

---

## Pattern 3: "Best Ending Here" (Kadane's)

Used for contiguous subarrays. The state `dp[i]` represents the optimal subarray that *must end exactly at index `i`*.

### Maximum Subarray
**Problem Statement:** Given an integer array `nums`, find the subarray with the largest sum, and return its sum.

**State Definition:**
Let `dp[i]` be the maximum subarray sum ending at index `i`.

**Recurrence Relation:**
At index `i`, you have a choice:
1. **Extend the previous best subarray** ending at `i-1` by adding `nums[i]`. ($dp[i-1] + nums[i]$)
2. **Start a completely new subarray** at `i`. ($nums[i]$)

You choose the maximum of these two.
$$dp[i] = \max(nums[i], dp[i-1] + nums[i])$$

Note that `dp[i]` only represents the best subarray *ending* at `i`. The true global maximum subarray could end anywhere, so we must also track the global maximum found across all `dp` states.


**Top-Down (Memoization):**
Note: Kadane's algorithm is usually written bottom-up because it's simpler, but the top-down equivalent helps understand the state transition.
```python
def max_subarray_memo(nums: list[int]) -> int:
    # memo[i] stores the max subarray sum ending exactly at index i
    memo = {}
    
    def dfs(i: int) -> int:
        if i == 0:
            return nums[0]
        if i in memo:
            return memo[i]
            
        # Either extend the previous subarray or start a new one here
        memo[i] = max(nums[i], dfs(i - 1) + nums[i])
        return memo[i]
        
    # We must compute all states to find the global max
    max_sum = float('-inf')
    for i in range(len(nums)):
        max_sum = max(max_sum, dfs(i))
        
    return int(max_sum)
```

**Bottom-Up (Kadane's Algorithm):**
```python
def max_subarray(nums: list[int]) -> int:
    """
    Time: O(n) | Space: O(1)
    """
    # Initialize both to the first element
    # curr_sum represents dp[i]
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
**Problem Statement:** Given an integer array `nums`, find a subarray that has the largest product, and return the product. The test cases are generated so that the answer will fit in a 32-bit integer.

**Insight:** Because multiplying two negative numbers yields a positive number, a very small (negative) product can instantly become the largest product if the current number is negative. Therefore, we must track *both* the **maximum** and **minimum** products ending at `i`.


**Top-Down (Memoization):**
```python
def max_product_memo(nums: list[int]) -> int:
    # Need to track both max and min ending at i
    # memo[i] = (max_ending_here, min_ending_here)
    memo = {}
    
    def dfs(i: int) -> tuple[int, int]:
        if i == 0:
            return (nums[0], nums[0])
        if i in memo:
            return memo[i]
            
        prev_max, prev_min = dfs(i - 1)
        num = nums[i]
        
        curr_max = max(num, prev_max * num, prev_min * num)
        curr_min = min(num, prev_max * num, prev_min * num)
        
        memo[i] = (curr_max, curr_min)
        return memo[i]
        
    res = float('-inf')
    for i in range(len(nums)):
        res = max(res, dfs(i)[0])
        
    return int(res)
```

**Bottom-Up (Tabulation - Optimized Space):**
```python
def max_product(nums: list[int]) -> int:
    """
    Time: O(n) | Space: O(1)
    """
    if not nums:
        return 0

    # res stores the global maximum
    res = nums[0]
    
    # curr_min and curr_max store the min/max product of subarrays ending at index i
    curr_min, curr_max = nums[0], nums[0]

    for i in range(1, len(nums)):
        num = nums[i]

        # We must store the previous curr_max in a temp variable because we
        # need to use its value to calculate the new curr_min, before it is overwritten.
        # Candidates for new max/min:
        # 1. Start a new subarray here: `num`
        # 2. Extend the max product subarray: `curr_max * num`
        # 3. Extend the min product subarray (critical when num < 0): `curr_min * num`
        
        temp_max = max(num, curr_max * num, curr_min * num)
        curr_min = min(num, curr_max * num, curr_min * num)
        curr_max = temp_max

        res = max(res, curr_max)

    return res
```

---

## Pattern 4: Combinatorics (Counting Ways)

Counting the total number of ways to reach a state.

### Decode Ways
**Problem Statement:** A message containing letters from A-Z can be encoded into numbers using the following mapping: 'A' -> "1", 'B' -> "2", ..., 'Z' -> "26". To decode an encoded message, all the digits must be grouped then mapped back into letters using the reverse of the mapping above (there may be multiple ways). For example, "11106" can be mapped into: "AAJF" with the grouping (1 1 10 6), "KJF" with the grouping (11 10 6). Note that the grouping (1 11 06) is invalid because "06" cannot be mapped into 'F' since "6" is different from "06". Given a string s containing only digits, return the number of ways to decode it.

**State Definition:**
Let `dp[i]` be the number of ways to decode the prefix of `s` of length `i` (i.e., `s[0...i-1]`).

**Recurrence Relation:**
To find `dp[i]`:
- If the single character `s[i-1]` is valid ('1'-'9'), we can append it to all decodings of length `i-1`. Add `dp[i-1]`.
- If the two characters ending at `s[i-1]` (i.e., `s[i-2:i]`) form a valid number ('10'-'26'), we can append it to all decodings of length `i-2`. Add `dp[i-2]`.


**Top-Down (Memoization):**
```python
def num_decodings_memo(s: str) -> int:
    memo = {}
    
    def dfs(i: int) -> int:
        # Base case: empty string has 1 way to decode
        if i == len(s):
            return 1
        # Invalid decoding starts with '0'
        if s[i] == '0':
            return 0
        if i in memo:
            return memo[i]
            
        # Single digit decode
        res = dfs(i + 1)
        
        # Two digit decode
        if i + 1 < len(s) and (s[i] == '1' or (s[i] == '2' and s[i + 1] in '0123456')):
            res += dfs(i + 2)
            
        memo[i] = res
        return res
        
    return dfs(0)
```

**Bottom-Up (Tabulation - Optimized Space):**
```python
def num_decodings(s: str) -> int:
    """
    Time: O(n) | Space: O(1)
    """
    if not s or s[0] == '0':
        return 0

    # prev2 = dp[i-2], prev1 = dp[i-1]
    # Length 0 has 1 way (empty string), Length 1 has 1 way (we checked it's not '0')
    prev2, prev1 = 1, 1

    for i in range(2, len(s) + 1):
        curr = 0

        # Check single digit decode (1-9)
        if s[i-1] != '0':
            curr += prev1

        # Check two digit decode (10-26)
        two_digit = int(s[i-2:i])
        if 10 <= two_digit <= 26:
            curr += prev2

        # Shift variables
        prev2, prev1 = prev1, curr

    return prev1
```

---

## Pattern 5: Unbounded Lookback

Sometimes `dp[i]` depends on all previous states `dp[0]...dp[i-1]`, not just a constant number. This means $O(n)$ space is required, and time complexity is usually $O(n^2)$ or $O(n\sqrt{n})$.

### Perfect Squares
**Problem Statement:** Given an integer `n`, return the least number of perfect square numbers that sum to `n`. A perfect square is an integer that is the square of an integer; in other words, it is the product of some integer with itself. For example, 1, 4, 9, and 16 are perfect squares while 3 and 11 are not.

**State Definition:**
Let `dp[i]` be the minimum number of perfect squares that sum to `i`.

**Recurrence Relation:**
To find `dp[i]`, we can try subtracting every valid perfect square $j^2 \le i$. The answer is 1 (for the square we just subtracted) plus the optimal answer for the remainder $i - j^2$. We want the minimum over all valid $j$.
$$dp[i] = 1 + \min_{j^2 \le i}(dp[i - j^2])$$


**Top-Down (Memoization):**
```python
import math

def num_squares_memo(n: int) -> int:
    memo = {}
    
    def dfs(target: int) -> int:
        if target == 0:
            return 0
        if target in memo:
            return memo[target]
            
        res = float('inf')
        j = 1
        while j * j <= target:
            res = min(res, 1 + dfs(target - j * j))
            j += 1
            
        memo[target] = res
        return res
        
    return dfs(n)
```

**Bottom-Up (Tabulation):**
```python
def num_squares(n: int) -> int:
    """
    Time: O(n * sqrt(n)) | Space: O(n)
    """
    # Initialize with infinity for minimum problems
    dp = [float('inf')] * (n + 1)
    dp[0] = 0  # Base case: 0 requires 0 squares

    for target in range(1, n + 1):
        # Check all possible squares less than or equal to current target
        j = 1
        while j * j <= target:
            dp[target] = min(dp[target], 1 + dp[target - j * j])
            j += 1

    return dp[n]
```

---



## Progressive Problems

To master 1D DP, practice these problems in this recommended order:

1. **Fibonacci-style**:
   - [Climbing Stairs](https://leetcode.com/problems/climbing-stairs/) (Easy)
   - [Min Cost Climbing Stairs](https://leetcode.com/problems/min-cost-climbing-stairs/) (Easy)
   - [N-th Tribonacci Number](https://leetcode.com/problems/n-th-tribonacci-number/) (Easy)
2. **Take or Skip**:
   - [House Robber](https://leetcode.com/problems/house-robber/) (Medium)
   - [House Robber II](https://leetcode.com/problems/house-robber-ii/) (Medium)
   - [Delete and Earn](https://leetcode.com/problems/delete-and-earn/) (Medium)
3. **Best Ending Here (Kadane's)**:
   - [Maximum Subarray](https://leetcode.com/problems/maximum-subarray/) (Medium)
   - [Maximum Product Subarray](https://leetcode.com/problems/maximum-product-subarray/) (Medium)
4. **Combinatorics / Unbounded Lookback**:
   - [Decode Ways](https://leetcode.com/problems/decode-ways/) (Medium)
   - [Perfect Squares](https://leetcode.com/problems/perfect-squares/) (Medium)
   - [Word Break](https://leetcode.com/problems/word-break/) (Medium) - *Transitioning to boolean DP*

## Key Takeaways

1. **State Definition is King**: Clearly define what `dp[i]` represents in plain English (e.g., "The max profit robbing houses up to index i").
2. **Find the Recurrence**: Ask: "If I already knew the answers for smaller subproblems, how would I calculate the answer for the current step?"
3. **Check Space Optimization**: If the recurrence only looks at `dp[i-1]` and `dp[i-2]`, use variables for $O(1)$ space.
4. **Beware "Best Ending Here"**: For contiguous subarrays, the state *must* include the current element, and you track a separate global variable for the overall best answer.

---

## Next: [04-house-robber.md](./04-house-robber.md)

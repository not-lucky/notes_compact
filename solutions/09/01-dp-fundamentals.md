# Dynamic Programming

## Practice Problems

### 1. Climbing Stairs
**Difficulty:** Easy
**Concept:** Fibonacci

```python
def climb_stairs(n: int) -> int:
    """
    Count ways to reach nth stair (1 or 2 steps).
    Time: O(n)
    Space: O(1)
    """
    if n <= 2: return n
    prev2, prev1 = 1, 2
    for i in range(3, n + 1):
        curr = prev1 + prev2
        prev2, prev1 = prev1, curr
    return prev1
```

### 2. House Robber
**Difficulty:** Medium
**Concept:** Take/skip

```python
from typing import List

def rob(nums: List[int]) -> int:
    """
    Maximum sum of non-adjacent elements.
    Time: O(n)
    Space: O(1)
    """
    if not nums: return 0
    prev2, prev1 = 0, 0
    for n in nums:
        curr = max(prev1, prev2 + n)
        prev2, prev1 = prev1, curr
    return prev1
```

### 3. Longest Increasing Subsequence
**Difficulty:** Medium
**Concept:** DP + Binary Search

```python
import bisect

def length_of_lis(nums: List[int]) -> int:
    """
    Finds the length of the longest increasing subsequence.
    Time: O(n log n)
    Space: O(n)
    """
    tails = []
    for x in nums:
        idx = bisect.bisect_left(tails, x)
        if idx == len(tails):
            tails.append(x)
        else:
            tails[idx] = x
    return len(tails)
```

### 4. Coin Change
**Difficulty:** Medium
**Concept:** Unbounded knapsack

```python
def coin_change(coins: List[int], amount: int) -> int:
    """
    Minimum coins to reach amount.
    Time: O(amount * n_coins)
    Space: O(amount)
    """
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    for a in range(1, amount + 1):
        for c in coins:
            if a - c >= 0:
                dp[a] = min(dp[a], 1 + dp[a - c])
    return dp[amount] if dp[amount] != float('inf') else -1
```

### 5. Longest Common Subsequence
**Difficulty:** Medium
**Concept:** 2D DP

```python
def longest_common_subsequence(text1: str, text2: str) -> int:
    """
    Finds length of the LCS between two strings.
    Time: O(m * n)
    Space: O(m * n)
    """
    m, n = len(text1), len(text2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i-1] == text2[j-1]:
                dp[i][j] = 1 + dp[i-1][j-1]
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    return dp[m][n]
```

### 6. Word Break
**Difficulty:** Medium
**Concept:** String DP

```python
def word_break(s: str, word_dict: List[str]) -> bool:
    """
    Checks if string can be segmented into words from dictionary.
    Time: O(n^2 * m) where m is avg word length
    Space: O(n)
    """
    words = set(word_dict)
    dp = [False] * (len(s) + 1)
    dp[0] = True
    for i in range(1, len(s) + 1):
        for j in range(i):
            if dp[j] and s[j:i] in words:
                dp[i] = True
                break
    return dp[len(s)]
```

### 7. Unique Paths
**Difficulty:** Medium
**Concept:** Grid DP

```python
def unique_paths(m: int, n: int) -> int:
    """
    Count unique paths in m x n grid.
    Time: O(m * n)
    Space: O(n)
    """
    dp = [1] * n
    for i in range(1, m):
        for j in range(1, n):
            dp[j] += dp[j - 1]
    return dp[n - 1]
```

### 8. Minimum Path Sum
**Difficulty:** Medium
**Concept:** Path optimization

```python
def min_path_sum(grid: List[List[int]]) -> int:
    """
    Finds the path with the minimum sum.
    Time: O(m * n)
    Space: O(n)
    """
    m, n = len(grid), len(grid[0])
    dp = [float('inf')] * n
    dp[0] = 0
    for i in range(m):
        for j in range(n):
            if j == 0:
                dp[j] += grid[i][j]
            else:
                dp[j] = grid[i][j] + min(dp[j], dp[j - 1])
    return dp[n - 1]
```

### 9. Edit Distance
**Difficulty:** Hard
**Concept:** String transformation

```python
def min_distance(word1: str, word2: str) -> int:
    """
    Minimum operations (insert, delete, replace) to convert word1 to word2.
    Time: O(m * n)
    Space: O(n)
    """
    m, n = len(word1), len(word2)
    dp = list(range(n + 1))
    for i in range(1, m + 1):
        prev = dp[0]
        dp[0] = i
        for j in range(1, n + 1):
            temp = dp[j]
            if word1[i-1] == word2[j-1]:
                dp[j] = prev
            else:
                dp[j] = 1 + min(dp[j], dp[j-1], prev)
            prev = temp
    return dp[n]
```

### 10. 0/1 Knapsack (Subset Sum variant)
**Difficulty:** Medium
**Concept:** Include/Exclude

```python
def can_partition(nums: List[int], target: int) -> bool:
    """
    Checks if a subset sums to target.
    Time: O(n * target)
    Space: O(target)
    """
    dp = [False] * (target + 1)
    dp[0] = True
    for n in nums:
        for t in range(target, n - 1, -1):
            dp[t] = dp[t] or dp[t - n]
    return dp[target]
```

### 11. Longest Palindromic Subsequence
**Difficulty:** Medium
**Concept:** Interval DP

```python
def longest_palindrome_subseq(s: str) -> int:
    """
    Finds the length of the longest palindromic subsequence.
    Time: O(n^2)
    Space: O(n)
    """
    n = len(s)
    dp = [0] * n
    for i in range(n - 1, -1, -1):
        new_dp = [0] * n
        new_dp[i] = 1
        for j in range(i + 1, n):
            if s[i] == s[j]:
                new_dp[j] = dp[j - 1] + 2
            else:
                new_dp[j] = max(dp[j], new_dp[j - 1])
        dp = new_dp
    return dp[n - 1]
```

### 12. Best Time to Buy and Sell Stock with Cooldown
**Difficulty:** Medium
**Concept:** State Machine DP

```python
def max_profit(prices: List[int]) -> int:
    """
    Unlimited transactions with 1-day cooldown.
    Time: O(n)
    Space: O(1)
    """
    hold, sold, rest = float('-inf'), 0, 0
    for p in prices:
        prev_sold = sold
        sold = hold + p
        hold = max(hold, rest - p)
        rest = max(rest, prev_sold)
    return max(sold, rest)
```

### 13. Burst Balloons
**Difficulty:** Hard
**Concept:** Interval DP (Reverse thinking)

```python
def max_coins(nums: List[int]) -> int:
    """
    Max coins from bursting balloons.
    Time: O(n^3)
    Space: O(n^2)
    """
    nums = [1] + nums + [1]
    n = len(nums)
    dp = [[0] * n for _ in range(n)]
    for length in range(2, n):
        for i in range(n - length):
            j = i + length
            for k in range(i + 1, j):
                dp[i][j] = max(dp[i][j],
                               dp[i][k] + dp[k][j] + nums[i] * nums[k] * nums[j])
    return dp[0][n - 1]
```

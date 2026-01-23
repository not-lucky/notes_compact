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

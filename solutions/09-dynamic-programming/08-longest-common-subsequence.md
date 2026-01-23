# Longest Common Subsequence Solutions

## Problem: Longest Common Subsequence
Given two strings `text1` and `text2`, return the length of their longest common subsequence. If there is no common subsequence, return 0.

### Constraints
- 1 <= text1.length, text2.length <= 1000
- `text1` and `text2` consist of only lowercase English characters.

### Examples
- Input: text1 = "abcde", text2 = "ace" -> Output: 3 ("ace")
- Input: text1 = "abc", text2 = "abc" -> Output: 3
- Input: text1 = "abc", text2 = "def" -> Output: 0

### Implementation

```python
def longest_common_subsequence(text1: str, text2: str) -> int:
    """
    Finds length of LCS using space-optimized 2D DP.
    Time complexity: O(m * n)
    Space complexity: O(min(m, n))
    """
    # Ensure n is the smaller length for space optimization
    if len(text1) < len(text2):
        text1, text2 = text2, text1

    m, n = len(text1), len(text2)
    dp = [0] * (n + 1)

    for i in range(1, m + 1):
        prev_diag = 0 # dp[i-1][j-1]
        for j in range(1, n + 1):
            temp = dp[j] # Save dp[i-1][j]
            if text1[i-1] == text2[j-1]:
                dp[j] = prev_diag + 1
            else:
                dp[j] = max(dp[j], dp[j-1])
            prev_diag = temp

    return dp[n]
```

## Problem: Shortest Common Supersequence
Given two strings `str1` and `str2`, return the shortest string that has both `str1` and `str2` as subsequences. If there are multiple valid strings, return any of them.

### Implementation

```python
def shortest_common_supersequence(str1: str, str2: str) -> str:
    """
    Finds the SCS by first finding the LCS and then merging.
    Time complexity: O(m * n)
    Space complexity: O(m * n)
    """
    m, n = len(str1), len(str2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if str1[i-1] == str2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])

    # Backtrack from bottom-right to build SCS
    res = []
    i, j = m, n
    while i > 0 and j > 0:
        if str1[i-1] == str2[j-1]:
            res.append(str1[i-1])
            i -= 1
            j -= 1
        elif dp[i-1][j] > dp[i][j-1]:
            res.append(str1[i-1])
            i -= 1
        else:
            res.append(str2[j-1])
            j -= 1

    # Add remaining characters
    while i > 0:
        res.append(str1[i-1])
        i -= 1
    while j > 0:
        res.append(str2[j-1])
        j -= 1

    return "".join(reversed(res))
```

# Palindrome DP Solutions

## Problem: Longest Palindromic Substring
Given a string `s`, return the longest palindromic substring in `s`.

### Constraints
- 1 <= s.length <= 1000
- `s` consists of only digits and English letters.

### Examples
- Input: s = "babad" -> Output: "bab" or "aba"
- Input: s = "cbbd" -> Output: "bb"

### Implementation

```python
def longest_palindrome_substring(s: str) -> str:
    """
    Finds longest palindromic substring using expansion around center.
    Time complexity: O(n^2)
    Space complexity: O(1)
    """
    if not s:
        return ""

    def expand(left, right):
        while left >= 0 and right < len(s) and s[left] == s[right]:
            left -= 1
            right += 1
        return s[left + 1:right]

    res = ""
    for i in range(len(s)):
        # Odd length
        p1 = expand(i, i)
        # Even length
        p2 = expand(i, i + 1)
        res = max(res, p1, p2, key=len)

    return res
```

## Problem: Longest Palindromic Subsequence
Given a string `s`, find the longest palindromic subsequence's length in `s`.

### Constraints
- 1 <= s.length <= 1000

### Implementation

```python
def longest_palindrome_subseq(s: str) -> int:
    """
    Finds length of LPS using space-optimized 2D DP.
    Time complexity: O(n^2)
    Space complexity: O(n)
    """
    n = len(s)
    dp = [0] * n

    # Base case: single character
    for i in range(n - 1, -1, -1):
        new_dp = [0] * n
        new_dp[i] = 1
        for j in range(i + 1, n):
            if s[i] == s[j]:
                new_dp[j] = dp[j-1] + 2
            else:
                new_dp[j] = max(dp[j], new_dp[j-1])
        dp = new_dp

    return dp[n-1]
```

## Problem: Palindrome Partitioning II (Min Cuts)
Given a string `s`, partition `s` such that every substring of the partition is a palindrome. Return the minimum cuts needed for a palindrome partitioning of `s`.

### Implementation

```python
def min_cut(s: str) -> int:
    """
    Minimum cuts to partition s into palindromes.
    Time complexity: O(n^2)
    Space complexity: O(n^2)
    """
    n = len(s)
    # Precompute is_palindrome table
    is_p = [[False] * n for _ in range(n)]
    for i in range(n - 1, -1, -1):
        for j in range(i, n):
            if s[i] == s[j] and (j - i <= 2 or is_p[i+1][j-1]):
                is_p[i][j] = True

    # dp[i] is the min cuts for s[:i+1]
    dp = list(range(n))
    for i in range(n):
        if is_p[0][i]:
            dp[i] = 0
        else:
            for j in range(i):
                if is_p[j+1][i]:
                    dp[i] = min(dp[i], dp[j] + 1)
    return dp[n-1]
```

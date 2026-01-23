# DP on Strings Solutions

## Problem: Distinct Subsequences
Given two strings `s` and `t`, return the number of distinct subsequences of `s` which equals `t`.

### Constraints
- 1 <= s.length, t.length <= 1000
- `s` and `t` consist of English letters.

### Implementation

```python
def num_distinct(s: str, t: str) -> int:
    """
    Counts distinct subsequences of s that match t.
    Time complexity: O(m * n)
    Space complexity: O(n)
    """
    m, n = len(s), len(t)
    # dp[j] is number of ways to form t[:j]
    dp = [0] * (n + 1)
    dp[0] = 1 # Empty t can be formed by empty subsequence of s

    for i in range(1, m + 1):
        # Iterate backwards to avoid using current row's values
        for j in range(n, 0, -1):
            if s[i-1] == t[j-1]:
                dp[j] += dp[j-1]
    return dp[n]
```

## Problem: Interleaving String
Given strings `s1`, `s2`, and `s3`, find whether `s3` is formed by an interleaving of `s1` and `s2`.

### Implementation

```python
def is_interleave(s1: str, s2: str, s3: str) -> bool:
    """
    Checks if s3 is an interleaving of s1 and s2.
    Time complexity: O(m * n)
    Space complexity: O(n)
    """
    m, n = len(s1), len(s2)
    if m + n != len(s3):
        return False

    dp = [False] * (n + 1)
    dp[0] = True

    # Initial state for first row (s1 is empty)
    for j in range(1, n + 1):
        dp[j] = dp[j-1] and s2[j-1] == s3[j-1]

    for i in range(1, m + 1):
        # Initial state for first column (s2 is empty)
        dp[0] = dp[0] and s1[i-1] == s3[i-1]
        for j in range(1, n + 1):
            # Either last char of s3 came from s1 or s2
            dp[j] = (dp[j] and s1[i-1] == s3[i+j-1]) or \
                    (dp[j-1] and s2[j-1] == s3[i+j-1])
    return dp[n]
```

## Problem: Longest Valid Parentheses
Given a string containing just the characters '(' and ')', find the length of the longest valid (well-formed) parentheses substring.

### Implementation

```python
def longest_valid_parentheses(s: str) -> int:
    """
    Finds length of longest valid parentheses substring using 1D DP.
    Time complexity: O(n)
    Space complexity: O(n)
    """
    n = len(s)
    if n < 2:
        return 0
    # dp[i] is the length of longest valid parentheses ending at i
    dp = [0] * n
    max_len = 0
    for i in range(1, n):
        if s[i] == ')':
            if s[i-1] == '(':
                dp[i] = (dp[i-2] if i >= 2 else 0) + 2
            elif i - dp[i-1] > 0 and s[i - dp[i-1] - 1] == '(':
                # Case like "(())"
                inner_val = dp[i-1]
                prev_val = dp[i - dp[i-1] - 2] if i - dp[i-1] >= 2 else 0
                dp[i] = inner_val + 2 + prev_val
            max_len = max(max_len, dp[i])
    return max_len
```

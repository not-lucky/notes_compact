# Regex Matching Solutions

## Problem: Wildcard Matching
Given an input string (`s`) and a pattern (`p`), implement wildcard pattern matching with support for '?' and '*' where:
- '?' Matches any single character.
- '*' Matches any sequence of characters (including the empty sequence).

### Examples
- Input: s = "aa", p = "*" -> Output: true
- Input: s = "cb", p = "?a" -> Output: false
- Input: s = "adceb", p = "*a*b" -> Output: true

### Implementation

```python
def is_match_wildcard(s: str, p: str) -> bool:
    """
    Wildcard matching using 2D DP.
    Time complexity: O(m * n)
    Space complexity: O(n)
    """
    m, n = len(s), len(p)
    dp = [False] * (n + 1)
    dp[0] = True

    # Initial state for empty string matching pattern with leading '*'
    for j in range(1, n + 1):
        if p[j-1] == '*':
            dp[j] = dp[j-1]
        else:
            break

    for i in range(1, m + 1):
        prev_diag = dp[0]
        dp[0] = False # Non-empty string cannot match empty pattern
        for j in range(1, n + 1):
            temp = dp[j]
            if p[j-1] == '*':
                # dp[j] is dp[i-1][j] (match 1+ chars), dp[j-1] is dp[i][j-1] (match 0 chars)
                dp[j] = dp[j] or dp[j-1]
            elif p[j-1] == '?' or s[i-1] == p[j-1]:
                dp[j] = prev_diag
            else:
                dp[j] = False
            prev_diag = temp
    return dp[n]
```

## Problem: Regular Expression Matching
Given an input string `s` and a pattern `p`, implement regular expression matching with support for '.' and '*' where:
- '.' Matches any single character.
- '*' Matches zero or more of the preceding element.

### Examples
- Input: s = "aa", p = "a*" -> Output: true
- Input: s = "ab", p = ".*" -> Output: true
- Input: s = "aab", p = "c*a*b" -> Output: true

### Implementation

```python
def is_match_regex(s: str, p: str) -> bool:
    """
    Regex matching using 2D DP.
    Time complexity: O(m * n)
    Space complexity: O(m * n)
    """
    m, n = len(s), len(p)
    dp = [[False] * (n + 1) for _ in range(m + 1)]
    dp[0][0] = True

    # Handle patterns like a* or a*b* matching empty string
    for j in range(2, n + 1):
        if p[j-1] == '*':
            dp[0][j] = dp[0][j-2]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if p[j-1] == '*':
                # Case 1: Match 0 of preceding char
                dp[i][j] = dp[i][j-2]
                # Case 2: Match 1+ of preceding char (if it matches s[i-1])
                if p[j-2] == '.' or p[j-2] == s[i-1]:
                    dp[i][j] = dp[i][j] or dp[i-1][j]
            elif p[j-1] == '.' or p[j-1] == s[i-1]:
                dp[i][j] = dp[i-1][j-1]

    return dp[m][n]
```

# String Matching

## Practice Problems

### 1. Implement strStr()
**Difficulty:** Easy
**Pattern:** Brute force or KMP

```python
def str_str(haystack: str, needle: str) -> int:
    """
    Time: O(n * m)
    Space: O(1)
    """
    if not needle: return 0
    return haystack.find(needle)
```

### 2. Repeated Substring Pattern
**Difficulty:** Easy
**Pattern:** Pattern matching

```python
def repeated_substring_pattern(s: str) -> bool:
    """
    If s has repeated substring, it will be found in (s+s)[1:-1].
    Time: O(n)
    Space: O(n)
    """
    return s in (s + s)[1:-1]
```

### 3. Wildcard Matching
**Difficulty:** Hard
**Pattern:** DP

```python
def is_match(s: str, p: str) -> bool:
    """
    Time: O(n * m)
    Space: O(n * m)
    """
    n, m = len(s), len(p)
    dp = [[False] * (m + 1) for _ in range(n + 1)]
    dp[0][0] = True

    for j in range(1, m + 1):
        if p[j-1] == '*':
            dp[0][j] = dp[0][j-1]

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if p[j-1] == '*':
                dp[i][j] = dp[i-1][j] or dp[i][j-1]
            elif p[j-1] == '?' or s[i-1] == p[j-1]:
                dp[i][j] = dp[i-1][j-1]

    return dp[n][m]
```

### 4. Regular Expression Matching
**Difficulty:** Hard
**Pattern:** DP

```python
def is_match_regex(s: str, p: str) -> bool:
    """
    Time: O(n * m)
    Space: O(n * m)
    """
    n, m = len(s), len(p)
    dp = [[False] * (m + 1) for _ in range(n + 1)]
    dp[0][0] = True

    for j in range(2, m + 1):
        if p[j-1] == '*':
            dp[0][j] = dp[0][j-2]

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if p[j-1] == '*':
                if p[j-2] == '.' or p[j-2] == s[i-1]:
                    dp[i][j] = dp[i][j-2] or dp[i-1][j]
                else:
                    dp[i][j] = dp[i][j-2]
            elif p[j-1] == '.' or s[i-1] == p[j-1]:
                dp[i][j] = dp[i-1][j-1]

    return dp[n][m]
```

### 5. Shortest Palindrome
**Difficulty:** Hard
**Pattern:** KMP prefix function

```python
def shortest_palindrome(s: str) -> str:
    """
    Time: O(n)
    Space: O(n)
    """
    rev_s = s[::-1]
    new_s = s + "#" + rev_s
    n = len(new_s)
    lps = [0] * n
    for i in range(1, n):
        j = lps[i-1]
        while j > 0 and new_s[i] != new_s[j]:
            j = lps[j-1]
        if new_s[i] == new_s[j]:
            j += 1
        lps[i] = j
    return rev_s[:len(s) - lps[-1]] + s
```

### 6. Longest Happy Prefix
**Difficulty:** Hard
**Pattern:** KMP LPS

```python
def longest_prefix(s: str) -> str:
    """
    Time: O(n)
    Space: O(n)
    """
    n = len(s)
    lps = [0] * n
    for i in range(1, n):
        j = lps[i-1]
        while j > 0 and s[i] != s[j]:
            j = lps[j-1]
        if s[i] == s[j]:
            j += 1
        lps[i] = j
    return s[:lps[-1]]
```

### 7. Find All Anagrams
**Difficulty:** Medium
**Pattern:** Sliding window + hash

```python
from collections import Counter

def find_anagrams(s: str, p: str) -> list[int]:
    """
    Time: O(n)
    Space: O(1)
    """
    if len(p) > len(s): return []
    p_cnt = Counter(p)
    s_cnt = Counter(s[:len(p)])
    res = []
    if s_cnt == p_cnt: res.append(0)

    for i in range(len(p), len(s)):
        s_cnt[s[i]] += 1
        s_cnt[s[i-len(p)]] -= 1
        if s_cnt[s[i-len(p)]] == 0:
            del s_cnt[s[i-len(p)]]
        if s_cnt == p_cnt:
            res.append(i - len(p) + 1)
    return res
```

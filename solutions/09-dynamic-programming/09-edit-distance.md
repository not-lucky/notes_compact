# Edit Distance Solutions

## Problem: Edit Distance
Given two strings `word1` and `word2`, return the minimum number of operations required to convert `word1` to `word2`. You have the following three operations permitted on a word:
1. Insert a character
2. Delete a character
3. Replace a character

### Constraints
- 0 <= word1.length, word2.length <= 500
- `word1` and `word2` consist of lowercase English letters.

### Examples
- Input: word1 = "horse", word2 = "ros" -> Output: 3
- Input: word1 = "intention", word2 = "execution" -> Output: 5

### Implementation

```python
def min_distance(word1: str, word2: str) -> int:
    """
    Finds the Levenshtein distance between two words.
    Time complexity: O(m * n)
    Space complexity: O(n)
    """
    m, n = len(word1), len(word2)
    # Ensure n is the smaller dimension for space optimization
    if m < n:
        word1, word2 = word2, word1
        m, n = n, m

    # dp[j] is the distance between word1[0:i] and word2[0:j]
    dp = list(range(n + 1))

    for i in range(1, m + 1):
        prev_diag = dp[0] # dp[i-1][j-1]
        dp[0] = i # Distance from word1[0:i] to ""
        for j in range(1, n + 1):
            temp = dp[j] # Save dp[i-1][j]
            if word1[i-1] == word2[j-1]:
                dp[j] = prev_diag
            else:
                # 1 + min(delete, insert, replace)
                dp[j] = 1 + min(dp[j], dp[j-1], prev_diag)
            prev_diag = temp
    return dp[n]
```

## Problem: One Edit Distance
Given two strings `s` and `t`, return `true` if they are both one edit distance apart, otherwise return `false`.

### Implementation

```python
def is_one_edit_distance(s: str, t: str) -> bool:
    """
    Checks if s and t are exactly one edit apart.
    Time complexity: O(n)
    Space complexity: O(1)
    """
    ns, nt = len(s), len(t)
    if ns > nt:
        return is_one_edit_distance(t, s)

    if nt - ns > 1:
        return False

    for i in range(ns):
        if s[i] != t[i]:
            if ns == nt:
                # Must be a replacement
                return s[i+1:] == t[i+1:]
            else:
                # Must be an insertion into s
                return s[i:] == t[i+1:]

    # All characters match, nt must be ns + 1
    return ns + 1 == nt
```

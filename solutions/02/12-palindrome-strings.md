# Palindrome Strings

## Practice Problems

### 1. Valid Palindrome
**Difficulty:** Easy
**Technique:** Two pointers

```python
def is_palindrome(s: str) -> bool:
    """
    Time: O(n)
    Space: O(1)
    """
    l, r = 0, len(s) - 1
    while l < r:
        if not s[l].isalnum(): l += 1
        elif not s[r].isalnum(): r -= 1
        else:
            if s[l].lower() != s[r].lower(): return False
            l += 1; r -= 1
    return True
```

### 2. Valid Palindrome II
**Difficulty:** Easy
**Technique:** Two pointers + try both

```python
def valid_palindrome_ii(s: str) -> bool:
    """
    Time: O(n)
    Space: O(1)
    """
    def check(l, r):
        while l < r:
            if s[l] != s[r]: return False
            l += 1; r -= 1
        return True

    l, r = 0, len(s) - 1
    while l < r:
        if s[l] != s[r]:
            return check(l+1, r) or check(l, r-1)
        l += 1; r -= 1
    return True
```

### 3. Longest Palindromic Substring
**Difficulty:** Medium
**Technique:** Expand from center

```python
def longest_palindrome(s: str) -> str:
    """
    Time: O(n^2)
    Space: O(1)
    """
    def expand(l, r):
        while l >= 0 and r < len(s) and s[l] == s[r]:
            l -= 1; r += 1
        return s[l+1:r]

    res = ""
    for i in range(len(s)):
        res = max(res, expand(i, i), expand(i, i+1), key=len)
    return res
```

### 4. Palindromic Substrings
**Difficulty:** Medium
**Technique:** Count with expansion

```python
def count_substrings(s: str) -> int:
    """
    Time: O(n^2)
    Space: O(1)
    """
    def count_expand(l, r):
        cnt = 0
        while l >= 0 and r < len(s) and s[l] == s[r]:
            cnt += 1
            l -= 1; r += 1
        return cnt

    res = 0
    for i in range(len(s)):
        res += count_expand(i, i) + count_expand(i, i+1)
    return res
```

### 5. Longest Palindromic Subsequence
**Difficulty:** Medium
**Technique:** DP

```python
def longest_palindrome_subseq(s: str) -> int:
    """
    Time: O(n^2)
    Space: O(n^2)
    """
    n = len(s)
    dp = [[0] * n for _ in range(n)]
    for i in range(n-1, -1, -1):
        dp[i][i] = 1
        for j in range(i+1, n):
            if s[i] == s[j]:
                dp[i][j] = dp[i+1][j-1] + 2
            else:
                dp[i][j] = max(dp[i+1][j], dp[i][j-1])
    return dp[0][n-1]
```

### 6. Palindrome Partitioning
**Difficulty:** Medium
**Technique:** Backtracking

```python
def partition(s: str) -> list[list[str]]:
    """
    Time: O(n * 2^n)
    Space: O(n)
    """
    res = []
    def backtrack(start, path):
        if start == len(s):
            res.append(path[:])
            return
        for end in range(start + 1, len(s) + 1):
            sub = s[start:end]
            if sub == sub[::-1]:
                path.append(sub)
                backtrack(end, path)
                path.pop()
    backtrack(0, [])
    return res
```

### 7. Palindrome Partitioning II
**Difficulty:** Hard
**Technique:** DP min cuts

```python
def min_cut(s: str) -> int:
    """
    Time: O(n^2)
    Space: O(n^2)
    """
    n = len(s)
    pal = [[False] * n for _ in range(n)]
    for i in range(n-1, -1, -1):
        for j in range(i, n):
            if s[i] == s[j] and (j - i < 2 or pal[i+1][j-1]):
                pal[i][j] = True

    cuts = [i for i in range(n)]
    for i in range(n):
        if pal[0][i]:
            cuts[i] = 0
        else:
            for j in range(i):
                if pal[j+1][i]:
                    cuts[i] = min(cuts[i], cuts[j] + 1)
    return cuts[n-1]
```

### 8. Shortest Palindrome
**Difficulty:** Hard
**Technique:** KMP/hashing

```python
def shortest_palindrome(s: str) -> str:
    """
    Time: O(n)
    Space: O(n)
    """
    rev = s[::-1]
    new_s = s + "#" + rev
    lps = [0] * len(new_s)
    for i in range(1, len(new_s)):
        j = lps[i-1]
        while j > 0 and new_s[i] != new_s[j]:
            j = lps[j-1]
        if new_s[i] == new_s[j]:
            j += 1
        lps[i] = j
    return rev[:len(s) - lps[-1]] + s
```

# String Matching - Solutions

## Practice Problems

### 1. Implement strStr()
**Problem Statement**: Given two strings `needle` and `haystack`, return the index of the first occurrence of `needle` in `haystack`, or `-1` if `needle` is not part of `haystack`.

**Optimal Python Solution**:
```python
def strStr(haystack: str, needle: str) -> int:
    # Python's built-in 'find' is highly optimized (usually Boyer-Moore or similar)
    return haystack.find(needle)

# For educational purposes, KMP implementation:
def strStr_kmp(haystack: str, needle: str) -> int:
    if not needle: return 0

    # 1. Build LPS array
    lps = [0] * len(needle)
    prevLPS, i = 0, 1
    while i < len(needle):
        if needle[i] == needle[prevLPS]:
            lps[i] = prevLPS + 1
            prevLPS += 1
            i += 1
        elif prevLPS == 0:
            lps[i] = 0
            i += 1
        else:
            prevLPS = lps[prevLPS - 1]

    # 2. Match
    i = 0 # ptr for haystack
    j = 0 # ptr for needle
    while i < len(haystack):
        if haystack[i] == needle[j]:
            i, j = i + 1, j + 1
        else:
            if j == 0:
                i += 1
            else:
                j = lps[j - 1]

        if j == len(needle):
            return i - len(needle)

    return -1
```

**Explanation**:
KMP (Knuth-Morris-Pratt) avoids redundant comparisons by precomputing a "Longest Prefix Suffix" (LPS) array for the pattern. When a mismatch occurs, we use the LPS array to determine how many characters we can skip without missing a potential match.

**Complexity Analysis**:
- **Time Complexity**: O(n + m), where n is length of haystack and m is length of needle. Building LPS takes O(m), matching takes O(n).
- **Space Complexity**: O(m) to store the LPS array.

---

### 2. Repeated Substring Pattern
**Problem Statement**: Given a string `s`, check if it can be constructed by taking a substring of it and appending multiple copies of the substring together.

**Optimal Python Solution**:
```python
def repeatedSubstringPattern(s: str) -> bool:
    # Trick: If s contains a repeated pattern, then s + s (excluding the very first
    # and very last character) must contain s.
    return s in (s + s)[1:-1]
```

**Explanation**:
If `s` is made of $n$ copies of substring $P$, then $s = P \times n$. $s+s = P \times 2n$. By removing the first and last characters, we remove one $P$ from each end (or parts of it), leaving $2n-2$ copies of $P$ plus fragments. If $n \ge 2$, we still have at least $n$ copies of $P$ in the middle, allowing us to find $s$.

**Complexity Analysis**:
- **Time Complexity**: O(n), due to the string search `in`.
- **Space Complexity**: O(n) to create the `s + s` string.

---

### 3. Wildcard Matching
**Problem Statement**: Implement wildcard pattern matching with support for `'?'` (matches any single character) and `'*'` (matches any sequence of characters including empty).

**Optimal Python Solution**:
```python
def isMatch(s: str, p: str) -> bool:
    m, n = len(s), len(p)
    # dp[i][j] means s[:i] matches p[:j]
    dp = [[False] * (n + 1) for _ in range(m + 1)]
    dp[0][0] = True

    # Base case for pattern with '*'
    for j in range(1, n + 1):
        if p[j-1] == '*':
            dp[0][j] = dp[0][j-1]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if p[j-1] == '*':
                # '*' matches empty string (dp[i][j-1])
                # or '*' matches s[i-1] (dp[i-1][j])
                dp[i][j] = dp[i][j-1] or dp[i-1][j]
            elif p[j-1] == '?' or s[i-1] == p[j-1]:
                dp[i][j] = dp[i-1][j-1]

    return dp[m][n]
```

**Explanation**:
We use Dynamic Programming. The most complex part is handling `*`. A `*` can either represent an empty string (look at the result without using this `*`) or it can represent one or more characters from `s` (look at the result for the previous character in `s` using this same `*`).

**Complexity Analysis**:
- **Time Complexity**: O(m * n).
- **Space Complexity**: O(m * n).

---

### 4. Regular Expression Matching
**Problem Statement**: Implement regular expression matching with support for `'.'` and `'*'`. `'.'` matches any single character. `'*'` matches zero or more of the preceding element.

**Optimal Python Solution**:
```python
def isMatch(s: str, p: str) -> bool:
    memo = {}

    def dp(i, j):
        if (i, j) in memo: return memo[(i, j)]
        if j == len(p): return i == len(s)

        first_match = i < len(s) and p[j] in {s[i], '.'}

        if j + 1 < len(p) and p[j+1] == '*':
            # Case 1: zero occurrences of p[j] (skip p[j*])
            # Case 2: one or more occurrences (if first_match, move to s[i+1])
            res = dp(i, j + 2) or (first_match and dp(i + 1, j))
        else:
            res = first_match and dp(i + 1, j + 1)

        memo[(i, j)] = res
        return res

    return dp(0, 0)
```

**Explanation**:
The `'*'` in regex is different from wildcard; it applies to the *preceding* character. We use recursion with memoization. If we see a character followed by `*`, we either skip both (0 occurrences) or, if the current character matches, we consume one character of `s` and keep the pattern the same to match more.

**Complexity Analysis**:
- **Time Complexity**: O(m * n).
- **Space Complexity**: O(m * n).

---

### 5. Shortest Palindrome
**Problem Statement**: You are given a string `s`. You can convert `s` to a palindrome by adding characters in front of it. Find and return the shortest palindrome you can find by performing this transformation.

**Optimal Python Solution**:
```python
def shortestPalindrome(s: str) -> str:
    # We need to find the longest prefix of s that is already a palindrome.
    # We can use the KMP LPS trick.
    # Create string: s + "#" + reversed_s
    rev_s = s[::-1]
    new_s = s + "#" + rev_s

    lps = [0] * len(new_s)
    for i in range(1, len(new_s)):
        j = lps[i-1]
        while j > 0 and new_s[i] != new_s[j]:
            j = lps[j-1]
        if new_s[i] == new_s[j]:
            j += 1
        lps[i] = j

    # The last value in lps tells us the length of the longest prefix of s
    # that is a suffix of rev_s (meaning it's a palindrome).
    palindrome_prefix_len = lps[-1]
    return rev_s[:len(s) - palindrome_prefix_len] + s
```

**Explanation**:
To make the shortest palindrome by adding to the front, we want to keep as much of the existing string as possible as the "center" or "end". This means finding the longest prefix of `s` that is already a palindrome. By using KMP's LPS array on `s + # + reverse(s)`, the last element of the array tells us exactly how many characters from the start of `s` match the end of `reverse(s)`.

**Complexity Analysis**:
- **Time Complexity**: O(n).
- **Space Complexity**: O(n).

---

### 6. Longest Happy Prefix
**Problem Statement**: A string is called a happy prefix if is a non-empty prefix which is also a suffix (excluding itself). Given a string `s`, return the longest happy prefix of `s`.

**Optimal Python Solution**:
```python
def longestPrefix(s: str) -> str:
    # This is exactly what the LPS array in KMP computes for the last index.
    lps = [0] * len(s)
    j = 0
    for i in range(1, len(s)):
        while j > 0 and s[i] != s[j]:
            j = lps[j-1]
        if s[i] == s[j]:
            j += 1
        lps[i] = j

    return s[:lps[-1]]
```

**Complexity Analysis**:
- **Time Complexity**: O(n).
- **Space Complexity**: O(n).

---

### 7. Find All Anagrams
**Problem Statement**: Find all start indices of `p`'s anagrams in `s`.

**Optimal Python Solution**:
```python
from collections import Counter

def findAnagrams(s: str, p: str) -> list[int]:
    ns, np = len(s), len(p)
    if ns < np: return []

    p_cnt = Counter(p)
    s_cnt = Counter(s[:np])
    res = []

    if p_cnt == s_cnt: res.append(0)

    for i in range(np, ns):
        s_cnt[s[i]] += 1
        s_cnt[s[i-np]] -= 1
        if s_cnt[s[i-np]] == 0:
            del s_cnt[s[i-np]]
        if s_cnt == p_cnt:
            res.append(i - np + 1)

    return res
```

**Complexity Analysis**:
- **Time Complexity**: O(n).
- **Space Complexity**: O(1) (limited alphabet).

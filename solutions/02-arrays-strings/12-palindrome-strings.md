# Palindrome Strings - Solutions

## Practice Problems

### 1. Valid Palindrome

**Problem Statement**: Given a string `s`, return `true` if it is a palindrome, or `false` otherwise, after converting all uppercase letters into lowercase letters and removing all non-alphanumeric characters.

**Optimal Python Solution**:

```python
def isPalindrome(s: str) -> bool:
    left, right = 0, len(s) - 1

    while left < right:
        # Move pointers to skip non-alphanumeric
        while left < right and not s[left].isalnum():
            left += 1
        while left < right and not s[right].isalnum():
            right -= 1

        if s[left].lower() != s[right].lower():
            return False

        left += 1
        right -= 1

    return True
```

**Complexity Analysis**:

- **Time Complexity**: O(n).
- **Space Complexity**: O(1).

---

### 2. Valid Palindrome II

**Problem Statement**: Given a string `s`, return `true` if the `s` can be palindrome after deleting at most one character from it.

**Optimal Python Solution**:

```python
def validPalindrome(s: str) -> bool:
    def check(l, r):
        while l < r:
            if s[l] != s[r]:
                return False
            l += 1
            r -= 1
        return True

    left, right = 0, len(s) - 1
    while left < right:
        if s[left] != s[right]:
            # Try skipping the left char or skipping the right char
            return check(left + 1, right) or check(left, right - 1)
        left += 1
        right -= 1

    return True
```

**Explanation**:
When we find a mismatch, we have two choices: delete the character at `left` or delete the character at `right`. If either of the remaining substrings is a palindrome, then the original string satisfies the condition.

**Complexity Analysis**:

- **Time Complexity**: O(n).
- **Space Complexity**: O(1).

---

### 3. Longest Palindromic Substring

**Problem Statement**: Given a string `s`, return the longest palindromic substring in `s`.

**Optimal Python Solution**:

```python
def longestPalindrome(s: str) -> str:
    if not s: return ""

    def expand(l, r):
        while l >= 0 and r < len(s) and s[l] == s[r]:
            l -= 1
            r += 1
        # Return the palindrome found (indices l+1 to r-1)
        return s[l + 1 : r]

    res = ""
    for i in range(len(s)):
        # Odd length palindromes
        p1 = expand(i, i)
        # Even length palindromes
        p2 = expand(i, i + 1)

        if len(p1) > len(res): res = p1
        if len(p2) > len(res): res = p2

    return res
```

**Explanation**:
We treat each character (and each gap between characters) as a potential center of a palindrome and expand outwards as far as possible while the symmetry holds.

**Complexity Analysis**:

- **Time Complexity**: O(n²).
- **Space Complexity**: O(1) extra space (excluding result).

---

### 4. Palindromic Substrings

**Problem Statement**: Given a string `s`, return the number of palindromic substrings in it.

**Optimal Python Solution**:

```python
def countSubstrings(s: str) -> int:
    def count_from_center(l, r):
        count = 0
        while l >= 0 and r < len(s) and s[l] == s[r]:
            count += 1
            l -= 1
            r += 1
        return count

    total = 0
    for i in range(len(s)):
        total += count_from_center(i, i)      # Odd
        total += count_from_center(i, i + 1)  # Even
    return total
```

**Complexity Analysis**:

- **Time Complexity**: O(n²).
- **Space Complexity**: O(1).

---

### 5. Longest Palindromic Subsequence

**Problem Statement**: Given a string `s`, find the length of the longest palindromic subsequence in `s`.

**Optimal Python Solution**:

```python
def longestPalindromeSubseq(s: str) -> int:
    n = len(s)
    # dp[i][j] stores length of LPS in s[i...j]
    dp = [[0] * n for _ in range(n)]

    # Every single character is a palindrome of length 1
    for i in range(n - 1, -1, -1):
        dp[i][i] = 1
        for j in range(i + 1, n):
            if s[i] == s[j]:
                dp[i][j] = dp[i + 1][j - 1] + 2
            else:
                dp[i][j] = max(dp[i + 1][j], dp[i][j - 1])

    return dp[0][n - 1]
```

**Explanation**:
We use DP. If the outer characters match, they contribute 2 to the length of the LPS of the inner string. If they don't match, the LPS is the maximum of the LPS found by ignoring either the left or the right character.

**Complexity Analysis**:

- **Time Complexity**: O(n²).
- **Space Complexity**: O(n²).

---

### 6. Palindrome Partitioning

**Problem Statement**: Given a string `s`, partition `s` such that every substring of the partition is a palindrome. Return all possible palindrome partitioning of `s`.

**Optimal Python Solution**:

```python
def partition(s: str) -> list[list[str]]:
    res = []
    part = []

    def is_pal(string):
        return string == string[::-1]

    def dfs(i):
        if i >= len(s):
            res.append(part[:])
            return

        for j in range(i, len(s)):
            if is_pal(s[i : j + 1]):
                part.append(s[i : j + 1])
                dfs(j + 1)
                part.pop()

    dfs(0)
    return res
```

**Explanation**:
This is a backtracking problem. At each step, we find a prefix that is a palindrome, add it to our current partition, and recursively solve for the remaining string.

**Complexity Analysis**:

- **Time Complexity**: O(N \* 2^N) in the worst case (e.g., "aaaa").
- **Space Complexity**: O(N).

---

### 7. Palindrome Partitioning II

**Problem Statement**: Given a string `s`, partition `s` such that every substring of the partition is a palindrome. Return the minimum cuts needed for a palindrome partitioning of `s`.

**Optimal Python Solution**:

```python
def minCut(s: str) -> int:
    n = len(s)
    # dp[i] is the minimum cuts for s[i...n-1]
    dp = [0] * (n + 1)
    for i in range(n + 1):
        dp[i] = n - i - 1

    # is_pal[i][j] is True if s[i...j] is a palindrome
    is_pal = [[False] * n for _ in range(n)]

    for i in range(n - 1, -1, -1):
        for j in range(i, n):
            if s[i] == s[j] and (j - i < 2 or is_pal[i+1][j-1]):
                is_pal[i][j] = True
                # If s[i...j] is a palindrome, then cuts(s[i...n-1])
                # could be 1 + cuts(s[j+1...n-1])
                dp[i] = min(dp[i], 1 + dp[j + 1])

    return dp[0]
```

**Explanation**:
We use DP to solve this in O(n²). We first precalculate palindrome status for all substrings. Then we find the minimum cuts for each suffix of the string.

**Complexity Analysis**:

- **Time Complexity**: O(n²).
- **Space Complexity**: O(n²).

---

### 8. Shortest Palindrome

**Problem Statement**: Add characters in front of `s` to make it a palindrome. Return the shortest such palindrome.

**Optimal Python Solution**:

```python
def shortestPalindrome(s: str) -> str:
    # Use KMP LPS technique
    t = s + "#" + s[::-1]
    lps = [0] * len(t)
    for i in range(1, len(t)):
        j = lps[i - 1]
        while j > 0 and t[i] != t[j]:
            j = lps[j - 1]
        if t[i] == t[j]:
            j += 1
        lps[i] = j

    # lps[-1] is the length of the longest palindromic prefix
    add = s[lps[-1] :][::-1]
    return add + s
```

**Complexity Analysis**:

- **Time Complexity**: O(n).
- **Space Complexity**: O(n).

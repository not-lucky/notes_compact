# Palindrome Strings

> **Prerequisites:** [09-string-basics.md](./09-string-basics.md)

## Interview Context

Palindrome problems are interview favorites because they:

- Test string manipulation skills
- Have multiple solution approaches (two pointers, DP, expand from center)
- Scale from easy to hard difficulty
- Appear in both array and string contexts

Key problems: Valid Palindrome, Longest Palindromic Substring, Palindrome Partitioning.

---

## What is a Palindrome?

A string that reads the same forwards and backwards.

```
"racecar" → Palindrome ✓
"madam" → Palindrome ✓
"hello" → Not a palindrome ✗
"a" → Palindrome ✓ (single character)
"" → Palindrome ✓ (empty string)
```

---

## Template: Check Palindrome (Two Pointers)

```python
def is_palindrome(s: str) -> bool:
    """
    Check if string is a palindrome.

    Time: O(n)
    Space: O(1)
    """
    left, right = 0, len(s) - 1

    while left < right:
        if s[left] != s[right]:
            return False
        left += 1
        right -= 1

    return True
```

### One-Liner (Less Efficient)

```python
def is_palindrome_slice(s: str) -> bool:
    """
    Time: O(n)
    Space: O(n) - creates reversed copy
    """
    return s == s[::-1]
```

---

## Template: Valid Palindrome (Alphanumeric Only)

```python
def is_palindrome_alphanum(s: str) -> bool:
    """
    Check palindrome ignoring non-alphanumeric characters and case.

    Time: O(n)
    Space: O(1)

    Example:
    "A man, a plan, a canal: Panama" → True
    "race a car" → False
    """
    left, right = 0, len(s) - 1

    while left < right:
        # Skip non-alphanumeric from left
        while left < right and not s[left].isalnum():
            left += 1

        # Skip non-alphanumeric from right
        while left < right and not s[right].isalnum():
            right -= 1

        if s[left].lower() != s[right].lower():
            return False

        left += 1
        right -= 1

    return True
```

---

## Template: Valid Palindrome II (Remove at Most One)

```python
def valid_palindrome_ii(s: str) -> bool:
    """
    Check if string can be palindrome by removing at most one character.

    Time: O(n)
    Space: O(1)

    Example:
    "aba" → True
    "abca" → True (remove 'c')
    "abc" → False
    """
    def is_palindrome_range(left: int, right: int) -> bool:
        while left < right:
            if s[left] != s[right]:
                return False
            left += 1
            right -= 1
        return True

    left, right = 0, len(s) - 1

    while left < right:
        if s[left] != s[right]:
            # Try removing either character
            return (is_palindrome_range(left + 1, right) or
                    is_palindrome_range(left, right - 1))
        left += 1
        right -= 1

    return True
```

---

## Template: Longest Palindromic Substring (Expand from Center)

```python
def longest_palindrome(s: str) -> str:
    """
    Find the longest palindromic substring.

    Time: O(n²)
    Space: O(1)

    Example:
    "babad" → "bab" or "aba"
    "cbbd" → "bb"
    """
    if not s:
        return ""

    def expand_from_center(left: int, right: int) -> str:
        """Expand as long as we have a palindrome."""
        while left >= 0 and right < len(s) and s[left] == s[right]:
            left -= 1
            right += 1
        # Return the palindrome (left+1 to right-1, exclusive right)
        return s[left + 1:right]

    longest = ""

    for i in range(len(s)):
        # Odd length palindrome (single center)
        odd = expand_from_center(i, i)
        if len(odd) > len(longest):
            longest = odd

        # Even length palindrome (two centers)
        even = expand_from_center(i, i + 1)
        if len(even) > len(longest):
            longest = even

    return longest
```

### Visual: Expand from Center

```
s = "babad"

Center at index 1 ('a'):
  Expand: b[a]b → "bab" ✓
  Expand: [bab]ad → can't expand more

Center at index 2 ('b'):
  Expand: a[b]a → "aba" ✓

Both "bab" and "aba" are valid answers.
```

---

## Template: Longest Palindromic Substring (DP)

```python
def longest_palindrome_dp(s: str) -> str:
    """
    DP approach: dp[i][j] = True if s[i:j+1] is palindrome.

    Time: O(n²)
    Space: O(n²)
    """
    n = len(s)
    if n < 2:
        return s

    # dp[i][j] = True if s[i:j+1] is palindrome
    dp = [[False] * n for _ in range(n)]

    start = 0
    max_len = 1

    # All single characters are palindromes
    for i in range(n):
        dp[i][i] = True

    # Check for length 2
    for i in range(n - 1):
        if s[i] == s[i + 1]:
            dp[i][i + 1] = True
            start = i
            max_len = 2

    # Check for lengths > 2
    for length in range(3, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1

            if s[i] == s[j] and dp[i + 1][j - 1]:
                dp[i][j] = True
                start = i
                max_len = length

    return s[start:start + max_len]
```

---

## Template: Count Palindromic Substrings

```python
def count_substrings(s: str) -> int:
    """
    Count all palindromic substrings.

    Time: O(n²)
    Space: O(1)

    Example:
    "abc" → 3 ("a", "b", "c")
    "aaa" → 6 ("a"×3, "aa"×2, "aaa"×1)
    """
    count = 0

    def expand(left: int, right: int) -> int:
        """Count palindromes with this center."""
        cnt = 0
        while left >= 0 and right < len(s) and s[left] == s[right]:
            cnt += 1
            left -= 1
            right += 1
        return cnt

    for i in range(len(s)):
        count += expand(i, i)      # Odd length
        count += expand(i, i + 1)  # Even length

    return count
```

---

## Template: Longest Palindromic Subsequence (DP)

```python
def longest_palindrome_subseq(s: str) -> int:
    """
    Find length of longest palindromic SUBSEQUENCE (not substring).
    Subsequence doesn't need to be contiguous.

    Time: O(n²)
    Space: O(n²) or O(n) with optimization

    Example:
    "bbbab" → 4 ("bbbb")
    "cbbd" → 2 ("bb")
    """
    n = len(s)
    # dp[i][j] = longest palindromic subsequence in s[i:j+1]
    dp = [[0] * n for _ in range(n)]

    # Single characters
    for i in range(n):
        dp[i][i] = 1

    # Fill by increasing length
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1

            if s[i] == s[j]:
                dp[i][j] = dp[i + 1][j - 1] + 2
            else:
                dp[i][j] = max(dp[i + 1][j], dp[i][j - 1])

    return dp[0][n - 1]
```

---

## Template: Palindrome Partitioning

```python
def partition(s: str) -> list[list[str]]:
    """
    Partition s such that every substring is a palindrome.
    Return all possible partitions.

    Time: O(n × 2^n) - 2^n partitions, O(n) to check each
    Space: O(n) for recursion

    Example:
    "aab" → [["a", "a", "b"], ["aa", "b"]]
    """
    result = []

    def is_palindrome(left: int, right: int) -> bool:
        while left < right:
            if s[left] != s[right]:
                return False
            left += 1
            right -= 1
        return True

    def backtrack(start: int, path: list[str]) -> None:
        if start == len(s):
            result.append(path[:])
            return

        for end in range(start + 1, len(s) + 1):
            if is_palindrome(start, end - 1):
                path.append(s[start:end])
                backtrack(end, path)
                path.pop()

    backtrack(0, [])
    return result
```

---

## Template: Minimum Cuts for Palindrome Partitioning

```python
def min_cut(s: str) -> int:
    """
    Minimum cuts needed to partition into palindromes.

    Time: O(n²)
    Space: O(n²)

    Example:
    "aab" → 1 (cut: "aa" | "b")
    """
    n = len(s)

    # is_palindrome[i][j] = True if s[i:j+1] is palindrome
    is_palindrome = [[False] * n for _ in range(n)]

    for i in range(n - 1, -1, -1):
        for j in range(i, n):
            if s[i] == s[j] and (j - i <= 2 or is_palindrome[i + 1][j - 1]):
                is_palindrome[i][j] = True

    # dp[i] = min cuts for s[0:i+1]
    dp = [0] * n

    for i in range(n):
        if is_palindrome[0][i]:
            dp[i] = 0
        else:
            dp[i] = i  # Worst case: cut after every character
            for j in range(1, i + 1):
                if is_palindrome[j][i]:
                    dp[i] = min(dp[i], dp[j - 1] + 1)

    return dp[n - 1]
```

---

## Template: Make Palindrome by Inserting Characters

```python
def min_insertions(s: str) -> int:
    """
    Minimum insertions to make string a palindrome.

    Key insight: n - LPS (Longest Palindromic Subsequence)

    Time: O(n²)
    Space: O(n²)

    Example:
    "zzazz" → 0 (already palindrome)
    "mbadm" → 2 (insert 'b' and 'a' → "mbdadbm")
    """
    n = len(s)
    lps = longest_palindrome_subseq(s)
    return n - lps
```

---

## Edge Cases

```python
# Empty string
"" → True (palindrome), LPS = 0

# Single character
"a" → True, LPS = 1

# All same characters
"aaaa" → True, LPS = 4

# No palindrome > 1
"abcd" → LPS = 1

# Even vs odd length
"abba" (even), "aba" (odd)
```

---

## Practice Problems

| # | Problem | Difficulty | Technique |
|---|---------|------------|-----------|
| 1 | Valid Palindrome | Easy | Two pointers |
| 2 | Valid Palindrome II | Easy | Two pointers + try both |
| 3 | Longest Palindromic Substring | Medium | Expand from center |
| 4 | Palindromic Substrings | Medium | Count with expansion |
| 5 | Longest Palindromic Subsequence | Medium | DP |
| 6 | Palindrome Partitioning | Medium | Backtracking |
| 7 | Palindrome Partitioning II | Hard | DP min cuts |
| 8 | Shortest Palindrome | Hard | KMP/hashing |

---

## Key Takeaways

1. **Two pointers** for basic palindrome check
2. **Expand from center** for finding palindromic substrings
3. **DP[i][j]** for substring/subsequence problems
4. **Odd and even** centers both need checking
5. **LPS** (subsequence) ≠ longest palindromic substring

---

## Next: [13-matrix-traversal.md](./13-matrix-traversal.md)

Learn matrix traversal patterns: spiral, diagonal, and search.

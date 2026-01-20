# Palindrome DP

> **Prerequisites:** [07-2d-dp-basics](./07-2d-dp-basics.md)

## Overview

Palindrome DP problems involve finding, counting, or partitioning palindromic structures within strings.

## Building Intuition

**Why are palindrome problems well-suited for DP?**

1. **Natural Substructure**: A string is a palindrome if its first and last characters match AND the substring between them is a palindrome. This is perfect recursive structure.

2. **Interval DP Pattern**: We define dp[i][j] = "is s[i..j] a palindrome?" or "LPS length for s[i..j]". The answer for larger ranges depends on smaller ranges.

3. **Two Types of Problems**:
   - **Substring (contiguous)**: "Expand around center" is often simpler and O(1) space
   - **Subsequence (non-contiguous)**: Requires 2D DP, similar to LCS

4. **The Fill Order**: For interval DP, we must fill by increasing length (or decreasing i). dp[i][j] depends on dp[i+1][j-1], so inner ranges must be computed first.

5. **LPS Key Insight**: Longest Palindromic Subsequence of s = LCS(s, reverse(s)). This is because a common subsequence that reads same forwards and backwards is palindromic.

6. **Mental Model (Substring)**: Place your fingers at both ends of a string. If characters match, move both inward. If they ever don't match, the full string isn't a palindrome. For longest, try all centers and expand.

7. **Mental Model (Subsequence)**: If ends match, they're part of the LPS. If not, the LPS is either "without left end" or "without right end"—try both.

## Interview Context

Palindrome DP problems are popular because:

1. **Multiple variants**: Substring vs subsequence
2. **Different objectives**: Longest, count, partition
3. **Interval DP introduction**: Natural dp[i][j] structure
4. **String manipulation skills**: Common in real applications

---

## When NOT to Use Palindrome DP

1. **Longest Palindromic Substring**: Expand-around-center is simpler and uses O(1) space. Manacher's algorithm gives O(n) time. DP is overkill.

2. **Simple Palindrome Check**: For checking if a single string is a palindrome, use two pointers (O(n) time, O(1) space). DP is unnecessary.

3. **Very Long Strings**: 2D DP for LPS is O(n²) time and space. For n = 10^6, this is infeasible. Consider different algorithms or approximations.

4. **Need O(1) Space**: Expand-around-center for substring, or the 1D space-optimized LPS, but these have trade-offs.

5. **Counting All Palindromic Subsequences (Distinct)**: This is a different, harder problem requiring careful handling of duplicates.

**Choose the Right Approach:**
- Palindrome check → Two pointers
- Longest substring → Expand around center (or Manacher's)
- Longest subsequence → 2D DP (or LCS with reverse)
- Partition into palindromes → DP with precomputed palindrome table

---

## Longest Palindromic Substring

### Approach 1: Expand Around Center - O(n²)

```python
def longest_palindrome_substring(s: str) -> str:
    """
    Find longest palindromic substring.

    Expand around each center (single char and between chars).

    Time: O(n²)
    Space: O(1)
    """
    if not s:
        return ""

    start, max_len = 0, 1

    def expand(left: int, right: int) -> int:
        while left >= 0 and right < len(s) and s[left] == s[right]:
            left -= 1
            right += 1
        return right - left - 1

    for i in range(len(s)):
        # Odd length palindrome
        len1 = expand(i, i)
        # Even length palindrome
        len2 = expand(i, i + 1)

        curr_len = max(len1, len2)
        if curr_len > max_len:
            max_len = curr_len
            start = i - (curr_len - 1) // 2

    return s[start:start + max_len]
```

### Approach 2: DP - O(n²)

```python
def longest_palindrome_dp(s: str) -> str:
    """
    DP approach for longest palindromic substring.

    State: dp[i][j] = True if s[i..j] is palindrome
    Recurrence: dp[i][j] = (s[i] == s[j]) and dp[i+1][j-1]

    Time: O(n²)
    Space: O(n²)
    """
    n = len(s)
    if n < 2:
        return s

    dp = [[False] * n for _ in range(n)]
    start, max_len = 0, 1

    # Base case: single characters
    for i in range(n):
        dp[i][i] = True

    # Fill table for increasing lengths
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1

            if length == 2:
                dp[i][j] = (s[i] == s[j])
            else:
                dp[i][j] = (s[i] == s[j]) and dp[i + 1][j - 1]

            if dp[i][j] and length > max_len:
                start = i
                max_len = length

    return s[start:start + max_len]
```

---

## Longest Palindromic Subsequence

```python
def longest_palindrome_subseq(s: str) -> int:
    """
    Find length of longest palindromic subsequence.

    State: dp[i][j] = LPS length for s[i..j]
    Recurrence:
        If s[i] == s[j]: dp[i][j] = dp[i+1][j-1] + 2
        Else: dp[i][j] = max(dp[i+1][j], dp[i][j-1])

    Time: O(n²)
    Space: O(n)
    """
    n = len(s)
    dp = [0] * n

    for i in range(n - 1, -1, -1):
        new_dp = [0] * n
        new_dp[i] = 1  # Single character

        for j in range(i + 1, n):
            if s[i] == s[j]:
                new_dp[j] = dp[j - 1] + 2
            else:
                new_dp[j] = max(dp[j], new_dp[j - 1])

        dp = new_dp

    return dp[n - 1] if n > 0 else 0
```

### 2D Version

```python
def longest_palindrome_subseq_2d(s: str) -> int:
    """
    2D DP version for clarity.
    """
    n = len(s)
    dp = [[0] * n for _ in range(n)]

    # Base case: single characters
    for i in range(n):
        dp[i][i] = 1

    # Fill for increasing lengths
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

## Count Palindromic Substrings

```python
def count_substrings(s: str) -> int:
    """
    Count palindromic substrings.

    Time: O(n²)
    Space: O(1)
    """
    count = 0

    def expand(left: int, right: int) -> int:
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

## Palindrome Partitioning II (Min Cuts)

```python
def min_cut(s: str) -> int:
    """
    Minimum cuts to partition s into palindromes.

    Time: O(n²)
    Space: O(n²)
    """
    n = len(s)

    # Precompute palindrome table
    is_palin = [[False] * n for _ in range(n)]
    for i in range(n - 1, -1, -1):
        for j in range(i, n):
            if s[i] == s[j] and (j - i <= 2 or is_palin[i + 1][j - 1]):
                is_palin[i][j] = True

    # DP for minimum cuts
    dp = list(range(n))  # dp[i] = min cuts for s[0..i]

    for i in range(n):
        if is_palin[0][i]:
            dp[i] = 0
        else:
            for j in range(i):
                if is_palin[j + 1][i]:
                    dp[i] = min(dp[i], dp[j] + 1)

    return dp[n - 1]
```

---

## Palindrome Partitioning (All Partitions)

```python
def partition(s: str) -> list[list[str]]:
    """
    Find all palindrome partitions.

    Time: O(n × 2^n)
    Space: O(n)
    """
    result = []

    def is_palindrome(start: int, end: int) -> bool:
        while start < end:
            if s[start] != s[end]:
                return False
            start += 1
            end -= 1
        return True

    def backtrack(start: int, path: list[str]):
        if start == len(s):
            result.append(path[:])
            return

        for end in range(start, len(s)):
            if is_palindrome(start, end):
                path.append(s[start:end + 1])
                backtrack(end + 1, path)
                path.pop()

    backtrack(0, [])
    return result
```

---

## Valid Palindrome III (K Deletions)

```python
def is_valid_palindrome(s: str, k: int) -> bool:
    """
    Can make palindrome by deleting at most k characters?

    Key insight: n - LPS(s) = min deletions needed

    Time: O(n²)
    Space: O(n)
    """
    n = len(s)
    dp = [0] * n

    for i in range(n - 1, -1, -1):
        new_dp = [0] * n
        new_dp[i] = 1

        for j in range(i + 1, n):
            if s[i] == s[j]:
                new_dp[j] = dp[j - 1] + 2
            else:
                new_dp[j] = max(dp[j], new_dp[j - 1])

        dp = new_dp

    lps = dp[n - 1]
    return n - lps <= k
```

---

## Make String Palindrome (Min Insertions)

```python
def min_insertions(s: str) -> int:
    """
    Minimum insertions to make palindrome.

    Answer = n - LPS(s)

    Time: O(n²)
    Space: O(n)
    """
    n = len(s)
    dp = [0] * n

    for i in range(n - 1, -1, -1):
        new_dp = [0] * n
        new_dp[i] = 1

        for j in range(i + 1, n):
            if s[i] == s[j]:
                new_dp[j] = dp[j - 1] + 2
            else:
                new_dp[j] = max(dp[j], new_dp[j - 1])

        dp = new_dp

    lps = dp[n - 1]
    return n - lps
```

---

## Substring vs Subsequence

| Problem | Type | Example |
|---------|------|---------|
| Longest Palindromic Substring | Contiguous | "babad" → "bab" |
| Longest Palindromic Subsequence | Non-contiguous | "bbbab" → "bbbb" |
| Count Palindromic Substrings | Count contiguous | "aaa" → 6 |
| Min Cuts | Partition | "aab" → 1 |

---

## Edge Cases

```python
# 1. Empty string
s = ""
# Substring: "", Subsequence: 0

# 2. Single character
s = "a"
# Substring: "a", Subsequence: 1

# 3. All same characters
s = "aaaa"
# Substring: "aaaa", Subsequence: 4

# 4. No palindrome > 1
s = "abcd"
# Substring: "a" (any single), Subsequence: 1

# 5. Already palindrome
s = "racecar"
# Substring: "racecar", Subsequence: 7
```

---

## Common Mistakes

```python
# WRONG: Wrong iteration order for interval DP
for i in range(n):
    for j in range(i, n):  # dp[i+1][j-1] not computed yet!
        ...

# CORRECT: Iterate by length or reverse i
for length in range(1, n + 1):
    for i in range(n - length + 1):
        j = i + length - 1
        ...

# OR
for i in range(n - 1, -1, -1):  # Reverse
    for j in range(i, n):
        ...


# WRONG: Confusing substring with subsequence
if s[i] != s[j]:
    dp[i][j] = 0  # This is for SUBSTRING

# For SUBSEQUENCE:
dp[i][j] = max(dp[i+1][j], dp[i][j-1])
```

---

## Complexity

| Problem | Time | Space |
|---------|------|-------|
| Longest Palindromic Substring | O(n²) | O(1) or O(n²) |
| Longest Palindromic Subsequence | O(n²) | O(n) |
| Count Substrings | O(n²) | O(1) |
| Min Cuts | O(n²) | O(n²) |
| All Partitions | O(n × 2ⁿ) | O(n) |

---

## Interview Tips

1. **Know the difference**: Substring (contiguous) vs subsequence
2. **Expand around center**: Often optimal for substring
3. **Interval DP**: Fill by increasing length
4. **LPS relation**: Min insertions/deletions = n - LPS
5. **Precompute palindromes**: Useful for partition problems

---

## Practice Problems

| # | Problem | Difficulty | Type |
|---|---------|------------|------|
| 1 | Longest Palindromic Substring | Medium | Substring |
| 2 | Longest Palindromic Subsequence | Medium | Subsequence |
| 3 | Palindromic Substrings | Medium | Count |
| 4 | Palindrome Partitioning | Medium | All partitions |
| 5 | Palindrome Partitioning II | Hard | Min cuts |

---

## Key Takeaways

1. **Two main types**: Substring (contiguous) vs subsequence
2. **Expand around center**: Best for substring problems
3. **Interval DP**: dp[i][j] for range problems
4. **LPS is key**: Many problems reduce to finding LPS
5. **Iteration order**: Fill by increasing length

---

## Next: [13-word-break.md](./13-word-break.md)

Learn dictionary-based DP with Word Break problems.

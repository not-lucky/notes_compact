# Palindrome DP

> **Prerequisites:** [07-2d-dp-basics](./07-2d-dp-basics.md)

## Overview

Palindrome DP problems involve finding, counting, or partitioning palindromic structures within strings. These naturally form **Interval DP** problems. Instead of processing the string left-to-right (prefixes) like we do in most 1D DP, we solve for small intervals (substrings) and expand outward to larger intervals.

## Core Intuition: Expanding Intervals

A string is a palindrome if:
1. Its first and last characters match ($s[i] == s[j]$).
2. The substring strictly between them ($s[i+1 \dots j-1]$) is also a palindrome.

Because the answer for a large interval $[i, j]$ depends on a smaller strictly nested interval $[i+1, j-1]$, we **must solve smaller lengths before larger lengths**.

### The Two Valid Traversal Orders for Interval DP

To ensure $dp[i+1][j-1]$ is computed before $dp[i][j]$, you can loop in one of two ways:

1. **Loop by Length (Diagonal Traversal):**
   ```python
   for length in range(1, n + 1):
       for i in range(n - length + 1):
           j = i + length - 1
   ```

2. **Loop Endpoints Backwards (Bottom-Up Traversal):**
   ```python
   for i in range(n - 1, -1, -1):  # i moves left
       for j in range(i, n):       # j moves right
   ```

*Common Mistake:* A standard forward nested loop (`for i in range(n): for j in range(i, n):`) **will fail** because it tries to access $dp[i+1]$ before row $i+1$ has been computed!

---

## Types of Palindrome Problems

Grouping problems conceptually helps you know which algorithm to apply:

### Type 1: Substring (Contiguous)
*Examples: Longest Palindromic Substring, Count Palindromic Substrings.*
- **Characteristics**: Must be unbroken sequences of characters.
- **Best Approach**: Expand Around Center. Takes $O(n^2)$ time and **$O(1)$ space**.
- **When to use DP**: Only use $O(n^2)$ space DP if you need to quickly answer many `is_palindrome(i, j)` queries later (e.g., in partitioning problems).

### Type 2: Subsequence (Non-contiguous)
*Examples: Longest Palindromic Subsequence, Valid Palindrome III, Minimum Insertions.*
- **Characteristics**: Can skip characters.
- **Best Approach**: 2D Interval DP ($O(n^2)$ time). Can be space-optimized to $O(n)$.

### Type 3: Partitioning
*Examples: Palindrome Partitioning I & II.*
- **Characteristics**: Break the string into chunks that are each valid palindromes.
- **Best Approach**: Precompute all valid palindromic substrings using Interval DP ($O(n^2)$), then run a 1D DP or Backtracking over the string splits to find cuts.

---

## 1. Substring Problems (Contiguous)

For contiguous palindromes, "Expand Around Center" is the optimal approach because it avoids the $O(n^2)$ memory overhead of a DP table.

### Expand Around Center (Best Practice)

We treat every character (and every space between characters) as a potential center and expand outwards.

```python
def longest_palindrome_substring(s: str) -> str:
    """
    Time: O(n^2) where n is the length of the string.
    Space: O(1) beyond the output string.
    """
    if not s:
        return ""
    start, max_len = 0, 1

    def expand_around_center(left: int, right: int) -> int:
        while left >= 0 and right < len(s) and s[left] == s[right]:
            left -= 1
            right += 1
        # Length is (right - 1) - (left + 1) + 1 = right - left - 1
        return right - left - 1

    for i in range(len(s)):
        # Odd length (center is character i)
        len1 = expand_around_center(i, i)
        # Even length (center is between i and i+1)
        len2 = expand_around_center(i, i + 1)

        curr_max = max(len1, len2)
        if curr_max > max_len:
            max_len = curr_max
            # Calculate start index based on center 'i' and length
            start = i - (curr_max - 1) // 2

    return s[start:start + max_len]
```

### Precomputing Substring Palindromes (Interval DP)

If a problem requires checking $O(n^2)$ different substrings for palindromes multiple times, we precompute a boolean DP table.

**Recurrence:**
$dp[i][j]$ is `True` if $s[i \dots j]$ is a palindrome.
$$
dp[i][j] = s[i] == s[j] \text{ AND } dp[i+1][j-1]
$$

```python
def get_palindrome_table(s: str) -> list[list[bool]]:
    """
    Time: O(n^2)
    Space: O(n^2) for the 2D DP matrix.
    """
    n = len(s)
    dp = [[False] * n for _ in range(n)]

    # Fill base cases: length 1
    for i in range(n):
        dp[i][i] = True

    # Fill for increasing lengths (Interval DP)
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1

            if s[i] == s[j]:
                # length 2 only requires matching characters
                if length == 2 or dp[i + 1][j - 1]:
                    dp[i][j] = True

    return dp
```

---

## 2. Subsequence Problems (Non-contiguous)

Longest Palindromic Subsequence (LPS) allows skipping characters.

**Recurrence Insight:**
If the outer characters match ($s[i] == s[j]$), they *must* form the ends of the best subsequence.
If they don't match, the best subsequence is the maximum of either ignoring the left character ($i+1$) or the right character ($j-1$).

$$
dp[i][j] =
\begin{cases}
1 & \text{if } i = j \\
2 + dp[i+1][j-1] & \text{if } s[i] == s[j] \\
\max(dp[i+1][j], dp[i][j-1]) & \text{if } s[i] \neq s[j]
\end{cases}
$$

### Space-Optimized Interval DP

Since $dp[i][j]$ only depends on $dp[i+1][\dots]$ (the row directly below) and $dp[i][j-1]$ (the current row), we can optimize space to $O(n)$. We iterate `i` backwards.

```python
def longest_palindrome_subseq(s: str) -> int:
    """
    Time: O(n^2)
    Space: O(n) using 1D row arrays.
    """
    n = len(s)
    # row_below represents dp[i+1]
    row_below = [0] * n

    for i in range(n - 1, -1, -1):
        # curr_row represents dp[i]
        curr_row = [0] * n
        curr_row[i] = 1  # Base case: single character palindrome

        for j in range(i + 1, n):
            if s[i] == s[j]:
                # 2 + inner subsequence (from the row below, shifted left)
                curr_row[j] = 2 + row_below[j - 1]
            else:
                # Max of excluding left char (row_below[j]) or right char (curr_row[j-1])
                curr_row[j] = max(row_below[j], curr_row[j - 1])

        row_below = curr_row

    return row_below[n - 1]
```

### LPS Variations

Many "Make String Palindrome" problems gracefully reduce to finding the Longest Palindromic Subsequence.

*   **Valid Palindrome III (Can make palindrome with $\le K$ Deletions?)**
    Every character *not* part of the LPS must be deleted. Check if `len(s) - LPS(s) <= k`.
*   **Minimum Insertions to Make String Palindrome**
    Every character *not* in the LPS needs a matching partner inserted on the opposite side. Insertions required = `len(s) - LPS(s)`.

```python
def min_insertions(s: str) -> int:
    """
    Time: O(n^2)
    Space: O(n)
    """
    n = len(s)
    row_below = [0] * n
    for i in range(n - 1, -1, -1):
        curr_row = [0] * n
        curr_row[i] = 1
        for j in range(i + 1, n):
            if s[i] == s[j]:
                curr_row[j] = 2 + row_below[j - 1]
            else:
                curr_row[j] = max(row_below[j], curr_row[j - 1])
        row_below = curr_row

    lps_length = row_below[n - 1]
    return n - lps_length
```

---

## 3. Partitioning Problems

Problems like Minimum Cuts (Palindrome Partitioning II) require breaking the string into valid palindromes. This combines Interval DP (for precomputing palindromes) with a 1D linear DP (for the cuts).

### Minimum Cuts (Palindrome Partitioning II)

```python
def min_cut(s: str) -> int:
    """
    Time: O(n^2) - O(n^2) to precompute palindromes, O(n^2) for the 1D DP.
    Space: O(n^2) for the boolean matrix.
    """
    n = len(s)
    if n <= 1:
        return 0

    # 1. Precompute valid palindromes using Interval DP
    is_palindrome = [[False] * n for _ in range(n)]
    for length in range(1, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            if s[i] == s[j] and (length <= 2 or is_palindrome[i + 1][j - 1]):
                is_palindrome[i][j] = True

    # 2. 1D DP to find minimum cuts
    # dp[i] = min cuts needed for prefix s[0..i]
    dp = [0] * n
    for i in range(n):
        if is_palindrome[0][i]:
            dp[i] = 0  # Whole prefix is palindrome, 0 cuts needed
        else:
            dp[i] = i  # Max possible cuts (each char is separate)
            for j in range(i):
                # If s[j+1..i] is a palindrome, we can cut after j
                if is_palindrome[j + 1][i]:
                    dp[i] = min(dp[i], dp[j] + 1)

    return dp[n - 1]
```

# Palindrome DP

> **Prerequisites:** [07-2d-dp-basics](./07-2d-dp-basics.md)

## Overview

Palindrome DP problems involve finding, counting, or partitioning palindromic structures within strings. These naturally form **Interval DP** problems, where we solve for small intervals and expand outward to larger intervals.

## Formal Recurrence

Let $s$ be a string of length $n$.

### 1. Palindromic Substring (Contiguous)
Let $dp[i][j]$ be `True` if the substring $s[i..j]$ is a palindrome.

A substring is a palindrome if its first and last characters match, AND the inner substring is also a palindrome.

$$
dp[i][j] =
\begin{cases}
\text{True} & \text{if } i = j \text{ (length 1)} \\
s[i] == s[j] & \text{if } j - i = 1 \text{ (length 2)} \\
s[i] == s[j] \text{ and } dp[i+1][j-1] & \text{if } j - i > 1
\end{cases}
$$

### 2. Longest Palindromic Subsequence (Non-contiguous)
Let $dp[i][j]$ be the length of the longest palindromic subsequence in $s[i..j]$.

If the outer characters match, they form the ends of the LPS. If they don't, the LPS is the maximum of either ignoring the left character or the right character.

$$
dp[i][j] =
\begin{cases}
1 & \text{if } i = j \\
2 + dp[i+1][j-1] & \text{if } s[i] == s[j] \\
\max(dp[i+1][j], dp[i][j-1]) & \text{if } s[i] \neq s[j]
\end{cases}
$$

## Building Intuition

**Why are palindrome problems well-suited for DP?**

1. **Natural Substructure**: A string is a palindrome if its first and last characters match AND the substring between them is a palindrome. This is a perfect recursive structure.
2. **Interval DP Pattern**: We define the state based on start and end indices `(i, j)`. The answer for larger intervals depends strictly on smaller intervals.
3. **The Fill Order**: For interval DP, we must evaluate smaller lengths before larger lengths. This means either:
   - Outer loop `length` from 1 to $n$, inner loop `i` from 0 to $n - length$.
   - Outer loop `i` backwards from $n-1$ down to 0, inner loop `j` forwards from `i` to $n-1$.
4. **LPS Key Insight**: The Longest Palindromic Subsequence of $s$ is equivalent to `LCS(s, reverse(s))`. This is because a common subsequence that reads the same forwards and backwards is inherently palindromic.

## Substring vs Subsequence Types

Grouping problems conceptually helps you know which algorithm to apply:

### Type 1: Substring (Contiguous)
*Examples: Longest Palindromic Substring, Count Palindromic Substrings.*
- **Characteristics**: Must be unbroken sequences of characters.
- **Best Approach**: Expand Around Center ($O(n^2)$ time, $O(1)$ space). DP takes $O(n^2)$ space, which is strictly worse. Manacher's Algorithm is $O(n)$ time but generally too complex for interviews.

### Type 2: Subsequence (Non-contiguous)
*Examples: Longest Palindromic Subsequence, Valid Palindrome III (K deletions), Minimum Insertions to Make Palindrome.*
- **Characteristics**: Can skip characters.
- **Best Approach**: 2D Interval DP ($O(n^2)$ time and space). Can be space-optimized to $O(n)$.

### Type 3: Partitioning
*Examples: Palindrome Partitioning I & II.*
- **Characteristics**: Break the string into chunks that are each valid palindromes.
- **Best Approach**: Precompute all valid palindromic substrings using Interval DP ($O(n^2)$), then run a 1D DP or Backtracking over the string splits.

---

## When NOT to Use DP

1. **Longest Palindromic Substring**: "Expand Around Center" is simpler and uses $O(1)$ space compared to DP's $O(n^2)$.
2. **Simple Palindrome Check**: For checking if a single complete string is a palindrome, use two pointers ($O(n)$ time, $O(1)$ space). DP is completely unnecessary.
3. **Very Long Strings**: 2D DP for LPS is $O(n^2)$ time and space. For $n \ge 10^4$, this will cause MLE (Memory Limit Exceeded) or TLE (Time Limit Exceeded).
4. **Counting Distinct Palindromic Subsequences**: This is a much harder problem requiring careful handling of duplicates, often needing state beyond just `[i][j]`.

---

## Longest Palindromic Substring & Counting (Contiguous)

For contiguous palindromes, "Expand Around Center" is the optimal approach.

### Approach 1: Expand Around Center (Best Practice) - O(n²) time, O(1) space

```python
def longest_palindrome_substring(s: str) -> str:
    if not s:
        return ""
    start, max_len = 0, 1

    def expand(left: int, right: int) -> int:
        while left >= 0 and right < len(s) and s[left] == s[right]:
            left -= 1
            right += 1
        # Length is (right - 1) - (left + 1) + 1 = right - left - 1
        return right - left - 1

    for i in range(len(s)):
        # Odd length (center is character i)
        len1 = expand(i, i)
        # Even length (center is between i and i+1)
        len2 = expand(i, i + 1)

        curr_len = max(len1, len2)
        if curr_len > max_len:
            max_len = curr_len
            start = i - (curr_len - 1) // 2

    return s[start:start + max_len]
```

### Approach 2: Count Palindromic Substrings - O(n²) time, O(1) space

The same expansion logic can be used to count all palindromic substrings simply by counting each successful expansion.

```python
def count_substrings(s: str) -> int:
    count = 0

    def expand_and_count(left: int, right: int) -> int:
        palindromes = 0
        while left >= 0 and right < len(s) and s[left] == s[right]:
            palindromes += 1
            left -= 1
            right += 1
        return palindromes

    for i in range(len(s)):
        count += expand_and_count(i, i)      # Odd length palindromes
        count += expand_and_count(i, i + 1)  # Even length palindromes

    return count
```

### Approach 3: DP Tabulation - O(n²) time, O(n²) space

DP for substrings is useful when you need to answer *many* `is_palindrome(i, j)` queries later, such as in partitioning problems.

```python
def get_palindrome_table(s: str) -> list[list[bool]]:
    n = len(s)
    dp = [[False] * n for _ in range(n)]

    # Base cases: length 1
    for i in range(n):
        dp[i][i] = True

    # Fill for increasing lengths
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1

            if s[i] == s[j]:
                if length == 2 or dp[i + 1][j - 1]:
                    dp[i][j] = True

    return dp
```

---

## Longest Palindromic Subsequence (Non-contiguous)

### Approach 1: Top-Down (Memoization)

```python
def longest_palindrome_subseq_memo(s: str) -> int:
    memo = {}

    def dfs(i: int, j: int) -> int:
        if i > j:
            return 0
        if i == j:
            return 1

        if (i, j) in memo:
            return memo[(i, j)]

        if s[i] == s[j]:
            res = 2 + dfs(i + 1, j - 1)
        else:
            res = max(dfs(i + 1, j), dfs(i, j - 1))

        memo[(i, j)] = res
        return res

    return dfs(0, len(s) - 1)
```

### Approach 2: Space-Optimized Tabulation

Since `dp[i][j]` depends on `dp[i+1][...]` (the row below) and `dp[i][j-1]` (left), we can optimize space to $O(n)$ by iterating `i` backwards.

```python
def longest_palindrome_subseq(s: str) -> int:
    n = len(s)
    # dp[j] will represent the row `i+1` (the row below the current one).
    dp = [0] * n

    for i in range(n - 1, -1, -1):
        # new_dp[j] represents the current row `i` being computed.
        new_dp = [0] * n
        new_dp[i] = 1  # Base case: single character palindrome

        for j in range(i + 1, n):
            if s[i] == s[j]:
                # dp[j-1] is from row i+1 (computed in previous outer loop iteration)
                new_dp[j] = 2 + dp[j - 1]
            else:
                # new_dp[j-1] is from current row, left. dp[j] is row below.
                new_dp[j] = max(dp[j], new_dp[j - 1])

        dp = new_dp

    return dp[n - 1]
```

### DP Table Visualization for Subsequence
`s = "bbbab"`

| i \ j | 0 (b) | 1 (b) | 2 (b) | 3 (a) | 4 (b) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **0 (b)** | 1 | 2 | 3 | 3 | 4 |
| **1 (b)** | - | 1 | 2 | 2 | 3 |
| **2 (b)** | - | - | 1 | 1 | 3 |
| **3 (a)** | - | - | - | 1 | 1 |
| **4 (b)** | - | - | - | - | 1 |

*Note: Table is filled diagonally or bottom-to-top. The lower left is empty because $i \leq j$.*

---

## Make String Palindrome Variations

These problems elegantly reduce to the Longest Palindromic Subsequence (LPS).

### Valid Palindrome III (Can make palindrome with $\leq$ K Deletions?)
Every character in $s$ that is *not* part of the LPS must be deleted.
Deletions required = `len(s) - LPS(s)`.
Check if `len(s) - LPS(s) <= k`.

### Minimum Insertions to Make String Palindrome
Every character not in the LPS needs a matching partner inserted on the opposite side.
Insertions required = `len(s) - LPS(s)`.

```python
def min_insertions(s: str) -> int:
    # Just return len(s) - longest_palindrome_subseq(s)
    n = len(s)
    dp = [0] * n
    for i in range(n - 1, -1, -1):
        new_dp = [0] * n
        new_dp[i] = 1
        for j in range(i + 1, n):
            if s[i] == s[j]:
                new_dp[j] = 2 + dp[j - 1]
            else:
                new_dp[j] = max(dp[j], new_dp[j - 1])
        dp = new_dp
    return n - dp[n - 1]
```

---

## Palindrome Partitioning

### Minimum Cuts (Palindrome Partitioning II)

```python
def min_cut(s: str) -> int:
    n = len(s)
    if n <= 1:
        return 0

    # 1. Precompute palindromes in O(n^2)
    is_palin = [[False] * n for _ in range(n)]
    for i in range(n):
        is_palin[i][i] = True

    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            if s[i] == s[j] and (length <= 2 or is_palin[i + 1][j - 1]):
                is_palin[i][j] = True

    # 2. 1D DP for minimum cuts
    # dp[i] = min cuts for substring s[0..i]
    dp = [0] * n
    for i in range(n):
        if is_palin[0][i]:
            dp[i] = 0  # Whole prefix is palindrome, 0 cuts
        else:
            dp[i] = i  # Max possible cuts (each char separate)
            for j in range(i):
                if is_palin[j + 1][i]:
                    dp[i] = min(dp[i], dp[j] + 1)

    return dp[n - 1]
```

---

## Common Mistakes

```python
# WRONG: Iterating normally for Interval DP
for i in range(n):
    for j in range(i, n):
        # ERROR: dp[i+1][j-1] hasn't been computed yet!
        dp[i][j] = dp[i+1][j-1] + 2

# CORRECT: Iterate by length
for length in range(1, n + 1):
    for i in range(n - length + 1):
        j = i + length - 1

# OR CORRECT: Iterate `i` backwards
for i in range(n - 1, -1, -1):
    for j in range(i, n):
```

---

## Complexity

| Problem | Time | Space | Notes |
| :--- | :--- | :--- | :--- |
| Longest Palindromic Substring | $O(n^2)$ | $O(1)$ | Use Expand Around Center |
| Longest Palindromic Subsequence | $O(n^2)$ | $O(n)$ | 1D Space Optimized Interval DP |
| Count Substrings | $O(n^2)$ | $O(1)$ | Use Expand Around Center |
| Min Cuts (Partitioning II) | $O(n^2)$ | $O(n^2)$ | Precompute + 1D DP |
| All Partitions | $O(n \times 2^n)$ | $O(n)$ | Backtracking |

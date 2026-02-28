# Longest Common Subsequence (LCS)

> **Prerequisites:** [2D DP Basics](./07-2d-dp-basics.md)

## Overview

The Longest Common Subsequence (LCS) problem is a cornerstone of string algorithms and dynamic programming. It forms the foundation for many real-world applications.

### Real-World Motivation

Why do we care about finding the longest common subsequence?
*   **Version Control (`git diff`)**: When comparing two versions of a file, `diff` algorithms use LCS to find the longest sequence of lines that haven't changed. Everything else is treated as an insertion or deletion.
*   **Bioinformatics (Sequence Alignment)**: DNA is just a long string of characters (`A`, `C`, `G`, `T`). Comparing two DNA sequences to find their longest common subsequence helps scientists determine how closely related two species are, or identify genetic mutations.
*   **Spell Checking & Plagiarism Detection**: Comparing a misspelled word against a dictionary, or checking a student's essay against known sources, relies on finding how much of the sequences overlap in the same relative order.

### Subsequence vs. Substring

It is crucial to understand the difference between these two concepts:

*   **Substring**: Must be **contiguous** (no gaps allowed).
    *   For the string `"abcde"`, valid substrings are `"abc"`, `"cde"`, `"b"`.
    *   `"ace"` is *not* a substring.
*   **Subsequence**: Characters can be skipped, but the **relative order must be maintained**.
    *   For the string `"abcde"`, `"ace"` *is* a valid subsequence.
    *   `"ca"` is *not* a valid subsequence (order is wrong).

**The Problem:** Given two strings, `text1` and `text2`, what is the length of the longest sequence that appears in both strings in the same relative order?

---

## Building Intuition

**Why does LCS require 2D DP?**

Because we are dealing with two distinct sequences, we need to track our progress through both of them simultaneously. A 1D array isn't enough to capture the state of "where we are in `text1`" *and* "where we are in `text2`".

Therefore, we use a 2D array where `dp[i][j]` represents the length of the LCS for the prefix `text1[0...i-1]` and the prefix `text2[0...j-1]`.

### The Core Insight

Imagine you are looking at the last characters of the prefixes you are currently considering: `text1[i-1]` and `text2[j-1]`.

1.  **If the characters match (`text1[i-1] == text2[j-1]`):**
    You've found a piece of the common subsequence! Because these characters match, the longest common subsequence up to these points *must* include this character. The length of the LCS is simply 1 plus the LCS of the prefixes *before* these matching characters.
    *   **Transition:** `dp[i][j] = 1 + dp[i-1][j-1]` (Move diagonally up-left)

2.  **If they don't match (`text1[i-1] != text2[j-1]`):**
    These two characters cannot both be the end of the common subsequence. The LCS might end with `text1[i-1]`, or it might end with `text2[j-1]`, or neither. But it *cannot* end with both. So, we must drop one of the characters and see which option gives us a better result.
    *   **Option A:** Drop `text1[i-1]` and look at `(text1[0...i-2], text2[0...j-1])` -> `dp[i-1][j]`
    *   **Option B:** Drop `text2[j-1]` and look at `(text1[0...i-1], text2[0...j-2])` -> `dp[i][j-1]`
    *   **Transition:** We take the best of these two paths: `dp[i][j] = max(dp[i-1][j], dp[i][j-1])` (Max of cell above or cell to the left)

    Because LCS is a *subsequence* (gaps allowed), we "carry forward" the best score we've seen so far when there is a mismatch. We do *not* reset the score to `0`.

## Formal Recurrence Relation

Let $dp[i][j]$ be the length of the Longest Common Subsequence of the prefixes `text1[0...i-1]` and `text2[0...j-1]`.

**State:**
`dp[i][j]` is the LCS length for prefixes of length $i$ and $j$.

**Base Cases:**
- $dp[i][0] = 0$ for all $i \in [0, M]$ (An empty `text2` means an LCS of `0`)
- $dp[0][j] = 0$ for all $j \in [0, N]$ (An empty `text1` means an LCS of `0`)

**Recursive Step:**
For given prefix lengths $i > 0$ and $j > 0$:
$$
dp[i][j] = \begin{cases}
1 + dp[i-1][j-1] & \text{if } text1[i-1] == text2[j-1] \\
\max(dp[i-1][j], dp[i][j-1]) & \text{if } text1[i-1] \neq text2[j-1]
\end{cases}
$$

**Result:**
$$dp[M][N]$$ where $M$ and $N$ are the lengths of `text1` and `text2`.

---

## Visual Walkthrough

Let's trace the LCS for `text1="abcde"`, `text2="ace"`.

We build a table of size $(M+1) \times (N+1)$ to accommodate the empty string prefixes (length 0).

```text
       ""    a    c    e
    +----+----+----+----+
 "" |  0 |  0 |  0 |  0 |
    +----+----+----+----+
  a |  0 |  1 |  1 |  1 |
    +----+----+----+----+
  b |  0 |  1 |  1 |  1 |
    +----+----+----+----+
  c |  0 |  1 |  2 |  2 |
    +----+----+----+----+
  d |  0 |  1 |  2 |  2 |
    +----+----+----+----+
  e |  0 |  1 |  2 |  3 |
    +----+----+----+----+
```

**Step-by-Step Execution:**

1.  **Row 1 (`a`):**
    *   **`a` vs `a` (`dp[1][1]`):** Match! We take the diagonal value (`dp[0][0]=0`) and add `1`. Result: `1`.
    *   **`a` vs `c` (`dp[1][2]`):** Mismatch. We take the max of the value above (`dp[0][2]=0`) and the value to the left (`dp[1][1]=1`). We carry the `1` forward. Result: `1`.
    *   **`a` vs `e` (`dp[1][3]`):** Mismatch. Max of above (`0`) and left (`1`). Result: `1`.

2.  **Row 2 (`b`):**
    *   **`b` vs `a` (`dp[2][1]`):** Mismatch. Max of above (`1`) and left (`0`). We carry the `1` down. Result: `1`.
    *   ... (mismatches continue, carrying the `1` forward and down).

3.  **Row 3 (`c`):**
    *   **`c` vs `c` (`dp[3][2]`):** Match! We look diagonally up-left to `dp[2][1]` (which is `1`, representing the matched `"a"`). We add `1`. Result: `2`.

4.  **Row 5 (`e`):**
    *   **`e` vs `e` (`dp[5][3]`):** Match! Diagonal up-left `dp[4][2]` is `2` (representing `"ac"`). Add `1`. Result: `3`.

When there's a mismatch, we pull the value from the top or left, whichever is larger, effectively carrying our best "matched score" forward. When there's a match, we add 1 to the best score from *before* considering both of these letters (the diagonal).

---

## Solutions

### 1. Top-Down (Memoization)

```python
def longest_common_subsequence_memo(text1: str, text2: str) -> int:
    """
    Time Complexity: O(M * N) where M and N are the string lengths.
    Space Complexity: O(M * N) for the memoization dictionary and recursion stack.
    """
    m, n = len(text1), len(text2)
    memo = {}

    def dfs(i: int, j: int) -> int:
        # Base case: if either prefix is empty, LCS is 0
        if i == 0 or j == 0:
            return 0

        if (i, j) in memo:
            return memo[(i, j)]

        # If characters match, add 1 and shrink both prefixes
        if text1[i - 1] == text2[j - 1]:
            res = 1 + dfs(i - 1, j - 1)
        else:
            # If mismatch, try dropping one character from either string
            res = max(dfs(i - 1, j), dfs(i, j - 1))

        memo[(i, j)] = res
        return res

    return dfs(m, n)
```

### 2. Bottom-Up 2D DP

This is the standard, most intuitive way to write LCS.

```python
def longest_common_subsequence_2d(text1: str, text2: str) -> int:
    """
    Time Complexity: O(M * N)
    Space Complexity: O(M * N)
    """
    m, n = len(text1), len(text2)

    # dp[i][j] represents LCS of text1[0...i-1] and text2[0...j-1]
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i - 1] == text2[j - 1]:
                # Characters match: diagonal + 1
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                # Characters mismatch: max of top or left
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    return dp[m][n]
```

### 3. Space-Optimized Bottom-Up DP (1D Array)

Notice in the 2D approach that to compute `dp[i][j]` (the current cell), we only ever look at:
1. `dp[i-1][j]` (directly above)
2. `dp[i][j-1]` (directly left)
3. `dp[i-1][j-1]` (diagonally up-left)

Because we compute row by row, we don't need the entire $M \times N$ matrix. We only need the *current* row being built and the *previous* row. We can optimize this even further to a single 1D array of size $N+1$ by keeping track of the `prev_diagonal` value in a separate variable.

```python
def longest_common_subsequence(text1: str, text2: str) -> int:
    """
    Time Complexity: O(M * N)
    Space Complexity: O(min(M, N)) - optimized to use only a 1D array.
    """
    # Optimization: Ensure text2 is the shorter string to minimize array size
    if len(text1) < len(text2):
        text1, text2 = text2, text1

    m, n = len(text1), len(text2)
    # dp represents the "current row" we are building
    dp = [0] * (n + 1)

    for i in range(1, m + 1):
        # prev_diagonal represents dp[i-1][j-1]. At the start of a row, j=0,
        # so dp[i-1][0] is always 0.
        prev_diagonal = 0

        for j in range(1, n + 1):
            # Save the current dp[j] (which is dp[i-1][j] from the previous row)
            # because we are about to overwrite it, but we'll need it as the
            # prev_diagonal for the NEXT j step.
            temp = dp[j]

            if text1[i - 1] == text2[j - 1]:
                # 1 + dp[i-1][j-1]
                dp[j] = prev_diagonal + 1
            else:
                # max(dp[i-1][j], dp[i][j-1])
                # dp[j] is currently the value from the row above
                # dp[j-1] is the value we just calculated on the left
                dp[j] = max(dp[j], dp[j - 1])

            # The old dp[i-1][j] becomes the prev_diagonal (dp[i-1][j-1]) for j+1
            prev_diagonal = temp

    return dp[n]
```

---

## Reconstructing the LCS String

Finding the *length* of the LCS is usually the goal, but sometimes you need to return the actual string. You can find it by backtracking through the filled 2D `dp` table starting from the bottom-right `dp[m][n]`.

```python
def get_lcs_string(text1: str, text2: str) -> str:
    """
    Time Complexity: O(M * N)
    Space Complexity: O(M * N)
    """
    m, n = len(text1), len(text2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # 1. Build the DP table
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i - 1] == text2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    # 2. Backtrack to find the sequence
    lcs_chars = []
    i, j = m, n

    while i > 0 and j > 0:
        if text1[i - 1] == text2[j - 1]:
            # Character belongs to LCS, add it and move diagonally up-left
            lcs_chars.append(text1[i - 1])
            i -= 1
            j -= 1
        elif dp[i - 1][j] > dp[i][j - 1]:
            # The larger value came from above, so move up
            i -= 1
        else:
            # The larger value came from the left (or they are equal), so move left
            j -= 1

    # We backtracked from end to start, so reverse the accumulated characters
    return "".join(reversed(lcs_chars))
```

---

## Common Variations & Applications

LCS is a foundational pattern. Many problems are just LCS in disguise or require minor tweaks to the recurrence relation.

### 1. Longest Common Substring
*Difference: The matching characters must be contiguous.*

Because characters must be contiguous, the state definition changes. `dp[i][j]` is now the length of the longest common substring **ending exactly at** `text1[i-1]` and `text2[j-1]`.

If the characters mismatch, the contiguous chain is broken, so we **must reset the length to `0`**. The answer is not necessarily at `dp[m][n]` anymore; it's the maximum value found anywhere in the table.

```python
def longest_common_substring(text1: str, text2: str) -> int:
    """
    Time Complexity: O(M * N)
    Space Complexity: O(M * N)
    """
    m, n = len(text1), len(text2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    max_len = 0

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i - 1] == text2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
                max_len = max(max_len, dp[i][j])
            else:
                dp[i][j] = 0 # Contiguous chain broken, reset to 0

    return max_len
```

### 2. Minimum ASCII Delete Sum for Two Strings (LeetCode 712)
*Difference: Instead of maximizing length, we minimize the ASCII sum of deleted characters to make the strings equal.*

If characters match, there's no cost. If they differ, we must delete either `s1[i-1]` or `s2[j-1]` and add its ASCII value to our running cost.

```python
def minimum_delete_sum(s1: str, s2: str) -> int:
    """
    Time Complexity: O(M * N)
    Space Complexity: O(M * N)
    """
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # Base cases: cost to delete all characters if the other string is empty
    for i in range(1, m + 1):
        dp[i][0] = dp[i - 1][0] + ord(s1[i - 1])
    for j in range(1, n + 1):
        dp[0][j] = dp[0][j - 1] + ord(s2[j - 1])

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                # Cost is the same as the cost before these characters
                dp[i][j] = dp[i - 1][j - 1]
            else:
                # Min cost of deleting from s1 OR deleting from s2
                dp[i][j] = min(
                    dp[i - 1][j] + ord(s1[i - 1]),
                    dp[i][j - 1] + ord(s2[j - 1])
                )
    return dp[m][n]
```

### 3. Shortest Common Supersequence
*Problem: Find the shortest string that has both `str1` and `str2` as subsequences.*

**Insight:** The shortest common supersequence consists of the Longest Common Subsequence included exactly once, padded with all the remaining un-matched characters from both strings.
`Length = len(str1) + len(str2) - len(LCS(str1, str2))`

### 4. Longest Palindromic Subsequence
*Problem: Find the longest subsequence of a string `s` that is a palindrome.*

**Insight:** A clever trick! The longest palindromic subsequence of `s` is simply the Longest Common Subsequence of `s` and `reverse(s)`.

```python
def longest_palindrome_subseq(s: str) -> int:
    """
    Time Complexity: O(N^2)
    Space Complexity: O(N^2)
    """
    # Reverse string in Python: s[::-1]
    return longest_common_subsequence(s, s[::-1])
```

### 5. Uncrossed Lines (LeetCode 1035)
*Problem: Given two arrays `nums1` and `nums2`, draw uncrossed lines connecting matching elements. What is the max number of uncrossed lines?*

**Insight:** Because the lines cannot cross, the relative order of the matched elements is strictly preserved. This problem is literally just finding the Longest Common Subsequence of the two arrays.

```python
def max_uncrossed_lines(nums1: list[int], nums2: list[int]) -> int:
    """
    Time Complexity: O(M * N)
    Space Complexity: O(M * N)
    """
    # Identical to LCS 2D code, just swapping strings for lists
    m, n = len(nums1), len(nums2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if nums1[i - 1] == nums2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    return dp[m][n]
```

## Summary

- **State:** `dp[i][j]` = length of LCS of `text1[0...i-1]` and `text2[0...j-1]`.
- **Match:** `dp[i][j] = dp[i-1][j-1] + 1` (Move diagonally).
- **Mismatch:** `dp[i][j] = max(dp[i-1][j], dp[i][j-1])` (Move up or left).
- **Time / Space:** $O(M \times N)$ standard, $O(\min(M, N))$ space-optimized.
- **Pattern Recognition:** "Two sequences", "relative order matters", "can skip elements", "maximum length".

---

## Next: [Edit Distance](./09-edit-distance.md)

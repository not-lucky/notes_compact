# Longest Common Subsequence (LCS)

> **Prerequisites:** [07-2d-dp-basics](./07-2d-dp-basics.md)

## Overview

The Longest Common Subsequence (LCS) problem is a classic dynamic programming challenge. A **subsequence** is a sequence that can be derived from another sequence by deleting zero or more elements without changing the order of the remaining elements.

The LCS problem asks: Given two strings, `text1` and `text2`, what is the length of the longest sequence that appears in both strings in the same relative order? (The characters do not need to be contiguous).

## Building Intuition

**Why does LCS work with 2D DP?**

1. **Two Strings = Two Dimensions**: We need to track progress through both strings simultaneously. We use a 2D array where `dp[i][j]` represents the length of the LCS for the prefix of `text1` ending at index `i-1` and the prefix of `text2` ending at index `j-1`.

2. **The Core Insight**: At each pair of indices `(i, j)`, we compare the current characters `text1[i-1]` and `text2[j-1]`.
   - **If they match (`text1[i-1] == text2[j-1]`)**: We have found a new common character! This character extends the LCS we had before considering these two characters. So, `dp[i][j] = 1 + dp[i-1][j-1]`.
   - **If they don't match (`text1[i-1] != text2[j-1]`)**: The current characters cannot both be part of the LCS ending at these indices. The LCS must either not include `text1[i-1]` or not include `text2[j-1]`. We take the maximum of these two possibilities: `dp[i][j] = max(dp[i-1][j], dp[i][j-1])`.

3. **Subsequence vs. Substring**: Because LCS allows gaps (it's a subsequence, not a substring), when characters don't match, we *carry forward* the best LCS length we've found so far by taking the maximum of the adjacent cells. We do *not* reset the count to 0 (which is what we would do if we were looking for a contiguous substring).

4. **Space Optimization Insight**: To compute a cell `dp[i][j]`, we only need values from the current row `i` (`dp[i][j-1]`) and the previous row `i-1` (`dp[i-1][j]` and `dp[i-1][j-1]`). Therefore, we don't need the entire $O(M \times N)$ grid in memory at once; $O(\min(M, N))$ space is sufficient.

## Formal Recurrence Relation

Let $dp[i][j]$ be the length of the Longest Common Subsequence of the prefixes `text1[0...i-1]` and `text2[0...j-1]`.

**Base Case:**
- $dp[i][0] = 0$ for all $i \in [0, M]$ (LCS with an empty string is 0)
- $dp[0][j] = 0$ for all $j \in [0, N]$ (LCS with an empty string is 0)

**Recursive Step:**
For given lengths $i > 0$ and $j > 0$:

- If the characters match (`text1[i-1] == text2[j-1]`):
  $$dp[i][j] = 1 + dp[i-1][j-1]$$
- If the characters DO NOT match (`text1[i-1] != text2[j-1]`):
  $$dp[i][j] = \max(dp[i-1][j], dp[i][j-1])$$

**Result:**
$$dp[M][N]$$ where $M$ and $N$ are the lengths of `text1` and `text2`.

## Visual Walkthrough

Let's trace the LCS for `text1="abcde"`, `text2="ace"`.

```markdown
|     | ""  | a   | c   | e   |
|-----|-----|-----|-----|-----|
| ""  | [0] |  0  |  0  |  0  |
| a   |  0  | [1] |  1  |  1  |
| b   |  0  |  1  |  1  |  1  |
| c   |  0  |  1  | [2] |  2  |
| d   |  0  |  1  |  2  |  2  |
| e   |  0  |  1  |  2  | [3] |
```

- Match at ('a', 'a'): `dp[1][1] = dp[0][0] + 1 = 1`
- Mismatch at ('b', 'a'): `dp[2][1] = max(dp[1][1], dp[2][0]) = max(1, 0) = 1`
- Mismatch at ('b', 'c'): `dp[2][2] = max(dp[1][2], dp[2][1]) = max(1, 1) = 1`
- Match at ('c', 'c'): `dp[3][2] = dp[2][1] + 1 = 2`
- Match at ('e', 'e'): `dp[5][3] = dp[4][2] + 1 = 3`

Result is `dp[5][3] = 3`.

---

## Solutions

### 1. Top-Down (Memoization)

```python
def longest_common_subsequence_memo(text1: str, text2: str) -> int:
    """
    Top-Down Memoization approach.

    Time: O(M * N)
    Space: O(M * N) for memo dictionary and recursion stack
    """
    m, n = len(text1), len(text2)
    memo = {}

    def helper(i: int, j: int) -> int:
        # Base case: if either string is empty, LCS is 0
        if i == 0 or j == 0:
            return 0

        if (i, j) in memo:
            return memo[(i, j)]

        # If characters match, add 1 and move both pointers back
        if text1[i - 1] == text2[j - 1]:
            memo[(i, j)] = 1 + helper(i - 1, j - 1)
        else:
            # If no match, try skipping one char from either string and take max
            memo[(i, j)] = max(helper(i - 1, j), helper(i, j - 1))

        return memo[(i, j)]

    return helper(m, n)
```

### 2. Bottom-Up 2D DP

This is the standard, most intuitive way to write LCS.

```python
def longest_common_subsequence_2d(text1: str, text2: str) -> int:
    """
    Standard Bottom-Up 2D DP approach.

    Time: O(M * N)
    Space: O(M * N)
    """
    m, n = len(text1), len(text2)
    # dp[i][j] represents LCS of text1[0:i] and text2[0:j]
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i - 1] == text2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    return dp[m][n]
```

### 3. Space-Optimized Bottom-Up DP (1D Array)

Notice in the 2D approach that to compute row `i`, we only need the values from row `i` and row `i-1`. We can reduce the space complexity from $O(M \times N)$ to $O(N)$ by keeping track of just one row and a variable to represent the diagonal element (`dp[i-1][j-1]`).

```python
def longest_common_subsequence(text1: str, text2: str) -> int:
    """
    Space-optimized bottom-up DP using a 1D array.

    Time: O(M * N)
    Space: O(min(M, N)) - We can ensure we use the shorter string for the array
    """
    # Optimization: Ensure text2 is the shorter string to minimize space
    if len(text1) < len(text2):
        text1, text2 = text2, text1

    m, n = len(text1), len(text2)
    dp = [0] * (n + 1)

    for i in range(1, m + 1):
        prev_diagonal = 0 # Represents dp[i-1][0] which is 0
        for j in range(1, n + 1):
            # Save the value before we overwrite it (this is dp[i-1][j])
            temp = dp[j]

            if text1[i - 1] == text2[j - 1]:
                dp[j] = prev_diagonal + 1
            else:
                dp[j] = max(dp[j], dp[j - 1])

            # The old dp[i-1][j] (temp) becomes the new prev_diagonal (dp[i-1][j-1]) for the next iteration
            prev_diagonal = temp

    return dp[n]
```

---

## Reconstructing the LCS String

Finding the *length* of the LCS is one thing, but often you need the actual string. We can backtrack through the filled 2D `dp` table from `dp[m][n]` to `dp[0][0]`.

```python
def get_lcs_string(text1: str, text2: str) -> str:
    """
    Reconstructs the actual Longest Common Subsequence string.
    Time: O(M * N) to build table, O(M + N) to backtrack.
    Space: O(M * N)
    """
    m, n = len(text1), len(text2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # Build the DP table
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i - 1] == text2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    # Backtrack to find the LCS
    lcs_chars = []
    i, j = m, n

    while i > 0 and j > 0:
        if text1[i - 1] == text2[j - 1]:
            # Character belongs to LCS
            lcs_chars.append(text1[i - 1])
            i -= 1
            j -= 1
        elif dp[i - 1][j] > dp[i][j - 1]:
            # Value came from top
            i -= 1
        else:
            # Value came from left
            j -= 1

    # We backtracked from end to start, so reverse the result
    return "".join(reversed(lcs_chars))
```

---

## Common Variations & Applications

LCS is a foundational DP pattern. Many problems are just LCS in disguise or require minor tweaks to the recurrence relation.

### 1. Longest Common Substring
*Difference: The matching characters must be contiguous.*

If characters mismatch, the common substring breaks, so we **reset** the length to 0. We also need to keep track of the overall maximum length found anywhere in the table, as it won't necessarily be at `dp[m][n]`.

```python
def longest_common_substring(text1: str, text2: str) -> int:
    m, n = len(text1), len(text2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    max_len = 0

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i - 1] == text2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
                max_len = max(max_len, dp[i][j])
            else:
                dp[i][j] = 0 # Reset to 0 for substring!

    return max_len
```

### 2. Minimum ASCII Delete Sum for Two Strings
*Difference: Instead of maximizing length, we minimize ASCII sum of deleted characters.*

```python
def minimum_delete_sum(s1: str, s2: str) -> int:
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # Base cases: cost to delete all characters of the prefix
    for i in range(1, m + 1):
        dp[i][0] = dp[i-1][0] + ord(s1[i-1])
    for j in range(1, n + 1):
        dp[0][j] = dp[0][j-1] + ord(s2[j-1])

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                # Cost is same as before this char
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

**Insight:** The shortest common supersequence will include the Longest Common Subsequence *exactly once*, plus all the other characters from both strings.
Length = `len(str1) + len(str2) - len(LCS(str1, str2))`

To reconstruct the string, you perform a similar backtracking as LCS, but you append characters from `str1` or `str2` when moving up or left, and append the common character when moving diagonally.

### 4. Longest Palindromic Subsequence
*Problem: Find the longest subsequence of a string `s` that is a palindrome.*

**Insight:** This is secretly an LCS problem! The longest palindromic subsequence of `s` is simply the Longest Common Subsequence of `s` and `reverse(s)`.

```python
def longest_palindrome_subseq(s: str) -> int:
    return longest_common_subsequence(s, s[::-1])
```

### 5. Uncrossed Lines
*Problem: You are given two arrays `nums1` and `nums2`. You can draw uncrossed lines connecting `nums1[i]` and `nums2[j]` such that `nums1[i] == nums2[j]`. What is the maximum number of uncrossed lines?*

**Insight:** Because the lines cannot cross, the relative order of the matched elements must be preserved. This is literally just finding the Longest Common Subsequence of the two arrays.

```python
def max_uncrossed_lines(nums1: list[int], nums2: list[int]) -> int:
    # This is exactly the same code as LCS
    m, n = len(nums1), len(nums2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if nums1[i-1] == nums2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    return dp[m][n]
```

---

## When NOT to Use Standard LCS

1. **Need Contiguous Match:** Use the Longest Common Substring approach (resetting `dp[i][j]` to 0).
2. **Three or More Strings:** LCS for 3 strings requires $O(L \times M \times N)$ time and space via 3D DP, which becomes extremely slow for strings longer than ~100 characters.
3. **Very Long Strings ($10^5$+)**: $O(M \times N)$ will Time Out and Memory Out. In bioinformatics (e.g., DNA sequence alignment), specialized algorithms like Hunt-Szymanski or suffix tree approaches are used, or heuristics like BLAST.
4. **Edit Distance**: While related, Edit Distance (Levenshtein Distance) allows for substitutions, which standard LCS does not. If you have substitution costs, use the Edit Distance pattern.

## Summary

- **State:** `dp[i][j]` = length of LCS of `text1[0...i-1]` and `text2[0...j-1]`.
- **Match:** `dp[i][j] = 1 + dp[i-1][j-1]` (Move diagonally).
- **Mismatch:** `dp[i][j] = max(dp[i-1][j], dp[i][j-1])` (Move up or left).
- **Time / Space:** $O(M \times N)$ standard, $O(\min(M, N))$ space-optimized.
- **Pattern Recognition:** "Two sequences", "relative order matters", "can skip elements", "maximum length".

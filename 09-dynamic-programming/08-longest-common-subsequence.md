# Longest Common Subsequence

> **Prerequisites:** [07-2d-dp-basics](./07-2d-dp-basics.md)

## Interview Context

LCS is a classic because:

1. **Foundational string DP**: Template for many problems
2. **Real applications**: Diff tools, DNA sequence alignment
3. **Multiple variants**: Substring, editing, printing
4. **Space optimization**: 2D → 1D demonstration

---

## Problem Statement

Find the length of the longest subsequence common to both strings.

```
Input: text1 = "abcde", text2 = "ace"
Output: 3
Explanation: LCS is "ace"
```

---

## Solution

```python
def longest_common_subsequence(text1: str, text2: str) -> int:
    """
    Find length of longest common subsequence.

    State: dp[i][j] = LCS of text1[0..i-1] and text2[0..j-1]
    Recurrence:
        If match: dp[i][j] = dp[i-1][j-1] + 1
        Else: dp[i][j] = max(dp[i-1][j], dp[i][j-1])

    Time: O(m × n)
    Space: O(n)
    """
    m, n = len(text1), len(text2)
    dp = [0] * (n + 1)

    for i in range(1, m + 1):
        prev = 0  # dp[i-1][j-1]
        for j in range(1, n + 1):
            temp = dp[j]  # Save for next iteration
            if text1[i - 1] == text2[j - 1]:
                dp[j] = prev + 1
            else:
                dp[j] = max(dp[j], dp[j - 1])
            prev = temp

    return dp[n]
```

### 2D Version (Clearer)

```python
def lcs_2d(text1: str, text2: str) -> int:
    """
    2D DP version for clarity.

    Time: O(m × n)
    Space: O(m × n)
    """
    m, n = len(text1), len(text2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i - 1] == text2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    return dp[m][n]
```

---

## Visual Walkthrough

```
text1 = "abcde", text2 = "ace"

    ""  a  c  e
""   0  0  0  0
a    0  1  1  1
b    0  1  1  1
c    0  1  2  2
d    0  1  2  2
e    0  1  2  3

Match at (a,a): dp[1][1] = dp[0][0] + 1 = 1
Match at (c,c): dp[3][2] = dp[2][1] + 1 = 2
Match at (e,e): dp[5][3] = dp[4][2] + 1 = 3

Answer: 3
```

---

## Reconstructing the LCS

```python
def lcs_with_string(text1: str, text2: str) -> tuple[int, str]:
    """
    Return both length and the actual LCS.
    """
    m, n = len(text1), len(text2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i - 1] == text2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    # Backtrack to find LCS
    lcs = []
    i, j = m, n
    while i > 0 and j > 0:
        if text1[i - 1] == text2[j - 1]:
            lcs.append(text1[i - 1])
            i -= 1
            j -= 1
        elif dp[i - 1][j] > dp[i][j - 1]:
            i -= 1
        else:
            j -= 1

    return dp[m][n], ''.join(reversed(lcs))
```

---

## Related: Longest Common Substring

Contiguous, not subsequence.

```python
def longest_common_substring(text1: str, text2: str) -> int:
    """
    Longest CONTIGUOUS common substring.

    Difference: Reset to 0 if no match (can't skip characters).

    Time: O(m × n)
    Space: O(n)
    """
    m, n = len(text1), len(text2)
    dp = [0] * (n + 1)
    max_len = 0

    for i in range(1, m + 1):
        prev = 0
        for j in range(1, n + 1):
            temp = dp[j]
            if text1[i - 1] == text2[j - 1]:
                dp[j] = prev + 1
                max_len = max(max_len, dp[j])
            else:
                dp[j] = 0  # Reset, not max!
            prev = temp

    return max_len
```

---

## Related: Shortest Common Supersequence

```python
def shortest_common_supersequence(str1: str, str2: str) -> str:
    """
    Shortest string that has both str1 and str2 as subsequences.

    Length = len(str1) + len(str2) - LCS

    Time: O(m × n)
    Space: O(m × n)
    """
    m, n = len(str1), len(str2)

    # Build LCS table
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if str1[i - 1] == str2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    # Reconstruct supersequence
    result = []
    i, j = m, n

    while i > 0 and j > 0:
        if str1[i - 1] == str2[j - 1]:
            result.append(str1[i - 1])
            i -= 1
            j -= 1
        elif dp[i - 1][j] > dp[i][j - 1]:
            result.append(str1[i - 1])
            i -= 1
        else:
            result.append(str2[j - 1])
            j -= 1

    # Add remaining characters
    while i > 0:
        result.append(str1[i - 1])
        i -= 1
    while j > 0:
        result.append(str2[j - 1])
        j -= 1

    return ''.join(reversed(result))
```

---

## Related: Delete Operations for Two Strings

```python
def min_distance(word1: str, word2: str) -> int:
    """
    Minimum deletions to make strings equal.

    Answer = len(word1) + len(word2) - 2 * LCS

    Time: O(m × n)
    Space: O(n)
    """
    lcs = longest_common_subsequence(word1, word2)
    return len(word1) + len(word2) - 2 * lcs
```

---

## Related: Longest Repeating Subsequence

```python
def longest_repeating_subsequence(s: str) -> int:
    """
    Longest subsequence that appears at least twice.

    LCS of s with itself, but characters must be at different indices.

    Time: O(n²)
    Space: O(n)
    """
    n = len(s)
    dp = [0] * (n + 1)

    for i in range(1, n + 1):
        prev = 0
        for j in range(1, n + 1):
            temp = dp[j]
            if s[i - 1] == s[j - 1] and i != j:
                dp[j] = prev + 1
            else:
                dp[j] = max(dp[j], dp[j - 1])
            prev = temp

    return dp[n]
```

---

## LCS of Three Strings

```python
def lcs_of_three(s1: str, s2: str, s3: str) -> int:
    """
    LCS of three strings.

    Time: O(l × m × n)
    Space: O(m × n)
    """
    l, m, n = len(s1), len(s2), len(s3)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(1, l + 1):
        # Save previous layer
        prev_dp = [row[:] for row in dp]

        for j in range(1, m + 1):
            for k in range(1, n + 1):
                if s1[i - 1] == s2[j - 1] == s3[k - 1]:
                    dp[j][k] = prev_dp[j - 1][k - 1] + 1
                else:
                    dp[j][k] = max(
                        prev_dp[j][k],
                        dp[j - 1][k],
                        dp[j][k - 1]
                    )

    return dp[m][n]
```

---

## Edge Cases

```python
# 1. Empty string
text1 = "", text2 = "abc"
# LCS = 0

# 2. No common characters
text1 = "abc", text2 = "xyz"
# LCS = 0

# 3. One is subsequence of other
text1 = "abc", text2 = "aebdc"
# LCS = 3 ("abc")

# 4. Identical strings
text1 = "abc", text2 = "abc"
# LCS = 3

# 5. Single character
text1 = "a", text2 = "a"
# LCS = 1
```

---

## Common Mistakes

```python
# WRONG: Confusing substring with subsequence
if text1[i-1] == text2[j-1]:
    dp[i][j] = dp[i-1][j-1] + 1
else:
    dp[i][j] = 0  # This is for SUBSTRING!

# CORRECT for subsequence:
else:
    dp[i][j] = max(dp[i-1][j], dp[i][j-1])


# WRONG: Off-by-one in indexing
for i in range(m):  # Should be range(1, m+1)
    for j in range(n):
        if text1[i] == text2[j]:  # Indices wrong
```

---

## Complexity

| Problem | Time | Space |
|---------|------|-------|
| LCS (2 strings) | O(mn) | O(n) |
| LCS (3 strings) | O(lmn) | O(mn) |
| Longest Common Substring | O(mn) | O(n) |
| Shortest Common Supersequence | O(mn) | O(mn) |

---

## Interview Tips

1. **Start with 2D**: Easier to understand and debug
2. **Draw the table**: Visualize state transitions
3. **Know the variants**: Substring vs subsequence
4. **Reconstruction**: Often asked as follow-up
5. **Space optimize**: Mention even if not implemented

---

## Practice Problems

| # | Problem | Difficulty | Variant |
|---|---------|------------|---------|
| 1 | LCS | Medium | Classic |
| 2 | Longest Common Substring | Medium | Contiguous |
| 3 | Delete Operations | Medium | LCS application |
| 4 | Shortest Common Supersequence | Hard | Construct string |
| 5 | Uncrossed Lines | Medium | LCS disguised |

---

## Key Takeaways

1. **Match**: Extend from diagonal dp[i-1][j-1]
2. **No match**: Take max of excluding either char
3. **Substring vs Subsequence**: Reset vs max
4. **Reconstruction**: Backtrack through table
5. **Applications**: Diff, alignment, editing

---

## Next: [09-edit-distance.md](./09-edit-distance.md)

Learn Levenshtein distance and string transformation.

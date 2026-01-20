# Edit Distance

> **Prerequisites:** [08-longest-common-subsequence](./08-longest-common-subsequence.md)

## Overview

Edit Distance (Levenshtein Distance) measures the minimum number of single-character operations (insert, delete, replace) to transform one string into another.

## Building Intuition

**Why does Edit Distance need three operations?**

1. **Complete Transformation**: With only insert and delete, you can transform any string to any other. But replace makes it efficient—turning 'a' into 'b' is 1 operation, not 2 (delete 'a', insert 'b').

2. **The Recurrence Logic**: At position (i, j), we're converting word1[0..i-1] to word2[0..j-1]:
   - **Characters match**: No operation needed. Cost = dp[i-1][j-1].
   - **Characters differ**: Three choices, pick cheapest:
     - Delete from word1: Now convert word1[0..i-2] to word2[0..j-1]. Cost = dp[i-1][j] + 1.
     - Insert into word1: Add word2[j-1] to match. Now convert word1[0..i-1] to word2[0..j-2]. Cost = dp[i][j-1] + 1.
     - Replace: Change word1[i-1] to word2[j-1]. Cost = dp[i-1][j-1] + 1.

3. **Why Base Cases Matter**: Converting to empty string requires deleting all characters (dp[i][0] = i). Converting from empty requires inserting all (dp[0][j] = j).

4. **Relationship to LCS**: Edit Distance (delete + insert only) = m + n - 2×LCS. This shows LCS captures the "unchanging core" of both strings.

5. **Mental Model**: Imagine you're an editor with three keys: Delete, Insert, and Replace. You process word1 from left to right, making it match word2. At each position, you choose the key that minimizes total presses.

## Interview Context

Edit Distance (Levenshtein Distance) is essential because:

1. **Classic string DP**: Foundation for many problems
2. **Real applications**: Spell checkers, DNA alignment, diff tools
3. **Three operations**: Insert, delete, replace
4. **Interview favorite**: Meta, Google, Microsoft

---

## When NOT to Use Edit Distance

1. **Fuzzy Matching at Scale**: For searching millions of strings, Edit Distance is O(m×n) per comparison. Use BK-trees, Levenshtein automata, or embedding-based similarity instead.

2. **Operations Have Different Costs**: Standard Edit Distance assumes cost=1 for all operations. If insert costs differ from delete (e.g., keyboard distance), modify the DP accordingly.

3. **Block Operations Allowed**: If you can move/copy entire substrings (like text editors), Edit Distance doesn't model this. Use sequence alignment or diff algorithms.

4. **Only Need Approximate Answer**: For "is edit distance ≤ k" queries, you can prune the DP to only compute a diagonal band of width 2k+1, giving O(n×k) instead of O(m×n).

5. **Strings Are Similar (Low Distance Expected)**: When k is known to be small, use Ukkonen's algorithm or the band optimization for O(n×k) time.

**Recognize Edit Distance Pattern When:**
- Transform one string to another
- Operations: insert, delete, replace (with costs)
- Need minimum operations or similarity measure

---

## Problem Statement

Find minimum operations to convert word1 to word2.
Operations: insert, delete, or replace a character.

```
Input: word1 = "horse", word2 = "ros"
Output: 3
Explanation:
horse → rorse (replace 'h' with 'r')
rorse → rose (remove 'r')
rose → ros (remove 'e')
```

---

## Solution

```python
def min_distance(word1: str, word2: str) -> int:
    """
    Minimum edit distance (Levenshtein distance).

    State: dp[i][j] = min ops to convert word1[0..i-1] to word2[0..j-1]

    Recurrence:
        If match: dp[i][j] = dp[i-1][j-1]
        Else: dp[i][j] = 1 + min(
            dp[i-1][j],      # delete from word1
            dp[i][j-1],      # insert into word1
            dp[i-1][j-1]     # replace
        )

    Time: O(m × n)
    Space: O(n)
    """
    m, n = len(word1), len(word2)

    # dp[j] represents dp[i][j] in 2D version
    dp = list(range(n + 1))  # Base: converting "" to word2[0..j]

    for i in range(1, m + 1):
        prev = dp[0]  # dp[i-1][j-1]
        dp[0] = i     # Converting word1[0..i-1] to ""

        for j in range(1, n + 1):
            temp = dp[j]

            if word1[i - 1] == word2[j - 1]:
                dp[j] = prev
            else:
                dp[j] = 1 + min(dp[j], dp[j - 1], prev)

            prev = temp

    return dp[n]
```

### 2D Version (Clearer)

```python
def min_distance_2d(word1: str, word2: str) -> int:
    """
    2D DP version for clarity.
    """
    m, n = len(word1), len(word2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # Base cases
    for i in range(m + 1):
        dp[i][0] = i  # Delete all characters
    for j in range(n + 1):
        dp[0][j] = j  # Insert all characters

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i - 1] == word2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(
                    dp[i - 1][j],      # Delete
                    dp[i][j - 1],      # Insert
                    dp[i - 1][j - 1]   # Replace
                )

    return dp[m][n]
```

---

## Visual Walkthrough

```
word1 = "horse", word2 = "ros"

      ""  r  o  s
""     0  1  2  3
h      1  1  2  3
o      2  2  1  2
r      3  2  2  2
s      4  3  3  2
e      5  4  4  3

Operations (backtrack from dp[5][3]):
dp[5][3] = 3: 'e' ≠ 's' → came from dp[4][3] (delete 'e')
dp[4][3] = 2: 's' = 's' → came from dp[3][2] (match)
dp[3][2] = 2: 'r' ≠ 'o' → came from dp[2][2] (delete 'r')
dp[2][2] = 1: 'o' = 'o' → came from dp[1][1] (match)
dp[1][1] = 1: 'h' ≠ 'r' → came from dp[0][0] (replace 'h' → 'r')

Answer: 3
```

---

## Understanding the Operations

```
dp[i-1][j] + 1:   Delete from word1
                  "abc" → "ab" then convert to target

dp[i][j-1] + 1:   Insert into word1
                  "ab" → "abc" by inserting, matching target

dp[i-1][j-1] + 1: Replace in word1
                  "abc" → "adc" by replacing 'b' with 'd'
```

---

## Reconstructing the Edits

```python
def edit_distance_with_ops(word1: str, word2: str) -> tuple[int, list]:
    """
    Return min distance and list of operations.
    """
    m, n = len(word1), len(word2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i - 1] == word2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])

    # Backtrack to find operations
    ops = []
    i, j = m, n

    while i > 0 or j > 0:
        if i > 0 and j > 0 and word1[i - 1] == word2[j - 1]:
            i -= 1
            j -= 1
        elif i > 0 and j > 0 and dp[i][j] == dp[i - 1][j - 1] + 1:
            ops.append(f"Replace '{word1[i-1]}' with '{word2[j-1]}' at {i-1}")
            i -= 1
            j -= 1
        elif i > 0 and dp[i][j] == dp[i - 1][j] + 1:
            ops.append(f"Delete '{word1[i-1]}' at {i-1}")
            i -= 1
        else:
            ops.append(f"Insert '{word2[j-1]}' at {i}")
            j -= 1

    return dp[m][n], ops[::-1]
```

---

## Variant: One Edit Distance

```python
def is_one_edit_distance(s: str, t: str) -> bool:
    """
    Check if strings are exactly one edit apart.

    Time: O(n)
    Space: O(1)
    """
    m, n = len(s), len(t)

    if abs(m - n) > 1:
        return False

    if m > n:
        s, t = t, s
        m, n = n, m

    # Now m <= n
    for i in range(m):
        if s[i] != t[i]:
            if m == n:
                return s[i + 1:] == t[i + 1:]  # Replace
            else:
                return s[i:] == t[i + 1:]  # Insert/Delete

    return m + 1 == n  # Only valid if t is one longer
```

---

## Variant: Delete Operations Only

```python
def min_delete_distance(word1: str, word2: str) -> int:
    """
    Minimum deletions (from both) to make strings equal.

    Answer = m + n - 2 * LCS

    Time: O(m × n)
    Space: O(n)
    """
    m, n = len(word1), len(word2)
    dp = [0] * (n + 1)

    for i in range(1, m + 1):
        prev = 0
        for j in range(1, n + 1):
            temp = dp[j]
            if word1[i - 1] == word2[j - 1]:
                dp[j] = prev + 1
            else:
                dp[j] = max(dp[j], dp[j - 1])
            prev = temp

    lcs = dp[n]
    return m + n - 2 * lcs
```

---

## Variant: Different Operation Costs

```python
def weighted_edit_distance(word1: str, word2: str,
                            insert_cost: int = 1,
                            delete_cost: int = 1,
                            replace_cost: int = 1) -> int:
    """
    Edit distance with custom operation costs.
    """
    m, n = len(word1), len(word2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(m + 1):
        dp[i][0] = i * delete_cost
    for j in range(n + 1):
        dp[0][j] = j * insert_cost

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i - 1] == word2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = min(
                    dp[i - 1][j] + delete_cost,
                    dp[i][j - 1] + insert_cost,
                    dp[i - 1][j - 1] + replace_cost
                )

    return dp[m][n]
```

---

## Edge Cases

```python
# 1. Empty strings
word1 = "", word2 = "abc"
# Distance = 3 (insert a, b, c)

# 2. Same strings
word1 = "abc", word2 = "abc"
# Distance = 0

# 3. Completely different
word1 = "abc", word2 = "xyz"
# Distance = 3 (replace all)

# 4. One character
word1 = "a", word2 = "b"
# Distance = 1 (replace)

# 5. Anagrams
word1 = "abc", word2 = "cab"
# Distance = 2 (various ways)
```

---

## Common Mistakes

```python
# WRONG: Forgetting base cases
dp = [[0] * (n + 1) for _ in range(m + 1)]
# dp[i][0] and dp[0][j] are 0, but should be i and j!

# CORRECT:
for i in range(m + 1):
    dp[i][0] = i
for j in range(n + 1):
    dp[0][j] = j


# WRONG: Wrong min calculation
dp[i][j] = min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])  # Missing +1

# CORRECT:
dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])
```

---

## Relationship with LCS

```
Edit Distance with only insert/delete = m + n - 2 * LCS

Example: "abc" → "ace"
m = 3, n = 3, LCS = 2 (ac)
Delete distance = 3 + 3 - 2*2 = 2
```

---

## Complexity

| Variant | Time | Space |
|---------|------|-------|
| Standard | O(mn) | O(n) |
| With reconstruction | O(mn) | O(mn) |
| One edit check | O(n) | O(1) |
| Delete only (via LCS) | O(mn) | O(n) |

---

## Interview Tips

1. **Draw the DP table**: Helps visualization
2. **Explain operations**: Insert, delete, replace
3. **Know relationship with LCS**: Shows deeper understanding
4. **Handle edge cases**: Empty strings
5. **Space optimize**: Mention 1D array approach

---

## Practice Problems

| # | Problem | Difficulty | Variant |
|---|---------|------------|---------|
| 1 | Edit Distance | Medium | Classic |
| 2 | One Edit Distance | Medium | Boolean check |
| 3 | Delete Operations | Medium | LCS-based |
| 4 | Min ASCII Delete Sum | Medium | Weighted delete |
| 5 | Distinct Subsequences | Hard | Count variations |

---

## Key Takeaways

1. **Three operations**: Insert, delete, replace (each cost 1)
2. **Base cases matter**: Converting to/from empty string
3. **Match = no cost**: Take diagonal value
4. **No match = min + 1**: Choose best operation
5. **Space optimizable**: Only need previous row

---

## Next: [10-knapsack-01.md](./10-knapsack-01.md)

Learn the 0/1 Knapsack pattern.

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

3. **Why Base Cases Matter**: `dp[i][0]` represents converting a string of length $i$ to an empty string. The *only* way to do this is to delete all $i$ characters. Thus, `dp[i][0] = i`. Similarly, converting an empty string to a string of length $j$ requires inserting all $j$ characters, so `dp[0][j] = j`.

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
   *Counter-example:* "Find closest spelling correction from dictionary of 100,000 words." Standard $O(M \times N)$ DP for each word is too slow; Trie + Levenshtein automaton is strictly better.

2. **Operations Have Different Costs**: Standard Edit Distance assumes cost=1 for all operations. If insert costs differ from delete (e.g., keyboard distance), modify the DP accordingly.
   *Counter-example:* "Minimum ASCII Delete Sum for Two Strings." Replacing a character is not a standard operation, and the cost of deletion varies based on ASCII value. Modify the state transition to add ASCII values instead of just `+1`.

3. **Block Operations Allowed**: If you can move/copy entire substrings (like text editors), Edit Distance doesn't model this. Use sequence alignment or diff algorithms.

4. **Only Need Approximate Answer**: For "is edit distance ≤ k" queries, you can prune the DP to only compute a diagonal band of width 2k+1, giving O(n×k) instead of O(m×n).
   *Counter-example:* "Are these two strings one edit apart?" Using full $O(M \times N)$ DP is overkill. Just use two pointers in $O(N)$ time.

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

## Formal Recurrence Relation

Let $dp[i][j]$ be the minimum number of operations required to convert the prefix `word1[0...i-1]` to the prefix `word2[0...j-1]`.

**Base Cases:**
$dp[i][0] = i$ for all $i \in [0, m]$ (deleting $i$ characters to reach an empty string)
$dp[0][j] = j$ for all $j \in [0, n]$ (inserting $j$ characters to reach a string of length $j$)

**Recursive Step:**
If characters match (`word1[i-1] == word2[j-1]`):
$$dp[i][j] = dp[i-1][j-1]$$
*(No operation needed, carry over the cost from the prefixes before these characters)*

If characters DO NOT match:
$$dp[i][j] = 1 + \min(dp[i-1][j], \quad dp[i][j-1], \quad dp[i-1][j-1])$$
- $dp[i-1][j]$ represents **Deleting** `word1[i-1]`
- $dp[i][j-1]$ represents **Inserting** `word2[j-1]` into `word1`
- $dp[i-1][j-1]$ represents **Replacing** `word1[i-1]` with `word2[j-1]`

**Result:**
$$dp[m][n]$$ where $m$ and $n$ are the lengths of `word1` and `word2`.

---

## Solution

### Top-Down (Memoization)

```python
def min_distance_memo(word1: str, word2: str) -> int:
    """
    Top-Down Memoization approach.

    Time: O(m × n)
    Space: O(m × n) for memo array and recursion stack
    """
    m, n = len(word1), len(word2)
    memo = {}

    def helper(i: int, j: int) -> int:
        # Base cases
        if i == 0: return j  # Insert all remaining characters of word2
        if j == 0: return i  # Delete all remaining characters of word1

        if (i, j) in memo:
            return memo[(i, j)]

        if word1[i - 1] == word2[j - 1]:
            memo[(i, j)] = helper(i - 1, j - 1)
        else:
            memo[(i, j)] = 1 + min(
                helper(i - 1, j),      # Delete
                helper(i, j - 1),      # Insert
                helper(i - 1, j - 1)   # Replace
            )

        return memo[(i, j)]

    return helper(m, n)
```

### Bottom-Up 2D DP (Clearer)

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

### Bottom-Up with Space Optimization

**Space Optimization Logic:** Similar to LCS, calculating $dp[i][j]$ requires only the current row $dp[i][...]$ and the previous row $dp[i-1][...]$. By iterating through the columns and carefully managing a `prev_diagonal` variable (which holds $dp[i-1][j-1]$), we can compute the entire matrix using a single 1D array, reducing space complexity from $O(M \times N)$ to $O(N)$.

```python
def min_distance(word1: str, word2: str) -> int:
    """
    Minimum edit distance (Levenshtein distance).
    Space-optimized bottom-up DP.

    Time: O(m × n)
    Space: O(n)
    """
    m, n = len(word1), len(word2)

    # dp_row represents the current row of the DP table
    # Base case: converting "" to word2[0..j] requires j insertions
    dp_row = list(range(n + 1))

    for i in range(1, m + 1):
        # prev_diagonal represents dp[i-1][j-1].
        # Before we process column 1, dp[i-1][0] is just `dp_row[0]`.
        prev_diagonal = dp_row[0]

        # Base case for the new row: converting word1[0..i] to "" requires i deletions
        dp_row[0] = i

        for j in range(1, n + 1):
            temp = dp_row[j] # Save dp[i-1][j] before overwriting

            if word1[i - 1] == word2[j - 1]:
                dp_row[j] = prev_diagonal
            else:
                dp_row[j] = 1 + min(
                    temp,            # Delete: dp[i-1][j]
                    dp_row[j - 1],   # Insert: dp[i][j-1]
                    prev_diagonal    # Replace: dp[i-1][j-1]
                )

            prev_diagonal = temp # The old dp[i-1][j] becomes the diagonal for j+1

    return dp_row[n]
```

---

## Visual Walkthrough

**Edit Distance Grid for `word1="horse"`, `word2="ros"`:**

```markdown
|     | ""  | r   | o   | s   |
|-----|-----|-----|-----|-----|
| ""  | [0] | [1] | [2] | [3] |
| h   | [1] | [1] | [2] | [3] |
| o   | [2] | [2] | [1] | [2] |
| r   | [3] | [2] | [2] | [2] |
| s   | [4] | [3] | [3] | [2] |
| e   | [5] | [4] | [4] | [3] |
```

Operations (backtrack from `dp[5][3]`):
- `dp[5][3] = 3`: 'e' ≠ 's' → came from `dp[4][3]` (delete 'e')
- `dp[4][3] = 2`: 's' = 's' → came from `dp[3][2]` (match)
- `dp[3][2] = 2`: 'r' ≠ 'o' → came from `dp[2][2]` (delete 'r')
- `dp[2][2] = 1`: 'o' = 'o' → came from `dp[1][1]` (match)
- `dp[1][1] = 1`: 'h' ≠ 'r' → came from `dp[0][0]` (replace 'h' → 'r')

Answer: 3

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

| Variant               | Time  | Space |
| --------------------- | ----- | ----- |
| Standard              | O(mn) | O(n)  |
| With reconstruction   | O(mn) | O(mn) |
| One edit check        | O(n)  | O(1)  |
| Delete only (via LCS) | O(mn) | O(n)  |

---

## Interview Tips

1. **Draw the DP table**: Helps visualization
2. **Explain operations**: Insert, delete, replace
3. **Know relationship with LCS**: Shows deeper understanding
4. **Handle edge cases**: Empty strings
5. **Space optimize**: Mention 1D array approach

---

## Practice Problems

| #   | Problem               | Difficulty | Variant          |
| --- | --------------------- | ---------- | ---------------- |
| 1   | Edit Distance         | Medium     | Classic          |
| 2   | One Edit Distance     | Medium     | Boolean check    |
| 3   | Delete Operations     | Medium     | LCS-based        |
| 4   | Min ASCII Delete Sum  | Medium     | Weighted delete  |
| 5   | Distinct Subsequences | Hard       | Count variations |

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

# Edit Distance (Levenshtein Distance)

> **Prerequisites:** [08-longest-common-subsequence](./08-longest-common-subsequence.md)

## Overview

Edit Distance (Levenshtein Distance) measures the minimum number of single-character operations (insert, delete, replace) required to transform one string into another. It is the fundamental problem for string matching, spell checking, and computational biology (DNA sequence alignment).

## Building Intuition

Imagine transforming `word1` into `word2` by scanning both strings from left to right. At each step, comparing prefixes `word1[0...i-1]` and `word2[0...j-1]`, you have choices:

1. **Why three operations?**
   With only *insert* and *delete*, you can transform any string to any other. But *replace* acts as a shortcut. Turning 'a' into 'b' takes 1 *replace* operation instead of 2 (delete 'a', then insert 'b').

2. **The Recurrence Logic (The Prefix Approach)**
   - **If the last characters match (`word1[i-1] == word2[j-1]`)**:
     No new operations are needed for these characters. The cost is simply the cost of transforming the remaining prefixes: `dp[i-1][j-1]`.
   - **If the last characters DO NOT match**:
     We must perform exactly 1 operation to fix the mismatch. We try all three possibilities and take the minimum:
     - **Replace**: Change `word1[i-1]` to `word2[j-1]`. Now they match. Cost = `1 + dp[i-1][j-1]`.
     - **Delete**: Remove `word1[i-1]`. We still need to match the remaining `word1` prefix with the current `word2` prefix. Cost = `1 + dp[i-1][j]`.
     - **Insert**: Insert `word2[j-1]` at the end of `word1`. Now the ends match. We still need to match the current `word1` prefix with the remaining `word2` prefix. Cost = `1 + dp[i][j-1]`.

3. **Base Cases (Empty Strings)**
   Converting an empty string to a string of length $j$ requires exactly $j$ insertions. Converting a string of length $i$ to an empty string requires exactly $i$ deletions.

## Problem Statement

Find the minimum operations to convert `word1` to `word2`.
Operations allowed: insert, delete, or replace a character.

```text
Input: word1 = "horse", word2 = "ros"
Output: 3
Explanation:
horse → rorse (replace 'h' with 'r')
rorse → rose (remove 'r')
rose → ros (remove 'e')
```

---

## Formal Recurrence Relation

Let $dp[i][j]$ be the minimum number of operations to convert `word1[0...i-1]` to `word2[0...j-1]`.

**Base Cases:**
$dp[i][0] = i$ for all $i \in [0, m]$ (deleting $i$ characters)
$dp[0][j] = j$ for all $j \in [0, n]$ (inserting $j$ characters)

**Recursive Step:**
If `word1[i-1] == word2[j-1]`:
$$dp[i][j] = dp[i-1][j-1]$$

If `word1[i-1] \neq word2[j-1]`:
$$dp[i][j] = 1 + \min(dp[i-1][j], \quad dp[i][j-1], \quad dp[i-1][j-1])$$
*(Delete, Insert, Replace respectively)*

**Result:**
$$dp[m][n]$$

---

## Solutions

### 1. Top-Down (Memoization)

```python
def min_distance_memo(word1: str, word2: str) -> int:
    """
    Top-Down Memoization approach.

    Time: O(m * n)
    Space: O(m * n) for memo dictionary and recursion stack
    """
    m, n = len(word1), len(word2)
    memo = {}

    def helper(i: int, j: int) -> int:
        # Base cases
        if i == 0: return j  # Insert remaining characters
        if j == 0: return i  # Delete remaining characters

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

### 2. Bottom-Up 2D DP (Clearer)

```python
def min_distance_2d(word1: str, word2: str) -> int:
    """
    2D DP version for clarity.

    Time: O(m * n)
    Space: O(m * n)
    """
    m, n = len(word1), len(word2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # Base cases
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j

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

### 3. Bottom-Up with Space Optimization (Best)

**Optimization Logic:**
To calculate $dp[i][j]$, we only need values from the current row $dp[i][...]$ and the previous row $dp[i-1][...]$. By maintaining a 1D array and a `prev_diagonal` variable (which holds $dp[i-1][j-1]$), we drop the space complexity to $O(N)$.
*Bonus:* We can ensure $O(\min(M, N))$ space by swapping `word1` and `word2` so the columns correspond to the shorter string.

```python
def min_distance(word1: str, word2: str) -> int:
    """
    Minimum edit distance (Levenshtein distance).
    Space-optimized bottom-up DP.

    Time: O(m * n)
    Space: O(min(m, n))
    """
    # Swap to ensure word2 is the shorter string for O(min(m, n)) space
    if len(word1) < len(word2):
        word1, word2 = word2, word1

    m, n = len(word1), len(word2)

    # dp_row represents the current row of the DP table
    dp_row = list(range(n + 1))

    for i in range(1, m + 1):
        # prev_diagonal represents dp[i-1][j-1]
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

---

## When NOT to Use Edit Distance

Recognizing when standard Edit Distance is the *wrong* tool is a crucial senior engineer signal.

1. **Fuzzy Matching at Scale**: For searching millions of strings, $O(M \times N)$ per comparison is too slow.
   *Use Instead:* BK-trees, Levenshtein automata, or embedding-based vector search.
2. **Operations Have Variable Costs**: Standard Edit Distance assumes `cost=1` for all operations. If insert costs differ from delete (e.g., keyboard distance), modify the state transition to add custom values instead of just `+1`.
3. **Block Operations Allowed**: If you can move/copy entire substrings (like a text editor), standard DP won't model this.
   *Use Instead:* Sequence alignment algorithms or diff algorithms (like Myers' diff algorithm).
4. **Only Need Approximate Answer**: For "is edit distance ≤ k" queries, you can prune the DP to compute only a diagonal band of width $2k+1$, dropping complexity to $O(N \times K)$.
   *Counter-example:* "Are these two strings one edit apart?" Just use a two-pointer approach in $O(N)$ time.

---

## Variants

### 1. One Edit Distance
Check if two strings are exactly one edit apart. Overkill to use full DP; use two pointers instead.

```python
def is_one_edit_distance(s: str, t: str) -> bool:
    """
    Time: O(n), Space: O(1)
    """
    m, n = len(s), len(t)
    if abs(m - n) > 1:
        return False

    if m > n:  # Ensure s is the shorter string
        s, t = t, s
        m, n = n, m

    for i in range(m):
        if s[i] != t[i]:
            if m == n:
                return s[i + 1:] == t[i + 1:]  # Replace case
            else:
                return s[i:] == t[i + 1:]      # Insert case (into shorter string)

    return m + 1 == n  # True if exactly one char appended
```

### 2. Delete Operations Only
Find minimum deletions (from both strings) to make them equal.
*Insight*: The characters that *aren't* deleted form the Longest Common Subsequence (LCS).
Answer = Length(word1) + Length(word2) - 2 * Length(LCS).

```python
def min_delete_distance(word1: str, word2: str) -> int:
    """
    Time: O(m * n), Space: O(n)
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

### 3. Reconstructing the Edits
We can backtrack through our DP table to find the actual list of operations.

```python
def get_edit_operations(word1: str, word2: str) -> list[str]:
    # ... (Assume dp table is built using 2D DP) ...
    ops = []
    i, j = m, n

    while i > 0 or j > 0:
        if i > 0 and j > 0 and word1[i - 1] == word2[j - 1]:
            i -= 1; j -= 1
        elif i > 0 and j > 0 and dp[i][j] == dp[i - 1][j - 1] + 1:
            ops.append(f"Replace '{word1[i-1]}' with '{word2[j-1]}' (at pos {i-1})")
            i -= 1; j -= 1
        elif i > 0 and dp[i][j] == dp[i - 1][j] + 1:
            ops.append(f"Delete '{word1[i-1]}' (at pos {i-1})")
            i -= 1
        else:
            ops.append(f"Insert '{word2[j-1]}' (after pos {i-1})")
            j -= 1

    return ops[::-1]
```
*(Note: Position indices reflect original `word1` string before applying any mutations)*

### 4. Different Operation Costs
Sometimes, insert, delete, and replace operations have different associated costs.

```python
def weighted_edit_distance(word1: str, word2: str,
                           insert_cost: int = 1,
                           delete_cost: int = 1,
                           replace_cost: int = 1) -> int:
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

## Complexity Profile

| Approach | Time | Space | Notes |
| :--- | :--- | :--- | :--- |
| **Top-Down Memoization** | $O(M \times N)$ | $O(M \times N)$ | High recursion overhead |
| **Bottom-Up 2D DP** | $O(M \times N)$ | $O(M \times N)$ | Best for visualization/backtracking |
| **Bottom-Up 1D DP** | $O(M \times N)$ | $O(\min(M, N))$ | **Optimal.** Swap strings to minimize space |

---

## Edge Cases to Consider
When solving sequence alignment problems, immediately test your logic against these core edge cases:
- **Empty strings**: `word1 = "", word2 = "abc"` → Distance 3 (Insert all).
- **Identical strings**: `word1 = "abc", word2 = "abc"` → Distance 0.
- **Completely distinct**: `word1 = "abc", word2 = "xyz"` → Distance 3 (Replace all).
- **Single character mismatch**: `word1 = "a", word2 = "b"` → Distance 1 (Replace).
- **Anagrams**: `word1 = "abc", word2 = "cab"` → Distance 2 (Delete and Insert).

---

## Common Mistakes

1. **Forgetting Base Cases**:
   Initializing the matrix with all `0`s instead of $i$ and $j$ for the first row and column. `dp[i][0]` must be $i$, because converting a string of length $i$ to an empty string takes $i$ deletions.
2. **Missing `+1` in Transition**:
   `dp[i][j] = min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])` is wrong. You are performing an operation, so it costs `1 + min(...)`.
3. **Array Out of Bounds**:
   When indexing `word1[i-1]` and `word2[j-1]`, ensure $i$ and $j$ loop from $1$ to $m$ and $n$ respectively.

---

## Interview Tips
- Always point out the space optimization ($O(M \times N) \rightarrow O(\min(M, N))$). Showing that you know to swap the variables so the inner loop runs over the shorter string is a massive "hire" signal.
- Know the relationship between Edit Distance and Longest Common Subsequence (LCS).
- Understand why dynamic programming is superior to pure recursion ($O(3^{\max(m, n)})$ bounds without memoization).

## Next: [10-knapsack-01.md](./10-knapsack-01.md)

Learn the 0/1 Knapsack pattern.

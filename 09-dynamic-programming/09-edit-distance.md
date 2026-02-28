# Edit Distance (Levenshtein Distance)

> **Prerequisites:** [08-longest-common-subsequence](./08-longest-common-subsequence.md)

## Overview

Edit Distance (Levenshtein Distance) measures the minimum number of single-character operations (insert, delete, replace) required to transform one string into another. It is the foundational problem for string matching algorithms, spell checking, fuzzy search, and computational biology (DNA sequence alignment).

## Building Intuition

Imagine transforming `word1` into `word2` by scanning both strings from left to right. At each step, we compare prefixes of the strings: `word1[0...i-1]` (length $i$) and `word2[0...j-1]` (length $j$).

1. **Why three operations?**
   With only *insert* and *delete*, you can transform any string to any other. But *replace* acts as an optimal shortcut. Turning 'a' into 'b' takes 1 *replace* operation instead of 2 operations (delete 'a', then insert 'b').

2. **The Recurrence Logic (The Prefix Approach)**
   Let's say we know the optimal way to transform all smaller prefixes. Now we are looking at the $i$-th character of `word1` and the $j$-th character of `word2`.

   - **If the last characters match (`word1[i-1] == word2[j-1]`)**:
     Hooray! No new operations are needed for these specific characters. The cost is simply whatever it cost to transform the remaining prefixes before them: `dp[i-1][j-1]`.

   - **If the last characters DO NOT match (`word1[i-1] != word2[j-1]`)**:
     We must perform exactly 1 operation to fix the mismatch at the end. We try all three possibilities and take the minimum:

     - **Replace**: We change `word1[i-1]` to exactly match `word2[j-1]`. Now the last characters match. The remaining problem is transforming the prefixes before them.
       *Cost* = `1 + dp[i-1][j-1]`
     - **Delete**: We delete `word1[i-1]`. Now we still need to form the entire prefix `word2[0...j-1]` using the remaining part of `word1[0...i-2]`.
       *Cost* = `1 + dp[i-1][j]`
     - **Insert**: We insert a character matching `word2[j-1]` at the end of `word1`. Now the ends match. We still need to form the remaining prefix `word2[0...j-2]` using all of `word1[0...i-1]`.
       *Cost* = `1 + dp[i][j-1]`

3. **Base Cases (Empty Strings)**
   - Converting an empty string to a string of length $j$ requires exactly $j$ insertions.
   - Converting a string of length $i$ to an empty string requires exactly $i$ deletions.

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

Let $dp[i][j]$ be the minimum number of operations to convert `word1[0...i-1]` (a prefix of length $i$) to `word2[0...j-1]` (a prefix of length $j$).

**Base Cases:**
- $dp[i][0] = i$ for all $i \in [0, m]$ (deleting $i$ characters to match an empty string)
- $dp[0][j] = j$ for all $j \in [0, n]$ (inserting $j$ characters to build a string from an empty string)

**Recursive Step:**
If `word1[i-1] == word2[j-1]`:
$$dp[i][j] = dp[i-1][j-1]$$

If `word1[i-1] \neq word2[j-1]`:
$$dp[i][j] = 1 + \min\begin{cases}
dp[i-1][j] & \text{(Delete from word1)} \\
dp[i][j-1] & \text{(Insert into word1)} \\
dp[i-1][j-1] & \text{(Replace in word1)}
\end{cases}$$

**Result:**
$$dp[m][n]$$ (where $m$ is the length of `word1` and $n$ is the length of `word2`)

---

## Solutions

### 1. Top-Down (Memoization)

The top-down approach is intuitive because it directly translates the recurrence relation. We use indices representing the *length* of the prefixes being compared.

```python
def min_distance_memo(word1: str, word2: str) -> int:
    """
    Top-Down Memoization approach for Edit Distance.

    Time: O(m * n)
    Space: O(m * n) for memoization dictionary and recursion stack
    """
    m, n = len(word1), len(word2)
    memo = {}

    def dfs(i: int, j: int) -> int:
        # Base cases: if one string is empty, operation count is the length of the other
        if i == 0: return j  # Need j insertions
        if j == 0: return i  # Need i deletions

        if (i, j) in memo:
            return memo[(i, j)]

        # If characters match, no operations needed for this position
        if word1[i - 1] == word2[j - 1]:
            memo[(i, j)] = dfs(i - 1, j - 1)
        else:
            # If they don't match, try all 3 operations and find the minimum
            memo[(i, j)] = 1 + min(
                dfs(i - 1, j),      # Delete from word1
                dfs(i, j - 1),      # Insert into word1
                dfs(i - 1, j - 1)   # Replace in word1
            )

        return memo[(i, j)]

    return dfs(m, n)
```

### 2. Bottom-Up 2D DP (Tabulation)

Building the matrix from the bottom up is the standard way to solve this problem iteratively. It avoids recursion overhead and makes reconstructing the actual edits easier.

```python
def min_distance_2d(word1: str, word2: str) -> int:
    """
    2D Tabulation DP approach for Edit Distance.

    Time: O(m * n)
    Space: O(m * n)
    """
    m, n = len(word1), len(word2)

    # dp[i][j] means min operations to convert word1[0...i-1] to word2[0...j-1]
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # Initialize Base Cases
    # Converting any string of length i to an empty string takes i deletions
    for i in range(m + 1):
        dp[i][0] = i

    # Converting an empty string to any string of length j takes j insertions
    for j in range(n + 1):
        dp[0][j] = j

    # Fill the DP table
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i - 1] == word2[j - 1]:
                # Characters match, inherit the cost from the diagonal
                dp[i][j] = dp[i - 1][j - 1]
            else:
                # Characters differ, take 1 + min of left, top, and diagonal
                dp[i][j] = 1 + min(
                    dp[i - 1][j],      # Delete: look up (dp[i-1][j])
                    dp[i][j - 1],      # Insert: look left (dp[i][j-1])
                    dp[i - 1][j - 1]   # Replace: look top-left diagonal (dp[i-1][j-1])
                )

    return dp[m][n]
```

### 3. Bottom-Up 1D DP (Space Optimized)

**The Optimization Logic:**
If you look closely at the 2D matrix transition:
`dp[i][j]` only ever depends on:
1. `dp[i-1][j]` (same column, previous row)
2. `dp[i][j-1]` (previous column, current row)
3. `dp[i-1][j-1]` (previous column, previous row - the diagonal)

Since we only need the *current* row and the *previous* row, we can reduce the space to $O(N)$ by keeping just one 1D array representing the current row.

The trickiest part is tracking the `dp[i-1][j-1]` (diagonal) value, because as we iterate through the 1D array and overwrite it, we lose the previous row's value. We solve this by keeping a scalar variable `prev_diagonal` that stores this value before it gets overwritten.

*Pro-Tip:* We can guarantee $O(\min(M, N))$ space complexity by ensuring the 1D array length corresponds to the shorter string. We do this by swapping `word1` and `word2` if necessary.

```python
def min_distance(word1: str, word2: str) -> int:
    """
    Space-optimized bottom-up DP for Edit Distance.

    Time: O(m * n)
    Space: O(min(m, n))
    """
    # Ensure word2 is the shorter string to optimize space
    if len(word1) < len(word2):
        word1, word2 = word2, word1

    m, n = len(word1), len(word2)

    # dp[j] represents the minimum operations to convert word1[0...i] to word2[0...j]
    # Initialize the first row (converting "" to word2[0...j])
    dp = list(range(n + 1))

    for i in range(1, m + 1):
        # The first element of the new row represents converting word1[0...i] to ""
        # So it takes i deletions.
        # prev_diagonal will initially hold the previous row's dp[0] (which is i - 1)
        prev_diagonal = dp[0]
        dp[0] = i

        for j in range(1, n + 1):
            # Save the current dp[j] (from the previous row) before overwriting it.
            # This becomes the diagonal (prev_diagonal) for the next column (j + 1).
            temp = dp[j]

            if word1[i - 1] == word2[j - 1]:
                # Characters match: cost is the diagonal value
                dp[j] = prev_diagonal
            else:
                # Characters differ: 1 + min(delete, insert, replace)
                dp[j] = 1 + min(
                    dp[j],            # Delete (from previous row above)
                    dp[j - 1],        # Insert (from current row left)
                    prev_diagonal     # Replace (from previous row diagonal)
                )

            # Update prev_diagonal for the next iteration
            prev_diagonal = temp

    return dp[n]
```

---

## Visual Walkthrough

Let's build the Edit Distance matrix for `word1="horse"`, `word2="ros"`.

```text
|     | ""  | r   | o   | s   |
|-----|-----|-----|-----|-----|
| ""  |  0  |  1  |  2  |  3  |
| h   |  1  |  1  |  2  |  3  |
| o   |  2  |  2  |  1  |  2  |
| r   |  3  |  2  |  2  |  2  |
| s   |  4  |  3  |  3  |  2  |
| e   |  5  |  4  |  4  |  3  |
```

**Traceback (How we got `dp[5][3] = 3`):**
Starting at the bottom right `(5, 3)`:
- `dp[5][3] = 3`: 'e' ≠ 's'. The minimum neighbor is `dp[4][3]` (value 2). Moving UP means **delete** 'e'.
- `dp[4][3] = 2`: 's' == 's'. We move diagonally UP-LEFT for free.
- `dp[3][2] = 2`: 'r' ≠ 'o'. The minimum neighbor is `dp[2][2]` (value 1). Moving UP means **delete** 'r'.
- `dp[2][2] = 1`: 'o' == 'o'. We move diagonally UP-LEFT for free.
- `dp[1][1] = 1`: 'h' ≠ 'r'. The minimum neighbor is `dp[0][0]` (value 0). Moving DIAGONALLY means **replace** 'h' with 'r'.
- We reach `dp[0][0]`, cost is 0. Total cost = 1 (delete) + 1 (delete) + 1 (replace) = 3 operations.

---

## When NOT to Use Edit Distance

Recognizing when standard Edit Distance is the *wrong* tool is a crucial senior engineer signal.

1. **Fuzzy Matching at Scale**: For searching millions of strings (e.g., a dictionary app), $O(M \times N)$ per comparison is far too slow.
   *Use Instead:* BK-trees, Levenshtein automata, or trigram-based indices.
2. **Operations Have Variable Costs**: Standard Edit Distance assumes `cost=1` for all operations. If insert costs differ from delete (e.g., accounting for keyboard layout distances in a spell-checker), you must modify the state transition to add custom values instead of just `+1`.
3. **Block Operations Allowed**: If you can move/copy entire substrings (like copy-pasting in a text editor), standard DP won't model this efficiently.
   *Use Instead:* Sequence alignment algorithms or diff algorithms (like Myers' diff algorithm).
4. **Only Need Approximate Answer**: For "is edit distance $\le K$" queries (where $K$ is small), you can prune the DP to compute only a diagonal band of width $2K+1$, dropping complexity from $O(M \times N)$ to $O(N \times K)$.
   *Counter-example:* "Are these two strings one edit apart?" Never use DP for this; use a two-pointer approach in $O(N)$ time.

---

## Variants

### 1. Reconstructing the Edits (The Backtrack)
We can backtrack through our full 2D DP table to find the actual sequence of operations. This is heavily used in standard diff tools.

```python
def get_edit_operations(word1: str, word2: str) -> list[str]:
    """
    Returns the sequence of operations to convert word1 to word2.
    """
    m, n = len(word1), len(word2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # Build the DP table (same as min_distance_2d)
    for i in range(m + 1): dp[i][0] = i
    for j in range(n + 1): dp[0][j] = j
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i - 1] == word2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])

    ops = []
    i, j = m, n

    # Backtrack from bottom-right to top-left
    while i > 0 or j > 0:
        if i > 0 and j > 0 and word1[i - 1] == word2[j - 1]:
            # Characters matched, no operation
            i -= 1
            j -= 1
        else:
            # Find which operation gave us the minimum cost to get to dp[i][j]
            # Prioritize Replace, then Delete, then Insert (arbitrary tie-breaking)
            if i > 0 and j > 0 and dp[i][j] == dp[i - 1][j - 1] + 1:
                ops.append(f"Replace '{word1[i-1]}' with '{word2[j-1]}'")
                i -= 1
                j -= 1
            elif i > 0 and dp[i][j] == dp[i - 1][j] + 1:
                ops.append(f"Delete '{word1[i-1]}'")
                i -= 1
            else:
                ops.append(f"Insert '{word2[j-1]}'")
                j -= 1

    # Operations were found backwards, so reverse them
    return ops[::-1]
```

### 2. Delete Operations Only
Find the minimum deletions (from *both* strings) to make them equal.
*Insight*: The characters that *aren't* deleted form the Longest Common Subsequence (LCS). The shortest path to equality is leaving the LCS intact and deleting everything else.
*Answer* = `Length(word1) + Length(word2) - 2 * Length(LCS)`

```python
def min_delete_distance(word1: str, word2: str) -> int:
    """
    Finds minimum deletions to make word1 and word2 identical.
    Time: O(m * n), Space: O(min(m, n))
    """
    m, n = len(word1), len(word2)
    if m < n:
        word1, word2 = word2, word1
        m, n = n, m

    # Standard 1D Space-Optimized LCS DP
    dp = [0] * (n + 1)

    for i in range(1, m + 1):
        prev_diagonal = 0
        for j in range(1, n + 1):
            temp = dp[j]
            if word1[i - 1] == word2[j - 1]:
                dp[j] = prev_diagonal + 1
            else:
                dp[j] = max(dp[j], dp[j - 1])
            prev_diagonal = temp

    lcs_length = dp[n]

    # Calculate total deletions needed
    return m + n - 2 * lcs_length
```

### 3. One Edit Distance
Check if two strings are exactly one edit apart. Using full $O(M \times N)$ DP is massive overkill; use two pointers instead.

```python
def is_one_edit_distance(s: str, t: str) -> bool:
    """
    Checks if s and t are exactly 1 edit distance apart.
    Time: O(N), Space: O(1)
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
                # Same length: must be a replace operation. Rest of string must match.
                return s[i + 1:] == t[i + 1:]
            else:
                # Different length: must be an insert operation into the shorter string (s).
                # Rest of s must match the rest of t (shifted by 1).
                return s[i:] == t[i + 1:]

    # If we got here, strings matched up to the length of s.
    # It's 1 edit apart ONLY IF t has exactly 1 more character.
    return m + 1 == n
```

---

## Complexity Profile

| Approach | Time | Space | Notes |
| :--- | :--- | :--- | :--- |
| **Top-Down Memoization** | $O(M \times N)$ | $O(M \times N)$ | Clean to write, but has recursion overhead |
| **Bottom-Up 2D DP** | $O(M \times N)$ | $O(M \times N)$ | Best if you need to backtrack the operations |
| **Bottom-Up 1D DP** | $O(M \times N)$ | $O(\min(M, N))$ | **Optimal.** Standard for interviews. |

---

## Edge Cases to Consider

When solving sequence alignment problems, mentally test your logic against these core cases:
- **Empty strings**: `word1 = "", word2 = "abc"` $\rightarrow$ Distance 3 (Insert all). Handled gracefully by the base cases initialization.
- **Identical strings**: `word1 = "abc", word2 = "abc"` $\rightarrow$ Distance 0.
- **Completely distinct**: `word1 = "abc", word2 = "xyz"` $\rightarrow$ Distance 3 (Replace all).
- **Single character mismatch**: `word1 = "a", word2 = "b"` $\rightarrow$ Distance 1 (Replace).
- **Anagrams**: `word1 = "abc", word2 = "cab"` $\rightarrow$ Distance 2 (Delete 'c', Insert 'c').

---

## Common Mistakes

1. **Forgetting Base Cases initialization**:
   Initializing the matrix with all `0`s instead of $i$ and $j$ for the first row and column. `dp[i][0]` must be $i$, because converting a string of length $i$ to an empty string requires exactly $i$ deletions.
2. **Missing the `+1` cost in the transition**:
   `dp[i][j] = min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])` is incorrect logic. You are *performing* an operation at this step, so you must account for its cost: `1 + min(...)`.
3. **Off-by-one errors with string indexing vs matrix bounds**:
   The DP matrix is size $(M+1) \times (N+1)$ to handle the "empty prefix" base cases. This means `dp[i][j]` maps to the string characters `word1[i-1]` and `word2[j-1]`.

---

## Interview Tips

- **Mention the Space Optimization Immediately**: Start by writing or describing the 2D DP, but explicitly mention "we can optimize this to $O(\min(M, N))$ space because we only need the previous row." This shows foresight and system-level thinking.
- **Understand the LCS Relationship**: Be prepared to answer follow-ups comparing Edit Distance to Longest Common Subsequence (they are closely related prefix-matching DP patterns).
- **Explain the "Why"**: Don't just memorize the 3 operations formula. Explain to the interviewer *why* looking at `dp[i-1][j]` represents a delete operation on `word1`.

## Next: [10-knapsack-01.md](./10-knapsack-01.md)

Learn the foundational 0/1 Knapsack pattern.
# Regex and Wildcard Matching

> **Prerequisites:** [08-longest-common-subsequence](./08-longest-common-subsequence.md)

## Overview

Regex and Wildcard Matching are classic 2D Dynamic Programming string problems. Given a string and a pattern, the task is to determine if the string fully matches the pattern.

If we only had literal characters and a single-character wildcard (like `.`), we could just use two pointers and scan left-to-right in $O(N)$ time. The difficulty—and the reason we need DP—comes entirely from the `*` character.

The `*` symbol introduces **branching choices** and **overlapping subproblems**:
- Should this `*` match zero characters so we can move on?
- Should this `*` match one character and then we move on?
- Should this `*` match multiple characters, consuming the string while keeping the `*` active?

Because multiple choices might lead to a valid match, we must explore the decision tree. DP saves us by caching the results of `(string_index, pattern_index)` states.

## Wildcard vs. Regular Expression

The most critical first step in an interview is understanding which variation you are solving.

| Feature | Wildcard Matching | Regular Expression Matching |
| :--- | :--- | :--- |
| **Any single char** | `?` | `.` |
| **The `*` symbol** | Matches **any sequence** of characters (including empty). It is a standalone token. | Matches **zero or more** of the **preceding** element. It modifies the character before it. |
| **Valid `*` Usage** | `*a`, `a**b`, `*` | `a*`, `.*`, `c*a*b` (Cannot have leading `*`) |

**Example of `*` difference:**
* In **Wildcard**, `a*b` matches `aXYZb`. The `*` became the sequence `XYZ`.
* In **Regex**, `a*b` matches `aaab` or `b`. The `*` means "repeat the preceding `a` zero or more times".

---

## 1. Regular Expression Matching (LeetCode 10)

**Problem:** Given an input string `s` and a pattern `p`, implement regular expression matching with support for `.` and `*`.

### Recurrence Relation

Let $dp[i][j]$ be `True` if the prefix $s[0 \dots i-1]$ matches the prefix $p[0 \dots j-1]$.
Here, $i$ is the length of the string prefix, and $j$ is the length of the pattern prefix.

**Base Cases:**
* $dp[0][0] = \text{True}$ (Empty string matches empty pattern).
* $dp[i][0] = \text{False}$ for $i > 0$ (Non-empty string never matches empty pattern).
* $dp[0][j]$: An empty string can match a pattern *only if* the pattern consists entirely of elements that can be repeated zero times (e.g., `a*`, `.*`, `a*b*`).
  Since `*` modifies the preceding character, we need the `char` + `*` pair to vanish.
  If $p[j-1] == '*'$, then $dp[0][j] = dp[0][j-2]$.

**Transitions:**
For $i > 0$ (string length) and $j > 0$ (pattern length):

1.  **Direct Match (`p[j-1] == s[i-1]` or `p[j-1] == '.'`):**
    $$dp[i][j] = dp[i-1][j-1]$$
    *If the current characters match, the current state depends on whether the prefixes right before them matched.*

2.  **Star Match (`p[j-1] == '*'`):**
    We look at the *preceding* character in the pattern: $p[j-2]$.
    We have two branches (we take the logical OR):
    $$dp[i][j] = dp[i][j-2] \lor (\text{match} \land dp[i-1][j])$$
    *   **Zero Occurrences ($dp[i][j-2]$):** We drop the `char*` pair from the pattern (moving back 2 steps in the pattern). We don't care if the preceding character matches the string or not.
    *   **One or More Occurrences ($\text{match} \land dp[i-1][j]$):** `match` is true if the preceding char $p[j-2]$ matches the current string char $s[i-1]$ (or is `.`). If it matches, we "consume" $s[i-1]$ (moving back 1 step in the string to $i-1$) but **keep** the `char*` in the pattern (staying at $j$) so it can potentially match more characters.

### Top-Down DP (Memoization)

Memoization often feels more natural for string matching because the branching logic mimics how we mentally evaluate a regex left-to-right.

```python
def isMatch(s: str, p: str) -> bool:
    """
    Time Complexity: O(M * N)
    Space Complexity: O(M * N)
    """
    memo = {}

    def dfs(i: int, j: int) -> bool:
        """Returns True if suffix s[i:] matches suffix p[j:]"""
        if (i, j) in memo:
            return memo[(i, j)]

        # Base Cases
        if j == len(p):
            return i == len(s) # True if both exhausted

        # Check if the current characters match
        first_match = i < len(s) and (s[i] == p[j] or p[j] == '.')

        # If the NEXT character in the pattern is a '*'
        if j + 1 < len(p) and p[j+1] == '*':
            # Branch 1: Match 0 times (skip the 'x*' in pattern, move j+2)
            # Branch 2: Match 1+ times (first_match must be true, consume s[i], keep pattern at j)
            ans = dfs(i, j + 2) or (first_match and dfs(i + 1, j))
        else:
            # Normal character match
            ans = first_match and dfs(i + 1, j + 1)

        memo[(i, j)] = ans
        return ans

    return dfs(0, 0)
```

### Bottom-Up DP (Tabulation)

```python
def is_match_regex(s: str, p: str) -> bool:
    """
    Time Complexity: O(M * N)
    Space Complexity: O(M * N)
    """
    m, n = len(s), len(p)
    # dp[i][j] represents if s[0..i-1] matches p[0..j-1]
    dp = [[False] * (n + 1) for _ in range(m + 1)]

    dp[0][0] = True

    # Base case: Empty string matching against patterns like a*, a*b*, .*
    for j in range(2, n + 1):
        if p[j - 1] == '*':
            dp[0][j] = dp[0][j - 2]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            curr_p = p[j - 1]
            curr_s = s[i - 1]

            if curr_p == curr_s or curr_p == '.':
                # Characters match, inherit from diagonal
                dp[i][j] = dp[i - 1][j - 1]

            elif curr_p == '*':
                prev_p = p[j - 2]

                # Branch 1: Match zero occurrences of preceding element (drop 'x*')
                match_zero = dp[i][j - 2]

                # Branch 2: Match one or more occurrences
                # Preceding element MUST match the current string char
                match_one_more = False
                if prev_p == curr_s or prev_p == '.':
                    # Keep the '*' in the pattern (j), consume one char from string (i-1)
                    match_one_more = dp[i - 1][j]

                dp[i][j] = match_zero or match_one_more

    return dp[m][n]
```

### Space Optimization (1D DP)

Notice that to compute `dp[i][j]`, we only ever need values from the current row `dp[i][...]` and the previous row `dp[i-1][...]`. We can reduce the space complexity to $O(N)$ by keeping just two rows.

```python
def is_match_regex_optimized(s: str, p: str) -> bool:
    """
    Time Complexity: O(M * N)
    Space Complexity: O(N) using two rows.
    """
    m, n = len(s), len(p)

    # prev_row tracks the matching status for the PREVIOUS string character (i-1)
    prev_row = [False] * (n + 1)
    prev_row[0] = True

    # Base cases for empty string
    for j in range(2, n + 1):
        if p[j - 1] == '*':
            prev_row[j] = prev_row[j - 2]

    for i in range(1, m + 1):
        # curr_row tracks the matching status for the CURRENT string character (i)
        curr_row = [False] * (n + 1)
        # An empty pattern never matches a non-empty string, so curr_row[0] remains False

        for j in range(1, n + 1):
            curr_p = p[j - 1]
            curr_s = s[i - 1]

            if curr_p == curr_s or curr_p == '.':
                curr_row[j] = prev_row[j - 1]

            elif curr_p == '*':
                prev_p = p[j - 2]

                # Match 0 times (look left 2 cols in current row)
                match_zero = curr_row[j - 2]

                # Match 1+ times (look directly up to previous row)
                match_one_more = False
                if prev_p == curr_s or prev_p == '.':
                    match_one_more = prev_row[j]

                curr_row[j] = match_zero or match_one_more

        prev_row = curr_row

    return prev_row[n]
```

### Visual Walkthrough: Regex

Let `s = "aab"` and `p = "c*a*b"`

| `dp[i][j]` | `""` (j=0) | `c` (j=1) | `*` (j=2) | `a` (j=3) | `*` (j=4) | `b` (j=5) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **`""` (i=0)** | **T** | F | **T** | F | **T** | F |
| **`a` (i=1)** | F | F | F | T | **T** | F |
| **`a` (i=2)** | F | F | F | F | **T** | F |
| **`b` (i=3)** | F | F | F | F | F | **T** |

**How to trace back:**
1.  **`dp[0][2] = T`**: `"c*"` matches empty. It pulls the `T` from `dp[0][0]` (Match zero times: $dp[i][j-2]$).
2.  **`dp[1][4] = T`**: `"a*"` matches the first `"a"`. Since `p[j-2]` (`'a'`) matches `s[i-1]`, we check the "match one or more" branch $dp[i-1][j]$ (directly above it), which is `T`.
3.  **`dp[2][4] = T`**: `"a*"` matches the second `"a"`. Again, `p[j-2] == 'a'`, so we pull `T` from directly above.
4.  **`dp[3][5] = T`**: `"b"` matches `"b"`. Pulls `T` from top-left diagonal.

---

## 2. Wildcard Matching (LeetCode 44)

**Problem:** Given an input string `s` and a pattern `p`, implement wildcard pattern matching with support for `?` and `*`.

### Recurrence Relation

Let $dp[i][j]$ be `True` if $s[0 \dots i-1]$ matches $p[0 \dots j-1]$.

**Base Cases:**
* $dp[0][0] = \text{True}$
* $dp[i][0] = \text{False}$ for $i > 0$
* $dp[0][j]$: An empty string matches a pattern *only if* the pattern consists entirely of `*`s. If $p[j-1] == '*'$, then $dp[0][j] = dp[0][j-1]$.

**Transitions:**
For $i > 0$ and $j > 0$:

1.  **Direct Match (`p[j-1] == s[i-1]` or `p[j-1] == '?'`):**
    $$dp[i][j] = dp[i-1][j-1]$$

2.  **Star Match (`p[j-1] == '*'`):**
    $$dp[i][j] = dp[i][j-1] \lor dp[i-1][j]$$
    *   **Match Empty ($dp[i][j-1]$):** We move past the `*` in the pattern, staying on the same string index (look left).
    *   **Match Sequence ($dp[i-1][j]$):** The `*` consumes the current character $s[i-1]$. We move to $i-1$ in the string but *stay on the `*`* in the pattern (look up) to potentially consume more characters.

Notice how much simpler the `*` transition is compared to Regex Matching! We don't need to look at `p[j-2]` because `*` stands alone.

### Bottom-Up DP (Tabulation)

```python
def is_match_wildcard(s: str, p: str) -> bool:
    """
    Time Complexity: O(M * N)
    Space Complexity: O(M * N)
    """
    m, n = len(s), len(p)
    dp = [[False] * (n + 1) for _ in range(m + 1)]

    dp[0][0] = True

    # Base case: Empty string matching against leading *s
    for j in range(1, n + 1):
        if p[j - 1] == '*':
            dp[0][j] = dp[0][j - 1]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if p[j - 1] == s[i - 1] or p[j - 1] == '?':
                dp[i][j] = dp[i - 1][j - 1]
            elif p[j - 1] == '*':
                # Match empty sequence (drop *) OR Match current char (keep *)
                dp[i][j] = dp[i][j - 1] or dp[i - 1][j]

    return dp[m][n]
```

### Visual Walkthrough: Wildcard

Let `s = "adceb"`, `p = "*a*b"`

| `dp[i][j]` | `""` (j=0) | `*` (j=1) | `a` (j=2) | `*` (j=3) | `b` (j=4) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **`""` (i=0)** | **T** | **T** | F | F | F |
| **`a` (i=1)** | F | T | **T** | **T** | F |
| **`d` (i=2)** | F | T | F | **T** | F |
| **`c` (i=3)** | F | T | F | **T** | F |
| **`e` (i=4)** | F | T | F | **T** | F |
| **`b` (i=5)** | F | T | F | **T** | **T** |

**Key transitions:**
- `dp[0][1] = T`: `*` matches empty string. Pulls `T` from left (`dp[0][0]`).
- `dp[1][2] = T`: `"a"` matches `"a"`. Pulls `T` from top-left (`dp[0][1]`).
- `dp[4][3] = T`: The `*` consumes `"d"`, `"c"`, `"e"`. The `T` drops straight down the column because $dp[i][j] = dp[i-1][j]$ (it pulls `T` from top).
- `dp[5][4] = T`: `"b"` matches `"b"`. Pulls `T` from top-left diagonal.

---

## Common Interview Mistakes

1.  **Confusing the `*` Semantics:** The most common failure point. Always clarify with the interviewer if `*` is a wildcard (standalone) or a regex quantifier (modifies preceding char).
2.  **Incorrect Base Cases:** Forgetting to initialize the first row `dp[0][j]` for patterns that can match an empty string (like `*` for wildcard or `a*b*` for regex).
3.  **Regex `*` Transition Bug:** When processing `*` in regex, a common bug is writing `dp[i][j] = dp[i-1][j]` without verifying that the preceding character `p[j-2]` actually matches `s[i-1]`.
4.  **Off-By-One Errors:** Since $dp[i][j]$ represents the match up to $s[i-1]$ and $p[j-1]$, be very careful with string indices inside the loops.

---

## Complexity Summary

| Approach | Time Complexity | Space Complexity |
| :--- | :--- | :--- |
| **2D Tabulation** | $O(M \times N)$ | $O(M \times N)$ |
| **Memoization** | $O(M \times N)$ | $O(M \times N)$ |
| **1D Tabulation** | $O(M \times N)$ | $O(N)$ |

Where $M$ is the length of string `s` and $N$ is the length of pattern `p`.

**Note:** Memoization has recursive overhead but might avoid computing unreachable states, making it practically faster on average for inputs that fail early. 1D Tabulation is the optimal space solution and highly recommended to know for interviews.

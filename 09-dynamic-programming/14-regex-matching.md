# Regex Matching

> **Prerequisites:** [08-longest-common-subsequence](./08-longest-common-subsequence.md)

## Overview

Regex and Wildcard Matching are classic 2D Dynamic Programming string problems. Given a string and a pattern, the task is to determine if the string fully matches the pattern. These problems are challenging due to the branching possibilities introduced by special characters like `*`.

## Wildcard vs. Regular Expression

The most critical first step is understanding the difference between the two common variations of this problem.

| Feature | Wildcard Matching | Regular Expression Matching |
| :--- | :--- | :--- |
| **Any single char** | `?` | `.` |
| **The `*` symbol** | Matches **any sequence** of characters (including the empty sequence). It stands alone. | Matches **zero or more** of the **preceding** element. It modifies the character before it. |
| **Valid `*` Usage** | `*a`, `a**b`, `*` | `a*`, `.*`, `c*a*b` (Cannot have leading `*`) |

**Example of `*` difference:**
* In Wildcard, `a*b` matches `aXYZb`. The `*` became `XYZ`.
* In Regex, `a*b` matches `aaab` or `b`. The `*` means "repeat the `a` zero or more times".

---

## 1. Regular Expression Matching

Let's start with Regular Expression Matching, as it's the more common and slightly more complex interview question.

**Problem:** Given an input string `s` and a pattern `p`, implement regular expression matching with support for `.` and `*` where:
* `.` Matches any single character.
* `*` Matches zero or more of the preceding element.

### Building Intuition

If we only had literal characters and `.`, we could just use two pointers and compare `s[i]` with `p[j]` (where `p[j] == '.'` is an automatic match).

Why is this a DP problem? The difficulty comes entirely from the `*` character because it introduces **branching choices** that lead to **overlapping subproblems**. When we see a character followed by `*` (like `a*`), we have a choice:
1. **Zero Occurrences:** We can choose to match *zero* `a`s. This means we ignore the `a*` in our pattern and see if the remaining pattern matches the current string.
2. **One or More Occurrences:** If the current string character matches the preceding character of the `*` (either literally an `a` or a `.`), we can "consume" this character from the string. Crucially, *we keep the `a*` in the pattern* because it might match more `a`s later!

Because both branches might lead to a valid match, we must explore both. This creates a massive decision tree. DP saves us by caching the results of `(string_index, pattern_index)` states.

### Recurrence Relation

Let $dp[i][j]$ be `True` if the prefix $s[0 \dots i-1]$ matches the prefix $p[0 \dots j-1]$.
Here, $i$ is the length of the string prefix (or index in `dp`), and $j$ is the length of the pattern prefix.

**Base Cases:**
* $dp[0][0] = \text{True}$ (Empty string matches empty pattern).
* $dp[i][0] = \text{False}$ for $i > 0$ (Non-empty string never matches empty pattern).
* $dp[0][j]$: An empty string can match a pattern *only if* the pattern consists entirely of characters that can be matched zero times (e.g., `a*`, `.*`, `a*b*`). Since `*` modifies the preceding character, we need pairs of characters to vanish. If $p[j-1] == '*'$, then $dp[0][j] = dp[0][j-2]$.

**Transitions:**
For $i > 0$ (string index) and $j > 0$ (pattern index):

1.  **Direct Match (`p[j-1] == s[i-1]` or `p[j-1] == '.'`):**
    $$dp[i][j] = dp[i-1][j-1]$$
    *If the current characters match, the current state depends on whether the prefixes right before them matched.*

2.  **Star Match (`p[j-1] == '*'`):**
    We look at the *preceding* character in the pattern: $p[j-2]$.
    $$dp[i][j] = dp[i][j-2] \lor (\text{match} \land dp[i-1][j])$$
    *   $dp[i][j-2]$: Match zero times. We drop the `x*` from the pattern (moving back 2 steps in the pattern).
    *   $\text{match} \land dp[i-1][j]$: Match one or more times. `match` is true if the preceding char $p[j-2]$ matches the current string char $s[i-1]$. If it matches, we consume $s[i-1]$ (moving back 1 step in the string, to $i-1$) but **keep** the `*` in the pattern (staying at $j$).

### Top-Down DP (Memoization)

Memoization often feels more natural for string matching because the branching logic mimics how we mentally evaluate a regex.

```python
def isMatch(s: str, p: str) -> bool:
    memo = {}

    def dfs(i: int, j: int) -> bool:
        """Returns True if s[i:] matches p[j:]"""
        if (i, j) in memo:
            return memo[(i, j)]

        # Base Cases
        if j == len(p):
            return i == len(s) # True if both exhausted

        # Check if the current characters match
        match = i < len(s) and (s[i] == p[j] or p[j] == '.')

        # If the NEXT character is a '*'
        if j + 1 < len(p) and p[j+1] == '*':
            # Branch 1: Match 0 times (skip the 'x*' in pattern)
            # Branch 2: Match 1+ times (consume s[i], keep 'x*' in pattern)
            res = dfs(i, j + 2) or (match and dfs(i + 1, j))
        else:
            # Normal character match
            res = match and dfs(i + 1, j + 1)

        memo[(i, j)] = res
        return res

    return dfs(0, 0)
```

### Bottom-Up DP (Tabulation)

```python
def is_match_regex(s: str, p: str) -> bool:
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
            pattern_char = p[j - 1]
            string_char = s[i - 1]

            if pattern_char == string_char or pattern_char == '.':
                dp[i][j] = dp[i - 1][j - 1]

            elif pattern_char == '*':
                preceding_char = p[j - 2]

                # 1. Match zero occurrences of preceding element (drop 'x*')
                match_zero = dp[i][j - 2]

                # 2. Match one or more occurrences
                # Must check if the preceding element matches the current string char
                match_one_more = False
                if preceding_char == string_char or preceding_char == '.':
                    # Keep the '*' in the pattern, consume one char from string
                    match_one_more = dp[i - 1][j]

                dp[i][j] = match_zero or match_one_more

    return dp[m][n]
```

### Space Optimization (1D DP)

Notice that to compute `dp[i][j]`, we only ever need values from the current row `dp[i][...]` and the previous row `dp[i-1][...]`. We can reduce the space complexity from $O(M \times N)$ to $O(N)$ by keeping just two rows, or even a single row array.

```python
def is_match_regex_optimized(s: str, p: str) -> bool:
    m, n = len(s), len(p)

    # dp tracks the matching status for the PREVIOUS string character (i-1)
    dp = [False] * (n + 1)
    dp[0] = True

    # Base cases for empty string
    for j in range(2, n + 1):
        if p[j - 1] == '*':
            dp[j] = dp[j - 2]

    for i in range(1, m + 1):
        # new_dp tracks the matching status for the CURRENT string character (i)
        new_dp = [False] * (n + 1)
        # An empty pattern never matches a non-empty string, so new_dp[0] remains False

        for j in range(1, n + 1):
            pattern_char = p[j - 1]
            string_char = s[i - 1]

            if pattern_char == string_char or pattern_char == '.':
                new_dp[j] = dp[j - 1]

            elif pattern_char == '*':
                preceding_char = p[j - 2]

                # Match 0 times
                new_dp[j] = new_dp[j - 2]

                # Match 1+ times
                if preceding_char == string_char or preceding_char == '.':
                    new_dp[j] = new_dp[j] or dp[j]

        dp = new_dp

    return dp[n]
```

---

## 2. Wildcard Matching

**Problem:** Given an input string `s` and a pattern `p`, implement wildcard pattern matching with support for `?` and `*` where:
* `?` Matches any single character.
* `*` Matches any sequence of characters (including the empty sequence).

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
    *   $dp[i][j-1]$: `*` matches the empty sequence (we move past the `*` in the pattern, staying on the same string index).
    *   $dp[i-1][j]$: `*` matches the current character $s[i-1]$. We consume the character from the string (moving to $i-1$) but *stay on the `*`* in the pattern (staying at $j$) to potentially match more characters.

Notice how much simpler the `*` transition is compared to Regex Matching! We don't need to look at `p[j-2]` because `*` stands alone.

### Bottom-Up DP (Tabulation)

```python
def is_match_wildcard(s: str, p: str) -> bool:
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

---

## Visual Walkthrough: Wildcard

Let `s = "adceb"`, `p = "*a*b"`

| | "" (j=0) | `*` (j=1) | `a` (j=2) | `*` (j=3) | `b` (j=4) |
|---|---|---|---|---|---|
| **"" (i=0)** | **T** | **T** | F | F | F |
| **`a` (i=1)** | F | T | **T** | **T** | F |
| **`d` (i=2)** | F | T | F | **T** | F |
| **`c` (i=3)** | F | T | F | **T** | F |
| **`e` (i=4)** | F | T | F | **T** | F |
| **`b` (i=5)** | F | T | F | **T** | **T** |

**Key transitions:**
- `dp[0][1] = T`: `*` matches empty string. Pulls `T` from left (`dp[0][0]`).
- `dp[1][2] = T`: `"a"` matches `"a"`. Pulls `T` from top-left (`dp[0][1]`).
- `dp[1][3] = T`: `*` matches empty string (after `"a"`). Pulls `T` from left (`dp[1][2]`).
- `dp[4][3] = T`: The `*` consumes the `"e"` (and previously `"d"`, `"c"`). The `T` drops straight down the column because `dp[i][j] = dp[i-1][j]` (it pulls `T` from top).
- `dp[5][4] = T`: `"b"` matches `"b"`. Pulls `T` from top-left (`dp[4][3]`).

## Visual Walkthrough: Regex

Let `s = "aab"` and `p = "c*a*b"`

| | "" (j=0) | `c` (j=1) | `*` (j=2) | `a` (j=3) | `*` (j=4) | `b` (j=5) |
|---|---|---|---|---|---|---|
| **"" (i=0)** | **T** | F | **T** | F | **T** | F |
| **`a` (i=1)** | F | F | F | T | **T** | F |
| **`a` (i=2)** | F | F | F | F | **T** | F |
| **`b` (i=3)** | F | F | F | F | F | **T** |

**Key transitions:**
- `dp[0][2] = T`: `"c*"` matches empty. It pulls the `T` from `dp[0][0]` (two columns left: $dp[i][j-2]$).
- `dp[0][4] = T`: `"c*a*"` matches empty. It pulls the `T` from `dp[0][2]` (two columns left).
- `dp[1][4] = T`: `"a*"` matches the first `"a"`. Since `p[j-2] == 'a'` matches `s[i-1]`, we evaluate the "match one or more" branch and check $dp[i-1][j]$ (directly above it), which is `T`.
- `dp[2][4] = T`: `"a*"` matches the second `"a"`. Again, `p[j-2] == 'a'`, and $dp[i-1][j]$ (directly above) is `T`.
- `dp[3][5] = T`: `"b"` matches `"b"`. Pulls `T` from top-left (`dp[2][4]`).

---

## Complexity

| Approach | Time Complexity | Space Complexity |
| :--- | :--- | :--- |
| **2D Tabulation** | $O(M \times N)$ | $O(M \times N)$ |
| **Memoization** | $O(M \times N)$ | $O(M \times N)$ |
| **1D Tabulation** | $O(M \times N)$ | $O(N)$ |

Where $M$ is the length of string `s` and $N$ is the length of pattern `p`.

**Note:** Memoization has recursive overhead but might avoid computing unreachable states, making it practically faster on average for inputs that fail early. 1D Tabulation is the optimal space solution and highly recommended to know for interviews.

---

## Common Interview Mistakes

1.  **Confusing the `*` Semantics:** The most common failure point. Always clarify with the interviewer if `*` is a wildcard (standalone) or a regex quantifier (modifies preceding char).
2.  **Incorrect Base Cases:** Forgetting to initialize the first row `dp[0][j]` for patterns that can match an empty string (like `*` for wildcard or `a*b*` for regex).
3.  **Regex `*` Transition Bug:** When processing `*` in regex, a common bug is writing `dp[i][j] = dp[i-1][j]` without verifying that the preceding character `p[j-2]` actually matches `s[i-1]`.
4.  **Off-By-One Errors:** Since $dp[i][j]$ represents the match up to $s[i-1]$ and $p[j-1]$, be very careful with string indices inside the loops. Using well-named variables like `pattern_char` and `string_char` helps avoid confusion.

---

## When NOT to Use Regex DP

DP is $O(M \times N)$. In the real world, regex engines process strings and patterns of massive sizes.
*   **Simple matches without `*`:** Just use $O(N)$ two pointers.
*   **Production Regex Engines:** They use Finite Automata (NFAs and DFAs) to achieve $O(M)$ time complexity, rather than $O(M \times N)$ DP.
*   **Multiple Patterns:** If searching a string against many patterns (like a firewall), use the Aho-Corasick algorithm or build a combined NFA.

---

## Practice Problems

| # | Problem | Difficulty | Notes |
| --- | --- | --- | --- |
| 1 | [Regular Expression Matching](https://leetcode.com/problems/regular-expression-matching/) | Hard | The classic Regex DP problem. |
| 2 | [Wildcard Matching](https://leetcode.com/problems/wildcard-matching/) | Hard | The classic Wildcard DP problem. |
| 3 | [Valid Parenthesis String](https://leetcode.com/problems/valid-parenthesis-string/) | Medium | Uses a similar concept of "branching possibilities", though usually solved with Greedy. |

---

## Next: [15-buy-sell-stock.md](./15-buy-sell-stock.md)

Learn State Machine DP by mastering the Buy and Sell Stock series.
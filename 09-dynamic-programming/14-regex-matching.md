# Regex Matching

> **Prerequisites:** [08-longest-common-subsequence](./08-longest-common-subsequence.md)

## Overview

Regex Matching uses DP to determine if a string matches a pattern containing wildcards (\*) and single-character matches (. or ?).

## Building Intuition

**Why is regex matching harder than simple string comparison?**

1. **Wildcards Create Branching**: The `*` can match 0, 1, 2, ... characters. We must try all possibilities. DP handles this by encoding "match 0" vs "match 1+" as transitions.

2. **Two Different `*` Semantics**:
   - **Wildcard `*`**: Matches ANY sequence (standalone)
   - **Regex `*`**: Matches 0+ of the PRECEDING character (never standalone)

   This subtle difference completely changes the recurrence!

3. **Regex `*` Logic**: For pattern `a*`:
   - Match 0 'a's: Skip the `a*` entirely → dp[i][j-2]
   - Match 1+ 'a's: Current char must be 'a', and remaining string must match `a*` → dp[i-1][j]

4. **Wildcard `*` Logic**: For pattern `*`:
   - Match empty: dp[i][j-1]
   - Match one char and continue with `*`: dp[i-1][j]

5. **Base Cases Are Tricky**: Empty string matching `a*b*c*`? Yes! Each `x*` can match 0 of that character. So dp[0][j] depends on whether pattern[0..j-1] consists only of `x*` pairs.

6. **Mental Model**: Think of regex matching as a two-player game. Player 1 reveals string characters one by one. Player 2 must "spend" pattern characters to match. `*` is a "loop card" that can match repeatedly.

## Interview Context

Pattern matching DP is challenging because:

1. **Complex recurrence**: Multiple cases to handle
2. **Wildcard vs regex**: Subtly different rules
3. **Edge cases**: Empty pattern, consecutive wildcards
4. **Real-world relevance**: Shell globbing, regex engines

---

## When NOT to Use Regex DP

1. **Simple Patterns (No `*`)**: If pattern has only literal characters and `.`, simple $O(n)$ two-pointer matching works.
   - *Example*: Checking if `"abc"` matches `"a.c"`. Just loop through and compare `s[i] == p[i]` or `p[i] == '.'`.

2. **Full Regex Features**: DP handles `*` and `.`, but not `+`, `?`, `{n,m}`, `|`, `()`, etc. For full regex, use proper regex engines (NFA/DFA).
   - *Example*: Validating an email address with `^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$`.

3. **Very Long Strings/Patterns**: $O(m \times n)$ can be slow for $m, n = 10^5$. Specialized algorithms or compiled regex engines are faster.
   - *Example*: Grepping a 10MB log file with a 100-character regex. DP would take $10^9$ operations, which is too slow for real-time processing.

4. **Multiple Patterns**: For matching against many patterns, build a combined automaton (Aho-Corasick for literals, NFA for regex).
   - *Example*: A WAF (Web Application Firewall) matching incoming requests against 1000 known malicious signatures. Running DP 1000 times for every request is unscalable.

5. **Streaming Input**: DP assumes you have the full string in memory. For streaming regex matching, use DFA simulation.
   - *Example*: Matching network packets on the fly where you don't have the whole string in memory at once and need to maintain state across packet boundaries.

**Distinguish Wildcard vs Regex:**

- Wildcard: `*` alone matches any sequence
- Regex: `*` modifies preceding char (match 0+)
- Both: `.` or `?` matches single char

---

## Wildcard Matching

Pattern with:
- `?` matches any single character
- `*` matches any sequence (including empty)

### Base Cases
Proper base cases are crucial for correctly initializing the DP state:
- **`dp[0][0] = True`**: Empty string matches empty pattern.
- **`dp[i][0] = False` (for $i > 0$)**: Non-empty string cannot match an empty pattern.
- **`dp[0][j]`**: An empty string can match a non-empty pattern **only if** the pattern consists entirely of wildcards (`*`). E.g. `s=""`, `p="***"`.


### Recurrence Relation

Let $dp[i][j]$ be whether $s[0 \dots i-1]$ matches $p[0 \dots j-1]$.

$$
dp[i][j] =
\begin{cases}
True & \text{if } i=0, j=0 \\
dp[0][j-1] & \text{if } i=0, p[j-1] = '*' \\
dp[i-1][j-1] & \text{if } i>0, p[j-1] \in \{s[i-1], '?'\} \\
dp[i][j-1] \lor dp[i-1][j] & \text{if } i>0, p[j-1] = '*' \\
False & \text{otherwise}
\end{cases}
$$

### Top-Down (Memoization)

```python
def isMatchWildcardMemo(s: str, p: str) -> bool:
    m, n = len(s), len(p)
    memo = {}

    def dfs(i: int, j: int) -> bool:
        if (i, j) in memo:
            return memo[(i, j)]

        # Base case 1: both empty
        if i == m and j == n:
            return True

        # Base case 2: pattern empty but string not
        if j == n:
            return False

        # Base case 3: string empty but pattern has remaining '*'
        if i == m:
            return p[j] == '*' and dfs(i, j + 1)

        match = False
        if p[j] == '*':
            # Match 0 chars (skip '*') OR match 1+ chars (consume s[i])
            match = dfs(i, j + 1) or dfs(i + 1, j)
        elif p[j] in {s[i], '?'}:
            match = dfs(i + 1, j + 1)

        memo[(i, j)] = match
        return match

    return dfs(0, 0)
```

### Bottom-Up (Tabulation)

```python
def is_match_wildcard(s: str, p: str) -> bool:
    """
    Wildcard pattern matching.

    State: dp[i][j] = does s[0..i-1] match p[0..j-1]

    Recurrence:
        p[j-1] == s[i-1] or p[j-1] == '?':
            dp[i][j] = dp[i-1][j-1]
        p[j-1] == '*':
            dp[i][j] = dp[i][j-1] (empty match) or dp[i-1][j] (consume char)

    Time: O(m × n)
    Space: O(n)
    """
    m, n = len(s), len(p)
    dp = [False] * (n + 1)
    dp[0] = True  # Empty pattern matches empty string

    # Handle leading *s
    for j in range(1, n + 1):
        if p[j - 1] == '*':
            dp[j] = dp[j - 1]
        else:
            break

    for i in range(1, m + 1):
        new_dp = [False] * (n + 1)

        for j in range(1, n + 1):
            if p[j - 1] == '*':
                # Empty match (dp[j-1]) or consume character (dp[j] from prev row)
                new_dp[j] = new_dp[j - 1] or dp[j]
            elif p[j - 1] == '?' or p[j - 1] == s[i - 1]:
                new_dp[j] = dp[j - 1]

        dp = new_dp

    return dp[n]
```

### 2D Version

```python
def is_match_wildcard_2d(s: str, p: str) -> bool:
    """
    2D DP for clarity.
    """
    m, n = len(s), len(p)
    dp = [[False] * (n + 1) for _ in range(m + 1)]

    dp[0][0] = True

    # Initialize: * can match empty string
    for j in range(1, n + 1):
        if p[j - 1] == '*':
            dp[0][j] = dp[0][j - 1]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if p[j - 1] == '*':
                dp[i][j] = dp[i][j - 1] or dp[i - 1][j]
            elif p[j - 1] == '?' or p[j - 1] == s[i - 1]:
                dp[i][j] = dp[i - 1][j - 1]

    return dp[m][n]
```

---

## Regular Expression Matching

Pattern with:
- `.` matches any single character
- `*` matches zero or more of the preceding element

### Base Cases
Proper base cases are crucial here as well:
- **`dp[0][0] = True`**: Empty string matches empty pattern.
- **`dp[i][0] = False` (for $i > 0$)**: Non-empty string cannot match an empty pattern.
- **`dp[0][j]`**: An empty string can match a non-empty pattern **only if** the pattern consists of characters followed by `*` (which can match 0 occurrences). E.g., `s=""`, `p="a*b*c*"`. If `p[j-1] == '*'`, then `dp[0][j] = dp[0][j-2]`.

### Recurrence Relation

Let $dp[i][j]$ be whether $s[0 \dots i-1]$ matches $p[0 \dots j-1]$.

$$
dp[i][j] =
\begin{cases}
True & \text{if } i=0, j=0 \\
dp[0][j-2] & \text{if } i=0, p[j-1] = '*' \text{ (match zero chars)} \\
dp[i-1][j-1] & \text{if } i>0, p[j-1] \in \{s[i-1], '.'\} \\
dp[i][j-2] \lor (dp[i-1][j] \land p[j-2] \in \{s[i-1], '.'\}) & \text{if } i>0, p[j-1] = '*' \\
False & \text{otherwise}
\end{cases}
$$

### Top-Down (Memoization)

```python
def isMatchRegexMemo(s: str, p: str) -> bool:
    m, n = len(s), len(p)
    memo = {}

    def dfs(i: int, j: int) -> bool:
        if (i, j) in memo:
            return memo[(i, j)]

        # Base case 1: both empty
        if i == m and j == n:
            return True

        # Base case 2: pattern empty but string not
        if j == n:
            return False

        match = False
        first_match = i < m and p[j] in {s[i], '.'}

        if j + 1 < n and p[j + 1] == '*':
            # Match 0 chars OR (match 1 char and stay at '*')
            match = dfs(i, j + 2) or (first_match and dfs(i + 1, j))
        elif first_match:
            match = dfs(i + 1, j + 1)

        memo[(i, j)] = match
        return match

    return dfs(0, 0)
```

### Bottom-Up (Tabulation)

```python
def is_match_regex(s: str, p: str) -> bool:
    """
    Regex pattern matching with . and *.

    Note: * applies to PRECEDING element, unlike wildcard.

    State: dp[i][j] = does s[0..i-1] match p[0..j-1]

    Recurrence:
        p[j-1] == s[i-1] or p[j-1] == '.':
            dp[i][j] = dp[i-1][j-1]
        p[j-1] == '*':
            dp[i][j] = dp[i][j-2] (zero occurrence)
                    or (dp[i-1][j] and (p[j-2] == s[i-1] or p[j-2] == '.'))

    Time: O(m × n)
    Space: O(n)
    """
    m, n = len(s), len(p)
    dp = [[False] * (n + 1) for _ in range(m + 1)]

    dp[0][0] = True

    # Pattern with x* can match empty string
    for j in range(2, n + 1):
        if p[j - 1] == '*':
            dp[0][j] = dp[0][j - 2]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if p[j - 1] == s[i - 1] or p[j - 1] == '.':
                dp[i][j] = dp[i - 1][j - 1]
            elif p[j - 1] == '*':
                # Zero occurrences of preceding element
                dp[i][j] = dp[i][j - 2]

                # One or more occurrences
                if p[j - 2] == s[i - 1] or p[j - 2] == '.':
                    dp[i][j] = dp[i][j] or dp[i - 1][j]

    return dp[m][n]
```

---

## Visual Walkthrough: Wildcard

| | "" | `*` | `a` | `*` | `b` |
|---|---|---|---|---|---|
| **""** | T | T | F | F | F |
| **`a`** | F | T | T | T | F |
| **`d`** | F | T | F | T | F |
| **`c`** | F | T | F | T | F |
| **`e`** | F | T | F | T | F |
| **`b`** | F | T | F | T | T ← Answer |

Key transitions:
- `dp[0][1] = T`: `*` matches empty string.
- `dp[1][2] = T`: `"a"` matches `"a"`.
- `dp[1][3] = T`: `*` matches empty string (after `"a"`).
- `dp[5][4] = T`: `*` matches `"dce"` (the previous `T` in the column drops down).
- `dp[5][5] = T`: `"b"` matches `"b"`.

---

## Visual Walkthrough: Regex

| | "" | `c` | `*` | `a` | `*` | `b` |
|---|---|---|---|---|---|---|
| **""** | T | F | T | F | T | F |
| **`a`** | F | F | F | T | T | F |
| **`a`** | F | F | F | F | T | F |
| **`b`** | F | F | F | F | F | T ← Answer |

Key transitions:
- `dp[0][2] = T`: `"c*"` matches empty (zero c's). `dp[0][0]` propagates.
- `dp[0][4] = T`: `"c*a*"` matches empty. `dp[0][2]` propagates.
- `dp[1][4] = T`: `"a*"` matches `"a"`. `dp[0][4]` propagates because `a` matches `a`.
- `dp[2][4] = T`: `"a*"` matches `"aa"`. `dp[1][4]` propagates because `a` matches `a`.
- `dp[3][5] = T`: `"b"` matches `"b"`.

---

## Key Differences

| Aspect         | Wildcard                   | Regex                     |
| -------------- | -------------------------- | ------------------------- |
| `*` meaning    | Match any sequence         | Match 0+ of preceding     |
| `?` or `.`     | Single char                | Single char               |
| `*` standalone | Valid                      | Invalid (needs preceding) |
| "a\*" matches  | Anything starting with 'a' | "", "a", "aa", "aaa"...   |

---

## Edge Cases

```python
# 1. Empty string and pattern
s = "", p = ""
# True

# 2. Empty string, pattern with only *
s = "", p = "***"
# True (wildcard), True if ".*" (regex)

# 3. Empty pattern
s = "abc", p = ""
# False

# 4. Consecutive stars (wildcard)
s = "abc", p = "a**c"
# True (multiple * same as single)

# 5. Star without preceding (regex)
p = "*abc"  # Invalid regex pattern

# 6. Dot matches any
s = "ab", p = ".."
# True
```

---

## Common Mistakes

```python
# WRONG: Not handling leading * for empty string
dp[0][0] = True
# Missing: dp[0][j] for * patterns

# CORRECT (Wildcard):
for j in range(1, n + 1):
    if p[j-1] == '*':
        dp[0][j] = dp[0][j-1]

# CORRECT (Regex):
for j in range(2, n + 1):
    if p[j-1] == '*':
        dp[0][j] = dp[0][j-2]  # Skip the "x*"


# WRONG: Confusing regex * with wildcard *
if p[j-1] == '*':
    dp[i][j] = dp[i][j-1]  # Wrong for regex!

# CORRECT for regex:
dp[i][j] = dp[i][j-2]  # Zero occurrences of preceding


# WRONG: Not checking preceding element for regex *
if p[j-1] == '*':
    dp[i][j] = dp[i-1][j]  # Need to check if preceding matches!

# CORRECT:
if p[j-2] == s[i-1] or p[j-2] == '.':
    dp[i][j] = dp[i][j] or dp[i-1][j]
```

---

### Space-Optimized Regex (Tabulation)

Notice in our recurrence relation: $dp[i][j]$ only depends on $dp[i-1][\dots]$ (the previous row) and $dp[i][\dots]$ (the current row). We can optimize the $O(m \times n)$ 2D matrix down to two $O(n)$ arrays or even a single $1D$ array of size $n$.
By just holding onto the current row and the previous row of results, our space complexity drops significantly without affecting the time complexity.

```python
def is_match_regex_optimized(s: str, p: str) -> bool:
    """
    O(n) space regex matching.
    """
    m, n = len(s), len(p)
    dp = [False] * (n + 1)
    dp[0] = True

    # Initialize base cases for empty string matching a pattern of `x*y*z*`
    for j in range(2, n + 1):
        if p[j - 1] == '*':
            dp[j] = dp[j - 2]

    for i in range(1, m + 1):
        new_dp = [False] * (n + 1)

        for j in range(1, n + 1):
            if p[j - 1] == s[i - 1] or p[j - 1] == '.':
                new_dp[j] = dp[j - 1]
            elif p[j - 1] == '*':
                new_dp[j] = new_dp[j - 2]  # Zero occurrences of preceding char
                if p[j - 2] == s[i - 1] or p[j - 2] == '.':
                    new_dp[j] = new_dp[j] or dp[j]  # One or more occurrences

        dp = new_dp

    return dp[n]
```

---

## Recursive with Memoization

```python
from functools import lru_cache

def is_match_memo(s: str, p: str) -> bool:
    """
    Memoized recursive solution.
    """
    @lru_cache(maxsize=None)
    def match(i: int, j: int) -> bool:
        # Base case: pattern exhausted
        if j == len(p):
            return i == len(s)

        # Check first character match
        first_match = i < len(s) and (p[j] == s[i] or p[j] == '.')

        # Handle *
        if j + 1 < len(p) and p[j + 1] == '*':
            # Zero occurrences OR one+ occurrences
            return match(i, j + 2) or (first_match and match(i + 1, j))

        return first_match and match(i + 1, j + 1)

    return match(0, 0)
```

---

## Complexity

| Problem       | Time  | Space |
| ------------- | ----- | ----- |
| Wildcard (DP) | O(mn) | O(n)  |
| Regex (DP)    | O(mn) | O(n)  |
| Regex (Memo)  | O(mn) | O(mn) |

---

## Interview Tips

1. **Know both patterns**: Wildcard vs regex
2. **Handle base cases**: Empty string, empty pattern
3. **Understand \* semantics**: Standalone vs preceding
4. **Draw DP table**: Helps visualize transitions
5. **Mention optimizations**: Space reduction

---

## Practice Problems

| #   | Problem                     | Difficulty | Type            |
| --- | --------------------------- | ---------- | --------------- |
| 1   | Wildcard Matching           | Hard       | Wildcard        |
| 2   | Regular Expression Matching | Hard       | Regex           |
| 3   | Valid Parenthesis String    | Medium     | Similar concept |

---

## Key Takeaways

1. **Two different problems**: Wildcard ≠ regex
2. **Regex \* needs preceding**: "x\*" matches zero or more x
3. **Wildcard \* is standalone**: Matches any sequence
4. **Initialize for empty string**: Important for \* patterns
5. **2D then optimize**: Start with 2D, reduce to 1D

---

## Next: [15-buy-sell-stock.md](./15-buy-sell-stock.md)

Learn state machine DP with stock problems.

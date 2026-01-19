# Regex Matching

> **Prerequisites:** [08-longest-common-subsequence](./08-longest-common-subsequence.md)

## Interview Context

Pattern matching DP is challenging because:

1. **Complex recurrence**: Multiple cases to handle
2. **Wildcard vs regex**: Subtly different rules
3. **Edge cases**: Empty pattern, consecutive wildcards
4. **Real-world relevance**: Shell globbing, regex engines

---

## Wildcard Matching

Pattern with:
- `?` matches any single character
- `*` matches any sequence (including empty)

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

```
s = "adceb", p = "*a*b"

    ""  *  a  *  b
""   T  T  F  F  F
a    F  T  T  T  F
d    F  T  F  T  F
c    F  T  F  T  F
e    F  T  F  T  F
b    F  T  F  T  T ← Answer

Key transitions:
- dp[0][1] = T: * matches empty
- dp[1][2] = T: "a" matches "a"
- dp[1][3] = T: * matches empty
- dp[5][4] = T: * matches "dce"
- dp[5][5] = T: "b" matches "b"
```

---

## Visual Walkthrough: Regex

```
s = "aab", p = "c*a*b"

    ""  c  *  a  *  b
""   T  F  T  F  T  F
a    F  F  F  T  T  F
a    F  F  F  F  T  F
b    F  F  F  F  F  T ← Answer

Key transitions:
- dp[0][2] = T: "c*" matches empty (zero c's)
- dp[0][4] = T: "c*a*" matches empty
- dp[1][4] = T: "a*" matches "a"
- dp[2][4] = T: "a*" matches "aa"
- dp[3][5] = T: "b" matches "b"
```

---

## Key Differences

| Aspect | Wildcard | Regex |
|--------|----------|-------|
| `*` meaning | Match any sequence | Match 0+ of preceding |
| `?` or `.` | Single char | Single char |
| `*` standalone | Valid | Invalid (needs preceding) |
| "a*" matches | Anything starting with 'a' | "", "a", "aa", "aaa"... |

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

## Space-Optimized Regex

```python
def is_match_regex_optimized(s: str, p: str) -> bool:
    """
    O(n) space regex matching.
    """
    m, n = len(s), len(p)
    dp = [False] * (n + 1)
    dp[0] = True

    # Initialize for x* patterns
    for j in range(2, n + 1):
        if p[j - 1] == '*':
            dp[j] = dp[j - 2]

    for i in range(1, m + 1):
        new_dp = [False] * (n + 1)

        for j in range(1, n + 1):
            if p[j - 1] == s[i - 1] or p[j - 1] == '.':
                new_dp[j] = dp[j - 1]
            elif p[j - 1] == '*':
                new_dp[j] = new_dp[j - 2]  # Zero occurrences
                if p[j - 2] == s[i - 1] or p[j - 2] == '.':
                    new_dp[j] = new_dp[j] or dp[j]

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

| Problem | Time | Space |
|---------|------|-------|
| Wildcard (DP) | O(mn) | O(n) |
| Regex (DP) | O(mn) | O(n) |
| Regex (Memo) | O(mn) | O(mn) |

---

## Interview Tips

1. **Know both patterns**: Wildcard vs regex
2. **Handle base cases**: Empty string, empty pattern
3. **Understand * semantics**: Standalone vs preceding
4. **Draw DP table**: Helps visualize transitions
5. **Mention optimizations**: Space reduction

---

## Practice Problems

| # | Problem | Difficulty | Type |
|---|---------|------------|------|
| 1 | Wildcard Matching | Hard | Wildcard |
| 2 | Regular Expression Matching | Hard | Regex |
| 3 | Valid Parenthesis String | Medium | Similar concept |

---

## Key Takeaways

1. **Two different problems**: Wildcard ≠ regex
2. **Regex * needs preceding**: "x*" matches zero or more x
3. **Wildcard * is standalone**: Matches any sequence
4. **Initialize for empty string**: Important for * patterns
5. **2D then optimize**: Start with 2D, reduce to 1D

---

## Next: [15-buy-sell-stock.md](./15-buy-sell-stock.md)

Learn state machine DP with stock problems.

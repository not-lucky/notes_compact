# Solutions: Regex Matching

## 1. Wildcard Matching
**Problem:** Pattern matching with `?` (any char) and `*` (any sequence).

### Optimal Python Solution
```python
def is_match(s: str, p: str) -> bool:
    # State: dp[i][j] = matches s[:i] with p[:j]
    m, n = len(s), len(p)
    dp = [[False] * (n + 1) for _ in range(m + 1)]
    dp[0][0] = True

    # Handle leading * in pattern
    for j in range(1, n + 1):
        if p[j-1] == '*':
            dp[0][j] = dp[0][j-1]
        else:
            break

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if p[j-1] == '*':
                # Case 1: * matches empty (dp[i][j-1])
                # Case 2: * matches current char (dp[i-1][j])
                dp[i][j] = dp[i][j-1] or dp[i-1][j]
            elif p[j-1] == '?' or p[j-1] == s[i-1]:
                dp[i][j] = dp[i-1][j-1]
    return dp[m][n]

---

## 3. Valid Parenthesis String
**Problem:** String containing `(`, `)`, and `*`. `*` can be `(`, `)`, or empty. Is it valid?

### Optimal Python Solution (Greedy Range)
```python
def check_valid_string(s: str) -> bool:
    # Track the range of possible open counts: [low, high]
    low = high = 0
    for char in s:
        if char == '(':
            low += 1
            high += 1
        elif char == ')':
            low -= 1
            high -= 1
        else: # char == '*'
            low -= 1 # Treat as ')'
            high += 1 # Treat as '('

        if high < 0: return False # Too many ')'
        if low < 0: low = 0 # Cannot have negative open count

    return low == 0
```

### Explanation
1.  **Flexible Balance**: Since `*` can be three things, we don't have a single balance count. Instead, we track a **range** of possible open bracket counts.
2.  **`low`**: Minimum possible open brackets (treating `*` as `)` or empty).
3.  **`high`**: Maximum possible open brackets (treating `*` as `(`).
4.  **Validity**:
    - If `high` drops below 0, it's impossible to balance even if all `*` were `(`.
    - `low` is clamped at 0 because we can't have negative brackets; if we have "extra" closing brackets, we assume some `*` were empty or `(`.
    - Finally, if `low == 0`, it's possible to have perfectly balanced brackets.

### Complexity Analysis
- **Time:** $O(n)$
- **Space:** $O(1)$
```

### Complexity Analysis
- **Time:** $O(mn)$
- **Space:** $O(mn)$ (can be optimized to O(n))

---

## 2. Regular Expression Matching
**Problem:** Pattern matching with `.` (any char) and `*` (zero or more of preceding).

### Optimal Python Solution
```python
def is_match_regex(s: str, p: str) -> bool:
    m, n = len(s), len(p)
    dp = [[False] * (n + 1) for _ in range(m + 1)]
    dp[0][0] = True

    # Handle a*b*c* patterns matching empty string
    for j in range(2, n + 1):
        if p[j-1] == '*':
            dp[0][j] = dp[0][j-2]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if p[j-1] == '*':
                # Case 1: zero occurrences (dp[i][j-2])
                # Case 2: one or more if preceding matches (dp[i-1][j])
                dp[i][j] = dp[i][j-2]
                if p[j-2] == s[i-1] or p[j-2] == '.':
                    dp[i][j] = dp[i][j] or dp[i-1][j]
            elif p[j-1] == '.' or p[j-1] == s[i-1]:
                dp[i][j] = dp[i-1][j-1]
    return dp[m][n]

---

## 3. Valid Parenthesis String
**Problem:** String containing `(`, `)`, and `*`. `*` can be `(`, `)`, or empty. Is it valid?

### Optimal Python Solution (Greedy Range)
```python
def check_valid_string(s: str) -> bool:
    # Track the range of possible open counts: [low, high]
    low = high = 0
    for char in s:
        if char == '(':
            low += 1
            high += 1
        elif char == ')':
            low -= 1
            high -= 1
        else: # char == '*'
            low -= 1 # Treat as ')'
            high += 1 # Treat as '('

        if high < 0: return False # Too many ')'
        if low < 0: low = 0 # Cannot have negative open count

    return low == 0
```

### Explanation
1.  **Flexible Balance**: Since `*` can be three things, we don't have a single balance count. Instead, we track a **range** of possible open bracket counts.
2.  **`low`**: Minimum possible open brackets (treating `*` as `)` or empty).
3.  **`high`**: Maximum possible open brackets (treating `*` as `(`).
4.  **Validity**:
    - If `high` drops below 0, it's impossible to balance even if all `*` were `(`.
    - `low` is clamped at 0 because we can't have negative brackets; if we have "extra" closing brackets, we assume some `*` were empty or `(`.
    - Finally, if `low == 0`, it's possible to have perfectly balanced brackets.

### Complexity Analysis
- **Time:** $O(n)$
- **Space:** $O(1)$
```

### Complexity Analysis
- **Time:** $O(mn)$
- **Space:** $O(mn)$

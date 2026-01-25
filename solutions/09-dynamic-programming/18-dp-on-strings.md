# Solutions: Advanced String DP

## 1. Distinct Subsequences
**Problem:** Count distinct subsequences of `s` that equal `t`.

### Optimal Python Solution
```python
def num_distinct(s: str, t: str) -> int:
    m, n = len(s), len(t)
    # Space optimized: O(n)
    dp = [0] * (n + 1)
    dp[0] = 1 # Empty t can be formed by empty subsequence of s

    for i in range(1, m + 1):
        for j in range(n, 0, -1):
            if s[i-1] == t[j-1]:
                dp[j] += dp[j-1]
    return dp[n]
```

### Complexity Analysis
- **Time:** $O(mn)$
- **Space:** $O(n)$

---

## 2. Interleaving String
**Problem:** Is `s3` an interleaving of `s1` and `s2`?

### Optimal Python Solution
```python
def is_interleave(s1: str, s2: str, s3: str) -> bool:
    m, n = len(s1), len(s2)
    if m + n != len(s3): return False

    dp = [False] * (n + 1)
    dp[0] = True

    # Initialize first row (s1 is empty)
    for j in range(1, n + 1):
        dp[j] = dp[j-1] and s2[j-1] == s3[j-1]

    for i in range(1, m + 1):
        # Update first column (s2 is empty)
        dp[0] = dp[0] and s1[i-1] == s3[i-1]
        for j in range(1, n + 1):
            # Matches s1 OR matches s2
            dp[j] = (dp[j] and s1[i-1] == s3[i+j-1]) or \
                    (dp[j-1] and s2[j-1] == s3[i+j-1])
    return dp[n]
```

### Complexity Analysis
- **Time:** $O(mn)$
- **Space:** $O(n)$

---

## 3. Scramble String
**Problem:** Is `s2` a scrambled version of `s1`?

### Optimal Python Solution
```python
from functools import lru_cache

@lru_cache(None)
def is_scramble(s1: str, s2: str) -> bool:
    if s1 == s2: return True
    if sorted(s1) != sorted(s2): return False

    n = len(s1)
    for i in range(1, n):
        # Case 1: No swap
        if is_scramble(s1[:i], s2[:i]) and is_scramble(s1[i:], s2[i:]):
            return True
        # Case 2: Swap
        if is_scramble(s1[:i], s2[n-i:]) and is_scramble(s1[i:], s2[:n-i]):
            return True
    return False
```

### Complexity Analysis
- **Time:** $O(n^4)$ due to memoization states and string slicing.
- **Space:** $O(n^4)$

---

## 4. Longest Valid Parentheses
**Problem:** Length of longest valid parentheses substring.

### Optimal Python Solution
```python
def longest_valid_parentheses(s: str) -> int:
    n = len(s)
    dp = [0] * n # Length of valid substring ending at i
    max_len = 0
    for i in range(1, n):
        if s[i] == ')':
            if s[i-1] == '(':
                dp[i] = (dp[i-2] if i >= 2 else 0) + 2
            elif i - dp[i-1] - 1 >= 0 and s[i - dp[i-1] - 1] == '(':
                # Case: ((...))
                dp[i] = dp[i-1] + 2
                if i - dp[i-1] - 2 >= 0:
                    dp[i] += dp[i - dp[i-1] - 2]
            max_len = max(max_len, dp[i])
    return max_len

---

## 6. Palindrome Pairs
**Problem:** Find all pairs of indices `(i, j)` such that `words[i] + words[j]` is a palindrome.

### Optimal Python Solution
```python
def palindrome_pairs(words: list[str]) -> list[list[int]]:
    word_to_idx = {w: i for i, w in enumerate(words)}
    res = []

    for i, word in enumerate(words):
        for j in range(len(word) + 1):
            prefix, suffix = word[:j], word[j:]

            # Case 1: Prefix is palindrome, reversed suffix exists to the left
            if prefix == prefix[::-1]:
                rev_suffix = suffix[::-1]
                if rev_suffix in word_to_idx and word_to_idx[rev_suffix] != i:
                    res.append([word_to_idx[rev_suffix], i])

            # Case 2: Suffix is palindrome, reversed prefix exists to the right
            # (j != 0 to avoid duplicate work with Case 1 when prefix is empty)
            if j != 0 and suffix == suffix[::-1]:
                rev_prefix = prefix[::-1]
                if rev_prefix in word_to_idx and word_to_idx[rev_prefix] != i:
                    res.append([i, word_to_idx[rev_prefix]])
    return res

---

## 7. Decode Ways II
**Problem:** Decode string with `*` (matches 1-9).

### Optimal Python Solution
```python
def num_decodings_ii(s: str) -> int:
    MOD = 10**9 + 7
    n = len(s)
    # prev2, prev1 = dp[i-2], dp[i-1]
    prev2, prev1 = 1, 0

    def single(c):
        if c == '*': return 9
        return 1 if '1' <= c <= '9' else 0

    def double(c1, c2):
        if c1 == '*' and c2 == '*': return 15 # 11-19, 21-26
        if c1 == '*':
            return 2 if '0' <= c2 <= '6' else 1 # 1x, 2x
        if c2 == '*':
            if c1 == '1': return 9
            if c1 == '2': return 6
            return 0
        return 1 if 10 <= int(c1+c2) <= 26 else 0

    prev1 = single(s[0])
    for i in range(1, n):
        curr = (single(s[i]) * prev1 + double(s[i-1], s[i]) * prev2) % MOD
        prev2, prev1 = prev1, curr

    return prev1
```

### Explanation
1.  **Expansion of Decode Ways**: We now have wildcards. The logic remains the same (1-digit vs 2-digit) but the "ways" for each step are multipliers.
2.  **`*` as 1-digit**: 9 ways (1-9).
3.  **`*` as 2-digit**:
    - `**`: 15 ways (11-19, 21-26).
    - `*X`: If X is 0-6, could be 1X or 2X (2 ways). If 7-9, only 1X (1 way).
    - `X*`: If X is 1, 9 ways. If 2, 6 ways.

### Complexity Analysis
- **Time:** $O(n)$
- **Space:** $O(1)$

---

## 8. Count Different Palindromic Subsequences
**Problem:** Count non-empty distinct palindromic subsequences in $s$.

### Optimal Python Solution
```python
def count_palindromic_subsequences(s: str) -> int:
    n = len(s)
    MOD = 10**9 + 7
    dp = [[0] * n for _ in range(n)]

    for i in range(n): dp[i][i] = 1

    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            if s[i] == s[j]:
                left, right = i + 1, j - 1
                while left <= right and s[left] != s[i]: left += 1
                while left <= right and s[right] != s[j]: right -= 1

                if left > right: # No matching char inside
                    dp[i][j] = dp[i+1][j-1] * 2 + 2
                elif left == right: # One matching char inside
                    dp[i][j] = dp[i+1][j-1] * 2 + 1
                else: # Multiple matching chars inside
                    dp[i][j] = dp[i+1][j-1] * 2 - dp[left+1][right-1]
            else:
                dp[i][j] = dp[i+1][j] + dp[i][j-1] - dp[i+1][j-1]
            dp[i][j] %= MOD

    return dp[0][n-1]
```

### Complexity Analysis
- **Time:** $O(n^2)$ - Actually $O(n^3)$ due to the inner while loops, but can be optimized to $O(n^2)$ with precomputation.
- **Space:** $O(n^2)$
```

### Explanation
1.  **The Trick**: Instead of checking all $O(n^2)$ pairs, we iterate over each word and split it into all possible `prefix` and `suffix` parts ($O(k)$ splits).
2.  **Logic**:
    - If `prefix` is a palindrome, then `reverse(suffix) + prefix + suffix` is a palindrome. We check if `reverse(suffix)` exists in our dictionary.
    - If `suffix` is a palindrome, then `prefix + suffix + reverse(prefix)` is a palindrome. We check if `reverse(prefix)` exists.
3.  **Efficiency**: By using a hash map for dictionary lookups, we reduce the complexity from $O(n^2 k)$ to $O(n k^2)$.

### Complexity Analysis
- **Time:** $O(n \times k^2)$ - Where $n$ is number of words and $k$ is max length.
- **Space:** $O(n \times k)$ - For the hash map.
```

### Complexity Analysis
- **Time:** $O(n)$
- **Space:** $O(n)$

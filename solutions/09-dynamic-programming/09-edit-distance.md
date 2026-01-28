# Solutions: Edit Distance

## 1. Edit Distance (Levenshtein Distance)

**Problem:** Minimum operations (insert, delete, replace) to convert `word1` to `word2`.

### Optimal Python Solution

````python
def min_distance(word1: str, word2: str) -> int:
    m, n = len(word1), len(word2)
    # dp[j] represents distance for prefix of word2
    dp = list(range(n + 1))

    for i in range(1, m + 1):
        prev_diag = dp[0] # dp[i-1][j-1]
        dp[0] = i # Base case: word1[:i] to empty word2
        for j in range(1, n + 1):
            temp = dp[j]
            if word1[i-1] == word2[j-1]:
                dp[j] = prev_diag
            else:
                # 1 + min(Replace, Delete, Insert)
                dp[j] = 1 + min(prev_diag, dp[j], dp[j-1])
            prev_diag = temp
    return dp[n]

```
---

## 4. Distinct Subsequences
**Problem:** Count distinct subsequences of `s` that equal `t`.

### Optimal Python Solution
```python
def num_distinct(s: str, t: str) -> int:
    m, n = len(s), len(t)
    # State: dp[j] = ways to form t[:j]
    dp = [0] * (n + 1)
    dp[0] = 1 # Empty t can be formed by empty subsequence of s

    for i in range(1, m + 1):
        # Iterate backwards to use values from "previous" s character
        for j in range(n, 0, -1):
            if s[i-1] == t[j-1]:
                dp[j] += dp[j-1]
    return dp[n]
````

### Explanation

1.  **Counting DP**: This is a variant of the Knapsack pattern applied to strings.
2.  **Logic**: If `s[i] == t[j]`, we have two choices:
    - Include `s[i]` to form `t[:j]`: This adds `dp[i-1][j-1]` ways.
    - Exclude `s[i]`: This leaves `dp[i-1][j]` ways.
3.  **Space Optimization**: By iterating backwards through `j`, we only need a 1D array.

### Complexity Analysis

- **Time:** $O(m \times n)$
- **Space:** $O(n)$

---

## 5. Distinct Subsequences II

**Problem:** Count distinct non-empty subsequences of a string `s`.

### Optimal Python Solution

```python
def distinct_subsequences_2(s: str) -> int:
    MOD = 10**9 + 7
    # dp[i] = total distinct subsequences using first i chars
    # dp[i] = 2 * dp[i-1] - (dp[last_seen[s[i]] - 1])
    n = len(s)
    dp = [0] * (n + 1)
    dp[0] = 1 # Base case: empty subsequence

    last = {} # Map char to its last seen index
    for i, char in enumerate(s):
        dp[i+1] = (dp[i] * 2) % MOD
        if char in last:
            # Subtract subsequences that were already counted when we last saw this char
            dp[i+1] = (dp[i+1] - dp[last[char]]) % MOD
        last[char] = i

    return (dp[n] - 1) % MOD # Subtract 1 for the empty subsequence
```

### Explanation

1.  **Doubling Strategy**: When we add a new character, we can append it to all existing distinct subsequences, doubling the total count.
2.  **Removing Duplicates**: If we've seen the character before, some of these "new" subsequences were already created when we added that character the previous time. We subtract the count from just before that previous occurrence.
3.  **Modulo Arithmetic**: Ensure results remain positive after subtraction.

### Complexity Analysis

- **Time:** $O(n)$
- **Space:** $O(n)$

````

### Complexity Analysis
- **Time:** $O(mn)$
- **Space:** $O(n)$

---

## 2. One Edit Distance
**Problem:** Check if strings are exactly one edit apart.

### Optimal Python Solution
```python
def is_one_edit_distance(s: str, t: str) -> bool:
    ns, nt = len(s), len(t)
    if ns > nt: return is_one_edit_distance(t, s)
    if nt - ns > 1: return False

    for i in range(ns):
        if s[i] != t[i]:
            if ns == nt: # Replace
                return s[i+1:] == t[i+1:]
            else: # Insert into S
                return s[i:] == t[i+1:]

    return ns + 1 == nt
````

### Complexity Analysis

- **Time:** $O(n)$ - Single pass through strings.
- **Space:** $O(1)$ (ignoring string slices).

---

## 3. Min ASCII Delete Sum for Two Strings

**Problem:** Minimum ASCII sum of deleted characters to make two strings equal.

### Optimal Python Solution

````python
def minimum_delete_sum(s1: str, s2: str) -> int:
    m, n = len(s1), len(s2)
    dp = [0] * (n + 1)

    # Base case: empty s1
    for j in range(1, n + 1):
        dp[j] = dp[j-1] + ord(s2[j-1])

    for i in range(1, m + 1):
        prev_diag = dp[0]
        dp[0] += ord(s1[i-1])
        for j in range(1, n + 1):
            temp = dp[j]
            if s1[i-1] == s2[j-1]:
                dp[j] = prev_diag
            else:
                dp[j] = min(dp[j] + ord(s1[i-1]), dp[j-1] + ord(s2[j-1]))
            prev_diag = temp

    return dp[n]

```
---

## 4. Distinct Subsequences
**Problem:** Count distinct subsequences of `s` that equal `t`.

### Optimal Python Solution
```python
def num_distinct(s: str, t: str) -> int:
    m, n = len(s), len(t)
    # State: dp[j] = ways to form t[:j]
    dp = [0] * (n + 1)
    dp[0] = 1 # Empty t can be formed by empty subsequence of s

    for i in range(1, m + 1):
        # Iterate backwards to use values from "previous" s character
        for j in range(n, 0, -1):
            if s[i-1] == t[j-1]:
                dp[j] += dp[j-1]
    return dp[n]
````

### Explanation

1.  **Counting DP**: This is a variant of the Knapsack pattern applied to strings.
2.  **Logic**: If `s[i] == t[j]`, we have two choices:
    - Include `s[i]` to form `t[:j]`: This adds `dp[i-1][j-1]` ways.
    - Exclude `s[i]`: This leaves `dp[i-1][j]` ways.
3.  **Space Optimization**: By iterating backwards through `j`, we only need a 1D array.

### Complexity Analysis

- **Time:** $O(m \times n)$
- **Space:** $O(n)$

---

## 5. Distinct Subsequences II

**Problem:** Count distinct non-empty subsequences of a string `s`.

### Optimal Python Solution

```python
def distinct_subsequences_2(s: str) -> int:
    MOD = 10**9 + 7
    # dp[i] = total distinct subsequences using first i chars
    # dp[i] = 2 * dp[i-1] - (dp[last_seen[s[i]] - 1])
    n = len(s)
    dp = [0] * (n + 1)
    dp[0] = 1 # Base case: empty subsequence

    last = {} # Map char to its last seen index
    for i, char in enumerate(s):
        dp[i+1] = (dp[i] * 2) % MOD
        if char in last:
            # Subtract subsequences that were already counted when we last saw this char
            dp[i+1] = (dp[i+1] - dp[last[char]]) % MOD
        last[char] = i

    return (dp[n] - 1) % MOD # Subtract 1 for the empty subsequence
```

### Explanation

1.  **Doubling Strategy**: When we add a new character, we can append it to all existing distinct subsequences, doubling the total count.
2.  **Removing Duplicates**: If we've seen the character before, some of these "new" subsequences were already created when we added that character the previous time. We subtract the count from just before that previous occurrence.
3.  **Modulo Arithmetic**: Ensure results remain positive after subtraction.

### Complexity Analysis

- **Time:** $O(n)$
- **Space:** $O(n)$

```

### Complexity Analysis
- **Time:** $O(mn)$
- **Space:** $O(n)$
```

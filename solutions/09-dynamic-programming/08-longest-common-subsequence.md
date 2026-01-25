# Solutions: Longest Common Subsequence

## 1. Longest Common Subsequence (LCS)
**Problem:** Find length of longest common subsequence between two strings.

### Optimal Python Solution
```python
def longest_common_subsequence(text1: str, text2: str) -> int:
    # State: dp[i][j] = LCS of text1[:i] and text2[:j]
    # Space optimization: O(n)
    m, n = len(text1), len(text2)
    if m < n: text1, text2, m, n = text2, text1, n, m

    dp = [0] * (n + 1)
    for i in range(1, m + 1):
        prev_diag = 0 # dp[i-1][j-1]
        for j in range(1, n + 1):
            temp = dp[j]
            if text1[i-1] == text2[j-1]:
                dp[j] = prev_diag + 1
            else:
                dp[j] = max(dp[j], dp[j-1])
            prev_diag = temp
    return dp[n]
```

### Complexity Analysis
- **Time:** $O(mn)$
- **Space:** $O(\min(m, n))$

---

## 2. Longest Common Substring
**Problem:** Find length of longest contiguous common substring.

### Optimal Python Solution
```python
def longest_common_substring(s1: str, s2: str) -> int:
    m, n = len(s1), len(s2)
    dp = [0] * (n + 1)
    max_len = 0
    for i in range(1, m + 1):
        prev_diag = 0
        for j in range(1, n + 1):
            temp = dp[j]
            if s1[i-1] == s2[j-1]:
                dp[j] = prev_diag + 1
                max_len = max(max_len, dp[j])
            else:
                dp[j] = 0 # Contiguous constraint
            prev_diag = temp
    return max_len
```

### Complexity Analysis
- **Time:** $O(mn)$
- **Space:** $O(n)$

---

## 3. Delete Operations for Two Strings
**Problem:** Minimum deletions to make two strings equal.

### Optimal Python Solution
```python
def min_distance(word1: str, word2: str) -> int:
    # Insight: Result = len(word1) + len(word2) - 2 * LCS
    m, n = len(word1), len(word2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i-1] == word2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])

    lcs = dp[m][n]
    return m + n - 2 * lcs
```

### Complexity Analysis
- **Time:** $O(mn)$
- **Space:** $O(mn)$ (can be optimized to O(n))

---

## 4. Shortest Common Supersequence
**Problem:** Find the shortest string that contains both strings as subsequences.

### Optimal Python Solution
```python
def shortest_common_supersequence(str1: str, str2: str) -> str:
    # 1. Build LCS table
    m, n = len(str1), len(str2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if str1[i-1] == str2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])

    # 2. Backtrack to construct string
    res = []
    i, j = m, n
    while i > 0 and j > 0:
        if str1[i-1] == str2[j-1]:
            res.append(str1[i-1])
            i -= 1
            j -= 1
        elif dp[i-1][j] > dp[i][j-1]:
            res.append(str1[i-1])
            i -= 1
        else:
            res.append(str2[j-1])
            j -= 1

    # Add leftovers
    while i > 0: res.append(str1[i-1]); i -= 1
    while j > 0: res.append(str2[j-1]); j -= 1

    return "".join(res[::-1])

---

## 5. Uncrossed Lines
**Problem:** Connect same numbers in two arrays without lines crossing.

### Optimal Python Solution
```python
def max_uncrossed_lines(nums1: list[int], nums2: list[int]) -> int:
    # Key Insight: This is identical to Longest Common Subsequence
    # A line between nums1[i] and nums2[j] is possible if they are equal.
    # Lines don't cross if the indices of selected pairs are strictly increasing.
    m, n = len(nums1), len(nums2)
    dp = [0] * (n + 1)

    for i in range(1, m + 1):
        prev_diag = 0
        for j in range(1, n + 1):
            temp = dp[j]
            if nums1[i-1] == nums2[j-1]:
                dp[j] = prev_diag + 1
            else:
                dp[j] = max(dp[j], dp[j-1])
            prev_diag = temp
    return dp[n]
```

### Explanation
1.  **Reduction to LCS**: The constraints of the problem (lines cannot cross and endpoints must match) are exactly the definition of a common subsequence.
2.  **Implementation**: We use the space-optimized $O(n)$ LCS algorithm.

### Complexity Analysis
- **Time:** $O(m \times n)$
- **Space:** $O(n)$
```

### Complexity Analysis
- **Time:** $O(mn)$
- **Space:** $O(mn)$ - Required for backtracking string construction.

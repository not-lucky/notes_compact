# Solutions: Palindrome DP

## 1. Longest Palindromic Substring

**Problem:** Find the longest contiguous substring that is a palindrome.

### Optimal Python Solution ($O(1)$ space)

```python
def longest_palindrome(s: str) -> str:
    # Pattern: Expand Around Center
    if not s: return ""
    start, max_len = 0, 1

    def expand(l, r):
        while l >= 0 and r < len(s) and s[l] == s[r]:
            l -= 1
            r += 1
        return r - l - 1

    for i in range(len(s)):
        l1 = expand(i, i) # Odd
        l2 = expand(i, i + 1) # Even
        cur = max(l1, l2)
        if cur > max_len:
            max_len = cur
            start = i - (cur - 1) // 2
    return s[start:start+max_len]
```

### Complexity Analysis

- **Time:** $O(n^2)$
- **Space:** $O(1)$

---

## 2. Longest Palindromic Subsequence (LPS)

**Problem:** Find length of longest non-contiguous palindromic subsequence.

### Optimal Python Solution

```python
def longest_palindrome_subseq(s: str) -> int:
    # Interval DP: dp[i][j] = LPS of s[i..j]
    n = len(s)
    dp = [0] * n
    for i in range(n - 1, -1, -1):
        new_dp = [0] * n
        new_dp[i] = 1
        for j in range(i + 1, n):
            if s[i] == s[j]:
                new_dp[j] = dp[j-1] + 2
            else:
                new_dp[j] = max(dp[j], new_dp[j-1])
        dp = new_dp
    return dp[n-1]
```

### Complexity Analysis

- **Time:** $O(n^2)$
- **Space:** $O(n)$

---

## 3. Palindromic Substrings

**Problem:** Count all palindromic substrings.

### Optimal Python Solution

```python
def count_substrings(s: str) -> int:
    count = 0
    def expand(l, r):
        res = 0
        while l >= 0 and r < len(s) and s[l] == s[r]:
            res += 1
            l -= 1
            r += 1
        return res

    for i in range(len(s)):
        count += expand(i, i)
        count += expand(i, i + 1)
    return count
```

### Complexity Analysis

- **Time:** $O(n^2)$
- **Space:** $O(1)$

---

## 4. Palindrome Partitioning II (Min Cuts)

**Problem:** Minimum cuts to partition string into palindromes.

### Optimal Python Solution

````python
def min_cut(s: str) -> int:
    n = len(s)
    # Precompute palindrome matrix
    is_pal = [[False] * n for _ in range(n)]
    for i in range(n - 1, -1, -1):
        for j in range(i, n):
            if s[i] == s[j] and (j - i <= 2 or is_pal[i+1][j-1]):
                is_pal[i][j] = True

    # DP for min cuts
    dp = list(range(n))
    for i in range(n):
        if is_pal[0][i]:
            dp[i] = 0
        else:
            for j in range(i):
                if is_pal[j+1][i]:
                    dp[i] = min(dp[i], dp[j] + 1)
    return dp[-1]

```
---

## 5. Palindrome Partitioning (All Partitions)
**Problem:** Find all possible ways to partition a string into palindromes.

### Optimal Python Solution (Backtracking + DP Precomputation)
```python
def partition(s: str) -> list[list[str]]:
    n = len(s)
    # 1. Precompute palindrome status for all intervals
    is_pal = [[False] * n for _ in range(n)]
    for i in range(n - 1, -1, -1):
        for j in range(i, n):
            if s[i] == s[j] and (j - i <= 2 or is_pal[i+1][j-1]):
                is_pal[i][j] = True

    result = []

    # 2. Backtracking to find all combinations
    def backtrack(start, path):
        if start == n:
            result.append(path[:])
            return

        for end in range(start, n):
            if is_pal[start][end]:
                path.append(s[start:end+1])
                backtrack(end + 1, path)
                path.pop()

    backtrack(0, [])
    return result
````

### Explanation

1.  **Step 1: DP Precomputation**: We build an $n \times n$ table `is_pal` where `is_pal[i][j]` is true if `s[i..j]` is a palindrome. This avoids redundant $O(n)$ checks during backtracking.
2.  **Step 2: Backtracking**: We try to split the string at every possible position. If the current prefix is a palindrome, we recurse on the remainder.
3.  **Efficiency**: Precomputing the palindrome table reduces the check from $O(n)$ to $O(1)$ inside the recursion.

### Complexity Analysis

- **Time:** $O(n \times 2^n)$ - In worst case (e.g., "aaaa"), there are $2^n$ possible partitions.
- **Space:** $O(n^2)$ - To store the palindrome matrix.

```

### Complexity Analysis
- **Time:** $O(n^2)$
- **Space:** $O(n^2)$
```

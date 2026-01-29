# Solutions: Longest Increasing Subsequence

## 1. Longest Increasing Subsequence (LIS)

**Problem:** Find the length of the longest strictly increasing subsequence.

### Optimal Python Solution ($O(n \log n)$)

````python
import bisect

def length_of_lis(nums: list[int]) -> int:
    # Pattern: Binary Search on tails array
    # tails[i] = smallest tail of all increasing subsequences of length i+1
    tails = []
    for num in nums:
        idx = bisect.bisect_left(tails, num)
        if idx == len(tails):
            tails.append(num)
        else:
            tails[idx] = num
    return len(tails)
```

---

## 5. Longest Increasing Path in a Matrix
**Problem:** Find the length of the longest increasing path in an $m \times n$ integers matrix. You can move up, down, left, or right.

### Optimal Python Solution (DFS + Memoization)
```python
def longest_increasing_path(matrix: list[list[int]]) -> int:
    if not matrix: return 0
    m, n = len(matrix), len(matrix[0])
    memo = [[0] * n for _ in range(m)]

    def dfs(r, c):
        if memo[r][c]: return memo[r][c]

        res = 1
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < m and 0 <= nc < n and matrix[nr][nc] > matrix[r][c]:
                res = max(res, 1 + dfs(nr, nc))

        memo[r][c] = res
        return res

    return max(dfs(r, c) for r in range(m) for c in range(n))
````

### Explanation

1.  **State**: `memo[r][c]` stores the length of the longest increasing path starting from cell `(r, c)`.
2.  **Transitions**: From each cell, we explore all 4 neighbors. If a neighbor has a strictly greater value, we recursively find the longest path from that neighbor and add 1.
3.  **Memoization**: Since we only move to strictly larger values, there are no cycles. Each cell's result is computed once and reused.
4.  **Result**: The answer is the maximum value found across all possible starting cells in the matrix.

### Complexity Analysis

- **Time:** $O(m \times n)$ - Each cell is visited and computed exactly once.
- **Space:** $O(m \times n)$ - For the memoization table and the recursion stack.

````

### Complexity Analysis
- **Time:** $O(n \log n)$ - $n$ iterations, each with a $\log n$ binary search.
- **Space:** $O(n)$ - To store the `tails` array.

---

## 2. Number of Longest Increasing Subsequences
**Problem:** Count how many LIS of maximum length exist.

### Optimal Python Solution
```python
def find_number_of_lis(nums: list[int]) -> int:
    if not nums: return 0
    n = len(nums)
    lengths = [1] * n
    counts = [1] * n

    for i in range(n):
        for j in range(i):
            if nums[j] < nums[i]:
                if lengths[j] + 1 > lengths[i]:
                    lengths[i] = lengths[j] + 1
                    counts[i] = counts[j]
                elif lengths[j] + 1 == lengths[i]:
                    counts[i] += counts[j]

    max_len = max(lengths)
    return sum(c for l, c in zip(lengths, counts) if l == max_len)
````

### Complexity Analysis

- **Time:** $O(n^2)$
- **Space:** $O(n)$

---

## 3. Increasing Triplet Subsequence

**Problem:** Return if there exists an increasing triplet (length 3).

### Optimal Python Solution

```python
def increasing_triplet(nums: list[int]) -> bool:
    first = second = float('inf')
    for n in nums:
        if n <= first:
            first = n
        elif n <= second:
            second = n
        else:
            return True # Found third
    return False
```

### Complexity Analysis

- **Time:** $O(n)$
- **Space:** $O(1)$

---

## 4. Russian Doll Envelopes

**Problem:** Maximize envelopes that fit inside each other (both width and height must be strictly larger).

### Optimal Python Solution

````python
import bisect

def max_envelopes(envelopes: list[list[int]]) -> int:
    # Key: Sort width asc, then height desc for same width
    # This prevents picking two envelopes with same width
    envelopes.sort(key=lambda x: (x[0], -x[1]))

    # Now find LIS on heights
    tails = []
    for _, h in envelopes:
        idx = bisect.bisect_left(tails, h)
        if idx == len(tails):
            tails.append(h)
        else:
            tails[idx] = h
    return len(tails)
```

---

## 5. Longest Increasing Path in a Matrix
**Problem:** Find the length of the longest increasing path in an $m \times n$ integers matrix. You can move up, down, left, or right.

### Optimal Python Solution (DFS + Memoization)
```python
def longest_increasing_path(matrix: list[list[int]]) -> int:
    if not matrix: return 0
    m, n = len(matrix), len(matrix[0])
    memo = [[0] * n for _ in range(m)]

    def dfs(r, c):
        if memo[r][c]: return memo[r][c]

        res = 1
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < m and 0 <= nc < n and matrix[nr][nc] > matrix[r][c]:
                res = max(res, 1 + dfs(nr, nc))

        memo[r][c] = res
        return res

    return max(dfs(r, c) for r in range(m) for c in range(n))
````

### Explanation

1.  **State**: `memo[r][c]` stores the length of the longest increasing path starting from cell `(r, c)`.
2.  **Transitions**: From each cell, we explore all 4 neighbors. If a neighbor has a strictly greater value, we recursively find the longest path from that neighbor and add 1.
3.  **Memoization**: Since we only move to strictly larger values, there are no cycles. Each cell's result is computed once and reused.
4.  **Result**: The answer is the maximum value found across all possible starting cells in the matrix.

### Complexity Analysis

- **Time:** $O(m \times n)$ - Each cell is visited and computed exactly once.
- **Space:** $O(m \times n)$ - For the memoization table and the recursion stack.

```

### Complexity Analysis
- **Time:** $O(n \log n)$
- **Space:** $O(n)$
```

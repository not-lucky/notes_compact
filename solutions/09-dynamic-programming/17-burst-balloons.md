# Solutions: Burst Balloons (Interval DP)

## 1. Burst Balloons

**Problem:** Maximize coins by bursting balloons. Bursting $i$ gives `nums[i-1]*nums[i]*nums[i+1]`.

### Optimal Python Solution

````python
def max_coins(nums: list[int]) -> int:
    # Key Insight: Think about the LAST balloon to burst in a range.
    # If k is last burst in (i, j), its neighbors are i and j.
    vals = [1] + nums + [1]
    n = len(vals)
    dp = [[0] * n for _ in range(n)]

    # length of window (i..j)
    for length in range(2, n):
        for i in range(n - length):
            j = i + length
            for k in range(i + 1, j):
                # coins = (left_bursts) + (right_bursts) + (current_burst_with_fixed_neighbors)
                dp[i][j] = max(dp[i][j],
                               dp[i][k] + dp[k][j] + vals[i] * vals[k] * vals[j])
    return dp[0][n-1]

```
---

## 3. Remove Boxes
**Problem:** Remove consecutive same-color boxes for points (points = count²). Maximize score.

### Optimal Python Solution (3D DP)
```python
def remove_boxes(boxes: list[int]) -> int:
    n = len(boxes)
    memo = {}

    def dp(i, j, k):
        # i, j is range, k is count of boxes with same color as boxes[i]
        # that were left over from a previous removal to the left.
        if i > j: return 0
        state = (i, j, k)
        if state in memo: return memo[state]

        # Optimization: Group same colored boxes at the start
        i0, k0 = i, k
        while i + 1 <= j and boxes[i+1] == boxes[i]:
            i += 1
            k += 1

        # Option 1: Remove boxes[i] and its k attached neighbors
        res = (k + 1) ** 2 + dp(i + 1, j, 0)

        # Option 2: Try to merge boxes[i] with a later box of same color
        for m in range(i + 1, j + 1):
            if boxes[m] == boxes[i]:
                res = max(res, dp(i + 1, m - 1, 0) + dp(m, j, k + 1))

        memo[state] = res
        return res

    return dp(0, n - 1, 0)
````

### Explanation

1.  **The "Sticky" Problem**: Standard 2D DP fails because removing a box can bring two separate groups of the same color together.
2.  **3rd Dimension**: We track `k`, the number of boxes to the left of index `i` that have the same color as `boxes[i]`.
3.  **Recursive Choices**:
    - We can burst the `k+1` group now.
    - Or, we can "save" them and try to find another box of the same color later in the range `(m)`, first clearing everything between `i` and `m`.

### Complexity Analysis

- **Time:** $O(n^4)$
- **Space:** $O(n^3)$

---

## 4. Strange Printer

**Problem:** Printer can print a sequence of same characters. Find min turns to print string `s`.

### Optimal Python Solution

```python
def strange_printer(s: str) -> int:
    if not s: return 0
    # Remove consecutive duplicates: "aaabbb" -> "ab"
    temp = []
    for char in s:
        if not temp or char != temp[-1]:
            temp.append(char)
    s = "".join(temp)
    n = len(s)

    dp = [[0] * n for _ in range(n)]
    for i in range(n): dp[i][i] = 1

    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            # Initial: print s[i] then print rest
            dp[i][j] = 1 + dp[i+1][j]
            for k in range(i + 1, j + 1):
                if s[k] == s[i]:
                    # If s[k] matches s[i], we can print them in one turn
                    # This reduces turns by merging with the subproblem
                    dp[i][j] = min(dp[i][j], dp[i+1][k-1] + dp[k][j])

    return dp[0][n-1]
```

### Explanation

1.  **Pre-processing**: Consecutive identical characters can always be printed in one turn, so we collapse them.
2.  **Interval DP**: `dp[i][j]` is the min turns for `s[i..j]`.
3.  **Optimization**: If `s[i] == s[k]`, we can assume `s[i]` was printed in the same turn as `s[k]`, effectively merging two intervals without adding a turn.

### Complexity Analysis

- **Time:** $O(n^3)$
- **Space:** $O(n^2)$

````

### Complexity Analysis
- **Time:** $O(n^3)$
- **Space:** $O(n^2)$

---

## 2. Minimum Score Triangulation of Polygon
**Problem:** Triangulate polygon, score of triangle is product of vertices. Minimize sum.

### Optimal Python Solution
```python
def min_score_triangulation(values: list[int]) -> int:
    # Identical structure to Burst Balloons / Matrix Chain
    n = len(values)
    dp = [[0] * n for _ in range(n)]

    for length in range(2, n):
        for i in range(n - length):
            j = i + length
            dp[i][j] = float('inf')
            for k in range(i + 1, j):
                dp[i][j] = min(dp[i][j],
                               dp[i][k] + dp[k][j] + values[i] * values[k] * values[j])
    return dp[0][n-1]

```
---

## 3. Remove Boxes
**Problem:** Remove consecutive same-color boxes for points (points = count²). Maximize score.

### Optimal Python Solution (3D DP)
```python
def remove_boxes(boxes: list[int]) -> int:
    n = len(boxes)
    memo = {}

    def dp(i, j, k):
        # i, j is range, k is count of boxes with same color as boxes[i]
        # that were left over from a previous removal to the left.
        if i > j: return 0
        state = (i, j, k)
        if state in memo: return memo[state]

        # Optimization: Group same colored boxes at the start
        i0, k0 = i, k
        while i + 1 <= j and boxes[i+1] == boxes[i]:
            i += 1
            k += 1

        # Option 1: Remove boxes[i] and its k attached neighbors
        res = (k + 1) ** 2 + dp(i + 1, j, 0)

        # Option 2: Try to merge boxes[i] with a later box of same color
        for m in range(i + 1, j + 1):
            if boxes[m] == boxes[i]:
                res = max(res, dp(i + 1, m - 1, 0) + dp(m, j, k + 1))

        memo[state] = res
        return res

    return dp(0, n - 1, 0)
````

### Explanation

1.  **The "Sticky" Problem**: Standard 2D DP fails because removing a box can bring two separate groups of the same color together.
2.  **3rd Dimension**: We track `k`, the number of boxes to the left of index `i` that have the same color as `boxes[i]`.
3.  **Recursive Choices**:
    - We can burst the `k+1` group now.
    - Or, we can "save" them and try to find another box of the same color later in the range `(m)`, first clearing everything between `i` and `m`.

### Complexity Analysis

- **Time:** $O(n^4)$
- **Space:** $O(n^3)$

---

## 4. Strange Printer

**Problem:** Printer can print a sequence of same characters. Find min turns to print string `s`.

### Optimal Python Solution

```python
def strange_printer(s: str) -> int:
    if not s: return 0
    # Remove consecutive duplicates: "aaabbb" -> "ab"
    temp = []
    for char in s:
        if not temp or char != temp[-1]:
            temp.append(char)
    s = "".join(temp)
    n = len(s)

    dp = [[0] * n for _ in range(n)]
    for i in range(n): dp[i][i] = 1

    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            # Initial: print s[i] then print rest
            dp[i][j] = 1 + dp[i+1][j]
            for k in range(i + 1, j + 1):
                if s[k] == s[i]:
                    # If s[k] matches s[i], we can print them in one turn
                    # This reduces turns by merging with the subproblem
                    dp[i][j] = min(dp[i][j], dp[i+1][k-1] + dp[k][j])

    return dp[0][n-1]
```

### Explanation

1.  **Pre-processing**: Consecutive identical characters can always be printed in one turn, so we collapse them.
2.  **Interval DP**: `dp[i][j]` is the min turns for `s[i..j]`.
3.  **Optimization**: If `s[i] == s[k]`, we can assume `s[i]` was printed in the same turn as `s[k]`, effectively merging two intervals without adding a turn.

### Complexity Analysis

- **Time:** $O(n^3)$
- **Space:** $O(n^2)$

```

### Complexity Analysis
- **Time:** $O(n^3)$
- **Space:** $O(n^2)$
```

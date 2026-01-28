# Solutions: Matrix Chain Multiplication (Interval DP)

## 1. Matrix Chain Multiplication

**Problem:** Minimum scalar multiplications to multiply a chain of matrices.

### Optimal Python Solution

````python
def matrix_chain_order(p: list[int]) -> int:
    # State: dp[i][j] = min cost to multiply matrices i through j
    n = len(p) - 1
    dp = [[0] * (n + 1) for _ in range(n + 1)]

    # length of chain
    for length in range(2, n + 1):
        for i in range(1, n - length + 2):
            j = i + length - 1
            dp[i][j] = float('inf')
            # Try all possible split points
            for k in range(i, j):
                cost = dp[i][k] + dp[k+1][j] + p[i-1]*p[k]*p[j]
                dp[i][j] = min(dp[i][j], cost)

    return dp[1][n]

```
---

## 4. Burst Balloons
**Problem:** Maximize coins by bursting balloons. Bursting $i$ gives `nums[i-1]*nums[i]*nums[i+1]`.

### Optimal Python Solution
```python
def max_coins(nums: list[int]) -> int:
    # Key Insight: Consider which balloon is burst LAST in each range.
    # Add virtual 1s at boundaries.
    vals = [1] + nums + [1]
    n = len(vals)
    dp = [[0] * n for _ in range(n)]

    for length in range(2, n):
        for i in range(n - length):
            j = i + length
            for k in range(i + 1, j):
                # coins = (left_bursts) + (right_bursts) + (current_burst_with_neighbors_i_j)
                dp[i][j] = max(dp[i][j],
                               dp[i][k] + dp[k][j] + vals[i] * vals[k] * vals[j])
    return dp[0][n-1]

```
---

## 6. Optimal Binary Search Tree
**Problem:** Given keys and their search frequencies, construct a BST that minimizes total search cost.

### Optimal Python Solution
```python
def optimal_bst(freq: list[int]) -> int:
    n = len(freq)
    # dp[i][j] = min cost for search keys in range i..j
    dp = [[0] * n for _ in range(n)]

    # Prefix sums for range sum of frequencies O(1)
    prefix = [0] * (n + 1)
    for i in range(n): prefix[i+1] = prefix[i] + freq[i]

    # Initialize single keys
    for i in range(n): dp[i][i] = freq[i]

    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            dp[i][j] = float('inf')
            # Try every key in range as root
            weight = prefix[j+1] - prefix[i]
            for r in range(i, j + 1):
                left = dp[i][r-1] if r > i else 0
                right = dp[r+1][j] if r < j else 0
                dp[i][j] = min(dp[i][j], left + right + weight)
    return dp[0][n-1]
````

### Explanation

1.  **The Cost Logic**: If we pick `r` as root for range `(i, j)`, then every node in the left sub-tree `(i..r-1)` and right sub-tree `(r+1..j)` becomes one level deeper. Their contribution to the cost increases by exactly the sum of their frequencies.
2.  **State**: `dp[i][j]` is the minimum cost for range `i` to `j`.
3.  **Recurrence**: `dp[i][j] = min(dp[left] + dp[right] + sum_of_freqs_in_range)`.

### Complexity Analysis

- **Time:** $O(n^3)$
- **Space:** $O(n^2)$

````

### Explanation
1.  **The Core Insight**: If we burst balloon `k` last in the range `(i, j)`, its neighbors at that moment are guaranteed to be `i` and `j` because everything in between has already been burst.
2.  **Interval DP**: We solve for smaller ranges first. `dp[i][j]` represents the max coins from bursting all balloons strictly between index `i` and `j`.
3.  **Boundaries**: Adding 1s at the ends simplifies the multiplication logic for edge balloons.

### Complexity Analysis
- **Time:** $O(n^3)$
- **Space:** $O(n^2)$

---

## 5. Minimum Score Triangulation of Polygon
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

## 6. Optimal Binary Search Tree
**Problem:** Given keys and their search frequencies, construct a BST that minimizes total search cost.

### Optimal Python Solution
```python
def optimal_bst(freq: list[int]) -> int:
    n = len(freq)
    # dp[i][j] = min cost for search keys in range i..j
    dp = [[0] * n for _ in range(n)]

    # Prefix sums for range sum of frequencies O(1)
    prefix = [0] * (n + 1)
    for i in range(n): prefix[i+1] = prefix[i] + freq[i]

    # Initialize single keys
    for i in range(n): dp[i][i] = freq[i]

    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            dp[i][j] = float('inf')
            # Try every key in range as root
            weight = prefix[j+1] - prefix[i]
            for r in range(i, j + 1):
                left = dp[i][r-1] if r > i else 0
                right = dp[r+1][j] if r < j else 0
                dp[i][j] = min(dp[i][j], left + right + weight)
    return dp[0][n-1]
````

### Explanation

1.  **The Cost Logic**: If we pick `r` as root for range `(i, j)`, then every node in the left sub-tree `(i..r-1)` and right sub-tree `(r+1..j)` becomes one level deeper. Their contribution to the cost increases by exactly the sum of their frequencies.
2.  **State**: `dp[i][j]` is the minimum cost for range `i` to `j`.
3.  **Recurrence**: `dp[i][j] = min(dp[left] + dp[right] + sum_of_freqs_in_range)`.

### Complexity Analysis

- **Time:** $O(n^3)$
- **Space:** $O(n^2)$

```

### Explanation
1.  **Polygon Splitting**: Choosing a side `(i, j)` and a vertex `k` forms a triangle `(i, j, k)` and splits the remaining polygon into two smaller polygons `(i..k)` and `(k..j)`.
2.  **Pattern**: This is the same interval DP pattern as Matrix Chain Multiplication and Burst Balloons.

### Complexity Analysis
- **Time:** $O(n^3)$
- **Space:** $O(n^2)$
```

### Complexity Analysis

- **Time:** $O(n^3)$ - Three nested loops: length, starting point, split point.
- **Space:** $O(n^2)$ - To store results for all matrix intervals.

---

## 2. Minimum Cost to Merge Stones

**Problem:** Merge $k$ consecutive piles into one, minimize total cost.

### Optimal Python Solution

````python
def merge_stones(stones: list[int], k: int) -> int:
    n = len(stones)
    if (n - 1) % (k - 1): return -1

    prefix = [0] * (n + 1)
    for i in range(n): prefix[i+1] = prefix[i] + stones[i]

    dp = [[0] * n for _ in range(n)]
    for length in range(k, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            dp[i][j] = float('inf')
            # Split point mid must be such that (mid-i) is divisible by (k-1)
            for mid in range(i, j, k - 1):
                dp[i][j] = min(dp[i][j], dp[i][mid] + dp[mid+1][j])

            # If we can merge the entire range into one pile
            if (j - i) % (k - 1) == 0:
                dp[i][j] += prefix[j+1] - prefix[i]
    return dp[0][n-1]

```
---

## 6. Optimal Binary Search Tree
**Problem:** Given keys and their search frequencies, construct a BST that minimizes total search cost.

### Optimal Python Solution
```python
def optimal_bst(freq: list[int]) -> int:
    n = len(freq)
    # dp[i][j] = min cost for search keys in range i..j
    dp = [[0] * n for _ in range(n)]

    # Prefix sums for range sum of frequencies O(1)
    prefix = [0] * (n + 1)
    for i in range(n): prefix[i+1] = prefix[i] + freq[i]

    # Initialize single keys
    for i in range(n): dp[i][i] = freq[i]

    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            dp[i][j] = float('inf')
            # Try every key in range as root
            weight = prefix[j+1] - prefix[i]
            for r in range(i, j + 1):
                left = dp[i][r-1] if r > i else 0
                right = dp[r+1][j] if r < j else 0
                dp[i][j] = min(dp[i][j], left + right + weight)
    return dp[0][n-1]
````

### Explanation

1.  **The Cost Logic**: If we pick `r` as root for range `(i, j)`, then every node in the left sub-tree `(i..r-1)` and right sub-tree `(r+1..j)` becomes one level deeper. Their contribution to the cost increases by exactly the sum of their frequencies.
2.  **State**: `dp[i][j]` is the minimum cost for range `i` to `j`.
3.  **Recurrence**: `dp[i][j] = min(dp[left] + dp[right] + sum_of_freqs_in_range)`.

### Complexity Analysis

- **Time:** $O(n^3)$
- **Space:** $O(n^2)$

````

### Complexity Analysis
- **Time:** $O(n^3 / k)$
- **Space:** $O(n^2)$

---

## 3. Optimal Binary Search Tree
**Problem:** Search keys with frequencies, minimize total search cost.

### Optimal Python Solution
```python
def optimal_bst(freq: list[int]) -> int:
    n = len(freq)
    dp = [[0] * n for _ in range(n)]

    prefix = [0] * (n + 1)
    for i in range(n): prefix[i+1] = prefix[i] + freq[i]

    for length in range(1, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            dp[i][j] = float('inf')
            weight = prefix[j+1] - prefix[i]
            for r in range(i, j + 1):
                left = dp[i][r-1] if r > i else 0
                right = dp[r+1][j] if r < j else 0
                dp[i][j] = min(dp[i][j], left + right + weight)
    return dp[0][n-1]

```
---

## 6. Optimal Binary Search Tree
**Problem:** Given keys and their search frequencies, construct a BST that minimizes total search cost.

### Optimal Python Solution
```python
def optimal_bst(freq: list[int]) -> int:
    n = len(freq)
    # dp[i][j] = min cost for search keys in range i..j
    dp = [[0] * n for _ in range(n)]

    # Prefix sums for range sum of frequencies O(1)
    prefix = [0] * (n + 1)
    for i in range(n): prefix[i+1] = prefix[i] + freq[i]

    # Initialize single keys
    for i in range(n): dp[i][i] = freq[i]

    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            dp[i][j] = float('inf')
            # Try every key in range as root
            weight = prefix[j+1] - prefix[i]
            for r in range(i, j + 1):
                left = dp[i][r-1] if r > i else 0
                right = dp[r+1][j] if r < j else 0
                dp[i][j] = min(dp[i][j], left + right + weight)
    return dp[0][n-1]
````

### Explanation

1.  **The Cost Logic**: If we pick `r` as root for range `(i, j)`, then every node in the left sub-tree `(i..r-1)` and right sub-tree `(r+1..j)` becomes one level deeper. Their contribution to the cost increases by exactly the sum of their frequencies.
2.  **State**: `dp[i][j]` is the minimum cost for range `i` to `j`.
3.  **Recurrence**: `dp[i][j] = min(dp[left] + dp[right] + sum_of_freqs_in_range)`.

### Complexity Analysis

- **Time:** $O(n^3)$
- **Space:** $O(n^2)$

```

### Complexity Analysis
- **Time:** $O(n^3)$
- **Space:** $O(n^2)$
```

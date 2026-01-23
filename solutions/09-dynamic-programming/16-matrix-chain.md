# Matrix Chain Multiplication Solutions

## Problem: Matrix Chain Multiplication
Given a sequence of matrices, find the most efficient way to multiply these matrices together. The problem is not actually to perform the multiplications, but merely to decide in which order to perform the multiplications.

### Constraints
- 2 <= n <= 100
- 1 <= p[i] <= 100

### Implementation

```python
def matrix_chain_order(p: list[int]) -> int:
    """
    Finds min multiplications needed to multiply n matrices.
    p[i-1] x p[i] is the dimension of the i-th matrix.
    Time complexity: O(n^3)
    Space complexity: O(n^2)
    """
    n = len(p) - 1
    # dp[i][j] is the min multiplications for matrices i to j
    dp = [[0] * (n + 1) for _ in range(n + 1)]

    for length in range(2, n + 1):
        for i in range(1, n - length + 2):
            j = i + length - 1
            dp[i][j] = float('inf')
            for k in range(i, j):
                # Split point k
                cost = dp[i][k] + dp[k+1][j] + p[i-1] * p[k] * p[j]
                dp[i][j] = min(dp[i][j], cost)

    return dp[1][n]
```

## Problem: Minimum Cost to Merge Stones
There are `n` piles of stones arranged in a row. The `i-th` pile has `stones[i]` stones. A move consists of merging exactly `k` consecutive piles into one pile, and the cost of this move is equal to the total number of stones in these `k` piles. Find the minimum cost to merge all piles of stones into one pile. If it is impossible, return -1.

### Implementation

```python
def merge_stones(stones: list[int], k: int) -> int:
    """
    Min cost to merge n piles into 1 using k-way merges.
    Time complexity: O(n^3 / k)
    Space complexity: O(n^2)
    """
    n = len(stones)
    if (n - 1) % (k - 1) != 0:
        return -1

    prefix_sums = [0] * (n + 1)
    for i in range(n):
        prefix_sums[i+1] = prefix_sums[i] + stones[i]

    # dp[i][j] is min cost to merge stones[i:j+1] as much as possible
    dp = [[0] * n for _ in range(n)]

    for length in range(k, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            dp[i][j] = float('inf')
            # Split point mid must ensure left/right can be merged
            for mid in range(i, j, k - 1):
                dp[i][j] = min(dp[i][j], dp[i][mid] + dp[mid+1][j])

            # If the current range [i, j] can be merged into 1 pile
            if (j - i) % (k - 1) == 0:
                dp[i][j] += prefix_sums[j+1] - prefix_sums[i]

    return dp[0][n-1]
```

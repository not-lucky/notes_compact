# Climbing Stairs

## Problem Statement

You are climbing a staircase. It takes `n` steps to reach the top. Each time you can either climb 1 or 2 steps.

In how many distinct ways can you climb to the top?

**Example:**
```
Input: n = 3
Output: 3
Explanation: Three ways: 1+1+1, 1+2, 2+1

Input: n = 5
Output: 8
```

## Approach

### Key Insight
To reach step n, you can come from:
- Step n-1 (taking 1 step)
- Step n-2 (taking 2 steps)

So: `ways(n) = ways(n-1) + ways(n-2)`

This is the Fibonacci sequence!

### Methods
1. **Recursion with Memoization**: Top-down
2. **Dynamic Programming**: Bottom-up with array
3. **Optimized DP**: O(1) space with two variables
4. **Matrix Exponentiation**: O(log n) time

## Implementation

```python
def climb_stairs(n: int) -> int:
    """
    Count ways using optimized DP.

    Time: O(n)
    Space: O(1)
    """
    if n <= 2:
        return n

    prev2 = 1  # ways to reach step 1
    prev1 = 2  # ways to reach step 2

    for _ in range(3, n + 1):
        current = prev1 + prev2
        prev2 = prev1
        prev1 = current

    return prev1


def climb_stairs_dp_array(n: int) -> int:
    """
    DP with array (more intuitive).

    Time: O(n)
    Space: O(n)
    """
    if n <= 2:
        return n

    dp = [0] * (n + 1)
    dp[1] = 1
    dp[2] = 2

    for i in range(3, n + 1):
        dp[i] = dp[i-1] + dp[i-2]

    return dp[n]


def climb_stairs_memo(n: int) -> int:
    """
    Recursive with memoization.

    Time: O(n)
    Space: O(n)
    """
    memo = {}

    def helper(step: int) -> int:
        if step <= 2:
            return step
        if step in memo:
            return memo[step]

        memo[step] = helper(step - 1) + helper(step - 2)
        return memo[step]

    return helper(n)


def climb_stairs_matrix(n: int) -> int:
    """
    Matrix exponentiation for O(log n) time.

    [F(n+1)]   [1 1]^n   [1]
    [F(n)  ] = [1 0]   × [0]

    Time: O(log n)
    Space: O(1)
    """
    def matrix_mult(A, B):
        return [
            [A[0][0]*B[0][0] + A[0][1]*B[1][0], A[0][0]*B[0][1] + A[0][1]*B[1][1]],
            [A[1][0]*B[0][0] + A[1][1]*B[1][0], A[1][0]*B[0][1] + A[1][1]*B[1][1]]
        ]

    def matrix_pow(M, p):
        result = [[1, 0], [0, 1]]  # Identity
        while p:
            if p & 1:
                result = matrix_mult(result, M)
            M = matrix_mult(M, M)
            p >>= 1
        return result

    if n <= 2:
        return n

    M = [[1, 1], [1, 0]]
    result = matrix_pow(M, n)
    return result[0][0]
```

## Complexity Analysis

| Method | Time | Space | Notes |
|--------|------|-------|-------|
| Optimized DP | O(n) | O(1) | Best for interviews |
| DP Array | O(n) | O(n) | More intuitive |
| Memoization | O(n) | O(n) | Top-down approach |
| Matrix Exp | O(log n) | O(1) | Fastest |

## Visual Walkthrough

```
n = 5

Ways to reach each step:
Step 1: 1 way (just take 1 step)
Step 2: 2 ways (1+1 or 2)
Step 3: 3 ways (from step 1 + from step 2 = 1+2)
Step 4: 5 ways (2+3)
Step 5: 8 ways (3+5)

         Ways
Step 1:    1
Step 2:    2
Step 3:    3  = 1 + 2
Step 4:    5  = 2 + 3
Step 5:    8  = 3 + 5
```

## Edge Cases

1. **n = 0**: 0 or 1 (depends on interpretation)
2. **n = 1**: 1 way
3. **n = 2**: 2 ways
4. **Large n**: May need modulo for overflow in some problems

## Common Mistakes

1. **Base case off by one**: n=1 → 1, n=2 → 2
2. **Forgetting memoization**: Exponential without it
3. **Array index errors**: Careful with 0 vs 1 indexing
4. **Integer overflow**: Use long or modulo for large n

## Variations

### Climbing Stairs with k Steps
```python
def climb_stairs_k_steps(n: int, k: int) -> int:
    """
    Can take 1, 2, ..., k steps at a time.

    Time: O(n × k)
    Space: O(n)
    """
    dp = [0] * (n + 1)
    dp[0] = 1

    for i in range(1, n + 1):
        for j in range(1, min(i, k) + 1):
            dp[i] += dp[i - j]

    return dp[n]
```

### Min Cost Climbing Stairs
```python
def min_cost_climbing_stairs(cost: list[int]) -> int:
    """
    Pay cost[i] to step on stair i.
    Find minimum cost to reach top.

    Time: O(n)
    Space: O(1)
    """
    n = len(cost)
    prev2 = 0  # cost to reach step 0
    prev1 = 0  # cost to reach step 1

    for i in range(2, n + 1):
        current = min(prev1 + cost[i-1], prev2 + cost[i-2])
        prev2 = prev1
        prev1 = current

    return prev1
```

### Climbing Stairs with Forbidden Steps
```python
def climb_stairs_forbidden(n: int, forbidden: set) -> int:
    """
    Some step sizes are forbidden.
    """
    if n <= 0:
        return 1 if n == 0 else 0

    dp = [0] * (n + 1)
    dp[0] = 1

    for i in range(1, n + 1):
        for step in [1, 2]:
            if step not in forbidden and i >= step:
                dp[i] += dp[i - step]

    return dp[n]
```

### Distinct Ways to Reach Target (Combination Sum IV)
```python
def combination_sum_iv(nums: list[int], target: int) -> int:
    """
    Given nums (step sizes), count ways to reach target.
    Order matters (1+2 ≠ 2+1).

    Time: O(target × len(nums))
    Space: O(target)
    """
    dp = [0] * (target + 1)
    dp[0] = 1

    for i in range(1, target + 1):
        for num in nums:
            if i >= num:
                dp[i] += dp[i - num]

    return dp[target]
```

## Related Problems

- **Min Cost Climbing Stairs** - Add costs to steps
- **House Robber** - Similar recurrence relation
- **Fibonacci Number** - Identical mathematical structure
- **Decode Ways** - Similar counting problem
- **Unique Paths** - 2D version of this problem
- **Combination Sum IV** - Generalized step sizes

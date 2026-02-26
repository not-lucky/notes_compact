# Coin Change

> **Prerequisites:** [03-1d-dp-basics](./03-1d-dp-basics.md)

## Overview

Coin Change is the canonical unbounded knapsack problem where you find the minimum/count of ways to reach a target amount using unlimited coins of given denominations.

## Building Intuition

**Why does Coin Change work with DP?**

1. **Optimal Substructure**: If the optimal way to make amount 11 uses a coin of value 5, then the remaining 6 must also be made optimally. Using a suboptimal solution for 6 would make the overall solution suboptimal.

2. **Overlapping Subproblems**: To make 11, we try subtracting each coin denomination. If coins = [1, 5], we need solutions for 10 and 6. But making 10 also needs 6! Subproblems overlap heavily.

3. **Why Greedy Fails**: Greedy (always use largest coin) fails for coins = [1, 3, 4], amount = 6. Greedy: 4+1+1 = 3 coins. Optimal: 3+3 = 2 coins.

4. **The Unbounded Nature**: Unlike 0/1 knapsack, we can use each coin infinitely. This changes the iteration direction: we iterate forward through amounts so updated values can be reused (allowing multiple uses of same coin).

5. **Mental Model**: Think of building a staircase. To reach step N, you can hop from any step that's exactly one coin-value behind. The minimum hops to N is 1 + minimum hops to the best previous step.

6. **Counting vs Minimizing**: For counting ways, we add possibilities (dp[amount] += dp[amount - coin]). For minimizing coins, we take min (dp[amount] = min(dp[amount], dp[amount - coin] + 1)).

## Interview Context

Coin Change is a must-know problem because:

1. **Classic unbounded knapsack**: Unlimited use of each item
2. **Two variants**: Min coins (optimization) and count ways (counting)
3. **Foundation for harder problems**: Knapsack, subset sum
4. **Interview staple**: Amazon, Google, Meta favorites

---

## When NOT to Use Coin Change Pattern

1. **Limited Coin Usage**: If each coin can only be used once, this is 0/1 Knapsack, not Coin Change. Use backward iteration instead of forward.

2. **Greedy Works for Canonical Systems**: For "canonical" coin systems (like US currency: 1, 5, 10, 25), greedy actually works. Only use DP when coins are arbitrary.

3. **Order Matters (Permutations)**: Coin Change counts combinations (1+2 = 2+1). If order matters, you need different loop ordering (amount outer, coins inner).

4. **Very Large Amounts**: For amount = 10^9 with few coins, DP array is too large. Consider matrix exponentiation or formula-based approaches.

5. **Negative Coin Values**: Coin Change assumes positive denominations. Negative values break the subproblem ordering.

**Recognize Coin Change Pattern When:**

- Unlimited use of items
- Target sum/amount to reach
- Minimize count OR count combinations
- All values positive

---

## Problem 1: Minimum Coins

Find minimum number of coins to make amount. Return -1 if impossible.

**Mathematical Recurrence:**
$$
dp[i] = \begin{cases}
0 & \text{if } i = 0 \\
\min_{c \in coins, c \le i} (dp[i - c] + 1) & \text{if } i > 0
\end{cases}
$$

**Base Case Explained:**
`dp[0] = 0`: It takes exactly 0 coins to make the amount 0. All other amounts are initialized to infinity (`float('inf')`), because initially, we don't know if they can be made at all.

### Bottom-Up Solution

```python
def coin_change(coins: list[int], amount: int) -> int:
    """
    Minimum coins to make amount.

    State: dp[i] = min coins to make amount i
    Recurrence: dp[i] = min(dp[i - coin] + 1) for each coin

    Time: O(amount × len(coins))
    Space: O(amount)
    """
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0  # 0 coins for amount 0

    for i in range(1, amount + 1):
        for coin in coins:
            if coin <= i and dp[i - coin] != float('inf'):
                dp[i] = min(dp[i], dp[i - coin] + 1)

    return dp[amount] if dp[amount] != float('inf') else -1
```

### Top-Down Solution

```python
def coin_change_memo(coins: list[int], amount: int) -> int:
    """
    Memoized recursive solution.
    """
    from functools import lru_cache

    @lru_cache(maxsize=None)
    def dp(remaining: int) -> int:
        if remaining == 0:
            return 0
        if remaining < 0:
            return float('inf')

        min_coins = float('inf')
        for coin in coins:
            result = dp(remaining - coin)
            if result != float('inf'):
                min_coins = min(min_coins, result + 1)

        return min_coins

    result = dp(amount)
    return result if result != float('inf') else -1
```

### Visual Walkthrough

**Coin Change DP Table:**
`coins = [1, 2, 5]`, `amount = 5`

| i | 0 | 1 | 2 | 3 | 4 | 5 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `dp[i]` | 0 | 1 | 1 | 2 | 2 | 1 |

*Explanation for `dp[5]`*:
- From coin `1`: `dp[5-1] + 1` = `dp[4] + 1` = `2 + 1 = 3`
- From coin `2`: `dp[5-2] + 1` = `dp[3] + 1` = `2 + 1 = 3`
- From coin `5`: `dp[5-5] + 1` = `dp[0] + 1` = `0 + 1 = 1`
- `dp[5] = \min(3, 3, 1) = 1`

---

## Problem 2: Number of Ways (Coin Change II)

Count number of ways to make amount using coins.

**Mathematical Recurrence:**
$$
dp[i] = \begin{cases}
1 & \text{if } i = 0 \\
\sum_{c \in coins, c \le i} dp[i - c] & \text{if } i > 0
\end{cases}
$$

**Base Case Explained:**
`dp[0] = 1`: There is exactly 1 way to make the amount 0 (by using no coins). This is the foundation of the counting DP; if this was 0, multiplying/adding from it would yield 0 for all states. All other states are initialized to 0.

### Visual Walkthrough

**Coin Change II DP Table:**
`coins = [1, 2]`, `amount = 3`

| i (amount) | 0 | 1 | 2 | 3 |
| :--- | :--- | :--- | :--- | :--- |
| Initial `dp` | 1 | 0 | 0 | 0 |
| After coin `1` | 1 | 1 | 1 | 1 |
| After coin `2` | 1 | 1 | 2 | 2 |

*Explanation*:
- Initial: `dp[0] = 1` (1 way to make 0), rest are 0.
- Coin `1`: Updates `dp[1]`, `dp[2]`, `dp[3]`. `dp[i] += dp[i-1]`.
  - `dp[1] += dp[0]` → 1
  - `dp[2] += dp[1]` → 1
  - `dp[3] += dp[2]` → 1
- Coin `2`: Updates `dp[2]`, `dp[3]`. `dp[i] += dp[i-2]`.
  - `dp[2] += dp[0]` → `1 + 1 = 2` ways (`{1,1}`, `{2}`)
  - `dp[3] += dp[1]` → `1 + 1 = 2` ways (`{1,1,1}`, `{1,2}`)

### Bottom-Up Solution (Combinations)

**Forward Iteration vs Backward Iteration**
In unbounded knapsack problems like Coin Change, we can reuse the same coin multiple times. To achieve this, we iterate **forward** through the amounts (`for i in range(coin, amount + 1)`). When computing `dp[i]`, we rely on `dp[i - coin]`, which may have *already* been updated using the same coin in the current iteration. This allows the coin to be used multiple times.

In contrast, 0/1 Knapsack uses **backward** iteration (`for i in range(amount, coin - 1, -1)`) to ensure each item is only used once, because `dp[i]` then relies on the *un-updated* previous state of the array from the previous item's iteration.

```python
def change(amount: int, coins: list[int]) -> int:
    """
    Count combinations (order doesn't matter).

    Key: Iterate coins in outer loop to avoid duplicates.

    Time: O(amount × len(coins))
    Space: O(amount)
    """
    dp = [0] * (amount + 1)
    dp[0] = 1  # One way to make 0

    # Process each coin completely before next
    for coin in coins:
        for i in range(coin, amount + 1):
            dp[i] += dp[i - coin]

    return dp[amount]
```

### Top-Down Solution (Combinations)

```python
def change_memo(amount: int, coins: list[int]) -> int:
    """
    Memoized recursive solution for counting combinations.

    State requires both the current amount and coin index to avoid
    duplicate combinations (e.g., treating {1,2} and {2,1} as the same).

    Time: O(amount × len(coins))
    Space: O(amount × len(coins)) for the memoization cache
    """
    from functools import lru_cache

    @lru_cache(maxsize=None)
    def dp(idx: int, remaining: int) -> int:
        # Base cases
        if remaining == 0:
            return 1
        if remaining < 0 or idx == len(coins):
            return 0

        # Option 1: Use the current coin (stay at same idx since unbounded)
        include = dp(idx, remaining - coins[idx])

        # Option 2: Skip the current coin, move to next
        skip = dp(idx + 1, remaining)

        return include + skip

    return dp(0, amount)
```

### Why Outer Coin Loop?

```
coins = [1, 2], amount = 3

CORRECT (coins outer - combinations):
After coin 1: dp = [1, 1, 1, 1]  (ways: empty, 1, 1+1, 1+1+1)
After coin 2: dp = [1, 1, 2, 2]  (add: 2, 2+1)
Combinations: {1+1+1}, {1+2} = 2 ways

WRONG (amount outer - permutations):
dp[1] = 1 (just 1)
dp[2] = 2 (1+1, 2)
dp[3] = 3 (1+1+1, 1+2, 2+1)  ← Counts 1+2 and 2+1 separately!
```

### Order Matters (Permutations)

**Mathematical Recurrence:**
$$
dp[i] = \begin{cases}
1 & \text{if } i = 0 \\
\sum_{c \in coins, c \le i} dp[i - c] & \text{if } i > 0
\end{cases}
$$

*(Note: The recurrence looks mathematically identical to combinations, but the state evaluation order changes the result. Here we build the sum by iterating $i$ first, treating $1+2$ and $2+1$ as distinct paths to reach $i$.)*

```python
def num_ways_permutations(amount: int, coins: list[int]) -> int:
    """
    Count permutations (order matters).

    Key: Iterate amount in outer loop.

    Time: O(amount × len(coins))
    Space: O(amount)
    """
    dp = [0] * (amount + 1)
    dp[0] = 1

    # Process each amount, try all coins
    for i in range(1, amount + 1):
        for coin in coins:
            if coin <= i:
                dp[i] += dp[i - coin]

    return dp[amount]
```

---

## Comparison: Combinations vs Permutations

| Aspect          | Combinations   | Permutations            |
| --------------- | -------------- | ----------------------- |
| Loop order      | Coins outer    | Amount outer            |
| {1,2} and {2,1} | Same           | Different               |
| Use case        | Coin Change II | Climbing Stairs variant |

---

## Variation: Fewest Coins with Path

By storing the last coin added in `parent[i]`, we can reconstruct the optimal path backwards from `amount` down to `0`.

```python
def coin_change_with_path(coins: list[int], amount: int) -> tuple:
    """
    Return (min_coins, coins_used).
    """
    dp = [float('inf')] * (amount + 1)
    parent = [-1] * (amount + 1)
    dp[0] = 0

    for i in range(1, amount + 1):
        for coin in coins:
            if coin <= i and dp[i - coin] + 1 < dp[i]:
                dp[i] = dp[i - coin] + 1
                parent[i] = coin

    if dp[amount] == float('inf'):
        return -1, []

    # Reconstruct path
    coins_used = []
    curr = amount
    while curr > 0:
        coins_used.append(parent[curr])
        curr -= parent[curr]

    return dp[amount], coins_used
```

---

## Related: Perfect Squares

Minimum perfect squares that sum to n.

**Mathematical Recurrence:**
$$
dp[i] = \begin{cases}
0 & \text{if } i = 0 \\
\min_{1 \le j^2 \le i} (dp[i - j^2] + 1) & \text{if } i > 0
\end{cases}
$$

```python
def num_squares(n: int) -> int:
    """
    Same as coin change with coins = [1, 4, 9, 16, ...].

    Time: O(n√n)
    Space: O(n)
    """
    dp = [float('inf')] * (n + 1)
    dp[0] = 0

    for i in range(1, n + 1):
        j = 1
        while j * j <= i:
            dp[i] = min(dp[i], dp[i - j * j] + 1)
            j += 1

    return dp[n]
```

---

## Related: Combination Sum IV

Count permutations of nums that sum to target.

**Mathematical Recurrence:**
$$
dp[i] = \begin{cases}
1 & \text{if } i = 0 \\
\sum_{num \in nums, num \le i} dp[i - num] & \text{if } i > 0
\end{cases}
$$

```python
def combination_sum_4(nums: list[int], target: int) -> int:
    """
    Count permutations of nums that sum to target.

    Same as coin change permutation version.

    Time: O(target × len(nums))
    Space: O(target)
    """
    dp = [0] * (target + 1)
    dp[0] = 1

    for i in range(1, target + 1):
        for num in nums:
            if num <= i:
                dp[i] += dp[i - num]

    return dp[target]
```

---

## BFS Alternative for Min Coins

```python
from collections import deque

def coin_change_bfs(coins: list[int], amount: int) -> int:
    """
    BFS approach - finds minimum naturally.

    Time: O(amount × len(coins))
    Space: O(amount)
    """
    if amount == 0:
        return 0

    visited = set([0])
    queue = deque([(0, 0)])  # (current_sum, num_coins)

    while queue:
        curr_sum, num_coins = queue.popleft()

        for coin in coins:
            next_sum = curr_sum + coin

            if next_sum == amount:
                return num_coins + 1

            if next_sum < amount and next_sum not in visited:
                visited.add(next_sum)
                queue.append((next_sum, num_coins + 1))

    return -1
```

---

## Edge Cases

```python
# 1. Amount is 0
amount = 0
# Return 0 (no coins needed)

# 2. Impossible amount
coins = [2], amount = 3
# Return -1

# 3. Single coin equals amount
coins = [5], amount = 5
# Return 1

# 4. Large amount, small coins
coins = [1], amount = 1000
# Return 1000

# 5. No coins
coins = [], amount = 5
# Return -1
```

---

## Common Mistakes

```python
# WRONG: Using 0 as impossible marker
dp = [0] * (amount + 1)
dp[0] = 0
for coin in coins:
    if dp[i - coin] != 0:  # Wrong! 0 is valid for amount 0

# CORRECT: Use infinity
dp = [float('inf')] * (amount + 1)
dp[0] = 0


# WRONG: Combinations vs permutations confusion
# This counts permutations, not combinations!
for i in range(amount + 1):
    for coin in coins:
        dp[i] += dp[i - coin]


# WRONG: Not checking coin <= i
for coin in coins:
    dp[i] = min(dp[i], dp[i - coin] + 1)  # IndexError when coin > i

# CORRECT:
for coin in coins:
    if coin <= i:
        dp[i] = min(dp[i], dp[i - coin] + 1)
```

---

## Greedy Doesn't Work

```
coins = [1, 3, 4], amount = 6

Greedy: 4 + 1 + 1 = 3 coins
Optimal: 3 + 3 = 2 coins

Greedy fails because larger coin isn't always better!
```

---

## Complexity Analysis

| Problem         | Time              | Space     |
| --------------- | ----------------- | --------- |
| Min coins       | O(amount × coins) | O(amount) |
| Count ways      | O(amount × coins) | O(amount) |
| Perfect squares | O(n√n)            | O(n)      |

---

## Interview Tips

1. **Clarify the variant**: Min coins or count ways?
2. **Order matters?**: Affects loop structure
3. **Handle impossible**: Return -1 or 0 appropriately
4. **Explain greedy failure**: Shows deeper understanding
5. **Know both approaches**: Top-down and bottom-up

---

## Practice Problems

| #   | Problem            | Difficulty | Variant            |
| --- | ------------------ | ---------- | ------------------ |
| 1   | Coin Change        | Medium     | Min coins          |
| 2   | Coin Change II     | Medium     | Count combinations |
| 3   | Perfect Squares    | Medium     | Special coins      |
| 4   | Combination Sum IV | Medium     | Count permutations |
| 5   | Integer Break      | Medium     | Max product        |

---

## Key Takeaways

1. **Unbounded knapsack**: Each coin usable unlimited times
2. **Combinations vs permutations**: Loop order matters
3. **Infinity for impossible**: Not 0
4. **Greedy fails**: Must use DP
5. **Space O(amount)**: 1D array sufficient

---

## Next: [06-longest-increasing-subsequence.md](./06-longest-increasing-subsequence.md)

Learn the LIS pattern with O(n log n) optimization.

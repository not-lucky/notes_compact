# Unbounded Knapsack

> **Prerequisites:** [10-knapsack-01](./10-knapsack-01.md)

## Interview Context

Unbounded Knapsack is important because:

1. **Unlimited item usage**: Each item can be used multiple times
2. **Different iteration**: Forward instead of backward
3. **Common applications**: Coin change, rod cutting
4. **Contrast with 0/1**: Tests understanding of both patterns

---

## Problem Statement

Given weights and values of n items with unlimited supply, find maximum value that fits in capacity W.

```
Input:
  weights = [1, 3, 4, 5]
  values = [10, 40, 50, 70]
  capacity = 8

Output: 110
Explanation: Take weight-1 item 3 times + weight-5 item once
            (3×10 + 1×70 = 100) or other combinations
            Actually: two weight-4 items (2×50 = 100) or
            weight-3 twice + weight-1 twice = 80 + 20 = 100
            Best: 8 items of weight 1 = 80... let me recalculate
            weight-3 + weight-5 = 40 + 70 = 110 ✓
```

---

## Solution

```python
def unbounded_knapsack(weights: list[int], values: list[int],
                        capacity: int) -> int:
    """
    Unbounded knapsack - items can be used unlimited times.

    Key difference from 0/1: Iterate FORWARD through capacity.

    Time: O(n × W)
    Space: O(W)
    """
    dp = [0] * (capacity + 1)

    for w in range(1, capacity + 1):
        for i in range(len(weights)):
            if weights[i] <= w:
                dp[w] = max(dp[w], dp[w - weights[i]] + values[i])

    return dp[capacity]
```

### Alternative: Item-First Iteration

```python
def unbounded_knapsack_alt(weights: list[int], values: list[int],
                            capacity: int) -> int:
    """
    Alternative: Process each item, forward through capacity.
    """
    n = len(weights)
    dp = [0] * (capacity + 1)

    for i in range(n):
        for w in range(weights[i], capacity + 1):  # Forward!
            dp[w] = max(dp[w], dp[w - weights[i]] + values[i])

    return dp[capacity]
```

---

## Why Forward Iteration Works

```
For unbounded, we WANT to use same item multiple times.

weights = [2], values = [3], capacity = 6

Forward iteration:
w=2: dp[2] = max(0, dp[0] + 3) = 3   (1 item)
w=4: dp[4] = max(0, dp[2] + 3) = 6   (2 items)
w=6: dp[6] = max(0, dp[4] + 3) = 9   (3 items) ✓
```

---

## Related: Coin Change (Min Coins)

```python
def coin_change(coins: list[int], amount: int) -> int:
    """
    Minimum coins to make amount.

    Time: O(amount × len(coins))
    Space: O(amount)
    """
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0

    for a in range(1, amount + 1):
        for coin in coins:
            if coin <= a and dp[a - coin] != float('inf'):
                dp[a] = min(dp[a], dp[a - coin] + 1)

    return dp[amount] if dp[amount] != float('inf') else -1
```

---

## Related: Coin Change II (Count Ways)

```python
def change(amount: int, coins: list[int]) -> int:
    """
    Count combinations to make amount.

    Key: Process coins in outer loop to avoid counting permutations.

    Time: O(amount × len(coins))
    Space: O(amount)
    """
    dp = [0] * (amount + 1)
    dp[0] = 1

    for coin in coins:  # Coin outer loop
        for a in range(coin, amount + 1):
            dp[a] += dp[a - coin]

    return dp[amount]
```

---

## Related: Rod Cutting

```python
def rod_cutting(prices: list[int], n: int) -> int:
    """
    Maximum revenue from cutting rod of length n.
    prices[i] = price of rod of length i+1.

    Time: O(n²)
    Space: O(n)
    """
    dp = [0] * (n + 1)

    for length in range(1, n + 1):
        for cut in range(1, length + 1):
            dp[length] = max(dp[length],
                            prices[cut - 1] + dp[length - cut])

    return dp[n]
```

---

## Related: Integer Break

```python
def integer_break(n: int) -> int:
    """
    Break n into sum of integers, maximize product.

    Time: O(n²)
    Space: O(n)
    """
    if n <= 3:
        return n - 1

    dp = [0] * (n + 1)
    dp[1] = 1
    dp[2] = 1

    for i in range(3, n + 1):
        for j in range(1, i):
            # j * (i-j): don't break further
            # j * dp[i-j]: break (i-j) further
            dp[i] = max(dp[i], j * (i - j), j * dp[i - j])

    return dp[n]
```

---

## Related: Perfect Squares

```python
def num_squares(n: int) -> int:
    """
    Minimum perfect squares that sum to n.

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

## 0/1 vs Unbounded Comparison

| Aspect | 0/1 Knapsack | Unbounded Knapsack |
|--------|--------------|-------------------|
| Item usage | Once | Unlimited |
| Iteration | Backward | Forward |
| Example | Subset sum | Coin change |
| Key insight | Use dp[i-1] values | Use dp[i] values |

### Side-by-Side Code

```python
# 0/1 Knapsack - Backward
for i in range(n):
    for w in range(capacity, weights[i] - 1, -1):  # Backward
        dp[w] = max(dp[w], dp[w - weights[i]] + values[i])

# Unbounded Knapsack - Forward
for i in range(n):
    for w in range(weights[i], capacity + 1):  # Forward
        dp[w] = max(dp[w], dp[w - weights[i]] + values[i])
```

---

## Combinations vs Permutations

```python
# Combinations (order doesn't matter): Coin outer loop
for coin in coins:
    for amount in range(coin, target + 1):
        dp[amount] += dp[amount - coin]
# [1,2] and [2,1] counted once

# Permutations (order matters): Amount outer loop
for amount in range(1, target + 1):
    for coin in coins:
        if coin <= amount:
            dp[amount] += dp[amount - coin]
# [1,2] and [2,1] counted separately
```

---

## Edge Cases

```python
# 1. Zero capacity
capacity = 0
# Return 0

# 2. Single item larger than capacity
weights = [10]
values = [100]
capacity = 5
# Return 0

# 3. Capacity exactly fits one item
weights = [5]
values = [10]
capacity = 5
# Return 10

# 4. Large capacity, small weights
weights = [1]
values = [1]
capacity = 1000
# Return 1000
```

---

## Common Mistakes

```python
# WRONG: Using backward iteration for unbounded
for w in range(capacity, weights[i] - 1, -1):  # Wrong!
    dp[w] = max(dp[w], dp[w - weights[i]] + values[i])
# Only uses each item once!

# CORRECT: Forward iteration
for w in range(weights[i], capacity + 1):
    dp[w] = max(dp[w], dp[w - weights[i]] + values[i])


# WRONG: Wrong loop order for counting combinations
for amount in range(1, target + 1):  # Amount first
    for coin in coins:
        dp[amount] += dp[amount - coin]
# This counts permutations, not combinations!
```

---

## Complexity

| Problem | Time | Space |
|---------|------|-------|
| Unbounded Knapsack | O(n × W) | O(W) |
| Coin Change | O(amount × coins) | O(amount) |
| Rod Cutting | O(n²) | O(n) |
| Perfect Squares | O(n√n) | O(n) |

---

## Interview Tips

1. **Identify unbounded**: "Unlimited supply" or "each item multiple times"
2. **Know iteration direction**: Forward for unbounded
3. **Combinations vs permutations**: Loop order matters
4. **Compare with 0/1**: Show understanding of both
5. **Common problems**: Coin change, rod cutting

---

## Practice Problems

| # | Problem | Difficulty | Type |
|---|---------|------------|------|
| 1 | Coin Change | Medium | Min coins |
| 2 | Coin Change II | Medium | Count ways |
| 3 | Perfect Squares | Medium | Min squares |
| 4 | Integer Break | Medium | Max product |
| 5 | Cutting a Rod | Medium | Max value |

---

## Key Takeaways

1. **Forward iteration**: Allows reusing items
2. **Same item multiple times**: Key difference from 0/1
3. **Loop order for counting**: Coins first = combinations
4. **Common applications**: Coin change, rod cutting
5. **Compare with 0/1**: Essential interview knowledge

---

## Next: [12-palindrome-dp.md](./12-palindrome-dp.md)

Learn palindrome-related DP problems.

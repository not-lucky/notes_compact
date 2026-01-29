# Solutions: Unbounded Knapsack Patterns

## 1. Unbounded Knapsack (Basic)

**Problem:** Maximize value within capacity $W$ using each item unlimited times.

### Optimal Python Solution

```python
def unbounded_knapsack(weights: list[int], values: list[int], capacity: int) -> int:
    # Key: Iterate FORWARD through capacity to allow reuse of items
    dp = [0] * (capacity + 1)
    for i in range(len(weights)):
        for w in range(weights[i], capacity + 1):
            dp[w] = max(dp[w], dp[w - weights[i]] + values[i])
    return dp[capacity]
```

### Complexity Analysis

- **Time:** $O(n \times W)$
- **Space:** $O(W)$

---

## 2. Coin Change (Min Coins)

**Problem:** Minimum coins to make total amount.

### Optimal Python Solution

```python
def coin_change(coins: list[int], amount: int) -> int:
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    for coin in coins:
        for i in range(coin, amount + 1):
            dp[i] = min(dp[i], dp[i - coin] + 1)
    return dp[amount] if dp[amount] != float('inf') else -1
```

### Complexity Analysis

- **Time:** $O(\text{amount} \times |coins|)$
- **Space:** $O(\text{amount})$

---

## 3. Cutting a Rod

**Problem:** Maximize revenue from cutting rod of length $n$.

### Optimal Python Solution

```python
def rod_cutting(prices: list[int], n: int) -> int:
    # prices[i] is price of rod of length i+1
    dp = [0] * (n + 1)
    for i in range(1, n + 1):
        for j in range(i):
            dp[i] = max(dp[i], prices[j] + dp[i-j-1])
    return dp[n]

```

## 5. Coin Change II (Count Combinations)

**Problem:** Number of ways to make up an amount using given coins (unlimited supply).

### Optimal Python Solution

```python
def change(amount: int, coins: list[int]) -> int:
    # State: dp[i] = ways to make amount i
    # Key: Iterate through COINS first to ensure combinations (1+2 is same as 2+1)
    dp = [0] * (amount + 1)
    dp[0] = 1

    for coin in coins:
        for i in range(coin, amount + 1):
            dp[i] += dp[i - coin]
    return dp[amount]
```

### Explanation

1.  **Combination Logic**: By placing the coin loop on the outside, we ensure that we finish all ways to use one coin before moving to the next. This prevents counting different orderings of the same coins.
2.  **Unbounded Property**: The inner loop moves forward (`range(coin, amount + 1)`), allowing us to use the same coin multiple times.

### Complexity Analysis

- **Time:** $O(\text{amount} \times \text{len(coins)})$
- **Space:** $O(\text{amount})$

### Complexity Analysis

- **Time:** $O(n^2)$
- **Space:** $O(n)$

## 4. Integer Break

**Problem:** Maximize product of integers that sum to $n$.

### Optimal Python Solution

```python
def integer_break(n: int) -> int:
    if n <= 3: return n - 1
    dp = [0] * (n + 1)
    for i in range(1, 4): dp[i] = i
    for i in range(4, n + 1):
        for j in range(1, i // 2 + 1):
            dp[i] = max(dp[i], dp[j] * dp[i-j])
    return dp[n]

```

## 5. Coin Change II (Count Combinations)

**Problem:** Number of ways to make up an amount using given coins (unlimited supply).

### Optimal Python Solution

```python
def change(amount: int, coins: list[int]) -> int:
    # State: dp[i] = ways to make amount i
    # Key: Iterate through COINS first to ensure combinations (1+2 is same as 2+1)
    dp = [0] * (amount + 1)
    dp[0] = 1

    for coin in coins:
        for i in range(coin, amount + 1):
            dp[i] += dp[i - coin]
    return dp[amount]
```

### Explanation

1.  **Combination Logic**: By placing the coin loop on the outside, we ensure that we finish all ways to use one coin before moving to the next. This prevents counting different orderings of the same coins.
2.  **Unbounded Property**: The inner loop moves forward (`range(coin, amount + 1)`), allowing us to use the same coin multiple times.

### Complexity Analysis

- **Time:** $O(\text{amount} \times \text{len(coins)})$
- **Space:** $O(\text{amount})$

### Complexity Analysis

- **Time:** $O(n^2)$
- **Space:** $O(n)$

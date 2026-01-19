# Buy and Sell Stock

> **Prerequisites:** [03-1d-dp-basics](./03-1d-dp-basics.md)

## Interview Context

Stock problems are popular because:

1. **State machine DP**: Clean model for complex constraints
2. **Multiple variants**: Each adds new constraint
3. **Progressively harder**: Good interview escalation
4. **Real-world relevance**: Trading algorithms

---

## Problem Family Overview

| Problem | Transactions | Cooldown | Fee |
|---------|--------------|----------|-----|
| I | 1 | No | No |
| II | Unlimited | No | No |
| III | 2 | No | No |
| IV | k | No | No |
| With Cooldown | Unlimited | Yes | No |
| With Fee | Unlimited | No | Yes |

---

## Best Time to Buy and Sell Stock I

One transaction only.

```python
def max_profit_1(prices: list[int]) -> int:
    """
    Maximum profit with at most ONE transaction.

    Track minimum price seen, update max profit.

    Time: O(n)
    Space: O(1)
    """
    min_price = float('inf')
    max_profit = 0

    for price in prices:
        min_price = min(min_price, price)
        max_profit = max(max_profit, price - min_price)

    return max_profit
```

---

## Best Time to Buy and Sell Stock II

Unlimited transactions.

```python
def max_profit_2(prices: list[int]) -> int:
    """
    Maximum profit with UNLIMITED transactions.

    Greedy: Take all upward movements.

    Time: O(n)
    Space: O(1)
    """
    profit = 0

    for i in range(1, len(prices)):
        if prices[i] > prices[i - 1]:
            profit += prices[i] - prices[i - 1]

    return profit
```

### State Machine Approach

```python
def max_profit_2_dp(prices: list[int]) -> int:
    """
    State machine DP version.

    States: hold (have stock), cash (no stock)
    """
    hold = float('-inf')  # Profit if holding stock
    cash = 0              # Profit if not holding

    for price in prices:
        hold = max(hold, cash - price)   # Buy
        cash = max(cash, hold + price)   # Sell

    return cash
```

---

## Best Time to Buy and Sell Stock III

At most 2 transactions.

```python
def max_profit_3(prices: list[int]) -> int:
    """
    Maximum profit with at most 2 transactions.

    Track profit after each buy/sell.

    Time: O(n)
    Space: O(1)
    """
    buy1 = buy2 = float('-inf')
    sell1 = sell2 = 0

    for price in prices:
        buy1 = max(buy1, -price)           # First buy
        sell1 = max(sell1, buy1 + price)   # First sell
        buy2 = max(buy2, sell1 - price)    # Second buy
        sell2 = max(sell2, buy2 + price)   # Second sell

    return sell2
```

---

## Best Time to Buy and Sell Stock IV

At most k transactions.

```python
def max_profit_4(k: int, prices: list[int]) -> int:
    """
    Maximum profit with at most k transactions.

    Time: O(n × k)
    Space: O(k)
    """
    n = len(prices)

    if not prices or k == 0:
        return 0

    # If k >= n/2, unlimited transactions
    if k >= n // 2:
        return sum(max(0, prices[i] - prices[i-1]) for i in range(1, n))

    # DP with k transactions
    buy = [float('-inf')] * (k + 1)
    sell = [0] * (k + 1)

    for price in prices:
        for j in range(1, k + 1):
            buy[j] = max(buy[j], sell[j - 1] - price)
            sell[j] = max(sell[j], buy[j] + price)

    return sell[k]
```

---

## With Cooldown

After selling, must wait one day before buying.

```python
def max_profit_cooldown(prices: list[int]) -> int:
    """
    Unlimited transactions with 1-day cooldown after selling.

    States:
        hold: have stock
        sold: just sold (cooldown next)
        rest: no stock, can buy

    Time: O(n)
    Space: O(1)
    """
    hold = float('-inf')
    sold = 0
    rest = 0

    for price in prices:
        prev_sold = sold

        sold = hold + price          # Sell today
        hold = max(hold, rest - price)  # Buy today (from rest)
        rest = max(rest, prev_sold)  # Do nothing (or came from sold)

    return max(sold, rest)
```

### State Machine Diagram

```
         buy
    ↗——————→
   rest        hold
    ↖——————←
         sell (→ cooldown)
              ↓
            sold
              ↓
            rest
```

---

## With Transaction Fee

Pay fee for each transaction.

```python
def max_profit_fee(prices: list[int], fee: int) -> int:
    """
    Unlimited transactions with transaction fee.

    Time: O(n)
    Space: O(1)
    """
    hold = float('-inf')
    cash = 0

    for price in prices:
        hold = max(hold, cash - price)
        cash = max(cash, hold + price - fee)

    return cash
```

---

## General Framework

All stock problems can be modeled with this state machine:

```python
def max_profit_general(prices: list[int], k: int,
                        cooldown: int = 0, fee: int = 0) -> int:
    """
    General solution for all variants.

    States: dp[day][transactions_used][holding]
    """
    n = len(prices)

    if not prices or k == 0:
        return 0

    # dp[j][0] = max profit with j transactions, not holding
    # dp[j][1] = max profit with j transactions, holding
    dp = [[0, float('-inf')] for _ in range(k + 1)]

    for i in range(n):
        for j in range(k, 0, -1):
            # Sell
            dp[j][0] = max(dp[j][0], dp[j][1] + prices[i] - fee)
            # Buy
            if i >= cooldown:
                dp[j][1] = max(dp[j][1], dp[j - 1][0] - prices[i])

    return dp[k][0]
```

---

## State Transitions Summary

```
For each day and transaction count:

Not Holding → Not Holding: rest (do nothing)
Not Holding → Holding:     buy (pay price)
Holding → Holding:         rest (do nothing)
Holding → Not Holding:     sell (gain price - fee)

With cooldown:
After sell, must go to "sold" state before "rest"
```

---

## Edge Cases

```python
# 1. Empty prices
prices = []
# Return 0

# 2. Single price
prices = [5]
# Return 0 (can't profit)

# 3. Decreasing prices
prices = [7, 6, 4, 3, 1]
# Return 0 (no profit possible)

# 4. k = 0 transactions
k = 0
# Return 0

# 5. Large k
k >= len(prices) // 2
# Same as unlimited transactions
```

---

## Common Mistakes

```python
# WRONG: Updating in wrong order
for price in prices:
    sell = max(sell, buy + price)
    buy = max(buy, -price)  # Uses updated sell!

# CORRECT: Use previous values
for price in prices:
    new_buy = max(buy, sell_prev - price)
    new_sell = max(sell, buy + price)
    buy, sell = new_buy, new_sell


# WRONG: Not handling k >= n/2
if k >= len(prices) // 2:
    # Treat as unlimited - optimization needed!


# WRONG: Cooldown state confusion
sold = hold + price
rest = max(rest, sold)  # Wrong! sold is current, need prev
```

---

## Complexity

| Problem | Time | Space |
|---------|------|-------|
| I (1 transaction) | O(n) | O(1) |
| II (unlimited) | O(n) | O(1) |
| III (2 transactions) | O(n) | O(1) |
| IV (k transactions) | O(nk) | O(k) |
| With Cooldown | O(n) | O(1) |
| With Fee | O(n) | O(1) |

---

## Interview Tips

1. **Know the progression**: I → II → III → IV
2. **Understand state machine**: Draw the states
3. **Handle k optimization**: Large k = unlimited
4. **Remember initialization**: buy = -inf, sell = 0
5. **Trace through example**: Verify transitions

---

## Practice Problems

| # | Problem | Difficulty | Constraint |
|---|---------|------------|------------|
| 1 | Best Time I | Easy | 1 transaction |
| 2 | Best Time II | Medium | Unlimited |
| 3 | Best Time III | Hard | 2 transactions |
| 4 | Best Time IV | Hard | k transactions |
| 5 | With Cooldown | Medium | 1-day wait |
| 6 | With Fee | Medium | Transaction fee |

---

## Key Takeaways

1. **State machine model**: hold/cash states
2. **Track profit at each state**: Not actual holdings
3. **Order matters**: Update correctly to use previous values
4. **K optimization**: k ≥ n/2 → unlimited
5. **Cooldown adds state**: sold → rest transition

---

## Next: [16-matrix-chain.md](./16-matrix-chain.md)

Learn interval DP with matrix chain multiplication.

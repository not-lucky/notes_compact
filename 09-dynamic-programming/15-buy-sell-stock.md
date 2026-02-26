# Buy and Sell Stock

> **Prerequisites:** [03-1d-dp-basics](./03-1d-dp-basics.md)

## Overview

Stock problems use state machine DP to model trading constraints like transaction limits, cooldowns, and fees.

## Building Intuition

**Why does state machine DP work for stock problems?**

1. **Two States, Clear Transitions**: At any time, you either HOLD a stock or have CASH. Every day, you transition:
   - Hold → Hold (rest) or Hold → Cash (sell)
   - Cash → Cash (rest) or Cash → Hold (buy)

2. **State Encapsulates History**: The key insight is that "how I got here" doesn't matter—only "what state am I in now?" Whether I bought yesterday or last week, my current profit depends only on today's price and my current state.

3. **Constraints Add Dimensions**:
   - k transactions → add "transactions used" dimension
   - Cooldown → add "just sold" state (can't buy immediately)
   - Fee → subtract fee when selling

4. **Why Stock I Is Simple**: With one transaction, you just track min price seen and max profit possible. No need for full DP.

5. **Why Stock II Is Greedy**: With unlimited transactions, take every upward price movement. If price goes up, you would have profited by buying yesterday and selling today.

6. **Mental Model**: Imagine two parallel universes at each time step—one where you hold stock, one where you have cash. Each day, compute the best profit in each universe, considering what you could have done yesterday.

7. **The Recurrence Pattern**:
   - hold[i] = max(hold[i-1], cash[i-1] - price[i])
   - cash[i] = max(cash[i-1], hold[i-1] + price[i])

## Interview Context

Stock problems are popular because:

1. **State machine DP**: Clean model for complex constraints
2. **Multiple variants**: Each adds new constraint
3. **Progressively harder**: Good interview escalation
4. **Real-world relevance**: Trading algorithms

---

## When NOT to Use State Machine DP

1. **Stock I (One Transaction)**: Simple min-tracking suffices. DP is overkill.
   - *Counter-example*: Using a 2D array `dp[n][2]` when you only need to track the lowest price seen so far and the max difference.

2. **Stock II (Unlimited, No Cooldown/Fee)**: Greedy (sum all positive differences) is O(n) and simpler.
   - *Counter-example*: Setting up a state machine for `[1, 5, 3, 6]` when you can just add `(5-1) + (6-3) = 7`.

3. **Prices Unknown in Advance**: DP assumes full price history. For online/streaming decisions, use different algorithms (like moving averages or ML models).

4. **Short Selling**: Standard stock DP assumes buy-before-sell. Short selling (sell-before-buy) needs modified states.

5. **Complex Fee Structures**: If fees depend on transaction size (e.g., a percentage of the trade value) or are non-linear, the standard recurrence doesn't apply because the state no longer captures all necessary information (you'd need to know the exact buy price to calculate the fee).

**Choose the Right Approach:**

- 1 transaction → min tracking
- Unlimited, no constraints → greedy
- Limited transactions (k) → state machine DP
- Cooldown or fees → add states to DP

---

## Problem Family Overview

| Problem       | Transactions | Cooldown | Fee |
| ------------- | ------------ | -------- | --- |
| I             | 1            | No       | No  |
| II            | Unlimited    | No       | No  |
| III           | 2            | No       | No  |
| IV            | k            | No       | No  |
| With Cooldown | Unlimited    | Yes      | No  |
| With Fee      | Unlimited    | No       | Yes |

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

#### Recurrence Relation

Let $hold[i]$ be max profit on day $i$ while holding a stock.
Let $cash[i]$ be max profit on day $i$ while holding no stock.

$$
hold[i] = \max(hold[i-1], cash[i-1] - price[i])
$$
$$
cash[i] = \max(cash[i-1], hold[i-1] + price[i])
$$

#### Tabulation (Space-Optimized)

```python
def max_profit_2_dp(prices: list[int]) -> int:
    """
    State machine DP version.
    """
    hold = float('-inf')  # Profit if holding stock
    cash = 0              # Profit if not holding

    for price in prices:
        # Buy stock: decrease cash by price
        # Keep stock: profit doesn't change
        new_hold = max(hold, cash - price)

        # Sell stock: increase cash by price
        # Keep empty hands: profit doesn't change
        new_cash = max(cash, hold + price)

        hold, cash = new_hold, new_cash

    return cash
```

#### Top-Down (Memoization)

```python
def max_profit_2_memo(prices: list[int]) -> int:
    """
    Memoization version of State machine DP.
    """
    memo = {}

    def dfs(i: int, holding: bool) -> int:
        if i == len(prices):
            return 0  # End of days, no more profit

        if (i, holding) in memo:
            return memo[(i, holding)]

        if holding:
            # Sell today or do nothing
            res = max(dfs(i + 1, False) + prices[i], dfs(i + 1, True))
        else:
            # Buy today or do nothing
            res = max(dfs(i + 1, True) - prices[i], dfs(i + 1, False))

        memo[(i, holding)] = res
        return res

    return dfs(0, False)
```

---

## Best Time to Buy and Sell Stock III

At most 2 transactions.

### Recurrence Relation

Let $buy1$ be max profit after 1st buy. Let $sell1$ be max profit after 1st sell.
Let $buy2$ be max profit after 2nd buy. Let $sell2$ be max profit after 2nd sell.

$$
buy1_i = \max(buy1_{i-1}, -price_i)
$$
$$
sell1_i = \max(sell1_{i-1}, buy1_{i-1} + price_i)
$$
$$
buy2_i = \max(buy2_{i-1}, sell1_{i-1} - price_i)
$$
$$
sell2_i = \max(sell2_{i-1}, buy2_{i-1} + price_i)
$$

### Space-Optimized Tabulation

```python
def max_profit_3(prices: list[int]) -> int:
    """
    Maximum profit with at most 2 transactions.

    Track profit after each buy/sell.

    Time: O(n)
    Space: O(1)
    """
    buy1 = float('-inf')
    sell1 = 0
    buy2 = float('-inf')
    sell2 = 0

    for price in prices:
        # Think backwards:
        sell2 = max(sell2, buy2 + price)
        buy2 = max(buy2, sell1 - price)
        sell1 = max(sell1, buy1 + price)
        buy1 = max(buy1, -price)

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

### Recurrence Relation

Let $hold[i]$ be max profit on day $i$ while holding a stock.
Let $sold[i]$ be max profit on day $i$ right after selling a stock.
Let $rest[i]$ be max profit on day $i$ after resting (either came from $sold[i-1]$ or $rest[i-1]$).

$$
hold[i] = \max(hold[i-1], rest[i-1] - price[i])
$$
$$
sold[i] = hold[i-1] + price[i]
$$
$$
rest[i] = \max(rest[i-1], sold[i-1])
$$

### Space-Optimized Tabulation

```python
def max_profit_cooldown(prices: list[int]) -> int:
    """
    Unlimited transactions with 1-day cooldown after selling.
    """
    hold = float('-inf')
    sold = 0
    rest = 0

    for price in prices:
        # Cache previous day's sold state
        prev_sold = sold

        # 1. Sell stock today
        sold = hold + price

        # 2. Buy today (must come from resting, can't buy right after sell)
        # OR Hold from yesterday
        hold = max(hold, rest - price)

        # 3. Rest today (came from sold yesterday, or rested yesterday)
        rest = max(rest, prev_sold)

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
    cash = max(cash, hold + price)
    hold = max(hold, -price)  # Uses updated sell!

# CORRECT: Use previous values
for price in prices:
    new_hold = max(hold, cash_prev - price)
    new_cash = max(cash, hold + price)
    hold, cash = new_hold, new_cash


# WRONG: Not handling k >= n/2
if k >= len(prices) // 2:
    # Treat as unlimited - optimization needed!


# WRONG: Cooldown state confusion
sold = hold + price
rest = max(rest, sold)  # Wrong! sold is current, need prev
```

---

## Complexity

| Problem              | Time  | Space |
| -------------------- | ----- | ----- |
| I (1 transaction)    | O(n)  | O(1)  |
| II (unlimited)       | O(n)  | O(1)  |
| III (2 transactions) | O(n)  | O(1)  |
| IV (k transactions)  | O(nk) | O(k)  |
| With Cooldown        | O(n)  | O(1)  |
| With Fee             | O(n)  | O(1)  |

---

## Interview Tips

1. **Know the progression**: I → II → III → IV
2. **Understand state machine**: Draw the states
3. **Handle k optimization**: Large k = unlimited
4. **Remember initialization**: buy = -inf, sell = 0
5. **Trace through example**: Verify transitions

---

## Practice Problems

| #   | Problem       | Difficulty | Constraint      |
| --- | ------------- | ---------- | --------------- |
| 1   | Best Time I   | Easy       | 1 transaction   |
| 2   | Best Time II  | Medium     | Unlimited       |
| 3   | Best Time III | Hard       | 2 transactions  |
| 4   | Best Time IV  | Hard       | k transactions  |
| 5   | With Cooldown | Medium     | 1-day wait      |
| 6   | With Fee      | Medium     | Transaction fee |

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

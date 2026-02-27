# Buy and Sell Stock

> **Prerequisites:** [03-1d-dp-basics](./03-1d-dp-basics.md)

## Overview

Stock problems are a classic family of interview questions that perfectly illustrate **State Machine Dynamic Programming**. By defining clear states (e.g., holding stock, having cash, being on cooldown) and mapping out the transitions between them, we can gracefully handle complex trading constraints.

## Building Intuition

**Why does state machine DP work so well here?**

1. **Finite States**: On any given day, you are in a specific state. For basic problems, it's binary: you either `HOLD` a stock, or you have `CASH` (no stock).
2. **State Encapsulates History**: The core DP insight is that "how I got here" doesn't matter. Whether you bought yesterday or last year, your maximum future profit depends *only* on your current state and today's price.
3. **Daily Transitions**: Each day, you make a choice:
   - If in `HOLD`: Do nothing (stay in `HOLD`), or Sell (transition to `CASH`).
   - If in `CASH`: Do nothing (stay in `CASH`), or Buy (transition to `HOLD`).
4. **Constraints Add Dimensions**:
   - *k transactions* → add a "transactions used" dimension.
   - *Cooldown* → add a "just sold" state to delay buying.
   - *Fee* → subtract a fee during the sell transition.

### When NOT to Use State Machine DP

While powerful, full state machine DP is overkill for the simplest variants:
1. **Stock I (One Transaction)**: Simple min-tracking suffices.
2. **Stock II (Unlimited, No Restrictions)**: A greedy approach (summing all positive daily price differences) is $O(n)$ and simpler.

**The Golden Rule:**
- 1 transaction → Min tracking
- Unlimited, no constraints → Greedy
- Limited transactions ($k$) → State Machine DP
- Cooldown or fees → State Machine DP

---

## Problem Family Overview

| Problem | Transactions | Cooldown | Fee | Optimal Approach |
| :--- | :--- | :--- | :--- | :--- |
| **I** | 1 | No | No | Min-tracking ($O(n)$) |
| **II** | Unlimited | No | No | Greedy ($O(n)$) |
| **III** | 2 | No | No | State Machine ($O(n)$) |
| **IV** | $k$ | No | No | State Machine ($O(nk)$) |
| **Cooldown** | Unlimited | Yes | No | State Machine ($O(n)$) |
| **Fee** | Unlimited | No | Yes | State Machine ($O(n)$) |

---

## Best Time to Buy and Sell Stock I

**Constraint:** At most ONE transaction.

We don't need DP here. Just track the lowest price seen so far and the maximum profit we could get if we sold today.

```python
def max_profit_1(prices: list[int]) -> int:
    """
    Time: O(n) | Space: O(1)
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

**Constraint:** Unlimited transactions.

### 1. Greedy Approach (Optimal)
Since we can trade as much as we want, we should simply capture every single upward price movement.

```python
def max_profit_2_greedy(prices: list[int]) -> int:
    """
    Time: O(n) | Space: O(1)
    """
    profit = 0
    for i in range(1, len(prices)):
        if prices[i] > prices[i - 1]:
            profit += prices[i] - prices[i - 1]
    return profit
```

### 2. State Machine Approach
We introduce the DP approach here as it serves as the foundation for the harder variants.

Let $hold[i]$ be the max profit on day $i$ if we end the day **holding** a stock.
Let $cash[i]$ be the max profit on day $i$ if we end the day **without** a stock.

Transitions:
- $hold[i] = \max(hold[i-1], cash[i-1] - price[i])$  *(Keep holding OR Buy today)*
- $cash[i] = \max(cash[i-1], hold[i-1] + price[i])$  *(Keep cash OR Sell today)*

```python
def max_profit_2_dp(prices: list[int]) -> int:
    """
    Time: O(n) | Space: O(1)
    """
    hold = float('-inf')
    cash = 0

    for price in prices:
        # Simultaneous assignment ensures we use strictly yesterday's states!
        hold, cash = max(hold, cash - price), max(cash, hold + price)

    return cash
```
*(Note the elegant use of Python's simultaneous assignment to prevent "state pollution" where we accidentally use today's updated `hold` to compute today's `cash`.)*

---

## Best Time to Buy and Sell Stock III

**Constraint:** At most TWO transactions.

We expand our states to track the exact transaction we are on: `buy1`, `sell1`, `buy2`, `sell2`.

To avoid state pollution (using a value updated in the same day), we evaluate the transitions in **reverse order**.

```python
def max_profit_3(prices: list[int]) -> int:
    """
    Time: O(n) | Space: O(1)
    """
    buy1 = float('-inf')
    sell1 = 0
    buy2 = float('-inf')
    sell2 = 0

    for price in prices:
        # Think backwards: update the latest states first
        # This guarantees we only use states from the previous day
        sell2 = max(sell2, buy2 + price)
        buy2 = max(buy2, sell1 - price)
        sell1 = max(sell1, buy1 + price)
        buy1 = max(buy1, -price)

    return sell2
```

---

## Best Time to Buy and Sell Stock IV

**Constraint:** At most $k$ transactions.

This is a generalized version of Stock III. We use arrays of size $k+1$ to track the `buy` and `sell` states for each transaction limit.

**Crucial Optimization:** If $k \ge n/2$, we effectively have unlimited transactions because we can at most buy and sell on alternating days. We must fall back to the $O(n)$ greedy approach to avoid Time Limit Exceeded (TLE) errors.

```python
def max_profit_4(k: int, prices: list[int]) -> int:
    """
    Time: O(nk) | Space: O(k)
    """
    n = len(prices)
    if not prices or k == 0:
        return 0

    # Optimization: If k >= n/2, it's equivalent to unlimited transactions
    if k >= n // 2:
        return sum(max(0, prices[i] - prices[i-1]) for i in range(1, n))

    buy = [float('-inf')] * (k + 1)
    sell = [0] * (k + 1)

    for price in prices:
        # Iterate backwards to safely use previous day's states (just like Stock III)
        for j in range(k, 0, -1):
            sell[j] = max(sell[j], buy[j] + price)
            buy[j] = max(buy[j], sell[j - 1] - price)

    return sell[k]
```

---

## With Cooldown

**Constraint:** Unlimited transactions, but after selling, you must wait 1 day before buying again.

We introduce a 3rd state to our basic DP machine to enforce the cooldown.
- `hold`: Holding a stock.
- `sold`: Just sold the stock today (triggers cooldown tomorrow).
- `rest`: Not holding a stock, and didn't sell today (free to buy).

**State Diagram:**
```text
          buy
  rest ————————→ hold
   ↑ ↖            |
   |  rest        | sell
   |              ↓
   └←—————————— sold
    (forced wait)
```

```python
def max_profit_cooldown(prices: list[int]) -> int:
    """
    Time: O(n) | Space: O(1)
    """
    hold = float('-inf')
    sold = 0
    rest = 0

    for price in prices:
        # Simultaneous assignment elegantly handles state transitions
        # without needing temporary variables like 'prev_sold'
        hold, sold, rest = (
            max(hold, rest - price), # Keep holding OR buy today (must come from rest)
            hold + price,            # Sell today
            max(rest, sold)          # Keep resting OR just finished cooldown
        )

    return max(sold, rest)
```

---

## With Transaction Fee

**Constraint:** Unlimited transactions, but you pay a fixed fee for every completed trade (buy + sell).

We simply subtract the fee during the sell transition.

```python
def max_profit_fee(prices: list[int], fee: int) -> int:
    """
    Time: O(n) | Space: O(1)
    """
    hold = float('-inf')
    cash = 0

    for price in prices:
        # Note: We subtract the fee when transitioning from hold to cash (selling)
        hold, cash = max(hold, cash - price), max(cash, hold + price - fee)

    return cash
```

---

## Common Mistakes

1. **State Pollution (Updating in the Wrong Order):**
   If you update `cash` and then immediately use the new `cash` to update `hold`, you are effectively allowing a "buy and sell on the same day" logic which breaks strict day-by-day transitions. **Fix:** Use simultaneous assignment in Python (`a, b = new_a, new_b`) or iterate backwards for array states.
2. **Forgetting to Initialize `hold` to `-inf`:**
   Profit can be negative while holding a stock. Initializing `hold = 0` will cause the DP to incorrectly prefer `0` over a legitimate state where you are down money after buying.
3. **Missing the $k \ge n/2$ Optimization in Stock IV:**
   A large $k$ will cause the $O(nk)$ algorithm to hit a Time Limit Exceeded (TLE) on platforms like LeetCode. Always fall back to the $O(n)$ greedy approach when $k$ is large enough to be unbounded.

---

## Interview Tips

1. **Master the Progression**: Interviewers often start with Stock I or II and ask you to modify your code for Cooldown or a Fee.
2. **Draw the State Machine**: If you get a novel constraint (e.g., "you can hold at most 2 shares at once"), don't panic. Draw the states (0 shares, 1 share, 2 shares) and draw the arrows (buy, sell, rest). The code is just a literal translation of those arrows.
3. **Define Your States Clearly**: Say out loud: *"Let `hold` be the maximum profit I can have on day `i` if I go to sleep holding a stock."* This prevents off-by-one errors in your logic.

---

## Practice Problems

| # | Problem | Difficulty | Constraint |
| --- | --- | --- | --- |
| 1 | Best Time I | Easy | 1 transaction |
| 2 | Best Time II | Medium | Unlimited |
| 3 | Best Time III | Hard | 2 transactions |
| 4 | Best Time IV | Hard | $k$ transactions |
| 5 | With Cooldown | Medium | 1-day wait |
| 6 | With Fee | Medium | Transaction fee |

---

## Next: [16-matrix-chain.md](./16-matrix-chain.md)

Learn interval DP with matrix chain multiplication.
# Buy and Sell Stock

> **Prerequisites:** [03-1d-dp-basics](./03-1d-dp-basics.md)

## Overview

Stock problems are a classic family of interview questions that perfectly illustrate **State Machine Dynamic Programming**. In standard DP, the "state" is usually just an index (e.g., $i$ for the $i$-th element). In **State Machine DP**, the state has an *additional* dimension representing the categorical "status" or "condition" we are in at that index (e.g., "holding stock", "having cash", "on cooldown").

By defining these clear states and mapping out the transitions between them, we can gracefully handle complex trading constraints.

## Building Intuition

**Why does State Machine DP work so well here?**

1. **Finite States**: On any given day, you are in a specific state. For basic problems, it's binary: you either `HOLD` a stock, or you have `CASH` (no stock).
2. **State Encapsulates History**: The core DP insight is that "how I got here" doesn't matter. Whether you bought yesterday or last year, your maximum profit achieved so far depends *only* on your current state and today's price.
3. **Daily Transitions**: Each day, you make a choice that determines your state for the next day.
   - If in `HOLD`: Do nothing (stay in `HOLD`), or Sell (transition to `CASH`).
   - If in `CASH`: Do nothing (stay in `CASH`), or Buy (transition to `HOLD`).
4. **Constraints Add Dimensions**:
   - *k transactions* → add a "transactions used" dimension.
   - *Cooldown* → add a "just sold" state to delay buying.
   - *Fee* → subtract a fee during the sell transition.

### The Standard State Machine

The foundation of almost all stock problems is this two-state machine:

```text
        buy (-price)
 CASH ───────────────> HOLD
  ↑ ↖                  |
  |  CASH              | sell (+price)
  |                    ↓
  └<───────────────────┘
```

### Top-Down vs Bottom-Up

For stock problems, it's highly recommended to understand the **top-down memoized DFS** approach first. It maps perfectly to the decisions you make on each day:
1. What day is it? (`index`)
2. Am I holding a stock? (`holding`)
3. How many transactions do I have left? (`k`)

From there, transitioning to the $O(1)$ space bottom-up State Machine DP becomes a mechanical translation.

---

## Problem Family Overview

| Problem | Transactions | Cooldown | Fee | Optimal Approach | Time Complexity | Space Complexity |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **I** | 1 | No | No | Min-tracking | $O(n)$ | $O(1)$ |
| **II** | Unlimited | No | No | State Machine / Greedy | $O(n)$ | $O(1)$ |
| **III** | 2 | No | No | State Machine | $O(n)$ | $O(1)$ |
| **IV** | $k$ | No | No | State Machine | $O(nk)$ | $O(k)$ |
| **Cooldown**| Unlimited | Yes | No | State Machine | $O(n)$ | $O(1)$ |
| **Fee** | Unlimited | No | Yes | State Machine | $O(n)$ | $O(1)$ |

---

## Best Time to Buy and Sell Stock I

**Constraint:** At most ONE transaction.

We don't need DP here. Just track the lowest price seen so far, and the maximum profit we could get if we sold today.

```python
def maxProfit_1(prices: list[int]) -> int:
    """
    Time: O(n) | Space: O(1)
    """
    min_price = float('inf')
    max_profit = 0

    for price in prices:
        # What is the lowest price we could have bought at?
        min_price = min(min_price, price)
        # What is the max profit if we sell today?
        max_profit = max(max_profit, price - min_price)

    return max_profit
```

---

## Best Time to Buy and Sell Stock II

**Constraint:** Unlimited transactions.

### 1. Top-Down Memoization
Let's build the intuition using DP. At any day `i`, we are either holding a stock or not.
If we hold a stock, we can sell it or do nothing.
If we don't hold a stock, we can buy it or do nothing.

```python
def maxProfit_2_top_down(prices: list[int]) -> int:
    """
    Time: O(n) | Space: O(n) for memoization stack
    """
    memo = {}
    
    def dfs(i: int, holding: bool) -> int:
        # Base case: we've reached the end of the days
        if i == len(prices):
            return 0
            
        if (i, holding) in memo:
            return memo[(i, holding)]
            
        # Do nothing (skip to next day)
        do_nothing = dfs(i + 1, holding)
        
        if holding:
            # Sell the stock
            do_something = prices[i] + dfs(i + 1, False)
        else:
            # Buy the stock
            do_something = -prices[i] + dfs(i + 1, True)
            
        memo[(i, holding)] = max(do_nothing, do_something)
        return memo[(i, holding)]
        
    return dfs(0, False)
```

### 2. Bottom-Up State Machine DP
Translating the above into $O(1)$ space iterative DP. Let `hold` be the max profit ending today holding a stock, and `cash` be the max profit ending today without a stock.

```python
def maxProfit_2_dp(prices: list[int]) -> int:
    """
    Time: O(n) | Space: O(1)
    """
    hold = float('-inf') 
    cash = 0             

    for price in prices:
        # hold: max(keep holding, buy today)
        # cash: max(keep cash, sell today)
        hold, cash = max(hold, cash - price), max(cash, hold + price)

    return cash
```

### 3. Greedy Approach (Optimal)
Since we can trade as much as we want, we should simply capture every single upward price movement.

```python
def maxProfit_2_greedy(prices: list[int]) -> int:
    """
    Time: O(n) | Space: O(1)
    """
    profit = 0
    for i in range(1, len(prices)):
        if prices[i] > prices[i - 1]:
            profit += prices[i] - prices[i - 1]
    return profit
```

---

## Best Time to Buy and Sell Stock III

**Constraint:** At most TWO transactions.

### 1. Top-Down Memoization
Now we add a third parameter to our state: `transactions_left`. A transaction is considered complete when we *sell*.

```python
def maxProfit_3_top_down(prices: list[int]) -> int:
    """
    Time: O(n) | Space: O(n)
    """
    memo = {}
    
    def dfs(i: int, holding: bool, transactions_left: int) -> int:
        # Base case
        if i == len(prices) or transactions_left == 0:
            return 0
            
        if (i, holding, transactions_left) in memo:
            return memo[(i, holding, transactions_left)]
            
        do_nothing = dfs(i + 1, holding, transactions_left)
        
        if holding:
            # Sell stock -> transaction complete, decrement transactions_left
            do_something = prices[i] + dfs(i + 1, False, transactions_left - 1)
        else:
            # Buy stock
            do_something = -prices[i] + dfs(i + 1, True, transactions_left)
            
        memo[(i, holding, transactions_left)] = max(do_nothing, do_something)
        return memo[(i, holding, transactions_left)]
        
    return dfs(0, False, 2)
```

### 2. Bottom-Up State Machine DP
The states are: `buy1`, `sell1`, `buy2`, `sell2`.

```python
def maxProfit_3_dp(prices: list[int]) -> int:
    """
    Time: O(n) | Space: O(1)
    """
    buy1 = float('-inf')
    sell1 = 0
    buy2 = float('-inf')
    sell2 = 0

    for price in prices:
        # Note: In Python, simultaneous assignment or order matters.
        # Think backwards to use the state from the *previous* day.
        sell2 = max(sell2, buy2 + price)
        buy2 = max(buy2, sell1 - price)
        sell1 = max(sell1, buy1 + price)
        buy1 = max(buy1, -price) 

    return sell2
```

---

## Best Time to Buy and Sell Stock IV

**Constraint:** At most $k$ transactions.

### 1. Top-Down Memoization
Exactly the same as Stock III, but we pass `k` instead of `2` as the initial `transactions_left`.

```python
def maxProfit_4_top_down(k: int, prices: list[int]) -> int:
    """
    Time: O(n*k) | Space: O(n*k)
    """
    if not prices or k == 0:
        return 0
        
    # Optimization: If k >= n/2, it's equivalent to unlimited transactions
    if k >= len(prices) // 2:
        return sum(max(0, prices[i] - prices[i-1]) for i in range(1, len(prices)) if prices[i] > prices[i-1])

    memo = {}
    
    def dfs(i: int, holding: bool, transactions_left: int) -> int:
        if i == len(prices) or transactions_left == 0:
            return 0
            
        if (i, holding, transactions_left) in memo:
            return memo[(i, holding, transactions_left)]
            
        do_nothing = dfs(i + 1, holding, transactions_left)
        
        if holding:
            do_something = prices[i] + dfs(i + 1, False, transactions_left - 1)
        else:
            do_something = -prices[i] + dfs(i + 1, True, transactions_left)
            
        memo[(i, holding, transactions_left)] = max(do_nothing, do_something)
        return memo[(i, holding, transactions_left)]
        
    return dfs(0, False, k)
```

### 2. Bottom-Up State Machine DP
We use arrays to track $k$ transactions.

```python
def maxProfit_4_dp(k: int, prices: list[int]) -> int:
    """
    Time: O(n*k) | Space: O(k)
    """
    n = len(prices)
    if not prices or k == 0:
        return 0

    if k >= n // 2:
        return sum(max(0, prices[i] - prices[i-1]) for i in range(1, n) if prices[i] > prices[i-1])

    buy = [float('-inf')] * (k + 1)
    sell = [0] * (k + 1)

    for price in prices:
        # Iterate backwards to safely use previous day's states
        for j in range(k, 0, -1):
            sell[j] = max(sell[j], buy[j] + price)
            buy[j] = max(buy[j], sell[j - 1] - price)

    return sell[k]
```

---

## With Cooldown

**Constraint:** Unlimited transactions, 1 day cooldown after selling.

### 1. Top-Down Memoization
The easiest way to implement cooldown in Top-Down DP is just to skip an extra day when you sell: `dfs(i + 2, False)`.

```python
def maxProfit_cooldown_top_down(prices: list[int]) -> int:
    """
    Time: O(n) | Space: O(n)
    """
    memo = {}
    
    def dfs(i: int, holding: bool) -> int:
        if i >= len(prices):
            return 0
            
        if (i, holding) in memo:
            return memo[(i, holding)]
            
        do_nothing = dfs(i + 1, holding)
        
        if holding:
            # Sell stock -> skip a day for cooldown (i + 2)
            do_something = prices[i] + dfs(i + 2, False)
        else:
            # Buy stock
            do_something = -prices[i] + dfs(i + 1, True)
            
        memo[(i, holding)] = max(do_nothing, do_something)
        return memo[(i, holding)]
        
    return dfs(0, False)
```

### 2. Bottom-Up State Machine DP
Here we explicitly model the 3 states: `hold`, `sold` (just sold, now on cooldown), and `rest` (can buy).

```python
def maxProfit_cooldown_dp(prices: list[int]) -> int:
    """
    Time: O(n) | Space: O(1)
    """
    hold = float('-inf')
    sold = 0
    rest = 0

    for price in prices:
        # Simultaneous assignment handles transitions cleanly
        hold, sold, rest = (
            max(hold, rest - price), # Keep holding OR buy today (must come from rest!)
            hold + price,            # Sell today (moves to sold state)
            max(rest, sold)          # Keep resting OR just finished cooldown
        )

    return max(sold, rest)
```

---

## With Transaction Fee

**Constraint:** Unlimited transactions, pay a fee for every trade.

### 1. Top-Down Memoization

```python
def maxProfit_fee_top_down(prices: list[int], fee: int) -> int:
    """
    Time: O(n) | Space: O(n)
    """
    memo = {}
    
    def dfs(i: int, holding: bool) -> int:
        if i == len(prices):
            return 0
            
        if (i, holding) in memo:
            return memo[(i, holding)]
            
        do_nothing = dfs(i + 1, holding)
        
        if holding:
            # Sell stock, pay the fee
            do_something = prices[i] - fee + dfs(i + 1, False)
        else:
            # Buy stock
            do_something = -prices[i] + dfs(i + 1, True)
            
        memo[(i, holding)] = max(do_nothing, do_something)
        return memo[(i, holding)]
        
    return dfs(0, False)
```

### 2. Bottom-Up State Machine DP

```python
def maxProfit_fee_dp(prices: list[int], fee: int) -> int:
    """
    Time: O(n) | Space: O(1)
    """
    hold = float('-inf')
    cash = 0

    for price in prices:
        # Subtract fee when selling
        hold, cash = max(hold, cash - price), max(cash, hold + price - fee)

    return cash
```

---

## Common Mistakes

1. **State Pollution (Updating in the Wrong Order):**
   If you update `cash` and then immediately use the new `cash` to update `hold`, you are effectively allowing a "buy and sell on the same day" logic which breaks strict day-by-day transitions.
   **Fix:** Use simultaneous assignment in Python (`a, b = new_a, new_b`), or iterate backwards for array states (like in Stock III and IV), or use temporary `prev` variables.
2. **Forgetting to Initialize `hold` to `-inf`:**
   Profit can be negative while holding a stock. Initializing `hold = 0` will cause the DP to incorrectly prefer `0` over a legitimate state where you are down money after buying (e.g., you bought at $\$10$, profit is $-10$, which is less than $0$).
3. **Missing the $k \ge n/2$ Optimization in Stock IV:**
   A large $k$ will cause the $O(nk)$ algorithm to hit a Time Limit Exceeded (TLE) on platforms like LeetCode. Always fall back to the $O(n)$ greedy approach when $k$ is large enough to be unbounded.

---

## Interview Tips

1. **Top-Down First**: Always derive the transitions using Top-Down DFS with Memoization. It's much easier to explain to an interviewer: "At day $i$, I can either hold, buy, or sell. Let's explore all branches and cache the results."
2. **Draw the State Machine**: If you are asked to optimize space to $O(1)$, draw the states (e.g. `rest`, `hold`, `sold`) and draw the arrows (buy, sell, rest). The bottom-up $O(1)$ code is just a literal translation of those arrows using simultaneous assignment.
3. **Define Your States Clearly**: Say out loud: *"Let `hold` be the maximum profit I can have on day `i` if I go to sleep holding a stock."* This prevents off-by-one errors in your logic.

---

## Practice Problems

| # | Problem | Difficulty | Constraint | Description |
| --- | --- | --- | --- | --- |
| 1 | [Best Time to Buy and Sell Stock](https://leetcode.com/problems/best-time-to-buy-and-sell-stock/) | Easy | 1 transaction | Simple min-tracking. Good for understanding the core problem. |
| 2 | [Best Time to Buy and Sell Stock II](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-ii/) | Medium | Unlimited | Introduces greedy approach and foundational DP. |
| 3 | [Best Time to Buy and Sell Stock with Cooldown](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-with-cooldown/) | Medium | 1-day wait | Adds a cooldown state. The `dfs(i + 2)` logic shines here. |
| 4 | [Best Time to Buy and Sell Stock with Transaction Fee](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-with-transaction-fee/) | Medium | Transaction fee | Simple modification to the standard machine. |
| 5 | [Best Time to Buy and Sell Stock III](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-iii/) | Hard | 2 transactions | Introduces multi-transaction tracking. |
| 6 | [Best Time to Buy and Sell Stock IV](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-iv/) | Hard | $k$ transactions | Generalizes III to $k$ transactions. Teaches TLE avoidance. |

---

## Next: [16-matrix-chain.md](./16-matrix-chain.md)

Learn interval DP with matrix chain multiplication.

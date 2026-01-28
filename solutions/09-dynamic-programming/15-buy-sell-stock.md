# Solutions: Buy and Sell Stock (State Machine DP)

## 1. Stock I (1 Transaction)

**Problem:** Max profit with at most one transaction.

### Optimal Python Solution

```python
def max_profit_1(prices: list[int]) -> int:
    min_price = float('inf')
    max_profit = 0
    for p in prices:
        min_price = min(min_price, p)
        max_profit = max(max_profit, p - min_price)
    return max_profit
```

### Complexity Analysis

- **Time:** $O(n)$
- **Space:** $O(1)$

---

## 2. Stock II (Unlimited Transactions)

**Problem:** Max profit with unlimited transactions.

### Optimal Python Solution

```python
def max_profit_2(prices: list[int]) -> int:
    # Greedy: Sum all positive daily differences
    profit = 0
    for i in range(1, len(prices)):
        if prices[i] > prices[i-1]:
            profit += prices[i] - prices[i-1]
    return profit
```

### Complexity Analysis

- **Time:** $O(n)$
- **Space:** $O(1)$

---

## 3. Stock III (2 Transactions)

**Problem:** Max profit with at most two transactions.

### Optimal Python Solution

```python
def max_profit_3(prices: list[int]) -> int:
    buy1 = buy2 = float('-inf')
    sell1 = sell2 = 0
    for p in prices:
        buy1 = max(buy1, -p)
        sell1 = max(sell1, buy1 + p)
        buy2 = max(buy2, sell1 - p)
        sell2 = max(sell2, buy2 + p)
    return sell2
```

### Complexity Analysis

- **Time:** $O(n)$
- **Space:** $O(1)$

---

## 4. Stock IV (k Transactions)

**Problem:** Max profit with at most $k$ transactions.

### Optimal Python Solution

```python
def max_profit_4(k: int, prices: list[int]) -> int:
    if not prices or k == 0: return 0
    n = len(prices)
    if k >= n // 2: # Treat as unlimited
        return sum(max(0, prices[i] - prices[i-1]) for i in range(1, n))

    buy = [float('-inf')] * (k + 1)
    sell = [0] * (k + 1)
    for p in prices:
        for j in range(1, k + 1):
            buy[j] = max(buy[j], sell[j-1] - p)
            sell[j] = max(sell[j], buy[j] + p)
    return sell[k]
```

### Complexity Analysis

- **Time:** $O(nk)$
- **Space:** $O(k)$

---

## 5. Stock with Cooldown

**Problem:** Unlimited transactions, 1-day cooldown after selling.

### Optimal Python Solution

```python
def max_profit_cooldown(prices: list[int]) -> int:
    # States: hold, sold (just sold, must cool), rest (can buy)
    hold = float('-inf')
    sold = rest = 0
    for p in prices:
        prev_sold = sold
        sold = hold + p
        hold = max(hold, rest - p)
        rest = max(rest, prev_sold)
    return max(sold, rest)
```

### Complexity Analysis

- **Time:** $O(n)$
- **Space:** $O(1)$

---

## 6. Stock with Transaction Fee

**Problem:** Unlimited transactions, pay fee for each sell.

### Optimal Python Solution

```python
def max_profit_fee(prices: list[int], fee: int) -> int:
    hold = float('-inf')
    cash = 0
    for p in prices:
        hold = max(hold, cash - p)
        cash = max(cash, hold + p - fee)
    return cash
```

### Complexity Analysis

- **Time:** $O(n)$
- **Space:** $O(1)$

# Buy and Sell Stock Solutions

## Problem: Buy and Sell Stock I
You are given an array `prices` where `prices[i]` is the price of a given stock on the `i-th` day. You want to maximize your profit by choosing a single day to buy one stock and choosing a different day in the future to sell that stock. Return the maximum profit you can achieve from this transaction. If you cannot achieve any profit, return 0.

### Implementation

```python
def max_profit_1(prices: list[int]) -> int:
    """
    Finds max profit with at most one transaction.
    Time complexity: O(n)
    Space complexity: O(1)
    """
    min_price = float('inf')
    max_p = 0
    for price in prices:
        min_price = min(min_price, price)
        max_p = max(max_p, price - min_price)
    return max_p
```

## Problem: Buy and Sell Stock II
You are given an integer array `prices` where `prices[i]` is the price of a given stock on the `i-th` day. On each day, you may decide to buy and/or sell the stock. You can only hold at most one share of the stock at any time. However, you can buy it then immediately sell it on the same day. Find and return the maximum profit you can achieve.

### Implementation

```python
def max_profit_2(prices: list[int]) -> int:
    """
    Finds max profit with unlimited transactions.
    Time complexity: O(n)
    Space complexity: O(1)
    """
    profit = 0
    for i in range(1, len(prices)):
        if prices[i] > prices[i-1]:
            profit += prices[i] - prices[i-1]
    return profit
```

## Problem: Buy and Sell Stock III
Find the maximum profit you can achieve. You may complete at most two transactions.

### Implementation

```python
def max_profit_3(prices: list[int]) -> int:
    """
    Finds max profit with at most two transactions.
    Time complexity: O(n)
    Space complexity: O(1)
    """
    # buy1/buy2 represent the net profit after buying (negative)
    buy1, buy2 = float('-inf'), float('-inf')
    sell1, sell2 = 0, 0
    for price in prices:
        buy1 = max(buy1, -price)
        sell1 = max(sell1, buy1 + price)
        buy2 = max(buy2, sell1 - price)
        sell2 = max(sell2, buy2 + price)
    return sell2
```

## Problem: Buy and Sell Stock with Cooldown
You are given an array `prices` where `prices[i]` is the price of a given stock on the `i-th` day. Find the maximum profit you can achieve. You may complete as many transactions as you like (i.e., buy one and sell one share of the stock multiple times) with the following restriction: After you sell your stock, you cannot buy stock on the next day (i.e., cooldown one day).

### Implementation

```python
def max_profit_cooldown(prices: list[int]) -> int:
    """
    Max profit with unlimited transactions and 1-day cooldown.
    Time complexity: O(n)
    Space complexity: O(1)
    """
    if not prices:
        return 0
    # hold: max profit if holding stock
    # sold: max profit if just sold stock
    # rest: max profit if not holding and not in cooldown
    hold, sold, rest = float('-inf'), 0, 0

    for price in prices:
        prev_sold = sold
        sold = hold + price
        hold = max(hold, rest - price)
        rest = max(rest, prev_sold)

    return max(sold, rest)
```

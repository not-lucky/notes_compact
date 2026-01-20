# Best Time to Buy and Sell Stock

## Problem Statement

Given an array `prices` where `prices[i]` is the price of a given stock on day `i`, find the maximum profit you can achieve from one transaction (buy one and sell one share).

You must buy before you sell. If no profit is possible, return 0.

**Example:**
```
Input: prices = [7, 1, 5, 3, 6, 4]
Output: 5
Explanation: Buy on day 2 (price=1), sell on day 5 (price=6). Profit = 6-1 = 5.
```

## Building Intuition

### Why This Works

The key insight is that profit depends on two things: the buy price and the sell price. Since we must buy before we sell, as we scan forward through time, we only care about the minimum price we have seen so far (the best possible buy point for any future sell).

At each day, we ask: "If I sold today, what is the maximum profit I could make?" The answer is simply today's price minus the minimum price seen so far. We track the global maximum of this value across all days.

This works because we are decomposing a two-variable optimization (choose buy day AND sell day) into a single-variable scan. By maintaining the running minimum, we have already solved "what is the best buy day for any sell day up to now?" implicitly.

### How to Discover This

When you see a problem involving pairs where one must come before the other (buy before sell, start before end), consider: can I maintain a running aggregate (min, max, sum) that captures the best choice for the first element?

The pattern of "for each position, what is the best result ending/starting here?" is extremely common. It leads to Kadane's algorithm, prefix sums, and many DP solutions.

### Pattern Recognition

This is the **Running Minimum/Maximum** pattern, closely related to **Kadane's Algorithm**. The stock problem is actually equivalent to finding the maximum subarray sum of daily price changes (differences between consecutive days).

You will see this pattern in:
- Maximum subarray problems
- Best time to buy/sell variants
- Finding maximum difference with order constraint
- Prefix/suffix optimization problems

## When NOT to Use

- **When multiple transactions are allowed**: The simple min-tracking approach assumes one buy and one sell. For multiple transactions, you need DP or state machines.
- **When there is a cooldown or transaction fee**: These add state dependencies that require explicit DP formulation.
- **When you need the actual days, not just the profit**: You would need to track the indices of min and max, not just their values.
- **When prices can go negative**: The algorithm still works, but make sure your understanding of "profit" accounts for this (selling at -5 after buying at -10 is still a profit of 5).

## Approach

### Key Insight
We want to find the maximum difference between any two elements where the smaller element comes before the larger one.

### Optimal: Single Pass with Minimum Tracking
1. Track the minimum price seen so far
2. At each price, calculate potential profit (current - minimum)
3. Update maximum profit if current profit is larger
4. Update minimum if current price is smaller

```
prices = [7, 1, 5, 3, 6, 4]

Day 1: price=7, min=7, profit=0, max_profit=0
Day 2: price=1, min=1, profit=0, max_profit=0
Day 3: price=5, min=1, profit=4, max_profit=4
Day 4: price=3, min=1, profit=2, max_profit=4
Day 5: price=6, min=1, profit=5, max_profit=5
Day 6: price=4, min=1, profit=3, max_profit=5

Result: 5
```

## Implementation

```python
def max_profit(prices: list[int]) -> int:
    """
    Find maximum profit from single buy-sell transaction.

    Time: O(n) - single pass
    Space: O(1) - only tracking two variables
    """
    if not prices:
        return 0

    min_price = prices[0]
    max_profit = 0

    for price in prices:
        # Calculate profit if we sold today
        profit = price - min_price
        max_profit = max(max_profit, profit)

        # Update minimum price for future sells
        min_price = min(min_price, price)

    return max_profit


def max_profit_kadane(prices: list[int]) -> int:
    """
    Alternative: Transform to max subarray problem.

    Convert prices to daily gains: [7,1,5,3,6,4] → [-6,4,-2,3,-2]
    Then find max subarray sum (Kadane's algorithm)
    """
    if len(prices) < 2:
        return 0

    max_current = 0
    max_profit = 0

    for i in range(1, len(prices)):
        daily_gain = prices[i] - prices[i-1]
        max_current = max(0, max_current + daily_gain)
        max_profit = max(max_profit, max_current)

    return max_profit
```

## Complexity Analysis

| Aspect | Complexity | Explanation |
|--------|------------|-------------|
| Time | O(n) | Single pass through prices array |
| Space | O(1) | Only two variables: min_price, max_profit |

## Edge Cases

1. **Empty array**: Return 0
2. **Single element**: Can't make transaction, return 0
3. **Decreasing prices**: `[7, 6, 4, 3, 1]` → Profit is 0
4. **All same prices**: `[5, 5, 5, 5]` → Profit is 0
5. **Minimum at end**: `[7, 3, 5, 1]` → Still works, profit is 2
6. **Large values**: Works with any integer range

## Common Mistakes

1. **Selling before buying**: Must track minimum BEFORE current price
2. **Returning negative profit**: If no profit possible, return 0
3. **Multiple transactions**: This problem only allows ONE transaction

## Variations

### Best Time to Buy and Sell Stock II
Can make unlimited transactions - sum all positive differences.

```python
def max_profit_ii(prices: list[int]) -> int:
    """Buy and sell any number of times."""
    return sum(max(0, prices[i] - prices[i-1])
               for i in range(1, len(prices)))
```

### Best Time to Buy and Sell Stock III
At most 2 transactions - use state machine DP.

### Best Time to Buy and Sell Stock IV
At most k transactions - generalized DP approach.

### Best Time with Cooldown
Must wait one day after selling before buying again.

### Best Time with Transaction Fee
Each transaction costs a fee.

## Visual Explanation

```
Price
  7 |  *
  6 |        *     *
  5 |     *           *
  4 |
  3 |        *
  2 |
  1 |  *
    +-------------------> Day
       1  2  3  4  5  6

Buy at day 2 (price=1), sell at day 5 (price=6)
Profit = 6 - 1 = 5
```

## Related Problems

- **Maximum Subarray (Kadane's)** - Same concept, different framing
- **Best Time II/III/IV** - Multiple transaction variants
- **Buy/Sell with Cooldown** - State machine approach
- **Buy/Sell with Transaction Fee** - Greedy with fee consideration

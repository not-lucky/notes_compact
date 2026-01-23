# Practice Problems - Greedy Basics

## 1. Assign Cookies

### Problem Statement
Assume you are an awesome parent and want to give your children some cookies. But, you should give each child at most one cookie. Each child `i` has a greed factor `g[i]`, which is the minimum size of a cookie that the child will be content with; and each cookie `j` has a size `s[j]`. If `s[j] >= g[i]`, we can assign the cookie `j` to the child `i`, and the child `i` will be content. Your goal is to maximize the number of your content children and output the maximum number.

### Constraints
- `1 <= g.length <= 3 * 10^4`
- `0 <= s.length <= 3 * 10^4`
- `1 <= g[i], s[j] <= 2^31 - 1`

### Example
**Input:** `g = [1,2,3], s = [1,1]`
**Output:** `1`
**Explanation:** You have 3 children and 2 cookies. The greed factors of 3 children are 1, 2, 3. And even though you have 2 cookies, since their size is both 1, you could only make the child whose greed factor is 1 content.

### Python Implementation
```python
def findContentChildren(g: list[int], s: list[int]) -> int:
    g.sort()
    s.sort()
    child_i = 0
    cookie_j = 0
    while child_i < len(g) and cookie_j < len(s):
        if s[cookie_j] >= g[child_i]:
            child_i += 1
        cookie_j += 1
    return child_i
```

## 2. Lemonade Change

### Problem Statement
At a lemonade stand, each lemonade costs $5. Customers are standing in a queue to buy from you and order one at a time. Each customer will only buy one lemonade and pay with either a $5, $10, or $20 bill. You must provide the correct change to each customer so that the net transaction is that the customer pays $5.

Note that you do not have any change in hand at first.

Given an integer array `bills` where `bills[i]` is the bill the `i-th` customer pays, return `true` if you can provide every customer with the correct change, or `false` otherwise.

### Constraints
- `1 <= bills.length <= 10^5`
- `bills[i]` is either 5, 10, or 20.

### Example
**Input:** `bills = [5,5,5,10,20]`
**Output:** `true`
**Explanation:**
From the first 3 customers, we collect three $5 bills in order.
From the fourth customer, we collect a $10 bill and give back a $5 bill.
From the fifth customer, we give a $10 bill and a $5 bill.
Since all customers got correct change, we output true.

### Python Implementation
```python
def lemonadeChange(bills: list[int]) -> bool:
    five = ten = 0
    for bill in bills:
        if bill == 5:
            five += 1
        elif bill == 10:
            if not five: return False
            five -= 1
            ten += 1
        else:
            if ten and five:
                ten -= 1
                five -= 1
            elif five >= 3:
                five -= 3
            else:
                return False
    return True
```

## 3. Best Time to Buy and Sell Stock II

### Problem Statement
You are given an integer array `prices` where `prices[i]` is the price of a given stock on the `i-th` day.
On each day, you may decide to buy and/or sell the stock. You can only hold at most one share of the stock at any time. However, you can buy it then immediately sell it on the same day.
Find and return the maximum profit you can achieve.

### Constraints
- `1 <= prices.length <= 3 * 10^4`
- `0 <= prices[i] <= 10^4`

### Example
**Input:** `prices = [7,1,5,3,6,4]`
**Output:** `7`
**Explanation:** Buy on day 2 (price = 1) and sell on day 3 (price = 5), profit = 5-1 = 4.
Then buy on day 4 (price = 3) and sell on day 5 (price = 6), profit = 6-3 = 3.
Total profit is 4 + 3 = 7.

### Python Implementation
```python
def maxProfit(prices: list[int]) -> int:
    profit = 0
    for i in range(1, len(prices)):
        if prices[i] > prices[i-1]:
            profit += prices[i] - prices[i-1]
    return profit
```

## 4. Boats to Save People

### Problem Statement
You are given an array `people` where `people[i]` is the weight of the `i-th` person, and an infinite number of boats where each boat can carry a maximum weight of `limit`. Each boat carries at most two people at the same time, provided the sum of the weight of those people is at most `limit`.
Return the minimum number of boats to carry every given person.

### Constraints
- `1 <= people.length <= 5 * 10^4`
- `1 <= people[i] <= limit <= 3 * 10^4`

### Example
**Input:** `people = [3,2,2,1], limit = 3`
**Output:** `3`
**Explanation:** 3 boats (1, 2), (2) and (3)

### Python Implementation
```python
def numRescueBoats(people: list[int], limit: int) -> int:
    people.sort()
    i, j = 0, len(people) - 1
    boats = 0
    while i <= j:
        if people[i] + people[j] <= limit:
            i += 1
        j -= 1
        boats += 1
    return boats
```

## 5. Minimum Number of Arrows to Burst Balloons

### Problem Statement
There are some spherical balloons taped onto a flat wall that represents the XY-plane. The balloons are represented as a 2D integer array `points` where `points[i] = [x_start, x_end]` denotes a balloon whose horizontal diameter stretches between `x_start` and `x_end`. You do not know the exact y-coordinates of the balloons.

Arrows can be shot up vertically (in the positive y-direction) from different points along the x-axis. A balloon with `x_start` and `x_end` is burst by an arrow shot at `x` if `x_start <= x <= x_end`. There is no limit to the number of arrows that can be shot. A shot arrow keeps traveling up infinitely, bursting any balloons in its path.

Given the array `points`, return the minimum number of arrows that must be shot to burst all balloons.

### Constraints
- `1 <= points.length <= 10^5`
- `points[i].length == 2`
- `-2^31 <= x_start < x_end <= 2^31 - 1`

### Example
**Input:** `points = [[10,16],[2,8],[1,6],[7,12]]`
**Output:** `2`
**Explanation:** The balloons can be burst by 2 arrows:
- Shoot an arrow at x = 6, bursting the balloons [2,8] and [1,6].
- Shoot an arrow at x = 11, bursting the balloons [10,16] and [7,12].

### Python Implementation
```python
def findMinArrowShots(points: list[list[int]]) -> int:
    if not points: return 0
    points.sort(key=lambda x: x[1])
    arrows = 1
    end = points[0][1]
    for i in range(1, len(points)):
        if points[i][0] > end:
            arrows += 1
            end = points[i][1]
    return arrows
```

# Solutions: Greedy Basics

## 1. Assign Cookies
**Problem Statement**:
Assume you are an awesome parent and want to give your children some cookies. But, you should give each child at most one cookie. Each child `i` has a greed factor `g[i]`, which is the minimum size of a cookie that the child will be content with; and each cookie `j` has a size `s[j]`. If `s[j] >= g[i]`, we can assign the cookie `j` to the child `i`, and the child `i` will be content. Your goal is to maximize the number of your content children and output the maximum number.

**Examples & Edge Cases**:
- **Example 1**:
    - Input: `g = [1,2,3], s = [1,1]`
    - Output: `1`
    - Explanation: You have 3 children and 2 cookies. The greed factors of 3 children are 1, 2, 3. Even though you have 2 cookies, since their size is both 1, you could only make the child whose greed factor is 1 content.
- **Example 2**:
    - Input: `g = [1,2], s = [1,2,3]`
    - Output: `2`
    - Explanation: You have 2 children and 3 cookies. The greed factors of 2 children are 1, 2. You have 3 cookies and their sizes are big enough to gratify all of the children.
- **Edge Cases**:
    - `g` or `s` is empty: Return 0.
    - All cookies are smaller than the smallest greed factor: Return 0.
    - All cookies are larger than the largest greed factor: All children (or all cookies if fewer) can be satisfied.

**Optimal Python Solution**:
```python
def findContentChildren(g: list[int], s: list[int]) -> int:
    """
    Assign cookies to children to maximize satisfied children.
    Greedy Strategy: Satisfy the child with the smallest greed factor
    using the smallest possible cookie that meets the requirement.
    """
    # Sort both greed factors and cookie sizes
    g.sort()
    s.sort()

    child_i = 0
    cookie_j = 0

    # Iterate until we run out of children or cookies
    while child_i < len(g) and cookie_j < len(s):
        # If current cookie can satisfy current child
        if s[cookie_j] >= g[child_i]:
            # Move to next child
            child_i += 1
        # Move to next cookie regardless (if current didn't satisfy,
        # it won't satisfy any subsequent child with higher greed)
        cookie_j += 1

    return child_i
```

**Explanation**:
1.  **Sorting**: We sort both the greed factors (`g`) and the cookie sizes (`s`). This allows us to use a greedy approach where we try to satisfy the least greedy children first with the smallest possible cookies.
2.  **Two Pointers**: We use two pointers, `child_i` and `cookie_j`, to traverse the arrays.
3.  **Greedy Choice**: For each child, we look for the first cookie that is large enough. Since the cookies are sorted, the first one we find is the smallest one that works, leaving larger cookies for potentially more greedy children.
4.  **Efficiency**: If a cookie doesn't satisfy the current child, it certainly won't satisfy any later child because the children are sorted by increasing greed. Thus, we move to the next cookie.

**Complexity Analysis**:
- **Time Complexity**: `O(N log N + M log M)`, where `N` is the number of children and `M` is the number of cookies. This is due to sorting both arrays. The subsequent two-pointer traversal takes `O(N + M)`.
- **Space Complexity**: `O(1)` (or `O(N+M)` depending on the sorting implementation's internal space usage) as we only use a constant amount of extra space for pointers.

---

## 2. Lemonade Change
**Problem Statement**:
At a lemonade stand, each lemonade costs $5. Customers are standing in a queue to buy from you and order one at a time (in the order specified by bills). Each customer will only buy one lemonade and pay with either a $5, $10, or $20 bill. You must provide the correct change to each customer such that the net transaction is that the customer pays $5.

Note that you do not have any change in hand at first. Return `true` if and only if you can provide every customer with the correct change.

**Examples & Edge Cases**:
- **Example 1**:
    - Input: `bills = [5,5,5,10,20]`
    - Output: `true`
    - Explanation: We collect three $5 bills. For $10, we give one $5 back. For $20, we give one $10 and one $5 back.
- **Example 2**:
    - Input: `bills = [5,5,10,10,20]`
    - Output: `false`
    - Explanation: From the first two customers, we collect two $5 bills. For the next two customers in order, we collect two $10 bills and give back two $5 bills. For the last customer, we need $15 change, but we only have two $10 bills left.
- **Edge Cases**:
    - First bill is not $5: Return `false` immediately.
    - Only $5 bills: Always `true`.
    - Mixture of bills where $5s run out quickly.

**Optimal Python Solution**:
```python
def lemonadeChange(bills: list[int]) -> bool:
    """
    Give correct change for $5 lemonade using greedy choice for $20 bills.
    """
    five = 0
    ten = 0

    for bill in bills:
        if bill == 5:
            five += 1
        elif bill == 10:
            if not five:
                return False
            five -= 1
            ten += 1
        else: # bill == 20
            # Greedy: prioritize giving one $10 and one $5 as change
            # because $5 is more versatile (can be used for $10 or $20).
            if ten > 0 and five > 0:
                ten -= 1
                five -= 1
            elif five >= 3:
                five -= 3
            else:
                return False

    return True
```

**Explanation**:
1.  **Tracking Cash**: We only need to track $5 and $10 bills because $20 bills are never used as change.
2.  **Handling $5**: No change needed, just increment the count.
3.  **Handling $10**: Need one $5 as change. If we don't have it, return `false`.
4.  **Handling $20 (Greedy Choice)**: We need $15 in change. We have two options: (one $10 + one $5) OR (three $5s).
    - **Greedy Logic**: We prefer to use a $10 bill if we have one. Why? Because a $5 bill is more "valuable" for future change needs (it can satisfy a $10 bill customer, whereas a $10 bill cannot). By saving $5 bills, we increase our chances of satisfying future customers.
5.  **Termination**: If at any point we can't provide change, return `false`.

**Complexity Analysis**:
- **Time Complexity**: `O(N)`, where `N` is the number of bills. We iterate through the list of bills exactly once.
- **Space Complexity**: `O(1)`, as we only store the counts of $5 and $10 bills.

---

## 3. Best Time to Buy and Sell Stock II
**Problem Statement**:
You are given an integer array `prices` where `prices[i]` is the price of a given stock on the `i-th` day. On each day, you may decide to buy and/or sell the stock. You can only hold at most one share of the stock at any time. However, you can buy it then immediately sell it on the same day. Find and return the maximum profit you can achieve.

**Examples & Edge Cases**:
- **Example 1**:
    - Input: `prices = [7,1,5,3,6,4]`
    - Output: `7`
    - Explanation: Buy on day 2 (price = 1) and sell on day 3 (price = 5), profit = 4. Then buy on day 4 (price = 3) and sell on day 5 (price = 6), profit = 3. Total profit = 7.
- **Example 2**:
    - Input: `prices = [1,2,3,4,5]`
    - Output: `4`
    - Explanation: Buy on day 1 (price = 1) and sell on day 5 (price = 5), profit = 4.
- **Edge Cases**:
    - Prices are strictly decreasing: Profit is 0.
    - Only one day: Profit is 0.
    - All prices are the same: Profit is 0.

**Optimal Python Solution**:
```python
def maxProfit(prices: list[int]) -> int:
    """
    Maximize profit by collecting all upward price movements.
    """
    max_profit = 0

    # Iterate through prices starting from the second day
    for i in range(1, len(prices)):
        # If the price today is higher than yesterday
        if prices[i] > prices[i-1]:
            # "Buy" yesterday and "sell" today to capture the profit
            max_profit += prices[i] - prices[i-1]

    return max_profit
```

**Explanation**:
1.  **Locally Optimal Choice**: The problem allows multiple transactions. To maximize profit, we should capture every single "upward" price movement between consecutive days.
2.  **Summing Slopes**: If `prices[i] > prices[i-1]`, we add the difference to our total profit. This is equivalent to buying at a valley and selling at the next peak. Even if the price continues to rise (e.g., [1, 2, 3]), adding (2-1) and then (3-2) is the same as (3-1).
3.  **Why Greedy Works**: Since we can perform transactions on the same day, we don't need to worry about "missing" a better future price by selling today. If the price goes up again tomorrow, we can just "buy" today (at the same price we sold) and "sell" tomorrow.

**Complexity Analysis**:
- **Time Complexity**: `O(N)`, where `N` is the number of days. We perform a single pass through the array.
- **Space Complexity**: `O(1)`, as we only store the `max_profit` variable.

---

## 4. Boats to Save People
**Problem Statement**:
You are given an array `people` where `people[i]` is the weight of the `i-th` person, and an infinite number of boats where each boat can carry a maximum weight of `limit`. Each boat carries at most two people at the same time, provided the sum of the weight of those people is at most `limit`. Return the minimum number of boats to carry every given person.

**Examples & Edge Cases**:
- **Example 1**:
    - Input: `people = [1,2], limit = 3`
    - Output: `1`
- **Example 2**:
    - Input: `people = [3,2,2,1], limit = 3`
    - Output: `3` (boats: [1,2], [2], [3])
- **Edge Cases**:
    - One person: 1 boat.
    - All people are exactly the `limit`: Each needs their own boat.
    - Smallest person + largest person > `limit`: The largest person MUST go alone.

**Optimal Python Solution**:
```python
def numRescueBoats(people: list[int], limit: int) -> int:
    """
    Minimize boats by pairing the heaviest person with the lightest
    person possible using a two-pointer greedy approach.
    """
    people.sort()

    left = 0
    right = len(people) - 1
    boats = 0

    while left <= right:
        # Heaviest person always needs a boat
        boats += 1
        # If the lightest person can fit with the heaviest person
        if people[left] + people[right] <= limit:
            # Move the lightest person pointer
            left += 1
        # Move the heaviest person pointer (they are now on the boat)
        right -= 1

    return boats
```

**Explanation**:
1.  **Sorting**: Sort people by weight to enable pairing.
2.  **Two Pointers**: Use `left` for the lightest person and `right` for the heaviest.
3.  **Greedy Strategy**: The heaviest person (`people[right]`) *must* be on a boat. To maximize efficiency, we check if they can share that boat with the lightest person (`people[left]`).
    - If they *can* share, we increment the boat count and move both pointers.
    - If they *cannot* share, the heaviest person must go alone. We still increment the boat count but only move the `right` pointer.
4.  **Optimality**: By pairing the heaviest with the lightest, we free up the "lightest" capacity to potentially pair with other heavy people later.

**Complexity Analysis**:
- **Time Complexity**: `O(N log N)`, where `N` is the number of people. Sorting dominates the complexity. The two-pointer walk is `O(N)`.
- **Space Complexity**: `O(1)` or `O(N)` depending on the sorting implementation.

---

## 5. Minimum Number of Arrows to Burst Balloons
**Problem Statement**:
There are some spherical balloons taped onto a flat wall that represents the XY-plane. For each balloon, provided input is the horizontal range `[x_start, x_end]`. You do not know the exact y-coordinates. Arrows can be shot up vertically (in the positive y-direction) from different points along the x-axis. A balloon with `x_start` and `x_end` is burst by an arrow shot at `x` if `x_start <= x <= x_end`. There is no limit to the number of arrows that can be shot. A single arrow can burst multiple balloons. Given the array `points`, return the minimum number of arrows that must be shot to burst all balloons.

**Examples & Edge Cases**:
- **Example 1**:
    - Input: `points = [[10,16],[2,8],[1,6],[7,12]]`
    - Output: `2` (One arrow at x=6 bursts [1,6] and [2,8]. One arrow at x=12 bursts [7,12] and [10,16]).
- **Example 2**:
    - Input: `points = [[1,2],[3,4],[5,6],[7,8]]`
    - Output: `4`
- **Edge Cases**:
    - Empty input: 0 arrows.
    - All balloons overlap at one point: 1 arrow.
    - No balloons overlap: `N` arrows.

**Optimal Python Solution**:
```python
def findMinArrowShots(points: list[list[int]]) -> int:
    """
    Minimize arrows by sorting by end position and shooting at the
    end of the first available balloon.
    """
    if not points:
        return 0

    # Sort balloons by their end coordinate
    # Sorting by end ensures we handle the "earliest finishing" overlap
    points.sort(key=lambda x: x[1])

    arrows = 1
    # Initial arrow shot at the end of the first balloon
    first_end = points[0][1]

    for i in range(1, len(points)):
        # If the current balloon starts AFTER the last arrow position
        if points[i][0] > first_end:
            # Need a new arrow
            arrows += 1
            # Update arrow position to the end of this balloon
            first_end = points[i][1]

    return arrows
```

**Explanation**:
1.  **Greedy Choice**: To burst as many balloons as possible with one arrow, we should shoot the arrow as far to the right as possible for any given balloon.
2.  **Sorting by End**: By sorting by the *end* coordinate, we ensure that when we decide where to shoot an arrow, we shoot it at `points[i][1]`. This is the best position to catch any subsequent balloons that start before or at this end point.
3.  **Iterative Step**: We track the position of the last arrow shot (`first_end`). If a new balloon's start point is greater than `first_end`, it means the previous arrow cannot burst it. We must shoot a new arrow and we greedily place it at the end of this new balloon.

**Complexity Analysis**:
- **Time Complexity**: `O(N log N)`, where `N` is the number of balloons. Sorting is the bottleneck. The scan is `O(N)`.
- **Space Complexity**: `O(1)` or `O(N)` depending on the sorting implementation.

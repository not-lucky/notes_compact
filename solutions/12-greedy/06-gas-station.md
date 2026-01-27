# Solutions: Gas Station

## 1. Gas Station
**Problem Statement**:
There are `n` gas stations along a circular route, where the amount of gas at the `i-th` station is `gas[i]`. You have a car with an unlimited gas tank and it costs `cost[i]` of gas to travel from the `i-th` station to its next `(i+1)-th` station. You begin the journey with an empty tank at one of the gas stations.

Given two integer arrays `gas` and `cost`, return the starting gas station's index if you can travel around the circuit once in the clockwise direction, otherwise return `-1`. If there exists a solution, it is guaranteed to be unique.

**Examples & Edge Cases**:
- **Example 1**:
    - Input: `gas = [1,2,3,4,5], cost = [3,4,5,1,2]`
    - Output: `3`
    - Explanation: Start at station 3. You have 4 unit of gas. Cost to next is 1. Tank = 3. At station 4, gain 5, tank = 8. Cost to next is 2. Tank = 6...
- **Example 2**:
    - Input: `gas = [2,3,4], cost = [3,4,3]`
    - Output: `-1`
- **Edge Cases**:
    - `sum(gas) < sum(cost)`: Impossible.
    - Single station.

**Optimal Python Solution**:
```python
def canCompleteCircuit(gas: list[int], cost: list[int]) -> int:
    """
    Greedy solution based on total feasibility and local failure elimination.
    """
    # 1. If total gas is less than total cost, it's impossible.
    if sum(gas) < sum(cost):
        return -1

    total_tank = 0
    start_index = 0
    current_tank = 0

    for i in range(len(gas)):
        # Calculate net gas gain/loss at this station
        gain = gas[i] - cost[i]

        total_tank += gain
        current_tank += gain

        # 2. If current_tank drops below 0, we cannot reach the next station
        # from our current start_index.
        if current_tank < 0:
            # Greedy Insight: If we fail at i, then NO station between
            # the current start_index and i can be the starting point.
            # So we try the next station as the new start.
            start_index = i + 1
            current_tank = 0

    return start_index
```

**Explanation**:
1.  **Global Feasibility**: If the total amount of gas in all stations is less than the total cost to travel the whole loop, no starting point will ever work.
2.  **Greedy Elimination**: Suppose we start at station `A` and run out of gas at station `B`. This means that any station between `A` and `B` would also fail to reach `B` (because we would have even less gas starting from them than we had arriving from `A`). Thus, we can safely skip all stations in the range `[A, B]` and try starting at `B + 1`.
3.  **Unique Solution**: Because the problem guarantees a unique solution if one exists, the first `start_index` that makes it to the end of the array without the `current_tank` going negative is the correct answer.

**Complexity Analysis**:
- **Time Complexity**: `O(N)`, as we traverse the arrays once.
- **Space Complexity**: `O(1)`, as we only use a few variables.

---

## 2. Maximum Sum Circular Subarray
**Problem Statement**:
Given a circular integer array `nums` of length `n`, return the maximum possible sum of a non-empty subarray of `nums`.

**Examples & Edge Cases**:
- **Example 1**:
    - Input: `nums = [1,-2,3,-2]`
    - Output: `3`
- **Example 2**:
    - Input: `nums = [5,-3,5]`
    - Output: `10` (5 + 5 from circular wrap)
- **Edge Cases**:
    - All negative numbers.

**Optimal Python Solution**:
```python
def maxSubarraySumCircular(nums: list[int]) -> int:
    """
    Max circular subarray = max(normal_kadane, total_sum - min_kadane).
    """
    # 1. Find normal Max Subarray Sum (Kadane's)
    current_max = 0
    max_total = nums[0]

    # 2. Find Min Subarray Sum (to calculate the circular wrap)
    current_min = 0
    min_total = nums[0]

    total_sum = 0

    for x in nums:
        total_sum += x

        # Kadane for Max
        current_max = max(x, current_max + x)
        max_total = max(max_total, current_max)

        # Kadane for Min
        current_min = min(x, current_min + x)
        min_total = min(min_total, current_min)

    # Edge Case: If all numbers are negative, max_total is the answer.
    # (total_sum - min_total would result in 0, which is an empty subarray)
    if max_total < 0:
        return max_total

    # The max circular sum is the total minus the "middle" minimum part
    return max(max_total, total_sum - min_total)
```

**Explanation**:
1.  **Two Cases**:
    - **Case 1**: The maximum subarray is in the middle (standard Kadane's).
    - **Case 2**: The maximum subarray wraps around (it includes the head and tail).
2.  **Wrap-around Logic**: If the subarray wraps around, then the *unused* part in the middle must be the minimum subarray. Therefore, `Max Circular = Total Sum - Min Subarray`.
3.  **Kadane's**: We run the standard Kadane's algorithm twice (once for max, once for min) in a single pass.

**Complexity Analysis**:
- **Time Complexity**: `O(N)`.
- **Space Complexity**: `O(1)`.

---

## 3. Minimum Number of Refueling Stops
**Problem Statement**:
A car travels from a `target` distance. It starts with `startFuel`. There are gas stations along the way. `stations[i] = [position_i, fuel_i]`. You want to reach the `target` with minimum refueling stops.

**Optimal Python Solution (Greedy with Heap)**:
```python
import heapq

def minRefuelStops(target: int, startFuel: int, stations: list[list[int]]) -> int:
    """
    Greedy: At each step, go as far as you can. If you run out,
    'retroactively' refuel at the best station you passed.
    """
    # Max-heap to store fuel from stations we passed but didn't use
    passed_fuel = []

    current_fuel = startFuel
    stops = 0
    prev_pos = 0

    # Add target as a dummy station to handle the final stretch
    for pos, fuel in stations + [[target, 0]]:
        distance = pos - prev_pos
        current_fuel -= distance

        # If we ran out of fuel, refuel from the best passed station
        while passed_fuel and current_fuel < 0:
            # heapq is a min-heap, so we store negative values for max-heap
            current_fuel += -heapq.heappop(passed_fuel)
            stops += 1

        if current_fuel < 0:
            return -1

        heapq.heappush(passed_fuel, -fuel)
        prev_pos = pos

    return stops
```

**Explanation**:
1.  **Lazy Greedy**: We drive as far as we can. If we run out of gas, we look back at all the gas stations we passed and pick the one with the most gas.
2.  **Heap**: We use a max-heap to store the gas amounts of all passed stations so we can always pick the largest one.
3.  **Efficiency**: We only refuel when absolutely necessary, ensuring the minimum number of stops.

**Complexity Analysis**:
- **Time Complexity**: `O(N log N)`.
- **Space Complexity**: `O(N)` for the heap.

---

## 4. Cheapest Flights Within K Stops
**Problem Statement**:
There are `n` cities connected by some number of flights. You are given an array `flights` where `flights[i] = [from_i, to_i, price_i]` indicates that there is a flight from city `from_i` to city `to_i` with cost `price_i`. You are also given three integers `src`, `dst`, and `k`, return the cheapest price from `src` to `dst` with at most `k` stops. If there is no such route, return `-1`.

**Optimal Python Solution (BFS / Bellman-Ford variant)**:
```python
from collections import deque

def findCheapestPrice(n: int, flights: list[list[int]], src: int, dst: int, k: int) -> int:
    """
    Greedy BFS (Bellman-Ford variant): track minimum cost to each city within k stops.
    """
    # Adjacency list
    adj = {i: [] for i in range(n)}
    for f, t, p in flights:
        adj[f].append((t, p))

    # Track min cost to each city
    prices = [float('inf')] * n
    prices[src] = 0

    # Queue for BFS: (city, current_cost)
    queue = deque([(src, 0)])
    stops = 0

    while queue and stops <= k:
        size = len(queue)
        for _ in range(size):
            curr_city, curr_cost = queue.popleft()

            for neighbor, price in adj[curr_city]:
                if curr_cost + price < prices[neighbor]:
                    prices[neighbor] = curr_cost + price
                    queue.append((neighbor, prices[neighbor]))
        stops += 1

    return int(prices[dst]) if prices[dst] != float('inf') else -1
```

**Explanation**:
1.  **Greedy BFS**: We explore the graph level by level (where each level represents one stop).
2.  **State**: We maintain the minimum price to reach each city found so far.
3.  **Optimization**: If we find a cheaper way to reach a city within the allowed stops, we update its price and add it back to the queue for further exploration.
4.  **Termination**: We stop after `k + 1` levels (which corresponds to `k` stops).

**Complexity Analysis**:
- **Time Complexity**: `O(K * E)`, where `E` is the number of flights (edges).
- **Space Complexity**: `O(V + E)`, for the adjacency list and prices array.

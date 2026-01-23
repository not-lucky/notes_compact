# Practice Problems - Gas Station

## 1. Gas Station

### Problem Statement
There are `n` gas stations along a circular route, where the amount of gas at the `i-th` station is `gas[i]`.
You have a car with an unlimited gas tank and it costs `cost[i]` of gas to travel from the `i-th` station to its next `(i + 1)-th` station. You begin the journey with an empty tank at one of the gas stations.
Given two integer arrays `gas` and `cost`, return the starting gas station's index if you can travel around the circuit once in the clockwise direction, otherwise return -1. If there exists a solution, it is guaranteed to be unique.

### Constraints
- `n == gas.length == cost.length`
- `1 <= n <= 10^5`
- `0 <= gas[i], cost[i] <= 10^4`

### Example
**Input:** `gas = [1,2,3,4,5], cost = [3,4,5,1,2]`
**Output:** `3`

### Python Implementation
```python
def canCompleteCircuit(gas: list[int], cost: list[int]) -> int:
    if sum(gas) < sum(cost): return -1
    total = 0
    start = 0
    for i in range(len(gas)):
        total += gas[i] - cost[i]
        if total < 0:
            total = 0
            start = i + 1
    return start
```

## 2. Maximum Sum Circular Subarray

### Problem Statement
Given a circular integer array `nums` of length `n`, return the maximum possible sum of a non-empty subarray of `nums`.
A circular array means the end of the array connects to the beginning of the array. Formally, the next element of `nums[i]` is `nums[(i + 1) % n]` and the previous element of `nums[i]` is `nums[(i - 1 + n) % n]`.
A subarray may only include each element of the fixed buffer `nums` at most once.

### Constraints
- `n == nums.length`
- `1 <= n <= 3 * 10^4`
- `-3 * 10^4 <= nums[i] <= 3 * 10^4`

### Example
**Input:** `nums = [1,-2,3,-2]`
**Output:** `3`

### Python Implementation
```python
def maxSubarraySumCircular(nums: list[int]) -> int:
    total = 0
    cur_max = 0
    max_sum = nums[0]
    cur_min = 0
    min_sum = nums[0]

    for x in nums:
        total += x
        cur_max = max(cur_max + x, x)
        max_sum = max(max_sum, cur_max)
        cur_min = min(cur_min + x, x)
        min_sum = min(min_sum, cur_min)

    if max_sum < 0: return max_sum
    return max(max_sum, total - min_sum)
```

## 3. Minimum Number of Refueling Stops

### Problem Statement
A car travels from a starting position to a `target` destination. There are gas stations along the way. The `i-th` gas station is at `stations[i][0]` and has `stations[i][1]` liters of gas.
The car starts with `startFuel` liters of gas. It uses 1 liter of gas per 1 unit of distance. When the car reaches a gas station, it may stop and refuel, transferring all the gas from the station into the car.
What is the minimum number of refueling stops the car must make in order to reach its destination? If it cannot reach the destination, return -1.

### Constraints
- `1 <= target, startFuel <= 10^9`
- `0 <= stations.length <= 500`
- `0 < stations[i][0] < stations[i+1][0] < target`
- `1 <= stations[i][1] <= 10^9`

### Example
**Input:** `target = 100, startFuel = 10, stations = [[10,60],[20,30],[30,30],[60,40]]`
**Output:** `2`

### Python Implementation
```python
import heapq

def minRefuelStops(target: int, startFuel: int, stations: list[list[int]]) -> int:
    max_heap = []
    res = 0
    cur_dist = startFuel
    i = 0
    while cur_dist < target:
        while i < len(stations) and stations[i][0] <= cur_dist:
            heapq.heappush(max_heap, -stations[i][1])
            i += 1
        if not max_heap: return -1
        cur_dist += -heapq.heappop(max_heap)
        res += 1
    return res
```

## 4. Cheapest Flights Within K Stops

### Problem Statement
There are `n` cities connected by some number of flights. You are given an array `flights` where `flights[i] = [from_i, to_i, price_i]` indicates that there is a flight from city `from_i` to city `to_i` with cost `price_i`.
You are also given three integers `src`, `dst`, and `k`, return the cheapest price from `src` to `dst` with at most `k` stops. If there is no such route, return -1.

### Constraints
- `1 <= n <= 100`
- `0 <= flights.length <= (n * (n - 1) / 2)`
- `flights[i].length == 3`
- `0 <= from_i, to_i < n`
- `from_i != to_i`
- `1 <= price_i <= 10^4`
- `0 <= src, dst, k < n`
- `src != dst`

### Example
**Input:** `n = 4, flights = [[0,1,100],[1,2,100],[2,0,100],[1,3,600],[2,3,200]], src = 0, dst = 3, k = 1`
**Output:** `700`

### Python Implementation
```python
def findCheapestPrice(n: int, flights: list[list[int]], src: int, dst: int, k: int) -> int:
    prices = [float('inf')] * n
    prices[src] = 0

    for _ in range(k + 1):
        temp = list(prices)
        for u, v, w in flights:
            if prices[u] != float('inf'):
                temp[v] = min(temp[v], prices[u] + w)
        prices = temp

    return prices[dst] if prices[dst] != float('inf') else -1
```

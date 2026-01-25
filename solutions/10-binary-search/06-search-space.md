# Binary Search on Answer Space Solutions

## 1. Koko Eating Bananas
[LeetCode 875](https://leetcode.com/problems/koko-eating-bananas/)

### Problem Description
Koko loves to eat bananas. There are `n` piles of bananas, the `i`-th pile has `piles[i]` bananas. The guards have gone and will come back in `h` hours. Koko can decide her bananas-per-hour eating speed of `k`. Each hour, she chooses some pile of bananas and eats `k` bananas from that pile. If the pile has less than `k` bananas, she eats all of them instead and will not eat any more bananas during this hour. Return the minimum integer `k` such that she can eat all the bananas within `h` hours.

### Solution
```python
import math

def minEatingSpeed(piles: list[int], h: int) -> int:
    def canFinish(k: int) -> bool:
        hours = 0
        for pile in piles:
            hours += math.ceil(pile / k)
        return hours <= h

    left, right = 1, max(piles)
    while left < right:
        mid = left + (right - left) // 2
        if canFinish(mid):
            right = mid
        else:
            left = mid + 1
    return left
```
- **Time Complexity**: O(n log(max(piles)))
- **Space Complexity**: O(1)

---

## 2. Capacity To Ship Packages Within D Days
[LeetCode 1011](https://leetcode.com/problems/capacity-to-ship-packages-within-d-days/)

### Problem Description
A conveyor belt has packages that must be shipped from one port to another within `days` days. The `i`-th package on the conveyor belt has a weight of `weights[i]`. Each day, we load the ship with packages on the conveyor belt (in the order given by weights). We may not load more weight than the maximum weight capacity of the ship. Return the least weight capacity of the ship that will result in all the packages on the conveyor belt being shipped within `days` days.

### Solution
```python
def shipWithinDays(weights: list[int], days: int) -> int:
    def canShip(capacity: int) -> bool:
        days_needed = 1
        curr_weight = 0
        for w in weights:
            if curr_weight + w > capacity:
                days_needed += 1
                curr_weight = w
            else:
                curr_weight += w
        return days_needed <= days

    left, right = max(weights), sum(weights)
    while left < right:
        mid = left + (right - left) // 2
        if canShip(mid):
            right = mid
        else:
            left = mid + 1
    return left
```
- **Time Complexity**: O(n log(sum(weights)))
- **Space Complexity**: O(1)

---

## 3. Split Array Largest Sum
[LeetCode 410](https://leetcode.com/problems/split-array-largest-sum/)

### Problem Description
Given an integer array `nums` and an integer `k`, split `nums` into `k` non-empty continuous subarrays such that the largest sum of any subarray is minimized. Return the minimized largest sum of the split.

### Solution
```python
def splitArray(nums: list[int], k: int) -> int:
    def canSplit(max_sum: int) -> bool:
        count = 1
        curr_sum = 0
        for num in nums:
            if curr_sum + num > max_sum:
                count += 1
                curr_sum = num
            else:
                curr_sum += num
        return count <= k

    left, right = max(nums), sum(nums)
    while left < right:
        mid = left + (right - left) // 2
        if canSplit(mid):
            right = mid
        else:
            left = mid + 1
    return left
```
- **Time Complexity**: O(n log(sum(nums)))
- **Space Complexity**: O(1)

---

## 4. Minimize Max Distance to Gas Station
[LeetCode 774](https://leetcode.com/problems/minimize-max-distance-to-gas-station/)

### Problem Description
You are given an integer array `stations` that represents the positions of gas stations on a 1D line. You are also given an integer `k`. You should add `k` new gas stations. You can add the stations anywhere on the 1D line, and not necessarily at integer positions. After adding the `k` stations, let `d` be the maximum distance between adjacent gas stations. Return the minimum possible value of `d`. Answers within $10^{-6}$ of the actual answer will be accepted.

### Solution
```python
def minmaxGasDist(stations: list[int], k: int) -> float:
    def canPlace(d: float) -> bool:
        count = 0
        for i in range(len(stations) - 1):
            count += int((stations[i+1] - stations[i]) / d)
        return count <= k

    left, right = 0, stations[-1] - stations[0]
    # Use a fixed number of iterations for float binary search (100 is usually enough)
    for _ in range(100):
        mid = (left + right) / 2
        if canPlace(mid):
            right = mid
        else:
            left = mid
    return left
```
- **Time Complexity**: O(n * log((max-min)/precision))
- **Space Complexity**: O(1)

---

## 5. Magnetic Force Between Two Balls
[LeetCode 1552](https://leetcode.com/problems/magnetic-force-between-two-balls/)

### Problem Description
Rick has `n` empty baskets at `position[i]`. He has `m` balls and needs to distribute them such that the minimum magnetic force between any two balls is maximized. Return the required force.

### Solution
```python
def maxDistance(position: list[int], m: int) -> int:
    position.sort()

    def canPlace(min_dist: int) -> bool:
        count = 1
        last_pos = position[0]
        for i in range(1, len(position)):
            if position[i] - last_pos >= min_dist:
                count += 1
                last_pos = position[i]
                if count >= m:
                    return True
        return False

    left, right = 1, position[-1] - position[0]
    res = 1
    while left <= right:
        mid = left + (right - left) // 2
        if canPlace(mid):
            res = mid
            left = mid + 1
        else:
            right = mid - 1
    return res
```
- **Time Complexity**: O(n log n + n log(max_dist))
- **Space Complexity**: O(1)

---

## 6. Find the Smallest Divisor Given a Threshold
[LeetCode 1283](https://leetcode.com/problems/find-the-smallest-divisor-given-a-threshold/)

### Problem Description
Given an array of integers `nums` and an integer `threshold`, choose a positive integer `divisor`, divide all the array by it, and sum the result's division. Each result of the division is rounded to the nearest integer greater than or equal to that element. Find the smallest divisor such that the result mentioned above is less than or equal to `threshold`.

### Solution
```python
import math

def smallestDivisor(nums: list[int], threshold: int) -> int:
    def getSum(divisor: int) -> int:
        return sum(math.ceil(num / divisor) for num in nums)

    left, right = 1, max(nums)
    while left < right:
        mid = left + (right - left) // 2
        if getSum(mid) <= threshold:
            right = mid
        else:
            left = mid + 1
    return left
```
- **Time Complexity**: O(n log(max(nums)))
- **Space Complexity**: O(1)

---

## 7. Minimum Time to Complete Trips
[LeetCode 2187](https://leetcode.com/problems/minimum-time-to-complete-trips/)

### Problem Description
You are given an array `time` where `time[i]` denotes the time taken by the `i`-th bus to complete one trip. Each bus can make multiple trips successively. Given an integer `totalTrips`, return the minimum time required for all buses to complete at least `totalTrips` trips.

### Solution
```python
def minimumTime(time: list[int], totalTrips: int) -> int:
    def canComplete(total_time: int) -> bool:
        trips = 0
        for t in time:
            trips += total_time // t
            if trips >= totalTrips:
                return True
        return trips >= totalTrips

    left = 1
    right = min(time) * totalTrips

    while left < right:
        mid = left + (right - left) // 2
        if canComplete(mid):
            right = mid
        else:
            left = mid + 1
    return left
```
- **Time Complexity**: O(n log(min(time) * totalTrips))
- **Space Complexity**: O(1)

---

## 8. Maximum Candies Allocated to K Children
[LeetCode 2226](https://leetcode.com/problems/maximum-candies-allocated-to-k-children/)

### Problem Description
You are given a 0-indexed integer array `candies`, where each element is a pile of candies. You can divide each pile into any number of sub-piles, but you cannot merge two piles. You are also given an integer `k`. You should allocate piles to `k` children such that each child gets the same number of candies. Each child can take at most one pile of candies and some piles of candies may go unused. Return the maximum number of candies each child can get.

### Solution
```python
def maximumCandies(candies: list[int], k: int) -> int:
    def canDistribute(amount: int) -> bool:
        if amount == 0: return True
        count = 0
        for c in candies:
            count += c // amount
            if count >= k:
                return True
        return count >= k

    left, right = 0, sum(candies) // k
    res = 0
    while left <= right:
        mid = left + (right - left) // 2
        if canDistribute(mid):
            res = mid
            left = mid + 1
        else:
            right = mid - 1
    return res
```
- **Time Complexity**: O(n log(max_candies))
- **Space Complexity**: O(1)

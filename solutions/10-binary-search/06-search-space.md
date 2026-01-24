# Practice Problems - Binary Search on Answer Space

## 1. Koko Eating Bananas (LeetCode 875)

### Problem Statement
Koko loves to eat bananas. There are `n` piles of bananas, the `i-th` pile has `piles[i]` bananas. The guards have gone and will come back in `h` hours.
Koko can decide her bananas-per-hour eating speed of `k`. Each hour, she chooses some pile of bananas and eats `k` bananas from that pile. If the pile has less than `k` bananas, she eats all of them instead and will not eat any more bananas during this hour.
Koko likes to eat slowly but still wants to finish eating all the bananas before the guards return.
Return the minimum integer `k` such that she can eat all the bananas within `h` hours.

### Constraints
- `1 <= piles.length <= 10^4`
- `piles.length <= h <= 10^9`
- `1 <= piles[i] <= 10^9`

### Example
**Input:** `piles = [3,6,7,11], h = 8`
**Output:** `4`

### Python Block
```python
import math

def min_eating_speed(piles: list[int], h: int) -> int:
    def can_finish(k: int) -> bool:
        hours = 0
        for pile in piles:
            hours += math.ceil(pile / k)
        return hours <= h

    left, right = 1, max(piles)
    while left < right:
        mid = left + (right - left) // 2
        if can_finish(mid):
            right = mid
        else:
            left = mid + 1
    return left
```

## 2. Capacity To Ship Packages Within D Days (LeetCode 1011)

### Problem Statement
A conveyor belt has packages that must be shipped from one port to another within `days` days.
The `i-th` package on the conveyor belt has a weight of `weights[i]`. Each day, we load the ship with packages on the conveyor belt (in the order given by `weights`). We may not load more weight than the maximum weight capacity of the ship.
Return the least weight capacity of the ship that will result in all the packages on the conveyor belt being shipped within `days` days.

### Constraints
- `1 <= days <= weights.length <= 5 * 10^4`
- `1 <= weights[i] <= 500`

### Example
**Input:** `weights = [1,2,3,4,5,6,7,8,9,10], days = 5`
**Output:** `15`

### Python Block
```python
def ship_within_days(weights: list[int], days: int) -> int:
    def can_ship(capacity: int) -> bool:
        needed_days = 1
        curr_weight = 0
        for w in weights:
            if curr_weight + w > capacity:
                needed_days += 1
                curr_weight = w
            else:
                curr_weight += w
        return needed_days <= days

    left, right = max(weights), sum(weights)
    while left < right:
        mid = left + (right - left) // 2
        if can_ship(mid):
            right = mid
        else:
            left = mid + 1
    return left
```

## 3. Split Array Largest Sum (LeetCode 410)

### Problem Statement
Given an integer array `nums` and an integer `k`, split `nums` into `k` non-empty continuous subarrays such that the largest sum of any subarray is minimized.
Return the minimized largest sum of the split.

### Constraints
- `1 <= nums.length <= 1000`
- `0 <= nums[i] <= 10^6`
- `1 <= k <= min(50, nums.length)`

### Example
**Input:** `nums = [7,2,5,10,8], k = 2`
**Output:** `18`

### Python Block
```python
def split_array(nums: list[int], k: int) -> int:
    def can_split(max_sum: int) -> bool:
        count = 1
        curr_sum = 0
        for n in nums:
            if curr_sum + n > max_sum:
                count += 1
                curr_sum = n
            else:
                curr_sum += n
        return count <= k

    left, right = max(nums), sum(nums)
    while left < right:
        mid = left + (right - left) // 2
        if can_split(mid):
            right = mid
        else:
            left = mid + 1
    return left
```

## 4. Minimize Max Distance to Gas Station (LeetCode 774)

### Problem Statement
You are given an integer array `stations` representing the positions of gas stations on a 1D road and an integer `k`.
You want to add `k` new gas stations. You can add the stations anywhere on the road (not necessarily at integer positions).
Let `penalty` be the maximum distance between adjacent gas stations after adding the `k` new stations.
Return the minimum possible value of `penalty`. Answers within `10^-6` of the actual answer will be accepted.

### Python Block
```python
def min_max_gas_dist(stations: list[int], k: int) -> float:
    def can_achieve(dist: float) -> bool:
        count = 0
        for i in range(len(stations) - 1):
            count += int((stations[i+1] - stations[i]) / dist)
        return count <= k

    left, right = 0, stations[-1] - stations[0]
    while right - left > 1e-6:
        mid = (left + right) / 2
        if can_achieve(mid):
            right = mid
        else:
            left = mid
    return left
```

## 5. Magnetic Force Between Two Balls (LeetCode 1552)

### Problem Statement
In the universe Earth C-137, Rick discovered a special form of magnetic force between two balls. Rick has `n` empty baskets, the `i-th` basket is at `position[i]`, Morty has `m` balls and needs to distribute the balls into the baskets such that the minimum magnetic force between any two balls is maximized.
Rick stated that magnetic force between two balls at positions `x` and `y` is `|x - y|`.
Given the integer array `position` and the integer `m`, return the required force.

### Constraints
- `n == position.length`
- `2 <= n <= 10^5`
- `1 <= position[i] <= 10^9`
- All integers in `position` are distinct.
- `2 <= m <= position.length`

### Example
**Input:** `position = [1,2,3,4,7], m = 3`
**Output:** `3`

### Python Block
```python
def max_distance(position: list[int], m: int) -> int:
    position.sort()

    def can_place(min_dist: int) -> bool:
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
    ans = 1
    while left <= right:
        mid = left + (right - left) // 2
        if can_place(mid):
            ans = mid
            left = mid + 1
        else:
            right = mid - 1
    return ans
```

## 6. Find the Smallest Divisor Given a Threshold (LeetCode 1283)

### Problem Statement
Given an array of integers `nums` and an integer `threshold`, we will choose a positive integer `divisor`, divide all the array by it, and sum the division's result. Foreach element of the array, the result of the division is the smallest integer greater than or equal to that element divided by the divisor (i.e., ceiling of division).
Find the smallest divisor such that the result mentioned above is less than or equal to `threshold`.

### Constraints
- `1 <= nums.length <= 5 * 10^4`
- `1 <= nums[i] <= 10^6`
- `nums.length <= threshold <= 10^6`

### Example
**Input:** `nums = [1,2,5,9], threshold = 6`
**Output:** `5`

### Python Block
```python
import math

def smallest_divisor(nums: list[int], threshold: int) -> int:
    def check(divisor: int) -> bool:
        total = 0
        for n in nums:
            total += math.ceil(n / divisor)
        return total <= threshold

    left, right = 1, max(nums)
    while left < right:
        mid = left + (right - left) // 2
        if check(mid):
            right = mid
        else:
            left = mid + 1
    return left
```

## 7. Minimum Time to Complete Trips (LeetCode 2187)

### Problem Statement
You are given an array `time` where `time[i]` denotes the time taken by the `i-th` bus to complete one trip.
Each bus can make multiple trips successively; that is, the next trip can start immediately after completing the current trip. Also, each bus operates independently; that is, the trips of one bus do not influence the trips of any other bus.
You are also given an integer `totalTrips`, which denotes the number of trips all buses should make in total. Return the minimum time required for all buses to complete at least `totalTrips` trips.

### Constraints
- `1 <= time.length <= 10^5`
- `1 <= time[i], totalTrips <= 10^7`

### Example
**Input:** `time = [1,2,3], totalTrips = 5`
**Output:** `3`

### Python Block
```python
def minimum_time(time: list[int], total_trips: int) -> int:
    def can_complete(t: int) -> bool:
        trips = 0
        for bus_time in time:
            trips += t // bus_time
        return trips >= total_trips

    left = 1
    right = min(time) * total_trips
    while left < right:
        mid = left + (right - left) // 2
        if can_complete(mid):
            right = mid
        else:
            left = mid + 1
    return left
```

## 8. Maximum Candies Allocated to K Children (LeetCode 2226)

### Problem Statement
You are given a **0-indexed** integer array `candies`, where `candies[i]` denotes the number of candies in the `i-th` pile. You are also given an integer `k`. You should allocate piles of candies to `k` children such that each child gets the **same number** of candies. Each child can take at most one pile of candies and some candies of the pile may go unused.
Return the maximum number of candies each child can get.

### Constraints
- `1 <= candies.length <= 10^5`
- `1 <= candies[i] <= 10^7`
- `1 <= k <= 10^12`

### Example
**Input:** `candies = [5,8,6], k = 3`
**Output:** `5`

### Python Block
```python
def maximum_candies(candies: list[int], k: int) -> int:
    def can_allocate(num: int) -> bool:
        if num == 0: return True
        count = 0
        for c in candies:
            count += c // num
        return count >= k

    left, right = 0, sum(candies) // k
    ans = 0
    while left <= right:
        mid = left + (right - left) // 2
        if can_allocate(mid):
            ans = mid
            left = mid + 1
        else:
            right = mid - 1
    return ans
```

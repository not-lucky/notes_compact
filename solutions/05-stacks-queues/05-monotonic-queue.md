# Monotonic Queue - Practice Solutions

This file provides optimal Python solutions and explanations for the practice problems listed in the Monotonic Queue notes.

## 1. Sliding Window Maximum

**Problem Statement**: You are given an array of integers `nums`, there is a sliding window of size `k` which is moving from the very left of the array to the very right. Return the max sliding window.

### Examples & Edge Cases

- **Example 1**: `nums = [1,3,-1,-3,5,3,6,7], k = 3` -> `[3,3,5,5,6,7]`
- **Edge Case**: `k = 1` -> Return `nums`
- **Edge Case**: `k = len(nums)` -> Return `[max(nums)]`

### Optimal Python Solution

```python
from collections import deque

def maxSlidingWindow(nums: list[int], k: int) -> list[int]:
    # Monotonic decreasing deque (stores indices)
    dq = deque()
    result = []

    for i, num in enumerate(nums):
        # 1. Remove indices that are outside the current window
        if dq and dq[0] < i - k + 1:
            dq.popleft()

        # 2. Maintain monotonic property (decreasing)
        # If current num is larger than elements at the back, they can never be max
        while dq and nums[dq[-1]] < num:
            dq.pop()

        dq.append(i)

        # 3. Add to result once window is full
        if i >= k - 1:
            result.append(nums[dq[0]])

    return result
```

### Explanation

We use a `deque` to store indices of elements in the current window. We maintain a "Monotonic Decreasing" property: elements in the deque are ordered from largest to smallest. When a new element comes, we remove all smaller elements from the back because they can never be the maximum of any future window. The front of the deque always contains the index of the maximum element for the current window.

### Complexity Analysis

- **Time Complexity**: O(n), where n is the number of elements. Each index is added and removed from the deque at most once.
- **Space Complexity**: O(k), the deque stores at most k indices.

---

## 2. Shortest Subarray with Sum at Least K

**Problem Statement**: Return the length of the shortest, non-empty, contiguous subarray of `nums` with sum at least `k`. `nums` can contain negative numbers.

### Optimal Python Solution

```python
from collections import deque

def shortestSubarray(nums: list[int], k: int) -> int:
    n = len(nums)
    # Prefix sums array
    prefix_sum = [0] * (n + 1)
    for i in range(n):
        prefix_sum[i+1] = prefix_sum[i] + nums[i]

    res = float('inf')
    # Monotonic increasing deque (stores indices of prefix_sum)
    dq = deque()

    for i, curr_sum in enumerate(prefix_sum):
        # 1. Check if we found a valid subarray
        while dq and curr_sum - prefix_sum[dq[0]] >= k:
            res = min(res, i - dq.popleft())

        # 2. Maintain monotonic increasing property
        # If curr_sum <= previous sum, previous sum is less useful
        while dq and curr_sum <= prefix_sum[dq[-1]]:
            dq.pop()

        dq.append(i)

    return res if res != float('inf') else -1
```

### Complexity Analysis

- **Time Complexity**: O(n), where n is the length of `nums`. We compute prefix sums in O(n) and then perform a single pass where each index is added/removed from the deque at most once.
- **Space Complexity**: O(n), to store prefix sums and the deque.

---

## 3. Jump Game VI

**Problem Statement**: You are at index 0. In each step, you can jump between 1 to `k` steps forward. Each cell has a score. Return the maximum score you can get to reach the last index.

### Optimal Python Solution

````python
from collections import deque

def maxResult(nums: list[int], k: int) -> int:
    n = len(nums)
    # dp[i] = max score to reach index i
    dp = [0] * n
    dp[0] = nums[0]

    # Monotonic decreasing deque of dp values
    dq = deque([0])

    for i in range(1, n):
        # 1. Remove indices outside jump range [i-k, i-1]
        if dq[0] < i - k:
            dq.popleft()

        # 2. Transition: current dp is max of range + current score
        dp[i] = nums[i] + dp[dq[0]]

        # 3. Maintain monotonic property in deque
        while dq and dp[dq[-1]] <= dp[i]:
            dq.pop()
        dq.append(i)

```
### Complexity Analysis
- **Time Complexity**: O(n), where n is the number of elements. We perform a single pass where each element is processed using O(1) deque operations.
- **Space Complexity**: O(k), where k is the jump limit, to store potential candidates in the deque.

### Complexity Analysis
- **Time Complexity**: O(n), one pass through the array.
- **Space Complexity**: O(n) for DP array, O(k) for deque.

---

## 4. Constrained Subsequence Sum
**Problem Statement**: Return the maximum sum of a non-empty subsequence such that for every two consecutive integers in the subsequence, their indices differ by at most `k`.

### Optimal Python Solution
```python
from collections import deque

def constrainedSubsetSum(nums: list[int], k: int) -> int:
    # dp[i] = max sum of subsequence ending at index i
    dq = deque()
    ans = float('-inf')

    for i, num in enumerate(nums):
        # 1. Max value from previous k indices
        max_prev = nums[dq[0]] if dq else 0
        curr = num + max(0, max_prev)
        ans = max(ans, curr)

        # 2. Update dp (reusing nums to save space)
        nums[i] = curr

        # 3. Window expiry
        if dq and dq[0] <= i - k:
            dq.popleft()

        # 4. Monotonic property
        while dq and nums[dq[-1]] <= curr:
            dq.pop()
        dq.append(i)

```
### Complexity Analysis
- **Time Complexity**: O(n), where n is the number of elements. We traverse the array once and perform amortized O(1) work per element using the monotonic queue.
- **Space Complexity**: O(k), where k is the distance limit, to store indices in the deque.

---

## 5. Longest Continuous Subarray With Absolute Diff Less Than or Equal to Limit
**Problem Statement**: Find the length of the longest non-empty subarray such that the absolute difference between any two elements of this subarray is less than or equal to `limit`.

### Optimal Python Solution
```python
from collections import deque

def longestSubarray(nums: list[int], limit: int) -> int:
    max_dq = deque() # monotonic decreasing for max
    min_dq = deque() # monotonic increasing for min
    left = 0
    res = 0

    for right, num in enumerate(nums):
        # Update monotonic queues
        while max_dq and nums[max_dq[-1]] < num: max_dq.pop()
        while min_dq and nums[min_dq[-1]] > num: min_dq.pop()
        max_dq.append(right)
        min_dq.append(right)

        # If limit exceeded, shrink window from left
        while nums[max_dq[0]] - nums[min_dq[0]] > limit:
            if max_dq[0] == left: max_dq.popleft()
            if min_dq[0] == left: min_dq.popleft()
            left += 1

        res = max(res, right - left + 1)

    return res

```
### Complexity Analysis
- **Time Complexity**: O(n), where n is the length of `nums`. We use two pointers (sliding window) and each element is added/removed from each deque at most once.
- **Space Complexity**: O(n), to store indices in the two deques in the worst case.

---

## 6. Max Value of Equation
**Problem Statement**: You are given an array `points` containing the coordinates of points on a 2D plane, sorted by the x-values, where `points[i] = [xi, yi]` such that `xi < xj` for all `1 <= i < j <= points.length`. You are also given an integer `k`. Return the maximum value of the equation `yi + yj + |xi - xj|` where `|xi - xj| <= k` and `1 <= i < j <= points.length`.

### Optimal Python Solution
```python
from collections import deque

def findMaxValueOfEquation(points: list[list[int]], k: int) -> int:
    # Maximize (yi - xi) + (yj + xj) where xj - xi <= k
    # Monotonic queue stores (yi - xi, xi) in decreasing order of (yi - xi)
    dq = deque()
    res = float('-inf')

    for xj, yj in points:
        # 1. Remove points where xj - xi > k
        while dq and xj - dq[0][1] > k:
            dq.popleft()

        # 2. Max value is (yi - xi) + (yj + xj)
        if dq:
            res = max(res, dq[0][0] + yj + xj)

        # 3. Maintain monotonic property for (yi - xi)
        curr_val = yj - xj
        while dq and dq[-1][0] <= curr_val:
            dq.pop()
        dq.append((curr_val, xj))

```
### Complexity Analysis
- **Time Complexity**: O(n), where n is the length of `nums`. We use two pointers (sliding window) and each element is added/removed from each deque at most once.
- **Space Complexity**: O(n), to store indices in the two deques in the worst case.

### Explanation
We rewrite the equation `yi + yj + |xi - xj|` as `(yi - xi) + (yj + xj)` since `xj > xi`. For each point `j`, we want to find a point `i` that maximizes `yi - xi` within the window `xj - xi <= k`. A monotonic queue efficiently maintains the best `yi - xi` candidates.
````

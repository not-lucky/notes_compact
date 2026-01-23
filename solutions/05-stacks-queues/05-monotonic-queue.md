# Solution: Monotonic Queue Practice Problems

## Problem 1: Sliding Window Maximum
### Problem Statement
You are given an array of integers `nums`, there is a sliding window of size `k` which is moving from the very left of the array to the very right. You can only see the `k` numbers in the window. Each time the sliding window moves right by one position.

Return the max sliding window.

### Constraints
- `1 <= nums.length <= 10^5`
- `-10^4 <= nums[i] <= 10^4`
- `1 <= k <= nums.length`

### Example
Input: `nums = [1,3,-1,-3,5,3,6,7], k = 3`
Output: `[3,3,5,5,6,7]`

### Python Implementation
```python
from collections import deque

def maxSlidingWindow(nums: list[int], k: int) -> list[int]:
    """
    Time Complexity: O(n)
    Space Complexity: O(k)
    """
    dq = deque() # indices
    res = []
    for i, num in enumerate(nums):
        # Remove indices outside current window
        while dq and dq[0] < i - k + 1:
            dq.popleft()

        # Remove smaller elements as they can't be the max
        while dq and nums[dq[-1]] < num:
            dq.pop()

        dq.append(i)

        # Append current max to result
        if i >= k - 1:
            res.append(nums[dq[0]])
    return res
```

---

## Problem 2: Shortest Subarray with Sum at Least K
### Problem Statement
Given an integer array `nums` and an integer `k`, return the length of the shortest non-empty subarray of `nums` with a sum of at least `k`. If there is no such subarray, return -1.

### Constraints
- `1 <= nums.length <= 10^5`
- `-10^5 <= nums[i] <= 10^5`
- `1 <= k <= 10^9`

### Example
Input: `nums = [2,-1,2], k = 3`
Output: `3`

### Python Implementation
```python
from collections import deque

def shortestSubarray(nums: list[int], k: int) -> int:
    """
    Time Complexity: O(n)
    Space Complexity: O(n)
    """
    n = len(nums)
    prefix_sum = [0] * (n + 1)
    for i in range(n):
        prefix_sum[i + 1] = prefix_sum[i] + nums[i]

    dq = deque()
    res = float('inf')

    for i in range(n + 1):
        while dq and prefix_sum[i] - prefix_sum[dq[0]] >= k:
            res = min(res, i - dq.popleft())

        while dq and prefix_sum[i] <= prefix_sum[dq[-1]]:
            dq.pop()

        dq.append(i)

    return res if res != float('inf') else -1
```

---

## Problem 3: Jump Game VI
### Problem Statement
You are given a 0-indexed integer array `nums` and an integer `k`.

You are initially standing at index 0. In one move, you can jump at most `k` steps forward without going outside the boundaries of the array. That is, you can jump from index `i` to any index in the range `[i + 1, min(n - 1, i + k)]` inclusive.

You want to reach the last index of the array (index `n - 1`). Your score is the sum of all `nums[j]` for each index `j` you visited in the array.

Return the maximum score you can get.

### Constraints
- `1 <= nums.length, k <= 10^5`
- `-10^4 <= nums[i] <= 10^4`

### Example
Input: `nums = [1,-1,-2,4,-7,3], k = 2`
Output: `7`

### Python Implementation
```python
from collections import deque

def maxResult(nums: list[int], k: int) -> int:
    """
    Time Complexity: O(n)
    Space Complexity: O(k)
    """
    n = len(nums)
    dp = [0] * n
    dp[0] = nums[0]
    dq = deque([0])

    for i in range(1, n):
        # Remove elements out of range k
        while dq and dq[0] < i - k:
            dq.popleft()

        dp[i] = dp[dq[0]] + nums[i]

        # Maintain decreasing order in deque
        while dq and dp[i] >= dp[dq[-1]]:
            dq.pop()

        dq.append(i)

    return dp[-1]
```

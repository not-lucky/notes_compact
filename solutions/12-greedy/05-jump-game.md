# Practice Problems - Jump Game

## 1. Jump Game

### Problem Statement
You are given an integer array `nums`. You are initially positioned at the array's first index, and each element in the array represents your maximum jump length at that position.
Return `true` if you can reach the last index, or `false` otherwise.

### Constraints
- `1 <= nums.length <= 10^4`
- `0 <= nums[i] <= 10^5`

### Example
**Input:** `nums = [2,3,1,1,4]`
**Output:** `true`

### Python Implementation
```python
def canJump(nums: list[int]) -> bool:
    max_reach = 0
    for i, jump in enumerate(nums):
        if i > max_reach: return False
        max_reach = max(max_reach, i + jump)
    return True
```

## 2. Jump Game II

### Problem Statement
You are given a 0-indexed array of integers `nums` of length `n`. You are initially positioned at `nums[0]`.
Each element `nums[i]` represents the maximum length of a forward jump from index `i`. In other words, if you are at `nums[i]`, you can jump to any `nums[i + j]` where `0 <= j <= nums[i]` and `i + j < n`.
Return the minimum number of jumps to reach `nums[n - 1]`. You can assume that you can always reach the last index.

### Constraints
- `1 <= nums.length <= 10^4`
- `0 <= nums[i] <= 1000`

### Example
**Input:** `nums = [2,3,1,1,4]`
**Output:** `2`

### Python Implementation
```python
def jump(nums: list[int]) -> int:
    jumps = 0
    cur_end = 0
    farthest = 0
    for i in range(len(nums) - 1):
        farthest = max(farthest, i + nums[i])
        if i == cur_end:
            jumps += 1
            cur_end = farthest
    return jumps
```

## 3. Jump Game III

### Problem Statement
Given an array of non-negative integers `arr`, you are initially positioned at `start` index of the array. When you are at index `i`, you can jump to `i + arr[i]` or `i - arr[i]`, check if you can reach to any index with value 0.
Notice that you can not jump outside of the array at any time.

### Constraints
- `1 <= arr.length <= 5 * 10^4`
- `0 <= arr[i] < arr.length`
- `0 <= start < arr.length`

### Example
**Input:** `arr = [4,2,3,0,3,1,2], start = 5`
**Output:** `true`

### Python Implementation
```python
from collections import deque

def canReach(arr: list[int], start: int) -> bool:
    queue = deque([start])
    visited = {start}
    while queue:
        i = queue.popleft()
        if arr[i] == 0: return True
        for next_i in [i + arr[i], i - arr[i]]:
            if 0 <= next_i < len(arr) and next_i not in visited:
                visited.add(next_i)
                queue.append(next_i)
    return False
```

## 4. Jump Game IV

### Problem Statement
Given an array of integers `arr`, you are initially positioned at the first index of the array.
In one step you can jump from index `i` to index:
- `i + 1` where `i + 1 < arr.length`.
- `i - 1` where `i - 1 >= 0`.
- `j` where `arr[i] == arr[j]` and `i != j`.
Return the minimum number of steps to reach the last index of the array.

### Constraints
- `1 <= arr.length <= 5 * 10^4`
- `-10^8 <= arr[i] <= 10^8`

### Example
**Input:** `arr = [100,-23,-23,404,100,23,23,23,3,404]`
**Output:** `3`

### Python Implementation
```python
from collections import deque, defaultdict

def minJumps(arr: list[int]) -> int:
    n = len(arr)
    if n <= 1: return 0
    graph = defaultdict(list)
    for i, x in enumerate(arr):
        graph[x].append(i)

    queue = deque([(0, 0)])
    visited = {0}
    while queue:
        i, step = queue.popleft()
        if i == n - 1: return step
        for next_i in [i-1, i+1] + graph[arr[i]]:
            if 0 <= next_i < n and next_i not in visited:
                visited.add(next_i)
                queue.append((next_i, step + 1))
        # Important optimization: clear the same-value list to avoid redundant checks
        del graph[arr[i]]
    return -1
```

## 5. Frog Jump

### Problem Statement
A frog is crossing a river. The river is divided into some number of units, and at each unit, there may or may not be a stone. The frog can jump on a stone, but it must not jump into the water.
Given a list of `stones` positions (in units) in sorted ascending order, determine if the frog can cross the river by landing on the last stone. Initially, the frog is on the first stone and assumes the first jump must be 1 unit.
If the frog's last jump was `k` units, its next jump must be either `k - 1`, `k`, or `k + 1` units. The frog can only jump in the forward direction.

### Constraints
- `2 <= stones.length <= 2000`
- `0 <= stones[i] <= 2^31 - 1`
- `stones[0] == 0`

### Example
**Input:** `stones = [0,1,3,5,6,8,12,17]`
**Output:** `true`

### Python Implementation
```python
def canCross(stones: list[int]) -> bool:
    stone_set = set(stones)
    target = stones[-1]
    dp = {stone: set() for stone in stones}
    dp[0].add(0)

    for s in stones:
        for k in dp[s]:
            for jump in [k-1, k, k+1]:
                if jump > 0:
                    next_s = s + jump
                    if next_s == target: return True
                    if next_s in stone_set:
                        dp[next_s].add(jump)
    return False
```

## 6. Jump Game V

### Problem Statement
Given an array of integers `arr` and an integer `d`. In one step you can jump from index `i` to index `j` such that:
- `i - d <= j <= i + d`.
- `i != j` and `0 <= j < arr.length`.
- `arr[i] > arr[j]` and `arr[i] > arr[k]` for all indices `k` between `i` and `j` (inclusive).
Return the maximum number of indices you can visit.

### Constraints
- `1 <= arr.length <= 1000`
- `1 <= arr[i] <= 10^5`
- `1 <= d <= arr.length`

### Example
**Input:** `arr = [6,4,14,6,8,13,9,7,10,6,12], d = 2`
**Output:** `4`

### Python Implementation
```python
def maxJumps(arr: list[int], d: int) -> int:
    n = len(arr)
    memo = [0] * n

    def dp(i):
        if memo[i]: return memo[i]
        res = 1
        # Check right
        for j in range(i + 1, min(i + d + 1, n)):
            if arr[j] >= arr[i]: break
            res = max(res, 1 + dp(j))
        # Check left
        for j in range(i - 1, max(i - d - 1, -1), -1):
            if arr[j] >= arr[i]: break
            res = max(res, 1 + dp(j))
        memo[i] = res
        return res

    for i in range(n):
        dp(i)
    return max(memo)
```

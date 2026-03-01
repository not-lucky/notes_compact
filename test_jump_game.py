import collections
from typing import List

# Jump Game I
def can_jump(nums: list[int]) -> bool:
    max_reach = 0
    for i, jump_len in enumerate(nums):
        if i > max_reach:
            return False
        max_reach = max(max_reach, i + jump_len)
        if max_reach >= len(nums) - 1:
            return True
    return True

# Jump Game II
def jump(nums: list[int]) -> int:
    n = len(nums)
    if n <= 1:
        return 0
    jumps = 0
    current_end = 0
    farthest = 0
    for i in range(n - 1):
        farthest = max(farthest, i + nums[i])
        if i == current_end:
            jumps += 1
            current_end = farthest
            if current_end >= n - 1:
                break
    return jumps

# Jump Game III
def can_reach(arr: list[int], start: int) -> bool:
    if start < 0 or start >= len(arr) or arr[start] < 0:
        return False
    if arr[start] == 0:
        return True
    jump_dist = arr[start]
    arr[start] = -arr[start]
    return can_reach(arr, start + jump_dist) or can_reach(arr, start - jump_dist)

# Jump Game IV
from collections import defaultdict, deque
def min_jumps(arr: list[int]) -> int:
    n = len(arr)
    if n <= 1:
        return 0
    val_to_indices = defaultdict(list)
    for i, val in enumerate(arr):
        val_to_indices[val].append(i)
    visited = {0}
    queue = deque([0])
    steps = 0
    while queue:
        steps += 1
        for _ in range(len(queue)):
            pos = queue.popleft()
            next_positions = [pos - 1, pos + 1] + val_to_indices[arr[pos]]
            val_to_indices[arr[pos]].clear()
            for next_pos in next_positions:
                if next_pos == n - 1:
                    return steps
                if 0 <= next_pos < n and next_pos not in visited:
                    visited.add(next_pos)
                    queue.append(next_pos)
    return -1

# Jump Game V
from functools import cache
def max_jumps(arr: list[int], d: int) -> int:
    n = len(arr)
    @cache
    def dfs(i: int) -> int:
        res = 1
        for j in range(i - 1, max(i - d - 1, -1), -1):
            if arr[j] >= arr[i]: break
            res = max(res, 1 + dfs(j))
        for j in range(i + 1, min(i + d + 1, n)):
            if arr[j] >= arr[i]: break
            res = max(res, 1 + dfs(j))
        return res
    return max(dfs(i) for i in range(n))

# Jump Game VI
def max_result(nums: list[int], k: int) -> int:
    n = len(nums)
    dp = [0] * n
    dp[0] = nums[0]
    q = deque([0])
    for i in range(1, n):
        while q and q[0] < i - k:
            q.popleft()
        dp[i] = nums[i] + dp[q[0]]
        while q and dp[q[-1]] <= dp[i]:
            q.pop()
        q.append(i)
    return dp[-1]

# Jump Game VII
def can_reach_vii(s: str, minJump: int, maxJump: int) -> bool:
    if s[-1] == '1': return False
    n = len(s)
    q = deque([0])
    farthest_checked = 0
    while q:
        i = q.popleft()
        start = max(i + minJump, farthest_checked + 1)
        end = min(i + maxJump, n - 1)
        for j in range(start, end + 1):
            if s[j] == '0':
                if j == n - 1:
                    return True
                q.append(j)
        farthest_checked = max(farthest_checked, i + maxJump)
    return False

# Frog Jump
def can_cross(stones: list[int]) -> bool:
    if stones[1] != 1:
        return False
    target = stones[-1]
    dp = {stone: set() for stone in stones}
    dp[1].add(1)
    for stone in stones[1:]:
        for k in dp[stone]:
            for next_jump in [k - 1, k, k + 1]:
                if next_jump > 0:
                    next_pos = stone + next_jump
                    if next_pos == target:
                        return True
                    if next_pos in dp:
                        dp[next_pos].add(next_jump)
    return False

def test():
    assert can_jump([2, 3, 1, 1, 4]) == True
    assert can_jump([3, 2, 1, 0, 4]) == False
    assert jump([2, 3, 1, 1, 4]) == 2
    assert can_reach([4, 2, 3, 0, 3, 1, 2], 5) == True
    assert min_jumps([100, -23, -23, 404, 100, 23, 23, 23, 3, 404]) == 3
    assert max_jumps([6,4,14,6,8,13,9,7,10,6,12], 2) == 4
    assert max_result([1,-1,-2,4,-7,3], 2) == 7
    assert can_reach_vii("011010", 2, 3) == True
    assert can_reach_vii("01101110", 2, 3) == False
    assert can_cross([0,1,3,5,6,8,12,17]) == True
    assert can_cross([0,1,2,3,4,8,9,11]) == False
    print("All tests passed!")

test()

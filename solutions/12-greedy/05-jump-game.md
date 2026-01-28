# Solutions: Jump Game

## 1. Jump Game

**Problem Statement**:
You are given an integer array `nums`. You are initially positioned at the array's first index, and each element in the array represents your maximum jump length at that position. Return `true` if you can reach the last index, or `false` otherwise.

**Examples & Edge Cases**:

- **Example 1**:
  - Input: `nums = [2,3,1,1,4]`
  - Output: `true`
  - Explanation: Jump 1 step from index 0 to 1, then 3 steps to the last index.
- **Example 2**:
  - Input: `nums = [3,2,1,0,4]`
  - Output: `false`
  - Explanation: You will always arrive at index 3 no matter what. Its maximum jump length is 0, which makes it impossible to reach the last index.
- **Edge Cases**:
  - Single element: `true` (already at the end).
  - Zeros in the middle: Must be jumpable.

**Optimal Python Solution**:

```python
def canJump(nums: list[int]) -> bool:
    """
    Greedy strategy: Track the farthest position reachable.
    """
    max_reach = 0
    n = len(nums)

    for i in range(n):
        # If current index is beyond our max_reach, we are stuck
        if i > max_reach:
            return False

        # Update max_reach if current position allows a further jump
        max_reach = max(max_reach, i + nums[i])

        # Optimization: If we can already reach the end, return True
        if max_reach >= n - 1:
            return True

    return True
```

**Explanation**:

1.  **Greedy Logic**: At each step `i`, we calculate the farthest point we can possibly reach from here: `i + nums[i]`. We maintain a global `max_reach`.
2.  **Feasibility**: If we ever encounter an index `i` that is greater than our current `max_reach`, it means that index is unreachable from the start.
3.  **Efficiency**: We only need one pass through the array.

**Complexity Analysis**:

- **Time Complexity**: `O(N)`, where `N` is the length of the array.
- **Space Complexity**: `O(1)`, as we only store `max_reach`.

---

## 2. Jump Game II

**Problem Statement**:
Given an array of non-negative integers `nums`, you are initially positioned at the first index of the array. Each element in the array represents your maximum jump length at that position. Your goal is to reach the last index in the minimum number of jumps. (Assume you can always reach the last index).

**Examples & Edge Cases**:

- **Example 1**:
  - Input: `nums = [2,3,1,1,4]`
  - Output: `2`
  - Explanation: The minimum number of jumps to reach the last index is 2. Jump 1 step from index 0 to 1, then 3 steps to the last index.
- **Edge Cases**:
  - Single element: 0 jumps.

**Optimal Python Solution**:

```python
def jump(nums: list[int]) -> int:
    """
    Greedy BFS-like strategy: Find the farthest reach for each jump "level".
    """
    n = len(nums)
    if n <= 1:
        return 0

    jumps = 0
    current_end = 0
    farthest = 0

    # We iterate up to n-1 because we don't need to jump FROM the last element
    for i in range(n - 1):
        # Update the farthest reachable point from the current position
        farthest = max(farthest, i + nums[i])

        # When we reach the end of the current jump's range
        if i == current_end:
            jumps += 1
            current_end = farthest

            # Optimization: If current jump already reaches the end
            if current_end >= n - 1:
                break

    return jumps
```

**Explanation**:

1.  **Thinking in Levels**: Imagine the indices reachable in 1 jump, then 2 jumps, etc.
2.  **Variables**:
    - `farthest`: The absolute farthest index we can reach from any position visited so far.
    - `current_end`: The boundary of the current jump. Once we cross this, we _must_ have made another jump.
3.  **Greedy Step**: We don't care exactly _which_ index we jump to; we just know that for a given jump, we want to pick the next jump point that gives us the maximum future reach.

**Complexity Analysis**:

- **Time Complexity**: `O(N)`.
- **Space Complexity**: `O(1)`.

---

## 3. Jump Game III

**Problem Statement**:
Given an array of non-negative integers `arr` and a `start` index, you can jump to `i + arr[i]` or `i - arr[i]`. Return `true` if you can reach any index with value 0.

**Examples & Edge Cases**:

- **Example 1**:
  - Input: `arr = [4,2,3,0,3,1,2], start = 5`
  - Output: `true`
- **Edge Cases**:
  - Cycles in jumps (infinite loops).
  - `start` is already a 0.

**Optimal Python Solution (BFS)**:

```python
from collections import deque

def canReach(arr: list[int], start: int) -> bool:
    """
    BFS to explore all reachable indices.
    """
    queue = deque([start])
    visited = {start}
    n = len(arr)

    while queue:
        curr = queue.popleft()

        if arr[curr] == 0:
            return True

        # Try jumping forward and backward
        for next_idx in [curr + arr[curr], curr - arr[curr]]:
            if 0 <= next_idx < n and next_idx not in visited:
                visited.add(next_idx)
                queue.append(next_idx)

    return False
```

**Explanation**:

1.  **Exploration**: This is a graph traversal problem (specifically BFS or DFS).
2.  **State**: Each index is a node, and the possible jumps are directed edges.
3.  **Cycle Prevention**: We must use a `visited` set to avoid infinite loops in cycles.

**Complexity Analysis**:

- **Time Complexity**: `O(N)`, as we visit each index at most once.
- **Space Complexity**: `O(N)` for the queue and visited set.

---

## 4. Jump Game IV

**Problem Statement**:
Given an array `arr`, you are at index 0. In one step you can jump to `i+1`, `i-1`, or any `j` where `arr[i] == arr[j]`. Find the minimum steps to reach the last index.

**Optimal Python Solution (Optimized BFS)**:

```python
from collections import deque, defaultdict

def minJumps(arr: list[int]) -> int:
    """
    BFS with an optimization to handle same-value groups.
    """
    n = len(arr)
    if n <= 1:
        return 0

    # Pre-process: group indices by value
    graph = defaultdict(list)
    for i, val in enumerate(arr):
        graph[val].append(i)

    queue = deque([(0, 0)]) # (index, steps)
    visited = {0}

    while queue:
        curr, steps = queue.popleft()

        if curr == n - 1:
            return steps

        # Potential next steps
        neighbors = [curr - 1, curr + 1]
        # Add all indices with same value
        neighbors.extend(graph[arr[curr]])

        # CRUCIAL OPTIMIZATION: Clear the list for this value after visiting once.
        # This prevents redundant O(N) checks for large groups of same values.
        graph[arr[curr]] = []

        for nxt in neighbors:
            if 0 <= nxt < n and nxt not in visited:
                visited.add(nxt)
                queue.append((nxt, steps + 1))

    return -1
```

**Explanation**:

1.  **Value Groups**: The most powerful move is jumping to any other index with the same value.
2.  **The Trap**: If you have 10,000 instances of the value "7", simple BFS will check all 10,000 every time it lands on a "7", leading to `O(N^2)`.
3.  **Optimization**: Once you've processed the group of "7"s, you've added all those indices to the queue. You never need to look at that group again from a different "7". Clearing `graph[arr[curr]]` is the key.

**Complexity Analysis**:

- **Time Complexity**: `O(N)`. Each index is added to the queue once, and each value-group list is processed once.
- **Space Complexity**: `O(N)` for the graph and queue.

---

## 5. Frog Jump

**Problem Statement**:
A frog is crossing a river. The river is divided into units and at each unit there may or may not be a stone. The frog can jump on a stone, but it must not jump into the water. Given a list of `stones` (positions), if the frog's last jump was `k` units, its next jump must be either `k - 1`, `k`, or `k + 1` units. Initially, the frog is on the first stone and assumes the first jump must be 1 unit. Return `true` if the frog can reach the last stone.

**Optimal Python Solution (DP with HashSets)**:

```python
def canCross(stones: list[int]) -> bool:
    """
    DP approach: mapping each stone position to the set of jump sizes
    that can be made FROM that stone.
    """
    # map: stone_position -> {set of jump sizes that reached this stone}
    dp = {stone: set() for stone in stones}
    dp[0].add(0)

    for stone in stones:
        for k in dp[stone]:
            # Try next jumps of k-1, k, k+1
            for step in [k - 1, k, k + 1]:
                if step > 0 and (stone + step) in dp:
                    dp[stone + step].add(step)

    return len(dp[stones[-1]]) > 0
```

**Explanation**:

1.  **State**: We need to know where the frog is AND how big its previous jump was.
2.  **DP Table**: We use a dictionary where keys are stone positions and values are sets of "incoming" jump sizes.
3.  **Transition**: From each stone, look at all the ways we got there (`k`). For each `k`, try jumping `k-1`, `k`, and `k+1`. If we land on a stone, record that jump size in that stone's set.
4.  **Result**: If the last stone has any incoming jump sizes in its set, it's reachable.

**Complexity Analysis**:

- **Time Complexity**: `O(N^2)` in the worst case (though often much faster in practice).
- **Space Complexity**: `O(N^2)` to store jump sizes for each stone.

---

## 6. Jump Game V

**Problem Statement**:
Given an array `arr` and an integer `d`. In one step you can jump from index `i` to index `j` if:

1. `i-d <= j <= i+d` and `i != j`.
2. `arr[i] > arr[j]` and `arr[i] > arr[k]` for all `k` between `i` and `j`.
   Find the maximum number of indices you can visit.

**Optimal Python Solution (Greedy with Memoization/DP)**:

```python
def maxJumps(arr: list[int], d: int) -> int:
    """
    DP with Memoization: The result for an index depends on the results
    of indices it can jump to.
    """
    n = len(arr)
    memo = {}

    def dp(i):
        if i in memo:
            return memo[i]

        res = 1
        # Try jumping right
        for j in range(i + 1, min(i + d + 1, n)):
            if arr[j] >= arr[i]: break
            res = max(res, 1 + dp(j))

        # Try jumping left
        for j in range(i - 1, max(i - d - 1, -1), -1):
            if arr[j] >= arr[i]: break
            res = max(res, 1 + dp(j))

        memo[i] = res
        return res

    return max(dp(i) for i in range(n))
```

**Explanation**:

1.  **Dependency**: This is a DAG (Directed Acyclic Graph) because you can only jump to indices with smaller values.
2.  **Greedy/DP**: For each index, the maximum indices visited is `1 + max(dp(reachable_indices))`.
3.  **Memoization**: We store results to avoid redundant calculations.

**Complexity Analysis**:

- **Time Complexity**: `O(N * D)`.
- **Space Complexity**: `O(N)`.

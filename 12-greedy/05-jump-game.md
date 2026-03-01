# Jump Game

> **Prerequisites:** [Greedy Basics](./01-greedy-basics.md)

## Interview Context

Jump game problems test:

1. **Greedy reachability**: Track farthest position reachable (`max_reach`).
2. **Optimization**: Find minimum jumps by treating jumps like BFS levels.
3. **Pattern recognition**: Knowing when to use Greedy vs. DP vs. BFS vs. Monotonic Queue.
4. **Edge case handling**: Zero jump lengths, already at the end, array modification limits.

---

## Building Intuition

**The "Reach" Concept**

Imagine you're hopping across stones in a river. At each stone, you see how far you CAN jump from there. The key insight:

_You don't need to track WHERE you jump—just HOW FAR you can reach._

```
nums = [2, 3, 1, 1, 4]
        ↑
From index 0, can reach index 0+2=2

But from index 1 (reachable via index 0):
Can reach index 1+3=4 (the end!)

We never explicitly chose "jump from 0 to 1"—we just tracked that
reaching index 4 is possible.
```

**Mental Model: The Expanding Frontier**

Think of your "reachable zone" as water spreading across the array:

```
nums = [2, 3, 1, 1, 4]

Initial:    [X] [ ] [ ] [ ] [ ]  reach=0
After i=0:  [X] [X] [X] [ ] [ ]  reach=2 (can see indices 0,1,2)
After i=1:  [X] [X] [X] [X] [X]  reach=4 (from index 1, jump 3)
                              ↑
                           Reached the end!
```

**Why Greedy Works Here**

The crucial observation: _If you can reach position i, you can reach ALL positions 0 through i_ (since jumps are "up to" `nums[i]`). Reachability is always a contiguous prefix -- there are no gaps. This means only the frontier matters, not the path taken to get there. (See [detailed proof below](#why-greedy-works-for-jump-game).)

**Jump Game II: "Levels" of Jumps**

For minimum jumps, think of it like BFS levels. Each "level" represents positions reachable with exactly that many jumps.

```
nums = [2, 3, 1, 1, 4]

Jump 0 (start): Can see indices 0
Jump 1:         Can see indices 1, 2 (reachable from index 0)
Jump 2:         Can see indices 3, 4 (reachable from indices 1 or 2)
                Index 4 is the end → 2 jumps!

Level 0: [0]
Level 1: [1, 2]
Level 2: [3, 4] ← contains end
```

---

## When NOT to Use the Standard Approach

**1. When Jumps Can Go Backwards**

Jump Game III allows jumping to `i + arr[i]` OR `i - arr[i]`. This breaks the contiguous-frontier property -- positions can be revisited, so use BFS/DFS with a visited set.

**2. When Jumps Have Costs / Specific Values**

If each landing position has a cost, greedy "minimum jumps" might choose an expensive path. Need DP: `dp[i] = maximum/minimum cost to reach index i`.

**3. When You Must Land on Specific Indices**

If only certain indices are valid landing spots (e.g., Frog Jump with stones), the reachable set is sparse, not contiguous. Use DP with state = `(position, last_jump_size)`.

**4. When Jump Sizes Depend on History**

If the next jump size depends on the previous jump (e.g., must be `k-1`, `k`, or `k+1`), the problem requires tracking path history. Greedy only tracks a single frontier, so use DP with state = `(position, last_jump_size)`.

---

## Jump Game I: Can You Reach the End?

### Problem Statement

Given an array where `nums[i]` represents the maximum jump length from position `i`, determine if you can reach the last index.

```
Input:  nums = [2, 3, 1, 1, 4]
Output: true (0 → 1 → 4)

Input:  nums = [3, 2, 1, 0, 4]
Output: false (stuck at index 3)
```

### Solution: Track Maximum Reach

```python
def can_jump(nums: list[int]) -> bool:
    """
    Determine if last index is reachable.

    Greedy: Track the farthest index reachable from positions seen so far.
    If current position > farthest, we're stuck.

    Time: O(n)
    Space: O(1)
    """
    max_reach = 0

    for i, jump_len in enumerate(nums):
        # Check if current position is reachable
        if i > max_reach:
            return False

        # Update the farthest position we can reach from index i
        max_reach = max(max_reach, i + jump_len)

        # Early termination: if we can already reach the end, return True
        if max_reach >= len(nums) - 1:
            return True

    return True
```

### Visual Trace

**Example 1: `nums = [2, 3, 1, 1, 4]`**
```
indices:    0   1   2   3   4
nums:      [2,  3,  1,  1,  4]

i=0: jump_len=2, max_reach = max(0, 0+2) = 2
i=1: 1 <= 2 ✓, jump_len=3, max_reach = max(2, 1+3) = 4 >= 4 → return True

Path: 0 → 1 → 4 (or 0 → 2 → 3 → 4, both work)
```

**Example 2: `nums = [3, 2, 1, 0, 4]`**
```
indices:    0   1   2   3   4
nums:      [3,  2,  1,  0,  4]
              ↘
i=0: jump_len=3, max_reach = max(0, 0+3) = 3  (can reach indices 1,2,3)
i=1: 1 <= 3 ✓, jump_len=2, max_reach = max(3, 1+2) = 3
i=2: 2 <= 3 ✓, jump_len=1, max_reach = max(3, 2+1) = 3
i=3: 3 <= 3 ✓, jump_len=0, max_reach = max(3, 3+0) = 3  (stuck!)
i=4: 4 > 3 ✗ → return False

Problem: Index 3 has value 0, creating a "dead zone" that blocks progress.
```

---

## Jump Game II: Minimum Jumps

### Problem Statement

Given the same setup, find the **minimum number of jumps** to reach the last index. Assume you can always reach the end.

```
Input:  nums = [2, 3, 1, 1, 4]
Output: 2 (0 → 1 → 4)
```

### Solution: Greedy Range Expansion

```python
def jump(nums: list[int]) -> int:
    """
    Find minimum jumps to reach last index.

    Greedy: Implicitly performs BFS by tracking level boundaries.
    - current_end: right boundary of the current BFS level
    - farthest: right boundary of the next BFS level
    - When i reaches current_end, we've exhausted this level → jump

    Time: O(n)
    Space: O(1)
    """
    n = len(nums)
    if n <= 1:
        return 0

    jumps = 0
    current_end = 0    # Right boundary of current BFS level
    farthest = 0       # Farthest reachable from any position in current level

    for i in range(n - 1):  # Stop before last index since we only need to reach it
        farthest = max(farthest, i + nums[i])

        if i == current_end:
            # Exhausted all positions in this level -- must take another jump
            jumps += 1
            current_end = farthest

            # Early exit: if we can already reach the last index
            if current_end >= n - 1:
                break

    return jumps
```

### BFS Alternative (Conceptual)

The greedy solution above is essentially an optimized BFS. Here's the explicit BFS to show the connection -- each "level" represents positions reachable in exactly that many jumps. The greedy version avoids the queue and visited set by exploiting the contiguous-range property.

```python
from collections import deque

def jump_bfs(nums: list[int]) -> int:
    """
    BFS approach: level = number of jumps.

    Note: Jump Game II guarantees the end is reachable.

    Time: O(n^2) worst case if tracking visited loosely -- greedy avoids this.
    Space: O(n)
    """
    n = len(nums)
    if n <= 1:
        return 0

    queue = deque([0])
    visited = {0}
    jumps = 0

    while queue:
        jumps += 1
        for _ in range(len(queue)):
            pos = queue.popleft()
            for next_pos in range(pos + 1, min(pos + nums[pos] + 1, n)):
                if next_pos == n - 1:
                    return jumps
                if next_pos not in visited:
                    visited.add(next_pos)
                    queue.append(next_pos)

    return -1
```

---

## Why Greedy Works for Jump Game

### Jump Game I: Reachability

**Greedy choice**: At each reachable position, update the maximum reach.

**Why it works** (exchange argument):
- Jumps go "up to" `nums[i]` positions forward, so if position `i` is reachable, every position in `0..i` is also reachable.
- Therefore, reachability is always a contiguous prefix `[0..max_reach]` -- there are never gaps.
- No "better path" exists to consider -- any path that reaches position `i` yields the same set of reachable indices from `i`, so greedy never misses anything.

### Jump Game II: Minimum Jumps

**Greedy choice**: At each "level" (set of positions reachable in exactly `k` jumps), find the farthest position reachable. That becomes the boundary of the next level.

**Why it works**:
- This is implicit BFS: each level boundary corresponds to exactly one jump.
- Expanding the next level's boundary as far as possible can only help or be neutral -- it never excludes positions that a narrower boundary would include.

---

## Jump Game III: Can Reach Zero

**Different pattern** -- uses BFS or DFS, not greedy.

### Problem Statement

Given a non-negative array `arr` and a starting index, you can jump to `i + arr[i]` or `i - arr[i]`. Determine if you can reach any index with value 0.

```
Input:  arr = [4, 2, 3, 0, 3, 1, 2], start = 5
Output: true (5 → 4 → 1 → 3)
```

### Solution: DFS with O(1) Space

Interviewers love the in-place marking optimization to save `O(N)` auxiliary space for a `visited` set. If modifying the array is strictly prohibited by the interviewer, use a standard `visited = set([start])`.

```python
def can_reach(arr: list[int], start: int) -> bool:
    """
    DFS approach with O(1) auxiliary space (ignoring recursion stack).
    We mark visited elements by making them negative.

    Time: O(n)
    Space: O(n) worst-case recursion stack
    """
    # Base cases: out of bounds or already visited (negative)
    if start < 0 or start >= len(arr) or arr[start] < 0:
        return False

    # Found the target
    if arr[start] == 0:
        return True

    # Mark current index as visited
    jump_dist = arr[start]
    arr[start] = -arr[start]

    # Explore both directions
    return can_reach(arr, start + jump_dist) or can_reach(arr, start - jump_dist)
```

---

## Jump Game IV: Minimum Jumps with Same Values

### Problem Statement

From index `i`, you can jump to `i+1`, `i-1`, or any index `j` where `arr[i] == arr[j]`. Find the minimum number of jumps from index 0 to the last index.

```
Input:  arr = [100, -23, -23, 404, 100, 23, 23, 23, 3, 404]
Output: 3 (0 → 4 → 3 → 9, using same-value jump 100→100, then -1, then same-value 404→404)
```

### Solution: BFS with Optimization

```python
from collections import defaultdict, deque

def min_jumps(arr: list[int]) -> int:
    """
    BFS with same-value jumps.

    Key optimization: after processing a value group, clear it from the map.
    Without this, indices with the same value get re-enumerated at every BFS
    level that touches them, leading to O(n^2) total work. Clearing ensures
    each value group is iterated exactly once across the entire BFS.

    Time: O(n)
    Space: O(n)
    """
    n = len(arr)
    if n <= 1:
        return 0

    # Build value -> indices mapping for O(1) same-value teleportation
    val_to_indices: dict[int, list[int]] = defaultdict(list)
    for i, val in enumerate(arr):
        val_to_indices[val].append(i)

    visited = {0}
    queue = deque([0])
    steps = 0

    while queue:
        steps += 1
        for _ in range(len(queue)):
            pos = queue.popleft()

            # Next positions: left neighbor, right neighbor, and same-value teleports
            next_positions = [pos - 1, pos + 1] + val_to_indices[arr[pos]]

            # Critical: clear the group to ensure each value is processed only once
            # Keeps the algorithm O(n) instead of O(n^2)
            val_to_indices[arr[pos]].clear()

            for next_pos in next_positions:
                if next_pos == n - 1:
                    return steps
                if 0 <= next_pos < n and next_pos not in visited:
                    visited.add(next_pos)
                    queue.append(next_pos)

    return -1
```

---

## Jump Game V: Maximum Score (Constraint Jumps)

### Problem Statement

Given an array `arr` and a maximum jump distance `d`, you can jump from index `i` to `i + x` or `i - x` (where `1 <= x <= d`).

**Constraint**: You can only jump to index `j` if `arr[j] < arr[i]` AND all intermediate elements between `i` and `j` are also strictly smaller than `arr[i]`.

Find the maximum score (number of indices visited) starting from any index. 

### Solution: Top-Down DP with Memoization

```python
from functools import cache

def max_jumps(arr: list[int], d: int) -> int:
    """
    Top-Down DP with Memoization.
    
    The constraint that we can only jump to strictly smaller elements
    guarantees that our jumps form a Directed Acyclic Graph (DAG).
    Top-down memoization cleanly resolves the evaluation order.

    Time: O(n * d) - each state computed once, d transitions per state
    Space: O(n) - recursion stack and memo cache
    """
    n = len(arr)

    @cache
    def dfs(i: int) -> int:
        res = 1  # Can always visit self (length 1 path)
        
        # Check left jumps
        for j in range(i - 1, max(i - d - 1, -1), -1):
            if arr[j] >= arr[i]:
                break  # Blocked by a larger or equal element
            res = max(res, 1 + dfs(j))
            
        # Check right jumps
        for j in range(i + 1, min(i + d + 1, n)):
            if arr[j] >= arr[i]:
                break  # Blocked by a larger or equal element
            res = max(res, 1 + dfs(j))
            
        return res

    # Start from any index, find the global maximum
    return max(dfs(i) for i in range(n))
```

*Note: You can also solve this Bottom-Up by explicitly sorting the indices by their values in ascending order, computing DP on the smallest values first. But the top-down approach is usually faster to write and less prone to DAG-ordering errors in interviews.*

---

## Jump Game VI: Max Score with Monotonic Queue (LC 1696)

### Problem Statement
Given a 0-indexed integer array `nums` and an integer `k`, you can jump at most `k` steps forward. Find the **maximum score** (sum of visited elements) to reach the last index.

```
Input: nums = [1,-1,-2,4,-7,3], k = 2
Output: 7 (Path: 1 -> -1 -> 4 -> 3)
```

### Solution: DP + Monotonic Queue

Standard DP formulation would be `dp[i] = nums[i] + max(dp[i-k] ... dp[i-1])`, yielding O(N * k) time. We can optimize this to **O(N)** by maintaining the sliding window maximum of the DP array using a monotonic decreasing queue!

```python
from collections import deque

def max_result(nums: list[int], k: int) -> int:
    """
    DP + Monotonic Decreasing Queue optimization.
    The queue efficiently stores the max DP value in our jump window of size k.

    Time: O(n)
    Space: O(n) for the dp array and queue
    """
    n = len(nums)
    if n == 0:
        return 0

    dp = [0] * n
    dp[0] = nums[0]

    # Queue stores indices, keeping dp values strictly monotonically decreasing
    q = deque([0])

    for i in range(1, n):
        # 1. Remove indices that are outside the window of size k
        if q and q[0] < i - k:
            q.popleft()

        # 2. The max element in the window is at the front of the queue
        dp[i] = nums[i] + dp[q[0]]

        # 3. Maintain monotonic decreasing property:
        # pop smaller values because they'll never be the max if dp[i] is larger
        while q and dp[q[-1]] <= dp[i]:
            q.pop()

        q.append(i)

    return dp[-1]
```

This is a **critical pattern** bridging Dynamic Programming with Sliding Window techniques.

---

## Jump Game VII: Reachable Zeros with Min/Max Jump (LC 1871)

### Problem Statement

Given a 0-indexed binary string `s` and two integers `minJump` and `maxJump`, determine if you can reach the last index. You start at index `0` (which is always `'0'`).
You can jump from `i` to `j` if:
- `i + minJump <= j <= min(i + maxJump, len(s) - 1)`
- `s[j] == '0'`

```text
Input: s = "011010", minJump = 2, maxJump = 3
Output: true (0 -> 3 -> 5)
```

### Solution: BFS with Range Optimization

A naive BFS iterates through all possible next jumps `[i + minJump, i + maxJump]`, but overlapping intervals lead to `O(N * maxJump)` which is `O(N^2)` worst-case (Time Limit Exceeded). 
To optimize, we track the `farthest_checked` index we have evaluated to avoid re-adding or re-checking the same intervals.

```python
from collections import deque

def can_reach_vii(s: str, minJump: int, maxJump: int) -> bool:
    """
    Optimized BFS. We track `farthest_checked` to avoid iterating over
    the same indices multiple times.

    Time: O(n) - each index is checked at most once
    Space: O(n) - queue can store up to n indices
    """
    n = len(s)
    if n == 0 or s[-1] == '1':
        return False

    q = deque([0])
    farthest_checked = 0

    while q:
        i = q.popleft()

        # The range we can jump to from index i
        # We start checking from farthest_checked + 1 to avoid duplicate work
        start = max(i + minJump, farthest_checked + 1)
        end = min(i + maxJump, n - 1)

        for j in range(start, end + 1):
            if s[j] == '0':
                if j == n - 1:
                    return True
                q.append(j)

        # Update farthest checked so we don't scan overlapping intervals again
        farthest_checked = max(farthest_checked, i + maxJump)

    return False
```

---

## Frog Jump (LeetCode 403)

### Problem Statement

A frog is crossing a river. The river is divided into some number of units, and at each unit, there may or may not exist a stone. The frog can jump on a stone, but it must not jump into the water.

Given a list of `stones` positions (in units) in sorted strictly increasing order, determine if the frog can cross the river by landing on the last stone. Initially, the frog is on the first stone and assumes the first jump must be `1` unit.

If the frog's last jump was `k` units, its next jump must be either `k - 1`, `k`, or `k + 1` units. The frog can only jump in the forward direction.

```text
Input: stones = [0,1,3,5,6,8,12,17]
Output: true
Explanation: The frog can jump to the last stone by jumping 1 unit to the 2nd stone, then 2 units to the 3rd stone, then 2 units to the 4th stone, then 3 units to the 6th stone, 4 units to the 7th stone, and 5 units to the 8th stone.
```

### Solution: DP with HashSet

```python
def can_cross(stones: list[int]) -> bool:
    """
    State: for each stone, track which jump sizes can land on it.
    Transition: from stone s with jump size k, try jumps of k-1, k, k+1.

    Time: O(n^2) -- each stone can accumulate up to n jump sizes
    Space: O(n^2)
    """
    n = len(stones)
    if n <= 1:
        return True

    # The first jump must be exactly 1 unit
    if stones[1] != 1:
        return False

    target = stones[-1]

    # dp[stone] = set of valid previous jump sizes that reached this stone
    dp = {stone: set() for stone in stones}
    dp[1].add(1) # We landed on stone 1 with a jump of size 1

    # Note: Iterating through the list `stones` directly ensures we
    # process stones safely in increasing positional order.
    # Start from index 1 since index 0 is already processed
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
```

---

## Jump Game Variant Comparison

| Variant | Approach | Time | Space | Key Insight |
|---------|----------|------|-------|-------------|
| I (can reach?) | Greedy | O(n) | O(1) | Track max reach (`max_reach = max(max_reach, i + nums[i])`) |
| II (min jumps) | Greedy | O(n) | O(1) | BFS-like levels tracking `farthest` and `current_end` |
| III (reach zero) | DFS/BFS | O(n) | O(n) | Bidirectional jumps. Use in-place array mutation (`-nums[i]`) |
| IV (same values) | BFS | O(n) | O(n) | Map values to indices; MUST `clear()` visited groups to avoid O(n²) |
| V (max path) | Top-Down DP | O(nd) | O(n) | Constraints create a DAG. Use recursion + memoization |
| VI (max score win) | DP + MonoQ | O(n) | O(n) | Use a monotonic queue to find sliding window maximum in O(1) |
| VII (min/max range) | BFS + Opt | O(n) | O(n) | Avoid re-processing sliding intervals using `farthest_checked` |

---

## Edge Cases

- **Array length 1**: Already at end, return true (I), 0 (II), or `nums[0]` (VI).
- **First element 0**: Can't move anywhere (except if n=1, already at end).
- **Large jumps**: Handled correctly — `max_reach >= len(nums) - 1` short-circuits without out-of-bounds issues.
- **Negative values**: Standard Jump Game I/II/III arrays are non-negative. Jump Game VI specifically uses negative values to force careful DP optimization.

---

## Practice Problems

| # | Problem | Difficulty | Key Insight |
|---|---------|------------|-------------|
| 1 | [Jump Game](https://leetcode.com/problems/jump-game/) (LC 55) | Medium | Track max reach |
| 2 | [Jump Game II](https://leetcode.com/problems/jump-game-ii/) (LC 45) | Medium | Greedy level expansion |
| 3 | [Jump Game III](https://leetcode.com/problems/jump-game-iii/) (LC 1306) | Medium | DFS/BFS bidirectional, O(1) space mod |
| 4 | [Jump Game IV](https://leetcode.com/problems/jump-game-iv/) (LC 1345) | Hard | BFS with group clearing |
| 5 | [Jump Game V](https://leetcode.com/problems/jump-game-v/) (LC 1340) | Hard | Top-down DP for DAG ordering |
| 6 | [Jump Game VI](https://leetcode.com/problems/jump-game-vi/) (LC 1696) | Medium | DP + Monotonic Queue optimization |
| 7 | [Jump Game VII](https://leetcode.com/problems/jump-game-vii/) (LC 1871) | Medium | BFS with `farthest_checked` optimization |
| 8 | [Frog Jump](https://leetcode.com/problems/frog-jump/) (LC 403) | Hard | DP with dynamic jump sizes state |

---

## Interview Tips

1. **Identify the variant**: Can reach? Min jumps? Bidirectional? Constraints? Value scores?
2. **Choose right approach**:
   - Greedy for I/II (forward-only, contiguous reachability)
   - BFS/DFS for III/IV (bidirectional or teleportation)
   - DP for V/VI and Frog Jump (score aggregation or history-dependent constraints)
3. **Trace through example**: Show `max_reach` updates for Jump Game I, `current_end`/`farthest` for Jump Game II.
4. **Know the DP optimization**: Jump Game VI explicitly targets your ability to optimize an O(N*K) DP equation into O(N) using sliding window monotonic queues!
5. **Jump Game V insight**: Recursion solves the topological DAG order easily!

---

## Key Takeaways

1. **Greedy works when**: jumps are forward-only and reachable positions form a contiguous range.
2. **Jump Game I**: Track maximum reachable index. Reachability is a contiguous prefix, so a single variable suffices.
3. **Jump Game II**: Implicit BFS via greedy. Count "levels" using `current_end` as the level boundary, `farthest` as the next boundary.
4. **Bidirectional jumps** (III) -- DFS with in-place visited set marking (make element negative).
5. **Same-value jumps** (IV) -- BFS with `.clear()` to avoid O(n²) re-processing of value groups.
6. **DP + Monotonic Queue** (VI) -- Huge pattern: when DP needs max/min over a sliding window, a deque gives O(1) lookups.
7. **Range Jumps** (VII) -- BFS with `farthest_checked` to avoid re-adding intervals.

---

## Next: [06-gas-station.md](./06-gas-station.md)

Learn the gas station problem - circular greedy with clever insight.

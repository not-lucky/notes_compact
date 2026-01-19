# Jump Game

> **Prerequisites:** [Greedy Basics](./01-greedy-basics.md)

## Interview Context

Jump game problems test:
1. **Greedy reachability**: Track farthest position reachable
2. **Optimization**: Find minimum jumps
3. **Pattern recognition**: When greedy vs DP vs BFS
4. **Edge case handling**: Zero jumps, already at end

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

    for i, jump in enumerate(nums):
        if i > max_reach:
            # Can't reach this position
            return False
        max_reach = max(max_reach, i + jump)
        if max_reach >= len(nums) - 1:
            return True

    return True
```

### Visual Trace

```
nums = [2, 3, 1, 1, 4]
indices: 0  1  2  3  4

i=0: jump=2, max_reach = max(0, 0+2) = 2
i=1: 1 <= 2 ✓, jump=3, max_reach = max(2, 1+3) = 4 >= 4 → return True

nums = [3, 2, 1, 0, 4]
indices: 0  1  2  3  4

i=0: jump=3, max_reach = max(0, 0+3) = 3
i=1: 1 <= 3 ✓, jump=2, max_reach = max(3, 1+2) = 3
i=2: 2 <= 3 ✓, jump=1, max_reach = max(3, 2+1) = 3
i=3: 3 <= 3 ✓, jump=0, max_reach = max(3, 3+0) = 3
i=4: 4 > 3 → return False
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

    Greedy: Jump to position that maximizes next reach.
    Track: current range end, farthest reachable, jump count.

    Time: O(n)
    Space: O(1)
    """
    n = len(nums)
    if n <= 1:
        return 0

    jumps = 0
    current_end = 0    # End of current jump range
    farthest = 0       # Farthest we can reach

    for i in range(n - 1):  # Don't need to jump from last position
        farthest = max(farthest, i + nums[i])

        if i == current_end:
            # Must jump now - reached end of current range
            jumps += 1
            current_end = farthest

            if current_end >= n - 1:
                break

    return jumps
```

### Visual Trace

```
nums = [2, 3, 1, 1, 4]
indices: 0  1  2  3  4

Initial: jumps=0, current_end=0, farthest=0

i=0: farthest = max(0, 0+2) = 2
     i == current_end → jump! jumps=1, current_end=2

i=1: farthest = max(2, 1+3) = 4
     i != current_end

i=2: farthest = max(4, 2+1) = 4
     i == current_end → jump! jumps=2, current_end=4
     current_end >= 4 → break

Answer: 2
```

### BFS Alternative

```python
from collections import deque

def jump_bfs(nums: list[int]) -> int:
    """
    BFS approach: level = number of jumps.

    Time: O(n)
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

    return -1  # Can't reach
```

---

## Why Greedy Works for Jump Game

### Jump Game I: Reachability

**Greedy choice**: Always track maximum reach from all visited positions.

**Why it works**:
- If we can reach position `i`, we can reach all positions `0..i`
- Maximum reach from `0..i` determines if `i+1` is reachable
- No need to track which specific path was taken

### Jump Game II: Minimum Jumps

**Greedy choice**: At each "level", jump to maximize next level's reach.

**Why it works**:
- BFS-like level expansion
- Each level = one jump
- Jumping to farthest reach minimizes total jumps

---

## Jump Game III: Can Reach Zero

**Different pattern** - uses BFS, not greedy.

### Problem Statement

You can jump to `i + arr[i]` or `i - arr[i]`. Can you reach any index with value 0?

```
Input:  arr = [4, 2, 3, 0, 3, 1, 2], start = 5
Output: true (5 → 4 → 1 → 3)
```

### Solution: BFS

```python
from collections import deque

def can_reach(arr: list[int], start: int) -> bool:
    """
    BFS to check if any 0-valued index is reachable.

    Time: O(n)
    Space: O(n)
    """
    n = len(arr)
    visited = set()
    queue = deque([start])

    while queue:
        pos = queue.popleft()

        if arr[pos] == 0:
            return True

        if pos in visited:
            continue
        visited.add(pos)

        # Try both directions
        for next_pos in [pos + arr[pos], pos - arr[pos]]:
            if 0 <= next_pos < n and next_pos not in visited:
                queue.append(next_pos)

    return False
```

---

## Jump Game IV: Minimum Jumps with Same Values

### Problem Statement

Jump to `i+1`, `i-1`, or any index `j` where `arr[i] == arr[j]`. Find minimum jumps to reach end.

```
Input:  arr = [100, -23, -23, 404, 100, 23, 23, 23, 3, 404]
Output: 3
```

### Solution: BFS with Optimization

```python
from collections import defaultdict, deque

def min_jumps(arr: list[int]) -> int:
    """
    BFS with same-value jumps.
    Key optimization: clear value's indices after first visit.

    Time: O(n)
    Space: O(n)
    """
    n = len(arr)
    if n <= 1:
        return 0

    # Build value → indices mapping
    value_indices = defaultdict(list)
    for i, val in enumerate(arr):
        value_indices[val].append(i)

    visited = {0}
    queue = deque([0])
    steps = 0

    while queue:
        steps += 1
        for _ in range(len(queue)):
            pos = queue.popleft()

            # Next positions: neighbors + same values
            next_positions = [pos - 1, pos + 1]
            next_positions.extend(value_indices[arr[pos]])
            # Clear to avoid re-visiting same-value group
            value_indices[arr[pos]] = []

            for next_pos in next_positions:
                if next_pos == n - 1:
                    return steps
                if 0 <= next_pos < n and next_pos not in visited:
                    visited.add(next_pos)
                    queue.append(next_pos)

    return -1
```

---

## Jump Game Variant Comparison

| Variant | Approach | Time | Key Insight |
|---------|----------|------|-------------|
| I (can reach?) | Greedy | O(n) | Track max reach |
| II (min jumps) | Greedy | O(n) | BFS-like levels |
| III (reach zero) | BFS | O(n) | Bidirectional jumps |
| IV (same values) | BFS | O(n) | Clear visited groups |
| V (max score) | DP | O(n log n) | Monotonic deque |

---

## Frog Jump (LeetCode 403)

A frog crosses a river by jumping on stones. Different pattern - uses DP.

```python
def can_cross(stones: list[int]) -> bool:
    """
    Frog must land on stones only.
    If last jump was k, next can be k-1, k, or k+1.

    Time: O(n²)
    Space: O(n²)
    """
    stone_set = set(stones)
    target = stones[-1]

    # memo[position] = set of valid jump sizes to reach this position
    memo = {stone: set() for stone in stones}
    memo[0].add(0)  # Starting position with jump size 0

    for stone in stones:
        for k in memo[stone]:
            for next_jump in [k - 1, k, k + 1]:
                if next_jump > 0:
                    next_pos = stone + next_jump
                    if next_pos in stone_set:
                        if next_pos == target:
                            return True
                        memo[next_pos].add(next_jump)

    return False
```

---

## Complexity Analysis

| Problem | Time | Space | Approach |
|---------|------|-------|----------|
| Jump Game I | O(n) | O(1) | Greedy |
| Jump Game II | O(n) | O(1) | Greedy |
| Jump Game III | O(n) | O(n) | BFS |
| Jump Game IV | O(n) | O(n) | BFS |
| Frog Jump | O(n²) | O(n²) | DP |

---

## Edge Cases

- [ ] Array length 1 → already at end, return true/0
- [ ] First element 0 → can't move (except if n=1)
- [ ] All zeros except first → check reachability
- [ ] Large jumps → should still work, track max reach
- [ ] Negative values → only in specific variants

---

## Practice Problems

| # | Problem | Difficulty | Key Insight |
|---|---------|------------|-------------|
| 1 | Jump Game | Medium | Track max reach |
| 2 | Jump Game II | Medium | Greedy level expansion |
| 3 | Jump Game III | Medium | BFS bidirectional |
| 4 | Jump Game IV | Hard | BFS with optimization |
| 5 | Frog Jump | Hard | DP with jump sizes |
| 6 | Jump Game V | Hard | DP with monotonic stack |

---

## Interview Tips

1. **Identify the variant**: Can reach? Min jumps? Bidirectional?
2. **Choose right approach**: Greedy for I/II, BFS for III/IV
3. **Trace through example**: Show max reach updates
4. **Handle edge cases**: Single element, zero at start
5. **Know the optimization**: Jump IV needs to clear value groups

---

## Key Takeaways

1. Jump Game I: track maximum reachable position
2. Jump Game II: BFS-like greedy, count "levels"
3. Bidirectional jumps → use BFS instead of greedy
4. Same-value jumps → BFS with group clearing
5. Greedy works when forward-only and optimal substructure exists

---

## Next: [06-gas-station.md](./06-gas-station.md)

Learn the gas station problem - circular greedy with clever insight.

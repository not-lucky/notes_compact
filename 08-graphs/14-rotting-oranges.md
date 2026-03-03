# Rotting Oranges (Multi-Source BFS)

> **Prerequisites:** [02-bfs-basics](./02-bfs-basics.md), [13-grid-problems](./13-grid-problems.md)

## Interview Context

Rotting Oranges is a FANG+ classic because:

1. **Multi-source BFS**: Multiple starting points expand simultaneously
2. **Time/level tracking**: Return minimum time, not just reachability
3. **Real-world analogy**: Spreading fire, infection, signal propagation
4. **Clean problem statement**: Easy to understand, tricky to implement correctly

This problem appears frequently at Amazon, Meta, and Google.

### FANG Context: The Quintessential Amazon Grid Problem

This is arguably the most recognizable "Amazon Grid Problem." Amazon heavily favors 2D grid matrix problems because they test graph traversal without the need to parse complex graph representations (like adjacency lists). If you interview at Amazon, you are highly likely to encounter a variation of this problem (e.g., zombie matrix, package delivery times, server cluster updates). Expect follow-ups about scaling to massive grids where the matrix doesn't fit in memory (requiring chunking or Spark/Hadoop-style map-reduce approaches) or sparse matrices.

---

## Why BFS, Not DFS?

This is a critical interview talking point. Many candidates instinctively reach for DFS because it's simpler to write recursively, but DFS is **wrong** for this problem:

1. **Simultaneous spreading**: Rotting happens from *all* rotten oranges at the same time, level by level. BFS naturally models this wave-like, layer-by-layer expansion. DFS would explore one deep path before backtracking, which doesn't model simultaneous spreading.

2. **Minimum time guarantee**: BFS guarantees that the first time you reach a cell is via the shortest path. DFS may reach a cell via a longer path first, then revisit it via a shorter path — but if you've already marked it visited, you'll record the wrong time. You'd need to revisit cells to correct this, destroying the time complexity.

3. **Time = BFS depth**: Each BFS level corresponds to exactly one minute. This 1:1 mapping between BFS levels and time steps is what makes BFS natural here. DFS has no concept of "levels."

**Analogy**: Think of dropping a stone in water — the ripple expands outward uniformly (BFS). DFS would be like a single stream of water snaking through the grid in one direction before backing up.

---

## Theory Deep Dive: Multi-Source vs Single-Source BFS

In a standard BFS, you start at a single node and expand outwards layer by layer. The time taken to reach a node is its shortest path distance from that single source.

But what if you want the shortest distance to a set of targets, starting from *any* of multiple sources?
If you run single-source BFS from each source independently, the time complexity becomes `O(K × (V+E))` where `K` is the number of sources. In a grid, this degrades to `O((R×C)²)` in the worst case (e.g., half the grid is rotten oranges, half is fresh).

**Multi-source BFS** solves this elegantly by pushing *all* sources into the queue at distance 0 before starting the loop.
You can think of it in two ways:
1. **The "Super Source" concept**: Imagine a dummy node "Super Source" connected to all your starting nodes with directed edges of weight 0. A standard BFS from this Super Source is mathematically equivalent to multi-source BFS.
2. **Parallel wave propagation**: Like dropping multiple stones in a pond simultaneously. The ripples expand together, and a point is covered by whichever ripple reaches it first.

Because the queue only ever contains nodes at distance `d` and `d+1` (monotonicity), the first time you visit a node, it is guaranteed to be via the shortest possible path from *any* source. This keeps the time complexity strictly `O(V+E)` regardless of the number of sources.

---

## Problem Statement

In a grid:

- `0` = empty cell
- `1` = fresh orange
- `2` = rotten orange

Every minute, fresh oranges adjacent (4-directionally) to rotten ones become rotten.
Return the minimum minutes until no fresh oranges remain, or `-1` if impossible.

```
Example:
[[2,1,1],     After 1 min:    After 2 min:    After 3 min:    After 4 min:
 [1,1,0],     [[2,2,1],       [[2,2,2],       [[2,2,2],       [[2,2,2],
 [0,1,1]]      [2,1,0],        [2,2,0],        [2,2,0],        [2,2,0],
               [0,1,1]]        [0,2,1]]        [0,2,2]]        [0,2,2]]

Answer: 4 minutes
```

---

## Multi-Source BFS Solution

### Approach 1: Time Stored Per Cell

Each queue entry carries its own timestamp. Simple and avoids the level-loop pattern.

```python
from collections import deque

def oranges_rotting(grid: list[list[int]]) -> int:
    """
    Find minimum time for all oranges to rot using multi-source BFS.

    Each queue entry stores (row, col, time) so we track time per cell.

    Time:  O(rows × cols) — every cell visited at most once
    Space: O(rows × cols) — queue can hold all cells in worst case
    """
    rows, cols = len(grid), len(grid[0])
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    # Phase 1: Seed the queue with ALL rotten oranges at time 0
    queue: deque[tuple[int, int, int]] = deque()
    fresh_count = 0

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 2:
                queue.append((r, c, 0))  # (row, col, time)
            elif grid[r][c] == 1:
                fresh_count += 1

    # Edge case: no fresh oranges — nothing to rot
    if fresh_count == 0:
        return 0

    max_time = 0

    # Phase 2: BFS — expand the rot wave
    while queue:
        r, c, time = queue.popleft()

        for dr, dc in directions:
            nr, nc = r + dr, c + dc

            if (0 <= nr < rows and 0 <= nc < cols
                    and grid[nr][nc] == 1):
                grid[nr][nc] = 2       # Mark as rotten (acts as "visited")
                fresh_count -= 1
                max_time = time + 1    # Track latest time any orange rotted
                queue.append((nr, nc, time + 1))

    # If fresh oranges remain, some were unreachable
    return max_time if fresh_count == 0 else -1
```

### Approach 2: Level-by-Level BFS

Process the entire queue level at once. Each full pass through the level = one minute.
This pattern is useful when you need to process all nodes at the same distance together.

```python
from collections import deque

def oranges_rotting_level(grid: list[list[int]]) -> int:
    """
    Multi-source BFS with explicit level-by-level processing.

    Instead of tracking time per cell, we process all cells at the same
    BFS depth in one loop iteration — each iteration = one minute.

    Time:  O(rows × cols)
    Space: O(rows × cols)
    """
    rows, cols = len(grid), len(grid[0])
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    queue: deque[tuple[int, int]] = deque()
    fresh_count = 0

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 2:
                queue.append((r, c))
            elif grid[r][c] == 1:
                fresh_count += 1

    if fresh_count == 0:
        return 0

    minutes = 0

    while queue:
        # Process ALL oranges rotted at the current time step
        level_size = len(queue)

        for _ in range(level_size):
            r, c = queue.popleft()

            for dr, dc in directions:
                nr, nc = r + dr, c + dc

                if (0 <= nr < rows and 0 <= nc < cols
                        and grid[nr][nc] == 1):
                    grid[nr][nc] = 2
                    fresh_count -= 1
                    queue.append((nr, nc))

        # Only count a minute if new oranges were actually rotted
        if queue:
            minutes += 1

    return minutes if fresh_count == 0 else -1
```

**Which approach to use in interviews?** Both are correct. Approach 1 is slightly simpler to reason about. Approach 2 generalizes better to problems that need to process all nodes at the same depth together (e.g., binary tree level-order traversal). Know both.

---

## Visual Walkthrough

```
Initial state:              Queue (row, col, time): [(0,0,0)]
[[2,1,1],                   fresh_count = 6
 [1,1,0],
 [0,1,1]]

────────────────────────────────────────────────────

Time 0: Process (0,0,0)
        Rot neighbors → (0,1) and (1,0)
        Queue: [(0,1,1), (1,0,1)]
        Grid:
        [[2, 2, 1],
         [2, 1, 0],
         [0, 1, 1]]
        fresh_count = 4

────────────────────────────────────────────────────

Time 1: Process (0,1,1) and (1,0,1)
        From (0,1): rot (0,2) and (1,1)
        From (1,0): (1,1) already rotten — skip
        Queue: [(0,2,2), (1,1,2)]
        Grid:
        [[2, 2, 2],
         [2, 2, 0],
         [0, 1, 1]]
        fresh_count = 2

────────────────────────────────────────────────────

Time 2: Process (0,2,2) and (1,1,2)
        From (0,2): no fresh neighbors
        From (1,1): rot (2,1)
        Queue: [(2,1,3)]
        Grid:
        [[2, 2, 2],
         [2, 2, 0],
         [0, 2, 1]]
        fresh_count = 1

────────────────────────────────────────────────────

Time 3: Process (2,1,3)
        Rot (2,2)
        Queue: [(2,2,4)]
        Grid:
        [[2, 2, 2],
         [2, 2, 0],
         [0, 2, 2]]
        fresh_count = 0

────────────────────────────────────────────────────

Time 4: Process (2,2,4)
        No fresh neighbors
        Queue: empty
        fresh_count == 0 → return max_time = 4
```

---

## Edge Cases

```python
# 1. No fresh oranges → nothing to rot
[[0, 2]]
# Return 0

# 2. No rotten oranges but fresh exist → impossible to start rotting
[[1, 1]]
# Return -1

# 3. Unreachable fresh orange (blocked by empty cell)
[[2, 1, 0, 1]]
# Return -1 (rightmost 1 is isolated by the 0)

# 4. All already rotten
[[2, 2], [2, 2]]
# Return 0

# 5. Single fresh cell, no rotten → impossible
[[1]]
# Return -1

# 6. Single rotten cell, no fresh → already done
[[2]]
# Return 0

# 7. Empty grid (all zeros) → no fresh oranges
[[0, 0], [0, 0]]
# Return 0
```

---

## Common Mistakes

```python
# ❌ MISTAKE 1: Running independent BFS from each rotten orange
# This processes them sequentially — later BFS runs may revisit cells
# with incorrect (longer) times, and the total cost is O(K × R × C).
for r in range(rows):
    for c in range(cols):
        if grid[r][c] == 2:
            bfs(r, c)  # Sequential, not simultaneous!

# ✅ CORRECT: Add ALL rotten oranges to queue first, then run ONE BFS
for r in range(rows):
    for c in range(cols):
        if grid[r][c] == 2:
            queue.append((r, c))
# ... then run BFS loop once


# ❌ MISTAKE 2: Incrementing time for each neighbor
for dr, dc in directions:
    ...
    queue.append((nr, nc))
    minutes += 1  # Wrong! Multiple neighbors rot in the SAME minute

# ✅ CORRECT: Track time per cell, or use level-by-level processing


# ❌ MISTAKE 3: Forgetting to check if all fresh oranges were reached
# Without this check, you might return a time even though some fresh
# oranges were unreachable (isolated by empty cells).
return max_time  # Might be wrong if fresh_count > 0!

# ✅ CORRECT: Verify all fresh oranges were rotted
return max_time if fresh_count == 0 else -1


# ❌ MISTAKE 4: Using DFS instead of BFS
# DFS doesn't model simultaneous spreading — it explores one full path
# before backtracking, giving incorrect minimum times.
```

---

## Related: 01 Matrix (LC 542)

Find distance to nearest 0 for each cell. Same multi-source BFS pattern — seed all 0-cells as sources.

```python
from collections import deque

def update_matrix(mat: list[list[int]]) -> list[list[int]]:
    """
    For each cell, find distance to nearest 0 using multi-source BFS.

    Time:  O(rows × cols)
    Space: O(rows × cols)
    """
    rows, cols = len(mat), len(mat[0])
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    # Seed BFS with all 0-cells at distance 0
    queue: deque[tuple[int, int]] = deque()
    # Use -1 to represent unvisited cells
    dist = [[-1] * cols for _ in range(rows)]

    for r in range(rows):
        for c in range(cols):
            if mat[r][c] == 0:
                dist[r][c] = 0
                queue.append((r, c))

    # BFS: expand outward from all 0-cells simultaneously
    while queue:
        r, c = queue.popleft()

        for dr, dc in directions:
            nr, nc = r + dr, c + dc

            # Since it's BFS, the first time we visit a cell, it's the shortest path
            if 0 <= nr < rows and 0 <= nc < cols and dist[nr][nc] == -1:
                dist[nr][nc] = dist[r][c] + 1
                queue.append((nr, nc))

    return dist
```

---

## Related: Walls and Gates (LC 286)

```python
from collections import deque

def walls_and_gates(rooms: list[list[int]]) -> None:
    """
    Fill distance to nearest gate for each empty room. Modify in-place.
    -1 = wall, 0 = gate, INF = empty room.

    Time:  O(rows × cols)
    Space: O(rows × cols)
    """
    if not rooms:
        return

    rows, cols = len(rooms), len(rooms[0])
    INF = 2147483647
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    # Seed BFS with all gates
    queue: deque[tuple[int, int]] = deque()

    for r in range(rows):
        for c in range(cols):
            if rooms[r][c] == 0:  # Gate
                queue.append((r, c))

    while queue:
        r, c = queue.popleft()

        for dr, dc in directions:
            nr, nc = r + dr, c + dc

            if (0 <= nr < rows and 0 <= nc < cols
                    and rooms[nr][nc] == INF):
                rooms[nr][nc] = rooms[r][c] + 1
                queue.append((nr, nc))
```

---

## Related: Shortest Bridge (LC 934)

```python
from collections import deque

def shortest_bridge(grid: list[list[int]]) -> int:
    """
    Find shortest bridge (number of 0-cells to flip) between two islands.

    Strategy:
    1. Find first island with BFS (or DFS), mark it as 2, add its cells to queue.
    2. Multi-source BFS from the entire first island to find second island.

    Time:  O(n²)
    Space: O(n²)
    """
    n = len(grid)
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    # Phase 1: Find and mark first island using BFS
    # (BFS is preferred over recursive DFS in Python to avoid recursion depth limits)
    queue: deque[tuple[int, int, int]] = deque()
    
    def find_first_island() -> None:
        for r in range(n):
            for c in range(n):
                if grid[r][c] == 1:
                    # Found first island cell, run BFS to mark it entirely
                    grid[r][c] = 2
                    queue.append((r, c, 0))
                    
                    island_q = deque([(r, c)])
                    while island_q:
                        curr_r, curr_c = island_q.popleft()
                        for dr, dc in directions:
                            nr, nc = curr_r + dr, curr_c + dc
                            if 0 <= nr < n and 0 <= nc < n and grid[nr][nc] == 1:
                                grid[nr][nc] = 2
                                queue.append((nr, nc, 0))
                                island_q.append((nr, nc))
                    return

    find_first_island()

    # Phase 2: BFS from first island to find second island
    while queue:
        r, c, dist = queue.popleft()

        for dr, dc in directions:
            nr, nc = r + dr, c + dc

            if 0 <= nr < n and 0 <= nc < n:
                if grid[nr][nc] == 1:
                    return dist       # Reached second island
                if grid[nr][nc] == 0:
                    grid[nr][nc] = 2  # Mark water as visited
                    queue.append((nr, nc, dist + 1))

    return -1  # Should not reach here if input is valid
```

---

## Complexity Analysis

| Operation    | Time           | Space          |
| ------------ | -------------- | -------------- |
| Initial scan | O(rows × cols) | O(1)           |
| BFS          | O(rows × cols) | O(rows × cols) |
| **Total**    | O(rows × cols) | O(rows × cols) |

### Deep Dive

**Time Complexity**: Let $N = \text{rows} \times \text{cols}$.
- In a standard graph, BFS takes $O(V + E)$. Our grid is an implicit graph where $V = N$ and $E \le 4N$ (each cell has at most 4 neighbors). So $O(V + E) = O(5N) = O(N)$.
- The initial scan to find all rotten oranges takes $O(N)$.
- In the BFS phase, each fresh orange is enqueued at most once and dequeued at most once. For each dequeued cell, we check at most 4 neighbors — constant work per cell.
- Total: $O(N)$ regardless of how many rotten oranges we start with.

**Space Complexity**:
- The BFS queue is the dominant space cost.
- **Worst case**: All cells are rotten initially → queue holds $O(N)$ elements at the start. Or in a large grid, the BFS wavefront can hold $O(\min(R, C))$ elements at a time in practice, but $O(N)$ in the degenerate case.
- We modify the grid in-place (changing `1` → `2` acts as our "visited" set). If the input is immutable, we'd need an $O(N)$ visited set — same asymptotic space.

---

## Interview Tips

1. **Identify multi-source**: Multiple starting points = add all to queue before starting
2. **Track time correctly**: Either per-cell timestamps or level-by-level processing
3. **Count reachability**: Track `fresh_count` and verify it reaches 0 at the end
4. **Handle edge cases first**: No fresh oranges → return 0. No rotten oranges + fresh exist → return -1
5. **Explain BFS choice**: "BFS models simultaneous expansion; each level = one time step. DFS can't model simultaneous spreading and doesn't guarantee minimum time."
6. **Mention in-place trade-off**: We mutate the grid to avoid a visited set. Discuss with interviewer if this is acceptable.

---

## Practice Problems

| #   | Problem                                 | LC # | Difficulty | Key Concept                 | Hint                                                                 |
| --- | --------------------------------------- | ---- | ---------- | --------------------------- | -------------------------------------------------------------------- |
| 1   | Rotting Oranges                         | 994  | Medium     | Multi-source BFS, time      | Seed all rotten oranges at t=0, BFS level = 1 minute                 |
| 2   | 01 Matrix                               | 542  | Medium     | Multi-source BFS, distance  | Seed all 0-cells, BFS outward to fill distances                      |
| 3   | Walls and Gates                         | 286  | Medium     | Multi-source BFS, in-place  | Identical pattern to 01 Matrix but with walls blocking               |
| 4   | Shortest Bridge                         | 934  | Medium     | DFS + multi-source BFS      | DFS to find island 1, BFS from its entire boundary to reach island 2 |
| 5   | As Far from Land as Possible            | 1162 | Medium     | Multi-source BFS, max dist  | Seed all land cells, BFS to find farthest water cell                 |
| 6   | Map of Highest Peak                     | 1765 | Medium     | Multi-source BFS, elevation | Seed all water cells at height 0, BFS outward incrementing height    |
| 7   | Shortest Path in Binary Matrix          | 1091 | Medium     | Single-source BFS, 8-dir    | Standard BFS but with 8 directions instead of 4                      |
| 8   | Number of Islands                       | 200  | Medium     | BFS/DFS on grid             | Foundational grid traversal — practice before this problem           |
| 9   | Pacific Atlantic Water Flow             | 417  | Medium     | Multi-source BFS/DFS        | Start from ocean borders and flow uphill to find reachable cells     |

**Suggested progression**: 8 → 1 → 2 → 3 → 5 → 6 → 4 → 9 → 7

---

## Key Takeaways

1. **Multi-source BFS**: Add all sources to queue before starting — they all begin at distance 0
2. **Simultaneous expansion**: Equivalent to adding a "super source" node connected to all start points
3. **Level = time step**: Each BFS level corresponds to one unit of time
4. **Verify reachability**: Always check if all targets were reached (fresh_count == 0)
5. **Same complexity**: Still O(V + E) even with multiple sources — each cell is visited at most once
6. **BFS, not DFS**: DFS cannot model simultaneous spreading and doesn't guarantee minimum time

---

## Next: [15-word-ladder.md](./15-word-ladder.md)

Learn implicit graph problems with Word Ladder.

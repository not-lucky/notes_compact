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

## Theory Deep Dive: Multi-Source vs Single-Source BFS

In a standard BFS, you start at a single node and expand outwards layer by layer. The time taken to reach a node is its shortest path distance from that single source.

But what if you want the shortest distance to a set of targets, starting from *any* of multiple sources?
If you run single-source BFS from each source independently, the time complexity becomes `O(K × (V+E))` where `K` is the number of sources. In a grid, this degrades to `O((R×C)²)` in the worst case (e.g., half the grid is rotten oranges, half is fresh).

**Multi-source BFS** solves this elegantly by pushing *all* sources into the queue at distance 0 before starting the loop.
You can think of it in two ways mathematically:
1. **The "Super Source" concept**: Imagine a dummy node "Super Source" connected to all your starting nodes with directed edges of weight 0. A standard BFS from this Super Source is mathematically equivalent to multi-source BFS.
2. **Parallel wave propagation**: Like dropping multiple stones in a pond simultaneously. The ripples expand together, and a point is covered by whichever ripple reaches it first.

Because the queue only ever contains nodes at distance `d` and `d+1` (monotonicity), the first time you visit a node, it is guaranteed to be via the shortest possible path from *any* source. This keeps the time complexity strictly `O(V+E)` regardless of the number of sources.

---

## Problem Statement

In a grid:

- `0` = empty cell
- `1` = fresh orange
- `2` = rotten orange

Every minute, fresh oranges adjacent to rotten ones become rotten.
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

```python
from collections import deque

def oranges_rotting(grid: list[list[int]]) -> int:
    """
    Find minimum time for all oranges to rot.

    Time: O(rows × cols)
    Space: O(rows × cols)

    Key insight: Start BFS from ALL rotten oranges simultaneously.
    """
    rows, cols = len(grid), len(grid[0])
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    # Initialize queue with all rotten oranges
    queue = deque()
    fresh_count = 0

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 2:
                queue.append((r, c, 0))  # (row, col, time)
            elif grid[r][c] == 1:
                fresh_count += 1

    # Edge case: no fresh oranges
    if fresh_count == 0:
        return 0

    max_time = 0

    while queue:
        r, c, time = queue.popleft()

        for dr, dc in directions:
            nr, nc = r + dr, c + dc

            if (0 <= nr < rows and 0 <= nc < cols and
                grid[nr][nc] == 1):
                grid[nr][nc] = 2  # Mark as rotten
                fresh_count -= 1
                max_time = time + 1
                queue.append((nr, nc, time + 1))

    return max_time if fresh_count == 0 else -1
```

```python
from collections import deque

def oranges_rotting_level(grid: list[list[int]]) -> int:
    """
    Multi-source BFS with explicit level tracking.
    """
    rows, cols = len(grid), len(grid[0])
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    queue = deque()
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
        # Process all oranges at current time step
        level_size = len(queue)

        for _ in range(level_size):
            r, c = queue.popleft()

            for dr, dc in directions:
                nr, nc = r + dr, c + dc

                if (0 <= nr < rows and 0 <= nc < cols and
                    grid[nr][nc] == 1):
                    grid[nr][nc] = 2
                    fresh_count -= 1
                    queue.append((nr, nc))

        if queue:  # Only increment if more work to do
            minutes += 1

    return minutes if fresh_count == 0 else -1
```

---

## Visual Walkthrough

```
Initial:                Queue: [(0,0)]
[[2,1,1],               fresh = 6
 [1,1,0],
 [0,1,1]]

Time 0: Process (0,0)
        Rot neighbors: (0,1), (1,0)
        Queue: [(0,1,1), (1,0,1)]
        Grid after:
        [[2,2,1],
         [2,1,0],
         [0,1,1]]
        fresh = 4

Time 1: Process (0,1), (1,0)
        From (0,1): rot (0,2), (1,1)
        From (1,0): (1,1) already being rotted
        Queue: [(0,2,2), (1,1,2)]
        Grid after:
        [[2,2,2],
         [2,2,0],
         [0,1,1]]
        fresh = 2

Time 2: Process (0,2), (1,1)
        From (0,2): no fresh neighbors
        From (1,1): rot (2,1)
        Queue: [(2,1,3)]
        Grid after:
        [[2,2,2],
         [2,2,0],
         [0,2,1]]
        fresh = 1

Time 3: Process (2,1)
        Rot (2,2)
        Queue: [(2,2,4)]
        fresh = 0

Time 4: All rotten!
        Return 4
```

---

## Related: 01 Matrix

Find distance to nearest 0 for each cell.

```python
from collections import deque

def update_matrix(mat: list[list[int]]) -> list[list[int]]:
    """
    For each cell, find distance to nearest 0.

    Time: O(rows × cols)
    Space: O(rows × cols)
    """
    rows, cols = len(mat), len(mat[0])
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    # Multi-source BFS from all 0s
    queue = deque()
    dist = [[float('inf')] * cols for _ in range(rows)]

    for r in range(rows):
        for c in range(cols):
            if mat[r][c] == 0:
                dist[r][c] = 0
                queue.append((r, c))

    while queue:
        r, c = queue.popleft()

        for dr, dc in directions:
            nr, nc = r + dr, c + dc

            if (0 <= nr < rows and 0 <= nc < cols and
                dist[nr][nc] > dist[r][c] + 1):
                dist[nr][nc] = dist[r][c] + 1
                queue.append((nr, nc))

    return dist
```

---

## Related: Walls and Gates

```python
from collections import deque

def walls_and_gates(rooms: list[list[int]]) -> None:
    """
    Fill distance to nearest gate for each empty room.
    -1 = wall, 0 = gate, INF = empty room

    Modify in-place.

    Time: O(rows × cols)
    Space: O(rows × cols)
    """
    if not rooms:
        return

    rows, cols = len(rooms), len(rooms[0])
    INF = 2147483647
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    # Multi-source BFS from all gates
    queue = deque()

    for r in range(rows):
        for c in range(cols):
            if rooms[r][c] == 0:  # Gate
                queue.append((r, c))

    while queue:
        r, c = queue.popleft()

        for dr, dc in directions:
            nr, nc = r + dr, c + dc

            if (0 <= nr < rows and 0 <= nc < cols and
                rooms[nr][nc] == INF):
                rooms[nr][nc] = rooms[r][c] + 1
                queue.append((nr, nc))
```

---

## Related: Shortest Bridge

```python
from collections import deque

def shortest_bridge(grid: list[list[int]]) -> int:
    """
    Find shortest path between two islands.

    Time: O(n²)
    Space: O(n²)

    Strategy: Find first island with DFS, expand from it with BFS.
    """
    n = len(grid)
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    # Find first island
    queue = deque()
    found = False

    def dfs(r, c):
        if (r < 0 or r >= n or c < 0 or c >= n or grid[r][c] != 1):
            return
        grid[r][c] = 2  # Mark as visited (first island)
        queue.append((r, c, 0))

        dfs(r + 1, c)
        dfs(r - 1, c)
        dfs(r, c + 1)
        dfs(r, c - 1)

    for r in range(n):
        if found:
            break
        for c in range(n):
            if grid[r][c] == 1:
                dfs(r, c)
                found = True
                break

    # BFS from first island to find second
    while queue:
        r, c, dist = queue.popleft()

        for dr, dc in directions:
            nr, nc = r + dr, c + dc

            if 0 <= nr < n and 0 <= nc < n:
                if grid[nr][nc] == 1:
                    return dist  # Found second island

                if grid[nr][nc] == 0:
                    grid[nr][nc] = 2  # Mark as visited
                    queue.append((nr, nc, dist + 1))

    return -1
```

---

## Edge Cases

```python
# 1. No fresh oranges
[[0, 2]]
# Return 0 (nothing to rot)

# 2. No rotten oranges, but fresh exist
[[1, 1]]
# Return -1 (can't rot any)

# 3. Unreachable fresh orange
[[2, 1, 0, 1]]
# Return -1 (rightmost 1 unreachable)

# 4. All rotten already
[[2, 2], [2, 2]]
# Return 0

# 5. Single cell with fresh
[[1]]
# Return -1

# 6. Single cell with rotten
[[2]]
# Return 0
```

---

## Common Mistakes

```python
# WRONG: Starting from single source
for r in range(rows):
    for c in range(cols):
        if grid[r][c] == 2:
            bfs(r, c)  # Only processes first rotten!

# CORRECT: Add ALL rotten to queue first
for r in range(rows):
    for c in range(cols):
        if grid[r][c] == 2:
            queue.append((r, c))


# WRONG: Incrementing time inside loop
for dr, dc in directions:
    ...
    queue.append((nr, nc))
    minutes += 1  # Wrong! Multiple neighbors in same minute

# CORRECT: Track time per cell or use level-by-level


# WRONG: Not counting initial fresh
# May return 0 when there are unreachable fresh oranges

# CORRECT: Count fresh and verify it reaches 0
fresh_count = sum(row.count(1) for row in grid)
# ... after BFS ...
return time if fresh_count == 0 else -1
```

---

## Complexity Analysis

| Operation    | Time           | Space          |
| ------------ | -------------- | -------------- |
| Initial scan | O(rows × cols) | O(rows × cols) |
| BFS          | O(rows × cols) | O(rows × cols) |
| Total        | O(rows × cols) | O(rows × cols) |

### Deep Dive into Complexity

**Time Complexity**: Let $N = \text{rows} \times \text{cols}$.
- **Graph vs Grid Representation**: In a standard graph, BFS takes $O(V + E)$. Here, our grid represents an implicit graph.
- The number of vertices $V = N$.
- The number of edges $E$ is at most $4N$ (since each cell has at most 4 neighbors).
- So, $O(V + E) = O(N + 4N) = O(N)$.
- The initial scan to find all rotten oranges takes exactly $O(N)$.
- In the BFS phase, each fresh orange is added to the queue at most once and popped at most once. For each popped orange, we check 4 adjacent cells. This means we process each cell a constant number of times.
- Therefore, the total time complexity is strictly bounded by $O(N)$ or $O(rows \times cols)$.

**Space Complexity**:
- The only extra space we use (besides a few variables) is the BFS `queue`.
- **Worst-Case Space Scenario**: What is the maximum number of items in the queue at any given time?
- Consider a scenario where all edge cells of the grid are rotten and the inner cells are fresh. Or consider a worst-case dense graph scenario where the grid is filled with rotten oranges initially. The queue would instantly take $O(N)$ space.
- Another worst-case scenario is a checkerboard pattern of rotten and fresh oranges. However, the true max queue size for a BFS wave spreading in a 2D grid is bounded by the perimeter of the "wavefront", which scales with the grid's dimensions, but in the absolute worst case (e.g., completely filled with rotten oranges at the start), the queue stores $O(N)$ elements.
- We do an in-place modification of the `grid` (changing `1` to `2`). If the input matrix was immutable (e.g., read-only or we are forbidden from modifying it), we would need an auxiliary $O(N)$ `visited` set or matrix, doubling the space footprint but keeping it asymptotically $O(N)$.

---

## Interview Tips

1. **Identify multi-source**: Multiple starting points = add all to queue
2. **Track time correctly**: Either per-cell or level-by-level
3. **Count reachability**: Track if all targets were reached
4. **Handle edge cases**: No sources, no targets, unreachable targets
5. **Explain BFS choice**: Simultaneous expansion gives minimum time

---

## Practice Problems

| #   | Problem                      | Difficulty | Key Variation       |
| --- | ---------------------------- | ---------- | ------------------- |
| 1   | Rotting Oranges              | Medium     | Core problem        |
| 2   | 01 Matrix                    | Medium     | Distance to 0       |
| 3   | Walls and Gates              | Medium     | Distance to gate    |
| 4   | Shortest Bridge              | Medium     | Two islands         |
| 5   | As Far from Land as Possible | Medium     | Max distance        |
| 6   | Map of Highest Peak          | Medium     | Distance from water |

---

## Key Takeaways

1. **Multi-source BFS**: Add all sources to queue before starting
2. **Simultaneous expansion**: All sources at distance 0
3. **Level tracking**: For minimum time problems
4. **Verify reachability**: Count targets reached
5. **Same complexity**: Still O(V + E) even with multiple sources

---

## Next: [15-word-ladder.md](./15-word-ladder.md)

Learn implicit graph problems with Word Ladder.

# Rotting Oranges (Multi-Source BFS)

> **Prerequisites:** [02-bfs-basics](./02-bfs-basics.md), [13-grid-problems](./13-grid-problems.md)

## Interview Context

Rotting Oranges is a FANG+ classic because:

1. **Multi-source BFS**: Multiple starting points expand simultaneously
2. **Time/level tracking**: Return minimum time, not just reachability
3. **Real-world analogy**: Spreading fire, infection, signal propagation
4. **Clean problem statement**: Easy to understand, tricky to implement correctly

This problem appears frequently at Amazon, Meta, and Google.

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

---

## Level-by-Level BFS Alternative

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

| Operation | Time | Space |
|-----------|------|-------|
| Initial scan | O(rows × cols) | O(rows × cols) |
| BFS | O(rows × cols) | O(rows × cols) |
| Total | O(rows × cols) | O(rows × cols) |

Each cell is visited at most once.

---

## Interview Tips

1. **Identify multi-source**: Multiple starting points = add all to queue
2. **Track time correctly**: Either per-cell or level-by-level
3. **Count reachability**: Track if all targets were reached
4. **Handle edge cases**: No sources, no targets, unreachable targets
5. **Explain BFS choice**: Simultaneous expansion gives minimum time

---

## Practice Problems

| # | Problem | Difficulty | Key Variation |
|---|---------|------------|---------------|
| 1 | Rotting Oranges | Medium | Core problem |
| 2 | 01 Matrix | Medium | Distance to 0 |
| 3 | Walls and Gates | Medium | Distance to gate |
| 4 | Shortest Bridge | Medium | Two islands |
| 5 | As Far from Land as Possible | Medium | Max distance |
| 6 | Map of Highest Peak | Medium | Distance from water |

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

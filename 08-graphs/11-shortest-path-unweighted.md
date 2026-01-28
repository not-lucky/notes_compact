# Shortest Path in Unweighted Graphs

> **Prerequisites:** [02-bfs-basics](./02-bfs-basics.md)

## Interview Context

BFS for shortest path is fundamental because:

1. **Optimal for unweighted**: O(V + E) is the best we can do
2. **Foundation for other algorithms**: Dijkstra extends this concept
3. **Very common in interviews**: Grid shortest paths, word ladders
4. **Simpler than Dijkstra**: No heap needed

When all edges have equal weight, BFS is the answer.

---

## Core Concept

In an unweighted graph (or where all edges have the same weight), **BFS guarantees shortest path** because it explores vertices level by level.

```
Graph:              BFS from 0:
    0 --- 1         Level 0: 0 (dist 0)
    |     |         Level 1: 1, 2 (dist 1)
    2 --- 3         Level 2: 3 (dist 2)

Shortest path 0→3: 0→1→3 or 0→2→3, both length 2
```

---

## BFS Shortest Path Template

```python
from collections import deque

def shortest_path_bfs(graph: dict[int, list[int]],
                       start: int, end: int) -> int:
    """
    Find shortest path in unweighted graph.

    Time: O(V + E)
    Space: O(V)

    Returns -1 if no path exists.
    """
    if start == end:
        return 0

    visited = set([start])
    queue = deque([(start, 0)])  # (node, distance)

    while queue:
        node, dist = queue.popleft()

        for neighbor in graph[node]:
            if neighbor == end:
                return dist + 1

            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, dist + 1))

    return -1
```

---

## Grid Shortest Path

```python
from collections import deque

def shortest_path_grid(grid: list[list[int]],
                        start: tuple[int, int],
                        end: tuple[int, int]) -> int:
    """
    Shortest path in a grid (0 = passable, 1 = blocked).

    Time: O(rows × cols)
    Space: O(rows × cols)
    """
    if grid[start[0]][start[1]] == 1 or grid[end[0]][end[1]] == 1:
        return -1

    if start == end:
        return 0

    rows, cols = len(grid), len(grid[0])
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    visited = set([start])
    queue = deque([(start[0], start[1], 0)])  # (row, col, distance)

    while queue:
        r, c, dist = queue.popleft()

        for dr, dc in directions:
            nr, nc = r + dr, c + dc

            if (nr, nc) == end:
                return dist + 1

            if (0 <= nr < rows and 0 <= nc < cols and
                (nr, nc) not in visited and grid[nr][nc] == 0):
                visited.add((nr, nc))
                queue.append((nr, nc, dist + 1))

    return -1
```

---

## Shortest Path in Binary Matrix (8 Directions)

```python
from collections import deque

def shortest_path_binary_matrix(grid: list[list[int]]) -> int:
    """
    Shortest path from (0,0) to (n-1,n-1) with 8-directional movement.
    0 = passable, 1 = blocked.

    Time: O(n²)
    Space: O(n²)
    """
    n = len(grid)

    if grid[0][0] == 1 or grid[n-1][n-1] == 1:
        return -1

    if n == 1:
        return 1

    # 8 directions including diagonals
    directions = [
        (0, 1), (0, -1), (1, 0), (-1, 0),
        (1, 1), (1, -1), (-1, 1), (-1, -1)
    ]

    visited = set([(0, 0)])
    queue = deque([(0, 0, 1)])  # (row, col, path_length)

    while queue:
        r, c, length = queue.popleft()

        for dr, dc in directions:
            nr, nc = r + dr, c + dc

            if nr == n - 1 and nc == n - 1:
                return length + 1

            if (0 <= nr < n and 0 <= nc < n and
                (nr, nc) not in visited and grid[nr][nc] == 0):
                visited.add((nr, nc))
                queue.append((nr, nc, length + 1))

    return -1
```

---

## All Shortest Paths

```python
from collections import deque, defaultdict

def all_shortest_paths(graph: dict[int, list[int]],
                        start: int, end: int) -> list[list[int]]:
    """
    Find ALL shortest paths from start to end.

    Time: O(V + E + P) where P is number of paths
    Space: O(V + P)
    """
    if start == end:
        return [[start]]

    # BFS to find distances and predecessors
    dist = {start: 0}
    predecessors = defaultdict(list)
    queue = deque([start])

    while queue:
        node = queue.popleft()

        for neighbor in graph[node]:
            if neighbor not in dist:
                dist[neighbor] = dist[node] + 1
                queue.append(neighbor)

            # Add as predecessor if on a shortest path
            if dist.get(neighbor, float('inf')) == dist[node] + 1:
                predecessors[neighbor].append(node)

    if end not in dist:
        return []

    # Backtrack to find all paths
    paths = []

    def backtrack(node: int, path: list[int]):
        if node == start:
            paths.append(path[::-1])
            return

        for pred in predecessors[node]:
            path.append(pred)
            backtrack(pred, path)
            path.pop()

    backtrack(end, [end])
    return paths
```

---

## Comparison with Other Algorithms

| Algorithm      | Graph Type          | Time           | When to Use                    |
| -------------- | ------------------- | -------------- | ------------------------------ |
| BFS            | Unweighted          | O(V + E)       | All edges same weight          |
| Dijkstra       | Weighted (positive) | O((V+E) log V) | Different positive weights     |
| Bellman-Ford   | Weighted (any)      | O(V × E)       | Negative weights               |
| Floyd-Warshall | All pairs           | O(V³)          | Multiple source-target queries |

---

## 0-1 BFS

Special case: edges have weight 0 or 1. Use deque, add weight-0 edges to front:

```python
from collections import deque

def shortest_path_01(graph: dict[int, list[tuple[int, int]]],
                      start: int, end: int) -> int:
    """
    Shortest path when edges have weight 0 or 1.

    graph[u] = [(v, weight), ...]

    Time: O(V + E)
    Space: O(V)
    """
    dist = {start: 0}
    queue = deque([start])

    while queue:
        node = queue.popleft()

        for neighbor, weight in graph[node]:
            new_dist = dist[node] + weight

            if neighbor not in dist or new_dist < dist[neighbor]:
                dist[neighbor] = new_dist

                if weight == 0:
                    queue.appendleft(neighbor)  # Add to front
                else:
                    queue.append(neighbor)  # Add to back

    return dist.get(end, -1)
```

---

## Minimum Knight Moves

```python
from collections import deque

def min_knight_moves(x: int, y: int) -> int:
    """
    Minimum moves for knight to reach (x, y) from (0, 0).

    Time: O(|x| × |y|)
    Space: O(|x| × |y|)
    """
    # Knight moves
    moves = [
        (2, 1), (2, -1), (-2, 1), (-2, -1),
        (1, 2), (1, -2), (-1, 2), (-1, -2)
    ]

    # Work in first quadrant (symmetry)
    x, y = abs(x), abs(y)

    visited = set([(0, 0)])
    queue = deque([(0, 0, 0)])  # (x, y, moves)

    while queue:
        cx, cy, steps = queue.popleft()

        if (cx, cy) == (x, y):
            return steps

        for dx, dy in moves:
            nx, ny = cx + dx, cy + dy

            # Allow small negative to handle edge cases
            if (nx, ny) not in visited and nx >= -2 and ny >= -2:
                visited.add((nx, ny))
                queue.append((nx, ny, steps + 1))

    return -1
```

---

## Edge Cases

```python
# 1. Start equals end
shortest_path(graph, 0, 0)  # Return 0

# 2. No path exists
# Graph is disconnected
# Return -1

# 3. Empty graph
graph = {}
# Handle gracefully

# 4. Single node
graph = {0: []}
shortest_path(graph, 0, 0)  # Return 0

# 5. Large grid
# Ensure using deque, not list
```

---

## Common Mistakes

```python
# WRONG: Using DFS for shortest path
def shortest_wrong(graph, start, end):
    def dfs(node, dist):
        if node == end:
            return dist
        # DFS might find longer path first!

# CORRECT: Use BFS


# WRONG: Not marking visited when enqueuing
while queue:
    node = queue.popleft()
    visited.add(node)  # Too late! May enqueue duplicates

# CORRECT: Mark when enqueuing
if neighbor not in visited:
    visited.add(neighbor)  # Mark immediately
    queue.append(neighbor)


# WRONG: Checking destination when dequeuing
while queue:
    node, dist = queue.popleft()
    if node == end:  # Correct, but can optimize
        return dist

# BETTER: Check when enqueuing (earlier termination)
for neighbor in graph[node]:
    if neighbor == end:
        return dist + 1  # Found!
    if neighbor not in visited:
        ...
```

---

## Interview Tips

1. **BFS = shortest in unweighted**: Know this relationship
2. **Use deque**: `popleft()` is O(1), `list.pop(0)` is O(n)
3. **Mark visited when enqueuing**: Prevents duplicates
4. **Check destination early**: Can return when neighbor is found
5. **Grid = implicit graph**: Each cell is a node

---

## Practice Problems

| #   | Problem                        | Difficulty | Key Variation   |
| --- | ------------------------------ | ---------- | --------------- |
| 1   | Shortest Path in Binary Matrix | Medium     | 8-directional   |
| 2   | Word Ladder                    | Hard       | Implicit graph  |
| 3   | Minimum Knight Moves           | Medium     | Chess moves     |
| 4   | Open the Lock                  | Medium     | State graph     |
| 5   | Jump Game III                  | Medium     | Can reach index |
| 6   | Nearest Exit from Entrance     | Medium     | Grid BFS        |

---

## Key Takeaways

1. **BFS guarantees shortest**: Level-by-level exploration
2. **O(V + E) optimal**: Can't do better for shortest path
3. **Mark visited on enqueue**: Critical for correctness
4. **Grid is implicit graph**: Treat cells as nodes
5. **0-1 BFS special case**: Deque with front/back insertion

---

## Next: [12-clone-graph.md](./12-clone-graph.md)

Learn to deep copy graphs.

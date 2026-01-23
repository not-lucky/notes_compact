# Graphs

## Practice Problems

### 1. Find if Path Exists in Graph
**Difficulty:** Easy
**Concept:** Basic graph traversal

```python
from collections import defaultdict, deque
from typing import List

def valid_path(n: int, edges: List[List[int]], source: int, destination: int) -> bool:
    """
    Checks if a path exists between source and destination.
    Time: O(V + E)
    Space: O(V + E)
    """
    if source == destination: return True

    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)

    visited = {source}
    queue = deque([source])

    while queue:
        node = queue.popleft()
        if node == destination: return True
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    return False
```

### 2. Clone Graph
**Difficulty:** Medium
**Concept:** Graph construction

```python
class Node:
    def __init__(self, val=0, neighbors=None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []

def clone_graph(node: 'Node') -> 'Node':
    """
    Creates a deep copy of a graph.
    Time: O(V + E)
    Space: O(V)
    """
    if not node: return None

    old_to_new = {node: Node(node.val)}
    queue = deque([node])

    while queue:
        curr = queue.popleft()
        for neighbor in curr.neighbors:
            if neighbor not in old_to_new:
                old_to_new[neighbor] = Node(neighbor.val)
                queue.append(neighbor)
            old_to_new[curr].neighbors.append(old_to_new[neighbor])

    return old_to_new[node]
```

### 3. Number of Islands
**Difficulty:** Medium
**Concept:** Grid as graph

```python
def num_islands(grid: List[List[str]]) -> int:
    """
    Counts connected components in a grid.
    Time: O(R * C)
    Space: O(R * C)
    """
    if not grid: return 0
    rows, cols = len(grid), len(grid[0])
    islands = 0

    def dfs(r, c):
        if r < 0 or r >= rows or c < 0 or c >= cols or grid[r][c] == "0":
            return
        grid[r][c] = "0" # Mark visited
        dfs(r+1, c)
        dfs(r-1, c)
        dfs(r, c+1)
        dfs(r, c-1)

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "1":
                islands += 1
                dfs(r, c)
    return islands
```

### 4. Course Schedule
**Difficulty:** Medium
**Concept:** Cycle detection (Directed)

```python
def can_finish(num_courses: int, prerequisites: List[List[int]]) -> bool:
    """
    Checks if all courses can be finished (no cycles).
    Time: O(V + E)
    Space: O(V + E)
    """
    adj = defaultdict(list)
    for crs, pre in prerequisites:
        adj[pre].append(crs)

    # 0: unvisited, 1: visiting, 2: visited
    state = [0] * num_courses

    def has_cycle(v):
        if state[v] == 1: return True
        if state[v] == 2: return False

        state[v] = 1
        for neighbor in adj[v]:
            if has_cycle(neighbor): return True
        state[v] = 2
        return False

    for i in range(num_courses):
        if has_cycle(i): return False
    return True
```

### 5. Dijkstra's Algorithm (Shortest Path)
**Difficulty:** Medium
**Concept:** Weighted graph

```python
import heapq

def network_delay_time(times: List[List[int]], n: int, k: int) -> int:
    """
    Finds the shortest time for signal to reach all nodes.
    Time: O(E log V)
    Space: O(V + E)
    """
    adj = defaultdict(list)
    for u, v, w in times:
        adj[u].append((v, w))

    pq = [(0, k)] # (weight, node)
    dist = {}

    while pq:
        d, node = heapq.heappop(pq)
        if node in dist: continue
        dist[node] = d
        for neighbor, weight in adj[node]:
            if neighbor not in dist:
                heapq.heappush(pq, (d + weight, neighbor))

    return max(dist.values()) if len(dist) == n else -1
```

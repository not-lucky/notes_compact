# Graph Representations

## Practice Problems

### 1. Find if Path Exists in Graph
**Difficulty:** Easy
**Concept:** Basic graph traversal

```python
from collections import defaultdict, deque
from typing import List

def valid_path(n: int, edges: List[List[int]], source: int, destination: int) -> bool:
    """
    There is a bi-directional graph with n vertices, where each vertex is labeled from 0 to n - 1.
    Given edges, where each edges[i] = [u, v] denotes a bi-directional edge between vertex u and vertex v.
    Every vertex pair is connected by at most one edge, and no vertex has an edge to itself.
    Check if there is a valid path from source to destination.

    >>> valid_path(3, [[0,1],[1,2],[2,0]], 0, 2)
    True
    >>> valid_path(6, [[0,1],[0,2],[3,5],[5,4],[4,3]], 0, 5)
    False

    Time: O(V + E)
    Space: O(V + E)
    """
    if source == destination:
        return True

    # Build adjacency list
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)

    # BFS
    queue = deque([source])
    visited = {source}

    while queue:
        node = queue.popleft()
        if node == destination:
            return True

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
from typing import Optional, Dict

class Node:
    def __init__(self, val = 0, neighbors = None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []

def clone_graph(node: Optional['Node']) -> Optional['Node']:
    """
    Given a reference of a node in a connected undirected graph.
    Return a deep copy (clone) of the graph.

    Time: O(V + E)
    Space: O(V)
    """
    if not node:
        return None

    old_to_new: Dict['Node', 'Node'] = {}

    def dfs(curr: 'Node') -> 'Node':
        if curr in old_to_new:
            return old_to_new[curr]

        copy = Node(curr.val)
        old_to_new[curr] = copy

        for neighbor in curr.neighbors:
            copy.neighbors.append(dfs(neighbor))

        return copy

    return dfs(node)
```

### 3. Number of Islands
**Difficulty:** Medium
**Concept:** Grid as graph

```python
from typing import List

def num_islands(grid: List[List[str]]) -> int:
    """
    Given an m x n 2D binary grid grid which represents a map of '1's (land)
    and '0's (water), return the number of islands.

    >>> num_islands([["1","1","1","1","0"],["1","1","0","1","0"],["1","1","0","0","0"],["0","0","0","0","0"]])
    1
    >>> num_islands([["1","1","0","0","0"],["1","1","0","0","0"],["0","0","1","0","0"],["0","0","0","1","1"]])
    3

    Time: O(M * N)
    Space: O(M * N)
    """
    if not grid:
        return 0

    rows, cols = len(grid), len(grid[0])
    islands = 0
    visited = set()

    def dfs(r: int, c: int):
        if (r < 0 or r >= rows or c < 0 or c >= cols or
            grid[r][c] == "0" or (r, c) in visited):
            return

        visited.add((r, c))
        dfs(r + 1, c)
        dfs(r - 1, c)
        dfs(r, c + 1)
        dfs(r, c - 1)

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "1" and (r, c) not in visited:
                islands += 1
                dfs(r, c)

    return islands
```

### 4. Graph Valid Tree
**Difficulty:** Medium
**Concept:** Connected + acyclic

```python
from collections import defaultdict
from typing import List

def valid_tree(n: int, edges: List[List[int]]) -> bool:
    """
    Given n nodes labeled from 0 to n-1 and a list of undirected edges.
    Check if these edges make up a valid tree.

    >>> valid_tree(5, [[0,1],[0,2],[0,3],[1,4]])
    True
    >>> valid_tree(5, [[0,1],[1,2],[2,3],[1,3],[1,4]])
    False

    Time: O(V + E)
    Space: O(V + E)
    """
    # A tree with n nodes must have exactly n-1 edges
    if len(edges) != n - 1:
        return False

    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)

    visited = set()

    def dfs(node: int):
        visited.add(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                dfs(neighbor)

    if n > 0:
        dfs(0)

    return len(visited) == n
```

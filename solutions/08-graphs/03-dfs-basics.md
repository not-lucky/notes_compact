# DFS Basics

## Practice Problems

### 1. Flood Fill
**Difficulty:** Easy
**Concept:** Basic grid DFS

```python
from typing import List

def flood_fill(image: List[List[int]], sr: int, sc: int, color: int) -> List[List[int]]:
    """
    An image is represented by an m x n integer grid image where image[i][j]
    represents the pixel value of the image.
    Perform a flood fill on the image starting from the pixel (sr, sc).

    >>> flood_fill([[1,1,1],[1,1,0],[1,0,1]], 1, 1, 2)
    [[2, 2, 2], [2, 2, 0], [2, 0, 1]]
    >>> flood_fill([[0,0,0],[0,0,0]], 0, 0, 0)
    [[0, 0, 0], [0, 0, 0]]

    Time: O(M * N)
    Space: O(M * N)
    """
    start_color = image[sr][sc]
    if start_color == color:
        return image

    rows, cols = len(image), len(image[0])

    def dfs(r: int, c: int):
        if r < 0 or r >= rows or c < 0 or c >= cols or image[r][c] != start_color:
            return

        image[r][c] = color
        dfs(r + 1, c)
        dfs(r - 1, c)
        dfs(r, c + 1)
        dfs(r, c - 1)

    dfs(sr, sc)
    return image
```

### 2. All Paths From Source to Target
**Difficulty:** Medium
**Concept:** Path enumeration

```python
from typing import List

def all_paths_source_target(graph: List[List[int]]) -> List[List[int]]:
    """
    Given a directed acyclic graph (DAG) of n nodes labeled from 0 to n - 1,
    find all possible paths from node 0 to node n - 1 and return them in any order.
    The graph is given as follows: graph[i] is a list of all nodes you can
    visit from node i (i.e., there is a directed edge from node i to node graph[i][j]).

    >>> all_paths_source_target([[1,2],[3],[3],[]])
    [[0, 1, 3], [0, 2, 3]]
    >>> all_paths_source_target([[4,3,1],[3,2,4],[3],[4],[]])
    [[0, 4], [0, 3, 4], [0, 1, 3, 4], [0, 1, 2, 3, 4], [0, 1, 4]]

    Time: O(2^V * V)
    Space: O(V)
    """
    target = len(graph) - 1
    results = []

    def dfs(node: int, path: List[int]):
        if node == target:
            results.append(list(path))
            return

        for neighbor in graph[node]:
            path.append(neighbor)
            dfs(neighbor, path)
            path.pop() # backtrack

    dfs(0, [0])
    return results
```

### 3. Clone Graph
**Difficulty:** Medium
**Concept:** DFS with mapping

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

### 4. Course Schedule II
**Difficulty:** Medium
**Concept:** Topological sort DFS

```python
from collections import defaultdict
from typing import List

def find_order(numCourses: int, prerequisites: List[List[int]]) -> List[int]:
    """
    There are a total of numCourses courses you have to take, labeled from 0 to numCourses - 1.
    You are given an array prerequisites where prerequisites[i] = [ai, bi] indicates
    that you must take course bi first if you want to take course ai.
    Return the ordering of courses you should take to finish all courses.
    If there are many valid answers, return any of them. If it is impossible
    to finish all courses, return an empty array.

    >>> find_order(2, [[1,0]])
    [0, 1]
    >>> find_order(4, [[1,0],[2,0],[3,1],[3,2]])
    [0, 1, 2, 3]

    Time: O(V + E)
    Space: O(V + E)
    """
    graph = defaultdict(list)
    for a, b in prerequisites:
        graph[b].append(a)

    visited = [0] * numCourses # 0: unvisited, 1: visiting, 2: visited
    order = []
    has_cycle = False

    def dfs(node: int):
        nonlocal has_cycle
        if has_cycle:
            return

        visited[node] = 1
        for neighbor in graph[node]:
            if visited[neighbor] == 0:
                dfs(neighbor)
            elif visited[neighbor] == 1:
                has_cycle = True
                return

        visited[node] = 2
        order.append(node)

    for i in range(numCourses):
        if visited[i] == 0:
            dfs(i)

    return order[::-1] if not has_cycle else []
```

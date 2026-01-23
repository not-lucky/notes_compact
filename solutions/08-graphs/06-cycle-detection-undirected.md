# Cycle Detection in Undirected Graphs

## Practice Problems

### 1. Graph Valid Tree
**Difficulty:** Medium
**Concept:** Tree validation

```python
from collections import defaultdict
from typing import List

def valid_tree(n: int, edges: List[List[int]]) -> bool:
    """
    You have a graph of n nodes labeled from 0 to n - 1. You are given an
    integer n and a list of edges where edges[i] = [ai, bi] indicates that
    there is an undirected edge between nodes ai and bi.
    Return true if the edges of the given graph make up a valid tree,
    and false otherwise.

    >>> valid_tree(5, [[0,1],[0,2],[0,3],[1,4]])
    True
    >>> valid_tree(5, [[0,1],[1,2],[2,3],[1,3],[1,4]])
    False

    Time: O(V + E)
    Space: O(V + E)
    """
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

### 2. Redundant Connection
**Difficulty:** Medium
**Concept:** Find cycle edge

```python
from typing import List

class UnionFind:
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x: int) -> int:
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x: int, y: int) -> bool:
        px, py = self.find(x), self.find(y)
        if px == py:
            return False
        if self.rank[px] < self.rank[py]:
            px, py = py, px
        self.parent[py] = px
        if self.rank[px] == self.rank[py]:
            self.rank[px] += 1
        return True

def find_redundant_connection(edges: List[List[int]]) -> List[int]:
    """
    In this problem, a tree is an undirected graph that is connected and
    has no cycles.
    You are given a graph that started as a tree with n nodes labeled from
    1 to n, with one additional edge added.
    Return an edge that can be removed so that the resulting graph is a
    tree of n nodes.

    >>> find_redundant_connection([[1,2],[1,3],[2,3]])
    [2, 3]
    >>> find_redundant_connection([[1,2],[2,3],[3,4],[1,4],[1,5]])
    [1, 4]

    Time: O(V * α(V))
    Space: O(V)
    """
    n = len(edges)
    uf = UnionFind(n + 1)
    for u, v in edges:
        if not uf.union(u, v):
            return [u, v]
    return []
```

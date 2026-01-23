# Bipartite Check (Graph Coloring)

## Practice Problems

### 1. Is Graph Bipartite?
**Difficulty:** Medium
**Concept:** Core problem

```python
from collections import deque
from typing import List

def is_bipartite(graph: List[List[int]]) -> bool:
    """
    Check if a graph is bipartite.

    >>> is_bipartite([[1,2,3],[0,2],[0,1,3],[0,2]])
    False
    >>> is_bipartite([[1,3],[0,2],[1,3],[0,2]])
    True

    Time: O(V + E)
    Space: O(V)
    """
    n = len(graph)
    color = [-1] * n # -1: uncolored, 0: red, 1: blue

    for i in range(n):
        if color[i] == -1:
            color[i] = 0
            queue = deque([i])
            while queue:
                node = queue.popleft()
                for neighbor in graph[node]:
                    if color[neighbor] == -1:
                        color[neighbor] = 1 - color[node]
                        queue.append(neighbor)
                    elif color[neighbor] == color[node]:
                        return False
    return True
```

### 2. Possible Bipartition
**Difficulty:** Medium
**Concept:** People/dislikes framing

```python
from collections import defaultdict, deque
from typing import List

def possible_bipartition(n: int, dislikes: List[List[int]]) -> bool:
    """
    Can n people be split into two groups with no dislikes in the same group?

    >>> possible_bipartition(4, [[1,2],[1,3],[2,4]])
    True
    >>> possible_bipartition(3, [[1,2],[1,3],[2,3]])
    False

    Time: O(V + E)
    Space: O(V + E)
    """
    graph = defaultdict(list)
    for u, v in dislikes:
        graph[u].append(v)
        graph[v].append(u)

    color = [-1] * (n + 1)

    for i in range(1, n + 1):
        if color[i] == -1:
            color[i] = 0
            queue = deque([i])
            while queue:
                u = queue.popleft()
                for v in graph[u]:
                    if color[v] == -1:
                        color[v] = 1 - color[u]
                        queue.append(v)
                    elif color[v] == color[u]:
                        return False
    return True
```

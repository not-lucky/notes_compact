# Cycle Detection in Directed Graphs

## Practice Problems

### 1. Course Schedule
**Difficulty:** Medium
**Concept:** Core cycle detection

```python
from collections import defaultdict
from typing import List

def can_finish(num_courses: int, prerequisites: List[List[int]]) -> bool:
    """
    There are a total of num_courses courses you have to take, labeled from 0 to num_courses - 1.
    You are given an array prerequisites where prerequisites[i] = [ai, bi] indicates
    that you must take course bi first if you want to take course ai.
    Return true if you can finish all courses. Otherwise, return false.

    >>> can_finish(2, [[1,0]])
    True
    >>> can_finish(2, [[1,0],[0,1]])
    False

    Time: O(V + E)
    Space: O(V + E)
    """
    graph = defaultdict(list)
    for a, b in prerequisites:
        graph[b].append(a)

    visited = [0] * num_courses # 0: unvisited, 1: visiting, 2: visited

    def has_cycle(node: int) -> bool:
        visited[node] = 1 # Mark as visiting
        for neighbor in graph[node]:
            if visited[neighbor] == 1:
                return True
            if visited[neighbor] == 0:
                if has_cycle(neighbor):
                    return True
        visited[node] = 2 # Mark as visited
        return False

    for i in range(num_courses):
        if visited[i] == 0:
            if has_cycle(i):
                return False

    return True
```

### 2. Find Eventual Safe States
**Difficulty:** Medium
**Concept:** Nodes not in any cycle

```python
from typing import List

def eventual_safe_nodes(graph: List[List[int]]) -> List[int]:
    """
    There is a directed graph of n nodes with each node labeled from 0 to n - 1.
    The graph is represented by a 0-indexed 2D integer array graph where graph[i]
    is an integer array of nodes adjacent to node i.
    A node is a safe node if every possible path starting from that node leads to a terminal node.
    Return an array containing all the safe nodes of the graph. The answer should be sorted in ascending order.

    >>> eventual_safe_nodes([[1,2],[2,3],[5],[0],[5],[],[]])
    [2, 4, 5, 6]
    >>> eventual_safe_nodes([[1,2,3,4],[1,2],[3,4],[0,4],[]])
    [4]

    Time: O(V + E)
    Space: O(V)
    """
    n = len(graph)
    visited = [0] * n # 0: unvisited, 1: visiting, 2: safe

    def is_safe(node: int) -> bool:
        if visited[node] > 0:
            return visited[node] == 2

        visited[node] = 1 # visiting
        for neighbor in graph[node]:
            if not is_safe(neighbor):
                return False

        visited[node] = 2 # safe
        return True

    return [i for i in range(n) if is_safe(i)]
```

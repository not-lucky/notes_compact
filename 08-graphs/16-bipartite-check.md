# Bipartite Check (Graph Coloring)

> **Prerequisites:** [02-bfs-basics](./02-bfs-basics.md), [03-dfs-basics](./03-dfs-basics.md)

## Interview Context

Bipartite checking is important because:

1. **Graph theory fundamental**: Core concept in graph algorithms
2. **Two-coloring**: Can graph be divided into two groups with no intra-group edges?
3. **Real applications**: Matching problems, scheduling, conflict detection
4. **BFS/DFS practice**: Standard traversal with coloring

Common in Google and Microsoft interviews.

---

## Core Concept: What is Bipartite?

A graph is **bipartite** if vertices can be divided into two disjoint sets such that every edge connects a vertex in one set to a vertex in the other.

Equivalently: A graph is bipartite **if and only if** it contains no odd-length cycles.

```
Bipartite:              Not Bipartite:
  1 --- 3                  1 --- 2
  |     |                   \   /
  2 --- 4                    \ /
                              3
Sets: {1,4} and {2,3}     Triangle has odd cycle
```

---

## BFS Approach (Two-Coloring)

```python
from collections import deque

def is_bipartite_bfs(graph: list[list[int]]) -> bool:
    """
    Check if graph is bipartite using BFS.

    graph[i] = list of neighbors of node i

    Time: O(V + E)
    Space: O(V)
    """
    n = len(graph)
    color = [-1] * n  # -1 = uncolored, 0 or 1 = color

    for start in range(n):
        if color[start] != -1:
            continue  # Already colored

        # BFS from this component
        queue = deque([start])
        color[start] = 0

        while queue:
            node = queue.popleft()

            for neighbor in graph[node]:
                if color[neighbor] == -1:
                    # Color with opposite color
                    color[neighbor] = 1 - color[node]
                    queue.append(neighbor)
                elif color[neighbor] == color[node]:
                    # Same color as neighbor = not bipartite
                    return False

    return True
```

---

## DFS Approach

```python
def is_bipartite_dfs(graph: list[list[int]]) -> bool:
    """
    Check if graph is bipartite using DFS.

    Time: O(V + E)
    Space: O(V)
    """
    n = len(graph)
    color = [-1] * n

    def dfs(node: int, c: int) -> bool:
        color[node] = c

        for neighbor in graph[node]:
            if color[neighbor] == -1:
                if not dfs(neighbor, 1 - c):
                    return False
            elif color[neighbor] == c:
                return False

        return True

    for start in range(n):
        if color[start] == -1:
            if not dfs(start, 0):
                return False

    return True
```

---

## Visual Example

```
Graph:                  Coloring:
  0 --- 1               0 (Red) --- 1 (Blue)
  |     |               |           |
  2 --- 3               2 (Blue) --- 3 (Red)

BFS from 0:
  color[0] = 0 (Red)
  Neighbors: 1, 2
  color[1] = 1 (Blue)
  color[2] = 1 (Blue)

BFS from 1:
  Neighbors: 0, 3
  0 already colored (different, OK)
  color[3] = 0 (Red)

BFS from 2:
  Neighbors: 0, 3
  0 already colored 0 ≠ 1 (OK)
  3 already colored 0 ≠ 1 (OK)

BFS from 3:
  All neighbors already colored correctly

Result: Bipartite! Sets: {0, 3} and {1, 2}
```

---

## Union-Find Approach

```python
class UnionFind:
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x: int) -> int:
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x: int, y: int):
        px, py = self.find(x), self.find(y)
        if px == py:
            return
        if self.rank[px] < self.rank[py]:
            px, py = py, px
        self.parent[py] = px
        if self.rank[px] == self.rank[py]:
            self.rank[px] += 1


def is_bipartite_uf(graph: list[list[int]]) -> bool:
    """
    Check bipartite using Union-Find.

    Idea: All neighbors of a node should be in the same group
    (the "other" group). If node and neighbor are in same group, not bipartite.

    Time: O((V + E) × α(V))
    Space: O(V)
    """
    n = len(graph)
    uf = UnionFind(n)

    for node in range(n):
        for neighbor in graph[node]:
            # Node and neighbor should be in different groups
            if uf.find(node) == uf.find(neighbor):
                return False

            # All neighbors should be in the same group
            uf.union(graph[node][0], neighbor)

    return True
```

---

## Possible Bipartitions (Groups with Dislikes)

```python
from collections import deque

def possible_bipartition(n: int, dislikes: list[list[int]]) -> bool:
    """
    Can n people be split into two groups such that
    no one dislikes someone in their group?

    dislikes[i] = [a, b] means a and b dislike each other.

    Time: O(V + E)
    Space: O(V + E)
    """
    # Build graph
    graph = [[] for _ in range(n + 1)]  # 1-indexed
    for a, b in dislikes:
        graph[a].append(b)
        graph[b].append(a)

    color = [-1] * (n + 1)

    for start in range(1, n + 1):
        if color[start] != -1:
            continue

        queue = deque([start])
        color[start] = 0

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

---

## Related: Is Graph Bipartite? (Return Groups)

```python
def get_bipartition(graph: list[list[int]]) -> tuple[list[int], list[int]]:
    """
    Return the two groups if bipartite, empty lists otherwise.
    """
    n = len(graph)
    color = [-1] * n

    for start in range(n):
        if color[start] != -1:
            continue

        queue = deque([start])
        color[start] = 0

        while queue:
            node = queue.popleft()

            for neighbor in graph[node]:
                if color[neighbor] == -1:
                    color[neighbor] = 1 - color[node]
                    queue.append(neighbor)
                elif color[neighbor] == color[node]:
                    return [], []  # Not bipartite

    group0 = [i for i in range(n) if color[i] == 0]
    group1 = [i for i in range(n) if color[i] == 1]

    return group0, group1
```

---

## Key Insight: Odd Cycles

A graph is NOT bipartite if and only if it contains an odd-length cycle.

```
Odd cycle (triangle):
    1 --- 2
     \   /
      \ /
       3

Try coloring:
  1 = Red
  2 = Blue (neighbor of 1)
  3 = Red (neighbor of 2)
  But 3 is also neighbor of 1, same color!

Impossible to 2-color.
```

---

## Edge Cases

```python
# 1. Single node
graph = [[]]
# Bipartite (trivially)

# 2. No edges
graph = [[], [], []]
# Bipartite (any partition works)

# 3. Complete graph K3
graph = [[1, 2], [0, 2], [0, 1]]
# Not bipartite (triangle)

# 4. Self-loop
graph = [[0]]
# Not bipartite (node conflicts with itself)

# 5. Disconnected components
# Each component must be bipartite
```

---

## Common Mistakes

```python
# WRONG: Only checking from node 0
def is_bipartite_wrong(graph):
    color = [-1] * n
    color[0] = 0
    # Only processes one component!

# CORRECT: Check all components
for start in range(n):
    if color[start] == -1:
        # BFS/DFS from start


# WRONG: Not handling same-color detection
for neighbor in graph[node]:
    if color[neighbor] == -1:
        color[neighbor] = 1 - color[node]
    # Missing: check if neighbor has same color

# CORRECT:
elif color[neighbor] == color[node]:
    return False


# WRONG: Using visited instead of color
visited = set()
# Visited doesn't track which group!

# CORRECT: Track color (0 or 1)
color = [-1] * n  # -1 = unvisited, 0 or 1 = group
```

---

## Complexity Analysis

| Approach   | Time              | Space |
| ---------- | ----------------- | ----- |
| BFS        | O(V + E)          | O(V)  |
| DFS        | O(V + E)          | O(V)  |
| Union-Find | O((V + E) × α(V)) | O(V)  |

---

## Interview Tips

1. **Two-coloring = bipartite**: Same problem
2. **Handle disconnected graphs**: Check all components
3. **Color when visiting**: Not when processing
4. **Odd cycle = not bipartite**: Key insight
5. **Know both BFS and DFS**: Either works

---

## Practice Problems

| #   | Problem                   | Difficulty | Key Variation           |
| --- | ------------------------- | ---------- | ----------------------- |
| 1   | Is Graph Bipartite?       | Medium     | Core problem            |
| 2   | Possible Bipartition      | Medium     | People/dislikes framing |
| 3   | Graph Coloring (k colors) | Hard       | Generalization          |

---

## Key Takeaways

1. **Two-coloring**: Alternate colors with neighbors
2. **Same color = conflict**: Not bipartite
3. **Odd cycle**: Only way to fail
4. **Check all components**: Graph may be disconnected
5. **Both BFS and DFS work**: Pick your preference

---

## Next: [17-alien-dictionary.md](./17-alien-dictionary.md)

Learn topological sort from comparison constraints.

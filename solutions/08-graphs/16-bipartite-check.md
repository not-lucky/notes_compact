# Solutions: Bipartite Check (Graph Coloring)

## Practice Problems

| #   | Problem                   | Difficulty | Key Variation           |
| --- | ------------------------- | ---------- | ----------------------- |
| 1   | Is Graph Bipartite?       | Medium     | Core problem            |
| 2   | Possible Bipartition      | Medium     | People/dislikes framing |
| 3   | Graph Coloring (k colors) | Hard       | Generalization          |

---

## 1. Is Graph Bipartite?

### Problem Statement

Determine if the given undirected graph is bipartite.

### Optimal Python Solution

```python
from collections import deque

def isBipartite(graph: list[list[int]]) -> bool:
    n = len(graph)
    color = [-1] * n # -1: uncolored, 0: color A, 1: color B

    for i in range(n):
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

### Explanation

- **Algorithm**: BFS with two-coloring.
- **Logic**: A graph is bipartite if and only if it's two-colorable. If we find an adjacent node with the same color, it's not bipartite.
- **Complexity**: Time O(V + E), Space O(V).

---

## 2. Possible Bipartition

### Problem Statement

Can `n` people be split into two groups such that no two people in the same group dislike each other?

### Optimal Python Solution

```python
from collections import defaultdict, deque

def possibleBipartition(n: int, dislikes: list[list[int]]) -> bool:
    adj = defaultdict(list)
    for u, v in dislikes:
        adj[u].append(v)
        adj[v].append(u)

    color = [-1] * (n + 1)
    for i in range(1, n + 1):
        if color[i] == -1:
            color[i] = 0
            queue = deque([i])
            while queue:
                u = queue.popleft()
                for v in adj[u]:
                    if color[v] == -1:
                        color[v] = 1 - color[u]
                        queue.append(v)
                    elif color[v] == color[u]:
                        return False
    return True
```

### Explanation

- **Logic**: This is the exact same problem as `Is Graph Bipartite?`, just framed with people and dislikes.
- **Complexity**: Time O(V + E), Space O(V + E).

---

## 3. Graph Coloring (k colors)

### Problem Statement

Given an undirected graph and a number `k`, determine if the graph can be colored with at most `k` colors such that no two adjacent vertices have the same color.

### Optimal Python Solution (Backtracking)

```python
def isSafe(v, graph, color, c):
    for i in range(len(graph)):
        if graph[v][i] == 1 and color[i] == c:
            return False
    return True

def graphColoring(graph, k, color, v):
    if v == len(graph):
        return True

    for c in range(1, k + 1):
        if isSafe(v, graph, color, c):
            color[v] = c
            if graphColoring(graph, k, color, v + 1):
                return True
            color[v] = 0 # Backtrack

    return False
```

### Explanation

- **Algorithm**: Backtracking.
- **Complexity**: Time O(k^V), Space O(V). This is a general version of the bipartite check (which is k=2).
- **Note**: This is an NP-complete problem for k > 2.
  - O(V + E) for k=2 (Bipartite).
  - O(k^V) for k > 2.

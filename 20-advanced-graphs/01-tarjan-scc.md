# Tarjan's Algorithm: SCCs, Bridges, & Articulation Points

> **Prerequisites:** [08-graphs](../08-graphs/README.md) (DFS)

## Overview

Tarjan's algorithm is a powerful DFS-based approach to find structural properties of a graph in $O(V + E)$ time.

### Key Concepts

1.  **Discovery Time (`ids`)**: The order in which nodes are visited during DFS.
2.  **Low Link Value (`low`)**: The smallest discovery time reachable from a node (including itself) using back-edges.
3.  **On-Stack**: Tracks nodes currently in the recursion stack (used for SCCs).

---

## 1. Strongly Connected Components (SCCs)

In a directed graph, an SCC is a maximal subgraph where every node is reachable from every other node.

```python
def find_sccs(n, adj):
    ids = [-1] * n
    low = [0] * n
    on_stack = [False] * n
    stack = []
    timer = 0
    sccs = []

    def dfs(u):
        nonlocal timer
        ids[u] = low[u] = timer
        timer += 1
        stack.append(u)
        on_stack[u] = True

        for v in adj[u]:
            if ids[v] == -1:
                dfs(v)
                low[u] = min(low[u], low[v])
            elif on_stack[v]:
                low[u] = min(low[u], ids[v])

        if ids[u] == low[u]:
            component = []
            while stack:
                node = stack.pop()
                on_stack[node] = False
                component.append(node)
                if node == u: break
            sccs.append(component)

    for i in range(n):
        if ids[i] == -1:
            dfs(i)
    return sccs
```

---

## 2. Bridges and Articulation Points

In an undirected graph:
-   **Bridge**: An edge whose removal increases the number of connected components.
-   **Articulation Point**: A vertex whose removal increases the number of connected components.

```python
def find_bridges_and_points(n, adj):
    ids = [-1] * n
    low = [0] * n
    bridges = []
    points = set()
    timer = 0

    def dfs(u, p=-1):
        nonlocal timer
        ids[u] = low[u] = timer
        timer += 1
        children = 0

        for v in adj[u]:
            if v == p: continue
            if ids[v] == -1:
                children += 1
                dfs(v, u)
                low[u] = min(low[u], low[v])
                if low[v] > ids[u]:
                    bridges.append((u, v))
                if p != -1 and low[v] >= ids[u]:
                    points.add(u)
            else:
                low[u] = min(low[u], ids[v])

        return children

    for i in range(n):
        if ids[i] == -1:
            if dfs(i) > 1:
                points.add(i)
    return bridges, points
```

---

## Summary Checklist

- [ ] **SCCs**: Use `on_stack` to only consider back-edges to current path.
- [ ] **Bridges**: Edge $(u, v)$ is a bridge if `low[v] > ids[u]`.
- [ ] **Articulation Points**: Node $u$ is a point if `low[v] >= ids[u]` (and handle root case).
- [ ] **Complexity**: All are $O(V+E)$ time and $O(V)$ space.

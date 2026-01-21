# Lowest Common Ancestor (LCA) via Binary Lifting

> **Prerequisites:** [06-trees](../06-trees/README.md), [15-bit-manipulation](../15-bit-manipulation/README.md)

## Overview

Binary Lifting is a technique used to find the Lowest Common Ancestor (LCA) of two nodes in a tree in $O(\log N)$ time with $O(N \log N)$ preprocessing. It can also be extended to answer path queries (e.g., "minimum edge on path from $u$ to $v$").

## Core Logic

We precompute `up[u][i]`, which represents the $2^i$-th ancestor of node $u$.
-   `up[u][0]` is the direct parent of $u$.
-   `up[u][i] = up[up[u][i-1]][i-1]` (The $2^i$-th ancestor is the $2^{i-1}$-th ancestor of the $2^{i-1}$-th ancestor).

---

## Implementation Template

```python
class LCA:
    def __init__(self, n, adj, root=0):
        self.n = n
        self.log = n.bit_length()
        self.depth = [0] * n
        self.up = [[-1] * self.log for _ in range(n)]

        self._dfs(root, -1, 0, adj)

    def _dfs(self, u, p, d, adj):
        self.depth[u] = d
        self.up[u][0] = p
        for i in range(1, self.log):
            if self.up[u][i-1] != -1:
                self.up[u][i] = self.up[self.up[u][i-1]][i-1]

        for v in adj[u]:
            if v != p:
                self._dfs(v, u, d + 1, adj)

    def get_lca(self, u, v):
        if self.depth[u] < self.depth[v]:
            u, v = v, u

        # 1. Lift u to the same depth as v
        diff = self.depth[u] - self.depth[v]
        for i in range(self.log):
            if (diff >> i) & 1:
                u = self.up[u][i]

        if u == v:
            return u

        # 2. Lift both u and v until they have the same parent
        for i in range(self.log - 1, -1, -1):
            if self.up[u][i] != self.up[v][i]:
                u = self.up[u][i]
                v = self.up[v][i]

        return self.up[u][0]
```

---

## Complexity Analysis

| Phase | Complexity | Note |
| :--- | :--- | :--- |
| **Preprocessing**| $O(N \log N)$ | DFS + Filling the `up` table. |
| **Query (LCA)** | $O(\log N)$ | At most $2 \times \log N$ jumps. |
| **Space** | $O(N \log N)$ | Size of the `up` table. |

---

## Common Use Cases

1.  **Distance between nodes**: `dist(u, v) = depth[u] + depth[v] - 2 * depth[lca(u, v)]`.
2.  **Path Queries**: Find max/min/sum on the path between $u$ and $v$ by adding another DP table `val[u][i]`.
3.  **Tree Updates**: Some problems involving adding edges to trees and maintaining properties.

## Summary Checklist

- [ ] Is the `up` table size large enough ($N \times \log N$)?
- [ ] Are depth levels correctly calculated?
- [ ] In `get_lca`, do you lift the deeper node first?
- [ ] Base cases: $u=v$ after first lift, and root ancestors being $-1$.

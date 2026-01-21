# Euler Tour (Tree Flattening)

> **Prerequisites:** [06-trees](../06-trees/README.md), [08-graphs](../08-graphs/README.md) (DFS)

## Overview

Euler Tour is a technique to represent a tree as a linear array by recording the entry and exit times of each node during a DFS traversal. This "flattens" the tree, allowing subtree queries and path queries to be handled by linear data structures like Segment Trees or Fenwick Trees.

## Core Logic

We maintain two timers/indices for each node:
-   `tin[u]`: Time when we enter node `u`.
-   `tout[u]`: Time when we exit node `u`.

The range `[tin[u], tout[u]]` in the flattened array represents the entire subtree of `u`.

---

## Implementation Template

```python
def euler_tour(n, adj, root=0):
    tin = [0] * n
    tout = [0] * n
    flat_array = []
    timer = 0

    def dfs(u, p):
        nonlocal timer
        tin[u] = timer
        flat_array.append(u)
        timer += 1

        for v in adj[u]:
            if v != p:
                dfs(v, u)

        tout[u] = timer - 1 # Subtree ends at current timer - 1

    dfs(root, -1)
    return tin, tout, flat_array

# To query subtree sum of node u:
# query_range(tin[u], tout[u]) on a Fenwick/Segment Tree
# built over values mapped to flat_array.
```

---

## Applications

### 1. Subtree Queries
A subtree rooted at `u` corresponds to the range `[tin[u], tout[u]]` in the flattened representation.
- **Update**: Update value at `tin[u]`.
- **Query**: Sum in range `[tin[u], tout[u]]`.
- **Complexity**: $O(\log N)$ with BIT/Segment Tree.

### 2. Path Queries
There are two ways to represent paths:
- **Version A**: Record entry and exit. Path $u \to v$ involves nodes that appear exactly once in the tour between $tin[u]$ and $tin[v]$ (requires LCA handling).
- **Version B**: Use properties like `dist(u, v) = depth[u] + depth[v] - 2 * depth[lca(u, v)]`.

---

## Summary Checklist

- [ ] Does `tout[u]` include the entire subtree? (Usually `tout[u] = timer - 1`).
- [ ] Is the `flat_array` correctly mapped to node values?
- [ ] For subtree updates, are you updating the correct index in the BIT/Segment Tree (`tin[u]`)?
- [ ] Complexity: $O(N)$ to build, $O(1)$ to find range, $O(\log N)$ for operations on the range.

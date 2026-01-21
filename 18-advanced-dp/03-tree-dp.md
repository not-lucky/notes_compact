# DP on Trees

> **Prerequisites:** [06-trees](../06-trees/README.md), [09-dynamic-programming](../09-dynamic-programming/README.md)

## Overview

Tree DP involves solving optimization problems on tree structures. Since a tree is a naturally recursive structure, DP is often implemented using DFS.

## Building Intuition

In a standard tree DP problem, the result for a node depends on the results from its children.

**Key Techniques**:
1.  **Standard DFS DP**: $O(N)$ traversal. At each node, compute a value based on children's values.
2.  **Rerooting DP**: When the answer depends on which node is the root. We first compute the answer for an arbitrary root (e.g., node 0), then do a second DFS to "shift" the root to each neighbor in $O(1)$ and compute their answers.

---

## Template (Post-order Traversal)

```python
def tree_dp(node, parent):
    dp[node] = initial_value

    for child in adj[node]:
        if child == parent: continue

        tree_dp(child, node)
        # Combine child result into current node
        dp[node] = combine(dp[node], dp[child])
```

---

## Problem 1: Binary Tree Maximum Path Sum (LeetCode 124)

Find the maximum path sum in a binary tree where the path can start and end at any node.

### Intuition
For each node, we want to know:
1.  The max path sum that *passes through* this node (left subtree + node + right subtree).
2.  The max path sum that can be *extended upwards* (node + max of left or right subtree).

### Solution

```python
def maxPathSum(root):
    self.max_sum = float('-inf')

    def get_max_gain(node):
        if not node:
            return 0

        # Max gain from left and right subtrees (ignore if negative)
        left_gain = max(get_max_gain(node.left), 0)
        right_gain = max(get_max_gain(node.right), 0)

        # Path sum passing through this node
        current_path_sum = node.val + left_gain + right_gain
        self.max_sum = max(self.max_sum, current_path_sum)

        # For recursion: return max gain if we continue the path upwards
        return node.val + max(left_gain, right_gain)

    get_max_gain(root)
    return self.max_sum
```

---

## Problem 2: Tree Diameter (General Tree)

Find the longest path between any two nodes in an undirected tree.

### Intuition
The diameter is the maximum of:
1.  Diameters within any of the subtrees.
2.  The sum of the two longest paths from the current node down to leaves in different subtrees.

### Solution

```python
def tree_diameter(n: int, edges: list[list[int]]) -> int:
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)

    self.diameter = 0

    def dfs(node, parent):
        # Returns the longest path starting at 'node' downwards
        max_h1, max_h2 = 0, 0 # Two longest branches

        for neighbor in adj[node]:
            if neighbor == parent: continue

            h = dfs(neighbor, node) + 1
            if h > max_h1:
                max_h1, max_h2 = h, max_h1
            elif h > max_h2:
                max_h2 = h

        # Diameter through this node is sum of two longest branches
        self.diameter = max(self.diameter, max_h1 + max_h2)
        return max_h1

    dfs(0, -1)
    return self.diameter
```

---

## Problem 3: Sum of Distances in Tree (Rerooting)

Given an undirected tree, find the sum of distances from each node to all other nodes.

### Intuition
1.  **First DFS**: For a fixed root, compute `count[node]` (nodes in subtree) and `ans[node]` (sum of distances to nodes in subtree).
2.  **Second DFS**: When moving root from `u` to `v`:
    *   `v`'s subtree nodes move 1 unit closer.
    *   The other `N - count[v]` nodes move 1 unit further away.
    *   `ans[v] = ans[u] - count[v] + (N - count[v])`

### Solution

```python
def sum_of_distances_in_tree(n: int, edges: list[list[int]]) -> list[int]:
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)

    count = [1] * n
    ans = [0] * n

    def dfs_bottom_up(u, p):
        for v in adj[u]:
            if v == p: continue
            dfs_bottom_up(v, u)
            count[u] += count[v]
            ans[u] += ans[v] + count[v]

    def dfs_top_down(u, p):
        for v in adj[u]:
            if v == p: continue
            # Reroot from u to v
            ans[v] = ans[u] - count[v] + (n - count[v])
            dfs_top_down(v, u)

    dfs_bottom_up(0, -1)
    dfs_top_down(0, -1)
    return ans
```

---

## Summary Checklist

- [ ] Is it a tree? (N nodes, N-1 edges, connected).
- [ ] Most tree DP is $O(N)$ using DFS.
- [ ] Use post-order (bottom-up) for values depending on subtrees.
- [ ] Use pre-order (top-down) for values depending on path from root.
- [ ] Use **Rerooting** if you need the answer for *every* node as a root and the naive $O(N^2)$ is too slow.

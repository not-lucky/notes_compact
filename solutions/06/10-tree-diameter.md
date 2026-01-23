# Tree Diameter

## Practice Problems

### 1. Diameter of Binary Tree
**Difficulty:** Easy
**Concept:** Longest path between any two nodes

```python
from typing import Optional

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def diameter_of_binary_tree(root: Optional[TreeNode]) -> int:
    """
    Returns the diameter of a binary tree.
    Time: O(n)
    Space: O(h)
    """
    res = 0

    def depth(node):
        nonlocal res
        if not node:
            return 0

        left = depth(node.left)
        right = depth(node.right)

        res = max(res, left + right)
        return 1 + max(left, right)

    depth(root)
    return res
```

### 2. Longest Univalue Path
**Difficulty:** Medium
**Concept:** Diameter with same-value constraint

```python
def longest_univalue_path(root: Optional[TreeNode]) -> int:
    """
    Returns the longest path where each node has the same value.
    Time: O(n)
    Space: O(h)
    """
    res = 0

    def dfs(node):
        nonlocal res
        if not node:
            return 0

        left = dfs(node.left)
        right = dfs(node.right)

        left_path = left + 1 if node.left and node.left.val == node.val else 0
        right_path = right + 1 if node.right and node.right.val == node.val else 0

        res = max(res, left_path + right_path)
        return max(left_path, right_path)

    dfs(root)
    return res
```

### 3. Tree Diameter (Unrooted Tree)
**Difficulty:** Medium
**Concept:** BFS from any node

```python
from collections import deque, defaultdict
from typing import List

def tree_diameter_unrooted(edges: List[List[int]]) -> int:
    """
    Returns the diameter of an unrooted tree.
    Time: O(n)
    Space: O(n)
    """
    if not edges:
        return 0

    adj = defaultdict(list)
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)

    def bfs(start_node):
        dist = {start_node: 0}
        queue = deque([start_node])
        farthest_node = start_node

        while queue:
            u = queue.popleft()
            if dist[u] > dist[farthest_node]:
                farthest_node = u

            for v in adj[u]:
                if v not in dist:
                    dist[v] = dist[u] + 1
                    queue.append(v)

        return farthest_node, dist[farthest_node]

    # Two BFS strategy:
    # 1. Start from any node and find the farthest node u
    # 2. Start from u and find the farthest node v
    # 3. The distance between u and v is the diameter
    u, _ = bfs(0)
    v, diameter = bfs(u)
    return diameter
```

# Solution: Tree Diameter

## Problem 1: Diameter of Binary Tree
### Problem Statement
Given the `root` of a binary tree, return the length of the diameter of the tree.

The diameter of a binary tree is the length of the longest path between any two nodes in a tree. This path may or may not pass through the root.

The length of a path between two nodes is represented by the number of edges between them.

### Constraints
- The number of nodes in the tree is in the range `[1, 10^4]`.
- `-100 <= Node.val <= 100`

### Example
Input: `root = [1,2,3,4,5]`
Output: `3`
Explanation: `3` is the length of the path `[4,2,1,3]` or `[5,2,1,3]`.

### Python Implementation
```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def diameterOfBinaryTree(root: TreeNode) -> int:
    """
    Time Complexity: O(n)
    Space Complexity: O(h)
    """
    diameter = 0

    def get_height(node):
        nonlocal diameter
        if not node:
            return 0

        left_h = get_height(node.left)
        right_h = get_height(node.right)

        # Update diameter with path passing through this node
        diameter = max(diameter, left_h + right_h)

        # Return height of this node
        return 1 + max(left_h, right_h)

    get_height(root)
    return diameter
```

---

## Problem 2: Longest Path With Different Adjacent Characters
### Problem Statement
You are given a tree (i.e. a connected, undirected graph that has no cycles) rooted at node `0` consisting of `n` nodes numbered from `0` to `n - 1`. The tree is represented by a 0-indexed array `parent` of size `n`, where `parent[i]` is the parent of node `i`. Since node `0` is the root, `parent[0] == -1`.

You are also given a string `s` of length `n`, where `s[i]` is the character assigned to node `i`.

Return the length of the longest path in the tree such that no pair of adjacent nodes on the path have the same character assigned to them.

### Constraints
- `n == parent.length == s.length`
- `1 <= n <= 10^5`
- `0 <= parent[i] <= n - 1` for all `i >= 1`
- `parent[0] == -1`
- `parent` represents a valid tree.
- `s` consists of only lowercase English letters.

### Example
Input: `parent = [-1,0,0,1,1,2], s = "abacbe"`
Output: `3`
Explanation: The longest path where each two adjacent nodes have different characters is the path: `0 -> 1 -> 3`. The length of this path is `3`. Note that the path `4 -> 1 -> 0 -> 2 -> 5` is also valid and has a length of `3`.

### Python Implementation
```python
from collections import defaultdict

def longestPath(parent: list[int], s: str) -> int:
    """
    Time Complexity: O(n)
    Space Complexity: O(n)
    """
    n = len(parent)
    children = defaultdict(list)
    for i in range(1, n):
        children[parent[i]].append(i)

    self_longest = 1

    def dfs(node):
        nonlocal self_longest

        # We need the two longest paths from children to form the longest path through this node
        max1 = 0
        max2 = 0

        for child in children[node]:
            child_len = dfs(child)

            if s[child] != s[node]:
                if child_len > max1:
                    max2 = max1
                    max1 = child_len
                elif child_len > max2:
                    max2 = child_len

        # Path passing through this node
        self_longest = max(self_longest, max1 + max2 + 1)

        # Return the longest single path ending at this node
        return max1 + 1

    dfs(0)
    return self_longest
```

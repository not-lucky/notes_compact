# Solution: Lowest Common Ancestor (LCA) Practice Problems

## Problem 1: Lowest Common Ancestor of a Binary Search Tree
### Problem Statement
Given a binary search tree (BST), find the lowest common ancestor (LCA) node of two given nodes in the BST.

According to the definition of LCA on Wikipedia: "The lowest common ancestor is defined between two nodes `p` and `q` as the lowest node in `T` that has both `p` and `q` as descendants (where we allow a node to be a descendant of itself)."

### Constraints
- The number of nodes in the tree is in the range `[2, 10^5]`.
- `-10^9 <= Node.val <= 10^9`
- All `Node.val` are unique.
- `p != q`
- `p` and `q` will exist in the BST.

### Example
Input: `root = [6,2,8,0,4,7,9,null,null,3,5], p = 2, q = 8`
Output: `6`

### Python Implementation
```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def lowestCommonAncestor(root: TreeNode, p: TreeNode, q: TreeNode) -> TreeNode:
    """
    Time Complexity: O(h)
    Space Complexity: O(h)
    """
    if p.val < root.val and q.val < root.val:
        return lowestCommonAncestor(root.left, p, q)
    if p.val > root.val and q.val > root.val:
        return lowestCommonAncestor(root.right, p, q)
    return root
```

---

## Problem 2: Lowest Common Ancestor of a Binary Tree
### Problem Statement
Given a binary tree, find the lowest common ancestor (LCA) of two given nodes in the tree.

### Constraints
- The number of nodes in the tree is in the range `[2, 10^5]`.
- `-10^9 <= Node.val <= 10^9`
- All `Node.val` are unique.
- `p != q`
- `p` and `q` will exist in the tree.

### Example
Input: `root = [3,5,1,6,2,0,8,null,null,7,4], p = 5, q = 1`
Output: `3`

### Python Implementation
```python
def lowestCommonAncestor(root: TreeNode, p: TreeNode, q: TreeNode) -> TreeNode:
    """
    Time Complexity: O(n)
    Space Complexity: O(h)
    """
    if not root or root == p or root == q:
        return root

    left = lowestCommonAncestor(root.left, p, q)
    right = lowestCommonAncestor(root.right, p, q)

    if left and right:
        return root
    return left if left else right
```

---

## Problem 3: Lowest Common Ancestor of a Binary Tree II
### Problem Statement
Given the root of a binary tree, return the lowest common ancestor (LCA) of two nodes, `p` and `q`. If either node `p` or `q` does not exist in the tree, return `null`. All values of the nodes in the tree are unique.

### Constraints
- The number of nodes in the tree is in the range `[1, 10^4]`.
- `-10^9 <= Node.val <= 10^9`
- All `Node.val` are unique.
- `p != q`

### Example
Input: `root = [3,5,1,6,2,0,8,null,null,7,4], p = 5, q = 10`
Output: `null`

### Python Implementation
```python
def lowestCommonAncestor(root: TreeNode, p: TreeNode, q: TreeNode) -> TreeNode:
    """
    Time Complexity: O(n)
    Space Complexity: O(h)
    """
    count = 0
    def dfs(node):
        nonlocal count
        if not node:
            return None

        left = dfs(node.left)
        right = dfs(node.right)

        if node == p or node == q:
            count += 1
            return node

        if left and right:
            return node
        return left if left else right

    res = dfs(root)
    return res if count == 2 else None
```

---

## Problem 4: Lowest Common Ancestor of a Binary Tree III
### Problem Statement
Given two nodes of a binary tree `p` and `q`, return their lowest common ancestor (LCA). Each node will have a reference to its parent node. The definition for `Node` is below:

```python
class Node:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None
        self.parent = None
```

### Constraints
- The number of nodes in the tree is in the range `[2, 10^5]`.
- `-10^9 <= Node.val <= 10^9`
- All `Node.val` are unique.
- `p != q`
- `p` and `q` exist in the tree.

### Example
Input: `p = 5, q = 1`
Output: `3`

### Python Implementation
```python
def lowestCommonAncestor(p: 'Node', q: 'Node') -> 'Node':
    """
    Time Complexity: O(h)
    Space Complexity: O(1)
    """
    a, b = p, q
    while a != b:
        a = a.parent if a.parent else q
        b = b.parent if b.parent else p
    return a
```

---

## Problem 5: Lowest Common Ancestor of Deepest Leaves
### Problem Statement
Given the `root` of a binary tree, return the lowest common ancestor of its deepest leaves.

### Constraints
- The number of nodes in the tree will be in the range `[1, 1000]`.
- `0 <= Node.val <= 1000`
- The values of the nodes in the tree are unique.

### Example
Input: `root = [3,5,1,6,2,0,8,null,null,7,4]`
Output: `[2,7,4]`

### Python Implementation
```python
def lcaDeepestLeaves(root: TreeNode) -> TreeNode:
    """
    Time Complexity: O(n)
    Space Complexity: O(h)
    """
    def helper(node):
        if not node:
            return 0, None

        d1, lca1 = helper(node.left)
        d2, lca2 = helper(node.right)

        if d1 > d2:
            return d1 + 1, lca1
        if d2 > d1:
            return d2 + 1, lca2
        return d1 + 1, node

    return helper(root)[1]
```

---

## Problem 6: Step-By-Step Directions From a Binary Tree Node to Another
### Problem Statement
You are given the `root` of a binary tree with `n` nodes. Each node is uniquely valued from `1` to `n`. You are also given an integer `startValue` representing the value of the start node `s`, and a different integer `destValue` representing the value of the destination node `t`.

Find the shortest path starting from node `s` and ending at node `t`. Generate step-by-step directions of such path as a string consisting of only the uppercase letters `'U'`, `'L'`, and `'R'`.

### Constraints
- The number of nodes in the tree is `n`.
- `2 <= n <= 10^5`
- `1 <= Node.val <= n`
- All `Node.val` are unique.
- `1 <= startValue, destValue <= n`
- `startValue != destValue`

### Example
Input: `root = [5,1,2,3,null,6,4], startValue = 3, destValue = 6`
Output: `"UURL"`

### Python Implementation
```python
def getDirections(root: TreeNode, startValue: int, destValue: int) -> str:
    """
    Time Complexity: O(n)
    Space Complexity: O(n)
    """
    def find_path(node, target, path):
        if not node:
            return False
        if node.val == target:
            return True

        path.append('L')
        if find_path(node.left, target, path):
            return True
        path.pop()

        path.append('R')
        if find_path(node.right, target, path):
            return True
        path.pop()

        return False

    start_path = []
    dest_path = []

    find_path(root, startValue, start_path)
    find_path(root, destValue, dest_path)

    # Find where paths diverge
    i = 0
    while i < min(len(start_path), len(dest_path)) and start_path[i] == dest_path[i]:
        i += 1

    return 'U' * (len(start_path) - i) + "".join(dest_path[i:])
```

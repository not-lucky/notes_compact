# Lowest Common Ancestor (LCA)

## Practice Problems

### 1. Lowest Common Ancestor of a Binary Search Tree
**Difficulty:** Medium
**Concept:** BST split point

```python
from typing import Optional

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def lowest_common_ancestor_bst(root: Optional[TreeNode], p: TreeNode, q: TreeNode) -> Optional[TreeNode]:
    """
    Finds the LCA of two nodes in a BST.
    Time: O(h)
    Space: O(1) iterative
    """
    while root:
        if p.val < root.val and q.val < root.val:
            root = root.left
        elif p.val > root.val and q.val > root.val:
            root = root.right
        else:
            return root
    return None
```

### 2. Lowest Common Ancestor of a Binary Tree
**Difficulty:** Medium
**Concept:** General recursive search

```python
def lowest_common_ancestor(root: Optional[TreeNode], p: TreeNode, q: TreeNode) -> Optional[TreeNode]:
    """
    Finds the LCA of two nodes in a general binary tree.
    Time: O(n)
    Space: O(h)
    """
    if not root or root == p or root == q:
        return root

    left = lowest_common_ancestor(root.left, p, q)
    right = lowest_common_ancestor(root.right, p, q)

    if left and right:
        return root
    return left if left else right
```

### 3. Lowest Common Ancestor of a Binary Tree II
**Difficulty:** Medium
**Concept:** Handle non-existence

```python
def lca_with_existence(root: Optional[TreeNode], p: TreeNode, q: TreeNode) -> Optional[TreeNode]:
    """
    Finds the LCA, but returns None if p or q don't exist.
    Time: O(n)
    Space: O(h)
    """
    found_p = found_q = False

    def dfs(node):
        nonlocal found_p, found_q
        if not node:
            return None

        # Postorder to visit all nodes even if one is ancestor
        left = dfs(node.left)
        right = dfs(node.right)

        if node == p:
            found_p = True
            return node
        if node == q:
            found_q = True
            return node

        if left and right:
            return node
        return left if left else right

    res = dfs(root)
    return res if found_p and found_q else None
```

### 4. Lowest Common Ancestor of a Binary Tree III
**Difficulty:** Medium
**Concept:** Nodes with parent pointers

```python
class NodeWithParent:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None
        self.parent = None

def lca_parent_pointers(p: 'NodeWithParent', q: 'NodeWithParent') -> 'NodeWithParent':
    """
    Finds LCA when nodes have parent pointers (intersection of linked lists).
    Time: O(h)
    Space: O(1)
    """
    a, b = p, q
    while a != b:
        a = a.parent if a.parent else q
        b = b.parent if b.parent else p
    return a
```

### 5. Lowest Common Ancestor of Deepest Leaves
**Difficulty:** Medium
**Concept:** Deepest leaves LCA

```python
def lca_deepest_leaves(root: Optional[TreeNode]) -> Optional[TreeNode]:
    """
    Finds the LCA of all deepest leaves.
    Time: O(n)
    Space: O(h)
    """
    def dfs(node):
        if not node:
            return 0, None # depth, lca

        l_depth, l_lca = dfs(node.left)
        r_depth, r_lca = dfs(node.right)

        if l_depth == r_depth:
            return l_depth + 1, node
        elif l_depth > r_depth:
            return l_depth + 1, l_lca
        else:
            return r_depth + 1, r_lca

    return dfs(root)[1]
```

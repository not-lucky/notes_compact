# Tree Basics

## Practice Problems

### 1. Maximum Depth of Binary Tree
**Difficulty:** Easy
**Concept:** Basic recursion

```python
from typing import Optional

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def max_depth(root: Optional[TreeNode]) -> int:
    """
    Finds the maximum depth of a binary tree.
    Time: O(n) - visit each node once
    Space: O(h) - recursion stack height
    """
    if not root:
        return 0
    return 1 + max(max_depth(root.left), max_depth(root.right))
```

### 2. Invert Binary Tree
**Difficulty:** Easy
**Concept:** Tree manipulation

```python
def invert_tree(root: Optional[TreeNode]) -> Optional[TreeNode]:
    """
    Inverts a binary tree (mirror image).
    Time: O(n)
    Space: O(h)
    """
    if not root:
        return None

    # Swap children
    root.left, root.right = invert_tree(root.right), invert_tree(root.left)
    return root
```

### 3. Same Tree
**Difficulty:** Easy
**Concept:** Tree comparison

```python
def is_same_tree(p: Optional[TreeNode], q: Optional[TreeNode]) -> bool:
    """
    Checks if two binary trees are the same.
    Time: O(n)
    Space: O(h)
    """
    if not p and not q:
        return True
    if not p or not q or p.val != q.val:
        return False

    return is_same_tree(p.left, q.left) and is_same_tree(p.right, q.right)
```

### 4. Count Complete Tree Nodes
**Difficulty:** Medium
**Concept:** Tree properties

```python
def count_nodes(root: Optional[TreeNode]) -> int:
    """
    Counts nodes in a complete binary tree in less than O(n).
    Time: O(log(n)^2)
    Space: O(log(n))
    """
    if not root:
        return 0

    def get_height(node, is_left):
        h = 0
        while node:
            h += 1
            node = node.left if is_left else node.right
        return h

    l_height = get_height(root, True)
    r_height = get_height(root, False)

    if l_height == r_height:
        return (2 ** l_height) - 1

    return 1 + count_nodes(root.left) + count_nodes(root.right)
```

### 5. Subtree of Another Tree
**Difficulty:** Easy
**Concept:** Tree matching

```python
def is_subtree(root: Optional[TreeNode], sub_root: Optional[TreeNode]) -> bool:
    """
    Checks if a tree has a subtree identical to sub_root.
    Time: O(n * m) - n nodes in root, m nodes in sub_root
    Space: O(h)
    """
    if not root:
        return False

    def is_same(p, q):
        if not p and not q: return True
        if not p or not q or p.val != q.val: return False
        return is_same(p.left, q.left) and is_same(p.right, q.right)

    if is_same(root, sub_root):
        return True

    return is_subtree(root.left, sub_root) or is_subtree(root.right, sub_root)
```

# Symmetric Tree and Same Tree

## Practice Problems

### 1. Same Tree
**Difficulty:** Easy
**Concept:** Structural and value identity

```python
from typing import Optional

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def is_same_tree(p: Optional[TreeNode], q: Optional[TreeNode]) -> bool:
    """
    Checks if two trees are identical.
    Time: O(n)
    Space: O(h)
    """
    if not p and not q:
        return True
    if not p or not q or p.val != q.val:
        return False

    return is_same_tree(p.left, q.left) and is_same_tree(p.right, q.right)
```

### 2. Symmetric Tree
**Difficulty:** Easy
**Concept:** Mirror identity

```python
def is_symmetric(root: Optional[TreeNode]) -> bool:
    """
    Checks if a tree is a mirror of itself.
    Time: O(n)
    Space: O(h)
    """
    if not root:
        return True

    def is_mirror(t1, t2):
        if not t1 and not t2:
            return True
        if not t1 or not t2 or t1.val != t2.val:
            return False

        return is_mirror(t1.left, t2.right) and is_mirror(t1.right, t2.left)

    return is_mirror(root.left, root.right)
```

### 3. Subtree of Another Tree
**Difficulty:** Easy
**Concept:** Recursive matching

```python
def is_subtree(root: Optional[TreeNode], sub_root: Optional[TreeNode]) -> bool:
    """
    Checks if sub_root is a subtree of root.
    Time: O(m*n)
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

### 4. Flip Equivalent Binary Trees
**Difficulty:** Medium
**Concept:** Recursive flip or no-flip

```python
def flip_equiv(root1: Optional[TreeNode], root2: Optional[TreeNode]) -> bool:
    """
    Checks if two trees are flip equivalent.
    Time: O(n)
    Space: O(h)
    """
    if root1 is root2:
        return True
    if not root1 or not root2 or root1.val != root2.val:
        return False

    return (flip_equiv(root1.left, root2.left) and flip_equiv(root1.right, root2.right)) or \
           (flip_equiv(root1.left, root2.right) and flip_equiv(root1.right, root2.left))
```

### 5. Merge Two Binary Trees
**Difficulty:** Easy
**Concept:** Overlapping node merge

```python
def merge_trees(root1: Optional[TreeNode], root2: Optional[TreeNode]) -> Optional[TreeNode]:
    """
    Merges two binary trees.
    Time: O(min(n1, n2))
    Space: O(min(h1, h2))
    """
    if not root1:
        return root2
    if not root2:
        return root1

    root1.val += root2.val
    root1.left = merge_trees(root1.left, root2.left)
    root1.right = merge_trees(root1.right, root2.right)
    return root1
```

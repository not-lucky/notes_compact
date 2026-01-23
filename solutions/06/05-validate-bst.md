# Validate BST

## Practice Problems

### 1. Validate Binary Search Tree
**Difficulty:** Medium
**Concept:** Core validation

```python
from typing import Optional

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def is_valid_bst(root: Optional[TreeNode]) -> bool:
    """
    Validates a BST using range constraints.
    Time: O(n)
    Space: O(h)
    """
    def validate(node, low=float('-inf'), high=float('inf')):
        if not node:
            return True
        if not (low < node.val < high):
            return False
        return validate(node.left, low, node.val) and \
               validate(node.right, node.val, high)

    return validate(root)
```

### 2. Recover Binary Search Tree
**Difficulty:** Medium
**Concept:** Find and fix swapped nodes

```python
def recover_tree(root: Optional[TreeNode]) -> None:
    """
    Fixes a BST where exactly two nodes were swapped.
    Time: O(n)
    Space: O(h)
    """
    first = second = prev = None

    def inorder(node):
        nonlocal first, second, prev
        if not node: return

        inorder(node.left)

        if prev and node.val < prev.val:
            if not first:
                first = prev
            second = node
        prev = node

        inorder(node.right)

    inorder(root)
    if first and second:
        first.val, second.val = second.val, first.val
```

### 3. Largest BST Subtree
**Difficulty:** Medium
**Concept:** Validate subtrees

```python
def largest_bst_subtree(root: Optional[TreeNode]) -> int:
    """
    Finds the size of the largest subtree that is a BST.
    Time: O(n)
    Space: O(h)
    """
    res = 0
    def dfs(node):
        nonlocal res
        if not node:
            return float('inf'), float('-inf'), 0

        l_min, l_max, l_size = dfs(node.left)
        r_min, r_max, r_size = dfs(node.right)

        if l_max < node.val < r_min:
            size = l_size + r_size + 1
            res = max(res, size)
            return min(l_min, node.val), max(r_max, node.val), size

        return float('-inf'), float('inf'), 0

    dfs(root)
    return res
```

### 4. Minimum Distance Between BST Nodes
**Difficulty:** Easy
**Concept:** Inorder with gaps

```python
def min_diff_in_bst(root: Optional[TreeNode]) -> int:
    """
    Finds the minimum difference between any two nodes in a BST.
    Time: O(n)
    Space: O(h)
    """
    prev = None
    res = float('inf')

    def inorder(node):
        nonlocal prev, res
        if not node: return

        inorder(node.left)
        if prev is not None:
            res = min(res, node.val - prev)
        prev = node.val
        inorder(node.right)

    inorder(root)
    return int(res)
```

### 5. Two Sum IV - Input is a BST
**Difficulty:** Easy
**Concept:** BST traversal + two sum

```python
def find_target(root: Optional[TreeNode], k: int) -> bool:
    """
    Checks if there exist two nodes in the BST that sum to k.
    Time: O(n)
    Space: O(n)
    """
    seen = set()
    def dfs(node):
        if not node: return False
        if k - node.val in seen: return True
        seen.add(node.val)
        return dfs(node.left) or dfs(node.right)
    return dfs(root)
```

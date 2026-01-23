# BST Operations

## Practice Problems

### 1. Search in a Binary Search Tree
**Difficulty:** Easy
**Concept:** Basic search

```python
from typing import Optional

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def search_bst(root: Optional[TreeNode], val: int) -> Optional[TreeNode]:
    """
    Searches for a value in a BST.
    Time: O(h)
    Space: O(h)
    """
    if not root or root.val == val:
        return root

    if val < root.val:
        return search_bst(root.left, val)
    return search_bst(root.right, val)
```

### 2. Insert into a Binary Search Tree
**Difficulty:** Medium
**Concept:** Basic insert

```python
def insert_into_bst(root: Optional[TreeNode], val: int) -> Optional[TreeNode]:
    """
    Inserts a value into a BST.
    Time: O(h)
    Space: O(h)
    """
    if not root:
        return TreeNode(val)

    if val < root.val:
        root.left = insert_into_bst(root.left, val)
    else:
        root.right = insert_into_bst(root.right, val)
    return root
```

### 3. Delete Node in a BST
**Difficulty:** Medium
**Concept:** Delete with cases

```python
def delete_node(root: Optional[TreeNode], key: int) -> Optional[TreeNode]:
    """
    Deletes a node from a BST.
    Time: O(h)
    Space: O(h)
    """
    if not root:
        return None

    if key < root.val:
        root.left = delete_node(root.left, key)
    elif key > root.val:
        root.right = delete_node(root.right, key)
    else:
        # Case 1 & 2: Leaf or one child
        if not root.left: return root.right
        if not root.right: return root.left

        # Case 3: Two children - find inorder successor
        curr = root.right
        while curr.left:
            curr = curr.left
        root.val = curr.val
        root.right = delete_node(root.right, curr.val)

    return root
```

### 4. Inorder Successor in BST
**Difficulty:** Medium
**Concept:** Successor finding

```python
def inorder_successor(root: Optional[TreeNode], p: TreeNode) -> Optional[TreeNode]:
    """
    Finds the inorder successor of node p in a BST.
    Time: O(h)
    Space: O(1)
    """
    res = None
    while root:
        if p.val < root.val:
            res = root
            root = root.left
        else:
            root = root.right
    return res
```

### 5. Range Sum of BST
**Difficulty:** Easy
**Concept:** Range query

```python
def range_sum_bst(root: Optional[TreeNode], low: int, high: int) -> int:
    """
    Sums values of all nodes within [low, high].
    Time: O(n)
    Space: O(h)
    """
    if not root:
        return 0

    if root.val < low:
        return range_sum_bst(root.right, low, high)
    if root.val > high:
        return range_sum_bst(root.left, low, high)

    return root.val + range_sum_bst(root.left, low, high) + \
           range_sum_bst(root.right, low, high)
```

### 6. Closest Binary Search Tree Value
**Difficulty:** Easy
**Concept:** Floor/ceiling

```python
def closest_value(root: Optional[TreeNode], target: float) -> int:
    """
    Finds the value in the BST that is closest to the target.
    Time: O(h)
    Space: O(1)
    """
    closest = root.val
    while root:
        if abs(root.val - target) < abs(closest - target):
            closest = root.val
        root = root.left if target < root.val else root.right
    return closest
```

### 7. Trim a Binary Search Tree
**Difficulty:** Medium
**Concept:** Range pruning

```python
def trim_bst(root: Optional[TreeNode], low: int, high: int) -> Optional[TreeNode]:
    """
    Trims the tree so all its elements are in [low, high].
    Time: O(n)
    Space: O(h)
    """
    if not root:
        return None

    if root.val < low:
        return trim_bst(root.right, low, high)
    if root.val > high:
        return trim_bst(root.left, low, high)

    root.left = trim_bst(root.left, low, high)
    root.right = trim_bst(root.right, low, high)
    return root
```

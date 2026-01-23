# Tree Depth and Balance

## Practice Problems

### 1. Maximum Depth of Binary Tree
**Difficulty:** Easy
**Concept:** Simple recursion

```python
from typing import Optional

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def max_depth(root: Optional[TreeNode]) -> int:
    """
    Returns the maximum depth of a binary tree.
    Time: O(n)
    Space: O(h)
    """
    if not root:
        return 0
    return 1 + max(max_depth(root.left), max_depth(root.right))
```

### 2. Minimum Depth of Binary Tree
**Difficulty:** Easy
**Concept:** Shortest path to leaf

```python
from collections import deque

def min_depth(root: Optional[TreeNode]) -> int:
    """
    Returns the minimum depth of a binary tree using BFS for efficiency.
    Time: O(n)
    Space: O(w)
    """
    if not root:
        return 0

    queue = deque([(root, 1)])
    while queue:
        node, depth = queue.popleft()
        if not node.left and not node.right:
            return depth
        if node.left:
            queue.append((node.left, depth + 1))
        if node.right:
            queue.append((node.right, depth + 1))
    return 0
```

### 3. Balanced Binary Tree
**Difficulty:** Easy
**Concept:** Height check with early exit

```python
def is_balanced(root: Optional[TreeNode]) -> bool:
    """
    Checks if a binary tree is height-balanced.
    Time: O(n)
    Space: O(h)
    """
    def check(node):
        if not node:
            return 0

        left = check(node.left)
        if left == -1: return -1

        right = check(node.right)
        if right == -1: return -1

        if abs(left - right) > 1:
            return -1

        return 1 + max(left, right)

    return check(root) != -1
```

### 4. Count Complete Tree Nodes
**Difficulty:** Medium
**Concept:** O(log^2 n) count

```python
def count_nodes(root: Optional[TreeNode]) -> int:
    """
    Counts nodes in a complete binary tree.
    Time: O(log^2 n)
    Space: O(log n)
    """
    if not root:
        return 0

    def get_height(node):
        h = 0
        while node:
            h += 1
            node = node.left
        return h

    left_h = get_height(root.left)
    right_h = get_height(root.right)

    if left_h == right_h:
        return (1 << left_h) + count_nodes(root.right)
    else:
        return (1 << right_h) + count_nodes(root.left)
```

### 5. Check Completeness of a Binary Tree
**Difficulty:** Medium
**Concept:** BFS null check

```python
def is_complete_tree(root: Optional[TreeNode]) -> bool:
    """
    Checks if a binary tree is complete.
    Time: O(n)
    Space: O(w)
    """
    if not root:
        return True

    queue = deque([root])
    seen_null = False

    while queue:
        node = queue.popleft()
        if not node:
            seen_null = True
        else:
            if seen_null:
                return False
            queue.append(node.left)
            queue.append(node.right)

    return True
```

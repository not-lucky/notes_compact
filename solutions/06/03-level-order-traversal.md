# Level-Order Traversal (BFS)

## Practice Problems

### 1. Binary Tree Level Order Traversal
**Difficulty:** Medium
**Concept:** Basic level-order

```python
from typing import Optional, List
from collections import deque

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def level_order(root: Optional[TreeNode]) -> List[List[int]]:
    """
    Groups nodes level by level.
    Time: O(n)
    Space: O(w) - max width of tree
    """
    if not root: return []
    res = []
    queue = deque([root])
    while queue:
        level_size = len(queue)
        level = []
        for _ in range(level_size):
            node = queue.popleft()
            level.append(node.val)
            if node.left: queue.append(node.left)
            if node.right: queue.append(node.right)
        res.append(level)
    return res
```

### 2. Binary Tree Level Order Traversal II
**Difficulty:** Medium
**Concept:** Bottom-up

```python
def level_order_bottom(root: Optional[TreeNode]) -> List[List[int]]:
    """
    Returns level order from bottom to top.
    Time: O(n)
    Space: O(w)
    """
    if not root: return []
    res = deque()
    queue = deque([root])
    while queue:
        level_size = len(queue)
        level = []
        for _ in range(level_size):
            node = queue.popleft()
            level.append(node.val)
            if node.left: queue.append(node.left)
            if node.right: queue.append(node.right)
        res.appendleft(level)
    return list(res)
```

### 3. Binary Tree Zigzag Level Order Traversal
**Difficulty:** Medium
**Concept:** Alternating direction

```python
def zigzag_level_order(root: Optional[TreeNode]) -> List[List[int]]:
    """
    Traverses tree in zigzag order.
    Time: O(n)
    Space: O(w)
    """
    if not root: return []
    res = []
    queue = deque([root])
    left_to_right = True
    while queue:
        level_size = len(queue)
        level = deque()
        for _ in range(level_size):
            node = queue.popleft()
            if left_to_right:
                level.append(node.val)
            else:
                level.appendleft(node.val)
            if node.left: queue.append(node.left)
            if node.right: queue.append(node.right)
        res.append(list(level))
        left_to_right = not left_to_right
    return res
```

### 4. Binary Tree Right Side View
**Difficulty:** Medium
**Concept:** Last node per level

```python
def right_side_view(root: Optional[TreeNode]) -> List[int]:
    """
    Returns nodes visible from the right side.
    Time: O(n)
    Space: O(w)
    """
    if not root: return []
    res = []
    queue = deque([root])
    while queue:
        level_size = len(queue)
        for i in range(level_size):
            node = queue.popleft()
            if i == level_size - 1:
                res.append(node.val)
            if node.left: queue.append(node.left)
            if node.right: queue.append(node.right)
    return res
```

### 5. Average of Levels in Binary Tree
**Difficulty:** Easy
**Concept:** Level statistics

```python
def average_of_levels(root: Optional[TreeNode]) -> List[float]:
    """
    Calculates the average value of nodes at each level.
    Time: O(n)
    Space: O(w)
    """
    if not root: return []
    res = []
    queue = deque([root])
    while queue:
        level_size = len(queue)
        level_sum = 0
        for _ in range(level_size):
            node = queue.popleft()
            level_sum += node.val
            if node.left: queue.append(node.left)
            if node.right: queue.append(node.right)
        res.append(level_sum / level_size)
    return res
```

### 6. Maximum Width of Binary Tree
**Difficulty:** Medium
**Concept:** Position tracking

```python
def width_of_binary_tree(root: Optional[TreeNode]) -> int:
    """
    Finds the maximum width of the tree.
    Time: O(n)
    Space: O(w)
    """
    if not root: return 0
    max_w = 0
    queue = deque([(root, 0)])
    while queue:
        level_size = len(queue)
        _, start_idx = queue[0]
        _, end_idx = queue[-1]
        max_w = max(max_w, end_idx - start_idx + 1)
        for _ in range(level_size):
            node, idx = queue.popleft()
            if node.left: queue.append((node.left, 2 * idx))
            if node.right: queue.append((node.right, 2 * idx + 1))
    return max_w
```

### 7. Find Largest Value in Each Tree Row
**Difficulty:** Medium
**Concept:** Level max

```python
def largest_values(root: Optional[TreeNode]) -> List[int]:
    """
    Finds the largest value in each level.
    Time: O(n)
    Space: O(w)
    """
    if not root: return []
    res = []
    queue = deque([root])
    while queue:
        level_size = len(queue)
        max_val = float('-inf')
        for _ in range(level_size):
            node = queue.popleft()
            max_val = max(max_val, node.val)
            if node.left: queue.append(node.left)
            if node.right: queue.append(node.right)
        res.append(max_val)
    return res
```

### 8. Populating Next Right Pointers
**Difficulty:** Medium
**Concept:** Connect level nodes

```python
class Node:
    def __init__(self, val: int = 0, left: 'Node' = None, right: 'Node' = None, next: 'Node' = None):
        self.val = val
        self.left = left
        self.right = right
        self.next = next

def connect(root: Optional['Node']) -> Optional['Node']:
    """
    Connects nodes at the same level.
    Time: O(n)
    Space: O(1) for perfect binary tree (using next pointers)
    """
    if not root: return None
    leftmost = root
    while leftmost.left:
        head = leftmost
        while head:
            # Connection 1: within same parent
            head.left.next = head.right
            # Connection 2: between siblings
            if head.next:
                head.right.next = head.next.left
            head = head.next
        leftmost = leftmost.left
    return root
```

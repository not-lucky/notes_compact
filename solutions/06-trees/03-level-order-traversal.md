# Solution: Level-Order Traversal Practice Problems

## Problem 1: Binary Tree Level Order Traversal
### Problem Statement
Given the `root` of a binary tree, return the level order traversal of its nodes' values. (i.e., from left to right, level by level).

### Constraints
- The number of nodes in the tree is in the range `[0, 2000]`.
- `-1000 <= Node.val <= 1000`

### Example
Input: `root = [3,9,20,null,null,15,7]`
Output: `[[3],[9,20],[15,7]]`

### Python Implementation
```python
from collections import deque

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def levelOrder(root: TreeNode) -> list[list[int]]:
    """
    Time Complexity: O(n)
    Space Complexity: O(n)
    """
    if not root:
        return []

    res = []
    queue = deque([root])

    while queue:
        level = []
        for _ in range(len(queue)):
            node = queue.popleft()
            level.append(node.val)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        res.append(level)

    return res
```

---

## Problem 2: Binary Tree Level Order Traversal II
### Problem Statement
Given the `root` of a binary tree, return the bottom-up level order traversal of its nodes' values. (i.e., from left to right, level by level from leaf to root).

### Constraints
- The number of nodes in the tree is in the range `[0, 2000]`.
- `-1000 <= Node.val <= 1000`

### Example
Input: `root = [3,9,20,null,null,15,7]`
Output: `[[15,7],[9,20],[3]]`

### Python Implementation
```python
def levelOrderBottom(root: TreeNode) -> list[list[int]]:
    """
    Time Complexity: O(n)
    Space Complexity: O(n)
    """
    if not root:
        return []

    res = []
    queue = deque([root])

    while queue:
        level = []
        for _ in range(len(queue)):
            node = queue.popleft()
            level.append(node.val)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        res.append(level)

    return res[::-1]
```

---

## Problem 3: Binary Tree Zigzag Level Order Traversal
### Problem Statement
Given the `root` of a binary tree, return the zigzag level order traversal of its nodes' values. (i.e., from left to right, then right to left for the next level and alternate between).

### Constraints
- The number of nodes in the tree is in the range `[0, 2000]`.
- `-100 <= Node.val <= 100`

### Example
Input: `root = [3,9,20,null,null,15,7]`
Output: `[[3],[20,9],[15,7]]`

### Python Implementation
```python
def zigzagLevelOrder(root: TreeNode) -> list[list[int]]:
    """
    Time Complexity: O(n)
    Space Complexity: O(n)
    """
    if not root:
        return []

    res = []
    queue = deque([root])
    left_to_right = True

    while queue:
        level = deque()
        for _ in range(len(queue)):
            node = queue.popleft()
            if left_to_right:
                level.append(node.val)
            else:
                level.appendleft(node.val)

            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)

        res.append(list(level))
        left_to_right = not left_to_right

    return res
```

---

## Problem 4: Binary Tree Right Side View
### Problem Statement
Given the `root` of a binary tree, imagine yourself standing on the right side of it, return the values of the nodes you can see ordered from top to bottom.

### Constraints
- The number of nodes in the tree is in the range `[0, 100]`.
- `-100 <= Node.val <= 100`

### Example
Input: `root = [1,2,3,null,5,null,4]`
Output: `[1,3,4]`

### Python Implementation
```python
def rightSideView(root: TreeNode) -> list[int]:
    """
    Time Complexity: O(n)
    Space Complexity: O(n)
    """
    if not root:
        return []

    res = []
    queue = deque([root])

    while queue:
        level_size = len(queue)
        for i in range(level_size):
            node = queue.popleft()
            if i == level_size - 1:
                res.append(node.val)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)

    return res
```

---

## Problem 5: Average of Levels in Binary Tree
### Problem Statement
Given the `root` of a binary tree, return the average value of the nodes on each level in the form of an array. Answers within 10^-5 of the actual answer will be accepted.

### Constraints
- The number of nodes in the tree is in the range `[1, 10^4]`.
- `-2^31 <= Node.val <= 2^31 - 1`

### Example
Input: `root = [3,9,20,null,null,15,7]`
Output: `[3.00000,14.50000,11.00000]`

### Python Implementation
```python
def averageOfLevels(root: TreeNode) -> list[float]:
    """
    Time Complexity: O(n)
    Space Complexity: O(n)
    """
    res = []
    queue = deque([root])

    while queue:
        level_sum = 0
        count = len(queue)
        for _ in range(count):
            node = queue.popleft()
            level_sum += node.val
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        res.append(level_sum / count)

    return res
```

---

## Problem 6: Maximum Width of Binary Tree
### Problem Statement
Given the `root` of a binary tree, return the maximum width of the given tree.

The maximum width of a tree is the maximum width among all levels.

The width of one level is defined as the length between the end-nodes (the leftmost and rightmost non-null nodes), where the null nodes between the end-nodes that would be present in a complete binary tree extending down to that level are also counted into the length calculation.

### Constraints
- The number of nodes in the tree is in the range `[1, 3000]`.
- `-100 <= Node.val <= 100`

### Example
Input: `root = [1,3,2,5,3,null,9]`
Output: `4`

### Python Implementation
```python
def widthOfBinaryTree(root: TreeNode) -> int:
    """
    Time Complexity: O(n)
    Space Complexity: O(n)
    """
    if not root:
        return 0

    max_width = 0
    queue = deque([(root, 0)])

    while queue:
        level_size = len(queue)
        _, first_pos = queue[0]
        pos = 0

        for _ in range(level_size):
            node, pos = queue.popleft()
            if node.left:
                queue.append((node.left, 2 * pos))
            if node.right:
                queue.append((node.right, 2 * pos + 1))

        max_width = max(max_width, pos - first_pos + 1)

    return max_width
```

---

## Problem 7: Find Largest Value in Each Tree Row
### Problem Statement
Given the `root` of a binary tree, return an array of the largest value in each row of the tree (0-indexed).

### Constraints
- The number of nodes in the tree is in the range `[0, 10^4]`.
- `-2^31 <= Node.val <= 2^31 - 1`

### Example
Input: `root = [1,3,2,5,3,null,9]`
Output: `[1,3,9]`

### Python Implementation
```python
def largestValues(root: TreeNode) -> list[int]:
    """
    Time Complexity: O(n)
    Space Complexity: O(n)
    """
    if not root:
        return []

    res = []
    queue = deque([root])

    while queue:
        level_max = -float('inf')
        for _ in range(len(queue)):
            node = queue.popleft()
            level_max = max(level_max, node.val)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        res.append(level_max)

    return res
```

---

## Problem 8: Populating Next Right Pointers in Each Node
### Problem Statement
You are given a perfect binary tree where all leaves are on the same level, and every parent has two children. The binary tree has the following definition:

```python
class Node:
    def __init__(self, val=0, left=None, right=None, next=None):
        self.val = val
        self.left = left
        self.right = right
        self.next = next
```

Populate each next pointer to point to its next right node. If there is no next right node, the next pointer should be set to `NULL`.

### Constraints
- The number of nodes in the tree is in the range `[0, 2^12 - 1]`.
- `-1000 <= Node.val <= 1000`

### Example
Input: `root = [1,2,3,4,5,6,7]`
Output: `[1,#,2,3,#,4,5,6,7,#]`

### Python Implementation
```python
def connect(root: 'Node') -> 'Node':
    """
    Time Complexity: O(n)
    Space Complexity: O(n)
    """
    if not root:
        return None

    queue = deque([root])

    while queue:
        size = len(queue)
        for i in range(size):
            node = queue.popleft()
            if i < size - 1:
                node.next = queue[0]

            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)

    return root
```

# Solution: Tree Depth and Balance Practice Problems

## Problem 1: Maximum Depth of Binary Tree
### Problem Statement
Given the `root` of a binary tree, return its maximum depth.

A binary tree's maximum depth is the number of nodes along the longest path from the root node down to the farthest leaf node.

### Constraints
- The number of nodes in the tree is in the range `[0, 10^4]`.
- `-100 <= Node.val <= 100`

### Example
Input: `root = [3,9,20,null,null,15,7]`
Output: `3`

### Python Implementation
```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def maxDepth(root: TreeNode) -> int:
    """
    Time Complexity: O(n)
    Space Complexity: O(h)
    """
    if not root:
        return 0

    return 1 + max(maxDepth(root.left), maxDepth(root.right))
```

---

## Problem 2: Minimum Depth of Binary Tree
### Problem Statement
Given a binary tree, find its minimum depth.

The minimum depth is the number of nodes along the shortest path from the root node down to the nearest leaf node.

Note: A leaf is a node with no children.

### Constraints
- The number of nodes in the tree is in the range `[0, 10^5]`.
- `-1000 <= Node.val <= 1000`

### Example
Input: `root = [3,9,20,null,null,15,7]`
Output: `2`

### Python Implementation
```python
def minDepth(root: TreeNode) -> int:
    """
    Time Complexity: O(n)
    Space Complexity: O(h)
    """
    if not root:
        return 0

    if not root.left:
        return 1 + minDepth(root.right)
    if not root.right:
        return 1 + minDepth(root.left)

    return 1 + min(minDepth(root.left), minDepth(root.right))
```

---

## Problem 3: Balanced Binary Tree
### Problem Statement
Given a binary tree, determine if it is height-balanced.

For this problem, a height-balanced binary tree is defined as:
a binary tree in which the left and right subtrees of every node differ in height by no more than 1.

### Constraints
- The number of nodes in the tree is in the range `[0, 5000]`.
- `-10^4 <= Node.val <= 10^4`

### Example
Input: `root = [3,9,20,null,null,15,7]`
Output: `true`

### Python Implementation
```python
def isBalanced(root: TreeNode) -> bool:
    """
    Time Complexity: O(n)
    Space Complexity: O(h)
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

---

## Problem 4: Count Complete Tree Nodes
### Problem Statement
Given the `root` of a complete binary tree, return the number of the nodes in the tree.

Design an algorithm that runs in less than `O(n)` time complexity.

### Constraints
- The number of nodes in the tree is in the range `[0, 5 * 10^4]`.
- `0 <= Node.val <= 5 * 10^4`
- The tree is guaranteed to be complete.

### Example
Input: `root = [1,2,3,4,5,6]`
Output: `6`

### Python Implementation
```python
def countNodes(root: TreeNode) -> int:
    """
    Time Complexity: O(log^2 n)
    Space Complexity: O(log n)
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
        # Left subtree is perfect
        return (1 << left_h) + countNodes(root.right)
    else:
        # Right subtree is perfect (one level shorter)
        return (1 << right_h) + countNodes(root.left)
```

---

## Problem 5: Check Completeness of a Binary Tree
### Problem Statement
Given the `root` of a binary tree, determine if it is a complete binary tree.

### Constraints
- The number of nodes in the tree is in the range `[1, 100]`.
- `1 <= Node.val <= 1000`

### Example
Input: `root = [1,2,3,4,5,6]`
Output: `true`

### Python Implementation
```python
from collections import deque

def isCompleteTree(root: TreeNode) -> bool:
    """
    Time Complexity: O(n)
    Space Complexity: O(n)
    """
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

---

## Problem 6: Maximum Level Sum of a Binary Tree
### Problem Statement
Given the `root` of a binary tree, the level of its root is `1`, the level of its children is `2`, and so on.

Return the smallest level `x` such that the sum of all the values of nodes at level `x` is maximal.

### Constraints
- The number of nodes in the tree is in the range `[1, 10^4]`.
- `-10^5 <= Node.val <= 10^5`

### Example
Input: `root = [1,7,0,7,-8,null,null]`
Output: `2`

### Python Implementation
```python
def maxLevelSum(root: TreeNode) -> int:
    """
    Time Complexity: O(n)
    Space Complexity: O(n)
    """
    max_sum = -float('inf')
    max_level = 1
    curr_level = 1
    queue = deque([root])

    while queue:
        level_sum = 0
        for _ in range(len(queue)):
            node = queue.popleft()
            level_sum += node.val
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)

        if level_sum > max_sum:
            max_sum = level_sum
            max_level = curr_level

        curr_level += 1

    return max_level
```

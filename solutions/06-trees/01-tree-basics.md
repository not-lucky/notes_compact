# Solution: Tree Basics Practice Problems

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
    Space Complexity: O(h) where h is the height of the tree
    """
    if not root:
        return 0

    return 1 + max(maxDepth(root.left), maxDepth(root.right))
```

---

## Problem 2: Invert Binary Tree
### Problem Statement
Given the `root` of a binary tree, invert the tree, and return its root.

### Constraints
- The number of nodes in the tree is in the range `[0, 100]`.
- `-100 <= Node.val <= 100`

### Example
Input: `root = [4,2,7,1,3,6,9]`
Output: `[4,7,2,9,6,3,1]`

### Python Implementation
```python
def invertTree(root: TreeNode) -> TreeNode:
    """
    Time Complexity: O(n)
    Space Complexity: O(h)
    """
    if not root:
        return None

    root.left, root.right = invertTree(root.right), invertTree(root.left)
    return root
```

---

## Problem 3: Same Tree
### Problem Statement
Given the roots of two binary trees `p` and `q`, write a function to check if they are the same or not.

Two binary trees are considered the same if they are structurally identical, and the nodes have the same value.

### Constraints
- The number of nodes in both trees is in the range `[0, 100]`.
- `-10^4 <= Node.val <= 10^4`

### Example
Input: `p = [1,2,3], q = [1,2,3]`
Output: `true`

### Python Implementation
```python
def isSameTree(p: TreeNode, q: TreeNode) -> bool:
    """
    Time Complexity: O(min(N, M)) where N and M are nodes in trees
    Space Complexity: O(min(H1, H2))
    """
    if not p and not q:
        return True
    if not p or not q or p.val != q.val:
        return False

    return isSameTree(p.left, q.left) and isSameTree(p.right, q.right)
```

---

## Problem 4: Count Complete Tree Nodes
### Problem Statement
Given the `root` of a complete binary tree, return the number of the nodes in the tree.

According to Wikipedia, every level, except possibly the last, is completely filled in a complete binary tree, and all nodes in the last level are as far left as possible. It can have between 1 and 2^h nodes at the last level h.

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
    Time Complexity: O(log(n)^2)
    Space Complexity: O(log(n))
    """
    if not root:
        return 0

    def get_height(node, is_left):
        height = 0
        while node:
            height += 1
            node = node.left if is_left else node.right
        return height

    left_height = get_height(root, True)
    right_height = get_height(root, False)

    if left_height == right_height:
        return (2 ** left_height) - 1

    return 1 + countNodes(root.left) + countNodes(root.right)
```

---

## Problem 5: Subtree of Another Tree
### Problem Statement
Given the roots of two binary trees `root` and `subRoot`, return `true` if there is a subtree of `root` with the same structure and node values of `subRoot` and `false` otherwise.

A subtree of a binary tree `tree` is a tree that consists of a node in `tree` and all of this node's descendants. The tree `tree` could also be considered as a subtree of itself.

### Constraints
- The number of nodes in the `root` tree is in the range `[1, 2000]`.
- The number of nodes in the `subRoot` tree is in the range `[1, 1000]`.
- `-10^4 <= root.val <= 10^4`
- `-10^4 <= subRoot.val <= 10^4`

### Example
Input: `root = [3,4,5,1,2], subRoot = [4,1,2]`
Output: `true`

### Python Implementation
```python
def isSubtree(root: TreeNode, subRoot: TreeNode) -> bool:
    """
    Time Complexity: O(N * M)
    Space Complexity: O(H_root)
    """
    if not root:
        return False

    def isSame(p, q):
        if not p and not q:
            return True
        if not p or not q or p.val != q.val:
            return False
        return isSame(p.left, q.left) and isSame(p.right, q.right)

    if isSame(root, subRoot):
        return True

    return isSubtree(root.left, subRoot) or isSubtree(root.right, subRoot)
```

# Solution: Validate BST Practice Problems

## Problem 1: Validate Binary Search Tree
### Problem Statement
Given the `root` of a binary tree, determine if it is a valid binary search tree (BST).

A valid BST is defined as follows:
- The left subtree of a node contains only nodes with keys less than the node's key.
- The right subtree of a node contains only nodes with keys greater than the node's key.
- Both the left and right subtrees must also be binary search trees.

### Constraints
- The number of nodes in the tree is in the range `[1, 10^4]`.
- `-2^31 <= Node.val <= 2^31 - 1`

### Example
Input: `root = [2,1,3]`
Output: `true`

### Python Implementation
```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def isValidBST(root: TreeNode) -> bool:
    """
    Time Complexity: O(n)
    Space Complexity: O(h)
    """
    def validate(node, low, high):
        if not node:
            return True
        if not (low < node.val < high):
            return False
        return validate(node.left, low, node.val) and \
               validate(node.right, node.val, high)

    return validate(root, float('-inf'), float('inf'))
```

---

## Problem 2: Recover Binary Search Tree
### Problem Statement
You are given the `root` of a binary search tree (BST), where the values of exactly two nodes of the tree were swapped by mistake. Recover the tree without changing its structure.

### Constraints
- The number of nodes in the tree is in the range `[2, 1000]`.
- `-2^31 <= Node.val <= 2^31 - 1`

### Example
Input: `root = [1,3,null,null,2]`
Output: `[3,1,null,null,2]`

### Python Implementation
```python
def recoverTree(root: TreeNode) -> None:
    """
    Time Complexity: O(n)
    Space Complexity: O(h)
    Do not return anything, modify root in-place instead.
    """
    first = second = prev = None
    stack = []
    curr = root

    while stack or curr:
        while curr:
            stack.append(curr)
            curr = curr.left
        curr = stack.pop()

        if prev and curr.val < prev.val:
            if not first:
                first = prev
            second = curr

        prev = curr
        curr = curr.right

    first.val, second.val = second.val, first.val
```

---

## Problem 3: Largest BST Subtree
### Problem Statement
Given the root of a binary tree, find the largest subtree, which is also a Binary Search Tree (BST), where the largest means subtree has the maximum number of nodes.

A subtree is a tree that consists of a node in the tree and all of this node's descendants.

### Constraints
- The number of nodes in the tree is in the range `[0, 10^4]`.
- `-10^4 <= Node.val <= 10^4`

### Example
Input: `root = [10,5,15,1,8,null,7]`
Output: `3`
Explanation: The largest BST subtree is `[5,1,8]`.

### Python Implementation
```python
def largestBSTSubtree(root: TreeNode) -> int:
    """
    Time Complexity: O(n)
    Space Complexity: O(h)
    """
    def helper(node):
        if not node:
            return True, 0, float('inf'), float('-inf')

        is_left_bst, left_size, left_min, left_max = helper(node.left)
        is_right_bst, right_size, right_min, right_max = helper(node.right)

        if is_left_bst and is_right_bst and left_max < node.val < right_min:
            return True, 1 + left_size + right_size, min(node.val, left_min), max(node.val, right_max)

        return False, max(left_size, right_size), 0, 0

    return helper(root)[1]
```

---

## Problem 4: Minimum Distance Between BST Nodes
### Problem Statement
Given the `root` of a Binary Search Tree (BST), return the minimum difference between the values of any two different nodes in the tree.

### Constraints
- The number of nodes in the tree is in the range `[2, 100]`.
- `0 <= Node.val <= 10^5`

### Example
Input: `root = [4,2,6,1,3]`
Output: `1`

### Python Implementation
```python
def minDiffInBST(root: TreeNode) -> int:
    """
    Time Complexity: O(n)
    Space Complexity: O(h)
    """
    prev = None
    min_diff = float('inf')

    def inorder(node):
        nonlocal prev, min_diff
        if not node:
            return

        inorder(node.left)
        if prev is not None:
            min_diff = min(min_diff, node.val - prev)
        prev = node.val
        inorder(node.right)

    inorder(root)
    return min_diff
```

---

## Problem 5: Two Sum IV - Input is a BST
### Problem Statement
Given the `root` of a binary search tree and an integer `k`, return `true` if there exist two elements in the BST such that their sum is equal to `k`, or `false` otherwise.

### Constraints
- The number of nodes in the tree is in the range `[1, 10^4]`.
- `-10^4 <= Node.val <= 10^4`
- `root` is guaranteed to be a valid binary search tree.
- `-10^5 <= k <= 10^5`

### Example
Input: `root = [5,3,6,2,4,null,7], k = 9`
Output: `true`

### Python Implementation
```python
def findTarget(root: TreeNode, k: int) -> bool:
    """
    Time Complexity: O(n)
    Space Complexity: O(n)
    """
    seen = set()
    def dfs(node):
        if not node:
            return False
        if k - node.val in seen:
            return True
        seen.add(node.val)
        return dfs(node.left) or dfs(node.right)

    return dfs(root)
```

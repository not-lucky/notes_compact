# Solution: Symmetric Tree and Same Tree Practice Problems

## Problem 1: Same Tree
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
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def isSameTree(p: TreeNode, q: TreeNode) -> bool:
    """
    Time Complexity: O(n)
    Space Complexity: O(h)
    """
    if not p and not q:
        return True
    if not p or not q or p.val != q.val:
        return False

    return isSameTree(p.left, q.left) and isSameTree(p.right, q.right)
```

---

## Problem 2: Symmetric Tree
### Problem Statement
Given the `root` of a binary tree, check whether it is a mirror of itself (i.e., symmetric around its center).

### Constraints
- The number of nodes in the tree is in the range `[1, 1000]`.
- `-100 <= Node.val <= 100`

### Example
Input: `root = [1,2,2,3,4,4,3]`
Output: `true`

### Python Implementation
```python
def isSymmetric(root: TreeNode) -> bool:
    """
    Time Complexity: O(n)
    Space Complexity: O(h)
    """
    def isMirror(t1, t2):
        if not t1 and not t2:
            return True
        if not t1 or not t2:
            return False
        return t1.val == t2.val and \
               isMirror(t1.left, t2.right) and \
               isMirror(t1.right, t2.left)

    return isMirror(root.left, root.right) if root else True
```

---

## Problem 3: Subtree of Another Tree
### Problem Statement
Given the roots of two binary trees `root` and `subRoot`, return `true` if there is a subtree of `root` with the same structure and node values of `subRoot` and `false` otherwise.

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
    Time Complexity: O(M*N)
    Space Complexity: O(h)
    """
    def isSame(p, q):
        if not p and not q:
            return True
        if not p or not q or p.val != q.val:
            return False
        return isSame(p.left, q.left) and isSame(p.right, q.right)

    if not root:
        return False
    if isSame(root, subRoot):
        return True
    return isSubtree(root.left, subRoot) or isSubtree(root.right, subRoot)
```

---

## Problem 4: Invert Binary Tree
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

## Problem 5: Flip Equivalent Binary Trees
### Problem Statement
For a binary tree T, we can define a flip operation as follows: choose any node, and swap the left and right child subtrees.

Two binary trees X and Y are flip equivalent if they are equal after some number of flip operations.

Given the roots of two binary trees `root1` and `root2`, return `true` if the two trees are flip equivalent.

### Constraints
- The number of nodes in each tree is in the range `[0, 100]`.
- Each tree will have unique node values in the range `[0, 99]`.

### Example
Input: `root1 = [1,2,3,4,5,6,null,null,null,7,8], root2 = [1,3,2,null,6,4,5,null,null,null,null,8,7]`
Output: `true`

### Python Implementation
```python
def flipEquiv(root1: TreeNode, root2: TreeNode) -> bool:
    """
    Time Complexity: O(n)
    Space Complexity: O(h)
    """
    if root1 is root2:
        return True
    if not root1 or not root2 or root1.val != root2.val:
        return False

    return (flipEquiv(root1.left, root2.left) and flipEquiv(root1.right, root2.right) or
            flipEquiv(root1.left, root2.right) and flipEquiv(root1.right, root2.left))
```

---

## Problem 6: Merge Two Binary Trees
### Problem Statement
You are given two binary trees `root1` and `root2`.

Imagine that when you put one of them to cover the other, some nodes of the two trees are overlapped while the others are not. You need to merge the two trees into a new binary tree. The merge rule is that if two nodes overlap, then sum node values up as the new value of the merged node. Otherwise, the NOT null node will be used as the node of the new tree.

Return the merged tree.

Note: The merging process must start from the root nodes of both trees.

### Constraints
- The number of nodes in both trees is in the range `[0, 2000]`.
- `-10^4 <= Node.val <= 10^4`

### Example
Input: `root1 = [1,3,2,5], root2 = [2,1,3,null,4,null,7]`
Output: `[3,4,5,5,4,null,7]`

### Python Implementation
```python
def mergeTrees(root1: TreeNode, root2: TreeNode) -> TreeNode:
    """
    Time Complexity: O(n)
    Space Complexity: O(h)
    """
    if not root1:
        return root2
    if not root2:
        return root1

    root1.val += root2.val
    root1.left = mergeTrees(root1.left, root2.left)
    root1.right = mergeTrees(root1.right, root2.right)

    return root1
```

---

## Problem 7: Leaf-Similar Trees
### Problem Statement
Consider all the leaves of a binary tree, from left to right order, the values of those leaves form a leaf value sequence.

For example, in the given tree `[3,5,1,6,2,9,8,null,null,7,4]`, the leaf value sequence is `(6, 7, 4, 9, 8)`.

Two binary trees are considered leaf-similar if their leaf value sequence is the same.

Return `true` if and only if the two given trees with head nodes `root1` and `root2` are leaf-similar.

### Constraints
- The number of nodes in each tree will be in the range `[1, 200]`.
- Both of the given trees will have values between `0` and `200`.

### Example
Input: `root1 = [3,5,1,6,2,9,8,null,null,7,4], root2 = [3,5,1,6,7,4,2,null,null,null,null,null,null,9,8]`
Output: `true`

### Python Implementation
```python
def leafSimilar(root1: TreeNode, root2: TreeNode) -> bool:
    """
    Time Complexity: O(n)
    Space Complexity: O(n)
    """
    def get_leaves(node):
        if not node:
            return []
        if not node.left and not node.right:
            return [node.val]
        return get_leaves(node.left) + get_leaves(node.right)

    return get_leaves(root1) == get_leaves(root2)
```

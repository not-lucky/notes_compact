# Solution: BST Operations Practice Problems

## Problem 1: Search in a Binary Search Tree
### Problem Statement
You are given the `root` of a binary search tree (BST) and an integer `val`.

Find the node in the BST that the node's value equals `val` and return the subtree rooted with that node. If such a node does not exist, return `null`.

### Constraints
- The number of nodes in the tree is in the range `[1, 5000]`.
- `1 <= Node.val <= 10^7`
- `root` is a binary search tree.
- `1 <= val <= 10^7`

### Example
Input: `root = [4,2,7,1,3], val = 2`
Output: `[2,1,3]`

### Python Implementation
```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def searchBST(root: TreeNode, val: int) -> TreeNode:
    """
    Time Complexity: O(h)
    Space Complexity: O(h)
    """
    if not root or root.val == val:
        return root

    if val < root.val:
        return searchBST(root.left, val)
    return searchBST(root.right, val)
```

---

## Problem 2: Insert into a Binary Search Tree
### Problem Statement
You are given the `root` node of a binary search tree (BST) and a `value` to insert into the tree. Return the root node of the BST after the insertion. It is guaranteed that the new value does not exist in the original BST.

Notice that there may exist multiple valid ways for the insertion, as long as the tree remains a BST after insertion. You can return any of them.

### Constraints
- The number of nodes in the tree will be in the range `[0, 10^4]`.
- `-10^8 <= Node.val <= 10^8`
- All the values `Node.val` are unique.
- `-10^8 <= val <= 10^8`
- It's guaranteed that `val` does not exist in the original BST.

### Example
Input: `root = [4,2,7,1,3], val = 5`
Output: `[4,2,7,1,3,5]`

### Python Implementation
```python
def insertIntoBST(root: TreeNode, val: int) -> TreeNode:
    """
    Time Complexity: O(h)
    Space Complexity: O(h)
    """
    if not root:
        return TreeNode(val)

    if val < root.val:
        root.left = insertIntoBST(root.left, val)
    else:
        root.right = insertIntoBST(root.right, val)

    return root
```

---

## Problem 3: Delete Node in a BST
### Problem Statement
Given a root node reference of a BST and a key, delete the node with the given key in the BST. Return the root node reference (possibly updated) of the BST.

Basically, the deletion can be divided into two stages:
1. Search for a node to remove.
2. If the node is found, delete the node.

### Constraints
- The number of nodes in the tree is in the range `[0, 10^4]`.
- `-10^5 <= Node.val <= 10^5`
- Each node has a unique value.
- `root` is a valid binary search tree.
- `-10^5 <= key <= 10^5`

### Example
Input: `root = [5,3,6,2,4,null,7], key = 3`
Output: `[5,4,6,2,null,null,7]`

### Python Implementation
```python
def deleteNode(root: TreeNode, key: int) -> TreeNode:
    """
    Time Complexity: O(h)
    Space Complexity: O(h)
    """
    if not root:
        return None

    if key < root.val:
        root.left = deleteNode(root.left, key)
    elif key > root.val:
        root.right = deleteNode(root.right, key)
    else:
        # Node to be deleted found
        if not root.left:
            return root.right
        if not root.right:
            return root.left

        # Node has two children: get inorder successor
        successor = root.right
        while successor.left:
            successor = successor.left

        root.val = successor.val
        root.right = deleteNode(root.right, successor.val)

    return root
```

---

## Problem 4: Inorder Successor in BST
### Problem Statement
Given the `root` of a binary search tree and a node `p` in it, return the in-order successor of that node in the BST. If the given node has no in-order successor in the tree, return `null`.

The successor of a node `p` is the node with the smallest key greater than `p.val`.

### Constraints
- The number of nodes in the tree is in the range `[1, 10^4]`.
- `-10^5 <= Node.val <= 10^5`
- All `Node.val` are unique.

### Example
Input: `root = [2,1,3], p = 1`
Output: `2`

### Python Implementation
```python
def inorderSuccessor(root: TreeNode, p: TreeNode) -> TreeNode:
    """
    Time Complexity: O(h)
    Space Complexity: O(1)
    """
    successor = None
    while root:
        if p.val < root.val:
            successor = root
            root = root.left
        else:
            root = root.right
    return successor
```

---

## Problem 5: Range Sum of BST
### Problem Statement
Given the `root` node of a binary search tree and two integers `low` and `high`, return the sum of values of all nodes with a value in the inclusive range `[low, high]`.

### Constraints
- The number of nodes in the tree is in the range `[1, 2 * 10^4]`.
- `1 <= Node.val <= 10^5`
- `1 <= low <= high <= 10^5`
- All `Node.val` are unique.

### Example
Input: `root = [10,5,15,3,7,null,18], low = 7, high = 15`
Output: `32`

### Python Implementation
```python
def rangeSumBST(root: TreeNode, low: int, high: int) -> int:
    """
    Time Complexity: O(n)
    Space Complexity: O(h)
    """
    if not root:
        return 0

    if root.val < low:
        return rangeSumBST(root.right, low, high)
    if root.val > high:
        return rangeSumBST(root.left, low, high)

    return root.val + rangeSumBST(root.left, low, high) + rangeSumBST(root.right, low, high)
```

---

## Problem 6: Closest Binary Search Tree Value
### Problem Statement
Given the `root` of a binary search tree and a `target` value, return the value in the BST that is closest to the `target`. If there are multiple answers, print the smallest.

### Constraints
- The number of nodes in the tree is in the range `[1, 10^4]`.
- `0 <= Node.val <= 10^9`
- `-10^9 <= target <= 10^9`

### Example
Input: `root = [4,2,5,1,3], target = 3.714286`
Output: `4`

### Python Implementation
```python
def closestValue(root: TreeNode, target: float) -> int:
    """
    Time Complexity: O(h)
    Space Complexity: O(1)
    """
    closest = root.val
    while root:
        if abs(root.val - target) < abs(closest - target):
            closest = root.val
        elif abs(root.val - target) == abs(closest - target):
            closest = min(closest, root.val)

        root = root.left if target < root.val else root.right
    return closest
```

---

## Problem 7: Trim a Binary Search Tree
### Problem Statement
Given the `root` of a binary search tree and the lowest and highest boundaries as `low` and `high`, trim the tree so that all its elements lies in `[low, high]`. Trimming the tree should not change the relative structure of the elements that will remain in the tree (i.e., any node's descendant should remain a descendant). It can be proven that there is a unique answer.

Return the root of the trimmed binary search tree. Note that the root may change depending on the given boundaries.

### Constraints
- The number of nodes in the tree is in the range `[1, 10^4]`.
- `0 <= Node.val <= 10^4`
- The value of each node in the tree is unique.
- `root` is guaranteed to be a valid binary search tree.
- `0 <= low <= high <= 10^4`

### Example
Input: `root = [1,0,2], low = 1, high = 2`
Output: `[1,null,2]`

### Python Implementation
```python
def trimBST(root: TreeNode, low: int, high: int) -> TreeNode:
    """
    Time Complexity: O(n)
    Space Complexity: O(h)
    """
    if not root:
        return None

    if root.val < low:
        return trimBST(root.right, low, high)
    if root.val > high:
        return trimBST(root.left, low, high)

    root.left = trimBST(root.left, low, high)
    root.right = trimBST(root.right, low, high)
    return root
```

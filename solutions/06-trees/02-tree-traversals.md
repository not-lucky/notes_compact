# Solution: Tree Traversals Practice Problems

## Problem 1: Binary Tree Inorder Traversal
### Problem Statement
Given the `root` of a binary tree, return the inorder traversal of its nodes' values.

### Constraints
- The number of nodes in the tree is in the range `[0, 100]`.
- `-100 <= Node.val <= 100`

### Example
Input: `root = [1,null,2,3]`
Output: `[1,3,2]`

### Python Implementation
```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def inorderTraversal(root: TreeNode) -> list[int]:
    """
    Time Complexity: O(n)
    Space Complexity: O(h)
    """
    res = []
    def traverse(node):
        if not node:
            return
        traverse(node.left)
        res.append(node.val)
        traverse(node.right)
    traverse(root)
    return res
```

---

## Problem 2: Binary Tree Preorder Traversal
### Problem Statement
Given the `root` of a binary tree, return the preorder traversal of its nodes' values.

### Constraints
- The number of nodes in the tree is in the range `[0, 100]`.
- `-100 <= Node.val <= 100`

### Example
Input: `root = [1,null,2,3]`
Output: `[1,2,3]`

### Python Implementation
```python
def preorderTraversal(root: TreeNode) -> list[int]:
    """
    Time Complexity: O(n)
    Space Complexity: O(h)
    """
    res = []
    def traverse(node):
        if not node:
            return
        res.append(node.val)
        traverse(node.left)
        traverse(node.right)
    traverse(root)
    return res
```

---

## Problem 3: Binary Tree Postorder Traversal
### Problem Statement
Given the `root` of a binary tree, return the postorder traversal of its nodes' values.

### Constraints
- The number of nodes in the tree is in the range `[0, 100]`.
- `-100 <= Node.val <= 100`

### Example
Input: `root = [1,null,2,3]`
Output: `[3,2,1]`

### Python Implementation
```python
def postorderTraversal(root: TreeNode) -> list[int]:
    """
    Time Complexity: O(n)
    Space Complexity: O(h)
    """
    res = []
    def traverse(node):
        if not node:
            return
        traverse(node.left)
        traverse(node.right)
        res.append(node.val)
    traverse(root)
    return res
```

---

## Problem 4: Kth Smallest Element in BST
### Problem Statement
Given the `root` of a binary search tree, and an integer `k`, return the `k`th smallest value (1-indexed) of all the values of the nodes in the tree.

### Constraints
- The number of nodes in the tree is `n`.
- `1 <= k <= n <= 10^4`
- `0 <= Node.val <= 10^4`

### Example
Input: `root = [3,1,4,null,2], k = 1`
Output: `1`

### Python Implementation
```python
def kthSmallest(root: TreeNode, k: int) -> int:
    """
    Time Complexity: O(h + k)
    Space Complexity: O(h)
    """
    stack = []
    while True:
        while root:
            stack.append(root)
            root = root.left
        root = stack.pop()
        k -= 1
        if k == 0:
            return root.val
        root = root.right
```

---

## Problem 5: Validate Binary Search Tree
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
def isValidBST(root: TreeNode) -> bool:
    """
    Time Complexity: O(n)
    Space Complexity: O(h)
    """
    def validate(node, low=-float('inf'), high=float('inf')):
        if not node:
            return True
        if not (low < node.val < high):
            return False

        return validate(node.left, low, node.val) and \
               validate(node.right, node.val, high)

    return validate(root)
```

---

## Problem 6: Flatten Binary Tree to Linked List
### Problem Statement
Given the `root` of a binary tree, flatten the tree into a "linked list":
- The "linked list" should use the same `TreeNode` class where the `right` child pointer points to the next node in the list and the `left` child pointer is always `null`.
- The "linked list" should be in the same order as a pre-order traversal of the binary tree.

### Constraints
- The number of nodes in the tree is in the range `[0, 2000]`.
- `-100 <= Node.val <= 100`

### Example
Input: `root = [1,2,5,3,4,null,6]`
Output: `[1,null,2,null,3,null,4,null,5,null,6]`

### Python Implementation
```python
def flatten(root: TreeNode) -> None:
    """
    Time Complexity: O(n)
    Space Complexity: O(h)
    Do not return anything, modify root in-place instead.
    """
    curr = root
    while curr:
        if curr.left:
            # Find the rightmost node of the left subtree
            prev = curr.left
            while prev.right:
                prev = prev.right

            # Connect the original right subtree to the right of prev
            prev.right = curr.right
            # Move the left subtree to the right
            curr.right = curr.left
            curr.left = None

        # Move to the next node on the right
        curr = curr.right
```

---

## Problem 7: Construct Binary Tree from Preorder and Inorder
### Problem Statement
Given two integer arrays `preorder` and `inorder` where `preorder` is the preorder traversal of a binary tree and `inorder` is the inorder traversal of the same tree, construct and return the binary tree.

### Constraints
- `1 <= preorder.length <= 3000`
- `inorder.length == preorder.length`
- `-3000 <= preorder[i], inorder[i] <= 3000`
- `preorder` and `inorder` consist of unique values.
- Each value of `inorder` also appears in `preorder`.
- `preorder` is guaranteed to be the preorder traversal of the tree.
- `inorder` is guaranteed to be the inorder traversal of the tree.

### Example
Input: `preorder = [3,9,20,15,7], inorder = [9,3,15,20,7]`
Output: `[3,9,20,null,null,15,7]`

### Python Implementation
```python
def buildTree(preorder: list[int], inorder: list[int]) -> TreeNode:
    """
    Time Complexity: O(n)
    Space Complexity: O(n)
    """
    idx_map = {val: i for i, val in enumerate(inorder)}
    pre_idx = 0

    def helper(in_left, in_right):
        nonlocal pre_idx
        if in_left > in_right:
            return None

        val = preorder[pre_idx]
        root = TreeNode(val)
        pre_idx += 1

        index = idx_map[val]

        root.left = helper(in_left, index - 1)
        root.right = helper(index + 1, in_right)
        return root

    return helper(0, len(inorder) - 1)
```

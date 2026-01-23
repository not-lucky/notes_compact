# Solution: Tree Construction Practice Problems

## Problem 1: Construct Binary Tree from Preorder and Inorder Traversal
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
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

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

---

## Problem 2: Construct Binary Tree from Inorder and Postorder Traversal
### Problem Statement
Given two integer arrays `inorder` and `postorder` where `inorder` is the inorder traversal of a binary tree and `postorder` is the postorder traversal of the same tree, construct and return the binary tree.

### Constraints
- `1 <= inorder.length <= 3000`
- `postorder.length == inorder.length`
- `-3000 <= inorder[i], postorder[i] <= 3000`
- `inorder` and `postorder` consist of unique values.
- Each value of `postorder` also appears in `inorder`.
- `inorder` is guaranteed to be the inorder traversal of the tree.
- `postorder` is guaranteed to be the postorder traversal of the tree.

### Example
Input: `inorder = [9,3,15,20,7], postorder = [9,15,7,20,3]`
Output: `[3,9,20,null,null,15,7]`

### Python Implementation
```python
def buildTree(inorder: list[int], postorder: list[int]) -> TreeNode:
    """
    Time Complexity: O(n)
    Space Complexity: O(n)
    """
    idx_map = {val: i for i, val in enumerate(inorder)}

    def helper(in_left, in_right):
        if in_left > in_right:
            return None

        val = postorder.pop()
        root = TreeNode(val)

        index = idx_map[val]

        # Right subtree first because we are popping from postorder end
        root.right = helper(index + 1, in_right)
        root.left = helper(in_left, index - 1)
        return root

    return helper(0, len(inorder) - 1)
```

---

## Problem 3: Construct Binary Search Tree from Preorder Traversal
### Problem Statement
Given an array of integers `preorder`, which represents the preorder traversal of a BST (i.e., binary search tree), construct the tree and return its root.

It is guaranteed that there is always possible to find a binary search tree with the given requirements for the given test cases.

A binary search tree is a binary tree where for every node, any descendant of `Node.left` has a value `< Node.val`, and any descendant of `Node.right` has a value `> Node.val`.

A preorder traversal of a binary tree displays the value of the node first, then traverses `Node.left`, then traverses `Node.right`.

### Constraints
- `1 <= preorder.length <= 100`
- `1 <= preorder[i] <= 1000`
- All the values of `preorder` are unique.

### Example
Input: `preorder = [8,5,1,7,10,12]`
Output: `[8,5,10,1,7,null,12]`

### Python Implementation
```python
def bstFromPreorder(preorder: list[int]) -> TreeNode:
    """
    Time Complexity: O(n)
    Space Complexity: O(h)
    """
    idx = 0
    def helper(lower=float('-inf'), upper=float('inf')):
        nonlocal idx
        if idx == len(preorder):
            return None

        val = preorder[idx]
        if val < lower or val > upper:
            return None

        idx += 1
        root = TreeNode(val)
        root.left = helper(lower, val)
        root.right = helper(val, upper)
        return root

    return helper()
```

---

## Problem 4: Convert Sorted Array to Binary Search Tree
### Problem Statement
Given an integer array `nums` where the elements are sorted in ascending order, convert it to a height-balanced binary search tree.

### Constraints
- `1 <= nums.length <= 10^4`
- `-10^4 <= nums[i] <= 10^4`
- `nums` is sorted in a strictly increasing order.

### Example
Input: `nums = [-10,-3,0,5,9]`
Output: `[0,-3,9,-10,null,5]`

### Python Implementation
```python
def sortedArrayToBST(nums: list[int]) -> TreeNode:
    """
    Time Complexity: O(n)
    Space Complexity: O(log n)
    """
    def helper(left, right):
        if left > right:
            return None

        mid = (left + right) // 2
        root = TreeNode(nums[mid])
        root.left = helper(left, mid - 1)
        root.right = helper(mid + 1, right)
        return root

    return helper(0, len(nums) - 1)
```

---

## Problem 5: Maximum Binary Tree
### Problem Statement
You are given an integer array `nums` with no duplicates. A maximum binary tree can be built recursively from `nums` using the following algorithm:
1. Create a root node whose value is the maximum value in `nums`.
2. Recursively build the left subtree on the subarray prefix to the left of the maximum value.
3. Recursively build the right subtree on the subarray suffix to the right of the maximum value.

Return the maximum binary tree built from `nums`.

### Constraints
- `1 <= nums.length <= 1000`
- `0 <= nums[i] <= 1000`
- All integers in `nums` are unique.

### Example
Input: `nums = [3,2,1,6,0,5]`
Output: `[6,3,5,null,2,0,null,null,1]`

### Python Implementation
```python
def constructMaximumBinaryTree(nums: list[int]) -> TreeNode:
    """
    Time Complexity: O(n^2) - can be O(n) with monotonic stack
    Space Complexity: O(n)
    """
    if not nums:
        return None

    max_val = max(nums)
    idx = nums.index(max_val)

    root = TreeNode(max_val)
    root.left = constructMaximumBinaryTree(nums[:idx])
    root.right = constructMaximumBinaryTree(nums[idx+1:])

    return root
```

---

## Problem 6: Convert Sorted List to Binary Search Tree
### Problem Statement
Given the `head` of a singly linked list where elements are sorted in ascending order, convert it to a height-balanced binary search tree.

### Constraints
- The number of nodes in `head` is in the range `[0, 2 * 10^4]`.
- `-10^5 <= Node.val <= 10^5`

### Example
Input: `head = [-10,-3,0,5,9]`
Output: `[0,-3,9,-10,null,5]`

### Python Implementation
```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def sortedListToBST(head: ListNode) -> TreeNode:
    """
    Time Complexity: O(n log n)
    Space Complexity: O(log n)
    """
    if not head:
        return None
    if not head.next:
        return TreeNode(head.val)

    # Find middle element using slow and fast pointers
    prev = None
    slow = fast = head
    while fast and fast.next:
        prev = slow
        slow = slow.next
        fast = fast.next.next

    # slow is now the middle element
    # Disconnect the left part from the middle
    if prev:
        prev.next = None

    root = TreeNode(slow.val)
    root.left = sortedListToBST(head)
    root.right = sortedListToBST(slow.next)

    return root
```

# Tree Construction

## Practice Problems

### 1. Construct Binary Tree from Preorder and Inorder Traversal
**Difficulty:** Medium
**Concept:** Classic construction

```python
from typing import List, Optional

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def build_tree(preorder: List[int], inorder: List[int]) -> Optional[TreeNode]:
    """
    Builds a binary tree from preorder and inorder traversals.
    Time: O(n) - with hashmap for inorder lookups
    Space: O(n) - hashmap and recursion stack
    """
    inorder_map = {val: i for i, val in enumerate(inorder)}
    pre_idx = 0

    def build(left: int, right: int) -> Optional[TreeNode]:
        nonlocal pre_idx
        if left > right:
            return None

        root_val = preorder[pre_idx]
        root = TreeNode(root_val)
        pre_idx += 1

        mid = inorder_map[root_val]
        root.left = build(left, mid - 1)
        root.right = build(mid + 1, right)
        return root

    return build(0, len(inorder) - 1)
```

### 2. Construct Binary Tree from Inorder and Postorder Traversal
**Difficulty:** Medium
**Concept:** Similar approach

```python
def build_tree_post(inorder: List[int], postorder: List[int]) -> Optional[TreeNode]:
    """
    Builds a binary tree from inorder and postorder traversals.
    Time: O(n)
    Space: O(n)
    """
    inorder_map = {val: i for i, val in enumerate(inorder)}
    post_idx = len(postorder) - 1

    def build(left: int, right: int) -> Optional[TreeNode]:
        nonlocal post_idx
        if left > right:
            return None

        root_val = postorder[post_idx]
        root = TreeNode(root_val)
        post_idx -= 1

        mid = inorder_map[root_val]
        # In postorder, we process right before left
        root.right = build(mid + 1, right)
        root.left = build(left, mid - 1)
        return root

    return build(0, len(inorder) - 1)
```

### 3. Construct Binary Search Tree from Preorder Traversal
**Difficulty:** Medium
**Concept:** BST bounds

```python
def bst_from_preorder(preorder: List[int]) -> Optional[TreeNode]:
    """
    Constructs a BST from preorder traversal.
    Time: O(n)
    Space: O(h)
    """
    idx = 0

    def build(upper_bound: float) -> Optional[TreeNode]:
        nonlocal idx
        if idx == len(preorder) or preorder[idx] > upper_bound:
            return None

        root = TreeNode(preorder[idx])
        idx += 1
        root.left = build(root.val)
        root.right = build(upper_bound)
        return root

    return build(float('inf'))
```

### 4. Convert Sorted Array to Binary Search Tree
**Difficulty:** Easy
**Concept:** Balanced BST

```python
def sorted_array_to_bst(nums: List[int]) -> Optional[TreeNode]:
    """
    Converts a sorted array to a height-balanced BST.
    Time: O(n)
    Space: O(log n)
    """
    def build(left: int, right: int) -> Optional[TreeNode]:
        if left > right:
            return None

        mid = (left + right) // 2
        root = TreeNode(nums[mid])
        root.left = build(left, mid - 1)
        root.right = build(mid + 1, right)
        return root

    return build(0, len(nums) - 1)
```

### 5. Maximum Binary Tree
**Difficulty:** Medium
**Concept:** Max element root

```python
def construct_maximum_binary_tree(nums: List[int]) -> Optional[TreeNode]:
    """
    Builds a tree where the root is the maximum element in the range.
    Time: O(n^2) average, O(n) with monotonic stack
    Space: O(n)
    """
    if not nums:
        return None

    max_val = max(nums)
    max_idx = nums.index(max_val)

    root = TreeNode(max_val)
    root.left = construct_maximum_binary_tree(nums[:max_idx])
    root.right = construct_maximum_binary_tree(nums[max_idx + 1:])
    return root
```

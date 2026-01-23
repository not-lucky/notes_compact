# Tree Traversals

## Practice Problems

### 1. Binary Tree Inorder Traversal
**Difficulty:** Easy
**Concept:** Basic inorder

```python
from typing import Optional, List

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def inorder_traversal(root: Optional[TreeNode]) -> List[int]:
    """
    Inorder traversal: Left -> Root -> Right
    Time: O(n)
    Space: O(h)
    """
    res = []
    def traverse(node):
        if not node: return
        traverse(node.left)
        res.append(node.val)
        traverse(node.right)
    traverse(root)
    return res
```

### 2. Binary Tree Preorder Traversal
**Difficulty:** Easy
**Concept:** Basic preorder

```python
def preorder_traversal(root: Optional[TreeNode]) -> List[int]:
    """
    Preorder traversal: Root -> Left -> Right
    Time: O(n)
    Space: O(h)
    """
    res = []
    def traverse(node):
        if not node: return
        res.append(node.val)
        traverse(node.left)
        traverse(node.right)
    traverse(root)
    return res
```

### 3. Binary Tree Postorder Traversal
**Difficulty:** Easy
**Concept:** Basic postorder

```python
def postorder_traversal(root: Optional[TreeNode]) -> List[int]:
    """
    Postorder traversal: Left -> Right -> Root
    Time: O(n)
    Space: O(h)
    """
    res = []
    def traverse(node):
        if not node: return
        traverse(node.left)
        traverse(node.right)
        res.append(node.val)
    traverse(root)
    return res
```

### 4. Kth Smallest Element in BST
**Difficulty:** Medium
**Concept:** Inorder + counting

```python
def kth_smallest(root: Optional[TreeNode], k: int) -> int:
    """
    Finds the kth smallest element in a BST.
    Time: O(h + k)
    Space: O(h)
    """
    stack = []
    curr = root
    while curr or stack:
        while curr:
            stack.append(curr)
            curr = curr.left
        curr = stack.pop()
        k -= 1
        if k == 0: return curr.val
        curr = curr.right
    return -1
```

### 5. Validate Binary Search Tree
**Difficulty:** Medium
**Concept:** Inorder sorted check

```python
def is_valid_bst(root: Optional[TreeNode]) -> bool:
    """
    Validates if a tree is a valid BST.
    Time: O(n)
    Space: O(h)
    """
    def validate(node, low=float('-inf'), high=float('inf')):
        if not node: return True
        if not (low < node.val < high): return False
        return validate(node.left, low, node.val) and \
               validate(node.right, node.val, high)
    return validate(root)
```

### 6. Flatten Binary Tree to Linked List
**Difficulty:** Medium
**Concept:** Preorder modification

```python
def flatten(root: Optional[TreeNode]) -> None:
    """
    Flattens a binary tree to a "linked list" in-place (right child only).
    Time: O(n)
    Space: O(h)
    """
    curr = root
    while curr:
        if curr.left:
            # Find the rightmost node in the left subtree
            pre = curr.left
            while pre.right:
                pre = pre.right
            # Attach the original right subtree to the right of the rightmost node
            pre.right = curr.right
            # Move the left subtree to the right
            curr.right = curr.left
            curr.left = None
        curr = curr.right
```

### 7. Construct Binary Tree from Preorder and Inorder
**Difficulty:** Medium
**Concept:** Tree construction

```python
def build_tree(preorder: List[int], inorder: List[int]) -> Optional[TreeNode]:
    """
    Builds a binary tree from preorder and inorder traversals.
    Time: O(n)
    Space: O(n)
    """
    if not preorder or not inorder: return None

    root_val = preorder[0]
    root = TreeNode(root_val)
    mid = inorder.index(root_val)

    root.left = build_tree(preorder[1:mid+1], inorder[:mid])
    root.right = build_tree(preorder[mid+1:], inorder[mid+1:])
    return root
```

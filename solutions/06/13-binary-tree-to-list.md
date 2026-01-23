# Binary Tree to Linked List Conversions

## Practice Problems

### 1. Flatten Binary Tree to Linked List
**Difficulty:** Medium
**Concept:** Preorder flatten in-place

```python
from typing import Optional

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def flatten(root: Optional[TreeNode]) -> None:
    """
    Flattens a binary tree to a "linked list" using preorder traversal.
    Time: O(n)
    Space: O(1) - Morris-like approach
    """
    curr = root
    while curr:
        if curr.left:
            # Find the rightmost node in the left subtree
            pre = curr.left
            while pre.right:
                pre = pre.right
            # Attach the original right subtree
            pre.right = curr.right
            # Move the left subtree to the right
            curr.right = curr.left
            curr.left = None
        curr = curr.right
```

### 2. Convert BST to Sorted Doubly Linked List
**Difficulty:** Medium
**Concept:** Inorder traversal linking

```python
def tree_to_doubly_list(root: Optional[TreeNode]) -> Optional[TreeNode]:
    """
    Converts a BST to a circular doubly linked list in sorted order.
    Time: O(n)
    Space: O(h)
    """
    if not root:
        return None

    first = last = None

    def inorder(node):
        nonlocal first, last
        if not node:
            return

        inorder(node.left)

        if last:
            last.right = node
            node.left = last
        else:
            first = node
        last = node

        inorder(node.right)

    inorder(root)
    # Make it circular
    last.right = first
    first.left = last
    return first
```

### 3. Convert Sorted List to Binary Search Tree
**Difficulty:** Medium
**Concept:** Slow/fast pointer middle root

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def sorted_list_to_bst(head: Optional[ListNode]) -> Optional[TreeNode]:
    """
    Converts a sorted linked list to a balanced BST.
    Time: O(n log n)
    Space: O(log n)
    """
    if not head:
        return None
    if not head.next:
        return TreeNode(head.val)

    # Find middle
    prev = None
    slow = fast = head
    while fast and fast.next:
        prev = slow
        slow = slow.next
        fast = fast.next.next

    # Break link
    if prev:
        prev.next = None

    root = TreeNode(slow.val)
    root.left = sorted_list_to_bst(head if prev else None)
    root.right = sorted_list_to_bst(slow.next)
    return root
```

### 4. Increasing Order Search Tree
**Difficulty:** Easy
**Concept:** Inorder traversal linking

```python
def increasing_bst(root: Optional[TreeNode]) -> Optional[TreeNode]:
    """
    Rearranges BST so nodes have only right children in sorted order.
    Time: O(n)
    Space: O(h)
    """
    dummy = TreeNode(0)
    curr = dummy

    def inorder(node):
        nonlocal curr
        if not node:
            return

        inorder(node.left)

        # Process current node
        node.left = None
        curr.right = node
        curr = node

        inorder(node.right)

    inorder(root)
    return dummy.right
```

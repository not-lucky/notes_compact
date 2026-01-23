# Solution: Binary Tree to Linked List Practice Problems

## Problem 1: Flatten Binary Tree to Linked List
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
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def flatten(root: TreeNode) -> None:
    """
    Time Complexity: O(n)
    Space Complexity: O(1)
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

## Problem 2: Convert BST to Sorted Doubly Linked List
### Problem Statement
Convert a Binary Search Tree to a sorted Circular Doubly Linked List in place.

You can think of the left and right pointers as synonymous to the predecessor and successor pointers in a doubly-linked list. For a circular doubly linked list, the predecessor of the first element is the last element, and the successor of the last element is the first element.

### Constraints
- The number of nodes in the tree is in the range `[0, 2000]`.
- `-1000 <= Node.val <= 1000`

### Python Implementation
```python
def treeToDoublyList(root: TreeNode) -> TreeNode:
    """
    Time Complexity: O(n)
    Space Complexity: O(h)
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
    last.right = first
    first.left = last

    return first
```

---

## Problem 3: Convert Sorted List to Binary Search Tree
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

---

## Problem 4: Increasing Order Search Tree
### Problem Statement
Given the `root` of a binary search tree, rearrange the tree in in-order so that the leftmost node in the tree is now the root of the tree, and every node has no left child and only one right child.

### Constraints
- The number of nodes in the given tree will be in the range `[1, 100]`.
- `0 <= Node.val <= 1000`

### Example
Input: `root = [5,3,6,2,4,null,8,1,null,null,null,7,9]`
Output: `[1,null,2,null,3,null,4,null,5,null,6,null,7,null,8,null,9]`

### Python Implementation
```python
def increasingBST(root: TreeNode) -> TreeNode:
    """
    Time Complexity: O(n)
    Space Complexity: O(h)
    """
    dummy = TreeNode(0)
    curr = dummy

    def inorder(node):
        nonlocal curr
        if not node:
            return

        inorder(node.left)

        node.left = None
        curr.right = node
        curr = node

        inorder(node.right)

    inorder(root)
    return dummy.right
```

---

## Problem 5: Flatten a Multilevel Doubly Linked List
### Problem Statement
You are given a doubly linked list, which contains nodes that have a next pointer, a previous pointer, and an additional child pointer. This child pointer may or may not point to a separate doubly linked list, also containing these special nodes. These child lists may have one or more children of their own, and so on, to produce a multilevel data structure as shown in the example below.

Given the head of the first level of the list, flatten the list so that all the nodes appear in a single-level, doubly linked list. Let curr be a node with a child list. The nodes in the child list should appear after curr and before curr.next in the flattened list.

Return the head of the flattened list. The nodes in the list must have all of their child pointers set to NULL.

### Constraints
- The number of nodes in the list will be in the range `[0, 1000]`.
- `1 <= Node.val <= 10^5`

### Python Implementation
```python
class Node:
    def __init__(self, val, prev, next, child):
        self.val = val
        self.prev = prev
        self.next = next
        self.child = child

def flatten(head: 'Node') -> 'Node':
    """
    Time Complexity: O(n)
    Space Complexity: O(h)
    """
    if not head:
        return None

    def dfs(node):
        curr = node
        last = node
        while curr:
            next_node = curr.next
            if curr.child:
                child_head = curr.child
                child_tail = dfs(curr.child)

                curr.next = child_head
                child_head.prev = curr

                if next_node:
                    child_tail.next = next_node
                    next_node.prev = child_tail

                curr.child = None
                last = child_tail
            else:
                last = curr
            curr = next_node
        return last

    dfs(head)
    return head
```

# Binary Tree to Linked List Conversions

> **Prerequisites:** [02-tree-traversals](./02-tree-traversals.md), [04-linked-lists](../04-linked-lists/README.md)

## Interview Context

Tree-to-list conversions are important because:

1. **Tests multiple concepts**: Trees, linked lists, and pointer manipulation
2. **In-place requirements**: Often asked to do without extra space
3. **Multiple variations**: Flatten to preorder, BST to sorted list, etc.
4. **Classic interview problem**: "Flatten Binary Tree to Linked List" is very common

Common at Google, Meta, and Microsoft interviews.

---

## Flatten Binary Tree to Linked List (Preorder)

Convert tree to linked list following **preorder** traversal. Use right pointers only.

```text
     1               1
    / \               \
   2   5      →        2
  / \   \               \
 3   4   6               3
                          \
                           4
                            \
                             5
                              \
                               6
```

### Approach 1: Recursive (Post-processing)

```python
from typing import Optional

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def flatten(root: Optional[TreeNode]) -> None:
    r"""
    Flatten tree to linked list in-place (preorder).

    LeetCode 114: Flatten Binary Tree to Linked List

    Time: $\mathcal{O}(N)$
    Space: $\mathcal{O}(H)$ for the recursive call stack
    """
    if not root:
        return

    # Recursively flatten left and right subtrees
    flatten(root.left)
    flatten(root.right)

    # Save right subtree
    right_subtree = root.right

    # Move left subtree to right
    root.right = root.left
    root.left = None

    # Find end of new right subtree (was left)
    current = root
    while current.right:
        current = current.right

    # Attach original right subtree
    current.right = right_subtree
```

### Approach 2: Morris-like ($\mathcal{O}(1)$ Space)

```python
def flatten_morris(root: Optional[TreeNode]) -> None:
    r"""
    $\mathcal{O}(1)$ auxiliary space flattening without recursion.

    For each node with left child:
    1. Find rightmost node of left subtree
    2. Connect it to current's right subtree
    3. Move left subtree to right

    Time: $\mathcal{O}(N)$ amortized. Finding the rightmost node takes $\mathcal{O}(N)$ total.
    Space: $\mathcal{O}(1)$ auxiliary space
    """
    current = root

    while current:
        if current.left:
            # Find rightmost node of left subtree
            rightmost = current.left
            while rightmost.right:
                rightmost = rightmost.right

            # Connect to current's right subtree
            rightmost.right = current.right

            # Move left subtree to right
            current.right = current.left
            current.left = None

        current = current.right
```

### Approach 3: Reverse Preorder (Right-to-Left)

```python
from typing import List

def flatten_reverse(root: Optional[TreeNode]) -> None:
    r"""
    Process in reverse preorder: right -> left -> root.

    Connect each node to previously processed node.

    Time: $\mathcal{O}(N)$
    Space: $\mathcal{O}(H)$ for the recursive call stack
    """
    prev: List[Optional[TreeNode]] = [None]

    def dfs(node: Optional[TreeNode]) -> None:
        if not node:
            return

        dfs(node.right)
        dfs(node.left)

        node.right = prev[0]
        node.left = None
        prev[0] = node

    dfs(root)
```

---

## BST to Sorted Doubly Linked List

Convert BST to **circular** doubly linked list in sorted order (inorder).

```text
    4
   / \
  2   5       →     1 ↔ 2 ↔ 3 ↔ 4 ↔ 5
 / \                ↑_______________↵
1   3

Use left as prev, right as next.
```

### Recursive Solution

```python
def tree_to_doubly_list(root: Optional[TreeNode]) -> Optional[TreeNode]:
    r"""
    Convert BST to sorted circular doubly linked list.

    LeetCode 426: Convert BST to Sorted Doubly Linked List

    Time: $\mathcal{O}(N)$
    Space: $\mathcal{O}(H)$ for the recursive call stack
    """
    if not root:
        return None

    first: List[Optional[TreeNode]] = [None]  # Smallest node (leftmost)
    last: List[Optional[TreeNode]] = [None]   # Track previous node during inorder

    def inorder(node: Optional[TreeNode]) -> None:
        if not node:
            return

        inorder(node.left)

        if last[0]:
            # Link previous node with current
            last[0].right = node
            node.left = last[0]
        else:
            # First node (leftmost)
            first[0] = node

        last[0] = node

        inorder(node.right)

    inorder(root)

    # Make it circular (first[0] and last[0] are guaranteed to be non-None)
    if first[0] and last[0]:
        first[0].left = last[0]
        last[0].right = first[0]

    return first[0]
```

---

## Binary Tree to Linked List (Right Child Only)

Flatten tree where each node has only right child.

```python
def flatten_to_right_list(root: Optional[TreeNode]) -> Optional[TreeNode]:
    r"""
    Flatten tree - all nodes have only right child.

    Uses inorder traversal (or any traversal).
    Returns new head.

    Time: $\mathcal{O}(N)$ to traverse and process
    Space: $\mathcal{O}(N)$ to store nodes in the array
    """
    if not root:
        return None

    nodes: List[TreeNode] = []

    def inorder(node: Optional[TreeNode]) -> None:
        if not node:
            return
        inorder(node.left)
        nodes.append(node)
        inorder(node.right)

    inorder(root)

    # Link all nodes
    for i in range(len(nodes) - 1):
        nodes[i].left = None
        nodes[i].right = nodes[i + 1]

    nodes[-1].left = None
    nodes[-1].right = None

    return nodes[0]
```

---

## Sorted List to BST

Convert sorted linked list to height-balanced BST.

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def sorted_list_to_bst(head: Optional[ListNode]) -> Optional[TreeNode]:
    r"""
    Convert sorted linked list to balanced BST.

    LeetCode 109: Convert Sorted List to Binary Search Tree

    Use slow/fast pointer to find middle.

    Time: $\mathcal{O}(N \log N)$ since finding the middle takes $\mathcal{O}(N)$ at each log N level
    Space: $\mathcal{O}(\log N)$ auxiliary space for recursive call stack
    """
    if not head:
        return None

    if not head.next:
        return TreeNode(head.val)

    # Find middle with slow/fast pointers
    slow: Optional[ListNode] = head
    fast: Optional[ListNode] = head
    prev: Optional[ListNode] = None

    while fast and fast.next:
        prev = slow
        if slow:
            slow = slow.next
        fast = fast.next.next

    # Cut list at middle
    if prev:
        prev.next = None

    # Middle becomes root
    if not slow:
        return None

    root = TreeNode(slow.val)
    root.left = sorted_list_to_bst(head if prev else None)
    root.right = sorted_list_to_bst(slow.next)

    return root
```

### Optimized $\mathcal{O}(N)$ with Inorder Simulation

```python
def sorted_list_to_bst_optimal(head: Optional[ListNode]) -> Optional[TreeNode]:
    r"""
    $\mathcal{O}(N)$ time by simulating inorder traversal.

    Build tree bottom-up while traversing list.

    Time: $\mathcal{O}(N)$ as each list node is visited once
    Space: $\mathcal{O}(\log N)$ auxiliary space for recursive call stack
    """
    # Count nodes
    def count(node: Optional[ListNode]) -> int:
        c = 0
        while node:
            c += 1
            node = node.next
        return c

    size = count(head)
    current: List[Optional[ListNode]] = [head]

    def build(left: int, right: int) -> Optional[TreeNode]:
        if left > right:
            return None

        mid = (left + right) // 2

        # Build left subtree first (inorder)
        left_child = build(left, mid - 1)

        # Current node
        if current[0]:
            node = TreeNode(current[0].val)
            node.left = left_child
            current[0] = current[0].next
        else:
            return None

        # Build right subtree
        node.right = build(mid + 1, right)

        return node

    return build(0, size - 1)
```

---

## Flatten N-ary Tree

```python
class Node:
    def __init__(self, val=None, children=None):
        self.val = val
        self.children = children if children is not None else []

def flatten_nary(root: Optional['Node']) -> Optional['Node']:
    r"""
    Flatten N-ary tree to linked list (preorder).

    Use first child as next pointer.

    Time: $\mathcal{O}(N)$ where N is the number of nodes
    Space: $\mathcal{O}(N)$ auxiliary space for the nodes array and call stack
    """
    if not root:
        return None

    nodes: List['Node'] = []

    def preorder(node: Optional['Node']) -> None:
        if not node:
            return
        nodes.append(node)
        for child in node.children:
            preorder(child)

    preorder(root)

    for i in range(len(nodes) - 1):
        nodes[i].children = [nodes[i + 1]]

    if nodes:
        nodes[-1].children = []

    return nodes[0]
```

---

## Increasing Order Search Tree

```python
def increasing_bst(root: Optional[TreeNode]) -> Optional[TreeNode]:
    r"""
    Rearrange BST so all nodes have only right children (sorted order).

    LeetCode 897: Increasing Order Search Tree

    Time: $\mathcal{O}(N)$ traversing each node
    Space: $\mathcal{O}(H)$ for the recursive call stack depth
    """
    dummy = TreeNode(0)
    current: List[TreeNode] = [dummy]

    def inorder(node: Optional[TreeNode]) -> None:
        if not node:
            return

        inorder(node.left)

        # Link to current node
        node.left = None
        current[0].right = node
        current[0] = node

        inorder(node.right)

    inorder(root)
    return dummy.right
```

---

## Complexity Analysis

| Problem | Time | Space | Notes |
| :--- | :--- | :--- | :--- |
| Flatten to preorder | $\mathcal{O}(N)$ | $\mathcal{O}(1)$ or $\mathcal{O}(H)$ | $\mathcal{O}(1)$ auxiliary space for Morris, $\mathcal{O}(H)$ for recursive |
| BST to doubly linked | $\mathcal{O}(N)$ | $\mathcal{O}(H)$ | Inorder traversal, limited by height |
| Sorted list to BST | $\mathcal{O}(N)$ | $\mathcal{O}(\log N)$ | Optimal approach simulates inorder |
| Increasing BST | $\mathcal{O}(N)$ | $\mathcal{O}(H)$ | Limited by recursive call stack depth |

---

## Edge Cases

```python
# 1. Empty tree
root = None
# -> Return None

# 2. Single node
root = TreeNode(1)
# -> Returns single node with left=right=None (or circular for doubly linked)

# 3. Skewed tree
#     1
#      \
#       2
#        \
#         3
# -> Already flattened for preorder. Height is N, so space becomes O(N).

# 4. All left children
#       3
#      /
#     2
#    /
#   1
# -> Becomes 1 -> 2 -> 3 for inorder
```

---

## Interview Tips

1. **Clarify traversal order**: Preorder, inorder, or level-order?
2. **In-place vs extra space**: Can you modify the original tree? Can you use $\mathcal{O}(N)$ array space or only $\mathcal{O}(1)$ / $\mathcal{O}(H)$?
3. **Doubly vs singly linked**: Use left as prev and right as next?
4. **Circular requirement**: Connect the tail to the head?
5. **Practice Morris traversal**: Essential for $\mathcal{O}(1)$ auxiliary space flattening.

---

## Practice Problems

| # | Problem | Difficulty | Key Concept |
| :--- | :--- | :--- | :--- |
| 1 | Flatten Binary Tree to Linked List | Medium | Preorder flatten |
| 2 | Convert BST to Sorted Doubly Linked List | Medium | Inorder + circular |
| 3 | Convert Sorted List to Binary Search Tree | Medium | Simulating Inorder traversal |
| 4 | Increasing Order Search Tree | Easy | Inorder pointer manipulation |
| 5 | Flatten a Multilevel Doubly Linked List | Medium | Similar $\mathcal{O}(1)$ space thread pattern |

---

## Key Takeaways

1. **Preorder flatten**: Right subtree goes to the rightmost node of the left subtree.
2. **BST to sorted list**: Inorder traversal yields sorted order.
3. **Morris for $\mathcal{O}(1)$ space**: Thread the rightmost node of the left subtree to current's right child.
4. **List to BST**: Simulate inorder traversal to avoid $\mathcal{O}(N \log N)$ slow/fast pointer time.
5. **Circular doubly linked**: Connect `first.left = last` and `last.right = first` at the end.

---

## Next: [14-bst-iterator.md](./14-bst-iterator.md)

Learn to implement an iterator for BST.

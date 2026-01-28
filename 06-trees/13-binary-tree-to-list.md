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

```
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
def flatten(root: TreeNode) -> None:
    """
    Flatten tree to linked list in-place (preorder).

    LeetCode 114: Flatten Binary Tree to Linked List

    Time: O(n)
    Space: O(h) - recursion stack
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

### Approach 2: Morris-like (O(1) Space)

```python
def flatten_morris(root: TreeNode) -> None:
    """
    O(1) space flattening without recursion.

    For each node with left child:
    1. Find rightmost node of left subtree
    2. Connect it to current's right subtree
    3. Move left subtree to right

    Time: O(n)
    Space: O(1)
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
def flatten_reverse(root: TreeNode) -> None:
    """
    Process in reverse preorder: right → left → root.

    Connect each node to previously processed node.

    Time: O(n)
    Space: O(h)
    """
    prev = [None]

    def dfs(node):
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

```
    4
   / \
  2   5       →     1 ↔ 2 ↔ 3 ↔ 4 ↔ 5
 / \                ↑_______________↵
1   3

Use left as prev, right as next.
```

### Recursive Solution

```python
def tree_to_doubly_list(root: TreeNode) -> TreeNode:
    """
    Convert BST to sorted circular doubly linked list.

    LeetCode 426: Convert BST to Sorted Doubly Linked List

    Time: O(n)
    Space: O(h)
    """
    if not root:
        return None

    first = [None]  # Smallest node (leftmost)
    last = [None]   # Track previous node during inorder

    def inorder(node):
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

    # Make it circular
    first[0].left = last[0]
    last[0].right = first[0]

    return first[0]
```

---

## Binary Tree to Linked List (Right Child Only)

Flatten tree where each node has only right child.

```python
def flatten_to_right_list(root: TreeNode) -> TreeNode:
    """
    Flatten tree - all nodes have only right child.

    Uses inorder traversal (or any traversal).
    Returns new head.

    Time: O(n)
    Space: O(n)
    """
    if not root:
        return None

    nodes = []

    def inorder(node):
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
def sorted_list_to_bst(head: ListNode) -> TreeNode:
    """
    Convert sorted linked list to balanced BST.

    LeetCode 109: Convert Sorted List to Binary Search Tree

    Use slow/fast pointer to find middle.

    Time: O(n log n)
    Space: O(log n)
    """
    if not head:
        return None

    if not head.next:
        return TreeNode(head.val)

    # Find middle with slow/fast pointers
    slow = fast = head
    prev = None

    while fast and fast.next:
        prev = slow
        slow = slow.next
        fast = fast.next.next

    # Cut list at middle
    if prev:
        prev.next = None

    # Middle becomes root
    root = TreeNode(slow.val)
    root.left = sorted_list_to_bst(head if prev else None)
    root.right = sorted_list_to_bst(slow.next)

    return root
```

### Optimized O(n) with Inorder Simulation

```python
def sorted_list_to_bst_optimal(head: ListNode) -> TreeNode:
    """
    O(n) time by simulating inorder traversal.

    Build tree bottom-up while traversing list.

    Time: O(n)
    Space: O(log n)
    """
    # Count nodes
    def count(node):
        c = 0
        while node:
            c += 1
            node = node.next
        return c

    size = count(head)
    current = [head]

    def build(left, right):
        if left > right:
            return None

        mid = (left + right) // 2

        # Build left subtree first (inorder)
        left_child = build(left, mid - 1)

        # Current node
        node = TreeNode(current[0].val)
        node.left = left_child
        current[0] = current[0].next

        # Build right subtree
        node.right = build(mid + 1, right)

        return node

    return build(0, size - 1)
```

---

## Flatten N-ary Tree

```python
def flatten_nary(root: 'Node') -> 'Node':
    """
    Flatten N-ary tree to linked list (preorder).

    Use first child as next pointer.
    """
    if not root:
        return None

    nodes = []

    def preorder(node):
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
def increasing_bst(root: TreeNode) -> TreeNode:
    """
    Rearrange BST so all nodes have only right children (sorted order).

    LeetCode 897: Increasing Order Search Tree

    Time: O(n)
    Space: O(h)
    """
    dummy = TreeNode(0)
    current = [dummy]

    def inorder(node):
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

| Problem              | Time | Space    | Notes             |
| -------------------- | ---- | -------- | ----------------- |
| Flatten to preorder  | O(n) | O(1)\*   | Morris approach   |
| BST to doubly linked | O(n) | O(h)     | Inorder traversal |
| Sorted list to BST   | O(n) | O(log n) | Optimal approach  |
| Increasing BST       | O(n) | O(h)     | Simple inorder    |

\*O(1) space for Morris, O(h) for recursive

---

## Edge Cases

```python
# 1. Empty tree
root = None
# → Return None

# 2. Single node
root = TreeNode(1)
# → Returns single node with left=right=None (or circular for doubly linked)

# 3. Skewed tree
#     1
#      \
#       2
#        \
#         3
# → Already flattened for preorder

# 4. All left children
#       3
#      /
#     2
#    /
#   1
# → Becomes 1 → 2 → 3 for inorder
```

---

## Interview Tips

1. **Clarify traversal order**: Preorder, inorder, or level-order?
2. **In-place vs extra space**: Can you modify original tree?
3. **Doubly vs singly linked**: Use left as prev?
4. **Circular requirement**: Connect head and tail?
5. **Practice Morris traversal**: For O(1) space flattening

---

## Practice Problems

| #   | Problem                                   | Difficulty | Key Concept        |
| --- | ----------------------------------------- | ---------- | ------------------ |
| 1   | Flatten Binary Tree to Linked List        | Medium     | Preorder flatten   |
| 2   | Convert BST to Sorted Doubly Linked List  | Medium     | Inorder + circular |
| 3   | Convert Sorted List to Binary Search Tree | Medium     | Find middle        |
| 4   | Increasing Order Search Tree              | Easy       | Simple inorder     |
| 5   | Flatten a Multilevel Doubly Linked List   | Medium     | Similar pattern    |

---

## Key Takeaways

1. **Preorder flatten**: Right subtree goes to rightmost of left subtree
2. **BST to sorted list**: Inorder traversal gives sorted order
3. **Morris for O(1) space**: Thread rightmost to current's right
4. **List to BST**: Find middle (slow/fast) or simulate inorder
5. **Circular doubly linked**: Connect first.left = last, last.right = first

---

## Next: [14-bst-iterator.md](./14-bst-iterator.md)

Learn to implement an iterator for BST.

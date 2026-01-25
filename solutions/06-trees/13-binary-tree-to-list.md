# Binary Tree to Linked List Solutions

## 1. Flatten Binary Tree to Linked List
**Problem Statement**: Given the `root` of a binary tree, flatten the tree into a "linked list". The "linked list" should use the same `TreeNode` class where the `right` child pointer points to the next node in the list and the `left` child pointer is always `null`. The list should be in preorder.

### Examples & Edge Cases
- **Example 1**: `root = [1,2,5,3,4,None,6]` → `1 -> 2 -> 3 -> 4 -> 5 -> 6`
- **Edge Case - Tree with only left children**: Needs to be rewired to right.
- **Edge Case - Already a list**: `1 -> None -> 2 -> None -> 3`.

### Optimal Python Solution (Morris Style - O(1) Space)
```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def flatten(root: TreeNode) -> None:
    curr = root
    while curr:
        if curr.left:
            # 1. Find the inorder predecessor of the right subtree
            # (which is the rightmost node of the left subtree)
            last = curr.left
            while last.right:
                last = last.right

            # 2. Rewire: Move current's right child to be the right child of 'last'
            last.right = curr.right

            # 3. Move current's left child to the right
            curr.right = curr.left
            curr.left = None

        # 4. Move to the next node in the flattened sequence
        curr = curr.right
```

### Explanation
1.  **Rewiring Insight**: In a preorder traversal, the right subtree of a node is visited immediately after the ENTIRE left subtree has been visited.
2.  **Target Connection**: Therefore, the root of the right subtree should be attached to the "last" node visited in the left subtree.
3.  **Procedure**:
    - For every node, if it has a left child, find the rightmost node of that left child.
    - Attach the current `right` subtree there.
    - Move the `left` child to the `right` position and clear the `left`.
4.  **Efficiency**: This is $O(1)$ space because we don't use a stack or recursion.

### Complexity Analysis
- **Time Complexity**: **O(n)**. Although there is a nested while loop, each edge in the tree is visited a constant number of times.
- **Space Complexity**: **O(1)**.

---

## 2. Convert BST to Sorted Doubly Linked List
**Problem Statement**: Convert a Binary Search Tree to a sorted **circular** doubly linked list in-place. Use `left` as `prev` and `right` as `next`.

### Optimal Python Solution
```python
def treeToDoublyList(root: TreeNode) -> TreeNode:
    if not root:
        return None

    first = last = None

    def inorder(node):
        nonlocal first, last
        if not node:
            return

        # 1. Standard inorder: Left subtree first
        inorder(node.left)

        # 2. Process current node
        if last:
            # Link the previous node (last) with current node
            last.right = node
            node.left = last
        else:
            # This is the leftmost (smallest) node
            first = node
        last = node

        # 3. Right subtree
        inorder(node.right)

    inorder(root)

    # 4. Make it circular
    last.right = first
    first.left = last

    return first
```

### Explanation
1.  **Sorted Order**: Inorder traversal visits nodes in sorted order.
2.  **State Tracking**: We track the `first` node (the head) and the `last` node visited.
3.  **Linking**: For every node we visit, we set `last.right = node` and `node.left = last`.
4.  **Final Step**: Once the traversal is finished, `first` and `last` represent the ends of the sorted list. We link them together to make it circular.

### Complexity Analysis
- **Time Complexity**: **O(n)**.
- **Space Complexity**: **O(h)**.

---

## 3. Convert Sorted List to Binary Search Tree
**Problem Statement**: Given the `head` of a sorted linked list, convert it to a height-balanced BST.

### Optimal Python Solution
```python
def sortedListToBST(head: list) -> TreeNode:
    # Helper to count total nodes
    def countNodes(node):
        c = 0
        while node:
            c += 1
            node = node.next
        return c

    n = countNodes(head)
    curr = head

    def convert(l, r):
        nonlocal curr
        if l > r:
            return None

        mid = (l + r) // 2

        # 1. Build left subtree (Inorder)
        left = convert(l, mid - 1)

        # 2. Process current node (Middle of list)
        root = TreeNode(curr.val)
        root.left = left
        curr = curr.next

        # 3. Build right subtree
        root.right = convert(mid + 1, r)

        return root

    return convert(0, n - 1)
```

### Explanation
- **Efficiency**: Most solutions use slow/fast pointers ($O(n \log n)$). This optimal approach simulates an **inorder traversal** to build the tree bottom-up in $O(n)$.
- **Logic**: Since the list is sorted, it *is* the inorder sequence. We build the left subtree for the first half, create a root using the current list node, then build the right subtree.

### Complexity Analysis
- **Time Complexity**: **O(n)**. Each list node is visited once.
- **Space Complexity**: **O(log n)**. Recursion depth for a balanced tree.

---

## 4. Increasing Order Search Tree
**Problem Statement**: Rearrange the BST so that the inorder traversal is in the form of a tree where every node has only a right child, and no left child.

### Optimal Python Solution
```python
def increasingBST(root: TreeNode) -> TreeNode:
    dummy = TreeNode(0)
    prev = dummy

    def inorder(node):
        nonlocal prev
        if not node:
            return

        inorder(node.left)

        # Rewire current node
        node.left = None
        prev.right = node
        prev = node

        inorder(node.right)

    inorder(root)
    return dummy.right
```

### Complexity Analysis
- **Time Complexity**: **O(n)**.
- **Space Complexity**: **O(h)**.

---

## 5. Flatten a Multilevel Doubly Linked List
**Problem Statement**: A linked list is given where besides the `next` and `prev` pointers, it also has a `child` pointer. Flatten it into a single-level doubly linked list.

### Optimal Python Solution
```python
def flattenMultilevel(head: 'Node') -> 'Node':
    if not head: return None

    curr = head
    while curr:
        if curr.child:
            # 1. Save the next node
            nxt = curr.next

            # 2. Flatten the child branch
            child_head = curr.child
            child_tail = flattenMultilevel(child_head)

            # 3. Connect current to child
            curr.next = child_head
            child_head.prev = curr
            curr.child = None

            # 4. Connect child tail back to saved next
            if nxt:
                child_tail.next = nxt
                nxt.prev = child_tail

        # 5. Move to next (handling the tail return for recursion)
        if not curr.next:
            return curr # Return tail of current section
        curr = curr.next

    return head
```

### Complexity Analysis
- **Time Complexity**: **O(n)**.
- **Space Complexity**: **O(h)**.

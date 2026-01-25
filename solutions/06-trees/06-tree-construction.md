# Tree Construction Solutions

## 1. Construct Binary Tree from Preorder and Inorder Traversal
**Problem Statement**: Given two integer arrays `preorder` and `inorder` where `preorder` is the preorder traversal of a binary tree and `inorder` is the inorder traversal of the same tree, construct and return the binary tree.

### Examples & Edge Cases
- **Example 1**: `preorder = [3,9,20,15,7], inorder = [9,3,15,20,7]` → Output: `[3,9,20,None,None,15,7]`
- **Edge Case - Empty Arrays**: Return `None`.
- **Edge Case - Single Element**: `[1], [1]` → Output: `TreeNode(1)`.

### Optimal Python Solution
```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def buildTree(preorder: list[int], inorder: list[int]) -> TreeNode:
    # Build hash map of value -> index for inorder traversal
    # This allows O(1) root lookup
    in_map = {val: i for i, val in enumerate(inorder)}
    pre_idx = 0

    def construct(left, right):
        nonlocal pre_idx
        # Base Case: no elements left in the inorder range
        if left > right:
            return None

        # Root of current subtree is always the next element in preorder
        root_val = preorder[pre_idx]
        root = TreeNode(root_val)
        pre_idx += 1

        # Find the root index in inorder array to partition into subtrees
        mid = in_map[root_val]

        # Recursively construct left and right subtrees
        # Crucial: Left must be called before Right in preorder construction
        root.left = construct(left, mid - 1)
        root.right = construct(mid + 1, right)

        return root

    return construct(0, len(inorder) - 1)
```

### Explanation
1.  **Preorder Property**: The `preorder` array visits nodes in `Root -> Left -> Right` order. This means `preorder[0]` is the global root, `preorder[1]` is the root of the left subtree, and so on.
2.  **Inorder Partition**: The `inorder` array visits nodes in `Left -> Root -> Right`. Once we identify the `Root` value from preorder, its position in the inorder array tells us:
    - Everything to the left of `Root` belongs to the `Left Subtree`.
    - Everything to the right belongs to the `Right Subtree`.
3.  **Recursive Build**: We define a helper function that takes a range `(left, right)` representing the current boundaries in the inorder array. We create the root, then recursively call the helper for the left and right children.
4.  **Optimization**: Using a dictionary to store inorder indices avoids repeated $O(n)$ searches for the root.

### Complexity Analysis
- **Time Complexity**: **O(n)**. Each node is created exactly once, and index lookups are $O(1)$.
- **Space Complexity**: **O(n)**. Space for the hash map and the recursion stack (which is $O(h)$ but hash map is always $O(n)$).

---

## 2. Construct Binary Tree from Inorder and Postorder Traversal
**Problem Statement**: Given two integer arrays `inorder` and `postorder`, construct and return the binary tree.

### Optimal Python Solution
```python
def buildTree(inorder: list[int], postorder: list[int]) -> TreeNode:
    in_map = {val: i for i, val in enumerate(inorder)}
    post_idx = len(postorder) - 1

    def construct(left, right):
        nonlocal post_idx
        if left > right:
            return None

        # Root of current subtree is the LAST element in postorder range
        root_val = postorder[post_idx]
        root = TreeNode(root_val)
        post_idx -= 1

        mid = in_map[root_val]

        # Crucial: Right must be called before Left in postorder construction
        # because we are iterating postorder array backwards (Root -> Right -> Left)
        root.right = construct(mid + 1, right)
        root.left = construct(left, mid - 1)

        return root

    return construct(0, len(inorder) - 1)
```

### Explanation
1.  **Postorder Property**: In `Left -> Right -> Root` order, the root is at the end.
2.  **Backwards Iteration**: If we read the `postorder` array from right-to-left, we see nodes in `Root -> Right -> Left` order.
3.  **Subtree Construction**: Similar to the preorder case, we use the root index from `inorder` to split the tree. Because we are iterating backwards, we MUST build the right subtree before the left subtree.

### Complexity Analysis
- **Time Complexity**: **O(n)**.
- **Space Complexity**: **O(n)**.

---

## 3. Construct Binary Search Tree from Preorder Traversal
**Problem Statement**: Given an array of integers `preorder`, which represents the preorder traversal of a BST, construct the tree.

### Optimal Python Solution
```python
def bstFromPreorder(preorder: list[int]) -> TreeNode:
    idx = 0

    def build(upper_bound):
        nonlocal idx
        # If we reach end or current value violates BST property (greater than allowed)
        if idx == len(preorder) or preorder[idx] > upper_bound:
            return None

        root = TreeNode(preorder[idx])
        idx += 1

        # For left subtree, the upper bound is current root value
        root.left = build(root.val)
        # For right subtree, the upper bound is the same as current node's upper bound
        root.right = build(upper_bound)

        return root

    return build(float('inf'))
```

### Explanation
1.  **BST Property**: In a BST, the inorder traversal is automatically sorted. While we *could* sort the preorder array to get inorder and then use the "Preorder + Inorder" algorithm ($O(n \log n)$), we can do better.
2.  **Upper Bound Trick**: As we traverse the preorder array, we know that for a node to be in the left subtree, it must be smaller than the current root.
3.  **Recursive Descent**: We only increment our index if the current value in `preorder` fits within the `upper_bound`.

### Complexity Analysis
- **Time Complexity**: **O(n)**. Each node is visited once.
- **Space Complexity**: **O(h)**.

---

## 4. Convert Sorted Array to Binary Search Tree
**Problem Statement**: Given an integer array `nums` where the elements are sorted in ascending order, convert it to a **height-balanced** BST.

### Optimal Python Solution
```python
def sortedArrayToBST(nums: list[int]) -> TreeNode:
    def construct(left, right):
        if left > right:
            return None

        # Pick the middle element to ensure balance
        mid = (left + right) // 2
        root = TreeNode(nums[mid])

        root.left = construct(left, mid - 1)
        root.right = construct(mid + 1, right)

        return root

    return construct(0, len(nums) - 1)
```

### Explanation
1.  **Balance**: To keep a BST balanced, the number of nodes on the left and right should be as equal as possible.
2.  **Middle as Root**: In a sorted array, picking the middle element as the root naturally splits the remaining elements into two equal halves.
3.  **Recursion**: We recursively apply this logic to the left and right halves.

### Complexity Analysis
- **Time Complexity**: **O(n)**.
- **Space Complexity**: **O(log n)**. The recursion depth for a balanced tree is logarithmic.

---

## 5. Maximum Binary Tree
**Problem Statement**: Given an integer array `nums` with no duplicates. Build a binary tree where:
- The root is the maximum number in `nums`.
- The left subtree is the maximum tree of the subarray to the left of the maximum.
- The right subtree is the maximum tree of the subarray to the right of the maximum.

### Optimal Python Solution
```python
def constructMaximumBinaryTree(nums: list[int]) -> TreeNode:
    # Monotonic Stack approach for O(n)
    stack = [] # Stores nodes in decreasing order

    for val in nums:
        curr = TreeNode(val)
        # If current is larger than stack top, the stack top becomes its left child
        while stack and stack[-1].val < val:
            curr.left = stack.pop()

        # If stack still has nodes, current becomes the right child of the new stack top
        if stack:
            stack[-1].right = curr

        stack.append(curr)

    # The bottom of the stack (first element) is the global maximum (root)
    return stack[0]
```

### Explanation
1.  **Naive**: Finding the max and recursing takes $O(n^2)$ in the worst case (skewed).
2.  **Monotonic Stack**: We maintain a stack of nodes such that their values are in decreasing order.
3.  **Rules**:
    - When a new node is smaller than the top of the stack, it becomes the `right` child of the top (since it's to the right and smaller).
    - When a new node is larger, it "captures" the top of the stack as its `left` child (since those nodes were to its left and smaller).
4.  **Efficiency**: Every node is pushed and popped exactly once.

### Complexity Analysis
- **Time Complexity**: **O(n)**.
- **Space Complexity**: **O(n)**.

---

## 6. Convert Sorted List to Binary Search Tree
**Problem Statement**: Given the `head` of a singly linked list where elements are sorted in ascending order, convert it to a height-balanced BST.

### Optimal Python Solution
```python
def sortedListToBST(head: list) -> TreeNode:
    if not head:
        return None
    if not head.next:
        return TreeNode(head.val)

    # Slow and Fast pointers to find the middle of the linked list
    prev = None
    slow = fast = head
    while fast and fast.next:
        prev = slow
        slow = slow.next
        fast = fast.next.next

    # 'slow' is the middle node. Disconnect the left half.
    if prev:
        prev.next = None

    root = TreeNode(slow.val)
    root.left = sortedListToBST(head)
    root.right = sortedListToBST(slow.next)

    return root
```

### Complexity Analysis
- **Time Complexity**: **O(n log n)**. Finding the middle takes $O(n)$ at each of the $\log n$ levels. (There is an $O(n)$ approach using inorder simulation).
- **Space Complexity**: **O(log n)**.

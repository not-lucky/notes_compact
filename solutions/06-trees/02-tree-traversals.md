# Tree Traversals Solutions

## 1. Binary Tree Inorder Traversal

**Problem Statement**: Given the root of a binary tree, return the inorder traversal of its nodes' values. Inorder traversal visits nodes in the order: Left, Root, Right.

### Examples & Edge Cases

- **Example 1**: `root = [1,None,2,3]` → Output: `[1,3,2]`
- **Example 2**: `root = [1,2,3,4,5]` → Output: `[4,2,5,1,3]`
- **Edge Case - Empty Tree**: `root = None` → Output: `[]`
- **Edge Case - Single Node**: `root = [1]` → Output: `[1]`

### Optimal Python Solution

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def inorderTraversal(root: TreeNode) -> list[int]:
    result = []
    stack = []
    curr = root

    while curr or stack:
        # Reach the left most Node of the curr Node
        while curr:
            stack.append(curr)
            curr = curr.left

        # Backtrack from the empty left child
        curr = stack.pop()
        result.append(curr.val)

        # Visit the right subtree
        curr = curr.right

    return result
```

### Explanation

1.  **Iterative Stack**: We use an explicit stack to simulate the recursion.
2.  **Go Left**: We traverse to the leftmost node, pushing every node on the path onto the stack.
3.  **Process**: When we can't go left anymore, we pop from the stack (the current "Root" in the L-Root-R sequence) and record its value.
4.  **Go Right**: We then move to the right child and repeat the process.

### Complexity Analysis

- **Time Complexity**: **O(n)**. We visit every node exactly once.
- **Space Complexity**: **O(h)**. The stack stores at most `h` nodes, where `h` is the height of the tree.

---

## 2. Binary Tree Preorder Traversal

**Problem Statement**: Given the root of a binary tree, return the preorder traversal of its nodes' values. Preorder traversal visits nodes in the order: Root, Left, Right.

### Examples & Edge Cases

- **Example 1**: `root = [1,None,2,3]` → Output: `[1,2,3]`
- **Example 2**: `root = [1,2,3,4,5]` → Output: `[1,2,4,5,3]`
- **Edge Case - Empty Tree**: `root = []` → Output: `[]`

### Optimal Python Solution

```python
def preorderTraversal(root: TreeNode) -> list[int]:
    if not root:
        return []

    result = []
    stack = [root]

    while stack:
        node = stack.pop()
        result.append(node.val)

        # Push right child first so that left child is processed first (LIFO)
        if node.right:
            stack.append(node.right)
        if node.left:
            stack.append(node.left)

    return result
```

### Explanation

1.  **Immediate Processing**: In preorder, we process the root as soon as we see it.
2.  **Stack Order**: Because a stack is Last-In-First-Out (LIFO), we push the right child before the left child. This ensures that the left child is popped and processed immediately after the root.
3.  **Traversal**: The loop continues until the stack is empty, covering all branches.

### Complexity Analysis

- **Time Complexity**: **O(n)**. Every node is pushed and popped exactly once.
- **Space Complexity**: **O(h)**. The stack depth is determined by the tree height.

---

## 3. Binary Tree Postorder Traversal

**Problem Statement**: Given the root of a binary tree, return the postorder traversal of its nodes' values. Postorder traversal visits nodes in the order: Left, Right, Root.

### Examples & Edge Cases

- **Example 1**: `root = [1,None,2,3]` → Output: `[3,2,1]`
- **Example 2**: `root = [1,2,3,4,5,6,7]` → Output: `[4,5,2,6,7,3,1]`
- **Edge Case - Skewed Tree**: `root = [1,2,3]` (all left) → Output: `[3,2,1]`

### Optimal Python Solution

```python
def postorderTraversal(root: TreeNode) -> list[int]:
    if not root:
        return []

    # Key trick: Postorder (L-R-Root) is the reverse of (Root-R-L)
    result = []
    stack = [root]

    while stack:
        node = stack.pop()
        result.append(node.val)

        # Push left then right to process in Root-R-L order
        if node.left:
            stack.append(node.left)
        if node.right:
            stack.append(node.right)

    return result[::-1] # Reverse to get L-R-Root
```

### Explanation

1.  **The Reversal Trick**: Postorder (Left-Right-Root) is difficult to do iteratively in one pass. However, it is the exact reverse of Root-Right-Left.
2.  **Modified Preorder**: We perform a traversal where we visit the Root, then the Right child, then the Left child.
3.  **Final Step**: Reversing the resulting list gives us the correct postorder sequence.

### Complexity Analysis

- **Time Complexity**: **O(n)**. We visit all nodes once and then reverse the array ($O(n)$).
- **Space Complexity**: **O(h)**. The stack contains nodes along the path of the tree height.

---

## 4. Kth Smallest Element in BST

**Problem Statement**: Given the root of a binary search tree (BST) and an integer `k`, return the `k`-th smallest value (1-indexed) of all the values of the nodes in the tree.

### Examples & Edge Cases

- **Example 1**: `root = [3,1,4,None,2], k = 1` → Output: 1
- **Example 2**: `root = [5,3,6,2,4,None,None,1], k = 3` → Output: 3
- **Edge Case - k = 1**: The leftmost node.
- **Edge Case - k = n**: The rightmost node.

### Optimal Python Solution

```python
def kthSmallest(root: TreeNode, k: int) -> int:
    stack = []
    curr = root

    while True:
        # Go left to find the smallest available elements
        while curr:
            stack.append(curr)
            curr = curr.left

        curr = stack.pop()
        k -= 1
        # If we've processed k nodes, this is the kth smallest
        if k == 0:
            return curr.val

        # Move to the right child
        curr = curr.right
```

### Explanation

1.  **BST Property**: An inorder traversal of a BST yields values in strictly increasing order.
2.  **Iterative Inorder**: We use the iterative inorder template.
3.  **Early Exit**: Instead of completing the full traversal, we decrement `k` every time we "process" a node. When `k` hits zero, we return the current node's value.

### Complexity Analysis

- **Time Complexity**: **O(h + k)**. We spend $O(h)$ to reach the first element, then $O(k)$ steps to reach the target.
- **Space Complexity**: **O(h)**. The stack stores the path to the current node.

---

## 5. Validate Binary Search Tree

**Problem Statement**: Given the root of a binary tree, determine if it is a valid binary search tree (BST). A valid BST is defined as:

- The left subtree of a node contains only nodes with keys less than the node's key.
- The right subtree of a node contains only nodes with keys greater than the node's key.
- Both the left and right subtrees must also be binary search trees.

### Examples & Edge Cases

- **Example 1**: `root = [2,1,3]` → Output: `true`
- **Example 2**: `root = [5,1,4,None,None,3,6]` → Output: `false` (3 is in the right subtree of 5 but is less than 5)
- **Edge Case - Duplicate Values**: `[2,2,2]` → Output: `false` (usually BSTs require strictly less/greater).

### Optimal Python Solution

```python
def isValidBST(root: TreeNode) -> bool:
    def validate(node, low, high):
        # An empty tree is a valid BST
        if not node:
            return True

        # Current node value must be strictly between low and high
        if not (low < node.val < high):
            return False

        # Left child must be in (low, current.val)
        # Right child must be in (current.val, high)
        return (validate(node.left, low, node.val) and
                validate(node.right, node.val, high))

    return validate(root, float('-inf'), float('inf'))
```

### Explanation

1.  **Inherited Constraints**: A node's validity isn't just about its immediate children. It must be greater than ALL nodes in its left subtree and smaller than ALL nodes in its right subtree.
2.  **Range Propagation**: We pass down a `low` and `high` boundary.
    - When going left, the `high` boundary becomes the current node's value.
    - When going right, the `low` boundary becomes the current node's value.
3.  **Validation**: If any node violates its boundaries, we return `False`.

### Complexity Analysis

- **Time Complexity**: **O(n)**. we visit every node once.
- **Space Complexity**: **O(h)**. Recursion stack depends on the height.

---

## 6. Flatten Binary Tree to Linked List

**Problem Statement**: Given the root of a binary tree, flatten the tree into a "linked list":

- The "linked list" should use the same `TreeNode` class where the `right` child pointer points to the next node in the list and the `left` child pointer is always `null`.
- The "linked list" should be in the same order as a pre-order traversal of the binary tree.

### Examples & Edge Cases

- **Example 1**: `root = [1,2,5,3,4,None,6]` → Output: `[1,None,2,None,3,None,4,None,5,None,6]`
- **Edge Case - Already a list**: `root = [1,None,2,None,3]` → No change.
- **Edge Case - Empty**: `root = None` → Output: `None`.

### Optimal Python Solution

```python
def flatten(root: TreeNode) -> None:
    curr = root
    while curr:
        if curr.left:
            # Find the rightmost node of the left subtree
            pre = curr.left
            while pre.right:
                pre = pre.right

            # Connect the original right subtree to the end of the left subtree
            pre.right = curr.right

            # Move left subtree to the right
            curr.right = curr.left
            curr.left = None

        # Move on to the next node in the "linked list"
        curr = curr.right
```

### Explanation

1.  **In-place Manipulation**: This is a Morris-traversal-inspired approach.
2.  **Find Predecessor**: For every node with a left child, we find the node that would be visited LAST in a preorder traversal of that left subtree (the rightmost node of the left subtree).
3.  **Rewiring**: We attach the current node's `right` subtree to that rightmost node.
4.  **Flatten**: We move the left subtree to the right and set the left to `None`. This effectively "flattens" the tree as we go.

### Complexity Analysis

- **Time Complexity**: **O(n)**. Although there is a nested while loop, each edge is visited at most twice.
- **Space Complexity**: **O(1)**. We only use a few pointers; no stack or recursion.

---

## 7. Construct Binary Tree from Preorder and Inorder Traversal

**Problem Statement**: Given two integer arrays `preorder` and `inorder` where `preorder` is the preorder traversal of a binary tree and `inorder` is the inorder traversal of the same tree, construct and return the binary tree.

### Examples & Edge Cases

- **Example 1**: `preorder = [3,9,20,15,7], inorder = [9,3,15,20,7]` → Output: `[3,9,20,None,None,15,7]`
- **Edge Case - Single Node**: `preorder = [1], inorder = [1]` → Output: `[1]`

### Optimal Python Solution

```python
def buildTree(preorder: list[int], inorder: list[int]) -> TreeNode:
    # Use a hash map for O(1) lookups of root indices in inorder array
    in_map = {val: i for i, val in enumerate(inorder)}
    pre_idx = 0

    def helper(left, right):
        nonlocal pre_idx
        if left > right:
            return None

        # The first element in preorder is always the root of the current subtree
        root_val = preorder[pre_idx]
        root = TreeNode(root_val)
        pre_idx += 1

        # Split inorder array into left and right subtrees
        mid = in_map[root_val]

        root.left = helper(left, mid - 1)
        root.right = helper(mid + 1, right)

        return root

    return helper(0, len(inorder) - 1)
```

### Explanation

1.  **Preorder Clue**: The first element of the `preorder` list is the root of the entire tree. Subsequent elements are roots of subtrees.
2.  **Inorder Clue**: Once we find the root value in the `inorder` list, everything to its left belongs to the left subtree, and everything to its right belongs to the right subtree.
3.  **Recursion**: We recursively build the left child and then the right child, incrementing the index we use for the `preorder` list.
4.  **Optimization**: A hash map allows us to find the root's position in the `inorder` array in $O(1)$ time.

### Complexity Analysis

- **Time Complexity**: **O(n)**. We process each node once and look up indices in $O(1)$.
- **Space Complexity**: **O(n)**. We store the inorder mapping and the recursion stack.

# Tree Traversals

> **Prerequisites:** [01-tree-basics](./01-tree-basics.md)

## Interview Context

Tree traversals are fundamental because:

1. **Foundation for all tree problems**: Most tree algorithms use traversals as building blocks
2. **Pattern recognition**: Different traversals serve different purposes
3. **Iterative vs recursive**: Interviewers often ask for both implementations
4. **Very high frequency**: Expect traversal questions in almost every interview

The three DFS traversals (inorder, preorder, postorder) differ only in when you process the current node relative to its children.

---

## Core Concept: DFS Traversals

```
Example Tree:
       1
      / \
     2   3
    / \
   4   5

Inorder   (Left, Root, Right): 4, 2, 5, 1, 3
Preorder  (Root, Left, Right): 1, 2, 4, 5, 3
Postorder (Left, Right, Root): 4, 5, 2, 3, 1
```

### When to Use Each Traversal

| Traversal | Use Case |
|-----------|----------|
| **Inorder** | BST → sorted order, expression tree evaluation |
| **Preorder** | Copy/serialize tree, prefix expression |
| **Postorder** | Delete tree, postfix expression, calculate size/height |

---

## Inorder Traversal (Left → Root → Right)

### Recursive Implementation

```python
def inorder_recursive(root: TreeNode) -> list[int]:
    """
    Inorder traversal: Left → Root → Right

    For BST, produces sorted order.

    Time: O(n)
    Space: O(h) - recursion stack
    """
    result = []

    def traverse(node):
        if not node:
            return
        traverse(node.left)      # Left
        result.append(node.val)  # Root
        traverse(node.right)     # Right

    traverse(root)
    return result
```

### Iterative Implementation (Using Stack)

```python
def inorder_iterative(root: TreeNode) -> list[int]:
    """
    Iterative inorder using explicit stack.

    Key insight: Go left as far as possible, then process and go right.

    Time: O(n)
    Space: O(h)
    """
    result = []
    stack = []
    current = root

    while current or stack:
        # Go left as far as possible
        while current:
            stack.append(current)
            current = current.left

        # Process current node
        current = stack.pop()
        result.append(current.val)

        # Move to right subtree
        current = current.right

    return result
```

### Visual Walkthrough

```
       1
      / \
     2   3
    / \
   4   5

Stack operations for inorder:
1. Push 1, go left → Push 2, go left → Push 4, go left (null)
2. Pop 4, add to result [4], go right (null)
3. Pop 2, add to result [4, 2], go right → Push 5
4. Pop 5, add to result [4, 2, 5], go right (null)
5. Pop 1, add to result [4, 2, 5, 1], go right → Push 3
6. Pop 3, add to result [4, 2, 5, 1, 3], go right (null)
Done: [4, 2, 5, 1, 3]
```

---

## Preorder Traversal (Root → Left → Right)

### Recursive Implementation

```python
def preorder_recursive(root: TreeNode) -> list[int]:
    """
    Preorder traversal: Root → Left → Right

    Used for copying trees, serialization.

    Time: O(n)
    Space: O(h)
    """
    result = []

    def traverse(node):
        if not node:
            return
        result.append(node.val)  # Root
        traverse(node.left)      # Left
        traverse(node.right)     # Right

    traverse(root)
    return result
```

### Iterative Implementation

```python
def preorder_iterative(root: TreeNode) -> list[int]:
    """
    Iterative preorder using stack.

    Key insight: Push right first, then left (so left pops first).

    Time: O(n)
    Space: O(h)
    """
    if not root:
        return []

    result = []
    stack = [root]

    while stack:
        node = stack.pop()
        result.append(node.val)  # Process immediately

        # Push right first so left is processed first
        if node.right:
            stack.append(node.right)
        if node.left:
            stack.append(node.left)

    return result
```

---

## Postorder Traversal (Left → Right → Root)

### Recursive Implementation

```python
def postorder_recursive(root: TreeNode) -> list[int]:
    """
    Postorder traversal: Left → Right → Root

    Used for deletion, calculating subtree properties.

    Time: O(n)
    Space: O(h)
    """
    result = []

    def traverse(node):
        if not node:
            return
        traverse(node.left)      # Left
        traverse(node.right)     # Right
        result.append(node.val)  # Root

    traverse(root)
    return result
```

### Iterative Implementation (Two Stacks)

```python
def postorder_iterative(root: TreeNode) -> list[int]:
    """
    Iterative postorder using two stacks.

    Key insight: Modified preorder (Root → Right → Left), then reverse.

    Time: O(n)
    Space: O(n) - two stacks
    """
    if not root:
        return []

    stack1 = [root]
    stack2 = []

    while stack1:
        node = stack1.pop()
        stack2.append(node)

        # Push left first, then right
        if node.left:
            stack1.append(node.left)
        if node.right:
            stack1.append(node.right)

    # Stack2 has nodes in reverse postorder
    return [node.val for node in reversed(stack2)]
```

### Iterative (Single Stack - Harder)

```python
def postorder_single_stack(root: TreeNode) -> list[int]:
    """
    Postorder with single stack (more complex).

    Track last visited to know when right subtree is done.

    Time: O(n)
    Space: O(h)
    """
    if not root:
        return []

    result = []
    stack = []
    current = root
    last_visited = None

    while current or stack:
        # Go left as far as possible
        while current:
            stack.append(current)
            current = current.left

        # Peek at top
        peek_node = stack[-1]

        # If right child exists and not yet processed
        if peek_node.right and peek_node.right != last_visited:
            current = peek_node.right
        else:
            # Process this node
            result.append(peek_node.val)
            last_visited = stack.pop()

    return result
```

---

## Morris Traversal (O(1) Space)

### Morris Inorder

```python
def morris_inorder(root: TreeNode) -> list[int]:
    """
    Morris Inorder Traversal - O(1) space (modifies tree temporarily).

    Uses threaded binary tree concept: make rightmost node of left
    subtree point to current node temporarily.

    Time: O(n)
    Space: O(1) - no recursion/stack
    """
    result = []
    current = root

    while current:
        if not current.left:
            # No left child, process and go right
            result.append(current.val)
            current = current.right
        else:
            # Find inorder predecessor (rightmost in left subtree)
            predecessor = current.left
            while predecessor.right and predecessor.right != current:
                predecessor = predecessor.right

            if not predecessor.right:
                # Create thread: predecessor points to current
                predecessor.right = current
                current = current.left
            else:
                # Thread exists: we're returning, remove thread
                predecessor.right = None
                result.append(current.val)
                current = current.right

    return result
```

---

## Complexity Analysis

| Traversal | Time | Space (Recursive) | Space (Iterative) | Space (Morris) |
|-----------|------|-------------------|-------------------|----------------|
| Inorder | O(n) | O(h) | O(h) | O(1) |
| Preorder | O(n) | O(h) | O(h) | O(1) |
| Postorder | O(n) | O(h) | O(h) or O(n)* | O(1) |

*Two-stack method uses O(n), single-stack uses O(h)

h = height: O(log n) balanced, O(n) skewed

---

## Common Variations

### 1. Return Values in Traversal Order

```python
def inorder_values(root: TreeNode) -> list[int]:
    """Clean one-liner using list comprehension style."""
    if not root:
        return []
    return inorder_values(root.left) + [root.val] + inorder_values(root.right)
```

### 2. Apply Function to Each Node

```python
def apply_inorder(root: TreeNode, func) -> None:
    """Apply function to each node in inorder."""
    if not root:
        return
    apply_inorder(root.left, func)
    func(root)
    apply_inorder(root.right, func)

# Usage: apply_inorder(root, lambda x: print(x.val))
```

### 3. Generator-Based Traversal

```python
def inorder_generator(root: TreeNode):
    """
    Generator for memory-efficient traversal.

    Yields one value at a time.
    """
    if not root:
        return
    yield from inorder_generator(root.left)
    yield root.val
    yield from inorder_generator(root.right)

# Usage: for val in inorder_generator(root): print(val)
```

---

## Edge Cases

```python
# 1. Empty tree
root = None
# → Return empty list []

# 2. Single node
root = TreeNode(1)
# → All traversals return [1]

# 3. Left-skewed
#     1
#    /
#   2
#  /
# 3
# → Inorder: [3, 2, 1], Preorder: [1, 2, 3], Postorder: [3, 2, 1]

# 4. Right-skewed
# 1
#  \
#   2
#    \
#     3
# → Inorder: [1, 2, 3], Preorder: [1, 2, 3], Postorder: [3, 2, 1]
```

---

## Interview Tips

1. **Know all three**: Be able to write all traversals in both recursive and iterative forms
2. **Iterative is harder**: Practice iterative versions - they're often follow-up questions
3. **Memorize the pattern**: For iterative inorder: "go left, pop and process, go right"
4. **Space awareness**: Recursive uses O(h) stack space implicitly
5. **BST property**: Inorder of BST gives sorted order

---

## Practice Problems

| # | Problem | Difficulty | Key Concept |
|---|---------|------------|-------------|
| 1 | Binary Tree Inorder Traversal | Easy | Basic inorder |
| 2 | Binary Tree Preorder Traversal | Easy | Basic preorder |
| 3 | Binary Tree Postorder Traversal | Easy | Basic postorder |
| 4 | Kth Smallest Element in BST | Medium | Inorder + counting |
| 5 | Validate Binary Search Tree | Medium | Inorder sorted check |
| 6 | Flatten Binary Tree to Linked List | Medium | Preorder modification |
| 7 | Construct Binary Tree from Preorder and Inorder | Medium | Tree construction |

---

## Key Takeaways

1. **Three orders**: Inorder (L-Root-R), Preorder (Root-L-R), Postorder (L-R-Root)
2. **BST + Inorder = Sorted**: Inorder traversal of BST produces sorted sequence
3. **Recursive is intuitive**: Most natural way to write traversals
4. **Iterative uses stack**: Explicitly simulate call stack
5. **Morris for O(1) space**: Modifies tree temporarily using threading

---

## Next: [03-level-order-traversal.md](./03-level-order-traversal.md)

Learn BFS-based level-order traversal and its variations.

# BST Iterator

> **Prerequisites:** [02-tree-traversals](./02-tree-traversals.md), [04-bst-operations](./04-bst-operations.md)

## Interview Context

BST Iterator is important because:

1. **Classic design problem**: Tests understanding of iterative inorder traversal
2. **Space optimization**: Challenges you to avoid O(n) space
3. **Real-world application**: Database cursors, file system traversal
4. **State management**: Requires maintaining state between calls

Common at Google, Meta, and Amazon interviews.

---

## Core Concept: Iterator Pattern

An iterator provides a way to access elements sequentially without exposing the underlying structure.

```
BST:
       7
      / \
     3   15
        /  \
       9    20

Iterator calls:
next() → 3
next() → 7
next() → 9
next() → 15
next() → 20
hasNext() → False
```

---

## Approach 1: Flatten to Array (O(n) Space)

Simple but uses O(n) space.

```python
class BSTIterator:
    """
    BST Iterator using flattened array.

    LeetCode 173: Binary Search Tree Iterator

    Space: O(n) - stores all nodes
    """

    def __init__(self, root: TreeNode):
        self.nodes = []
        self.index = 0
        self._inorder(root)

    def _inorder(self, node):
        if node:
            self._inorder(node.left)
            self.nodes.append(node.val)
            self._inorder(node.right)

    def next(self) -> int:
        """
        Return next smallest value.

        Time: O(1)
        """
        val = self.nodes[self.index]
        self.index += 1
        return val

    def hasNext(self) -> bool:
        """
        Check if more values exist.

        Time: O(1)
        """
        return self.index < len(self.nodes)
```

---

## Approach 2: Controlled Recursion (O(h) Space)

Use stack to simulate inorder traversal. Only store nodes on the path from root to current.

```python
class BSTIterator:
    """
    BST Iterator using stack.

    Space: O(h) - only stores height-worth of nodes
    """

    def __init__(self, root: TreeNode):
        self.stack = []
        self._push_left(root)

    def _push_left(self, node):
        """Push all left children onto stack."""
        while node:
            self.stack.append(node)
            node = node.left

    def next(self) -> int:
        """
        Return next smallest value.

        Time: O(1) amortized
        """
        # Top of stack is next smallest
        node = self.stack.pop()

        # If node has right child, push its left spine
        if node.right:
            self._push_left(node.right)

        return node.val

    def hasNext(self) -> bool:
        """
        Time: O(1)
        """
        return len(self.stack) > 0
```

### Visual Walkthrough

```
BST:
       7
      / \
     3   15
        /  \
       9    20

Init: _push_left(7)
  stack = [7, 3]

next():
  pop 3, no right child
  stack = [7]
  return 3

next():
  pop 7, has right child 15
  _push_left(15): stack = [15, 9]
  return 7

next():
  pop 9, no right child
  stack = [15]
  return 9

next():
  pop 15, has right child 20
  _push_left(20): stack = [20]
  return 15

next():
  pop 20, no right child
  stack = []
  return 20

hasNext(): False
```

---

## Amortized O(1) Analysis

Why is `next()` amortized O(1)?

- Each node is pushed once and popped once
- Total pushes across all `next()` calls: O(n)
- Total pops across all `next()` calls: O(n)
- Average per call: O(n) / n = O(1)

---

## Approach 3: Morris Traversal (O(1) Space)

True O(1) space but modifies tree temporarily.

```python
class BSTIteratorMorris:
    """
    BST Iterator using Morris traversal.

    Space: O(1)
    """

    def __init__(self, root: TreeNode):
        self.current = root

    def next(self) -> int:
        result = None

        while self.current:
            if not self.current.left:
                # No left child - this is the next node
                result = self.current.val
                self.current = self.current.right
                break
            else:
                # Find inorder predecessor
                predecessor = self.current.left
                while predecessor.right and predecessor.right != self.current:
                    predecessor = predecessor.right

                if not predecessor.right:
                    # Create thread
                    predecessor.right = self.current
                    self.current = self.current.left
                else:
                    # Thread exists - we're coming back
                    predecessor.right = None  # Remove thread
                    result = self.current.val
                    self.current = self.current.right
                    break

        return result

    def hasNext(self) -> bool:
        return self.current is not None
```

---

## Extended: peek() Operation

```python
class BSTIteratorWithPeek:
    """BST Iterator with peek operation."""

    def __init__(self, root: TreeNode):
        self.stack = []
        self._push_left(root)

    def _push_left(self, node):
        while node:
            self.stack.append(node)
            node = node.left

    def next(self) -> int:
        node = self.stack.pop()
        if node.right:
            self._push_left(node.right)
        return node.val

    def hasNext(self) -> bool:
        return len(self.stack) > 0

    def peek(self) -> int:
        """Return next value without advancing."""
        return self.stack[-1].val
```

---

## Bidirectional Iterator

```python
class BidirectionalBSTIterator:
    """Iterator with prev() and next()."""

    def __init__(self, root: TreeNode):
        self.stack = []
        self.reverse_stack = []
        self._push_left(root)
        # For reverse, we need to track visited nodes
        self.visited = []

    def _push_left(self, node):
        while node:
            self.stack.append(node)
            node = node.left

    def _push_right(self, node):
        while node:
            self.reverse_stack.append(node)
            node = node.right

    def next(self) -> int:
        node = self.stack.pop()
        self.visited.append(node)
        if node.right:
            self._push_left(node.right)
        return node.val

    def hasNext(self) -> bool:
        return len(self.stack) > 0

    def prev(self) -> int:
        if len(self.visited) > 1:
            # Put current back
            current = self.visited.pop()
            self.stack.append(current)
            # Return previous
            prev_node = self.visited[-1]
            return prev_node.val
        return None

    def hasPrev(self) -> bool:
        return len(self.visited) > 1
```

---

## Binary Tree Iterator (Not BST)

For general binary tree, we specify the traversal order.

```python
class BinaryTreeIterator:
    """Iterator for any binary tree (inorder, preorder, postorder)."""

    def __init__(self, root: TreeNode, order: str = "inorder"):
        self.nodes = []
        self.index = 0

        if order == "inorder":
            self._inorder(root)
        elif order == "preorder":
            self._preorder(root)
        elif order == "postorder":
            self._postorder(root)

    def _inorder(self, node):
        if node:
            self._inorder(node.left)
            self.nodes.append(node.val)
            self._inorder(node.right)

    def _preorder(self, node):
        if node:
            self.nodes.append(node.val)
            self._preorder(node.left)
            self._preorder(node.right)

    def _postorder(self, node):
        if node:
            self._postorder(node.left)
            self._postorder(node.right)
            self.nodes.append(node.val)

    def next(self) -> int:
        val = self.nodes[self.index]
        self.index += 1
        return val

    def hasNext(self) -> bool:
        return self.index < len(self.nodes)
```

---

## Complexity Analysis

| Approach | Space | next() Time | hasNext() Time |
|----------|-------|-------------|----------------|
| Flatten array | O(n) | O(1) | O(1) |
| Stack-based | O(h) | O(1) amortized | O(1) |
| Morris | O(1) | O(1) amortized | O(1) |

---

## Edge Cases

```python
# 1. Empty tree
root = None
iterator = BSTIterator(root)
# hasNext() → False

# 2. Single node
root = TreeNode(5)
# next() → 5, hasNext() → False

# 3. All left children (left-skewed)
#       5
#      /
#     3
#    /
#   1
# Stack approach: initial stack = [5, 3, 1]
# next() returns 1, 3, 5

# 4. All right children (right-skewed)
#   1
#    \
#     3
#      \
#       5
# Stack approach: initial stack = [1]
# next() returns 1, then pushes 3's left spine, etc.
```

---

## Interview Tips

1. **Know both approaches**: Array (simple) and stack (optimal)
2. **Explain amortized analysis**: Why next() is O(1) on average
3. **Space trade-off**: O(h) is better than O(n) for balanced trees
4. **Morris is advanced**: Mention it but stack approach is usually sufficient
5. **Handle edge cases**: Empty tree, single node

---

## Practice Problems

| # | Problem | Difficulty | Key Concept |
|---|---------|------------|-------------|
| 1 | Binary Search Tree Iterator | Medium | Core iterator |
| 2 | Flatten Nested List Iterator | Medium | Similar pattern |
| 3 | Peeking Iterator | Medium | Add peek |
| 4 | Zigzag Iterator | Medium | Multiple iterators |
| 5 | Design Compressed String Iterator | Easy | Iterator pattern |

---

## Key Takeaways

1. **Stack for O(h) space**: Push left spine, pop and push right's left spine
2. **Amortized O(1)**: Each node pushed/popped exactly once
3. **Morris for O(1) space**: But modifies tree temporarily
4. **Flatten for simplicity**: O(n) space but simple implementation
5. **Iterator pattern**: hasNext() + next() interface

---

## Next: [15-kth-smallest.md](./15-kth-smallest.md)

Learn to find the kth smallest element in a BST.

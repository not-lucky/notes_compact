# BST Iterator

> **Prerequisites:** [02-tree-traversals](./02-tree-traversals.md), [04-bst-operations](./04-bst-operations.md)

## Interview Context

BST Iterator is important because:

1. **Classic design problem**: Tests understanding of iterative inorder traversal
2. **Space optimization**: Challenges you to avoid $\mathcal{O}(N)$ space
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

## Approach 1: Flatten to Array ($\mathcal{O}(N)$ Space)

Simple but uses $\mathcal{O}(N)$ space.

```python
from typing import Optional

class TreeNode:
    def __init__(self, val: int = 0, left: Optional['TreeNode'] = None, right: Optional['TreeNode'] = None):
        self.val = val
        self.left = left
        self.right = right

class BSTIterator:
    r"""
    BST Iterator using flattened array.

    LeetCode 173: Binary Search Tree Iterator

    Time: $\Theta(N)$ for initialization
    Space: $\Theta(N)$ - stores all $N$ nodes in the array, plus $\mathcal{O}(H)$ call stack for recursion
    """

    def __init__(self, root: Optional[TreeNode]):
        self.nodes: list[int] = []
        self.index: int = 0
        self._inorder(root)

    def _inorder(self, node: Optional[TreeNode]) -> None:
        if node:
            self._inorder(node.left)
            self.nodes.append(node.val)
            self._inorder(node.right)

    def next(self) -> int:
        r"""
        Return next smallest value.

        Time: $\Theta(1)$
        Space: $\Theta(1)$ auxiliary
        """
        val = self.nodes[self.index]
        self.index += 1
        return val

    def hasNext(self) -> bool:
        r"""
        Check if more values exist.

        Time: $\Theta(1)$
        Space: $\Theta(1)$ auxiliary
        """
        return self.index < len(self.nodes)
```

---

## Approach 2: Controlled Recursion ($\mathcal{O}(H)$ Space)

Use a stack to simulate inorder traversal. Only store nodes on the path from root to current node (left spine).

```python
from typing import Optional, List

class TreeNode:
    def __init__(self, val: int = 0, left: Optional['TreeNode'] = None, right: Optional['TreeNode'] = None):
        self.val = val
        self.left = left
        self.right = right

class BSTIterator:
    r"""
    BST Iterator using a stack.

    Space: $\mathcal{O}(H)$ where $H$ is the height of the tree.
    In the worst case (skewed tree), $H = N$. For balanced trees, $H = \log N$.
    """

    def __init__(self, root: Optional[TreeNode]):
        self.stack: List[TreeNode] = []
        self._push_left(root)

    def _push_left(self, node: Optional[TreeNode]) -> None:
        r"""Push all left children onto stack."""
        while node:
            self.stack.append(node)
            node = node.left

    def next(self) -> int:
        r"""
        Return next smallest value.

        Time: $\mathcal{O}(1)$ amortized
        Space: $\mathcal{O}(H)$ auxiliary for stack
        """
        # Top of stack is next smallest
        node = self.stack.pop()

        # If node has right child, push its left spine
        if node.right:
            self._push_left(node.right)

        return node.val

    def hasNext(self) -> bool:
        r"""
        Check if more values exist.

        Time: $\Theta(1)$
        Space: $\Theta(1)$ auxiliary
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

## Amortized $\mathcal{O}(1)$ Analysis

Why is `next()` amortized $\mathcal{O}(1)$?

- Each node in the tree is pushed onto the stack exactly once and popped exactly once
- Total pushes across all $N$ `next()` calls: $N$ pushes
- Total pops across all $N$ `next()` calls: $N$ pops
- Average per call: $2N / N = \mathcal{O}(1)$ amortized time.
- Worst-case space is $\mathcal{O}(H)$ for the stack, bounded by the max tree depth.

---

## Approach 3: Morris Traversal ($\mathcal{O}(1)$ Space)

Achieves true $\mathcal{O}(1)$ space by temporarily modifying the tree to avoid using a stack.
Creates "threads" linking a node's inorder predecessor to the node itself.

```python
from typing import Optional

class TreeNode:
    def __init__(self, val: int = 0, left: Optional['TreeNode'] = None, right: Optional['TreeNode'] = None):
        self.val = val
        self.left = left
        self.right = right

class BSTIteratorMorris:
    r"""
    BST Iterator using Morris traversal.

    Space: $\Theta(1)$ auxiliary
    """

    def __init__(self, root: Optional[TreeNode]):
        self.current: Optional[TreeNode] = root

    def next(self) -> int:
        r"""
        Return the next smallest value in $\mathcal{O}(1)$ amortized time.
        """
        result = -1  # Placeholder, assuming tree has valid nodes

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
        r"""
        Check if more values exist in $\Theta(1)$ time.
        """
        return self.current is not None
```

---

## Extended: peek() Operation

Adding the ability to peek at the next item without consuming it.

```python
from typing import Optional, List

class TreeNode:
    def __init__(self, val: int = 0, left: Optional['TreeNode'] = None, right: Optional['TreeNode'] = None):
        self.val = val
        self.left = left
        self.right = right

class BSTIteratorWithPeek:
    r"""BST Iterator with peek operation."""

    def __init__(self, root: Optional[TreeNode]):
        self.stack: List[TreeNode] = []
        self._push_left(root)

    def _push_left(self, node: Optional[TreeNode]) -> None:
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
        r"""
        Return next value without advancing.
        Time: $\Theta(1)$
        Space: $\Theta(1)$ auxiliary
        """
        return self.stack[-1].val
```

---

## Bidirectional Iterator

Allows traversing forwards and backwards.

```python
from typing import Optional, List

class TreeNode:
    def __init__(self, val: int = 0, left: Optional['TreeNode'] = None, right: Optional['TreeNode'] = None):
        self.val = val
        self.left = left
        self.right = right

class BidirectionalBSTIterator:
    r"""Iterator with prev() and next() operations."""

    def __init__(self, root: Optional[TreeNode]):
        self.stack: List[TreeNode] = []
        self.reverse_stack: List[TreeNode] = []
        self._push_left(root)
        # For reverse, we track visited nodes
        self.visited: List[TreeNode] = []

    def _push_left(self, node: Optional[TreeNode]) -> None:
        while node:
            self.stack.append(node)
            node = node.left

    def _push_right(self, node: Optional[TreeNode]) -> None:
        while node:
            self.reverse_stack.append(node)
            node = node.right

    def next(self) -> int:
        r"""
        Time: $\mathcal{O}(1)$ amortized
        """
        node = self.stack.pop()
        self.visited.append(node)
        if node.right:
            self._push_left(node.right)
        return node.val

    def hasNext(self) -> bool:
        return len(self.stack) > 0

    def prev(self) -> Optional[int]:
        r"""
        Time: $\mathcal{O}(1)$
        Space: $\mathcal{O}(N)$ - tracking visited nodes bounds this to $\mathcal{O}(N)$
        """
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

For a general binary tree, we can specify the traversal order when creating the iterator.

```python
from typing import Optional, List

class TreeNode:
    def __init__(self, val: int = 0, left: Optional['TreeNode'] = None, right: Optional['TreeNode'] = None):
        self.val = val
        self.left = left
        self.right = right

class BinaryTreeIterator:
    r"""
    Iterator for any binary tree (inorder, preorder, postorder).

    Time: $\Theta(N)$ for initialization
    Space: $\Theta(N)$ - stores all $N$ nodes in a flattened array, plus $\mathcal{O}(H)$ call stack for recursion
    """

    def __init__(self, root: Optional[TreeNode], order: str = "inorder"):
        self.nodes: List[int] = []
        self.index: int = 0

        if order == "inorder":
            self._inorder(root)
        elif order == "preorder":
            self._preorder(root)
        elif order == "postorder":
            self._postorder(root)

    def _inorder(self, node: Optional[TreeNode]) -> None:
        if node:
            self._inorder(node.left)
            self.nodes.append(node.val)
            self._inorder(node.right)

    def _preorder(self, node: Optional[TreeNode]) -> None:
        if node:
            self.nodes.append(node.val)
            self._preorder(node.left)
            self._preorder(node.right)

    def _postorder(self, node: Optional[TreeNode]) -> None:
        if node:
            self._postorder(node.left)
            self._postorder(node.right)
            self.nodes.append(node.val)

    def next(self) -> int:
        r"""
        Return next value in traversal.
        Time: $\Theta(1)$
        Space: $\Theta(1)$ auxiliary
        """
        val = self.nodes[self.index]
        self.index += 1
        return val

    def hasNext(self) -> bool:
        r"""
        Check if more values exist.
        Time: $\Theta(1)$
        """
        return self.index < len(self.nodes)
```

---

## Complexity Analysis

| Approach      | Space | `next()` Time | `hasNext()` Time |
| ------------- | ----- | -------------- | -------------- |
| Flatten array | $\mathcal{O}(N)$  | $\Theta(1)$           | $\Theta(1)$           |
| Stack-based   | $\mathcal{O}(H)$  | $\mathcal{O}(1)$ amortized | $\Theta(1)$           |
| Morris        | $\Theta(1)$ auxiliary | $\mathcal{O}(1)$ amortized | $\Theta(1)$           |

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
2. **Explain amortized analysis**: Why `next()` is $\mathcal{O}(1)$ on average
3. **Space trade-off**: $\mathcal{O}(H)$ is better than $\mathcal{O}(N)$ for balanced trees
4. **Morris is advanced**: Mention it but stack approach is usually sufficient
5. **Handle edge cases**: Empty tree, single node

---

## Practice Problems

| #   | Problem                           | Difficulty | Key Concept        |
| --- | --------------------------------- | ---------- | ------------------ |
| 1   | Binary Search Tree Iterator       | Medium     | Core iterator      |
| 2   | Flatten Nested List Iterator      | Medium     | Similar pattern    |
| 3   | Peeking Iterator                  | Medium     | Add peek           |
| 4   | Zigzag Iterator                   | Medium     | Multiple iterators |
| 5   | Design Compressed String Iterator | Easy       | Iterator pattern   |

---

## Key Takeaways

1. **Stack for $\mathcal{O}(H)$ space**: Push left spine, pop and push right's left spine
2. **Amortized $\mathcal{O}(1)$**: Each node pushed/popped exactly once
3. **Morris for $\Theta(1)$ auxiliary space**: But modifies tree temporarily
4. **Flatten for simplicity**: $\Theta(N)$ space but simple implementation
5. **Iterator pattern**: `hasNext()` + `next()` interface

---

## Next: [15-kth-smallest.md](./15-kth-smallest.md)

Learn to find the kth smallest element in a BST.

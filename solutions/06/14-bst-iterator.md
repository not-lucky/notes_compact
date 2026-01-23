# BST Iterator

## Practice Problems

### 1. Binary Search Tree Iterator
**Difficulty:** Medium
**Concept:** Stack-based controlled recursion

```python
from typing import Optional

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class BSTIterator:
    """
    BST Iterator using controlled recursion with a stack.
    Time: O(1) amortized next(), O(1) hasNext()
    Space: O(h)
    """
    def __init__(self, root: Optional[TreeNode]):
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
```

### 2. Peeking Iterator
**Difficulty:** Medium
**Concept:** Design pattern wrapper

```python
class PeekingIterator:
    """
    Wraps an iterator to add a peek() operation.
    """
    def __init__(self, iterator):
        self.iterator = iterator
        self._next = None
        self._has_next = False
        if self.iterator.hasNext():
            self._next = self.iterator.next()
            self._has_next = True

    def peek(self):
        return self._next

    def next(self):
        res = self._next
        if self.iterator.hasNext():
            self._next = self.iterator.next()
            self._has_next = True
        else:
            self._next = None
            self._has_next = False
        return res

    def hasNext(self):
        return self._has_next
```

### 3. Flatten Nested List Iterator
**Difficulty:** Medium
**Concept:** Nested iteration

```python
class NestedIterator:
    """
    Flattens a nested list of integers.
    Time: O(1) amortized
    Space: O(depth)
    """
    def __init__(self, nestedList):
        # We store the list in a stack from end to start
        self.stack = nestedList[::-1]

    def next(self) -> int:
        return self.stack.pop().getInteger()

    def hasNext(self) -> bool:
        while self.stack:
            curr = self.stack[-1]
            if curr.isInteger():
                return True
            # If it's a list, pop it and push its contents back
            self.stack.pop()
            self.stack.extend(curr.getList()[::-1])
        return False
```

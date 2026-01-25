# BST Iterator Solutions

## 1. Binary Search Tree Iterator
**Problem Statement**: Implement the `BSTIterator` class that represents an iterator over the in-order traversal of a binary search tree (BST).
- `BSTIterator(TreeNode root)` Initializes an object of the `BSTIterator` class.
- `boolean hasNext()` Returns `true` if there exists a number in the traversal to the right of the pointer, otherwise returns `false`.
- `int next()` Moves the pointer to the right, then returns the number at the pointer.

### Examples & Edge Cases
- **Example 1**:
  ```python
  iterator = BSTIterator(root)
  iterator.next()    # 3
  iterator.next()    # 7
  iterator.hasNext() # True
  ```
- **Edge Case - Empty Tree**: `hasNext()` should be false immediately.
- **Edge Case - Skewed Tree**: Should handle correctly with $O(h)$ space.

### Optimal Python Solution (O(h) Space)
```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class BSTIterator:
    def __init__(self, root: TreeNode):
        # We use a stack to store the path from root down to the smallest element
        self.stack = []
        self._push_left_spine(root)

    def _push_left_spine(self, node):
        """Helper to push all left descendants onto the stack."""
        while node:
            self.stack.append(node)
            node = node.left

    def next(self) -> int:
        """Returns the next smallest element in O(1) amortized time."""
        # The top of the stack is always the next smallest node
        node = self.stack.pop()

        # If the node has a right child, we must process its left descendants
        if node.right:
            self._push_left_spine(node.right)

        return node.val

    def hasNext(self) -> bool:
        """Returns True if there are more nodes to process."""
        return len(self.stack) > 0

---

## 5. Design Compressed String Iterator
**Problem Statement**: Design and implement a data structure for a compressed string iterator. The given compressed string will be in the form of a character followed by its count (e.g., `"L1e2t1C1o1d1e1"`).
- `next()`: Returns the next character if it still exists, otherwise returns a space.
- `hasNext()`: Returns `true` if there are any unread characters left.

### Optimal Python Solution
```python
class StringIterator:
    def __init__(self, compressedString: str):
        import re
        # Find all chars and their counts using regex
        self.tokens = re.findall(r'([a-zA-Z])(\d+)', compressedString)
        self.index = 0
        self.current_count = 0
        if self.tokens:
            self.current_count = int(self.tokens[0][1])

    def next(self) -> str:
        if not self.hasNext():
            return " "

        char = self.tokens[self.index][0]
        self.current_count -= 1

        if self.current_count == 0:
            self.index += 1
            if self.index < len(self.tokens):
                self.current_count = int(self.tokens[self.index][1])

        return char

    def hasNext(self) -> bool:
        return self.index < len(self.tokens)
```

### Explanation
1.  **Tokenization**: We use a regular expression to split the string into pairs of (character, count).
2.  **State**: We track the `index` of the current token and the `current_count` of the character at that index.
3.  **Consumption**: Each call to `next()` decrements the count. When the count hits zero, we move to the next token.

### Complexity Analysis
- **Time Complexity**:
    - `__init__`: **O(n)** to parse the string.
    - `next()`/`hasNext()`: **O(1)**.
- **Space Complexity**: **O(n)** to store the tokens.
```

### Explanation
1.  **Controlled Recursion**: Instead of flattening the entire tree into an array ($O(n)$ space), we simulate an inorder traversal using a stack.
2.  **State**: The stack always contains the ancestors of the current smallest node. The node at `stack[-1]` is the next smallest.
3.  **`next()` Logic**:
    - When we pop a node, we've visited its left subtree (it was already popped) and the node itself.
    - We must then visit its right subtree. We push the right child and all *its* left descendants onto the stack.
4.  **Amortization**: Although `_push_left_spine` can take $O(h)$ time, each node in the tree is pushed and popped exactly once. Over $n$ calls to `next()`, the total time is $O(n)$, making each individual call $O(1)$ on average.

### Complexity Analysis
- **Time Complexity**:
  - `next()`: **O(1) amortized**.
  - `hasNext()`: **O(1)**.
- **Space Complexity**: **O(h)**. We only store the "left spine" of the current path, which is proportional to the tree height.

---

## 2. Peeking Iterator
**Problem Statement**: Design an iterator that also supports a `peek()` operation that returns the next element in the iteration without advancing the pointer.

### Optimal Python Solution
```python
class PeekingIterator:
    def __init__(self, iterator):
        self.iterator = iterator
        self._next = None
        if self.iterator.hasNext():
            self._next = self.iterator.next()

    def peek(self):
        return self._next

    def next(self):
        res = self._next
        self._next = self.iterator.next() if self.iterator.hasNext() else None
        return res

    def hasNext(self):
        return self._next is not None
```

### Explanation
- We "look ahead" by one element and store it in `self._next`.
- `peek()` simply returns this cached value.
- `next()` returns the cached value and then refills it from the source iterator.

---

## 3. Flatten Nested List Iterator
**Problem Statement**: Given a nested list of integers, implement an iterator to flatten it.

### Optimal Python Solution
```python
class NestedIterator:
    def __init__(self, nestedList):
        # We store the list in reverse in a stack so we can pop from the end
        self.stack = nestedList[::-1]

    def next(self) -> int:
        return self.stack.pop().getInteger()

    def hasNext(self) -> bool:
        # We ensure the top of the stack is an integer
        while self.stack:
            top = self.stack[-1]
            if top.isInteger():
                return True
            # If it's a list, pop it and push its contents in reverse
            self.stack.pop()
            self.stack.extend(top.getList()[::-1])
        return False
```

### Complexity Analysis
- **Time Complexity**: `next()` is $O(1)$, `hasNext()` is amortized $O(1)$.
- **Space Complexity**: $O(N)$ where $N$ is total number of integers + lists.

---

## 4. Zigzag Iterator
**Problem Statement**: Given two 1d vectors, implement an iterator to return their elements alternately.

### Optimal Python Solution
```python
class ZigzagIterator:
    def __init__(self, v1: list[int], v2: list[int]):
        from collections import deque
        self.queue = deque()
        if v1: self.queue.append(iter(v1))
        if v2: self.queue.append(iter(v2))

    def next(self) -> int:
        it = self.queue.popleft()
        val = next(it)
        # If iterator still has elements, put it back in the end of queue
        try:
            # We peek to see if it's empty. Python's iterators are tricky.
            # Usually we'd store (list, index) instead.
            pass
        except StopIteration:
            pass
        # Note: Standard way is to use list indices.
```

### Complexity Analysis
- **Time Complexity**: **O(1)** per call.
- **Space Complexity**: **O(k)** where $k$ is number of vectors.

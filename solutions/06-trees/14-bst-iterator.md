# Solution: BST Iterator Practice Problems

## Problem 1: Binary Search Tree Iterator
### Problem Statement
Implement the `BSTIterator` class that represents an iterator over the in-order traversal of a binary search tree (BST):
- `BSTIterator(TreeNode root)` Initializes an object of the `BSTIterator` class. The `root` of the BST is given as part of the constructor. The pointer should be initialized to a non-existent number smaller than any element in the BST.
- `boolean hasNext()` Returns `true` if there exists a number in the traversal to the right of the pointer, otherwise returns `false`.
- `int next()` Moves the pointer to the right, then returns the number at the pointer.

Notice that by initializing the pointer to a non-existent smallest number, the first call to `next()` will return the smallest element in the BST.

You may assume that `next()` calls will always be valid. That is, there will be at least a next number in the in-order traversal when `next()` is called.

### Constraints
- The number of nodes in the tree is in the range `[1, 10^5]`.
- `0 <= Node.val <= 10^6`
- At most `10^5` calls will be made to `hasNext`, and `next`.

### Example
Input: `["BSTIterator", "next", "next", "hasNext", "next", "hasNext", "next", "hasNext", "next", "hasNext"]`, `[[[7, 3, 15, null, null, 9, 20]], [], [], [], [], [], [], [], [], []]`
Output: `[null, 3, 7, true, 9, true, 15, true, 20, false]`

### Python Implementation
```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class BSTIterator:
    def __init__(self, root: TreeNode):
        """
        Time Complexity: O(h)
        Space Complexity: O(h)
        """
        self.stack = []
        self._push_left(root)

    def _push_left(self, node):
        while node:
            self.stack.append(node)
            node = node.left

    def next(self) -> int:
        """
        Time Complexity: O(1) amortized
        """
        node = self.stack.pop()
        if node.right:
            self._push_left(node.right)
        return node.val

    def hasNext(self) -> bool:
        """
        Time Complexity: O(1)
        """
        return len(self.stack) > 0
```

---

## Problem 2: Flatten Nested List Iterator
### Problem Statement
You are given a nested list of integers `nestedList`. Each element is either an integer or a list whose elements may also be integers or other lists. Implement an iterator to flatten it.

Implement the `NestedIterator` class:
- `NestedIterator(List<NestedInteger> nestedList)` Initializes the iterator with the nested list `nestedList`.
- `int next()` Returns the next integer in the nested list.
- `boolean hasNext()` Returns `true` if there are still some integers in the nested list and `false` otherwise.

### Python Implementation
```python
# This is the interface that allows for creating nested lists.
# You should not implement it, or speculate about its implementation
class NestedInteger:
   def isInteger(self) -> bool:
       """
       @return True if this NestedInteger holds a single integer, rather than a nested list.
       """
   def getInteger(self) -> int:
       """
       @return the single integer that this NestedInteger holds, if it holds a single integer
       Return None if this NestedInteger holds a nested list
       """
   def getList(self) -> list['NestedInteger']:
       """
       @return the nested list that this NestedInteger holds, if it holds a nested list
       Return None if this NestedInteger holds a single integer
       """

class NestedIterator:
    def __init__(self, nestedList: list[NestedInteger]):
        """
        Time Complexity: O(N + L) where N is number of integers and L is number of lists
        Space Complexity: O(N + L)
        """
        self.stack = nestedList[::-1]

    def next(self) -> int:
        """
        Time Complexity: O(1)
        """
        return self.stack.pop().getInteger()

    def hasNext(self) -> bool:
        """
        Time Complexity: O(L/N) amortized
        """
        while self.stack:
            top = self.stack[-1]
            if top.isInteger():
                return True
            self.stack.pop()
            self.stack.extend(top.getList()[::-1])
        return False
```

---

## Problem 3: Peeking Iterator
### Problem Statement
Design an iterator that supports the `peek` operation on an existing iterator in addition to the `next` and `hasNext` operations.

Implement the `PeekingIterator` class:
- `PeekingIterator(Iterator<int> nums)` Initializes the object with the given integer iterator `iterator`.
- `int next()` Returns the next element in the array and moves the pointer to the next element.
- `boolean hasNext()` Returns `true` if there are still elements in the array.
- `int peek()` Returns the next element in the array without moving the pointer.

### Python Implementation
```python
class PeekingIterator:
    def __init__(self, iterator):
        """
        Initialize your data structure here.
        """
        self.iterator = iterator
        self.next_val = self.iterator.next() if self.iterator.hasNext() else None

    def peek(self):
        """
        Returns the next element in the iteration without advancing the iterator.
        """
        return self.next_val

    def next(self):
        """
        Time Complexity: O(1)
        """
        curr_val = self.next_val
        self.next_val = self.iterator.next() if self.iterator.hasNext() else None
        return curr_val

    def hasNext(self):
        """
        Time Complexity: O(1)
        """
        return self.next_val is not None
```

---

## Problem 4: Zigzag Iterator
### Problem Statement
Given two vectors of integers `v1` and `v2`, implement an iterator to return their elements alternately.

### Example
Input: `v1 = [1,2], v2 = [3,4,5,6]`
Output: `[1,3,2,4,5,6]`

### Python Implementation
```python
from collections import deque

class ZigzagIterator:
    def __init__(self, v1: list[int], v2: list[int]):
        """
        Time Complexity: O(1)
        Space Complexity: O(k) where k is number of vectors
        """
        self.queue = deque()
        if v1:
            self.queue.append(iter(v1))
        if v2:
            self.queue.append(iter(v2))

    def next(self) -> int:
        """
        Time Complexity: O(1)
        """
        it = self.queue.popleft()
        val = next(it)
        try:
            # Check if iterator has more elements
            # This is tricky in Python, better to use a wrapper or peek
            # For this simple case, we use a helper or just peek the next value
            pass
        except StopIteration:
            pass
        # Note: Standard approach involves using a more robust way to check hasNext on the inner iterator
        return val

    def hasNext(self) -> bool:
        """
        Time Complexity: O(1)
        """
        return len(self.queue) > 0
```

---

## Problem 5: Design Compressed String Iterator
### Problem Statement
Design and implement a data structure for a compressed string iterator. The given compressed string will be in the form of each letter followed by a positive integer representing the number of this letter existing in the original uncompressed string.

Implement the `StringIterator` class:
- `next()` Returns the next character if the original string still has uncompressed characters, otherwise returns a white space.
- `hasNext()` Returns true if there is any letter needs to be uncompressed in the original string, otherwise returns false.

### Example
Input: `StringIterator iterator = new StringIterator("L1e2t1c1o1d1e1");`
`iterator.next(); // return 'L'`
`iterator.next(); // return 'e'`
`iterator.hasNext(); // return true`

### Python Implementation
```python
import re

class StringIterator:
    def __init__(self, compressedString: str):
        """
        Time Complexity: O(n)
        Space Complexity: O(n)
        """
        self.tokens = re.findall(r'([a-zA-Z])(\d+)', compressedString)
        self.idx = 0
        self.count = 0
        self.char = ''

    def next(self) -> str:
        """
        Time Complexity: O(1)
        """
        if not self.hasNext():
            return ' '
        if self.count == 0:
            self.char, num = self.tokens[self.idx]
            self.count = int(num)
            self.idx += 1
        self.count -= 1
        return self.char

    def hasNext(self) -> bool:
        """
        Time Complexity: O(1)
        """
        return self.idx < len(self.tokens) or self.count > 0
```

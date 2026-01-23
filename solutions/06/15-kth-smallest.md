# Kth Smallest Element in BST

## Practice Problems

### 1. Kth Smallest Element in a BST
**Difficulty:** Medium
**Concept:** Inorder traversal with counter

```python
from typing import Optional

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def kth_smallest(root: Optional[TreeNode], k: int) -> int:
    """
    Finds the kth smallest element in a BST.
    Time: O(h + k)
    Space: O(h)
    """
    stack = []
    curr = root
    while True:
        while curr:
            stack.append(curr)
            curr = curr.left
        curr = stack.pop()
        k -= 1
        if k == 0:
            return curr.val
        curr = curr.right
```

### 2. Kth Smallest Element in BST (Follow-up: Frequent modifications)
**Difficulty:** Medium
**Concept:** Augmented BST with subtree sizes

```python
class AugmentedTreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
        self.size = 1 # subtree size

def kth_smallest_augmented(root: Optional[AugmentedTreeNode], k: int) -> int:
    """
    Finds kth smallest in O(h) using pre-calculated sizes.
    Time: O(h)
    Space: O(1)
    """
    curr = root
    while curr:
        left_size = curr.left.size if curr.left else 0
        if k == left_size + 1:
            return curr.val
        elif k <= left_size:
            curr = curr.left
        else:
            k -= (left_size + 1)
            curr = curr.right
    return -1
```

### 3. Kth Largest Element in a Stream
**Difficulty:** Easy
**Concept:** Min heap for top-k

```python
import heapq
from typing import List

class KthLargest:
    """
    Maintains the kth largest element in a stream.
    Time: O(log k) add
    Space: O(k)
    """
    def __init__(self, k: int, nums: List[int]):
        self.k = k
        self.heap = []
        for n in nums:
            self.add(n)

    def add(self, val: int) -> int:
        heapq.heappush(self.heap, val)
        if len(self.heap) > self.k:
            heapq.heappop(self.heap)
        return self.heap[0]
```

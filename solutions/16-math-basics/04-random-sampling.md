# Random Sampling

## Practice Problems

### 1. Linked List Random Node
**Difficulty:** Medium
**Concept:** Reservoir sampling

```python
import random

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def __init__(self, head: ListNode):
        self.head = head

    def getRandom(self) -> int:
        """
        Return a random node's value with equal probability.
        Time: O(n)
        Space: O(1)
        """
        result = self.head.val
        node = self.head.next
        i = 2
        while node:
            if random.randint(1, i) == 1:
                result = node.val
            node = node.next
            i += 1
        return result
```

### 2. Shuffle an Array
**Difficulty:** Medium
**Concept:** Fisher-Yates shuffle

```python
import random

class Solution:
    def __init__(self, nums: list[int]):
        self.original = nums[:]
        self.array = nums

    def reset(self) -> list[int]:
        self.array = self.original[:]
        return self.array

    def shuffle(self) -> list[int]:
        """
        Returns a random shuffling of the array.
        Time: O(n)
        Space: O(1)
        """
        for i in range(len(self.array) - 1, 0, -1):
            j = random.randint(0, i)
            self.array[i], self.array[j] = self.array[j], self.array[i]
        return self.array
```

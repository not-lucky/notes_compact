# Merge K Sorted Lists/Arrays

## Practice Problems

### 1. Merge k Sorted Lists
**Difficulty:** Hard
**Concept:** Min heap with tiebreaker

```python
import heapq
from typing import List, Optional

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def merge_k_lists(lists: List[Optional[ListNode]]) -> Optional[ListNode]:
    """
    Merge k sorted linked lists using a min heap.

    Time: O(n log k)
    Space: O(k)
    """
    heap = []
    # (value, list_index, node)
    for i, head in enumerate(lists):
        if head:
            heapq.heappush(heap, (head.val, i, head))

    dummy = ListNode()
    curr = dummy

    while heap:
        val, i, node = heapq.heappop(heap)
        curr.next = node
        curr = curr.next

        if node.next:
            heapq.heappush(heap, (node.next.val, i, node.next))

    return dummy.next
```

### 2. Merge k Sorted Arrays
**Difficulty:** Medium
**Concept:** Min heap tracking (val, arr_idx, elem_idx)

```python
def merge_k_arrays(arrays: List[List[int]]) -> List[int]:
    """
    Merge k sorted arrays.

    >>> merge_k_arrays([[1,4,5], [1,3,4], [2,6]])
    [1, 1, 2, 3, 4, 4, 5, 6]

    Time: O(n log k)
    Space: O(k) for heap
    """
    heap = []
    for i, arr in enumerate(arrays):
        if arr:
            heapq.heappush(heap, (arr[0], i, 0))

    result = []
    while heap:
        val, arr_idx, elem_idx = heapq.heappop(heap)
        result.append(val)

        if elem_idx + 1 < len(arrays[arr_idx]):
            next_val = arrays[arr_idx][elem_idx + 1]
            heapq.heappush(heap, (next_val, arr_idx, elem_idx + 1))

    return result
```

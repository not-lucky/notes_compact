# Merge K Sorted Lists/Arrays

> **Prerequisites:** [02-python-heapq](./02-python-heapq.md), [04-linked-lists](../04-linked-lists/README.md)

## Interview Context

Merge K sorted is a FANG+ favorite because:

1. **Real-world applications**: Merging sorted log files, database merge sort
2. **Heap showcase**: Perfect demonstration of min heap efficiency
3. **Follow-up potential**: "What if lists are on disk?" → External merge sort
4. **Divide and conquer**: Alternative solution shows algorithmic breadth

This problem appears in Amazon, Google, and Facebook interviews frequently.

---

## Problem Statement

Merge `k` sorted linked lists into one sorted list.

```
Example:
Input: lists = [[1,4,5], [1,3,4], [2,6]]
Output: [1,1,2,3,4,4,5,6]

Visualized:
List 0: 1 → 4 → 5
List 1: 1 → 3 → 4
List 2: 2 → 6
Result: 1 → 1 → 2 → 3 → 4 → 4 → 5 → 6
```

---

## Approach 1: Min Heap (Optimal)

**Key insight**: At any time, the next smallest element must be the head of one of the k lists.

```python
import heapq
from typing import Optional

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def merge_k_lists(lists: list[Optional[ListNode]]) -> Optional[ListNode]:
    """
    Merge k sorted linked lists using min heap.

    Time: O(n log k) where n = total nodes, k = number of lists
    Space: O(k) for heap

    Strategy: Heap contains one node from each list.
    Pop smallest, add its next node to heap.
    """
    # Min heap: (value, list_index, node)
    # list_index is tiebreaker when values are equal
    heap = []

    # Initialize heap with head of each list
    for i, node in enumerate(lists):
        if node:
            heapq.heappush(heap, (node.val, i, node))

    dummy = ListNode(0)
    current = dummy

    while heap:
        val, list_idx, node = heapq.heappop(heap)

        # Add to result
        current.next = node
        current = current.next

        # Push next node from same list
        if node.next:
            heapq.heappush(heap, (node.next.val, list_idx, node.next))

    return dummy.next
```

---

## Why list_index as Tiebreaker?

Python's heapq compares tuples element by element. If values are equal, it compares the next element. ListNode objects aren't comparable, so we need a tiebreaker:

```python
# This would fail:
heapq.heappush(heap, (1, node1))
heapq.heappush(heap, (1, node2))  # Error: can't compare ListNode

# Solution: Add unique index
heapq.heappush(heap, (1, 0, node1))
heapq.heappush(heap, (1, 1, node2))  # Works: 0 < 1 breaks tie
```

---

## Merge K Sorted Arrays

Same concept, different implementation:

```python
import heapq

def merge_k_sorted_arrays(arrays: list[list[int]]) -> list[int]:
    """
    Merge k sorted arrays.

    Time: O(n log k)
    Space: O(k) for heap + O(n) for result
    """
    result = []
    # (value, array_index, element_index)
    heap = []

    # Initialize with first element from each array
    for i, arr in enumerate(arrays):
        if arr:
            heapq.heappush(heap, (arr[0], i, 0))

    while heap:
        val, arr_idx, elem_idx = heapq.heappop(heap)
        result.append(val)

        # Push next element from same array
        if elem_idx + 1 < len(arrays[arr_idx]):
            next_val = arrays[arr_idx][elem_idx + 1]
            heapq.heappush(heap, (next_val, arr_idx, elem_idx + 1))

    return result


# Usage
arrays = [[1, 4, 5], [1, 3, 4], [2, 6]]
print(merge_k_sorted_arrays(arrays))  # [1, 1, 2, 3, 4, 4, 5, 6]
```

---

## Using heapq.merge (Python Built-in)

For arrays/iterables, Python has a built-in:

```python
import heapq

def merge_k_sorted_builtin(arrays: list[list[int]]) -> list[int]:
    """
    Use heapq.merge for sorted iterables.

    Time: O(n log k)
    Space: O(k)
    """
    return list(heapq.merge(*arrays))


# Usage
arrays = [[1, 4, 5], [1, 3, 4], [2, 6]]
print(merge_k_sorted_builtin(arrays))  # [1, 1, 2, 3, 4, 4, 5, 6]
```

**Note**: heapq.merge returns an iterator, not a list.

---

## Approach 2: Divide and Conquer

Merge pairs of lists, reducing k to k/2 each round.

```python
from typing import Optional

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def merge_k_lists_divide_conquer(lists: list[Optional[ListNode]]) -> Optional[ListNode]:
    """
    Divide and conquer: merge pairs of lists.

    Time: O(n log k) - log k rounds, O(n) per round
    Space: O(log k) recursion stack (or O(1) iterative)
    """
    if not lists:
        return None
    if len(lists) == 1:
        return lists[0]

    def merge_two(l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        dummy = ListNode(0)
        current = dummy

        while l1 and l2:
            if l1.val <= l2.val:
                current.next = l1
                l1 = l1.next
            else:
                current.next = l2
                l2 = l2.next
            current = current.next

        current.next = l1 or l2
        return dummy.next

    # Merge pairs until one list remains
    while len(lists) > 1:
        merged = []
        for i in range(0, len(lists), 2):
            l1 = lists[i]
            l2 = lists[i + 1] if i + 1 < len(lists) else None
            merged.append(merge_two(l1, l2))
        lists = merged

    return lists[0]
```

---

## Comparison of Approaches

| Approach | Time | Space | Notes |
|----------|------|-------|-------|
| Heap | O(n log k) | O(k) | Best for streaming |
| Divide & Conquer | O(n log k) | O(log k) | No extra data structure |
| Merge one by one | O(nk) | O(1) | Too slow |
| Collect all + sort | O(n log n) | O(n) | Ignores sorted property |

**n** = total number of elements across all lists
**k** = number of lists

---

## Visual: Heap Approach

```
Initial lists:
[1→4→5]  [1→3→4]  [2→6]

Heap: [(1,0,node), (1,1,node), (2,2,node)]
                ^
              min

Pop (1,0): result=[1], push 4 from list 0
Heap: [(1,1,node), (2,2,node), (4,0,node)]

Pop (1,1): result=[1,1], push 3 from list 1
Heap: [(2,2,node), (3,1,node), (4,0,node)]

Pop (2,2): result=[1,1,2], push 6 from list 2
Heap: [(3,1,node), (4,0,node), (6,2,node)]

... continue until heap empty

Final: [1,1,2,3,4,4,5,6]
```

---

## Related Problem: Smallest Range Covering K Lists

Given k sorted lists, find the smallest range that includes at least one number from each list.

```python
import heapq

def smallest_range(nums: list[list[int]]) -> list[int]:
    """
    Find smallest range covering all k lists.

    Time: O(n log k)
    Space: O(k)

    Track current max while heap tracks current min.
    """
    k = len(nums)
    # (value, list_index, element_index)
    heap = [(lst[0], i, 0) for i, lst in enumerate(nums) if lst]
    heapq.heapify(heap)

    current_max = max(lst[0] for lst in nums if lst)
    result = [heap[0][0], current_max]

    while True:
        min_val, list_idx, elem_idx = heapq.heappop(heap)

        # Update result if current range is smaller
        if current_max - min_val < result[1] - result[0]:
            result = [min_val, current_max]

        # Try to advance in the list that had minimum
        if elem_idx + 1 >= len(nums[list_idx]):
            break  # Can't advance, this is optimal

        next_val = nums[list_idx][elem_idx + 1]
        current_max = max(current_max, next_val)
        heapq.heappush(heap, (next_val, list_idx, elem_idx + 1))

    return result
```

---

## Edge Cases

```python
# 1. Empty lists array
merge_k_lists([])  # → None

# 2. All empty lists
merge_k_lists([None, None])  # → None

# 3. Single list
merge_k_lists([[1, 2, 3]])  # → [1, 2, 3]

# 4. One empty list
merge_k_lists([[1, 2], []])  # → [1, 2]

# 5. All same values
merge_k_lists([[1, 1], [1, 1]])  # → [1, 1, 1, 1]

# 6. Large k, small lists
merge_k_lists([[1], [2], [3], ...])  # Works fine with heap
```

---

## Interview Tips

1. **Draw the heap state**: Show interviewer you understand what's in heap
2. **Explain tiebreaker**: Why we need (value, index, node) not just (value, node)
3. **Mention both approaches**: Heap and divide & conquer
4. **Discuss trade-offs**: Heap better for streaming, D&C uses less space
5. **Handle edge cases**: Empty lists, None heads

---

## Common Mistakes

```python
# WRONG: Comparing ListNode objects
heap = [(node.val, node) for node in lists if node]
# Fails when values are equal

# CORRECT: Add unique index
heap = [(node.val, i, node) for i, node in enumerate(lists) if node]


# WRONG: Not checking for empty lists
for node in lists:
    heapq.heappush(heap, (node.val, 0, node))  # None.val fails!

# CORRECT: Filter None
for i, node in enumerate(lists):
    if node:
        heapq.heappush(heap, (node.val, i, node))


# WRONG: Forgetting to advance in same list
while heap:
    val, _, node = heapq.heappop(heap)
    result.append(val)
    # Missing: push node.next if exists!
```

---

## Practice Problems

| # | Problem | Difficulty | Key Variation |
|---|---------|------------|---------------|
| 1 | Merge k Sorted Lists | Hard | Core problem |
| 2 | Merge Two Sorted Lists | Easy | Building block |
| 3 | Smallest Range Covering Elements from K Lists | Hard | Range tracking |
| 4 | Find K Pairs with Smallest Sums | Medium | Two arrays |
| 5 | Kth Smallest Element in a Sorted Matrix | Medium | Matrix as k lists |

---

## Key Takeaways

1. **Min heap tracks k candidates**: One from each list
2. **Time O(n log k)**: Each of n elements does log k heap operations
3. **Tiebreaker needed**: Use index when values can be equal
4. **Two approaches**: Heap (streaming) vs Divide & Conquer
5. **heapq.merge**: Built-in for sorted iterables

---

## Next: [06-median-stream.md](./06-median-stream.md)

Learn the two-heap pattern for finding median from data stream.

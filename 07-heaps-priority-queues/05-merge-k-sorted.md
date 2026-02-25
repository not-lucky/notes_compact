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

## Building Intuition

**The Core Question: What's the Next Smallest Element?**

When merging sorted lists, at any moment the next element in the result MUST be the smallest among all current "heads":

```
Lists:
List 0: [1, 4, 5]    ← head is 1
List 1: [1, 3, 4]    ← head is 1
List 2: [2, 6]       ← head is 2

Next element = min(1, 1, 2) = 1 (from list 0 or 1)
```

**Why Heap? The Candidate Pool**

Think of it as a competition with k contestants, where each list sends one representative:

```
Round 1: Representatives = [1, 1, 2] from lists [0, 1, 2]
Winner: 1 from list 0
List 0 sends new representative: 4

Round 2: Representatives = [4, 1, 2]
Winner: 1 from list 1
List 1 sends new representative: 3

...and so on
```

The heap is our "judging panel" that quickly finds the winner (O(log k)).

**Why O(N log k) and Not O(N·k)?**

Let **N** be the total number of elements across all lists, and **k** be the number of lists.

```
Naive approach: For each of N elements, scan all k heads → O(N·k)

Heap approach: For each of N elements, do one heap operation → O(N log k)

With k=1000 lists and N=1,000,000 elements:
- Naive: 1,000,000 × 1,000 = 1 billion comparisons
- Heap: 1,000,000 × log₂(1000) ≈ 10 million comparisons
```

**Mental Model: K Conveyor Belts**

Imagine k conveyor belts, each holding a sorted sequence of boxes. You have one "output" belt where you place boxes in sorted order.

- You can only see the first box on each belt (the heads)
- To find the next box for output, compare all visible boxes and take the smallest
- That belt advances, revealing its next box

The heap is like a "quick-glance display" showing which belt currently has the smallest visible box.

**Why the Tiebreaker Index Matters**

```python
# When two heads have equal values:
(1, node_from_list_0)  vs  (1, node_from_list_1)

# Python tries to compare nodes → Error!
# Solution: (value, list_index, node)
(1, 0, node_from_list_0)  vs  (1, 1, node_from_list_1)
# Now: 0 < 1, comparison succeeds
```

---

## When NOT to Use Heap for Merge K Sorted

**1. K = 2 (Just Two Lists)**

For two lists, a simple two-pointer merge is cleaner:

```python
# Overkill for k=2:
heap = [(lists[0].val, 0, lists[0]), (lists[1].val, 1, lists[1])]

# Simpler:
while l1 and l2:
    if l1.val < l2.val:
        result.append(l1.val)
        l1 = l1.next
    else:
        result.append(l2.val)
        l2 = l2.next
```

**2. Lists Are Very Short**

If average list length is small, divide-and-conquer might have better constants:

```
10 lists of 5 elements each:
- Heap: overhead of heap operations for 50 elements
- D&C: simple merge of pairs, no heap overhead
```

**3. Lists Are on Disk (External Merge Sort)**

For datasets too large to fit in memory (e.g., merging many large server log files), you must use **External Merge Sort**:
- The principle remains the same: a min-heap tracks the smallest elements.
- Instead of tracking all individual nodes in RAM, you read small sorted "chunks" from each file into an in-memory buffer.
- When an element is popped from the heap, you pull the next item from that file's stream.
- This is exactly how massive databases perform large-scale `ORDER BY` operations.

**4. You Don't Need Fully Sorted Output**

If you just need, say, the first $m$ elements from the merged result:

```python
# Heap approach is perfect! Just stop after popping m elements.
# There is no need to process the rest of the elements.
```

**Red Flags:**

- "K is always 2" → Use a simple two-pointer merge
- "Files don't fit in memory" → You need an external merge sort (buffering chunks)
- "Only need first m elements" → Stop early; the heap approach is optimal here
- "Lists are actually linked lists" → Be careful to handle `None` gracefully

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

    Time: O(N log k) where N = total nodes, k = number of lists
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

Python's heapq compares tuples element by element. If values are equal, it compares the next element. `ListNode` objects aren't natively comparable in Python, so we need a tiebreaker:

```python
# This would fail:
heapq.heappush(heap, (1, node1))
heapq.heappush(heap, (1, node2))  # Error: '<' not supported between instances of 'ListNode' and 'ListNode'

# Solution 1: Add unique index (Cleanest)
heapq.heappush(heap, (1, 0, node1))
heapq.heappush(heap, (1, 1, node2))  # Works: 0 < 1 breaks tie
```

**Alternative: Wrapper Class**
In interviews, you may be asked how to solve this using Object-Oriented principles. You can create a wrapper class with the `__lt__` (less than) magic method:

```python
class Wrapper:
    def __init__(self, node):
        self.node = node

    def __lt__(self, other):
        # Only compare values. Python will now know how to sort Wrappers
        return self.node.val < other.node.val

# Usage: heapq.heappush(heap, Wrapper(node))
```

---

## Merge K Sorted Arrays

Same concept, different implementation:

```python
import heapq

def merge_k_sorted_arrays(arrays: list[list[int]]) -> list[int]:
    """
    Merge k sorted arrays.

    Time: O(N log k) where N is total elements across all k arrays
    Space: O(k) for heap + O(N) for result
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

    Time: O(N log k)
    Space: O(k) for iterators + O(N) for result list
    """
    return list(heapq.merge(*arrays))


# Usage
arrays = [[1, 4, 5], [1, 3, 4], [2, 6]]
print(merge_k_sorted_builtin(arrays))  # [1, 1, 2, 3, 4, 4, 5, 6]
```

**Note**: heapq.merge returns an iterator, not a list.

---

## Approach 2: Divide and Conquer

Merge pairs of lists iteratively, reducing k to k/2 each round. This can be done in `O(1)` auxiliary space without a recursion stack or allocating new lists in each round.

```python
from typing import Optional

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def merge_k_lists_divide_conquer(lists: list[Optional[ListNode]]) -> Optional[ListNode]:
    """
    Divide and conquer: merge pairs of lists iteratively.

    Time: O(N log k) - log k rounds, O(N) comparisons per round
    Space: O(1) auxiliary space (done in-place)
    """
    if not lists:
        return None

    amount = len(lists)
    interval = 1

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

    # Iteratively merge pairs in-place
    while interval < amount:
        for i in range(0, amount - interval, interval * 2):
            lists[i] = merge_two(lists[i], lists[i + interval])
        interval *= 2

    return lists[0]
```

---

## Comparison of Approaches

| Approach             | Time       | Space    | Notes                                  |
| -------------------- | ---------- | -------- | -------------------------------------- |
| Heap (Min Priority)  | O(N log k) | O(k)     | Best for streaming or large inputs     |
| Divide & Conquer     | O(N log k) | O(1)     | Iterative in-place needs no extra space|
| Merge one by one     | O(N·k)     | O(1)     | Naive loop comparison is too slow      |
| Collect all + sort   | O(N log N) | O(N)     | Easy to write but ignores sorted input |

**N** = total number of elements across all lists
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

    Time: O(N log k) where N is total elements, k is lists
    Space: O(k) for tracking one element from each list

    Track current max iteratively while heap tracks current min.
    """
    k = len(nums)
    heap = []
    current_max = float('-inf')

    # Initialize heap and current_max
    for i in range(k):
        # Only process if list is non-empty. If an empty list is allowed and
        # required to be in the range, the problem is impossible.
        if nums[i]:
            val = nums[i][0]
            heapq.heappush(heap, (val, i, 0))
            current_max = max(current_max, val)

    # If any list was empty, we can't find a range covering all lists
    if len(heap) < k:
        return []

    # Initialize result with initial min and max
    result = [heap[0][0], current_max]

    while True:
        min_val, list_idx, elem_idx = heapq.heappop(heap)

        # Update result if current range is strictly smaller
        if current_max - min_val < result[1] - result[0]:
            result = [min_val, current_max]

        # Try to advance in the list that had the minimum value
        if elem_idx + 1 >= len(nums[list_idx]):
            break  # Can't advance further, so this range is optimal

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
# Fails when values are equal (Python tries to compare node < node)

# CORRECT 1: Add unique index tiebreaker
heap = [(node.val, i, node) for i, node in enumerate(lists) if node]

# CORRECT 2: Wrapper Class with __lt__ defined


# WRONG: Not checking for empty lists
for node in lists:
    heapq.heappush(heap, (node.val, 0, node))  # None.val causes AttributeError!

# CORRECT: Filter None heads
for i, node in enumerate(lists):
    if node:
        heapq.heappush(heap, (node.val, i, node))


# WRONG: Forgetting to advance to the next node in the same list
while heap:
    val, idx, node = heapq.heappop(heap)
    result.append(val)
    # Missing: Must push node.next if it exists!
```

---

## Practice Problems

| #   | Problem                                       | Difficulty | Key Variation     |
| --- | --------------------------------------------- | ---------- | ----------------- |
| 1   | Merge k Sorted Lists                          | Hard       | Core problem      |
| 2   | Merge Two Sorted Lists                        | Easy       | Building block    |
| 3   | Smallest Range Covering Elements from K Lists | Hard       | Range tracking    |
| 4   | Find K Pairs with Smallest Sums               | Medium     | Two arrays        |
| 5   | Kth Smallest Element in a Sorted Matrix       | Medium     | Matrix as k lists |

---

## Key Takeaways

1. **Min heap tracks k candidates**: One from each list
2. **Time O(N log k)**: Each of N total elements does log k heap operations
3. **Tiebreaker needed**: Use index or wrapper class when values can be equal
4. **Two approaches**: Heap (streaming/large N) vs Divide & Conquer (in-place)
5. **heapq.merge**: Built-in for sorted iterables in Python

---

## Next: [06-median-stream.md](./06-median-stream.md)

Learn the two-heap pattern for finding median from data stream.

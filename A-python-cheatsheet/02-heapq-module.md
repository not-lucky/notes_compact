# Heapq Module

> **Prerequisites:** Understanding of heap data structure

## Interview Context

Python's `heapq` module implements a min-heap. It's essential for:

- **Top-K problems**: Find k largest/smallest elements
- **Merge K sorted lists**: Classic interview problem
- **Priority scheduling**: Task with priorities
- **Median finding**: Two-heap approach

**Key limitation**: Python only has min-heap. For max-heap, negate values.

---

## Basic Heap Operations

```python
import heapq

# Create heap from list (in-place, O(n))
nums = [3, 1, 4, 1, 5, 9, 2, 6]
heapq.heapify(nums)
print(nums)  # [1, 1, 2, 3, 5, 9, 4, 6] - heap property maintained

# Push element (O(log n))
heapq.heappush(nums, 0)
print(nums[0])  # 0 (new minimum)

# Pop minimum (O(log n))
smallest = heapq.heappop(nums)
print(smallest)  # 0

# Peek minimum without removing (O(1))
print(nums[0])  # 1 (next smallest)

# Push and pop in one operation (more efficient)
result = heapq.heappushpop(nums, -1)  # Push -1, then pop min
print(result)  # -1 (the new -1 was smallest, so it got popped)

# Pop and push in one operation
result = heapq.heapreplace(nums, 100)  # Pop min, then push 100
print(result)  # 1 (the old minimum)
```

---

## Max-Heap Workaround

```python
import heapq

# For max-heap, negate values
nums = [3, 1, 4, 1, 5, 9]

# Create max-heap by negating
max_heap = [-x for x in nums]
heapq.heapify(max_heap)

# Push (negate on insert)
heapq.heappush(max_heap, -10)

# Pop (negate on retrieval)
largest = -heapq.heappop(max_heap)
print(largest)  # 10

# Peek max
print(-max_heap[0])  # 9
```

---

## Top-K Operations

```python
import heapq

nums = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]

# K largest elements (O(n log k))
k_largest = heapq.nlargest(3, nums)
print(k_largest)  # [9, 6, 5]

# K smallest elements (O(n log k))
k_smallest = heapq.nsmallest(3, nums)
print(k_smallest)  # [1, 1, 2]

# With key function
words = ["apple", "pie", "banana", "cherry"]
longest = heapq.nlargest(2, words, key=len)
print(longest)  # ['banana', 'cherry']
```

### When to Use nlargest/nsmallest

```python
# Small k relative to n: Use heap (O(n log k))
heapq.nlargest(3, million_items)

# Large k (most of n): Sort instead (O(n log n), but faster in practice)
sorted(items)[-k:]

# k == 1: Just use min()/max()
max(items)
```

---

## Pattern: Top K Frequent Elements

```python
import heapq
from collections import Counter

def top_k_frequent(nums: list[int], k: int) -> list[int]:
    """
    Find k most frequent elements.

    Time: O(n log k)
    Space: O(n)
    """
    count = Counter(nums)

    # Use nlargest with key
    return heapq.nlargest(k, count.keys(), key=count.get)


# Alternative: min-heap of size k
def top_k_frequent_heap(nums: list[int], k: int) -> list[int]:
    count = Counter(nums)

    # Keep k largest by maintaining min-heap of size k
    heap = []
    for num, freq in count.items():
        heapq.heappush(heap, (freq, num))
        if len(heap) > k:
            heapq.heappop(heap)

    return [num for freq, num in heap]


# Test
print(top_k_frequent([1, 1, 1, 2, 2, 3], 2))  # [1, 2]
```

---

## Pattern: Merge K Sorted Lists

```python
import heapq

def merge_k_sorted(lists: list[list[int]]) -> list[int]:
    """
    Merge k sorted lists into one sorted list.

    Time: O(N log k) where N = total elements
    Space: O(k) for heap
    """
    result = []
    # Heap of (value, list_index, element_index)
    heap = []

    # Initialize with first element of each list
    for i, lst in enumerate(lists):
        if lst:
            heapq.heappush(heap, (lst[0], i, 0))

    while heap:
        val, list_idx, elem_idx = heapq.heappop(heap)
        result.append(val)

        # Push next element from same list
        if elem_idx + 1 < len(lists[list_idx]):
            next_val = lists[list_idx][elem_idx + 1]
            heapq.heappush(heap, (next_val, list_idx, elem_idx + 1))

    return result


# Test
lists = [[1, 4, 5], [1, 3, 4], [2, 6]]
print(merge_k_sorted(lists))  # [1, 1, 2, 3, 4, 4, 5, 6]
```

---

## Pattern: Kth Largest Element

```python
import heapq

def find_kth_largest(nums: list[int], k: int) -> int:
    """
    Find kth largest element.

    Time: O(n log k)
    Space: O(k)
    """
    # Maintain min-heap of size k
    heap = []
    for num in nums:
        heapq.heappush(heap, num)
        if len(heap) > k:
            heapq.heappop(heap)

    return heap[0]  # Smallest among k largest = kth largest


# Alternative: Use nlargest
def find_kth_largest_v2(nums: list[int], k: int) -> int:
    return heapq.nlargest(k, nums)[-1]


# Test
print(find_kth_largest([3, 2, 1, 5, 6, 4], 2))  # 5
```

---

## Pattern: Median from Data Stream

```python
import heapq

class MedianFinder:
    """
    Two heaps: max-heap for lower half, min-heap for upper half.

    Invariant: len(small) == len(large) or len(small) == len(large) + 1

    Time: O(log n) add, O(1) find
    Space: O(n)
    """

    def __init__(self):
        self.small = []  # Max-heap (negated values)
        self.large = []  # Min-heap

    def addNum(self, num: int) -> None:
        # Add to max-heap
        heapq.heappush(self.small, -num)

        # Balance: move largest of small to large
        heapq.heappush(self.large, -heapq.heappop(self.small))

        # Ensure small >= large in size
        if len(self.large) > len(self.small):
            heapq.heappush(self.small, -heapq.heappop(self.large))

    def findMedian(self) -> float:
        if len(self.small) > len(self.large):
            return -self.small[0]
        return (-self.small[0] + self.large[0]) / 2


# Test
mf = MedianFinder()
mf.addNum(1)
mf.addNum(2)
print(mf.findMedian())  # 1.5
mf.addNum(3)
print(mf.findMedian())  # 2
```

---

## Pattern: Task Scheduler

```python
import heapq
from collections import Counter

def least_interval(tasks: list[str], n: int) -> int:
    """
    Find minimum intervals to complete all tasks with cooldown n.

    Time: O(T log 26) where T = total tasks
    Space: O(26) = O(1)
    """
    count = Counter(tasks)

    # Max-heap of remaining counts (negated)
    heap = [-c for c in count.values()]
    heapq.heapify(heap)

    time = 0

    while heap:
        # Process up to n+1 tasks in each round
        temp = []
        for _ in range(n + 1):
            if heap:
                cnt = -heapq.heappop(heap)
                if cnt > 1:
                    temp.append(-(cnt - 1))

            time += 1

            # If heap and temp are both empty, we're done
            if not heap and not temp:
                break

        # Push remaining tasks back
        for item in temp:
            heapq.heappush(heap, item)

    return time


# Test
print(least_interval(["A", "A", "A", "B", "B", "B"], 2))  # 8
```

---

## Pattern: K Closest Points

```python
import heapq

def k_closest(points: list[list[int]], k: int) -> list[list[int]]:
    """
    Find k closest points to origin.

    Time: O(n log k)
    Space: O(k)
    """
    # Max-heap of (-distance, point)
    heap = []

    for x, y in points:
        dist = x * x + y * y
        heapq.heappush(heap, (-dist, [x, y]))
        if len(heap) > k:
            heapq.heappop(heap)

    return [point for _, point in heap]


# Test
points = [[1, 3], [-2, 2], [5, 8], [0, 1]]
print(k_closest(points, 2))  # [[-2, 2], [0, 1]] or [[0, 1], [-2, 2]]
```

---

## Heap with Custom Comparison

```python
import heapq

# Method 1: Use tuples (compares element by element)
tasks = [(3, "low"), (1, "high"), (2, "medium")]
heapq.heapify(tasks)
print(heapq.heappop(tasks))  # (1, 'high')

# Method 2: Wrapper class with __lt__
class Task:
    def __init__(self, priority, name):
        self.priority = priority
        self.name = name

    def __lt__(self, other):
        return self.priority < other.priority

heap = [Task(3, "low"), Task(1, "high")]
heapq.heapify(heap)
print(heapq.heappop(heap).name)  # 'high'
```

---

## Complexity Summary

| Operation | Time | Notes |
|-----------|------|-------|
| heapify | O(n) | Build heap from list |
| heappush | O(log n) | Add element |
| heappop | O(log n) | Remove min |
| heap[0] | O(1) | Peek min |
| nlargest(k, n) | O(n log k) | Find k largest |
| nsmallest(k, n) | O(n log k) | Find k smallest |

---

## Common Mistakes

1. **Forgetting it's min-heap only**: Negate for max-heap
2. **Modifying heap directly**: Use heapq functions, not list methods
3. **Assuming sorted**: Heap is NOT fully sorted, only heap property
4. **Using for max when k is large**: Sort may be faster

---

## Practice Problems

| # | Problem | Pattern |
|---|---------|---------|
| 1 | Kth Largest Element | Min-heap of size k |
| 2 | Top K Frequent Elements | Counter + heap |
| 3 | Merge K Sorted Lists | Multi-way merge |
| 4 | Find Median from Data Stream | Two heaps |
| 5 | Task Scheduler | Max-heap + simulation |
| 6 | K Closest Points to Origin | Max-heap of size k |
| 7 | Ugly Number II | Min-heap for generation |

---

## Related Sections

- [Collections Module](./01-collections-module.md) - Counter for frequency
- [Bisect Module](./03-bisect-module.md) - Alternative for sorted data

# Python heapq Module Solutions

## 1. Kth Largest Element in a Stream

Design a class to find the kth largest element in a stream. Note that it is the kth largest element in the sorted order, not the kth distinct element.

### Examples & Edge Cases

- **Example**: `k=3, nums=[4, 5, 8, 2]`. `add(3) -> 4`, `add(5) -> 5`.
- **Edge Case: k=1**: Track only the maximum element.
- **Edge Case: All same values**: Handled correctly by heap property.

### Optimal Python Solution

```python
import heapq

class KthLargest:
    """
    Maintains a min-heap of the k largest elements seen so far.
    The root of the min-heap is the kth largest element.

    Time Complexity: O(n log k) for init, O(log k) for add
    Space Complexity: O(k)
    """
    def __init__(self, k: int, nums: list[int]):
        self.k = k
        self.min_heap = nums
        heapq.heapify(self.min_heap)

        # Shrink heap to exactly k largest elements
        while len(self.min_heap) > k:
            heapq.heappop(self.min_heap)

    def add(self, val: int) -> int:
        if len(self.min_heap) < self.k:
            heapq.heappush(self.min_heap, val)
        elif val > self.min_heap[0]:
            # Only push if val is larger than the current kth largest
            heapq.heapreplace(self.min_heap, val)

        return self.min_heap[0]
```

### Explanation

1.  **Min-Heap of Top-K**: To track the $k$ largest elements, a min-heap is used. The smallest element in this "large" set is the $k$-th largest element of the entire stream.
2.  **Add Logic**: We only need to store $k$ elements. If a new value is larger than the root (the current $k$-th largest), it replaces the root.

### Complexity Analysis

- **Time Complexity**:
  - `__init__`: $O(n \log k)$ (or $O(n)$ if we pop $n-k$ times).
  - `add`: $O(\log k)$ to maintain the heap.
- **Space Complexity**: $O(k)$ to store the heap.

---

## 2. Last Stone Weight

Smash the two heaviest stones. Return the weight of the last stone or 0.

### Examples & Edge Cases

- **Example**: `[2,7,4,1,8,1] -> 1`
- **Edge Case: One stone**: Returns that stone.
- **Edge Case: No stones**: Returns 0.

### Optimal Python Solution

```python
import heapq

def lastStoneWeight(stones: list[int]) -> int:
    """
    Use a max-heap (negated values) to repeatedly get the two largest stones.

    Time Complexity: O(n log n)
    Space Complexity: O(n)
    """
    # Create max-heap by negating values
    max_heap = [-s for s in stones]
    heapq.heapify(max_heap)

    while len(max_heap) > 1:
        s1 = -heapq.heappop(max_heap)
        s2 = -heapq.heappop(max_heap)

        if s1 != s2:
            heapq.heappush(max_heap, -(s1 - s2))

    return -max_heap[0] if max_heap else 0
```

### Explanation

1.  **Max-Heap Simulation**: Since Python's `heapq` is a min-heap, we negate the values to turn it into a max-heap.
2.  **Greedy Removal**: We always pop the two largest. The difference, if non-zero, is pushed back.

### Complexity Analysis

- **Time Complexity**: $O(n \log n)$.
- **Space Complexity**: $O(n)$.

---

## 3. Top K Frequent Elements

Given an integer array `nums` and an integer `k`, return the `k` most frequent elements.

### Examples & Edge Cases

- **Example**: `nums = [1,1,1,2,2,3], k = 2` -> `[1,2]`
- **Edge Case: k = unique elements**: Return all unique elements.
- **Edge Case: Ties in frequency**: Any of the tied elements can be part of the result.

### Optimal Python Solution

```python
import heapq
from collections import Counter

def topKFrequent(nums: list[int], k: int) -> list[int]:
    """
    Use a hash map for counts, then a min-heap of size k to find the top frequent.

    Time Complexity: O(n log k)
    Space Complexity: O(n)
    """
    if k == len(nums):
        return nums

    # 1. Count frequencies: O(n)
    counts = Counter(nums)

    # 2. Find k largest elements based on frequency: O(u log k) where u is unique elements
    return heapq.nlargest(k, counts.keys(), key=counts.get)
```

### Explanation

1.  **Count**: We first count occurrences using `Counter`.
2.  **Heap Selection**: `heapq.nlargest` allows us to find the top $k$ keys based on their values (frequencies) in $O(n \log k)$ time.

### Complexity Analysis

- **Time Complexity**: $O(n \log k)$. Counting is $O(n)$, and selection is $O(u \log k)$ where $u$ is number of unique elements.
- **Space Complexity**: $O(n)$ to store the frequencies.

---

## 4. Merge k Sorted Lists

Merge `k` sorted linked lists and return it as one sorted list.

### Examples & Edge Cases

- **Example**: `[[1,4,5], [1,3,4], [2,6]] -> [1,1,2,3,4,4,5,6]`
- **Edge Case: Empty input**: `[]` -> `None`.
- **Edge Case: Empty lists inside input**: `[[], [1]]` -> `[1]`.

### Optimal Python Solution

```python
import heapq

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def mergeKLists(lists: list[ListNode]) -> ListNode:
    """
    Use a min-heap to keep track of the head of each list.

    Time Complexity: O(N log k) where N is total nodes, k is number of lists
    Space Complexity: O(k) for the heap
    """
    min_heap = []

    # Initialize heap with the head of each non-empty list
    # Use the index 'i' as a tiebreaker because ListNode is not comparable
    for i, l in enumerate(lists):
        if l:
            heapq.heappush(min_heap, (l.val, i, l))

    dummy = ListNode()
    current = dummy

    while min_heap:
        val, i, node = heapq.heappop(min_heap)

        # Append the smallest node found to our result list
        current.next = node
        current = current.next

        # If the extracted node has a next node, push it to the heap
        if node.next:
            heapq.heappush(min_heap, (node.next.val, i, node.next))

    return dummy.next
```

### Explanation

1.  **Heap of Heads**: We keep the current head of each list in a min-heap.
2.  **Tie-breaking**: We store `(val, i, node)` in the heap. The index `i` ensures that if two nodes have the same value, Python compares the indices instead of trying to compare the `ListNode` objects (which would raise a TypeError).
3.  **Efficiency**: Each time we pop a node, we add its `next` pointer to the heap, maintaining exactly $k$ elements in the heap at all times.

### Complexity Analysis

- **Time Complexity**: $O(N \log k)$. Each of the $N$ nodes is added and removed from the heap once.
- **Space Complexity**: $O(k)$ for the heap.

---

## 5. Find Median from Data Stream

Implement `MedianFinder` class with `addNum` and `findMedian`.

### Examples & Edge Cases

- **Example**: `add(1), add(2) -> median 1.5`, `add(3) -> median 2`.
- **Edge Case: Single element**: Median is the element.
- **Edge Case: Large data stream**: The two-heap approach handles this efficiently.

### Optimal Python Solution

```python
import heapq

class MedianFinder:
    """
    Uses two heaps: a max-heap for the smaller half and a min-heap for the larger half.

    Time Complexity: O(log n) for add, O(1) for median
    Space Complexity: O(n)
    """
    def __init__(self):
        # max_heap (negated) stores the smaller half
        self.small = []
        # min_heap stores the larger half
        self.large = []

    def addNum(self, num: int) -> None:
        # 1. Push to max_heap (small half)
        heapq.heappush(self.small, -num)

        # 2. Ensure every element in small <= every element in large
        # Pop max from small and push to large
        val = -heapq.heappop(self.small)
        heapq.heappush(self.large, val)

        # 3. Balance sizes: small can have at most 1 more element than large
        if len(self.large) > len(self.small):
            val = heapq.heappop(self.large)
            heapq.heappush(self.small, -val)

    def findMedian(self) -> float:
        if len(self.small) > len(self.large):
            return -self.small[0]
        else:
            return (-self.small[0] + self.large[0]) / 2.0
```

### Explanation

1.  **Two Heaps**: We divide the numbers into two halves. The lower half is in a max-heap (`small`), and the upper half is in a min-heap (`large`).
2.  **Balancing**:
    - We push to `small` first, then move the largest of `small` to `large` to ensure the "smaller half" property.
    - We then balance so that `small` always has the same or one more element than `large`.
3.  **Median Calculation**: If the total count is odd, the root of `small` is the median. If even, the average of the two roots is the median.

### Complexity Analysis

- **Time Complexity**: `addNum` is $O(\log n)$, `findMedian` is $O(1)$.
- **Space Complexity**: $O(n)$ to store all numbers.

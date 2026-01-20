# Top K Frequent Elements

## Problem Statement

Given an integer array `nums` and an integer `k`, return the `k` most frequent elements. You may return the answer in any order.

**Example:**
```
Input: nums = [1,1,1,2,2,3], k = 2
Output: [1, 2]

Input: nums = [1], k = 1
Output: [1]
```

## Building Intuition

### Why This Works

The problem breaks into two phases: counting frequencies (O(n) with hash map), then finding the top k by frequency. The heap approach maintains a min-heap of size k - by keeping only k elements and evicting the smallest whenever we exceed k, the heap eventually contains exactly the k largest.

Bucket sort exploits a key constraint: frequencies are bounded by n (a number can appear at most n times). We create n+1 buckets, place each number in the bucket matching its frequency, then collect from highest bucket down until we have k elements. This achieves O(n) time because bucket operations are O(1).

Quickselect partitions elements so that the k most frequent end up on one side, without fully sorting. It's like quicksort but only recursing on the side containing the k-th position.

### How to Discover This

When you see "top k" or "k largest/smallest," think heaps (O(n log k)) or quickselect (O(n) average). When frequencies are involved, consider bucket sort if the frequency range is bounded. The choice depends on constraints: heap for guaranteed O(n log k), bucket for O(n) when frequencies are bounded, quickselect for average O(n) with worse worst case.

### Pattern Recognition

This is the **Top K Selection** pattern. Count occurrences with a hash map, then select top k using either: (1) min-heap of size k, (2) bucket sort when range is bounded, or (3) quickselect for average O(n). The same pattern solves "k closest points," "k most frequent words," and similar problems.

## When NOT to Use

- **When k equals n (return all elements sorted)**: Full sorting is cleaner than heap/quickselect; just sort the unique elements by frequency.
- **When frequencies are unbounded or unknown**: Bucket sort requires knowing the maximum frequency; use heap or quickselect instead.
- **When you need stable ordering among equal-frequency elements**: Heaps and quickselect don't preserve insertion order; additional bookkeeping is needed.
- **When the data is streaming and k changes dynamically**: A single query structure doesn't adapt well; consider data structures designed for dynamic top-k tracking.

## Approach

### Method 1: Heap
Count frequencies, use min-heap of size k.

### Method 2: Bucket Sort
Create buckets by frequency, iterate from highest.

### Method 3: Quickselect
Partition based on frequency (average O(n)).

## Implementation

```python
def top_k_frequent(nums: list[int], k: int) -> list[int]:
    """
    Using heap approach.

    Time: O(n log k)
    Space: O(n)
    """
    from collections import Counter
    import heapq

    count = Counter(nums)

    # Min heap of (freq, num), keep size k
    return heapq.nlargest(k, count.keys(), key=count.get)


def top_k_frequent_bucket(nums: list[int], k: int) -> list[int]:
    """
    Using bucket sort (O(n) time).

    Time: O(n)
    Space: O(n)
    """
    from collections import Counter

    count = Counter(nums)

    # Buckets: index = frequency, value = list of numbers
    n = len(nums)
    buckets = [[] for _ in range(n + 1)]

    for num, freq in count.items():
        buckets[freq].append(num)

    # Collect k elements from highest frequency
    result = []
    for freq in range(n, 0, -1):
        for num in buckets[freq]:
            result.append(num)
            if len(result) == k:
                return result

    return result


def top_k_frequent_quickselect(nums: list[int], k: int) -> list[int]:
    """
    Using quickselect (average O(n)).

    Time: O(n) average, O(n²) worst
    Space: O(n)
    """
    from collections import Counter
    import random

    count = Counter(nums)
    unique = list(count.keys())

    def partition(left: int, right: int) -> int:
        pivot_idx = random.randint(left, right)
        pivot_freq = count[unique[pivot_idx]]

        # Move pivot to end
        unique[pivot_idx], unique[right] = unique[right], unique[pivot_idx]

        store_idx = left
        for i in range(left, right):
            if count[unique[i]] > pivot_freq:
                unique[store_idx], unique[i] = unique[i], unique[store_idx]
                store_idx += 1

        # Move pivot to final position
        unique[store_idx], unique[right] = unique[right], unique[store_idx]
        return store_idx

    left, right = 0, len(unique) - 1

    while left <= right:
        pivot_idx = partition(left, right)
        if pivot_idx == k - 1:
            return unique[:k]
        elif pivot_idx < k - 1:
            left = pivot_idx + 1
        else:
            right = pivot_idx - 1

    return unique[:k]
```

## Complexity Analysis

| Method | Time | Space | Notes |
|--------|------|-------|-------|
| Heap | O(n log k) | O(n + k) | Good for small k |
| Bucket Sort | O(n) | O(n) | Best worst-case |
| Quickselect | O(n) avg | O(n) | O(n²) worst |

## Variations

### Kth Largest Element
```python
def find_kth_largest(nums: list[int], k: int) -> int:
    """
    Find kth largest element.

    Time: O(n) average with quickselect
    Space: O(1)
    """
    import heapq
    return heapq.nlargest(k, nums)[-1]


def find_kth_largest_quickselect(nums: list[int], k: int) -> int:
    """
    Quickselect approach.
    """
    import random

    def partition(left, right):
        pivot_idx = random.randint(left, right)
        pivot = nums[pivot_idx]
        nums[pivot_idx], nums[right] = nums[right], nums[pivot_idx]

        store = left
        for i in range(left, right):
            if nums[i] > pivot:
                nums[store], nums[i] = nums[i], nums[store]
                store += 1

        nums[store], nums[right] = nums[right], nums[store]
        return store

    left, right = 0, len(nums) - 1
    target = k - 1

    while left <= right:
        pivot = partition(left, right)
        if pivot == target:
            return nums[pivot]
        elif pivot < target:
            left = pivot + 1
        else:
            right = pivot - 1

    return -1
```

### Merge K Sorted Lists
```python
def merge_k_lists(lists: list) -> 'ListNode':
    """
    Merge k sorted linked lists.

    Time: O(N log k) where N = total nodes
    Space: O(k)
    """
    import heapq

    # Make ListNode comparable
    ListNode.__lt__ = lambda self, other: self.val < other.val

    heap = []
    for lst in lists:
        if lst:
            heapq.heappush(heap, lst)

    dummy = ListNode(0)
    current = dummy

    while heap:
        node = heapq.heappop(heap)
        current.next = node
        current = current.next

        if node.next:
            heapq.heappush(heap, node.next)

    return dummy.next
```

### K Closest Points to Origin
```python
def k_closest(points: list[list[int]], k: int) -> list[list[int]]:
    """
    Find k closest points to origin.

    Time: O(n log k)
    Space: O(k)
    """
    import heapq

    # Max heap (negate distance)
    heap = []

    for x, y in points:
        dist = -(x*x + y*y)  # Negate for max heap

        if len(heap) < k:
            heapq.heappush(heap, (dist, [x, y]))
        elif dist > heap[0][0]:
            heapq.heapreplace(heap, (dist, [x, y]))

    return [point for _, point in heap]
```

## Related Problems

- **Kth Largest Element in an Array** - Single element, not top k
- **Merge K Sorted Lists** - Heap for ordered merging
- **K Closest Points to Origin** - Similar pattern
- **Sort Characters By Frequency** - Bucket sort approach
- **Top K Frequent Words** - With lexicographic tiebreaker

# Solution: Python heapq Module Practice Problems

## Problem 1: Kth Largest Element in a Stream
### Problem Statement
Design a class to find the kth largest element in a stream. Note that it is the kth largest element in the sorted order, not the kth distinct element.

Implement `KthLargest` class:
- `KthLargest(int k, int[] nums)` Initializes the object with the integer `k` and the stream of integers `nums`.
- `int add(int val)` Appends the integer `val` to the stream and returns the element representing the kth largest element in the stream.

### Constraints
- `1 <= k <= 10^4`
- `0 <= nums.length <= 10^4`
- `-10^4 <= nums[i] <= 10^4`
- `-10^4 <= val <= 10^4`
- At most `10^4` calls will be made to `add`.

### Example
Input: `["KthLargest", "add", "add", "add", "add", "add"]`, `[[3, [4, 5, 8, 2]], [3], [5], [10], [9], [4]]`
Output: `[null, 4, 5, 5, 8, 8]`

### Python Implementation
```python
import heapq

class KthLargest:
    def __init__(self, k: int, nums: list[int]):
        """
        Time Complexity: O(n log k)
        Space Complexity: O(k)
        """
        self.k = k
        self.heap = []
        for n in nums:
            self.add(n)

    def add(self, val: int) -> int:
        """
        Time Complexity: O(log k)
        """
        heapq.heappush(self.heap, val)
        if len(self.heap) > self.k:
            heapq.heappop(self.heap)
        return self.heap[0]
```

---

## Problem 2: Last Stone Weight
### Problem Statement
You are given an array of integers `stones` where `stones[i]` is the weight of the `i`th stone.

We are playing a game with the stones. On each turn, we choose the heaviest two stones and smash them together. Suppose the heaviest two stones have weights `x` and `y` with `x <= y`. The result of this smash is:
- If `x == y`, both stones are destroyed.
- If `x != y`, the stone of weight `x` is destroyed, and the stone of weight `y` has new weight `y - x`.

At the end of the game, there is at most one stone left. Return the weight of the last remaining stone. If there are no stones left, return 0.

### Constraints
- `1 <= stones.length <= 30`
- `1 <= stones[i] <= 1000`

### Example
Input: `stones = [2,7,4,1,8,1]`
Output: `1`

### Python Implementation
```python
import heapq

def lastStoneWeight(stones: list[int]) -> int:
    """
    Time Complexity: O(n log n)
    Space Complexity: O(n)
    """
    # Max heap (negated values)
    max_heap = [-s for s in stones]
    heapq.heapify(max_heap)

    while len(max_heap) > 1:
        y = -heapq.heappop(max_heap)
        x = -heapq.heappop(max_heap)

        if x != y:
            heapq.heappush(max_heap, -(y - x))

    return -max_heap[0] if max_heap else 0
```

---

## Problem 3: Top K Frequent Elements
### Problem Statement
Given an integer array `nums` and an integer `k`, return the `k` most frequent elements. You may return the answer in any order.

### Constraints
- `1 <= nums.length <= 10^5`
- `k` is in the range `[1, the number of unique elements in the array]`.
- It is guaranteed that the answer is unique.

### Example
Input: `nums = [1,1,1,2,2,3], k = 2`
Output: `[1,2]`

### Python Implementation
```python
import heapq
from collections import Counter

def topKFrequent(nums: list[int], k: int) -> list[int]:
    """
    Time Complexity: O(n log k)
    Space Complexity: O(n)
    """
    if k == len(nums):
        return nums

    count = Counter(nums)
    return heapq.nlargest(k, count.keys(), key=count.get)
```

---

## Problem 4: Merge k Sorted Lists
### Problem Statement
You are given an array of `k` linked-lists `lists`, each linked-list is sorted in ascending order.

Merge all the linked-lists into one sorted linked-list and return it.

### Constraints
- `k == lists.length`
- `0 <= k <= 10^4`
- `0 <= lists[i].length <= 500`
- `-10^4 <= lists[i][j] <= 10^4`
- `lists[i]` is sorted in ascending order.
- The total number of nodes will not exceed `10^4`.

### Python Implementation
```python
import heapq
from typing import Optional

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def mergeKLists(lists: list[Optional[ListNode]]) -> Optional[ListNode]:
    """
    Time Complexity: O(n log k)
    Space Complexity: O(k)
    """
    heap = []
    for i, node in enumerate(lists):
        if node:
            heapq.heappush(heap, (node.val, i, node))

    dummy = ListNode(0)
    curr = dummy

    while heap:
        val, i, node = heapq.heappop(heap)
        curr.next = node
        curr = curr.next
        if node.next:
            heapq.heappush(heap, (node.next.val, i, node.next))

    return dummy.next
```

---

## Problem 5: Find Median from Data Stream
### Problem Statement
The median is the middle value in an ordered integer list. If the size of the list is even, there is no middle value, and the median is the mean of the two middle values.

Implement the `MedianFinder` class:
- `MedianFinder()` initializes the `MedianFinder` object.
- `void addNum(int num)` adds the integer `num` from the data stream to the data structure.
- `double findMedian()` returns the median of all elements so far. Answers within `10^-5` of the actual answer will be accepted.

### Constraints
- `-10^5 <= num <= 10^5`
- There will be at least one element in the data structure before calling `findMedian`.
- At most `5 * 10^4` calls will be made to `addNum` and `findMedian`.

### Python Implementation
```python
import heapq

class MedianFinder:
    def __init__(self):
        """
        Time Complexity: O(log n) for addNum, O(1) for findMedian
        Space Complexity: O(n)
        """
        self.left = []   # Max heap (negated)
        self.right = []  # Min heap

    def addNum(self, num: int) -> None:
        heapq.heappush(self.left, -num)
        heapq.heappush(self.right, -heapq.heappop(self.left))
        if len(self.left) < len(self.right):
            heapq.heappush(self.left, -heapq.heappop(self.right))

    def findMedian(self) -> float:
        if len(self.left) > len(self.right):
            return -self.left[0]
        return (-self.left[0] + self.right[0]) / 2.0
```

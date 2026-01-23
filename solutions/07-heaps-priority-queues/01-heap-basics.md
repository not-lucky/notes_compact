# Solution: Heap Basics Practice Problems

## Problem 1: Last Stone Weight
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
Explanation:
We combine 7 and 8 to get 1 so the array converts to [2,4,1,1,1] then,
we combine 2 and 4 to get 2 so the array converts to [2,1,1,1] then,
we combine 2 and 1 to get 1 so the array converts to [1,1,1] then,
we combine 1 and 1 to get 0 so the array converts to [1] then that's the value of the last stone.

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

## Problem 2: Kth Largest Element in a Stream
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

## Problem 3: Sort an Array (Heap Sort)
### Problem Statement
Given an array of integers `nums`, sort the array in ascending order and return it.

### Constraints
- `1 <= nums.length <= 5 * 10^4`
- `-5 * 10^4 <= nums[i] <= 5 * 10^4`

### Example
Input: `nums = [5,2,3,1]`
Output: `[1,2,3,5]`

### Python Implementation
```python
import heapq

def sortArray(nums: list[int]) -> list[int]:
    """
    Time Complexity: O(n log n)
    Space Complexity: O(n)
    """
    heapq.heapify(nums)
    return [heapq.heappop(nums) for _ in range(len(nums))]
```

---

## Problem 4: Kth Largest Element in an Array
### Problem Statement
Given an integer array `nums` and an integer `k`, return the `k`th largest element in the array.

Note that it is the `k`th largest element in the sorted order, not the `k`th distinct element.

### Constraints
- `1 <= k <= nums.length <= 10^5`
- `-10^4 <= nums[i] <= 10^4`

### Example
Input: `nums = [3,2,1,5,6,4], k = 2`
Output: `5`

### Python Implementation
```python
import heapq

def findKthLargest(nums: list[int], k: int) -> int:
    """
    Time Complexity: O(n log k)
    Space Complexity: O(k)
    """
    heap = []
    for num in nums:
        heapq.heappush(heap, num)
        if len(heap) > k:
            heapq.heappop(heap)
    return heap[0]
```

# Solution: Top-K Pattern Practice Problems

## Problem 1: Kth Largest Element in an Array
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

---

## Problem 2: Top K Frequent Elements
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
    count = Counter(nums)
    return heapq.nlargest(k, count.keys(), key=count.get)
```

---

## Problem 3: K Closest Points to Origin
### Problem Statement
Given an array of `points` where `points[i] = [xi, yi]` represents a point on the X-Y plane and an integer `k`, return the `k` closest points to the origin `(0, 0)`.

The distance between two points on the X-Y plane is the Euclidean distance (i.e., `√(x1 - x2)^2 + (y1 - y2)^2`).

### Constraints
- `1 <= k <= points.length <= 10^4`
- `-10^4 <= xi, yi <= 10^4`

### Example
Input: `points = [[1,3],[-2,2]], k = 1`
Output: `[[-2,2]]`

### Python Implementation
```python
import heapq

def kClosest(points: list[list[int]], k: int) -> list[list[int]]:
    """
    Time Complexity: O(n log k)
    Space Complexity: O(k)
    """
    # Max heap of (-distance, point)
    heap = []
    for x, y in points:
        dist = x*x + y*y
        if len(heap) < k:
            heapq.heappush(heap, (-dist, [x, y]))
        elif dist < -heap[0][0]:
            heapq.heapreplace(heap, (-dist, [x, y]))

    return [p for d, p in heap]
```

---

## Problem 4: Kth Largest Element in a Stream
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

## Problem 5: Top K Frequent Words
### Problem Statement
Given an array of strings `words` and an integer `k`, return the `k` most frequent strings.

Return the answer sorted by the frequency from highest to lowest. Sort the words with the same frequency by their lexicographical order.

### Constraints
- `1 <= words.length <= 500`
- `1 <= words[i].length <= 10`
- `words[i]` consists of lowercase English letters.
- `k` is in the range `[1, The number of unique words[i]]`

### Example
Input: `words = ["i","love","leetcode","i","love","coding"], k = 2`
Output: `["i","love"]`

### Python Implementation
```python
import heapq
from collections import Counter

class Word:
    def __init__(self, word, freq):
        self.word = word
        self.freq = freq

    def __lt__(self, other):
        if self.freq == other.freq:
            # For min-heap to keep k largest frequencies,
            # we want to keep lexicographically smaller words.
            # So in min-heap, larger word is "smaller" (to be popped).
            return self.word > other.word
        return self.freq < other.freq

def topKFrequent(words: list[str], k: int) -> list[str]:
    """
    Time Complexity: O(n log k)
    Space Complexity: O(n)
    """
    count = Counter(words)
    heap = []

    for word, freq in count.items():
        heapq.heappush(heap, Word(word, freq))
        if len(heap) > k:
            heapq.heappop(heap)

    res = []
    while heap:
        res.append(heapq.heappop(heap).word)
    return res[::-1]
```

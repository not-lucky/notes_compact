# Solution: Median from Stream Practice Problems

## Problem 1: Find Median from Data Stream
### Problem Statement
The median is the middle value in an ordered integer list. If the size of the list is even, there is no middle value, and the median is the mean of the two middle values.

Implement the `MedianFinder` class:
- `MedianFinder()` initializes the `MedianFinder` object.
- `void addNum(int num)` adds the integer `num` from the data stream to the data structure.
- `double findMedian()` returns the median of all elements so far.

### Constraints
- `-10^5 <= num <= 10^5`
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
        # Step 1: Add to left (max heap)
        heapq.heappush(self.left, -num)

        # Step 2: Balance - largest of left goes to right
        heapq.heappush(self.right, -heapq.heappop(self.left))

        # Step 3: Ensure left has >= elements than right
        if len(self.left) < len(self.right):
            heapq.heappush(self.left, -heapq.heappop(self.right))

    def findMedian(self) -> float:
        if len(self.left) > len(self.right):
            return -self.left[0]
        return (-self.left[0] + self.right[0]) / 2.0
```

---

## Problem 2: Sliding Window Median
### Problem Statement
Given an integer array `nums` and an integer `k`, there is a sliding window of size `k` which is moving from the very left of the array to the very right. You can only see the `k` numbers in the window. Each time the sliding window moves right by one position.

Return the median array for each window in the original array.

### Constraints
- `1 <= nums.length <= 10^5`
- `1 <= k <= nums.length`
- `-2^31 <= nums[i] <= 2^31 - 1`

### Python Implementation
```python
import heapq
from collections import defaultdict

class SlidingWindowMedian:
    def __init__(self, k):
        self.k = k
        self.left = []   # Max heap
        self.right = []  # Min heap
        self.removed = defaultdict(int)
        self.left_size = 0
        self.right_size = 0

    def add(self, num):
        if not self.left or num <= -self.left[0]:
            heapq.heappush(self.left, -num)
            self.left_size += 1
        else:
            heapq.heappush(self.right, num)
            self.right_size += 1
        self._balance()

    def remove(self, num):
        self.removed[num] += 1
        if num <= -self.left[0]:
            self.left_size -= 1
        else:
            self.right_size -= 1
        self._balance()

    def _balance(self):
        while self.left_size > (self.k + 1) // 2:
            val = -heapq.heappop(self.left)
            if self.removed[val] > 0:
                self.removed[val] -= 1
            else:
                heapq.heappush(self.right, val)
                self.right_size += 1
                self.left_size -= 1

        while self.left_size < (self.k + 1) // 2:
            val = heapq.heappop(self.right)
            if self.removed[val] > 0:
                self.removed[val] -= 1
            else:
                heapq.heappush(self.left, -val)
                self.left_size += 1
                self.right_size -= 1

        while self.left and self.removed[-self.left[0]] > 0:
            self.removed[-heapq.heappop(self.left)] -= 1
        while self.right and self.removed[self.right[0]] > 0:
            self.removed[heapq.heappop(self.right)] -= 1

    def get_median(self):
        if self.k % 2 == 1:
            return float(-self.left[0])
        return (-self.left[0] + self.right[0]) / 2.0

def medianSlidingWindow(nums: list[int], k: int) -> list[float]:
    """
    Time Complexity: O(n log k)
    Space Complexity: O(k)
    """
    swm = SlidingWindowMedian(k)
    res = []
    for i in range(len(nums)):
        swm.add(nums[i])
        if i >= k:
            swm.remove(nums[i - k])
        if i >= k - 1:
            res.append(swm.get_median())
    return res
```

---

## Problem 3: IPO
### Problem Statement
Suppose LeetCode will start its IPO soon. In order to sell a good price of its shares to Venture Capital, LeetCode would like to work on some projects to increase its capital before the IPO. Since it has limited resources, it can only finish at most `k` distinct projects before the IPO. Help LeetCode design the best way to maximize its total capital after finishing at most `k` distinct projects.

You are given `n` projects where the `i`th project has a pure profit `profits[i]` and a minimum capital `capital[i]` needed to start it.

Initially, you have `w` capital. When you finish a project, you will obtain its pure profit and the profit will be added to your total capital.

Pick a list of at most `k` distinct projects from given projects to maximize your final capital, and return the final maximized capital.

### Constraints
- `1 <= k <= 10^5`
- `0 <= w <= 10^9`
- `n == profits.length == capital.length`
- `1 <= n <= 10^5`
- `0 <= profits[i] <= 10^4`
- `0 <= capital[i] <= 10^9`

### Python Implementation
```python
import heapq

def findMaximizedCapital(k: int, w: int, profits: list[int], capital: list[int]) -> int:
    """
    Time Complexity: O(n log n + k log n)
    Space Complexity: O(n)
    """
    n = len(profits)
    projects = sorted(zip(capital, profits))

    available_profits = [] # Max heap
    curr = 0

    for _ in range(k):
        # Add all projects we can afford to the max heap
        while curr < n and projects[curr][0] <= w:
            heapq.heappush(available_profits, -projects[curr][1])
            curr += 1

        if not available_profits:
            break

        # Pick the project with the highest profit
        w += -heapq.heappop(available_profits)

    return w
```

---

## Problem 4: K Closest Points to Origin
### Problem Statement
Given an array of `points` where `points[i] = [xi, yi]` represents a point on the X-Y plane and an integer `k`, return the `k` closest points to the origin `(0, 0)`.

### Python Implementation
```python
import heapq

def kClosest(points: list[list[int]], k: int) -> list[list[int]]:
    """
    Time Complexity: O(n log k)
    Space Complexity: O(k)
    """
    heap = [] # Max heap
    for x, y in points:
        dist = x*x + y*y
        if len(heap) < k:
            heapq.heappush(heap, (-dist, [x, y]))
        elif dist < -heap[0][0]:
            heapq.heapreplace(heap, (-dist, [x, y]))

    return [p for d, p in heap]
```

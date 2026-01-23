# Find Median from Data Stream

## Practice Problems

### 1. MedianFinder
**Difficulty:** Hard
**Concept:** Two heaps (max-heap for smaller half, min-heap for larger half)

```python
import heapq

class MedianFinder:
    """
    Design a data structure that supports adding numbers and finding the median.

    >>> mf = MedianFinder()
    >>> mf.add_num(1)
    >>> mf.add_num(2)
    >>> mf.find_median()
    1.5
    >>> mf.add_num(3)
    >>> mf.find_median()
    2.0

    Time: O(log n) for add, O(1) for median
    Space: O(n)
    """
    def __init__(self):
        self.small = []  # Max heap (negated)
        self.large = []  # Min heap

    def add_num(self, num: int) -> None:
        # Step 1: Push to max heap
        heapq.heappush(self.small, -num)

        # Step 2: Ensure every element in small <= every element in large
        if self.small and self.large and (-self.small[0] > self.large[0]):
            val = -heapq.heappop(self.small)
            heapq.heappush(self.large, val)

        # Step 3: Balance sizes (abs difference <= 1)
        if len(self.small) > len(self.large) + 1:
            val = -heapq.heappop(self.small)
            heapq.heappush(self.large, val)
        elif len(self.large) > len(self.small) + 1:
            val = heapq.heappop(self.large)
            heapq.heappush(self.small, -val)

    def find_median(self) -> float:
        if len(self.small) > len(self.large):
            return float(-self.small[0])
        elif len(self.large) > len(self.small):
            return float(self.large[0])
        else:
            return (-self.small[0] + self.large[0]) / 2.0
```

# Find Median from Data Stream

> **Prerequisites:** [02-python-heapq](./02-python-heapq.md)

## Interview Context

The "Find Median from Data Stream" problem is a FANG+ classic because:

1. **Two-heap pattern**: Elegant solution using two heaps working together
2. **Streaming data**: Tests handling real-time data
3. **Optimal complexity**: O(log n) add, O(1) find — better than alternatives
4. **Follow-ups**: Sliding window median, percentiles, etc.

This problem frequently appears at Google, Facebook, and Amazon.

---

## Problem Statement

Design a data structure that supports:
- `addNum(int num)`: Add a number from the data stream
- `findMedian() -> float`: Return the median of all numbers so far

```
Example:
addNum(1)
addNum(2)
findMedian() → 1.5      # (1 + 2) / 2
addNum(3)
findMedian() → 2        # middle of [1, 2, 3]
```

---

## Core Insight: Two Heaps

Divide numbers into two halves:
- **Max heap (left)**: Stores smaller half
- **Min heap (right)**: Stores larger half

```
Numbers: [1, 2, 3, 4, 5]

Max Heap (left):     Min Heap (right):
    2                    3
   / \                  / \
  1                    4   5

Left stores: [1, 2]   Right stores: [3, 4, 5]
Median = 3 (right's root since odd count)
```

**Invariants:**
1. Left max ≤ Right min (left elements ≤ right elements)
2. Size difference ≤ 1 (balanced)

---

## Implementation

```python
import heapq

class MedianFinder:
    """
    Find median from data stream using two heaps.

    Time: O(log n) for addNum, O(1) for findMedian
    Space: O(n)

    Left heap (max): smaller half, stores negated values
    Right heap (min): larger half
    """

    def __init__(self):
        self.left = []   # Max heap (negated)
        self.right = []  # Min heap

    def addNum(self, num: int) -> None:
        """Add a number to the data structure."""
        # Step 1: Add to left (max heap)
        heapq.heappush(self.left, -num)

        # Step 2: Balance - largest of left should go to right
        heapq.heappush(self.right, -heapq.heappop(self.left))

        # Step 3: Ensure left has >= elements than right
        if len(self.left) < len(self.right):
            heapq.heappush(self.left, -heapq.heappop(self.right))

    def findMedian(self) -> float:
        """Return median of current numbers."""
        if len(self.left) > len(self.right):
            return -self.left[0]  # Odd: left has extra element
        return (-self.left[0] + self.right[0]) / 2  # Even: average of middles


# Usage
mf = MedianFinder()
mf.addNum(1)
mf.addNum(2)
print(mf.findMedian())  # 1.5
mf.addNum(3)
print(mf.findMedian())  # 2.0
```

---

## Visual Walkthrough

```
addNum(5):
  left = [-5], right = []
  After balance: left = [-5], right = []
  Sizes: left=1, right=0 ✓

addNum(3):
  Push -3 to left: [-3, -5]
  Pop -5 (max), push 5 to right: left=[-3], right=[5]
  Sizes: left=1, right=1 ✓

addNum(8):
  Push -8 to left: [-8, -3]
  Pop -8 (max), push 8 to right: left=[-3], right=[5,8]
  Sizes: left=1, right=2 → rebalance
  Pop 5 from right, push -5 to left: left=[-5,-3], right=[8]
  Sizes: left=2, right=1 ✓

findMedian():
  left has more elements
  return -left[0] = 5 ✓

Sorted: [3, 5, 8], median = 5 ✓
```

---

## Alternative: Insert to Correct Side First

```python
import heapq

class MedianFinder:
    """Alternative implementation with explicit side choice."""

    def __init__(self):
        self.left = []   # Max heap (negated)
        self.right = []  # Min heap

    def addNum(self, num: int) -> None:
        # Decide which heap to add to
        if not self.left or num <= -self.left[0]:
            heapq.heappush(self.left, -num)
        else:
            heapq.heappush(self.right, num)

        # Rebalance
        if len(self.left) > len(self.right) + 1:
            heapq.heappush(self.right, -heapq.heappop(self.left))
        elif len(self.right) > len(self.left):
            heapq.heappush(self.left, -heapq.heappop(self.right))

    def findMedian(self) -> float:
        if len(self.left) > len(self.right):
            return -self.left[0]
        return (-self.left[0] + self.right[0]) / 2
```

---

## Why Two Heaps?

| Approach | addNum | findMedian | Notes |
|----------|--------|------------|-------|
| Two Heaps | O(log n) | O(1) | Optimal |
| Sorted List | O(n) | O(1) | Insert is slow |
| BST (balanced) | O(log n) | O(log n) | More complex |
| Array + Sort | O(1) | O(n log n) | Sort every time |

Two heaps give the best balance of add and find operations.

---

## Follow-up: Sliding Window Median

For sliding window, we need to support removal. Use two heaps + lazy deletion:

```python
import heapq
from collections import defaultdict

class SlidingWindowMedian:
    """
    Find median in sliding window of size k.

    Time: O(n log k) for n elements
    Space: O(k)
    """

    def __init__(self):
        self.left = []   # Max heap (negated)
        self.right = []  # Min heap
        self.removed = defaultdict(int)  # Lazy removal count
        self.left_size = 0
        self.right_size = 0

    def add(self, num: int) -> None:
        """Add number to structure."""
        if not self.left or num <= -self.left[0]:
            heapq.heappush(self.left, -num)
            self.left_size += 1
        else:
            heapq.heappush(self.right, num)
            self.right_size += 1
        self._balance()

    def remove(self, num: int) -> None:
        """Lazy remove number from structure."""
        self.removed[num] += 1
        if self.left and num <= -self.left[0]:
            self.left_size -= 1
        else:
            self.right_size -= 1
        self._balance()

    def _balance(self) -> None:
        """Balance heaps and clean removed elements."""
        # Balance sizes
        while self.left_size > self.right_size + 1:
            val = -heapq.heappop(self.left)
            self.left_size -= 1
            if self.removed[val] > 0:
                self.removed[val] -= 1
            else:
                heapq.heappush(self.right, val)
                self.right_size += 1

        while self.right_size > self.left_size:
            val = heapq.heappop(self.right)
            self.right_size -= 1
            if self.removed[val] > 0:
                self.removed[val] -= 1
            else:
                heapq.heappush(self.left, -val)
                self.left_size += 1

        # Clean removed from heap tops
        while self.left and self.removed[-self.left[0]] > 0:
            self.removed[-heapq.heappop(self.left)] -= 1

        while self.right and self.removed[self.right[0]] > 0:
            self.removed[heapq.heappop(self.right)] -= 1

    def find_median(self, is_odd: bool) -> float:
        """Get current median."""
        if is_odd:
            return float(-self.left[0])
        return (-self.left[0] + self.right[0]) / 2


def medianSlidingWindow(nums: list[int], k: int) -> list[float]:
    """
    Return medians for each window of size k.

    Time: O(n log k)
    Space: O(k)
    """
    swm = SlidingWindowMedian()
    result = []

    for i, num in enumerate(nums):
        swm.add(num)

        if i >= k:
            swm.remove(nums[i - k])

        if i >= k - 1:
            result.append(swm.find_median(k % 2 == 1))

    return result
```

---

## Edge Cases

```python
# 1. Single element
mf = MedianFinder()
mf.addNum(5)
mf.findMedian()  # 5.0

# 2. Two elements
mf.addNum(1)
mf.addNum(2)
mf.findMedian()  # 1.5

# 3. Negative numbers
mf.addNum(-5)
mf.addNum(-3)
mf.addNum(-1)
mf.findMedian()  # -3.0

# 4. Duplicates
mf.addNum(2)
mf.addNum(2)
mf.addNum(2)
mf.findMedian()  # 2.0

# 5. Large range
mf.addNum(-10**9)
mf.addNum(10**9)
mf.findMedian()  # 0.0
```

---

## Common Mistakes

```python
# WRONG: Forgetting to negate for max heap
self.left = []
heapq.heappush(self.left, num)  # This is min heap!

# CORRECT:
heapq.heappush(self.left, -num)


# WRONG: Not handling empty heaps
def findMedian(self):
    return (-self.left[0] + self.right[0]) / 2  # Fails if right is empty!

# CORRECT:
def findMedian(self):
    if len(self.left) > len(self.right):
        return -self.left[0]
    return (-self.left[0] + self.right[0]) / 2


# WRONG: Integer division
return (-self.left[0] + self.right[0]) // 2  # Truncates!

# CORRECT:
return (-self.left[0] + self.right[0]) / 2  # Float division
```

---

## Complexity Analysis

| Operation | Time | Space |
|-----------|------|-------|
| addNum | O(log n) | O(1) |
| findMedian | O(1) | O(1) |
| Overall space | - | O(n) |

For sliding window:
| Operation | Time |
|-----------|------|
| Add | O(log k) |
| Remove (lazy) | O(1) |
| Balance | O(log k) amortized |
| Find median | O(1) |

---

## Interview Tips

1. **Draw the two heaps**: Left = smaller half, Right = larger half
2. **Explain invariants**: Left max ≤ Right min, sizes differ by ≤ 1
3. **Trace through example**: Show addNum step by step
4. **Know follow-ups**: Sliding window uses lazy deletion
5. **Mention alternatives**: Why two heaps beats sorted list

---

## Practice Problems

| # | Problem | Difficulty | Key Variation |
|---|---------|------------|---------------|
| 1 | Find Median from Data Stream | Hard | Core problem |
| 2 | Sliding Window Median | Hard | With removal |
| 3 | IPO | Hard | Two heaps + greedy |
| 4 | K Closest Points to Origin | Medium | Related pattern |

---

## Key Takeaways

1. **Two heaps**: Max heap (left) for smaller half, min heap (right) for larger
2. **Invariants**: Left max ≤ right min, balanced sizes
3. **O(log n) add, O(1) find**: Optimal for streaming
4. **Negate for max heap**: Python heapq is min heap only
5. **Sliding window**: Add lazy deletion for removal support

---

## Next: [07-task-scheduler.md](./07-task-scheduler.md)

Learn the heap + cooldown pattern for task scheduling.

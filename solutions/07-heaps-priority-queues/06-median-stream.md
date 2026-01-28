# Median from Stream Solutions

## 1. Find Median from Data Stream

The median is the middle value in an ordered integer list. Implement `MedianFinder` class.

### Optimal Python Solution (Two Heaps)

```python
import heapq

class MedianFinder:
    def __init__(self):
        # Max-heap for the smaller half (negate values)
        self.small = []
        # Min-heap for the larger half
        self.large = []

    def addNum(self, num: int) -> None:
        # 1. Add to small, move largest of small to large
        heapq.heappush(self.small, -num)
        heapq.heappush(self.large, -heapq.heappop(self.small))

        # 2. Maintain size invariant: small can be at most 1 larger than large
        if len(self.large) > len(self.small):
            heapq.heappush(self.small, -heapq.heappop(self.large))

    def findMedian(self) -> float:
        if len(self.small) > len(self.large):
            return -self.small[0]
        return (-self.small[0] + self.large[0]) / 2.0
```

### Explanation

- **small**: A max-heap storing the lower half of the numbers.
- **large**: A min-heap storing the upper half of the numbers.
- **addNum**: Ensures numbers are partitioned correctly and heaps are balanced.
- **findMedian**: Returns the average of roots if total count is even, else the root of the larger heap (`small`).

### Complexity Analysis

- **Time Complexity**: $O(\log n)$ for `addNum`, $O(1)$ for `findMedian`.
- **Space Complexity**: $O(n)$ to store all numbers.

---

## 2. Sliding Window Median

Given an array `nums` and a window size `k`, return the median of each sliding window.

### Examples & Edge Cases

- **Example**: `nums = [1,3,-1,-3,5,3,6,7], k = 3` -> `[1.00000,-1.00000,-1.00000,3.00000,5.00000,6.00000]`
- **Edge Case: k = 1**: Median is just the element itself.
- **Edge Case: k = n**: Median of the entire array.

### Optimal Python Solution (Two Heaps + Lazy Deletion)

```python
import heapq
from collections import defaultdict

class SlidingWindowMedian:
    def medianSlidingWindow(self, nums: list[int], k: int) -> list[float]:
        """
        Maintain two heaps for the sliding window. Since heapq doesn't support
        O(log n) removal of arbitrary elements, we use lazy deletion with a hash map.

        Time Complexity: O(n log k)
        Space Complexity: O(n) (due to lazy deletion hash map)
        """
        small = []  # Max-heap (negated)
        large = []  # Min-heap
        delayed = defaultdict(int)

        # Track the actual number of valid elements in each heap
        small_size = 0
        large_size = 0

        def prune(heap, is_small):
            # Remove elements from the top of the heap if they've been marked for deletion
            while heap:
                val = -heap[0] if is_small else heap[0]
                if val in delayed and delayed[val] > 0:
                    delayed[val] -= 1
                    heapq.heappop(heap)
                else:
                    break

        def update_sizes():
            nonlocal small_size, large_size
            # Balance the heaps: small can have same or one more than large
            if small_size > large_size + 1:
                val = -heapq.heappop(small)
                heapq.heappush(large, val)
                small_size -= 1
                large_size += 1
                prune(small, True)
            elif small_size < large_size:
                val = heapq.heappop(large)
                heapq.heappush(small, -val)
                small_size += 1
                large_size -= 1
                prune(large, False)

        def get_median():
            if k % 2 == 1:
                return float(-small[0])
            else:
                return (-small[0] + large[0]) / 2.0

        # Initialize first window
        for i in range(k):
            heapq.heappush(small, -nums[i])
            small_size += 1
        for _ in range(k // 2):
            val = -heapq.heappop(small)
            heapq.heappush(large, val)
            small_size -= 1
            large_size += 1

        res = [get_median()]

        for i in range(k, len(nums)):
            balance = 0 # Net change in small heap size

            # 1. Remove element leaving the window
            out_num = nums[i - k]
            delayed[out_num] += 1
            if out_num <= -small[0]:
                balance -= 1
            else:
                balance += 1

            # 2. Add element entering the window
            in_num = nums[i]
            if small and in_num <= -small[0]:
                heapq.heappush(small, -in_num)
                balance += 1
            else:
                heapq.heappush(large, in_num)
                balance -= 1

            # 3. Rebalance heaps
            if balance < 0: # small lost an element or large gained one
                heapq.heappush(small, -heapq.heappop(large))
                prune(large, False)
            elif balance > 0: # small gained an element or large lost one
                heapq.heappush(large, -heapq.heappop(small))
                prune(small, True)

            # 4. Final top pruning
            prune(small, True)
            prune(large, False)

            res.append(get_median())

        return res
```

### Explanation

1.  **Lazy Deletion**: Standard heaps don't support efficient removal of arbitrary elements. When an element leaves the sliding window, we increment its count in a `delayed` hash map.
2.  **Pruning**: We only remove the "zombie" elements when they reach the top of a heap.
3.  **Two Heaps**: Similar to the "Median from Data Stream" problem, we use a max-heap for the lower half and a min-heap for the upper half to find the median in $O(1)$ once balanced.
4.  **Balancing**: We use a `balance` factor to track how the addition and removal of elements shifted the equilibrium between the two heaps.

### Complexity Analysis

- **Time Complexity**: $O(n \log k)$. Each element is pushed and popped from the heaps at most once.
- **Space Complexity**: $O(n)$ in the worst case to store the `delayed` elements, though it stays $O(k)$ for the heaps themselves.

---

## 3. IPO

Maximize your capital by picking at most `k` projects.

### Examples & Edge Cases

- **Example**: `k = 2, w = 0, profits = [1,2,3], capital = [0,1,1]` -> `4`
- **Edge Case: No affordable projects**: Should stop and return current capital.

### Optimal Python Solution (Greedy + Heap)

```python
import heapq

def findMaximizedCapital(k: int, w: int, profits: list[int], capital: list[int]) -> int:
    """
    To maximize capital, always pick the most profitable project among those
    we can afford.

    Time Complexity: O(n log n + k log n)
    Space Complexity: O(n)
    """
    # 1. Group projects and sort by capital required: O(n log n)
    projects = sorted(zip(capital, profits))
    max_profit_heap = []
    i = 0
    n = len(projects)

    for _ in range(k):
        # 2. Add all projects that we can now afford into a max-profit heap
        while i < n and projects[i][0] <= w:
            # Negate for max-heap
            heapq.heappush(max_profit_heap, -projects[i][1])
            i += 1

        # 3. If no affordable projects are available, we are done
        if not max_profit_heap:
            break

        # 4. Pick the best project (highest profit)
        w += -heapq.heappop(max_profit_heap)

    return w
```

### Explanation

1.  **Greedy Choice**: At any point, our best strategy is to take the project that gives the maximum profit among all projects we can afford.
2.  **Sorting**: We sort projects by capital so we can efficiently find "newly affordable" projects as our capital `w` grows.
3.  **Heap**: A max-heap stores the profits of all currently affordable projects, allowing $O(1)$ access to the best one and $O(\log n)$ updates.

### Complexity Analysis

- **Time Complexity**: $O(n \log n + k \log n)$. Sorting is $O(n \log n)$. We push and pop each project from the heap at most once, which is $O(n \log n)$.
- **Space Complexity**: $O(n)$ to store the projects and the heap.

---

## 4. K Closest Points to Origin

Given an array of `points` and an integer `k`, return the `k` closest points to `(0,0)`.

### Examples & Edge Cases

- **Example**: `points = [[3,3],[5,-1],[-2,4]], k = 2` -> `[[3,3],[-2,4]]`
- **Edge Case: k = 1**: Returns the single closest point.

### Optimal Python Solution (Max-Heap)

```python
import heapq

def kClosest(points: list[list[int]], k: int) -> list[list[int]]:
    """
    Use a max-heap of size k to maintain the k closest points.

    Time Complexity: O(n log k)
    Space Complexity: O(k)
    """
    max_heap = []

    for x, y in points:
        # 1. Squared distance for speed and stability
        dist = x*x + y*y

        # 2. Push negated distance to maintain a max-heap
        if len(max_heap) < k:
            heapq.heappush(max_heap, (-dist, [x, y]))
        elif dist < -max_heap[0][0]:
            # Replace the furthest point in our top-k with this closer point
            heapq.heapreplace(max_heap, (-dist, [x, y]))

    return [p for d, p in max_heap]
```

### Explanation

1.  **Top-K Smallest**: Since we want the $k$ _closest_ points, we maintain a _max-heap_ of our current candidates. The root is the "worst" (furthest) point in our set.
2.  **Efficiency**: This approach only uses $O(k)$ space, which is better than sorting ($O(n \log n)$) or a full heap ($O(n)$) when $k \ll n$.

### Complexity Analysis

- **Time Complexity**: $O(n \log k)$.
- **Space Complexity**: $O(k)$.

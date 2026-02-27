# K Closest Points to Origin

> **Prerequisites:** [03-top-k-pattern](./03-top-k-pattern.md)

## Interview Context

K Closest Points is a FANG+ favorite because:

1. **Top-K variation**: Same pattern, different domain
2. **Math component**: Euclidean distance (or squared distance trick)
3. **Multiple approaches**: Heap, QuickSelect, sorting
4. **Follow-ups**: K closest to arbitrary point, streaming data

This problem appears frequently at Amazon, Facebook, and Google.

---

## Building Intuition

**What Are We Really Looking For?**

We want the k points with the smallest distances to origin. This is a Top-K Smallest problem:

```
Points:    A(1,3)  B(-2,2)  C(3,3)
Distances: √10    √8       √18
           ≈3.16  ≈2.83    ≈4.24

K=2 closest: B and A (smallest distances)
```

**Why Use MAX Heap (Not Min)?**

Same reasoning as Top-K Smallest:

- We want the k CLOSEST (smallest distance)
- We need to EVICT the furthest candidate when we find a closer one
- MAX heap gives O(1) access to the furthest in our candidate set

```
K=2, processing points in order:

A(dist=10) → heap = [A]
B(dist=8)  → heap = [A, B], max=A
C(dist=18) → 18 > 10 (max), skip C
D(dist=5)  → 5 < 10 (max), evict A, heap = [B, D]

Final: B and D are k closest
```

**Why Skip the Square Root?**

Square root is:

1. Computationally expensive
2. Introduces floating-point errors
3. UNNECESSARY for comparisons!

```
If √a < √b, then a < b (sqrt is monotonic)

So instead of:
√(x₁² + y₁²) < √(x₂² + y₂²)

Just use:
x₁² + y₁² < x₂² + y₂²
```

**Mental Model: Lifeguard Rescue Priority**

Imagine a lifeguard at the origin who needs to rescue k swimmers. They can only save k people (limited boat capacity).

- New swimmer spotted → Is this swimmer closer than my furthest planned rescue?
- If yes → Drop the furthest one, add this swimmer to my list
- MAX heap = "Who is the furthest person I'm currently planning to save?"

**The Heap Stores Negated Distances**

Python heapq is min heap. For max heap behavior:

```python
# Store (-distance, point)
# Min of -distance = Max of distance
# heap[0] gives the FURTHEST point (what we might evict)
```

---

## When NOT to Use Heap for K Closest

**1. K = 1 (Just Find Closest)**

Don't use heap for a single point:

```python
# Overkill:
heapq.nsmallest(1, points, key=lambda p: p[0]**2 + p[1]**2)

# Simpler:
min(points, key=lambda p: p[0]**2 + p[1]**2)
```

**2. K ≈ N (Most Points)**

When k is close to n, just sort:

```python
# If k > n/2, sorting might be faster
sorted_points = sorted(points, key=lambda p: p[0]**2 + p[1]**2)
return sorted_points[:k]
```

**3. Points Are Already Sorted by Distance**

If input is pre-sorted by distance:

```python
# Just slice
return points[:k]
```

**4. Need Exact Distances (Not Just Ranking)**

If you need actual distance values:

```python
# Can't skip sqrt if you need the actual number
actual_distance = math.sqrt(x**2 + y**2)
```

**5. Points in Special Structures (KD-Tree Available)**

For repeated queries on same point set:

```python
# KD-tree gives O(k log n) per query after O(n log n) build
# Better if you'll do many queries
from scipy.spatial import KDTree
tree = KDTree(points)
distances, indices = tree.query([0, 0], k=k)
```

**Red Flags:**

- "K is 1" → Use min()
- "K equals n" → Return all points
- "Multiple queries on same points" → Consider KD-tree
- "Need exact distance values" → Must compute sqrt
- "3D or higher dimensions" → Same approach, but consider KD-tree

---

## Problem Statement

Given an array of `points` where `points[i] = [xi, yi]` represents a point on the X-Y plane and an integer `k`, return the `k` closest points to the origin `(0, 0)`.

Distance is Euclidean: √(x² + y²)

```
Example 1:
points = [[1,3],[-2,2]], k = 1
Output: [[-2,2]]

Distance to (1,3): √(1² + 3²) = √10 ≈ 3.16
Distance to (-2,2): √((-2)² + 2²) = √8 ≈ 2.83

[-2,2] is closer ✓

Example 2:
points = [[3,3],[5,-1],[-2,4]], k = 2
Output: [[3,3],[-2,4]] (order doesn't matter)
```

---

## Key Insight: Skip the Square Root

Since we only compare distances (not compute exact values), we can use squared distance:

```
√(x₁² + y₁²) < √(x₂² + y₂²)
⟺
x₁² + y₁² < x₂² + y₂²
```

Squared distance is faster and avoids floating-point issues.

---

## Approach 1: Max Heap of Size K

For K closest, use **max heap** of size K. Evict furthest point.

```python
import heapq
from typing import List

def k_closest(points: List[List[int]], k: int) -> List[List[int]]:
    """
    Find k closest points to origin using max heap.

    Time: O(n log k)
    Space: O(k)
    """
    # Max heap: (-distance, point)
    # We want to evict furthest, so max heap by distance
    heap = []

    for x, y in points:
        dist = x * x + y * y  # Squared distance

        if len(heap) < k:
            heapq.heappush(heap, (-dist, [x, y]))
        elif dist < -heap[0][0]:  # Closer than furthest in heap
            heapq.heapreplace(heap, (-dist, [x, y]))

    return [point for _, point in heap]


# Usage
points = [[1, 3], [-2, 2]]
print(k_closest(points, 1))  # [[-2, 2]]
```

---

## Why Max Heap for K Closest?

```
Finding K closest = Finding K smallest distances

Use MAX heap of size K:
- Root = largest distance in our K candidates
- If new point is closer than root → replace root
- Root is what we might evict (furthest of the closest)

This is same pattern as "K largest elements" but inverted:
- K largest → min heap (evict smallest)
- K smallest → max heap (evict largest)
```

---

## Approach 2: Min Heap of All Points

Less efficient but simpler:

```python
import heapq
from typing import List

def k_closest_min_heap(points: List[List[int]], k: int) -> List[List[int]]:
    """
    Build min heap of all points, pop k times.

    Time: O(n + k log n)
    Space: O(n)
    """
    # (distance, point)
    heap = [(x*x + y*y, [x, y]) for x, y in points]
    heapq.heapify(heap)

    return [heapq.heappop(heap)[1] for _ in range(k)]
```

---

## Approach 3: Using heapq.nsmallest

```python
import heapq
from typing import List

def k_closest_nsmallest(points: List[List[int]], k: int) -> List[List[int]]:
    """
    Use heapq.nsmallest with a key function.

    Time: O(n log k) internally if k << n (Python does quick optimizations)
    Space: O(k)
    """
    return heapq.nsmallest(k, points, key=lambda p: p[0]**2 + p[1]**2)
```

Cleanest solution, internally uses a heap (and falls back to sorting if k is close to n, or min() if k=1).

---

## Approach 4: QuickSelect

Average O(n) time:

```python
import random
from typing import List

def k_closest_quickselect(points: List[List[int]], k: int) -> List[List[int]]:
    """
    QuickSelect to partition points by distance.

    Time: O(n) average, O(n²) worst
    Space: O(1) excluding output
    """
    def dist(point: List[int]) -> int:
        return point[0]**2 + point[1]**2

    def partition(left: int, right: int, pivot_idx: int) -> int:
        pivot_dist = dist(points[pivot_idx])
        # Move pivot to end
        points[pivot_idx], points[right] = points[right], points[pivot_idx]

        # store_idx keeps track of where the next element smaller than pivot should go
        store_idx = left
        for i in range(left, right):
            if dist(points[i]) < pivot_dist:
                points[i], points[store_idx] = points[store_idx], points[i]
                store_idx += 1

        # Move pivot to its final place
        points[store_idx], points[right] = points[right], points[store_idx]
        return store_idx

    left, right = 0, len(points) - 1

    while left <= right:
        # Choose a random pivot index between left and right inclusive
        pivot_idx = random.randint(left, right)

        # Partition the array and get the final position of the pivot
        true_pivot_idx = partition(left, right, pivot_idx)

        # If the pivot is exactly at position k, we have our k closest points
        # in the first k positions of the array (0 to k-1)
        if true_pivot_idx == k:
            break
        # If pivot is at position k-1, we also have exactly k elements (0 to k-1)
        elif true_pivot_idx == k - 1:
            break
        elif true_pivot_idx < k:
            # We need more elements, search in the right half
            left = true_pivot_idx + 1
        else:
            # We have too many elements, search in the left half
            right = true_pivot_idx - 1

    return points[:k]
```

---

## Comparison of Approaches

| Approach     | Time           | Space | Notes                            |
| ------------ | -------------- | ----- | -------------------------------- |
| Max Heap K   | O(n log k)     | O(k)  | Best for streaming               |
| nsmallest    | O(n log k)     | O(k)  | Cleanest code, fast in Python    |
| Min Heap all | O(n + k log n) | O(n)  | Simple but more space            |
| Sort         | O(n log n)     | O(n)  | Simple, not optimal              |
| QuickSelect  | O(n) avg       | O(1)  | Best average, but modifies input |

---

## Variation: K Closest to Arbitrary Point

```python
import heapq
from typing import List

def k_closest_to_point(points: List[List[int]], k: int,
                       target: List[int]) -> List[List[int]]:
    """
    Find k closest points to target (not origin).

    Time: O(n log k)
    Space: O(k)
    """
    tx, ty = target

    def dist(p: List[int]) -> int:
        return (p[0] - tx)**2 + (p[1] - ty)**2

    return heapq.nsmallest(k, points, key=dist)
```

---

## Variation: K Closest in Streaming Data

```python
import heapq
from typing import List

class KClosestStream:
    """
    Maintain k closest points in streaming data.

    Time: O(log k) per add
    Space: O(k)
    """

    def __init__(self, k: int):
        self.k = k
        self.heap = []  # Max heap: (-dist, point)

    def add(self, point: List[int]) -> List[List[int]]:
        x, y = point
        dist = x*x + y*y

        if len(self.heap) < self.k:
            heapq.heappush(self.heap, (-dist, point))
        elif dist < -self.heap[0][0]:
            heapq.heapreplace(self.heap, (-dist, point))

        return [p for _, p in self.heap]
```

---

## Related: K Closest Elements in Sorted Array

Different problem, different approach:

```python
from typing import List

def find_closest_elements(arr: List[int], k: int, x: int) -> List[int]:
    """
    Find k closest elements to x in sorted array.

    Time: O(log(n-k) + k)
    Space: O(1)

    Binary search for left boundary of k-element window.
    """
    left, right = 0, len(arr) - k

    while left < right:
        mid = (left + right) // 2

        # Compare distances of window edges to x
        # If right edge is closer or same distance but we prefer left, move right
        # (Since x - arr[mid] > arr[mid + k] - x means arr[mid + k] is strictly closer to x than arr[mid])
        if x - arr[mid] > arr[mid + k] - x:
            left = mid + 1
        else:
            right = mid

    return arr[left:left + k]
```

---

## Related: Find K Pairs with Smallest Sums

```python
import heapq
from typing import List

def k_smallest_pairs(nums1: List[int], nums2: List[int],
                     k: int) -> List[List[int]]:
    """
    Find k pairs with smallest sums from two sorted arrays.

    Time: O(k log k)
    Space: O(k) for the heap
    """
    if not nums1 or not nums2:
        return []

    result = []
    # Min heap: (sum, index1, index2)
    # We only push elements paired with nums2[0] initially to avoid O(N*M) space
    heap = []
    for i in range(min(k, len(nums1))):
        heapq.heappush(heap, (nums1[i] + nums2[0], i, 0))

    while heap and len(result) < k:
        _, i, j = heapq.heappop(heap)
        result.append([nums1[i], nums2[j]])

        # If there's another element in nums2 to pair with nums1[i], add it to heap
        if j + 1 < len(nums2):
            heapq.heappush(heap, (nums1[i] + nums2[j + 1], i, j + 1))

    return result
```

---

## Edge Cases

```python
# 1. k equals number of points
k_closest([[1,1], [2,2]], 2)  # Return all points

# 2. k = 1
k_closest([[1,1], [2,2], [3,3]], 1)  # [[1,1]]

# 3. Negative coordinates
k_closest([[-1,-1], [1,1]], 1)  # Either one (same distance)

# 4. Origin in points
k_closest([[0,0], [1,1]], 1)  # [[0,0]]

# 5. Ties (same distance)
k_closest([[1,0], [0,1]], 1)  # Either one

# 6. All same distance
k_closest([[1,0], [0,1], [-1,0], [0,-1]], 2)  # Any 2
```

---

## Common Mistakes

```python
# WRONG: Using sqrt (unnecessary, slower)
import math
dist = math.sqrt(x*x + y*y)

# CORRECT: Use squared distance
dist = x*x + y*y


# WRONG: Using min heap for k closest
# Min heap evicts smallest, but we want to keep smallest!
heap = [(dist, point) for ...]
# This keeps all n elements, defeats the purpose

# CORRECT: Use max heap of size k
# Max heap evicts largest (furthest), keeps closest


# WRONG: Returning unsorted when order matters
return [point for _, point in heap]
# Heap order is NOT sorted order

# CORRECT: Sort if order matters (usually doesn't for this problem)
return sorted(heap, key=lambda x: -x[0])
```

---

## Interview Tips

1. **Mention squared distance**: Shows awareness of optimization
2. **Know multiple approaches**: Heap, QuickSelect, nsmallest
3. **Discuss trade-offs**: Heap for streaming, QuickSelect for one-shot
4. **Handle ties**: Usually any k closest is acceptable
5. **Clarify output order**: Usually doesn't matter

---

## Practice Problems

| #   | Problem                               | Difficulty | Key Variation               |
| --- | ------------------------------------- | ---------- | --------------------------- |
| 1   | K Closest Points to Origin            | Medium     | Core problem                |
| 2   | Find K Closest Elements               | Medium     | Sorted array, binary search |
| 3   | Find K Pairs with Smallest Sums       | Medium     | Two arrays                  |
| 4   | Kth Smallest Element in Sorted Matrix | Medium     | Matrix as k lists           |
| 5   | Closest Binary Search Tree Value II   | Hard       | BST, k closest              |

---

## Key Takeaways

1. **K closest → Max heap**: Evict furthest of the closest
2. **Skip sqrt**: Squared distance preserves ordering
3. **O(n log k)**: Better than O(n log n) sort when k << n
4. **heapq.nsmallest**: Cleanest solution in interviews
5. **QuickSelect O(n)**: Best average case for single query

---

## Summary: Heaps & Priority Queues

You've now covered the essential heap patterns:

| Pattern        | Key Insight                  |
| -------------- | ---------------------------- |
| Top-K          | Opposite heap type, size K   |
| Kth element    | Heap root is answer          |
| Merge K sorted | Min heap tracks K candidates |
| Median stream  | Two heaps split at median    |
| Task scheduler | Max heap + cooldown queue    |
| K closest      | Max heap, squared distance   |

These patterns cover 90% of heap interview questions at FANG+ companies.

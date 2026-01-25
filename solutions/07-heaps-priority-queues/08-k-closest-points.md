# K Closest Points Solutions

## 1. K Closest Points to Origin
Find the k points closest to (0,0).

### Optimal Python Solution
```python
import heapq

def kClosest(points: list[list[int]], k: int) -> list[list[int]]:
    """
    Max-heap of size k to store the closest points seen.
    Use squared distance to avoid float/sqrt.

    Time Complexity: O(n log k)
    Space Complexity: O(k)
    """
    # Max-heap: (-distance, point)
    max_heap = []

    for x, y in points:
        dist = x*x + y*y
        if len(max_heap) < k:
            heapq.heappush(max_heap, (-dist, [x, y]))
        elif dist < -max_heap[0][0]:
            heapq.heapreplace(max_heap, (-dist, [x, y]))

    return [p for d, p in max_heap]
```

---

## 2. Find K Closest Elements
Find k integers closest to `x` in a sorted array.

### Optimal Python Solution (Binary Search + Two Pointers)
Note: While this is a heap chapter, for a *sorted* array, the two-pointer/binary search approach is more optimal.

```python
def findClosestElements(arr: list[int], k: int, x: int) -> list[int]:
    """
    Binary search for the left bound of the k-element window.

    Time Complexity: O(log(n-k) + k)
    Space Complexity: O(1)
    """
    l, r = 0, len(arr) - k

    while l < r:
        m = (l + r) // 2
        # Check if x is closer to arr[m] or arr[m+k]
        if x - arr[m] > arr[m + k] - x:
            l = m + 1
        else:
            r = m

    return arr[l:l + k]
```

---

## 3. Find K Pairs with Smallest Sums
Given two sorted arrays and an integer `k`, find the `k` pairs `(u, v)` with the smallest sums.

### Examples & Edge Cases
- **Example**: `nums1 = [1,7,11], nums2 = [2,4,6], k = 3` -> `[[1,2],[1,4],[1,6]]`

### Optimal Python Solution (Min-Heap)
```python
import heapq

def kSmallestPairs(nums1: list[int], nums2: list[int], k: int) -> list[list[int]]:
    """
    Standard Min-Heap approach for finding k smallest elements across combinations.

    Time Complexity: O(k log k)
    Space Complexity: O(k)
    """
    if not nums1 or not nums2: return []

    res = []
    min_heap = [] # (sum, i, j)

    # Initial pairs using the first elements of nums1
    for i in range(min(len(nums1), k)):
        heapq.heappush(min_heap, (nums1[i] + nums2[0], i, 0))

    while min_heap and len(res) < k:
        curr_sum, i, j = heapq.heappop(min_heap)
        res.append([nums1[i], nums2[j]])

        # Explore the next element in nums2 for the current nums1[i]
        if j + 1 < len(nums2):
            heapq.heappush(min_heap, (nums1[i] + nums2[j + 1], i, j + 1))

    return res
```

### Explanation
1.  **Dijkstra-like Exploration**: We start at the smallest possible pair (top-left of a virtual sum grid) and explore adjacent cells (incrementing indices) using a heap to always pick the smallest sum.

---

## 4. Kth Smallest Element in Sorted Matrix
Given an `n x n` matrix where rows and columns are sorted, find the kth smallest element.

### Examples & Edge Cases
- **Example**: `matrix = [[1,5,9],[10,11,13],[12,13,15]], k = 8` -> `13`

### Optimal Python Solution (Min-Heap)
```python
import heapq

def kthSmallest(matrix: list[list[int]], k: int) -> int:
    """
    Treat the sorted matrix as k-sorted lists.

    Time Complexity: O(k log n)
    Space Complexity: O(n)
    """
    n = len(matrix)
    min_heap = []

    # Initialize heap with the first element of each row
    for i in range(min(n, k)):
        heapq.heappush(min_heap, (matrix[i][0], i, 0))

    for _ in range(k):
        val, r, c = heapq.heappop(min_heap)
        if c + 1 < n:
            heapq.heappush(min_heap, (matrix[r][c + 1], r, c + 1))

    return val
```

### Explanation
1.  **Merge-K Concept**: We use the sorted property of the rows to find the globally smallest elements one by one using a min-heap.

---

## 5. Closest Binary Search Tree Value II
Given a BST and a target, find `k` values in the BST that are closest to the target.

### Optimal Python Solution (In-order Traversal + Deque)
```python
from collections import deque

def closestKValues(root: Optional[TreeNode], target: float, k: int) -> list[int]:
    """
    In-order traversal visits nodes in ascending order.
    Maintain a sliding window of size k using a deque.

    Time Complexity: O(N)
    Space Complexity: O(H + k)
    """
    res = deque()

    def inorder(node):
        if not node: return
        inorder(node.left)

        if len(res) < k:
            res.append(node.val)
        else:
            # Check if current node is closer than the oldest in our window
            if abs(node.val - target) < abs(res[0] - target):
                res.popleft()
                res.append(node.val)
            else:
                # Since values are increasing, if current is further, all future nodes are further
                return

        inorder(node.right)

    inorder(root)
    return list(res)
```
*(Alternative: Use two stacks to simulate an iterator for pre-order and post-order from the target node for $O(H + k)$ time).*

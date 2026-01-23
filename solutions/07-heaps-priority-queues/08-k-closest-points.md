# Solution: K Closest Points Practice Problems

## Problem 1: K Closest Points to Origin
### Problem Statement
Given an array of `points` where `points[i] = [xi, yi]` represents a point on the X-Y plane and an integer `k`, return the `k` closest points to the origin `(0, 0)`.

The distance between two points on the X-Y plane is the Euclidean distance (i.e., `√(x1 - x2)^2 + (y1 - y2)^2`).

You may return the answer in any order. The answer is guaranteed to be unique (except for the order that it is in).

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
    # We use a max-heap because we want to keep the k smallest distances.
    # When the heap exceeds size k, we pop the largest distance.
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

## Problem 2: Find K Closest Elements
### Problem Statement
Given a sorted integer array `arr`, two integers `k` and `x`, return the `k` closest integers to `x` in the array. The result should also be sorted in ascending order.

An integer `a` is closer to `x` than an integer `b` if:
- `|a - x| < |b - x|`, or
- `|a - x| == |b - x|` and `a < b`

### Constraints
- `1 <= k <= arr.length`
- `1 <= arr.length <= 10^4`
- `arr` is sorted in ascending order.
- `-10^4 <= arr[i], x <= 10^4`

### Example
Input: `arr = [1,2,3,4,5], k = 4, x = 3`
Output: `[1,2,3,4]`

### Python Implementation
```python
import heapq

def findClosestElements(arr: list[int], k: int, x: int) -> list[int]:
    """
    Time Complexity: O(n log k)
    Space Complexity: O(k)
    """
    # Max heap: (-diff, -val)
    # Using -val as second element in tuple to handle the tie-breaking rule:
    # "if |a - x| == |b - x| and a < b, a is closer".
    # In a max-heap of (-diff, -val), the "largest" will be popped first.
    # If diffs are equal, the one with smaller -val (larger val) will be popped.
    # This keeps smaller val in the heap.
    heap = []
    for val in arr:
        diff = abs(val - x)
        if len(heap) < k:
            heapq.heappush(heap, (-diff, -val))
        elif diff < -heap[0][0]:
            heapq.heapreplace(heap, (-diff, -val))
        # No need to check diff == -heap[0][0] because arr is sorted,
        # and tie-break always prefers smaller val (already in heap or arriving).

    res = sorted([-val for diff, val in heap])
    return res
```

---

## Problem 3: Find K Pairs with Smallest Sums
### Problem Statement
You are given two integer arrays `nums1` and `nums2` sorted in non-decreasing order and an integer `k`.

Define a pair `(u, v)` which consists of one element from the first array and one element from the second array.

Return the `k` pairs `(u1, v1), (u2, v2), ..., (uk, vk)` with the smallest sums.

### Python Implementation
```python
import heapq

def kSmallestPairs(nums1: list[int], nums2: list[int], k: int) -> list[list[int]]:
    """
    Time Complexity: O(k log k)
    Space Complexity: O(k)
    """
    if not nums1 or not nums2:
        return []

    res = []
    heap = [] # (sum, i, j)
    # Initialize with first k elements from nums1 paired with nums2[0]
    for i in range(min(k, len(nums1))):
        heapq.heappush(heap, (nums1[i] + nums2[0], i, 0))

    while heap and len(res) < k:
        _, i, j = heapq.heappop(heap)
        res.append([nums1[i], nums2[j]])
        if j + 1 < len(nums2):
            heapq.heappush(heap, (nums1[i] + nums2[j + 1], i, j + 1))

    return res
```

---

## Problem 4: Kth Smallest Element in Sorted Matrix
### Problem Statement
Given an `n x n` `matrix` where each of the rows and columns is sorted in ascending order, return the `k`th smallest element in the matrix.

### Python Implementation
```python
import heapq

def kthSmallest(matrix: list[list[int]], k: int) -> int:
    """
    Time Complexity: O(k log n) where n is min(n, k)
    Space Complexity: O(n)
    """
    n = len(matrix)
    heap = [] # (val, r, c)
    for r in range(min(k, n)):
        heapq.heappush(heap, (matrix[r][0], r, 0))

    val = 0
    for _ in range(k):
        val, r, c = heapq.heappop(heap)
        if c + 1 < n:
            heapq.heappush(heap, (matrix[r][c + 1], r, c + 1))

    return val
```

---

## Problem 5: Closest Binary Search Tree Value II
### Problem Statement
Given the `root` of a binary search tree, a `target` value, and an integer `k`, return the `k` values in the BST that are closest to the `target`. You may return the answer in any order.

You are guaranteed to have only one unique set of `k` values in the BST that are closest to the `target`.

### Python Implementation
```python
import heapq

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def closestKValues(root: TreeNode, target: float, k: int) -> list[int]:
    """
    Time Complexity: O(n log k)
    Space Complexity: O(h + k)
    """
    heap = [] # Max heap of (-diff, val)

    def inorder(node):
        if not node:
            return

        inorder(node.left)

        diff = abs(node.val - target)
        if len(heap) < k:
            heapq.heappush(heap, (-diff, node.val))
        elif diff < -heap[0][0]:
            heapq.heapreplace(heap, (-diff, node.val))
        else:
            # Since it's inorder, if current node is further than max in heap,
            # all subsequent nodes will also be further (for values > target).
            # But values < target might still be closer.
            # However, standard inorder is enough.
            pass

        inorder(node.right)

    inorder(root)
    return [val for diff, val in heap]
```

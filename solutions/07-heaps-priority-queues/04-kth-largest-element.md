# Solution: Kth Largest Element Practice Problems

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

## Problem 2: Kth Smallest Element in a Sorted Matrix
### Problem Statement
Given an `n x n` `matrix` where each of the rows and columns is sorted in ascending order, return the `k`th smallest element in the matrix.

Note that it is the `k`th smallest element in the sorted order, not the `k`th distinct element.

### Constraints
- `n == matrix.length == matrix[i].length`
- `1 <= n <= 300`
- `-10^9 <= matrix[i][j] <= 10^9`
- `1 <= k <= n^2`

### Example
Input: `matrix = [[1,5,9],[10,11,13],[12,13,15]], k = 8`
Output: `13`

### Python Implementation
```python
import heapq

def kthSmallest(matrix: list[list[int]], k: int) -> int:
    """
    Time Complexity: O(k log n) where n is min(n, k)
    Space Complexity: O(n)
    """
    n = len(matrix)
    heap = [] # (val, row, col)

    # Initialize heap with first element of each row (up to k rows)
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

## Problem 3: Find K Pairs with Smallest Sums
### Problem Statement
You are given two integer arrays `nums1` and `nums2` sorted in non-decreasing order and an integer `k`.

Define a pair `(u, v)` which consists of one element from the first array and one element from the second array.

Return the `k` pairs `(u1, v1), (u2, v2), ..., (uk, vk)` with the smallest sums.

### Constraints
- `1 <= nums1.length, nums2.length <= 10^5`
- `-10^9 <= nums1[i], nums2[i] <= 10^9`
- `nums1` and `nums2` are sorted in non-decreasing order.
- `1 <= k <= 10^4`

### Example
Input: `nums1 = [1,7,11], nums2 = [2,4,6], k = 3`
Output: `[[1,2],[1,4],[1,6]]`

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

## Problem 4: Kth Smallest Element in a BST
### Problem Statement
Given the `root` of a binary search tree, and an integer `k`, return the `k`th smallest value (1-indexed) of all the values of the nodes in the tree.

### Constraints
- The number of nodes in the tree is `n`.
- `1 <= k <= n <= 10^4`
- `0 <= Node.val <= 10^4`

### Python Implementation
```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def kthSmallest(root: TreeNode, k: int) -> int:
    """
    Time Complexity: O(h + k)
    Space Complexity: O(h)
    """
    stack = []
    while True:
        while root:
            stack.append(root)
            root = root.left
        root = stack.pop()
        k -= 1
        if k == 0:
            return root.val
        root = root.right
```

---

## Problem 5: Third Maximum Number
### Problem Statement
Given an integer array `nums`, return the third distinct maximum number in this array. If the third maximum does not exist, return the maximum number.

### Constraints
- `1 <= nums.length <= 10^4`
- `-2^31 <= nums[i] <= 2^31 - 1`

### Example
Input: `nums = [3,2,1]`
Output: `1`

### Python Implementation
```python
import heapq

def thirdMax(nums: list[int]) -> int:
    """
    Time Complexity: O(n log 3) = O(n)
    Space Complexity: O(3) = O(1)
    """
    # Use a min-heap to store at most 3 distinct maximums
    heap = []
    seen = set()

    for num in nums:
        if num not in seen:
            seen.add(num)
            heapq.heappush(heap, num)
            if len(heap) > 3:
                val = heapq.heappop(heap)
                seen.remove(val)

    if len(heap) < 3:
        return max(heap)
    return heap[0]
```

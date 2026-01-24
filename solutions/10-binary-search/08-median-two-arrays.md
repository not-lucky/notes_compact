# Practice Problems - Median of Two Sorted Arrays

## 1. Median of Two Sorted Arrays (LeetCode 4)

### Problem Statement
Given two sorted arrays `nums1` and `nums2` of size `m` and `n` respectively, return the median of the two sorted arrays.
The overall run time complexity should be `O(log (m+n))`.

### Constraints
- `nums1.length == m`
- `nums2.length == n`
- `0 <= m, n <= 1000`
- `1 <= m + n <= 2000`
- `-10^6 <= nums1[i], nums2[i] <= 10^6`

### Example
**Input:** `nums1 = [1,3], nums2 = [2]`
**Output:** `2.00000`

### Python Block
```python
def find_median_sorted_arrays(nums1: list[int], nums2: list[int]) -> float:
    # Ensure nums1 is the smaller array
    if len(nums1) > len(nums2):
        nums1, nums2 = nums2, nums1

    m, n = len(nums1), len(nums2)
    total = m + n
    half = (total + 1) // 2

    left, right = 0, m
    while left <= right:
        i = left + (right - left) // 2
        j = half - i

        nums1_left = nums1[i - 1] if i > 0 else float('-inf')
        nums1_right = nums1[i] if i < m else float('inf')
        nums2_left = nums2[j - 1] if j > 0 else float('-inf')
        nums2_right = nums2[j] if j < n else float('inf')

        # Correct partition
        if nums1_left <= nums2_right and nums2_left <= nums1_right:
            if total % 2 == 1:
                return max(nums1_left, nums2_left)
            return (max(nums1_left, nums2_left) + min(nums1_right, nums2_right)) / 2
        elif nums1_left > nums2_right:
            right = i - 1
        else:
            left = i + 1

    return 0.0
```

## 2. Kth Smallest Element in a Sorted Matrix (LeetCode 378)

### Problem Statement
Given an `n x n` `matrix` where each of the rows and columns is sorted in ascending order, return the `k-th` smallest element in the matrix.

### Constraints
- `n == matrix.length == matrix[i].length`
- `1 <= n <= 300`
- `-10^9 <= matrix[i][j] <= 10^9`
- `1 <= k <= n^2`

### Python Block
```python
def kth_smallest(matrix: list[list[int]], k: int) -> int:
    n = len(matrix)

    def count_less_equal(mid: int) -> int:
        count = 0
        row, col = n - 1, 0
        while row >= 0 and col < n:
            if matrix[row][col] <= mid:
                count += row + 1
                col += 1
            else:
                row -= 1
        return count

    left, right = matrix[0][0], matrix[n - 1][n - 1]
    while left < right:
        mid = left + (right - left) // 2
        if count_less_equal(mid) < k:
            left = mid + 1
        else:
            right = mid
    return left
```

## 3. Find K Pairs with Smallest Sums (LeetCode 373)

### Problem Statement
You are given two integer arrays `nums1` and `nums2` sorted in ascending order and an integer `k`.
Define a pair `(u, v)` which consists of one element from the first array and one element from the second array.
Return the `k` pairs `(u1, v1), (u2, v2), ..., (uk, vk)` with the smallest sums.

### Constraints
- `1 <= nums1.length, nums2.length <= 10^5`
- `-10^9 <= nums1[i], nums2[i] <= 10^9`
- `nums1` and `nums2` are sorted in ascending order.
- `1 <= k <= 10^4`

### Example
**Input:** `nums1 = [1,7,11], nums2 = [2,4,6], k = 3`
**Output:** `[[1,2],[1,4],[1,6]]`

### Python Block
```python
import heapq

def k_smallest_pairs(nums1: list[int], nums2: list[int], k: int) -> list[list[int]]:
    if not nums1 or not nums2:
        return []

    res = []
    # min_heap stores (sum, i, j)
    min_heap = []

    # Initialize heap with first element of nums1 and all elements of nums2
    # OR first element of nums2 and some elements of nums1
    # Optimization: push (nums1[i] + nums2[0], i, 0) for i in range(min(k, len(nums1)))
    for i in range(min(k, len(nums1))):
        heapq.heappush(min_heap, (nums1[i] + nums2[0], i, 0))

    while k > 0 and min_heap:
        s, i, j = heapq.heappop(min_heap)
        res.append([nums1[i], nums2[j]])
        if j + 1 < len(nums2):
            heapq.heappush(min_heap, (nums1[i] + nums2[j + 1], i, j + 1))
        k -= 1

    return res
```

## 4. Merge K Sorted Lists (LeetCode 23)

### Problem Statement
You are given an array of `k` linked-lists `lists`, each linked-list is sorted in ascending order.
Merge all the linked-lists into one sorted linked-list and return it.

### Constraints
- `k == lists.length`
- `0 <= k <= 10^4`
- `0 <= lists[i].length <= 500`
- `-10^4 <= lists[i][j] <= 10^4`
- `lists[i]` is sorted in ascending order.
- The sum of `lists[i].length` will not exceed `10^4`.

### Python Block
```python
import heapq

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def merge_k_lists(lists: list[ListNode]) -> ListNode:
    dummy = ListNode(0)
    curr = dummy
    min_heap = []

    for i, l in enumerate(lists):
        if l:
            # Store (val, index) to handle uncomparable ListNode
            heapq.heappush(min_heap, (l.val, i))

    while min_heap:
        val, i = heapq.heappop(min_heap)
        curr.next = ListNode(val)
        curr = curr.next
        lists[i] = lists[i].next
        if lists[i]:
            heapq.heappush(min_heap, (lists[i].val, i))

    return dummy.next
```

## 5. Find Median from Data Stream (LeetCode 295)

### Problem Statement
The **median** is the middle value in an ordered integer list. If the size of the list is even, there is no middle value, and the median is the mean of the two middle values.
Implement the `MedianFinder` class.

### Python Block
```python
import heapq

class MedianFinder:
    def __init__(self):
        # max_heap for left half (smaller elements)
        self.left = []
        # min_heap for right half (larger elements)
        self.right = []

    def add_num(self, num: int) -> None:
        if not self.left or num <= -self.left[0]:
            heapq.heappush(self.left, -num)
        else:
            heapq.heappush(self.right, num)

        # Balance heaps
        if len(self.left) > len(self.right) + 1:
            heapq.heappush(self.right, -heapq.heappop(self.left))
        elif len(self.right) > len(self.left):
            heapq.heappush(self.left, -heapq.heappop(self.right))

    def find_median(self) -> float:
        if len(self.left) > len(self.right):
            return float(-self.left[0])
        return (-self.left[0] + self.right[0]) / 2.0
```

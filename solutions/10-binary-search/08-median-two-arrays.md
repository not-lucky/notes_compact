# Median of Two Sorted Arrays Solutions

## 1. Median of Two Sorted Arrays
[LeetCode 4](https://leetcode.com/problems/median-of-two-sorted-arrays/)

### Problem Description
Given two sorted arrays `nums1` and `nums2` of size `m` and `n` respectively, return the median of the two sorted arrays. The overall run time complexity should be `O(log (m+n))`.

### Solution
```python
def findMedianSortedArrays(nums1: list[int], nums2: list[int]) -> float:
    # Ensure nums1 is the smaller array to optimize binary search
    if len(nums1) > len(nums2):
        nums1, nums2 = nums2, nums1

    m, n = len(nums1), len(nums2)
    total = m + n
    half = (total + 1) // 2

    left, right = 0, m

    while left <= right:
        i = (left + right) // 2
        j = half - i

        # Edge cases: use -inf/inf for out of bounds
        nums1_left = nums1[i-1] if i > 0 else float('-inf')
        nums1_right = nums1[i] if i < m else float('inf')
        nums2_left = nums2[j-1] if j > 0 else float('-inf')
        nums2_right = nums2[j] if j < n else float('inf')

        # Check if partition is correct
        if nums1_left <= nums2_right and nums2_left <= nums1_right:
            # Valid partition
            if total % 2 == 1:
                return float(max(nums1_left, nums2_left))
            else:
                return (max(nums1_left, nums2_left) + min(nums1_right, nums2_right)) / 2.0
        elif nums1_left > nums2_right:
            # Too many elements from nums1
            right = i - 1
        else:
            # Too few elements from nums1
            left = i + 1

    return 0.0
```
- **Time Complexity**: O(log(min(m, n)))
- **Space Complexity**: O(1)

---

## 2. Kth Smallest Element in a Sorted Matrix
[LeetCode 378](https://leetcode.com/problems/kth-smallest-element-in-a-sorted-matrix/)

### Problem Description
Given an `n x n` matrix where each of the rows and columns is sorted in ascending order, return the `k`-th smallest element in the matrix.

### Solution
```python
def kthSmallest(matrix: list[list[int]], k: int) -> int:
    n = len(matrix)

    def countLessEqual(val: int) -> int:
        count = 0
        row, col = n - 1, 0  # Start bottom-left
        while row >= 0 and col < n:
            if matrix[row][col] <= val:
                count += row + 1
                col += 1
            else:
                row -= 1
        return count

    left, right = matrix[0][0], matrix[n-1][n-1]
    res = left
    while left <= right:
        mid = left + (right - left) // 2
        if countLessEqual(mid) >= k:
            res = mid
            right = mid - 1
        else:
            left = mid + 1

    return res
```
- **Time Complexity**: O(n log(max-min))
- **Space Complexity**: O(1)

---

## 3. Find K Pairs with Smallest Sums
[LeetCode 373](https://leetcode.com/problems/find-k-pairs-with-smallest-sums/)

### Problem Description
You are given two integer arrays `nums1` and `nums2` sorted in ascending order and an integer `k`. Define a pair `(u, v)` which consists of one element from the first array and one element from the second array. Return the `k` pairs `(u1, v1), (u2, v2), ..., (uk, vk)` with the smallest sums.

### Solution
```python
import heapq

def kSmallestPairs(nums1: list[int], nums2: list[int], k: int) -> list[list[int]]:
    if not nums1 or not nums2: return []

    res = []
    # Min heap: (sum, i, j)
    # We always take nums1[i] and nums2[j]
    heap = []

    # Initialize heap with first element of nums2 and all necessary elements of nums1
    # We only need at most k elements from nums1
    for i in range(min(len(nums1), k)):
        heapq.heappush(heap, (nums1[i] + nums2[0], i, 0))

    while heap and len(res) < k:
        curr_sum, i, j = heapq.heappop(heap)
        res.append([nums1[i], nums2[j]])

        # If there is a next element in nums2, add it to the heap
        if j + 1 < len(nums2):
            heapq.heappush(heap, (nums1[i] + nums2[j + 1], i, j + 1))

    return res
```
- **Time Complexity**: O(k log(min(n, k)))
- **Space Complexity**: O(min(n, k))

---

## 4. Merge K Sorted Lists
[LeetCode 23](https://leetcode.com/problems/merge-k-sorted-lists/)

### Problem Description
You are given an array of `k` linked-lists `lists`, each linked-list is sorted in ascending order. Merge all the linked-lists into one sorted linked-list and return it.

### Solution
```python
import heapq

# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def mergeKLists(lists: list[ListNode]) -> ListNode:
    heap = []
    # Put the head of each list into the heap
    for i, l in enumerate(lists):
        if l:
            # Include index i to avoid comparison of ListNode objects if values are equal
            heapq.heappush(heap, (l.val, i, l))

    dummy = ListNode(0)
    curr = dummy

    while heap:
        val, i, node = heapq.heappop(heap)
        curr.next = ListNode(val)
        curr = curr.next

        if node.next:
            heapq.heappush(heap, (node.next.val, i, node.next))

    return dummy.next
```
- **Time Complexity**: O(N log k), where N is total number of nodes and k is number of lists.
- **Space Complexity**: O(k) for the heap.

---

## 5. Find Median from Data Stream
[LeetCode 295](https://leetcode.com/problems/find-median-from-data-stream/)

### Problem Description
The median is the middle value in an ordered integer list. If the size of the list is even, there is no middle value and the median is the mean of the two middle values. Implement the `MedianFinder` class.

### Solution
```python
import heapq

class MedianFinder:
    def __init__(self):
        # max_heap stores the smaller half (negative values for max heap)
        self.small = []
        # min_heap stores the larger half
        self.large = []

    def addNum(self, num: int) -> None:
        # Add to small, then move the largest of small to large
        heapq.heappush(self.small, -num)
        heapq.heappush(self.large, -heapq.heappop(self.small))

        # Maintain balance: small can have at most one more element than large
        if len(self.large) > len(self.small):
            heapq.heappush(self.small, -heapq.heappop(self.large))

    def findMedian(self) -> float:
        if len(self.small) > len(self.large):
            return float(-self.small[0])
        return (-self.small[0] + self.large[0]) / 2.0
```
- **Time Complexity**: O(log n) for `addNum`, O(1) for `findMedian`.
- **Space Complexity**: O(n) to store all numbers.

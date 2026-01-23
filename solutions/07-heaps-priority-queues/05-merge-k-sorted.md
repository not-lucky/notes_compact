# Solution: Merge K Sorted Practice Problems

## Problem 1: Merge k Sorted Lists
### Problem Statement
You are given an array of `k` linked-lists `lists`, each linked-list is sorted in ascending order.

Merge all the linked-lists into one sorted linked-list and return it.

### Constraints
- `k == lists.length`
- `0 <= k <= 10^4`
- `0 <= lists[i].length <= 500`
- `-10^4 <= lists[i][j] <= 10^4`
- `lists[i]` is sorted in ascending order.
- The total number of nodes will not exceed `10^4`.

### Example
Input: `lists = [[1,4,5],[1,3,4],[2,6]]`
Output: `[1,1,2,3,4,4,5,6]`

### Python Implementation
```python
import heapq
from typing import Optional

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def mergeKLists(lists: list[Optional[ListNode]]) -> Optional[ListNode]:
    """
    Time Complexity: O(n log k)
    Space Complexity: O(k)
    """
    heap = []
    # (value, list_index, node)
    for i, node in enumerate(lists):
        if node:
            heapq.heappush(heap, (node.val, i, node))

    dummy = ListNode(0)
    curr = dummy

    while heap:
        val, i, node = heapq.heappop(heap)
        curr.next = node
        curr = curr.next
        if node.next:
            heapq.heappush(heap, (node.next.val, i, node.next))

    return dummy.next
```

---

## Problem 2: Merge Two Sorted Lists
### Problem Statement
You are given the heads of two sorted linked lists `list1` and `list2`.

Merge the two lists into one sorted list. The list should be made by splicing together the nodes of the first two lists.

Return the head of the merged linked list.

### Constraints
- The number of nodes in both lists is in the range `[0, 50]`.
- `-100 <= Node.val <= 100`
- Both `list1` and `list2` are sorted in non-decreasing order.

### Python Implementation
```python
from typing import Optional

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def mergeTwoLists(list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
    """
    Time Complexity: O(n + m)
    Space Complexity: O(1)
    """
    dummy = ListNode(0)
    curr = dummy

    while list1 and list2:
        if list1.val <= list2.val:
            curr.next = list1
            list1 = list1.next
        else:
            curr.next = list2
            list2 = list2.next
        curr = curr.next

    curr.next = list1 or list2
    return dummy.next
```

---

## Problem 3: Smallest Range Covering Elements from K Lists
### Problem Statement
You have `k` lists of sorted integers in non-decreasing order. Find the smallest range that includes at least one number from each of the `k` lists.

We define the range `[a, b]` is smaller than range `[c, d]` if `b - a < d - c` or `a < c` if `b - a == d - c`.

### Constraints
- `nums.length == k`
- `1 <= k <= 3500`
- `1 <= nums[i].length <= 50`
- `-10^5 <= nums[i][j] <= 10^5`
- `nums[i]` is sorted in non-decreasing order.

### Example
Input: `nums = [[4,10,15,24,26],[0,9,12,20],[5,18,22,30]]`
Output: `[20,24]`

### Python Implementation
```python
import heapq

def smallestRange(nums: list[list[int]]) -> list[int]:
    """
    Time Complexity: O(n log k)
    Space Complexity: O(k)
    """
    k = len(nums)
    # (value, list_index, element_index)
    heap = [(lst[0], i, 0) for i, lst in enumerate(nums) if lst]
    heapq.heapify(heap)

    curr_max = max(lst[0] for lst in nums if lst)
    res = [heap[0][0], curr_max]

    while True:
        min_val, list_idx, elem_idx = heapq.heappop(heap)

        if curr_max - min_val < res[1] - res[0]:
            res = [min_val, curr_max]

        if elem_idx + 1 >= len(nums[list_idx]):
            break

        next_val = nums[list_idx][elem_idx + 1]
        curr_max = max(curr_max, next_val)
        heapq.heappush(heap, (next_val, list_idx, elem_idx + 1))

    return res
```

---

## Problem 4: Find K Pairs with Smallest Sums
### Problem Statement
You are given two integer arrays `nums1` and `nums2` sorted in non-decreasing order and an integer `k`. Return the `k` pairs `(u, v)` with the smallest sums.

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

## Problem 5: Kth Smallest Element in a Sorted Matrix
### Problem Statement
Given an `n x n` `matrix` where each of the rows and columns is sorted in ascending order, return the `k`th smallest element in the matrix.

### Python Implementation
```python
import heapq

def kthSmallest(matrix: list[list[int]], k: int) -> int:
    """
    Time Complexity: O(k log n)
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

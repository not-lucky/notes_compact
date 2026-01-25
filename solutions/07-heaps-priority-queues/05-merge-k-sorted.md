# Merge K Sorted Solutions

## 1. Merge k Sorted Lists
Merge `k` sorted linked lists and return it as one sorted list.

### Examples & Edge Cases
- **Example**: `[[1,4,5], [1,3,4], [2,6]] -> [1,1,2,3,4,4,5,6]`
- **Edge Case: Empty lists**: Should return `None`.

### Optimal Python Solution (Min-Heap)
```python
import heapq

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def mergeKLists(lists: list[ListNode]) -> ListNode:
    """
    Min-heap stores the current heads of each list.

    Time Complexity: O(N log k)
    Space Complexity: O(k)
    """
    min_heap = []

    # Initialize heap with non-empty list heads
    for i, l in enumerate(lists):
        if l:
            heapq.heappush(min_heap, (l.val, i, l))

    dummy = ListNode()
    curr = dummy

    while min_heap:
        val, i, node = heapq.heappop(min_heap)
        curr.next = node
        curr = curr.next

        if node.next:
            heapq.heappush(min_heap, (node.next.val, i, node.next))

    return dummy.next
```

---

## 2. Merge Two Sorted Lists
Merge two sorted linked lists and return it as a sorted list.

### Optimal Python Solution
```python
def mergeTwoLists(l1: ListNode, l2: ListNode) -> ListNode:
    """
    Iterative merge using dummy head.

    Time Complexity: O(n + m)
    Space Complexity: O(1)
    """
    dummy = ListNode()
    curr = dummy

    while l1 and l2:
        if l1.val <= l2.val:
            curr.next = l1
            l1 = l1.next
        else:
            curr.next = l2
            l2 = l2.next
        curr = curr.next

    curr.next = l1 or l2
    return dummy.next
```

---

## 3. Smallest Range Covering Elements from K Lists
You have `k` lists of sorted integers in non-decreasing order. Find the smallest range that includes at least one number from each of the `k` lists.

### Optimal Python Solution
```python
import heapq

def smallestRange(nums: list[list[int]]) -> list[int]:
    """
    Use a Min-Heap to track the minimum element of the current range across k lists.
    Also track the current maximum to calculate the range size.

    Time Complexity: O(N log k) where N is total elements
    Space Complexity: O(k)
    """
    min_heap = []
    curr_max = float('-inf')

    # Initial setup
    for i in range(len(nums)):
        heapq.heappush(min_heap, (nums[i][0], i, 0))
        curr_max = max(curr_max, nums[i][0])

    res = [float('-inf'), float('inf')]

    while min_heap:
        curr_min, row, col = heapq.heappop(min_heap)

        # Update result if a smaller range is found
        if curr_max - curr_min < res[1] - res[0]:
            res = [curr_min, curr_max]

        # If we reach the end of one list, we can't form a range with all lists anymore
        if col + 1 == len(nums[row]):
            return res

        # Push next element from the same list
        next_val = nums[row][col + 1]
        heapq.heappush(min_heap, (next_val, row, col + 1))
        curr_max = max(curr_max, next_val)
```

---

## 4. Find K Pairs with Smallest Sums
Given two sorted arrays and an integer `k`, find the `k` pairs `(u, v)` with the smallest sums.

### Examples & Edge Cases
- **Example**: `nums1 = [1,7,11], nums2 = [2,4,6], k = 3` -> `[[1,2],[1,4],[1,6]]`
- **Edge Case: k > total possible pairs**: Return all pairs.

### Optimal Python Solution (Min-Heap)
```python
import heapq

def kSmallestPairs(nums1: list[int], nums2: list[int], k: int) -> list[list[int]]:
    """
    Use a Min-Heap. The next smallest pair always comes from either increasing
     the index in nums1 or nums2 from a previously explored pair.

    Time Complexity: O(k log k)
    Space Complexity: O(k)
    """
    if not nums1 or not nums2:
        return []

    res = []
    # (sum, index_in_nums1, index_in_nums2)
    min_heap = []

    # Initialize with pairs (nums1[i], nums2[0])
    # We only need to check at most k elements from nums1
    for i in range(min(len(nums1), k)):
        heapq.heappush(min_heap, (nums1[i] + nums2[0], i, 0))

    while min_heap and len(res) < k:
        curr_sum, i, j = heapq.heappop(min_heap)
        res.append([nums1[i], nums2[j]])

        # If there is a next element in nums2, push the new pair
        if j + 1 < len(nums2):
            heapq.heappush(min_heap, (nums1[i] + nums2[j + 1], i, j + 1))

    return res
```

### Explanation
1.  **Heap of Potential Pairs**: We maintain a min-heap of candidate pairs.
2.  **Initialization**: We start by pairing each of the first $k$ elements of `nums1` with the first element of `nums2`.
3.  **Progression**: Every time we pop a pair $(nums1[i], nums2[j])$, the next potential smallest pair involving $nums1[i]$ must be $(nums1[i], nums2[j+1])$.

### Complexity Analysis
- **Time Complexity**: $O(k \log k)$. We perform $k$ pop and push operations.
- **Space Complexity**: $O(k)$ for the heap.

---

## 5. Kth Smallest Element in a Sorted Matrix
Given an `n x n` matrix where each row and column is sorted, find the `k`-th smallest element.

### Examples & Edge Cases
- **Example**: `matrix = [[1,5,9],[10,11,13],[12,13,15]], k = 8` -> `13`
- **Edge Case: k = 1**: Returns `matrix[0][0]`.

### Optimal Python Solution (Min-Heap)
```python
import heapq

def kthSmallest(matrix: list[list[int]], k: int) -> int:
    """
    Treat the matrix as n sorted lists and merge them using a min-heap.

    Time Complexity: O(k log n)
    Space Complexity: O(n)
    """
    n = len(matrix)
    # Min-heap: (value, row, col)
    min_heap = []

    # Initialize heap with the first element of each row
    for i in range(min(n, k)):
        heapq.heappush(min_heap, (matrix[i][0], i, 0))

    val = 0
    for _ in range(k):
        val, r, c = heapq.heappop(min_heap)
        if c + 1 < n:
            heapq.heappush(min_heap, (matrix[r][c + 1], r, c + 1))

    return val
```

### Explanation
1.  **Merge-K Strategy**: Since each row is sorted, this is exactly like merging $n$ sorted lists. We pop the smallest element across all lists and push the next element from that same list (row) into the heap.

### Complexity Analysis
- **Time Complexity**: $O(k \log (\min(n, k)))$.
- **Space Complexity**: $O(\min(n, k))$.

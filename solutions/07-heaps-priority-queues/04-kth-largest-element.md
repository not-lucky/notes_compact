# Kth Largest Element Solutions

## 1. Kth Largest Element in an Array

Find the kth largest element in an array.

### Examples & Edge Cases

- **Example**: `nums = [3,2,3,1,2,4,5,5,6], k = 4` -> Output: 4
- **Edge Case: k = 1**: Should return the maximum.

### Optimal Python Solution (QuickSelect)

```python
import random

def findKthLargest(nums: list[int], k: int) -> int:
    """
    QuickSelect Algorithm (Hoare's Selection Algorithm).
    Average Time: O(n), Worst Time: O(n^2)
    Space: O(1)
    """
    target = len(nums) - k  # Convert kth largest to index in sorted ascending array

    def partition(left, right):
        pivot_idx = random.randint(left, right)
        pivot = nums[pivot_idx]
        # Move pivot to end
        nums[pivot_idx], nums[right] = nums[right], nums[pivot_idx]

        store_idx = left
        for i in range(left, right):
            if nums[i] < pivot:
                nums[i], nums[store_idx] = nums[store_idx], nums[i]
                store_idx += 1

        nums[store_idx], nums[right] = nums[right], nums[store_idx]
        return store_idx

    left, right = 0, len(nums) - 1
    while left <= right:
        idx = partition(left, right)
        if idx == target:
            return nums[idx]
        elif idx < target:
            left = idx + 1
        else:
            right = idx - 1
```

### Explanation

1.  **Pivot Selection**: We choose a random pivot to avoid the $O(n^2)$ worst case on sorted/nearly sorted inputs.
2.  **Partitioning**: We rearrange elements so that all elements smaller than the pivot are to its left.
3.  **Selection**: Unlike QuickSort, we only recurse into the side that contains our `target` index.

### Complexity Analysis

- **Time Complexity**: Average $O(n)$, Worst $O(n^2)$.
- **Space Complexity**: $O(1)$ iterative, or $O(\log n)$ recursive for call stack.

---

## 2. Kth Smallest Element in a Sorted Matrix

Given an `n x n` matrix where each row and column is sorted in ascending order, find the kth smallest element.

### Optimal Python Solution (Min-Heap)

```python
import heapq

def kthSmallest(matrix: list[list[int]], k: int) -> int:
    """
    Use a Min-Heap to track the smallest available elements from each row.
    This is similar to merging k sorted lists.

    Time Complexity: O(k log n)
    Space Complexity: O(n)
    """
    n = len(matrix)
    # Min-heap: (value, row, col)
    # Initialize with the first element of each row
    min_heap = [(matrix[i][0], i, 0) for i in range(min(n, k))]
    heapq.heapify(min_heap)

    ans = 0
    for _ in range(k):
        ans, r, c = heapq.heappop(min_heap)
        if c + 1 < n:
            heapq.heappush(min_heap, (matrix[r][c + 1], r, c + 1))

    return ans
```

### Complexity Analysis

- **Time Complexity**: $O(k \log (\min(n, k)))$.
- **Space Complexity**: $O(\min(n, k))$.

---

## 3. Find K Pairs with Smallest Sums

Find `k` pairs `(u, v)` with one element from `nums1` and one from `nums2` such that the sum is smallest.

### Optimal Python Solution

```python
import heapq

def kSmallestPairs(nums1: list[int], nums2: list[int], k: int) -> list[list[int]]:
    """
    Use a Min-Heap. Start with pairs (nums1[i], nums2[0]).

    Time Complexity: O(k log k)
    Space Complexity: O(k)
    """
    if not nums1 or not nums2: return []

    res = []
    min_heap = []

    # Initialize heap with (nums1[i] + nums2[0], i, 0) for first k elements of nums1
    for i in range(min(len(nums1), k)):
        heapq.heappush(min_heap, (nums1[i] + nums2[0], i, 0))

    while min_heap and len(res) < k:
        summ, i, j = heapq.heappop(min_heap)
        res.append([nums1[i], nums2[j]])

        if j + 1 < len(nums2):
            heapq.heappush(min_heap, (nums1[i] + nums2[j + 1], i, j + 1))

    return res
```

### Complexity Analysis

- **Time Complexity**: $O(k \log k)$.
- **Space Complexity**: $O(k)$.

---

## 4. Kth Smallest Element in a BST

Given the root of a binary search tree, and an integer `k`, return the kth smallest value (1-indexed).

### Optimal Python Solution (In-order Traversal)

```python
def kthSmallest(root: Optional[TreeNode], k: int) -> int:
    """
    In-order traversal of a BST visits nodes in sorted order.

    Time Complexity: O(H + k) where H is tree height
    Space Complexity: O(H) for recursion stack
    """
    stack = []
    curr = root

    while stack or curr:
        while curr:
            stack.append(curr)
            curr = curr.left

        curr = stack.pop()
        k -= 1
        if k == 0:
            return curr.val
        curr = curr.right
```

---

## 5. Third Maximum Number

Return the third maximum distinct number in an array. If it does not exist, return the maximum number.

### Optimal Python Solution

```python
def thirdMax(nums: list[int]) -> int:
    """
    Maintain three variables to track top 3 distinct maximums.

    Time Complexity: O(n)
    Space Complexity: O(1)
    """
    first = second = third = float('-inf')

    for num in set(nums):
        if num > first:
            first, second, third = num, first, second
        elif num > second:
            second, third = num, second
        elif num > third:
            third = num

    return third if third != float('-inf') else first
```

### Complexity Analysis

- **Time Complexity**: $O(n)$.
- **Space Complexity**: $O(n)$ for the `set` conversion, or $O(1)$ if we use a different way to check for distinctness.

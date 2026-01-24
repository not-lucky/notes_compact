# Solution: Pattern Selection and Data Structures

## Problem 1: Two Sum II (Sorted Array)
### Problem Statement
Given a 1-indexed array of integers `numbers` that is already sorted in non-decreasing order, find two numbers such that they add up to a specific `target` number. Let these two numbers be `numbers[index1]` and `numbers[index2]` where `1 <= index1 < index2 <= numbers.length`.

Return the indices of the two numbers, `index1` and `index2`, added by one as an integer array `[index1, index2]` of length 2.

### Python Implementation
```python
def twoSum(numbers: list[int], target: int) -> list[int]:
    """
    Pattern: Two Pointers (Opposite Direction)
    Time Complexity: O(n)
    Space Complexity: O(1)
    """
    left, right = 0, len(numbers) - 1

    while left < right:
        curr_sum = numbers[left] + numbers[right]
        if curr_sum == target:
            return [left + 1, right + 1]
        elif curr_sum < target:
            left += 1
        else:
            right -= 1

    return []
```

---

## Problem 2: Longest Substring Without Repeating Characters
### Problem Statement
Given a string `s`, find the length of the longest substring without repeating characters.

### Python Implementation
```python
def lengthOfLongestSubstring(s: str) -> int:
    """
    Pattern: Sliding Window (Variable Size)
    Time Complexity: O(n)
    Space Complexity: O(min(m, n)) where m is size of charset
    """
    char_map = {}
    left = 0
    max_len = 0

    for right in range(len(s)):
        if s[right] in char_map:
            # Move left pointer to the right of the last seen position
            left = max(left, char_map[s[right]] + 1)

        char_map[s[right]] = right
        max_len = max(max_len, right - left + 1)

    return max_len
```

---

## Problem 3: Kth Largest Element in an Array
### Problem Statement
Given an integer array `nums` and an integer `k`, return the `kth` largest element in the array.

Note that it is the `kth` largest element in the sorted order, not the `kth` distinct element.

### Python Implementation
```python
import heapq

def findKthLargest(nums: list[int], k: int) -> int:
    """
    Pattern: Heap (Top-K)
    Time Complexity: O(n log k)
    Space Complexity: O(k)
    """
    # Use min-heap of size k
    heap = nums[:k]
    heapq.heapify(heap)

    for num in nums[k:]:
        if num > heap[0]:
            heapq.heapreplace(heap, num)

    return heap[0]
```

---

## Problem 4: Linked List Cycle
### Problem Statement
Given `head`, the head of a linked list, determine if the linked list has a cycle in it.

### Python Implementation
```python
class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None

def hasCycle(head: ListNode) -> bool:
    """
    Pattern: Fast & Slow Pointers (Floyd's Cycle-Finding)
    Time Complexity: O(n)
    Space Complexity: O(1)
    """
    if not head or not head.next:
        return False

    slow = head
    fast = head

    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next

        if slow == fast:
            return True

    return False
```

---

## Problem 5: Shortest Path in Binary Matrix
### Problem Statement
Given an `n x n` binary matrix `grid`, return the length of the shortest clear path in the matrix. If there is no clear path, return `-1`.

A clear path in a binary matrix is a path from the top-left cell (i.e., `(0, 0)`) to the bottom-right cell (i.e., `(n - 1, n - 1)`) such that:
- All the visited cells of the path are `0`.
- All the adjacent cells of the path are 8-directionally connected (i.e., they are different and they share an edge or a corner).

### Python Implementation
```python
from collections import deque

def shortestPathBinaryMatrix(grid: list[list[int]]) -> int:
    """
    Pattern: BFS (Shortest Path in Unweighted Graph)
    Time Complexity: O(n^2)
    Space Complexity: O(n^2)
    """
    n = len(grid)
    if grid[0][0] == 1 or grid[n-1][n-1] == 1:
        return -1

    queue = deque([(0, 0, 1)]) # row, col, distance
    visited = {(0, 0)}

    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

    while queue:
        r, c, dist = queue.popleft()

        if r == n - 1 and c == n - 1:
            return dist

        for dr, dc in directions:
            nr, nc = r + dr, c + dc

            if 0 <= nr < n and 0 <= nc < n and grid[nr][nc] == 0 and (nr, nc) not in visited:
                visited.add((nr, nc))
                queue.append((nr, nc, dist + 1))

    return -1
```

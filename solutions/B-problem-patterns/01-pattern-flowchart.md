# Problem Patterns Guide

## Practice Problems

### 1. Two Sum II - Input Array Is Sorted
**Difficulty:** Medium
**Key Technique:** Two Pointers (Opposite Direction)

```python
def two_sum(numbers: list[int], target: int) -> list[int]:
    """
    Time: O(n)
    Space: O(1)
    """
    l, r = 0, len(numbers) - 1
    while l < r:
        s = numbers[l] + numbers[r]
        if s == target: return [l + 1, r + 1]
        elif s < target: l += 1
        else: r -= 1
    return []
```

### 2. Longest Substring Without Repeating Characters
**Difficulty:** Medium
**Key Technique:** Sliding Window (Variable Size)

```python
def length_of_longest_substring(s: str) -> int:
    """
    Time: O(n)
    Space: O(min(n, m)) where m is alphabet size
    """
    seen = {}
    l = 0
    res = 0
    for r, char in enumerate(s):
        if char in seen:
            l = max(l, seen[char] + 1)
        seen[char] = r
        res = max(res, r - l + 1)
    return res
```

### 3. Binary Tree Level Order Traversal
**Difficulty:** Medium
**Key Technique:** BFS

```python
from collections import deque

def level_order(root) -> list[list[int]]:
    """
    Time: O(n)
    Space: O(n)
    """
    if not root: return []
    res = []
    q = deque([root])
    while q:
        level = []
        for _ in range(len(q)):
            node = q.popleft()
            level.append(node.val)
            if node.left: q.append(node.left)
            if node.right: q.append(node.right)
        res.append(level)
    return res
```

### 4. Climbing Stairs
**Difficulty:** Easy
**Key Technique:** 1D DP

```python
def climb_stairs(n: int) -> int:
    """
    Time: O(n)
    Space: O(1)
    """
    if n <= 2: return n
    p1, p2 = 1, 2
    for _ in range(3, n + 1):
        p1, p2 = p2, p1 + p2
    return p2
```

### 5. Next Greater Element I
**Difficulty:** Easy
**Key Technique:** Monotonic Stack

```python
def next_greater_element(nums1: list[int], nums2: list[int]) -> list[int]:
    """
    Time: O(n + m)
    Space: O(m)
    """
    res = {}
    stack = []
    for n in nums2:
        while stack and stack[-1] < n:
            res[stack.pop()] = n
        stack.append(n)
    return [res.get(n, -1) for n in nums1]
```

# Template Code for Major Patterns

> **Prerequisites:** [02-when-to-use-what.md](./02-when-to-use-what.md)

This file contains copy-paste-ready templates for the most common interview patterns. Each template is minimal and designed to be adapted to specific problems.

---

## Table of Contents

1. [Two Pointers](#1-two-pointers)
2. [Sliding Window](#2-sliding-window)
3. [Binary Search](#3-binary-search)
4. [BFS](#4-bfs)
5. [DFS](#5-dfs)
6. [Backtracking](#6-backtracking)
7. [Dynamic Programming](#7-dynamic-programming)
8. [Monotonic Stack](#8-monotonic-stack)
9. [Heap / Top-K](#9-heap--top-k)
10. [Union-Find](#10-union-find)
11. [Trie](#11-trie)
12. [Graph Algorithms](#12-graph-algorithms)
13. [Linked List Patterns](#13-linked-list-patterns)
14. [Intervals](#14-intervals)

---

## 1. Two Pointers

### Opposite Direction (Sorted Array)

```python
def two_sum_sorted(arr: list[int], target: int) -> list[int]:
    """Find indices of two numbers that sum to target in sorted array."""
    left, right = 0, len(arr) - 1

    while left < right:
        curr_sum = arr[left] + arr[right]

        if curr_sum == target:
            return [left, right]
        elif curr_sum < target:
            left += 1
        else:
            right -= 1

    return []  # No solution
```

### Same Direction (Fast/Slow)

```python
def remove_duplicates(arr: list[int]) -> int:
    """Remove duplicates in-place, return new length."""
    if not arr:
        return 0

    slow = 0  # Position to write next unique element

    for fast in range(1, len(arr)):
        if arr[fast] != arr[slow]:
            slow += 1
            arr[slow] = arr[fast]

    return slow + 1
```

### Three Pointers (3Sum)

```python
def three_sum(nums: list[int]) -> list[list[int]]:
    """Find all unique triplets that sum to zero."""
    nums.sort()
    result = []

    for i in range(len(nums) - 2):
        if i > 0 and nums[i] == nums[i - 1]:
            continue  # Skip duplicates

        left, right = i + 1, len(nums) - 1

        while left < right:
            total = nums[i] + nums[left] + nums[right]

            if total == 0:
                result.append([nums[i], nums[left], nums[right]])
                left += 1
                right -= 1
                while left < right and nums[left] == nums[left - 1]:
                    left += 1  # Skip duplicates
            elif total < 0:
                left += 1
            else:
                right -= 1

    return result
```

---

## 2. Sliding Window

### Fixed Size Window

```python
def max_sum_subarray_k(arr: list[int], k: int) -> int:
    """Find maximum sum of subarray of size k."""
    if len(arr) < k:
        return 0

    # Calculate sum of first window
    window_sum = sum(arr[:k])
    max_sum = window_sum

    # Slide the window
    for i in range(k, len(arr)):
        window_sum += arr[i] - arr[i - k]  # Add new, remove old
        max_sum = max(max_sum, window_sum)

    return max_sum
```

### Variable Size Window (Expand/Shrink)

```python
def longest_substring_k_distinct(s: str, k: int) -> int:
    """Find longest substring with at most k distinct characters."""
    from collections import defaultdict

    char_count = defaultdict(int)
    left = 0
    max_len = 0

    for right in range(len(s)):
        # Expand window
        char_count[s[right]] += 1

        # Shrink window until valid
        while len(char_count) > k:
            char_count[s[left]] -= 1
            if char_count[s[left]] == 0:
                del char_count[s[left]]
            left += 1

        # Update result
        max_len = max(max_len, right - left + 1)

    return max_len
```

### Variable Size Window (Find Minimum)

```python
def min_window_substring(s: str, t: str) -> str:
    """Find minimum window containing all characters of t."""
    from collections import Counter

    if not s or not t:
        return ""

    need = Counter(t)
    have = 0
    required = len(need)

    left = 0
    min_len = float('inf')
    result = ""

    for right in range(len(s)):
        char = s[right]
        if char in need:
            need[char] -= 1
            if need[char] == 0:
                have += 1

        # Shrink window while valid
        while have == required:
            if right - left + 1 < min_len:
                min_len = right - left + 1
                result = s[left:right + 1]

            left_char = s[left]
            if left_char in need:
                if need[left_char] == 0:
                    have -= 1
                need[left_char] += 1
            left += 1

    return result
```

---

## 3. Binary Search

### Standard Binary Search

```python
def binary_search(arr: list[int], target: int) -> int:
    """Find index of target, or -1 if not found."""
    left, right = 0, len(arr) - 1

    while left <= right:
        mid = left + (right - left) // 2

        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return -1
```

### Find Left Boundary (First Occurrence)

```python
def find_left_boundary(arr: list[int], target: int) -> int:
    """Find index of first occurrence of target."""
    left, right = 0, len(arr) - 1
    result = -1

    while left <= right:
        mid = left + (right - left) // 2

        if arr[mid] == target:
            result = mid
            right = mid - 1  # Keep searching left
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return result
```

### Find Right Boundary (Last Occurrence)

```python
def find_right_boundary(arr: list[int], target: int) -> int:
    """Find index of last occurrence of target."""
    left, right = 0, len(arr) - 1
    result = -1

    while left <= right:
        mid = left + (right - left) // 2

        if arr[mid] == target:
            result = mid
            left = mid + 1  # Keep searching right
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return result
```

### Binary Search on Answer

```python
def min_capacity(weights: list[int], days: int) -> int:
    """Find minimum ship capacity to ship all packages in D days."""
    def can_ship(capacity: int) -> bool:
        day_count = 1
        current_load = 0
        for w in weights:
            if current_load + w > capacity:
                day_count += 1
                current_load = 0
            current_load += w
        return day_count <= days

    left, right = max(weights), sum(weights)

    while left < right:
        mid = left + (right - left) // 2
        if can_ship(mid):
            right = mid
        else:
            left = mid + 1

    return left
```

---

## 4. BFS

### Standard BFS (Graph/Tree)

```python
from collections import deque

def bfs(graph: dict, start: int) -> list[int]:
    """Return nodes in BFS order."""
    visited = {start}
    queue = deque([start])
    order = []

    while queue:
        node = queue.popleft()
        order.append(node)

        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

    return order
```

### BFS Shortest Path (Unweighted)

```python
from collections import deque

def shortest_path(graph: dict, start: int, end: int) -> int:
    """Find shortest path length from start to end."""
    if start == end:
        return 0

    visited = {start}
    queue = deque([(start, 0)])  # (node, distance)

    while queue:
        node, dist = queue.popleft()

        for neighbor in graph[node]:
            if neighbor == end:
                return dist + 1
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, dist + 1))

    return -1  # No path found
```

### BFS Level Order (Tree)

```python
from collections import deque

def level_order(root) -> list[list[int]]:
    """Return level order traversal of binary tree."""
    if not root:
        return []

    result = []
    queue = deque([root])

    while queue:
        level_size = len(queue)
        level = []

        for _ in range(level_size):
            node = queue.popleft()
            level.append(node.val)

            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)

        result.append(level)

    return result
```

### Multi-Source BFS

```python
from collections import deque

def multi_source_bfs(grid: list[list[int]], sources: list[tuple]) -> list[list[int]]:
    """BFS from multiple starting points (e.g., rotting oranges)."""
    rows, cols = len(grid), len(grid[0])
    dist = [[-1] * cols for _ in range(rows)]
    queue = deque()

    # Initialize all sources
    for r, c in sources:
        dist[r][c] = 0
        queue.append((r, c))

    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    while queue:
        r, c = queue.popleft()

        for dr, dc in directions:
            nr, nc = r + dr, c + dc

            if 0 <= nr < rows and 0 <= nc < cols and dist[nr][nc] == -1:
                dist[nr][nc] = dist[r][c] + 1
                queue.append((nr, nc))

    return dist
```

---

## 5. DFS

### DFS on Graph

```python
def dfs_iterative(graph: dict, start: int) -> list[int]:
    """DFS using stack."""
    visited = set()
    stack = [start]
    order = []

    while stack:
        node = stack.pop()
        if node in visited:
            continue
        visited.add(node)
        order.append(node)

        for neighbor in graph[node]:
            if neighbor not in visited:
                stack.append(neighbor)

    return order


def dfs_recursive(graph: dict, start: int, visited: set = None) -> list[int]:
    """DFS using recursion."""
    if visited is None:
        visited = set()

    visited.add(start)
    order = [start]

    for neighbor in graph[start]:
        if neighbor not in visited:
            order.extend(dfs_recursive(graph, neighbor, visited))

    return order
```

### DFS on Grid (Islands)

```python
def count_islands(grid: list[list[str]]) -> int:
    """Count number of islands in a grid."""
    if not grid:
        return 0

    rows, cols = len(grid), len(grid[0])
    count = 0

    def dfs(r: int, c: int):
        if r < 0 or r >= rows or c < 0 or c >= cols or grid[r][c] != '1':
            return
        grid[r][c] = '0'  # Mark visited
        dfs(r + 1, c)
        dfs(r - 1, c)
        dfs(r, c + 1)
        dfs(r, c - 1)

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1':
                dfs(r, c)
                count += 1

    return count
```

### DFS Tree Path Sum

```python
def has_path_sum(root, target_sum: int) -> bool:
    """Check if tree has root-to-leaf path with given sum."""
    if not root:
        return False

    # Leaf node
    if not root.left and not root.right:
        return root.val == target_sum

    # Recursive case
    remaining = target_sum - root.val
    return (has_path_sum(root.left, remaining) or
            has_path_sum(root.right, remaining))
```

---

## 6. Backtracking

### Subsets

```python
def subsets(nums: list[int]) -> list[list[int]]:
    """Generate all subsets."""
    result = []

    def backtrack(start: int, path: list[int]):
        result.append(path[:])  # Add copy of current subset

        for i in range(start, len(nums)):
            path.append(nums[i])
            backtrack(i + 1, path)
            path.pop()

    backtrack(0, [])
    return result
```

### Permutations

```python
def permutations(nums: list[int]) -> list[list[int]]:
    """Generate all permutations."""
    result = []

    def backtrack(path: list[int], remaining: set):
        if not remaining:
            result.append(path[:])
            return

        for num in list(remaining):
            path.append(num)
            remaining.remove(num)
            backtrack(path, remaining)
            remaining.add(num)
            path.pop()

    backtrack([], set(nums))
    return result
```

### Combinations

```python
def combinations(n: int, k: int) -> list[list[int]]:
    """Generate all combinations of k numbers from 1 to n."""
    result = []

    def backtrack(start: int, path: list[int]):
        if len(path) == k:
            result.append(path[:])
            return

        # Pruning: need at least (k - len(path)) more elements
        for i in range(start, n - (k - len(path)) + 2):
            path.append(i)
            backtrack(i + 1, path)
            path.pop()

    backtrack(1, [])
    return result
```

### N-Queens

```python
def solve_n_queens(n: int) -> list[list[str]]:
    """Solve N-Queens problem."""
    result = []
    cols = set()
    diag1 = set()  # row - col
    diag2 = set()  # row + col

    def backtrack(row: int, queens: list[int]):
        if row == n:
            board = []
            for c in queens:
                board.append('.' * c + 'Q' + '.' * (n - c - 1))
            result.append(board)
            return

        for col in range(n):
            if col in cols or (row - col) in diag1 or (row + col) in diag2:
                continue

            cols.add(col)
            diag1.add(row - col)
            diag2.add(row + col)
            queens.append(col)

            backtrack(row + 1, queens)

            cols.remove(col)
            diag1.remove(row - col)
            diag2.remove(row + col)
            queens.pop()

    backtrack(0, [])
    return result
```

---

## 7. Dynamic Programming

### 1D DP (Climbing Stairs)

```python
def climb_stairs(n: int) -> int:
    """Count ways to climb n stairs (1 or 2 steps at a time)."""
    if n <= 2:
        return n

    prev2, prev1 = 1, 2

    for _ in range(3, n + 1):
        curr = prev1 + prev2
        prev2, prev1 = prev1, curr

    return prev1
```

### 1D DP with Choices (Coin Change)

```python
def coin_change(coins: list[int], amount: int) -> int:
    """Find minimum coins needed to make amount."""
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0

    for a in range(1, amount + 1):
        for coin in coins:
            if coin <= a:
                dp[a] = min(dp[a], dp[a - coin] + 1)

    return dp[amount] if dp[amount] != float('inf') else -1
```

### 2D DP (Longest Common Subsequence)

```python
def longest_common_subsequence(text1: str, text2: str) -> int:
    """Find length of LCS."""
    m, n = len(text1), len(text2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i - 1] == text2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    return dp[m][n]
```

### 0/1 Knapsack

```python
def knapsack(weights: list[int], values: list[int], capacity: int) -> int:
    """Find maximum value that fits in capacity."""
    n = len(weights)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        for w in range(capacity + 1):
            # Don't take item i
            dp[i][w] = dp[i - 1][w]
            # Take item i (if it fits)
            if weights[i - 1] <= w:
                dp[i][w] = max(dp[i][w],
                               dp[i - 1][w - weights[i - 1]] + values[i - 1])

    return dp[n][capacity]
```

### DP with Memoization

```python
from functools import lru_cache

def word_break(s: str, word_dict: list[str]) -> bool:
    """Check if string can be segmented into dictionary words."""
    word_set = set(word_dict)

    @lru_cache(maxsize=None)
    def dp(start: int) -> bool:
        if start == len(s):
            return True

        for end in range(start + 1, len(s) + 1):
            if s[start:end] in word_set and dp(end):
                return True

        return False

    return dp(0)
```

---

## 8. Monotonic Stack

### Next Greater Element

```python
def next_greater_element(nums: list[int]) -> list[int]:
    """Find next greater element for each element."""
    result = [-1] * len(nums)
    stack = []  # Store indices

    for i in range(len(nums)):
        while stack and nums[stack[-1]] < nums[i]:
            result[stack.pop()] = nums[i]
        stack.append(i)

    return result
```

### Largest Rectangle in Histogram

```python
def largest_rectangle_area(heights: list[int]) -> int:
    """Find largest rectangle in histogram."""
    stack = []  # Store indices
    max_area = 0
    heights.append(0)  # Sentinel

    for i, h in enumerate(heights):
        while stack and heights[stack[-1]] > h:
            height = heights[stack.pop()]
            width = i if not stack else i - stack[-1] - 1
            max_area = max(max_area, height * width)
        stack.append(i)

    heights.pop()  # Remove sentinel
    return max_area
```

---

## 9. Heap / Top-K

### Kth Largest Element

```python
import heapq

def find_kth_largest(nums: list[int], k: int) -> int:
    """Find kth largest element."""
    # Min heap of size k
    heap = nums[:k]
    heapq.heapify(heap)

    for num in nums[k:]:
        if num > heap[0]:
            heapq.heapreplace(heap, num)

    return heap[0]
```

### Top K Frequent Elements

```python
import heapq
from collections import Counter

def top_k_frequent(nums: list[int], k: int) -> list[int]:
    """Find k most frequent elements."""
    count = Counter(nums)
    return heapq.nlargest(k, count.keys(), key=count.get)
```

### Merge K Sorted Lists

```python
import heapq

def merge_k_lists(lists: list) -> list:
    """Merge k sorted lists."""
    heap = []
    for i, lst in enumerate(lists):
        if lst:
            heapq.heappush(heap, (lst[0], i, 0))

    result = []
    while heap:
        val, list_idx, elem_idx = heapq.heappop(heap)
        result.append(val)

        if elem_idx + 1 < len(lists[list_idx]):
            next_val = lists[list_idx][elem_idx + 1]
            heapq.heappush(heap, (next_val, list_idx, elem_idx + 1))

    return result
```

### Two Heaps (Find Median)

```python
import heapq

class MedianFinder:
    def __init__(self):
        self.small = []  # Max heap (negated)
        self.large = []  # Min heap

    def add_num(self, num: int) -> None:
        heapq.heappush(self.small, -num)
        heapq.heappush(self.large, -heapq.heappop(self.small))

        if len(self.large) > len(self.small):
            heapq.heappush(self.small, -heapq.heappop(self.large))

    def find_median(self) -> float:
        if len(self.small) > len(self.large):
            return -self.small[0]
        return (-self.small[0] + self.large[0]) / 2
```

---

## 10. Union-Find

```python
class UnionFind:
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.rank = [0] * n
        self.components = n

    def find(self, x: int) -> int:
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # Path compression
        return self.parent[x]

    def union(self, x: int, y: int) -> bool:
        px, py = self.find(x), self.find(y)
        if px == py:
            return False

        # Union by rank
        if self.rank[px] < self.rank[py]:
            px, py = py, px
        self.parent[py] = px
        if self.rank[px] == self.rank[py]:
            self.rank[px] += 1

        self.components -= 1
        return True

    def connected(self, x: int, y: int) -> bool:
        return self.find(x) == self.find(y)
```

---

## 11. Trie

```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True

    def search(self, word: str) -> bool:
        node = self._find_node(word)
        return node is not None and node.is_end

    def starts_with(self, prefix: str) -> bool:
        return self._find_node(prefix) is not None

    def _find_node(self, prefix: str) -> TrieNode:
        node = self.root
        for char in prefix:
            if char not in node.children:
                return None
            node = node.children[char]
        return node
```

---

## 12. Graph Algorithms

### Topological Sort (Kahn's Algorithm)

```python
from collections import deque

def topological_sort(num_nodes: int, edges: list[tuple]) -> list[int]:
    """Return topological order, or empty list if cycle exists."""
    graph = {i: [] for i in range(num_nodes)}
    in_degree = [0] * num_nodes

    for u, v in edges:
        graph[u].append(v)
        in_degree[v] += 1

    queue = deque([i for i in range(num_nodes) if in_degree[i] == 0])
    order = []

    while queue:
        node = queue.popleft()
        order.append(node)

        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    return order if len(order) == num_nodes else []
```

### Dijkstra's Algorithm

```python
import heapq

def dijkstra(graph: dict, start: int) -> dict:
    """Find shortest path from start to all nodes."""
    dist = {node: float('inf') for node in graph}
    dist[start] = 0
    heap = [(0, start)]

    while heap:
        d, node = heapq.heappop(heap)

        if d > dist[node]:
            continue

        for neighbor, weight in graph[node]:
            new_dist = d + weight
            if new_dist < dist[neighbor]:
                dist[neighbor] = new_dist
                heapq.heappush(heap, (new_dist, neighbor))

    return dist
```

---

## 13. Linked List Patterns

### Reverse Linked List

```python
def reverse_list(head):
    """Reverse linked list in-place."""
    prev = None
    curr = head

    while curr:
        next_node = curr.next
        curr.next = prev
        prev = curr
        curr = next_node

    return prev
```

### Detect Cycle

```python
def has_cycle(head) -> bool:
    """Detect if linked list has a cycle."""
    slow = fast = head

    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next

        if slow == fast:
            return True

    return False
```

### Find Middle

```python
def find_middle(head):
    """Find middle node of linked list."""
    slow = fast = head

    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next

    return slow
```

---

## 14. Intervals

### Merge Intervals

```python
def merge_intervals(intervals: list[list[int]]) -> list[list[int]]:
    """Merge overlapping intervals."""
    if not intervals:
        return []

    intervals.sort(key=lambda x: x[0])
    merged = [intervals[0]]

    for start, end in intervals[1:]:
        if start <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])

    return merged
```

### Insert Interval

```python
def insert_interval(intervals: list[list[int]], new: list[int]) -> list[list[int]]:
    """Insert and merge a new interval."""
    result = []
    i = 0
    n = len(intervals)

    # Add all intervals before new interval
    while i < n and intervals[i][1] < new[0]:
        result.append(intervals[i])
        i += 1

    # Merge overlapping intervals
    while i < n and intervals[i][0] <= new[1]:
        new[0] = min(new[0], intervals[i][0])
        new[1] = max(new[1], intervals[i][1])
        i += 1
    result.append(new)

    # Add remaining intervals
    result.extend(intervals[i:])

    return result
```

---

## Usage Tips

1. **Copy the template first** - Don't try to write from scratch
2. **Understand the invariants** - What stays true at each step
3. **Modify for the problem** - Templates are starting points
4. **Test with edge cases** - Empty input, single element, all same values
5. **Know the complexity** - Be ready to explain time/space

---

## Back to: [README.md](./README.md)

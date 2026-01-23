# Solution: Kth Smallest Element in BST Practice Problems

## Problem 1: Kth Smallest Element in a BST
### Problem Statement
Given the `root` of a binary search tree, and an integer `k`, return the `k`th smallest value (1-indexed) of all the values of the nodes in the tree.

### Constraints
- The number of nodes in the tree is `n`.
- `1 <= k <= n <= 10^4`
- `0 <= Node.val <= 10^4`

### Example
Input: `root = [3,1,4,null,2], k = 1`
Output: `1`

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

## Problem 2: Second Minimum Node In a Binary Tree
### Problem Statement
Given a non-empty special binary tree consisting of nodes with the non-negative value, where each node in this tree has exactly two or zero sub-node. If the node has two sub-nodes, then this node's value is the smaller value among its two sub-nodes. More formally, `root.val = min(root.left.val, root.right.val)` always holds.

Given such a binary tree, you need to output the second minimum value in the set made of all the nodes' value in the whole tree.

If no such second minimum value exists, output -1 instead.

### Constraints
- The number of nodes in the tree is in the range `[1, 25]`.
- `1 <= Node.val <= 2^31 - 1`
- `root.val = min(root.left.val, root.right.val)` always holds.

### Example
Input: `root = [2,2,5,null,null,5,7]`
Output: `5`

### Python Implementation
```python
def findSecondMinimumValue(root: TreeNode) -> int:
    """
    Time Complexity: O(n)
    Space Complexity: O(h)
    """
    res = [float('inf')]
    min_val = root.val

    def dfs(node):
        if not node:
            return
        if min_val < node.val < res[0]:
            res[0] = node.val
        elif node.val == min_val:
            dfs(node.left)
            dfs(node.right)

    dfs(root)
    return res[0] if res[0] != float('inf') else -1
```

---

## Problem 3: Count of Smaller Numbers After Self
### Problem Statement
Given an integer array `nums`, return an integer array `counts` where `counts[i]` is the number of smaller elements to the right of `nums[i]`.

### Constraints
- `1 <= nums.length <= 10^5`
- `-10^4 <= nums[i] <= 10^4`

### Example
Input: `nums = [5,2,6,1]`
Output: `[2,1,1,0]`

### Python Implementation
```python
class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None
        self.left_size = 0 # nodes in left subtree

def countSmaller(nums: list[int]) -> list[int]:
    """
    Time Complexity: O(n log n) average, O(n^2) worst case
    Space Complexity: O(n)
    """
    def insert(root, val):
        count = 0
        while True:
            if val <= root.val:
                root.left_size += 1
                if not root.left:
                    root.left = TreeNode(val)
                    break
                root = root.left
            else:
                count += root.left_size + 1
                if not root.right:
                    root.right = TreeNode(val)
                    break
                root = root.right
        return count

    if not nums:
        return []

    res = [0] * len(nums)
    root = TreeNode(nums[-1])

    for i in range(len(nums) - 2, -1, -1):
        res[i] = insert(root, nums[i])

    return res
```

---

## Problem 4: Kth Largest Element in a Stream
### Problem Statement
Design a class to find the kth largest element in a stream. Note that it is the kth largest element in the sorted order, not the kth distinct element.

Implement `KthLargest` class:
- `KthLargest(int k, int[] nums)` Initializes the object with the integer `k` and the stream of integers `nums`.
- `int add(int val)` Appends the integer `val` to the stream and returns the element representing the kth largest element in the stream.

### Constraints
- `1 <= k <= 10^4`
- `0 <= nums.length <= 10^4`
- `-10^4 <= nums[i] <= 10^4`
- `-10^4 <= val <= 10^4`
- At most `10^4` calls will be made to `add`.

### Python Implementation
```python
import heapq

class KthLargest:
    def __init__(self, k: int, nums: list[int]):
        """
        Time Complexity: O(n log k)
        Space Complexity: O(k)
        """
        self.k = k
        self.heap = []
        for n in nums:
            self.add(n)

    def add(self, val: int) -> int:
        """
        Time Complexity: O(log k)
        """
        heapq.heappush(self.heap, val)
        if len(self.heap) > self.k:
            heapq.heappop(self.heap)
        return self.heap[0]
```

---

## Problem 5: Find K-th Smallest Pair Distance
### Problem Statement
The distance of a pair of integers `a` and `b` is defined as the absolute difference between `a` and `b`.

Given an integer array `nums` and an integer `k`, return the `k`th smallest distance among all the pairs `nums[i]` and `nums[j]` where `0 <= i < j < nums.length`.

### Constraints
- `n == nums.length`
- `2 <= n <= 10^4`
- `0 <= nums[i] <= 10^6`
- `1 <= k <= n * (n - 1) / 2`

### Example
Input: `nums = [1,3,1], k = 1`
Output: `0`

### Python Implementation
```python
def smallestDistancePair(nums: list[int], k: int) -> int:
    """
    Time Complexity: O(n log n + n log max_diff)
    Space Complexity: O(1)
    """
    nums.sort()

    def count_pairs(mid):
        count = 0
        left = 0
        for right in range(len(nums)):
            while nums[right] - nums[left] > mid:
                left += 1
            count += right - left
        return count

    low = 0
    high = nums[-1] - nums[0]

    while low < high:
        mid = (low + high) // 2
        if count_pairs(mid) < k:
            low = mid + 1
        else:
            high = mid

    return low
```

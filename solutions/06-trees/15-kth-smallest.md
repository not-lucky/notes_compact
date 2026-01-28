# Kth Smallest Element in BST Solutions

## 1. Kth Smallest Element in a BST

**Problem Statement**: Given the `root` of a binary search tree (BST) and an integer `k`, return the `k`-th smallest value (1-indexed) of all the values of the nodes in the tree.

### Examples & Edge Cases

- **Example 1**: `root = [3,1,4,None,2], k = 1` → Output: `1`
- **Example 2**: `root = [5,3,6,2,4,None,None,1], k = 3` → Output: `3`
- **Edge Case - k = 1**: Returns the smallest element (leftmost).
- **Edge Case - k = n**: Returns the largest element (rightmost).

### Optimal Python Solution (Iterative Inorder)

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def kthSmallest(root: TreeNode, k: int) -> int:
    # BST Property: Inorder traversal yields sorted values
    stack = []
    curr = root

    while True:
        # 1. Travel as far left as possible
        while curr:
            stack.append(curr)
            curr = curr.left

        # 2. Pop the current smallest element
        curr = stack.pop()
        k -= 1

        # 3. If we've popped k elements, we found our target
        if k == 0:
            return curr.val

        # 4. Move to the right child and repeat
        curr = curr.right
```

### Explanation

1.  **BST Order**: In a Binary Search Tree, an **inorder traversal** (Left-Root-Right) visits nodes in non-decreasing order.
2.  **Iterative Advantage**: By using an iterative inorder traversal with an explicit stack, we can stop the traversal as soon as we reach the $k$-th element. This is more efficient than a full recursive traversal that might continue after $k$ is found.
3.  **Process**:
    - Push nodes while going left.
    - Pop a node (this is the next smallest).
    - Decrement $k$. If $k=0$, we are done.
    - Go right and repeat.

### Complexity Analysis

- **Time Complexity**: **O(h + k)**. We need $O(h)$ time to reach the smallest element, and then $O(k)$ time to find the $k$-th one.
- **Space Complexity**: **O(h)**. The stack stores the nodes along the current branch of the tree.

---

## 2. Second Minimum Node In a Binary Tree

**Problem Statement**: Given a special binary tree where each node has exactly 0 or 2 children, and `root.val = min(root.left.val, root.right.val)`, find the second minimum value in the tree.

### Optimal Python Solution

```python
def findSecondMinimumValue(root: TreeNode) -> int:
    # The root is always the absolute minimum
    min_val = root.val
    res = float('inf')

    def dfs(node):
        nonlocal res
        if not node:
            return

        # If we find a value larger than min_val, it's a candidate for second min
        if min_val < node.val < res:
            res = node.val

        # Optimization: if current node is already >= res, its children
        # cannot be the second minimum (since child.val >= parent.val)
        if node.val == min_val:
            dfs(node.left)
            dfs(node.right)

    dfs(root)
    return res if res != float('inf') else -1
```

### Complexity Analysis

- **Time Complexity**: **O(n)**.
- **Space Complexity**: **O(h)**.

---

## 3. Count of Smaller Numbers After Self

**Problem Statement**: Given an integer array `nums`, return an integer array `counts` where `counts[i]` is the number of smaller elements to the right of `nums[i]`.

### Optimal Python Solution (BST with Rank)

```python
class RankNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None
        self.left_size = 0 # Count of nodes in left subtree

def countSmaller(nums: list[int]) -> list[int]:
    if not nums: return []
    res = [0] * len(nums)

    def insert(root, val, i, current_count):
        if val <= root.val:
            root.left_size += 1
            if not root.left:
                root.left = RankNode(val)
                res[i] = current_count
            else:
                insert(root.left, val, i, current_count)
        else:
            # If we go right, the current value is larger than:
            # 1. The current root
            # 2. All nodes in current root's left subtree
            current_count += root.left_size + 1
            if not root.right:
                root.right = RankNode(val)
                res[i] = current_count
            else:
                insert(root.right, val, i, current_count)

    root = RankNode(nums[-1])
    for i in range(len(nums) - 2, -1, -1):
        insert(root, nums[i], i, 0)
    return res
```

### Explanation

- We build a BST while iterating through `nums` from right to left.
- Each node tracks the size of its left subtree.
- When inserting a new value, if we move to the right child, we know the new value is greater than the root and everything to the root's left. We accumulate these counts.

### Complexity Analysis

- **Time Complexity**: **O(n log n)** on average (O(n²) for sorted input).
- **Space Complexity**: **O(n)**.

---

## 4. Kth Largest Element in a Stream

**Problem Statement**: Design a class to find the kth largest element in a stream.

### Optimal Python Solution (Min-Heap)

```python
import heapq

class KthLargest:
    def __init__(self, k: int, nums: list[int]):
        self.k = k
        self.heap = nums
        heapq.heapify(self.heap)
        # Keep only the k largest elements in a min-heap
        while len(self.heap) > k:
            heapq.heappop(self.heap)

    def add(self, val: int) -> int:
        heapq.heappush(self.heap, val)
        if len(self.heap) > self.k:
            heapq.heappop(self.heap)
        # The smallest element in the min-heap is the kth largest overall
        return self.heap[0]
```

### Complexity Analysis

- **Time Complexity**: **O(log k)** per `add` operation.
- **Space Complexity**: **O(k)**.

---

## 5. Find K-th Smallest Pair Distance

**Problem Statement**: Given an integer array, return the k-th smallest distance among all pairs.

### Optimal Python Solution (Binary Search + Two Pointers)

```python
def smallestDistancePair(nums: list[int], k: int) -> int:
    nums.sort()

    def count_pairs(dist):
        # Count pairs with distance <= dist using two pointers
        count = left = 0
        for right in range(len(nums)):
            while nums[right] - nums[left] > dist:
                left += 1
            count += right - left
        return count

    # Binary search on the answer (distance)
    low, high = 0, nums[-1] - nums[0]
    while low < high:
        mid = (low + high) // 2
        if count_pairs(mid) < k:
            low = mid + 1
        else:
            high = mid
    return low
```

### Complexity Analysis

- **Time Complexity**: **O(n log n + n log W)** where $W$ is the max distance.
- **Space Complexity**: **O(1)**.

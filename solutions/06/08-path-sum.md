# Path Sum Problems

## Practice Problems

### 1. Path Sum
**Difficulty:** Easy
**Concept:** Root-to-leaf existence

```python
from typing import Optional

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def has_path_sum(root: Optional[TreeNode], target_sum: int) -> bool:
    """
    Checks if there's a root-to-leaf path with the given sum.
    Time: O(n)
    Space: O(h)
    """
    if not root:
        return False

    if not root.left and not root.right:
        return root.val == target_sum

    remaining = target_sum - root.val
    return has_path_sum(root.left, remaining) or \
           has_path_sum(root.right, remaining)
```

### 2. Path Sum II
**Difficulty:** Medium
**Concept:** Find all root-to-leaf paths

```python
from typing import List

def path_sum(root: Optional[TreeNode], target_sum: int) -> List[List[int]]:
    """
    Finds all root-to-leaf paths that sum to target_sum.
    Time: O(n^2) - worst case copying paths
    Space: O(h)
    """
    res = []

    def dfs(node, curr_sum, path):
        if not node:
            return

        path.append(node.val)
        if not node.left and not node.right and curr_sum == node.val:
            res.append(list(path))
        else:
            dfs(node.left, curr_sum - node.val, path)
            dfs(node.right, curr_sum - node.val, path)
        path.pop()

    dfs(root, target_sum, [])
    return res
```

### 3. Path Sum III
**Difficulty:** Medium
**Concept:** Downward paths with prefix sum

```python
from collections import defaultdict

def path_sum_iii(root: Optional[TreeNode], target_sum: int) -> int:
    """
    Counts downward paths that sum to target_sum.
    Time: O(n)
    Space: O(h)
    """
    prefix_sums = defaultdict(int)
    prefix_sums[0] = 1

    def dfs(node, curr_sum):
        if not node:
            return 0

        curr_sum += node.val
        count = prefix_sums[curr_sum - target_sum]

        prefix_sums[curr_sum] += 1
        count += dfs(node.left, curr_sum)
        count += dfs(node.right, curr_sum)
        prefix_sums[curr_sum] -= 1

        return count

    return dfs(root, 0)
```

### 4. Binary Tree Maximum Path Sum
**Difficulty:** Hard
**Concept:** Any-to-any path sum

```python
def max_path_sum(root: Optional[TreeNode]) -> int:
    """
    Finds the maximum path sum of any path in the tree.
    Time: O(n)
    Space: O(h)
    """
    res = float('-inf')

    def dfs(node):
        nonlocal res
        if not node:
            return 0

        left_max = max(dfs(node.left), 0)
        right_max = max(dfs(node.right), 0)

        res = max(res, node.val + left_max + right_max)
        return node.val + max(left_max, right_max)

    dfs(root)
    return int(res)
```

### 5. Sum Root to Leaf Numbers
**Difficulty:** Medium
**Concept:** Number construction

```python
def sum_numbers(root: Optional[TreeNode]) -> int:
    """
    Returns the sum of all numbers formed by root-to-leaf paths.
    Time: O(n)
    Space: O(h)
    """
    def dfs(node, curr_num):
        if not node:
            return 0

        curr_num = curr_num * 10 + node.val
        if not node.left and not node.right:
            return curr_num

        return dfs(node.left, curr_num) + dfs(node.right, curr_num)

    return dfs(root, 0)
```

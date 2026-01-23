# Solution: Path Sum Practice Problems

## Problem 1: Path Sum
### Problem Statement
Given the `root` of a binary tree and an integer `targetSum`, return `true` if the tree has a root-to-leaf path such that adding up all the values along the path equals `targetSum`.

A leaf is a node with no children.

### Constraints
- The number of nodes in the tree is in the range `[0, 5000]`.
- `-1000 <= Node.val <= 1000`
- `-1000 <= targetSum <= 1000`

### Example
Input: `root = [5,4,8,11,null,13,4,7,2,null,null,null,1], targetSum = 22`
Output: `true`

### Python Implementation
```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def hasPathSum(root: TreeNode, targetSum: int) -> bool:
    """
    Time Complexity: O(n)
    Space Complexity: O(h)
    """
    if not root:
        return False

    if not root.left and not root.right:
        return targetSum == root.val

    return hasPathSum(root.left, targetSum - root.val) or \
           hasPathSum(root.right, targetSum - root.val)
```

---

## Problem 2: Path Sum II
### Problem Statement
Given the `root` of a binary tree and an integer `targetSum`, return all root-to-leaf paths where the sum of the node values in the path equals `targetSum`. Each path should be returned as a list of the node values, not node references.

### Constraints
- The number of nodes in the tree is in the range `[0, 5000]`.
- `-1000 <= Node.val <= 1000`
- `-1000 <= targetSum <= 1000`

### Example
Input: `root = [5,4,8,11,null,13,4,7,2,null,null,5,1], targetSum = 22`
Output: `[[5,4,11,2],[5,8,4,5]]`

### Python Implementation
```python
def pathSum(root: TreeNode, targetSum: int) -> list[list[int]]:
    """
    Time Complexity: O(n^2) - due to path copying
    Space Complexity: O(n)
    """
    res = []
    def dfs(node, current_sum, path):
        if not node:
            return

        path.append(node.val)
        if not node.left and not node.right and current_sum == node.val:
            res.append(list(path))

        dfs(node.left, current_sum - node.val, path)
        dfs(node.right, current_sum - node.val, path)
        path.pop()

    dfs(root, targetSum, [])
    return res
```

---

## Problem 3: Path Sum III
### Problem Statement
Given the `root` of a binary tree and an integer `targetSum`, return the number of paths where the sum of the values along the path equals `targetSum`.

The path does not need to start or end at the root or a leaf, but it must go downwards (i.e., traveling only from parent nodes to child nodes).

### Constraints
- The number of nodes in the tree is in the range `[0, 1000]`.
- `-10^9 <= Node.val <= 10^9`
- `-1000 <= targetSum <= 1000`

### Example
Input: `root = [10,5,-3,3,2,null,11,3,-2,null,1], targetSum = 8`
Output: `3`

### Python Implementation
```python
from collections import defaultdict

def pathSum(root: TreeNode, targetSum: int) -> int:
    """
    Time Complexity: O(n)
    Space Complexity: O(h)
    """
    prefix_sums = defaultdict(int)
    prefix_sums[0] = 1

    def dfs(node, current_sum):
        if not node:
            return 0

        current_sum += node.val
        count = prefix_sums[current_sum - targetSum]

        prefix_sums[current_sum] += 1
        count += dfs(node.left, current_sum)
        count += dfs(node.right, current_sum)
        prefix_sums[current_sum] -= 1

        return count

    return dfs(root, 0)
```

---

## Problem 4: Binary Tree Maximum Path Sum
### Problem Statement
A path in a binary tree is a sequence of nodes where each pair of adjacent nodes in the sequence has an edge connecting them. A node can only appear in the sequence at most once. Note that the path does not need to pass through the root.

The path sum of a path is the sum of the node's values in the path.

Given the `root` of a binary tree, return the maximum path sum of any non-empty path.

### Constraints
- The number of nodes in the tree is in the range `[1, 3 * 10^4]`.
- `-1000 <= Node.val <= 1000`

### Example
Input: `root = [-10,9,20,null,null,15,7]`
Output: `42`

### Python Implementation
```python
def maxPathSum(root: TreeNode) -> int:
    """
    Time Complexity: O(n)
    Space Complexity: O(h)
    """
    max_sum = -float('inf')

    def dfs(node):
        nonlocal max_sum
        if not node:
            return 0

        left = max(dfs(node.left), 0)
        right = max(dfs(node.right), 0)

        max_sum = max(max_sum, node.val + left + right)

        return node.val + max(left, right)

    dfs(root)
    return max_sum
```

---

## Problem 5: Sum Root to Leaf Numbers
### Problem Statement
You are given the `root` of a binary tree containing digits from `0` to `9` only.

Each root-to-leaf path in the tree represents a number.
- For example, the root-to-leaf path `1 -> 2 -> 3` represents the number `123`.

Return the total sum of all root-to-leaf numbers. Test cases are generated so that the answer will fit in a 32-bit integer.

### Constraints
- The number of nodes in the tree is in the range `[1, 1000]`.
- `0 <= Node.val <= 9`
- The depth of the tree will not exceed `10`.

### Example
Input: `root = [1,2,3]`
Output: `25` (12 + 13)

### Python Implementation
```python
def sumNumbers(root: TreeNode) -> int:
    """
    Time Complexity: O(n)
    Space Complexity: O(h)
    """
    def dfs(node, current_num):
        if not node:
            return 0

        current_num = current_num * 10 + node.val
        if not node.left and not node.right:
            return current_num

        return dfs(node.left, current_num) + dfs(node.right, current_num)

    return dfs(root, 0)
```

---

## Problem 6: Binary Tree Paths
### Problem Statement
Given the `root` of a binary tree, return all root-to-leaf paths in any order.

### Constraints
- The number of nodes in the tree is in the range `[1, 100]`.
- `-100 <= Node.val <= 100`

### Example
Input: `root = [1,2,3,null,5]`
Output: `["1->2->5","1->3"]`

### Python Implementation
```python
def binaryTreePaths(root: TreeNode) -> list[str]:
    """
    Time Complexity: O(n^2) - due to string creation
    Space Complexity: O(n)
    """
    res = []
    def dfs(node, path):
        if not node:
            return

        path += str(node.val)
        if not node.left and not node.right:
            res.append(path)
        else:
            path += "->"
            dfs(node.left, path)
            dfs(node.right, path)

    dfs(root, "")
    return res
```

---

## Problem 7: Longest Univalue Path
### Problem Statement
Given the `root` of a binary tree, return the length of the longest path, where each node in the path has the same value. This path may or may not pass through the root.

The length of the path between two nodes is represented by the number of edges between them.

### Constraints
- The number of nodes in the tree is in the range `[0, 10^4]`.
- `-1000 <= Node.val <= 1000`
- The depth of the tree will not exceed `1000`.

### Example
Input: `root = [5,4,5,1,1,null,5]`
Output: `2`

### Python Implementation
```python
def longestUnivaluePath(root: TreeNode) -> int:
    """
    Time Complexity: O(n)
    Space Complexity: O(h)
    """
    max_len = 0

    def dfs(node):
        nonlocal max_len
        if not node:
            return 0

        left = dfs(node.left)
        right = dfs(node.right)

        left_path = left + 1 if node.left and node.left.val == node.val else 0
        right_path = right + 1 if node.right and node.right.val == node.val else 0

        max_len = max(max_len, left_path + right_path)

        return max(left_path, right_path)

    dfs(root)
    return max_len
```

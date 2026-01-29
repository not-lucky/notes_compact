# Path Sum Solutions

## 1. Path Sum

**Problem Statement**: Given the `root` of a binary tree and an integer `targetSum`, return `true` if the tree has a **root-to-leaf** path such that adding up all the values along the path equals `targetSum`.

### Examples & Edge Cases

- **Example 1**: `root = [5,4,8,11,None,13,4,7,2,None,None,None,1], targetSum = 22` → Output: `true` (5+4+11+2=22)
- **Edge Case - Empty Tree**: `root = None` → Output: `false`
- **Edge Case - Single Node**: `root = [1], targetSum = 1` → Output: `true`
- **Edge Case - Negative Values**: Path sums can decrease.

### Optimal Python Solution

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def hasPathSum(root: TreeNode, targetSum: int) -> bool:
    if not root:
        return False

    # Check if we are at a leaf node
    if not root.left and not root.right:
        return root.val == targetSum

    # Recurse down with the remaining sum needed
    remaining = targetSum - root.val
    return hasPathSum(root.left, remaining) or hasPathSum(root.right, remaining)
```

### Explanation

1.  **Base Case**: If the tree is empty, no path exists.
2.  **Leaf Logic**: A path is only valid if it ends at a leaf (a node with no children). We check if the remaining required sum equals the leaf's value.
3.  **Recursive Step**: We subtract the current node's value from the `targetSum` and check if either the left or right subtree can fulfill the rest.

### Complexity Analysis

- **Time Complexity**: **O(n)**. In the worst case, we visit all nodes.
- **Space Complexity**: **O(h)**. The recursion depth depends on the height of the tree.

---

## 2. Path Sum II

**Problem Statement**: Given the `root` of a binary tree and an integer `targetSum`, return all **root-to-leaf** paths where the sum of the node values in the path equals `targetSum`.

### Optimal Python Solution

```python
def pathSum(root: TreeNode, targetSum: int) -> list[list[int]]:
    result = []

    def backtrack(node, remaining, path):
        if not node:
            return

        # Choose the current node
        path.append(node.val)

        # Check if it's a leaf and the sum matches
        if not node.left and not node.right and remaining == node.val:
            result.append(list(path)) # Append a copy of the path

        # Explore children
        backtrack(node.left, remaining - node.val, path)
        backtrack(node.right, remaining - node.val, path)

        # Un-choose (backtrack)
        path.pop()

    backtrack(root, targetSum, [])
    return result
```

### Explanation

1.  **DFS with State**: We carry the current `path` and the `remaining` sum through the recursion.
2.  **Backtracking**: To avoid creating a new list at every node (which would be $O(n^2)$ space), we use a single list and `pop()` the element after the recursive calls return.
3.  **Copying**: We only copy the list (`list(path)`) when we find a valid solution.

### Complexity Analysis

- **Time Complexity**: **O(n²)**. We visit $n$ nodes, and in the worst case (a complete tree), there could be $O(n)$ paths, each requiring $O(n)$ time to copy.
- **Space Complexity**: **O(n)**. The space used by the path list and the recursion stack.

---

## 3. Path Sum III

**Problem Statement**: Given the `root` of a binary tree and an integer `targetSum`, return the number of paths where the sum of the values along the path equals `targetSum`. The path does not need to start or end at the root or a leaf, but it must go downwards.

### Optimal Python Solution

```python
from collections import defaultdict

def pathSumIII(root: TreeNode, targetSum: int) -> int:
    # map of prefix_sum -> count
    prefix_sums = defaultdict(int)
    prefix_sums[0] = 1 # Base case: a path starting from root has a prefix sum of 0 before it
    count = 0

    def dfs(node, current_sum):
        nonlocal count
        if not node:
            return

        current_sum += node.val

        # If current_sum - targetSum exists as a prefix, we found a path
        # (current_sum - prefix) == targetSum => prefix == (current_sum - targetSum)
        count += prefix_sums[current_sum - targetSum]

        # Add current_sum to the map for descendants
        prefix_sums[current_sum] += 1

        dfs(node.left, current_sum)
        dfs(node.right, current_sum)

        # Backtrack: remove current_sum so it doesn't affect other branches
        prefix_sums[current_sum] -= 1

    dfs(root, 0)
    return count
```

### Explanation

1.  **Prefix Sum Technique**: This is the tree version of "Subarray Sum Equals K".
2.  **Logic**: As we go down a path, we keep a running `current_sum`. If at some point `current_sum - targetSum` equals a prefix sum we saw earlier in the path, the segment between that ancestor and the current node sums to `targetSum`.
3.  **Backtracking**: Since we only want "downward" paths (ancestor to descendant), we must remove the current prefix sum from the map before returning to the parent, so nodes in the other sibling's subtree don't use it.

### Complexity Analysis

- **Time Complexity**: **O(n)**. We visit each node once and perform $O(1)$ hash map lookups.
- **Space Complexity**: **O(h)**. The hash map stores at most $h$ prefix sums (one for each ancestor).

---

## 4. Binary Tree Maximum Path Sum

**Problem Statement**: Find the maximum path sum of any non-empty path in a binary tree. A path can start and end at any node.

### Optimal Python Solution

```python
def maxPathSum(root: TreeNode) -> int:
    max_total = float('-inf')

    def get_gain(node):
        nonlocal max_total
        if not node:
            return 0

        # Max gain from subtrees. If gain is negative, we ignore the subtree (max(..., 0))
        left_gain = max(get_gain(node.left), 0)
        right_gain = max(get_gain(node.right), 0)

        # Potential max path passes through current node and "turns" here
        max_total = max(max_total, node.val + left_gain + right_gain)

        # Return the max gain this node can contribute to its parent
        # Can only pick ONE child to continue the path upward
        return node.val + max(left_gain, right_gain)

    get_gain(root)
    return max_total
```

### Explanation

1.  **Two Scenarios**: At any node, we consider:
    - **Scenario A**: The path "turns" at this node (Left Child -> Current -> Right Child). We update our global maximum with this sum.
    - **Scenario B**: The path continues upward to the parent. In this case, we can only include the current node and ONE of its children (whichever is larger).
2.  **Negative Pruning**: If a subtree has a negative total gain, it's better to not include it at all (`max(..., 0)`).

### Complexity Analysis

- **Time Complexity**: **O(n)**.
- **Space Complexity**: **O(h)**.

---

## 5. Sum Root to Leaf Numbers

**Problem Statement**: Each root-to-leaf path represents a number (e.g., path `1->2->3` is `123`). Return the sum of all such numbers.

### Optimal Python Solution

```python
def sumNumbers(root: TreeNode) -> int:
    def dfs(node, current_val):
        if not node:
            return 0

        current_val = current_val * 10 + node.val

        # If it's a leaf, return the accumulated value
        if not node.left and not node.right:
            return current_val

        # Otherwise, return the sum of numbers formed by subtrees
        return dfs(node.left, current_val) + dfs(node.right, current_val)

    return dfs(root, 0)
```

### Complexity Analysis

- **Time Complexity**: **O(n)**.
- **Space Complexity**: **O(h)**.

---

## 6. Binary Tree Paths

**Problem Statement**: Return all root-to-leaf paths as strings in the format `"1->2->3"`.

### Optimal Python Solution

```python
def binaryTreePaths(root: TreeNode) -> list[str]:
    result = []

    def dfs(node, path):
        if not node:
            return

        # Add current node to path string
        new_path = path + str(node.val)

        if not node.left and not node.right:
            result.append(new_path)
        else:
            new_path += "->"
            dfs(node.left, new_path)
            dfs(node.right, new_path)

    dfs(root, "")
    return result
```

### Complexity Analysis

- **Time Complexity**: **O(n²)**. Each string concatenation and path storage takes $O(L)$ where $L$ is path length.
- **Space Complexity**: **O(n²)**.

---

## 7. Longest Univalue Path

**Problem Statement**: Find the length of the longest path where each node in the path has the same value. The length is defined by the number of edges.

### Optimal Python Solution

```python
def longestUnivaluePath(root: TreeNode) -> int:
    ans = 0

    def dfs(node):
        nonlocal ans
        if not node:
            return 0

        left_len = dfs(node.left)
        right_len = dfs(node.right)

        left_arrow = right_arrow = 0

        # If child exists and has the same value, extend the path
        if node.left and node.left.val == node.val:
            left_arrow = left_len + 1
        if node.right and node.right.val == node.val:
            right_arrow = right_len + 1

        # Update global maximum (combining both sides)
        ans = max(ans, left_arrow + right_arrow)

        # Return the longest single-sided path to the parent
        return max(left_arrow, right_arrow)

    dfs(root)
    return ans
```

### Complexity Analysis

- **Time Complexity**: **O(n)**.
- **Space Complexity**: **O(h)**.

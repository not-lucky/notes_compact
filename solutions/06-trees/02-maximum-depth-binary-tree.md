# Maximum Depth of Binary Tree

## Problem Statement

Given the root of a binary tree, return its maximum depth.

Maximum depth is the number of nodes along the longest path from root to the farthest leaf.

**Example:**
```
Input:      3
          /   \
         9    20
             /  \
            15   7
Output: 3
```

## Building Intuition

### Why This Works

The maximum depth of a tree is defined recursively: it's 1 (for the current node) plus the maximum depth of its deepest subtree. An empty tree has depth 0 (base case). This recursive definition directly translates to code: `return 1 + max(depth(left), depth(right))`.

The beauty of this approach is that we don't need to track paths or maintain state - each subtree independently reports its depth, and we combine them at each level. Information flows up from leaves (which report depth 1) through internal nodes (which add 1 and take the max) to the root.

BFS offers an alternative intuition: depth is just the number of levels. Process the tree level by level, counting how many levels exist before the queue empties.

### How to Discover This

For tree measurement problems (depth, size, sum), think recursively: "How does the answer for the whole tree relate to answers for the subtrees?" Often it's a simple combination: max (for depth/height), plus (for size/sum), and/or (for boolean properties).

### Pattern Recognition

This is the **Recursive Tree Aggregation** pattern. Compute a value for each subtree and combine them at the parent. It works for depth, node count, sum, diameter, balance checking, and many other tree metrics.

## When NOT to Use

- **When you only need to know if depth exceeds a threshold**: Early termination can avoid exploring the entire tree. Check depth during traversal and stop when threshold is exceeded.
- **When tracking the path to the deepest node**: This approach only returns the count; you'd need to track the actual path separately.
- **When the tree is represented as an array (complete binary tree)**: For a complete binary tree in array form, depth is simply floor(log2(n)) + 1 - no traversal needed.
- **When depth is frequently queried on a static tree**: Cache the depth values instead of recomputing; or augment each node with its depth during construction.

## Approach

### Recursive DFS
Depth of tree = 1 + max(depth of left subtree, depth of right subtree)

### Iterative BFS
Count number of levels using level-order traversal.

### Iterative DFS
Use stack with depth tracking.

## Implementation

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def max_depth(root: TreeNode) -> int:
    """
    Find maximum depth using recursive DFS.

    Time: O(n) - visit each node
    Space: O(h) - recursion stack
    """
    if not root:
        return 0

    left_depth = max_depth(root.left)
    right_depth = max_depth(root.right)

    return 1 + max(left_depth, right_depth)


def max_depth_bfs(root: TreeNode) -> int:
    """
    Find maximum depth using BFS (level count).

    Time: O(n)
    Space: O(n) - queue holds entire level
    """
    if not root:
        return 0

    from collections import deque
    queue = deque([root])
    depth = 0

    while queue:
        depth += 1
        level_size = len(queue)

        for _ in range(level_size):
            node = queue.popleft()
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)

    return depth


def max_depth_iterative_dfs(root: TreeNode) -> int:
    """
    Find maximum depth using iterative DFS with stack.

    Time: O(n)
    Space: O(h)
    """
    if not root:
        return 0

    stack = [(root, 1)]
    max_d = 0

    while stack:
        node, depth = stack.pop()
        max_d = max(max_d, depth)

        if node.left:
            stack.append((node.left, depth + 1))
        if node.right:
            stack.append((node.right, depth + 1))

    return max_d
```

## Complexity Analysis

| Method | Time | Space | Notes |
|--------|------|-------|-------|
| Recursive | O(n) | O(h) | h = height |
| BFS | O(n) | O(w) | w = max width |
| Iterative DFS | O(n) | O(h) | Stack depth |

## Edge Cases

1. **Empty tree**: Return 0
2. **Single node**: Return 1
3. **Left-skewed tree**: Depth = n (linear)
4. **Balanced tree**: Depth = log(n)
5. **Full binary tree**: Consistent depth on all paths

## Common Mistakes

1. **Returning 0 for single node**: Should return 1
2. **Confusing depth vs height**: Same concept, different naming
3. **Not handling empty tree**: Check for null root

## Variations

### Minimum Depth of Binary Tree
```python
def min_depth(root: TreeNode) -> int:
    """
    Minimum depth is path to nearest LEAF node.
    Not just nearest null child!

    Time: O(n)
    Space: O(h)
    """
    if not root:
        return 0

    # If one child is null, we must go to the other
    if not root.left:
        return 1 + min_depth(root.right)
    if not root.right:
        return 1 + min_depth(root.left)

    return 1 + min(min_depth(root.left), min_depth(root.right))


def min_depth_bfs(root: TreeNode) -> int:
    """
    BFS approach - returns as soon as leaf is found.
    More efficient for trees with shallow leaves.
    """
    if not root:
        return 0

    from collections import deque
    queue = deque([(root, 1)])

    while queue:
        node, depth = queue.popleft()

        # Found a leaf
        if not node.left and not node.right:
            return depth

        if node.left:
            queue.append((node.left, depth + 1))
        if node.right:
            queue.append((node.right, depth + 1))

    return 0
```

### Balanced Binary Tree
```python
def is_balanced(root: TreeNode) -> bool:
    """
    Check if tree is height-balanced.
    Height-balanced: depths of two subtrees differ by at most 1.

    Time: O(n)
    Space: O(h)
    """
    def check_height(node: TreeNode) -> int:
        """Return height if balanced, -1 if not balanced."""
        if not node:
            return 0

        left_height = check_height(node.left)
        if left_height == -1:
            return -1

        right_height = check_height(node.right)
        if right_height == -1:
            return -1

        if abs(left_height - right_height) > 1:
            return -1

        return 1 + max(left_height, right_height)

    return check_height(root) != -1
```

### Diameter of Binary Tree
```python
def diameter_of_binary_tree(root: TreeNode) -> int:
    """
    Diameter = longest path between any two nodes.
    Path length = number of edges.

    Time: O(n)
    Space: O(h)
    """
    diameter = 0

    def depth(node: TreeNode) -> int:
        nonlocal diameter
        if not node:
            return 0

        left = depth(node.left)
        right = depth(node.right)

        # Update diameter: path through this node
        diameter = max(diameter, left + right)

        return 1 + max(left, right)

    depth(root)
    return diameter
```

### Maximum Depth of N-ary Tree
```python
def max_depth_nary(root: 'Node') -> int:
    """
    N-ary tree: each node can have any number of children.

    Time: O(n)
    Space: O(h)
    """
    if not root:
        return 0

    if not root.children:
        return 1

    return 1 + max(max_depth_nary(child) for child in root.children)
```

## Related Problems

- **Minimum Depth of Binary Tree** - Path to nearest leaf
- **Balanced Binary Tree** - Check height balance
- **Diameter of Binary Tree** - Longest path
- **Count Complete Tree Nodes** - Uses height for optimization
- **Deepest Leaves Sum** - Sum of nodes at max depth

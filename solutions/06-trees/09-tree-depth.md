# Tree Depth and Balance Solutions

## 1. Maximum Depth of Binary Tree
**Problem Statement**: Given the `root` of a binary tree, return its maximum depth.

### Examples & Edge Cases
- **Example 1**: `root = [3,9,20,None,None,15,7]` → Output: `3`
- **Edge Case - Empty Tree**: `root = None` → Output: `0`
- **Edge Case - Skewed Tree**: `root = [1,2,3]` → Output: `3`

### Optimal Python Solution
```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def maxDepth(root: TreeNode) -> int:
    # Base Case: empty tree has depth 0
    if not root:
        return 0

    # Depth is 1 (current node) + max depth of subtrees
    return 1 + max(maxDepth(root.left), maxDepth(root.right))
```

### Explanation
1.  **Recursive Intuition**: The depth of a tree is determined by its longest path.
2.  **Logic**: We ask for the height of the left branch and the right branch. We take the larger of the two and add `1` for the current node.
3.  **Bottom-up**: The calculation happens as the recursion "unwinds" from the leaf nodes back to the root.

### Complexity Analysis
- **Time Complexity**: **O(n)**. Every node is visited once.
- **Space Complexity**: **O(h)**. The height of the tree determines the recursion depth.

---

## 2. Minimum Depth of Binary Tree
**Problem Statement**: Find the minimum depth of a binary tree. The minimum depth is the number of nodes along the shortest path from the root node down to the nearest leaf node.

### Examples & Edge Cases
- **Example 1**: `root = [3,9,20,None,None,15,7]` → Output: `2` (Root 3 to Leaf 9)
- **Example 2**: `root = [2,None,3,None,4,None,5,None,6]` → Output: `5`
- **Edge Case - One child missing**: If a node has only a right child, the "nearest leaf" is NOT the missing left child. You must continue to the right.

### Optimal Python Solution
```python
from collections import deque

def minDepth(root: TreeNode) -> int:
    if not root:
        return 0

    # BFS is optimal for finding the "nearest" anything
    queue = deque([(root, 1)])

    while queue:
        node, depth = queue.popleft()

        # The first leaf we encounter is guaranteed to be at the minimum depth
        if not node.left and not node.right:
            return depth

        if node.left:
            queue.append((node.left, depth + 1))
        if node.right:
            queue.append((node.right, depth + 1))

    return 0
```

### Explanation
1.  **BFS vs DFS**: While DFS ($1 + \min(\text{left}, \text{right})$) works, BFS is usually better for "shortest path" problems.
2.  **Early Exit**: In BFS, we process level-by-level. As soon as we find a node that is a **leaf** (both children are `None`), we return its depth immediately. This avoids traversing the entire tree if a shallow leaf exists.

### Complexity Analysis
- **Time Complexity**: **O(n)**. In the worst case (skewed tree), we visit all nodes.
- **Space Complexity**: **O(w)**. We store at most one level of nodes in the queue.

---

## 3. Balanced Binary Tree
**Problem Statement**: Given a binary tree, determine if it is **height-balanced** (depth of two subtrees of every node never differs by more than 1).

### Optimal Python Solution
```python
def isBalanced(root: TreeNode) -> bool:
    def check_height(node):
        if not node:
            return 0

        left_h = check_height(node.left)
        if left_h == -1: return -1 # Propagate imbalance found in left

        right_h = check_height(node.right)
        if right_h == -1: return -1 # Propagate imbalance found in right

        # If current node is unbalanced, return -1
        if abs(left_h - right_h) > 1:
            return -1

        # Otherwise return actual height
        return 1 + max(left_h, right_h)

    return check_height(root) != -1
```

### Explanation
1.  **Bottom-Up Efficiency**: Instead of calling a `height` function for every node ($O(n^2)$), we calculate height while checking balance ($O(n)$).
2.  **Sentinel Value**: We return the height of the subtree if it is balanced. If we detect an imbalance anywhere, we return `-1`.
3.  **Short-circuiting**: If a child returns `-1`, the parent immediately returns `-1` without further calculation.

### Complexity Analysis
- **Time Complexity**: **O(n)**. Single post-order traversal.
- **Space Complexity**: **O(h)**.

---

## 4. Count Complete Tree Nodes
**Problem Statement**: Given the `root` of a **complete** binary tree, return the number of nodes in the tree.

### Optimal Python Solution
```python
def countNodes(root: TreeNode) -> int:
    if not root:
        return 0

    def get_height(node):
        h = 0
        while node:
            h += 1
            node = node.left
        return h

    left_h = get_height(root.left)
    right_h = get_height(root.right)

    if left_h == right_h:
        # Left subtree is perfect, right is complete
        return (1 << left_h) + countNodes(root.right)
    else:
        # Right subtree is perfect (height-1), left is complete
        return (1 << right_h) + countNodes(root.left)
```

### Complexity Analysis
- **Time Complexity**: **O(log² n)**.
- **Space Complexity**: **O(log n)**.

---

## 5. Check Completeness of a Binary Tree
**Problem Statement**: Check if a binary tree is complete (all levels full except potentially the last, which is filled left to right).

### Optimal Python Solution
```python
def isCompleteTree(root: TreeNode) -> bool:
    if not root:
        return True

    queue = deque([root])
    seen_null = False

    while queue:
        node = queue.popleft()

        if not node:
            seen_null = True
            continue

        # If we see a non-null node after seeing a null, it's not complete
        if seen_null:
            return False

        # Add children (including None) to the queue
        queue.append(node.left)
        queue.append(node.right)

    return True
```

### Explanation
1.  **BFS Null Marker**: We use BFS to traverse the tree.
2.  **The Invariant**: In a complete binary tree, once we encounter a `null` child during a level-order traversal, every subsequent node popped from the queue MUST also be `null`.
3.  **Check**: If we pop a valid node after `seen_null` became `True`, the tree is not complete.

### Complexity Analysis
- **Time Complexity**: **O(n)**.
- **Space Complexity**: **O(n)**.

---

## 6. Maximum Level Sum of a Binary Tree
**Problem Statement**: Given the `root` of a binary tree, the level of its root is `1`, the level of its children is `2`, and so on. Return the **smallest level** `x` such that the sum of all the values of nodes at level `x` is **maximal**.

### Optimal Python Solution
```python
def maxLevelSum(root: TreeNode) -> int:
    max_sum = float('-inf')
    max_level = 0
    curr_level = 0

    queue = deque([root])

    while queue:
        curr_level += 1
        level_sum = 0
        for _ in range(len(queue)):
            node = queue.popleft()
            level_sum += node.val
            if node.left: queue.append(node.left)
            if node.right: queue.append(node.right)

        if level_sum > max_sum:
            max_sum = level_sum
            max_level = curr_level

    return max_level
```

### Complexity Analysis
- **Time Complexity**: **O(n)**.
- **Space Complexity**: **O(w)**.

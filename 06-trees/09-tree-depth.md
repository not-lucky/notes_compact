# Tree Depth and Balance

> **Prerequisites:** [01-tree-basics](./01-tree-basics.md), [02-tree-traversals](./02-tree-traversals.md)

## Building Intuition

**The Tree Measurement Mental Model**: Think of measuring a tree in your backyard:

- **Depth** = How far down from the top? (Root is at the top in CS trees!)
- **Height** = How tall from bottom to top? (Max depth of any leaf)

```
Real tree (grows up):     CS tree (grows down):
      🌳                        1 (root, depth=0)
       |                       / \
       |                      2   3 (depth=1)
       |                     /
       |                    4 (depth=2, leaf)
    ground
                          Height = 2 (longest path from root to leaf)
```

**The recursive insight for max depth**:
Height of a tree = 1 + max(height of left, height of right)

```
      1
     / \
    2   3
   /
  4

height(4) = 0 (leaf, or 1 in some definitions)
height(2) = 1 + max(height(4), 0) = 1 + 1 = 2
height(3) = 0 (leaf)
height(1) = 1 + max(height(2), height(3)) = 1 + max(2, 0) = 3
```

**Balanced vs Unbalanced - why it matters**:

```
Balanced (good):          Unbalanced (bad):
      1                        1
     / \                        \
    2   3                        2
   / \ / \                        \
  4  5 6  7                        3
                                    \
Height = 2                           4
Operations = $\mathcal{O}(\log N)$
                                Height = 3 (approaching $N$)
                                Operations = $\mathcal{O}(N)$ worst case
```

A balanced tree guarantees $\mathcal{O}(\log N)$ operations because height is logarithmic in node count.

---

## When NOT to Use

**Depth/height calculations are overkill when:**

- Only need to check if tree is empty → Simple null check
- Need exact level of specific node → Track depth during search
- Tree is always balanced by design (heap) → Height is $\mathcal{O}(\log N)$ by definition

**Common mistake scenarios:**

- Confusing depth (from root) with height (from leaves)
- Off-by-one errors (0-indexed vs 1-indexed depth)
- Computing height twice per node → $\mathcal{O}(N^2)$ instead of $\Theta(N)$

**The balanced tree trap**:

```
Definition varies! Common definitions:
1. AVL: |height(left) - height(right)| ≤ 1 for ALL nodes
2. Red-Black: No path is more than 2x any other
3. "Approximately balanced": Height is $\mathcal{O}(\log N)$

Clarify with interviewer which definition to use!
```

**When specialized algorithms are better:**
| Problem | Better Than Recursive |
|---------|----------------------|
| Just max depth | BFS (level count) is equivalent |
| Is balanced? | Combined height + balance check |
| Min depth to leaf | BFS finds it faster (early termination) |
| Depth of specific node | DFS with target, not full traversal |

---

## Interview Context

Depth and balance problems are important because:

1. **Foundational concepts**: Understanding height/depth is prerequisite for many tree problems
2. **Common interview questions**: Max depth, min depth, balanced check are frequent
3. **Building blocks**: These calculations are used in more complex problems
4. **Time complexity implications**: Tree height determines performance of many operations

Very common at all FANG+ companies as warm-up or component problems.

---

## Core Concepts: Depth vs Height

```
         1          ← depth=0, height=3
        / \
       2   3        ← depth=1
      / \
     4   5          ← depth=2
    /
   6                ← depth=3 (leaf)

- Depth of node: distance from root to node (root has depth 0)
- Height of node: distance from node to deepest leaf (leaf has height 0)
- Height of tree: height of root = max depth of any node = 3
```

**Note**: Some definitions use 1-based counting (root at depth 1). Clarify in interviews!

---

## Maximum Depth (Height)

### Recursive Solution

```python
from typing import Optional

class TreeNode:
    def __init__(self, val: int = 0, left: Optional['TreeNode'] = None, right: Optional['TreeNode'] = None):
        self.val = val
        self.left = left
        self.right = right

def max_depth(root: Optional[TreeNode]) -> int:
    r"""
    Maximum depth of binary tree.

    LeetCode 104: Maximum Depth of Binary Tree

    Time: $\Theta(N)$ - visit every node exactly once
    Space: $\mathcal{O}(H)$ - recursion stack, where $H$ is tree height.
           Worst case $\mathcal{O}(N)$ for skewed tree, best/average case $\mathcal{O}(\log N)$ for balanced.
    """
    if not root:
        return 0

    return 1 + max(max_depth(root.left), max_depth(root.right))
```

### Iterative BFS

```python
from collections import deque
from typing import Optional

def max_depth_bfs(root: Optional[TreeNode]) -> int:
    r"""
    Max depth using level-order traversal (BFS).

    Time: $\Theta(N)$ - visit every node exactly once
    Space: $\mathcal{O}(W)$ - where $W$ is the maximum width of the tree.
           Worst case $\mathcal{O}(N)$ for a perfect binary tree, best case $\mathcal{O}(1)$ for a skewed tree.
    """
    if not root:
        return 0

    depth = 0
    queue = deque([root])

    while queue:
        depth += 1
        for _ in range(len(queue)):
            node = queue.popleft()
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)

    return depth
```

### Iterative DFS

```python
from typing import Optional

def max_depth_dfs_iterative(root: Optional[TreeNode]) -> int:
    r"""
    Max depth using DFS with explicit stack.

    Time: $\Theta(N)$ - visit every node exactly once
    Space: $\mathcal{O}(H)$ - explicit stack space, up to $\mathcal{O}(N)$ for skewed tree
    """
    if not root:
        return 0

    max_d = 0
    stack = [(root, 1)]

    while stack:
        node, depth = stack.pop()
        max_d = max(max_d, depth)

        if node.right:
            stack.append((node.right, depth + 1))
        if node.left:
            stack.append((node.left, depth + 1))

    return max_d
```

---

## Minimum Depth

Minimum depth is the shortest path from root to a **leaf** node.

### Key Difference from Max Depth

```
     1
    /
   2
  /
 3

Max depth = 3
Min depth = 3 (not 1! because right subtree has no leaf)

For min depth, we only count paths to LEAVES, not null children.
```

### Recursive Solution

```python
from typing import Optional

def min_depth(root: Optional[TreeNode]) -> int:
    r"""
    Minimum depth (shortest path to leaf).

    LeetCode 111: Minimum Depth of Binary Tree

    Time: $\mathcal{O}(N)$ - worst case visit every node
    Space: $\mathcal{O}(H)$ - recursion stack space. Worst case $\mathcal{O}(N)$ for skewed tree,
           best/average $\mathcal{O}(\log N)$ for balanced.
    """
    if not root:
        return 0

    # If no left child, only consider right subtree
    if not root.left:
        return 1 + min_depth(root.right)

    # If no right child, only consider left subtree
    if not root.right:
        return 1 + min_depth(root.left)

    # Both children exist
    return 1 + min(min_depth(root.left), min_depth(root.right))
```

### BFS (More Efficient for Balanced Trees)

```python
from collections import deque
from typing import Optional

def min_depth_bfs(root: Optional[TreeNode]) -> int:
    r"""
    Min depth using BFS - returns as soon as leaf found.

    More efficient when min depth << max depth.

    Time: $\mathcal{O}(N)$ worst case (all nodes at last level),
          often much less (stops at first leaf).
    Space: $\mathcal{O}(W)$ - max width of tree queue.
           Worst case $\mathcal{O}(N)$ for a perfect tree.
    """
    if not root:
        return 0

    queue = deque([(root, 1)])

    while queue:
        node, depth = queue.popleft()

        # First leaf we find is at minimum depth
        if not node.left and not node.right:
            return depth

        if node.left:
            queue.append((node.left, depth + 1))
        if node.right:
            queue.append((node.right, depth + 1))

    return 0
```

---

## Balanced Binary Tree

A binary tree is balanced if the height difference between left and right subtrees of every node is at most 1.

### Naive Approach: $\mathcal{O}(N^2)$

```python
from typing import Optional

def is_balanced_naive(root: Optional[TreeNode]) -> bool:
    r"""
    Check if tree is balanced (naive approach).

    Time: $\mathcal{O}(N^2)$ - height calculated repeatedly.
          For a skewed tree, height is $\mathcal{O}(N)$ nodes $\times$ $\mathcal{O}(N)$ depth computations.
    Space: $\mathcal{O}(H)$ - recursion stack. Worst case $\mathcal{O}(N)$ for skewed.
    """
    if not root:
        return True

    def height(node: Optional[TreeNode]) -> int:
        if not node:
            return 0
        return 1 + max(height(node.left), height(node.right))

    left_height = height(root.left)
    right_height = height(root.right)

    return (abs(left_height - right_height) <= 1 and
            is_balanced_naive(root.left) and
            is_balanced_naive(root.right))
```

### Optimized Approach: $\mathcal{O}(N)$

```python
from typing import Optional

def is_balanced(root: Optional[TreeNode]) -> bool:
    r"""
    Check if tree is balanced (optimized).

    LeetCode 110: Balanced Binary Tree

    Return height while checking balance. Use -1 to indicate unbalanced.

    Time: $\Theta(N)$ - single pass, each node visited once.
    Space: $\mathcal{O}(H)$ - recursion stack. Worst case $\mathcal{O}(N)$ for skewed.
    """
    def check_height(node: Optional[TreeNode]) -> int:
        if not node:
            return 0

        left_height = check_height(node.left)
        if left_height == -1:
            return -1  # Left subtree unbalanced

        right_height = check_height(node.right)
        if right_height == -1:
            return -1  # Right subtree unbalanced

        if abs(left_height - right_height) > 1:
            return -1  # Current node unbalanced

        return 1 + max(left_height, right_height)

    return check_height(root) != -1
```

### Alternative: Return Tuple

```python
from typing import Optional, Tuple

def is_balanced_tuple(root: Optional[TreeNode]) -> bool:
    r"""
    Return (is_balanced, height) tuple.

    Time: $\Theta(N)$ - single pass.
    Space: $\mathcal{O}(H)$ - recursion stack.
    """
    def dfs(node: Optional[TreeNode]) -> Tuple[bool, int]:
        if not node:
            return True, 0

        left_balanced, left_height = dfs(node.left)
        right_balanced, right_height = dfs(node.right)

        balanced = (left_balanced and
                   right_balanced and
                   abs(left_height - right_height) <= 1)

        height = 1 + max(left_height, right_height)

        return balanced, height

    return dfs(root)[0]
```

---

## Count Nodes at Depth K

```python
from typing import Optional, List

def nodes_at_depth(root: Optional[TreeNode], k: int) -> List[int]:
    r"""
    Return all nodes at depth k.

    Time: $\mathcal{O}(N)$ - worst case if target level $k$ is near leaf,
          we explore $\mathcal{O}(N)$ nodes.
    Space: $\mathcal{O}(N)$ - to hold results up to max width
           and $\mathcal{O}(H)$ for recursion stack.
    """
    result = []

    def dfs(node: Optional[TreeNode], depth: int) -> None:
        if not node:
            return

        if depth == k:
            result.append(node.val)
            return  # No need to go deeper

        dfs(node.left, depth + 1)
        dfs(node.right, depth + 1)

    dfs(root, 0)
    return result
```

---

## Depth of Deepest Odd Level Leaf

```python
from typing import Optional

def deepest_odd_level_leaf(root: Optional[TreeNode]) -> int:
    r"""
    Find depth of deepest leaf at an odd level.

    Levels are 1-indexed (root is level 1).

    Time: $\Theta(N)$ - visit every node once.
    Space: $\mathcal{O}(H)$ - recursion stack.
    """
    max_odd_depth = [0]

    def dfs(node: Optional[TreeNode], depth: int) -> None:
        if not node:
            return

        if not node.left and not node.right:  # Leaf
            if depth % 2 == 1:  # Odd level
                max_odd_depth[0] = max(max_odd_depth[0], depth)

        dfs(node.left, depth + 1)
        dfs(node.right, depth + 1)

    dfs(root, 1)
    return max_odd_depth[0]
```

---

## Complete Binary Tree Check

```python
from collections import deque
from typing import Optional

def is_complete_tree(root: Optional[TreeNode]) -> bool:
    r"""
    Check if tree is complete (all levels full except last,
    which is filled left to right).

    LeetCode 958: Check Completeness of a Binary Tree

    Time: $\Theta(N)$ - visit every node
    Space: $\mathcal{O}(W)$ - queue holds at most one level, where max width $W \approx N/2$
    """
    if not root:
        return True

    queue = deque([root])
    seen_null = False

    while queue:
        node = queue.popleft()

        if not node:
            seen_null = True
        else:
            # If we've seen a null, no more nodes should appear
            if seen_null:
                return False
            queue.append(node.left)
            queue.append(node.right)

    return True
```

---

## Count Complete Tree Nodes ($\mathcal{O}(\log^2 N)$)

```python
from typing import Optional

def count_nodes(root: Optional[TreeNode]) -> int:
    r"""
    Count nodes in complete binary tree.

    LeetCode 222: Count Complete Tree Nodes

    For complete tree, can use binary search on last level.

    Time: $\mathcal{O}(\log^2 N)$ - $\log N$ levels, $\log N$ to check each via get_height
    Space: $\mathcal{O}(\log N)$ - recursion stack depth matches tree height $\log N$
    """
    if not root:
        return 0

    def get_height(node: Optional[TreeNode]) -> int:
        height = 0
        while node:
            height += 1
            node = node.left
        return height

    left_height = get_height(root.left)
    right_height = get_height(root.right)

    if left_height == right_height:
        # Left subtree is perfect, recurse on right
        return (1 << left_height) - 1 + 1 + count_nodes(root.right)
    else:
        # Right subtree is perfect (one level shorter), recurse on left
        return (1 << right_height) - 1 + 1 + count_nodes(root.left)
```

---

## Complexity Analysis

| Problem             | Time     | Space    | Notes                       |
| ------------------- | -------- | -------- | --------------------------- |
| Max depth           | $\Theta(N)$ | $\mathcal{O}(H)$ | Visit all nodes             |
| Min depth           | $\mathcal{O}(N)$ | $\mathcal{O}(H)$ or $\mathcal{O}(W)$ | BFS can be faster (early exit) |
| Is balanced         | $\Theta(N)$ | $\mathcal{O}(H)$ | Single pass with early exit via -1 |
| Complete tree nodes | $\mathcal{O}(\log^2 N)$ | $\mathcal{O}(\log N)$ | Exploit tree properties     |

---

## Edge Cases

```python
# 1. Empty tree
root = None
# → max_depth = 0, min_depth = 0, is_balanced = True

# 2. Single node
root = TreeNode(1)
# → max_depth = 1, min_depth = 1, is_balanced = True

# 3. Skewed tree (like linked list)
#     1
#      \
#       2
#        \
#         3
# → max_depth = 3, min_depth = 3, is_balanced = False

# 4. Perfect binary tree
# → max_depth = min_depth = $\mathcal{O}(\log(N+1))$
```

---

## Interview Tips

1. **Clarify indexing**: Is depth 0-indexed or 1-indexed?
2. **Min depth trap**: Only count paths to leaves, not null children
3. **BFS for min depth**: Often more efficient (stops early)
4. **Balanced optimization**: Combine height calculation with balance check
5. **Complete tree**: Special algorithms exist for counting

---

## Practice Problems

| #   | Problem                           | Difficulty | Key Concept               |
| --- | --------------------------------- | ---------- | ------------------------- |
| 1   | Maximum Depth of Binary Tree      | Easy       | Basic recursion           |
| 2   | Minimum Depth of Binary Tree      | Easy       | Handle single child       |
| 3   | Balanced Binary Tree              | Easy       | Height + balance check    |
| 4   | Count Complete Tree Nodes         | Medium     | Exploit complete property |
| 5   | Check Completeness of Binary Tree | Medium     | BFS null check            |
| 6   | Maximum Level Sum of Binary Tree  | Medium     | Level-order + sum         |

---

## Key Takeaways

1. **Max depth = 1 + max(left, right)**: Simple recursion
2. **Min depth needs leaf check**: Don't count null children
3. **BFS for min depth**: Stops at first leaf found
4. **Balanced in $\Theta(N)$**: Use -1 sentinel or tuple return
5. **Complete tree tricks**: Binary search on last level

---

## Next: [10-tree-diameter.md](./10-tree-diameter.md)

Learn to calculate the diameter of a binary tree.

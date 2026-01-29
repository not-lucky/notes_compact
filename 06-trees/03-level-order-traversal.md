# Level-Order Traversal (BFS)

> **Prerequisites:** [02-tree-traversals](./02-tree-traversals.md), [05-stacks-queues](../05-stacks-queues/README.md)

## Building Intuition

**The Burning Building Mental Model**: Imagine a building where each floor is a level of the tree. Firefighters (BFS) clear floor by floor:

```
Floor 0:     🧑‍🚒    [1]          Clear first floor
Floor 1:    🧑‍🚒 🧑‍🚒   [2, 3]       Then second floor
Floor 2:   🧑‍🚒🧑‍🚒🧑‍🚒 [4, 5, 6]     Then third floor...

        1           ← Level 0
       / \
      2   3         ← Level 1
     / \   \
    4   5   6       ← Level 2
```

**Why we use a queue (FIFO)**:

- Enqueue all children of current level
- When we dequeue, we get them in order by level
- Stack (LIFO) would give DFS, not BFS

```
Queue visualization:
Start: [1]
After processing 1: [2, 3]     (1's children added)
After processing 2: [3, 4, 5]  (2's children added to end)
After processing 3: [4, 5, 6]  (3's children added to end)
...and so on, level by level!
```

**The "level size" trick**:
To process level by level (not just node by node), snapshot the queue size at start of each level:

```python
while queue:
    level_size = len(queue)  # All nodes currently in queue are at same level
    for _ in range(level_size):
        node = queue.popleft()
        # Process node, add children to queue
```

**DFS vs BFS for trees**:

| Property       | DFS                              | BFS                                |
| -------------- | -------------------------------- | ---------------------------------- |
| Data structure | Stack / Recursion                | Queue                              |
| Order          | Depth-first (down before across) | Breadth-first (across before down) |
| Space          | O(h) height                      | O(w) max width                     |
| Good for       | Path problems, tree shape        | Level problems, shortest path      |

---

## When NOT to Use

**Level-order traversal is overkill when:**

- Just need to visit all nodes in any order → DFS is simpler
- Processing subtrees independently → DFS maps to recursion naturally
- Tree is very wide → Queue can be huge (O(n/2) at widest level)

**Level-order is essential when:**

- Need level-by-level output
- Finding shortest path (in unweighted tree)
- Right-side view, left-side view, max per level
- Connecting nodes at same level

**Common mistake scenarios:**

- Using list instead of deque → O(n) pop from front!
- Forgetting to track level boundaries → Wrong level grouping
- Processing children before siblings → That's DFS, not BFS

**When DFS is better:**
| Problem Type | Use This |
|--------------|----------|
| "Collect all root-to-leaf paths" | DFS |
| "Calculate subtree values" | DFS (postorder) |
| "Serialize tree" | DFS (preorder) |
| "Return values by level" | BFS |
| "Find min depth" | BFS (early termination) |

**The space complexity insight**:

```
Wide tree (worst for BFS):     Skinny tree (worst for DFS):
         1                              1
     /   |   \                           \
    2    3    4                           2
   /|\ /|\ /|\                             \
  5 6 7 8 9 ...                             3

Queue: O(n/2) at bottom level   Stack: O(n) for chain
BFS space: O(width) = O(n)      DFS space: O(height) = O(n)
```

---

## Interview Context

Level-order traversal is essential because:

1. **BFS on trees**: Foundation for all breadth-first tree algorithms
2. **Level-based processing**: Many problems require processing by levels
3. **Common variations**: Zigzag, bottom-up, right-side view all use this pattern
4. **Queue mastery**: Demonstrates understanding of queue data structure

Interviewers use level-order problems to test your understanding of BFS and level-based thinking.

---

## Core Concept: Level-Order Traversal

Process nodes level by level, left to right, using a queue.

```
       1          Level 0: [1]
      / \
     2   3        Level 1: [2, 3]
    / \   \
   4   5   6      Level 2: [4, 5, 6]

Level-order: [1, 2, 3, 4, 5, 6]
By levels: [[1], [2, 3], [4, 5, 6]]
```

---

## Basic Level-Order (Flat List)

```python
from collections import deque

def level_order_flat(root: TreeNode) -> list[int]:
    """
    Basic level-order traversal returning flat list.

    Time: O(n) - visit every node
    Space: O(w) - where w is maximum width of tree
    """
    if not root:
        return []

    result = []
    queue = deque([root])

    while queue:
        node = queue.popleft()
        result.append(node.val)

        if node.left:
            queue.append(node.left)
        if node.right:
            queue.append(node.right)

    return result
```

---

## Level-Order by Levels (Most Common)

```python
def level_order(root: TreeNode) -> list[list[int]]:
    """
    Level-order traversal returning nodes grouped by level.

    LeetCode 102: Binary Tree Level Order Traversal

    Time: O(n)
    Space: O(w) - maximum width
    """
    if not root:
        return []

    result = []
    queue = deque([root])

    while queue:
        level_size = len(queue)  # Nodes at current level
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

### Visual Walkthrough

```
       1
      / \
     2   3
    / \
   4   5

Initial: queue = [1], result = []

Iteration 1: level_size = 1
  - Pop 1, add children 2, 3
  - level = [1], queue = [2, 3]
  - result = [[1]]

Iteration 2: level_size = 2
  - Pop 2, add children 4, 5
  - Pop 3, no children
  - level = [2, 3], queue = [4, 5]
  - result = [[1], [2, 3]]

Iteration 3: level_size = 2
  - Pop 4, no children
  - Pop 5, no children
  - level = [4, 5], queue = []
  - result = [[1], [2, 3], [4, 5]]

Done!
```

---

## Common Variations

### 1. Bottom-Up Level Order

```python
def level_order_bottom(root: TreeNode) -> list[list[int]]:
    """
    Bottom-up level-order (leaf level first).

    LeetCode 107: Binary Tree Level Order Traversal II

    Time: O(n)
    Space: O(w)
    """
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

    return result[::-1]  # Reverse at the end
```

### 2. Zigzag Level Order

```python
def zigzag_level_order(root: TreeNode) -> list[list[int]]:
    """
    Zigzag (alternating left-right, right-left).

    LeetCode 103: Binary Tree Zigzag Level Order Traversal

    Time: O(n)
    Space: O(w)
    """
    if not root:
        return []

    result = []
    queue = deque([root])
    left_to_right = True

    while queue:
        level_size = len(queue)
        level = deque()  # Use deque for efficient append on both ends

        for _ in range(level_size):
            node = queue.popleft()

            if left_to_right:
                level.append(node.val)
            else:
                level.appendleft(node.val)

            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)

        result.append(list(level))
        left_to_right = not left_to_right

    return result
```

### 3. Right Side View

```python
def right_side_view(root: TreeNode) -> list[int]:
    """
    Return rightmost node at each level.

    LeetCode 199: Binary Tree Right Side View

    Time: O(n)
    Space: O(w)
    """
    if not root:
        return []

    result = []
    queue = deque([root])

    while queue:
        level_size = len(queue)

        for i in range(level_size):
            node = queue.popleft()

            # Last node in level is rightmost
            if i == level_size - 1:
                result.append(node.val)

            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)

    return result
```

### 4. Average of Levels

```python
def average_of_levels(root: TreeNode) -> list[float]:
    """
    Average value of nodes at each level.

    LeetCode 637: Average of Levels in Binary Tree

    Time: O(n)
    Space: O(w)
    """
    if not root:
        return []

    result = []
    queue = deque([root])

    while queue:
        level_size = len(queue)
        level_sum = 0

        for _ in range(level_size):
            node = queue.popleft()
            level_sum += node.val

            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)

        result.append(level_sum / level_size)

    return result
```

### 5. Maximum Width of Binary Tree

```python
def width_of_binary_tree(root: TreeNode) -> int:
    """
    Maximum width (including nulls between nodes).

    LeetCode 662: Maximum Width of Binary Tree

    Track positions: left child = 2*i, right child = 2*i+1

    Time: O(n)
    Space: O(w)
    """
    if not root:
        return 0

    max_width = 0
    queue = deque([(root, 0)])  # (node, position)

    while queue:
        level_size = len(queue)
        _, first_pos = queue[0]

        for _ in range(level_size):
            node, pos = queue.popleft()

            if node.left:
                queue.append((node.left, 2 * pos))
            if node.right:
                queue.append((node.right, 2 * pos + 1))

        # Width = last position - first position + 1
        # pos holds the last processed position from this level
        max_width = max(max_width, pos - first_pos + 1)

    return max_width
```

### 6. Level with Minimum Sum

```python
def min_sum_level(root: TreeNode) -> int:
    """
    Return level with minimum sum (1-indexed).

    Time: O(n)
    Space: O(w)
    """
    if not root:
        return 0

    queue = deque([root])
    min_sum = float('inf')
    min_level = 0
    current_level = 0

    while queue:
        level_size = len(queue)
        level_sum = 0
        current_level += 1

        for _ in range(level_size):
            node = queue.popleft()
            level_sum += node.val

            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)

        if level_sum < min_sum:
            min_sum = level_sum
            min_level = current_level

    return min_level
```

---

## DFS Alternative for Level Order

```python
def level_order_dfs(root: TreeNode) -> list[list[int]]:
    """
    Level-order using DFS (recursive).

    Pass depth to track which level we're at.

    Time: O(n)
    Space: O(h) - recursion stack
    """
    result = []

    def dfs(node, depth):
        if not node:
            return

        # Extend result if we're at a new level
        if depth >= len(result):
            result.append([])

        result[depth].append(node.val)
        dfs(node.left, depth + 1)
        dfs(node.right, depth + 1)

    dfs(root, 0)
    return result
```

---

## Complexity Analysis

| Operation      | Time | Space | Notes           |
| -------------- | ---- | ----- | --------------- |
| Level-order    | O(n) | O(w)  | w = max width   |
| All variations | O(n) | O(w)  | Same complexity |

Width considerations:

- Perfect tree: width = n/2 at bottom level
- Skewed tree: width = 1
- Balanced tree: width ≈ n/2

---

## Edge Cases

```python
# 1. Empty tree
root = None
# → Return []

# 2. Single node
root = TreeNode(1)
# → Return [[1]]

# 3. Skewed tree (all right)
# 1
#  \
#   2
#    \
#     3
# → [[1], [2], [3]]

# 4. Complete binary tree
#      1
#    /   \
#   2     3
#  / \   /
# 4   5 6
# → [[1], [2, 3], [4, 5, 6]]
```

---

## Interview Tips

1. **Know the template**: level_size = len(queue), then process that many nodes
2. **Queue, not stack**: BFS uses queue (deque in Python)
3. **Track level info**: Many variations need level number or position
4. **Consider DFS alternative**: Sometimes DFS with depth tracking is simpler
5. **Space is width, not height**: Unlike DFS, BFS uses O(width) space

---

## Practice Problems

| #   | Problem                                  | Difficulty | Key Concept           |
| --- | ---------------------------------------- | ---------- | --------------------- |
| 1   | Binary Tree Level Order Traversal        | Medium     | Basic level-order     |
| 2   | Binary Tree Level Order Traversal II     | Medium     | Bottom-up             |
| 3   | Binary Tree Zigzag Level Order Traversal | Medium     | Alternating direction |
| 4   | Binary Tree Right Side View              | Medium     | Last node per level   |
| 5   | Average of Levels in Binary Tree         | Easy       | Level statistics      |
| 6   | Maximum Width of Binary Tree             | Medium     | Position tracking     |
| 7   | Find Largest Value in Each Tree Row      | Medium     | Level max             |
| 8   | Populating Next Right Pointers           | Medium     | Connect level nodes   |

---

## Key Takeaways

1. **Queue-based BFS**: Use deque for O(1) popleft
2. **Level size tracking**: Process len(queue) nodes per iteration
3. **Many variations**: Zigzag, bottom-up, right view all use same pattern
4. **Space = width**: O(w) where w can be up to n/2
5. **DFS alternative exists**: Track depth for recursive approach

---

## Next: [04-bst-operations.md](./04-bst-operations.md)

Learn BST search, insert, and delete operations.

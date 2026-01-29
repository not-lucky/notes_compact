# Level-Order Traversal (BFS) Solutions

## 1. Binary Tree Level Order Traversal

**Problem Statement**: Given the root of a binary tree, return the level order traversal of its nodes' values. (i.e., from left to right, level by level).

### Examples & Edge Cases

- **Example 1**: `root = [3,9,20,None,None,15,7]` → Output: `[[3],[9,20],[15,7]]`
- **Example 2**: `root = [1]` → Output: `[[1]]`
- **Edge Case - Empty Tree**: `root = []` → Output: `[]`
- **Edge Case - Skewed Tree**: `root = [1,2,3]` → Output: `[[1],[2],[3]]`

### Optimal Python Solution

```python
from collections import deque

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def levelOrder(root: TreeNode) -> list[list[int]]:
    if not root:
        return []

    result = []
    queue = deque([root])

    while queue:
        level_size = len(queue)
        current_level = []

        # Process all nodes at the current level
        for _ in range(level_size):
            node = queue.popleft()
            current_level.append(node.val)

            # Add children for the next level
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)

        result.append(current_level)

    return result
```

### Explanation

1.  **Queue for BFS**: We use a `deque` (double-ended queue) to store nodes. BFS naturally processes nodes in the order they are discovered.
2.  **Level Boundaries**: The crucial part is `level_size = len(queue)`. By capturing the size at the start of the `while` loop, we know exactly how many nodes belong to the _current_ level.
3.  **Iteration**: We pop exactly `level_size` nodes, add their values to a list, and push their children into the queue. These children will form the _next_ level.
4.  **Result**: Each `current_level` list is appended to the final result.

### Complexity Analysis

- **Time Complexity**: **O(n)**. Each node is enqueued and dequeued exactly once.
- **Space Complexity**: **O(w)**. The queue stores at most the maximum width of the tree. In a perfect binary tree, this is approximately $n/2$.

---

## 2. Binary Tree Level Order Traversal II

**Problem Statement**: Given the root of a binary tree, return the _bottom-up_ level order traversal of its nodes' values. (i.e., from left to right, level by level from leaf to root).

### Examples & Edge Cases

- **Example 1**: `root = [3,9,20,None,None,15,7]` → Output: `[[15,7],[9,20],[3]]`
- **Edge Case - Single Node**: `root = [1]` → Output: `[[1]]`

### Optimal Python Solution

```python
def levelOrderBottom(root: TreeNode) -> list[list[int]]:
    if not root:
        return []

    result = []
    queue = deque([root])

    while queue:
        level_size = len(queue)
        current_level = []

        for _ in range(level_size):
            node = queue.popleft()
            current_level.append(node.val)
            if node.left: queue.append(node.left)
            if node.right: queue.append(node.right)

        result.append(current_level)

    # Reverse the final result to get bottom-up order
    return result[::-1]
```

### Explanation

1.  **Standard BFS**: We perform the exact same level-order traversal as the previous problem.
2.  **Reversal**: After collecting all levels in a top-down manner, we reverse the list.
3.  **Alternative**: One could also use `result.insert(0, current_level)`, but in Python, inserting at index 0 of a list is $O(k)$ where $k$ is the current size of the list, making it less efficient than a final reversal.

### Complexity Analysis

- **Time Complexity**: **O(n)**. $O(n)$ for traversal and $O(\text{height})$ for the list reversal.
- **Space Complexity**: **O(w)**. Space depends on the maximum width of the tree.

---

## 3. Binary Tree Zigzag Level Order Traversal

**Problem Statement**: Given the root of a binary tree, return the zigzag level order traversal of its nodes' values. (i.e., from left to right, then right to left for the next level and alternate between).

### Examples & Edge Cases

- **Example 1**: `root = [3,9,20,None,None,15,7]` → Output: `[[3],[20,9],[15,7]]`
- **Edge Case - Single Node**: `[[1]]`

### Optimal Python Solution

```python
def zigzagLevelOrder(root: TreeNode) -> list[list[int]]:
    if not root:
        return []

    result = []
    queue = deque([root])
    left_to_right = True

    while queue:
        level_size = len(queue)
        # Use deque for current_level to allow O(1) append on both sides
        current_level = deque()

        for _ in range(level_size):
            node = queue.popleft()

            if left_to_right:
                current_level.append(node.val)
            else:
                current_level.appendleft(node.val)

            if node.left: queue.append(node.left)
            if node.right: queue.append(node.right)

        result.append(list(current_level))
        # Flip the direction for the next level
        left_to_right = not left_to_right

    return result
```

### Explanation

1.  **Direction Toggle**: We maintain a boolean `left_to_right`.
2.  **Efficient Appending**: We use a `deque` for the `current_level`. If we are going left-to-right, we append to the end. If right-to-left, we `appendleft`.
3.  **Consistency**: The nodes are still added to the main `queue` in the same order (left then right). Only the _storage_ of their values in the `current_level` list changes.

### Complexity Analysis

- **Time Complexity**: **O(n)**. Each node is processed once.
- **Space Complexity**: **O(w)**. Maximum width of the tree.

---

## 4. Binary Tree Right Side View

**Problem Statement**: Given the root of a binary tree, imagine yourself standing on the right side of it, return the values of the nodes you can see ordered from top to bottom.

### Examples & Edge Cases

- **Example 1**: `root = [1,2,3,None,5,None,4]` → Output: `[1,3,4]`
- **Edge Case - Left-heavy Tree**: Even if a node is on the "left", if it's the only node at that depth, it will be visible from the right.

### Optimal Python Solution

```python
def rightSideView(root: TreeNode) -> list[int]:
    if not root:
        return []

    result = []
    queue = deque([root])

    while queue:
        level_size = len(queue)

        for i in range(level_size):
            node = queue.popleft()

            # If it's the last node of the level, it's the rightmost one
            if i == level_size - 1:
                result.append(node.val)

            if node.left: queue.append(node.left)
            if node.right: queue.append(node.right)

    return result
```

### Explanation

1.  **BFS Property**: In each level iteration, the nodes are processed from left to right.
2.  **Visibility**: The last node processed in any given level is the one furthest to the right at that depth.
3.  **Check**: We simply check if the current iteration index `i` equals `level_size - 1`.

### Complexity Analysis

- **Time Complexity**: **O(n)**.
- **Space Complexity**: **O(w)**.

---

## 5. Average of Levels in Binary Tree

**Problem Statement**: Given the root of a binary tree, return the average value of the nodes on each level in the form of an array.

### Optimal Python Solution

```python
def averageOfLevels(root: TreeNode) -> list[float]:
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
            if node.left: queue.append(node.left)
            if node.right: queue.append(node.right)

        result.append(level_sum / level_size)

    return result
```

### Complexity Analysis

- **Time Complexity**: **O(n)**.
- **Space Complexity**: **O(w)**.

---

## 6. Maximum Width of Binary Tree

**Problem Statement**: Given the root of a binary tree, return the maximum width of the given tree. The maximum width of a tree is the maximum width among all levels. The width of one level is defined as the number of nodes between the end-nodes (the leftmost and rightmost non-null nodes), where the null nodes between the end-nodes are also counted into the length calculation.

### Optimal Python Solution

```python
def widthOfBinaryTree(root: TreeNode) -> int:
    if not root:
        return 0

    max_width = 0
    # Store tuples of (node, index)
    queue = deque([(root, 0)])

    while queue:
        level_size = len(queue)
        _, first_index = queue[0]
        _, last_index = queue[-1]

        max_width = max(max_width, last_index - first_index + 1)

        for _ in range(level_size):
            node, index = queue.popleft()

            # Heap-like indexing: left = 2*i, right = 2*i + 1
            if node.left:
                queue.append((node.left, 2 * index))
            if node.right:
                queue.append((node.right, 2 * index + 1))

    return max_width
```

### Explanation

1.  **Index Tracking**: We treat the tree like a heap array. If a node is at index `i`, its children are at `2i` and `2i + 1`.
2.  **Width Calculation**: At each level, the width is the difference between the index of the last node and the first node plus one.
3.  **Efficiency**: By tracking indices, we don't need to actually store `None` nodes in the queue.

### Complexity Analysis

- **Time Complexity**: **O(n)**. Each node is visited once.
- **Space Complexity**: **O(w)**. Maximum width of the tree.

---

## 7. Find Largest Value in Each Tree Row

**Problem Statement**: Given the root of a binary tree, return an array of the largest value in each row of the tree (0-indexed).

### Optimal Python Solution

```python
def largestValues(root: TreeNode) -> list[int]:
    if not root:
        return []

    result = []
    queue = deque([root])

    while queue:
        level_size = len(queue)
        max_val = float('-inf')

        for _ in range(level_size):
            node = queue.popleft()
            max_val = max(max_val, node.val)
            if node.left: queue.append(node.left)
            if node.right: queue.append(node.right)

        result.append(max_val)

    return result
```

### Complexity Analysis

- **Time Complexity**: **O(n)**.
- **Space Complexity**: **O(w)**.

---

## 8. Populating Next Right Pointers

**Problem Statement**: You are given a **perfect binary tree** where all leaves are on the same level, and every parent has two children. Populate each next pointer to point to its next right node. If there is no next right node, the next pointer should be set to `NULL`.

### Optimal Python Solution

```python
class Node:
    def __init__(self, val: int = 0, left: 'Node' = None, right: 'Node' = None, next: 'Node' = None):
        self.val = val
        self.left = left
        self.right = right
        self.next = next

def connect(root: 'Node') -> 'Node':
    if not root:
        return None

    # We use the previous level as a "linked list" to connect the current level
    curr_level_start = root

    while curr_level_start.left:
        curr = curr_level_start
        while curr:
            # Connect the two children of the same parent
            curr.left.next = curr.right

            # Connect the right child of one parent to the left child of the next parent
            if curr.next:
                curr.right.next = curr.next.left

            curr = curr.next

        # Move to the start of the next level
        curr_level_start = curr_level_start.left

    return root
```

### Explanation

1.  **Level-by-Level without Queue**: Since the tree is perfect and we have `next` pointers, we can use the already-connected level above to connect the level below.
2.  **Horizontal Traversal**: For a parent `curr`, we link `curr.left.next = curr.right`.
3.  **Bridge Gap**: We link `curr.right.next = curr.next.left` if a `curr.next` exists.
4.  **Space Efficiency**: This achieves $O(1)$ extra space (excluding recursion if done recursively).

### Complexity Analysis

- **Time Complexity**: **O(n)**. Every node is visited.
- **Space Complexity**: **O(1)**. No queue used.

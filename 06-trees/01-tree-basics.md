# Tree Basics

> **Prerequisites:** [01-complexity-analysis](../01-complexity-analysis/README.md)

## Building Intuition

**The Organizational Chart Mental Model**: Every company has a CEO (root), with VPs reporting to them (children), managers reporting to VPs, and so on. A tree captures this hierarchical structure perfectly:

```
         CEO (root)
        /    \
      VP1    VP2
      / \      \
   Mgr1 Mgr2  Mgr3 (leaves = no reports)
```

**Why trees appear everywhere in CS**:

- **File systems**: Folders containing folders containing files
- **HTML/DOM**: `<body>` contains `<div>` contains `<p>` contains text
- **Database indexes**: B-trees organize sorted data for fast lookup
- **Syntax trees**: Code is parsed into tree structure

**The recursion insight**: A tree is defined recursively - every subtree is itself a tree. This means most tree algorithms have elegant recursive solutions:

```python
def count(node):
    if not node:
        return 0
    return 1 + count(node.left) + count(node.right)
```

**Height vs Depth - remember the difference**:

- **Depth** = how far DOWN from root (root has depth 0)
- **Height** = how far UP from leaves (leaf has height 0, tree height = root's height)

```
         1     ← depth=0, height=2
        / \
       2   3   ← depth=1, height=1
      /
     4         ← depth=2, height=0 (leaf)
```

**Why height matters for complexity**: Most tree operations are $\mathcal{O}(h)$ where $h = \text{height}$:

- Balanced tree: $h = \log_2(n) \implies$ operations are $\mathcal{O}(\log n)$
- Skewed tree (like a linked list): $h = n \implies$ operations degrade to $\mathcal{O}(n)$

---

## When NOT to Use

**Don't use a tree when:**

- **Data is not hierarchical** $\rightarrow$ Use array, hash map, or graph instead
- **Frequent insertions in sorted order** $\rightarrow$ Use balanced tree or skip list
- **Need $\Theta(1)$ access by index** $\rightarrow$ Use array
- **Need $\Theta(1)$ amortized access by key** $\rightarrow$ Use hash map

**Trees are overkill when:**

- Simple linear data with no hierarchy $\rightarrow$ Use array/list
- Small data sets (< 100 elements) $\rightarrow$ Linear search is fine
- You only need LIFO/FIFO access $\rightarrow$ Use stack/queue

**Common mistake scenarios:**

- Using tree when hash map suffices for key-value storage
- Building a basic Binary Search Tree (BST) from sorted array (creates skewed tree) $\rightarrow$ Use middle element as root instead
- Forgetting that unbalanced trees lose their efficiency guarantees

**Binary tree vs other structures:**

| Use Case | Best Structure |
|----------|----------------|
| Hierarchical data | Tree |
| Key-value lookup | Hash Map |
| Sorted data with range queries | BST / B-tree |
| Priority access | Heap |
| Graph traversal | Graph (not tree) |

---

## Interview Context

Trees are fundamental because:

1. **Hierarchical structure**: Natural representation for nested data (file systems, DOM, org charts)
2. **Recursive nature**: Tree operations map perfectly to recursive thinking
3. **Foundation for BST/Heap**: Understanding tree basics is prerequisite for advanced structures
4. **Interview frequency**: Almost every FANG+ loop includes at least one tree problem

Interviewers use tree basics to test your understanding of pointer manipulation, recursion, and hierarchical problem-solving. **Always articulate the call stack space complexity in recursive solutions, bounded by the maximum tree depth.**

---

## Core Concept: What is a Binary Tree?

A binary tree is a hierarchical data structure where each node has at most two children, referred to as **left** and **right**.

```
Binary Tree Structure:

         1 [0x100]  ← root
        / \
 [0x140] 2   3 [0x180]  ← children of 1
       / \   \
[0x1C0] 4   5 [0x200]  6 [0x240] ← leaves: 4, 5, 6
```

### Key Terminology

| Term        | Definition                                    |
| ----------- | --------------------------------------------- |
| **Root**    | Topmost node (no parent)                      |
| **Node**    | Element containing value and child pointers   |
| **Edge**    | Connection between parent and child           |
| **Leaf**    | Node with no children                         |
| **Parent**  | Node with child node(s)                       |
| **Child**   | Node directly connected below a parent        |
| **Sibling** | Nodes sharing the same parent                 |
| **Subtree** | Tree formed by a node and all its descendants |
| **Depth**   | Distance from root to node (root has depth 0) |
| **Height**  | Maximum depth of any node in tree             |
| **Level**   | All nodes at the same depth                   |

---

## Tree Properties

### Height vs Depth

```
         1          depth=0, height=2
        / \
       2   3        depth=1
      /
     4              depth=2 (leaf)

Tree height = 2 (longest path from root to leaf)
```

### Tree Types

| Type                     | Property                                                          |
| ------------------------ | ----------------------------------------------------------------- |
| **Full Binary Tree**     | Every node has 0 or 2 children                                    |
| **Complete Binary Tree** | All levels filled except possibly last, which fills left to right |
| **Perfect Binary Tree**  | All internal nodes have 2 children, all leaves at same level      |
| **Balanced Binary Tree** | Height difference between subtrees is at most 1                   |
| **Degenerate/Skewed**    | Each node has only one child (like a linked list)                 |

```
Full:           Complete:        Perfect:         Skewed:
    1               1                1               1
   / \             / \              / \               \
  2   3           2   3            2   3               2
 / \             /                / \ / \               \
4   5           4                4  5 6  7               3
```

---

## Node Implementation

### Standard TreeNode (LeetCode Style)

```python
from typing import Optional

class TreeNode:
    r"""
    Standard binary tree node used in LeetCode.

    Attributes:
        val: The value stored in this node
        left: Reference to left child (or None)
        right: Reference to right child (or None)
    """
    def __init__(
        self,
        val: int = 0,
        left: Optional['TreeNode'] = None,
        right: Optional['TreeNode'] = None
    ):
        self.val = val
        self.left = left
        self.right = right


# Creating a tree:
#       1
#      / \
#     2   3
#    /
#   4

if __name__ == "__main__":
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.right = TreeNode(3)
    root.left.left = TreeNode(4)
```

### TreeNode with Parent Pointer

```python
from typing import Optional

class TreeNodeWithParent:
    r"""Binary tree node with parent pointer (used in some advanced problems)."""
    def __init__(self, val: int = 0):
        self.val = val
        self.left: Optional['TreeNodeWithParent'] = None
        self.right: Optional['TreeNodeWithParent'] = None
        self.parent: Optional['TreeNodeWithParent'] = None  # Useful for tracking ancestry
```

---

## Basic Tree Operations

### Count Nodes

```python
from typing import Optional

class TreeNode:
    def __init__(self, val: int = 0, left: Optional['TreeNode'] = None, right: Optional['TreeNode'] = None):
        self.val = val
        self.left = left
        self.right = right

def count_nodes(root: Optional[TreeNode]) -> int:
    r"""
    Count total nodes in tree.

    Time Complexity: $\Theta(N)$ where N is the number of nodes (must visit every node).
    Space Complexity: $\mathcal{O}(H)$ where H is the height of the tree, representing the recursion stack depth.
    Worst case skewed tree: $\mathcal{O}(N)$ space. Best case balanced tree: $\mathcal{O}(\log N)$ space.
    """
    if not root:
        return 0
    return 1 + count_nodes(root.left) + count_nodes(root.right)
```

### Check if Leaf

```python
from typing import Optional

def is_leaf(node: Optional['TreeNode']) -> bool:
    r"""
    Check if node is a leaf (no children).

    Time Complexity: $\Theta(1)$
    Space Complexity: $\Theta(1)$
    """
    return node is not None and node.left is None and node.right is None
```

### Count Leaves

```python
from typing import Optional

def count_leaves(root: Optional['TreeNode']) -> int:
    r"""
    Count leaf nodes in tree.

    Time Complexity: $\Theta(N)$ to visit every node.
    Space Complexity: $\mathcal{O}(H)$ for the recursive call stack.
    """
    if not root:
        return 0
    if not root.left and not root.right:
        return 1
    return count_leaves(root.left) + count_leaves(root.right)
```

### Find Maximum Value

```python
from typing import Optional

def find_max(root: Optional['TreeNode']) -> float:
    r"""
    Find maximum value in a binary tree.

    Time Complexity: $\Theta(N)$ - must check every node because it's not a BST.
    Space Complexity: $\mathcal{O}(H)$ for the call stack.
    """
    if not root:
        return float('-inf')

    left_max = find_max(root.left)
    right_max = find_max(root.right)

    return max(float(root.val), left_max, right_max)
```

### Search for Value

```python
from typing import Optional

def search(root: Optional['TreeNode'], target: int) -> bool:
    r"""
    Search for value in binary tree.

    Time Complexity: $\mathcal{O}(N)$ - may need to search all nodes in the worst case.
    Space Complexity: $\mathcal{O}(H)$ for the recursive call stack.
    """
    if not root:
        return False
    if root.val == target:
        return True
    return search(root.left, target) or search(root.right, target)
```

---

## Tree Construction from List

### Build from Level-Order List (LeetCode Style)

```python
from collections import deque
from typing import Optional

class TreeNode:
    def __init__(self, val: int = 0, left: Optional['TreeNode'] = None, right: Optional['TreeNode'] = None):
        self.val = val
        self.left = left
        self.right = right

def build_tree(values: list[Optional[int]]) -> Optional[TreeNode]:
    r"""
    Build tree from level-order list (LeetCode format).
    None represents missing nodes.

    Example: [1, 2, 3, None, 4] creates:
          1
         / \
        2   3
         \
          4

    Time Complexity: $\Theta(N)$ where N is the length of the list.
    Space Complexity: $\mathcal{O}(W)$ where W is the maximum width of the tree (for the queue).
    For a perfect binary tree, the last level has roughly N/2 nodes, so $\mathcal{O}(N)$ space.
    """
    if not values or values[0] is None:
        return None

    root = TreeNode(values[0])
    queue: deque[TreeNode] = deque([root])
    i = 1

    while queue and i < len(values):
        node = queue.popleft()

        # Left child
        if i < len(values) and values[i] is not None:
            # We know it's not None from the check above, but type hint requires cast or ignore
            # if we are being strict. Assuming values[i] is an int here.
            node.left = TreeNode(values[i]) # type: ignore
            queue.append(node.left)
        i += 1

        # Right child
        if i < len(values) and values[i] is not None:
            node.right = TreeNode(values[i]) # type: ignore
            queue.append(node.right)
        i += 1

    return root


if __name__ == "__main__":
    # Usage
    constructed_root = build_tree([1, 2, 3, None, 4, 5, 6])
    assert constructed_root and constructed_root.val == 1
    assert constructed_root.left and constructed_root.left.val == 2
    assert constructed_root.right and constructed_root.right.val == 3
    assert constructed_root.left.right and constructed_root.left.right.val == 4
    assert constructed_root.right.left and constructed_root.right.left.val == 5
    assert constructed_root.right.right and constructed_root.right.right.val == 6
```

---

## Complexity Analysis

| Operation        | Time   | Space | Notes                 |
| ---------------- | ------ | ----- | --------------------- |
| Count nodes      | $\Theta(N)$ | $\mathcal{O}(H)$ | Visit all nodes. Space is call stack |
| Find max/min     | $\Theta(N)$ | $\mathcal{O}(H)$ | Check all nodes. Space is call stack |
| Search           | $\mathcal{O}(N)$ | $\mathcal{O}(H)$ | Worst case: check all. Space is call stack |
| Height           | $\Theta(N)$ | $\mathcal{O}(H)$ | Visit all nodes. Space is call stack |
| Insert (general) | $\mathcal{O}(N)$*| $\mathcal{O}(H)$ | Find position first |

*Position finding is $\mathcal{O}(N)$, actual pointer manipulation for insertion is $\Theta(1)$.

$H$ = height of tree, which is bounded by:

- $\Theta(\log N)$ for balanced tree
- $\mathcal{O}(N)$ for skewed tree

---

## Common Variations

### 1. N-ary Tree

```python
from typing import Optional

class NaryNode:
    r"""N-ary tree node (any number of children)."""
    def __init__(self, val: int = 0, children: Optional[list['NaryNode']] = None):
        self.val = val
        self.children = children if children is not None else []
```

### 2. Binary Tree with Extra Data

```python
from typing import Optional

class TreeNodeAugmented:
    r"""Tree node with additional metadata, often useful in segment trees or balanced BSTs."""
    def __init__(self, val: int = 0):
        self.val = val
        self.left: Optional['TreeNodeAugmented'] = None
        self.right: Optional['TreeNodeAugmented'] = None
        self.size = 1     # Size of subtree rooted at this node
        self.height = 0   # Height of subtree rooted at this node
```

---

## Edge Cases

```python
# 1. Empty tree
root = None
# -> Most functions should handle gracefully (first line check)

# 2. Single node
# root = TreeNode(1)
# -> Is both root and leaf. Height is 0 (or 1 depending on convention).

# 3. Skewed tree (like linked list)
#     1
#      \
#       2
#        \
#         3
# -> Height = N-1 (or N depending on convention). Call stack depth reaches N, taking O(N) space.
# Operations that are O(H) become O(N).

# 4. All same values
# -> Still valid tree, be careful with search/count returning all paths.

# 5. Negative values
# -> Ensure min/max comparisons initialize with float('inf') or float('-inf'), not 0.
```

---

## Interview Tips

1. **Always handle null root**: The first line of recursive tree functions should typically check `if not root:`
2. **Clarify tree type**: Is it a Binary Search Tree (BST) or a general binary tree? Are duplicates allowed?
3. **Think recursively first**: Most tree problems have elegant recursive solutions. Write the base case, then the recursive relation.
4. **Consider space complexity**: Explicitly state that recursion uses $\mathcal{O}(H)$ call stack space. This differentiates intermediate candidates from senior candidates.
5. **Draw the tree**: Visualize inputs and state changes before coding. Trace a small 3-node tree on the whiteboard.

---

## Practice Problems

| #   | Problem                      | Difficulty | Key Concept       |
| --- | ---------------------------- | ---------- | ----------------- |
| 1   | Maximum Depth of Binary Tree | Easy       | Basic recursion   |
| 2   | Invert Binary Tree           | Easy       | Tree manipulation |
| 3   | Same Tree                    | Easy       | Tree comparison   |
| 4   | Count Complete Tree Nodes    | Medium     | Tree properties   |
| 5   | Subtree of Another Tree      | Easy       | Tree matching     |

---

## Key Takeaways

1. **Binary tree**: Each node has at most 2 children (left, right).
2. **Recursive structure**: Left and right subtrees are also trees, making recursion the natural control flow.
3. **Height matters**: Call stack memory and time bounds often rely on tree height $H$. Balanced = $\mathcal{O}(\log N)$, skewed = $\mathcal{O}(N)$.
4. **Null checks**: Always handle the empty tree case first.
5. **Foundation**: Understanding basics is a strict prerequisite for BSTs, traversals, and advanced patterns like graphs.

---

## Next: [02-tree-traversals.md](./02-tree-traversals.md)

Learn the four main traversal patterns: inorder, preorder, postorder, and level-order.

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

```
count(tree) = 1 + count(left_subtree) + count(right_subtree)
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

**Why height matters for complexity**: Most tree operations are O(h) where h = height:
- Balanced tree: h = log(n) → operations are O(log n)
- Skewed tree: h = n → operations degrade to O(n)

---

## When NOT to Use

**Don't use a tree when:**
- **Data is not hierarchical** → Use array, hash map, or graph instead
- **Frequent insertions in sorted order** → Use balanced tree or skip list
- **Need O(1) access by index** → Use array
- **Need O(1) access by key** → Use hash map

**Trees are overkill when:**
- Simple linear data with no hierarchy → Use array/list
- Small data sets (< 100 elements) → Linear search is fine
- You only need LIFO/FIFO access → Use stack/queue

**Common mistake scenarios:**
- Using tree when hash map suffices for key-value storage
- Building tree from sorted array (creates skewed tree) → Use middle element as root
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

Interviewers use tree basics to test your understanding of pointer manipulation, recursion, and hierarchical problem-solving.

---

## Core Concept: What is a Binary Tree?

A binary tree is a hierarchical data structure where each node has at most two children, referred to as **left** and **right**.

```
Binary Tree Structure:

         1          ← root
        / \
       2   3        ← children of 1
      / \   \
     4   5   6      ← leaves: 4, 5, 6
```

### Key Terminology

| Term | Definition |
|------|------------|
| **Root** | Topmost node (no parent) |
| **Node** | Element containing value and child pointers |
| **Edge** | Connection between parent and child |
| **Leaf** | Node with no children |
| **Parent** | Node with child node(s) |
| **Child** | Node directly connected below a parent |
| **Sibling** | Nodes sharing the same parent |
| **Subtree** | Tree formed by a node and all its descendants |
| **Depth** | Distance from root to node (root has depth 0) |
| **Height** | Maximum depth of any node in tree |
| **Level** | All nodes at the same depth |

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

| Type | Property |
|------|----------|
| **Full Binary Tree** | Every node has 0 or 2 children |
| **Complete Binary Tree** | All levels filled except possibly last, which fills left to right |
| **Perfect Binary Tree** | All internal nodes have 2 children, all leaves at same level |
| **Balanced Binary Tree** | Height difference between subtrees is at most 1 |
| **Degenerate/Skewed** | Each node has only one child (like a linked list) |

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
class TreeNode:
    """
    Standard binary tree node used in LeetCode.

    Attributes:
        val: The value stored in this node
        left: Reference to left child (or None)
        right: Reference to right child (or None)
    """
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


# Creating a tree:
#       1
#      / \
#     2   3
#    /
#   4

root = TreeNode(1)
root.left = TreeNode(2)
root.right = TreeNode(3)
root.left.left = TreeNode(4)
```

### TreeNode with Parent Pointer

```python
class TreeNodeWithParent:
    """Binary tree node with parent pointer (used in some problems)."""
    def __init__(self, val=0):
        self.val = val
        self.left = None
        self.right = None
        self.parent = None  # Useful for certain problems
```

---

## Basic Tree Operations

### Count Nodes

```python
def count_nodes(root: TreeNode) -> int:
    """
    Count total nodes in tree.

    Time: O(n) - visit every node
    Space: O(h) - recursion stack, h = height
    """
    if not root:
        return 0
    return 1 + count_nodes(root.left) + count_nodes(root.right)
```

### Check if Leaf

```python
def is_leaf(node: TreeNode) -> bool:
    """Check if node is a leaf (no children)."""
    return node is not None and node.left is None and node.right is None
```

### Count Leaves

```python
def count_leaves(root: TreeNode) -> int:
    """
    Count leaf nodes in tree.

    Time: O(n)
    Space: O(h)
    """
    if not root:
        return 0
    if not root.left and not root.right:
        return 1
    return count_leaves(root.left) + count_leaves(root.right)
```

### Find Maximum Value

```python
def find_max(root: TreeNode) -> int:
    """
    Find maximum value in binary tree.

    Time: O(n) - must check every node
    Space: O(h)
    """
    if not root:
        return float('-inf')

    left_max = find_max(root.left)
    right_max = find_max(root.right)

    return max(root.val, left_max, right_max)
```

### Search for Value

```python
def search(root: TreeNode, target: int) -> bool:
    """
    Search for value in binary tree.

    Time: O(n) - may need to search all nodes
    Space: O(h)
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

def build_tree(values: list) -> TreeNode:
    """
    Build tree from level-order list (LeetCode format).
    None represents missing nodes.

    Example: [1, 2, 3, None, 4] creates:
          1
         / \
        2   3
         \
          4
    """
    if not values or values[0] is None:
        return None

    root = TreeNode(values[0])
    queue = deque([root])
    i = 1

    while queue and i < len(values):
        node = queue.popleft()

        # Left child
        if i < len(values) and values[i] is not None:
            node.left = TreeNode(values[i])
            queue.append(node.left)
        i += 1

        # Right child
        if i < len(values) and values[i] is not None:
            node.right = TreeNode(values[i])
            queue.append(node.right)
        i += 1

    return root


# Usage
root = build_tree([1, 2, 3, None, 4, 5, 6])
```

---

## Complexity Analysis

| Operation | Time | Space | Notes |
|-----------|------|-------|-------|
| Count nodes | O(n) | O(h) | Visit all nodes |
| Find max/min | O(n) | O(h) | Check all nodes |
| Search | O(n) | O(h) | Worst case: check all |
| Height | O(n) | O(h) | Visit all nodes |
| Insert (general) | O(n)* | O(h) | Find position first |

*Position finding is O(n), actual insertion is O(1)

h = height of tree, which is:
- O(log n) for balanced tree
- O(n) for skewed tree

---

## Common Variations

### 1. N-ary Tree

```python
class NaryNode:
    """N-ary tree node (any number of children)."""
    def __init__(self, val=0, children=None):
        self.val = val
        self.children = children if children else []
```

### 2. Binary Tree with Extra Data

```python
class TreeNodeAugmented:
    """Tree node with additional metadata."""
    def __init__(self, val=0):
        self.val = val
        self.left = None
        self.right = None
        self.size = 1  # Size of subtree
        self.height = 0  # Height of subtree
```

---

## Edge Cases

```python
# 1. Empty tree
root = None
# → Most functions should handle gracefully

# 2. Single node
root = TreeNode(1)
# → Is both root and leaf

# 3. Skewed tree (like linked list)
#     1
#      \
#       2
#        \
#         3
# → Height = n-1, operations become O(n)

# 4. All same values
# → Still valid tree, be careful with search/count

# 5. Negative values
# → Handle in min/max comparisons
```

---

## Interview Tips

1. **Always handle null root**: First line should check `if not root`
2. **Clarify tree type**: Is it BST or general binary tree?
3. **Think recursively first**: Most tree problems have elegant recursive solutions
4. **Consider space complexity**: Recursion uses O(h) stack space
5. **Draw the tree**: Visualize before coding

---

## Practice Problems

| # | Problem | Difficulty | Key Concept |
|---|---------|------------|-------------|
| 1 | Maximum Depth of Binary Tree | Easy | Basic recursion |
| 2 | Invert Binary Tree | Easy | Tree manipulation |
| 3 | Same Tree | Easy | Tree comparison |
| 4 | Count Complete Tree Nodes | Medium | Tree properties |
| 5 | Subtree of Another Tree | Easy | Tree matching |

---

## Key Takeaways

1. **Binary tree**: Each node has at most 2 children (left, right)
2. **Recursive structure**: Left and right subtrees are also trees
3. **Height matters**: Balanced = O(log n), skewed = O(n)
4. **Null checks**: Always handle empty tree case first
5. **Foundation**: Understanding basics is prerequisite for BST, traversals, and advanced patterns

---

## Next: [02-tree-traversals.md](./02-tree-traversals.md)

Learn the four main traversal patterns: inorder, preorder, postorder, and level-order.

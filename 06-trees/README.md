# Chapter 06: Trees

## Why This Matters for Interviews

Trees are **among the most frequently tested topics** at FANG+ companies because:

1. **Hierarchical data**: Trees model real-world structures (file systems, DOM, org charts)
2. **Recursive thinking**: Tree problems naturally test recursive problem-solving skills
3. **Multiple patterns**: Traversals, BST operations, path problems, construction
4. **Foundation for graphs**: Tree understanding is prerequisite for graph algorithms
5. **Diverse difficulty**: Easy traversals to hard serialization/LCA problems

At FANG+ companies, expect at least one tree problem in most interview loops.

**Interview frequency**: Very High. Trees appear in 60-70% of technical interviews.

---

## Core Patterns to Master

| Pattern                | Frequency | Key Problems                                 |
| ---------------------- | --------- | -------------------------------------------- |
| Tree Traversals        | Very High | Inorder, preorder, postorder, level-order    |
| BST Operations         | Very High | Search, insert, delete, validate BST         |
| Lowest Common Ancestor | High      | LCA in BST and binary tree                   |
| Path Sum               | High      | Path sum, all paths, max path sum            |
| Tree Depth/Height      | High      | Max depth, min depth, balanced check         |
| Tree Construction      | Medium    | Build from traversals, serialize/deserialize |
| Tree ↔ List Conversion | Medium    | Flatten to list, BST to sorted list          |

---

## Chapter Sections

| Section                                                   | Topic                    | Key Takeaway                                         |
| --------------------------------------------------------- | ------------------------ | ---------------------------------------------------- |
| [01-tree-basics](./01-tree-basics.md)                     | Binary Tree Structure    | Node representation, properties                      |
| [02-tree-traversals](./02-tree-traversals.md)             | DFS Traversals           | Inorder, preorder, postorder (recursive + iterative) |
| [03-level-order-traversal](./03-level-order-traversal.md) | BFS on Trees             | Level-order, zigzag, bottom-up                       |
| [04-bst-operations](./04-bst-operations.md)               | BST Search/Insert/Delete | Core BST operations                                  |
| [05-validate-bst](./05-validate-bst.md)                   | Validate BST             | Check if tree is valid BST                           |
| [06-tree-construction](./06-tree-construction.md)         | Build from Traversals    | Construct tree from inorder + preorder/postorder     |
| [07-lca-problems](./07-lca-problems.md)                   | Lowest Common Ancestor   | LCA for BST and binary tree                          |
| [08-path-sum](./08-path-sum.md)                           | Path Sum Problems        | Has path sum, all paths, max path sum                |
| [09-tree-depth](./09-tree-depth.md)                       | Depth and Balance        | Max/min depth, balanced tree check                   |
| [10-tree-diameter](./10-tree-diameter.md)                 | Tree Diameter            | Longest path between any two nodes                   |
| [11-symmetric-tree](./11-symmetric-tree.md)               | Symmetric and Same Tree  | Mirror check, tree equality                          |
| [12-serialize-deserialize](./12-serialize-deserialize.md) | Tree Serialization       | Convert tree to string and back                      |
| [13-binary-tree-to-list](./13-binary-tree-to-list.md)     | Flatten Tree             | Tree to linked list conversions                      |
| [14-bst-iterator](./14-bst-iterator.md)                   | BST Iterator             | Implement next() and hasNext()                       |
| [15-kth-smallest](./15-kth-smallest.md)                   | Kth Smallest in BST      | Find kth smallest element                            |

---

## Common Mistakes Interviewers Watch For

1. **Forgetting null checks**: Not handling empty tree or null children
2. **Confusing traversal orders**: Mixing up inorder vs preorder vs postorder
3. **BST property violations**: Forgetting BST allows no duplicates (or left < root < right)
4. **Wrong LCA approach**: Using BT approach for BST (inefficient) or vice versa
5. **Not tracking state properly**: Losing track of path/sum in recursive calls
6. **Ignoring return values**: Not using recursive return values correctly
7. **Off-by-one in height**: Confusing depth (0-indexed) vs height

---

## Time Targets

| Difficulty | Target Time | Examples                            |
| ---------- | ----------- | ----------------------------------- |
| Easy       | 10-15 min   | Max Depth, Same Tree, Invert Tree   |
| Medium     | 15-25 min   | Validate BST, LCA, Path Sum II      |
| Hard       | 25-40 min   | Serialize/Deserialize, Max Path Sum |

---

## Pattern Recognition Guide

```
"Traverse tree..."             → Choose appropriate traversal
"Find in BST..."               → Use BST property (O(log n))
"Find in binary tree..."       → Must search all nodes (O(n))
"Lowest common ancestor..."    → LCA pattern (different for BST vs BT)
"Path from root to..."         → DFS with path tracking
"Level by level..."            → BFS with queue
"Height/depth..."              → DFS (recursion or stack)
"Balanced tree..."             → Check heights recursively
"Build tree from..."           → Divide and conquer construction
"Serialize/deserialize..."     → Preorder or level-order encoding
```

---

## Binary Tree Node Definition

```python
class TreeNode:
    """Standard binary tree node used in LeetCode."""
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
```

---

## Key Complexity Facts

| Operation         | Binary Tree | BST (balanced) | BST (skewed) |
| ----------------- | ----------- | -------------- | ------------ |
| Search            | O(n)        | O(log n)       | O(n)         |
| Insert            | O(n)        | O(log n)       | O(n)         |
| Delete            | O(n)        | O(log n)       | O(n)         |
| Traversal         | O(n)        | O(n)           | O(n)         |
| Height            | O(n)        | O(log n)       | O(n)         |
| Space (recursive) | O(h)        | O(log n)       | O(n)         |

*Note: For a general Binary Tree, finding the correct position for insertion/deletion takes O(n) time. The actual pointer manipulation takes O(1) time. The overall time complexity is O(n).*

---

## Prerequisites

> **Prerequisites:** [01-complexity-analysis](../01-complexity-analysis/README.md), [04-linked-lists](../04-linked-lists/README.md)

Understanding Big-O and linked list node manipulation is essential. Recursion knowledge is highly recommended.

---

## Next Steps

Start with [01-tree-basics.md](./01-tree-basics.md) to understand binary tree structure and properties. Then master traversals before moving to BST operations and more complex patterns. Traversals are the foundation for almost all tree problems.

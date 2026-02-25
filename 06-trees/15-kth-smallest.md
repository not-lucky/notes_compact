# Kth Smallest Element in BST

> **Prerequisites:** [02-tree-traversals](./02-tree-traversals.md), [04-bst-operations](./04-bst-operations.md), [14-bst-iterator](./14-bst-iterator.md)

## Interview Context

Finding kth smallest in BST is important because:

1. **Classic BST problem**: Tests understanding of inorder traversal
2. **Multiple approaches**: From simple to optimized for repeated queries
3. **Follow-up questions**: "What if the tree changes frequently?"
4. **Common interview question**: Frequently asked at Google, Amazon, Meta

This combines BST properties with order statistics.

---

## Core Insight

Inorder traversal of BST gives nodes in **sorted order**. The kth element in inorder is the kth smallest.

```
BST:
       5
      / \
     3   6
    / \
   2   4
  /
 1

Inorder: [1, 2, 3, 4, 5, 6]
k=1 → 1
k=3 → 3
k=5 → 5
```

---

## Approach 1: Inorder with Counter

Stop traversal when we've seen k elements.

### Recursive

```python
from typing import Optional

class TreeNode:
    def __init__(self, val: int = 0, left: Optional['TreeNode'] = None, right: Optional['TreeNode'] = None):
        self.val = val
        self.left = left
        self.right = right

def kth_smallest(root: Optional[TreeNode], k: int) -> int:
    r"""
    Find kth smallest element in BST.

    LeetCode 230: Kth Smallest Element in a BST

    Time: $\mathcal{O}(H + k)$ where $H$ is the height of the tree.
          In the worst case (skewed tree), this is $\mathcal{O}(N)$.
          On average (balanced tree), this is $\mathcal{O}(\log N + k)$.
    Space: $\mathcal{O}(H)$ for the recursive call stack.
           In the worst case (skewed tree), this is $\mathcal{O}(N)$.
           On average (balanced tree), this is $\mathcal{O}(\log N)$.
    """
    count = [0]
    result = [None]

    def inorder(node: Optional[TreeNode]) -> None:
        if node is None or result[0] is not None:
            return

        inorder(node.left)

        count[0] += 1
        if count[0] == k:
            result[0] = node.val
            return

        inorder(node.right)

    inorder(root)
    return result[0] if result[0] is not None else -1
```

### Iterative (More Control)

```python
def kth_smallest_iterative(root: Optional[TreeNode], k: int) -> int:
    r"""
    Iterative approach - can stop early.

    Time: $\mathcal{O}(H + k)$ where $H$ is the height of the tree.
          Worst case $\mathcal{O}(N)$, average case $\mathcal{O}(\log N + k)$.
    Space: $\mathcal{O}(H)$ for the explicit stack simulating recursion.
           Worst case $\mathcal{O}(N)$, average case $\mathcal{O}(\log N)$.
    """
    stack: list[TreeNode] = []
    current = root
    count = 0

    while current is not None or stack:
        # Go left as far as possible
        while current is not None:
            stack.append(current)
            current = current.left

        current = stack.pop()
        count += 1

        if count == k:
            return current.val

        current = current.right

    return -1  # k is larger than tree size
```

---

## Approach 2: Build Sorted Array

Simple but uses $\Theta(N)$ space.

```python
from typing import Optional

# Using dummy TreeNode defined earlier
def kth_smallest_array(root: Optional[TreeNode], k: int) -> int:
    r"""
    Build sorted array, return k-1 index.

    Time: $\Theta(N)$ because we traverse the entire tree.
    Space: $\Theta(N)$ for the returned array + $\mathcal{O}(H)$ for the recursive call stack.
           Overall auxiliary space bounds are $\Theta(N)$.
    """
    def inorder(node: Optional[TreeNode]) -> list[int]:
        if node is None:
            return []
        # Note: list concatenation with + creates a new list, leading to O(N^2) total time.
        # A better approach is to append to a single list or use .extend().
        # However, for conceptual simplicity of "building an array":
        left = inorder(node.left)
        right = inorder(node.right)
        return left + [node.val] + right

    return inorder(root)[k - 1] if root else -1
```

---

## Approach 3: Augmented BST (For Repeated Queries)

If we need frequent kth smallest queries, augment nodes with subtree size.

```python
from typing import Optional

class AugmentedTreeNode:
    """BST node with subtree size."""
    def __init__(self, val: int = 0):
        self.val = val
        self.left: Optional['AugmentedTreeNode'] = None
        self.right: Optional['AugmentedTreeNode'] = None
        self.size = 1  # Size of subtree rooted at this node


def kth_smallest_augmented(root: Optional[AugmentedTreeNode], k: int) -> int:
    r"""
    $\mathcal{O}(H)$ query using subtree sizes.

    Time: $\mathcal{O}(H)$ where $H$ is the height of the tree.
          Worst case $\mathcal{O}(N)$, average case $\mathcal{O}(\log N)$.
    Space: $\mathcal{O}(1)$ iterative approach requires no extra call stack.
    """
    while root is not None:
        left_size = root.left.size if root.left is not None else 0

        if k == left_size + 1:
            return root.val
        elif k <= left_size:
            root = root.left
        else:
            k -= left_size + 1
            root = root.right

    return -1


def update_sizes(root: Optional[AugmentedTreeNode]) -> int:
    r"""
    Update subtree sizes after insertion/deletion.

    Time: $\mathcal{O}(N)$ to traverse all nodes and update.
    Space: $\mathcal{O}(H)$ for recursive call stack.
    """
    if root is None:
        return 0

    left_size = update_sizes(root.left)
    right_size = update_sizes(root.right)
    root.size = 1 + left_size + right_size

    return root.size
```

---

## Kth Largest Element

For kth largest, use **reverse inorder** (right → root → left).

```python
from typing import Optional

def kth_largest(root: Optional[TreeNode], k: int) -> int:
    r"""
    Find kth largest element in BST.

    Time: $\mathcal{O}(H + k)$ where $H$ is the height of the tree.
          Worst case $\mathcal{O}(N)$, average case $\mathcal{O}(\log N + k)$.
    Space: $\mathcal{O}(H)$ for the stack simulating recursion.
           Worst case $\mathcal{O}(N)$, average case $\mathcal{O}(\log N)$.
    """
    stack: list[TreeNode] = []
    current = root
    count = 0

    while current is not None or stack:
        # Go right as far as possible (reverse inorder)
        while current is not None:
            stack.append(current)
            current = current.right

        current = stack.pop()
        count += 1

        if count == k:
            return current.val

        current = current.left

    return -1
```

---

## Follow-up: Frequent Modifications

**Q**: What if the BST is modified frequently and we need to find kth smallest often?

**A**: Use augmented BST with subtree sizes.

| Operation    | Standard BST        | Augmented BST       |
| ------------ | ------------------- | ------------------- |
| Insert       | $\mathcal{O}(H)$    | $\mathcal{O}(H)$    |
| Delete       | $\mathcal{O}(H)$    | $\mathcal{O}(H)$    |
| Kth smallest | $\mathcal{O}(H + k)$| $\mathcal{O}(H)$    |

The augmented approach is better when k queries >> modifications.

---

## Related: Count Smaller Before Self

```python
from typing import Optional

def count_smaller(nums: list[int]) -> list[int]:
    r"""
    Count elements smaller than nums[i] to its right.

    LeetCode 315: Count of Smaller Numbers After Self

    Use BST with subtree sizes.
    Time: $\mathcal{O}(N \log N)$ average, $\mathcal{O}(N^2)$ worst case (skewed).
          Note: This BST approach is less optimal than Merge Sort or Fenwick/Segment Tree
          which guarantee $\mathcal{O}(N \log N)$ worst-case time complexity.
    Space: $\mathcal{O}(N)$ for the BST and the result array.
    """
    class CountNode:
        def __init__(self, val: int):
            self.val = val
            self.left: Optional['CountNode'] = None
            self.right: Optional['CountNode'] = None
            self.left_count = 0  # Count of nodes in left subtree

    def insert(root: CountNode, val: int) -> int:
        count = 0
        current: Optional['CountNode'] = root

        while current is not None:
            if val <= current.val:
                current.left_count += 1
                if current.left is None:
                    current.left = CountNode(val)
                    break
                current = current.left
            else:
                count += current.left_count + 1
                if current.right is None:
                    current.right = CountNode(val)
                    break
                current = current.right
        return count

    if not nums:
        return []

    result = [0] * len(nums)
    root = CountNode(nums[-1])

    for i in range(len(nums) - 2, -1, -1):
        result[i] = insert(root, nums[i])

    return result
```

---

## Complexity Analysis

| Approach        | Time                 | Space               | Best For                         |
| --------------- | -------------------- | ------------------- | -------------------------------- |
| Inorder counter | $\mathcal{O}(H + k)$ | $\mathcal{O}(H)$    | Single query                     |
| Build array     | $\Theta(N)$          | $\Theta(N)$         | Multiple queries, static tree    |
| Augmented BST   | $\mathcal{O}(H)$     | $\mathcal{O}(1)$    | Frequent queries + modifications |

---

## Edge Cases

```python
# 1. k = 1 (smallest element)
# → Go all the way left

# 2. k = N (largest element)
# → Go all the way right

# 3. k out of range
# → Return -1 or raise exception

# 4. Single node tree
# → k must be 1

# 5. Skewed tree
# → Worst case H = N
```

---

## Interview Tips

1. **Start with inorder**: Explain why inorder gives sorted order
2. **Iterative is preferred**: More control, can stop early
3. **Mention augmented BST**: Shows you think about optimization
4. **Analyze complexity**: $\mathcal{O}(H + k)$ for single query
5. **Ask about frequency**: "How often is this called?" determines approach

---

## Practice Problems

| #   | Problem                              | Difficulty | Key Concept           |
| --- | ------------------------------------ | ---------- | --------------------- |
| 1   | Kth Smallest Element in a BST        | Medium     | Core problem          |
| 2   | Second Minimum Node In a Binary Tree | Easy       | Variant               |
| 3   | Count of Smaller Numbers After Self  | Hard       | BST order statistics  |
| 4   | Kth Largest Element in a Stream      | Easy       | Min heap alternative  |
| 5   | Find K-th Smallest Pair Distance     | Hard       | Binary search + count |

---

## Key Takeaways

1. **Inorder = sorted**: BST inorder traversal gives sorted order
2. **Early termination**: Stop after finding k elements
3. **Augmented BST**: Store subtree sizes for $\mathcal{O}(H)$ queries
4. **Kth largest**: Reverse inorder (right first)
5. **Follow-up ready**: Know when to use augmented approach

---

## Chapter Summary

This chapter covered essential tree patterns for FANG+ interviews:

- **Basics**: Tree structure, node definitions
- **Traversals**: Inorder, preorder, postorder (recursive + iterative)
- **Level-order**: BFS-based traversal and variations
- **BST Operations**: Search, insert, delete
- **Validate BST**: Range-based and inorder approaches
- **Tree Construction**: Build from traversals
- **LCA**: Lowest Common Ancestor for BST and BT
- **Path Sum**: Various path sum problems
- **Depth/Balance**: Height calculations and balance checks
- **Diameter**: Longest path between any two nodes
- **Symmetric/Same**: Tree comparison problems
- **Serialization**: Convert tree to/from string
- **Tree to List**: Various conversion patterns
- **BST Iterator**: Iterator design pattern
- **Kth Smallest**: Order statistics in BST

Master these patterns and you'll be well-prepared for tree problems in technical interviews!

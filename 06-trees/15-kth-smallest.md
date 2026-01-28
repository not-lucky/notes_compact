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
def kth_smallest(root: TreeNode, k: int) -> int:
    """
    Find kth smallest element in BST.

    LeetCode 230: Kth Smallest Element in a BST

    Time: O(H + k) where H is height
    Space: O(H) for recursion
    """
    count = [0]
    result = [None]

    def inorder(node):
        if not node or result[0] is not None:
            return

        inorder(node.left)

        count[0] += 1
        if count[0] == k:
            result[0] = node.val
            return

        inorder(node.right)

    inorder(root)
    return result[0]
```

### Iterative (More Control)

```python
def kth_smallest_iterative(root: TreeNode, k: int) -> int:
    """
    Iterative approach - can stop early.

    Time: O(H + k)
    Space: O(H)
    """
    stack = []
    current = root
    count = 0

    while current or stack:
        # Go left as far as possible
        while current:
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

Simple but uses O(n) space.

```python
def kth_smallest_array(root: TreeNode, k: int) -> int:
    """
    Build sorted array, return k-1 index.

    Time: O(n)
    Space: O(n)
    """
    def inorder(node):
        return inorder(node.left) + [node.val] + inorder(node.right) if node else []

    return inorder(root)[k - 1]
```

---

## Approach 3: Augmented BST (For Repeated Queries)

If we need frequent kth smallest queries, augment nodes with subtree size.

```python
class AugmentedTreeNode:
    """BST node with subtree size."""
    def __init__(self, val=0):
        self.val = val
        self.left = None
        self.right = None
        self.size = 1  # Size of subtree rooted at this node


def kth_smallest_augmented(root: AugmentedTreeNode, k: int) -> int:
    """
    O(H) query using subtree sizes.

    Time: O(H)
    Space: O(1) iterative
    """
    while root:
        left_size = root.left.size if root.left else 0

        if k == left_size + 1:
            return root.val
        elif k <= left_size:
            root = root.left
        else:
            k -= left_size + 1
            root = root.right

    return -1


def update_sizes(root: AugmentedTreeNode) -> int:
    """Update subtree sizes after insertion/deletion."""
    if not root:
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
def kth_largest(root: TreeNode, k: int) -> int:
    """
    Find kth largest element in BST.

    Time: O(H + k)
    Space: O(H)
    """
    stack = []
    current = root
    count = 0

    while current or stack:
        # Go right as far as possible (reverse inorder)
        while current:
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

| Operation    | Standard BST | Augmented BST |
| ------------ | ------------ | ------------- |
| Insert       | O(H)         | O(H)          |
| Delete       | O(H)         | O(H)          |
| Kth smallest | O(H + k)     | O(H)          |

The augmented approach is better when k queries >> modifications.

---

## Related: Count Smaller Before Self

```python
def count_smaller(nums: list[int]) -> list[int]:
    """
    Count elements smaller than nums[i] to its right.

    LeetCode 315: Count of Smaller Numbers After Self

    Use BST with subtree sizes.
    """
    class TreeNode:
        def __init__(self, val):
            self.val = val
            self.left = None
            self.right = None
            self.left_count = 0  # Count of nodes in left subtree

    def insert(root, val):
        count = 0
        while root:
            if val <= root.val:
                root.left_count += 1
                if not root.left:
                    root.left = TreeNode(val)
                    break
                root = root.left
            else:
                count += root.left_count + 1
                if not root.right:
                    root.right = TreeNode(val)
                    break
                root = root.right
        return count

    if not nums:
        return []

    result = [0] * len(nums)
    root = TreeNode(nums[-1])

    for i in range(len(nums) - 2, -1, -1):
        result[i] = insert(root, nums[i])

    return result
```

---

## Complexity Analysis

| Approach        | Time     | Space | Best For                         |
| --------------- | -------- | ----- | -------------------------------- |
| Inorder counter | O(H + k) | O(H)  | Single query                     |
| Build array     | O(n)     | O(n)  | Multiple queries, static tree    |
| Augmented BST   | O(H)     | O(1)  | Frequent queries + modifications |

---

## Edge Cases

```python
# 1. k = 1 (smallest element)
# → Go all the way left

# 2. k = n (largest element)
# → Go all the way right

# 3. k out of range
# → Return -1 or raise exception

# 4. Single node tree
# → k must be 1

# 5. Skewed tree
# → Worst case H = n
```

---

## Interview Tips

1. **Start with inorder**: Explain why inorder gives sorted order
2. **Iterative is preferred**: More control, can stop early
3. **Mention augmented BST**: Shows you think about optimization
4. **Analyze complexity**: O(H + k) for single query
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
3. **Augmented BST**: Store subtree sizes for O(H) queries
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

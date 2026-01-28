# Symmetric Tree and Same Tree

> **Prerequisites:** [01-tree-basics](./01-tree-basics.md), [02-tree-traversals](./02-tree-traversals.md)

## Interview Context

Tree comparison problems are important because:

1. **Warm-up problems**: Often used as interview warm-ups at FANG+
2. **Foundation for harder problems**: Logic extends to subtree matching
3. **Tests recursion understanding**: Clean recursive solutions
4. **Multiple approaches**: Recursive, iterative, and serialization-based

These are considered "easy" but tricky to get right on the first try.

---

## Same Tree

Check if two trees are structurally identical with same values.

### Recursive Solution

```python
def is_same_tree(p: TreeNode, q: TreeNode) -> bool:
    """
    Check if two trees are identical.

    LeetCode 100: Same Tree

    Time: O(min(n, m)) - stop at first mismatch
    Space: O(min(h1, h2)) - recursion depth
    """
    # Both null
    if not p and not q:
        return True

    # One null, one not
    if not p or not q:
        return False

    # Both exist - check value and subtrees
    return (p.val == q.val and
            is_same_tree(p.left, q.left) and
            is_same_tree(p.right, q.right))
```

### Iterative Solution

```python
from collections import deque

def is_same_tree_iterative(p: TreeNode, q: TreeNode) -> bool:
    """
    Iterative same tree check using BFS.

    Time: O(min(n, m))
    Space: O(min(w1, w2)) - queue width
    """
    queue = deque([(p, q)])

    while queue:
        node1, node2 = queue.popleft()

        if not node1 and not node2:
            continue
        if not node1 or not node2:
            return False
        if node1.val != node2.val:
            return False

        queue.append((node1.left, node2.left))
        queue.append((node1.right, node2.right))

    return True
```

---

## Symmetric Tree

Check if a tree is a mirror of itself.

```
Symmetric:          Not Symmetric:
     1                   1
    / \                 / \
   2   2               2   2
  / \ / \               \   \
 3  4 4  3               3   3

Mirror property: left subtree mirrors right subtree
```

### Recursive Solution

```python
def is_symmetric(root: TreeNode) -> bool:
    """
    Check if tree is symmetric (mirror of itself).

    LeetCode 101: Symmetric Tree

    Time: O(n)
    Space: O(h)
    """
    if not root:
        return True

    def is_mirror(left, right):
        # Both null
        if not left and not right:
            return True

        # One null
        if not left or not right:
            return False

        # Check: same value, and cross-compare children
        return (left.val == right.val and
                is_mirror(left.left, right.right) and  # Outer
                is_mirror(left.right, right.left))     # Inner

    return is_mirror(root.left, root.right)
```

### Iterative Solution

```python
def is_symmetric_iterative(root: TreeNode) -> bool:
    """
    Iterative symmetry check using queue.

    Time: O(n)
    Space: O(w)
    """
    if not root:
        return True

    queue = deque([(root.left, root.right)])

    while queue:
        left, right = queue.popleft()

        if not left and not right:
            continue
        if not left or not right:
            return False
        if left.val != right.val:
            return False

        # Add pairs in mirror order
        queue.append((left.left, right.right))
        queue.append((left.right, right.left))

    return True
```

---

## Visual Explanation of Symmetric Check

```
     1
    / \
   2   2
  / \ / \
 3  4 4  3

is_mirror(2, 2):
  - 2.val == 2.val ✓
  - is_mirror(2.left, 2.right) → is_mirror(3, 3)
  - is_mirror(2.right, 2.left) → is_mirror(4, 4)

is_mirror(3, 3):
  - 3.val == 3.val ✓
  - is_mirror(null, null) → True
  - is_mirror(null, null) → True

All checks pass → Symmetric!
```

---

## Subtree of Another Tree

```python
def is_subtree(root: TreeNode, sub_root: TreeNode) -> bool:
    """
    Check if sub_root is a subtree of root.

    LeetCode 572: Subtree of Another Tree

    Time: O(m * n) where m, n are sizes of trees
    Space: O(h)
    """
    if not sub_root:
        return True

    if not root:
        return False

    if is_same_tree(root, sub_root):
        return True

    return is_subtree(root.left, sub_root) or is_subtree(root.right, sub_root)


def is_same_tree(p, q):
    if not p and not q:
        return True
    if not p or not q:
        return False
    return (p.val == q.val and
            is_same_tree(p.left, q.left) and
            is_same_tree(p.right, q.right))
```

### Optimized with Serialization

```python
def is_subtree_optimized(root: TreeNode, sub_root: TreeNode) -> bool:
    """
    Serialize trees and use string matching.

    Time: O(m + n) with KMP
    Space: O(m + n) for strings
    """
    def serialize(node):
        if not node:
            return "#"
        # Use delimiters to avoid false matches
        return f"^{node.val},{serialize(node.left)},{serialize(node.right)}"

    root_str = serialize(root)
    sub_str = serialize(sub_root)

    return sub_str in root_str
```

---

## Invert Binary Tree

```python
def invert_tree(root: TreeNode) -> TreeNode:
    """
    Invert binary tree (mirror it).

    LeetCode 226: Invert Binary Tree

    Time: O(n)
    Space: O(h)
    """
    if not root:
        return None

    # Swap children
    root.left, root.right = root.right, root.left

    # Recursively invert subtrees
    invert_tree(root.left)
    invert_tree(root.right)

    return root
```

### Iterative Version

```python
from collections import deque

def invert_tree_iterative(root: TreeNode) -> TreeNode:
    """
    Iterative tree inversion.

    Time: O(n)
    Space: O(w)
    """
    if not root:
        return None

    queue = deque([root])

    while queue:
        node = queue.popleft()
        node.left, node.right = node.right, node.left

        if node.left:
            queue.append(node.left)
        if node.right:
            queue.append(node.right)

    return root
```

---

## Flip Equivalent Binary Trees

```python
def flip_equiv(root1: TreeNode, root2: TreeNode) -> bool:
    """
    Check if trees are flip equivalent.

    Trees are flip equivalent if we can make them identical
    by flipping some nodes (swapping left and right children).

    LeetCode 951: Flip Equivalent Binary Trees

    Time: O(n)
    Space: O(h)
    """
    if not root1 and not root2:
        return True

    if not root1 or not root2:
        return False

    if root1.val != root2.val:
        return False

    # Either no flip or flip
    return ((flip_equiv(root1.left, root2.left) and
             flip_equiv(root1.right, root2.right)) or
            (flip_equiv(root1.left, root2.right) and
             flip_equiv(root1.right, root2.left)))
```

---

## Merge Two Binary Trees

```python
def merge_trees(root1: TreeNode, root2: TreeNode) -> TreeNode:
    """
    Merge two trees by summing overlapping nodes.

    LeetCode 617: Merge Two Binary Trees

    Time: O(min(n1, n2))
    Space: O(min(h1, h2))
    """
    if not root1:
        return root2
    if not root2:
        return root1

    # Merge values
    root1.val += root2.val

    # Recursively merge children
    root1.left = merge_trees(root1.left, root2.left)
    root1.right = merge_trees(root1.right, root2.right)

    return root1
```

---

## Complexity Analysis

| Problem         | Time          | Space | Notes                     |
| --------------- | ------------- | ----- | ------------------------- |
| Same Tree       | O(n)          | O(h)  | Stop at first mismatch    |
| Symmetric Tree  | O(n)          | O(h)  | Compare mirror pairs      |
| Subtree Check   | O(m\*n)       | O(h)  | O(m+n) with serialization |
| Invert Tree     | O(n)          | O(h)  | Visit all nodes           |
| Flip Equivalent | O(n)          | O(h)  | Branch on flip/no-flip    |
| Merge Trees     | O(min(n1,n2)) | O(h)  | Only overlapping nodes    |

---

## Edge Cases

```python
# 1. Empty trees
is_same_tree(None, None)  # True
is_symmetric(None)        # True

# 2. One empty, one not
is_same_tree(TreeNode(1), None)  # False

# 3. Single node
is_symmetric(TreeNode(1))  # True

# 4. Values matter
#     1          1
#    /          /
#   2    vs    3
is_same_tree(...)  # False - different values

# 5. Structure matters
#     1          1
#    /            \
#   2              2
is_symmetric(...)  # False - not mirror
```

---

## Interview Tips

1. **Handle both null first**: Common pattern for tree comparison
2. **Order of checks matters**: null checks before value access
3. **Symmetric ≠ Same**: Symmetric compares with self, same compares two trees
4. **Draw the mirroring**: For symmetric, left.left ↔ right.right
5. **Subtree optimization**: Mention serialization + string matching

---

## Practice Problems

| #   | Problem                      | Difficulty | Key Concept             |
| --- | ---------------------------- | ---------- | ----------------------- |
| 1   | Same Tree                    | Easy       | Basic comparison        |
| 2   | Symmetric Tree               | Easy       | Mirror comparison       |
| 3   | Subtree of Another Tree      | Easy       | Recursive subtree check |
| 4   | Invert Binary Tree           | Easy       | Swap children           |
| 5   | Flip Equivalent Binary Trees | Medium     | Flip or no flip         |
| 6   | Merge Two Binary Trees       | Easy       | Sum overlapping         |
| 7   | Leaf-Similar Trees           | Easy       | Compare leaf sequences  |

---

## Key Takeaways

1. **Same tree**: Compare value, then both subtrees recursively
2. **Symmetric**: Compare left.left with right.right (cross-compare)
3. **Null handling**: Always check null before accessing values
4. **Iterative option**: Use queue with pairs of nodes
5. **Subtree matching**: Either brute force or serialize

---

## Next: [12-serialize-deserialize.md](./12-serialize-deserialize.md)

Learn to serialize and deserialize binary trees.

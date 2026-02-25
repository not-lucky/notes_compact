# Symmetric Tree and Same Tree

> **Prerequisites:** [01-tree-basics](./01-tree-basics.md), [02-tree-traversals](./02-tree-traversals.md)

## Interview Context

Tree comparison problems are important because:

1. **Warm-up problems**: Often used as interview warm-ups at FANG+
2. **Foundation for harder problems**: Logic extends to subtree matching
3. **Tests recursion understanding**: Clean recursive solutions
4. **Multiple approaches**: Recursive, iterative, and serialization-based

These are considered "easy" but tricky to get right on the first try.

*Note: All code examples assume the following `TreeNode` definition:*
```python
from typing import Optional

class TreeNode:
    def __init__(self, val: int = 0, left: Optional['TreeNode'] = None, right: Optional['TreeNode'] = None):
        self.val = val
        self.left = left
        self.right = right
```

---

## Same Tree

Check if two trees are structurally identical with same values.

### Recursive Solution

```python
from typing import Optional

def is_same_tree(p: Optional[TreeNode], q: Optional[TreeNode]) -> bool:
    r"""
    Check if two trees are identical.

    LeetCode 100: Same Tree

    Time Complexity: $\mathcal{O}(\min(N, M))$ where $N, M$ are the number of nodes in trees `p` and `q`. We stop at the first mismatch.
    Space Complexity: $\mathcal{O}(\min(H_1, H_2))$ where $H_1, H_2$ are the heights of the trees, due to the recursive call stack. In the worst case (skewed tree), this is $\mathcal{O}(\min(N, M))$. In a balanced tree, it is $\mathcal{O}(\min(\log N, \log M))$.
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
from typing import Optional, Tuple
from collections import deque

def is_same_tree_iterative(p: Optional[TreeNode], q: Optional[TreeNode]) -> bool:
    r"""
    Iterative same tree check using BFS.

    Time Complexity: $\mathcal{O}(\min(N, M))$ where $N, M$ are the number of nodes.
    Space Complexity: $\mathcal{O}(\min(W_1, W_2))$ where $W_1, W_2$ are the maximum widths of the trees. In the worst case (a full binary tree), the width is roughly $\frac{N}{2}$, so space is $\mathcal{O}(\min(N, M))$.
    """
    queue: deque[Tuple[Optional[TreeNode], Optional[TreeNode]]] = deque([(p, q)])

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
from typing import Optional

def is_symmetric(root: Optional[TreeNode]) -> bool:
    r"""
    Check if tree is symmetric (mirror of itself).

    LeetCode 101: Symmetric Tree

    Time Complexity: $\Theta(N)$ where $N$ is the number of nodes. We must visit all nodes to confirm symmetry.
    Space Complexity: $\mathcal{O}(H)$ where $H$ is the height of the tree, representing the recursive call stack. Worst case $\mathcal{O}(N)$ for skewed trees, $\mathcal{O}(\log N)$ for balanced trees.
    """
    if not root:
        return True

    def is_mirror(left: Optional[TreeNode], right: Optional[TreeNode]) -> bool:
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
from typing import Optional, Tuple
from collections import deque

def is_symmetric_iterative(root: Optional[TreeNode]) -> bool:
    r"""
    Iterative symmetry check using queue.

    Time Complexity: $\Theta(N)$ to visit all nodes if symmetric.
    Space Complexity: $\mathcal{O}(W)$ where $W$ is the maximum width of the tree. In a balanced tree, the widest level contains roughly $\frac{N}{2}$ nodes, making space $\mathcal{O}(N)$ in the worst case.
    """
    if not root:
        return True

    queue: deque[Tuple[Optional[TreeNode], Optional[TreeNode]]] = deque([(root.left, root.right)])

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
from typing import Optional

def is_subtree(root: Optional[TreeNode], sub_root: Optional[TreeNode]) -> bool:
    r"""
    Check if sub_root is a subtree of root.

    LeetCode 572: Subtree of Another Tree

    Time Complexity: $\mathcal{O}(M \cdot N)$ where $M$ is the number of nodes in `root` and $N$ is the number of nodes in `sub_root`. In the worst case, we compare the entire `sub_root` for every node in `root`.
    Space Complexity: $\mathcal{O}(H_M + H_N)$ where $H_M$ and $H_N$ are the heights of the two trees. This accounts for the maximum depth of the nested recursive call stacks.
    """
    if not sub_root:
        return True

    if not root:
        return False

    if is_same_tree_helper(root, sub_root):
        return True

    return is_subtree(root.left, sub_root) or is_subtree(root.right, sub_root)


def is_same_tree_helper(p: Optional[TreeNode], q: Optional[TreeNode]) -> bool:
    if not p and not q:
        return True
    if not p or not q:
        return False
    return (p.val == q.val and
            is_same_tree_helper(p.left, q.left) and
            is_same_tree_helper(p.right, q.right))
```

### Optimized with Serialization

```python
from typing import Optional

def is_subtree_optimized(root: Optional[TreeNode], sub_root: Optional[TreeNode]) -> bool:
    r"""
    Serialize trees and use string matching.

    Time Complexity: $\Theta(M + N)$ where $M$ and $N$ are the number of nodes in each tree. Preorder traversal takes $\Theta(M+N)$ time. Python's `in` operator uses an implementation of Boyer-Moore-Horspool or similar, bounded closely to $\mathcal{O}(M + N)$ in typical string matching, though technically $\mathcal{O}(M \cdot N)$ in adversarial worst cases. KMP strictly gives $\mathcal{O}(M+N)$.
    Space Complexity: $\Theta(M + N)$ for the serialized strings, plus $\mathcal{O}(\max(H_M, H_N))$ for the recursive traversal stack. Overall $\Theta(M + N)$.
    """
    def serialize(node: Optional[TreeNode]) -> str:
        if not node:
            return "#"
        # Use delimiters to avoid false matches (e.g. 12 in 123)
        return f"^{node.val},{serialize(node.left)},{serialize(node.right)}"

    root_str = serialize(root)
    sub_str = serialize(sub_root)

    return sub_str in root_str
```

---

## Invert Binary Tree

```python
from typing import Optional

def invert_tree(root: Optional[TreeNode]) -> Optional[TreeNode]:
    r"""
    Invert binary tree (mirror it).

    LeetCode 226: Invert Binary Tree

    Time Complexity: $\Theta(N)$ because every node in the tree is visited exactly once.
    Space Complexity: $\mathcal{O}(H)$ where $H$ is the height of the tree. The recursive call stack bounds space to $\mathcal{O}(\log N)$ for balanced trees and $\mathcal{O}(N)$ worst-case for skewed trees.
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
from typing import Optional
from collections import deque

def invert_tree_iterative(root: Optional[TreeNode]) -> Optional[TreeNode]:
    r"""
    Iterative tree inversion.

    Time Complexity: $\Theta(N)$ since we process every node once.
    Space Complexity: $\mathcal{O}(W)$ where $W$ is the maximum width of the tree, which corresponds to the maximum size of the queue. For balanced trees, this is $\mathcal{O}(N)$.
    """
    if not root:
        return None

    queue: deque[TreeNode] = deque([root])

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
from typing import Optional

def flip_equiv(root1: Optional[TreeNode], root2: Optional[TreeNode]) -> bool:
    r"""
    Check if trees are flip equivalent.

    Trees are flip equivalent if we can make them identical
    by flipping some nodes (swapping left and right children).

    LeetCode 951: Flip Equivalent Binary Trees

    Time Complexity: $\mathcal{O}(\min(N_1, N_2))$ where $N_1$ and $N_2$ are the number of nodes in each tree. We essentially traverse matched pairs, short-circuiting on mismatch.
    Space Complexity: $\mathcal{O}(\min(H_1, H_2))$ where $H_1, H_2$ are the heights of the trees, bounding the recursive call stack length.
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
from typing import Optional

def merge_trees(root1: Optional[TreeNode], root2: Optional[TreeNode]) -> Optional[TreeNode]:
    r"""
    Merge two trees by summing overlapping nodes.

    LeetCode 617: Merge Two Binary Trees

    Time Complexity: $\mathcal{O}(\min(N_1, N_2))$ since we only traverse and compute where both trees have overlapping nodes.
    Space Complexity: $\mathcal{O}(\min(H_1, H_2))$ representing the maximum recursion depth, which stops at the shortest leaf traversal path among matching subtrees.
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

| Problem         | Time Complexity | Space Complexity | Notes                     |
| --------------- | --------------- | ---------------- | ------------------------- |
| Same Tree       | $\mathcal{O}(\min(N, M))$ | $\mathcal{O}(\min(H_1, H_2))$ | Stop at first mismatch    |
| Symmetric Tree  | $\Theta(N)$ | $\mathcal{O}(H)$ | Compare mirror pairs      |
| Subtree Check   | $\mathcal{O}(M \cdot N)$ | $\mathcal{O}(H_M + H_N)$ | $\Theta(M+N)$ with serialization |
| Invert Tree     | $\Theta(N)$ | $\mathcal{O}(H)$ | Visit all nodes           |
| Flip Equivalent | $\mathcal{O}(\min(N_1, N_2))$ | $\mathcal{O}(\min(H_1, H_2))$ | Branch on flip/no-flip    |
| Merge Trees     | $\mathcal{O}(\min(N_1, N_2))$ | $\mathcal{O}(\min(H_1, H_2))$ | Only overlapping nodes    |

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

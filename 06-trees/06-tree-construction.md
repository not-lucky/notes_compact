# Tree Construction

> **Prerequisites:** [02-tree-traversals](./02-tree-traversals.md)

## Building Intuition

**The Detective Puzzle Mental Model**: You're given clues (traversals) and must reconstruct the original tree. Each traversal gives different information:

```text
Preorder tells you: "Who is the root?"  (first element)
Inorder tells you:  "Who is left vs right of root?" (position relative to root)
Postorder tells you: "Who is the root?" (last element)
```

**Why you need TWO traversals**:
A single traversal can correspond to multiple different trees:

```text
Preorder [1, 2, 3] could be:      Inorder [1, 2, 3] could be:
    1           1                    1           2
   /             \                    \         / \
  2               2                    2       1   3
 /                 \                    \
3                   3                    3
```

But (preorder + inorder) or (postorder + inorder) uniquely determines the tree!

**The recursive construction insight**:

1. Find root from `preorder[0]` (or `postorder[-1]`)
2. Locate root in inorder → splits left/right subtrees
3. Calculate sizes → determine preorder/postorder ranges for subtrees
4. Recurse on left and right

```text
Preorder: [3, 9, 20, 15, 7]    Inorder: [9, 3, 15, 20, 7]
           ↑ root                         ↑ root position

Left subtree:  inorder[0:1] = [9]
Right subtree: inorder[2:5] = [15, 20, 7]

Recurse on each subtree!
```

**Why inorder is always needed**:

- Preorder/postorder can identify the root.
- Only inorder can tell us which nodes belong to the left vs. right subtree.
- Without inorder, we cannot determine subtree boundaries.

**The hashmap optimization**:
Finding a root in an array using `inorder.index(root_val)` takes $\mathcal{O}(n)$ per node, leading to $\mathcal{O}(n^2)$ total time. Instead, build a hashmap of `value -> index` beforehand to achieve $\Theta(1)$ lookups, reducing the total time to $\Theta(n)$.

---

## When NOT to Use

**Tree construction doesn't work when:**

- **Only one traversal given** → Multiple valid trees exist (unless special constraints).
- **Duplicate values exist** → Cannot uniquely locate the root in inorder.
- **Preorder + Postorder only** → Cannot determine left/right boundaries (for general Binary Trees).

**Special cases where one traversal suffices:**

- Full binary tree + preorder + postorder → Unique reconstruction possible.
- BST + one traversal → BST property constrains structure.
- Complete binary tree + level order → Positions are deterministic.

**Common mistake scenarios:**

- Forgetting to handle empty subtrees (`left_size = 0`).
- Off-by-one errors in slicing arrays or passing index boundaries.
- Not using a hashmap, resulting in Time Limit Exceeded (TLE) on large inputs.
- Assuming preorder + postorder works (it doesn't for general BT).

**When to use alternative approaches:**
| Input Given | Approach |
|-------------|----------|
| Level-order array | Build using index math: `left = 2*i + 1`, `right = 2*i + 2` |
| BST + any traversal | Use BST property to bound values (min/max bounds) |
| Serialized string | Parse with preorder-style DFS |
| Parent array | Build with hashmap of `parent -> list[children]` |

---

## Interview Context

Tree construction problems are important because:

1. **Tests deep understanding**: Requires knowing what makes traversals unique.
2. **Classic interview problem**: "Build tree from preorder and inorder" is very common.
3. **Divide and conquer**: Excellent example of recursive problem-solving.
4. **Multiple variations**: From inorder+preorder, inorder+postorder, level-order, etc.

This is a favorite at Google, Meta, and Amazon interviews.

---

## Core Insight: Why Two Traversals?

A single traversal is **not enough** to uniquely determine a binary tree.

```text
These different trees have the same preorder [1, 2, 3]:

    1           1
   /             \
  2               2
 /                 \
3                   3

But inorder differs: [3, 2, 1] vs [1, 2, 3]
```

**Key insight**: Inorder tells us which nodes are in left vs right subtree. Preorder or postorder tells us the root.

---

## TreeNode Definition

For the following code snippets to be runnable, we assume this `TreeNode` structure:

```python
from typing import Optional

class TreeNode:
    def __init__(self, val: int = 0, left: Optional['TreeNode'] = None, right: Optional['TreeNode'] = None):
        self.val = val
        self.left = left
        self.right = right
```

## Build from Preorder and Inorder

### The Algorithm

1. First element of preorder is the **root**
2. Find root in inorder → elements to left are left subtree, elements to right are right subtree
3. Recursively build left and right subtrees

```text
Preorder: [3, 9, 20, 15, 7]
Inorder:  [9, 3, 15, 20, 7]

Step 1: root = 3 (first in preorder)
Step 2: Find 3 in inorder at index 1
        Left subtree inorder: [9]
        Right subtree inorder: [15, 20, 7]
Step 3: Left subtree preorder: [9]
        Right subtree preorder: [20, 15, 7]
Step 4: Recurse

Result:
      3
     / \
    9  20
       / \
      15  7
```

### Implementation

```python
from typing import Optional

def build_tree(preorder: list[int], inorder: list[int]) -> Optional[TreeNode]:
    r"""
    Build tree from preorder and inorder traversals.

    LeetCode 105: Construct Binary Tree from Preorder and Inorder Traversal

    Time: $\Theta(n)$ as we visit each node once and hashmap lookups are $\mathcal{O}(1)$ average.
    Space: $\Theta(n)$ for the hashmap + $\mathcal{O}(h)$ for the recursion call stack,
           where $h$ is tree height. Worst-case space is $\mathcal{O}(n)$ total.
    """
    if not preorder or not inorder:
        return None

    # Build hashmap for O(1) index lookup
    inorder_map = {val: idx for idx, val in enumerate(inorder)}

    def build(pre_start: int, pre_end: int, in_start: int, in_end: int) -> Optional[TreeNode]:
        if pre_start > pre_end:
            return None

        # Root is first element in preorder range
        root_val = preorder[pre_start]
        root = TreeNode(root_val)

        # Find root in inorder
        root_idx = inorder_map[root_val]
        left_size = root_idx - in_start

        # Build subtrees
        root.left = build(
            pre_start + 1,
            pre_start + left_size,
            in_start,
            root_idx - 1
        )
        root.right = build(
            pre_start + left_size + 1,
            pre_end,
            root_idx + 1,
            in_end
        )

        return root

    return build(0, len(preorder) - 1, 0, len(inorder) - 1)
```

### Simplified Version (Creates New Arrays)

```python
def build_tree_simple(preorder: list[int], inorder: list[int]) -> Optional[TreeNode]:
    r"""
    Simpler but creates new arrays (less efficient).

    Time: $\mathcal{O}(n^2)$ worst-case due to array slicing and `index()` lookup.
    Space: $\mathcal{O}(n^2)$ worst-case due to new arrays created at each level of recursion.
    """
    if not inorder:
        return None

    root_val = preorder[0]
    root = TreeNode(root_val)

    root_idx = inorder.index(root_val)

    root.left = build_tree_simple(
        preorder[1:root_idx + 1],
        inorder[:root_idx]
    )
    root.right = build_tree_simple(
        preorder[root_idx + 1:],
        inorder[root_idx + 1:]
    )

    return root
```

---

## Build from Inorder and Postorder

### The Algorithm

Similar to preorder, but root is **last** element in postorder.

```text
Postorder: [9, 15, 7, 20, 3]
Inorder:   [9, 3, 15, 20, 7]

Root = 3 (last in postorder)
Left subtree (inorder): [9]
Right subtree (inorder): [15, 20, 7]

Result:
      3
     / \
    9  20
       / \
      15  7
```

### Implementation

```python
def build_tree_inorder_postorder(inorder: list[int], postorder: list[int]) -> Optional[TreeNode]:
    r"""
    Build tree from inorder and postorder traversals.

    LeetCode 106: Construct Binary Tree from Inorder and Postorder Traversal

    Time: $\Theta(n)$ for traversal and hashmap lookups.
    Space: $\Theta(n)$ for hashmap + $\mathcal{O}(h)$ call stack $\rightarrow \mathcal{O}(n)$ total.
    """
    if not inorder or not postorder:
        return None

    inorder_map = {val: idx for idx, val in enumerate(inorder)}

    def build(in_start: int, in_end: int, post_start: int, post_end: int) -> Optional[TreeNode]:
        if in_start > in_end:
            return None

        # Root is last element in postorder range
        root_val = postorder[post_end]
        root = TreeNode(root_val)

        root_idx = inorder_map[root_val]
        left_size = root_idx - in_start

        root.left = build(
            in_start,
            root_idx - 1,
            post_start,
            post_start + left_size - 1
        )
        root.right = build(
            root_idx + 1,
            in_end,
            post_start + left_size,
            post_end - 1
        )

        return root

    return build(0, len(inorder) - 1, 0, len(postorder) - 1)
```

---

## Build BST from Preorder

For a Binary Search Tree, we only need **preorder** because the BST property (left < root < right) provides ordering.

```python
def bst_from_preorder(preorder: list[int]) -> Optional[TreeNode]:
    r"""
    Construct BST from preorder traversal using min/max bounds.

    LeetCode 1008: Construct Binary Search Tree from Preorder Traversal

    Time: $\Theta(n)$ as each node is visited and placed correctly.
    Space: $\mathcal{O}(h)$ for the recursion call stack, worst case $\mathcal{O}(n)$ for a skewed tree.
    """
    if not preorder:
        return None

    idx = [0]  # Use list for mutable reference inside recursive function

    def build(min_val: float, max_val: float) -> Optional[TreeNode]:
        if idx[0] >= len(preorder):
            return None

        val = preorder[idx[0]]
        if val < min_val or val > max_val:
            return None

        idx[0] += 1
        node = TreeNode(val)
        node.left = build(min_val, val)
        node.right = build(val, max_val)
        return node

    return build(float('-inf'), float('inf'))
```

### Alternative: Using Stack

```python
def bst_from_preorder_stack(preorder: list[int]) -> Optional[TreeNode]:
    r"""
    Iterative BST construction from preorder using a monotonic decreasing stack.

    Time: $\Theta(n)$ since each node is pushed and popped at most once.
    Space: $\mathcal{O}(h)$ for the stack, which stores the rightmost path. Worst case $\mathcal{O}(n)$.
    """
    if not preorder:
        return None

    root = TreeNode(preorder[0])
    stack = [root]

    for val in preorder[1:]:
        node = TreeNode(val)

        if val < stack[-1].val:
            # Value is smaller, must be left child of the top element
            stack[-1].left = node
        else:
            # Value is larger, find the correct parent by popping smaller elements
            parent = stack[-1]
            while stack and val > stack[-1].val:
                parent = stack.pop()
            parent.right = node

        stack.append(node)

    return root
```

---

## Build BST from Sorted Array

```python
def sorted_array_to_bst(nums: list[int]) -> Optional[TreeNode]:
    r"""
    Convert sorted array to height-balanced BST.

    LeetCode 108: Convert Sorted Array to Binary Search Tree

    Uses middle element as root to ensure balance.

    Time: $\Theta(n)$ as every element is visited to form a node.
    Space: $\Theta(\log n)$ for the recursion call stack, since the tree is guaranteed to be balanced.
    """
    if not nums:
        return None

    def build(left: int, right: int) -> Optional[TreeNode]:
        if left > right:
            return None

        mid = (left + right) // 2
        node = TreeNode(nums[mid])
        node.left = build(left, mid - 1)
        node.right = build(mid + 1, right)
        return node

    return build(0, len(nums) - 1)
```

---

## Build from Level-Order (General BT)

```python
from collections import deque
from typing import Optional

def build_from_level_order(values: list[Optional[int]]) -> Optional[TreeNode]:
    r"""
    Build tree from level-order list (LeetCode array format).
    `None` represents missing nodes.

    Example: [1, 2, 3, None, 4] creates:
          1
         / \
        2   3
         \
          4

    Time: $\Theta(n)$ where $n$ is the length of the input array.
    Space: $\mathcal{O}(w)$ where $w$ is the maximum width of the tree, for the queue.
           Worst case $\mathcal{O}(n)$ space.
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
```

---

## Complexity Analysis

| Construction | Time | Space | Notes |
|---|---|---|---|
| Preorder + Inorder | $\Theta(n)$ | $\mathcal{O}(n)$ | Hashmap takes $\Theta(n)$ space, call stack $\mathcal{O}(h)$. |
| Postorder + Inorder | $\Theta(n)$ | $\mathcal{O}(n)$ | Hashmap takes $\Theta(n)$ space, call stack $\mathcal{O}(h)$. |
| BST from Preorder | $\Theta(n)$ | $\mathcal{O}(h)$ | Recursion/stack depth bounded by tree height $h$. |
| Sorted Array to BST | $\Theta(n)$ | $\Theta(\log n)$ | Guaranteed balanced tree result. |
| Level-order | $\Theta(n)$ | $\mathcal{O}(w)$ | Space bounded by max width $w$ of the tree (for the BFS queue). |

---

## Common Variations

### 1. Maximum Binary Tree

```python
def construct_maximum_binary_tree(nums: list[int]) -> Optional[TreeNode]:
    r"""
    Build tree where each root is max in its range.

    LeetCode 654: Maximum Binary Tree

    Time: $\mathcal{O}(n^2)$ worst-case if the array is sorted (finding max takes $\mathcal{O}(k)$ at each step).
          Average case is $\mathcal{O}(n \log n)$. (Can be optimized to $\mathcal{O}(n)$ using a monotonic stack).
    Space: $\mathcal{O}(n)$ worst-case for the call stack on a skewed tree.
    """
    if not nums:
        return None

    max_idx = nums.index(max(nums))
    root = TreeNode(nums[max_idx])
    root.left = construct_maximum_binary_tree(nums[:max_idx])
    root.right = construct_maximum_binary_tree(nums[max_idx + 1:])
    return root
```

### 2. Build Complete Binary Tree

```python
def insert_level_order(arr: list[Optional[int]], i: int = 0) -> Optional[TreeNode]:
    r"""
    Build complete binary tree from array indices.

    For node at index $i$:
    - Left child at $2i + 1$
    - Right child at $2i + 2$

    Time: $\Theta(n)$ where $n$ is the number of valid elements in the array.
    Space: $\mathcal{O}(h)$ for the recursion stack depth.
    """
    if i >= len(arr) or arr[i] is None:
        return None

    root = TreeNode(arr[i])
    root.left = insert_level_order(arr, 2 * i + 1)
    root.right = insert_level_order(arr, 2 * i + 2)
    return root
```

---

## Edge Cases

```python
# 1. Empty arrays
# -> Return None

# 2. Single element
preorder = [1]
inorder = [1]
# -> Single node tree

# 3. Skewed tree (worst-case call stack depth)
preorder = [1, 2, 3]
inorder = [3, 2, 1]  # Left skewed: h = n, Space = O(n)

# 4. All same values (invalid for typical BST)
# -> Clarify with interviewer about duplicate handling policies

# 5. Duplicate values in general BT construction
# -> Standard problem (Preorder+Inorder) assumes no duplicates, otherwise inorder hashmap fails.
```

---

## Interview Tips

1. **Draw it out**: Always draw the example before coding.
2. **Know the insight**: Preorder gives root, inorder gives partition.
3. **Use hashmap**: $\Theta(1)$ lookup for root index prevents $\mathcal{O}(n^2)$ time complexity.
4. **Track indices carefully**: Most bugs come from wrong index calculations (e.g. `left_size = root_idx - in_start`).
5. **BST is special**: Only need one traversal due to the ordering property acting as an implicit inorder traversal.

---

## Practice Problems

| # | Problem | Difficulty | Key Concept |
|---|---|---|---|
| 1 | Construct Binary Tree from Preorder and Inorder Traversal | Medium | Classic construction |
| 2 | Construct Binary Tree from Inorder and Postorder Traversal | Medium | Similar approach |
| 3 | Construct Binary Search Tree from Preorder Traversal | Medium | BST bounds |
| 4 | Convert Sorted Array to Binary Search Tree | Easy | Balanced BST |
| 5 | Maximum Binary Tree | Medium | Max element root |
| 6 | Convert Sorted List to Binary Search Tree | Medium | Slow-fast pointer / Inorder simulation |

---

## Key Takeaways

1. **Two traversals needed**: Inorder + (preorder OR postorder) for general BT.
2. **Preorder = root first**: First element is root.
3. **Postorder = root last**: Last element is root.
4. **Inorder = partition**: Tells which nodes are in left/right subtree.
5. **BST special case**: Only preorder needed (property bounds give structural constraints).

---

## Next: [07-lca-problems.md](./07-lca-problems.md)

Learn to find the Lowest Common Ancestor in trees.

# BST Operations

> **Prerequisites:** [01-tree-basics](./01-tree-basics.md)

## Building Intuition

**The Sorted Book Shelf Mental Model**: Imagine a bookshelf where every book on the left is "earlier" (alphabetically or numerically) than the book you're looking at, and every book on the right is "later". That's a BST!

```
Looking for "M" in a BST of letters:
      K
     / \
    D   P
   / \ / \
  A  F M  T

K < M → go right
P > M → go left
Found M!
```

**Why BST gives $\mathcal{O}(\log N)$ - the binary search insight**:
Each comparison eliminates half the remaining nodes. With $N$ nodes in a balanced tree:

- After 1 comparison: $N/2$ candidates
- After 2 comparisons: $N/4$ candidates
- After $\log_2(N)$ comparisons: 1 candidate

```
Search path for value X:
     Compare with root
           |
    ┌──────┴──────┐
  X < root      X > root
    |              |
  Go left       Go right
    |              |
  (half tree)   (half tree)
```

**The three deletion cases - visual intuition**:

```
Case 1: Leaf node        Case 2: One child       Case 3: Two children
  Delete 4                 Delete 3                Delete 5
      5                        5                       5
     / \                      / \                     / \
    3   7    →              3   7    →               3   7
   /   /                   /   /                    / \   \
  4   6                   1   6                    1   4   9
        (just remove)     └─(replace with child)  └─(replace with successor 6)
```

**The successor/predecessor insight**:

- **Inorder successor** = smallest value greater than current = leftmost node in right subtree
- **Inorder predecessor** = largest value smaller than current = rightmost node in left subtree

These are used in deletion (case 3) because they maintain the BST property when substituted.

---

## When NOT to Use

**Don't use a plain BST when:**

- **Data arrives in sorted order** → Tree becomes a linked list ($\mathcal{O}(N)$ operations)
- **Need $\mathcal{O}(1)$ lookups** → Use hash map instead
- **Data rarely changes** → Sorted array with binary search may be simpler
- **Need ordered iteration without tree overhead** → Use sorted array

**BST is overkill when:**

- Only need insertion order → Use array/list
- Data set is small → Linear search is fine
- No ordering requirements → Hash map is faster

**When to use self-balancing trees instead:**

- Production systems → Use AVL or Red-Black tree
- Insertions in sorted/reverse order → Plain BST degrades to $\mathcal{O}(N)$
- Guaranteed $\mathcal{O}(\log N)$ is critical → Balanced tree variants

**Common mistake scenarios:**

- Not considering tree balance in complexity analysis (assuming $\mathcal{O}(\log N)$ instead of worst-case $\mathcal{O}(N)$)
- Using BST when hash map would be simpler
- Forgetting that duplicate handling varies by implementation

**Performance comparison:**

| Structure | Search | Insert | Delete | Space |
|-----------|--------|--------|--------|-------|
| BST (balanced) | $\mathcal{O}(\log N)$ | $\mathcal{O}(\log N)$ | $\mathcal{O}(\log N)$ | $\mathcal{O}(N)$ |
| BST (skewed) | $\mathcal{O}(N)$ | $\mathcal{O}(N)$ | $\mathcal{O}(N)$ | $\mathcal{O}(N)$ |
| Hash Map | $\mathcal{O}(1)$ avg | $\mathcal{O}(1)$ avg | $\mathcal{O}(1)$ avg | $\mathcal{O}(N)$ |
| Sorted Array | $\mathcal{O}(\log N)$ | $\mathcal{O}(N)$ | $\mathcal{O}(N)$ | $\mathcal{O}(N)$ |

*Note: Hash map space is total auxiliary space. BST has recursion space bounded by height $\mathcal{O}(H)$, which is $\mathcal{O}(N)$ in the worst case.*

---

## Interview Context

BST operations are fundamental because:

1. **Core data structure**: BSTs are basis for many advanced structures (AVL, Red-Black trees)
2. **Efficient search**: $\mathcal{O}(\log N)$ operations in balanced trees
3. **High frequency**: Search, insert, delete are common interview problems
4. **Recursive thinking**: Clean recursive solutions demonstrate mastery

Interviewers use BST problems to test your understanding of the BST property and tree manipulation.

---

## Core Concept: BST Property

A Binary Search Tree maintains this invariant for every node:

- All values in **left subtree < node value**
- All values in **right subtree > node value**

```
Valid BST:          Invalid BST:
      5                  5
     / \                / \
    3   7              3   7
   / \   \            / \   \
  1   4   9          1   6   9  ← 6 > 5 but in left subtree
```

---

## BST Search

### Recursive Search

```python
from typing import Optional

def search_bst(root: Optional[TreeNode], val: int) -> Optional[TreeNode]:
    r"""
    Search for value in BST.

    LeetCode 700: Search in a Binary Search Tree

    Time: $\mathcal{O}(H)$ - $H$ is height, $\mathcal{O}(\log N)$ balanced, $\mathcal{O}(N)$ skewed
    Space: $\mathcal{O}(H)$ - recursion stack
    """
    if not root or root.val == val:
        return root

    if val < root.val:
        return search_bst(root.left, val)
    else:
        return search_bst(root.right, val)
```

### Iterative Search

```python
from typing import Optional

def search_bst_iterative(root: Optional[TreeNode], val: int) -> Optional[TreeNode]:
    r"""
    Iterative BST search - $\mathcal{O}(1)$ space.

    Time: $\mathcal{O}(H)$
    Space: $\mathcal{O}(1)$ auxiliary space
    """
    while root and root.val != val:
        if val < root.val:
            root = root.left
        else:
            root = root.right

    return root
```

---

## BST Insert

### Recursive Insert

```python
from typing import Optional

def insert_into_bst(root: Optional[TreeNode], val: int) -> Optional[TreeNode]:
    r"""
    Insert value into BST, return root.

    LeetCode 701: Insert into a Binary Search Tree

    Time: $\mathcal{O}(H)$
    Space: $\mathcal{O}(H)$ recursion stack
    """
    if not root:
        return TreeNode(val)

    if val < root.val:
        root.left = insert_into_bst(root.left, val)
    else:
        root.right = insert_into_bst(root.right, val)

    return root
```

### Iterative Insert

```python
from typing import Optional

def insert_into_bst_iterative(root: Optional[TreeNode], val: int) -> Optional[TreeNode]:
    r"""
    Iterative BST insert - $\mathcal{O}(1)$ space.

    Time: $\mathcal{O}(H)$
    Space: $\mathcal{O}(1)$ auxiliary space
    """
    new_node = TreeNode(val)

    if not root:
        return new_node

    current = root
    while True:
        if val < current.val:
            if not current.left:
                current.left = new_node
                break
            current = current.left
        else:
            if not current.right:
                current.right = new_node
                break
            current = current.right

    return root
```

### Visual Walkthrough: Insert 6

```
Before:          After:
      5              5
     / \            / \
    3   7          3   7
       / \            / \
      6   9          6   9

Insert 6:
1. 6 > 5 → go right
2. 6 < 7 → go left
3. 7.left is null → insert here
```

---

## BST Delete

This is the most complex BST operation with three cases.

### Three Cases for Deletion

```
Case 1: Node is leaf (no children)
  → Simply remove it

      5                 5
     / \               / \
    3   7    delete   3   7
   /     \   3.left     \
  1       9   →          9

Case 2: Node has one child
  → Replace node with its child

      5                 5
     / \               / \
    3   7    delete   1   7
   /     \   3          \
  1       9   →          9

Case 3: Node has two children
  → Replace with inorder successor (or predecessor)
  → Then delete the successor

      5                 6
     / \               / \
    3   7    delete   3   7
       / \   5           \
      6   9   →           9
```

### Implementation

```python
from typing import Optional

def delete_node(root: Optional[TreeNode], key: int) -> Optional[TreeNode]:
    r"""
    Delete node with given key from BST.

    LeetCode 450: Delete Node in a BST

    Time: $\mathcal{O}(H)$
    Space: $\mathcal{O}(H)$ recursion stack
    """
    if not root:
        return None

    if key < root.val:
        root.left = delete_node(root.left, key)
    elif key > root.val:
        root.right = delete_node(root.right, key)
    else:
        # Found the node to delete

        # Case 1 & 2: No left child
        if not root.left:
            return root.right

        # Case 2: No right child
        if not root.right:
            return root.left

        # Case 3: Two children
        # Find inorder successor (smallest in right subtree)
        successor = find_min(root.right)
        root.val = successor.val
        root.right = delete_node(root.right, successor.val)

    return root


def find_min(node: TreeNode) -> TreeNode:
    """Find minimum value node (leftmost)."""
    while node.left:
        node = node.left
    return node
```

### Alternative: Use Predecessor Instead

```python
from typing import Optional

def delete_node_predecessor(root: Optional[TreeNode], key: int) -> Optional[TreeNode]:
    """Delete using inorder predecessor (largest in left subtree)."""
    if not root:
        return None

    if key < root.val:
        root.left = delete_node_predecessor(root.left, key)
    elif key > root.val:
        root.right = delete_node_predecessor(root.right, key)
    else:
        if not root.left:
            return root.right
        if not root.right:
            return root.left

        # Find predecessor (rightmost in left subtree)
        predecessor = root.left
        while predecessor.right:
            predecessor = predecessor.right

        root.val = predecessor.val
        root.left = delete_node_predecessor(root.left, predecessor.val)

    return root
```

---

## Find Min and Max

```python
from typing import Optional

def find_minimum(root: Optional[TreeNode]) -> Optional[int]:
    r"""
    Find minimum value in BST.

    Time: $\mathcal{O}(H)$
    Space: $\mathcal{O}(1)$ auxiliary space
    """
    if not root:
        return None

    while root.left:
        root = root.left
    return root.val


def find_maximum(root: Optional[TreeNode]) -> Optional[int]:
    r"""
    Find maximum value in BST.

    Time: $\mathcal{O}(H)$
    Space: $\mathcal{O}(1)$ auxiliary space
    """
    if not root:
        return None

    while root.right:
        root = root.right
    return root.val
```

---

## Find Floor and Ceiling

```python
from typing import Optional

def floor(root: Optional[TreeNode], key: int) -> Optional[int]:
    r"""
    Find largest value <= key.

    Time: $\mathcal{O}(H)$
    Space: $\mathcal{O}(1)$ auxiliary space
    """
    floor_val = None

    while root:
        if root.val == key:
            return key
        elif root.val < key:
            floor_val = root.val  # Potential floor
            root = root.right
        else:
            root = root.left

    return floor_val


def ceiling(root: Optional[TreeNode], key: int) -> Optional[int]:
    r"""
    Find smallest value >= key.

    Time: $\mathcal{O}(H)$
    Space: $\mathcal{O}(1)$ auxiliary space
    """
    ceil_val = None

    while root:
        if root.val == key:
            return key
        elif root.val > key:
            ceil_val = root.val  # Potential ceiling
            root = root.left
        else:
            root = root.right

    return ceil_val
```

---

## Inorder Successor and Predecessor

```python
from typing import Optional

def inorder_successor(root: Optional[TreeNode], p: TreeNode) -> Optional[TreeNode]:
    r"""
    Find inorder successor of node p.

    LeetCode 285: Inorder Successor in BST

    Time: $\mathcal{O}(H)$
    Space: $\mathcal{O}(1)$ auxiliary space
    """
    successor = None

    while root:
        if p.val < root.val:
            successor = root  # Potential successor
            root = root.left
        else:
            root = root.right

    return successor


def inorder_predecessor(root: Optional[TreeNode], p: TreeNode) -> Optional[TreeNode]:
    """Find inorder predecessor of node p."""
    predecessor = None

    while root:
        if p.val > root.val:
            predecessor = root  # Potential predecessor
            root = root.right
        else:
            root = root.left

    return predecessor
```

---

## Complexity Analysis

| Operation | Average  | Worst (Skewed) | Space                |
| --------- | -------- | -------------- | -------------------- |
| Search    | $\mathcal{O}(\log N)$ | $\mathcal{O}(N)$           | $\mathcal{O}(1)$ iter / $\mathcal{O}(H)$ rec |
| Insert    | $\mathcal{O}(\log N)$ | $\mathcal{O}(N)$           | $\mathcal{O}(1)$ iter / $\mathcal{O}(H)$ rec |
| Delete    | $\mathcal{O}(\log N)$ | $\mathcal{O}(N)$           | $\mathcal{O}(H)$                 |
| Min/Max   | $\mathcal{O}(\log N)$ | $\mathcal{O}(N)$           | $\mathcal{O}(1)$                 |
| Successor | $\mathcal{O}(\log N)$ | $\mathcal{O}(N)$           | $\mathcal{O}(1)$                 |

Key insight: Performance degrades to $\mathcal{O}(N)$ if the tree becomes skewed. Self-balancing trees (AVL, Red-Black) maintain $\mathcal{O}(\log N)$. Ensure you specify that the recursive space complexity is related to the tree height $\mathcal{O}(H)$.

---

## Common Variations

### 1. Count Nodes in Range

```python
from typing import Optional

def count_in_range(root: Optional[TreeNode], low: int, high: int) -> int:
    r"""
    Count nodes with values in [low, high].

    Time: $\mathcal{O}(N)$ worst, $\mathcal{O}(\log N + K)$ average where K is nodes in range
    Space: $\mathcal{O}(H)$ recursion stack
    """
    if not root:
        return 0

    if root.val < low:
        return count_in_range(root.right, low, high)
    if root.val > high:
        return count_in_range(root.left, low, high)

    # root.val in range
    return (1 +
            count_in_range(root.left, low, high) +
            count_in_range(root.right, low, high))
```

### 2. Range Sum BST

```python
from typing import Optional

def range_sum_bst(root: Optional[TreeNode], low: int, high: int) -> int:
    r"""
    Sum of values in [low, high].

    LeetCode 938: Range Sum of BST

    Time: $\mathcal{O}(N)$ worst, $\mathcal{O}(\log N + K)$ average where K is nodes in range
    Space: $\mathcal{O}(H)$ recursion stack
    """
    if not root:
        return 0

    if root.val < low:
        return range_sum_bst(root.right, low, high)
    if root.val > high:
        return range_sum_bst(root.left, low, high)

    return (root.val +
            range_sum_bst(root.left, low, high) +
            range_sum_bst(root.right, low, high))
```

---

## Edge Cases

```python
# 1. Empty tree
root = None
# → Search returns None, Insert creates root

# 2. Single node
root = TreeNode(5)
delete_node(root, 5)  # Returns None

# 3. Delete root with two children
#      5
#     / \
#    3   7
# delete 5 → successor is 7, or predecessor is 3

# 4. Value not found
search_bst(root, 100)  # Returns None

# 5. Duplicate handling
# Standard BST: no duplicates, or put in right subtree
```

---

## Interview Tips

1. **Know all three operations**: Search, insert, delete must be second nature
2. **Understand delete cases**: Three cases - practice drawing them
3. **Iterative for space**: Use iterative versions when $\mathcal{O}(1)$ space needed
4. **Successor/predecessor**: Common follow-up questions
5. **Discuss balance**: Mention that balanced trees give $\mathcal{O}(\log N)$ guarantee

---

## Practice Problems

| #   | Problem                          | Difficulty | Key Concept       |
| --- | -------------------------------- | ---------- | ----------------- |
| 1   | Search in a Binary Search Tree   | Easy       | Basic search      |
| 2   | Insert into a Binary Search Tree | Medium     | Basic insert      |
| 3   | Delete Node in a BST             | Medium     | Delete with cases |
| 4   | Inorder Successor in BST         | Medium     | Successor finding |
| 5   | Range Sum of BST                 | Easy       | Range query       |
| 6   | Closest Binary Search Tree Value | Easy       | Floor/ceiling     |
| 7   | Trim a Binary Search Tree        | Medium     | Range pruning     |

---

## Key Takeaways

1. **BST property**: Left < Root < Right at every node
2. **$\mathcal{O}(\log N)$ when balanced**: Operations degrade to $\mathcal{O}(N)$ if skewed
3. **Delete is hardest**: Three cases based on number of children
4. **Successor/predecessor**: Key for delete and range queries
5. **Iterative saves space**: When $\mathcal{O}(1)$ space is required

---

## Next: [05-validate-bst](./05-validate-bst.md)

Learn how to validate if a tree is a valid BST.

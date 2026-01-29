# Tree Basics Solutions

## 1. Maximum Depth of Binary Tree

**Problem Statement**: Given the root of a binary tree, return its maximum depth. A binary tree's maximum depth is the number of nodes along the longest path from the root node down to the farthest leaf node.

### Examples & Edge Cases

- **Example 1**: `root = [3,9,20,None,None,15,7]` → Output: 3
- **Example 2**: `root = [1,None,2]` → Output: 2
- **Edge Case - Empty Tree**: `root = None` → Output: 0
- **Edge Case - Single Node**: `root = [1]` → Output: 1
- **Edge Case - Skewed Tree**: `root = [1,2,3,4,5]` → Output: 5

### Optimal Python Solution

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def maxDepth(root: TreeNode) -> int:
    # Base Case: If the tree is empty, depth is 0
    if not root:
        return 0

    # Recursively find the height of left and right subtrees
    left_height = maxDepth(root.left)
    right_height = maxDepth(root.right)

    # The height of the current node is 1 + the maximum height of its children
    return 1 + max(left_height, right_height)
```

### Explanation

1.  **Base Case**: If the current node is `None`, it means we've reached past a leaf. We return `0`.
2.  **Recursive Step**: For every non-null node, we ask its left child for its height and its right child for its height.
3.  **Aggregation**: We take the maximum of those two heights and add `1` (for the current node itself) to get the depth at this level.
4.  **Bottom-up**: The values bubble up from the leaves to the root.

### Complexity Analysis

- **Time Complexity**: **O(n)**. We visit every node exactly once to determine the height of the tree.
- **Space Complexity**: **O(h)**. In the worst case (a skewed tree), the recursion stack will contain `n` calls. In a balanced tree, it will be `O(log n)`.

---

## 2. Invert Binary Tree

**Problem Statement**: Given the root of a binary tree, invert the tree, and return its root. Inverting a tree means swapping every left and right child for all nodes.

### Examples & Edge Cases

- **Example 1**: `root = [4,2,7,1,3,6,9]` → Output: `[4,7,2,9,6,3,1]`
- **Example 2**: `root = [2,1,3]` → Output: `[2,3,1]`
- **Edge Case - Empty Tree**: `root = None` → Output: `None`
- **Edge Case - Single Node**: `root = [1]` → Output: `[1]`

### Optimal Python Solution

```python
def invertTree(root: TreeNode) -> TreeNode:
    # Base Case: If node is None, nothing to invert
    if not root:
        return None

    # Swap the left and right children
    root.left, root.right = root.right, root.left

    # Recursively invert the subtrees
    invertTree(root.left)
    invertTree(root.right)

    return root
```

### Explanation

1.  **Top-Down Swap**: We start at the root and swap its left and right child pointers.
2.  **Recursion**: We then call the same function on the now-swapped left child and right child.
3.  **Completion**: Once the recursion reaches the leaves, all children at all levels will have been swapped.

### Complexity Analysis

- **Time Complexity**: **O(n)**. We visit every node exactly once to perform the swap operation.
- **Space Complexity**: **O(h)**. The space used by the recursion stack is proportional to the height of the tree.

---

## 3. Same Tree

**Problem Statement**: Given the roots of two binary trees `p` and `q`, write a function to check if they are the same or not. Two binary trees are considered the same if they are structurally identical, and the nodes have the same value.

### Examples & Edge Cases

- **Example 1**: `p = [1,2,3], q = [1,2,3]` → Output: `true`
- **Example 2**: `p = [1,2], q = [1,None,2]` → Output: `false`
- **Edge Case - Both Empty**: `p = None, q = None` → Output: `true`
- **Edge Case - One Empty**: `p = [1], q = None` → Output: `false`

### Optimal Python Solution

```python
def isSameTree(p: TreeNode, q: TreeNode) -> bool:
    # If both nodes are null, they are the same
    if not p and not q:
        return True

    # If one is null and the other isn't, or values differ, they aren't the same
    if not p or not q or p.val != q.val:
        return False

    # Recursively check left subtrees and right subtrees
    return isSameTree(p.left, q.left) and isSameTree(p.right, q.right)
```

### Explanation

1.  **Identity Check**: If both nodes are `None`, we've successfully matched this path.
2.  **Structural/Value Mismatch**: If one node exists but the other doesn't, or if the values stored in the nodes are different, the trees are not identical.
3.  **Recursive Conjunction**: The trees are the same ONLY if the current nodes are the same AND the left subtrees are the same AND the right subtrees are the same.

### Complexity Analysis

- **Time Complexity**: **O(min(n, m))**. We traverse both trees until we find a mismatch or reach the end of the smaller tree.
- **Space Complexity**: **O(min(h1, h2))**. The recursion stack size is determined by the height of the shorter tree.

---

## 4. Count Complete Tree Nodes

**Problem Statement**: Given the root of a **complete** binary tree, return the number of nodes in the tree. A complete binary tree is a binary tree in which every level, except possibly the last, is completely filled, and all nodes in the last level are as far left as possible.

### Examples & Edge Cases

- **Example 1**: `root = [1,2,3,4,5,6]` → Output: 6
- **Example 2**: `root = []` → Output: 0
- **Edge Case - Perfect Tree**: Every level is full.
- **Edge Case - Single Node**: Output: 1

### Optimal Python Solution

```python
def countNodes(root: TreeNode) -> int:
    if not root:
        return 0

    def get_height(node):
        h = 0
        while node:
            h += 1
            node = node.left
        return h

    left_h = get_height(root.left)
    right_h = get_height(root.right)

    if left_h == right_h:
        # Left subtree is a perfect binary tree of height left_h
        # Total nodes = (nodes in left) + (root) + (recurse on right)
        # nodes in perfect tree = 2^h - 1. Here (2^left_h - 1) + 1 = 2^left_h
        return (1 << left_h) + countNodes(root.right)
    else:
        # Right subtree is a perfect binary tree of height right_h (one less than left)
        return (1 << right_h) + countNodes(root.left)
```

### Explanation

1.  **Exploiting Completeness**: In a complete tree, we can determine if a subtree is "perfect" by comparing heights.
2.  **Height Calculation**: We always go left to find the height in $O(h)$ time.
3.  **Decision**:
    - If `left_h == right_h`, the left subtree is perfect. We can calculate its node count using the formula $2^{height}$ and recurse on the right.
    - If `left_h > right_h`, the right subtree is perfect (but one level shorter). We calculate its count and recurse on the left.
4.  **Binary Search logic**: In each step, we discard half the tree, leading to $O(h^2)$ total time.

### Complexity Analysis

- **Time Complexity**: **O(log² n)**. We perform a height calculation ($O(\log n)$) at each level of the tree ($O(\log n)$ levels).
- **Space Complexity**: **O(log n)**. This is the space used by the recursion stack.

---

## 5. Subtree of Another Tree

**Problem Statement**: Given the roots of two binary trees `root` and `subRoot`, return `true` if there is a subtree of `root` with the same structure and node values of `subRoot` and `false` otherwise.

### Examples & Edge Cases

- **Example 1**: `root = [3,4,5,1,2], subRoot = [4,1,2]` → Output: `true`
- **Example 2**: `root = [3,4,5,1,2,None,None,None,None,0], subRoot = [4,1,2]` → Output: `false`
- **Edge Case - subRoot is empty**: Technically every tree has a null subtree, but problem usually specifies non-null.
- **Edge Case - Identical Trees**: A tree is a subtree of itself.

### Optimal Python Solution

```python
def isSubtree(root: TreeNode, subRoot: TreeNode) -> bool:
    if not subRoot: return True # Empty tree is always a subtree
    if not root: return False    # Non-empty subRoot cannot be in empty root

    # Check if the trees starting at current nodes are identical
    if isSame(root, subRoot):
        return True

    # Otherwise, check if subRoot is in the left or right subtrees
    return isSubtree(root.left, subRoot) or isSubtree(root.right, subRoot)

def isSame(s, t):
    if not s and not t: return True
    if not s or not t or s.val != t.val: return False
    return isSame(s.left, t.left) and isSame(s.right, t.right)
```

### Explanation

1.  **Main Function**: We traverse `root` using DFS. At each node, we call `isSame` to see if the subtree starting there matches `subRoot`.
2.  **Identity Check**: `isSame` is the standard "Same Tree" algorithm.
3.  **Recursive Search**: If the current node doesn't match, we search the left and right children.

### Complexity Analysis

- **Time Complexity**: **O(n \* m)**. In the worst case, for every node in `root` (n nodes), we might traverse all nodes in `subRoot` (m nodes).
- **Space Complexity**: **O(h)**. The recursion depth is bounded by the height of the `root` tree.

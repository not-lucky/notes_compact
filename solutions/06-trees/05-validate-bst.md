# Validate BST Solutions

## 1. Validate Binary Search Tree

**Problem Statement**: Given the `root` of a binary tree, determine if it is a valid binary search tree (BST).

### Examples & Edge Cases

- **Example 1**: `root = [2,1,3]` → Output: `true`
- **Example 2**: `root = [5,1,4,None,None,3,6]` → Output: `false` (3 is in the right subtree of 5 but is less than 5)
- **Edge Case - Min/Max values**: Tree contains `2^31 - 1` or `-2^31`.
- **Edge Case - Duplicates**: `[2,2,2]` should return `false`.

### Optimal Python Solution

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def isValidBST(root: TreeNode) -> bool:
    def validate(node, low, high):
        if not node:
            return True

        # Check the BST invariant for the current node
        if not (low < node.val < high):
            return False

        # Validate children with updated constraints
        return (validate(node.left, low, node.val) and
                validate(node.right, node.val, high))

    # Initialize with global infinity bounds
    return validate(root, float('-inf'), float('inf'))
```

### Explanation

1.  **Naive Fallacy**: A common mistake is to only check if `left < root < right`. This is insufficient because a node in the right subtree must be greater than its parent AND all ancestors that the parent was a right-child of.
2.  **Range Technique**: We define a valid range `(low, high)` for every node.
3.  **Propagation**:
    - For the **left child**, the value must be less than the current node's value. Thus, the new `high` bound is `node.val`.
    - For the **right child**, the value must be greater than the current node's value. Thus, the new `low` bound is `node.val`.
4.  **Consistency**: If any node falls outside its range, the entire tree is invalid.

### Complexity Analysis

- **Time Complexity**: **O(n)**. Every node is visited once.
- **Space Complexity**: **O(h)**. The depth of the recursion stack is determined by the height of the tree.

---

## 2. Recover Binary Search Tree

**Problem Statement**: You are given the `root` of a binary search tree (BST), where the values of **exactly two nodes** were swapped by mistake. Recover the tree without changing its structure.

### Examples & Edge Cases

- **Example 1**: `root = [1,3,None,None,2]` → Output: `[3,1,None,None,2]` (Inorder before: `[3,2,1]`, Inorder after: `[1,2,3]`)
- **Edge Case - Adjacent Swaps**: Two nodes were neighbors in inorder traversal.
- **Edge Case - Non-adjacent Swaps**: Swapped nodes are far apart.

### Optimal Python Solution

```python
def recoverTree(root: TreeNode) -> None:
    first = second = prev = None

    def inorder(node):
        nonlocal first, second, prev
        if not node:
            return

        inorder(node.left)

        # Check if the current value is less than the previous (violation)
        if prev and node.val < prev.val:
            # If this is the first violation, 'first' is the prev node
            if not first:
                first = prev
            # 'second' is always updated to the current node
            second = node

        prev = node
        inorder(node.right)

    inorder(root)
    # Swap values of the two identified nodes
    first.val, second.val = second.val, first.val
```

### Explanation

1.  **Inorder Insight**: In a sorted array, if you swap two elements, you will see one or two "dips" where an element is smaller than the one before it.
    - Example: `[1, 2, 3, 4, 5]` → swap 2 and 5 → `[1, 5, 3, 4, 2]`.
    - Violations: `5 > 3` (first) and `4 > 2` (second).
    - To fix: The first node involved is the _larger_ of the first violation (`5`), and the second node is the _smaller_ of the last violation (`2`).
2.  **Detection**: We perform an inorder traversal and track the `prev` node.
3.  **Repair**: We identify the two nodes (`first` and `second`) and swap their values.

### Complexity Analysis

- **Time Complexity**: **O(n)**. One full inorder traversal.
- **Space Complexity**: **O(h)**. Recursion stack. (Can be O(1) using Morris traversal).

---

## 3. Largest BST Subtree

**Problem Statement**: Given the root of a binary tree, find the largest subtree, which is also a Binary Search Tree (BST), where the largest means subtree has the largest number of nodes in it.

### Optimal Python Solution

```python
def largestBSTSubtree(root: TreeNode) -> int:
    max_size = 0

    def dfs(node):
        nonlocal max_size
        if not node:
            # (is_bst, size, min_val, max_val)
            return True, 0, float('inf'), float('-inf')

        left_is_bst, left_size, left_min, left_max = dfs(node.left)
        right_is_bst, right_size, right_min, right_max = dfs(node.right)

        # Current node is a BST if left/right are BSTs and value fits range
        if left_is_bst and right_is_bst and left_max < node.val < right_min:
            size = 1 + left_size + right_size
            max_size = max(max_size, size)
            # Return current min and max for parents to use
            return True, size, min(node.val, left_min), max(node.val, right_max)

        # Not a BST
        return False, 0, 0, 0

    dfs(root)
    return max_size
```

### Explanation

1.  **Bottom-Up DFS**: We need info from children to decide if the current node is a root of a BST.
2.  **State**: Each call returns:
    - If the subtree is a BST.
    - The size of that subtree.
    - The minimum and maximum values found in that subtree.
3.  **Validation**: A node is a root of a BST if `left_is_bst` is true, `right_is_bst` is true, AND `node.val` is strictly between the largest value on the left and the smallest value on the right.

### Complexity Analysis

- **Time Complexity**: **O(n)**. Single post-order traversal.
- **Space Complexity**: **O(h)**.

---

## 4. Minimum Distance Between BST Nodes

**Problem Statement**: Given the root of a Binary Search Tree (BST), return the minimum difference between the values of any two different nodes in the tree.

### Optimal Python Solution

```python
def minDiffInBST(root: TreeNode) -> int:
    prev = None
    min_diff = float('inf')

    def inorder(node):
        nonlocal prev, min_diff
        if not node:
            return

        inorder(node.left)

        # Inorder visits nodes in sorted order
        # Minimum difference must be between adjacent nodes in sorted order
        if prev is not None:
            min_diff = min(min_diff, node.val - prev)
        prev = node.val

        inorder(node.right)

    inorder(root)
    return min_diff
```

### Complexity Analysis

- **Time Complexity**: **O(n)**.
- **Space Complexity**: **O(h)**.

---

## 5. Two Sum IV - Input is a BST

**Problem Statement**: Given the root of a Binary Search Tree and a target number `k`, return `true` if there exist two elements in the BST such that their sum is equal to the given target.

### Optimal Python Solution

```python
def findTarget(root: TreeNode, k: int) -> bool:
    seen = set()

    def dfs(node):
        if not node:
            return False

        # Two-sum logic: if (k - val) is in set, we found a pair
        if (k - node.val) in seen:
            return True

        seen.add(node.val)

        return dfs(node.left) or dfs(node.right)

    return dfs(root)
```

### Explanation

1.  **Standard Two-Sum**: We use a hash set to track values we've already visited.
2.  **Traversal**: Since we just need _any_ two nodes, a standard DFS (preorder/inorder doesn't matter) is fine.
3.  **Property**: While we can use the BST property with two iterators (one starting from smallest, one from largest), the hash set approach is simple and $O(n)$ time.

### Complexity Analysis

- **Time Complexity**: **O(n)**.
- **Space Complexity**: **O(n)**. We store all values in a set.

# Symmetric Tree and Same Tree Solutions

## 1. Same Tree

**Problem Statement**: Given the roots of two binary trees `p` and `q`, check if they are the same. Two binary trees are the same if they are structurally identical and the nodes have the same value.

### Examples & Edge Cases

- **Example 1**: `p = [1,2,3], q = [1,2,3]` → Output: `true`
- **Example 2**: `p = [1,2], q = [1,None,2]` → Output: `false`
- **Edge Case - Both Empty**: `true`
- **Edge Case - One Empty**: `false`

### Optimal Python Solution

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def isSameTree(p: TreeNode, q: TreeNode) -> bool:
    # If both are null, they are identical
    if not p and not q:
        return True

    # If one is null and other is not, or values mismatch, they are different
    if not p or not q or p.val != q.val:
        return False

    # Recursively check structure and values of subtrees
    return isSameTree(p.left, q.left) and isSameTree(p.right, q.right)
```

### Explanation

1.  **Identity Base Case**: If we reach the end of both trees simultaneously (`None`), that path is identical.
2.  **Structural/Value Mismatch**: If one tree has a node where the other has `None`, or if the values differ, the trees are not the same.
3.  **Recursive Conjunction**: Both the left branch AND the right branch must be identical for the whole tree to be identical.

### Complexity Analysis

- **Time Complexity**: **O(min(n, m))**. We visit each node in the smaller tree once.
- **Space Complexity**: **O(min(h1, h2))**. The recursion stack depth.

---

## 2. Symmetric Tree

**Problem Statement**: Given the `root` of a binary tree, check whether it is a mirror of itself (i.e., symmetric around its center).

### Examples & Edge Cases

- **Example 1**: `root = [1,2,2,3,4,4,3]` → Output: `true`
- **Example 2**: `root = [1,2,2,None,3,None,3]` → Output: `false`
- **Edge Case - Single Node**: `true`

### Optimal Python Solution

```python
def isSymmetric(root: TreeNode) -> bool:
    if not root:
        return True

    def isMirror(t1, t2):
        # Both null is symmetric
        if not t1 and not t2:
            return True
        # One null or value mismatch is asymmetric
        if not t1 or not t2 or t1.val != t2.val:
            return False

        # Crucial: Compare t1's LEFT with t2's RIGHT (outer)
        # And t1's RIGHT with t2's LEFT (inner)
        return isMirror(t1.left, t2.right) and isMirror(t1.right, t2.left)

    return isMirror(root.left, root.right)
```

### Explanation

1.  **Mirror Definition**: Two trees are mirrors if:
    - Their roots have the same value.
    - The left child of the first tree is a mirror of the right child of the second tree.
    - The right child of the first tree is a mirror of the left child of the second tree.
2.  **Implementation**: We create a helper function that takes two nodes and checks the mirror properties recursively.

### Complexity Analysis

- **Time Complexity**: **O(n)**. We visit every node in the tree once.
- **Space Complexity**: **O(h)**.

---

## 3. Subtree of Another Tree

**Problem Statement**: Check if `subRoot` is a subtree of `root`.

### Optimal Python Solution

```python
def isSubtree(root: TreeNode, subRoot: TreeNode) -> bool:
    if not subRoot: return True
    if not root: return False

    # 1. Check if they are identical starting here
    if isSameTree(root, subRoot):
        return True

    # 2. Otherwise search left and right children
    return isSubtree(root.left, subRoot) or isSubtree(root.right, subRoot)

def isSameTree(p, q):
    if not p and not q: return True
    if not p or not q or p.val != q.val: return False
    return isSameTree(p.left, q.left) and isSameTree(p.right, q.right)
```

### Complexity Analysis

- **Time Complexity**: **O(n \* m)**. In the worst case, we check `isSameTree` ($O(m)$) for every node in `root` ($n$ nodes).
- **Space Complexity**: **O(h)**.

---

## 4. Invert Binary Tree

**Problem Statement**: Invert a binary tree (swap all left and right children).

### Optimal Python Solution

```python
def invertTree(root: TreeNode) -> TreeNode:
    if not root:
        return None

    # Swap children
    root.left, root.right = root.right, root.left

    # Recurse
    invertTree(root.left)
    invertTree(root.right)

    return root
```

### Complexity Analysis

- **Time Complexity**: **O(n)**.
- **Space Complexity**: **O(h)**.

---

## 5. Flip Equivalent Binary Trees

**Problem Statement**: Two binary trees are flip equivalent if we can make them identical by flipping some nodes (swapping left and right children).

### Optimal Python Solution

```python
def flipEquiv(root1: TreeNode, root2: TreeNode) -> bool:
    if not root1 and not root2:
        return True
    if not root1 or not root2 or root1.val != root2.val:
        return False

    # Check two cases:
    # 1. The children were NOT flipped (left matches left, right matches right)
    # 2. The children WERE flipped (left matches right, right matches left)
    return (flipEquiv(root1.left, root2.left) and flipEquiv(root1.right, root2.right)) or \
           (flipEquiv(root1.left, root2.right) and flipEquiv(root1.right, root2.left))
```

### Explanation

- This is a variation of the `isSameTree` problem.
- Instead of just checking `left==left` and `right==right`, we also check `left==right` and `right==left` as a valid "flip" possibility.

### Complexity Analysis

- **Time Complexity**: **O(min(n1, n2))**.
- **Space Complexity**: **O(min(h1, h2))**.

---

## 6. Merge Two Binary Trees

**Problem Statement**: Merge two trees. If two nodes overlap, sum their values. Otherwise, use the non-null node.

### Optimal Python Solution

```python
def mergeTrees(root1: TreeNode, root2: TreeNode) -> TreeNode:
    if not root1:
        return root2
    if not root2:
        return root1

    # Merge current node values
    root1.val += root2.val

    # Recursively merge subtrees
    root1.left = mergeTrees(root1.left, root2.left)
    root1.right = mergeTrees(root1.right, root2.right)

    return root1
```

### Complexity Analysis

- **Time Complexity**: **O(min(n1, n2))**. We only traverse the overlap.
- **Space Complexity**: **O(min(h1, h2))**.

---

## 7. Leaf-Similar Trees

**Problem Statement**: Two binary trees are leaf-similar if their leaf value sequence is the same.

### Optimal Python Solution

```python
def leafSimilar(root1: TreeNode, root2: TreeNode) -> bool:
    def getLeaves(node):
        if not node:
            return []
        if not node.left and not node.right:
            return [node.val]
        return getLeaves(node.left) + getLeaves(node.right)

    return getLeaves(root1) == getLeaves(root2)
```

### Complexity Analysis

- **Time Complexity**: **O(n1 + n2)**.
- **Space Complexity**: **O(leaves1 + leaves2)**.

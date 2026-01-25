# Lowest Common Ancestor (LCA) Solutions

## 1. Lowest Common Ancestor of a BST
**Problem Statement**: Given a binary search tree (BST), find the lowest common ancestor (LCA) node of two given nodes `p` and `q`.

### Examples & Edge Cases
- **Example 1**: `root = [6,2,8,0,4,7,9,None,None,3,5], p = 2, q = 8` → Output: `6`
- **Example 2**: `p = 2, q = 4` → Output: `2` (since a node can be a descendant of itself)
- **Edge Case - p or q is root**: Root is the LCA.
- **Edge Case - p and q are the same node**: The node itself is the LCA.

### Optimal Python Solution
```python
class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

def lowestCommonAncestorBST(root: 'TreeNode', p: 'TreeNode', q: 'TreeNode') -> 'TreeNode':
    curr = root

    while curr:
        # If both p and q are smaller than current, LCA must be in the left subtree
        if p.val < curr.val and q.val < curr.val:
            curr = curr.left
        # If both p and q are larger than current, LCA must be in the right subtree
        elif p.val > curr.val and q.val > curr.val:
            curr = curr.right
        else:
            # We found the "split" point. One node is on the left (or is current)
            # and the other is on the right (or is current). This is the LCA.
            return curr
```

### Explanation
1.  **BST Advantage**: We can use the property that `left < root < right` to determine which subtree to search.
2.  **Logic**:
    - If both nodes are smaller than the current node, we must go left to find their common ancestor.
    - If both nodes are larger, we must go right.
    - If one is smaller and one is larger (or if one equals the current node), the current node is the lowest node from which both can be reached. This is the "split point".

### Complexity Analysis
- **Time Complexity**: **O(h)**. We follow a single path from root to the LCA node. $h = \log n$ for balanced trees.
- **Space Complexity**: **O(1)**. The iterative approach uses no extra memory.

---

## 2. Lowest Common Ancestor of a Binary Tree
**Problem Statement**: Given a binary tree, find the lowest common ancestor (LCA) of two given nodes `p` and `q`.

### Optimal Python Solution
```python
def lowestCommonAncestor(root: 'TreeNode', p: 'TreeNode', q: 'TreeNode') -> 'TreeNode':
    # Base Case: if we reach None or find either p or q, return the current node
    if not root or root == p or root == q:
        return root

    # Search for p and q in the left and right subtrees
    left = lowestCommonAncestor(root.left, p, q)
    right = lowestCommonAncestor(root.right, p, q)

    # Result Interpretation:
    # If both subtrees returned a non-null value, it means p was found in one
    # and q was found in the other. Therefore, the current node is the LCA.
    if left and right:
        return root

    # If only one subtree returned a value, both p and q must be in that subtree
    # (or only one was found, and the other doesn't exist - though the problem guarantees existence).
    return left if left else right
```

### Explanation
1.  **Search Strategy**: This is a post-order traversal logic. We ask "Did you find p or q in your subtree?" to both children.
2.  **Bubble Up**:
    - If a child found one of the targets, it returns that target node.
    - If a node receives non-null values from *both* children, it knows it is the LCA and returns itself.
    - If a node receives only one non-null value, it passes that value up to its parent.

### Complexity Analysis
- **Time Complexity**: **O(n)**. In the worst case, we must visit every node to find p and q.
- **Space Complexity**: **O(h)**. The recursion stack can go as deep as the height of the tree.

---

## 3. Lowest Common Ancestor of a Binary Tree II
**Problem Statement**: Similar to LCA of a Binary Tree, but **p and q may not exist** in the tree. Return `null` if either does not exist.

### Optimal Python Solution
```python
def lowestCommonAncestorII(root: 'TreeNode', p: 'TreeNode', q: 'TreeNode') -> 'TreeNode':
    found_p = False
    found_q = False

    def find(node):
        nonlocal found_p, found_q
        if not node:
            return None

        # Post-order: visit children first to ensure we check the whole tree
        left = find(node.left)
        right = find(node.right)

        # Check if current node is p or q
        curr = None
        if node == p:
            found_p = True
            curr = node
        if node == q:
            found_q = True
            curr = node

        if left and right:
            return node

        # If current node is p or q, and we found the other in a child
        if curr and (left or right):
            return curr

        return curr if curr else (left if left else right)

    ans = find(root)
    return ans if (found_p and found_q) else None
```

### Complexity Analysis
- **Time Complexity**: **O(n)**.
- **Space Complexity**: **O(h)**.

---

## 4. Lowest Common Ancestor of a Binary Tree III
**Problem Statement**: Each node has a `parent` pointer. Find the LCA of `p` and `q`.

### Optimal Python Solution
```python
def lowestCommonAncestorIII(p: 'Node', q: 'Node') -> 'Node':
    # This is equivalent to finding the intersection of two linked lists
    a, b = p, q

    while a != b:
        # Move to parent, if at root, jump to the OTHER node's start
        # This equalizes the path lengths: (Path P to Root) + (Path Q to Root)
        a = a.parent if a.parent else q
        b = b.parent if b.parent else p

    return a
```

### Complexity Analysis
- **Time Complexity**: **O(h)**.
- **Space Complexity**: **O(1)**.

---

## 5. Lowest Common Ancestor of Deepest Leaves
**Problem Statement**: Return the lowest common ancestor of its deepest leaves.

### Optimal Python Solution
```python
def lcaDeepestLeaves(root: TreeNode) -> TreeNode:
    def get_lca(node):
        if not node:
            return 0, None

        left_h, left_lca = get_lca(node.left)
        right_h, right_lca = get_lca(node.right)

        if left_h > right_h:
            return left_h + 1, left_lca
        if right_h > left_h:
            return right_h + 1, right_lca

        # If heights are equal, this node is the LCA of the deepest leaves in its subtree
        return left_h + 1, node

    return get_lca(root)[1]
```

### Complexity Analysis
- **Time Complexity**: **O(n)**.
- **Space Complexity**: **O(h)**.

---

## 6. Step-By-Step Directions From a Binary Tree Node to Another
**Problem Statement**: Find the shortest path from node `startValue` to `destValue`. Return as a string of 'U' (up), 'L' (left), and 'R' (right).

### Optimal Python Solution
```python
def getDirections(root: TreeNode, startValue: int, destValue: int) -> str:
    # 1. Find the LCA to get the common branch point
    def findLCA(node, p, q):
        if not node or node.val == p or node.val == q:
            return node
        left = findLCA(node.left, p, q)
        right = findLCA(node.right, p, q)
        return node if left and right else (left or right)

    lca = findLCA(root, startValue, destValue)

    # 2. Find paths from LCA to start and destination
    def findPath(node, target, path):
        if not node: return False
        if node.val == target: return True

        path.append('L')
        if findPath(node.left, target, path): return True
        path.pop()

        path.append('R')
        if findPath(node.right, target, path): return True
        path.pop()

        return False

    path_to_start = []
    path_to_dest = []
    findPath(lca, startValue, path_to_start)
    findPath(lca, destValue, path_to_dest)

    # 3. All steps from start to LCA are 'U'
    return "U" * len(path_to_start) + "".join(path_to_dest)
```

### Complexity Analysis
- **Time Complexity**: **O(n)**.
- **Space Complexity**: **O(n)**.

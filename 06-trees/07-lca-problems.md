# Lowest Common Ancestor (LCA)

> **Prerequisites:** [01-tree-basics](./01-tree-basics.md), [04-bst-operations](./04-bst-operations.md)

## Building Intuition

**The Family Tree Mental Model**: LCA is like finding the most recent common ancestor of two family members. The "lowest" means the deepest in the tree (closest to both).

```
       Great-grandma
           /    \
       Grandpa  Grandma
        /   \
      Dad   Uncle
      / \
    You  Sibling

LCA(You, Sibling) = Dad      (immediate parent)
LCA(You, Uncle) = Grandpa    (one level up from Uncle)
LCA(Dad, Grandma) = Great-grandma
```

**Two different problems - BST vs General BT**:

| Tree Type  | Key Property                 | Approach                     |
| ---------- | ---------------------------- | ---------------------------- |
| BST        | Ordered: left < root < right | Use BST property to navigate |
| General BT | No ordering guarantee        | Search entire tree           |

**BST LCA - the split point insight**:
In a BST, the LCA is where p and q "split" - one goes left, one goes right:

```
BST:        Looking for LCA(2, 8):
      6
     / \
    2   8       At 6: 2 < 6 and 8 > 6 → SPLIT POINT!
   / \ / \      LCA = 6
  0  4 7  9

Looking for LCA(2, 4):
      6
     / \
    2   8       At 6: both < 6 → go left
   / \          At 2: 2 = 2 and 4 > 2 → SPLIT POINT!
  0   4         LCA = 2
```

**General BT LCA - the recursive search insight**:
Search for p and q in both subtrees. The LCA is:

- If found in different subtrees → current node is LCA
- If both in one subtree → LCA is in that subtree
- If current node is p or q → current node might be LCA

```
Recursive LCA logic:
1. If I am p or q → return myself
2. Search left subtree → left_result
3. Search right subtree → right_result
4. If both non-null → I am the LCA (split point)
5. Otherwise → return whichever is non-null
```

---

## When NOT to Use

**Standard LCA algorithms don't apply when:**

- **Tree has parent pointers** → Simpler: trace ancestors and find intersection
- **Need LCA for many queries** → Preprocess with binary lifting or Euler tour
- **Graph is not a tree** → Different algorithms needed

**BST approach fails when:**

- Tree is not a BST → Must use general BT approach
- Values are not unique → Cannot reliably navigate

**Common mistake scenarios:**

- Using BST algorithm on general binary tree → Wrong answer
- Not handling "node is ancestor of itself" case → Definition says node can be its own descendant
- Assuming both nodes exist → Add existence check if not guaranteed

**When to use specialized LCA algorithms:**
| Scenario | Best Approach |
|----------|---------------|
| Single query, BST | O(h) BST traversal |
| Single query, general BT | O(n) recursive search |
| Many queries, static tree | Binary lifting O(n log n) preprocess, O(log n) query |
| Queries with updates | Link-Cut trees (advanced) |
| Need all ancestors | Parent pointer + path comparison |

**The parent pointer simplification**:
If nodes have parent pointers, LCA becomes "find intersection of two linked lists":

1. Trace p's ancestors to root → path1
2. Trace q's ancestors to root → path2
3. Find last common node in both paths

---

## Interview Context

LCA problems are popular because:

1. **Fundamental concept**: LCA appears in many tree algorithms
2. **Two distinct approaches**: Different solutions for BST vs general BT
3. **Tests recursive thinking**: Clean recursive solutions exist
4. **Practical applications**: Git merge-base, DOM manipulation, genealogy

This is a **very common** interview question at FANG+ companies.

---

## Core Concept: What is LCA?

The Lowest Common Ancestor of two nodes p and q is the deepest node that has both p and q as descendants (a node can be a descendant of itself).

```
Example:
         3
        / \
       5   1
      / \ / \
     6  2 0  8
       / \
      7   4

LCA(5, 1) = 3  (both are children of 3)
LCA(5, 4) = 5  (4 is descendant of 5, 5 is ancestor of itself)
LCA(6, 4) = 5  (5 is lowest node that is ancestor of both)
```

---

## LCA in Binary Search Tree

For BST, we can use the BST property to efficiently find LCA.

### Key Insight

- If both p and q are smaller than root → LCA is in left subtree
- If both p and q are larger than root → LCA is in right subtree
- Otherwise, root is the LCA (split point)

### Recursive Solution

```python
def lowest_common_ancestor_bst(root: TreeNode, p: TreeNode, q: TreeNode) -> TreeNode:
    """
    LCA in Binary Search Tree.

    LeetCode 235: Lowest Common Ancestor of a Binary Search Tree

    Time: O(h) - follows one path down
    Space: O(h) - recursion stack
    """
    if p.val < root.val and q.val < root.val:
        # Both in left subtree
        return lowest_common_ancestor_bst(root.left, p, q)

    if p.val > root.val and q.val > root.val:
        # Both in right subtree
        return lowest_common_ancestor_bst(root.right, p, q)

    # Split point - current node is LCA
    return root
```

### Iterative Solution (O(1) Space)

```python
def lca_bst_iterative(root: TreeNode, p: TreeNode, q: TreeNode) -> TreeNode:
    """
    Iterative LCA for BST.

    Time: O(h)
    Space: O(1)
    """
    while root:
        if p.val < root.val and q.val < root.val:
            root = root.left
        elif p.val > root.val and q.val > root.val:
            root = root.right
        else:
            return root

    return None
```

### Visual Walkthrough

```
BST:
         6
        / \
       2   8
      / \ / \
     0  4 7  9
       / \
      3   5

LCA(2, 8):
- 2 < 6 and 8 > 6 → split! Return 6

LCA(2, 4):
- 2 < 6 and 4 < 6 → go left to 2
- 2 == 2 → one is root, other is descendant. Return 2

LCA(3, 5):
- 3 < 6 and 5 < 6 → go left to 2
- 3 > 2 and 5 > 2 → go right to 4
- 3 < 4 and 5 > 4 → split! Return 4
```

---

## LCA in Binary Tree (General)

For general binary tree, we can't use BST property. We need different approach.

### Recursive Solution

```python
def lowest_common_ancestor(root: TreeNode, p: TreeNode, q: TreeNode) -> TreeNode:
    """
    LCA in Binary Tree (general).

    LeetCode 236: Lowest Common Ancestor of a Binary Tree

    Key insight: If we find p or q, return it. If both subtrees return
    non-null, current node is LCA. Otherwise, return the non-null child.

    Time: O(n) - may visit all nodes
    Space: O(h) - recursion stack
    """
    # Base case: reached null or found p/q
    if not root or root == p or root == q:
        return root

    # Search in both subtrees
    left = lowest_common_ancestor(root.left, p, q)
    right = lowest_common_ancestor(root.right, p, q)

    # If both sides return something, root is LCA
    if left and right:
        return root

    # Otherwise, return the non-null side
    return left if left else right
```

### How It Works

```
Tree:
         3
        / \
       5   1
      / \
     6   2

LCA(5, 1):

Call on 3:
  left = call(5) → finds 5, returns 5
  right = call(1) → finds 1, returns 1
  Both non-null → return 3 ✓

LCA(5, 6):

Call on 3:
  left = call(5):
    left = call(6) → returns 6
    right = call(2) → returns None
    One non-null → returns 6? No!
    Actually, root == p (5), so returns 5 immediately
  right = call(1) → returns None
  Only left non-null → return 5 ✓
```

### Important Detail

The algorithm assumes p and q **exist** in the tree. If they might not exist, we need additional validation.

### Handling Non-Existence

```python
def lca_with_existence_check(root: TreeNode, p: TreeNode, q: TreeNode) -> TreeNode:
    """
    LCA that handles case where p or q might not exist.

    Time: O(n)
    Space: O(h)
    """
    result = [None]
    found = [False, False]  # [found_p, found_q]

    def dfs(node):
        if not node:
            return None

        left = dfs(node.left)
        right = dfs(node.right)

        if node == p:
            found[0] = True
            return node
        if node == q:
            found[1] = True
            return node

        if left and right:
            result[0] = node
            return node

        return left if left else right

    dfs(root)

    # Only return if both were found
    if found[0] and found[1]:
        # Check if one is ancestor of other
        if result[0]:
            return result[0]
        # p or q is LCA
        return p if search(p, q) else q if search(q, p) else None

    return None


def search(root, target):
    """Check if target exists in subtree rooted at root."""
    if not root:
        return False
    if root == target:
        return True
    return search(root.left, target) or search(root.right, target)
```

---

## LCA with Parent Pointers

If nodes have parent pointers, we can use a different approach.

```python
def lca_with_parent(p: TreeNode, q: TreeNode) -> TreeNode:
    """
    LCA when nodes have parent pointers.

    Similar to finding intersection of two linked lists.

    Time: O(h)
    Space: O(1)
    """
    # Get depths
    def get_depth(node):
        depth = 0
        while node.parent:
            node = node.parent
            depth += 1
        return depth

    depth_p = get_depth(p)
    depth_q = get_depth(q)

    # Align to same depth
    while depth_p > depth_q:
        p = p.parent
        depth_p -= 1

    while depth_q > depth_p:
        q = q.parent
        depth_q -= 1

    # Move up together until they meet
    while p != q:
        p = p.parent
        q = q.parent

    return p
```

### Using Set (Alternative)

```python
def lca_with_parent_set(p: TreeNode, q: TreeNode) -> TreeNode:
    """
    LCA with parent pointers using set.

    Time: O(h)
    Space: O(h)
    """
    ancestors = set()

    # Store all ancestors of p
    node = p
    while node:
        ancestors.add(node)
        node = node.parent

    # Find first common ancestor
    node = q
    while node:
        if node in ancestors:
            return node
        node = node.parent

    return None
```

---

## Complexity Analysis

| Approach            | Time | Space | Tree Type   |
| ------------------- | ---- | ----- | ----------- |
| BST recursive       | O(h) | O(h)  | BST         |
| BST iterative       | O(h) | O(1)  | BST         |
| BT recursive        | O(n) | O(h)  | General     |
| With parent (depth) | O(h) | O(1)  | With parent |
| With parent (set)   | O(h) | O(h)  | With parent |

---

## Common Variations

### 1. LCA of Multiple Nodes

```python
def lca_multiple(root: TreeNode, nodes: list[TreeNode]) -> TreeNode:
    """
    LCA of multiple nodes.

    Time: O(n)
    Space: O(h)
    """
    target_set = set(nodes)

    def dfs(node):
        if not node:
            return None
        if node in target_set:
            return node

        left = dfs(node.left)
        right = dfs(node.right)

        if left and right:
            return node
        return left if left else right

    return dfs(root)
```

### 2. LCA with Distance

```python
def lca_with_distance(root: TreeNode, p: TreeNode, q: TreeNode) -> tuple:
    """
    Return (LCA, distance from LCA to p, distance from LCA to q).
    """
    def find_path(node, target, path):
        if not node:
            return False
        path.append(node)
        if node == target:
            return True
        if find_path(node.left, target, path) or find_path(node.right, target, path):
            return True
        path.pop()
        return False

    path_p, path_q = [], []
    find_path(root, p, path_p)
    find_path(root, q, path_q)

    # Find divergence point
    lca = None
    for i in range(min(len(path_p), len(path_q))):
        if path_p[i] == path_q[i]:
            lca = path_p[i]
        else:
            break

    dist_p = len(path_p) - path_p.index(lca) - 1
    dist_q = len(path_q) - path_q.index(lca) - 1

    return lca, dist_p, dist_q
```

### 3. Distance Between Two Nodes

```python
def distance_between_nodes(root: TreeNode, p: TreeNode, q: TreeNode) -> int:
    """
    Distance between two nodes = dist(LCA, p) + dist(LCA, q).
    """
    lca = lowest_common_ancestor(root, p, q)

    def depth(node, target, d):
        if not node:
            return -1
        if node == target:
            return d
        left = depth(node.left, target, d + 1)
        if left != -1:
            return left
        return depth(node.right, target, d + 1)

    return depth(lca, p, 0) + depth(lca, q, 0)
```

---

## Edge Cases

```python
# 1. p or q is root
# → root is LCA

# 2. p is ancestor of q (or vice versa)
# → p is LCA

# 3. p == q
# → p (or q) is LCA

# 4. p or q not in tree
# → Need existence check

# 5. Single node tree
root = TreeNode(1)
# → If p and q are both root, return root
```

---

## Interview Tips

1. **Clarify tree type**: BST allows O(h) solution, general BT is O(n)
2. **Ask about parent pointers**: Different algorithm if available
3. **Confirm existence**: Ask if p and q guaranteed to exist
4. **Know both approaches**: BST split-point vs BT recursive search
5. **Practice the recursive solution**: It's elegant but tricky to explain

---

## Practice Problems

| #   | Problem                                         | Difficulty | Key Concept          |
| --- | ----------------------------------------------- | ---------- | -------------------- |
| 1   | Lowest Common Ancestor of a BST                 | Medium     | BST split point      |
| 2   | Lowest Common Ancestor of a Binary Tree         | Medium     | General recursive    |
| 3   | Lowest Common Ancestor of a Binary Tree II      | Medium     | Handle non-existence |
| 4   | Lowest Common Ancestor of a Binary Tree III     | Medium     | With parent pointers |
| 5   | Lowest Common Ancestor of Deepest Leaves        | Medium     | Special case         |
| 6   | Step-By-Step Directions From a Binary Tree Node | Medium     | LCA + path           |

---

## Key Takeaways

1. **BST uses split point**: O(h) time using BST property
2. **BT uses recursion**: Return p/q when found, check both subtrees
3. **Both non-null = LCA**: When left and right both return something
4. **Parent pointers help**: Can use ancestor set or depth alignment
5. **Existence matters**: Standard algorithm assumes p and q exist

---

## Next: [08-path-sum.md](./08-path-sum.md)

Learn path sum problems and path tracking in trees.

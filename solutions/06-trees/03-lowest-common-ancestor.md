# Lowest Common Ancestor of Binary Tree

## Problem Statement

Given a binary tree, find the lowest common ancestor (LCA) of two given nodes p and q.

LCA is the lowest node that has both p and q as descendants (a node can be its own descendant).

**Example:**
```
Input:      3
          /   \
         5     1
        / \   / \
       6   2 0   8
          / \
         7   4

p = 5, q = 1
Output: 3

p = 5, q = 4
Output: 5 (5 is ancestor of 4 and itself)
```

## Approach

### Recursive DFS
1. If current node is p or q, return it
2. Recursively search left and right subtrees
3. If both subtrees return non-null, current node is LCA
4. If only one returns non-null, return that one

### Key Insight
The LCA is the split point where p and q are in different subtrees, or one is the ancestor of the other.

## Implementation

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def lowest_common_ancestor(root: TreeNode, p: TreeNode, q: TreeNode) -> TreeNode:
    """
    Find LCA of p and q in binary tree.

    Time: O(n) - may visit all nodes
    Space: O(h) - recursion stack
    """
    # Base case: empty or found p or q
    if not root or root == p or root == q:
        return root

    # Search in left and right subtrees
    left = lowest_common_ancestor(root.left, p, q)
    right = lowest_common_ancestor(root.right, p, q)

    # If both sides found something, current node is LCA
    if left and right:
        return root

    # Otherwise return the non-null result
    return left if left else right


def lowest_common_ancestor_iterative(
    root: TreeNode, p: TreeNode, q: TreeNode
) -> TreeNode:
    """
    Iterative approach using parent pointers.

    Time: O(n)
    Space: O(n) - parent map
    """
    parent = {root: None}
    stack = [root]

    # Find parents of all nodes until we find both p and q
    while p not in parent or q not in parent:
        node = stack.pop()
        if node.left:
            parent[node.left] = node
            stack.append(node.left)
        if node.right:
            parent[node.right] = node
            stack.append(node.right)

    # Get ancestors of p
    ancestors = set()
    while p:
        ancestors.add(p)
        p = parent[p]

    # Find first ancestor of q that's also ancestor of p
    while q not in ancestors:
        q = parent[q]

    return q
```

## Complexity Analysis

| Method | Time | Space | Notes |
|--------|------|-------|-------|
| Recursive | O(n) | O(h) | h = height |
| Iterative | O(n) | O(n) | Parent map |

## Visual Walkthrough

```
Tree:       3
          /   \
         5     1
        / \   / \
       6   2 0   8
          / \
         7   4

Finding LCA(5, 4):

1. At node 3: search left (5) and right (1)
2. At node 5: 5 == p, return 5
3. At node 1: search left (0) and right (8)
   - Neither is p or q, both return null
   - Return null
4. Back at 3: left=5, right=null
   - Return 5 (the non-null result)

LCA(5, 4) = 5


Finding LCA(5, 1):

1. At node 3: search left and right
2. At node 5: return 5 (found p)
3. At node 1: return 1 (found q)
4. Back at 3: left=5, right=1
   - Both non-null! Return 3

LCA(5, 1) = 3
```

## Edge Cases

1. **p or q is root**: LCA is root
2. **p is ancestor of q**: LCA is p
3. **p and q are same**: LCA is that node
4. **p and q are in same subtree**: LCA is higher ancestor
5. **Nodes guaranteed to exist**: Problem assumes this

## Common Mistakes

1. **Not handling node being its own ancestor**: A node is descendant of itself
2. **Checking value instead of reference**: Compare nodes, not values
3. **Not considering one node as ancestor of other**: Handle this case
4. **Assuming BST properties**: This is general binary tree, not BST

## Variations

### LCA in Binary Search Tree
```python
def lca_bst(root: TreeNode, p: TreeNode, q: TreeNode) -> TreeNode:
    """
    LCA in BST - can use BST properties.

    Time: O(h)
    Space: O(1) iterative, O(h) recursive
    """
    # Ensure p.val < q.val for easier logic
    if p.val > q.val:
        p, q = q, p

    while root:
        if root.val > q.val:
            # Both in left subtree
            root = root.left
        elif root.val < p.val:
            # Both in right subtree
            root = root.right
        else:
            # Split point or one of them
            return root

    return None
```

### LCA with Parent Pointers
```python
def lca_with_parent(p: 'Node', q: 'Node') -> 'Node':
    """
    Find LCA when nodes have parent pointers.
    Similar to finding intersection of two linked lists.

    Time: O(h)
    Space: O(1)
    """
    a, b = p, q

    while a != b:
        a = a.parent if a else q
        b = b.parent if b else p

    return a
```

### LCA of Deepest Leaves
```python
def lca_deepest_leaves(root: TreeNode) -> TreeNode:
    """
    Find LCA of all deepest leaves.

    Time: O(n)
    Space: O(h)
    """
    def dfs(node):
        """Return (depth, lca) for subtree."""
        if not node:
            return 0, None

        left_depth, left_lca = dfs(node.left)
        right_depth, right_lca = dfs(node.right)

        if left_depth > right_depth:
            return left_depth + 1, left_lca
        elif right_depth > left_depth:
            return right_depth + 1, right_lca
        else:
            # Equal depth: current node is LCA
            return left_depth + 1, node

    return dfs(root)[1]
```

### LCA of Multiple Nodes
```python
def lca_multiple(root: TreeNode, nodes: set[TreeNode]) -> TreeNode:
    """
    Find LCA of multiple nodes.

    Time: O(n)
    Space: O(h)
    """
    if not root or root in nodes:
        return root

    left = lca_multiple(root.left, nodes)
    right = lca_multiple(root.right, nodes)

    if left and right:
        return root
    return left or right
```

## Related Problems

- **LCA in BST** - Simpler with BST properties
- **LCA with Parent Pointers** - Different approach
- **LCA of Deepest Leaves** - Combine with depth finding
- **Distance Between Nodes** - Uses LCA as building block
- **Path Sum III** - Related tree path problems

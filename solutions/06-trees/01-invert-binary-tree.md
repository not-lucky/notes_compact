# Invert Binary Tree

## Problem Statement

Given the root of a binary tree, invert the tree, and return its root.

Inverting means swapping left and right children for every node.

**Example:**
```
Input:      4               Output:     4
          /   \                       /   \
         2     7                     7     2
        / \   / \                   / \   / \
       1   3 6   9                 9   6 3   1
```

## Building Intuition

### Why This Works

Inverting a tree means creating its mirror image. At every node, what was on the left should now be on the right, and vice versa. The recursive insight is beautiful: to invert a tree, just swap the children of the root, then invert each subtree. The base case (null node) requires no action.

This works because the inversion property is compositional - a tree is inverted if and only if (1) its left and right children are swapped, AND (2) both subtrees are themselves inverted. By handling the swap locally and delegating the subtree inversion to recursion, we cover all nodes.

Whether you swap before recursing (preorder) or after (postorder), the final result is the same because each swap is independent - swapping at a parent doesn't affect what needs to happen at children, and vice versa.

### How to Discover This

For tree transformation problems, ask: "What needs to happen at each node, and how does it relate to the subtrees?" If the operation at each node is independent of the recursion results, you can do it before, during, or after the recursive calls. This is the hallmark of simple tree transformations.

### Pattern Recognition

This is the **Tree Transformation via Traversal** pattern. Visit each node, perform a local operation (swap), and recurse. The same pattern applies to tree coloring, value modification, or any per-node transformation.

## When NOT to Use

- **When you need to preserve the original tree**: This approach modifies in-place. Create a copy if you need both versions.
- **When working with very deep trees and recursion limits**: For trees with millions of nodes in a skewed shape, use iterative BFS/DFS to avoid stack overflow.
- **When the tree has special structure you want to preserve**: Inverting a BST destroys its BST property; if you need the BST property, inversion is the wrong operation.
- **When "inversion" means something different in your context**: Make sure swapping children is actually what's required; some problems use "invert" to mean something else.

## Approach

### Recursive (DFS)
1. Swap left and right children
2. Recursively invert left and right subtrees
3. Base case: null node returns null

### Iterative (BFS)
Use queue to traverse level by level, swapping children at each node.

## Implementation

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def invert_tree(root: TreeNode) -> TreeNode:
    """
    Invert binary tree recursively.

    Time: O(n) - visit each node once
    Space: O(h) - recursion stack, h = height
    """
    if not root:
        return None

    # Swap children
    root.left, root.right = root.right, root.left

    # Recursively invert subtrees
    invert_tree(root.left)
    invert_tree(root.right)

    return root


def invert_tree_postorder(root: TreeNode) -> TreeNode:
    """
    Alternative: Invert after recursing (postorder).
    """
    if not root:
        return None

    left = invert_tree_postorder(root.left)
    right = invert_tree_postorder(root.right)

    root.left = right
    root.right = left

    return root


def invert_tree_iterative(root: TreeNode) -> TreeNode:
    """
    Invert using BFS with queue.

    Time: O(n)
    Space: O(n) - queue can hold entire level
    """
    if not root:
        return None

    from collections import deque
    queue = deque([root])

    while queue:
        node = queue.popleft()

        # Swap children
        node.left, node.right = node.right, node.left

        # Add children to queue
        if node.left:
            queue.append(node.left)
        if node.right:
            queue.append(node.right)

    return root


def invert_tree_stack(root: TreeNode) -> TreeNode:
    """
    Invert using DFS with stack.

    Time: O(n)
    Space: O(h)
    """
    if not root:
        return None

    stack = [root]

    while stack:
        node = stack.pop()
        node.left, node.right = node.right, node.left

        if node.left:
            stack.append(node.left)
        if node.right:
            stack.append(node.right)

    return root
```

## Complexity Analysis

| Method | Time | Space | Notes |
|--------|------|-------|-------|
| Recursive | O(n) | O(h) | h = height, worst O(n) |
| Iterative BFS | O(n) | O(n) | Queue holds level width |
| Iterative DFS | O(n) | O(h) | Stack depth |

## Visual Walkthrough

```
Original:
        4
      /   \
     2     7
    / \   / \
   1   3 6   9

Step 1: Swap 4's children
        4
      /   \
     7     2
    / \   / \
   6   9 1   3

Step 2: Recurse on 7, swap its children
        4
      /   \
     7     2
    / \   / \
   9   6 1   3

Step 3: Recurse on 2, swap its children
        4
      /   \
     7     2
    / \   / \
   9   6 3   1

Done!
```

## Edge Cases

1. **Empty tree**: Return None
2. **Single node**: Return the node (no children to swap)
3. **Left-only tree**: Becomes right-only tree
4. **Full tree**: All children swapped
5. **Unbalanced tree**: Works correctly

## Common Mistakes

1. **Returning before swapping**: Make sure to swap first
2. **Not handling null**: Check for null before operations
3. **Only swapping one level**: Must recurse/iterate through all
4. **Modifying during traversal issues**: None here, we're modifying in place

## Variations

### Symmetric Tree
```python
def is_symmetric(root: TreeNode) -> bool:
    """
    Check if tree is mirror of itself.

    Time: O(n)
    Space: O(h)
    """
    def is_mirror(t1: TreeNode, t2: TreeNode) -> bool:
        if not t1 and not t2:
            return True
        if not t1 or not t2:
            return False
        return (t1.val == t2.val and
                is_mirror(t1.left, t2.right) and
                is_mirror(t1.right, t2.left))

    return is_mirror(root, root)
```

### Same Tree
```python
def is_same_tree(p: TreeNode, q: TreeNode) -> bool:
    """
    Check if two trees are identical.

    Time: O(n)
    Space: O(h)
    """
    if not p and not q:
        return True
    if not p or not q:
        return False
    return (p.val == q.val and
            is_same_tree(p.left, q.left) and
            is_same_tree(p.right, q.right))
```

### Flip Equivalent Binary Trees
```python
def flip_equiv(root1: TreeNode, root2: TreeNode) -> bool:
    """
    Check if trees are flip equivalent.
    Trees are flip equivalent if we can make them identical
    by swapping left and right children of some nodes.

    Time: O(n)
    Space: O(h)
    """
    if not root1 and not root2:
        return True
    if not root1 or not root2:
        return False
    if root1.val != root2.val:
        return False

    # Either same structure or flipped structure
    return ((flip_equiv(root1.left, root2.left) and
             flip_equiv(root1.right, root2.right)) or
            (flip_equiv(root1.left, root2.right) and
             flip_equiv(root1.right, root2.left)))
```

## Related Problems

- **Same Tree** - Check if two trees are identical
- **Symmetric Tree** - Check if tree is symmetric
- **Maximum Depth of Binary Tree** - Similar recursive structure
- **Subtree of Another Tree** - Uses same tree as subroutine
- **Flip Equivalent Binary Trees** - More flexible equivalence

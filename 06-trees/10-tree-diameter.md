# Tree Diameter

> **Prerequisites:** [09-tree-depth](./09-tree-depth.md), [02-tree-traversals](./02-tree-traversals.md)

## Interview Context

Tree diameter is important because:

1. **Classic interview problem**: Frequently asked at Google, Meta, Amazon
2. **Pattern reuse**: Same technique applies to longest path problems
3. **Tricky optimization**: Naive approach is O(n²), optimal is O(n)
4. **Tests understanding**: Requires grasping how paths combine at nodes

This problem has the same pattern as "Binary Tree Maximum Path Sum".

---

## Core Concept: What is Diameter?

The diameter of a binary tree is the **length of the longest path** between any two nodes. This path may or may not pass through the root.

```
Example 1:
       1
      / \
     2   3
    / \
   4   5

Diameter = 3 (path: 4 → 2 → 1 → 3 or 5 → 2 → 1 → 3)
Note: We count EDGES, not nodes. Path has 4 nodes but 3 edges.

Example 2:
       1
      /
     2
    / \
   4   5
  /     \
 6       7

Diameter = 4 (path: 6 → 4 → 2 → 5 → 7)
This path doesn't go through root!
```

---

## Key Insight

At each node, the longest path passing through it is:
- **left_depth + right_depth** (connecting deepest left to deepest right)

The diameter is the maximum of these values across all nodes.

---

## Solution: O(n) Single Pass

```python
def diameter_of_binary_tree(root: TreeNode) -> int:
    """
    Calculate diameter (longest path between any two nodes).

    LeetCode 543: Diameter of Binary Tree

    At each node, calculate left_depth + right_depth.
    Track maximum across all nodes.

    Time: O(n) - single DFS
    Space: O(h) - recursion stack
    """
    diameter = [0]  # Use list for mutable reference in nested function

    def depth(node):
        if not node:
            return 0

        left_depth = depth(node.left)
        right_depth = depth(node.right)

        # Path through this node = left_depth + right_depth
        diameter[0] = max(diameter[0], left_depth + right_depth)

        # Return depth for parent to use
        return 1 + max(left_depth, right_depth)

    depth(root)
    return diameter[0]
```

### Visual Walkthrough

```
       1
      / \
     2   3
    / \
   4   5

DFS traversal:
- At 4: left=0, right=0, path=0, return 1
- At 5: left=0, right=0, path=0, return 1
- At 2: left=1, right=1, path=2, diameter=2, return 2
- At 3: left=0, right=0, path=0, return 1
- At 1: left=2, right=1, path=3, diameter=3, return 3

Final diameter = 3
```

---

## Alternative: Return Tuple

```python
def diameter_tuple(root: TreeNode) -> int:
    """
    Alternative using tuple return (diameter, depth).
    """
    def dfs(node):
        if not node:
            return 0, 0  # (max_diameter_in_subtree, depth)

        left_dia, left_depth = dfs(node.left)
        right_dia, right_depth = dfs(node.right)

        # Diameter through this node
        through_node = left_depth + right_depth

        # Maximum diameter seen so far
        max_dia = max(left_dia, right_dia, through_node)

        # Depth of this subtree
        depth = 1 + max(left_depth, right_depth)

        return max_dia, depth

    return dfs(root)[0]
```

---

## Naive Approach: O(n²)

For comparison, here's the naive approach (don't use in interviews):

```python
def diameter_naive(root: TreeNode) -> int:
    """
    Naive O(n²) approach - calculates height at each node.
    """
    if not root:
        return 0

    def height(node):
        if not node:
            return 0
        return 1 + max(height(node.left), height(node.right))

    # Diameter through root
    through_root = height(root.left) + height(root.right)

    # Check if better diameter exists in subtrees
    left_diameter = diameter_naive(root.left)
    right_diameter = diameter_naive(root.right)

    return max(through_root, left_diameter, right_diameter)
```

---

## Diameter of N-ary Tree

```python
def diameter_n_ary(root: 'Node') -> int:
    """
    Diameter of N-ary tree.

    Find two deepest paths from any node.
    """
    diameter = [0]

    def dfs(node):
        if not node:
            return 0

        # Get depths of all children
        depths = [dfs(child) for child in node.children]

        if len(depths) >= 2:
            # Two longest paths
            depths.sort(reverse=True)
            diameter[0] = max(diameter[0], depths[0] + depths[1])
        elif len(depths) == 1:
            diameter[0] = max(diameter[0], depths[0])

        return 1 + (max(depths) if depths else 0)

    dfs(root)
    return diameter[0]
```

---

## Related Problem: Longest Path with Different Adjacent Characters

```python
def longest_path(parent: list[int], s: str) -> int:
    """
    Longest path where no two adjacent nodes have same character.

    LeetCode 2246: Longest Path With Different Adjacent Characters

    Build tree from parent array, then find longest valid path.
    """
    from collections import defaultdict

    n = len(parent)
    children = defaultdict(list)

    for i in range(1, n):
        children[parent[i]].append(i)

    longest = [0]

    def dfs(node):
        # Track two longest valid paths through children
        top_two = [0, 0]

        for child in children[node]:
            child_len = dfs(child)

            if s[child] != s[node]:  # Different characters
                # Update top two lengths
                if child_len > top_two[0]:
                    top_two = [child_len, top_two[0]]
                elif child_len > top_two[1]:
                    top_two[1] = child_len

        # Path through this node using top two children
        longest[0] = max(longest[0], top_two[0] + top_two[1] + 1)

        return top_two[0] + 1

    dfs(0)
    return longest[0]
```

---

## Complexity Analysis

| Approach | Time | Space | Notes |
|----------|------|-------|-------|
| Optimal (single pass) | O(n) | O(h) | Combine diameter and depth |
| Naive (separate height) | O(n²) | O(h) | Height at each node |
| N-ary tree | O(n log k) | O(h) | Sort children depths |

---

## Edge Cases

```python
# 1. Empty tree
root = None
# → diameter = 0

# 2. Single node
root = TreeNode(1)
# → diameter = 0 (no edges)

# 3. Linear tree (skewed)
#     1
#      \
#       2
#        \
#         3
# → diameter = 2 (edges: 1-2, 2-3)

# 4. Diameter not through root
#       1
#      /
#     2
#    / \
#   3   4
# → diameter = 2 (path: 3-2-4)
```

---

## Interview Tips

1. **Count edges, not nodes**: Common confusion point - clarify!
2. **Path may not include root**: Check examples like case 4 above
3. **Same pattern as max path sum**: "Through this node" vs "to parent"
4. **Single pass is expected**: O(n²) is usually considered suboptimal
5. **Draw examples**: Always verify with the provided examples

---

## Practice Problems

| # | Problem | Difficulty | Key Concept |
|---|---------|------------|-------------|
| 1 | Diameter of Binary Tree | Easy | Basic diameter |
| 2 | Binary Tree Maximum Path Sum | Hard | Similar pattern with values |
| 3 | Longest Univalue Path | Medium | Same value constraint |
| 4 | Longest Path With Different Adjacent Characters | Hard | Character constraint |
| 5 | Tree Diameter | Medium | Unrooted tree (graph) |

---

## Key Takeaways

1. **Diameter = left_depth + right_depth** at some node
2. **Track global max**: Update during DFS, not just at return
3. **Return depth, track diameter**: Two different things computed together
4. **Pattern reuse**: Same logic for max path sum, longest univalue path
5. **O(n) is achievable**: Don't recalculate heights

---

## Next: [11-symmetric-tree.md](./11-symmetric-tree.md)

Learn to check if a tree is symmetric and compare trees.

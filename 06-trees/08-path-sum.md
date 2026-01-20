# Path Sum Problems

> **Prerequisites:** [01-tree-basics](./01-tree-basics.md), [02-tree-traversals](./02-tree-traversals.md)

## Building Intuition

**The Trail Marker Mental Model**: Imagine hiking in a forest where each node has a "difficulty score". You're looking for trails with a specific total difficulty. As you walk:
- Add each node's score to your running total
- At a leaf (trail end), check if you hit the target
- Backtrack to try other trails

```
       5 (start hiking)
      / \
     4   8
    /   / \
   11  13  4
  / \       \
 7   2       1

Trail 5→4→11→2 = 22 (target sum!)
Trail 5→8→13 = 26 (not target)
```

**The "remaining sum" insight**:
Instead of tracking running sum and comparing at leaf, track remaining sum:
- Start with target
- Subtract each node's value
- At leaf, check if remaining == 0

```
Target = 22
At 5: remaining = 22 - 5 = 17
At 4: remaining = 17 - 4 = 13
At 11: remaining = 13 - 11 = 2
At 2: remaining = 2 - 2 = 0 → Found!
```

**Three types of path problems**:

| Type | Definition | Approach |
|------|------------|----------|
| **Root-to-leaf** | Start at root, end at leaf | Simple DFS with sum tracking |
| **Downward** | From any ancestor to any descendant | Prefix sum with hashmap |
| **Any-to-any** | Any node to any node (can go up) | DP on subtrees, track through root |

**The prefix sum insight for downward paths**:
For paths not starting at root, use cumulative sums:
```
If prefix[j] - prefix[i] = target, then nodes (i+1 to j) sum to target.

Path: root → ... → node_i → ... → node_j
Cumulative sum at i = 10
Cumulative sum at j = 18
Target = 8
Since 18 - 10 = 8, there's a valid path from i+1 to j!
```

---

## When NOT to Use

**Simple path sum approach fails when:**
- **Paths can go up** → Need to consider paths through root
- **Negative values exist** → Cannot prune early when sum > target
- **Need path count, not existence** → May need different tracking

**Path sum is overkill when:**
- Only need to know if any path exists → Simpler DFS
- Tree is actually a graph → Different traversal needed
- Just counting nodes → No sum logic needed

**Common mistake scenarios:**
- Forgetting to check leaf condition → Non-leaf nodes shouldn't match
- Not backtracking state properly in Path Sum II → Wrong paths
- Using wrong path definition → Root-to-leaf vs any-to-any

**Pattern matching guide:**
| Problem Asks For | Use This Pattern |
|------------------|------------------|
| "Has path root to leaf with sum?" | Simple DFS, subtract from target |
| "Find all such paths" | DFS + backtracking with path list |
| "Count paths anywhere with sum" | Prefix sum + hashmap |
| "Maximum path sum any-to-any" | DP: max(through_root, left_only, right_only) |

**The negative number trap**:
With positive numbers only, you can prune when current_sum > target. With negatives:
```
Target = 10
Path so far: 5 → 8 (sum = 13 > 10)
With positives: PRUNE, no hope
With negatives: CONTINUE, might find -3 later: 5 + 8 + (-3) = 10
```

---

## Interview Context

Path sum problems are important because:

1. **Classic DFS application**: Perfect for demonstrating recursive tree traversal
2. **Multiple variations**: Has path, find paths, max path, all common in interviews
3. **State tracking**: Tests ability to maintain state during traversal
4. **Backtracking preview**: Path sum II introduces backtracking concept

Very common at FANG+ interviews, especially Meta and Google.

---

## Core Concept: What is a Path?

Different problems define "path" differently:

1. **Root-to-leaf path**: From root to any leaf node
2. **Any-to-any path**: Between any two nodes (can go through root)
3. **Downward path**: From any ancestor to any descendant

```
Example Tree:
         5
        / \
       4   8
      /   / \
     11  13  4
    / \       \
   7   2       1

Root-to-leaf paths:
- 5 → 4 → 11 → 7 (sum = 27)
- 5 → 4 → 11 → 2 (sum = 22)
- 5 → 8 → 13 (sum = 26)
- 5 → 8 → 4 → 1 (sum = 18)
```

---

## Path Sum I: Has Root-to-Leaf Path

```python
def has_path_sum(root: TreeNode, target_sum: int) -> bool:
    """
    Check if tree has root-to-leaf path with given sum.

    LeetCode 112: Path Sum

    Time: O(n)
    Space: O(h)
    """
    if not root:
        return False

    # If leaf node, check if remaining sum equals node value
    if not root.left and not root.right:
        return root.val == target_sum

    # Check either subtree
    remaining = target_sum - root.val
    return (has_path_sum(root.left, remaining) or
            has_path_sum(root.right, remaining))
```

### Iterative Version

```python
def has_path_sum_iterative(root: TreeNode, target_sum: int) -> bool:
    """
    Iterative path sum check using stack.

    Time: O(n)
    Space: O(h)
    """
    if not root:
        return False

    stack = [(root, target_sum)]

    while stack:
        node, remaining = stack.pop()
        remaining -= node.val

        # Check if leaf with correct sum
        if not node.left and not node.right and remaining == 0:
            return True

        if node.right:
            stack.append((node.right, remaining))
        if node.left:
            stack.append((node.left, remaining))

    return False
```

---

## Path Sum II: Find All Root-to-Leaf Paths

```python
def path_sum(root: TreeNode, target_sum: int) -> list[list[int]]:
    """
    Find all root-to-leaf paths that sum to target.

    LeetCode 113: Path Sum II

    Time: O(n²) - O(n) nodes, O(n) to copy each path
    Space: O(n) - for storing paths
    """
    result = []

    def dfs(node, remaining, path):
        if not node:
            return

        path.append(node.val)

        # Check if leaf with correct sum
        if not node.left and not node.right and remaining == node.val:
            result.append(path[:])  # Copy current path

        # Continue search
        dfs(node.left, remaining - node.val, path)
        dfs(node.right, remaining - node.val, path)

        path.pop()  # Backtrack

    dfs(root, target_sum, [])
    return result
```

### Visual Walkthrough

```
Tree:
         5
        / \
       4   8
      /   / \
     11  13  4
    / \     / \
   7   2   5   1

Target: 22

DFS with path tracking (remaining = target - sum so far):
- Visit 5: path=[5], remaining=22-5=17
- Visit 4: path=[5,4], remaining=17-4=13
- Visit 11: path=[5,4,11], remaining=13-11=2
- Visit 7: path=[5,4,11,7], remaining=2, node.val=7 ≠ 2 ✗ (leaf, wrong)
- Backtrack, visit 2: path=[5,4,11,2], remaining=2, node.val=2 = 2 ✓ Found!
- Result: [[5,4,11,2]]
```

---

## Path Sum III: Count Paths (Any Start/End Downward)

```python
def path_sum_iii(root: TreeNode, target_sum: int) -> int:
    """
    Count paths summing to target (downward, any start/end).

    LeetCode 437: Path Sum III

    Uses prefix sum technique similar to subarray sum.

    Time: O(n)
    Space: O(h)
    """
    from collections import defaultdict

    count = [0]
    prefix_sums = defaultdict(int)
    prefix_sums[0] = 1  # Empty path

    def dfs(node, current_sum):
        if not node:
            return

        current_sum += node.val

        # Check if there's a prefix that creates target sum
        count[0] += prefix_sums[current_sum - target_sum]

        # Add current sum to prefix map
        prefix_sums[current_sum] += 1

        dfs(node.left, current_sum)
        dfs(node.right, current_sum)

        # Backtrack: remove current sum from prefix map
        prefix_sums[current_sum] -= 1

    dfs(root, 0)
    return count[0]
```

### How Prefix Sum Works

```
Tree:      10
          /  \
         5   -3
        / \    \
       3   2    11
      / \   \
     3  -2   1

Target: 8

At node 5 (sum from root = 15):
- current_sum = 15
- Looking for prefix = 15 - 8 = 7
- No prefix of 7 exists yet

At node 3 (left of 5), sum = 18:
- Looking for prefix = 18 - 8 = 10
- prefix_sums[10] = 1 (path 10)
- Found path: 10 → 5 → 3, but wait...
  Actually path 5 → 3 has sum 8? No, 5+3=8 ✓

The prefix sum at 10 is 10.
At node 3 (sum=18): 18-10=8 ✓ means path from after 10 to 3 sums to 8.
```

---

## Binary Tree Maximum Path Sum

```python
def max_path_sum(root: TreeNode) -> int:
    """
    Find maximum path sum (any node to any node).

    LeetCode 124: Binary Tree Maximum Path Sum (Hard)

    Path can start and end at any nodes.

    Time: O(n)
    Space: O(h)
    """
    max_sum = [float('-inf')]

    def dfs(node):
        if not node:
            return 0

        # Get max gain from left and right (ignore negative gains)
        left_gain = max(dfs(node.left), 0)
        right_gain = max(dfs(node.right), 0)

        # Path through this node (potentially the answer)
        path_sum = node.val + left_gain + right_gain
        max_sum[0] = max(max_sum[0], path_sum)

        # Return max gain if we continue path through this node
        # Can only go one direction (left OR right) when continuing up
        return node.val + max(left_gain, right_gain)

    dfs(root)
    return max_sum[0]
```

### Key Insight

```
At each node, we calculate two things:

1. Best path THROUGH this node (can use both children):
   path_sum = node.val + left_gain + right_gain

2. Best path TO this node (to continue upward, pick one child):
   return node.val + max(left_gain, right_gain)

       -10
       /  \
      9   20
         /  \
        15   7

At 20: left_gain=15, right_gain=7
- path_sum = 20 + 15 + 7 = 42 (best path through 20)
- return 20 + 15 = 35 (best path to parent)

At -10: left_gain=9, right_gain=35
- path_sum = -10 + 9 + 35 = 34
- But 42 > 34, so max path is through 20
```

---

## Sum Root to Leaf Numbers

```python
def sum_numbers(root: TreeNode) -> int:
    """
    Each root-to-leaf path forms a number. Return sum of all.

    LeetCode 129: Sum Root to Leaf Numbers

    Example: paths 1→2→3 and 1→3 give 123 + 13 = 136

    Time: O(n)
    Space: O(h)
    """
    total = [0]

    def dfs(node, current_num):
        if not node:
            return

        current_num = current_num * 10 + node.val

        if not node.left and not node.right:
            total[0] += current_num
            return

        dfs(node.left, current_num)
        dfs(node.right, current_num)

    dfs(root, 0)
    return total[0]
```

---

## All Root-to-Leaf Paths (as Strings)

```python
def binary_tree_paths(root: TreeNode) -> list[str]:
    """
    Return all root-to-leaf paths as strings.

    LeetCode 257: Binary Tree Paths

    Time: O(n)
    Space: O(n)
    """
    if not root:
        return []

    result = []

    def dfs(node, path):
        if not node.left and not node.right:
            result.append(path)
            return

        if node.left:
            dfs(node.left, path + "->" + str(node.left.val))
        if node.right:
            dfs(node.right, path + "->" + str(node.right.val))

    dfs(root, str(root.val))
    return result
```

---

## Complexity Analysis

| Problem | Time | Space | Notes |
|---------|------|-------|-------|
| Has Path Sum | O(n) | O(h) | Simple DFS |
| Path Sum II | O(n²) | O(n) | Copying paths |
| Path Sum III | O(n) | O(h) | Prefix sum trick |
| Max Path Sum | O(n) | O(h) | Track through vs to |
| Sum Root to Leaf | O(n) | O(h) | Build number |

---

## Common Variations

### 1. Longest Path with Same Value

```python
def longest_univalue_path(root: TreeNode) -> int:
    """
    Longest path where all nodes have same value.

    LeetCode 687: Longest Univalue Path

    Return edge count, not node count.
    """
    longest = [0]

    def dfs(node):
        if not node:
            return 0

        left = dfs(node.left)
        right = dfs(node.right)

        # Extend left path if same value
        left_path = left + 1 if node.left and node.left.val == node.val else 0
        right_path = right + 1 if node.right and node.right.val == node.val else 0

        # Path through this node
        longest[0] = max(longest[0], left_path + right_path)

        return max(left_path, right_path)

    dfs(root)
    return longest[0]
```

### 2. Path with Maximum Average

```python
def max_average_subtree(root: TreeNode) -> float:
    """
    Find subtree with maximum average value.
    """
    max_avg = [float('-inf')]

    def dfs(node):
        if not node:
            return 0, 0  # sum, count

        left_sum, left_count = dfs(node.left)
        right_sum, right_count = dfs(node.right)

        total_sum = left_sum + right_sum + node.val
        total_count = left_count + right_count + 1

        max_avg[0] = max(max_avg[0], total_sum / total_count)

        return total_sum, total_count

    dfs(root)
    return max_avg[0]
```

---

## Edge Cases

```python
# 1. Empty tree
root = None
# → has_path_sum returns False, paths return []

# 2. Single node
root = TreeNode(5), target = 5
# → True (single node is a valid path)

# 3. Negative values
#     -2
#       \
#        -3
# → Path sum = -5

# 4. Target = 0
# → Valid case, need paths that sum to 0

# 5. All paths have same sum
# → Return all of them
```

---

## Interview Tips

1. **Clarify path definition**: Root-to-leaf vs any-to-any vs downward
2. **Ask about negative values**: Affects pruning possibilities
3. **Backtracking for Path Sum II**: Remember to pop after DFS
4. **Prefix sum for Path Sum III**: Same technique as subarray sum
5. **Two values at each node**: For max path sum, track "through" vs "to"

---

## Practice Problems

| # | Problem | Difficulty | Key Concept |
|---|---------|------------|-------------|
| 1 | Path Sum | Easy | Basic has-path check |
| 2 | Path Sum II | Medium | Find all paths |
| 3 | Path Sum III | Medium | Prefix sum on tree |
| 4 | Binary Tree Maximum Path Sum | Hard | Any-to-any path |
| 5 | Sum Root to Leaf Numbers | Medium | Build numbers |
| 6 | Binary Tree Paths | Easy | Path as strings |
| 7 | Longest Univalue Path | Medium | Same-value paths |

---

## Key Takeaways

1. **Root-to-leaf**: Check at leaf nodes
2. **Backtracking**: Pop from path list after recursion
3. **Prefix sum**: For "any start" paths, use hashmap
4. **Max path sum**: Track "through" (use both children) vs "to" (continue up)
5. **Negative values matter**: Can't prune early

---

## Next: [09-tree-depth.md](./09-tree-depth.md)

Learn tree depth, height, and balance calculations.

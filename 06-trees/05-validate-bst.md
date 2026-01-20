# Validate BST

> **Prerequisites:** [04-bst-operations](./04-bst-operations.md), [02-tree-traversals](./02-tree-traversals.md)

## Building Intuition

**The Bouncer at the Door Mental Model**: Each node in a BST acts like a bouncer setting rules for who can enter left vs right:

```
At node 5: "Left side: only values < 5 allowed!"
           "Right side: only values > 5 allowed!"

But here's the catch: these rules ACCUMULATE as you go deeper!
```

**Why the naive approach fails**:
Checking only `left.val < node.val < right.val` misses inherited constraints:

```
      5
     / \
    1   7
       / \
      3   9    ← 3 < 7 ✓ (passes naive check)
               ← BUT 3 is in RIGHT subtree of 5!
               ← 3 must be > 5, but 3 < 5 ✗ INVALID!
```

**The range constraint insight**:
Every node must satisfy a range inherited from ALL ancestors:

```
     5 (range: -∞ to +∞)
    / \
   3   7 (range: 5 to +∞)
  / \   \
 1   4   9
         ↑
    (range: 7 to +∞)

At node 9: must be in (7, +∞) → 9 > 7 ✓
If we had 6 here instead: 6 > 7? No! ✗ Invalid
```

**Two equivalent approaches**:

| Approach | How It Works | Space |
|----------|--------------|-------|
| **Range-based** | Pass (min, max) bounds down, narrow at each step | O(h) stack |
| **Inorder traversal** | BST inorder should be strictly increasing | O(h) or O(1) with Morris |

**The inorder insight**:
```
Valid BST:        Inorder: [1, 3, 4, 5, 7, 9] → strictly increasing ✓
      5
     / \
    3   7
   / \   \
  1   4   9

Invalid BST:      Inorder: [1, 6, 4, 5, 7, 9] → 6 > 4 ✗ not increasing!
      5
     / \
    6   7          (6 is invalid - should be < 5)
   / \
  1   4
```

---

## When NOT to Use

**Range-based validation fails when:**
- Tree has duplicate values → Need to decide if duplicates allowed and where
- Range is unclear → With duplicates, is it `<` or `<=`?

**Inorder validation is simpler when:**
- You're already comfortable with inorder traversal
- Problem asks for sorted order verification anyway
- You want O(1) space (Morris traversal variant)

**Common mistake scenarios:**
- Only checking immediate children → Misses ancestor constraints
- Using `<=` instead of `<` → Depends on problem definition
- Integer overflow with min/max → Use `float('-inf')` and `float('inf')` in Python

**The duplicate value trap**:
```
Standard BST: left < root < right (no duplicates)
Some BSTs: left <= root < right (duplicates go left)
Others: left < root <= right (duplicates go right)

ALWAYS clarify with interviewer!
```

**When to use alternative approaches:**
| Scenario | Best Approach |
|----------|---------------|
| Standard validation | Range-based or inorder |
| Need sorted values anyway | Inorder (returns list too) |
| Memory constrained | Morris traversal |
| Just need true/false | Range-based is minimal |
| Debugging existing BST | Inorder shows problem clearly |

---

## Interview Context

Validating BST is a classic interview problem because:

1. **Tests BST understanding**: Must truly understand the BST property
2. **Common pitfall**: Naive solution (only checking immediate children) is wrong
3. **Multiple approaches**: Range-based, inorder traversal, or iterative
4. **Foundation for other problems**: Same logic applies to many BST problems

This is a **very common** interview question at FANG+ companies.

---

## Core Concept: The Trap

A common mistake is to only compare a node with its immediate children:

```
WRONG approach:
      5
     / \
    1   7
       / \
      3   9    ← 3 < 7 ✓ but 3 < 5 ✗

Checking only "left.val < root.val < right.val" misses this!
3 is in the RIGHT subtree of 5, so it must be > 5.
```

**Correct approach**: Each node must be within a valid **range** defined by its ancestors.

---

## Approach 1: Range-Based (Min/Max Bounds)

### Recursive Solution

```python
def is_valid_bst(root: TreeNode) -> bool:
    """
    Validate BST using min/max bounds.

    LeetCode 98: Validate Binary Search Tree

    For each node, track the valid range (min, max).
    Left child range: (min, parent)
    Right child range: (parent, max)

    Time: O(n) - visit every node
    Space: O(h) - recursion stack
    """
    def validate(node, min_val, max_val):
        if not node:
            return True

        # Node must be within valid range
        if node.val <= min_val or node.val >= max_val:
            return False

        # Left subtree: values must be < node.val
        # Right subtree: values must be > node.val
        return (validate(node.left, min_val, node.val) and
                validate(node.right, node.val, max_val))

    return validate(root, float('-inf'), float('inf'))
```

### Visual Walkthrough

```
Validate:
      5
     / \
    3   7
   / \
  1   4

validate(5, -∞, +∞): 5 in range ✓
  validate(3, -∞, 5): 3 in range ✓
    validate(1, -∞, 3): 1 in range ✓
    validate(4, 3, 5): 4 in range ✓
  validate(7, 5, +∞): 7 in range ✓
All pass → Valid BST!

Invalid example:
      5
     / \
    3   7
       /
      4    ← 4 should be > 5 but it's in right subtree

validate(7, 5, +∞): 7 in range ✓
  validate(4, 5, 7): 4 NOT in (5, 7) ✗
Invalid!
```

### Iterative Version

```python
def is_valid_bst_iterative(root: TreeNode) -> bool:
    """
    Iterative validation using stack with bounds.

    Time: O(n)
    Space: O(h)
    """
    if not root:
        return True

    stack = [(root, float('-inf'), float('inf'))]

    while stack:
        node, min_val, max_val = stack.pop()

        if node.val <= min_val or node.val >= max_val:
            return False

        if node.right:
            stack.append((node.right, node.val, max_val))
        if node.left:
            stack.append((node.left, min_val, node.val))

    return True
```

---

## Approach 2: Inorder Traversal

BST property guarantees that **inorder traversal produces sorted sequence**.

### Recursive Inorder

```python
def is_valid_bst_inorder(root: TreeNode) -> bool:
    """
    Use inorder traversal - must be strictly increasing.

    Time: O(n)
    Space: O(h)
    """
    prev = [float('-inf')]  # Use list to allow modification in nested function

    def inorder(node):
        if not node:
            return True

        # Check left subtree
        if not inorder(node.left):
            return False

        # Check current node against previous
        if node.val <= prev[0]:
            return False
        prev[0] = node.val

        # Check right subtree
        return inorder(node.right)

    return inorder(root)
```

### Iterative Inorder

```python
def is_valid_bst_inorder_iterative(root: TreeNode) -> bool:
    """
    Iterative inorder validation.

    Time: O(n)
    Space: O(h)
    """
    stack = []
    prev = float('-inf')
    current = root

    while current or stack:
        # Go left as far as possible
        while current:
            stack.append(current)
            current = current.left

        current = stack.pop()

        # Check if in order
        if current.val <= prev:
            return False
        prev = current.val

        current = current.right

    return True
```

---

## Approach 3: Morris Traversal (O(1) Space)

```python
def is_valid_bst_morris(root: TreeNode) -> bool:
    """
    Validate BST using Morris inorder traversal.

    Time: O(n)
    Space: O(1) - no recursion/stack
    """
    prev = float('-inf')
    current = root

    while current:
        if not current.left:
            # No left child - process and go right
            if current.val <= prev:
                return False
            prev = current.val
            current = current.right
        else:
            # Find predecessor
            predecessor = current.left
            while predecessor.right and predecessor.right != current:
                predecessor = predecessor.right

            if not predecessor.right:
                # Create thread
                predecessor.right = current
                current = current.left
            else:
                # Thread exists - we're returning
                predecessor.right = None
                if current.val <= prev:
                    return False
                prev = current.val
                current = current.right

    return True
```

---

## Complexity Analysis

| Approach | Time | Space | Notes |
|----------|------|-------|-------|
| Range-based (recursive) | O(n) | O(h) | Clean, intuitive |
| Range-based (iterative) | O(n) | O(h) | Avoids recursion |
| Inorder (recursive) | O(n) | O(h) | Uses BST property |
| Inorder (iterative) | O(n) | O(h) | Most common approach |
| Morris | O(n) | O(1) | Optimal space |

---

## Common Variations

### 1. With Equal Values Allowed

```python
def is_valid_bst_with_equals(root: TreeNode, allow_left_equal=True) -> bool:
    """
    Allow equal values on one side.

    Some definitions allow left <= root < right
    """
    def validate(node, min_val, max_val):
        if not node:
            return True

        if node.val < min_val or node.val > max_val:
            return False

        # Left can be equal, right must be strictly greater
        return (validate(node.left, min_val, node.val) and
                validate(node.right, node.val + 1, max_val))

    return validate(root, float('-inf'), float('inf'))
```

### 2. Find the Violating Nodes

```python
def find_bst_violations(root: TreeNode) -> list:
    """
    Find nodes that violate BST property.

    Useful for debugging or "recover BST" problems.
    """
    violations = []
    prev = [None]

    def inorder(node):
        if not node:
            return

        inorder(node.left)

        if prev[0] and node.val <= prev[0].val:
            violations.append((prev[0], node))
        prev[0] = node

        inorder(node.right)

    inorder(root)
    return violations
```

### 3. Recover BST (Two Nodes Swapped)

```python
def recover_tree(root: TreeNode) -> None:
    """
    Two nodes were swapped by mistake. Fix the BST.

    LeetCode 99: Recover Binary Search Tree

    Time: O(n)
    Space: O(h)
    """
    first = second = prev = None

    def inorder(node):
        nonlocal first, second, prev

        if not node:
            return

        inorder(node.left)

        if prev and node.val < prev.val:
            if not first:
                first = prev  # First violation
            second = node  # Second (or update second)

        prev = node
        inorder(node.right)

    inorder(root)

    # Swap values to fix
    first.val, second.val = second.val, first.val
```

---

## Edge Cases

```python
# 1. Empty tree
root = None
# → Valid BST (by convention)

# 2. Single node
root = TreeNode(1)
# → Valid BST

# 3. Two nodes
#   1
#    \
#     2   → Valid
#
#   2
#    \
#     1   → Invalid

# 4. Integer limits
root = TreeNode(2**31 - 1)  # Max int
# → Use float('-inf') and float('inf') for bounds

# 5. Duplicate values
#     2
#    /
#   2   → Invalid (standard BST doesn't allow duplicates)
```

---

## Interview Tips

1. **Know the trap**: Don't just check immediate children
2. **Prefer range approach**: More intuitive to explain
3. **Mention inorder**: Shows you know BST property
4. **Handle edge cases**: Empty tree, single node, integer overflow
5. **Clarify duplicates**: Ask if duplicates are allowed

---

## Practice Problems

| # | Problem | Difficulty | Key Concept |
|---|---------|------------|-------------|
| 1 | Validate Binary Search Tree | Medium | Core validation |
| 2 | Recover Binary Search Tree | Medium | Find and fix swapped nodes |
| 3 | Largest BST Subtree | Medium | Validate subtrees |
| 4 | Minimum Distance Between BST Nodes | Easy | Inorder with gaps |
| 5 | Two Sum IV - Input is a BST | Easy | BST traversal + two sum |

---

## Key Takeaways

1. **Use ranges**: Track valid (min, max) for each node
2. **Inorder = sorted**: BST inorder traversal is strictly increasing
3. **Watch for traps**: Don't just compare with parent
4. **Integer overflow**: Use float('-inf') and float('inf')
5. **Common follow-up**: "What if two nodes were swapped?"

---

## Next: [06-tree-construction.md](./06-tree-construction.md)

Learn how to construct binary trees from traversal sequences.

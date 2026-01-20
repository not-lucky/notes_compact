# Path Compression

> **Prerequisites:** [Union-Find Basics](./01-union-find-basics.md)

## Interview Context

Path compression is the first key optimization for Union-Find that reduces `find` operations from O(n) to O(log n) amortized. Interviewers expect you to know this optimization and implement it correctly. Combined with union by rank, it achieves nearly O(1) operations.

---

## Building Intuition

**The "Phone Tree" Mental Model**

Imagine a company where every employee knows their direct manager, but not the CEO. To find out who's the ultimate boss:

Without path compression:
```
Employee → Manager → Director → VP → CEO
Each query: "Who's your manager?" repeated up the chain
Every lookup: O(depth) time
```

With path compression:
```
First query: Employee → Manager → Director → VP → CEO
             (Remember: CEO is the ultimate boss!)
Update everyone: Employee → CEO
                 Manager → CEO
                 Director → CEO
                 VP → CEO

Next query: Employee → CEO (instant!)
```

**Why This Works**

The key insight: *We don't care about the intermediate managers—we only need the root.*

Once we've found the root, we "shortcut" everyone's pointer directly to it. This is lazy optimization:
- First access might be slow (traverse the chain)
- But it fixes the structure for all future accesses
- Amortized over many operations → nearly O(1)

**Visual Transformation**

```
Before find(7):                After find(7):
       0                              0
       |                         / / | \ \ \
       1                        1  2  3  4  5  7
       |
       2
       |
       3
       |
       4
       |
       5
       |
       7

Tall chain → flat star
```

**The Amortization Argument**

Each node can only move closer to the root, never further away. After path compression:
- A node at depth d gets moved to depth 1
- It can never go back to depth d
- Total "work" across all operations is bounded

---

## When NOT to Use Path Compression

**1. When You Need Parent Relationships**

Path compression destroys the original parent structure. If you need to know the original edges:

```python
# Original: 0 ← 1 ← 2 ← 3
# After find(3): 0 ← 1, 0 ← 2, 0 ← 3
# Lost: the information that 1 was parent of 2
```

**2. In Weighted Union-Find (Sometimes)**

With weighted Union-Find (tracking ratios like a/b = 2.5), path compression must also update weights. It's doable but requires careful implementation:

```python
# x/parent[x] = weight[x]
# When compressing x → root, must multiply weights along the path
```

**3. When Stack Depth is Constrained**

Recursive path compression can cause stack overflow on very deep trees. Use iterative version instead:

```python
# Recursive: O(depth) stack space
# Iterative two-pass: O(1) extra space
```

**4. When Modification is Forbidden**

If the structure is read-only or needs to remain unchanged for other uses, you can't apply path compression.

---

## The Problem: Tall Trees

Without optimization, the Union-Find tree can become a long chain:

```
After many unions without optimization:

  0
  |
  1
  |
  2
  |
  3
  |
  4

find(4) traverses: 4 → 3 → 2 → 1 → 0
That's O(n) for one find!
```

---

## Solution: Path Compression

**Key insight**: When we call `find(x)`, we traverse from x to the root. Why not make every node along the path point directly to the root?

### Before and After

```
Before find(4):
       0
       |
       1
       |
       2
       |
       3
       |
       4

After find(4) with path compression:
       0
     / | \ \
    1  2  3  4

All nodes now point directly to root!
Next find(4) is O(1).
```

---

## Implementation

### Recursive Path Compression

```python
class UnionFind:
    """
    Union-Find with path compression.

    Time: O(log n) amortized per operation
    Space: O(n) + O(log n) recursion stack
    """

    def __init__(self, n: int):
        self.parent = list(range(n))

    def find(self, x: int) -> int:
        """
        Find root with path compression.

        After this call, x and all its ancestors
        point directly to the root.
        """
        if self.parent[x] != x:
            # Recursively find root, then update parent
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x: int, y: int) -> bool:
        root_x = self.find(x)  # Path compression happens here
        root_y = self.find(y)  # And here

        if root_x == root_y:
            return False

        self.parent[root_y] = root_x
        return True


# Trace through example
uf = UnionFind(5)

# Build chain: 0 <- 1 <- 2 <- 3 <- 4
uf.parent = [0, 0, 1, 2, 3]

print("Before find(4):", uf.parent)  # [0, 0, 1, 2, 3]

root = uf.find(4)

print("After find(4):", uf.parent)   # [0, 0, 0, 0, 0]
print("Root:", root)                  # 0
```

### Iterative Path Compression (Two-Pass)

```python
def find(self, x: int) -> int:
    """
    Iterative path compression (two passes).

    Pass 1: Find the root
    Pass 2: Update all parents to root

    Advantage: No recursion stack overflow for deep trees.
    """
    # Pass 1: Find root
    root = x
    while self.parent[root] != root:
        root = self.parent[root]

    # Pass 2: Compress path
    while self.parent[x] != root:
        next_x = self.parent[x]
        self.parent[x] = root
        x = next_x

    return root
```

### Path Halving (One-Pass Approximation)

```python
def find(self, x: int) -> int:
    """
    Path halving: make every other node point to its grandparent.

    Simpler than full compression, similar performance.
    Single pass, no recursion.
    """
    while self.parent[x] != x:
        # Point to grandparent instead of parent
        self.parent[x] = self.parent[self.parent[x]]
        x = self.parent[x]
    return x
```

### Path Splitting (Another One-Pass Variant)

```python
def find(self, x: int) -> int:
    """
    Path splitting: every node points to its grandparent.

    Similar to halving but updates every node, not every other.
    """
    while self.parent[x] != x:
        next_x = self.parent[x]
        self.parent[x] = self.parent[next_x]  # Point to grandparent
        x = next_x
    return x
```

---

## Comparison of Techniques

```
Before: Chain 0 <- 1 <- 2 <- 3 <- 4 <- 5 <- 6 <- 7

Full compression after find(7):
       0
   / / | \ \ \ \
  1 2  3  4 5 6 7

Path halving after find(7):
       0
      /|
     1 2
      /|
     3 4
      /|
     5 6
       |
       7

Path splitting after find(7):
       0
      /|\
     1 2 4
         |\
         3 6
           |
           5 7
```

| Technique | Passes | Stack | Effectiveness |
|-----------|--------|-------|---------------|
| Full compression (recursive) | 2 | O(depth) | Best |
| Full compression (iterative) | 2 | O(1) | Best |
| Path halving | 1 | O(1) | Very good |
| Path splitting | 1 | O(1) | Very good |

---

## Problem: Longest Consecutive Sequence

**LeetCode 128**: Given an unsorted array of integers, find the length of the longest consecutive elements sequence.

### Example

```
Input: nums = [100, 4, 200, 1, 3, 2]
Output: 4
Explanation: The longest consecutive sequence is [1, 2, 3, 4].
```

### Union-Find Solution

```python
def longestConsecutive(nums: list[int]) -> int:
    """
    Use Union-Find to group consecutive numbers.

    Time: O(n × α(n)) ≈ O(n)
    Space: O(n)
    """
    if not nums:
        return 0

    parent = {}
    size = {}

    def find(x: int) -> int:
        if x not in parent:
            parent[x] = x
            size[x] = 1
        if parent[x] != x:
            parent[x] = find(parent[x])  # Path compression
        return parent[x]

    def union(x: int, y: int) -> None:
        px, py = find(x), find(y)
        if px != py:
            # Union by size
            if size[px] < size[py]:
                px, py = py, px
            parent[py] = px
            size[px] += size[py]

    num_set = set(nums)

    for num in num_set:
        # Only need to check one direction to avoid duplicate work
        if num + 1 in num_set:
            union(num, num + 1)

    # Find maximum component size
    max_length = 1
    for num in num_set:
        root = find(num)
        max_length = max(max_length, size[root])

    return max_length


# Trace
nums = [100, 4, 200, 1, 3, 2]
# After processing:
# 1-2, 2-3, 3-4 get unioned
# Component {1,2,3,4} has size 4
# 100 and 200 remain separate
```

---

## Problem: Satisfiability of Equality Equations

**LeetCode 990**: Given an array of equations like `["a==b","b!=c","c==a"]`, determine if all equations can be satisfied.

### Solution

```python
def equationsPossible(equations: list[str]) -> bool:
    """
    Use Union-Find: first union all equalities, then check inequalities.

    Time: O(n × α(26)) ≈ O(n)
    Space: O(26) = O(1)
    """
    parent = list(range(26))  # 26 letters

    def find(x: int) -> int:
        if parent[x] != x:
            parent[x] = find(parent[x])  # Path compression
        return parent[x]

    def union(x: int, y: int) -> None:
        parent[find(y)] = find(x)

    def char_to_idx(c: str) -> int:
        return ord(c) - ord('a')

    # First pass: process all equality equations
    for eq in equations:
        if eq[1] == '=':  # "a==b"
            x = char_to_idx(eq[0])
            y = char_to_idx(eq[3])
            union(x, y)

    # Second pass: check all inequality equations
    for eq in equations:
        if eq[1] == '!':  # "a!=b"
            x = char_to_idx(eq[0])
            y = char_to_idx(eq[3])
            if find(x) == find(y):
                return False  # Contradiction!

    return True


# Examples
print(equationsPossible(["a==b", "b!=a"]))  # False (a==b but a!=a is false)
print(equationsPossible(["a==b", "b==c", "a==c"]))  # True
print(equationsPossible(["a==b", "b!=c", "c==a"]))  # False (a==b==c but b!=c)
```

---

## Complexity Analysis

| Technique | Single find | m operations on n elements |
|-----------|-------------|---------------------------|
| No compression | O(n) | O(n × m) |
| Path compression only | O(log n)* | O(m × log n) |
| Path compression + rank | O(α(n))* | O(m × α(n)) |

*Amortized

The improvement comes from flattening the tree:
- After one expensive find, subsequent finds to the same path are O(1)
- Trees stay shallow over time

---

## Why Path Compression Works

```
Amortized analysis intuition:

Consider a node x at depth d.
- First find(x): O(d) work, but compresses path
- After compression: x is at depth 1
- Future finds: O(1)

Total work for all finds to x: O(d + k) for k finds
Amortized per find: O(d/k + 1)

As we do more finds, the amortized cost approaches O(1).
```

---

## Edge Cases

1. **Self-find**: `find(x)` when x is root → returns immediately
2. **Already compressed**: No extra work if path already flat
3. **Single element**: Works correctly (element is own root)
4. **Deep recursion**: Use iterative version for very deep trees

---

## Interview Tips

1. **Default to recursive**: Cleaner code, usually acceptable
2. **Mention iterative**: Show you know the stack overflow concern
3. **One-liner option**: `parent[x] = find(parent[x]); return parent[x]`
4. **Explain why it helps**: "Makes future finds faster by flattening the tree"

---

## Common Mistakes

1. **Forgetting to update parent**: `return find(self.parent[x])` without assignment
   ```python
   # Wrong
   def find(self, x):
       if self.parent[x] != x:
           return self.find(self.parent[x])  # Path not compressed!
       return x

   # Correct
   def find(self, x):
       if self.parent[x] != x:
           self.parent[x] = self.find(self.parent[x])  # Compress!
       return self.parent[x]
   ```

2. **Return wrong value**: Must return `parent[x]` after update, not `x`
   ```python
   # Wrong
   def find(self, x):
       if self.parent[x] != x:
           self.parent[x] = self.find(self.parent[x])
       return x  # Wrong! Should return parent[x]
   ```

---

## Practice Problems

| # | Problem | Difficulty | Key Concept |
|---|---------|------------|-------------|
| 1 | Longest Consecutive Sequence | Medium | Union consecutive numbers |
| 2 | Satisfiability of Equality Equations | Medium | Two-pass union then check |
| 3 | Number of Operations to Make Network Connected | Medium | Count components |
| 4 | Smallest String With Swaps | Medium | Group characters by index |
| 5 | Regions Cut By Slashes | Medium | Grid subdivision |

---

## Related Sections

- [Union-Find Basics](./01-union-find-basics.md) - Foundation
- [Union by Rank](./03-union-by-rank.md) - Second optimization
- [Connected Components](./04-connected-components.md) - Application

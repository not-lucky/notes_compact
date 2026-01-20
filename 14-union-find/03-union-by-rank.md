# Union by Rank

> **Prerequisites:** [Union-Find Basics](./01-union-find-basics.md), [Path Compression](./02-path-compression.md)

## Interview Context

Union by rank is the second key optimization for Union-Find. While path compression speeds up `find`, union by rank prevents tree imbalance during `union`. Together they achieve O(α(n)) ≈ O(1) amortized time per operation.

---

## Building Intuition

**The "Merging Companies" Mental Model**

Imagine two companies merging. Which CEO becomes the new overall CEO?

Bad strategy (arbitrary choice):
```
Company A (1000 employees) + Company B (10 employees)
If B's CEO becomes overall CEO:
  - 1000 employees must update their org chart
  - Deep hierarchy created unnecessarily
```

Good strategy (smaller under larger):
```
Company A (1000 employees) + Company B (10 employees)
A's CEO becomes overall CEO:
  - Only 10 employees update their direct reference
  - Hierarchy stays shallow
```

**The Key Insight**

*Attach the smaller/shorter tree under the larger/taller one.*

This minimizes the maximum depth any node can reach. If we always attach the tree with fewer levels under the taller tree, the combined tree's height grows minimally.

```
Two approaches:
1. Union by Rank (height): Track approximate tree height
2. Union by Size: Track number of elements

Both achieve O(log n) worst-case height guarantee.
```

**Why Height Matters**

```
Without union by rank:
Bad sequence: union(0,1), union(0,2), union(0,3), ...
Could create:  0 ← 1 ← 2 ← 3 ← 4 ← 5 ← ... ← n
Height: O(n)

With union by rank:
Same unions create:    0
                    / | | | \ \
                   1  2 3 4 5  ...
Height: O(1) for this case, O(log n) in general
```

**Visual Example**

```
Without rank (naive):
union(1, 0): 1 ← 0  (0 under 1)
union(2, 1): 2 ← 1 ← 0  (1 under 2)
union(3, 2): 3 ← 2 ← 1 ← 0  (2 under 3)
Result: Chain of height 3

With rank:
union(1, 0): 1 (rank 1)
             |
             0
union(2, 1): 1 (rank stays 1, since 2's rank is 0)
            /|
           2 0
union(3, 1): 1 (rank still 1)
           / | \
          2  0  3
Result: Star of height 1
```

---

## When NOT to Use Union by Rank

**1. When You Need Exact Component Sizes**

Rank is an approximation of height, not the actual count. If you need to know "how many elements are in this group?", use **union by size** instead:

```python
# Rank: Tracks tree height (approximate)
# After many operations, rank[root] might be 3
# But component could have 1000 elements

# Size: Tracks actual count
# size[root] = 1000 means exactly 1000 elements
```

**2. For Simple/Small Problems**

If n is small (< 1000) and you're doing few operations, the optimization overhead isn't worth it:

```python
# Small n: O(n) vs O(log n) doesn't matter much
# Code simplicity might be more valuable
# Naive union works fine for quick prototypes
```

**3. When Memory is Extremely Tight**

Union by rank requires an additional O(n) array for ranks. In memory-critical situations, you might skip it:

```python
# With rank: parent[n] + rank[n] = 2n space
# Without: parent[n] = n space
# For most practical cases, 2n is fine
```

**4. When Combined with Other Techniques**

Some advanced structures (like link-cut trees or offline algorithms) have their own balancing mechanisms that supersede union by rank.

---

## The Problem: Unbalanced Unions

Without rank-based union, we might always attach to the same root:

```
Naive union always attaches second to first:

union(0, 1): 0 <- 1
union(0, 2): 0 <- 1, 0 <- 2
union(0, 3): 0 <- 1, 0 <- 2, 0 <- 3

Result: Balanced tree (lucky case)
    0
   /|\
  1 2 3

But with different order:
union(1, 0): 1 <- 0
union(2, 1): 2 <- 1 <- 0
union(3, 2): 3 <- 2 <- 1 <- 0

Result: Chain (unlucky case)
3 <- 2 <- 1 <- 0

Tree height = O(n)
```

---

## Solution: Union by Rank

**Key insight**: Always attach the shorter tree under the taller tree. This keeps the combined tree as short as possible.

### Visualization

```
Union by rank example:

Before union(A, B):
  Tree A (rank 2)      Tree B (rank 1)
       a                    d
      / \                   |
     b   c                  e

After union(A, B):
Attach shorter (B) under taller (A)
       a
      / \
     b   c
          \
           d
           |
           e

Result: Height stays 2, not 3
```

---

## Implementation

### Union by Rank (Tree Height)

```python
class UnionFind:
    """
    Union-Find with path compression and union by rank.

    Time: O(α(n)) ≈ O(1) amortized per operation
    Space: O(n)
    """

    def __init__(self, n: int):
        self.parent = list(range(n))
        self.rank = [0] * n  # Approximate tree height

    def find(self, x: int) -> int:
        """Find with path compression."""
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x: int, y: int) -> bool:
        """
        Union by rank: attach smaller tree under larger.

        Returns True if merged, False if already same set.
        """
        px, py = self.find(x), self.find(y)

        if px == py:
            return False  # Already same set

        # Always attach smaller rank under larger rank
        if self.rank[px] < self.rank[py]:
            px, py = py, px  # Swap so px has larger rank

        self.parent[py] = px  # Attach py under px

        # Only increase rank if both had same rank
        if self.rank[px] == self.rank[py]:
            self.rank[px] += 1

        return True
```

### Why Rank Only Increases When Equal

```
Case 1: rank[px] > rank[py]
  Before:       After:
    px            px      Height unchanged
   /| \          /|\ \
  ...           ... py
                    |
                   ...

Case 2: rank[px] == rank[py]
  Before:       After:
    px   py       px       Height increases by 1
    |    |       /  \
   ...  ...     ...  py
                     |
                    ...

Case 3: rank[px] < rank[py] (handled by swap)
  Same as Case 1 after swapping px and py
```

---

### Union by Size (Alternative)

```python
class UnionFind:
    """
    Union-Find with union by size.

    Size is exact count of elements in subtree.
    Useful when you need to know component sizes.
    """

    def __init__(self, n: int):
        self.parent = list(range(n))
        self.size = [1] * n  # Each node starts as size 1

    def find(self, x: int) -> int:
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x: int, y: int) -> bool:
        px, py = self.find(x), self.find(y)

        if px == py:
            return False

        # Attach smaller tree under larger tree
        if self.size[px] < self.size[py]:
            px, py = py, px

        self.parent[py] = px
        self.size[px] += self.size[py]  # Update size

        return True

    def get_size(self, x: int) -> int:
        """Return size of component containing x."""
        return self.size[self.find(x)]
```

---

## Rank vs Size

| Aspect | Rank | Size |
|--------|------|------|
| Represents | Approximate tree height | Exact element count |
| Update | Only when ranks equal | Always add sizes |
| Use case | Pure optimization | When size needed |
| Complexity | Same O(α(n)) | Same O(α(n)) |
| Extra info | None | Component sizes |

```python
# Rank: Only tracks height, not count
# After many unions, rank[root] might be 3
# But component might have 1000 elements

# Size: Tracks actual count
# size[root] = 1000 means exactly 1000 elements
```

---

## Problem: Most Stones Removed with Same Row or Column

**LeetCode 947**: On a 2D plane, we place n stones at some integer coordinate points. Each coordinate point may have at most one stone. A stone can be removed if it shares either the same row or the same column as another stone. What is the maximum number of stones that can be removed?

### Key Insight

Stones in the same row/column form a connected component. From each component of size k, we can remove k-1 stones (leave one behind).

**Answer = n - number of components**

### Solution

```python
def removeStones(stones: list[list[int]]) -> int:
    """
    Use Union-Find to group stones by row/column.

    Key insight: Treat rows and columns as nodes.
    Stone at (r, c) connects row r with column c.
    Use offset to distinguish rows from columns.

    Time: O(n × α(n))
    Space: O(n)
    """
    parent = {}

    def find(x: int) -> int:
        if x not in parent:
            parent[x] = x
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    def union(x: int, y: int) -> None:
        parent[find(y)] = find(x)

    # Use offset to distinguish rows from columns
    # Row indices: 0, 1, 2, ...
    # Column indices: 10001, 10002, ... (offset by max coordinate + 1)
    OFFSET = 10001

    for r, c in stones:
        union(r, c + OFFSET)  # Connect row r with column c

    # Count unique components among the stones
    # Find all unique roots
    roots = set()
    for r, c in stones:
        roots.add(find(r))  # Could also use find(c + OFFSET)

    return len(stones) - len(roots)


# Example
stones = [[0,0],[0,1],[1,0],[1,2],[2,1],[2,2]]
# Visual:
#     0   1   2
# 0   X   X
# 1   X       X
# 2       X   X
#
# All connected through row/column sharing
# 1 component of 6 stones → remove 5
print(removeStones(stones))  # 5
```

---

## Problem: Swim in Rising Water

**LeetCode 778**: You're in an n×n grid where `grid[i][j]` represents elevation. At time `t`, you can swim to cells with elevation ≤ t. Find minimum time to reach from (0,0) to (n-1,n-1).

### Union-Find + Sorted Edges Approach

```python
def swimInWater(grid: list[list[int]]) -> int:
    """
    Process cells in order of elevation.
    When (0,0) and (n-1,n-1) are connected, return current elevation.

    Time: O(n² × α(n²)) ≈ O(n²)
    Space: O(n²)
    """
    n = len(grid)
    parent = list(range(n * n))
    rank = [0] * (n * n)

    def find(x: int) -> int:
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    def union(x: int, y: int) -> None:
        px, py = find(x), find(y)
        if px == py:
            return
        if rank[px] < rank[py]:
            px, py = py, px
        parent[py] = px
        if rank[px] == rank[py]:
            rank[px] += 1

    def to_idx(r: int, c: int) -> int:
        return r * n + c

    # Create list of (elevation, row, col) sorted by elevation
    cells = []
    for r in range(n):
        for c in range(n):
            cells.append((grid[r][c], r, c))
    cells.sort()

    # Process cells in order of elevation
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    for elevation, r, c in cells:
        # Connect with already-processed neighbors
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < n and 0 <= nc < n:
                if grid[nr][nc] <= elevation:  # Already processed
                    union(to_idx(r, c), to_idx(nr, nc))

        # Check if start and end are connected
        if find(0) == find(n * n - 1):
            return elevation

    return grid[n-1][n-1]  # Should not reach here
```

---

## Complexity Analysis

| Operation | Naive | Union by Rank Only | Path Compression Only | Both Optimizations |
|-----------|-------|-------------------|----------------------|-------------------|
| Find | O(n) | O(log n) | O(log n)* | O(α(n))* |
| Union | O(n) | O(log n) | O(log n)* | O(α(n))* |
| Connected | O(n) | O(log n) | O(log n)* | O(α(n))* |
| Space | O(n) | O(n) | O(n) | O(n) |

*Amortized. α(n) = inverse Ackermann function ≈ O(1) for practical inputs.

### Height Bound with Union by Rank

```
Theorem: With union by rank, tree height ≤ log₂(n)

Proof sketch:
- A tree of height h has at least 2^h nodes
- Why? To create height h, we need two height h-1 trees
- Height h-1 needs two height h-2 trees, etc.
- So height h needs at least 2^h nodes

Therefore: h ≤ log₂(n)
```

### Combined with Path Compression

```
With both optimizations:
- Time per operation: O(α(n)) amortized
- α(n) = inverse Ackermann function
- α(n) ≤ 4 for any n ≤ 10^80

For all practical purposes: O(1) per operation
```

---

## Common Mistakes

1. **Wrong rank update**:
   ```python
   # Wrong: always increment
   self.rank[px] += 1

   # Correct: only when equal
   if self.rank[px] == self.rank[py]:
       self.rank[px] += 1
   ```

2. **Forgetting to swap**:
   ```python
   # Wrong: might attach larger under smaller
   self.parent[py] = px

   # Correct: ensure px has larger rank first
   if self.rank[px] < self.rank[py]:
       px, py = py, px
   self.parent[py] = px
   ```

3. **Mixing rank and size semantics**:
   ```python
   # Wrong: treating rank as size
   self.rank[px] += self.rank[py]  # This is size logic!

   # Rank: only +1 when equal ranks
   # Size: always add sizes
   ```

---

## Edge Cases

1. **Single element**: Rank stays 0, element is its own root
2. **All elements same set**: Final rank ≤ log₂(n)
3. **Already same root**: union(x, y) when find(x) == find(y) returns False
4. **Duplicate unions**: No effect, rank doesn't increase incorrectly
5. **Large n**: Rank values stay small (max ~30 for n = 10^9)

---

## Interview Tips

1. **Default choice**: Use both rank and path compression
2. **Explain tradeoff**: "Rank keeps trees balanced during union"
3. **When to use size**: "If the problem needs component sizes"
4. **Quick implementation**: Can skip rank for simple problems, but mention it

---

## Practice Problems

| # | Problem | Difficulty | Key Concept |
|---|---------|------------|-------------|
| 1 | Most Stones Removed | Medium | Row/column as virtual nodes |
| 2 | Swim in Rising Water | Hard | Process in sorted order |
| 3 | Minimize Malware Spread | Hard | Component sizes matter |
| 4 | Minimize Malware Spread II | Hard | Remove node, recount |
| 5 | Making A Large Island | Hard | Try flipping each 0 |

---

## Related Sections

- [Union-Find Basics](./01-union-find-basics.md) - Foundation
- [Path Compression](./02-path-compression.md) - First optimization
- [Connected Components](./04-connected-components.md) - Counting components

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

_Attach the smaller/shorter tree under the larger/taller one._

This minimizes the maximum depth any node can reach. If we always attach the tree with fewer levels under the taller tree, the combined tree's height grows minimally.

```
Two approaches:
1. Union by Rank (height): Track upper bound on tree height
2. Union by Size: Track number of elements

Both achieve O(log n) worst-case height guarantee.
```

**Why Height Matters**

```
Without union by rank (naive: parent[find(y)] = find(x)):
Worst-case sequence: union(1,0), union(2,1), union(3,2), ...
Creates chain:  0 → 1 → 2 → 3 → ... → n-1
(each new node becomes root; old root points to it)
Height: O(n)

With union by rank:
Same unions create:       1
                       / | \ \
                      0  2  3  ...
(rank-1 root stays on top; rank-0 singletons attach under it)
Height: O(1) for this case, O(log n) worst case
```

**Visual Example**

Same 3 unions, different outcomes depending on strategy:

```
Without rank (naive worst case):

Naive union(x, y) does: parent[find(y)] = find(x)
This specific sequence always attaches the existing chain's root under
a fresh singleton, creating a degenerate chain.

union(1, 0): find(1)=1, find(0)=0 → parent[0] = 1
             Tree: 0 → 1

union(2, 1): find(2)=2, find(1)=1 → parent[1] = 2
             Tree: 0 → 1 → 2

union(3, 2): find(3)=3, find(2)=2 → parent[2] = 3
             Tree: 0 → 1 → 2 → 3

Result: Chain of height 3
Note: This is a WORST-CASE ordering. Different orderings (e.g., always
unioning into node 0) would produce a star even without rank.


With rank (same unions):

union(1, 0): find(1)=1, find(0)=0, rank[1]=rank[0]=0 (equal)
             → parent[0] = 1, rank[1] = 1
             Tree:  1 (rank 1)
                    |
                    0

union(2, 1): find(2)=2, find(1)=1, rank[2]=0 < rank[1]=1
             → swap so higher rank stays root: parent[2] = 1
             Tree:  1 (rank 1)
                   / \
                  0   2

union(3, 2): find(3)=3, find(2)=1, rank[3]=0 < rank[1]=1
             → swap: parent[3] = 1
             Tree:  1 (rank 1)
                   /|\
                  0 2 3

Result: Star of height 1
```

---

## When NOT to Use Union by Rank

**1. When You Need Exact Component Sizes**

Rank is an upper bound on tree height, not the actual count. If you need to know "how many elements are in this group?", use **union by size** instead:

```python
# Rank: Tracks tree height upper bound (not size)
# After path compression, rank[root] might be 3
# But actual tree height could be 1, and component could have 1000 elements

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

Without rank-based union, tree shape depends entirely on operation order:

```
Naive union(x, y) does: parent[find(y)] = find(x)

union(0, 1): find(0)=0, find(1)=1 → parent[1] = 0
union(0, 2): find(0)=0, find(2)=2 → parent[2] = 0
union(0, 3): find(0)=0, find(3)=3 → parent[3] = 0

Result: Balanced star (lucky ordering — root stays the same)
    0
   /|\
  1 2 3

But with different order:
union(1, 0): find(1)=1, find(0)=0 → parent[0] = 1
union(2, 1): find(2)=2, find(1)=1 → parent[1] = 2
union(3, 2): find(3)=3, find(2)=2 → parent[2] = 3

Result: Chain (unlucky ordering — each new node becomes root)
0 → 1 → 2 → 3

Tree height = O(n)
```

---

## Solution: Union by Rank

**Key insight**: Always attach the shorter tree under the taller tree. This keeps the combined tree as short as possible.

### Visualization

```
Union by rank example:

Before union(A, B):
  Tree A (rank 2)          Tree B (rank 1)
       a                        d
      / \                       |
     b   c                      e
     |
     f

After union(A, B):
Attach root of shorter tree (d) directly under root of taller tree (a)
         a
       / | \
      b  c  d
      |     |
      f     e

Result: Height stays 2, not 3
(d attaches under the ROOT, not under an arbitrary child)
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
        self.rank = [0] * n  # Upper bound on tree height

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

    def connected(self, x: int, y: int) -> bool:
        """Check if x and y are in the same set."""
        return self.find(x) == self.find(y)
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
    Union-Find with path compression and union by size.

    Size is exact count of elements in component.
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

    def connected(self, x: int, y: int) -> bool:
        """Check if x and y are in the same set."""
        return self.find(x) == self.find(y)
```

---

## Rank vs Size

| Aspect     | Rank                    | Size                |
| ---------- | ----------------------- | ------------------- |
| Represents | Upper bound on height   | Exact element count |
| Update     | Only when ranks equal   | Always add sizes    |
| Use case   | Pure optimization       | When size needed    |
| Complexity | Same O(α(n))            | Same O(α(n))        |
| Extra info | None                    | Component sizes     |

```python
# Rank: Only tracks height upper bound, not count
# After many unions, rank[root] might be 3
# But component might have 1000 elements

# Size: Tracks actual count
# size[root] = 1000 means exactly 1000 elements
```

---

## Problem: Maximum Tree Height After Unions (Warm-Up)

**Educational Problem**: Given `n` nodes (0 to n-1) and a list of union operations, compute the maximum tree height in the Union-Find forest **with** and **without** union by rank. This demonstrates why rank-based union matters.

### Key Insight

Without rank, a bad sequence of unions can produce a chain of height O(n). With rank, the same operations keep height ≤ log₂(n). This problem makes the difference concrete.

### Solution

```python
def max_tree_height_comparison(
    n: int, operations: list[tuple[int, int]]
) -> tuple[int, int]:
    """
    Perform the same union operations with and without union by rank.
    Return (height_without_rank, height_with_rank).

    Time: O(m × n) worst case without rank, O(m × log n) with rank
          (path compression disabled here to measure true tree height)
    Space: O(n)
    """
    # --- Without union by rank (naive) ---
    parent_naive: list[int] = list(range(n))

    def find_naive(x: int) -> int:
        while parent_naive[x] != x:
            x = parent_naive[x]
        return x

    def union_naive(x: int, y: int) -> None:
        px, py = find_naive(x), find_naive(y)
        if px != py:
            parent_naive[py] = px  # Always attach py under px (arbitrary)

    for x, y in operations:
        union_naive(x, y)

    # Measure height: for each node, walk to root and count steps (= depth)
    # The max depth across all nodes equals the tree height.
    def depth_of(parent: list[int], node: int) -> int:
        d = 0
        while parent[node] != node:
            node = parent[node]
            d += 1
        return d

    naive_max_height = max(depth_of(parent_naive, i) for i in range(n))

    # --- With union by rank ---
    parent_rank: list[int] = list(range(n))
    rank: list[int] = [0] * n

    def find_rank(x: int) -> int:
        # No path compression here so we can measure true tree height
        while parent_rank[x] != x:
            x = parent_rank[x]
        return x

    def union_rank(x: int, y: int) -> None:
        px, py = find_rank(x), find_rank(y)
        if px == py:
            return
        if rank[px] < rank[py]:
            px, py = py, px
        parent_rank[py] = px
        if rank[px] == rank[py]:
            rank[px] += 1

    for x, y in operations:
        union_rank(x, y)

    rank_max_height = max(depth_of(parent_rank, i) for i in range(n))

    return naive_max_height, rank_max_height


# --- Example 1: Worst-case sequence for naive ---
# union(i+1, i) attaches the existing chain's root under each new singleton,
# creating a degenerate chain in the naive case. Rank prevents this entirely.
n = 8
ops_chain = [(i + 1, i) for i in range(7)]
naive_h, rank_h = max_tree_height_comparison(n, ops_chain)
print(f"Chain sequence (n={n}): {ops_chain}")
print(f"  Without rank: max height = {naive_h}")  # 7 (degenerate chain)
print(f"  With rank:    max height = {rank_h}")    # 1 (star — all attach to root)

# --- Example 2: Balanced merge sequence (worst case for rank) ---
# Pair-wise merges force rank to grow. This is the worst case for rank,
# reaching its theoretical maximum of log₂(n). Naive gets the same height
# here because balanced merges don't create chains.
ops_balanced = [(0, 1), (2, 3), (4, 5), (6, 7), (0, 2), (4, 6), (0, 4)]
naive_h2, rank_h2 = max_tree_height_comparison(n, ops_balanced)
print(f"\nBalanced sequence (n={n}): {ops_balanced}")
print(f"  Without rank: max height = {naive_h2}")  # 3 (log₂(8) = 3)
print(f"  With rank:    max height = {rank_h2}")    # 3 (log₂(8) = 3)

# Takeaway: naive can degrade to O(n), but rank guarantees height ≤ log₂(n)
# regardless of operation order.
```

**Why this matters in interviews**: When an interviewer asks "why use union by rank?", you can explain that without it, `find()` degrades to O(n) per call in the worst case, making the overall algorithm potentially O(n²) instead of O(n log n) or O(n α(n)).

---

## Problem: Earliest Moment When Everyone Becomes Friends

**LeetCode 1101**: In a social group of `n` people (labeled `0` to `n-1`), you're given a list of logs where `logs[i] = [timestamp, x, y]` means persons `x` and `y` became friends at `timestamp`. Return the earliest time at which every person became acquainted with every other person (i.e., all are in one connected component). Return `-1` if it never happens.

### Key Insight

Sort logs by timestamp, process each friendship with union by rank, and track the number of components. When components reaches 1, return the current timestamp.

### Solution

```python
def earliestAcq(logs: list[list[int]], n: int) -> int:
    """
    Sort friendships by time, union them, return when all connected.

    Time: O(m log m + m × α(n)) where m = len(logs)
    Space: O(n)
    """
    parent = list(range(n))
    rank = [0] * n
    components = n

    def find(x: int) -> int:
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    def union(x: int, y: int) -> bool:
        px, py = find(x), find(y)
        if px == py:
            return False
        if rank[px] < rank[py]:
            px, py = py, px
        parent[py] = px
        if rank[px] == rank[py]:
            rank[px] += 1
        return True

    logs.sort()  # Sort by timestamp (first element)

    for timestamp, x, y in logs:
        if union(x, y):
            components -= 1
            if components == 1:
                return timestamp

    return -1


# Example
logs = [[0, 2, 0], [1, 0, 1], [3, 0, 3], [4, 1, 2], [7, 3, 1]]
print(earliestAcq(logs, 4))  # 3
# At t=0: {0,2}, {1}, {3}
# At t=1: {0,1,2}, {3}
# At t=3: {0,1,2,3} → all connected, return 3
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

    Time: O(n × α(n)) where n = len(stones)
    Space: O(n) for parent/rank dicts (at most 2n keys: n rows + n columns)
    """
    parent = {}
    rank = {}

    def find(x: int) -> int:
        if x not in parent:
            parent[x] = x
            rank[x] = 0
        if parent[x] != x:
            parent[x] = find(parent[x])  # Path compression
        return parent[x]

    def union(x: int, y: int) -> None:
        px, py = find(x), find(y)
        if px == py:
            return
        # Union by rank to keep trees balanced
        if rank[px] < rank[py]:
            px, py = py, px
        parent[py] = px
        if rank[px] == rank[py]:
            rank[px] += 1

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

## Problem: Redundant Connection

**LeetCode 684**: A tree is a connected graph with no cycles. You are given a graph that started as a tree with `n` nodes (labeled `1` to `n`), with one additional edge added. Return the edge that, if removed, would result in a tree. If there are multiple answers, return the edge that occurs last in the input.

### Key Insight

Process edges one by one. The first edge that connects two already-connected nodes creates a cycle -- that's the redundant edge. Union by rank ensures `find()` stays O(log n) worst case, so the overall algorithm is O(n * alpha(n)) instead of potentially O(n^2) with naive union.

### Solution

```python
def findRedundantConnection(edges: list[list[int]]) -> list[int]:
    """
    Process edges in order; the first that forms a cycle is redundant.

    Time: O(n * alpha(n)) -- n edges, each union/find is O(alpha(n))
    Space: O(n)
    """
    n = len(edges)  # n edges for n nodes means exactly 1 extra edge
    parent = list(range(n + 1))  # 1-indexed nodes
    rank = [0] * (n + 1)

    def find(x: int) -> int:
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    def union(x: int, y: int) -> bool:
        """Returns False if x and y are already connected (cycle detected)."""
        px, py = find(x), find(y)
        if px == py:
            return False  # Cycle: both already in same component
        if rank[px] < rank[py]:
            px, py = py, px
        parent[py] = px
        if rank[px] == rank[py]:
            rank[px] += 1
        return True

    for u, v in edges:
        if not union(u, v):
            return [u, v]

    return []  # Unreachable for valid input


# Example 1
edges1 = [[1, 2], [1, 3], [2, 3]]
print(findRedundantConnection(edges1))  # [2, 3]
# After [1,2]: {1,2}, {3}
# After [1,3]: {1,2,3}
# [2,3]: 2 and 3 already connected → redundant

# Example 2
edges2 = [[1, 2], [2, 3], [3, 4], [1, 4], [1, 5]]
print(findRedundantConnection(edges2))  # [1, 4]
# After [1,2],[2,3],[3,4]: chain 1-2-3-4
# [1,4]: 1 and 4 already connected → cycle detected
```

**Why union by rank matters here**: Without rank, processing the edges could build a degenerate chain, making each `find()` call O(n). With n edges, that's O(n^2) total. Union by rank guarantees O(n log n) worst case, and combined with path compression, O(n * alpha(n)).

---

## Problem: Swim in Rising Water

**LeetCode 778**: You're in an n×n grid where `grid[i][j]` represents elevation. At time `t`, you can swim to cells with elevation ≤ t. Find minimum time to reach from (0,0) to (n-1,n-1).

### Union-Find + Sorted Edges Approach

```python
def swimInWater(grid: list[list[int]]) -> int:
    """
    Process cells in order of elevation.
    When (0,0) and (n-1,n-1) are connected, return current elevation.

    Time: O(n^2 log n) due to sorting n^2 cells by elevation
          (Since elevations are a permutation of 0..n^2-1, we could use
          an index array to avoid sorting, but comparison sort is simpler.)
    Space: O(n^2)
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
    cells = sorted(
        (grid[r][c], r, c)
        for r in range(n)
        for c in range(n)
    )

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

    # Unreachable for valid input: the loop processes every cell, so at
    # minimum the last cell processed connects start to end.
    raise AssertionError("grid has no valid path")
```

---

## Complexity Analysis

| Operation | Naive | Union by Rank Only | Path Compression Only | Both Optimizations |
| --------- | ----- | ------------------ | --------------------- | ------------------ |
| Find      | O(n)  | O(log n)           | O(log n)\*            | O(α(n))\*          |
| Union     | O(n)  | O(log n)           | O(log n)\*            | O(α(n))\*          |
| Connected | O(n)  | O(log n)           | O(log n)\*            | O(α(n))\*          |
| Space     | O(n)  | O(n)               | O(n)                  | O(n)               |

\*Amortized. Union by rank alone gives O(log n) **worst-case per operation** (not amortized). Path compression alone gives O(log n) amortized. Combined, they give O(alpha(n)) amortized where alpha(n) is the inverse Ackermann function, effectively constant for all practical inputs (alpha(n) <= 4 for n <= 10^80).

### Height Bound Proof

```
Theorem: With union by rank (no path compression), tree height <= log_2(n).

Proof (by induction on rank r):
- Claim: A tree with root rank r has at least 2^r nodes.
- Base case (r=0): A rank-0 tree is a single node. 2^0 = 1. Check.
- Inductive step: A root's rank increases from r-1 to r only when
  merging with another rank-(r-1) tree (rank only increments when equal).
  By the inductive hypothesis, each subtree has >= 2^(r-1) nodes.
  Combined: >= 2^(r-1) + 2^(r-1) = 2^r nodes.
- Conclusion: A tree of rank r has >= 2^r nodes.
  Since total nodes n >= 2^r, we get r <= log_2(n).

Note: Path compression does NOT change rank values (rank is an upper
bound, not exact height). This is why rank remains a valid bound even
after path compression flattens the tree.
```

### Combined with Path Compression

```
With both optimizations:
- Time per operation: O(alpha(n)) amortized
- alpha(n) = inverse Ackermann function
- alpha(n) <= 4 for any n <= 10^80
- Proven optimal: no comparison-based UF can do better (Tarjan 1975)

For all practical purposes: O(1) per operation.
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

| #   | Problem                         | Difficulty | Key Concept                       |
| --- | ------------------------------- | ---------- | --------------------------------- |
| 0   | Max Tree Height (warm-up)       | Easy       | Compare height with/without rank  |
| 1   | LC 1101 - Earliest Friends      | Easy       | Sort + union + count components   |
| 2   | LC 947 - Most Stones Removed    | Medium     | Row/column as virtual nodes       |
| 3   | LC 684 - Redundant Connection   | Medium     | Detect cycle-forming edge         |
| 4   | LC 778 - Swim in Rising Water   | Hard       | Process in sorted order           |
| 5   | LC 924 - Minimize Malware       | Hard       | Component sizes matter            |
| 6   | LC 928 - Minimize Malware II    | Hard       | Remove node, recount              |
| 7   | LC 827 - Making A Large Island  | Hard       | Try flipping each 0               |

Problems 0-4 have full solutions in this file.

---

## Related Sections

- [Union-Find Basics](./01-union-find-basics.md) - Foundation
- [Path Compression](./02-path-compression.md) - First optimization
- [Connected Components](./04-connected-components.md) - Counting components

# Chapter 14: Union-Find / Disjoint Set

Union-Find (also called Disjoint Set Union or DSU) is a data structure that tracks elements partitioned into disjoint subsets. It provides near-constant time operations for combining sets and determining if two elements belong to the same set.

## Why Union-Find Matters

1. **Interview frequency**: Appears in ~5-10% of FANG interviews
2. **Efficiency**: O(α(n)) ≈ O(1) operations with optimizations
3. **Graph problems**: Essential for connected components and cycle detection
4. **System design**: Models network connectivity, social graphs

---

## Union-Find vs Other Approaches

| Problem | Union-Find | DFS/BFS | Time Comparison |
|---------|------------|---------|-----------------|
| Connected components (static) | O(n × α(n)) | O(V + E) | Similar |
| Connected components (dynamic) | O(n × α(n)) | O(n × (V + E)) | UF much faster |
| Cycle detection (undirected) | O(E × α(n)) | O(V + E) | Similar |
| Path connectivity queries | O(α(n)) per query | O(V + E) per query | UF much faster |

α(n) = inverse Ackermann function, effectively constant (≤ 4 for any practical n)

---

## Union-Find Structure Visualization

```
Initial: 5 separate elements [0, 1, 2, 3, 4]

Sets: {0}, {1}, {2}, {3}, {4}
Parent: [0, 1, 2, 3, 4]  (each element is its own parent)

After union(0, 1):
Sets: {0, 1}, {2}, {3}, {4}
Parent: [0, 0, 2, 3, 4]  (1 points to 0)
        0
        |
        1

After union(2, 3):
Sets: {0, 1}, {2, 3}, {4}
Parent: [0, 0, 2, 2, 4]
        0       2
        |       |
        1       3

After union(0, 2):
Sets: {0, 1, 2, 3}, {4}
Parent: [0, 0, 0, 2, 4]  (2's root now points to 0)
            0
          / |
         1  2
            |
            3
```

---

## When to Use Union-Find

### Strong Indicators (Use Union-Find)

1. **"Connected"/"grouped" elements**: Finding if two elements are connected
2. **"Merge"/"union" operations**: Combining groups of elements
3. **Dynamic connectivity**: Edges added over time, need real-time queries
4. **Cycle detection**: In undirected graphs
5. **Minimum spanning tree**: Kruskal's algorithm

### Weak Indicators (Consider Alternatives)

1. **Path between nodes**: BFS/DFS if you need the actual path
2. **Shortest path**: Dijkstra/BFS instead
3. **All connected components at once**: DFS might be simpler
4. **Directed graphs**: Union-Find doesn't handle direction

---

## Core Operations

| Operation | Time (naive) | Time (optimized) | Description |
|-----------|--------------|------------------|-------------|
| MakeSet | O(1) | O(1) | Create new set with single element |
| Find | O(n) | O(α(n)) ≈ O(1) | Find root/representative of element's set |
| Union | O(n) | O(α(n)) ≈ O(1) | Merge two sets |
| Connected | O(n) | O(α(n)) ≈ O(1) | Check if two elements in same set |

---

## Union-Find Patterns Overview

| Pattern | Problems | Key Strategy |
|---------|----------|--------------|
| Basic UF | Number of provinces, friend circles | Simple connectivity |
| UF + Rank | Most problems | Balanced trees |
| UF + Path Compression | Most problems | Flat trees |
| UF + Both | Optimal solution | Near O(1) operations |
| UF + Graph | Cycle detection, MST | Process edges |
| UF + Mapping | Accounts merge | Map strings to indices |

---

## Chapter Contents

| # | Topic | Key Concepts |
|---|-------|--------------|
| 01 | [Union-Find Basics](./01-union-find-basics.md) | Basic implementation, find, union |
| 02 | [Path Compression](./02-path-compression.md) | Flatten tree during find |
| 03 | [Union by Rank](./03-union-by-rank.md) | Balance trees during union |
| 04 | [Connected Components](./04-connected-components.md) | Count and identify groups |
| 05 | [Accounts Merge](./05-accounts-merge.md) | Complex merging with mapping |
| 06 | [Redundant Connection](./06-redundant-connection.md) | Cycle detection |

---

## Implementation Template

```python
class UnionFind:
    """
    Union-Find with path compression and union by rank.

    Time: O(α(n)) ≈ O(1) per operation
    Space: O(n)
    """

    def __init__(self, n: int):
        self.parent = list(range(n))  # Each element is its own parent
        self.rank = [0] * n           # Tree height (for balancing)

    def find(self, x: int) -> int:
        """Find root with path compression."""
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # Path compression
        return self.parent[x]

    def union(self, x: int, y: int) -> bool:
        """Union by rank. Returns True if merged, False if already same set."""
        px, py = self.find(x), self.find(y)
        if px == py:
            return False  # Already in same set

        # Union by rank: attach smaller tree under larger
        if self.rank[px] < self.rank[py]:
            px, py = py, px
        self.parent[py] = px
        if self.rank[px] == self.rank[py]:
            self.rank[px] += 1

        return True

    def connected(self, x: int, y: int) -> bool:
        """Check if two elements are in the same set."""
        return self.find(x) == self.find(y)
```

---

## Common Mistakes

1. **Forgetting path compression**: Makes operations O(n) instead of O(α(n))
2. **Wrong union direction**: Not using rank leads to unbalanced trees
3. **Off-by-one with indices**: Careful with 0-indexed vs 1-indexed
4. **Not handling self-loops**: find(x) should return x if parent[x] == x
5. **Modifying during iteration**: Union can change parents mid-loop

---

## Time Complexity Analysis

| Operation Sequence | Naive | Path Compression Only | Union by Rank Only | Both |
|--------------------|-------|----------------------|-------------------|------|
| n unions + m finds | O(n × m) | O(n + m × log n) | O(n + m × log n) | O(n + m × α(n)) |

The inverse Ackermann function α(n) grows extremely slowly:
- α(10^80) < 5
- For all practical purposes, α(n) ≤ 4

---

## Space Complexity

```
O(n) where n = number of elements

Storage:
- parent array: O(n)
- rank array: O(n)
- Total: O(n)

# No recursion stack with iterative path compression
```

---

## Classic Interview Problems by Company

| Company | Favorite Union-Find Problems |
|---------|------------------------------|
| Google | Accounts Merge, Number of Islands II, Satisfiability of Equality Equations |
| Meta | Friend Circles, Redundant Connection, Most Stones Removed |
| Amazon | Number of Provinces, Regions Cut By Slashes |
| Microsoft | Evaluate Division, Smallest String With Swaps |
| Apple | Graph Valid Tree, Longest Consecutive Sequence |

---

## Union-Find Problem Signals

Look for these keywords/patterns:

```
- "Connected"/"connectivity" → Union-Find
- "Group"/"cluster"/"partition" → Union-Find
- "Merge"/"union"/"combine" → Union-Find
- "Same set"/"same group" → Union-Find
- "Undirected graph + cycles" → Union-Find
- "Dynamic edges" (edges added over time) → Union-Find
- "Kruskal's MST" → Union-Find
```

---

## Comparison: When Union-Find vs DFS/BFS

| Scenario | Use Union-Find | Use DFS/BFS |
|----------|---------------|-------------|
| Dynamic edge additions | Yes | |
| Multiple connectivity queries | Yes | |
| Need actual path | | Yes |
| One-time component count | | Yes (simpler) |
| Cycle detection (undirected) | Yes | Yes |
| Cycle detection (directed) | | Yes |
| Shortest path | | Yes |

---

## Common Variations

### 1. Union-Find with Size

Track size of each set instead of rank:

```python
def __init__(self, n):
    self.parent = list(range(n))
    self.size = [1] * n  # Size of each set

def union(self, x, y):
    px, py = self.find(x), self.find(y)
    if px == py:
        return False

    # Union by size: attach smaller to larger
    if self.size[px] < self.size[py]:
        px, py = py, px
    self.parent[py] = px
    self.size[px] += self.size[py]
    return True
```

### 2. Union-Find with Component Count

```python
def __init__(self, n):
    self.parent = list(range(n))
    self.rank = [0] * n
    self.count = n  # Number of connected components

def union(self, x, y):
    px, py = self.find(x), self.find(y)
    if px == py:
        return False

    # Merge...
    self.count -= 1  # One less component
    return True

def get_count(self):
    return self.count
```

### 3. Weighted Union-Find

For problems like Evaluate Division (x/y = value):

```python
def __init__(self, n):
    self.parent = list(range(n))
    self.weight = [1.0] * n  # weight[x] = x / parent[x]

def find(self, x):
    if self.parent[x] != x:
        root = self.find(self.parent[x])
        self.weight[x] *= self.weight[self.parent[x]]
        self.parent[x] = root
    return self.parent[x]
```

---

## Quick Reference: When to Use Which Variant

| Variant | Use When |
|---------|----------|
| Basic + Path Compression + Rank | Default choice, most problems |
| With Size | Need size of largest component |
| With Count | Need number of components |
| Weighted | Ratios/relationships between elements |

---

## Start: [01-union-find-basics.md](./01-union-find-basics.md)

Begin with the fundamental Union-Find implementation that forms the basis for all Union-Find problems.

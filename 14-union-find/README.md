# Chapter 14: Union-Find / Disjoint Set

Union-Find (also called Disjoint Set Union or DSU) is a data structure that tracks elements partitioned into disjoint subsets. It provides near-constant time operations for combining sets and determining if two elements belong to the same set.

## Building Intuition

**The "Friendship Groups" Mental Model**

Imagine a school where students form friend groups:

- Initially, everyone is a stranger (n groups of 1)
- When two people become friends, their entire friend circles merge
- The question "Are A and B in the same friend group?" becomes easy

```
Day 1: Alice, Bob, Carol, Dave (4 separate groups)

Alice befriends Bob:    {Alice, Bob}, {Carol}, {Dave}
Carol befriends Dave:   {Alice, Bob}, {Carol, Dave}
Alice befriends Carol:  {Alice, Bob, Carol, Dave}  ← All connected!
```

**Why Union-Find is Elegant**

The magic is in how we answer "Are X and Y connected?":

- Each group has a "representative" (the root)
- Two people are in the same group if they have the same representative
- No need to store or search through member lists!

```
Traditional approach: Check if Y is in X's friend list
Time: O(n) per query

Union-Find approach: Check if find(X) == find(Y)
Time: O(α(n)) ≈ O(1) per query
```

**When Does Union-Find Shine?**

Union-Find is the go-to when you see:

1. **Dynamic grouping**: Elements merge over time
2. **Connectivity queries**: "Are these connected?"
3. **Cycle detection**: In undirected graphs
4. **Equivalence classes**: Transitive relationships

---

## Why Union-Find Matters

1. **Interview frequency**: Appears in ~5-10% of FANG interviews
2. **Efficiency**: $O(\alpha(n)) \approx O(1)$ operations with optimizations
3. **Graph problems**: Essential for connected components and cycle detection
4. **System design**: Models network connectivity, social graphs

---

## Union-Find vs Other Approaches

| Problem                        | Union-Find        | DFS/BFS            | Time Comparison |
| ------------------------------ | ----------------- | ------------------ | --------------- |
| Connected components (static)  | $O(E \cdot \alpha(V))$       | $O(V + E)$           | Similar         |
| Connected components (dynamic) | $O(\alpha(V))$ per update | $O(V + E)$ per query | UF much faster  |
| Cycle detection (undirected)   | $O(E \cdot \alpha(V))$       | $O(V + E)$           | Similar         |
| Path connectivity queries      | $O(\alpha(V))$ per query | $O(V + E)$ per query | UF much faster  |

$\alpha(V)$ = inverse Ackermann function, effectively constant ($\le 4$ for any practical $V$)

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

| Operation | Time (naive) | Time (optimized) | Description                               |
| --------- | ------------ | ---------------- | ----------------------------------------- |
| MakeSet   | $O(1)$         | $O(1)$             | Create new set with single element        |
| Find      | $O(n)$         | $O(\alpha(n)) \approx O(1)$   | Find root/representative of element's set |
| Connect/Union | $O(n)$         | $O(\alpha(n)) \approx O(1)$   | Merge two sets                            |
| Connected | $O(n)$         | $O(\alpha(n)) \approx O(1)$   | Check if two elements in same set         |

---

## Union-Find Patterns Overview

| Pattern               | Problems                            | Key Strategy           |
| --------------------- | ----------------------------------- | ---------------------- |
| Basic UF              | Number of provinces, friend circles | Simple connectivity    |
| UF + Rank             | Most problems                       | Balanced trees         |
| UF + Path Compression | Most problems                       | Flat trees             |
| UF + Both             | Optimal solution                    | Near O(1) operations   |
| UF + Graph            | Cycle detection, MST                | Process edges          |
| UF + Mapping          | Accounts merge                      | Map strings to indices |

---

## Chapter Contents

| #   | Topic                                                | Key Concepts                      |
| --- | ---------------------------------------------------- | --------------------------------- |
| 01  | [Union-Find Basics](./01-union-find-basics.md)       | Basic implementation, find, union |
| 02  | [Path Compression](./02-path-compression.md)         | Flatten tree during find          |
| 03  | [Union by Rank](./03-union-by-rank.md)               | Balance trees during union        |
| 04  | [Connected Components](./04-connected-components.md) | Count and identify groups         |
| 05  | [Accounts Merge](./05-accounts-merge.md)             | Complex merging with mapping      |
| 06  | [Redundant Connection](./06-redundant-connection.md) | Cycle detection                   |

---

## Implementation Template

```python
class UnionFind:
    """
    Union-Find with path compression and union by rank.

    Time:  O(α(n)) ≈ O(1) amortized per operation
    Space: O(n)
    """

    def __init__(self, n: int):
        self.parent = list(range(n))  # parent[i] = i means i is a root
        self.rank = [0] * n           # Upper bound on tree height

    def find(self, x: int) -> int:
        """Find root of x's set, compressing the path to the root."""
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # Path compression
        return self.parent[x]

    def union(self, x: int, y: int) -> bool:
        """Merge sets containing x and y. Returns False if already in same set."""
        px, py = self.find(x), self.find(y)
        if px == py:
            return False

        # Union by rank: attach shorter tree under taller tree's root
        if self.rank[px] < self.rank[py]:
            self.parent[px] = py
        elif self.rank[px] > self.rank[py]:
            self.parent[py] = px
        else:
            self.parent[py] = px
            self.rank[px] += 1  # Height increases only when ranks are equal

        return True

    def connected(self, x: int, y: int) -> bool:
        """Check if x and y belong to the same set."""
        return self.find(x) == self.find(y)
```

---

## Common Mistakes

1. **Forgetting path compression**: With rank but no path compression, a single `find` is $O(\log n)$; without either optimization, `find` degrades to $O(n)$ (a flat linked list)
2. **Wrong union direction**: Not using rank/size leads to unbalanced trees
3. **Off-by-one with indices**: Careful with 0-indexed vs 1-indexed
4. **Wrong base case in `find`**: `find(x)` must return `x` when `parent[x] == x`; also handle graph self-loops (edge from a node to itself) before calling `union`
5. **Modifying during iteration**: `union` can change parents mid-loop; collect results first
6. **Python recursion limit**: Recursive `find` can hit Python's default 1000-call limit on large inputs. Use `sys.setrecursionlimit` or an iterative `find`:

```python
def find_iterative(self, x: int) -> int:
    """Iterative find with two-pass path compression (no recursion limit risk)."""
    root = x
    while self.parent[root] != root:
        root = self.parent[root]
    while self.parent[x] != root:
        self.parent[x], x = root, self.parent[x]
    return root
```

---

## Time Complexity Analysis

| Operation Sequence | Naive    | Path Compression Only | Union by Rank Only | Both            |
| ------------------ | -------- | --------------------- | ------------------ | --------------- |
| $n$ unions + $m$ finds | $O(n \cdot m)$ | $O(n + m \log^* n)$      | $O(n + m \log n)$   | $O(n + m \cdot \alpha(n))$ |

$\log^* n$ = iterated logarithm (number of times you apply $\log$ before reaching $\le 1$).
Even slower-growing than $\log n$ but faster-growing than $\alpha(n)$.

The inverse Ackermann function $\alpha(n)$ grows extremely slowly:

- $\alpha(10^{80}) < 5$
- For all practical purposes, $\alpha(n) \le 4$

---

## Space Complexity

```
O(n) where n = number of elements

Storage:
- parent array: O(n)
- rank array:   O(n)
- Total:        O(n)

Note: Recursive path compression adds O(depth) stack space per find,
but after compression the depth approaches O(1). Use iterative
two-pass find to guarantee O(1) auxiliary space if needed.
```

---

## Classic Interview Problems by Company

| Company   | Favorite Union-Find Problems                                               |
| --------- | -------------------------------------------------------------------------- |
| Google    | Accounts Merge, Number of Islands II, Satisfiability of Equality Equations |
| Meta      | Friend Circles, Redundant Connection, Most Stones Removed                  |
| Amazon    | Number of Provinces, Regions Cut By Slashes                                |
| Microsoft | Evaluate Division, Smallest String With Swaps                              |
| Apple     | Graph Valid Tree, Longest Consecutive Sequence                             |

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

| Scenario                      | Use Union-Find | Use DFS/BFS   |
| ----------------------------- | -------------- | ------------- |
| Dynamic edge additions        | Yes            | --            |
| Multiple connectivity queries | Yes            | --            |
| Need actual path              | --             | Yes           |
| One-time component count      | --             | Yes (simpler) |
| Cycle detection (undirected)  | Yes            | Yes           |
| Cycle detection (directed)    | --             | Yes           |
| Shortest path                 | --             | Yes           |

---

## Common Variations

### 1. Union-Find with Size

Track size of each set instead of rank:

```python
class UnionFindWithSize:
    """Union-Find using union by size instead of rank."""

    def __init__(self, n: int):
        self.parent = list(range(n))
        self.size = [1] * n  # Size of each component

    def find(self, x: int) -> int:
        """Find root with path compression."""
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x: int, y: int) -> bool:
        """Union by size. Returns True if merged, False if already connected."""
        px, py = self.find(x), self.find(y)
        if px == py:
            return False

        # Attach smaller tree under the larger tree's root
        if self.size[px] < self.size[py]:
            self.parent[px] = py
            self.size[py] += self.size[px]
        else:
            self.parent[py] = px
            self.size[px] += self.size[py]
        return True

    def connected(self, x: int, y: int) -> bool:
        """Check if x and y belong to the same set."""
        return self.find(x) == self.find(y)

    def get_size(self, x: int) -> int:
        """Return the size of the component containing x."""
        return self.size[self.find(x)]
```

### 2. Union-Find with Component Count

```python
class UnionFindWithCount:
    """Union-Find that tracks the number of connected components."""

    def __init__(self, n: int):
        self.parent = list(range(n))
        self.rank = [0] * n
        self.count = n  # Number of connected components

    def find(self, x: int) -> int:
        """Find root with path compression."""
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x: int, y: int) -> bool:
        """Union by rank. Returns True if merged, False if already connected."""
        px, py = self.find(x), self.find(y)
        if px == py:
            return False

        # Union by rank
        if self.rank[px] < self.rank[py]:
            self.parent[px] = py
        elif self.rank[px] > self.rank[py]:
            self.parent[py] = px
        else:
            self.parent[py] = px
            self.rank[px] += 1

        self.count -= 1  # One fewer component after a successful merge
        return True

    def connected(self, x: int, y: int) -> bool:
        """Check if x and y belong to the same set."""
        return self.find(x) == self.find(y)

    def get_count(self) -> int:
        return self.count
```

### 3. Weighted Union-Find

For problems like Evaluate Division where edges carry values (e.g., a/b = 2.0).

Each node stores a weight representing the ratio `node / parent[node]`. During
`find(x)`, weights are multiplied along the path so that after compression,
`weight[x]` becomes the ratio `x / root(x)` (the node's value relative to
its root). During `union(x, y, value)` where `value = x / y`, we derive the
correct weight to link the two roots:

```
Derivation of weight[root_x] when linking root_x → root_y:

After find(x): weight[x] = x / root_x
After find(y): weight[y] = y / root_y

We want: weight[root_x] = root_x / root_y

From the weights we can express the roots:
  root_x = x / weight[x]
  root_y = y / weight[y]

So:
  root_x / root_y = (x / weight[x]) / (y / weight[y])
                   = (x / y) * (weight[y] / weight[x])
                   = value * weight[y] / weight[x]
```

```python
class WeightedUnionFind:
    """
    Weighted Union-Find for ratio / division relationship problems.

    Invariant: weight[x] = x / parent[x]
    - Initially parent[x] = x, so weight[x] = x / x = 1.0
    - After find(x) with path compression, parent[x] = root,
      so weight[x] = x / root (accumulated product along the path)
    """

    def __init__(self, n: int):
        self.parent = list(range(n))
        self.weight = [1.0] * n  # weight[x] = x / parent[x] = 1.0

    def find(self, x: int) -> int:
        """Find root with path compression, accumulating weights."""
        if self.parent[x] != x:
            root = self.find(self.parent[x])
            # Before: weight[x] = x / parent[x], weight[parent[x]] = parent[x] / root
            # After:  weight[x] = x / root = (x / parent[x]) * (parent[x] / root)
            self.weight[x] *= self.weight[self.parent[x]]
            self.parent[x] = root
        return self.parent[x]

    def union(self, x: int, y: int, value: float) -> bool:
        """
        Union x and y with the relationship x / y = value.
        Returns True if merged, False if already connected.
        """
        px, py = self.find(x), self.find(y)
        if px == py:
            return False

        # After find: weight[x] = x / px, weight[y] = y / py
        # Link px → py. Need weight[px] = px / py
        # px / py = (x / weight[x]) / (y / weight[y])
        #         = (x / y) * (weight[y] / weight[x])
        #         = value * weight[y] / weight[x]
        self.parent[px] = py
        self.weight[px] = value * self.weight[y] / self.weight[x]
        return True

    def query(self, x: int, y: int) -> float:
        """Return x / y if x and y are connected, else -1.0."""
        px, py = self.find(x), self.find(y)
        if px != py:
            return -1.0
        # After find: weight[x] = x / root, weight[y] = y / root
        # x / y = (x / root) / (y / root) = weight[x] / weight[y]
        return self.weight[x] / self.weight[y]
```

---

## Quick Reference: When to Use Which Variant

| Variant                         | Use When                              |
| ------------------------------- | ------------------------------------- |
| Basic + Path Compression + Rank | Default choice, most problems         |
| With Size                       | Need size of largest component        |
| With Count                      | Need number of components             |
| Weighted                        | Ratios/relationships between elements |

---

## Warm-Up Problem: Are Two Nodes Connected?

**Problem**: Given `n` nodes (labeled `0` to `n-1`) and a list of undirected edges,
determine if two specific nodes `a` and `b` are connected.

This is the simplest possible Union-Find application — use it to verify you can
write the data structure from scratch before tackling harder problems.

```python
def are_connected(n: int, edges: list[list[int]], a: int, b: int) -> bool:
    """Return True if nodes a and b are connected via the given edges."""
    parent = list(range(n))
    rank = [0] * n

    def find(x: int) -> int:
        if parent[x] != x:
            parent[x] = find(parent[x])  # Path compression
        return parent[x]

    def union(x: int, y: int) -> None:
        px, py = find(x), find(y)
        if px == py:
            return
        # Union by rank
        if rank[px] < rank[py]:
            parent[px] = py
        elif rank[px] > rank[py]:
            parent[py] = px
        else:
            parent[py] = px
            rank[px] += 1

    for u, v in edges:
        union(u, v)

    return find(a) == find(b)


# Example usage:
# 0 - 1 - 2    3 - 4
print(are_connected(5, [[0,1],[1,2],[3,4]], 0, 2))  # True
print(are_connected(5, [[0,1],[1,2],[3,4]], 0, 4))  # False
```

---

## Intermediate Problem: Number of Provinces (LeetCode 547)

**Problem**: Given an `n x n` adjacency matrix `isConnected` where `isConnected[i][j] = 1`
means cities `i` and `j` are directly connected, return the total number of provinces
(connected components).

This builds on the warm-up by asking you to **count** distinct groups rather than just
checking membership — a natural next step that introduces the component-counting pattern.

```python
def findCircleNum(isConnected: list[list[int]]) -> int:
    """
    Count connected components using Union-Find.

    Time:  O(n² × α(n)) ≈ O(n²) — we check every cell in the matrix
    Space: O(n)
    """
    n = len(isConnected)
    parent = list(range(n))
    rank = [0] * n
    components = n  # Start with n components, decrement on each merge

    def find(x: int) -> int:
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    def union(x: int, y: int) -> bool:
        px, py = find(x), find(y)
        if px == py:
            return False
        if rank[px] < rank[py]:
            parent[px] = py
        elif rank[px] > rank[py]:
            parent[py] = px
        else:
            parent[py] = px
            rank[px] += 1
        return True

    for i in range(n):
        for j in range(i + 1, n):  # Only upper triangle (symmetric matrix)
            if isConnected[i][j] == 1:
                if union(i, j):
                    components -= 1

    return components


# Example:
# City 0 -- City 1    City 2
# isConnected = [[1,1,0],[1,1,0],[0,0,1]]
print(findCircleNum([[1, 1, 0], [1, 1, 0], [0, 0, 1]]))  # 2

# All connected:
print(findCircleNum([[1, 1, 1], [1, 1, 1], [1, 1, 1]]))  # 1
```

---

## Practice Problem: Largest Component After Merges

**Problem**: You have `n` nodes labeled `0` to `n-1`. You are given a list of
edges to add one at a time. After **each** edge addition, return the size of the
largest connected component.

This problem builds on component counting by requiring you to **track component
sizes** — introducing the union-by-size variant and showing how Union-Find
naturally supports incremental queries.

```python
def largest_component_after_merges(
    n: int, edges: list[list[int]]
) -> list[int]:
    """
    After each edge is added, return the size of the largest component.

    Time:  O(E x alpha(n)) per edge ~ O(E) total
    Space: O(n)
    """
    parent = list(range(n))
    size = [1] * n
    max_size = 1

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]  # Path halving (iterative)
            x = parent[x]
        return x

    def union(x: int, y: int) -> None:
        nonlocal max_size
        px, py = find(x), find(y)
        if px == py:
            return
        # Union by size: attach smaller under larger
        if size[px] < size[py]:
            px, py = py, px
        parent[py] = px
        size[px] += size[py]
        max_size = max(max_size, size[px])

    result: list[int] = []
    for u, v in edges:
        union(u, v)
        result.append(max_size)
    return result


# Example: 5 nodes, edges added one at a time
# After [0,1]: {0,1}, {2}, {3}, {4}         -> largest = 2
# After [2,3]: {0,1}, {2,3}, {4}            -> largest = 2
# After [0,3]: {0,1,2,3}, {4}               -> largest = 4
# After [3,4]: {0,1,2,3,4}                  -> largest = 5
print(largest_component_after_merges(5, [[0,1],[2,3],[0,3],[3,4]]))
# Output: [2, 2, 4, 5]
```

Note: This uses **path halving** (`parent[x] = parent[parent[x]]`) instead of
full recursive path compression — an iterative alternative that avoids Python's
recursion limit and achieves the same amortized complexity.

---

## Practice Problem: Graph Valid Tree (LeetCode 261)

**Problem**: Given `n` nodes labeled `0` to `n-1` and a list of undirected edges,
determine if these edges form a valid tree.

A valid tree has exactly two properties: it is **connected** (one component) and
has **no cycles**. Union-Find checks both at once — a cycle exists exactly when
`union` tries to merge two nodes that already share a root.

```python
def validTree(n: int, edges: list[list[int]]) -> bool:
    """
    A graph is a valid tree iff it has exactly n-1 edges and no cycles.

    Time:  O(n × α(n)) ≈ O(n)
    Space: O(n)
    """
    # A tree with n nodes must have exactly n-1 edges
    if len(edges) != n - 1:
        return False

    parent = list(range(n))
    rank = [0] * n

    def find(x: int) -> int:
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    def union(x: int, y: int) -> bool:
        px, py = find(x), find(y)
        if px == py:
            return False  # Cycle detected!
        if rank[px] < rank[py]:
            parent[px] = py
        elif rank[px] > rank[py]:
            parent[py] = px
        else:
            parent[py] = px
            rank[px] += 1
        return True

    # If any union fails, there's a cycle → not a tree
    return all(union(u, v) for u, v in edges)


# Valid tree: 0-1-2-3-4 (4 edges, 5 nodes, no cycle)
print(validTree(5, [[0, 1], [0, 2], [0, 3], [1, 4]]))  # True

# Has cycle: 0-1-2-0 plus 3-4
print(validTree(5, [[0, 1], [1, 2], [2, 0], [3, 4]]))  # False

# Disconnected: only 2 edges for 5 nodes
print(validTree(5, [[0, 1], [2, 3]]))  # False (len != n-1)
```

---

## Practice Problem: Satisfiability of Equality Equations (LeetCode 990)

**Problem**: Given an array of strings `equations` where each string is of the
form `"a==b"` or `"a!=b"` (with single lowercase letter variables), return `True`
if it is possible to assign integers to variables so that all equations are
satisfied simultaneously.

This bridges to harder Union-Find problems by requiring a **two-pass strategy**:
first process all equalities (union), then check all inequalities for
contradictions. It also introduces **character-to-index mapping** — a common
pattern when Union-Find elements aren't simple integers.

```python
def equations_possible(equations: list[str]) -> bool:
    """
    Process '==' first (union), then check '!=' for contradictions.

    Time:  O(E x alpha(26)) = O(E) where E = len(equations)
    Space: O(1) — at most 26 lowercase letters
    """
    parent = list(range(26))  # 26 lowercase letters

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]  # Path halving
            x = parent[x]
        return x

    def union(x: int, y: int) -> None:
        px, py = find(x), find(y)
        if px != py:
            parent[px] = py

    # Pass 1: process all equalities — union the variables
    for eq in equations:
        if eq[1] == "=":
            x = ord(eq[0]) - ord("a")
            y = ord(eq[3]) - ord("a")
            union(x, y)

    # Pass 2: check all inequalities — find contradictions
    for eq in equations:
        if eq[1] == "!":
            x = ord(eq[0]) - ord("a")
            y = ord(eq[3]) - ord("a")
            if find(x) == find(y):
                return False  # Contradiction: can't be equal AND not equal

    return True


# "a==b", "b!=a" -> False (a==b contradicts b!=a)
print(equations_possible(["a==b", "b!=a"]))  # False

# "a==b", "b==c", "a==c" -> True (consistent)
print(equations_possible(["a==b", "b==c", "a==c"]))  # True

# "a==b", "b!=c", "c==a" -> False (a==b, c==a implies b==c, contradicts b!=c)
print(equations_possible(["a==b", "b!=c", "c==a"]))  # False
```

---

## Start: [01-union-find-basics.md](./01-union-find-basics.md)

Begin with the fundamental Union-Find implementation that forms the basis for all Union-Find problems.

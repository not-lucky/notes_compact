# Connected Components with Union-Find

> **Prerequisites:** [Union-Find Basics](./01-union-find-basics.md), [Path Compression](./02-path-compression.md), [Union by Rank](./03-union-by-rank.md)

## Interview Context

Counting and managing connected components is the most common application of Union-Find. While DFS/BFS can also count components, Union-Find excels when edges are added dynamically or when multiple connectivity queries are needed.

---

## Building Intuition

**The "Island Formation" Mental Model**

Imagine islands appearing in an ocean one by one:

- Each new island starts as its own landmass (count++)
- When a new island appears next to existing land, they merge (count--)

```
Initial: ocean (0 islands)

Add land at (0,0): 1 island
  X . .
  . . .

Add land at (0,1): Still 1 island (merged with (0,0))
  X X .
  . . .

Add land at (2,2): 2 islands (isolated)
  X X .
  . . .
  . . X
```

**The Key Insight: Start High, Decrement on Merge**

Union-Find makes component counting trivial:

1. Start with `count = n` (each element is its own component)
2. Each successful union decrements `count` by 1
3. Failed unions (already connected) don't change count

```python
# The beauty: O(1) count tracking!
def union(x, y):
    if find(x) == find(y):
        return False  # Already connected, count unchanged
    # ... merge trees ...
    self.count -= 1  # One less component!
    return True
```

**Why Union-Find Beats DFS for Dynamic Graphs**

```
Scenario: n nodes, add 1000 edges, query count after each

DFS approach:
- After each edge: rebuild graph + run full DFS to count components
- Total: O(1000 × (n + E))  — E grows with each edge

Union-Find approach:
- After each edge: one union operation O(α(n)) + O(1) count read
- Total: O(1000 × α(n)) ≈ O(1000)

Orders of magnitude faster for dynamic graphs!
```

**Visual: Tracking Component Count**

```
Initial: {0}, {1}, {2}, {3}, {4}  count = 5

union(0,1): {0,1}, {2}, {3}, {4}  count = 4

union(2,3): {0,1}, {2,3}, {4}     count = 3

union(0,2): {0,1,2,3}, {4}        count = 2

union(0,1): Same component!        count = 2 (no change)
```

---

## When NOT to Use Union-Find for Components

**1. When You Need Component Members**

Union-Find tracks count efficiently, but listing all members of each component requires extra work:

```python
# To get all elements in a component:
# Must iterate through all n elements and group by find(i)
# That's O(n × α(n)) every time you need the list

# If you frequently need member lists, consider:
# - Adjacency list + DFS (natural grouping)
# - Union-Find + size tracking + member sets
```

**2. For One-Time Static Analysis**

If you only need to count components once on a static graph, DFS is simpler:

```python
# DFS: Simple, intuitive, O(V+E)
def count_components_dfs(n: int, edges: list[list[int]]) -> int:
    # Build adjacency list from edge list
    graph: dict[int, list[int]] = {i: [] for i in range(n)}
    for a, b in edges:
        graph[a].append(b)
        graph[b].append(a)

    # NOTE: We initialize graph with all n nodes (not just those in edges)
    # so isolated nodes with no edges are still counted as components.

    visited: set[int] = set()
    count = 0
    for node in graph:
        if node not in visited:
            # Stack-based DFS to explore the entire component
            stack = [node]
            while stack:
                curr = stack.pop()
                if curr in visited:
                    continue
                visited.add(curr)
                for neighbor in graph[curr]:
                    if neighbor not in visited:
                        stack.append(neighbor)
            count += 1
    return count

# Union-Find: Same complexity, more setup
# Only wins when queries are repeated or graph is dynamic
```

**3. When Graph Has Weighted Shortest Paths**

If you eventually need shortest paths or distances (not just connectivity), use BFS or Dijkstra from the start. Union-Find can't provide path information.

**4. For Directed Graphs (Strongly Connected Components)**

Union-Find doesn't handle direction. For strongly connected components in directed graphs, use:

- Kosaraju's algorithm
- Tarjan's algorithm

---

## Pattern: Component Counting

Track the number of components by starting with n components and decrementing on each successful union.

### Implementation

```python
class UnionFind:
    """
    Union-Find with component counting.

    Time: O(α(n)) per operation
    Space: O(n)
    """

    def __init__(self, n: int):
        self.parent = list(range(n))
        self.rank = [0] * n
        self.count = n  # Number of connected components

    def find(self, x: int) -> int:
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x: int, y: int) -> bool:
        px, py = self.find(x), self.find(y)

        if px == py:
            return False  # Already connected

        if self.rank[px] < self.rank[py]:
            px, py = py, px
        self.parent[py] = px
        if self.rank[px] == self.rank[py]:
            self.rank[px] += 1

        self.count -= 1  # One less component
        return True

    def get_count(self) -> int:
        return self.count

    def connected(self, x: int, y: int) -> bool:
        return self.find(x) == self.find(y)
```

---

## Problem: Count Connected Components (Warm-Up)

**LeetCode 323**: Given `n` nodes labeled `0` to `n-1` and a list of undirected edges, find the number of connected components.

### Why Start Here?

This is the simplest component-counting problem — no grid, no dynamics, just nodes and edges. It maps directly to the Union-Find component counting pattern.

### Solution

```python
def countComponents(n: int, edges: list[list[int]]) -> int:
    """
    Count connected components in an undirected graph.

    Time: O(n + e × α(n)) where e = len(edges)
    Space: O(n)
    """
    parent = list(range(n))
    rank = [0] * n
    components = n

    def find(x: int) -> int:
        if parent[x] != x:
            parent[x] = find(parent[x])  # Path compression
        return parent[x]

    def union(x: int, y: int) -> bool:
        nonlocal components
        px, py = find(x), find(y)
        if px == py:
            return False  # Already in the same component

        # Union by rank
        if rank[px] < rank[py]:
            px, py = py, px
        parent[py] = px
        if rank[px] == rank[py]:
            rank[px] += 1

        components -= 1  # Merged two components into one
        return True

    for a, b in edges:
        union(a, b)

    return components


# Example
n = 5
edges = [[0, 1], [1, 2], [3, 4]]
# Components: {0,1,2}, {3,4} → 2
print(countComponents(n, edges))  # 2
```

---

## Problem: Graph Valid Tree (Stepping Stone)

**LeetCode 261**: Given `n` nodes labeled `0` to `n-1` and a list of undirected edges, determine if these edges form a valid tree. A valid tree has exactly one connected component and no cycles.

### Why This Problem?

This bridges basic component counting (LC 323) and dynamic problems. A tree with `n` nodes has exactly `n-1` edges and is fully connected. If `len(edges) != n-1`, it's immediately not a tree. Otherwise, process all edges with Union-Find: if any union returns `False`, there's a cycle (not a tree). This introduces **cycle detection via Union-Find** — a pattern used in redundant connection problems.

### Solution

```python
def validTree(n: int, edges: list[list[int]]) -> bool:
    """
    Check if n nodes and given edges form a valid tree.

    A valid tree has exactly n-1 edges and no cycles (single component).

    Time: O(n + e × α(n)) where e = len(edges)
    Space: O(n)
    """
    # A tree with n nodes must have exactly n-1 edges
    if len(edges) != n - 1:
        return False

    parent = list(range(n))
    rank = [0] * n

    def find(x: int) -> int:
        if parent[x] != x:
            parent[x] = find(parent[x])  # Path compression
        return parent[x]

    def union(x: int, y: int) -> bool:
        px, py = find(x), find(y)
        if px == py:
            return False  # Cycle detected

        # Union by rank
        if rank[px] < rank[py]:
            px, py = py, px
        parent[py] = px
        if rank[px] == rank[py]:
            rank[px] += 1

        return True

    for a, b in edges:
        if not union(a, b):
            return False  # Cycle found — not a tree

    # With n-1 edges and no cycles, must be a single connected tree
    return True


# Example 1: Valid tree
n = 5
edges = [[0, 1], [0, 2], [0, 3], [1, 4]]
# 5 nodes, 4 edges (n-1), no cycles → valid tree
print(validTree(n, edges))  # True

# Example 2: Has a cycle
n = 5
edges = [[0, 1], [1, 2], [2, 3], [1, 3], [1, 4]]
# 5 nodes, 5 edges (not n-1) → immediately False
print(validTree(n, edges))  # False

# Example 3: Disconnected (forest)
n = 4
edges = [[0, 1], [2, 3]]
# 4 nodes, 2 edges (not n-1) → immediately False
print(validTree(n, edges))  # False
```

---

## Problem: Earliest Time Everyone Becomes Friends

**LeetCode 1101**: Given `n` people and a list of `logs` where `logs[i] = [timestamp, x, y]` means person `x` and person `y` become friends at `timestamp`. Friendship is transitive. Return the earliest time at which all `n` people are connected (single component), or `-1` if impossible.

### Why This Problem?

This is the cleanest example of the "start high, decrement on merge" pattern with a twist: you stop as soon as `count == 1`. It also introduces sorting edges by a criterion (timestamp) before processing — a technique that reappears in harder problems.

### Solution

```python
def earliestAcq(logs: list[list[int]], n: int) -> int:
    """
    Find the earliest timestamp when all n people are connected.

    Time: O(L log L + L × α(n)) where L = len(logs)
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
        nonlocal components
        px, py = find(x), find(y)
        if px == py:
            return False

        if rank[px] < rank[py]:
            px, py = py, px
        parent[py] = px
        if rank[px] == rank[py]:
            rank[px] += 1

        components -= 1
        return True

    # Process friendships in chronological order
    logs.sort(key=lambda log: log[0])

    for timestamp, x, y in logs:
        union(x, y)
        if components == 1:
            return timestamp  # Everyone is connected!

    return -1  # Not all people became connected


# Example
logs = [[0,2,0], [1,0,1], [3,0,3], [4,1,2], [7,3,1]]
n = 4

# Sorted by timestamp (already sorted here):
#   t=0: union(2,0) → {0,2}, {1}, {3}       components=3
#   t=1: union(0,1) → {0,1,2}, {3}           components=2
#   t=3: union(0,3) → {0,1,2,3}              components=1 → return 3
#
# We never even process t=4 or t=7.

print(earliestAcq(logs, n))  # 3
```

---

## Problem: Number of Islands (Grid Components)

**LeetCode 200**: Given a 2D grid of `'1'`s (land) and `'0'`s (water), count the number of islands. An island is surrounded by water and formed by connecting adjacent lands horizontally or vertically.

### Why This Problem?

This bridges the gap between graph-based component counting (LC 323) and the dynamic version (LC 305). Here you learn to map a 2D grid to Union-Find by converting `(row, col)` into a flat index. DFS is simpler for this static problem, but solving it with Union-Find prepares you for the dynamic variant.

### Solution

```python
def numIslands(grid: list[list[str]]) -> int:
    """
    Count connected components of '1's in a grid.

    Time: O(m × n × α(m × n))
    Space: O(m × n)
    """
    if not grid or not grid[0]:
        return 0

    rows, cols = len(grid), len(grid[0])
    parent = list(range(rows * cols))
    rank = [0] * (rows * cols)
    components = 0

    def find(x: int) -> int:
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    def union(x: int, y: int) -> bool:
        nonlocal components
        px, py = find(x), find(y)
        if px == py:
            return False

        if rank[px] < rank[py]:
            px, py = py, px
        parent[py] = px
        if rank[px] == rank[py]:
            rank[px] += 1

        components -= 1
        return True

    # Count land cells and initialize components
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1':
                components += 1

    # Connect adjacent land cells
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1':
                idx = r * cols + c
                # Only check right and down to avoid duplicate unions
                if c + 1 < cols and grid[r][c + 1] == '1':
                    union(idx, idx + 1)
                if r + 1 < rows and grid[r + 1][c] == '1':
                    union(idx, idx + cols)

    return components


# Example
grid = [
    ['1', '1', '0', '0', '0'],
    ['1', '1', '0', '0', '0'],
    ['0', '0', '1', '0', '0'],
    ['0', '0', '0', '1', '1'],
]
# Three islands: top-left 2×2, center, bottom-right 1×2
print(numIslands(grid))  # 3
```

---

## Problem: Number of Islands II

**LeetCode 305**: You're given a 2D grid initialized with water. We add land one by one at positions given in `positions`. After each addition, return the number of islands.

### Why Union-Find?

This is a **dynamic connectivity** problem. With DFS, each query requires O(m×n) to count components. With Union-Find, each addition is O(α(m×n)).

```
m×n grid, k additions:
- DFS approach: O(k × m × n)
- Union-Find: O(k × α(m × n)) ≈ O(k)
```

### Solution

```python
def numIslands2(m: int, n: int, positions: list[list[int]]) -> list[int]:
    """
    Dynamically add land and count islands.

    Time: O(k × α(m×n)) where k = len(positions)
    Space: O(k) for the hash maps (at most k land cells)
    """
    parent = {}
    rank = {}
    count = 0
    result = []

    def find(x: tuple[int, int]) -> tuple[int, int]:
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    def union(x: tuple[int, int], y: tuple[int, int]) -> bool:
        nonlocal count
        px, py = find(x), find(y)
        if px == py:
            return False

        if rank[px] < rank[py]:
            px, py = py, px
        parent[py] = px
        if rank[px] == rank[py]:
            rank[px] += 1

        count -= 1
        return True

    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    for r, c in positions:
        pos = (r, c)

        # Skip if already land (duplicate position)
        if pos in parent:
            result.append(count)
            continue

        # Add new land
        parent[pos] = pos
        rank[pos] = 0
        count += 1  # New island

        # Try to connect with existing land neighbors
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            neighbor = (nr, nc)
            if neighbor in parent:  # Neighbor is land
                union(pos, neighbor)  # May decrease count

        result.append(count)

    return result


# Example
m, n = 3, 3
positions = [[0,0], [0,1], [1,2], [2,1]]

# Step by step:
# Add (0,0): 1 island
#   X . .
#   . . .
#   . . .
#
# Add (0,1): 1 island (connects to (0,0))
#   X X .
#   . . .
#   . . .
#
# Add (1,2): 2 islands (isolated)
#   X X .
#   . . X
#   . . .
#
# Add (2,1): 3 islands (isolated)
#   X X .
#   . . X
#   . X .

print(numIslands2(m, n, positions))  # [1, 1, 2, 3]
```

---

## Problem: Number of Operations to Make Network Connected

**LeetCode 1319**: There are n computers and connections between them. You can remove a cable and use it to connect two disconnected computers. Find the minimum number of operations to connect all computers.

### Key Insight

- If we have n computers and k components, we need k-1 cables to connect them
- We have spare cables if there are redundant connections (cycles)
- Redundant = edges that don't decrease component count

```
n computers, e edges, k components after processing all edges:
- A spanning forest of k components uses exactly (n - k) edges
- Redundant (spare) cables: e - (n - k)
- Need (k - 1) cables to connect k components into one
- If spare >= k-1: answer is k-1
- If e < n-1: impossible (not enough cables total)
```

### Solution

```python
def makeConnected(n: int, connections: list[list[int]]) -> int:
    """
    Find minimum operations to connect all computers.

    Time: O(n + e × α(n))
    Space: O(n)
    """
    # Need at least n-1 cables to connect n computers
    if len(connections) < n - 1:
        return -1

    parent = list(range(n))
    rank = [0] * n
    components = n

    def find(x: int) -> int:
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    def union(x: int, y: int) -> bool:
        nonlocal components
        px, py = find(x), find(y)
        if px == py:
            return False  # Redundant connection

        if rank[px] < rank[py]:
            px, py = py, px
        parent[py] = px
        if rank[px] == rank[py]:
            rank[px] += 1

        components -= 1
        return True

    for a, b in connections:
        union(a, b)

    # Need (components - 1) operations to connect all
    # We have enough cables since len(connections) >= n-1
    return components - 1


# Example
n = 6
connections = [[0,1], [0,2], [0,3], [1,2], [1,3]]
# Computers: 0-1-2-3 are connected, 4 and 5 are isolated
# Components: 3 ({0,1,2,3}, {4}, {5})
# Need components - 1 = 2 operations
# Have 5 edges for 4 connected nodes → 2 are redundant (cycles within {0,1,2,3}).
# 2 redundant cables >= 2 needed → possible.
print(makeConnected(n, connections))  # 2
```

---

## Problem: Smallest String With Swaps

**LeetCode 1202**: You can swap characters at given pairs of indices any number of times. Return the lexicographically smallest string possible.

### Key Insight

- If index i can swap with j, and j can swap with k, then i, j, k are all in the same group
- Within a group, characters can be rearranged in any order
- Sort characters within each group and assign smallest to smallest index

### Solution

```python
def smallestStringWithSwaps(s: str, pairs: list[list[int]]) -> str:
    """
    Group indices, sort characters within groups.

    Time: O(n log n + p × α(n)) where p = len(pairs)
    Space: O(n)
    """
    from collections import defaultdict

    n = len(s)
    parent = list(range(n))
    rank = [0] * n

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

    # Union all pairs
    for a, b in pairs:
        union(a, b)

    # Group indices by their root
    groups = defaultdict(list)
    for i in range(n):
        groups[find(i)].append(i)

    # Build result
    result = list(s)
    for indices in groups.values():
        # Get characters at these indices, sort them
        chars = sorted(s[i] for i in indices)
        # indices are already in order since we iterated range(n),
        # but sort defensively in case grouping logic changes
        indices.sort()

        # Assign sorted characters to sorted indices
        for i, char in zip(indices, chars):
            result[i] = char

    return ''.join(result)


# Example
s = "dcab"
pairs = [[0,3], [1,2]]

# Groups: {0,3} and {1,2}
# Group {0,3}: chars 'd','b' → sorted 'b','d' → indices 0,3 get 'b','d'
# Group {1,2}: chars 'c','a' → sorted 'a','c' → indices 1,2 get 'a','c'
# Result: "bacd"

print(smallestStringWithSwaps(s, pairs))  # "bacd"
```

---

## Problem: Satisfiability of Equality Equations

**LeetCode 990**: Given an array of strings `equations` where each equation is a 4-character string like `"a==b"` or `"a!=b"`, determine if it's possible to assign integers to variables such that all equations are satisfied simultaneously.

### Key Insight

- Process all `==` equations first: union the two variables together
- Then check all `!=` equations: if two variables that must be unequal are in the same component, return `False`
- This is a two-pass approach: build components, then validate constraints

### Solution

```python
def equationsPossible(equations: list[str]) -> bool:
    """
    Check if equality/inequality constraints are satisfiable.

    Time: O(e × α(26)) = O(e) where e = len(equations)
    Space: O(1) — at most 26 lowercase letters
    """
    parent = list(range(26))
    rank = [0] * 26

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

    # Pass 1: Process all equalities — union connected variables
    for eq in equations:
        if eq[1] == '=':
            x = ord(eq[0]) - ord('a')
            y = ord(eq[3]) - ord('a')
            union(x, y)

    # Pass 2: Check all inequalities — must be in different components
    for eq in equations:
        if eq[1] == '!':
            x = ord(eq[0]) - ord('a')
            y = ord(eq[3]) - ord('a')
            if find(x) == find(y):
                return False  # Contradiction: equal but must be unequal

    return True


# Example 1
equations = ["a==b", "b!=a"]
# Union a and b, then check a != b → a and b are in the same component → False
print(equationsPossible(equations))  # False

# Example 2
equations = ["a==b", "b==c", "a==c"]
# All in one component, no inequality constraints → True
print(equationsPossible(equations))  # True

# Example 3
equations = ["a==b", "b!=c", "c==a"]
# Union a-b, union c-a → {a,b,c} all connected
# Check b != c → both in same component → False
print(equationsPossible(equations))  # False
```

---

## Pattern: Get All Groups

Sometimes you need to enumerate all elements in each group.

```python
def get_all_groups(uf: UnionFind, n: int) -> dict[int, list[int]]:
    """
    Return mapping from root to list of elements.

    Time: O(n × α(n))
    Space: O(n)
    """
    from collections import defaultdict

    groups = defaultdict(list)
    for i in range(n):
        root = uf.find(i)
        groups[root].append(i)

    return dict(groups)


# Example
uf = UnionFind(6)
uf.union(0, 1)
uf.union(1, 2)
uf.union(3, 4)

groups = get_all_groups(uf, 6)
# Possible output: {0: [0, 1, 2], 3: [3, 4], 5: [5]}
```

---

## Pattern: Largest Component

Track the size of the largest component.

```python
class UnionFindWithSize:
    """
    Union-Find using union-by-size (not rank) to track component sizes.

    This variant merges smaller trees into larger ones and maintains
    the size of each component at its root.

    Time: O(α(n)) per operation
    Space: O(n)
    """

    def __init__(self, n: int):
        self.parent = list(range(n))
        self.size = [1] * n
        self.count = n  # Number of components
        self.max_size = 1 if n > 0 else 0

    def find(self, x: int) -> int:
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x: int, y: int) -> bool:
        px, py = self.find(x), self.find(y)
        if px == py:
            return False

        # Union by size: attach smaller tree under larger tree
        if self.size[px] < self.size[py]:
            px, py = py, px

        self.parent[py] = px
        self.size[px] += self.size[py]
        self.max_size = max(self.max_size, self.size[px])
        self.count -= 1
        return True

    def get_max_size(self) -> int:
        return self.max_size

    def get_size(self, x: int) -> int:
        """Return the size of the component containing x."""
        return self.size[self.find(x)]
```

---

## Complexity Comparison

| Approach        | Build       | Count    | Dynamic Add      |
| --------------- | ----------- | -------- | ---------------- |
| DFS on adj list | O(V + E)    | O(V + E) | O(V + E) per add |
| BFS on adj list | O(V + E)    | O(V + E) | O(V + E) per add |
| Union-Find      | O(E × α(V)) | O(1)     | O(α(V)) per add  |

Union-Find wins when:

- Multiple queries for component count
- Dynamic edge additions
- Need to track component sizes

---

## Edge Cases

1. **Empty graph**: n nodes, 0 edges → n components
2. **Complete graph**: n nodes, n(n-1)/2 edges → 1 component
3. **Self-loops**: union(x, x) → returns False, no effect
4. **Duplicate edges**: Second union returns False
5. **Invalid indices**: Validate bounds if needed

---

## Interview Tips

1. **Choose wisely**: Mention when Union-Find beats DFS/BFS
2. **Component count trick**: Start with n, decrement on union
3. **Size vs count**: Size tracks elements per component; count tracks number of components
4. **Dynamic problems**: Strong signal for Union-Find

---

## Practice Problems

| #   | Problem                                                  | Difficulty | Key Concept              |
| --- | -------------------------------------------------------- | ---------- | ------------------------ |
| 1   | Count Connected Components (LC 323)                      | Medium     | Basic component count    |
| 2   | Graph Valid Tree (LC 261)                                | Medium     | Components + cycle check |
| 3   | Earliest Moment Everyone Becomes Friends (LC 1101)       | Medium     | Sort + early exit        |
| 4   | Number of Islands (LC 200)                               | Medium     | Grid to Union-Find       |
| 5   | Number of Islands II (LC 305)                            | Hard       | Dynamic land addition    |
| 6   | Number of Operations to Make Network Connected (LC 1319) | Medium     | Spare cable counting     |
| 7   | Smallest String With Swaps (LC 1202)                     | Medium     | Group and sort           |
| 8   | Satisfiability of Equality Equations (LC 990)            | Medium     | Two-pass constraint check|
| 9   | Lexicographically Smallest Equivalent String (LC 1061)   | Medium     | Character groups         |
| 10  | Checking Existence of Edge Length Limited Paths (LC 1697) | Hard      | Sort queries and edges   |

---

## Related Sections

- [Accounts Merge](./05-accounts-merge.md) - Complex grouping
- [Redundant Connection](./06-redundant-connection.md) - Cycle detection
- [Graph DFS/BFS](../08-graphs/README.md) - Alternative approaches

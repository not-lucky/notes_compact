# Connected Components with Union-Find

> **Prerequisites:** [Union-Find Basics](./01-union-find-basics.md), [Path Compression](./02-path-compression.md), [Union by Rank](./03-union-by-rank.md)

## Interview Context

Counting and managing connected components is the most common application of Union-Find. While DFS/BFS can also count components, Union-Find excels when edges are added dynamically or when multiple connectivity queries are needed.

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
    Space: O(m × n)
    """
    parent = {}
    rank = {}
    count = 0
    result = []

    def find(x: tuple) -> tuple:
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    def union(x: tuple, y: tuple) -> bool:
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
n computers, e edges:
- Minimum edges needed: n-1 (tree)
- Spare cables: e - (n - k) where k = components
- Can connect k components with k-1 spare cables
- If spare < k-1: impossible
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
# Need 2 operations
# Have 5 edges, need 5 for tree of 6 → 0 spare, but we have redundant edges
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
        # Get characters at these indices
        chars = [s[i] for i in indices]
        chars.sort()
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
class UnionFind:
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.size = [1] * n
        self.max_size = 1

    def find(self, x: int) -> int:
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x: int, y: int) -> bool:
        px, py = self.find(x), self.find(y)
        if px == py:
            return False

        if self.size[px] < self.size[py]:
            px, py = py, px

        self.parent[py] = px
        self.size[px] += self.size[py]
        self.max_size = max(self.max_size, self.size[px])
        return True

    def get_max_size(self) -> int:
        return self.max_size
```

---

## Complexity Comparison

| Approach | Build | Count | Dynamic Add |
|----------|-------|-------|-------------|
| DFS on adj list | O(V + E) | O(V + E) | O(V + E) per add |
| BFS on adj list | O(V + E) | O(V + E) | O(V + E) per add |
| Union-Find | O(E × α(V)) | O(1) | O(α(V)) per add |

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

| # | Problem | Difficulty | Key Concept |
|---|---------|------------|-------------|
| 1 | Number of Islands II | Hard | Dynamic land addition |
| 2 | Number of Operations to Make Network Connected | Medium | Spare cable counting |
| 3 | Smallest String With Swaps | Medium | Group and sort |
| 4 | Lexicographically Smallest Equivalent String | Medium | Character groups |
| 5 | Checking Existence of Edge Length Limited Paths | Hard | Sort queries and edges |

---

## Related Sections

- [Accounts Merge](./05-accounts-merge.md) - Complex grouping
- [Redundant Connection](./06-redundant-connection.md) - Cycle detection
- [Graph DFS/BFS](../08-graphs/README.md) - Alternative approaches

# Connected Components Solutions

## 1. Number of Islands II
**Problem Statement**:
You are given an `m x n` grid where all cells are initially water. You are also given a list of `positions` where `positions[i] = [ri, ci]` represents adding land at that coordinate. Return an array of integers representing the number of islands after each addition.

**Examples & Edge Cases**:
- **Example 1**: `m = 3, n = 3, positions = [[0,0], [0,1], [1,2], [2,1]]` → `[1, 1, 2, 3]`.
- **Edge Case**: Adding land to the same position twice → Count should not change.
- **Edge Case**: `m = 1, n = 1, positions = [[0,0]]` → `[1]`.

**Optimal Python Solution**:
```python
def numIslands2(m: int, n: int, positions: list[list[int]]) -> list[int]:
    parent = {}
    rank = {}
    count = 0
    res = []
    grid = set() # To keep track of land cells

    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    def union(x, y):
        nonlocal count
        root_x, root_y = find(x), find(y)
        if root_x != root_y:
            if rank[root_x] < rank[root_y]:
                parent[root_x] = root_y
            elif rank[root_x] > rank[root_y]:
                parent[root_y] = root_x
            else:
                parent[root_x] = root_y
                rank[root_y] += 1
            count -= 1
            return True
        return False

    for r, c in positions:
        if (r, c) in grid:
            res.append(count)
            continue

        grid.add((r, c))
        pos = r * n + c
        parent[pos] = pos
        rank[pos] = 0
        count += 1

        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < m and 0 <= nc < n and (nr, nc) in grid:
                union(pos, nr * n + nc)

        res.append(count)

    return res
```

**Explanation**:
1. This is a dynamic connectivity problem. We add land cells one by one and need to update the island count.
2. Initially, each land cell is its own island (`count += 1`).
3. We then check its 4 neighbors. If a neighbor is already land, we `union` the current cell with the neighbor and decrement the `count` if they were in different components.
4. We use a dictionary for `parent` to handle the sparse nature of land cells efficiently.

**Complexity Analysis**:
- **Time Complexity**: $O(K \alpha(m \times n))$, where $K$ is the number of positions.
- **Space Complexity**: $O(K)$ to store the land cells and Union-Find structure.

---

## 2. Number of Operations to Make Network Connected
**Problem Statement**:
Given `n` computers and `connections`, find the minimum number of cables to move to connect all computers. Return -1 if impossible.

**Optimal Python Solution**:
```python
def makeConnected(n: int, connections: list[list[int]]) -> int:
    if len(connections) < n - 1:
        return -1

    parent = list(range(n))
    components = n

    rank = [0] * n

    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    def union(x, y):
        nonlocal components
        rx, ry = find(x), find(y)
        if rx != ry:
            if rank[rx] < rank[ry]:
                parent[rx] = ry
            elif rank[rx] > rank[ry]:
                parent[ry] = rx
            else:
                parent[rx] = ry
                rank[ry] += 1
            components -= 1

    for u, v in connections:
        union(u, v)

    return components - 1
```

**Explanation**:
1. We need $n-1$ edges total to connect $n$ nodes. If we have fewer, it's impossible.
2. We use Union-Find to find the current number of connected components.
3. To connect $k$ components, we need $k-1$ additional edges. Since we have enough edges in total, we can always find $k-1$ redundant edges to use.

**Complexity Analysis**:
- **Time Complexity**: $O(E \alpha(n))$.
- **Space Complexity**: $O(n)$.

---

## 3. Smallest String With Swaps
**Problem Statement**:
Given a string `s` and index pairs `(a, b)` that can be swapped, find the lexicographically smallest string.

**Optimal Python Solution**:
```python
from collections import defaultdict

def smallestStringWithSwaps(s: str, pairs: list[list[int]]) -> str:
    n = len(s)
    parent = list(range(n))
    rank = [0] * n

    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    def union(x, y):
        rx, ry = find(x), find(y)
        if rx != ry:
            if rank[rx] < rank[ry]:
                parent[rx] = ry
            elif rank[rx] > rank[ry]:
                parent[ry] = rx
            else:
                parent[rx] = ry
                rank[ry] += 1

    for u, v in pairs:
        union(u, v)

    groups = defaultdict(list)
    for i in range(n):
        groups[find(i)].append(i)

    res = [""] * n
    for indices in groups.values():
        chars = sorted([s[i] for i in indices])
        for idx, char in zip(sorted(indices), chars):
            res[idx] = char

    return "".join(res)
```

**Explanation**:
1. Swappable indices form connected components.
2. Within each component, characters can be moved to any position.
3. We sort characters within each component and place them back in sorted index positions.

**Complexity Analysis**:
- **Time Complexity**: $O((P+n) \alpha(n) + n \log n)$.
- **Space Complexity**: $O(n)$.

---

## 4. Lexicographically Smallest Equivalent String
**Problem Statement**:
You are given two strings `s1` and `s2` of the same length and a string `baseStr`. We say `s1[i]` and `s2[i]` are equivalent characters. Use these equivalences to find the lexicographically smallest version of `baseStr`.

**Examples & Edge Cases**:
- **Example 1**: `s1 = "parker", s2 = "morris", baseStr = "parser"` → `"makkek"`.
- **Edge Case**: Circular equivalences `a=b, b=c, c=a`.

**Optimal Python Solution**:
```python
def smallestEquivalentString(s1: str, s2: str, baseStr: str) -> str:
    parent = list(range(26))

    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    def union(x, y):
        rx, ry = find(x), find(y)
        if rx != ry:
            # Always point to the smaller character to keep it as root
            if rx < ry:
                parent[ry] = rx
            else:
                parent[rx] = ry

    for c1, c2 in zip(s1, s2):
        union(ord(c1) - ord('a'), ord(c2) - ord('a'))

    res = []
    for char in baseStr:
        root = find(ord(char) - ord('a'))
        res.append(chr(root + ord('a')))

    return "".join(res)
```

**Explanation**:
1. Equivalences define components of characters.
2. Within each component, all characters can be replaced by the smallest character in that component.
3. We use Union-Find and always make the smaller character the parent during `union`.
4. Finally, we replace each character in `baseStr` with its component's root.

**Complexity Analysis**:
- **Time Complexity**: $O((n+m) \alpha(26))$, where $n$ is length of $s1/s2$ and $m$ is length of `baseStr`.
- **Space Complexity**: $O(26) = O(1)$.

---

## 5. Checking Existence of Edge Length Limited Paths
**Problem Statement**:
An undirected graph with `n` nodes and `edgeList` where `edgeList[i] = [u, v, dis]`. You are given `queries` where `queries[j] = [p, q, limit]`. For each query, check if there is a path between `p` and `q` such that every edge on the path has distance strictly less than `limit`.

**Optimal Python Solution**:
```python
def distanceLimitedPathsExist(n: int, edgeList: list[list[int]], queries: list[list[int]]) -> list[bool]:
    # Sort edges and queries by weight/limit to use Union-Find incrementally
    edgeList.sort(key=lambda x: x[2])
    # Keep track of original query index for results
    sorted_queries = sorted(enumerate(queries), key=lambda x: x[1][2])

    parent = list(range(n))
    rank = [0] * n
    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    def union(x, y):
        rx, ry = find(x), find(y)
        if rx != ry:
            if rank[rx] < rank[ry]:
                parent[rx] = ry
            elif rank[rx] > rank[ry]:
                parent[ry] = rx
            else:
                parent[rx] = ry
                rank[ry] += 1

    res = [False] * len(queries)
    edge_idx = 0

    for query_idx, (p, q, limit) in sorted_queries:
        # Add all edges with weight < limit to the graph
        while edge_idx < len(edgeList) and edgeList[edge_idx][2] < limit:
            union(edgeList[edge_idx][0], edgeList[edge_idx][1])
            edge_idx += 1

        # Check if p and q are connected in the current graph
        if find(p) == find(q):
            res[query_idx] = True

    return res
```

**Explanation**:
1. This is an offline query problem. Instead of running a new search for each query, we sort both edges and queries.
2. We process queries in increasing order of their `limit`.
3. For each query, we add all edges from `edgeList` that are smaller than the current query's `limit`.
4. Then we simply check if the two nodes are connected using `find`.

**Complexity Analysis**:
- **Time Complexity**: $O(E \log E + Q \log Q + (E+Q) \alpha(n))$, where $E$ is edges and $Q$ is queries.
- **Space Complexity**: $O(n + Q)$ to store parent array and results.

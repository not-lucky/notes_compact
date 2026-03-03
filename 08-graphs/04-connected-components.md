# Connected Components

> **Prerequisites:** [02-bfs-basics](./02-bfs-basics.md), [03-dfs-basics](./03-dfs-basics.md)

## Building Intuition

**The Island Exploration Mental Model**: Imagine you're flying over an archipelago. Each island is separate — you can walk anywhere within an island, but you need to fly between islands.

```
Archipelago (Graph):        Components:
    0---1      4---5        Island 1: {0, 1, 2, 3}
    |   |      |            Island 2: {4, 5, 6}
    2---3      6            Island 3: {7}

               7
```

**The key insight**: A connected component is a "maximal" connected subgraph — you can't add more nodes without breaking connectivity.

### Why DFS/BFS Finds Components

Both DFS and BFS are *complete* traversals: starting from any node, they visit **every** reachable node exactly once. This maps perfectly to component discovery:

1. Pick any unvisited node — it belongs to a new, undiscovered component
2. Run DFS/BFS from that node — this visits the **entire** component
3. When the traversal finishes, every node in that component is now marked visited
4. Find the next unvisited node → that's a different component
5. Repeat until all nodes are visited

The number of times you start a new traversal = the number of components.

### Union-Find Perspective

Think of each edge as a "merge" operation — a bottom-up approach:

- **Initially**: every node is its own component (n components)
- **Each edge** unions two components into one (if they weren't already connected)
- **Final count** = n − (number of successful unions)

```
n=5, edges=[[0,1], [1,2], [3,4]]

Initial: 5 components {0}, {1}, {2}, {3}, {4}
Edge 0-1: union(0,1) → 4 components {0,1}, {2}, {3}, {4}
Edge 1-2: union(1,2) → 3 components {0,1,2}, {3}, {4}
Edge 3-4: union(3,4) → 2 components {0,1,2}, {3,4}
```

**When to prefer Union-Find over DFS/BFS:**
- Edges arrive incrementally (dynamic/streaming graph)
- You only need the count or connectivity queries, not the actual component members
- The graph is given as an edge list and you don't want to build an adjacency list

---

## Interview Context

Connected components problems are common because:

1. **Foundation concept**: Understanding graph connectivity
2. **Island problems**: Grid-based component counting
3. **Union-Find preview**: Alternative solution method
4. **Real applications**: Social networks, clustering, image segmentation

**FANG Context:**
- **Amazon** heavily favors grid-based "Island" problems. They love testing if you can traverse a 2D matrix efficiently and handle boundaries correctly without using extra space (modifying the grid in-place).
- **Google** prefers abstract graph representations (adjacency lists/matrices) and will often frame Connected Components as finding clusters of related users, machines, or events. They might also push for Union-Find to handle dynamic connectivity streams.

"Number of Islands" is one of the most frequently asked FANG+ problems.

---

## Core Concept

A **connected component** is a maximal set of vertices where a path exists between every pair.

```
Graph with 3 components:

  0---1      4---5      7
  |   |      |
  2---3      6

Component 1: {0, 1, 2, 3}
Component 2: {4, 5, 6}
Component 3: {7}
```

### Edge Types in DFS

When traversing to find components using DFS, understanding edge types helps debug cycle detection:

1. **Tree Edges**: Edges that discover new vertices during DFS. They form the DFS tree.
2. **Back Edges**: Edges connecting a node to an ancestor in the DFS tree. Indicates a **cycle**.

*In an undirected graph DFS, edges are strictly either Tree Edges or Back Edges. Forward edges and cross edges only appear in directed graphs.*

---

## Counting Components: DFS Approach

```python
from collections import defaultdict


def count_components(n: int, edges: list[list[int]]) -> int:
    """
    Count connected components using DFS.

    Time:  O(V + E) — visit every node and edge once
    Space: O(V + E) — adjacency list storage + visited set + recursion stack
    """
    # Build undirected adjacency list
    graph: dict[int, list[int]] = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)

    visited: set[int] = set()
    count = 0

    def dfs(node: int) -> None:
        visited.add(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                dfs(neighbor)

    # Key: iterate ALL nodes, not just those in the edge list
    # (isolated nodes with no edges are components too)
    for node in range(n):
        if node not in visited:
            dfs(node)  # Explores the entire component
            count += 1

    return count


# Usage
n = 5
edges = [[0, 1], [1, 2], [3, 4]]
print(count_components(n, edges))  # 2
```

---

## Counting Components: BFS Approach

```python
from collections import defaultdict, deque


def count_components_bfs(n: int, edges: list[list[int]]) -> int:
    """
    Count connected components using BFS.

    Time:  O(V + E)
    Space: O(V + E)
    """
    graph: dict[int, list[int]] = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)

    visited: set[int] = set()
    count = 0

    for node in range(n):
        if node not in visited:
            # BFS explores the entire component from this node
            queue = deque([node])
            visited.add(node)  # Mark visited BEFORE enqueuing

            while queue:
                curr = queue.popleft()
                for neighbor in graph[curr]:
                    if neighbor not in visited:
                        visited.add(neighbor)
                        queue.append(neighbor)

            count += 1

    return count
```

---

## Get All Components

```python
from collections import defaultdict


def find_all_components(n: int, edges: list[list[int]]) -> list[list[int]]:
    """
    Return all connected components as lists of nodes.

    Time:  O(V + E)
    Space: O(V + E)
    """
    graph: dict[int, list[int]] = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)

    visited: set[int] = set()
    components: list[list[int]] = []

    def dfs(node: int, component: list[int]) -> None:
        visited.add(node)
        component.append(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                dfs(neighbor, component)

    for node in range(n):
        if node not in visited:
            component: list[int] = []
            dfs(node, component)
            components.append(component)

    return components


# Usage
n = 5
edges = [[0, 1], [1, 2], [3, 4]]
print(find_all_components(n, edges))  # [[0, 1, 2], [3, 4]]
```

---

## Number of Islands (Grid Components)

```python
def num_islands(grid: list[list[str]]) -> int:
    """
    Count number of islands (connected '1's) in a grid.
    Modifies grid in-place to mark visited cells (replaces '1' with '0').

    Time:  O(rows × cols) — each cell visited at most once
    Space: O(rows × cols) — worst-case recursion depth (snake-shaped island)
    """
    if not grid:
        return 0

    rows, cols = len(grid), len(grid[0])
    count = 0

    def dfs(r: int, c: int) -> None:
        # Bounds check + already visited or water
        if r < 0 or r >= rows or c < 0 or c >= cols or grid[r][c] != '1':
            return

        grid[r][c] = '0'  # Mark visited by sinking the land

        # Explore all 4 directions
        dfs(r + 1, c)
        dfs(r - 1, c)
        dfs(r, c + 1)
        dfs(r, c - 1)

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1':
                dfs(r, c)  # Sink the entire island
                count += 1

    return count
```

---

## Islands with Separate Visited Set

When you can't modify the input grid:

```python
def num_islands_no_modify(grid: list[list[str]]) -> int:
    """
    Count islands without modifying grid.
    Uses a separate visited set instead of in-place mutation.

    Time:  O(rows × cols)
    Space: O(rows × cols) — for the visited set + recursion stack
    """
    if not grid:
        return 0

    rows, cols = len(grid), len(grid[0])
    visited: set[tuple[int, int]] = set()
    count = 0

    def dfs(r: int, c: int) -> None:
        if (r < 0 or r >= rows or c < 0 or c >= cols
                or (r, c) in visited or grid[r][c] != '1'):
            return

        visited.add((r, c))

        dfs(r + 1, c)
        dfs(r - 1, c)
        dfs(r, c + 1)
        dfs(r, c - 1)

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1' and (r, c) not in visited:
                dfs(r, c)
                count += 1

    return count
```

---

## BFS for Islands (Avoids Stack Overflow)

For large grids, recursive DFS can hit Python's recursion limit. BFS is the safe choice:

```python
from collections import deque


def num_islands_bfs(grid: list[list[str]]) -> int:
    """
    Count islands using BFS.
    Preferred for very large grids — no recursion limit issues.

    Time:  O(rows × cols)
    Space: O(min(rows, cols)) — BFS queue holds at most one diagonal layer
    """
    if not grid:
        return 0

    rows, cols = len(grid), len(grid[0])
    count = 0
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1':
                count += 1

                # BFS to mark all connected land
                queue = deque([(r, c)])
                grid[r][c] = '0'  # Mark visited immediately

                while queue:
                    cr, cc = queue.popleft()

                    for dr, dc in directions:
                        nr, nc = cr + dr, cc + dc
                        if (0 <= nr < rows and 0 <= nc < cols
                                and grid[nr][nc] == '1'):
                            grid[nr][nc] = '0'  # Mark BEFORE enqueuing
                            queue.append((nr, nc))

    return count
```

> **Space note**: BFS queue space for a grid is `O(min(rows, cols))` because the
> wavefront expands as a diagonal band. This is better than recursive DFS's
> `O(rows × cols)` worst-case stack depth.

---


## Iterative DFS for Islands (No Recursion Limit)

If you must use DFS but want to avoid the recursion depth limit, use an explicit stack. This is effectively the same as BFS but using a `list` (stack) instead of a `deque` (queue).

```python
def num_islands_iterative_dfs(grid: list[list[str]]) -> int:
    """
    Count islands using iterative DFS.
    Avoids Python recursion limits without using BFS.

    Time:  O(rows × cols)
    Space: O(rows × cols) — worst-case stack size
    """
    if not grid:
        return 0

    rows, cols = len(grid), len(grid[0])
    count = 0
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1':
                count += 1
                
                # Start iterative DFS
                stack = [(r, c)]
                grid[r][c] = '0'  # Mark visited immediately

                while stack:
                    cr, cc = stack.pop()  # Pop from end (LIFO)

                    for dr, dc in directions:
                        nr, nc = cr + dr, cc + dc
                        if (0 <= nr < rows and 0 <= nc < cols 
                                and grid[nr][nc] == '1'):
                            grid[nr][nc] = '0'  # Mark BEFORE pushing
                            stack.append((nr, nc))

    return count
```

## Largest Component Size

```python
from collections import defaultdict


def largest_component(n: int, edges: list[list[int]]) -> int:
    """
    Find the size of the largest connected component.

    Time:  O(V + E)
    Space: O(V + E)
    """
    graph: dict[int, list[int]] = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)

    visited: set[int] = set()
    max_size = 0

    def dfs(node: int) -> int:
        visited.add(node)
        size = 1
        for neighbor in graph[node]:
            if neighbor not in visited:
                size += dfs(neighbor)
        return size

    for node in range(n):
        if node not in visited:
            max_size = max(max_size, dfs(node))

    return max_size
```

---

## Max Area of Island

```python
def max_area_island(grid: list[list[int]]) -> int:
    """
    Find area of the largest island. (LC 695)
    Note: grid values are int (0/1), not str ('0'/'1').

    Time:  O(rows × cols)
    Space: O(rows × cols) — recursion stack
    """
    if not grid:
        return 0

    rows, cols = len(grid), len(grid[0])
    max_area = 0

    def dfs(r: int, c: int) -> int:
        if r < 0 or r >= rows or c < 0 or c >= cols or grid[r][c] != 1:
            return 0

        grid[r][c] = 0  # Mark visited
        area = 1
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            area += dfs(r + dr, c + dc)
        return area

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 1:
                max_area = max(max_area, dfs(r, c))

    return max_area
```

---

## Union-Find Approach

Union-Find (Disjoint Set Union) solves connectivity problems without explicitly building or traversing a graph. It processes edges directly.

**Core operations:**
- `find(x)` — returns the root representative of x's component (with path compression)
- `union(x, y)` — merges the components containing x and y (with union by rank)

Both operations run in amortized `O(α(n))` time, where `α` is the inverse Ackermann function — effectively constant.

```python
class UnionFind:
    """Disjoint Set Union with path compression and union by rank."""

    def __init__(self, n: int) -> None:
        self.parent = list(range(n))  # Each node is its own root initially
        self.rank = [0] * n           # Rank tracks tree depth (upper bound)
        self.count = n                # Number of distinct components

    def find(self, x: int) -> int:
        """Find root of x's component with path compression."""
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x: int, y: int) -> bool:
        """
        Merge components of x and y. Returns True if a merge happened
        (they were in different components), False if already connected.
        """
        root_x, root_y = self.find(x), self.find(y)
        if root_x == root_y:
            return False  # Already in the same component

        # Union by rank: attach smaller tree under larger tree's root
        if self.rank[root_x] < self.rank[root_y]:
            root_x, root_y = root_y, root_x
        self.parent[root_y] = root_x
        if self.rank[root_x] == self.rank[root_y]:
            self.rank[root_x] += 1

        self.count -= 1
        return True


def count_components_uf(n: int, edges: list[list[int]]) -> int:
    """Count connected components using Union-Find."""
    uf = UnionFind(n)
    for u, v in edges:
        uf.union(u, v)
    return uf.count
```

---


## Number of Provinces (Adjacency Matrix)

When the graph is given as an adjacency matrix (like in LeetCode 547) instead of an edge list, we adjust our traversal to loop through the matrix rows/cols.

```python
def find_circle_num(isConnected: list[list[int]]) -> int:
    """
    Count components when given an adjacency matrix.
    isConnected[i][j] == 1 means node i and node j are connected.

    Time:  O(V²) — we might check every cell in the V×V matrix
    Space: O(V)  — for the visited set and recursion stack
    """
    n = len(isConnected)
    visited = set()
    provinces = 0

    def dfs(node: int) -> None:
        visited.add(node)
        # Check all possible neighbors (0 to n-1)
        for neighbor in range(n):
            if isConnected[node][neighbor] == 1 and neighbor not in visited:
                dfs(neighbor)

    for i in range(n):
        if i not in visited:
            dfs(i)
            provinces += 1

    return provinces
```

## When to Use Which Approach

| Criterion                      | DFS/BFS              | Union-Find               |
| ------------------------------ | -------------------- | ------------------------ |
| Static graph, need components  | **Best** — simple    | Works but overkill       |
| Dynamic graph (edges added)    | Must rebuild         | **Best** — incremental   |
| Only need count/connectivity   | Works                | **Best** — no graph build|
| Need actual component members  | **Best** — natural   | Requires extra tracking  |
| Grid problem                   | **Best** — intuitive | Possible but awkward     |
| Directed graph                 | Need special algo    | Not applicable           |

**Common mistakes:**
- Forgetting isolated nodes → they're components too!
- Only running DFS from node 0 → misses other components
- Treating a directed graph as undirected → different semantics (use Tarjan's/Kosaraju's for strongly connected components)

**Grid-specific traps:**
- Not checking all 4 (or 8) directions → missed connections
- Stack overflow on large grids → use BFS or iterative DFS instead of recursive DFS

---

## Complexity Analysis

| Approach       | Time           | Space                    | Notes                         |
| -------------- | -------------- | ------------------------ | ----------------------------- |
| DFS (recursive)| O(V + E)       | O(V + E)                 | Graph storage + visited + stack |
| BFS            | O(V + E)       | O(V + E)                 | Graph storage + visited + queue |
| Union-Find     | O(V + E × α(V))| O(V)                     | No graph build needed          |
| Grid DFS       | O(rows × cols) | O(rows × cols)           | Recursion stack worst case     |
| Grid BFS       | O(rows × cols) | O(min(rows, cols))       | Queue holds one wavefront band |

> α(n) is the inverse Ackermann function — effectively constant for all practical inputs (α(n) ≤ 4 for n < 10^80).

### Sparse vs Dense Graphs

- **Sparse (E ≈ V)**: DFS/BFS run close to `O(V)`. Union-Find is effectively linear. Both are fast.
- **Dense (E ≈ V²)**: DFS/BFS hit `O(V²)`. Union-Find also processes all `O(V²)` edges. Adjacency matrix vs list matters here.

### Recursion Stack Limits

Recursive DFS has a critical real-world limitation: **Python's default recursion limit is 1000**.

- **Linear chains**: A path graph of V nodes requires V recursive calls.
- **Grid snakes**: A zig-zagging island can hit depth `rows × cols`.
- **Solution**: For grids larger than ~30×30 or graphs with 1000+ nodes, use **BFS or iterative DFS**.

You can raise the limit with `sys.setrecursionlimit()`, but this is fragile and not recommended for interviews — prefer iterative approaches.

---

## Edge Cases

```python
# 1. No nodes
count_components(0, [])          # → 0 components

# 2. All isolated nodes (no edges)
count_components(5, [])          # → 5 components

# 3. Fully connected graph
count_components(3, [[0,1], [1,2], [0,2]])  # → 1 component

# 4. Empty grid
num_islands([])                  # → 0 islands

# 5. All water
num_islands([['0','0'], ['0','0']])  # → 0 islands

# 6. All land
num_islands([['1','1'], ['1','1']])  # → 1 island

# 7. Single node, no edges
count_components(1, [])          # → 1 component
```

---

## Interview Tips

1. **Ask if you can modify input**: Grid modification saves space vs. a separate visited set.
2. **Consider stack overflow**: Mention BFS for large grids — interviewers love this awareness.
3. **Handle edge cases first**: Empty graph, single node, all isolated nodes.
4. **Know Union-Find as an alternative**: Especially for dynamic connectivity or when asked for a follow-up.
5. **8-directional movement**: Some problems count diagonal neighbors. Clarify before coding.
6. **Complexity precision**: Don't say "O(n)" — specify O(V + E) for graphs, O(rows × cols) for grids.

---

## Practice Problems

Progressive difficulty — master these in order:

| #   | Problem                                        | LC # | Difficulty | Key Concept                        | Hint                                            |
| --- | ---------------------------------------------- | ---- | ---------- | ---------------------------------- | ------------------------------------------------ |
| 1   | Flood Fill                                     | 733  | Easy       | Basic grid DFS/BFS                 | It's just "find the component and recolor it"    |
| 2   | Number of Islands                              | 200  | Medium     | Grid component counting            | Each '1' cell you haven't visited starts a new DFS|
| 3   | Max Area of Island                             | 695  | Medium     | Component size in grid             | DFS returns area; track the global max            |
| 4   | Number of Provinces                            | 547  | Medium     | Adjacency matrix components        | Input is a matrix, not edge list — adapt accordingly|
| 5   | Number of Connected Components in an Undirected Graph | 323 | Medium | Standard graph components     | Direct application of count_components above      |
| 6   | Accounts Merge                                 | 721  | Medium     | Union-Find on non-numeric keys     | Union emails that share an account; group by root |
| 7   | Surrounded Regions                             | 130  | Medium     | Border-connected components        | Start DFS from border 'O's; everything else flips |
| 8   | Making A Large Island                          | 827  | Hard       | Component sizes + flipping one cell| Label each island with its size; check neighbors of each '0' |

---

## Key Takeaways

1. **Iterate ALL nodes**: Don't assume the graph is connected — launch DFS/BFS from every unvisited node.
2. **Mark visited early**: Mark nodes visited *before* (BFS) or *upon entry* (DFS) to prevent revisiting.
3. **Grid = implicit graph**: Each cell is a node; adjacency is the 4 (or 8) cardinal neighbors.
4. **Modify vs. visited set**: In-place mutation saves space but destroys input — ask the interviewer.
5. **Union-Find for dynamic graphs**: When edges arrive over time, Union-Find avoids rebuilding the graph.
6. **BFS over recursive DFS for large inputs**: Avoids stack overflow; mention this proactively in interviews.

---

## Next: [05-cycle-detection-directed.md](./05-cycle-detection-directed.md)

Learn to detect cycles in directed graphs.

# Connected Components

> **Prerequisites:** [02-bfs-basics](./02-bfs-basics.md), [03-dfs-basics](./03-dfs-basics.md)

## Building Intuition

**The Island Exploration Mental Model**: Imagine you're flying over an archipelago. Each island is separate - you can walk anywhere within an island, but you need to fly between islands.

```
Archipelago (Graph):        Components:
    0---1      4---5        Island 1: {0, 1, 2, 3}
    |   |      |            Island 2: {4, 5, 6}
    2---3      6            Island 3: {7}

               7
```

**The key insight**: A connected component is a "maximal" connected subgraph - you can't add more nodes without breaking connectivity.

**Why DFS/BFS finds components**:

1. Start at any unvisited node
2. Traverse visits ALL reachable nodes (entire component)
3. When traversal ends, that's one complete component
4. Find another unvisited node → new component
5. Repeat until all nodes visited

**Union-Find perspective**:
Think of each edge as a "merge" operation:

- Initially: every node is its own component
- Each edge unions two components into one
- Final number of components = n - (successful unions)

```
n=5, edges=[[0,1], [1,2], [3,4]]

Initial: 5 components {0}, {1}, {2}, {3}, {4}
Edge 0-1: union(0,1) → 4 components {0,1}, {2}, {3}, {4}
Edge 1-2: union(1,2) → 3 components {0,1,2}, {3}, {4}
Edge 3-4: union(3,4) → 2 components {0,1,2}, {3,4}
```

---

## When NOT to Use

**DFS/BFS component counting is wrong when:**

- **Graph is directed** → "Connected" means different things (weak vs strong connectivity)
- **Dynamic graph** → Edges added/removed frequently; use Union-Find instead
- **Only need count, not actual components** → Union-Find is simpler

**Union-Find is overkill when:**

- Graph is static (won't change) → DFS is simpler to implement
- Need to output actual components → DFS naturally collects members
- Graph is small → Difference doesn't matter

**Common mistake scenarios:**

- Forgetting isolated nodes → They're components too!
- Only running DFS from node 0 → Misses other components
- Treating directed graph as undirected → Different semantics

**Grid-specific traps:**

- Not checking all 4/8 directions → Missed connections
- Stack overflow on large grids → Use BFS instead of recursive DFS

---

## Interview Context

Connected components problems are common because:

1. **Foundation concept**: Understanding graph connectivity
2. **Island problems**: Grid-based component counting
3. **Union-Find preview**: Alternative solution method
4. **Real applications**: Social networks, clustering

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

### Deep Dive: Edge Types in DFS
When traversing to find components using DFS, understanding edge types can help debug cycle detection and understand graph structure:
1. **Tree Edges**: Edges that discover new vertices during DFS. They form the "DFS tree" or component backbone.
2. **Back Edges**: Edges connecting a node to an ancestor in the DFS tree. A back edge indicates a **cycle** within the component.
3. **Forward Edges**: Edges connecting a node to a descendant (non-child) in the DFS tree. (Primarily relevant in directed graphs).
4. **Cross Edges**: All other edges. They can connect nodes in the same tree (without ancestor/descendant relationship) or across different DFS trees. (Common in directed graphs, cross-component edges don't exist in valid connected components of undirected graphs).

*Note: In an undirected graph DFS, edges are strictly either Tree Edges or Back Edges.*

---

## Counting Components: DFS Approach

```python
from collections import defaultdict

def count_components(n: int, edges: list[list[int]]) -> int:
    """
    Count connected components using DFS.

    Time: O(V + E)
    Space: O(V)
    """
    # Build graph
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)

    visited = set()
    count = 0

    def dfs(node: int):
        visited.add(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                dfs(neighbor)

    # Iterate over all nodes
    for node in range(n):
        if node not in visited:
            dfs(node)
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

    Time: O(V + E)
    Space: O(V)
    """
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)

    visited = set()
    count = 0

    for node in range(n):
        if node not in visited:
            # BFS from this node
            queue = deque([node])
            visited.add(node)

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
def find_all_components(n: int, edges: list[list[int]]) -> list[list[int]]:
    """
    Return all connected components as lists of nodes.

    Time: O(V + E)
    Space: O(V)
    """
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)

    visited = set()
    components = []

    def dfs(node: int, component: list):
        visited.add(node)
        component.append(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                dfs(neighbor, component)

    for node in range(n):
        if node not in visited:
            component = []
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
    Count number of islands (connected 1's).

    Time: O(rows × cols)
    Space: O(rows × cols) for recursion
    """
    if not grid:
        return 0

    rows, cols = len(grid), len(grid[0])
    count = 0

    def dfs(r: int, c: int):
        if (r < 0 or r >= rows or c < 0 or c >= cols or
            grid[r][c] != '1'):
            return

        grid[r][c] = '0'  # Mark as visited by modifying grid

        dfs(r + 1, c)
        dfs(r - 1, c)
        dfs(r, c + 1)
        dfs(r, c - 1)

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1':
                dfs(r, c)
                count += 1

    return count
```

---

## Islands with Separate Visited Set

If you can't modify the grid:

```python
def num_islands_no_modify(grid: list[list[str]]) -> int:
    """
    Count islands without modifying grid.

    Time: O(rows × cols)
    Space: O(rows × cols)
    """
    if not grid:
        return 0

    rows, cols = len(grid), len(grid[0])
    visited = set()
    count = 0

    def dfs(r: int, c: int):
        if (r < 0 or r >= rows or c < 0 or c >= cols or
            (r, c) in visited or grid[r][c] != '1'):
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

```python
from collections import deque

def num_islands_bfs(grid: list[list[str]]) -> int:
    """
    Count islands using BFS.
    Better for very large grids (no recursion limit).
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
                grid[r][c] = '0'

                while queue:
                    cr, cc = queue.popleft()

                    for dr, dc in directions:
                        nr, nc = cr + dr, cc + dc
                        if (0 <= nr < rows and 0 <= nc < cols and
                            grid[nr][nc] == '1'):
                            grid[nr][nc] = '0'
                            queue.append((nr, nc))

    return count
```

---

## Largest Component Size

```python
def largest_component(n: int, edges: list[list[int]]) -> int:
    """
    Find the size of the largest connected component.

    Time: O(V + E)
    Space: O(V)
    """
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)

    visited = set()
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
            component_size = dfs(node)
            max_size = max(max_size, component_size)

    return max_size
```

---

## Max Area of Island

```python
def max_area_island(grid: list[list[int]]) -> int:
    """
    Find area of largest island.

    Time: O(rows × cols)
    Space: O(rows × cols)
    """
    if not grid:
        return 0

    rows, cols = len(grid), len(grid[0])
    max_area = 0

    def dfs(r: int, c: int) -> int:
        if (r < 0 or r >= rows or c < 0 or c >= cols or
            grid[r][c] != 1):
            return 0

        grid[r][c] = 0  # Mark visited
        area = 1

        area += dfs(r + 1, c)
        area += dfs(r - 1, c)
        area += dfs(r, c + 1)
        area += dfs(r, c - 1)

        return area

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 1:
                max_area = max(max_area, dfs(r, c))

    return max_area
```

---

## Union-Find Alternative

For component problems, Union-Find can be more efficient:

```python
class UnionFind:
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.rank = [0] * n
        self.count = n  # Number of components

    def find(self, x: int) -> int:
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # Path compression
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

        self.count -= 1
        return True


def count_components_uf(n: int, edges: list[list[int]]) -> int:
    uf = UnionFind(n)
    for u, v in edges:
        uf.union(u, v)
    return uf.count
```

---

## Complexity Analysis

| Approach   | Time           | Space          |
| ---------- | -------------- | -------------- |
| DFS        | O(V + E)       | O(V)           |
| BFS        | O(V + E)       | O(V)           |
| Union-Find | O(E × α(V))    | O(V)           |
| Grid DFS   | O(rows × cols) | O(rows × cols) |

α(n) is inverse Ackermann, effectively constant.

### Sparse vs Dense Complexity Details
The graph structure significantly impacts the practical performance of connectivity algorithms:

*   **Sparse Graphs (E ≈ V)**: These are graphs with few edges per node (like trees or long linear chains).
    *   DFS & BFS are highly efficient, performing closer to `O(V)`.
    *   Union-Find handles sparse graphs well, effectively linear time.
*   **Dense Graphs (E ≈ V²)**: These graphs have many edges between nodes, nearing a complete graph.
    *   DFS & BFS can hit their worst-case `O(E) = O(V²)` bounds as they iterate through numerous connections. Adjacency lists vs Adjacency matrices become crucial here.
    *   Union-Find performance starts to bottleneck on the edge unions `O(E)`.

### Recursion Stack Space Limits
While DFS provides elegant and simple component counting, it suffers from a major real-world drawback: **Call Stack Limits**.

*   **Linear Chains**: The worst-case for recursion is a graph formatted like a long linked-list. Finding the connected component requires recursive calls equal to `V`.
*   **Grid "Snakes"**: In "Islands" problems, a zig-zagging island can hit depth `rows * cols`.
*   **Consequence**: Python has a default recursion limit of `1000`. An exceptionally long, thin island *will* crash your DFS implementation.
*   **Solution**: For production code or interviews where maximum grid size exceeds `10,000` cells, **always use BFS or Iterative DFS**.

---

## Edge Cases

```python
# 1. No nodes
n = 0, edges = []  # 0 components

# 2. All isolated nodes
n = 5, edges = []  # 5 components

# 3. Fully connected
n = 3, edges = [[0,1], [1,2], [0,2]]  # 1 component

# 4. Empty grid
grid = []  # 0 islands

# 5. All water
grid = [['0', '0'], ['0', '0']]  # 0 islands

# 6. All land
grid = [['1', '1'], ['1', '1']]  # 1 island
```

---

## Interview Tips

1. **Ask if you can modify input**: Grid modification vs separate visited
2. **Consider stack overflow**: Use BFS for very large grids
3. **Handle edge cases**: Empty graph, all isolated nodes
4. **Know Union-Find alternative**: More efficient for some variations
5. **8-directional**: Some problems allow diagonal movement

---

## Practice Problems

| #   | Problem                        | Difficulty | Key Variation          |
| --- | ------------------------------ | ---------- | ---------------------- |
| 1   | Number of Islands              | Medium     | Grid components        |
| 2   | Max Area of Island             | Medium     | Component size         |
| 3   | Number of Connected Components | Medium     | Graph components       |
| 4   | Friend Circles                 | Medium     | Adjacency matrix       |
| 5   | Surrounded Regions             | Medium     | Border-connected       |
| 6   | Number of Provinces            | Medium     | Same as friend circles |

---

## Key Takeaways

1. **Iterate all nodes**: Don't assume graph is connected
2. **Mark visited early**: Prevent revisiting
3. **Grid = implicit graph**: Each cell is a node
4. **Modify vs visited set**: Trade-off between space and immutability
5. **Union-Find alternative**: Good for dynamic connectivity

---

## Next: [05-cycle-detection-directed.md](./05-cycle-detection-directed.md)

Learn to detect cycles in directed graphs.

# Solutions: Graph Representations

## Practice Problems

| # | Problem | Difficulty | Key Concept |
|---|---------|------------|-------------|
| 1 | Find if Path Exists in Graph | Easy | Basic graph traversal |
| 2 | Clone Graph | Medium | Graph construction |
| 3 | Number of Islands | Medium | Grid as graph |
| 4 | Graph Valid Tree | Medium | Connected + acyclic |

---

## 1. Find if Path Exists in Graph

### Problem Statement
Given an undirected graph, determine if there is a valid path between a source vertex and a destination vertex. The graph is given as an edge list.

### Examples & Edge Cases
- **Example 1**: `n = 3, edges = [[0,1],[1,2],[2,0]], source = 0, destination = 2` -> `True` (Path: 0 -> 1 -> 2 or 0 -> 2)
- **Example 2**: `n = 6, edges = [[0,1],[0,2],[3,5],[5,4],[4,3]], source = 0, destination = 5` -> `False` (Components {0,1,2} and {3,4,5} are disconnected)
- **Edge Cases**:
    - `source == destination`: Always `True`.
    - `n = 1`: Always `True` if `source == destination == 0`.
    - Disconnected components: Must handle nodes that aren't reachable.
    - Cyclic graphs: Must use a `visited` set to avoid infinite loops.

### Optimal Python Solution

```python
from collections import defaultdict, deque

def validPath(n: int, edges: list[list[int]], source: int, destination: int) -> bool:
    # Handle base case
    if source == destination:
        return True

    # 1. Build Adjacency List
    # Time: O(E), Space: O(V + E)
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)

    # 2. BFS Traversal
    # Time: O(V + E), Space: O(V)
    visited = {source}
    queue = deque([source])

    while queue:
        curr = queue.popleft()

        # Check all neighbors
        for neighbor in graph[curr]:
            if neighbor == destination:
                return True
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

    return False
```

### Explanation
1. **Graph Construction**: We first convert the edge list into an adjacency list for efficient neighbor lookup. Using `defaultdict(list)` simplifies this process.
2. **Traversal**: We use Breadth-First Search (BFS) starting from the `source`. BFS explores neighbors layer by layer, which is ideal for finding connectivity.
3. **Cycle Prevention**: The `visited` set ensures we don't process the same node multiple times, preventing infinite loops in cyclic graphs.
4. **Early Exit**: If we encounter the `destination` node during traversal, we immediately return `True`.

### Complexity Analysis
- **Time Complexity**: **O(V + E)**. We spend O(E) to build the graph and O(V + E) to traverse it (visiting each node once and each edge twice).
- **Space Complexity**: **O(V + E)**. The adjacency list takes O(V + E) space, and the `visited` set/queue take O(V) space.

---

## 2. Clone Graph

### Problem Statement
Given a reference to a node in a connected undirected graph, return a deep copy (clone) of the graph. Each node contains a `val` (int) and a list of its `neighbors`.

### Examples & Edge Cases
- **Example 1**: Input `adjList = [[2,4],[1,3],[2,4],[1,3]]` -> Output a deep copy of the same structure.
- **Edge Cases**:
    - `None` input: Return `None`.
    - Single node graph: Return a copy of that node with empty neighbors.
    - Graph with cycles: Must track cloned nodes to avoid infinite recursion and ensure we link to the same instance.

### Optimal Python Solution

```python
class Node:
    def __init__(self, val = 0, neighbors = None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []

def cloneGraph(node: 'Node') -> 'Node':
    if not node:
        return None

    # Map to store {Original Node: Cloned Node}
    clones = {node: Node(node.val)}
    queue = deque([node])

    while queue:
        curr = queue.popleft()

        # Process neighbors
        for neighbor in curr.neighbors:
            # If neighbor not cloned yet, clone it and add to queue
            if neighbor not in clones:
                clones[neighbor] = Node(neighbor.val)
                queue.append(neighbor)

            # Link cloned curr node to cloned neighbor node
            clones[curr].neighbors.append(clones[neighbor])

    return clones[node]
```

### Explanation
1. **Mapping**: We use a dictionary `clones` to map original nodes to their copies. This serves two purposes: storing the result and acting as a `visited` set.
2. **Traversal**: We use BFS (or DFS) to explore the graph. When we encounter a neighbor, we check if it has already been cloned.
3. **Cloning & Linking**:
    - If the neighbor isn't in `clones`, we create a new `Node` and add it to the queue.
    - We then append the cloned neighbor to the `neighbors` list of the current cloned node.

### Complexity Analysis
- **Time Complexity**: **O(V + E)**. We visit every vertex and every edge once to perform the cloning and linking.
- **Space Complexity**: **O(V)**. The `clones` map stores V nodes, and the queue stores at most V nodes.

---

## 3. Number of Islands

### Problem Statement
Given an `m x n` 2D binary grid which represents a map of '1's (land) and '0's (water), return the number of islands. An island is surrounded by water and is formed by connecting adjacent lands horizontally or vertically.

### Examples & Edge Cases
- **Example 1**: `grid = [["1","1","0"],["1","1","0"],["0","0","1"]]` -> Output: 2
- **Edge Cases**:
    - Empty grid: 0 islands.
    - Grid with all '0's: 0 islands.
    - Grid with all '1's: 1 island.
    - Grid with diagonal land: Diagonals don't count as connected.

### Optimal Python Solution

```python
def numIslands(grid: list[list[str]]) -> int:
    if not grid:
        return 0

    rows, cols = len(grid), len(grid[0])
    islands = 0

    def bfs(r, c):
        queue = deque([(r, c)])
        grid[r][c] = "0"  # Mark as visited by sinking the island

        while queue:
            curr_r, curr_c = queue.popleft()
            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nr, nc = curr_r + dr, curr_c + dc
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == "1":
                    grid[nr][nc] = "0"  # Mark visited
                    queue.append((nr, nc))

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "1":
                islands += 1
                bfs(r, c)

    return islands
```

### Explanation
1. **Grid as Graph**: Each cell is a node, and adjacent '1's have edges between them.
2. **Traversal Strategy**: We iterate through every cell. When we find a '1', we've found a new island.
3. **Sinking the Island**: To mark cells as visited without extra space, we flip '1' to '0' during BFS.
4. **BFS Expansion**: The `bfs` function explores all connected land for the current island, ensuring each island is counted exactly once.

### Complexity Analysis
- **Time Complexity**: **O(M × N)**. We visit each cell at most once.
- **Space Complexity**: **O(min(M, N))**. The queue in BFS can grow to the size of the smaller dimension of the grid in the worst case.

---

## 4. Graph Valid Tree

### Problem Statement
Given `n` nodes labeled from `0` to `n - 1` and a list of undirected edges, write a function to check whether these edges make up a valid tree.

### Examples & Edge Cases
- **Example 1**: `n = 5, edges = [[0,1], [0,2], [0,3], [1,4]]` -> `True`
- **Example 2**: `n = 5, edges = [[0,1], [1,2], [2,3], [1,3], [1,4]]` -> `False` (Contains cycle)
- **Edge Cases**:
    - `n = 1, edges = []`: `True` (Single node is a tree).
    - Disconnected components: `False` (A tree must be connected).
    - Cyclic graph: `False`.

### Optimal Python Solution

```python
def validTree(n: int, edges: list[list[int]]) -> bool:
    # A tree with n nodes must have exactly n-1 edges
    if len(edges) != n - 1:
        return False

    # Build graph
    adj = defaultdict(list)
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)

    # Check connectivity using BFS
    visited = {0} if n > 0 else set()
    queue = deque([0]) if n > 0 else deque()

    while queue:
        curr = queue.popleft()
        for neighbor in adj[curr]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

    # If we visited all nodes, it's connected and thus a valid tree
    return len(visited) == n
```

### Explanation
1. **Math Property**: A valid tree must satisfy two conditions:
    - It is connected.
    - It has no cycles.
    - **Key Insight**: In a graph with `n` nodes, if it has exactly `n-1` edges AND is connected, it MUST be acyclic.
2. **Edge Count**: We first check if `len(edges) == n - 1`. If not, it's either disconnected or has a cycle.
3. **Connectivity**: We use BFS to see if we can reach all `n` nodes starting from node `0`.
4. **Conclusion**: If `len(visited) == n`, the graph is connected and has the correct number of edges, making it a valid tree.

### Complexity Analysis
- **Time Complexity**: **O(V + E)**. Building the graph takes O(E) and BFS takes O(V + E).
- **Space Complexity**: **O(V + E)**. To store the adjacency list and the visited set.

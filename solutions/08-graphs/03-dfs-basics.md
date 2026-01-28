# Solutions: DFS Basics

## Practice Problems

| #   | Problem                         | Difficulty | Key Pattern          |
| --- | ------------------------------- | ---------- | -------------------- |
| 1   | Flood Fill                      | Easy       | Basic grid DFS       |
| 2   | Number of Islands               | Medium     | Component counting   |
| 3   | All Paths From Source to Target | Medium     | Path enumeration     |
| 4   | Clone Graph                     | Medium     | DFS with mapping     |
| 5   | Course Schedule II              | Medium     | Topological sort DFS |

---

## 1. Flood Fill

### Problem Statement

Perform a flood fill on an `m x n` image starting from `(sr, sc)` with a new `color`. All connected pixels of the same original color must be changed to the new `color`.

### Examples & Edge Cases

- **Example 1**: `image = [[1,1,1],[1,1,0],[1,0,1]], sr = 1, sc = 1, color = 2` -> `[[2,2,2],[2,2,0],[2,0,1]]`
- **Edge Cases**: `newColor` matches original color (skip to avoid infinite recursion).

### Optimal Python Solution

```python
def floodFill(image: list[list[int]], sr: int, sc: int, color: int) -> list[list[int]]:
    start_color = image[sr][sc]
    if start_color == color:
        return image

    rows, cols = len(image), len(image[0])

    def dfs(r, c):
        # Base case: out of bounds or different color
        if r < 0 or r >= rows or c < 0 or c >= cols or image[r][c] != start_color:
            return

        # Update color
        image[r][c] = color

        # Recursive calls for 4 directions
        dfs(r + 1, c)
        dfs(r - 1, c)
        dfs(r, c + 1)
        dfs(r, c - 1)

    dfs(sr, sc)
    return image
```

### Explanation

1. **Recursive Exploration**: DFS naturally explores all connected components by going as deep as possible in each direction.
2. **Implicit Visited**: By changing the pixel color to the target `color`, we effectively mark it as visited (since `image[r][c] != start_color` will be true for it later).
3. **Safety Check**: The `start_color == color` check is critical to prevent infinite recursion when the target color is the same as the original.

### Complexity Analysis

- **Time Complexity**: **O(M × N)**. Every pixel is visited at most once.
- **Space Complexity**: **O(M × N)**. Worst case recursion stack depth for a grid where all pixels are the same color.

---

## 2. Number of Islands (DFS Focus)

### Problem Statement

Given an `m x n` 2D binary grid, return the number of islands (connected components of "1"s).

### Examples & Edge Cases

- **Example 1**: `grid = [["1","1","0"],["1","1","0"],["0","0","1"]]` -> Output: 2

### Optimal Python Solution

```python
def numIslands(grid: list[list[str]]) -> int:
    if not grid:
        return 0

    rows, cols = len(grid), len(grid[0])
    islands = 0

    def dfs(r, c):
        if r < 0 or r >= rows or c < 0 or c >= cols or grid[r][c] == "0":
            return

        grid[r][c] = "0" # Sink the land
        dfs(r + 1, c)
        dfs(r - 1, c)
        dfs(r, c + 1)
        dfs(r, c - 1)

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "1":
                islands += 1
                dfs(r, c)

    return islands
```

### Explanation

1. **Component Counting**: Each time we find an unvisited "1", it belongs to a new island.
2. **DFS Sinking**: The DFS visits every piece of land in the island and sets it to "0". This eliminates the need for an external `visited` set.
3. **Main Loop**: The nested loop ensures we check every cell in the grid.

### Complexity Analysis

- **Time Complexity**: **O(M × N)**. Every cell is processed exactly once.
- **Space Complexity**: **O(M × N)**. Recursion stack can go up to M\*N in the worst case (e.g., a single snake-like island).

---

## 3. All Paths From Source to Target

### Problem Statement

Given a directed acyclic graph (DAG) of `n` nodes labeled from `0` to `n - 1`, find all possible paths from node `0` to node `n - 1` and return them in any order.

### Examples & Edge Cases

- **Example 1**: `graph = [[1,2],[3],[3],[]]` -> Output: `[[0,1,3],[0,2,3]]`
- **Edge Cases**: The graph is guaranteed to be a DAG, so no cycles exist.

### Optimal Python Solution

```python
def allPathsSourceTarget(graph: list[list[int]]) -> list[list[int]]:
    target = len(graph) - 1
    results = []

    def dfs(node, path):
        if node == target:
            results.append(list(path))
            return

        for neighbor in graph[node]:
            path.append(neighbor)
            dfs(neighbor, path)
            path.pop() # Backtrack

    dfs(0, [0])
    return results
```

### Explanation

1. **Backtracking**: This is a classic backtracking problem using DFS. We maintain a `path` list and explore every neighbor.
2. **Path Maintenance**: After visiting a neighbor recursively, we `pop()` it from the `path` to explore other possibilities from the current node.
3. **Target Reached**: When `node == target`, we have found a valid path and add a copy of it to `results`.

### Complexity Analysis

- **Time Complexity**: **O(2^V × V)**. In a DAG, there can be up to 2^V possible paths, and each path can take O(V) time to copy.
- **Space Complexity**: **O(V)**. The recursion stack and the current path take O(V) space.

---

## 4. Clone Graph (DFS Focus)

### Problem Statement

Deep copy an undirected graph.

### Optimal Python Solution

```python
class Node:
    def __init__(self, val = 0, neighbors = None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []

def cloneGraph(node: 'Node') -> 'Node':
    visited = {} # Map original node to its copy

    def dfs(curr):
        if not curr:
            return None
        if curr in visited:
            return visited[curr]

        # Create copy and mark as visited before recursing neighbors
        copy = Node(curr.val)
        visited[curr] = copy

        for neighbor in curr.neighbors:
            copy.neighbors.append(dfs(neighbor))

        return copy

    return dfs(node)
```

### Explanation

1. **Mapping with Visited**: We use a dictionary to store already cloned nodes. This prevents redundant work and handles cycles.
2. **Recursive Construction**: For each node, we create its copy, add it to the map, and then recursively clone all its neighbors.
3. **Cycle Handling**: Because we add the `copy` to `visited` before recursing into its neighbors, cycles correctly link back to the existing copy.

### Complexity Analysis

- **Time Complexity**: **O(V + E)**. Every node and edge is visited once.
- **Space Complexity**: **O(V)**. To store the cloned nodes in the map and the recursion stack.

---

## 5. Course Schedule II

### Problem Statement

There are `numCourses` courses you have to take, labeled from `0` to `numCourses - 1`. Given a list of prerequisites where `prerequisites[i] = [ai, bi]` means you must take course `bi` before `ai`, return the ordering of courses you should take to finish all courses. If impossible, return an empty array.

### Examples & Edge Cases

- **Example 1**: `numCourses = 2, prerequisites = [[1,0]]` -> `[0,1]`
- **Edge Cases**: Cyclic dependencies (return `[]`).

### Optimal Python Solution

```python
def findOrder(numCourses: int, prerequisites: list[list[int]]) -> list[int]:
    # 1. Build Adjacency List
    adj = {i: [] for i in range(numCourses)}
    for course, prereq in prerequisites:
        adj[course].append(prereq)

    res = []
    # 0 = unvisited, 1 = visiting (in current path), 2 = visited
    visit = [0] * numCourses

    def dfs(course):
        if visit[course] == 1: # Cycle detected!
            return False
        if visit[course] == 2: # Already processed
            return True

        visit[course] = 1 # Mark as visiting
        for neighbor in adj[course]:
            if not dfs(neighbor):
                return False

        visit[course] = 2 # Mark as fully processed
        res.append(course)
        return True

    for i in range(numCourses):
        if not dfs(i):
            return []

    return res
```

### Explanation

1. **Topological Sort**: This problem asks for a topological ordering of courses.
2. **DFS Approach**: We use DFS to find the "post-order" traversal. A course is added to the result list only after all its prerequisites have been processed.
3. **Cycle Detection (3 Colors)**:
   - **Visiting (1)**: The node is in the current recursion stack. If we see it again, there is a cycle.
   - **Visited (2)**: The node and all its neighbors have been fully processed.
4. **Result**: The courses are added to `res` in the order they can be completed. Note that the logic above builds the list from prerequisite to course (or vice versa depending on how you build the graph; here `adj[course]` contains its prerequisites, so it adds prerequisites first).

### Complexity Analysis

- **Time Complexity**: **O(V + E)**. Standard DFS complexity.
- **Space Complexity**: **O(V + E)**. Adjacency list and recursion stack.

# DFS Basics

> **Prerequisites:** [01-graph-representations](./01-graph-representations.md)

## Building Intuition

**The Maze Explorer Mental Model**: Imagine exploring a maze with a ball of string. You:

1. Walk as far as possible in one direction
2. When you hit a dead end, follow the string back
3. Try a different unexplored path
4. Repeat until you've seen everything

```
Maze:             DFS Exploration (string = recursion stack):
┌───┬───┬───┐     Start at A, string at A
│ A │ B │ C │     Go to B, string: A→B
│   ├───┤   │     Go to D, string: A→B→D
│ D │ E │ F │     Dead end! Backtrack to B
│   ├───┤   │     E visited? No, go there: A→B→E
│ G │ H │ I │     Continue until all visited
└───┴───┴───┘
```

**Why DFS uses a stack (or recursion)**:

- Stack = LIFO (Last-In-First-Out)
- We explore the most recent discovery first
- Backtracking happens naturally when we pop
- Recursion IS a stack (the call stack)

**The Recursion Tree Visualization**:

```
DFS from node 0 in graph: 0-[1,2], 1-[3], 2-[4]

Call Stack:           Recursion Tree:
                            dfs(0)
                           /      \
                      dfs(1)      dfs(2)
                        |           |
                      dfs(3)      dfs(4)
```

Each call adds a frame to the stack. When a call finishes, we pop and return to the parent - this is backtracking!

**Key insight - Two types of "visited"**:

1. **Global visited** (for traversal): "Have I ever seen this node?" - prevents cycles
2. **Path visited** (for backtracking): "Is this node in my current path?" - for finding all paths

---

## When NOT to Use

**Don't use DFS when:**

- **Shortest path needed** → DFS may find long path first; use BFS
- **Graph is very wide** → Recursion depth explodes; use BFS or iterative DFS
- **Level-order processing** → BFS naturally gives levels
- **Multi-source problems** → BFS handles multiple starts elegantly

**DFS is problematic when:**

- Python recursion limit (~1000) → Use iterative DFS for deep graphs
- You need distance tracking → BFS is more natural
- Memory is tight and graph is wide → BFS uses O(max-level-width) while DFS uses O(depth)

**Common mistake scenarios:**

- Using global visited for path problems → Blocks valid paths through same node
- Not handling disconnected graphs → Must iterate all nodes
- Modifying graph during traversal → Unpredictable behavior

---

## Interview Context: FANG Expectations

**Amazon's Focus: 2D Grids**
- Amazon heavily tests implicit graphs. You **must** master Grid DFS.
- Problems like "Rotting Oranges", "Number of Islands", or "Word Search" are standard.
- You are expected to code boundary checks elegantly (e.g., using `directions` arrays).
- You are expected to know the exact time complexity: $O(R \times C)$, **not** $O(V + E)$ (although they are the same).
- You are expected to optimize space by modifying the grid in-place (e.g., changing '1' to '0' instead of a `visited` set) if permitted.

**Meta's Focus: Clone Graph & Components**
- Meta often asks "Clone Graph" or "Alien Dictionary" (Topological Sort).
- Meta candidates must know how to map an old node to a new node using a Hash Map.
- If you use Python at Meta, explicitly address the recursion limit (`sys.setrecursionlimit()`). Meta interviewers look for this system-level awareness.

DFS is essential because:

1. **Exhaustive exploration**: Visit all reachable nodes from source
2. **Path problems**: Finding all paths, detecting cycles
3. **Backtracking foundation**: DFS is backtracking on graphs
4. **Topological sort**: DFS-based approach is common

DFS and BFS are the two fundamental graph traversal patterns.

---

## Core Concept: How DFS Works

DFS explores as deep as possible before backtracking, using a **stack** (or recursion):

1. Start from source, push to stack
2. Pop vertex, mark visited, push unvisited neighbors
3. Repeat until stack is empty

```
Graph:          DFS from 0:
    0           Visit: 0 → 1 → 3 → (backtrack) → 2 → 4
   / \
  1   2
  |   |
  3   4

Order visited: 0 → 1 → 3 → 2 → 4
(depends on neighbor order)
```

---

## DFS Template: Recursive (Most Common)

### Python
```python
def dfs_recursive(graph: dict[int, list[int]], start: int) -> list[int]:
    """
    DFS using recursion.

    Time: O(V + E)
    Space: O(V) for recursion stack
    """
    visited = set()
    order = []

    def dfs(node: int):
        visited.add(node)
        order.append(node)

        for neighbor in graph[node]:
            if neighbor not in visited:
                dfs(neighbor)

    dfs(start)
    return order


# Usage
graph = {0: [1, 2], 1: [0, 3], 2: [0, 4], 3: [1], 4: [2]}
print(dfs_recursive(graph, 0))  # [0, 1, 3, 2, 4]
```

---

## DFS Template: Iterative (Using Stack)

### Python
```python
def dfs_iterative(graph: dict[int, list[int]], start: int) -> list[int]:
    """
    DFS using explicit stack.

    Time: O(V + E)
    Space: O(V)

    Note: Order may differ from recursive due to stack LIFO.
    """
    visited = set([start])
    stack = [start]
    order = []

    while stack:
        node = stack.pop()
        order.append(node)

        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                stack.append(neighbor)

    return order


# Usage
graph = {0: [1, 2], 1: [0, 3], 2: [0, 4], 3: [1], 4: [2]}
print(dfs_iterative(graph, 0))  # [0, 2, 4, 1, 3] (different order!)
```

**Note**: Iterative visits in reverse neighbor order due to stack LIFO. To match recursive order, reverse neighbors when pushing.

---

## DFS with Path Tracking

```python
def all_paths_dfs(graph: dict[int, list[int]],
                   start: int, end: int) -> list[list[int]]:
    """
    Find ALL paths from start to end.

    Time: O(V! in worst case - all permutations)
    Space: O(V) for current path
    """
    all_paths = []

    def dfs(node: int, path: list[int]):
        if node == end:
            all_paths.append(path[:])  # Copy current path
            return

        for neighbor in graph[node]:
            if neighbor not in path:  # Avoid cycles in current path
                path.append(neighbor)
                dfs(neighbor, path)
                path.pop()  # Backtrack

    dfs(start, [start])
    return all_paths


# Usage
graph = {0: [1, 2], 1: [0, 3], 2: [0, 3], 3: [1, 2]}
print(all_paths_dfs(graph, 0, 3))  # [[0, 1, 3], [0, 2, 3]]
```

## Theory: Deep Dive into Edge Types

When DFS runs on a graph, it categorizes all edges into four types based on the traversal. This theory is heavily tested in cycle detection and topological sorting.

```
Graph structure during DFS forms a "DFS Tree":

      A (start)
     / \
    B   C
    |    \
    D     E
```

1. **Tree Edge**: Edges in the DFS forest. You discover a new, unvisited vertex.
   - Example: A → B, A → C, B → D
   - **Check**: `visited[v] == false`

2. **Back Edge**: Edge from a vertex to one of its ancestors in the DFS tree.
   - Example: D → A (if edge existed)
   - **Check**: `visited[v] == true` AND `v` is currently in the recursion stack (usually tracked with an `in_path` or `color = GRAY` array).
   - **Crucial application**: The presence of a Back Edge means the graph has a **cycle**.

3. **Forward Edge**: Edge from a vertex to a non-child descendant.
   - Example: A → D (if edge existed, A reaches D without going through B)
   - **Check**: `visited[v] == true` AND `v` was fully processed (`color = BLACK`) AFTER the current vertex was discovered.

4. **Cross Edge**: Edge between two nodes that don't have an ancestor/descendant relationship.
   - Example: B → C or D → E
   - **Check**: `visited[v] == true` AND `v` was fully processed BEFORE the current vertex was discovered.

*Note: In undirected graphs, there are only Tree and Back edges. Forward and Cross edges only exist in directed graphs.*

---

## Theory: Grid Implicit Graphs

In many interview problems, the graph isn't given as an adjacency list. Instead, it's a 2D grid.

A 2D matrix is an **implicit graph**:
- **Vertices (V)**: The cells in the grid.
  - Number of vertices = `Rows × Cols`
- **Edges (E)**: Adjacency between neighboring cells (usually 4-directional: up, down, left, right).
  - Maximum edges = `4 × Rows × Cols`

### Key Differences from Standard Graphs:
1. **No need to build an adjacency list**: Building one takes $O(R \times C)$ extra space. You compute neighbors on the fly.
2. **Boundary Checks**: You must explicitly check if `row` and `col` are within bounds `(0 <= r < R)` and `(0 <= c < C)`.
3. **Space Complexity**: The recursion stack space is bounded by the grid size, which is $O(R \times C)$ worst-case (e.g., a grid shaped like a single winding snake path).

---

## Grid DFS Template

```python
def grid_dfs(grid: list[list[int]],
             start: tuple[int, int]) -> set[tuple[int, int]]:
    """
    DFS on a grid.

    Time: O(rows × cols)
    Space: O(rows × cols)
    """
    rows, cols = len(grid), len(grid[0])
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    visited = set()

    def dfs(r: int, c: int):
        if (r < 0 or r >= rows or c < 0 or c >= cols or
            (r, c) in visited or grid[r][c] != 1):
            return

        visited.add((r, c))

        for dr, dc in directions:
            dfs(r + dr, c + dc)

    dfs(start[0], start[1])
    return visited


# Iterative version (avoids stack overflow)
def grid_dfs_iterative(grid: list[list[int]],
                        start: tuple[int, int]) -> set[tuple[int, int]]:
    rows, cols = len(grid), len(grid[0])
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    visited = set([start])
    stack = [start]

    while stack:
        r, c = stack.pop()

        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if (0 <= nr < rows and 0 <= nc < cols and
                (nr, nc) not in visited and grid[nr][nc] == 1):
                visited.add((nr, nc))
                stack.append((nr, nc))

    return visited
```

---

## DFS for Connected Components

```python
def count_components(n: int, edges: list[list[int]]) -> int:
    """
    Count connected components in undirected graph.

    Time: O(V + E)
    Space: O(V)
    """
    from collections import defaultdict

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

## Pre-order vs Post-order DFS

```python
def dfs_with_order(graph: dict[int, list[int]], start: int):
    """
    DFS showing pre-order and post-order.

    Pre-order: When first visiting node
    Post-order: When finished with all descendants
    """
    visited = set()
    pre_order = []
    post_order = []

    def dfs(node: int):
        visited.add(node)
        pre_order.append(node)  # Before visiting children

        for neighbor in graph[node]:
            if neighbor not in visited:
                dfs(neighbor)

        post_order.append(node)  # After visiting all children

    dfs(start)
    return pre_order, post_order


# Usage
graph = {0: [1, 2], 1: [3], 2: [], 3: []}
pre, post = dfs_with_order(graph, 0)
print(f"Pre-order: {pre}")   # [0, 1, 3, 2]
print(f"Post-order: {post}") # [3, 1, 2, 0]
```

**Post-order is important for:**

- Topological sort (reverse post-order)
- Strongly connected components

---

## DFS with Entry/Exit Times

```python
def dfs_timestamps(graph: dict[int, list[int]], start: int):
    """
    Track when each node is entered and exited.
    Useful for many advanced algorithms.
    """
    visited = set()
    entry = {}
    exit_time = {}
    time = [0]  # Use list to make mutable in nested function

    def dfs(node: int):
        visited.add(node)
        entry[node] = time[0]
        time[0] += 1

        for neighbor in graph[node]:
            if neighbor not in visited:
                dfs(neighbor)

        exit_time[node] = time[0]
        time[0] += 1

    dfs(start)
    return entry, exit_time
```

---

## Recursive vs Iterative Comparison

| Aspect              | Recursive         | Iterative                  |
| ------------------- | ----------------- | -------------------------- |
| Code simplicity     | Cleaner           | More verbose               |
| Stack overflow risk | Yes (deep graphs) | No                         |
| Traversal order     | Natural           | May differ                 |
| Memory control      | Implicit stack    | Explicit stack             |
| When to use         | Default choice    | Deep graphs, Python limits |

**Python recursion limit**: ~1000 by default. Use iterative for deep graphs.

```python
import sys
sys.setrecursionlimit(10000)  # Increase if needed (not recommended)
```

---

## Common Mistakes

```python
# WRONG: Modifying collection while iterating
def dfs(node):
    for neighbor in graph[node]:  # graph may be modified
        if neighbor not in visited:
            dfs(neighbor)
            graph[node].remove(neighbor)  # DON'T!

# CORRECT: Make decisions, don't modify graph


# WRONG: Not handling disconnected graphs
def process_graph(graph):
    dfs(0)  # Only processes component containing 0

# CORRECT: Iterate over all nodes
for node in range(n):
    if node not in visited:
        dfs(node)


# WRONG: Using visited as path checker for backtracking
visited = set()
def dfs(node, path):
    visited.add(node)  # Permanent - blocks revisiting
    if node == end:
        results.append(path)
    for neighbor in graph[node]:
        if neighbor not in visited:
            dfs(neighbor, path + [neighbor])

# CORRECT: Use path as visited for backtracking
def dfs(node, path):
    if node == end:
        results.append(path)
        return
    for neighbor in graph[node]:
        if neighbor not in path:  # Check path, not global visited
            dfs(neighbor, path + [neighbor])
```

---

## Step-by-Step DFS Trace with ASCII Visualization

**Graph for demonstration:**

```
        0
       / \
      1   2
     / \   \
    3   4   5
```

Adjacency list: `{0:[1,2], 1:[0,3,4], 2:[0,5], 3:[1], 4:[1], 5:[2]}`

**Complete recursive DFS trace from node 0:**

```
CALL STACK VISUALIZATION (→ = call, ← = return):

→ dfs(0)
  │ Visited: {0}
  │ Neighbors: [1, 2]
  │
  ├→ dfs(1)          [1 not visited]
  │  │ Visited: {0, 1}
  │  │ Neighbors: [0, 3, 4]
  │  │ Skip 0 (visited)
  │  │
  │  ├→ dfs(3)       [3 not visited]
  │  │  │ Visited: {0, 1, 3}
  │  │  │ Neighbors: [1]
  │  │  │ Skip 1 (visited)
  │  │  │ No more neighbors
  │  │← Return from dfs(3)
  │  │
  │  ├→ dfs(4)       [4 not visited]
  │  │  │ Visited: {0, 1, 3, 4}
  │  │  │ Neighbors: [1]
  │  │  │ Skip 1 (visited)
  │  │  │ No more neighbors
  │  │← Return from dfs(4)
  │  │
  │← Return from dfs(1)
  │
  ├→ dfs(2)          [2 not visited]
  │  │ Visited: {0, 1, 3, 4, 2}
  │  │ Neighbors: [0, 5]
  │  │ Skip 0 (visited)
  │  │
  │  ├→ dfs(5)       [5 not visited]
  │  │  │ Visited: {0, 1, 3, 4, 2, 5}
  │  │  │ Neighbors: [2]
  │  │  │ Skip 2 (visited)
  │  │  │ No more neighbors
  │  │← Return from dfs(5)
  │  │
  │← Return from dfs(2)
  │
← Return from dfs(0)

TRAVERSAL ORDER: [0, 1, 3, 4, 2, 5]
```

**Stack state at each step (iterative visualization):**

```
Step 0: Stack = [0]              Visit 0
Step 1: Stack = [2, 1]           Visit 1 (push neighbors, visit last)
Step 2: Stack = [2, 4, 3]        Visit 3 (skip 0, push 3,4)
Step 3: Stack = [2, 4]           Visit 4 (3 has no unvisited neighbors)
Step 4: Stack = [2]              Visit 2 (4 has no unvisited neighbors)
Step 5: Stack = [5]              Visit 5 (skip 0, push 5)
Step 6: Stack = []               Done

Note: Iterative DFS visits in different order than recursive
depending on how you push neighbors (reverse vs forward).
```

---

## Complexity Derivation with Proof

**Time Complexity: O(V + E)**

```
Proof:
1. Each vertex is visited exactly once
   - The visited set check ensures this
   - Adding to visited happens once per vertex
   - Therefore: O(V) vertex operations

2. For each vertex, we examine all adjacent edges
   - When visiting vertex v, we iterate through adj[v]
   - Each edge is examined twice (undirected) or once (directed)
   - Total edge examinations: O(E)

3. Recursive call overhead is O(1) per call
   - At most V calls (one per vertex)
   - Therefore: O(V) function call overhead

4. Total: O(V) + O(E) = O(V + E)
```

**Space Complexity: O(V)**

```
Proof:
1. Visited set: O(V) space

2. Recursion stack (worst case):
   - Linear graph: 0 → 1 → 2 → ... → V-1
   - Maximum stack depth: V
   - Therefore: O(V) stack space

3. Iterative stack: same worst case O(V)

4. Total: O(V)

Comparison with BFS:
- DFS space depends on graph DEPTH
- BFS space depends on graph WIDTH
- For deep narrow graphs: DFS may use more space
- For wide shallow graphs: BFS may use more space
```

### Recursion Stack Space Limits by Language

This is a critical interview topic. When do you hit a **StackOverflowError**?

| Language | Default Stack Size | Approx. Max Recursion Depth | Risk of Stack Overflow |
|----------|-------------------|-----------------------------|------------------------|
| **Python**| Implicit limit | `sys.getrecursionlimit()` (~1000 by default) | **HIGH**. Exceeds easily on large grids ($30 \times 40 = 1200$). Use `sys.setrecursionlimit()`. |

**Interview Advice**:
- If writing **Python** and solving a 2D Grid problem (e.g., $M, N \le 200$), strongly consider using the Iterative Stack approach, or explicitly state: *"I'm using recursive DFS, but in Python I would need to increase `sys.setrecursionlimit(40000)` to handle worst-case deep paths."*

**Pre-order vs Post-order timing:**

```
Pre-order:  Record node BEFORE visiting children
Post-order: Record node AFTER visiting children

Graph: 0 → 1 → 2

Pre-order traversal:  [0, 1, 2]
Post-order traversal: [2, 1, 0]

Post-order is crucial for:
- Topological sort (reverse post-order)
- Dependency resolution
- Strongly connected components
```

---

## Edge Cases

```python
# 1. Single node
graph = {0: []}
dfs(graph, 0)  # [0]

# 2. No edges
graph = {0: [], 1: [], 2: []}
# Multiple components, each is single node

# 3. Cycle
graph = {0: [1], 1: [2], 2: [0]}
# Visited set prevents infinite loop

# 4. Self-loop
graph = {0: [0, 1]}
# Visited check handles this

# 5. Dense graph (all connected)
# Still O(V + E) time
```

---

## Interview Tips

1. **Default to recursive**: Cleaner code, easier to write correctly
2. **Know iterative version**: For when recursion limit is a concern
3. **Understand pre/post-order**: Critical for topological sort, SCC
4. **Handle disconnected graphs**: Iterate over all nodes
5. **Draw the traversal**: Show stack state if asked

---

## Practice Problems

| #   | Problem                         | Difficulty | Key Pattern          |
| --- | ------------------------------- | ---------- | -------------------- |
| 1   | Flood Fill                      | Easy       | Basic grid DFS       |
| 2   | Number of Islands               | Medium     | Component counting   |
| 3   | All Paths From Source to Target | Medium     | Path enumeration     |
| 4   | Clone Graph                     | Medium     | DFS with mapping     |
| 5   | Course Schedule II              | Medium     | Topological sort DFS |

---

## Key Takeaways

1. **DFS uses stack/recursion**: Go deep, then backtrack
2. **O(V + E) time**: Visit each vertex and edge once
3. **Recursive is cleaner**: But watch for stack overflow
4. **Pre-order vs post-order**: Know when each matters
5. **Global visited vs path**: Different for cycle detection vs path finding

---

## Next: [04-connected-components.md](./04-connected-components.md)

Learn to count and find connected components.

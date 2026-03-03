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

Each call adds a frame to the stack. When a call finishes, we pop and return to the parent — this is backtracking!

**Key insight — Two types of "visited"**:

1. **Global visited** (for traversal): "Have I ever seen this node?" — prevents cycles
2. **Path visited** (for backtracking): "Is this node in my current path?" — for finding all paths

---

## When to Prefer DFS vs BFS

| Use DFS when...                         | Use BFS when...                            |
| ---------------------------------------- | ------------------------------------------ |
| Exhaustive exploration (all paths, etc.) | Shortest path in unweighted graph          |
| Detecting cycles                         | Level-order processing                     |
| Topological ordering                     | Multi-source problems (e.g., rotting oranges) |
| Backtracking / constraint satisfaction   | Finding nearest target                     |
| Path existence (any path, not shortest)  | Distance tracking from source              |
| Deep, narrow graphs (space-efficient)    | Wide, shallow graphs (space-efficient)     |

**Don't use DFS when:**

- **Shortest path needed** → DFS may find a long path first; use BFS
- **Level-order processing** → BFS naturally gives levels
- **Multi-source problems** → BFS handles multiple starts elegantly

**DFS is problematic when:**

- Python recursion limit (~1000) → Use iterative DFS for deep graphs
- You need distance tracking → BFS is more natural
- Memory is tight and graph is deep → DFS stack grows with depth; BFS may use less space for shallow wide graphs

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
- You are expected to know the exact time complexity: $O(R \times C)$, **not** $O(V + E)$ (although they are equivalent for grids).
- You are expected to optimize space by modifying the grid in-place (e.g., changing `'1'` to `'0'` instead of a `visited` set) if permitted.

**Meta's Focus: Clone Graph & Components**
- Meta often asks "Clone Graph" or "Alien Dictionary" (Topological Sort).
- Meta candidates must know how to map an old node to a new node using a Hash Map.
- If you use Python at Meta, explicitly address the recursion limit (`sys.setrecursionlimit()`). Meta interviewers look for this system-level awareness.

DFS is essential because:

1. **Exhaustive exploration**: Visit all reachable nodes from source
2. **Path problems**: Finding all paths, detecting cycles
3. **Backtracking foundation**: DFS is backtracking on graphs
4. **Topological sort**: DFS-based approach is common

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

Recursive DFS maps directly to the mental model: explore one neighbor fully,
then backtrack and try the next. The call stack handles backtracking for you.

```python
def dfs_recursive(graph: dict[int, list[int]], start: int) -> list[int]:
    """
    DFS using recursion.

    Time:  O(V + E) — each vertex visited once, each edge examined once
    Space: O(V) — visited set + recursion stack (worst case: linear chain)
    """
    visited: set[int] = set()
    order: list[int] = []

    def dfs(node: int) -> None:
        visited.add(node)
        order.append(node)                 # Pre-order: process on entry

        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                dfs(neighbor)
        # Post-order work would go here (after all children processed)

    dfs(start)
    return order


# Usage
graph = {0: [1, 2], 1: [0, 3], 2: [0, 4], 3: [1], 4: [2]}
print(dfs_recursive(graph, 0))  # [0, 1, 3, 2, 4]
```

---

## DFS Template: Iterative (Using Stack)

Use iterative DFS when the graph can be deep (>1000 nodes in a chain) to
avoid Python's recursion limit. The explicit stack replaces the call stack.

**Subtle difference from recursive**: Because a stack is LIFO, neighbors pushed
left-to-right are popped right-to-left. To match recursive order, push
neighbors in **reverse**.

```python
def dfs_iterative(graph: dict[int, list[int]], start: int) -> list[int]:
    """
    DFS using explicit stack.

    Time:  O(V + E)
    Space: O(V)

    Note: Visits neighbors in reverse push order due to LIFO.
    """
    visited: set[int] = {start}
    stack: list[int] = [start]
    order: list[int] = []

    while stack:
        node = stack.pop()
        order.append(node)

        # Iterate neighbors in reverse to match recursive DFS order.
        # Without reversed(), the last neighbor is popped first (LIFO).
        for neighbor in reversed(graph.get(node, [])):
            if neighbor not in visited:
                visited.add(neighbor)      # Mark visited on push, not pop
                stack.append(neighbor)

    return order


# Usage
graph = {0: [1, 2], 1: [0, 3], 2: [0, 4], 3: [1], 4: [2]}
print(dfs_iterative(graph, 0))  # [0, 1, 3, 2, 4] (matches recursive with reversed)
```

**Why mark visited on push, not pop?** If you wait until pop, the same node can
be pushed multiple times by different neighbors, wasting time and space. Marking
on push prevents duplicate entries in the stack.

---

## DFS with Path Tracking

```python
def all_paths_dfs(graph: dict[int, list[int]],
                   start: int, end: int) -> list[list[int]]:
    """
    Find ALL paths from start to end (no repeated nodes per path).

    Time:  O(2^V * V) worst case — exponentially many paths, each up to length V
    Space: O(V) for the current path + O(2^V * V) to store all results
    """
    all_paths: list[list[int]] = []

    def dfs(node: int, path: list[int], on_path: set[int]) -> None:
        # 1. Process current node
        path.append(node)
        on_path.add(node)
        
        # 2. Check base case
        if node == end:
            all_paths.append(path[:])  # Copy current path
        else:
            # 3. Explore neighbors
            for neighbor in graph.get(node, []):
                if neighbor not in on_path:  # Check current path, not global visited
                    dfs(neighbor, path, on_path)
        
        # 4. Backtrack before returning to parent
        on_path.remove(node)
        path.pop()

    dfs(start, [], set())
    return all_paths


# Usage
graph = {0: [1, 2], 1: [0, 3], 2: [0, 3], 3: [1, 2]}
print(all_paths_dfs(graph, 0, 3))  # [[0, 1, 3], [0, 2, 3]]
```

**Key detail**: We use an `on_path` set for O(1) membership checks. Using
`neighbor not in path` (a list) is O(V) per check — fine for small graphs but
a hidden cost in interviews. Mention this trade-off.

---

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
  - Maximum edges ≈ `4 × Rows × Cols` (each cell has at most 4 neighbors)

### Key Differences from Standard Graphs:
1. **No need to build an adjacency list**: Building one takes $O(R \times C)$ extra space. You compute neighbors on the fly.
2. **Boundary Checks**: You must explicitly check if `row` and `col` are within bounds `(0 <= r < R)` and `(0 <= c < C)`.
3. **Space Complexity**: The recursion stack space is bounded by the grid size, which is $O(R \times C)$ worst-case (e.g., a grid shaped like a single winding snake path).
4. **BFS vs DFS Space Nuance on Grids**:
   - A DFS on a grid can have a recursion stack of $O(R \times C)$ if it winds through every cell like a snake.
   - A BFS on an open grid explores in a diamond "wavefront". The maximum wavefront size (the queue) is proportional to the diagonal, meaning BFS max space is often $O(min(R, C))$ or $O(R + C)$. So for empty grids, BFS can be much more space-efficient than DFS!

---

## Grid DFS Template

```python
def grid_dfs(grid: list[list[int]],
             start: tuple[int, int]) -> set[tuple[int, int]]:
    """
    DFS on a 2D grid. Explores all connected cells with value 1.

    Time:  O(rows × cols)
    Space: O(rows × cols) for visited set + recursion stack
    """
    rows, cols = len(grid), len(grid[0])
    # 4-directional movement: right, left, down, up
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    visited: set[tuple[int, int]] = set()

    def dfs(r: int, c: int) -> None:
        # Base cases: out of bounds, already visited, or not target value
        if (r < 0 or r >= rows or c < 0 or c >= cols
                or (r, c) in visited or grid[r][c] != 1):
            return

        visited.add((r, c))

        for dr, dc in directions:
            dfs(r + dr, c + dc)

    dfs(start[0], start[1])
    return visited


# Iterative version (avoids stack overflow on large grids)
def grid_dfs_iterative(grid: list[list[int]],
                        start: tuple[int, int]) -> set[tuple[int, int]]:
    """Iterative grid DFS — safe for grids up to any size."""
    rows, cols = len(grid), len(grid[0])
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    visited: set[tuple[int, int]] = {start}
    stack: list[tuple[int, int]] = [start]

    while stack:
        r, c = stack.pop()

        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if (0 <= nr < rows and 0 <= nc < cols
                    and (nr, nc) not in visited and grid[nr][nc] == 1):
                visited.add((nr, nc))
                stack.append((nr, nc))

    return visited
```

---

## DFS for Connected Components

```python
from collections import defaultdict


def count_components(n: int, edges: list[list[int]]) -> int:
    """
    Count connected components in undirected graph.

    Time:  O(V + E)
    Space: O(V + E) for adjacency list + visited set
    """
    # Build adjacency list
    graph: dict[int, list[int]] = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)

    visited: set[int] = set()
    count = 0

    def dfs(node: int) -> None:
        visited.add(node)
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                dfs(neighbor)

    # Must try every node — some may be in disconnected components
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

Understanding **when** you process a node relative to its children is critical
for many graph algorithms.

- **Pre-order**: Process the node **before** visiting its children.
  Use when you need top-down information (e.g., copying a graph, recording
  discovery order).

- **Post-order**: Process the node **after** all descendants are finished.
  Use when you need bottom-up information (e.g., topological sort via reverse
  post-order, computing subtree sizes, strongly connected components).

```python
def dfs_with_order(graph: dict[int, list[int]], start: int) -> tuple[list[int], list[int]]:
    """
    DFS showing pre-order and post-order traversal.

    Pre-order:  recorded when first visiting node (top-down)
    Post-order: recorded when finished with all descendants (bottom-up)
    """
    visited: set[int] = set()
    pre_order: list[int] = []
    post_order: list[int] = []

    def dfs(node: int) -> None:
        visited.add(node)
        pre_order.append(node)          # PRE: before visiting children

        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                dfs(neighbor)

        post_order.append(node)         # POST: after all children done

    dfs(start)
    return pre_order, post_order


# Usage (directed graph — no back-edges to parent)
graph = {0: [1, 2], 1: [3], 2: [], 3: []}
pre, post = dfs_with_order(graph, 0)
print(f"Pre-order:  {pre}")   # [0, 1, 3, 2]
print(f"Post-order: {post}")  # [3, 1, 2, 0]
```

**Post-order is important for:**

- **Topological sort**: Reverse post-order gives a valid topological ordering
- **Strongly connected components** (Kosaraju's / Tarjan's algorithms)
- **Dependency resolution**: Process dependencies before dependents

---

## DFS with Entry/Exit Times

```python
def dfs_timestamps(graph: dict[int, list[int]], start: int) -> tuple[dict[int, int], dict[int, int]]:
    """
    Track when each node is entered and exited during DFS.

    Useful for:
    - Determining ancestor/descendant relationships in O(1)
      (u is ancestor of v iff entry[u] < entry[v] < exit[v] < exit[u])
    - Classifying edges (tree, back, forward, cross)
    """
    visited: set[int] = set()
    entry: dict[int, int] = {}
    exit_time: dict[int, int] = {}
    timer = 0

    def dfs(node: int) -> None:
        nonlocal timer                  # Python 3: cleaner than list hack
        visited.add(node)
        entry[node] = timer
        timer += 1

        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                dfs(neighbor)

        exit_time[node] = timer
        timer += 1

    dfs(start)
    return entry, exit_time
```

---

## Recursive vs Iterative Comparison

| Aspect              | Recursive              | Iterative                    |
| ------------------- | ---------------------- | ---------------------------- |
| Code simplicity     | Cleaner, less code     | More verbose                 |
| Stack overflow risk | Yes (deep graphs)      | No                           |
| Traversal order     | Natural left-to-right  | Reversed unless you reverse  |
| Memory control      | Implicit (call stack)  | Explicit (you control size)  |
| Pre/post-order      | Trivial to implement   | Post-order is tricky         |
| When to use         | Default choice         | Deep graphs, Python limits   |

**Python recursion limit**: ~1000 by default. Use iterative for deep graphs.

```python
import sys
sys.setrecursionlimit(10000)  # Use with caution — can cause segfault if too high
```

**Recursion Limit Warning**: Even with `sys.setrecursionlimit()`, your program is ultimately limited by the operating system's physical stack size limit for the process. If you increase the limit too much and hit a very deep recursion (like a snake path filling a 1000x1000 grid), your program will crash with a segmentation fault instead of a clean Python `RecursionError`.

**When iterative post-order matters**: Implementing post-order iteratively requires a two-stack approach or tracking "last visited child." In interviews, mention this complexity if asked to convert recursive post-order to iterative.

### Iterative Post-order DFS (Two-Stack Method)
This approach is particularly useful for iterative topological sort. We do a standard DFS but push nodes to a second stack instead of printing them, essentially giving us reversed post-order.

```python
def dfs_iterative_post_order(graph: dict[int, list[int]], start: int) -> list[int]:
    """
    Iterative post-order DFS using two stacks.

    Time:  O(V + E)
    Space: O(V)
    """
    stack = [start]
    out_stack = []
    visited = {start}

    while stack:
        node = stack.pop()
        out_stack.append(node)

        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                visited.add(neighbor)
                stack.append(neighbor)

    # out_stack now contains REVERSED post-order
    # Reverse it to get actual post-order
    return out_stack[::-1]
```

---

## Common Mistakes

```python
# ❌ WRONG: Modifying collection while iterating
def dfs_bad_modify(node, graph, visited):
    for neighbor in graph.get(node, []):         # graph[node] may be modified below
        if neighbor not in visited:
            dfs_bad_modify(neighbor, graph, visited)
            graph[node].remove(neighbor) # DON'T modify during iteration!

# ✅ CORRECT: Make decisions, don't modify the graph structure


# ❌ WRONG: Not handling disconnected graphs
def process_graph_bad(graph):
    dfs(0)  # Only processes the component containing node 0!

# ✅ CORRECT: Iterate over all nodes
# for node in range(n):
#     if node not in visited:
#         dfs(node)


# ❌ WRONG: Using global visited for path-finding / backtracking
def dfs_bad_visited(node, end, graph, visited, results):
    visited.add(node)               # Permanent mark — blocks revisiting on other paths!
    if node == end:
        results.append(path)
    for neighbor in graph.get(node, []):
        if neighbor not in visited:
            dfs_bad_visited(neighbor, end, graph, visited, results)

# ✅ CORRECT: Use per-path tracking and backtrack correctly
def dfs_good_path(node, end, path, on_path, graph, results):
    path.append(node)
    on_path.add(node)
    
    if node == end:
        results.append(path[:])
    else:
        for neighbor in graph.get(node, []):
            if neighbor not in on_path:  # Check current path, not global visited
                dfs_good_path(neighbor, end, path, on_path, graph, results)
                
    on_path.remove(node)    # Backtrack
    path.pop()              # Backtrack
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

**Stack state at each step (iterative with reversed neighbors):**

```
Step 0: Pop 0, mark visited        Stack: []           → Visit 0
        Push reversed nbrs [2,1]   Stack: [2, 1]         (push 2 then 1)
Step 1: Pop 1, mark visited        Stack: [2]          → Visit 1
        Push reversed nbrs [4,3]   Stack: [2, 4, 3]      (skip 0: visited)
Step 2: Pop 3, mark visited        Stack: [2, 4]       → Visit 3
        No unvisited nbrs          Stack: [2, 4]          (skip 1: visited)
Step 3: Pop 4, mark visited        Stack: [2]          → Visit 4
        No unvisited nbrs          Stack: [2]             (skip 1: visited)
Step 4: Pop 2, mark visited        Stack: []           → Visit 2
        Push reversed nbrs [5]     Stack: [5]             (skip 0: visited)
Step 5: Pop 5, mark visited        Stack: []           → Visit 5
        No unvisited nbrs          Stack: []              (skip 2: visited)

ORDER: [0, 1, 3, 4, 2, 5]  ← matches recursive!
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
- DFS space depends on graph DEPTH (longest path from root)
- BFS space depends on graph WIDTH (max nodes at any level)
- For deep narrow graphs: DFS uses more space
- For wide shallow graphs: BFS uses more space
```

### Recursion Stack Space Limits

This is a critical interview topic. When do you hit a **RecursionError**?

| Language   | Default Stack Limit                                   | Risk of Stack Overflow                                                                                         |
| ---------- | ----------------------------------------------------- | -------------------------------------------------------------------------------------------------------------- |
| **Python** | `sys.getrecursionlimit()` (~1000 by default)          | **HIGH**. A 30×40 grid = 1200 cells. A snake path hits the limit. Use `sys.setrecursionlimit()` or iterative. |

**Interview Advice**:
- If writing **Python** and solving a 2D Grid problem (e.g., $M, N \le 200$), strongly consider using the iterative stack approach, or explicitly state: *"I'm using recursive DFS, but in Python I would need to increase `sys.setrecursionlimit(40000)` to handle worst-case deep paths."*

---

## Edge Cases

```python
# 1. Single node
graph = {0: []}
# dfs(graph, 0) → [0]

# 2. No edges (disconnected singletons)
graph = {0: [], 1: [], 2: []}
# Must iterate all nodes to find 3 components

# 3. Cycle
graph = {0: [1], 1: [2], 2: [0]}
# Visited set prevents infinite loop

# 4. Self-loop
graph = {0: [0, 1], 1: []}
# Visited check skips the self-loop

# 5. Dense graph (complete graph)
# Still O(V + E), but E = V*(V-1)/2 so O(V^2)

# 6. Adjacency Matrix
# If the graph is given as a 2D V x V matrix (matrix[u][v] = 1 if edge exists),
# Time complexity of DFS is strictly O(V^2), even if there are very few edges!
# We must check matrix[node][v] for ALL v in 0..V-1 to find neighbors.

# 7. Empty graph (no nodes)
# Handle n=0 edge case before starting DFS
```

---

## Interview Tips

1. **Default to recursive**: Cleaner code, easier to write correctly
2. **Know iterative version**: For when recursion limit is a concern
3. **Understand pre/post-order**: Critical for topological sort, SCC
4. **Handle disconnected graphs**: Iterate over all nodes
5. **Draw the traversal**: Show stack state if asked
6. **State complexities proactively**: Don't wait to be asked — say "this is O(V+E) time, O(V) space"
7. **Mention the recursion limit**: In Python interviews, always acknowledge it for large inputs

---

## Practice Problems (Progressive Difficulty)

| #   | Problem                                | Difficulty | Key Pattern                    | Hint                                              |
| --- | -------------------------------------- | ---------- | ------------------------------ | ------------------------------------------------- |
| 1   | LC 733 — Flood Fill                    | Easy       | Basic grid DFS                 | DFS from starting pixel, change color recursively  |
| 2   | LC 200 — Number of Islands             | Medium     | Component counting on grid     | DFS from each unvisited `'1'`; mark visited        |
| 3   | LC 785 — Is Graph Bipartite?           | Medium     | Bipartite graph, 2 colors      | Use DFS to color nodes 0/1. If neighbor has same color, false. |
| 4   | LC 133 — Clone Graph                   | Medium     | DFS with hash map mapping      | Map old→new node; DFS to clone neighbors           |
| 5   | LC 417 — Pacific Atlantic Water Flow   | Medium     | Reverse DFS from edges         | Start DFS from both oceans, find cells reachable by both |
| 6   | LC 79 — Word Search                    | Medium     | DFS + Backtracking on grid     | Use `on_path` set or temporarily modify grid to track visited cells |
| 7   | LC 329 — Longest Increasing Path...    | Hard       | DFS + Memoization on grid      | Return max path length from a cell, cache the result! |
| 8   | LC 1192 — Critical Connections...      | Hard       | Tarjan's bridge-finding algo   | Track discovery time vs lowest discovery time reachable |

**Suggested progression**: 733 → 200 → 785 → 133 → 417 → 329 → 1192

---

## Key Takeaways

1. **DFS uses stack/recursion**: Go deep, then backtrack
2. **O(V + E) time, O(V) space**: Visit each vertex and edge once
3. **Recursive is cleaner**: But watch for stack overflow in Python (limit ~1000)
4. **Pre-order vs post-order**: Pre for top-down, post for bottom-up (topo sort, SCC)
5. **Global visited vs path visited**: Different tools for cycle detection vs path finding
6. **Iterative DFS with `reversed()`**: Matches recursive order; mark visited on push

---

## Next: [04-connected-components.md](./04-connected-components.md)

Learn to count and find connected components.

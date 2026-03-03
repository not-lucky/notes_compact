# Cycle Detection in Directed Graphs

> **Prerequisites:** [03-dfs-basics](./03-dfs-basics.md)

## Building Intuition

**The Deadlock Detection Mental Model**: In a directed graph, a cycle means "A waits for B waits for C waits for A" — classic deadlock!

```text
Deadlock Example (Process Dependencies):
Process A → waits for B → waits for C
    ↑                               ↓
    └──────── waits for ───────── Process D
```

**Why a simple "visited" set isn't enough for directed graphs**:

```text
This is NOT a cycle:            This IS a cycle:
    0 → 1                           0 → 1
    ↓   ↓                           ↓   ↓
    2 → 3                           2 ← 3

Path 0→2→3 and 0→1→3          0→1→3→2→0 is a cycle
share node 3 - that's fine!    (can walk forever)
```

In the left graph, revisiting node 3 is just "two roads lead to same place." A simple `visited` set would flag node 3 as already visited and incorrectly report a cycle. In the right graph, revisiting node 0 **while it's still on our current DFS path** means we've found a true back edge — a loop we can walk forever.

**The Three-Color Insight (White / Gray / Black)**:

We need to distinguish between "visited in some earlier path" and "visited **on the path we're currently walking**." Three colors give us exactly that:

- **WHITE (unvisited)**: Haven't touched this node yet.
- **GRAY (in progress)**: Currently on the recursion stack — we started exploring this node but haven't finished its subtree yet.
- **BLACK (done)**: Completely finished — this node and all its descendants are fully explored and guaranteed cycle-free.

**Why this works**: During DFS, all GRAY nodes form a chain from the DFS root down to the current node. If we ever encounter a neighbor that is already GRAY, that neighbor is an ancestor on our current path — meaning we've found a **back edge**, which is the definition of a cycle in a directed graph. BLACK nodes are safe to skip because their entire subtree is already proven cycle-free.

```text
DFS State Visualization (graph: 0→1→2→0):

Step 1:        Step 2:        Step 3:        Step 4:
[G]→[W]        [G]→[G]        [G]→[G]        CYCLE!
 ↓   ↓          ↓   ↓          ↓   ↓
[W]←[W]        [W]←[W]        [G]←[W]        Gray→Gray

G=Gray, W=White
When we try to go from node 2 to node 0, node 0 is GRAY = still on current path!
```

**Back edges vs cross edges**: In a DFS tree, a back edge points from a descendant back to an ancestor (GRAY → GRAY = cycle). A cross edge points to a node in a different, already-completed subtree (current → BLACK = no cycle). This distinction is why three colors work but two don't.

---

## Difference from Undirected Cycle Detection

This is a critical interview distinction:

| Aspect           | Directed Graph                   | Undirected Graph                   |
| ---------------- | -------------------------------- | ---------------------------------- |
| **Algorithm**    | Three-color DFS or Kahn's        | Simple DFS with parent tracking    |
| **Key check**    | Back edge to GRAY ancestor       | Visited neighbor that isn't parent |
| **Why different** | Cross edges are not cycles       | Any revisit (except parent) = cycle |
| **Reconvergence** | Allowed (two paths to same node) | Also allowed if via different parents |

In undirected graphs, every edge is bidirectional, so "visited and not my parent" is sufficient to detect a cycle. In directed graphs, reaching an already-visited node might just be a cross edge — you must verify the node is on your **current path** (GRAY).

---

## When to Use Each Approach

**Three-color DFS is ideal when:**
- You need to detect cycles in a directed graph (the standard approach).
- You want to find the actual cycle path (augment with parent tracking).
- You need it as part of topological sort via DFS.

**Kahn's algorithm (BFS) is better when:**
- You also need topological order if no cycle exists.
- You prefer iterative BFS over recursive DFS.
- The problem is framed as "can we process all nodes?"

---

## Three-Color (State) Algorithm

Track three states for each node:
- **WHITE (0)**: Unvisited
- **GRAY (1)**: Currently being processed (on the recursion stack)
- **BLACK (2)**: Completely processed (all descendants explored)

**Cycle exists if and only if we encounter a GRAY node during DFS** (a back edge).

```python
from collections import defaultdict

def has_cycle_directed(n: int, edges: list[list[int]]) -> bool:
    \"\"\"
    Detect cycle in directed graph using three-color DFS.

    Args:
        n: Number of nodes (labeled 0 to n-1).
        edges: List of [u, v] pairs representing directed edge u → v.

    Returns:
        True if the graph contains a cycle.

    Time:  O(V + E) — each node and edge visited once.
    Space: O(V + E) — adjacency list + color array + recursion stack.
    \"\"\"
    WHITE, GRAY, BLACK = 0, 1, 2

    # Build adjacency list
    graph: dict[int, list[int]] = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)

    color = [WHITE] * n

    def dfs(node: int) -> bool:
        color[node] = GRAY  # Mark: currently on recursion stack

        for neighbor in graph[node]:
            if color[neighbor] == GRAY:
                return True  # Back edge found → cycle!
            if color[neighbor] == WHITE:
                if dfs(neighbor):
                    return True
            # BLACK neighbors are safe — already fully explored

        color[node] = BLACK  # Mark: done with this subtree
        return False

    # Must check all nodes — graph may be disconnected
    for node in range(n):
        if color[node] == WHITE:
            if dfs(node):
                return True

    return False

# Usage
edges = [[0, 1], [1, 2], [2, 0]]  # Cycle: 0 → 1 → 2 → 0
print(has_cycle_directed(3, edges))  # True

edges = [[0, 1], [1, 2]]  # No cycle
print(has_cycle_directed(3, edges))  # False
```

---

## Course Schedule I (Can Finish?)

```python
from collections import defaultdict

def can_finish(num_courses: int, prerequisites: list[list[int]]) -> bool:
    \"\"\"
    LeetCode 207: Can all courses be finished? (No cycle in dependency graph)

    prerequisites[i] = [a, b] means "to take course a, you must first
    take course b" → directed edge b → a.

    Time:  O(V + E)
    Space: O(V + E) for the adjacency list
    \"\"\"
    WHITE, GRAY, BLACK = 0, 1, 2

    # Build dependency graph: prereq → course
    graph: dict[int, list[int]] = defaultdict(list)
    for course, prereq in prerequisites:
        graph[prereq].append(course)

    color = [WHITE] * num_courses

    def has_cycle(node: int) -> bool:
        color[node] = GRAY

        for next_course in graph[node]:
            if color[next_course] == GRAY:
                return True  # Circular dependency
            if color[next_course] == WHITE:
                if has_cycle(next_course):
                    return True

        color[node] = BLACK
        return False

    # Check every course — some may have no prerequisites
    for course in range(num_courses):
        if color[course] == WHITE:
            if has_cycle(course):
                return False  # Cycle found → can't finish

    return True  # No cycles → all courses completable
```

---

## Finding the Cycle (Not Just Detecting)

Sometimes you need to return the nodes involved in the cycle.

```python
from collections import defaultdict

def find_cycle(n: int, edges: list[list[int]]) -> list[int]:
    \"\"\"
    Find and return the nodes forming a cycle, if one exists.
    Returns the cycle as a list of nodes in order, or [] if no cycle.

    Time:  O(V + E)
    Space: O(V + E)
    \"\"\"
    WHITE, GRAY, BLACK = 0, 1, 2

    graph: dict[int, list[int]] = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)

    color = [WHITE] * n
    parent = [-1] * n
    cycle_start = -1
    cycle_end = -1

    def dfs(node: int) -> bool:
        nonlocal cycle_start, cycle_end
        color[node] = GRAY

        for neighbor in graph[node]:
            if color[neighbor] == GRAY:
                # Back edge found: neighbor is ancestor of node
                cycle_start = neighbor  # The ancestor we looped back to
                cycle_end = node        # The node that completed the loop
                return True
            if color[neighbor] == WHITE:
                parent[neighbor] = node
                if dfs(neighbor):
                    return True

        color[node] = BLACK
        return False

    for node in range(n):
        if color[node] == WHITE:
            if dfs(node):
                break

    if cycle_start == -1:
        return []

    # Reconstruct cycle by following parent pointers from cycle_end to cycle_start
    cycle = []
    current = cycle_end
    while current != cycle_start:
        cycle.append(current)
        current = parent[current]
    cycle.append(cycle_start)
    cycle.reverse()

    return cycle
```

---

## BFS Approach: Kahn's Algorithm

Detect cycle by checking if topological sort can process all nodes.

**Intuition**: Kahn's algorithm repeatedly removes nodes with in-degree 0 (no dependencies). If there's a cycle, the nodes in the cycle always have at least one incoming edge from another cycle node — their in-degree never reaches 0. So they're never processed, and `processed < n`.

```python
from collections import defaultdict, deque

def has_cycle_kahn(n: int, edges: list[list[int]]) -> bool:
    \"\"\"
    Detect cycle using Kahn's algorithm (BFS-based topological sort).

    Time:  O(V + E)
    Space: O(V + E) for adjacency list + in-degree array + queue
    \"\"\"
    graph: dict[int, list[int]] = defaultdict(list)
    in_degree = [0] * n

    for u, v in edges:
        graph[u].append(v)
        in_degree[v] += 1

    # Seed queue with all nodes that have no incoming edges
    queue = deque(node for node in range(n) if in_degree[node] == 0)
    processed = 0

    while queue:
        node = queue.popleft()
        processed += 1

        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    # If we couldn't process all nodes, remaining nodes form cycle(s)
    return processed != n
```

---

## Common Mistakes (Crucial for Interviews)

### 1. Using a simple `visited` set (Fails on Cross Edges)

A single `visited` set cannot distinguish between a "back edge" (cycle) and a "cross edge" (revisiting a node from a different path).

```python
# ❌ WRONG: Fails on cross edges (e.g., Diamond shape graph)
# Fails on this graph: 0 → 1, 0 → 2, 1 → 3, 2 → 3
# It will visit 3 twice and incorrectly report a cycle!
visited: set[int] = set()

def dfs(node: int) -> bool:
    if node in visited:
        return True  # WRONG! This might just be a cross edge
    visited.add(node)
    for neighbor in graph[node]:
        if dfs(neighbor):
            return True
    return False
```

### 2. Backtracking the `visited` set (Correct but TLE)

A common patch to the above mistake is to remove the node from the `visited` set after exploring its neighbors (backtracking). This correctly finds cycles, but **destroys the time complexity**.

```python
# ❌ WRONG: Correct logic, but O(2^V) time complexity!
# Fails on Complete DAG (dense edges, no cycle): 0 → 1, 0 → 2, 1 → 2 ...
path: set[int] = set()

def dfs(node: int) -> bool:
    if node in path:
        return True
    path.add(node)
    for neighbor in graph[node]:
        if dfs(neighbor):
            return True
    path.remove(node)  # Backtrack
    return False
```
By not remembering nodes that we've already proven to be cycle-free (the `BLACK` state in 3-color), a dense DAG will force the DFS to explore an exponential number of paths, resulting in Time Limit Exceeded (TLE).

### 3. ✅ The Correct Alternative: Explicit Recursion Stack Set

If you prefer Python sets over a `color` array, you must use **two** sets: one for fully processed nodes (`visited`), and one for the current path (`rec_stack`).

```python
# ✅ CORRECT: Track both path and fully explored nodes
visited: set[int] = set()    # Equivalent to BLACK (fully explored)
rec_stack: set[int] = set()  # Equivalent to GRAY (on current path)

def dfs(node: int) -> bool:
    visited.add(node)
    rec_stack.add(node)

    for neighbor in graph[node]:
        if neighbor in rec_stack:  # Back edge found
            return True
        if neighbor not in visited:
            if dfs(neighbor):
                return True

    rec_stack.remove(node)  # Leave current path
    return False
```

---

## Edge Cases to Consider

When solving cycle detection problems, always test these edge cases:

1. **Self-loops**: `0 → 0`. The smallest possible cycle. Handled naturally by both DFS and Kahn's.
2. **Disconnected graphs**: A cycle might exist in a component not reachable from node 0. Always loop through all nodes in the main function to start the search.
3. **Cross edges (Diamond shape)**: `0 → 1`, `0 → 2`, `1 → 3`, `2 → 3`. Multiple paths to the same node without a cycle. Tests if you falsely trigger on `visited`.
4. **Complete DAG**: A graph where every node $i$ points to every node $j > i$. No cycles, but $O(E)$ paths. Tests if your algorithm runs in exponential time (TLE) due to missing memoization of `BLACK` nodes.
5. **Two-node mutual cycle**: `0 → 1` and `1 → 0`. Smallest cycle involving multiple nodes.

---

## Practice Problems

| #   | Problem                                | LC # | Difficulty | Hint                                                        |
| --- | -------------------------------------- | ---- | ---------- | ----------------------------------------------------------- |
| 1   | Course Schedule                        | 207  | Medium     | Direct application: build graph from prereqs, detect cycle  |
| 2   | Course Schedule II                     | 210  | Medium     | Return topo order if no cycle; Kahn's gives order naturally  |
| 3   | Find Eventual Safe States              | 802  | Medium     | Safe nodes = not part of any cycle; BLACK nodes are safe     |
| 4   | Longest Cycle in a Graph               | 2360 | Hard       | Directed graph where each node has at most one outgoing edge |
| 5   | Redundant Connection II                | 685  | Hard       | Find the edge causing a cycle in a directed graph (rooted tree) |

**Progression strategy:**
- Start with **#1 (Course Schedule)** — the canonical cycle detection problem.
- Then **#2 (Course Schedule II)** — extends #1 with topological ordering.
- Then **#3 (Safe States)** — deepens understanding of what the BLACK state actually represents.
- Then **#4 (Longest Cycle)** — applies the concept and requires calculating cycle length.
- Finally **#5 (Redundant Connection II)** — advanced, combines cycle detection with Union-Find concepts.

---

## Key Takeaways

1. **Three states**: WHITE → GRAY → BLACK tracks DFS progress.
2. **GRAY = on current path**: A back edge to a GRAY node = cycle.
3. **Different from undirected**: Can't use simple visited check — cross edges are not cycles.
4. **Kahn's alternative**: Cycle exists if topological sort can't process all nodes.
5. **Always check all components**: Graph may be disconnected.
6. **Back edge intuition**: GRAY nodes form a path from root to current node; seeing GRAY means we've looped back to an ancestor.

---

## Next: [06-cycle-detection-undirected.md](./06-cycle-detection-undirected.md)

Learn cycle detection for undirected graphs — a simpler problem requiring only parent tracking.

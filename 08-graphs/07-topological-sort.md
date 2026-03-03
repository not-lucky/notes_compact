# Topological Sort

> **Prerequisites:** [05-cycle-detection-directed](./05-cycle-detection-directed.md)

## Building Intuition

**The Dependency Resolution Mental Model**: Think of getting dressed in the morning:

- Underwear before pants
- Socks before shoes
- Shirt before jacket

You need a valid order that respects all dependencies. Topological sort finds this order!

```
Dependencies:          Valid Orders:
underwear → pants      [underwear, socks, pants, shirt, shoes, jacket]
socks → shoes          [socks, underwear, shirt, pants, shoes, jacket]
shirt → jacket         (many valid orders exist if graph isn't a chain)
```

**Why it's called "topological"**:
The ordering respects the "topology" (structure) of dependencies. If A must come before B, A appears earlier in the sorted result.

**Key insight — Two equivalent approaches**:

1. **Kahn's (BFS) — "Peel off the ready layer"**:
   - Find nodes with no dependencies (in-degree 0) — these are "ready"
   - Process them, remove their outgoing edges (simulate completing that task)
   - New nodes may now have in-degree 0 — add them to the queue
   - Repeat until the queue is empty
   - **Intuition**: Like a task board — grab everything with no blockers, finish it, then see what's unblocked next

2. **DFS — "Finish the deepest dependency first"**:
   - Explore deeply along dependency chains
   - Add each node to the result only *after* all its descendants are fully processed (post-order)
   - Reverse the result at the end
   - **Intuition**: "Before I can record myself as done, all my dependencies must already be recorded"

**When to prefer each**:
- **Kahn's**: When you need cycle detection for free, lexicographic ordering (swap queue for heap), or level-by-level processing (parallel scheduling)
- **DFS**: When you already have DFS infrastructure in your solution, or when the problem naturally fits recursive exploration

**Visual proof — Why DFS post-order works**:

```
If A → B (A must come before B), there are two cases:
1. We start DFS at A (or an ancestor of A):
   - DFS from A will visit B
   - B finishes BEFORE A (post-order: deepest nodes finish first)
   - B is added to result BEFORE A
   - Reversing puts A before B ✓

2. We start DFS at B (or an ancestor of B that isn't A):
   - DFS from B visits everything B can reach, then B finishes
   - B is added to result
   - Later, we start DFS at A. A sees B is already finished (BLACK)
   - A finishes and is added to result AFTER B
   - Reversing puts A before B ✓

Graph:      DFS Post-order:    Reversed (topological):
A → B       [B, A]             [A, B] ✓
```

---

## When NOT to Use

**Don't use topological sort when:**

- **Graph has cycles** → No valid ordering exists; detect cycle first
- **Graph is undirected** → Concept doesn't apply (no "direction" of dependency)
- **You need shortest path** → Topological sort is about ordering, not distance (though topo sort *can* help with shortest paths in DAGs — see Dijkstra notes)
- **Order doesn't matter** → Simple traversal is simpler

**Topological sort is overkill when:**

- Graph is a simple chain → Just follow the links
- Only need to detect if ordering exists → Cycle detection is sufficient
- Problem asks for ANY traversal → BFS/DFS is simpler

**Common mistake scenarios:**

- Applying to undirected graphs → Meaningless result
- Forgetting to reverse DFS result → Order is backwards
- Not handling disconnected components → Must process all nodes
- Not checking for cycles → Silent incorrect results

---

## Interview Context

Topological sort is a FANG+ favorite because:

1. **Dependency resolution**: Build systems, package managers, task scheduling
2. **Course ordering**: Classic Course Schedule II problem
3. **Multiple algorithms**: Kahn's (BFS) and DFS approaches
4. **DAG validation**: Topological sort exists iff graph is acyclic

### Amazon Context
Amazon frequently asks variants of topological sort, particularly around **build systems** or **package installations**:
- Given a list of packages and their dependencies, what is the valid installation order?
- What is the lexicographically smallest installation order?
- Find the earliest time all packages can be installed if multiple independent ones can install simultaneously (parallel processing time).

### Real-World Applications

- **Build systems** (Make, Bazel): Compile dependencies before dependents
- **Package managers** (pip, npm): Install dependencies in correct order
- **Spreadsheet cell evaluation**: Calculate cells that others depend on first
- **Task scheduling**: Project management / CI pipeline ordering
- **Course prerequisites**: University course planning
- **Data pipeline orchestration** (Airflow): Execute DAG stages in order

If you see "ordering" or "dependencies", think topological sort.

---

## Core Concept

A **topological ordering** of a directed graph is a linear ordering of vertices such that for every edge u → v, u comes before v.

### Directed Acyclic Graph (DAG) Formalization
A directed graph $G = (V, E)$ is called a Directed Acyclic Graph (DAG) if there exists no path $v_1, v_2, ..., v_k$ such that $v_1 = v_k$.

**Theorem**: A directed graph $G$ has a topological ordering if and only if $G$ is a DAG.
- **Proof (Forward)**: If $G$ has a cycle $v_1 \rightarrow v_2 \rightarrow ... \rightarrow v_k \rightarrow v_1$, in any ordering, $v_1$ must precede $v_2$, which precedes $v_3$, ..., which precedes $v_k$, which must precede $v_1$. This implies $v_1$ precedes $v_1$, a contradiction. Thus, a topological ordering implies no cycles.
- **Proof (Backward)**: Every DAG has at least one node with in-degree 0. Pick it, remove it, and repeat. The remaining graph is still a DAG, so we can always pick a node until the graph is empty, producing a valid topological sort.

```
Dependencies:           Topological Order:
    0 → 1               0, 2, 1, 3
    ↓   ↓               (or 2, 0, 1, 3 - multiple valid orders)
    2 → 3

0 must come before 1
0 must come before 2
1 must come before 3
2 must come before 3
```

**Only possible on DAGs** (Directed Acyclic Graphs). Cycles make topological ordering impossible.

---

## Kahn's Algorithm (BFS)

Process nodes with in-degree 0 first, then reduce neighbors' in-degrees.

### Python
```python
from collections import defaultdict, deque

def topological_sort_kahn(n: int, edges: list[list[int]]) -> list[int]:
    """
    Topological sort using Kahn's algorithm (BFS).

    Args:
        n: Number of nodes (labeled 0 to n-1).
        edges: List of [u, v] meaning u must come before v.

    Returns:
        A valid topological ordering, or [] if a cycle exists.

    Time:  O(V + E)
    Space: O(V + E) for the adjacency list
    """
    # Build adjacency list and compute in-degrees
    graph: dict[int, list[int]] = defaultdict(list)
    in_degree: list[int] = [0] * n

    for u, v in edges:
        graph[u].append(v)
        in_degree[v] += 1

    # Start with all nodes that have no prerequisites
    queue: deque[int] = deque(i for i in range(n) if in_degree[i] == 0)
    result: list[int] = []

    while queue:
        node = queue.popleft()
        result.append(node)

        # "Remove" this node's outgoing edges by decrementing in-degrees
        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    # If not all nodes processed, remaining nodes are part of / blocked by a cycle
    if len(result) != n:
        return []

    return result
```


---

## Visual: Kahn's Algorithm

```
Graph: 0 → 1 → 3
       ↓
       2 -----↗

Initial in-degrees: [0, 1, 1, 2]
                     ^        ^ (3 has 2 incoming edges)
                     |
                   (0 has no incoming)

Step 1: queue = [0], result = []
        Process 0: result = [0]
        Reduce in-degree of 1 and 2
        in-degrees: [0, 0, 0, 2]
        queue = [1, 2]

Step 2: Process 1: result = [0, 1]
        Reduce in-degree of 3
        in-degrees: [0, 0, 0, 1]
        queue = [2]

Step 3: Process 2: result = [0, 1, 2]
        Reduce in-degree of 3
        in-degrees: [0, 0, 0, 0]
        queue = [3]

Step 4: Process 3: result = [0, 1, 2, 3]
        Done!
```

---

## DFS Approach (Reverse Post-Order)

DFS from each unvisited node, add to result after processing all descendants.

```python
from collections import defaultdict

def topological_sort_dfs(n: int, edges: list[list[int]]) -> list[int]:
    """
    Topological sort using DFS (reverse post-order).

    Uses 3-color marking for simultaneous cycle detection:
      - WHITE (0): Not yet visited
      - GRAY  (1): Currently in the DFS recursion stack (ancestor)
      - BLACK (2): Fully processed (all descendants done)

    Encountering a GRAY node means we've found a back edge → cycle.

    Args:
        n: Number of nodes (labeled 0 to n-1).
        edges: List of [u, v] meaning u must come before v.

    Returns:
        A valid topological ordering, or [] if a cycle exists.

    Time:  O(V + E)
    Space: O(V + E) for the adjacency list, O(V) for recursion stack
    """
    WHITE, GRAY, BLACK = 0, 1, 2

    graph: dict[int, list[int]] = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)

    color: list[int] = [WHITE] * n
    result: list[int] = []

    def dfs(node: int) -> bool:
        """Returns True if a cycle is detected, False otherwise."""
        color[node] = GRAY  # Mark as "in progress"

        for neighbor in graph[node]:
            if color[neighbor] == GRAY:
                return True  # Back edge → cycle detected
            if color[neighbor] == WHITE:
                if dfs(neighbor):
                    return True

        color[node] = BLACK  # Mark as fully processed
        result.append(node)  # Post-order: add AFTER all descendants are done
        return False

    # Must try every node as a starting point (handles disconnected components)
    for node in range(n):
        if color[node] == WHITE:
            if dfs(node):
                return []  # Cycle found, topological sort impossible

    return result[::-1]  # Reverse post-order = topological order
```

> **Python recursion limit**: For graphs with V > ~1000, Python's default
> recursion limit (1000) will cause `RecursionError`. Use `sys.setrecursionlimit(n + 10)`
> or convert to an iterative DFS. In interviews, mention this trade-off and
> prefer Kahn's for large inputs.

---

## Why Reverse Post-Order?

```
DFS visits:        Post-order:      Reversed:
    0              [3, 1, 2, 0]     [0, 2, 1, 3]
   / \
  1   2            (add node after  (this is correct
  |   |             visiting all    topological order)
  3   3             descendants)
```

We add a node to the result only after all its descendants are processed. Reversing gives us the correct order where dependencies come first.

**Why not just prepend instead of reverse?** You could use `result.appendleft()` with a `deque` to avoid the final reverse. Both work — reversing a list is O(V) and doesn't affect overall complexity.

---

## All Topological Orderings

```python
from collections import defaultdict

def all_topological_sorts(n: int, edges: list[list[int]]) -> list[list[int]]:
    """
    Find ALL valid topological orderings using backtracking.

    At each step, any node with in-degree 0 can be chosen next.
    We try all such choices and backtrack.

    Args:
        n: Number of nodes (labeled 0 to n-1).
        edges: List of [u, v] meaning u must come before v.

    Returns:
        A list of all valid topological orderings.

    Time:  O(V! * V) in worst case (graph with no edges)
    Space: O(V) for the recursion stack and temporary path
    """
    graph: dict[int, list[int]] = defaultdict(list)
    in_degree: list[int] = [0] * n

    for u, v in edges:
        graph[u].append(v)
        in_degree[v] += 1

    all_orderings: list[list[int]] = []
    current: list[int] = []

    def backtrack() -> None:
        if len(current) == n:
            all_orderings.append(current[:])
            return

        for node in range(n):
            if in_degree[node] == 0:
                # Choose this node
                in_degree[node] = -1  # Mark as processed
                current.append(node)
                
                # Update dependencies
                for neighbor in graph[node]:
                    in_degree[neighbor] -= 1

                backtrack()

                # Undo choice (backtrack)
                for neighbor in graph[node]:
                    in_degree[neighbor] += 1
                    
                current.pop()
                in_degree[node] = 0  # Unmark

    backtrack()
    return all_orderings
```

---

## Comparison: Kahn's vs DFS

| Aspect              | Kahn's (BFS)                  | DFS                           |
| ------------------- | ----------------------------- | ----------------------------- |
| Approach            | In-degree counting            | Reverse post-order            |
| Cycle detection     | Check if all nodes processed  | Use three colors (back edge)  |
| Implementation      | More intuitive                | Slightly shorter              |
| Lexicographic order | Use min-heap instead of queue | Harder to achieve             |
| All orderings       | Natural with backtracking     | Possible but tricky           |
| Stack overflow risk | None (iterative)              | Yes for deep graphs in Python |
| Best for            | Most interview problems       | When DFS already in solution  |

---

## Lexicographically Smallest Order

Use priority queue (min-heap) instead of regular queue:

```python
import heapq
from collections import defaultdict

def topological_sort_lex(n: int, edges: list[list[int]]) -> list[int]:
    """
    Topological sort producing the lexicographically smallest valid order.

    Replaces the FIFO queue with a min-heap so we always pick the
    smallest-numbered available node.

    Args:
        n: Number of nodes (labeled 0 to n-1).
        edges: List of [u, v] meaning u must come before v.

    Returns:
        The lexicographically smallest valid topological order, or [] if a cycle.

    Time:  O((V + E) log V)  — heap operations add log V factor
    Space: O(V + E)
    """
    graph: dict[int, list[int]] = defaultdict(list)
    in_degree: list[int] = [0] * n

    for u, v in edges:
        graph[u].append(v)
        in_degree[v] += 1

    # Use min-heap instead of queue
    heap: list[int] = [i for i in range(n) if in_degree[i] == 0]
    heapq.heapify(heap)
    result: list[int] = []

    while heap:
        node = heapq.heappop(heap)  # Always pick smallest available
        result.append(node)

        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                heapq.heappush(heap, neighbor)

    return result if len(result) == n else []
```

---

## Common Interview Variants

### 1. Check if Topological Sort is Unique

A topological order is unique if and only if at every step, exactly one node has in-degree 0 (i.e., the queue never has more than one element). This also means the topological order forms a **Hamiltonian path** in the DAG.

```python
from collections import defaultdict, deque

def is_unique_topological_sort(n: int, edges: list[list[int]]) -> bool:
    """
    Returns True if exactly one valid topological ordering exists.

    This happens when the queue size is always exactly 1 throughout
    Kahn's algorithm — there's never a "choice" of which node to pick next.

    Args:
        n: Number of nodes (labeled 0 to n-1).
        edges: List of [u, v] meaning u must come before v.

    Returns:
        True if exactly one valid topological order exists, False otherwise.

    Time:  O(V + E)
    Space: O(V + E)
    """
    graph: dict[int, list[int]] = defaultdict(list)
    in_degree: list[int] = [0] * n

    for u, v in edges:
        graph[u].append(v)
        in_degree[v] += 1

    queue: deque[int] = deque(i for i in range(n) if in_degree[i] == 0)
    processed = 0

    while queue:
        if len(queue) != 1:
            return False  # Multiple choices → not unique

        node = queue.popleft()
        processed += 1

        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    # Also verify no cycle (all nodes were processed)
    return processed == n
```

### 2. Parallel Processing Time (Minimum Semesters / Levels)

Find the minimum time to complete all tasks if independent tasks can run in parallel. This is essentially **BFS level counting** on the DAG.

```python
from collections import defaultdict, deque

def parallel_courses(n: int, relations: list[list[int]]) -> int:
    """
    Minimum number of semesters (parallel rounds) to complete all courses.

    Each semester, take ALL currently available courses (in-degree 0).
    This is a level-order BFS on the dependency DAG.

    Args:
        n: Number of courses (labeled 1 to n, 1-indexed).
        relations: List of [prereq, course] (1-indexed).

    Returns:
        Minimum semesters, or -1 if impossible (cycle exists).

    Time:  O(V + E)
    Space: O(V + E)
    """
    graph: dict[int, list[int]] = defaultdict(list)
    in_degree: list[int] = [0] * n

    for prereq, course in relations:
        graph[prereq - 1].append(course - 1)  # Convert to 0-indexed
        in_degree[course - 1] += 1

    queue: deque[int] = deque(i for i in range(n) if in_degree[i] == 0)
    semesters = 0
    completed = 0

    while queue:
        semesters += 1
        # Process ALL nodes at this level (one semester of parallel work)
        for _ in range(len(queue)):
            node = queue.popleft()
            completed += 1

            for neighbor in graph[node]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

    return semesters if completed == n else -1
```

### 3. DP on DAG (Longest Path)

Topological sort is frequently used as a precursor to Dynamic Programming on Directed Acyclic Graphs. If we process nodes in topological order, we guarantee that when we calculate the DP state for a node, all its dependencies have already been calculated.

```python
from collections import defaultdict, deque

def longest_path_in_dag(n: int, edges: list[list[int]]) -> int:
    """
    Finds the length of the longest path in a DAG.
    
    Args:
        n: Number of nodes.
        edges: List of [u, v] meaning directed edge from u to v.
        
    Returns:
        The length of the longest path (number of edges).
    """
    graph: dict[int, list[int]] = defaultdict(list)
    in_degree: list[int] = [0] * n
    
    for u, v in edges:
        graph[u].append(v)
        in_degree[v] += 1
        
    # Standard Kahn's Algorithm
    queue: deque[int] = deque(i for i in range(n) if in_degree[i] == 0)
    topo_order: list[int] = []
    
    while queue:
        node = queue.popleft()
        topo_order.append(node)
        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
                
    # If cycle exists, longest path is undefined (infinite)
    if len(topo_order) != n:
        return -1 
        
    # DP to find longest path
    # dp[i] = length of longest path ending at node i
    dp: list[int] = [0] * n
    
    # Process nodes in topological order
    for u in topo_order:
        for v in graph[u]:
            dp[v] = max(dp[v], dp[u] + 1)
            
    return max(dp) if dp else 0
```

---

## Step-by-Step Topological Sort Traces

**DAG for demonstration:**

```
    0 → 1 → 3
    ↓   ↓
    2 → 4
```

Edges: `[(0,1), (0,2), (1,3), (1,4), (2,4)]`

### Kahn's Algorithm (BFS) Trace:

```
INITIAL STATE:
In-degrees: {0: 0, 1: 1, 2: 1, 3: 1, 4: 2}
Queue: [0]  (only node with in-degree 0)
Result: []

╔══════════════════════════════════════════════════════════════════╗
║ ITERATION 1: Dequeue node 0                                      ║
╚══════════════════════════════════════════════════════════════════╝
  Add 0 to result: [0]

  Decrement in-degrees of 0's neighbors:
    1: 1 → 0  ← Now 0, add to queue!
    2: 1 → 0  ← Now 0, add to queue!

  In-degrees: {0: -, 1: 0, 2: 0, 3: 1, 4: 2}
  Queue: [1, 2]

╔══════════════════════════════════════════════════════════════════╗
║ ITERATION 2: Dequeue node 1                                      ║
╚══════════════════════════════════════════════════════════════════╝
  Add 1 to result: [0, 1]

  Decrement in-degrees of 1's neighbors:
    3: 1 → 0  ← Now 0, add to queue!
    4: 2 → 1  ← Not 0 yet

  In-degrees: {0: -, 1: -, 2: 0, 3: 0, 4: 1}
  Queue: [2, 3]

╔══════════════════════════════════════════════════════════════════╗
║ ITERATION 3: Dequeue node 2                                      ║
╚══════════════════════════════════════════════════════════════════╝
  Add 2 to result: [0, 1, 2]

  Decrement in-degrees of 2's neighbors:
    4: 1 → 0  ← Now 0, add to queue!

  In-degrees: {0: -, 1: -, 2: -, 3: 0, 4: 0}
  Queue: [3, 4]

╔══════════════════════════════════════════════════════════════════╗
║ ITERATIONS 4-5: Dequeue nodes 3, 4                               ║
╚══════════════════════════════════════════════════════════════════╝
  No outgoing edges from 3 and 4

FINAL RESULT: [0, 1, 2, 3, 4]
All 5 nodes processed → No cycle → Valid topological order!
```

### DFS Approach Trace:

```
INITIAL STATE:
Colors: {0: WHITE, 1: WHITE, 2: WHITE, 3: WHITE, 4: WHITE}
Result (post-order): []

DFS(0):
  Color 0 → GRAY
  │
  ├─ DFS(1):
  │    Color 1 → GRAY
  │    │
  │    ├─ DFS(3):
  │    │    Color 3 → GRAY
  │    │    No neighbors
  │    │    Color 3 → BLACK, add to result: [3]
  │    │
  │    ├─ DFS(4):
  │    │    Color 4 → GRAY
  │    │    No neighbors (or all BLACK)
  │    │    Color 4 → BLACK, add to result: [3, 4]
  │    │
  │    Color 1 → BLACK, add to result: [3, 4, 1]
  │
  ├─ DFS(2):
  │    Color 2 → GRAY
  │    4 is already BLACK (skip)
  │    Color 2 → BLACK, add to result: [3, 4, 1, 2]
  │
  Color 0 → BLACK, add to result: [3, 4, 1, 2, 0]

Post-order result: [3, 4, 1, 2, 0]
REVERSED (topological order): [0, 2, 1, 4, 3]

Both [0, 1, 2, 3, 4] and [0, 2, 1, 4, 3] are valid!
```

---

## Complexity Derivation with Proof

**Time Complexity: O(V + E)**

```
Kahn's Algorithm (BFS):
1. Computing in-degrees: O(E) to visit all edges
2. Queue initialization: O(V) to scan all in-degrees
3. Processing: Each vertex enqueued/dequeued exactly once: O(V)
4. Edge traversal: Each edge decrements in-degree exactly once: O(E)
Total Time: O(V + E)

DFS Algorithm:
1. Outer loop over V vertices: O(V)
2. DFS traversal visits each vertex exactly once
3. Each edge examined exactly once: O(E)
Total Time: O(V + E)
```

**Space Complexity: O(V + E)**

```
1. Graph storage (adjacency list): O(V + E)
2. In-degree array (Kahn's) or color array (DFS): O(V)
3. Queue (Kahn's) or Call Stack (DFS): O(V) worst case
Total Space: O(V + E)
```

### Trade-offs: Kahn's (BFS) vs Recursive DFS

While both algorithms have `O(V + E)` time complexity, their constant factors and space utilization behave differently:

1. **Stack Overflow Risk (DFS)**: In a completely linear graph (e.g., $v_1 \rightarrow v_2 \rightarrow ... \rightarrow v_n$), the recursive call stack depth will be exactly $V$. If $V = 10^5$, this will exceed the default recursion limit in Python (usually 1000) and cause a `RecursionError`. Kahn's algorithm avoids this entirely as it iterates using an explicit queue.
2. **Memory Locality**: Kahn's algorithm tends to have better cache locality because it processes adjacent nodes level by level, making it slightly faster in practice for dense graphs.
3. **Lexicographical Constraints**: Kahn's easily extends to "find the lexicographically smallest ordering" by swapping the standard queue for a min-heap. Doing this with recursive DFS is remarkably complex.

**Correctness proof for Kahn's algorithm:**

```
Theorem: If Kahn's processes all V vertices, the result is a valid topological order.

Proof:
1. Each processed vertex had in-degree 0 at processing time.
2. In-degree 0 means all predecessors were already processed.
3. Therefore, for every edge (u,v), u appears before v in result.
4. This is the definition of topological order. ∎

Corollary: If fewer than V vertices are processed, the graph contains a cycle.
Proof: The unprocessed vertices all have in-degree ≥ 1 among themselves.
No vertex in that subgraph can have in-degree 0, which means every vertex
has a predecessor within the subgraph. Following predecessors from any
unprocessed vertex must eventually revisit a vertex → cycle. ∎
```

---

## Edge Cases

```python
# 1. Empty graph (no edges)
n = 3; edges = []
# Result: [0, 1, 2] (any permutation is valid)

# 2. Single node
n = 1; edges = []
# Result: [0]

# 3. Linear chain (unique ordering)
edges = [[0, 1], [1, 2], [2, 3]]
# Result: [0, 1, 2, 3] (only one valid order)

# 4. Cycle (impossible)
edges = [[0, 1], [1, 2], [2, 0]]
# Result: [] (no valid topological order)

# 5. Disconnected DAG
edges = [[0, 1], [2, 3]]
# Result: Any interleaving, e.g., [0, 2, 1, 3] or [2, 0, 3, 1]

# 6. Diamond shape (multiple valid orderings)
edges = [[0, 1], [0, 2], [1, 3], [2, 3]]
# Result: [0, 1, 2, 3] or [0, 2, 1, 3]

# 7. Self-loop (trivial cycle)
edges = [[0, 0]]
# Result: [] (self-loop is a cycle)
```

---

## Interview Tips

1. **Know both algorithms**: Kahn's is more intuitive and safer in Python (no recursion limit); DFS is shorter
2. **Cycle detection is built-in**: Kahn's — check `len(result) != n`; DFS — check for GRAY→GRAY back edge
3. **Understand "topological order"**: u → v means u comes before v in the output
4. **Lexicographic variant**: Use min-heap instead of queue (adds log V factor)
5. **Parallel processing / critical path**: Count BFS levels in Kahn's
6. **Default to Kahn's in interviews**: It's iterative, handles cycles cleanly, and extends to variants easily
7. **Mention trade-offs proactively**: Shows depth of understanding

---

## Practice Problems

| #   | Problem                                     | Difficulty | Key Variation                                      | Hint                                                               |
| --- | ------------------------------------------- | ---------- | -------------------------------------------------- | ------------------------------------------------------------------ |
| 1   | [207. Course Schedule][lc207]               | Medium     | Cycle detection in a DAG                           | Just check if topo sort processes all nodes; don't need the order  |
| 2   | [210. Course Schedule II][lc210]            | Medium     | Return a valid topological order                   | Standard Kahn's; return `[]` if cycle                              |
| 3   | [269. Alien Dictionary][lc269]              | Hard       | Build graph from constraints, then topo sort       | Compare adjacent words to find char ordering edges; watch for invalid input |
| 4   | [1136. Parallel Courses][lc1136]            | Medium     | Minimum levels / parallel scheduling               | BFS level count — answer is the number of "rounds"                 |
| 5   | [444. Sequence Reconstruction][lc444]       | Medium     | Check if topo order is uniquely determined         | Queue must always have exactly 1 element at each step              |
| 6   | [2115. Find All Possible Recipes][lc2115]   | Medium     | Topo sort with string nodes and external supplies  | Build graph from recipes/ingredients; supplies are in-degree-0 sources |
| 7   | [802. Find Eventual Safe States][lc802]     | Medium     | Reverse graph + topo sort / cycle detection        | Nodes NOT in any cycle are "safe"; reverse edges and run Kahn's    |

[lc207]: https://leetcode.com/problems/course-schedule/
[lc210]: https://leetcode.com/problems/course-schedule-ii/
[lc269]: https://leetcode.com/problems/alien-dictionary/
[lc1136]: https://leetcode.com/problems/parallel-courses/
[lc444]: https://leetcode.com/problems/sequence-reconstruction/
[lc2115]: https://leetcode.com/problems/find-all-possible-recipes-from-given-supplies/
[lc802]: https://leetcode.com/problems/find-eventual-safe-states/

**Recommended progression**: 207 → 210 → 1136 → 444 → 2115 → 802 → 269

---

## Key Takeaways

1. **Kahn's Algorithm**: BFS with in-degree tracking — iterative, safe, extensible
2. **DFS Approach**: Reverse post-order — elegant, but watch recursion limits
3. **Only works on DAGs**: Cycle → no valid ordering (both approaches detect this)
4. **Multiple valid orders**: Unless the graph forms a single chain (Hamiltonian path)
5. **Lexicographic**: Swap queue for min-heap in Kahn's
6. **Parallel time**: Count BFS levels in Kahn's
7. **Default choice**: Prefer Kahn's in Python interviews unless DFS is more natural for the problem

---

## Next: [08-course-schedule.md](./08-course-schedule.md)

Deep dive into the Course Schedule problems.

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

**Key insight - Two equivalent approaches**:

1. **Kahn's (BFS) - "Process ready items first"**:
   - Find nodes with no dependencies (in-degree 0)
   - Process them, remove their outgoing edges
   - Repeat until done
   - Like: "What can I do right now? Do it, then check again."

2. **DFS - "Finish dependencies last"**:
   - Explore deeply, add to result when DONE (post-order)
   - Reverse at end
   - Like: "Go all the way, then on your way back, record the order."

**Visual proof - Why DFS post-order works**:
```
If A → B (A must come before B):
- DFS from A will visit B (directly or indirectly)
- B is added to result BEFORE A (post-order)
- Reversing puts A before B ✓

Graph:      DFS Post-order:    Reversed (topological):
A → B       [B, A]             [A, B] ✓
```

---

## When NOT to Use

**Don't use topological sort when:**
- **Graph has cycles** → No valid ordering exists; detect cycle first
- **Graph is undirected** → Concept doesn't apply (no "direction" of dependency)
- **You need shortest path** → Topological sort is about ordering, not distance
- **Order doesn't matter** → Simple traversal is simpler

**Topological sort is overkill when:**
- Graph is a simple chain → Just follow the links
- Only need to detect if ordering exists → Cycle detection is sufficient
- Problem asks for ANY traversal → BFS/DFS is simpler

**Common mistake scenarios:**
- Applying to undirected graphs → Meaningless result
- Forgetting to reverse DFS result → Order is backwards
- Not handling disconnected components → Must process all nodes

---

## Interview Context

Topological sort is a FANG+ favorite because:

1. **Dependency resolution**: Build systems, package managers, task scheduling
2. **Course ordering**: Classic Course Schedule II problem
3. **Multiple algorithms**: Kahn's (BFS) and DFS approaches
4. **DAG validation**: Topological sort exists iff graph is acyclic

If you see "ordering" or "dependencies", think topological sort.

---

## Core Concept

A **topological ordering** of a directed graph is a linear ordering of vertices such that for every edge u → v, u comes before v.

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

```python
from collections import defaultdict, deque

def topological_sort_kahn(n: int, edges: list[list[int]]) -> list[int]:
    """
    Topological sort using Kahn's algorithm (BFS).

    Time: O(V + E)
    Space: O(V)

    Returns empty list if cycle exists.
    """
    graph = defaultdict(list)
    in_degree = [0] * n

    for u, v in edges:
        graph[u].append(v)
        in_degree[v] += 1

    # Start with nodes having no dependencies
    queue = deque([i for i in range(n) if in_degree[i] == 0])
    result = []

    while queue:
        node = queue.popleft()
        result.append(node)

        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    # If not all nodes processed, cycle exists
    if len(result) != n:
        return []

    return result


# Usage
edges = [[0, 1], [0, 2], [1, 3], [2, 3]]
print(topological_sort_kahn(4, edges))  # [0, 1, 2, 3] or [0, 2, 1, 3]
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
def topological_sort_dfs(n: int, edges: list[list[int]]) -> list[int]:
    """
    Topological sort using DFS (reverse post-order).

    Time: O(V + E)
    Space: O(V)

    Returns empty list if cycle exists.
    """
    WHITE, GRAY, BLACK = 0, 1, 2

    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)

    color = [WHITE] * n
    result = []
    has_cycle = [False]  # Use list to modify in nested function

    def dfs(node: int):
        if has_cycle[0]:
            return

        color[node] = GRAY

        for neighbor in graph[node]:
            if color[neighbor] == GRAY:
                has_cycle[0] = True
                return
            if color[neighbor] == WHITE:
                dfs(neighbor)

        color[node] = BLACK
        result.append(node)  # Add to result when done with descendants

    for node in range(n):
        if color[node] == WHITE:
            dfs(node)

    if has_cycle[0]:
        return []

    return result[::-1]  # Reverse to get correct order
```

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

---

## All Topological Orderings

```python
def all_topological_sorts(n: int, edges: list[list[int]]) -> list[list[int]]:
    """
    Find ALL valid topological orderings.

    Time: O(V! × V) in worst case
    Space: O(V)

    Use for small graphs only.
    """
    graph = defaultdict(list)
    in_degree = [0] * n

    for u, v in edges:
        graph[u].append(v)
        in_degree[v] += 1

    result = []
    current = []
    visited = [False] * n

    def backtrack():
        if len(current) == n:
            result.append(current[:])
            return

        for node in range(n):
            if not visited[node] and in_degree[node] == 0:
                # Choose this node
                visited[node] = True
                current.append(node)
                for neighbor in graph[node]:
                    in_degree[neighbor] -= 1

                backtrack()

                # Undo choice
                visited[node] = False
                current.pop()
                for neighbor in graph[node]:
                    in_degree[neighbor] += 1

    backtrack()
    return result
```

---

## Comparison: Kahn's vs DFS

| Aspect | Kahn's (BFS) | DFS |
|--------|--------------|-----|
| Approach | In-degree counting | Reverse post-order |
| Cycle detection | Check if all nodes processed | Use three colors |
| Implementation | More intuitive | Slightly shorter |
| Lexicographic order | Use min-heap instead of queue | Harder to achieve |
| All orderings | Natural with backtracking | Possible but tricky |

---

## Lexicographically Smallest Order

Use priority queue (min-heap) instead of regular queue:

```python
import heapq

def topological_sort_lex(n: int, edges: list[list[int]]) -> list[int]:
    """
    Topological sort with lexicographically smallest order.

    Time: O((V + E) log V)
    Space: O(V)
    """
    graph = defaultdict(list)
    in_degree = [0] * n

    for u, v in edges:
        graph[u].append(v)
        in_degree[v] += 1

    # Use min-heap instead of queue
    heap = [i for i in range(n) if in_degree[i] == 0]
    heapq.heapify(heap)
    result = []

    while heap:
        node = heapq.heappop(heap)  # Always pick smallest
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

A topological order is unique if at every step, exactly one node has in-degree 0:

```python
def is_unique_topological_sort(n: int, edges: list[list[int]]) -> bool:
    graph = defaultdict(list)
    in_degree = [0] * n

    for u, v in edges:
        graph[u].append(v)
        in_degree[v] += 1

    queue = deque([i for i in range(n) if in_degree[i] == 0])

    while queue:
        if len(queue) != 1:
            return False  # Multiple choices = not unique

        node = queue.popleft()
        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    return True
```

### 2. Parallel Processing Time

Find the minimum time to complete all tasks if independent tasks can run in parallel:

```python
def parallel_courses(n: int, relations: list[list[int]]) -> int:
    """
    Minimum semesters to complete all courses.
    Each semester, take all available courses.
    """
    graph = defaultdict(list)
    in_degree = [0] * n

    for pre, course in relations:
        graph[pre - 1].append(course - 1)  # 1-indexed input
        in_degree[course - 1] += 1

    queue = deque([i for i in range(n) if in_degree[i] == 0])
    semesters = 0
    completed = 0

    while queue:
        semesters += 1
        next_queue = deque()

        # Process all current level (parallel)
        for _ in range(len(queue)):
            node = queue.popleft()
            completed += 1

            for neighbor in graph[node]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    next_queue.append(neighbor)

        queue = next_queue

    return semesters if completed == n else -1
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
Kahn's Algorithm:
1. Computing in-degrees: O(E)
2. Each vertex enqueued once: O(V)
3. Each edge decrements in-degree once: O(E)
4. Total: O(V + E)

DFS Algorithm:
1. Each vertex visited once: O(V)
2. Each edge examined once: O(E)
3. Total: O(V + E)
```

**Space Complexity: O(V + E)**

```
1. Graph storage: O(V + E)
2. In-degree array (Kahn's) or color array (DFS): O(V)
3. Queue/Stack: O(V)
4. Total: O(V + E)
```

**Correctness proof for Kahn's algorithm:**

```
Theorem: If Kahn's processes all V vertices, the result is a valid topological order.

Proof:
1. Each processed vertex had in-degree 0 at processing time.
2. In-degree 0 means all predecessors were already processed.
3. Therefore, for every edge (u,v), u appears before v in result.
4. This is the definition of topological order. ∎

Corollary: If not all vertices processed, a cycle exists.
Proof: Remaining vertices form a strongly connected component (cycle).
```

---

## Edge Cases

```python
# 1. Empty graph
n = 3, edges = []
# Result: [0, 1, 2] (any order)

# 2. Single node
n = 1, edges = []
# Result: [0]

# 3. Linear chain
edges = [[0, 1], [1, 2], [2, 3]]
# Result: [0, 1, 2, 3] (only one valid order)

# 4. Cycle
edges = [[0, 1], [1, 2], [2, 0]]
# Result: [] (no valid topological order)

# 5. Disconnected DAG
edges = [[0, 1], [2, 3]]
# Result: Any interleaving, e.g., [0, 2, 1, 3]
```

---

## Interview Tips

1. **Know both algorithms**: Kahn's is more intuitive, DFS is shorter
2. **Cycle detection**: Essential — check if all nodes are processed
3. **Understand "topological order"**: u → v means u comes before v
4. **Lexicographic variant**: Use heap instead of queue
5. **Parallel processing**: Count levels in BFS

---

## Practice Problems

| # | Problem | Difficulty | Key Variation |
|---|---------|------------|---------------|
| 1 | Course Schedule | Medium | Cycle detection |
| 2 | Course Schedule II | Medium | Return order |
| 3 | Alien Dictionary | Hard | Build graph from constraints |
| 4 | Parallel Courses | Medium | Minimum levels |
| 5 | Sequence Reconstruction | Medium | Unique order check |

---

## Key Takeaways

1. **Kahn's Algorithm**: BFS with in-degree tracking
2. **DFS Approach**: Reverse post-order
3. **Only works on DAGs**: Cycle → no valid ordering
4. **Multiple valid orders**: Unless graph is strictly linear
5. **Lexicographic**: Use heap instead of queue

---

## Next: [08-course-schedule.md](./08-course-schedule.md)

Deep dive into the Course Schedule problems.

# Topological Sort

> **Prerequisites:** [05-cycle-detection-directed](./05-cycle-detection-directed.md)

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

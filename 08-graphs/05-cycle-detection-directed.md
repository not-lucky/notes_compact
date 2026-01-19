# Cycle Detection in Directed Graphs

> **Prerequisites:** [03-dfs-basics](./03-dfs-basics.md)

## Interview Context

Cycle detection in directed graphs is essential because:

1. **Dependency validation**: Can we complete all tasks? (Course Schedule)
2. **Deadlock detection**: Finding circular dependencies
3. **DAG verification**: Topological sort only works on DAGs
4. **Different from undirected**: The algorithm is fundamentally different

Course Schedule I is a classic FANG+ interview problem.

---

## Core Concept: Why It's Different

In directed graphs, an edge back to a previously visited node isn't necessarily a cycle:

```
This is NOT a cycle:        This IS a cycle:
    0 → 1                       0 → 1
    ↓   ↓                       ↓   ↓
    2 → 3                       2 ← 3

0→2→3 and 0→1→3 share       0→1→3→2→0 forms a cycle
node 3 but no cycle
```

**Key insight**: A cycle exists only if we revisit a node that's **currently in our DFS path** (on the recursion stack).

---

## Three-Color (State) Algorithm

Track three states for each node:
- **WHITE (0)**: Unvisited
- **GRAY (1)**: Currently being processed (in recursion stack)
- **BLACK (2)**: Completely processed

**Cycle exists if we encounter a GRAY node during DFS.**

```python
from collections import defaultdict

def has_cycle_directed(n: int, edges: list[list[int]]) -> bool:
    """
    Detect cycle in directed graph using three colors.

    Time: O(V + E)
    Space: O(V)
    """
    WHITE, GRAY, BLACK = 0, 1, 2

    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)

    color = [WHITE] * n

    def dfs(node: int) -> bool:
        color[node] = GRAY  # Start processing

        for neighbor in graph[node]:
            if color[neighbor] == GRAY:
                return True  # Back edge = cycle
            if color[neighbor] == WHITE:
                if dfs(neighbor):
                    return True

        color[node] = BLACK  # Done processing
        return False

    # Check all nodes (graph may be disconnected)
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

## Alternative: Using Recursion Stack Set

```python
def has_cycle_rec_stack(n: int, edges: list[list[int]]) -> bool:
    """
    Detect cycle using explicit recursion stack tracking.

    Time: O(V + E)
    Space: O(V)
    """
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)

    visited = set()
    rec_stack = set()  # Nodes in current DFS path

    def dfs(node: int) -> bool:
        visited.add(node)
        rec_stack.add(node)

        for neighbor in graph[node]:
            if neighbor in rec_stack:
                return True  # Back edge
            if neighbor not in visited:
                if dfs(neighbor):
                    return True

        rec_stack.remove(node)  # Backtrack
        return False

    for node in range(n):
        if node not in visited:
            if dfs(node):
                return True

    return False
```

---

## Visual Example: Three Colors

```
Graph: 0 → 1 → 2 → 0 (has cycle)

DFS from 0:
Step 1: Color[0] = GRAY, visit 1
Step 2: Color[1] = GRAY, visit 2
Step 3: Color[2] = GRAY, visit 0
Step 4: Color[0] = GRAY → CYCLE DETECTED!

Graph: 0 → 1 → 2 (no cycle)
       ↓
       3

DFS from 0:
Step 1: Color[0] = GRAY, visit 1
Step 2: Color[1] = GRAY, visit 2
Step 3: Color[2] = GRAY, no neighbors
Step 4: Color[2] = BLACK, backtrack
Step 5: Color[1] = BLACK, backtrack, visit 3
Step 6: Color[3] = GRAY, no neighbors
Step 7: Color[3] = BLACK, backtrack
Step 8: Color[0] = BLACK, done
No cycle.
```

---

## Course Schedule I (Can Finish?)

```python
def can_finish(numCourses: int,
               prerequisites: list[list[int]]) -> bool:
    """
    Can all courses be finished? (No cycle in dependency graph)

    prerequisites[i] = [a, b] means b is prereq of a (b → a)

    Time: O(V + E)
    Space: O(V + E)
    """
    WHITE, GRAY, BLACK = 0, 1, 2

    graph = defaultdict(list)
    for course, prereq in prerequisites:
        graph[prereq].append(course)

    color = [WHITE] * numCourses

    def has_cycle(node: int) -> bool:
        color[node] = GRAY

        for next_course in graph[node]:
            if color[next_course] == GRAY:
                return True
            if color[next_course] == WHITE:
                if has_cycle(next_course):
                    return True

        color[node] = BLACK
        return False

    for course in range(numCourses):
        if color[course] == WHITE:
            if has_cycle(course):
                return False

    return True


# Usage
numCourses = 4
prerequisites = [[1, 0], [2, 1], [3, 2]]  # 0→1→2→3
print(can_finish(numCourses, prerequisites))  # True

prerequisites = [[1, 0], [0, 1]]  # Cycle: 0↔1
print(can_finish(2, prerequisites))  # False
```

---

## Finding the Cycle (Not Just Detecting)

```python
def find_cycle(n: int, edges: list[list[int]]) -> list[int]:
    """
    Find and return nodes in a cycle, if one exists.

    Returns empty list if no cycle.
    """
    WHITE, GRAY, BLACK = 0, 1, 2

    graph = defaultdict(list)
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
                cycle_start = neighbor
                cycle_end = node
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

    # Reconstruct cycle
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

Detect cycle by checking if topological sort is possible:

```python
from collections import deque

def has_cycle_kahn(n: int, edges: list[list[int]]) -> bool:
    """
    Detect cycle using Kahn's algorithm (BFS topological sort).

    If not all nodes are processed, a cycle exists.

    Time: O(V + E)
    Space: O(V)
    """
    graph = defaultdict(list)
    in_degree = [0] * n

    for u, v in edges:
        graph[u].append(v)
        in_degree[v] += 1

    # Start with nodes having no incoming edges
    queue = deque([i for i in range(n) if in_degree[i] == 0])
    processed = 0

    while queue:
        node = queue.popleft()
        processed += 1

        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    return processed != n  # Cycle if not all processed
```

---

## Comparison of Approaches

| Approach | Time | Space | Finds Cycle Nodes |
|----------|------|-------|-------------------|
| Three Colors (DFS) | O(V + E) | O(V) | With modification |
| Recursion Stack (DFS) | O(V + E) | O(V) | With modification |
| Kahn's (BFS) | O(V + E) | O(V) | No (just detects) |

---

## Common Mistakes

```python
# WRONG: Using simple visited set (works for undirected, not directed)
def has_cycle_wrong(n, edges):
    visited = set()

    def dfs(node):
        if node in visited:
            return True  # WRONG! This is not necessarily a cycle
        visited.add(node)
        for neighbor in graph[node]:
            if dfs(neighbor):
                return True
        return False
    ...

# CORRECT: Track recursion stack separately
def has_cycle_correct(n, edges):
    visited = set()
    rec_stack = set()

    def dfs(node):
        visited.add(node)
        rec_stack.add(node)
        for neighbor in graph[node]:
            if neighbor in rec_stack:  # In current path
                return True
            if neighbor not in visited:
                if dfs(neighbor):
                    return True
        rec_stack.remove(node)  # Remove when backtracking
        return False
```

---

## Edge Cases

```python
# 1. Self-loop
edges = [[0, 0]]  # Node with edge to itself = cycle

# 2. No edges
edges = []  # No cycle possible

# 3. Single node, no edges
n = 1, edges = []  # No cycle

# 4. Disconnected graph with cycle in one component
edges = [[0, 1], [1, 0], [2, 3]]  # Cycle in {0, 1}, none in {2, 3}

# 5. Long chain
edges = [[0, 1], [1, 2], ..., [n-2, n-1]]  # No cycle
```

---

## Interview Tips

1. **Clarify directed vs undirected**: Algorithms are different
2. **Know three-color approach**: Clean and intuitive
3. **Know Kahn's alternative**: Some prefer BFS
4. **Handle disconnected graphs**: Check all components
5. **Practice Course Schedule**: Most common problem variant

---

## Practice Problems

| # | Problem | Difficulty | Key Variation |
|---|---------|------------|---------------|
| 1 | Course Schedule | Medium | Core cycle detection |
| 2 | Course Schedule II | Medium | Topological sort if no cycle |
| 3 | Find Eventual Safe States | Medium | Nodes not in any cycle |
| 4 | Redundant Connection II | Hard | Find edge causing cycle |

---

## Key Takeaways

1. **Three states**: WHITE, GRAY, BLACK for DFS
2. **GRAY = in current path**: Back edge to GRAY = cycle
3. **Different from undirected**: Can't use simple visited check
4. **Kahn's alternative**: Cycle if topological sort fails
5. **Handle all components**: Graph may be disconnected

---

## Next: [06-cycle-detection-undirected.md](./06-cycle-detection-undirected.md)

Learn cycle detection for undirected graphs.

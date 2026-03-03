# Bipartite Check (Graph Coloring)

> **Prerequisites:** [02-bfs-basics](./02-bfs-basics.md), [03-dfs-basics](./03-dfs-basics.md)

## Interview Context

Bipartite checking is important because:

1. **Graph theory fundamental**: Core concept in graph algorithms
2. **Two-coloring**: Can graph be divided into two groups with no intra-group edges?
3. **Real applications**: Matching problems, scheduling, conflict detection
4. **BFS/DFS practice**: Standard traversal with coloring

**FANG Context**: Very common in Google and Amazon interviews. At Google, it often appears as a scheduling or resource allocation problem. At Amazon, it frequently shows up in relation to graph coloring and conflict resolution. Note that while this is a classic graph problem, **Word Ladder** (a shortest path BFS problem) is even more frequently asked at Amazon/Google and is highly recommended to practice alongside this.

---

## Core Concept: What is Bipartite?

A graph is **bipartite** if its vertices can be divided into two disjoint sets such that every edge connects a vertex in one set to a vertex in the other.

**Equivalent characterization**: A graph is bipartite **if and only if** it contains no odd-length cycles. If you find an odd cycle, it is impossible to 2-color the graph. (This is a classical result in graph theory.)

```
Bipartite:              Not Bipartite:
  1 --- 3                  1 --- 2
  |     |                   \   /
  2 --- 4                    \ /
                              3
Sets: {1,4} and {2,3}     Triangle has odd cycle
```

### Intuition: Why Two-Coloring Works

Think of it like assigning teams. Start at any node and put it on Team 0. All its
neighbors must be on Team 1. All their neighbors must be on Team 0, and so on.

- If you ever reach a neighbor that's **already on the same team** as the current
  node, you've found a conflict — an odd-length path (and therefore an odd cycle)
  between them. The graph is **not bipartite**.
- If you color the entire graph without any conflict, it **is bipartite**.

This is exactly what BFS and DFS do: propagate colors and detect conflicts.

---

## BFS Approach (Two-Coloring)

BFS is the most natural approach: color level by level, alternating colors.

```python
from collections import deque


def is_bipartite_bfs(graph: list[list[int]]) -> bool:
    """
    Check if an undirected graph is bipartite using BFS 2-coloring.

    Args:
        graph: Adjacency list where graph[i] contains neighbors of node i.

    Returns:
        True if the graph is bipartite, False otherwise.

    Time:  O(V + E)
    Space: O(V) for the color array and queue
    """
    n = len(graph)
    # -1 = uncolored, 0 = color A, 1 = color B
    color = [-1] * n

    # Must loop over all nodes to handle disconnected components
    for start in range(n):
        if color[start] != -1:
            continue  # Already colored in a previous BFS

        queue = deque([start])
        color[start] = 0

        while queue:
            node = queue.popleft()
            for neighbor in graph[node]:
                if color[neighbor] == -1:
                    # Assign the opposite color
                    color[neighbor] = 1 - color[node]
                    queue.append(neighbor)
                elif color[neighbor] == color[node]:
                    # Same color on both ends of an edge → not bipartite
                    return False

    return True
```

---

## DFS Approach

DFS works identically in logic: color the current node, recurse on neighbors
with the opposite color, and check for conflicts. The only difference is traversal
order (depth-first instead of breadth-first).

```python
def is_bipartite_dfs(graph: list[list[int]]) -> bool:
    """
    Check if an undirected graph is bipartite using DFS 2-coloring.

    Time:  O(V + E)
    Space: O(V) for color array + O(V) worst-case recursion depth
    """
    n = len(graph)
    color = [-1] * n

    def dfs(node: int, c: int) -> bool:
        """Color 'node' with color 'c' and recurse. Returns False on conflict."""
        color[node] = c
        for neighbor in graph[node]:
            if color[neighbor] == -1:
                if not dfs(neighbor, 1 - c):
                    return False
            elif color[neighbor] == c:
                return False  # Conflict: neighbor has the same color
        return True

    # Handle disconnected components
    for start in range(n):
        if color[start] == -1:
            if not dfs(start, 0):
                return False

    return True
```

### BFS vs DFS — When to Pick Which

| Aspect | BFS | DFS |
|---|---|---|
| Traversal | Level-by-level | Depth-first |
| Data structure | Queue (iterative) | Call stack (recursive) or explicit stack |
| Stack overflow risk | None | Yes, on deep/skewed graphs (up to V frames) |
| Interview default | Slightly more common for bipartite | Equally valid |
| Key advantage | Iterative — no recursion limit issues | Shorter to write |

Both have identical **O(V + E)** time and **O(V)** space. Use BFS if the graph could be very deep (long chains) or if you want to avoid recursion limits. Use DFS if you prefer concise recursive code and are sure depth won't exceed Python's recursion limit. In an interview, BFS is often the safer choice for this reason.

---

## Visual Example

```
Graph:                  Coloring:
  0 --- 1               0 (Red) --- 1 (Blue)
  |     |               |           |
  2 --- 3               2 (Blue) --- 3 (Red)

BFS from 0:
  color[0] = 0 (Red)
  Queue: [0]

  Process 0 → neighbors 1, 2:
    color[1] = 1 (Blue), enqueue 1
    color[2] = 1 (Blue), enqueue 2
  Queue: [1, 2]

  Process 1 → neighbors 0, 3:
    0 already colored 0 ≠ 1 ✓
    color[3] = 0 (Red), enqueue 3
  Queue: [2, 3]

  Process 2 → neighbors 0, 3:
    0 already colored 0 ≠ 1 ✓
    3 already colored 0 ≠ 1 ✓
  Queue: [3]

  Process 3 → neighbors 1, 2:
    All neighbors already colored correctly ✓

Result: Bipartite! Sets: {0, 3} and {1, 2}
```

---

## Union-Find Approach

The idea: for each node, **all of its neighbors must belong to the same group**
(the opposite group from the node). So we union all neighbors together, then
check that no node ends up in the same set as any of its neighbors.

```python
class UnionFind:
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x: int) -> int:
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x: int, y: int) -> None:
        px, py = self.find(x), self.find(y)
        if px == py:
            return
        if self.rank[px] < self.rank[py]:
            px, py = py, px
        self.parent[py] = px
        if self.rank[px] == self.rank[py]:
            self.rank[px] += 1


def is_bipartite_uf(graph: list[list[int]]) -> bool:
    """
    Check bipartite using Union-Find.

    Idea: All neighbors of a node should be in the same group
    (the "other" group). If a node and its neighbor are in the
    same group, the graph is not bipartite.

    Time:  O((V + E) * alpha(V))  — alpha is inverse Ackermann, practically O(1)
    Space: O(V)
    """
    n = len(graph)
    uf = UnionFind(n)

    for node in range(n):
        if not graph[node]:
            continue  # No neighbors — nothing to check

        # Union all neighbors of 'node' together (they must share a group)
        first_neighbor = graph[node][0]
        for neighbor in graph[node]:
            # If node is in the same set as a neighbor → conflict
            if uf.find(node) == uf.find(neighbor):
                return False
            # All neighbors belong together in the "other" group
            uf.union(first_neighbor, neighbor)

    return True
```

---

## Possible Bipartition (Groups with Dislikes)

Sometimes the graph isn't given to you explicitly as an adjacency list. In problems like *LeetCode 886: Possible Bipartition*, you are given a number of people `n` and a list of `dislikes` (edges). We just need to build the adjacency list first, then perform the exact same bipartite check.

```python
from collections import deque


def possible_bipartition(n: int, dislikes: list[list[int]]) -> bool:
    """
    Can n people be split into two groups such that
    no one dislikes someone in their group?

    dislikes[i] = [a, b] means a and b dislike each other.

    Time:  O(V + E)
    Space: O(V + E)
    """
    # Build adjacency list (people are 1-indexed)
    graph: list[list[int]] = [[] for _ in range(n + 1)]
    for a, b in dislikes:
        graph[a].append(b)
        graph[b].append(a)

    color = [-1] * (n + 1)

    for start in range(1, n + 1):
        if color[start] != -1:
            continue

        queue = deque([start])
        color[start] = 0

        while queue:
            node = queue.popleft()
            for neighbor in graph[node]:
                if color[neighbor] == -1:
                    color[neighbor] = 1 - color[node]
                    queue.append(neighbor)
                elif color[neighbor] == color[node]:
                    return False

    return True
```

---

## Related: Return the Two Groups

Sometimes it's not enough to know *if* a graph is bipartite; we actually need the groups themselves (e.g., assigning classes to two different classrooms, assigning people to two teams).

```python
from collections import deque


def get_bipartition(graph: list[list[int]]) -> tuple[list[int], list[int]]:
    """
    Return the two groups if bipartite, empty lists otherwise.

    Time:  O(V + E)
    Space: O(V)
    """
    n = len(graph)
    color = [-1] * n

    for start in range(n):
        if color[start] != -1:
            continue

        queue = deque([start])
        color[start] = 0

        while queue:
            node = queue.popleft()
            for neighbor in graph[node]:
                if color[neighbor] == -1:
                    color[neighbor] = 1 - color[node]
                    queue.append(neighbor)
                elif color[neighbor] == color[node]:
                    return [], []  # Not bipartite

    # Only reached if the entire graph is successfully colored
    group_a = [i for i in range(n) if color[i] == 0]
    group_b = [i for i in range(n) if color[i] == 1]
    return group_a, group_b
```

---

## Key Insight: Odd Cycles

A graph is NOT bipartite **if and only if** it contains an odd-length cycle.

```
Odd cycle (triangle):
    1 --- 2
     \   /
      \ /
       3

Try coloring:
  1 = Red
  2 = Blue (neighbor of 1)
  3 = Red (neighbor of 2)
  But 3 is also neighbor of 1 — same color! Conflict.

Impossible to 2-color.
```

**Why odd cycles break bipartiteness**: In a cycle of length k, you alternate
colors around the cycle. After k steps you return to the start. If k is even
you land on the original color (no conflict). If k is odd you land on the
opposite color — but the start node already has its original color, so two
adjacent nodes share a color. Contradiction.

---

## Handling Disconnected Graphs

A graph with multiple connected components is bipartite **only if every
component is bipartite**. This is why we loop over all nodes and start a
BFS/DFS from each unvisited node:

```python
for start in range(n):
    if color[start] == -1:
        # Start a new BFS/DFS from this component
        ...
```

Forgetting this outer loop is the single most common bug in bipartite solutions.

---

## Edge Cases

```python
# 1. Single node — bipartite (trivially)
graph = [[]]

# 2. No edges — bipartite (any partition works)
graph = [[], [], []]

# 3. Complete graph K3 — NOT bipartite (triangle = odd cycle)
graph = [[1, 2], [0, 2], [0, 1]]

# 4. Self-loop — NOT bipartite (node conflicts with itself)
graph = [[0]]

# 5. Disconnected components — each must be bipartite individually
```

---

## Common Mistakes

```python
# WRONG: Only checking from node 0 (misses disconnected components)
def is_bipartite_wrong(graph):
    n = len(graph)
    color = [-1] * n
    color[0] = 0
    # Only processes one component!

# CORRECT: Check all components
def is_bipartite_correct(graph):
    n = len(graph)
    color = [-1] * n
    for start in range(n):
        if color[start] == -1:
            # BFS/DFS from start
            ...


# WRONG: Not checking for same-color conflict
for neighbor in graph[node]:
    if color[neighbor] == -1:
        color[neighbor] = 1 - color[node]
        queue.append(neighbor)
    # Missing: what if neighbor already has the SAME color?

# CORRECT: Always check the conflict case
for neighbor in graph[node]:
    if color[neighbor] == -1:
        color[neighbor] = 1 - color[node]
        queue.append(neighbor)
    elif color[neighbor] == color[node]:
        return False


# WRONG: Using a visited set instead of a color array
visited = set()
# Visited only tracks "seen", not which group — useless for bipartite!

# CORRECT: Track color (0 or 1), with -1 meaning unvisited
color = [-1] * n
```

---

## Complexity Analysis

| Approach   | Time               | Space |
|------------|--------------------| ----- |
| BFS        | O(V + E)           | O(V)  |
| DFS        | O(V + E)           | O(V)  |
| Union-Find | O((V + E) * α(V)) | O(V)  |

### Deep Dive

**Time Complexity:**
- **BFS/DFS**: O(V + E). We visit every vertex once and examine each edge once (twice in an undirected graph stored as a symmetric adjacency list, but still O(E) total). For a dense graph E can be up to O(V²).
- **Union-Find**: O((V + E) * α(V)). Each `find`/`union` is nearly O(1) due to path compression and union by rank (α is the inverse Ackermann function). Practically the same as BFS/DFS, but with a larger constant factor.

**Space Complexity:**
- **BFS**: O(V) for the color array + queue. In the worst case (star graph), the queue holds O(V) nodes at once.
- **DFS**: O(V) for the color array + recursion stack. Worst case (long chain), the stack depth reaches V. Consider iterative DFS if stack overflow is a concern.
- **Union-Find**: O(V) for parent and rank arrays.

---

## Interview Tips

1. **"Two-coloring" = "bipartite check"**: Recognize these as the same problem.
2. **Handle disconnected graphs**: Always loop over all nodes as potential BFS/DFS roots.
3. **Color before enqueuing**: Assign the color when you add a neighbor to the queue (not when you dequeue). This prevents a node from being added multiple times with conflicting states.
4. **Odd cycle = not bipartite**: Mention this characterization to show graph theory depth.
5. **Know both BFS and DFS**: Either is acceptable. BFS is safer for deep graphs.

---

## Practice Problems

| #   | Problem | LeetCode # | Difficulty | Key Idea / Hint |
|-----|---------|------------|------------|-----------------|
| 1   | Is Graph Bipartite? | 785 | Medium | Direct BFS/DFS coloring on adjacency list. The baseline problem. |
| 2   | Possible Bipartition | 886 | Medium | Build a "dislike" graph, then check bipartiteness. 1-indexed nodes. |
| 3   | Flower Planting With No Adjacent | 1042 | Medium | Graph coloring with 4 colors — greedy, but bipartite thinking helps build intuition. |
| 4   | Shortest Cycle in a Graph | 2608 | Hard | BFS from each node to detect the shortest cycle. Odd-cycle theory ties directly into bipartite understanding. |
| 5   | Divide Nodes Into the Maximum Number of Groups | 2493 | Hard | Bipartite check as a prerequisite, then BFS layering to maximize group count. |

---

## Key Takeaways

1. **Two-coloring**: Alternate colors between neighbors using BFS or DFS.
2. **Same color on an edge = conflict**: The graph is not bipartite.
3. **Odd cycle**: The only structural reason a graph fails bipartiteness.
4. **Check all components**: The outer loop over unvisited nodes is essential.
5. **BFS and DFS are interchangeable**: Same logic, different traversal order.
6. **Union-Find is a valid alternative**: Union all neighbors together, check that no node shares a set with its neighbor.

---

## Next: [17-alien-dictionary.md](./17-alien-dictionary.md)

Learn topological sort from comparison constraints.

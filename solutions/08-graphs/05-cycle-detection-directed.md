# Solutions: Cycle Detection in Directed Graphs

## Practice Problems

| # | Problem | Difficulty | Key Variation |
|---|---------|------------|---------------|
| 1 | Course Schedule | Medium | Core cycle detection |
| 2 | Course Schedule II | Medium | Topological sort if no cycle |
| 3 | Find Eventual Safe States | Medium | Nodes not in any cycle |
| 4 | Redundant Connection II | Hard | Find edge causing cycle |

---

## 1. Course Schedule

### Problem Statement
Given `numCourses` and a list of `prerequisites` where `[a, b]` means you must take course `b` before `a`, determine if you can finish all courses.

### Optimal Python Solution

```python
from collections import defaultdict

def canFinish(numCourses: int, prerequisites: list[list[int]]) -> bool:
    # Build graph: b -> a for [a, b]
    adj = defaultdict(list)
    for course, pre in prerequisites:
        adj[pre].append(course)

    # States: 0 = unvisited, 1 = visiting, 2 = visited
    state = [0] * numCourses

    def has_cycle(node):
        if state[node] == 1: return True
        if state[node] == 2: return False

        state[node] = 1 # Mark as visiting
        for neighbor in adj[node]:
            if has_cycle(neighbor):
                return True

        state[node] = 2 # Mark as fully visited
        return False

    for i in range(numCourses):
        if state[i] == 0:
            if has_cycle(i):
                return False
    return True
```

### Explanation
- **Algorithm**: We use DFS with three states (Three-Coloring).
- **Logic**: A cycle in a directed graph exists if and only if we encounter a node that is currently being visited (`state == 1`) in the current recursion stack.
- **Complexity**: Time O(V + E), Space O(V + E) for graph storage.

---

## 2. Course Schedule II

### Problem Statement
Return the ordering of courses to finish all courses. Return `[]` if impossible.

### Optimal Python Solution

```python
from collections import defaultdict

def findOrder(numCourses: int, prerequisites: list[list[int]]) -> list[int]:
    adj = defaultdict(list)
    for course, pre in prerequisites:
        adj[pre].append(course)

    state = [0] * numCourses
    order = []

    def has_cycle(node):
        if state[node] == 1: return True
        if state[node] == 2: return False

        state[node] = 1
        for neighbor in adj[node]:
            if has_cycle(neighbor):
                return True

        state[node] = 2
        order.append(node) # Post-order
        return False

    for i in range(numCourses):
        if state[i] == 0:
            if has_cycle(i):
                return []

    return order[::-1] # Reverse post-order for topological sort
```

### Explanation
- **Topological Sort**: This is reverse post-order DFS.
- **Ordering**: We append the node to `order` after all its dependents are processed. Reversing gives the correct execution order.
- **Complexity**: Time O(V + E), Space O(V + E).

---

## 3. Find Eventual Safe States

### Problem Statement
A node is "safe" if every possible path starting from that node leads to a terminal node (a node with no outgoing edges). Return all safe nodes in ascending order.

### Optimal Python Solution

```python
def eventualSafeNodes(graph: list[list[int]]) -> list[int]:
    n = len(graph)
    # 0 = unvisited, 1 = visiting/part of cycle, 2 = safe
    state = [0] * n

    def is_safe(node):
        if state[node] > 0:
            return state[node] == 2

        state[node] = 1 # Assume unsafe/visiting
        for neighbor in graph[node]:
            if not is_safe(neighbor):
                return False

        state[node] = 2 # All paths lead to terminal nodes
        return True

    return [i for i in range(n) if is_safe(i)]
```

### Explanation
- **Concept**: A node is safe if it is NOT part of a cycle and doesn't lead to a cycle.
- **Algorithm**: Similar to cycle detection. If a node or any of its descendants can reach a "visiting" node, it's unsafe.
- **Complexity**: Time O(V + E), Space O(V).

---

## 4. Redundant Connection II

### Problem Statement
A directed tree with one additional edge added. Find the edge that can be removed to make it a rooted tree again.

### Optimal Python Solution

```python
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
    def find(self, i):
        if self.parent[i] == i: return i
        self.parent[i] = self.find(self.parent[i])
        return self.parent[i]
    def union(self, i, j):
        root_i, root_j = self.find(i), self.find(j)
        if root_i != root_j:
            self.parent[root_i] = root_j
            return True
        return False

def findRedundantDirectedConnection(edges: list[list[int]]) -> list[int]:
    n = len(edges)
    parent = {}
    candidates = []

    # 1. Check for node with two parents
    for u, v in edges:
        if v in parent:
            candidates.append([parent[v], v])
            candidates.append([u, v])
            break
        parent[v] = u

    # 2. Check for cycle using Union-Find
    uf = UnionFind(n + 1)
    for u, v in edges:
        if [u, v] in candidates and [u, v] == candidates[1]:
            continue # Skip the second candidate for now
        if not uf.union(u, v):
            # If no two-parent node, this edge creates the cycle
            if not candidates: return [u, v]
            # Otherwise, the first candidate must be the answer
            return candidates[0]

    # If we finished without cycle, the second candidate was the answer
    return candidates[1]
```

### Explanation
- **Cases**:
    1. A node has two parents (two edges pointing to it).
    2. There is a cycle.
    3. Both (one edge causes two parents AND a cycle).
- **Algorithm**: Identify if any node has two parents. If so, those two edges are our candidates. We use Union-Find to detect cycles.
- **Complexity**: Time O(V α(V)), Space O(V).

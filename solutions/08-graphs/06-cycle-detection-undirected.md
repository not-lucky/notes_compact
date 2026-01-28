# Solutions: Cycle Detection in Undirected Graphs

## Practice Problems

| #   | Problem                        | Difficulty | Key Variation      |
| --- | ------------------------------ | ---------- | ------------------ |
| 1   | Graph Valid Tree               | Medium     | Tree validation    |
| 2   | Redundant Connection           | Medium     | Find cycle edge    |
| 3   | Number of Connected Components | Medium     | Component counting |
| 4   | Redundant Connection II        | Hard       | Directed variation |

---

## 1. Graph Valid Tree

### Problem Statement

Determine if a graph is a valid tree.

### Optimal Python Solution

```python
def validTree(n: int, edges: list[list[int]]) -> bool:
    # A tree must have exactly n-1 edges
    if len(edges) != n - 1:
        return False

    from collections import defaultdict, deque
    adj = defaultdict(list)
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)

    # Check connectivity
    visited = {0} if n > 0 else set()
    queue = deque([0]) if n > 0 else deque()

    while queue:
        curr = queue.popleft()
        for neighbor in adj[curr]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

    return len(visited) == n
```

### Explanation

- **Property**: For a graph with `n` nodes, it's a tree if it is connected and has `n-1` edges.
- **Algorithm**: Check edge count, then run BFS to verify connectivity.
- **Complexity**: Time O(V + E), Space O(V + E).

---

## 2. Redundant Connection

### Problem Statement

Find an edge that can be removed so that the resulting graph is a tree of `n` nodes.

### Optimal Python Solution

```python
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n + 1))

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        rootX, rootY = self.find(x), self.find(y)
        if rootX == rootY:
            return False # Cycle detected
        self.parent[rootX] = rootY
        return True

def findRedundantConnection(edges: list[list[int]]) -> list[int]:
    uf = UnionFind(len(edges))
    for u, v in edges:
        if not uf.union(u, v):
            return [u, v]
```

### Explanation

- **Concept**: An edge is redundant if it connects two nodes that are already in the same connected component.
- **Algorithm**: Iterate through edges, adding them to a Union-Find structure. The first edge that fails to perform a `union` is the redundant one.
- **Complexity**: Time O(E α(V)), Space O(V).

---

## 3. Number of Connected Components

### Problem Statement

Find the number of connected components in an undirected graph.

### Optimal Python Solution

```python
from collections import defaultdict

def countComponents(n: int, edges: list[list[int]]) -> int:
    adj = defaultdict(list)
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)

    visited = set()
    count = 0

    def dfs(node):
        visited.add(node)
        for neighbor in adj[node]:
            if neighbor not in visited:
                dfs(neighbor)

    for i in range(n):
        if i not in visited:
            count += 1
            dfs(i)
    return count
```

### Explanation

- **Algorithm**: Standard traversal. Each time we start a traversal from an unvisited node, we've found a new component.
- **Complexity**: Time O(V + E), Space O(V + E).

---

## 4. Redundant Connection II

### Problem Statement

(Directed version included here for completeness as per practice list).

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

    for u, v in edges:
        if v in parent:
            candidates.append([parent[v], v])
            candidates.append([u, v])
            break
        parent[v] = u

    uf = UnionFind(n + 1)
    for u, v in edges:
        if candidates and [u, v] == candidates[1]: continue
        if not uf.union(u, v):
            if not candidates: return [u, v]
            return candidates[0]
    return candidates[1]
```

### Explanation

- **Logic**: This problem is harder because it's directed. We check for nodes with two parents or cycles.
- **Complexity**: Time O(E α(V)), Space O(V).

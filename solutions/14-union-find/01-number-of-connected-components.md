# Number of Connected Components

## Problem Statement

Given `n` nodes labeled from `0` to `n-1` and a list of undirected edges, find the number of connected components in the graph.

**Example:**
```
Input: n = 5, edges = [[0,1], [1,2], [3,4]]
Output: 2

Graph:
0 -- 1 -- 2     3 -- 4
(component 1)   (component 2)
```

## Building Intuition

### Why This Works

Union-Find treats connectivity as an equivalence relation: nodes in the same component are "equivalent." Each component has a representative (the root), and two nodes are connected if and only if they share the same root. The data structure maintains a forest where each tree is a component, and `find(x)` returns x's tree root.

The genius is how unions work: to connect two nodes, find their roots and link one root to the other. This merges two trees into one, reducing the component count by one. Initially, each node is its own root (n components). Each successful union decreases the count by 1. After processing all edges, the remaining count is the answer.

Path compression (`parent[x] = find(parent[x])`) and union by rank keep trees shallow, giving nearly O(1) amortized time per operation. Without these optimizations, trees could become long chains with O(n) find time.

### How to Discover This

When you see "groups," "connected components," or "are X and Y in the same group," think Union-Find. It's ideal when you're given edges incrementally and need to track connectivity dynamically. DFS/BFS work too, but Union-Find shines when you need to answer multiple "are these connected?" queries after some edges are added.

### Pattern Recognition

This is the **Disjoint Set Union (DSU) / Union-Find** pattern. Recognize it when:
- You're grouping elements into disjoint sets
- You need to efficiently merge sets and query membership
- The problem involves connectivity in graphs without needing actual paths

## When NOT to Use

- **When you need to find the actual path between nodes**: Union-Find only tracks connectivity, not paths. Use BFS/DFS for paths.
- **When edges can be deleted (dynamic connectivity)**: Standard Union-Find doesn't support "un-union." You'd need link-cut trees or offline algorithms.
- **When the graph is small and you only query once**: DFS is simpler and equally efficient for one-time component counting.
- **When you need to list all members of a component**: Union-Find doesn't maintain membership lists. You'd need an additional pass after building the structure.

## Approach

### Method 1: Union-Find
Use disjoint set to group connected nodes.

### Method 2: DFS/BFS
Visit all nodes, count number of DFS/BFS calls needed.

## Implementation

```python
def count_components(n: int, edges: list[list[int]]) -> int:
    """
    Count connected components using Union-Find.

    Time: O(E × α(N)) ≈ O(E) where E = edges
    Space: O(N)
    """
    parent = list(range(n))
    rank = [0] * n

    def find(x: int) -> int:
        if parent[x] != x:
            parent[x] = find(parent[x])  # Path compression
        return parent[x]

    def union(x: int, y: int) -> bool:
        px, py = find(x), find(y)
        if px == py:
            return False  # Already connected

        # Union by rank
        if rank[px] < rank[py]:
            px, py = py, px
        parent[py] = px
        if rank[px] == rank[py]:
            rank[px] += 1

        return True

    components = n

    for a, b in edges:
        if union(a, b):
            components -= 1

    return components


def count_components_dfs(n: int, edges: list[list[int]]) -> int:
    """
    Count connected components using DFS.

    Time: O(V + E)
    Space: O(V + E)
    """
    from collections import defaultdict

    # Build adjacency list
    graph = defaultdict(list)
    for a, b in edges:
        graph[a].append(b)
        graph[b].append(a)

    visited = set()
    components = 0

    def dfs(node: int):
        visited.add(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                dfs(neighbor)

    for node in range(n):
        if node not in visited:
            dfs(node)
            components += 1

    return components
```

## Complexity Analysis

| Method | Time | Space | Notes |
|--------|------|-------|-------|
| Union-Find | O(E × α(N)) | O(N) | Nearly O(E) |
| DFS | O(V + E) | O(V + E) | Graph storage |

## Variations

### Graph Valid Tree
```python
def valid_tree(n: int, edges: list[list[int]]) -> bool:
    """
    Check if edges form a valid tree.
    Valid tree: n-1 edges and all connected.

    Time: O(N)
    Space: O(N)
    """
    if len(edges) != n - 1:
        return False

    parent = list(range(n))

    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    def union(x, y):
        px, py = find(x), find(y)
        if px == py:
            return False  # Cycle detected
        parent[px] = py
        return True

    for a, b in edges:
        if not union(a, b):
            return False

    return True
```

### Redundant Connection
```python
def find_redundant_connection(edges: list[list[int]]) -> list[int]:
    """
    Find edge that creates a cycle.
    Return the last such edge.

    Time: O(N)
    Space: O(N)
    """
    n = len(edges)
    parent = list(range(n + 1))

    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    for a, b in edges:
        pa, pb = find(a), find(b)
        if pa == pb:
            return [a, b]  # This edge creates cycle
        parent[pa] = pb

    return []
```

### Accounts Merge
```python
def accounts_merge(accounts: list[list[str]]) -> list[list[str]]:
    """
    Merge accounts with same email.

    Time: O(N × K × α(N)) where K = max emails per account
    Space: O(N × K)
    """
    from collections import defaultdict

    email_to_id = {}
    email_to_name = {}
    parent = {}

    def find(x):
        if x not in parent:
            parent[x] = x
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    def union(x, y):
        parent[find(x)] = find(y)

    # Union emails in same account
    for account in accounts:
        name = account[0]
        first_email = account[1]

        for email in account[1:]:
            email_to_name[email] = name
            union(email, first_email)

    # Group emails by root
    components = defaultdict(list)
    for email in email_to_name:
        root = find(email)
        components[root].append(email)

    # Format result
    return [[email_to_name[root]] + sorted(emails)
            for root, emails in components.items()]
```

## Related Problems

- **Graph Valid Tree** - Check if graph is tree
- **Redundant Connection** - Find cycle-creating edge
- **Accounts Merge** - Union-Find on strings
- **Number of Islands** - Grid-based connectivity
- **Friend Circles** - Same problem, different name

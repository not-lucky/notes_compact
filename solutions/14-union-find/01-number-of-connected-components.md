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

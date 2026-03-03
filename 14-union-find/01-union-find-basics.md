# Union-Find Basics

> **Prerequisites:** [Arrays](../02-arrays-strings/README.md), [Hash Tables](../03-hashmaps-sets/README.md)

## Interview Context

Union-Find is a fundamental data structure for managing disjoint sets. It appears in problems involving connectivity, grouping, and cycle detection. Interviewers use it to test understanding of amortized analysis and optimization techniques.

---

## Building Intuition

**The "Club Membership" Mental Model**

Imagine a social network where people form clubs. Initially, everyone is in their own private club (a club of one). When two people become friends, their clubs merge—everyone in both clubs is now in the same combined club.

The key operations are:

- **Find**: "Which club is this person in?" (Find the club representative)
- **Union**: "Make these two people's clubs merge into one"

**Why Does This Work?**

Union-Find answers the question: "Are A and B connected?" The insight is that we don't need to track the entire path between A and B. We just need to know if they share the same "representative" or "root."

```
Think of it like last names:
- Initially: Alice Smith, Bob Jones, Carol Smith
- Alice and Carol share a "last name" (Smith) → same family/club
- Bob has a different "last name" (Jones) → different family/club

Union-Find uses a "parent pointer" structure where:
- Each element points to a parent
- The root points to itself
- Two elements are connected if they have the same root
```

**Visual Mental Model: Trees as Sets**

```
Elements: {A, B, C, D, E}

Initial state (5 separate sets):
  A    B    C    D    E     Each is its own root

After union(A,B) and union(C,D):
  A    C    E
  │    │
  B    D

After union(A,C):
      A
     ┌┴┐
     B C
       │
       D

Now A, B, C, D are all in the same set (root = A)
E is still in its own set (root = E)
```

---

## When NOT to Use Union-Find

**1. When You Need the Actual Path**

Union-Find only tells you IF two nodes are connected, not HOW they're connected. For the actual path, use BFS/DFS.

```python
# Union-Find: "Are nodes 5 and 10 connected?" → True/False
# But can't tell you: [5 → 7 → 3 → 10]
```

**2. For Directed Graph Connectivity**

Union-Find treats edges as undirected. For directed graphs with questions like "Can I reach B from A?" use DFS or topological sort.

```python
# A → B → C doesn't mean C can reach A!
# Union-Find would incorrectly merge them into one "connected" set
```

**3. When DFS/BFS is Simpler**

For one-time static connectivity queries, DFS/BFS might be cleaner:

```python
# Count connected components once on a static graph?
# DFS: O(V+E), simple, intuitive
# Union-Find: O(E * α(n)), slightly more code for same result

# But: Dynamic edges added over time with connectivity queries?
# Union-Find: O(α(n)) per union/find — handles new edges incrementally
# DFS: O(V+E) per query (must re-traverse the graph each time) → too slow
```

**4. When Edges Can Be Removed**

Standard Union-Find only supports adding connections. You can't efficiently "un-merge" two sets. For dynamic graphs with both additions and deletions, consider:

- Link-Cut Trees (O(log n) per operation)
- Rebuild periodically

---

## Pattern: Basic Union-Find

The core idea: maintain a forest where each tree represents a set. Each element points to its parent, and the root is the set's representative.

### Core Components

```
UnionFind:
├── parent[]: maps each element to its parent
├── find(x): returns the root/representative of x's set
├── union(x, y): merges the sets containing x and y
└── connected(x, y): checks if x and y are in the same set
```

### Visualization

```
Initial state: 5 elements, each in its own set
parent = [0, 1, 2, 3, 4]

  0    1    2    3    4     (each is its own root)

After union(1, 2):
parent = [0, 1, 1, 3, 4]    (2's parent becomes 1)

  0    1    3    4
       │
       2

After union(3, 4):
parent = [0, 1, 1, 3, 3]    (4's parent becomes 3)

  0    1    3
       │    │
       2    4

After union(1, 3):
parent = [0, 1, 1, 1, 3]    (root of 3 is 3, so parent[3] = root of 1 = 1)

       1
      ┌┴┐
     2   3
         │
         4

After union(0, 1):
parent = [0, 0, 1, 1, 3]    (root of 1 is 1, so parent[1] = root of 0 = 0)

        0
        │
        1
       ┌┴┐
       2  3
          │
          4
```

---

## Implementation

### Naive Union-Find

```python
class UnionFind:
    """
    Basic Union-Find without optimizations.

    Time: O(n) per operation in worst case
    Space: O(n)
    """

    def __init__(self, n: int):
        # Each element starts as its own parent (representative)
        self.parent = list(range(n))

    def find(self, x: int) -> int:
        """
        Find the root/representative of x's set.

        Traverse up the parent chain until we find an element
        that is its own parent (the root).
        """
        while self.parent[x] != x:
            x = self.parent[x]
        return x

    def union(self, x: int, y: int) -> bool:
        """
        Merge the sets containing x and y.

        Returns True if merged, False if already in same set.
        """
        root_x = self.find(x)
        root_y = self.find(y)

        if root_x == root_y:
            return False  # Already in same set

        # Make root_x the parent of root_y
        self.parent[root_y] = root_x
        return True

    def connected(self, x: int, y: int) -> bool:
        """Check if x and y are in the same set."""
        return self.find(x) == self.find(y)


# Example usage
uf = UnionFind(5)
print(uf.connected(0, 1))  # False
uf.union(0, 1)
print(uf.connected(0, 1))  # True
uf.union(1, 2)
print(uf.connected(0, 2))  # True (transitivity!)
```

### Why Naive Implementation is Slow

```
Problem: Chain formation

With parent[root_y] = root_x, certain union sequences create
a degenerate chain. For example:

union(1,0): find(1)=1, find(0)=0 → parent[0]=1  → parent=[1,1,2,3,4]
union(2,1): find(2)=2, find(1)=1 → parent[1]=2  → parent=[1,2,2,3,4]
union(3,2): find(3)=3, find(2)=2 → parent[2]=3  → parent=[1,2,3,3,4]
union(4,3): find(4)=4, find(3)=3 → parent[3]=4  → parent=[1,2,3,4,4]

Tree becomes a chain (arrow ← means "is parent of"):
4 ← 3 ← 2 ← 1 ← 0
i.e. parent[0]=1, parent[1]=2, parent[2]=3, parent[3]=4

find(0) needs to traverse: 0 → 1 → 2 → 3 → 4
That's O(n) for a single find!

The pattern: each union attaches the existing tree as a child
of a new single node, growing the chain by one level.

With n union operations, tree height can be O(n).
n find operations = O(n²) total time.
```

---

## Problem: Count Connected Components (Easy Warm-up)

Given `n` nodes labeled `0` to `n-1` and a list of edges, return the number of connected components.

This is the simplest Union-Find problem: just union every edge and count how many distinct sets remain.

### Example

```
Input: n = 5, edges = [[0,1],[1,2],[3,4]]
Output: 2

Components: {0, 1, 2} and {3, 4}
```

### Solution

```python
def count_components(n: int, edges: list[list[int]]) -> int:
    """
    Count connected components using Union-Find.

    Time: O(E * n) worst case with naive union-find (no optimizations)
    Space: O(n)
    """
    parent = list(range(n))

    def find(x: int) -> int:
        while parent[x] != x:
            x = parent[x]
        return x

    def union(x: int, y: int) -> bool:
        root_x, root_y = find(x), find(y)
        if root_x == root_y:
            return False
        parent[root_y] = root_x
        return True

    components = n
    for a, b in edges:
        if union(a, b):
            components -= 1

    return components


# Examples
print(count_components(5, [[0, 1], [1, 2], [3, 4]]))  # 2
print(count_components(5, []))                          # 5 (no edges)
print(count_components(1, []))                          # 1
print(count_components(4, [[0, 1], [1, 2], [2, 3]]))   # 1
```

---

## Problem: Friendship Query (Warm-up)

Given `n` people labeled `0` to `n-1` and a list of friendship pairs, determine if person `a` and person `b` are friends (directly or indirectly).

### Example

```
Input: n = 5, friendships = [[0,1],[1,2],[3,4]], queries = [[0,2],[0,3]]
Output: [True, False]

Explanation:
  0 - 1 - 2     3 - 4
  Person 0 and 2 are connected through 1 → True
  Person 0 and 3 are in different groups   → False
```

### Solution

```python
def friendship_queries(
    n: int,
    friendships: list[list[int]],
    queries: list[list[int]],
) -> list[bool]:
    """
    Check connectivity between pairs using Union-Find with path halving.

    Note: Uses path halving but NOT union by rank, so worst-case per
    operation is O(log n) amortized, not O(α(n)). For true O(α(n)),
    union by rank is also needed (see 02-path-compression.md and
    03-union-by-rank.md).

    Time: O((F + Q) × log n) where F = friendships, Q = queries
    Space: O(n)
    """
    parent = list(range(n))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]  # Path halving
            x = parent[x]
        return x

    def union(x: int, y: int) -> None:
        px, py = find(x), find(y)
        if px != py:
            parent[py] = px

    # Build the union-find structure from friendships
    for a, b in friendships:
        union(a, b)

    # Answer each query: are they in the same set?
    return [find(a) == find(b) for a, b in queries]


# Example
print(friendship_queries(5, [[0,1],[1,2],[3,4]], [[0,2],[0,3]]))
# Output: [True, False]
```

---

## Problem: Number of Provinces

**LeetCode 547**: There are `n` cities. Some of them are connected. If city `a` is connected to city `b`, and city `b` is connected to city `c`, then city `a` is connected to city `c`. Find the total number of provinces (groups of directly or indirectly connected cities).

### Example

```
Input: isConnected = [[1,1,0],[1,1,0],[0,0,1]]
Output: 2

Cities: 0, 1, 2
Connections: 0-1 (from matrix[0][1] = 1)
Result: Two provinces: {0, 1} and {2}

Visual:
  0 --- 1     2
  Province 1   Province 2
```

### Solution

```python
def findCircleNum(isConnected: list[list[int]]) -> int:
    """
    Count connected components using Union-Find.

    Note: Uses path halving but not union by rank, so per-operation
    cost is O(log n) amortized rather than O(α(n)).

    Time: O(n² × log n) — dominated by the n² matrix scan
    Space: O(n)
    """
    n = len(isConnected)
    parent = list(range(n))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]  # Path halving optimization
            x = parent[x]
        return x

    def union(x: int, y: int) -> bool:
        px, py = find(x), find(y)
        if px == py:
            return False
        parent[py] = px
        return True

    # Process connections
    provinces = n  # Start with n separate provinces

    for i in range(n):
        for j in range(i + 1, n):  # Only upper triangle
            if isConnected[i][j] == 1:
                if union(i, j):
                    provinces -= 1  # Merged two provinces

    return provinces


# Alternative: Track count in UnionFind class
class UnionFind:
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.count = n  # Number of components

    def find(self, x: int) -> int:
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]  # Path halving
            x = self.parent[x]
        return x

    def union(self, x: int, y: int) -> bool:
        px, py = self.find(x), self.find(y)
        if px == py:
            return False
        self.parent[py] = px
        self.count -= 1
        return True


def findCircleNum_v2(isConnected: list[list[int]]) -> int:
    n = len(isConnected)
    uf = UnionFind(n)

    for i in range(n):
        for j in range(i + 1, n):
            if isConnected[i][j] == 1:
                uf.union(i, j)

    return uf.count
```

---

## Problem: Graph Valid Tree

**LeetCode 261**: Given `n` nodes labeled from `0` to `n-1` and a list of undirected edges, check if these edges form a valid tree.

A valid tree has:

1. Exactly `n-1` edges
2. All nodes connected (one component)
3. No cycles

### Example

```
Input: n = 5, edges = [[0,1],[0,2],[0,3],[1,4]]
Output: True

  0 --- 1 --- 4
 / \
2   3

4 edges = n-1 = 4 ✓, no cycles ✓, all nodes connected ✓

Input: n = 5, edges = [[0,1],[1,2],[2,0],[3,4]]
Output: False

  0 --- 1     3 --- 4
   \   /
    2

4 edges = n-1 = 4, but cycle 0-1-2-0 → not a tree
```

### Solution

```python
def validTree(n: int, edges: list[list[int]]) -> bool:
    """
    Check if edges form a valid tree.

    Tree conditions:
    1. n-1 edges (necessary but not sufficient)
    2. No cycles (union returns False if cycle)
    3. Connected (one component at end)

    Note: Uses path halving without union by rank, so per-operation
    cost is O(log n) amortized.

    Time: O(n × log n)
    Space: O(n)
    """
    # Condition 1: Tree must have exactly n-1 edges
    if len(edges) != n - 1:
        return False

    parent = list(range(n))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]  # Path halving
            x = parent[x]
        return x

    def union(x: int, y: int) -> bool:
        px, py = find(x), find(y)
        if px == py:
            return False  # Cycle detected!
        parent[py] = px
        return True

    # Process all edges - if any union fails, there's a cycle
    for a, b in edges:
        if not union(a, b):
            return False

    # With n-1 edges and no cycles, must be connected
    return True


# Example
print(validTree(5, [[0,1],[0,2],[0,3],[1,4]]))  # True
print(validTree(5, [[0,1],[1,2],[2,3],[1,3],[1,4]]))  # False (5 edges ≠ n-1 = 4)
print(validTree(5, [[0,1],[1,2],[2,0],[3,4]]))  # False (n-1 edges but cycle: 0-1-2-0)
```

### Why This Works

```
For n nodes:
- Tree needs exactly n-1 edges
- If we have n-1 edges and no cycles → must be connected
- If we have n-1 edges with a cycle → some nodes disconnected

Why? With n-1 edges:
- No cycles: each edge connects 2 previously unconnected components
  Starting with n components, n-1 successful unions → 1 component
- Has cycle: one edge connects already-connected nodes
  Only n-2 "useful" unions → 2+ components
```

---

## Problem: Earliest Moment When Everyone Becomes Friends

**LeetCode 1101**: In a social group, there are `n` people labeled `0` to `n-1`. You are given a list of `logs` where `logs[i] = [timestamp_i, x_i, y_i]` means that `x_i` and `y_i` became friends at time `timestamp_i`. Return the earliest time at which every person became acquainted with every other person. If there is no such earliest time, return `-1`.

### Example

```
Input: logs = [[20190101,0,1],[20190104,3,4],[20190107,2,3],
               [20190211,1,5],[20190224,2,4],[20190301,0,3],
               [20190312,1,2],[20190322,4,5]], n = 6
Output: 20190301

Timeline:
  t=20190101: union(0,1) → {0,1} {2} {3} {4} {5}     5 components
  t=20190104: union(3,4) → {0,1} {2} {3,4} {5}        4 components
  t=20190107: union(2,3) → {0,1} {2,3,4} {5}          3 components
  t=20190211: union(1,5) → {0,1,5} {2,3,4}            2 components
  t=20190224: union(2,4) → already connected, skip     2 components
  t=20190301: union(0,3) → {0,1,2,3,4,5}              1 component ✓
```

### Key Insight

Sort logs by timestamp and process edges in order. The answer is the timestamp when the component count drops to 1. This is a natural fit for Union-Find because we're adding edges incrementally and tracking connectivity.

### Solution

```python
def earliestAcq(logs: list[list[int]], n: int) -> int:
    """
    Find the earliest time all n people are connected.

    Strategy:
    1. Sort logs by timestamp
    2. Process each friendship with union-find
    3. Track component count — return timestamp when it reaches 1

    Time: O(E log E + E × log n) where E = len(logs)
         (sorting + union-find operations with path halving)
    Space: O(n)
    """
    logs.sort(key=lambda x: x[0])  # Sort by timestamp

    parent = list(range(n))
    components = n

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]  # Path halving
            x = parent[x]
        return x

    def union(x: int, y: int) -> bool:
        px, py = find(x), find(y)
        if px == py:
            return False
        parent[py] = px
        return True

    for timestamp, x, y in logs:
        if union(x, y):
            components -= 1
            if components == 1:
                return timestamp  # Everyone is connected!

    return -1  # Never fully connected


# Example
logs = [
    [20190101,0,1], [20190104,3,4], [20190107,2,3],
    [20190211,1,5], [20190224,2,4], [20190301,0,3],
    [20190312,1,2], [20190322,4,5],
]
print(earliestAcq(logs, 6))  # 20190301
```

### Step-by-Step Trace

```
n=6, parent=[0,1,2,3,4,5], components=6

After sorting (already sorted by timestamp):

t=20190101, union(0,1):
  find(0)=0, find(1)=1, different → parent[1]=0
  parent=[0,0,2,3,4,5], components=5

t=20190104, union(3,4):
  find(3)=3, find(4)=4, different → parent[4]=3
  parent=[0,0,2,3,3,5], components=4

t=20190107, union(2,3):
  find(2)=2, find(3)=3, different → parent[3]=2
  parent=[0,0,2,2,3,5], components=3

t=20190211, union(1,5):
  find(1): parent[1]=0, parent[0]=0 → root=0
  find(5)=5, different → parent[5]=0
  parent=[0,0,2,2,3,0], components=2

t=20190224, union(2,4):
  find(2)=2
  find(4): parent[4]=3 → path halving: parent[4]=parent[3]=2, x=2
           parent[2]=2 → root=2
  Same root (2=2), skip. components=2
  parent=[0,0,2,2,2,0] (parent[4] updated by path halving)

t=20190301, union(0,3):
  find(0)=0
  find(3): parent[3]=2, parent[2]=2 → root=2
  Different → parent[2]=0
  parent=[0,0,0,2,2,0], components=1 → return 20190301 ✓
```

---

## Problem: Redundant Connection

**LeetCode 684**: You are given a graph that started as a tree with `n` nodes (labeled `1` to `n`), with one additional edge added. The additional edge connects two existing nodes and is given as part of the `edges` list. Return the edge that, if removed, would restore the graph to a tree. If there are multiple answers, return the one that occurs **last** in the input.

This is a direct application of cycle detection with Union-Find: the first edge whose union returns False is the edge that creates the cycle.

### Example

```
Input: edges = [[1,2],[1,3],[2,3]]
Output: [2,3]

Explanation:
  union(1,2): {1,2}, {3}  — success
  union(1,3): {1,2,3}     — success
  union(2,3): 2 and 3 already connected → this edge is redundant

Input: edges = [[1,2],[2,3],[3,4],[1,4],[1,5]]
Output: [1,4]

Explanation:
  union(1,2): success
  union(2,3): success
  union(3,4): success
  union(1,4): 1 and 4 already connected (via 1-2-3-4) → redundant
```

### Solution

```python
def findRedundantConnection(edges: list[list[int]]) -> list[int]:
    """
    Find the edge that creates a cycle in a graph that should be a tree.

    Strategy: Process edges in order. The first edge where both endpoints
    are already in the same component is the redundant edge. Since the
    problem guarantees exactly one extra edge (one cycle), exactly one
    union will fail — and that's our answer.

    Note: Nodes are 1-indexed per the problem statement.

    Time: O(n * log n) with path halving, no union by rank
    Space: O(n)
    """
    n = len(edges)
    parent = list(range(n + 1))  # 1-indexed nodes

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]  # Path halving
            x = parent[x]
        return x

    def union(x: int, y: int) -> bool:
        px, py = find(x), find(y)
        if px == py:
            return False  # Already connected — this edge creates a cycle
        parent[py] = px
        return True

    for a, b in edges:
        if not union(a, b):
            return [a, b]

    return []  # Should never reach here per problem constraints


# Examples
print(findRedundantConnection([[1, 2], [1, 3], [2, 3]]))        # [2, 3]
print(findRedundantConnection([[1, 2], [2, 3], [3, 4], [1, 4], [1, 5]]))  # [1, 4]
```

---

## Complexity Analysis

| Implementation        | Find       | Union      | Connected  | Space |
| --------------------- | ---------- | ---------- | ---------- | ----- |
| Naive                 | O(n)       | O(n)       | O(n)       | O(n)  |
| With path compression | O(log n)\* | O(log n)\* | O(log n)\* | O(n)  |
| With union by rank    | O(log n)   | O(log n)   | O(log n)   | O(n)  |
| Both optimizations    | O(α(n))    | O(α(n))    | O(α(n))    | O(n)  |

\*Amortized over many operations. "Path compression" here covers all variants (full path compression, path halving, path splitting).

---

## Common Variations

### 1. Dynamic Initialization

When elements aren't known upfront. Uses a dict instead of a list, so elements can be any hashable type and don't need to be pre-allocated.

> **Note:** This uses recursive path compression but no union by rank.
> Sufficient for most interview problems; add rank for O(α(n)) guarantees.

```python
class UnionFind:
    def __init__(self) -> None:
        self.parent: dict[int, int] = {}

    def find(self, x: int) -> int:
        if x not in self.parent:
            self.parent[x] = x  # Create new set on first access
            return x
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # Path compression
        return self.parent[x]

    def union(self, x: int, y: int) -> bool:
        px, py = self.find(x), self.find(y)
        if px == py:
            return False
        self.parent[py] = px
        return True
```

### 2. String Elements

Same dynamic pattern but with string keys — useful for problems involving emails, usernames, or account merging.

> **Note:** Uses recursive path compression, no union by rank. Same
> trade-off as Dynamic Initialization above.

```python
class UnionFind:
    def __init__(self) -> None:
        self.parent: dict[str, str] = {}

    def find(self, x: str) -> str:
        if x not in self.parent:
            self.parent[x] = x
            return x
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # Path compression
        return self.parent[x]

    def union(self, x: str, y: str) -> bool:
        px, py = self.find(x), self.find(y)
        if px == py:
            return False
        self.parent[py] = px
        return True


# Usage with string elements
uf = UnionFind()
uf.union("alice@email.com", "alice@work.com")
print(uf.find("alice@email.com") == uf.find("alice@work.com"))  # True
```

---

## Edge Cases

1. **Empty input**: n=0 → 0 components
2. **Single element**: n=1 → 1 component
3. **No edges**: Each element is its own component
4. **Self-loops**: union(x, x) should return False
5. **Duplicate edges**: Handle gracefully (second union returns False)
6. **Invalid indices**: Validate x and y are in range

---

## Interview Tips

1. **Start simple**: Implement naive version first, then optimize
2. **Ask about size**: Number of elements affects whether to optimize
3. **Clarify operations**: Just union/find or also need count/size?
4. **Mention optimizations**: Show you know path compression and union by rank
5. **Return value**: Union returning bool is useful for cycle detection

---

## Practice Problems

| #   | Problem                                            | Difficulty | Key Concept                    |
| --- | -------------------------------------------------- | ---------- | ------------------------------ |
| 1   | LC 323 — Number of Connected Components in Graph   | Medium     | Basic component counting       |
| 2   | LC 547 — Number of Provinces                       | Medium     | Adjacency matrix + counting    |
| 3   | LC 261 — Graph Valid Tree                          | Medium     | Cycle detection + connectivity |
| 4   | LC 684 — Redundant Connection                      | Medium     | Find the cycle-creating edge   |
| 5   | LC 1101 — Earliest Moment Everyone Becomes Friends | Medium     | Process edges in sorted order  |
| 6   | LC 200 — Number of Islands (Union-Find approach)   | Medium     | Grid as graph                  |

---

## Related Sections

- [Path Compression](./02-path-compression.md) - First optimization
- [Union by Rank](./03-union-by-rank.md) - Second optimization
- [Connected Components](./04-connected-components.md) - Classic application

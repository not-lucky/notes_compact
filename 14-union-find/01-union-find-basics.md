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
  |    |
  B    D

After union(A,C):
      A
     /|
    B C
      |
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
# DFS: Simple, intuitive
# Union-Find: Same complexity, more code

# But: Dynamic edges added over time?
# Union-Find: O(α(n)) per edge
# DFS: O(V+E) per query → too slow
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
       |
       2

After union(3, 4):
parent = [0, 1, 1, 3, 3]    (4's parent becomes 3)

  0    1    3
       |    |
       2    4

After union(1, 3):
parent = [0, 1, 1, 1, 3]    (3's root 3 -> parent becomes 1)

       1
      /|\
     2 3
       |
       4

After union(0, 1):
parent = [1, 1, 1, 1, 3]    (0's parent becomes 1)

       1
      /|\\
     0 2 3
         |
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
After union(0,1), union(1,2), union(2,3), union(3,4):

parent = [0, 0, 1, 2, 3]

Tree becomes a chain:
0 <- 1 <- 2 <- 3 <- 4

find(4) needs to traverse: 4 -> 3 -> 2 -> 1 -> 0
That's O(n) for a single find!

With n union operations, tree height can be O(n).
n find operations = O(n²) total time.
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

    Time: O(n² × α(n)) - check all pairs, near O(n²)
    Space: O(n)
    """
    n = len(isConnected)
    parent = list(range(n))

    def find(x: int) -> int:
        while parent[x] != x:
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

### Solution

```python
def validTree(n: int, edges: list[list[int]]) -> bool:
    """
    Check if edges form a valid tree.

    Tree conditions:
    1. n-1 edges (necessary but not sufficient)
    2. No cycles (union returns False if cycle)
    3. Connected (one component at end)

    Time: O(n × α(n))
    Space: O(n)
    """
    # Condition 1: Tree must have exactly n-1 edges
    if len(edges) != n - 1:
        return False

    parent = list(range(n))

    def find(x: int) -> int:
        while parent[x] != x:
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
print(validTree(5, [[0,1],[1,2],[2,3],[1,3],[1,4]]))  # False (cycle: 1-2-3-1)
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

## Complexity Analysis

| Implementation | Find | Union | Connected | Space |
|----------------|------|-------|-----------|-------|
| Naive | O(n) | O(n) | O(n) | O(n) |
| With path compression | O(log n)* | O(log n)* | O(log n)* | O(n) |
| With union by rank | O(log n) | O(log n) | O(log n) | O(n) |
| Both optimizations | O(α(n)) | O(α(n)) | O(α(n)) | O(n) |

*Amortized over many operations

---

## Common Variations

### 1. Dynamic Initialization

When elements aren't known upfront:

```python
class UnionFind:
    def __init__(self):
        self.parent = {}

    def find(self, x):
        if x not in self.parent:
            self.parent[x] = x  # Create new set

        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        px, py = self.find(x), self.find(y)
        if px != py:
            self.parent[py] = px
```

### 2. String Elements

```python
class UnionFind:
    def __init__(self):
        self.parent = {}

    def find(self, x: str) -> str:
        if x not in self.parent:
            self.parent[x] = x
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x: str, y: str) -> None:
        self.parent[self.find(y)] = self.find(x)


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

| # | Problem | Difficulty | Key Concept |
|---|---------|------------|-------------|
| 1 | Number of Provinces | Medium | Count components |
| 2 | Graph Valid Tree | Medium | Cycle detection + connectivity |
| 3 | Number of Connected Components | Medium | Basic counting |
| 4 | Earliest Moment When Everyone Becomes Friends | Medium | Process edges in order |
| 5 | Number of Islands (Union-Find approach) | Medium | Grid as graph |

---

## Related Sections

- [Path Compression](./02-path-compression.md) - First optimization
- [Union by Rank](./03-union-by-rank.md) - Second optimization
- [Connected Components](./04-connected-components.md) - Classic application

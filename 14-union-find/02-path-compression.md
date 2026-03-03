# Path Compression

> **Prerequisites:** [Union-Find Basics](./01-union-find-basics.md)

## Interview Context

Path compression is the first key optimization for Union-Find that reduces `find` from O(n) worst-case to O(log n) amortized. Interviewers expect you to implement it correctly. Combined with union by rank/size, it achieves O(α(n)) amortized per operation — effectively O(1) since the inverse Ackermann function α(n) ≤ 4 for any practical input size (up to ~2^65536).

---

## Building Intuition

**The "Phone Tree" Mental Model**

Imagine a company where every employee knows their direct manager, but not the CEO. To find out who's the ultimate boss:

Without path compression:

```
Employee → Manager → Director → VP → CEO
Each query: "Who's your manager?" repeated up the chain
Every lookup: O(depth) time
```

With path compression:

```
First query: Employee → Manager → Director → VP → CEO
             (Remember: CEO is the ultimate boss!)
Update everyone: Employee → CEO
                 Manager → CEO
                 Director → CEO
                 VP → CEO

Next query: Employee → CEO (instant!)
```

**Why This Works**

The key insight: _We don't care about the intermediate managers—we only need the root._

Once we've found the root, we "shortcut" everyone's pointer directly to it. This is lazy optimization:

- First access might be slow (traverse the chain)
- But it fixes the structure for all future accesses
- Amortized over many operations → O(log n) per find (or O(α(n)) with union by rank)

**Visual Transformation**

```
Before find(7):                After find(7):
       0                              0
       |                       /|\ \ \ \ \
       1                      1 2 3 4 5 6 7
       |
       2
       |
       3
       |
       4
       |
       5
       |
       6
       |
       7

Tall chain → flat star
```

**The Amortization Argument**

Each node can only move closer to the root, never further away. After path compression:

- A node at depth d gets moved to depth 1
- It can never go back to depth d
- Total "work" across all operations is bounded

---

## When NOT to Use Path Compression

**1. When You Need Parent Relationships**

Path compression destroys the original parent structure. If you need to know the original edges:

```python
# Original: 0 ← 1 ← 2 ← 3
# After find(3): 0 ← 1, 0 ← 2, 0 ← 3
# Lost: the information that 1 was parent of 2
```

**2. In Weighted Union-Find (Sometimes)**

With weighted Union-Find (tracking ratios like a/b = 2.5), path compression must also update weights along the compressed path. It's doable but requires careful implementation (see the Evaluate Division problem below):

```python
# weight[x] represents the ratio x / parent[x]
# When compressing x → root, multiply weights along the entire path
# e.g., x/parent = 2, parent/grandparent = 3 → x/root = 6
```

**3. When Stack Depth is Constrained (Use Iterative Instead)**

Recursive path compression can cause stack overflow on very deep trees. Use the iterative two-pass version instead:

```python
# Recursive: O(depth) stack space
# Iterative two-pass: O(1) extra space
```

**4. When Modification is Forbidden**

If the structure is read-only or needs to remain unchanged for other uses, you can't apply path compression.

---

## The Problem: Tall Trees

Without optimization, the Union-Find tree can become a long chain:

```
After many unions without optimization:

  0
  |
  1
  |
  2
  |
  3
  |
  4

find(4) traverses: 4 → 3 → 2 → 1 → 0
That's O(n) for one find!
```

---

## Solution: Path Compression

**Key insight**: When we call `find(x)`, we traverse from x to the root. Why not make every node along the path point directly to the root?

### Before and After

```
Before find(4):
       0
       |
       1
       |
       2
       |
       3
       |
       4

After find(4) with path compression:
       0
     / | \ \
    1  2  3  4

All nodes now point directly to root!
Next find(4) is O(1).
```

---

## Implementation

### Recursive Path Compression

```python
class UnionFind:
    """
    Union-Find with path compression.

    Time: O(log n) amortized per operation
    Space: O(n) + O(depth) recursion stack
           (first find on a chain of n is O(n) stack;
            after compression, subsequent finds are O(1) stack)
    """

    def __init__(self, n: int) -> None:
        self.parent: list[int] = list(range(n))

    def find(self, x: int) -> int:
        """
        Find root with path compression.

        After this call, x and all its ancestors
        point directly to the root.
        """
        if self.parent[x] != x:
            # Recursively find root, then update parent
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x: int, y: int) -> bool:
        root_x = self.find(x)  # Path compression happens here
        root_y = self.find(y)  # And here

        if root_x == root_y:
            return False

        self.parent[root_y] = root_x
        return True


# Trace through example
uf = UnionFind(5)

# Build chain: 0 <- 1 <- 2 <- 3 <- 4
uf.parent = [0, 0, 1, 2, 3]

print("Before find(4):", uf.parent)  # [0, 0, 1, 2, 3]

root = uf.find(4)

print("After find(4):", uf.parent)   # [0, 0, 0, 0, 0]
print("Root:", root)                  # 0
```

### Iterative Path Compression (Two-Pass)

```python
def find(self, x: int) -> int:
    """
    Iterative path compression (two passes).

    Pass 1: Find the root
    Pass 2: Update all parents to root

    Advantage: No recursion stack overflow for deep trees.
    """
    # Pass 1: Find root
    root = x
    while self.parent[root] != root:
        root = self.parent[root]

    # Pass 2: Compress path
    while self.parent[x] != root:
        next_x = self.parent[x]
        self.parent[x] = root
        x = next_x

    return root
```

### Path Halving (One-Pass Approximation)

```python
def find(self, x: int) -> int:
    """
    Path halving: each node visited skips to its grandparent.

    After setting parent[x] to grandparent, x advances to the
    grandparent (skipping one node), so only ~half the nodes
    on the path are visited and updated.
    Single pass, no recursion, same amortized complexity as full compression.
    """
    while self.parent[x] != x:
        # Point to grandparent instead of parent
        self.parent[x] = self.parent[self.parent[x]]
        x = self.parent[x]
    return x
```

### Path Splitting (Another One-Pass Variant)

```python
def find(self, x: int) -> int:
    """
    Path splitting: every node on the path points to its grandparent.

    Unlike halving, this visits and updates ALL nodes on the path
    (advancing to the original parent, not the new grandparent).
    Single pass, no recursion, same amortized complexity as full compression.
    """
    while self.parent[x] != x:
        next_x = self.parent[x]
        self.parent[x] = self.parent[next_x]  # Point to grandparent
        x = next_x
    return x
```

---

## Comparison of Techniques

```
Before: Chain 0 <- 1 <- 2 <- 3 <- 4 <- 5 <- 6 <- 7
parent = [0, 0, 1, 2, 3, 4, 5, 6]

Full compression after find(7):
parent = [0, 0, 0, 0, 0, 0, 0, 0]
Every node on the path points directly to root.

       0
   / / | \ \ \ \
  1 2  3  4 5 6 7

Path halving after find(7):
parent = [0, 0, 1, 1, 3, 3, 5, 5]
Nodes visited during traversal (7,5,3,1) each skip to grandparent.
Unvisited nodes (6,4,2) are unchanged.

        0
        |
        1
       / \
      2   3
         / \
        4   5
           / \
          6   7

Path splitting after find(7):
parent = [0, 0, 0, 1, 2, 3, 4, 5]
Every node on the path points to its original grandparent.
Unlike halving, splitting visits and updates ALL nodes on the path.

      0
     / \
    1   2
    |   |
    3   4
    |   |
    5   6
    |
    7
```

| Technique                    | Traversals | Stack    | Compression |
| ---------------------------- | ---------- | -------- | ----------- |
| Full compression (recursive) | 1 (+ backtrack) | O(depth) | Complete |
| Full compression (iterative) | 2 explicit | O(1)     | Complete    |
| Path halving                 | 1          | O(1)     | Partial     |
| Path splitting               | 1          | O(1)     | Partial     |

**Halving vs Splitting — the key difference:**

- **Path halving**: After updating `parent[x]` to grandparent, moves `x` to the _new_ parent (the grandparent), so it skips a node and visits ~half the path.
- **Path splitting**: After updating `parent[x]` to grandparent, moves `x` to the _old_ parent (next node), so it visits _every_ node on the path.
- Both achieve the same amortized O(α(n)) when combined with union by rank.

---

## Warm-Up: Path Compression on a Pre-Built Chain

**Problem**: Given a chain of N nodes (0←1←2←...←N-1), perform `find` operations and observe how path compression transforms the tree. This directly shows why path compression turns O(n) finds into O(1).

### Solution

```python
class UnionFindNoCompression:
    """Union-Find WITHOUT path compression — for comparison."""

    def __init__(self, n: int) -> None:
        self.parent: list[int] = list(range(n))

    def find(self, x: int) -> int:
        while self.parent[x] != x:
            x = self.parent[x]
        return x


class UnionFindWithCompression:
    """Union-Find WITH path compression."""

    def __init__(self, n: int) -> None:
        self.parent: list[int] = list(range(n))

    def find(self, x: int) -> int:
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]


def demonstrate_path_compression(n: int) -> None:
    """
    Build a worst-case chain, then show path compression in action.

    Time without compression: O(n) per find, O(n × q) total
    Time with compression:    O(n) first find, O(1) subsequent → O(n + q)
    """
    # Manually build a chain: 0 ← 1 ← 2 ← ... ← n-1
    # parent[i] = i-1 for i > 0
    chain_parent = [0] + list(range(n - 1))  # [0, 0, 1, 2, ..., n-2]

    # --- Without compression ---
    uf_no = UnionFindNoCompression(n)
    uf_no.parent = chain_parent[:]
    print("Chain (no compression):", uf_no.parent)

    uf_no.find(n - 1)  # Traverses entire chain
    print(f"After find({n - 1}) (no compression):", uf_no.parent)
    # parent unchanged! Still [0, 0, 1, 2, 3, 4, 5, 6]
    # Next find(n-1) will AGAIN traverse the full chain.

    # --- With compression ---
    uf_yes = UnionFindWithCompression(n)
    uf_yes.parent = chain_parent[:]
    print("\nChain (with compression):", uf_yes.parent)

    uf_yes.find(n - 1)  # Traverses chain AND compresses
    print(f"After find({n - 1}) (with compression):", uf_yes.parent)
    # parent = [0, 0, 0, 0, 0, 0, 0, 0]  — fully flat!
    # Every subsequent find is O(1).

    # Subsequent finds are instant
    uf_yes.find(n - 1)  # O(1)
    uf_yes.find(n // 2)  # O(1)
    print("All subsequent finds: O(1)")


demonstrate_path_compression(8)
# Output:
# Chain (no compression): [0, 0, 1, 2, 3, 4, 5, 6]
# After find(7) (no compression): [0, 0, 1, 2, 3, 4, 5, 6]  ← unchanged!
#
# Chain (with compression): [0, 0, 1, 2, 3, 4, 5, 6]
# After find(7) (with compression): [0, 0, 0, 0, 0, 0, 0, 0]  ← flat!
# All subsequent finds: O(1)
```

```
Before find(7):              After find(7) with compression:
       0                              0
       |                       / / | \ \ \ \
       1                      1  2  3  4 5 6 7
       |
       2                     Every node now points to root.
       |                     find(5) = O(1), find(7) = O(1)
       3
       |
       4                     Without compression?
       |                     Parent array unchanged.
       5                     find(7) is O(n) EVERY time.
       |
       6
       |
       7
```

---

## Problem: Number of Operations to Make Network Connected

**LeetCode 1319**: There are `n` computers numbered from `0` to `n - 1` connected by ethernet cables `connections[i] = [a, b]`. Return the minimum number of cables to move to connect all computers, or `-1` if impossible.

**Why this is a good path compression exercise**: With many union/find operations on a large graph, path compression is the difference between O(n²) and O(n × α(n)). This problem also reinforces counting connected components with Union-Find.

### Key Insight

- You need at least `n - 1` cables to connect `n` computers. If `len(connections) < n - 1`, return `-1`.
- Otherwise, count connected components `c`. You need exactly `c - 1` moves (each move connects two components).

### Solution

```python
def makeConnected(n: int, connections: list[list[int]]) -> int:
    """
    Count connected components via Union-Find, return components - 1.

    Time: O(E × α(n)) ≈ O(E) where E = len(connections)
    Space: O(n)
    """
    if len(connections) < n - 1:
        return -1  # Not enough cables

    parent = list(range(n))
    rank = [0] * n

    def find(x: int) -> int:
        if parent[x] != x:
            parent[x] = find(parent[x])  # Path compression
        return parent[x]

    def union(x: int, y: int) -> bool:
        rx, ry = find(x), find(y)
        if rx == ry:
            return False
        # Union by rank
        if rank[rx] < rank[ry]:
            rx, ry = ry, rx
        parent[ry] = rx
        if rank[rx] == rank[ry]:
            rank[rx] += 1
        return True

    components = n
    for a, b in connections:
        if union(a, b):
            components -= 1

    return components - 1


# Trace
# n=6, connections=[[0,1],[0,2],[0,3],[1,2],[1,3]]
# 5 cables, need at least 5 → OK
# Unions: {0,1}, {0,1,2}, {0,1,2,3} — 3 successful, 2 redundant
# components = 6 - 3 = 3 → groups: {0,1,2,3}, {4}, {5}
# Need 3 - 1 = 2 cable moves
print(makeConnected(6, [[0,1],[0,2],[0,3],[1,2],[1,3]]))  # 2
print(makeConnected(6, [[0,1],[0,2],[0,3],[1,2]]))         # -1 (only 4 cables < 5 needed)
```

---

## Problem: Longest Consecutive Sequence

**LeetCode 128**: Given an unsorted array of integers, find the length of the longest consecutive elements sequence.

### Example

```
Input: nums = [100, 4, 200, 1, 3, 2]
Output: 4
Explanation: The longest consecutive sequence is [1, 2, 3, 4].
```

### Union-Find Solution

```python
def longestConsecutive(nums: list[int]) -> int:
    """
    Use Union-Find to group consecutive numbers.

    Time: O(n × α(n)) ≈ O(n)
    Space: O(n)
    """
    if not nums:
        return 0

    parent = {}
    size = {}

    def find(x: int) -> int:
        """Find with lazy initialization — creates node on first access."""
        if x not in parent:
            parent[x] = x
            size[x] = 1
        if parent[x] != x:
            parent[x] = find(parent[x])  # Path compression
        return parent[x]

    def union(x: int, y: int) -> None:
        px, py = find(x), find(y)
        if px != py:
            # Union by size
            if size[px] < size[py]:
                px, py = py, px
            parent[py] = px
            size[px] += size[py]

    num_set = set(nums)

    for num in num_set:
        # Only need to check one direction to avoid duplicate work
        if num + 1 in num_set:
            union(num, num + 1)

    # Find maximum component size
    max_length = 1
    for num in num_set:
        root = find(num)
        max_length = max(max_length, size[root])

    return max_length


# Trace
nums = [100, 4, 200, 1, 3, 2]
# num_set = {1, 2, 3, 4, 100, 200}
# Unions: 1↔2, 2↔3, 3↔4 → component {1,2,3,4} has size 4
# 100 and 200 remain as singletons
print(longestConsecutive(nums))  # 4
```

---

## Problem: Satisfiability of Equality Equations

**LeetCode 990**: Given an array of equations like `["a==b","b!=c","c==a"]`, determine if all equations can be satisfied.

### Solution

```python
def equationsPossible(equations: list[str]) -> bool:
    """
    Use Union-Find: first union all equalities, then check inequalities.

    Time: O(n × α(26)) ≈ O(n)
    Space: O(26) = O(1)
    """
    parent = list(range(26))  # 26 letters

    def find(x: int) -> int:
        if parent[x] != x:
            parent[x] = find(parent[x])  # Path compression
        return parent[x]

    def union(x: int, y: int) -> None:
        parent[find(y)] = find(x)

    def char_to_idx(c: str) -> int:
        return ord(c) - ord('a')

    # First pass: process all equality equations
    for eq in equations:
        if eq[1] == '=':  # "a==b"
            x = char_to_idx(eq[0])
            y = char_to_idx(eq[3])
            union(x, y)

    # Second pass: check all inequality equations
    for eq in equations:
        if eq[1] == '!':  # "a!=b"
            x = char_to_idx(eq[0])
            y = char_to_idx(eq[3])
            if find(x) == find(y):
                return False  # Contradiction!

    return True


# Examples
print(equationsPossible(["a==b", "b!=a"]))  # False (a==b means a,b share a root, but b!=a contradicts that)
print(equationsPossible(["a==b", "b==c", "a==c"]))  # True
print(equationsPossible(["a==b", "b!=c", "c==a"]))  # False (a==b==c but b!=c)
```

---

## Problem: Lexicographically Smallest Equivalent String

**LeetCode 1061**: Given two strings `s1` and `s2` of the same length, and a string `baseStr`, return the lexicographically smallest equivalent string of `baseStr` by using the equivalence information from `s1` and `s2`. Characters at the same index in `s1` and `s2` are equivalent, and equivalence is transitive.

**Why this is a good path compression exercise**: Unlike standard Union-Find where root choice doesn't matter, here you must always keep the lexicographically smallest character as the root. Path compression then ensures that every character in an equivalence class quickly maps to the smallest member. This is one of the clearest examples of how root selection strategy interacts with path compression.

### Example

```
s1 = "parker", s2 = "morris", baseStr = "parser"
# p↔m, a↔o, r↔r, k↔r, e↔i, r↔s
# Equivalence classes: {m,p}, {a,o}, {k,r,s}, {e,i}
# Smallest in each:     m       a       k        e
# "parser" → m,a,k,k,e,k → "makkek"
Output: "makkek"
```

### Solution

```python
def smallestEquivalentString(s1: str, s2: str, baseStr: str) -> str:
    """
    Union-Find where the root of each component is always the
    smallest character. Path compression maps every character
    directly to its class's minimum.

    Time: O((n + m) * alpha(26)) ~ O(n + m) where n = len(s1), m = len(baseStr)
    Space: O(26) = O(1)
    """
    parent = list(range(26))

    def find(x: int) -> int:
        if parent[x] != x:
            parent[x] = find(parent[x])  # Path compression
        return parent[x]

    def union(x: int, y: int) -> None:
        rx, ry = find(x), find(y)
        if rx == ry:
            return
        # Always make the smaller character the root
        if rx < ry:
            parent[ry] = rx
        else:
            parent[rx] = ry

    for a, b in zip(s1, s2):
        union(ord(a) - ord('a'), ord(b) - ord('a'))

    result: list[str] = []
    for c in baseStr:
        root = find(ord(c) - ord('a'))
        result.append(chr(root + ord('a')))
    return ''.join(result)


# Trace through s1="parker", s2="morris", baseStr="parser"
# union(p,m): roots 15,12 → parent[15] = 12 (m < p, so m is root)
# union(a,o): roots 0,14  → parent[14] = 0  (a < o)
# union(r,r): same root, skip
# union(k,r): roots 10,17 → parent[17] = 10 (k < r)
# union(e,i): roots 4,8   → parent[8] = 4   (e < i)
# union(r,s): find(r)=find(17)=10(k), find(s)=18 → parent[18] = 10 (k < s)
#
# Now for "parser":
#   p → find(15) → 12 → 'm'
#   a → find(0)  → 0  → 'a'
#   r → find(17) → 10 → 'k'
#   s → find(18) → 10 → 'k' (path compressed through k)
#   e → find(4)  → 4  → 'e'
#   r → find(17) → 10 → 'k'
# Result: "makkek"
print(smallestEquivalentString("parker", "morris", "parser"))  # "makkek"
print(smallestEquivalentString("hello", "world", "hold"))      # "hdld"
```

---

## Problem: Evaluate Division (Path Compression with Weights)

**LeetCode 399**: You are given equations like `a / b = 2.0` and queries like `a / c = ?`. Return the answers to each query, or `-1.0` if undeterminable.

**Why this is the hardest path compression exercise here**: Path compression must accumulate weights (ratios) along the compressed path. When compressing `x → parent → grandparent → root` into `x → root`, you must multiply the weights along the entire chain (e.g., `weight[x] = weight[x] * weight[parent] * weight[grandparent] * ...`). The recursive implementation handles this naturally: each recursive call updates its level's weight before returning, so by the time we update `weight[x]`, `weight[parent[x]]` already reflects `parent[x] / root`. This directly connects to the "When NOT to Use Path Compression" section above.

### Example

```
equations = [["a","b"],["b","c"]]
values = [2.0, 3.0]
queries = [["a","c"],["b","a"],["a","e"],["a","a"],["x","x"]]

# a/b = 2.0, b/c = 3.0
# a/c = a/b * b/c = 6.0
# b/a = 1/2.0 = 0.5
# a/e = -1.0 (e unknown)
# a/a = 1.0
# x/x = -1.0 (x unknown)
Output: [6.0, 0.5, -1.0, 1.0, -1.0]
```

### Solution

```python
def calcEquation(
    equations: list[list[str]],
    values: list[float],
    queries: list[list[str]],
) -> list[float]:
    """
    Weighted Union-Find where weight[x] = x / parent[x].

    Path compression must multiply weights along the path so that
    after compression, weight[x] = x / root.

    Time: O((E + Q) × α(n)) ≈ O(E + Q)
    Space: O(n) where n = number of unique variables
    """
    parent: dict[str, str] = {}
    weight: dict[str, float] = {}  # weight[x] = x / parent[x]

    def find(x: str) -> str:
        if x not in parent:
            parent[x] = x
            weight[x] = 1.0

        if parent[x] != x:
            root = find(parent[x])
            # Before compression: weight[x] = x / parent[x]
            # weight[parent[x]] was just updated to parent[x] / root
            # After compression: weight[x] = x / root
            #                             = (x / parent[x]) * (parent[x] / root)
            weight[x] *= weight[parent[x]]
            parent[x] = root

        return parent[x]

    def union(a: str, b: str, val: float) -> None:
        """Record a / b = val."""
        root_a, root_b = find(a), find(b)
        if root_a == root_b:
            return
        parent[root_a] = root_b
        # We need: weight[root_a] = root_a / root_b
        # We know: weight[a] = a / root_a  →  root_a = a / weight[a]
        #          weight[b] = b / root_b  →  root_b = b / weight[b]
        #          val = a / b
        # root_a / root_b = (a / weight[a]) / (b / weight[b])
        #                 = (a/b) * (weight[b] / weight[a])
        #                 = val * weight[b] / weight[a]
        weight[root_a] = val * weight[b] / weight[a]

    # Build the weighted Union-Find
    for (a, b), val in zip(equations, values):
        union(a, b, val)

    # Answer queries
    results: list[float] = []
    for a, b in queries:
        if a not in parent or b not in parent:
            results.append(-1.0)
        elif find(a) != find(b):
            results.append(-1.0)
        else:
            # a / b = (a / root) / (b / root) = weight[a] / weight[b]
            results.append(weight[a] / weight[b])

    return results


# Trace
equations = [["a","b"],["b","c"]]
values = [2.0, 3.0]
queries = [["a","c"],["b","a"],["a","e"],["a","a"],["x","x"]]
print(calcEquation(equations, values, queries))
# [6.0, 0.5, -1.0, 1.0, -1.0]

# How path compression works here:
# After union(a, b, 2.0): parent = {a: b, b: b}, weight = {a: 2.0, b: 1.0}
# After union(b, c, 3.0): parent = {a: b, b: c, c: c}, weight = {a: 2.0, b: 3.0, c: 1.0}
# find(a):
#   parent[a] = b, not root → recurse to find(b)
#   find(b): parent[b] = c, not root → recurse to find(c)
#   find(c): parent[c] = c, root → return c
#   Back in find(b): weight[b] *= weight[c] → 3.0 * 1.0 = 3.0, parent[b] = c
#   Back in find(a): weight[a] *= weight[b] → 2.0 * 3.0 = 6.0, parent[a] = c
# Now weight[a] = 6.0 = a/c, weight[b] = 3.0 = b/c ← path fully compressed!
```

---

## Problem: Largest Component Size by Common Factor (Hard)

**LeetCode 952**: Given an array of unique positive integers `nums`, return the size of the largest connected component where two values are connected if they share a common factor > 1.

**Why this is a good path compression exercise**: With up to 20000 numbers each up to 100000, the naive approach of checking all pairs is O(n^2). Instead, we union each number with its prime factors, creating potentially deep trees. Without path compression, repeated `find` calls on factor-nodes would TLE. This is a case where path compression is the difference between AC and TLE.

### Example

```
Input: nums = [4, 6, 15, 35]
# 4 = 2*2, 6 = 2*3, 15 = 3*5, 35 = 5*7
# 4-6 share factor 2, 6-15 share factor 3, 15-35 share factor 5
# All connected transitively → component size = 4
Output: 4
```

### Solution

```python
from collections import Counter


def largestComponentSize(nums: list[int]) -> int:
    """
    Union each number with its prime factors, then count component sizes.

    Key trick: union numbers with factor-nodes (not with each other
    directly) to avoid O(n^2) pairwise comparison.

    Path compression is critical here: factor-nodes get unioned
    repeatedly, creating deep trees without compression.

    Time: O(n * sqrt(max_val) * alpha(n)) ~ O(n * sqrt(max_val))
    Space: O(n + max_val) for the parent map
    """
    parent: dict[int, int] = {}
    comp_size: dict[int, int] = {}

    def find(x: int) -> int:
        if x not in parent:
            parent[x] = x
            comp_size[x] = 1
        if parent[x] != x:
            parent[x] = find(parent[x])  # Path compression — critical for perf
        return parent[x]

    def union(x: int, y: int) -> None:
        rx, ry = find(x), find(y)
        if rx == ry:
            return
        # Union by size
        if comp_size[rx] < comp_size[ry]:
            rx, ry = ry, rx
        parent[ry] = rx
        comp_size[rx] += comp_size[ry]

    def prime_factors(n: int) -> list[int]:
        """Return unique prime factors of n."""
        factors: list[int] = []
        d = 2
        while d * d <= n:
            if n % d == 0:
                factors.append(d)
                while n % d == 0:
                    n //= d
            d += 1
        if n > 1:
            factors.append(n)
        return factors

    # Union each number with its prime factors
    # This implicitly connects numbers sharing a factor
    for num in nums:
        for factor in prime_factors(num):
            union(num, factor)

    # Count component sizes (only for actual nums, not factor-nodes)
    root_count: Counter[int] = Counter()
    for num in nums:
        root_count[find(num)] += 1

    return max(root_count.values())


# Trace for nums = [4, 6, 15, 35]:
# 4: factors [2] → union(4, 2)
# 6: factors [2, 3] → union(6, 2), union(6, 3) → 6 joins 4's component
# 15: factors [3, 5] → union(15, 3), union(15, 5) → 15 joins via factor 3
# 35: factors [5, 7] → union(35, 5), union(35, 7) → 35 joins via factor 5
# All nums share one root → component size = 4
print(largestComponentSize([4, 6, 15, 35]))    # 4
print(largestComponentSize([20, 50, 9, 63]))   # 2
print(largestComponentSize([2, 3, 6, 7, 4, 12, 21, 39]))  # 8
```

---

## Complexity Analysis

| Technique               | Single find | m operations on n elements |
| ----------------------- | ----------- | -------------------------- |
| No compression          | O(n)        | O(n × m)                   |
| Path compression only   | O(log n)\*  | O(m × log n)               |
| Path compression + rank | O(α(n))\*   | O(m × α(n))                |

\*Amortized

The improvement comes from flattening the tree:

- After one expensive find, subsequent finds to the same path are O(1)
- Trees stay shallow over time

---

## Why Path Compression Works

```
Amortized analysis intuition:

Consider a node x at depth d.
- First find(x): O(d) work, but compresses path
- After compression: x is at depth 1
- Future finds: O(1)

Total work for all finds to x: O(d + k) for k finds
Amortized per find: O(d/k + 1)

As we do more finds, the amortized cost approaches O(1).
```

---

## Edge Cases

1. **Self-find**: `find(x)` when x is root → returns immediately
2. **Already compressed**: No extra work if path already flat
3. **Single element**: Works correctly (element is own root)
4. **Deep recursion**: Use iterative version for very deep trees

---

## Interview Tips

1. **Default to recursive**: Cleaner code, usually acceptable
2. **Mention iterative**: Show you know the stack overflow concern
3. **Know the variants**: Path halving/splitting are single-pass alternatives worth mentioning
4. **Explain why it helps**: "Makes future finds faster by flattening the tree"

---

## Common Mistakes

1. **Forgetting to update parent**: `return find(self.parent[x])` without assignment

   ```python
   # Wrong
   def find(self, x: int) -> int:
       if self.parent[x] != x:
           return self.find(self.parent[x])  # Path not compressed!
       return x

   # Correct
   def find(self, x: int) -> int:
       if self.parent[x] != x:
           self.parent[x] = self.find(self.parent[x])  # Compress!
       return self.parent[x]
   ```

2. **Return wrong value**: Must return `parent[x]` after update, not `x`
   ```python
   # Wrong
   def find(self, x: int) -> int:
       if self.parent[x] != x:
           self.parent[x] = self.find(self.parent[x])
       return x  # Wrong! Should return parent[x]
   ```

---

## Practice Problems

| #   | Problem                                        | Difficulty | Key Concept                             |
| --- | ---------------------------------------------- | ---------- | --------------------------------------- |
| 1   | Number of Operations to Make Network Connected | Medium     | Count components, path compress         |
| 2   | Longest Consecutive Sequence                   | Medium     | Union consecutive numbers               |
| 3   | Satisfiability of Equality Equations           | Medium     | Two-pass union then check               |
| 4   | Lexicographically Smallest Equivalent (LC 1061)| Medium     | Root selection interacts with compression|
| 5   | Evaluate Division (LC 399)                     | Medium     | Weighted UF, path compression + weights |
| 6   | Largest Component Size by Common Factor (LC 952)| Hard      | Factor-node union, compression critical |
| 7   | Smallest String With Swaps                     | Medium     | Group characters by index               |
| 8   | Regions Cut By Slashes                         | Medium     | Grid subdivision                        |

---

## Related Sections

- [Union-Find Basics](./01-union-find-basics.md) - Foundation
- [Union by Rank](./03-union-by-rank.md) - Second optimization
- [Connected Components](./04-connected-components.md) - Application

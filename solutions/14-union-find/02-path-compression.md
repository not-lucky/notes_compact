# Path Compression Solutions

## 1. Longest Consecutive Sequence

**Problem Statement**:
Given an unsorted array of integers `nums`, return the length of the longest consecutive elements sequence. The algorithm must run in $O(n)$ time.

**Examples & Edge Cases**:

- **Example 1**: `nums = [100, 4, 200, 1, 3, 2]` → `4` (The sequence is `[1, 2, 3, 4]`).
- **Example 2**: `nums = [0, 3, 7, 2, 5, 8, 4, 6, 0, 1]` → `9`.
- **Edge Case**: Empty array → `0`.
- **Edge Case**: Array with one element → `1`.
- **Edge Case**: Duplicate elements → Should only count unique elements once.

**Optimal Python Solution**:

```python
def longestConsecutive(nums: list[int]) -> int:
    if not nums:
        return 0

    num_set = set(nums)
    parent = {num: num for num in num_set}
    size = {num: 1 for num in num_set}

    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x]) # Path compression
        return parent[x]

    def union(x, y):
        root_x = find(x)
        root_y = find(y)
        if root_x != root_y:
            # Union by size
            if size[root_x] < size[root_y]:
                root_x, root_y = root_y, root_x
            parent[root_y] = root_x
            size[root_x] += size[root_y]

    for num in num_set:
        if num + 1 in num_set:
            union(num, num + 1)

    return max(size.values()) if size else 0
```

**Explanation**:

1. We use a hash set to store unique numbers for $O(1)$ lookups.
2. We use Union-Find where each number points to itself initially.
3. For each number `num` in the set, if `num + 1` also exists, we `union` them.
4. Path compression ensures that the `find` operation is efficient.
5. We track the size of each component (consecutive sequence) and return the maximum size.

**Complexity Analysis**:

- **Time Complexity**: $O(n \alpha(n))$, where $n$ is the number of elements. Each number is processed once, and union/find operations are nearly constant.
- **Space Complexity**: $O(n)$ to store the set and Union-Find structures.

---

## 2. Satisfiability of Equality Equations

**Problem Statement**:
Given an array of strings `equations` that represent relationships between variables where each string is of length 4 and takes one of two forms: `"a==b"` or `"a!=b"`. Return `True` if it is possible to assign integers to variable names so as to satisfy all the given equations, or `False` otherwise.

**Examples & Edge Cases**:

- **Example 1**: `["a==b","b!=a"]` → `False`.
- **Example 2**: `["b==a","a==b"]` → `True`.
- **Edge Case**: Self-contradiction `["a!=a"]` → `False`.
- **Edge Case**: Transitive contradiction `["a==b","b==c","a!=c"]` → `False`.

**Optimal Python Solution**:

```python
def equationsPossible(equations: list[str]) -> bool:
    parent = list(range(26))

    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x]) # Path compression
        return parent[x]

    def union(x, y):
        root_x = find(x)
        root_y = find(y)
        if root_x != root_y:
            parent[root_x] = root_y

    # First pass: Process all "==" equations to group equal variables
    for eq in equations:
        if eq[1] == '=':
            union(ord(eq[0]) - ord('a'), ord(eq[3]) - ord('a'))

    # Second pass: Check if any "!=" equation is violated
    for eq in equations:
        if eq[1] == '!':
            if find(ord(eq[0]) - ord('a')) == find(ord(eq[3]) - ord('a')):
                return False

    return True
```

**Explanation**:

1. Equality is an equivalence relation (reflexive, symmetric, transitive), which maps perfectly to Union-Find.
2. In the first pass, we `union` variables that are explicitly equal.
3. In the second pass, we check the `"!= "` equations. If two variables are supposed to be unequal but they share the same root in our Union-Find structure, it means they are transitively equal, causing a contradiction.

**Complexity Analysis**:

- **Time Complexity**: $O(n \alpha(26)) \approx O(n)$, where $n$ is the number of equations.
- **Space Complexity**: $O(26) = O(1)$ for the parent array of fixed size.

---

## 3. Number of Operations to Make Network Connected

**Problem Statement**:
There are `n` computers and a list of `connections`. You can extract a cable from one pair of connected computers and connect another pair of disconnected computers. Find the minimum number of operations to make all computers connected. If it's impossible, return -1.

**Examples & Edge Cases**:

- **Example 1**: `n = 4, connections = [[0,1],[0,2],[1,2]]` → `1`.
- **Example 2**: `n = 6, connections = [[0,1],[0,2],[0,3],[1,2],[1,3]]` → `2`.
- **Edge Case**: `len(connections) < n - 1` → `-1` (Not enough cables).

**Optimal Python Solution**:

```python
def makeConnected(n: int, connections: list[list[int]]) -> int:
    # A graph with n nodes needs at least n-1 edges to be connected
    if len(connections) < n - 1:
        return -1

    parent = list(range(n))
    num_components = n
    rank = [0] * n

    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x]) # Path compression
        return parent[x]

    def union(x, y):
        nonlocal num_components
        root_x = find(x)
        root_y = find(y)
        if root_x != root_y:
            if rank[root_x] < rank[root_y]:
                parent[root_x] = root_y
            elif rank[root_x] > rank[root_y]:
                parent[root_y] = root_x
            else:
                parent[root_x] = root_y
                rank[root_y] += 1
            num_components -= 1
            return True
        return False

    for u, v in connections:
        union(u, v)

    # We need (num_components - 1) edges to connect all components
    return num_components - 1
```

**Explanation**:

1. To connect `n` nodes, we need at least `n-1` edges. If `len(connections) < n - 1`, we return `-1`.
2. We use Union-Find to count the number of connected components.
3. Every time we perform a successful `union`, the number of components decreases.
4. If we have `k` components, we need exactly `k-1` additional edges to connect them all. Since we already verified we have enough edges total, we can just move redundant edges to connect the components.

**Complexity Analysis**:

- **Time Complexity**: $O(E \alpha(n))$, where $E$ is the number of connections.
- **Space Complexity**: $O(n)$ for the parent array.

---

## 4. Smallest String With Swaps

**Problem Statement**:
Given a string `s` and an array of `pairs` where `pairs[i] = [a, b]` denotes that you can swap the characters at indices `a` and `b`. You can apply the swap any number of times. Return the lexicographically smallest string that `s` can be changed to.

**Examples & Edge Cases**:

- **Example 1**: `s = "dcab", pairs = [[0,3],[1,2]]` → `"bacd"`.
- **Example 2**: `s = "dcab", pairs = [[0,3],[1,2],[0,2]]` → `"abcd"`.
- **Edge Case**: No pairs → Return original string.
- **Edge Case**: All characters can be swapped → Return sorted string.

**Optimal Python Solution**:

```python
from collections import defaultdict

def smallestStringWithSwaps(s: str, pairs: list[list[int]]) -> str:
    n = len(s)
    parent = list(range(n))
    rank = [0] * n

    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x]) # Path compression
        return parent[x]

    def union(x, y):
        root_x = find(x)
        root_y = find(y)
        if root_x != root_y:
            if rank[root_x] < rank[root_y]:
                parent[root_x] = root_y
            elif rank[root_x] > rank[root_y]:
                parent[root_y] = root_x
            else:
                parent[root_x] = root_y
                rank[root_y] += 1

    # Group all indices that can be swapped with each other
    for u, v in pairs:
        union(u, v)

    # Collect characters for each group
    groups = defaultdict(list)
    for i in range(n):
        groups[find(i)].append(i)

    res = [''] * n
    for group_indices in groups.values():
        # Get characters at these indices and sort them
        chars = sorted([s[i] for i in group_indices])
        # Sort indices to place sorted characters back in correct positions
        for idx, char in zip(sorted(group_indices), chars):
            res[idx] = char

    return "".join(res)
```

**Explanation**:

1. If we can swap index `a` with `b` and `b` with `c`, we can effectively move any character among positions `a`, `b`, and `c` to any other position within that set.
2. This defines a connected component of indices. Within each component, we can sort the characters to get the lexicographically smallest result.
3. We use Union-Find to group indices.
4. For each group, we extract the characters, sort them, and place them back into the original indices in sorted order.

**Complexity Analysis**:

- **Time Complexity**: $O(P \alpha(n) + n \log n)$, where $P$ is the number of pairs and $n$ is string length. Sorting characters in groups takes $O(n \log n)$ total.
- **Space Complexity**: $O(n)$ to store groups and parent array.

---

## 5. Regions Cut By Slashes

**Problem Statement**:
An `n x n` grid is composed of `1 x 1` squares where each square contains a '/', '\', or blank space. These characters divide the square into regions. Return the total number of regions.

**Examples & Edge Cases**:

- **Example 1**: `grid = [" /","/ "]` → `2`.
- **Example 2**: `grid = [" /","  "]` → `1`.
- **Edge Case**: `n = 1`, `grid = ["/"]` → `2`.
- **Edge Case**: All blank → `1`.

**Optimal Python Solution**:

```python
def regionsBySlashes(grid: list[str]) -> int:
    n = len(grid)
    # Each 1x1 square is divided into 4 triangles: 0 (top), 1 (right), 2 (bottom), 3 (left)
    parent = list(range(4 * n * n))
    rank = [0] * (4 * n * n)
    count = 4 * n * n

    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    def union(x, y):
        nonlocal count
        root_x = find(x)
        root_y = find(y)
        if root_x != root_y:
            if rank[root_x] < rank[root_y]:
                parent[root_x] = root_y
            elif rank[root_x] > rank[root_y]:
                parent[root_y] = root_x
            else:
                parent[root_x] = root_y
                rank[root_y] += 1
            count -= 1

    for r in range(n):
        for c in range(n):
            root = 4 * (r * n + c)
            val = grid[r][c]

            # Internal connections within a 1x1 cell
            if val == ' ':
                union(root + 0, root + 1)
                union(root + 1, root + 2)
                union(root + 2, root + 3)
            elif val == '/':
                union(root + 0, root + 3)
                union(root + 1, root + 2)
            elif val == '\\':
                union(root + 0, root + 1)
                union(root + 2, root + 3)

            # External connections between adjacent cells
            # Connect bottom of current to top of below
            if r + 1 < n:
                union(root + 2, 4 * ((r + 1) * n + c) + 0)
            # Connect right of current to left of right
            if c + 1 < n:
                union(root + 1, 4 * (r * n + (c + 1)) + 3)

    return count
```

**Explanation**:

1. We divide each `1x1` square into 4 small triangles (Top, Right, Bottom, Left).
2. A blank space connects all 4 triangles.
3. A `/` connects (Top, Left) and (Bottom, Right).
4. A `\` connects (Top, Right) and (Bottom, Left).
5. We also connect triangles between adjacent cells: Bottom of `(r, c)` to Top of `(r+1, c)`, and Right of `(r, c)` to Left of `(r, c+1)`.
6. Each `union` operation reduces the total number of regions. We start with $4n^2$ regions and decrement for every successful merge.

**Complexity Analysis**:

- **Time Complexity**: $O(n^2 \alpha(n^2))$, as we process each cell once.
- **Space Complexity**: $O(n^2)$ for the parent array of size $4n^2$.

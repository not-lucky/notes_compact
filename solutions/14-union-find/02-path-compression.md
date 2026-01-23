# Practice Problems: Path Compression

## Problem 1: Longest Consecutive Sequence
**LeetCode 128**

### Problem Statement
Given an unsorted array of integers `nums`, return the length of the longest consecutive elements sequence.

You must write an algorithm that runs in `O(n)` time.

### Constraints
- `0 <= nums.length <= 10^5`
- `-10^9 <= nums[i] <= 10^9`

### Example
**Input:** `nums = [100,4,200,1,3,2]`
**Output:** `4`
**Explanation:** The longest consecutive elements sequence is `[1, 2, 3, 4]`. Therefore its length is 4.

### Python Implementation
```python
class UnionFind:
    def __init__(self, elements):
        self.parent = {el: el for el in elements}
        self.size = {el: 1 for el in elements}
        self.max_size = 1 if elements else 0

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x]) # Path compression
        return self.parent[x]

    def union(self, x, y):
        root_x = self.find(x)
        root_y = self.find(y)
        if root_x != root_y:
            # Union by size
            if self.size[root_x] < self.size[root_y]:
                root_x, root_y = root_y, root_x
            self.parent[root_y] = root_x
            self.size[root_x] += self.size[root_y]
            self.max_size = max(self.max_size, self.size[root_x])

def longestConsecutive(nums: list[int]) -> int:
    if not nums:
        return 0

    num_set = set(nums)
    uf = UnionFind(num_set)

    for num in num_set:
        if num + 1 in num_set:
            uf.union(num, num + 1)

    return uf.max_size
```

---

## Problem 2: Satisfiability of Equality Equations
**LeetCode 990**

### Problem Statement
You are given an array of strings `equations` that represent relationships between variables where each string `equations[i]` is of length 4 and takes one of two forms: `"xi==yi"` or `"xi!=yi"`. Here, `xi` and `yi` are lowercase letters (variable names) that represent integers.

Return `true` if it is possible to assign integers to variable names so as to satisfy all the given equations, or `false` otherwise.

### Constraints
- `1 <= equations.length <= 500`
- `equations[i].length == 4`
- `equations[i][0]` and `equations[i][3]` are lowercase letters.
- `equations[i][1]` is either `'='` or `'!'`.
- `equations[i][2]` is `'='`.

### Example
**Input:** `equations = ["a==b","b!=a"]`
**Output:** `false`

### Python Implementation
```python
class UnionFind:
    def __init__(self):
        self.parent = list(range(26))

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x]) # Path compression
        return self.parent[x]

    def union(self, x, y):
        root_x = self.find(x)
        root_y = self.find(y)
        if root_x != root_y:
            self.parent[root_x] = root_y

def equationsPossible(equations: list[str]) -> bool:
    uf = UnionFind()

    # First pass: process all equalities
    for eq in equations:
        if eq[1] == '=':
            u = ord(eq[0]) - ord('a')
            v = ord(eq[3]) - ord('a')
            uf.union(u, v)

    # Second pass: check inequalities
    for eq in equations:
        if eq[1] == '!':
            u = ord(eq[0]) - ord('a')
            v = ord(eq[3]) - ord('a')
            if uf.find(u) == uf.find(v):
                return False

    return True
```

---

## Problem 3: Number of Operations to Make Network Connected
**LeetCode 1319**

### Problem Statement
There are `n` computers numbered from `0` to `n - 1` connected by ethernet cables `connections` where `connections[i] = [ai, bi]` represents a connection between computers `ai` and `bi`. Any computer can reach any other computer directly or indirectly through the network.

You are given an initial computer network `connections`. You can extract certain cables between two directly connected computers, and place them between any two unconnected computers to make them directly connected.

Return the minimum number of times you need to do this in order to make all the computers connected. If it is not possible, return `-1`.

### Constraints
- `1 <= n <= 10^5`
- `1 <= connections.length <= min(n * (n - 1) / 2, 10^5)`
- `connections[i].length == 2`
- `0 <= ai, bi < n`
- `ai != bi`
- There are no repeated connections.
- No two computers are connected by more than one cable.

### Example
**Input:** `n = 4`, `connections = [[0,1],[0,2],[1,2]]`
**Output:** `1`

### Python Implementation
```python
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.components = n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        root_x = self.find(x)
        root_y = self.find(y)
        if root_x != root_y:
            self.parent[root_x] = root_y
            self.components -= 1
            return True
        return False

def makeConnected(n: int, connections: list[list[int]]) -> int:
    if len(connections) < n - 1:
        return -1

    uf = UnionFind(n)
    for u, v in connections:
        uf.union(u, v)

    return uf.components - 1
```

---

## Problem 4: Smallest String With Swaps
**LeetCode 1202**

### Problem Statement
You are given a string `s`, and an array of pairs of indices in the string `pairs` where `pairs[i] = [a, b]` indicates 2 indices (0-indexed) of the string.

You can swap the characters at any pair of indices in the given `pairs` any number of times.

Return the lexicographically smallest string that `s` can be changed to after using the swaps.

### Constraints
- `1 <= s.length <= 10^5`
- `0 <= pairs.length <= 10^5`
- `0 <= pairs[i][0], pairs[i][1] < s.length`
- `s` contains only lowercase English letters.

### Example
**Input:** `s = "dcab"`, `pairs = [[0,3],[1,2]]`
**Output:** `"bacd"`

### Python Implementation
```python
import collections

class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        root_x = self.find(x)
        root_y = self.find(y)
        if root_x != root_y:
            self.parent[root_x] = root_y

def smallestStringWithSwaps(s: str, pairs: list[list[int]]) -> str:
    n = len(s)
    uf = UnionFind(n)
    for u, v in pairs:
        uf.union(u, v)

    groups = collections.defaultdict(list)
    for i in range(n):
        groups[uf.find(i)].append(i)

    res = [''] * n
    for root in groups:
        indices = groups[root]
        chars = sorted([s[i] for i in indices])
        indices.sort()
        for i, char in zip(indices, chars):
            res[i] = char

    return "".join(res)
```

---

## Problem 5: Regions Cut By Slashes
**LeetCode 959**

### Problem Statement
An `n x n` grid is composed of `1 x 1` squares where each `1 x 1` square consists of a `'/'`, `'\'`, or blank space `' '`. These characters divide the square into contiguous regions.

Given the grid `grid` represented as a string array, return the number of regions.

Note that backslash characters are escaped, so a `'\'` is represented as `'\\'`.

### Constraints
- `n == grid.length == grid[i].length`
- `1 <= n <= 30`
- `grid[i][j]` is either `'/'`, `'\\'`, or `' '`.

### Example
**Input:** `grid = [" /","/ "]`
**Output:** `2`

### Python Implementation
```python
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.count = n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        root_x = self.find(x)
        root_y = self.find(y)
        if root_x != root_y:
            self.parent[root_x] = root_y
            self.count -= 1

def regionsBySlashes(grid: list[str]) -> int:
    n = len(grid)
    # Divide each cell into 4 triangles: 0 (top), 1 (right), 2 (bottom), 3 (left)
    uf = UnionFind(4 * n * n)

    for r in range(n):
        for c in range(n):
            root = 4 * (r * n + c)
            val = grid[r][c]

            # Internal unions within a cell
            if val == ' ':
                uf.union(root + 0, root + 1)
                uf.union(root + 1, root + 2)
                uf.union(root + 2, root + 3)
            elif val == '/':
                uf.union(root + 0, root + 3)
                uf.union(root + 1, root + 2)
            elif val == '\\':
                uf.union(root + 0, root + 1)
                uf.union(root + 2, root + 3)

            # External unions between cells
            # Connect bottom of current with top of cell below
            if r + 1 < n:
                uf.union(root + 2, 4 * ((r + 1) * n + c) + 0)
            # Connect right of current with left of cell to the right
            if c + 1 < n:
                uf.union(root + 1, 4 * (r * n + (c + 1)) + 3)

    return uf.count
```

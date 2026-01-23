# Practice Problems: Connected Components

## Problem 1: Number of Islands II
**LeetCode 305**

### Problem Statement
You are given an empty 2D binary grid of size `m x n`. The grid represents a map where `0` is water and `1` is land. Initially, all cells are water.

We perform `addLand` operations which turn the water at `position[i]` into land. Given a list of positions to operate, return an array of integers `answer` where `answer[i]` is the number of islands after the `ith` operation.

An **island** is formed by connecting adjacent lands 4-directionally.

### Constraints
- `1 <= m, n, positions.length <= 10^4`
- `1 <= m * n <= 10^4`
- `positions[i].length == 2`
- `0 <= ri < m`
- `0 <= ci < n`

### Example
**Input:** `m = 3, n = 3, positions = [[0,0],[0,1],[1,2],[2,1]]`
**Output:** `[1,1,2,3]`

### Python Implementation
```python
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.count = 0
        self.is_land = [False] * n

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

def numIslands2(m: int, n: int, positions: list[list[int]]) -> list[int]:
    uf = UnionFind(m * n)
    res = []
    for r, c in positions:
        idx = r * n + c
        if not uf.is_land[idx]:
            uf.is_land[idx] = True
            uf.count += 1
            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < m and 0 <= nc < n and uf.is_land[nr * n + nc]:
                    uf.union(idx, nr * n + nc)
        res.append(uf.count)
    return res
```

---

## Problem 2: Lexicographically Smallest Equivalent String
**LeetCode 1061**

### Problem Statement
You are given two strings `s1` and `s2` of the same length and a string `baseStr`.

Say `s1[i]` and `s2[i]` are equivalent characters. For example, if `s1 = "abc"` and `s2 = "cde"`, then we have `'a' == 'c'`, `'b' == 'd'`, and `'c' == 'e'`.

Equivalent characters follow the usual rules of any equivalence relation:
- Reflexivity: `'a' == 'a'`.
- Symmetry: `'a' == 'b'` implies `'b' == 'a'`.
- Transitivity: `'a' == 'b'` and `'b' == 'c'` implies `'a' == 'c'`.

For example, given the equivalency information from `s1 = "abc"` and `s2 = "cde"`, `'a'`, `'c'`, and `'e'` are all equivalent and `'b'` and `'d'` are equivalent.

Return the lexicographically smallest equivalent string of `baseStr` by using the equivalency information from `s1` and `s2`.

### Constraints
- `1 <= s1.length, s2.length, baseStr.length <= 1000`
- `s1.length == s2.length`
- `s1`, `s2`, and `baseStr` consist of lowercase English letters.

### Example
**Input:** `s1 = "parker", s2 = "morris", baseStr = "parser"`
**Output:** `"makkek"`

### Python Implementation
```python
class UnionFind:
    def __init__(self):
        self.parent = list(range(26))

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        root_x = self.find(x)
        root_y = self.find(y)
        if root_x != root_y:
            # Always make the smaller character the root
            if root_x < root_y:
                self.parent[root_y] = root_x
            else:
                self.parent[root_x] = root_y

def smallestEquivalentString(s1: str, s2: str, baseStr: str) -> str:
    uf = UnionFind()
    for c1, c2 in zip(s1, s2):
        uf.union(ord(c1) - ord('a'), ord(c2) - ord('a'))

    res = []
    for c in baseStr:
        root = uf.find(ord(c) - ord('a'))
        res.append(chr(root + ord('a')))

    return "".join(res)
```

---

## Problem 3: Checking Existence of Edge Length Limited Paths
**LeetCode 1697**

### Problem Statement
An undirected graph of `n` nodes is defined by `edgeList`, where `edgeList[i] = [ui, vi, disi]` denotes an edge between nodes `ui` and `vi` with distance `disi`. Note that there may be multiple edges between two nodes.

Given an array `queries`, where `queries[j] = [pj, qj, limitj]`, your task is to determine for each query `queries[j]` whether there is a path between `pj` and `qj` such that each edge on the path has a distance strictly less than `limitj`.

Return a boolean array `answer`, where `answer.length == queries.length` and the `jth` value of `answer` is `true` if there is a path for `queries[j]`.

### Constraints
- `2 <= n <= 10^5`
- `1 <= edgeList.length, queries.length <= 10^5`
- `edgeList[i].length == 3`
- `queries[j].length == 3`
- `0 <= ui, vi, pj, qj <= n - 1`
- `ui != vi`, `pj != qj`
- `1 <= disi, limitj <= 10^9`

### Example
**Input:** `n = 3, edgeList = [[0,1,2],[1,2,4],[2,0,8]], queries = [[0,1,2],[0,2,5]]`
**Output:** `[false,true]`

### Python Implementation
```python
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

def distanceLimitedPathsExist(n: int, edgeList: list[list[int]], queries: list[list[int]]) -> list[bool]:
    edgeList.sort(key=lambda x: x[2])
    # Add index to queries to restore original order
    indexed_queries = sorted([(q[0], q[1], q[2], i) for i, q in enumerate(queries)], key=lambda x: x[2])

    uf = UnionFind(n)
    res = [False] * len(queries)
    edge_idx = 0

    for u, v, limit, original_idx in indexed_queries:
        while edge_idx < len(edgeList) and edgeList[edge_idx][2] < limit:
            uf.union(edgeList[edge_idx][0], edgeList[edge_idx][1])
            edge_idx += 1
        res[original_idx] = uf.find(u) == uf.find(v)

    return res
```
---

## Problem 4: Synonymous Sentences
**LeetCode 1258**

### Problem Statement
You are given a list of equivalent string pairs `synonyms` and a sentence `text`.

Return all possible synonymous sentences sorted lexicographically.

### Constraints
- `0 <= synonyms.length <= 10`
- `synonyms[i].length == 2`
- `synonyms[0] != synonyms[1]`
- All words consist of English letters only.
- `text` contains at most 10 words.
- The total number of sentences is at most 1000.

### Example
**Input:** `synonyms = [["cheerful","glad"],["glad","very_happy"]], text = "I am cheerful"`
**Output:** `["I am cheerful","I am glad","I am very_happy"]`

### Python Implementation
```python
import collections

class UnionFind:
    def __init__(self):
        self.parent = {}

    def find(self, x):
        if x not in self.parent:
            self.parent[x] = x
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        root_x = self.find(x)
        root_y = self.find(y)
        if root_x != root_y:
            self.parent[root_x] = root_y

def generateSentences(synonyms: list[list[str]], text: str) -> list[str]:
    uf = UnionFind()
    for u, v in synonyms:
        uf.union(u, v)

    groups = collections.defaultdict(list)
    # Collect all words involved in synonyms
    words_in_synonyms = set()
    for u, v in synonyms:
        words_in_synonyms.add(u)
        words_in_synonyms.add(v)

    for word in words_in_synonyms:
        groups[uf.find(word)].append(word)

    for root in groups:
        groups[root].sort()

    words = text.split()
    res = []

    def backtrack(idx, current_sentence):
        if idx == len(words):
            res.append(" ".join(current_sentence))
            return

        word = words[idx]
        if word not in words_in_synonyms:
            backtrack(idx + 1, current_sentence + [word])
        else:
            root = uf.find(word)
            for synonym in groups[root]:
                backtrack(idx + 1, current_sentence + [synonym])

    backtrack(0, [])
    return sorted(res)
```
---

## Problem 5: Evaluate Division
**LeetCode 399**

### Problem Statement
You are given an array of variable pairs `equations` and an array of real numbers `values`, where `equations[i] = [Ai, Bi]` and `values[i]` represent the equation `Ai / Bi = values[i]`. Each `Ai` or `Bi` is a string that represents a single variable.

You are also given some `queries`, where `queries[j] = [Cj, Dj]` represents the `jth` query where you must find the answer for `Cj / Dj = ?`.

Return the answers to all queries. If a single answer cannot be determined, return `-1.0`.

Note: The input is always valid. You may assume that evaluating the queries will not result in division by zero and that there is no contradiction.

Note: The variables that do not occur in the list of equations are undefined, so the answer cannot be determined for them.

### Constraints
- `1 <= equations.length <= 20`
- `equations[i].length == 2`
- `values.length == equations.length`
- `0.0 < values[i] <= 20.0`
- `1 <= queries.length <= 20`
- `queries[i].length == 2`
- `Ai, Bi, Cj, Dj` consist of lower case English letters and have length between 1 and 5.

### Example
**Input:** `equations = [["a","b"],["b","c"]], values = [2.0,3.0], queries = [["a","c"],["b","a"],["a","e"],["a","a"],["x","x"]]`
**Output:** `[6.0,0.5,-1.0,1.0,-1.0]`

### Python Implementation
```python
class UnionFind:
    def __init__(self):
        self.parent = {}
        self.ratio = {} # ratio[x] = x / parent[x]

    def find(self, x):
        if x not in self.parent:
            self.parent[x] = x
            self.ratio[x] = 1.0
        if self.parent[x] != x:
            original_parent = self.parent[x]
            root = self.find(original_parent)
            self.parent[x] = root
            self.ratio[x] *= self.ratio[original_parent]
        return self.parent[x]

    def union(self, x, y, val):
        root_x = self.find(x)
        root_y = self.find(y)
        if root_x != root_y:
            # x / root_x = ratio[x]
            # y / root_y = ratio[y]
            # x / y = val
            # root_x / root_y = (x / ratio[x]) / (y / ratio[y]) = (x / y) * (ratio[y] / ratio[x]) = val * ratio[y] / ratio[x]
            self.parent[root_x] = root_y
            self.ratio[root_x] = val * self.ratio[y] / self.ratio[x]

def calcEquation(equations: list[list[str]], values: list[float], queries: list[list[str]]) -> list[float]:
    uf = UnionFind()
    for (u, v), val in zip(equations, values):
        uf.union(u, v, val)

    res = []
    for u, v in queries:
        if u not in uf.parent or v not in uf.parent:
            res.append(-1.0)
        else:
            root_u = uf.find(u)
            root_v = uf.find(v)
            if root_u != root_v:
                res.append(-1.0)
            else:
                # u / root_u = ratio[u]
                # v / root_v = ratio[v]
                # root_u == root_v
                # u / v = (u / root_u) / (v / root_v) = ratio[u] / ratio[v]
                res.append(uf.ratio[u] / uf.ratio[v])
    return res
```

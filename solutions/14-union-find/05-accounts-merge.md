# Accounts Merge Solutions

## 1. Accounts Merge

**Problem Statement**:
Given a list of `accounts` where each element `accounts[i]` is a list of strings, the first element `accounts[i][0]` is a name, and the rest of the elements are emails belonging to that account. If two accounts share an email, they belong to the same person. Merge the accounts and return the result with emails sorted.

**Examples & Edge Cases**:

- **Example 1**: `accounts = [["John","johnsmith@mail.com","john_newyork@mail.com"],["John","johnsmith@mail.com","john00@mail.com"],["Mary","mary@mail.com"],["John","johnnybravo@mail.com"]]` → `[["John","john00@mail.com","john_newyork@mail.com","johnsmith@mail.com"],["Mary","mary@mail.com"],["John","johnnybravo@mail.com"]]`.
- **Edge Case**: Multiple people with the same name but different emails.
- **Edge Case**: One person with many accounts that link together transitively.

**Optimal Python Solution**:

```python
from collections import defaultdict

def accountsMerge(accounts: list[list[str]]) -> list[list[str]]:
    parent = {}
    rank = {}
    email_to_name = {}

    def find(x):
        if x not in parent:
            parent[x] = x
            rank[x] = 0
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    def union(x, y):
        root_x, root_y = find(x), find(y)
        if root_x != root_y:
            if rank[root_x] < rank[root_y]:
                parent[root_x] = root_y
            elif rank[root_x] > rank[root_y]:
                parent[root_y] = root_x
            else:
                parent[root_x] = root_y
                rank[root_y] += 1

    # 1. Initialize Union-Find and map emails to names
    for account in accounts:
        name = account[0]
        first_email = account[1]
        for email in account[1:]:
            if email not in parent:
                parent[email] = email
            email_to_name[email] = name
            union(first_email, email)

    # 2. Group emails by their root parent
    groups = defaultdict(list)
    for email in parent:
        root = find(email)
        groups[root].append(email)

    # 3. Format result
    res = []
    for root, emails in groups.items():
        res.append([email_to_name[root]] + sorted(emails))

    return res
```

**Explanation**:

1. We use emails as nodes in our Union-Find structure.
2. For each account, we `union` all its emails together. This handles transitive merging automatically (if Account A shares an email with Account B, all emails from both merge into one set).
3. We maintain an `email_to_name` mapping because while emails are unique identifiers, names are not.
4. Finally, we group all emails by their representative (root) and sort them.

**Complexity Analysis**:

- **Time Complexity**: $O(NK \log(NK))$, where $N$ is number of accounts and $K$ is max emails. Sorting emails is the dominant part. Union-Find operations are $O(NK \alpha(NK))$.
- **Space Complexity**: $O(NK)$ to store the email mappings and Union-Find structure.

---

## 2. Similar String Groups

**Problem Statement**:
Two strings `X` and `Y` are similar if we can swap two letters in `X` to get `Y`. Given a list of strings `strs`, group them such that strings in the same group are similar (directly or indirectly). Return the number of groups.

**Examples & Edge Cases**:

- **Example 1**: `strs = ["tars","rats","arts","star"]` → `2` (`"tars","rats","arts"` are similar, `"star"` is separate).
- **Edge Case**: `n = 1` → `1`.
- **Edge Case**: All strings are identical.

**Optimal Python Solution**:

```python
def numSimilarGroups(strs: list[str]) -> int:
    n = len(strs)
    parent = list(range(n))
    rank = [0] * n
    count = n

    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    def union(x, y):
        nonlocal count
        rx, ry = find(x), find(y)
        if rx != ry:
            if rank[rx] < rank[ry]:
                parent[rx] = ry
            elif rank[rx] > rank[ry]:
                parent[ry] = rx
            else:
                parent[rx] = ry
                rank[ry] += 1
            count -= 1
            return True
        return False

    def isSimilar(s1, s2):
        diff = 0
        for c1, c2 in zip(s1, s2):
            if c1 != c2:
                diff += 1
                if diff > 2: return False
        return diff == 2 or diff == 0

    for i in range(n):
        for j in range(i + 1, n):
            if isSimilar(strs[i], strs[j]):
                union(i, j)

    return count
```

**Explanation**:

1. We treat each string as a node. Two strings have an edge if they are similar.
2. We iterate through all pairs of strings and `union` them if they are similar.
3. The final `count` of disjoint sets is the number of similar groups.

**Complexity Analysis**:

- **Time Complexity**: $O(n^2 m)$, where $n$ is number of strings and $m$ is string length.
- **Space Complexity**: $O(n)$ for parent array.

---

## 3. Sentence Similarity II

**Problem Statement**:
Given two sentences `words1` and `words2` and a list of `similarPairs`, determine if the sentences are similar. Similarity is transitive.

**Optimal Python Solution**:

```python
def areSentencesSimilarTwo(words1: list[str], words2: list[str], pairs: list[list[str]]) -> bool:
    if len(words1) != len(words2):
        return False

    parent = {}
    rank = {}

    def find(x):
        if x not in parent:
            parent[x] = x
            rank[x] = 0
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    def union(x, y):
        rx, ry = find(x), find(y)
        if rx != ry:
            if rank[rx] < rank[ry]:
                parent[rx] = ry
            elif rank[rx] > rank[ry]:
                parent[ry] = rx
            else:
                parent[rx] = ry
                rank[ry] += 1

    for u, v in pairs:
        union(u, v)

    for w1, w2 in zip(words1, words2):
        if w1 == w2: continue
        if find(w1) != find(w2):
            return False

    return True
```

**Explanation**:

1. We use Union-Find to group similar words together.
2. For each pair of words in the sentences, they are similar if they are the same word or if they belong to the same Union-Find component.

**Complexity Analysis**:

- **Time Complexity**: $O(P \alpha(P) + N \alpha(P))$, where $P$ is number of pairs and $N$ is sentence length.
- **Space Complexity**: $O(P)$ to store word relationships.

---

## 4. Synonymous Sentences

**Problem Statement**:
You are given a list of `synonyms` and a `text`. Return all possible sentences that can be formed by replacing words with their synonyms, in lexicographical order.

**Optimal Python Solution**:

```python
from collections import defaultdict

def generateSentences(synonyms: list[list[str]], text: str) -> list[str]:
    parent = {}
    rank = {}
    def find(x):
        if x not in parent:
            parent[x] = x
            rank[x] = 0
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    def union(x, y):
        rx, ry = find(x), find(y)
        if rx != ry:
            if rank[rx] < rank[ry]:
                parent[rx] = ry
            elif rank[rx] > rank[ry]:
                parent[ry] = rx
            else:
                parent[rx] = ry
                rank[ry] += 1

    for u, v in synonyms:
        union(u, v)

    # Group synonyms by root
    groups = defaultdict(list)
    for word in parent:
        groups[find(word)].append(word)

    for root in groups:
        groups[root].sort()

    words = text.split()
    res = []

    def backtrack(idx, current_sentence):
        if idx == len(words):
            res.append(" ".join(current_sentence))
            return

        word = words[idx]
        if word not in parent:
            backtrack(idx + 1, current_sentence + [word])
        else:
            root = find(word)
            for synonym in groups[root]:
                backtrack(idx + 1, current_sentence + [synonym])

    backtrack(0, [])
    return sorted(res)
```

**Explanation**:

1. Use Union-Find to group all synonymous words together.
2. For each word in the original sentence, if it has synonyms, we use backtracking to try all possible replacements from its synonym group.
3. Sort the final list of sentences lexicographically.

**Complexity Analysis**:

- **Time Complexity**: $O(P \alpha(P) + S)$, where $P$ is pairs and $S$ is the number of possible sentences (which can be exponential).
- **Space Complexity**: $O(P)$ for Union-Find and $O(S)$ for result storage.

---

## 5. Evaluate Division

**Problem Statement**:
You are given `equations` like `a / b = 2.0` and `values` representing the results. Return the results of `queries` like `a / c`. If the result cannot be determined, return -1.0.

**Optimal Python Solution**:

```python
def calcEquation(equations: list[list[str]], values: list[float], queries: list[list[str]]) -> list[float]:
    parent = {}
    # weight[x] = x / root(x)
    weight = {}

    def find(x):
        if x not in parent:
            parent[x] = x
            weight[x] = 1.0
            return x
        if parent[x] == x:
            return x

        root = find(parent[x])
        # x / new_root = (x / old_root) * (old_root / new_root)
        weight[x] *= weight[parent[x]]
        parent[x] = root
        return root

    def union(x, y, val):
        root_x, root_y = find(x), find(y)
        if root_x != root_y:
            # val = x / y
            # x / root_x = weight[x]
            # y / root_y = weight[y]
            # root_x / root_y = (x / weight[x]) / (y / weight[y]) = (x / y) * (weight[y] / weight[x])
            parent[root_x] = root_y
            weight[root_x] = val * weight[y] / weight[x]

    for (u, v), val in zip(equations, values):
        union(u, v, val)

    res = []
    for u, v in queries:
        if u not in parent or v not in parent or find(u) != find(v):
            res.append(-1.0)
        else:
            # u / v = (u / root) / (v / root)
            res.append(weight[u] / weight[v])

    return res
```

**Explanation**:

1. This is a "Weighted Union-Find" problem. Each node stores its relationship (ratio) to its parent.
2. `weight[x]` stores the value of `x / parent[x]`.
3. During `find` (with path compression), we update the weight to be `x / root`.
4. During `union(x, y, val)` where `x / y = val`, we calculate the ratio between their roots and update the parent and weight.
5. For a query `u / v`, if they share a root, the answer is `(u / root) / (v / root)`.

**Complexity Analysis**:

- **Time Complexity**: $O((E+Q) \alpha(V))$, where $E$ is equations and $Q$ is queries.
- **Space Complexity**: $O(V)$ for parent and weight maps.

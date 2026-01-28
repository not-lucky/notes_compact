# Solutions: Alien Dictionary

## Practice Problems

| #   | Problem                 | Difficulty | Key Variation            |
| --- | ----------------------- | ---------- | ------------------------ |
| 1   | Alien Dictionary        | Hard       | Core problem             |
| 2   | Course Schedule II      | Medium     | Similar topological sort |
| 3   | Sequence Reconstruction | Medium     | Verify unique order      |

---

## 1. Alien Dictionary

### Problem Statement

Derive the order of letters in an alien alphabet from a sorted list of words.

### Optimal Python Solution

```python
from collections import defaultdict, deque

def alienOrder(words: list[str]) -> str:
    adj = defaultdict(set)
    in_degree = {c: 0 for w in words for c in w}

    # Build graph
    for i in range(len(words) - 1):
        w1, w2 = words[i], words[i+1]
        for j in range(min(len(w1), len(w2))):
            if w1[j] != w2[j]:
                if w2[j] not in adj[w1[j]]:
                    adj[w1[j]].add(w2[j])
                    in_degree[w2[j]] += 1
                break
        else: # Check if prefix rule is violated
            if len(w1) > len(w2): return ""

    # Kahn's Algorithm
    queue = deque([c for c in in_degree if in_degree[c] == 0])
    res = []
    while queue:
        c = queue.popleft()
        res.append(c)
        for neighbor in adj[c]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    return "".join(res) if len(res) == len(in_degree) else ""
```

### Explanation

- **Algorithm**: Topological Sort (Kahn's).
- **Graph Construction**: Compare adjacent words to find relative character ordering.
- **Prefix Rule**: If word A is a prefix of word B, A must come before B. If B comes first, it's invalid.
- **Complexity**: Time O(C) (total characters), Space O(1) (fixed alphabet size).

---

## 2. Course Schedule II

### Problem Statement

Return a valid course ordering.

### Optimal Python Solution

```python
from collections import deque, defaultdict

def findOrder(numCourses: int, prerequisites: list[list[int]]) -> list[int]:
    adj = defaultdict(list)
    in_degree = [0] * numCourses
    for u, v in prerequisites:
        adj[v].append(u)
        in_degree[u] += 1

    queue = deque([i for i in range(numCourses) if in_degree[i] == 0])
    order = []
    while queue:
        u = queue.popleft()
        order.append(u)
        for v in adj[u]:
            in_degree[v] -= 1
            if in_degree[v] == 0:
                queue.append(v)
    return order if len(order) == numCourses else []
```

---

## 3. Sequence Reconstruction

### Problem Statement

Check if a sequence `nums` can be uniquely reconstructed from a set of `sequences`.

### Optimal Python Solution

```python
from collections import deque, defaultdict

def sequenceReconstruction(nums: list[int], sequences: list[list[int]]) -> bool:
    adj = defaultdict(list)
    in_degree = {num: 0 for num in nums}
    nodes = set()

    for seq in sequences:
        for i in range(len(seq)):
            nodes.add(seq[i])
            if i > 0:
                adj[seq[i-1]].append(seq[i])
                in_degree[seq[i]] += 1

    if nodes != set(nums): return False
    queue = deque([i for i in in_degree if in_degree[i] == 0])
    res = []

    while queue:
        if len(queue) > 1: return False # Unique order requires queue size == 1
        u = queue.popleft()
        res.append(u)
        for v in adj[u]:
            in_degree[v] -= 1
            if in_degree[v] == 0:
                queue.append(v)
    return res == nums
```

# Alien Dictionary

## Practice Problems

### 1. Alien Dictionary
**Difficulty:** Hard
**Concept:** Core problem

```python
from collections import defaultdict, deque
from typing import List

def alien_order(words: List[str]) -> str:
    """
    Derive alien alphabet order from sorted words.

    >>> alien_order(["wrt","wrf","er","ett","rftt"])
    'wertf'
    >>> alien_order(["z","x"])
    'zx'
    >>> alien_order(["z","x","z"])
    ''

    Time: O(C) where C is the total number of characters in all words
    Space: O(1) as there are at most 26 characters
    """
    graph = defaultdict(set)
    in_degree = {c: 0 for word in words for c in word}

    for i in range(len(words) - 1):
        w1, w2 = words[i], words[i+1]
        if len(w1) > len(w2) and w1.startswith(w2):
            return "" # Invalid prefix order

        for c1, c2 in zip(w1, w2):
            if c1 != c2:
                if c2 not in graph[c1]:
                    graph[c1].add(c2)
                    in_degree[c2] += 1
                break

    queue = deque([c for c in in_degree if in_degree[c] == 0])
    result = []

    while queue:
        c = queue.popleft()
        result.append(c)
        for neighbor in graph[c]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    return "".join(result) if len(result) == len(in_degree) else ""
```

### 2. Verifying an Alien Dictionary
**Difficulty:** Easy
**Concept:** Simpler verification

```python
from typing import List

def is_alien_sorted(words: List[str], order: str) -> bool:
    """
    Check if words are sorted according to alien order.

    Time: O(C) where C is total characters
    Space: O(1)
    """
    order_map = {c: i for i, c in enumerate(order)}

    for i in range(len(words) - 1):
        w1, w2 = words[i], words[i+1]
        for j in range(min(len(w1), len(w2))):
            if w1[j] != w2[j]:
                if order_map[w1[j]] > order_map[w2[j]]:
                    return False
                break
        else:
            if len(w1) > len(w2):
                return False
    return True
```

### 3. Sequence Reconstruction
**Difficulty:** Medium
**Concept:** Verify unique order

```python
from collections import defaultdict, deque
from typing import List

def sequence_reconstruction(nums: List[int], sequences: List[List[int]]) -> bool:
    """
    Check if nums is the unique shortest supersequence of sequences.

    Time: O(V + E)
    Space: O(V + E)
    """
    graph = defaultdict(list)
    in_degree = {num: 0 for num in nums}
    nodes = set()

    for seq in sequences:
        for x in seq:
            nodes.add(x)
        for i in range(len(seq) - 1):
            u, v = seq[i], seq[i+1]
            graph[u].append(v)
            if v in in_degree:
                in_degree[v] += 1
            else:
                return False # node in seq not in nums

    if nodes != set(nums):
        return False

    queue = deque([n for n in in_degree if in_degree[n] == 0])
    result = []

    while queue:
        if len(queue) > 1:
            return False # Not unique

        u = queue.popleft()
        result.append(u)

        for v in graph[u]:
            in_degree[v] -= 1
            if in_degree[v] == 0:
                queue.append(v)

    return result == nums
```

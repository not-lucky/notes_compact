# Word Ladder (Implicit Graph)

## Practice Problems

### 1. Word Ladder
**Difficulty:** Hard
**Concept:** Basic implicit graph

```python
from collections import deque
from typing import List

def ladder_length(begin_word: str, end_word: str, word_list: List[str]) -> int:
    """
    Find the shortest transformation sequence from beginWord to endWord.

    >>> ladder_length("hit", "cog", ["hot","dot","dog","lot","log","cog"])
    5

    Time: O(M^2 * N)
    Space: O(M * N)
    """
    word_set = set(word_list)
    if end_word not in word_set:
        return 0

    queue = deque([(begin_word, 1)])
    visited = {begin_word}

    while queue:
        word, length = queue.popleft()
        if word == end_word:
            return length

        for i in range(len(word)):
            for c in 'abcdefghijklmnopqrstuvwxyz':
                next_word = word[:i] + c + word[i+1:]
                if next_word in word_set and next_word not in visited:
                    visited.add(next_word)
                    queue.append((next_word, length + 1))

    return 0
```

### 2. Open the Lock
**Difficulty:** Medium
**Concept:** Digit state graph

```python
from collections import deque
from typing import List

def open_lock(deadends: List[str], target: str) -> int:
    """
    Find minimum turns to unlock from "0000" to target.

    Time: O(10^4 * 4 * 2)
    Space: O(10^4)
    """
    dead = set(deadends)
    if "0000" in dead:
        return -1

    queue = deque([("0000", 0)])
    visited = {"0000"}

    while queue:
        s, d = queue.popleft()
        if s == target:
            return d

        for i in range(4):
            digit = int(s[i])
            for move in [-1, 1]:
                new_digit = (digit + move) % 10
                new_s = s[:i] + str(new_digit) + s[i+1:]
                if new_s not in dead and new_s not in visited:
                    visited.add(new_s)
                    queue.append((new_s, d + 1))

    return -1
```

### 3. Minimum Genetic Mutation
**Difficulty:** Medium
**Concept:** 4-character alphabet

```python
from collections import deque
from typing import List

def min_mutation(start: str, end: str, bank: List[str]) -> int:
    """
    Minimum mutations to transform gene.

    Time: O(M^2 * N)
    Space: O(M * N)
    """
    bank_set = set(bank)
    if end not in bank_set:
        return -1

    queue = deque([(start, 0)])
    visited = {start}
    chars = ['A', 'C', 'G', 'T']

    while queue:
        gene, mutations = queue.popleft()
        if gene == end:
            return mutations

        for i in range(len(gene)):
            for c in chars:
                if c != gene[i]:
                    new_gene = gene[:i] + c + gene[i+1:]
                    if new_gene in bank_set and new_gene not in visited:
                        visited.add(new_gene)
                        queue.append((new_gene, mutations + 1))

    return -1
```

### 4. Word Ladder II
**Difficulty:** Hard
**Concept:** All shortest paths

```python
from collections import deque, defaultdict
from typing import List

def find_ladders(begin_word: str, end_word: str, word_list: List[str]) -> List[List[str]]:
    """
    Find all shortest transformation sequences.

    Time: O(M^2 * N + NumberOfPaths * M)
    Space: O(M^2 * N)
    """
    word_set = set(word_list)
    if end_word not in word_set: return []

    adj = defaultdict(list)
    levels = {begin_word: 0}
    found = False
    queue = deque([begin_word])

    while queue and not found:
        for _ in range(len(queue)):
            u = queue.popleft()
            for i in range(len(u)):
                for c in 'abcdefghijklmnopqrstuvwxyz':
                    v = u[:i] + c + u[i+1:]
                    if v in word_set:
                        if v not in levels:
                            levels[v] = levels[u] + 1
                            queue.append(v)
                            adj[u].append(v)
                        elif levels[v] == levels[u] + 1:
                            adj[u].append(v)
                        if v == end_word: found = True

    res = []
    def backtrack(curr, path):
        if curr == end_word:
            res.append(list(path))
            return
        for neighbor in adj[curr]:
            path.append(neighbor)
            backtrack(neighbor, path)
            path.pop()

    if found: backtrack(begin_word, [begin_word])
    return res
```

### 5. Sliding Puzzle
**Difficulty:** Hard
**Concept:** Board state graph

```python
from collections import deque

def sliding_puzzle(board: List[List[int]]) -> int:
    """
    Minimum moves to solve 2x3 sliding puzzle.

    Time: O(V!) where V=6
    Space: O(V!)
    """
    target = "123450"
    start = "".join(str(c) for r in board for c in r)
    adj = {0: [1, 3], 1: [0, 2, 4], 2: [1, 5], 3: [0, 4], 4: [1, 3, 5], 5: [2, 4]}

    queue = deque([(start, 0)])
    visited = {start}

    while queue:
        state, dist = queue.popleft()
        if state == target: return dist
        z = state.find('0')
        for neighbor in adj[z]:
            s_list = list(state)
            s_list[z], s_list[neighbor] = s_list[neighbor], s_list[z]
            new_state = "".join(s_list)
            if new_state not in visited:
                visited.add(new_state)
                queue.append((new_state, dist + 1))
    return -1
```

# Solutions: Word Ladder (Implicit Graph)

## Practice Problems

| #   | Problem                  | Difficulty | Key Variation        |
| --- | ------------------------ | ---------- | -------------------- |
| 1   | Word Ladder              | Hard       | Basic implicit graph |
| 2   | Word Ladder II           | Hard       | All shortest paths   |
| 3   | Open the Lock            | Medium     | Digit state graph    |
| 4   | Minimum Genetic Mutation | Medium     | 4-character alphabet |
| 5   | Sliding Puzzle           | Hard       | Board state graph    |

---

## 1. Word Ladder

### Problem Statement

Find the shortest transformation sequence from `beginWord` to `endWord`.

### Optimal Python Solution

```python
from collections import deque, defaultdict

def ladderLength(beginWord: str, endWord: str, wordList: list[str]) -> int:
    word_set = set(wordList)
    if endWord not in word_set: return 0

    L = len(beginWord)
    adj = defaultdict(list)
    for word in wordList:
        for i in range(L):
            adj[word[:i] + "*" + word[i+1:]].append(word)

    queue = deque([(beginWord, 1)])
    visited = {beginWord}

    while queue:
        word, d = queue.popleft()
        if word == endWord: return d
        for i in range(L):
            pattern = word[:i] + "*" + word[i+1:]
            for neighbor in adj[pattern]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, d + 1))
            adj[pattern] = [] # Optimization
    return 0
```

---

## 2. Word Ladder II

### Problem Statement

Find all shortest transformation sequences.

### Optimal Python Solution

```python
from collections import deque, defaultdict

def findLadders(beginWord: str, endWord: str, wordList: list[str]) -> list[list[str]]:
    word_set = set(wordList)
    if endWord not in word_set: return []

    L = len(beginWord)
    dist = {beginWord: 0}
    preds = defaultdict(list)
    queue = deque([beginWord])

    while queue:
        word = queue.popleft()
        if word == endWord: break
        for i in range(L):
            for c in 'abcdefghijklmnopqrstuvwxyz':
                nxt = word[:i] + c + word[i+1:]
                if nxt in word_set:
                    if nxt not in dist:
                        dist[nxt] = dist[word] + 1
                        queue.append(nxt)
                    if dist[nxt] == dist[word] + 1:
                        preds[nxt].append(word)

    res = []
    def backtrack(curr, path):
        if curr == beginWord:
            res.append(path[::-1])
            return
        for p in preds[curr]:
            backtrack(p, path + [p])

    if endWord in dist: backtrack(endWord, [endWord])
    return res
```

---

## 3. Open the Lock

### Problem Statement

Minimum turns to open the lock.

### Optimal Python Solution

```python
from collections import deque

def openLock(deadends: list[str], target: str) -> int:
    dead = set(deadends)
    if "0000" in dead: return -1
    queue = deque([("0000", 0)])
    visited = {"0000"}

    while queue:
        node, d = queue.popleft()
        if node == target: return d
        for i in range(4):
            for delta in [-1, 1]:
                nxt = node[:i] + str((int(node[i]) + delta) % 10) + node[i+1:]
                if nxt not in visited and nxt not in dead:
                    visited.add(nxt)
                    queue.append((nxt, d + 1))
    return -1
```

---

## 4. Minimum Genetic Mutation

### Problem Statement

Minimum mutations to transform the gene string.

### Optimal Python Solution

```python
from collections import deque

def minMutation(startGene: str, endGene: str, bank: list[str]) -> int:
    bank_set = set(bank)
    if endGene not in bank_set: return -1
    queue = deque([(startGene, 0)])
    visited = {startGene}

    while queue:
        gene, d = queue.popleft()
        if gene == endGene: return d
        for i in range(8):
            for c in "ACGT":
                nxt = gene[:i] + c + gene[i+1:]
                if nxt in bank_set and nxt not in visited:
                    visited.add(nxt)
                    queue.append((nxt, d + 1))
    return -1
```

---

## 5. Sliding Puzzle

### Problem Statement

Minimum moves to solve the sliding puzzle.

### Optimal Python Solution

```python
from collections import deque

def slidingPuzzle(board: list[list[int]]) -> int:
    start = "".join(str(c) for r in board for c in r)
    target = "123450"
    adj = {0:[1,3], 1:[0,2,4], 2:[1,5], 3:[0,4], 4:[1,3,5], 5:[2,4]}
    queue = deque([(start, 0)])
    visited = {start}

    while queue:
        state, d = queue.popleft()
        if state == target: return d
        idx = state.find('0')
        for neighbor in adj[idx]:
            l = list(state)
            l[idx], l[neighbor] = l[neighbor], l[idx]
            nxt = "".join(l)
            if nxt not in visited:
                visited.add(nxt)
                queue.append((nxt, d + 1))
    return -1
```

# Word Ladder (Implicit Graph)

> **Prerequisites:** [02-bfs-basics](./02-bfs-basics.md)

## Interview Context

Word Ladder is a FANG+ classic because:

1. **Implicit graph**: Graph isn't given, you build it from constraints
2. **BFS for shortest path**: Minimum transformations
3. **Optimization skills**: Naive approach is too slow
4. **Pattern recognition**: Many problems have hidden graph structure

This problem frequently appears at Google and Amazon.

---

## Problem Statement

Given `beginWord`, `endWord`, and `wordList`, find the shortest transformation sequence from beginWord to endWord where:

- Only one letter changes at a time
- Each intermediate word must be in wordList

Return the number of words in the shortest transformation, or 0 if impossible.

```
Example:
beginWord = "hit"
endWord = "cog"
wordList = ["hot", "dot", "dog", "lot", "log", "cog"]

Output: 5
Transformation: hit → hot → dot → dog → cog
```

---

## Core Insight: Words as Graph Nodes

Each word is a node. Two words are connected if they differ by exactly one character.

```
Graph:
    hit
     |
    hot
   /   \
  dot   lot
   |     |
  dog   log
     \ /
     cog
```

---

## Solution 1: BFS with All Neighbors Check

```python
from collections import deque

def ladder_length(beginWord: str, endWord: str,
                   wordList: list[str]) -> int:
    """
    BFS on implicit graph.

    Time: O(M² × N) where M = word length, N = wordList size
    Space: O(M × N)
    """
    word_set = set(wordList)

    if endWord not in word_set:
        return 0

    queue = deque([(beginWord, 1)])  # (word, length)
    visited = {beginWord}

    while queue:
        word, length = queue.popleft()

        if word == endWord:
            return length

        # Try changing each character
        for i in range(len(word)):
            for c in 'abcdefghijklmnopqrstuvwxyz':
                next_word = word[:i] + c + word[i+1:]

                if next_word in word_set and next_word not in visited:
                    visited.add(next_word)
                    queue.append((next_word, length + 1))

    return 0
```

---

## Solution 2: Preprocessing with Wildcards

For large wordLists, preprocess to find neighbors in O(1):

```python
from collections import defaultdict, deque

def ladder_length_optimized(beginWord: str, endWord: str,
                             wordList: list[str]) -> int:
    """
    Optimized BFS with wildcard preprocessing.

    Time: O(M² × N)
    Space: O(M² × N)

    Preprocessing: Create patterns like h*t → [hot, hit]
    """
    if endWord not in wordList:
        return 0

    L = len(beginWord)

    # Build pattern -> words mapping
    patterns = defaultdict(list)
    for word in wordList:
        for i in range(L):
            pattern = word[:i] + '*' + word[i+1:]
            patterns[pattern].append(word)

    queue = deque([(beginWord, 1)])
    visited = {beginWord}

    while queue:
        word, length = queue.popleft()

        for i in range(L):
            pattern = word[:i] + '*' + word[i+1:]

            for neighbor in patterns[pattern]:
                if neighbor == endWord:
                    return length + 1

                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, length + 1))

            # Clear to avoid revisiting (optimization)
            patterns[pattern] = []

    return 0
```

---

## Solution 3: Bidirectional BFS

Expand from both ends, meet in middle. Much faster for deep searches.

```python
from collections import defaultdict

def ladder_length_bidirectional(beginWord: str, endWord: str,
                                  wordList: list[str]) -> int:
    """
    Bidirectional BFS for faster search.

    Time: O(M² × N) but faster in practice
    Space: O(M × N)
    """
    if endWord not in wordList:
        return 0

    L = len(beginWord)
    word_set = set(wordList)
    word_set.add(beginWord)

    # Two frontiers
    front = {beginWord}
    back = {endWord}
    visited = {beginWord, endWord}

    length = 1

    while front and back:
        # Always expand smaller frontier
        if len(front) > len(back):
            front, back = back, front

        next_front = set()

        for word in front:
            for i in range(L):
                for c in 'abcdefghijklmnopqrstuvwxyz':
                    next_word = word[:i] + c + word[i+1:]

                    if next_word in back:
                        return length + 1

                    if next_word in word_set and next_word not in visited:
                        visited.add(next_word)
                        next_front.add(next_word)

        front = next_front
        length += 1

    return 0
```

---

## Word Ladder II (Find All Shortest Paths)

```python
from collections import defaultdict, deque

def find_ladders(beginWord: str, endWord: str,
                  wordList: list[str]) -> list[list[str]]:
    """
    Find ALL shortest transformation sequences.

    Time: O(M² × N + paths)
    Space: O(M² × N)
    """
    word_set = set(wordList)

    if endWord not in word_set:
        return []

    L = len(beginWord)

    # BFS to find shortest distance and build predecessor graph
    dist = {beginWord: 0}
    predecessors = defaultdict(list)

    queue = deque([beginWord])

    while queue:
        word = queue.popleft()

        if word == endWord:
            break

        for i in range(L):
            for c in 'abcdefghijklmnopqrstuvwxyz':
                next_word = word[:i] + c + word[i+1:]

                if next_word not in word_set:
                    continue

                # First time seeing this word
                if next_word not in dist:
                    dist[next_word] = dist[word] + 1
                    queue.append(next_word)

                # Add as predecessor if on shortest path
                if dist.get(next_word, float('inf')) == dist[word] + 1:
                    predecessors[next_word].append(word)

    # Backtrack to find all paths
    paths = []

    def backtrack(word: str, path: list[str]):
        if word == beginWord:
            paths.append(path[::-1])
            return

        for pred in predecessors[word]:
            path.append(pred)
            backtrack(pred, path)
            path.pop()

    if endWord in dist:
        backtrack(endWord, [endWord])

    return paths
```

---

## Other Implicit Graph Problems

### Open the Lock

```python
from collections import deque

def open_lock(deadends: list[str], target: str) -> int:
    """
    Find minimum turns to unlock from "0000" to target.

    Each turn: rotate one wheel up or down.
    """
    dead_set = set(deadends)

    if "0000" in dead_set:
        return -1

    if target == "0000":
        return 0

    queue = deque([("0000", 0)])
    visited = {"0000"}

    while queue:
        state, turns = queue.popleft()

        # Try each wheel
        for i in range(4):
            digit = int(state[i])

            for delta in [-1, 1]:
                new_digit = (digit + delta) % 10
                new_state = state[:i] + str(new_digit) + state[i+1:]

                if new_state == target:
                    return turns + 1

                if new_state not in visited and new_state not in dead_set:
                    visited.add(new_state)
                    queue.append((new_state, turns + 1))

    return -1
```

### Minimum Genetic Mutation

```python
from collections import deque

def min_mutation(start: str, end: str, bank: list[str]) -> int:
    """
    Minimum mutations to transform gene.
    Each position: A, C, G, T
    """
    bank_set = set(bank)

    if end not in bank_set:
        return -1

    queue = deque([(start, 0)])
    visited = {start}
    genes = ['A', 'C', 'G', 'T']

    while queue:
        gene, mutations = queue.popleft()

        if gene == end:
            return mutations

        for i in range(8):  # Gene has 8 characters
            for g in genes:
                if g != gene[i]:
                    new_gene = gene[:i] + g + gene[i+1:]

                    if new_gene in bank_set and new_gene not in visited:
                        visited.add(new_gene)
                        queue.append((new_gene, mutations + 1))

    return -1
```

---

## Pattern: Implicit Graph Recognition

If you see:

- States that transform into other states
- Minimum steps/operations to reach goal
- Valid intermediate states from a set

Think: **BFS on implicit graph**

---

## Complexity Analysis

| Approach           | Time                 | Space     |
| ------------------ | -------------------- | --------- |
| Basic BFS          | O(M² × N)            | O(M × N)  |
| With preprocessing | O(M² × N)            | O(M² × N) |
| Bidirectional      | O(M² × N) but faster | O(M × N)  |

M = word length, N = number of words

---

## Common Mistakes

```python
# WRONG: Not checking endWord in wordList
def ladder_length(beginWord, endWord, wordList):
    # Missing check
    queue = deque([beginWord])
    # If endWord not in wordList, will never find it

# CORRECT: Check first
if endWord not in set(wordList):
    return 0


# WRONG: Checking visited after generating word
next_word = word[:i] + c + word[i+1:]
if next_word in visited:
    continue
visited.add(next_word)
queue.append(next_word)
# Multiple paths may add same word to queue

# CORRECT: Check and mark atomically
if next_word not in visited and next_word in word_set:
    visited.add(next_word)  # Mark immediately
    queue.append(next_word)


# WRONG: Returning length without +1
if word == endWord:
    return length  # Off by one if length is edges, not nodes
```

---

## Interview Tips

1. **Recognize implicit graph**: States = nodes, transitions = edges
2. **BFS for shortest**: Because all edges have equal weight
3. **Consider bidirectional**: Faster for deep searches
4. **Preprocess if needed**: For faster neighbor lookup
5. **Handle edge cases**: endWord not in list, already at target

---

## Practice Problems

| #   | Problem                  | Difficulty | Key Variation        |
| --- | ------------------------ | ---------- | -------------------- |
| 1   | Word Ladder              | Hard       | Basic implicit graph |
| 2   | Word Ladder II           | Hard       | All shortest paths   |
| 3   | Open the Lock            | Medium     | Digit state graph    |
| 4   | Minimum Genetic Mutation | Medium     | 4-character alphabet |
| 5   | Sliding Puzzle           | Hard       | Board state graph    |

---

## Key Takeaways

1. **Implicit graph**: Not given, built from transitions
2. **BFS for minimum steps**: Unweighted edges
3. **Bidirectional optimization**: Meet in middle
4. **Wildcard preprocessing**: Faster neighbor lookup
5. **Word Ladder II**: BFS + backtracking for all paths

---

## Next: [16-bipartite-check.md](./16-bipartite-check.md)

Learn to check if a graph is bipartite (two-colorable).

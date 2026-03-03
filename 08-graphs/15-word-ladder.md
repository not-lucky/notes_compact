# Word Ladder (Implicit Graph)

> **Prerequisites:** [02-bfs-basics](./02-bfs-basics.md)
> **Prerequisites:** [03-dfs-basics](./03-dfs-basics.md) (For Word Ladder II)

## Interview Context

Word Ladder is a FANG+ classic because:

1. **Implicit graph**: Graph isn't given, you build it from constraints
2. **BFS for shortest path**: Minimum transformations in an unweighted graph
3. **Optimization skills**: Naive approach is too slow — you need to show you can do better
4. **Pattern recognition**: Many problems have hidden graph structure (states as nodes, transitions as edges)

This problem frequently appears at Google and Amazon.

### FANG Context: Amazon & Google
This problem is heavily tested at **Amazon** (frequently as a phone screen or online assessment) and **Google** (often as an onsite interview question to test optimization).
- **Amazon** focuses on whether you can get a working BFS solution and handle edge cases (like `endWord` not in the list).
- **Google** interviewers will almost always push you to optimize from standard BFS to the **Bidirectional BFS** approach. They want to see you recognize the exponential branching factor and understand how searching from both ends reduces the search space significantly.

---

## Problem Statement

**LeetCode 127 — Word Ladder**

Given `beginWord`, `endWord`, and `wordList`, find the shortest transformation sequence from `beginWord` to `endWord` where:

- Only one letter changes at a time
- Each intermediate word must be in `wordList`

Return the **number of words** in the shortest transformation sequence, or 0 if impossible.

```text
Example:
beginWord = "hit"
endWord = "cog"
wordList = ["hot", "dot", "dog", "lot", "log", "cog"]

Output: 5
Transformation: hit → hot → dot → dog → cog
                 1     2     3     4     5    (counting words, not edges)
```

---

## Core Insight: Words as Graph Nodes

**Why model this as a graph?** Each word is a **node**. Two words are connected by an
**edge** if they differ by exactly one character. The problem then becomes: find the
**shortest path** in an unweighted graph — which is exactly what BFS does.

**Why BFS guarantees shortest path:** In an unweighted graph, BFS explores nodes in
order of distance from the source. The first time BFS reaches a node, it has found
the shortest path to it. This is because BFS processes all nodes at distance `d`
before any node at distance `d+1`.

```text
Implicit Graph:
    hit
     |
    hot
   /   \
  dot   lot
   |     |
  dog   log
     \ /
     cog

Shortest path: hit → hot → dot → dog → cog (5 words = 4 edges)
```

---

## Solution 1: BFS — Generate All Neighbors (Brute Force)

**Idea:** For each word, try replacing every character with `a-z` to generate
candidate neighbors. Check if each candidate is in the word set.

```python
from collections import deque


def ladder_length(
    beginWord: str, endWord: str, wordList: list[str]
) -> int:
    """
    BFS on implicit graph — generate neighbors by trying all 26 letters
    at each position.

    Time:  O(M² × N) — for each of N words dequeued, we try M positions
           × 26 letters, and each string slice costs O(M).
    Space: O(M × N) — word_set + visited + queue all store up to N words
           of length M.
    """
    word_set = set(wordList)

    # Edge case: endWord must be reachable
    if endWord not in word_set:
        return 0

    queue = deque([(beginWord, 1)])  # (current_word, path_length)
    visited = {beginWord}

    while queue:
        word, length = queue.popleft()

        # Found the target — return immediately (BFS guarantees shortest)
        if word == endWord:
            return length

        # Try changing each character position
        for i in range(len(word)):
            for c in 'abcdefghijklmnopqrstuvwxyz':
                next_word = word[:i] + c + word[i + 1:]

                if next_word in word_set and next_word not in visited:
                    visited.add(next_word)  # Mark visited BEFORE enqueuing
                    queue.append((next_word, length + 1))

    return 0  # No path exists
```

---

## Solution 2: BFS — Wildcard Pattern Preprocessing (Optimized Neighbor Lookup)

**Intuition:** Instead of generating 26 × M candidates and checking each one,
we precompute a mapping from **wildcard patterns** to words. For example:

```
"hot" → ["h*t", "*ot", "ho*"]
"hit" → ["h*t", "*it", "hi*"]

Pattern "h*t" maps to → ["hot", "hit"]
```

Now, to find all neighbors of `"hot"`, we generate its 3 patterns and look them up
in the map — directly getting `["hit"]` from `"h*t"` (plus any others). This avoids
iterating through all 26 letters at each position.

**When is this faster?** When the word list is large. The brute-force approach always
generates `26 × M` candidates per word. The wildcard approach generates only `M`
patterns per word and directly retrieves actual neighbors.

```python
from collections import defaultdict, deque


def ladder_length_optimized(
    beginWord: str, endWord: str, wordList: list[str]
) -> int:
    """
    BFS with wildcard pattern preprocessing for faster neighbor lookup.

    Time:  O(M² × N) — preprocessing builds M patterns per word (each
           pattern costs O(M) to create), then BFS visits each word once.
    Space: O(M² × N) — the pattern map stores M patterns for each of
           N words, each pattern is O(M) characters.
    """
    if endWord not in wordList:
        return 0

    word_len = len(beginWord)

    # Preprocessing: map each wildcard pattern to matching words
    # e.g., "h*t" → ["hot", "hit"]
    pattern_to_words: dict[str, list[str]] = defaultdict(list)
    for word in wordList:
        for i in range(word_len):
            pattern = word[:i] + '*' + word[i + 1:]
            pattern_to_words[pattern].append(word)

    queue = deque([(beginWord, 1)])
    visited = {beginWord}

    while queue:
        word, length = queue.popleft()

        for i in range(word_len):
            pattern = word[:i] + '*' + word[i + 1:]

            for neighbor in pattern_to_words[pattern]:
                if neighbor == endWord:
                    return length + 1

                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, length + 1))

            # Clear this pattern's list to avoid reprocessing
            # (all words reachable via this pattern are already visited/queued)
            pattern_to_words[pattern] = []

    return 0
```

---

## Solution 3: Bidirectional BFS

### Theory: Why Bidirectional BFS?

In standard BFS, the number of nodes explored grows exponentially with distance:
$B^d$ nodes, where $B$ is the branching factor and $d$ is the distance.

In **Bidirectional BFS**, we run two BFS searches simultaneously — one forward from
`beginWord` and one backward from `endWord`. We stop when the two frontiers meet.

**The Math:**
- Standard BFS explores: $B^d$ nodes
- Bidirectional BFS explores: $2 \times B^{d/2}$ nodes
- For $B=10$, $d=6$: standard → $10^6 = 1{,}000{,}000$ nodes, bidirectional →
  $2 \times 10^3 = 2{,}000$ nodes. **500× speedup!**

**When to use Bidirectional BFS:**
1. You know both the start and target nodes
2. The branching factor is roughly the same in both directions
3. The graph is unweighted (or all edges have the same weight)

**Key optimization:** Always expand the **smaller** frontier first — this keeps both
frontiers roughly the same size, maximizing the benefit.

```python
def ladder_length_bidirectional(
    beginWord: str, endWord: str, wordList: list[str]
) -> int:
    """
    Bidirectional BFS — expand from both ends, meet in the middle.

    Time:  O(M² × N) worst case, but much faster in practice due to
           reduced search space (especially with high branching factor).
    Space: O(M × N) for the visited set and frontiers.
    """
    word_set = set(wordList)

    if endWord not in word_set:
        return 0

    word_len = len(beginWord)

    # Two frontiers expanding toward each other
    front = {beginWord}
    back = {endWord}
    visited = {beginWord, endWord}

    length = 1  # Count of words in the path (starts at 1 for beginWord)

    while front and back:
        # Always expand the smaller frontier (key optimization)
        if len(front) > len(back):
            front, back = back, front

        next_front = set()

        for word in front:
            for i in range(word_len):
                for c in 'abcdefghijklmnopqrstuvwxyz':
                    next_word = word[:i] + c + word[i + 1:]

                    # Frontiers meet — we found the shortest path
                    if next_word in back:
                        return length + 1

                    if next_word in word_set and next_word not in visited:
                        visited.add(next_word)
                        next_front.add(next_word)

        front = next_front
        length += 1

    return 0  # Frontiers exhausted without meeting
```

---

## Word Ladder II — Find All Shortest Paths

**LeetCode 126 — Word Ladder II**

This harder variant asks for **all** shortest transformation sequences. The strategy:
1. **BFS phase**: Explore the graph level by level, recording the shortest distance
   to each word and tracking predecessors (words that lead to it on a shortest path).
2. **Backtrack phase**: Reconstruct all shortest paths from `endWord` back to
   `beginWord` using the predecessor graph.

**Critical detail:** Do NOT `break` when you first dequeue `endWord`. Other words at
the same BFS level may still have valid predecessor relationships to record. Instead,
let the entire level finish processing.

```python
from collections import defaultdict, deque


def find_ladders(
    beginWord: str, endWord: str, wordList: list[str]
) -> list[list[str]]:
    """
    Find ALL shortest transformation sequences.

    Phase 1: BFS to build a predecessor graph (which words lead to which
             on shortest paths).
    Phase 2: DFS/backtrack from endWord to beginWord to collect all paths.

    Time:  O(M² × N + P) where P = total length of all shortest paths
    Space: O(M² × N)
    """
    word_set = set(wordList)

    if endWord not in word_set:
        return []

    word_len = len(beginWord)

    # Phase 1: BFS to compute shortest distances and predecessor graph
    dist: dict[str, int] = {beginWord: 0}
    predecessors: dict[str, list[str]] = defaultdict(list)
    found = False

    queue = deque([beginWord])

    while queue and not found:
        # Process entire level before checking if we found endWord
        level_size = len(queue)
        # Collect all words discovered at this level so we don't
        # prematurely block cross-level predecessor edges
        level_words: set[str] = set()

        for _ in range(level_size):
            word = queue.popleft()

            for i in range(word_len):
                for c in 'abcdefghijklmnopqrstuvwxyz':
                    next_word = word[:i] + c + word[i + 1:]

                    if next_word not in word_set:
                        continue

                    # First time seeing this word — record distance, enqueue
                    if next_word not in dist:
                        dist[next_word] = dist[word] + 1
                        level_words.add(next_word)

                        if next_word == endWord:
                            found = True

                    # Add predecessor if this is a shortest-path edge
                    if dist.get(next_word) == dist[word] + 1:
                        predecessors[next_word].append(word)

        # Enqueue all newly discovered words from this level
        for w in level_words:
            queue.append(w)

    if not found:
        return []

    # Phase 2: Backtrack from endWord to beginWord using predecessors
    paths: list[list[str]] = []

    def backtrack(word: str, path: list[str]) -> None:
        if word == beginWord:
            paths.append(path[::-1])  # Reverse since we built it backwards
            return

        for pred in predecessors[word]:
            path.append(pred)
            backtrack(pred, path)
            path.pop()

    backtrack(endWord, [endWord])
    return paths
```

---

## Word Ladder Variations

### Word Ladder III (Hypothetical) - Smallest Lexicographical Path

**Variation:** Instead of just finding the shortest path length or returning all shortest paths, what if you need to return exactly one shortest path that is the lexicographically smallest?

**Strategy:**
1. Do standard BFS.
2. When multiple valid next words exist, sort them lexicographically before adding to the queue.
3. Keep track of the path as you traverse (or use a predecessor map) to reconstruct the smallest path.

This emphasizes that BFS explores neighbors in the order they are enqueued. By sorting neighbors before enqueueing, you guarantee the first path found is lexicographically smallest.

---

## Related Problem: Open the Lock (LeetCode 752)

Another classic implicit graph BFS problem. Each 4-digit lock state is a node.
Rotating one wheel up or down creates an edge to a neighbor state.

```python
from collections import deque


def open_lock(deadends: list[str], target: str) -> int:
    """
    Find minimum turns to reach target from "0000", avoiding deadends.

    Each turn: rotate one wheel up or down by 1.
    States are 4-digit strings; each has 8 neighbors (4 wheels × 2 directions).

    Time:  O(10^4 × 4) — at most 10,000 states, 8 neighbors each
    Space: O(10^4)
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

        for i in range(4):  # Try each wheel
            digit = int(state[i])

            for delta in (-1, 1):  # Rotate up or down
                new_digit = (digit + delta) % 10
                new_state = state[:i] + str(new_digit) + state[i + 1:]

                if new_state == target:
                    return turns + 1

                if new_state not in visited and new_state not in dead_set:
                    visited.add(new_state)
                    queue.append((new_state, turns + 1))

    return -1  # Target unreachable
```

---

## Common Mistakes

### 1. Forgetting to check `endWord` in word list

```python
# WRONG — will search forever and return 0, but wastes time
def ladder_length(beginWord: str, endWord: str, wordList: list[str]) -> int:
    queue = deque([beginWord])
    pass  # endWord not in wordList → can never be found

# CORRECT — check upfront
def ladder_length(beginWord: str, endWord: str, wordList: list[str]) -> int:
    if endWord not in set(wordList):
        return 0
    pass
```

### 2. Adding to visited AFTER dequeuing instead of BEFORE enqueuing

```python
# WRONG — same word can be enqueued multiple times, wasting work
next_word = word[:i] + c + word[i + 1:]
queue.append(next_word)
# ... later, when dequeued:
# if next_word in visited:
#     continue
# visited.add(next_word)

# CORRECT — mark visited immediately when enqueueing
if next_word not in visited and next_word in word_set:
    visited.add(next_word)   # Mark BEFORE enqueuing
    queue.append((next_word, length + 1))
```

### 3. Off-by-one in return value

The problem asks for the **number of words** in the path, not the number of edges.

```python
# WRONG — returns edge count
if word == endWord:
    return length  # If length tracks edges, this is off by one

# CORRECT — ensure length tracks word count (initialize to 1 for beginWord)
queue = deque([(beginWord, 1)])  # Start counting from 1
```

---

## Complexity Comparison

| Approach                    | Time (Worst Case) | Time (Practical) | Space         |
| --------------------------- | ------------------ | ----------------- | ------------- |
| BFS + generate neighbors    | O(M² × N)         | Baseline          | O(M × N)      |
| BFS + wildcard preprocessing| O(M² × N)         | Faster for large N| O(M² × N)     |
| Bidirectional BFS           | O(M² × N)         | **Much faster**   | O(M × N)      |

Where M = word length, N = word list size.

- **Generate neighbors**: Always tries 26 × M candidates per word — simple but redundant.
- **Wildcard preprocessing**: Trades space for faster neighbor lookup — especially beneficial when `N` is large and many words share patterns.
- **Bidirectional BFS**: Same worst-case, but explores far fewer nodes in practice by searching from both ends.

---

## Interview Tips

1. **Recognize implicit graph**: States = nodes, valid transitions = edges
2. **BFS for shortest path**: Works because all edges have equal weight (1 transformation)
3. **Optimize neighbor generation**: Mention wildcard preprocessing as an optimization
4. **Propose bidirectional BFS**: Especially at Google — explain the $B^{d/2}$ math
5. **Handle edge cases first**: `endWord` not in list, `beginWord == endWord`, empty word list

---

## Practice Problems

| #   | LeetCode | Problem                  | Difficulty | Key Variation                  | Hint                                                      |
| --- | -------- | ------------------------ | ---------- | ------------------------------ | --------------------------------------------------------- |
| 1   | 127      | Word Ladder              | Hard       | Shortest transformation count  | BFS on implicit graph; try wildcard preprocessing          |
| 2   | 126      | Word Ladder II           | Hard       | All shortest paths             | BFS for distances + DFS backtrack for path reconstruction  |
| 3   | 752      | Open the Lock            | Medium     | Digit state graph with deadends| 4-digit state = node; 8 neighbors per state                |
| 4   | 433      | Minimum Genetic Mutation | Medium     | 4-char alphabet (A,C,G,T)     | Same as Word Ladder but only 4 possible chars per position |
| 5   | 773      | Sliding Puzzle           | Hard       | Board state as graph node      | Serialize board state as string; BFS on state space        |

---

## Key Takeaways

1. **Implicit graph**: Not given explicitly — you build it from the problem's transition rules
2. **BFS = shortest path in unweighted graphs**: First visit to any node is the shortest path
3. **Bidirectional BFS**: Reduces exponential search space from $B^d$ to $2 \times B^{d/2}$
4. **Wildcard preprocessing**: Trade space for faster neighbor lookup via pattern maps
5. **Word Ladder II**: BFS builds the predecessor graph, then DFS/backtrack collects all paths

---

## Next: [16-bipartite-check.md](./16-bipartite-check.md)

Learn to check if a graph is bipartite (two-colorable).

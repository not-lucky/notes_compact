# Word Search II

> **Prerequisites:** [Trie Implementation](./01-trie-implementation.md), [Backtracking](../11-recursion-backtracking/README.md), [Matrix Traversal](../02-arrays-strings/README.md)

## Interview Context

Word Search II (LeetCode 212) is a hard problem that combines trie with DFS/backtracking. It's a favorite at Google and Meta because it tests both data structure knowledge and algorithm optimization skills. The naive approach times out; you must optimize with a trie.

---

## Building Intuition

**The Naive Approach and Why It Fails**

Given a grid and k words, the brute force is: for each word, search the entire grid. This means k complete grid traversals, each potentially exploring 4^L paths (4 directions, L = word length).

```
10,000 words × 12×12 grid × 4^10 paths = astronomical
```

**The Key Insight: Search All Words Simultaneously**

Instead of asking "Does this grid contain word X?" k times, ask "As I walk through this grid, which words can I form?"

The trie transforms this from:

```
For each of 10,000 words:
    For each of 144 cells:
        DFS up to 10 levels deep
```

To:

```
For each of 144 cells:
    DFS up to 10 levels, but prune if path not in ANY word
```

**Why a Trie is Perfect Here**

Consider searching for ["oath", "pea", "eat", "rain"]. When you start DFS from cell 'o':

Without trie:

- Check if path matches "oath" → Yes? Continue. No? Check next word.
- Check if path matches "pea" → ...
- Check if path matches "eat" → ...
- Repeat for every step!

With trie:

- Is 'o' a valid prefix? Check ONE node. Yes → continue. No → prune entirely.
- At 'oa', is 'oa' valid? Check ONE node.
- At 'oat', is 'oat' valid? Check ONE node.

The trie gives a SINGLE O(1) check that answers "does ANY word start with this path?"

**The Pruning Power**

```
Grid position: currently at 'o', next cells are 'a', 'e', 'i', 't'

Without trie: Must explore all 4 directions for EACH word
With trie:    Check which directions have children in trie
              If trie node for 'o' only has child 'a', skip e, i, t entirely

This compounds exponentially. At depth 10, 4^10 ≈ 1 million.
But with pruning, maybe only 1-2 paths are valid → massive speedup.
```

**Storing the Word at Terminal Nodes**

A clever optimization: instead of reconstructing the word from the path, store the complete word at the terminal node:

```python
# During trie construction:
node['$'] = "oath"  # Store the word itself

# During DFS:
if '$' in node:
    result.append(node['$'])  # Instant retrieval!
    del node['$']  # Avoid duplicates
```

---

## When NOT to Use This Pattern

**1. Single Word Search**

If you only need to find ONE word in the grid, skip the trie. Simple DFS is sufficient:

```python
# Word Search I: Single word, no trie needed
def exist(board, word):
    # Just DFS checking word[i] at each step
```

Trie overhead isn't worth it for k=1.

**2. Very Short Word List**

If you have 5-10 words, the trie construction overhead might exceed the savings. Profile first.

**3. Dense Grid with Many Matches**

If almost every path matches some word, pruning provides little benefit. The trie still helps with duplicate detection, but less dramatically.

**4. When Grid is Tiny**

For a 3×3 grid with 5-letter words? Brute force might be faster due to lower constant factors.

**Red Flags:**

- "Find if ANY path matches pattern" → Regex/DP might be better
- "Find longest word in grid" → Similar but may need different termination
- "Find all substrings" (not starting from each cell) → Different problem entirely

---

## Problem Statement

Given an `m x n` board of characters and a list of words, find all words that can be formed by sequentially adjacent cells (horizontal or vertical). Each cell may only be used once per word.

```
Input:
board = [
  ['o','a','a','n'],
  ['e','t','a','e'],
  ['i','h','k','r'],
  ['i','f','l','v']
]
words = ["oath","pea","eat","rain"]

Output: ["eat","oath"]
```

---

## Pattern: Trie + DFS

### Why Trie?

Without trie: For each cell, for each word, do DFS → O(m × n × k × 4^L)
With trie: Build trie from words, single DFS checks all words → O(m × n × 4^L)

Where k = number of words, L = max word length.

The trie lets us prune paths that don't match any word prefix.

### Visualization

```
Words: ["oath", "eat"]

Trie:
    root
   /    \
  o      e
  |      |
  a      a
  |      |
  t      t*
  |
  h*

Board DFS from 'o' at (0,0):
o → a → t → h ✓ Found "oath"

Board DFS from 'e' at (0,3):
e → a → t ✓ Found "eat"

Pruning: DFS from 'a' at (0,1)?
- Check trie: no 'a' from root
- Prune immediately!
```

---

## Implementation

### Optimized Solution

```python
class Solution:
    def findWords(self, board: list[list[str]], words: list[str]) -> list[str]:
        """
        Find all words from the list that exist in the board.

        Time: O(m × n × 4^L) where L = max word length
        Space: O(total chars in words) for trie
        """
        # Build trie
        root = {}
        for word in words:
            node = root
            for char in word:
                node = node.setdefault(char, {})
            node['$'] = word  # Store complete word at terminal

        m, n = len(board), len(board[0])
        result = []

        def dfs(i: int, j: int, node: dict):
            """DFS from cell (i,j) following trie node."""
            char = board[i][j]

            if char not in node:
                return

            next_node = node[char]

            # Found a word
            if '$' in next_node:
                result.append(next_node['$'])
                del next_node['$']  # Avoid duplicates

            # Mark visited
            board[i][j] = '#'

            # Explore neighbors
            for di, dj in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                ni, nj = i + di, j + dj
                if 0 <= ni < m and 0 <= nj < n and board[ni][nj] != '#':
                    dfs(ni, nj, next_node)

            # Restore
            board[i][j] = char

            # Optimization: prune empty branches
            if not next_node:
                del node[char]

        # Start DFS from every cell
        for i in range(m):
            for j in range(n):
                dfs(i, j, root)

        return result
```

### With Explicit TrieNode Class

```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.word = None  # Store word at terminal


class Solution:
    def findWords(self, board: list[list[str]], words: list[str]) -> list[str]:
        # Build trie
        root = TrieNode()
        for word in words:
            node = root
            for char in word:
                if char not in node.children:
                    node.children[char] = TrieNode()
                node = node.children[char]
            node.word = word

        m, n = len(board), len(board[0])
        result = []

        def dfs(i: int, j: int, node: TrieNode):
            char = board[i][j]

            if char not in node.children:
                return

            child = node.children[char]

            if child.word:
                result.append(child.word)
                child.word = None  # Avoid duplicates

            board[i][j] = '#'

            for di, dj in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                ni, nj = i + di, j + dj
                if 0 <= ni < m and 0 <= nj < n and board[ni][nj] != '#':
                    dfs(ni, nj, child)

            board[i][j] = char

            # Prune optimization
            if not child.children and not child.word:
                del node.children[char]

        for i in range(m):
            for j in range(n):
                dfs(i, j, root)

        return result
```

---

## Key Optimizations

### 1. Store Word at Terminal (Instead of is_end)

```python
# Instead of
node.is_end = True
# And then reconstructing the word during DFS

# Do this:
node.word = word  # Store the complete word
```

This avoids reconstructing the word from path during DFS.

### 2. Remove Word After Finding (Avoid Duplicates)

```python
if child.word:
    result.append(child.word)
    child.word = None  # Don't find same word again
```

Without this, same word could be found from different starting cells.

### 3. Prune Empty Trie Branches

```python
# After DFS returns
if not child.children and not child.word:
    del node.children[char]
```

Once a word is found and no other words share this prefix, remove the branch. This speeds up future searches.

### 4. In-place Board Marking

```python
board[i][j] = '#'  # Mark visited
# ... DFS ...
board[i][j] = char  # Restore
```

Instead of using a separate visited set, modify board directly.

---

## Complexity Analysis

| Aspect            | Value                  | Explanation                                         |
| ----------------- | ---------------------- | --------------------------------------------------- |
| Time              | O(m × n × 4^L)         | Start from each cell, max L moves with 4 directions |
| Space             | O(sum of word lengths) | Trie storage                                        |
| Space (recursion) | O(L)                   | Max depth of DFS                                    |

### Comparison: With vs Without Trie

| Approach         | Time               | Notes                       |
| ---------------- | ------------------ | --------------------------- |
| Naive (per word) | O(m × n × k × 4^L) | DFS for each of k words     |
| With Trie        | O(m × n × 4^L)     | Single DFS checks all words |

For k = 10,000 words, trie is ~10,000x faster.

---

## Common Variations

### Word Search I (Single Word)

For a single word, trie isn't needed—just DFS:

```python
def exist(self, board: list[list[str]], word: str) -> bool:
    m, n = len(board), len(board[0])

    def dfs(i: int, j: int, k: int) -> bool:
        if k == len(word):
            return True

        if (i < 0 or i >= m or j < 0 or j >= n or
            board[i][j] != word[k]):
            return False

        temp = board[i][j]
        board[i][j] = '#'

        found = (dfs(i+1, j, k+1) or dfs(i-1, j, k+1) or
                 dfs(i, j+1, k+1) or dfs(i, j-1, k+1))

        board[i][j] = temp
        return found

    for i in range(m):
        for j in range(n):
            if dfs(i, j, 0):
                return True
    return False
```

### With Frequency Pre-check

Optimization: Check if board has enough characters before DFS:

```python
from collections import Counter

def findWords(self, board: list[list[str]], words: list[str]) -> list[str]:
    # Count characters in board
    board_count = Counter()
    for row in board:
        board_count.update(row)

    # Filter words that could possibly exist
    possible_words = []
    for word in words:
        word_count = Counter(word)
        if all(board_count[c] >= word_count[c] for c in word_count):
            possible_words.append(word)

    # Now run trie + DFS only on possible words
    # ... rest of solution
```

### Finding Longest Word

Modify to track longest found:

```python
def findLongestWord(self, board, words):
    # Same trie + DFS approach
    # Track: max_length, max_word
    # Update when finding a word longer than current max
```

---

## Edge Cases

1. **Empty board**: Return empty list
2. **Empty words list**: Return empty list
3. **Single cell board**: Only matches single-char words
4. **Word longer than board cells**: Cannot exist
5. **Duplicate words in input**: Trie handles naturally (store once)
6. **Same word found multiple times**: Use `child.word = None` after finding

---

## Interview Tips

1. **Start with brute force**: Explain O(m×n×k×4^L) approach first
2. **Identify the bottleneck**: "Checking each word separately is redundant"
3. **Introduce trie**: "Trie lets us check all words simultaneously"
4. **Mention optimizations**: Pruning, storing word at terminal
5. **Space-time tradeoff**: Trie uses extra space but reduces time significantly

---

## Step-by-Step Walkthrough

```
Board:          Words: ["oath", "eat"]
o a a n
e t a e         Trie:
i h k r             root
i f l v            /    \
                  o      e
                  |      |
                  a      a
                  |      |
                  t      t*
                  |
                  h*

DFS from (0,0) 'o':
  Path: o
  Trie: root -> 'o' exists
  DFS from (1,0) 'e':
    Path: o-e
    Trie: 'o' -> 'e' doesn't exist ✗
  DFS from (0,1) 'a':
    Path: o-a
    Trie: 'o' -> 'a' exists ✓
    DFS from (1,1) 't':
      Path: o-a-t
      Trie: 'a' -> 't' exists ✓
      DFS from (2,1) 'h':
        Path: o-a-t-h
        Trie: 't' -> 'h' exists, has word! ✓
        Found: "oath"

DFS from (0,3) 'e':
  ... similar process finds "eat"
```

---

## Practice Problems

| #   | Problem              | Difficulty | Key Concept          |
| --- | -------------------- | ---------- | -------------------- |
| 1   | Word Search          | Medium     | Single word DFS      |
| 2   | Word Search II       | Hard       | Trie + DFS           |
| 3   | Concatenated Words   | Hard       | Trie + DP            |
| 4   | Stream of Characters | Hard       | Suffix trie matching |
| 5   | Word Squares         | Hard       | Trie + backtracking  |

---

## Related Sections

- [Trie Implementation](./01-trie-implementation.md) - Basic trie operations
- [Backtracking](../11-recursion-backtracking/README.md) - DFS backtracking patterns
- [Matrix Traversal](../02-arrays-strings/README.md) - Grid DFS patterns

# Word Search

> **Prerequisites:** [Recursion Basics](./01-recursion-basics.md), grid traversal concepts

## Interview Context

Word search problems test:
1. **Grid-based backtracking**: Navigate 2D arrays with constraints
2. **Path marking**: Avoid revisiting cells in current path
3. **4-directional movement**: Up, down, left, right
4. **Early termination**: Prune when word can't be completed

---

## Problem Statement

Given an m×n board and a word, determine if the word exists in the grid. The word can be constructed from letters of sequentially adjacent cells (horizontally or vertically).

```
Input:
board = [
  ['A','B','C','E'],
  ['S','F','C','S'],
  ['A','D','E','E']
]
word = "ABCCED"

Output: True (A→B→C→C→E→D)

Path visualization:
[A][B][C] E
 S  F [C] S
 A [D][E] E
```

---

## The Core Insight

From each cell that matches the first letter, try to build the word by moving to adjacent cells. Mark visited cells to avoid reuse, then unmark when backtracking.

```
Start at each cell matching word[0]:
├── Match? → Try all 4 directions for word[1]
│   ├── Match? → Continue for word[2...]
│   └── No match → Backtrack
└── No match → Try next starting cell
```

---

## Approach 1: DFS Backtracking

```python
def exist(board: list[list[str]], word: str) -> bool:
    """
    Check if word exists in grid.

    Time: O(m × n × 4^L) where L = len(word)
    Space: O(L) - recursion depth
    """
    if not board or not board[0] or not word:
        return False

    rows, cols = len(board), len(board[0])

    def dfs(row: int, col: int, index: int) -> bool:
        # Base case: found all characters
        if index == len(word):
            return True

        # Boundary check
        if row < 0 or row >= rows or col < 0 or col >= cols:
            return False

        # Character mismatch
        if board[row][col] != word[index]:
            return False

        # Mark as visited (modify in place)
        temp = board[row][col]
        board[row][col] = '#'

        # Explore all 4 directions
        found = (
            dfs(row + 1, col, index + 1) or
            dfs(row - 1, col, index + 1) or
            dfs(row, col + 1, index + 1) or
            dfs(row, col - 1, index + 1)
        )

        # Backtrack: restore cell
        board[row][col] = temp

        return found

    # Try each cell as starting point
    for r in range(rows):
        for c in range(cols):
            if dfs(r, c, 0):
                return True

    return False
```

### Visual Trace

```
board:       word = "ABCCED"
A B C E
S F C S
A D E E

Start at (0,0) 'A' = word[0] ✓
├── Mark (0,0) as '#'
├── Try (1,0) 'S' ≠ 'B' ✗
├── Try (0,1) 'B' = word[1] ✓
│   ├── Mark (0,1) as '#'
│   ├── Try (0,2) 'C' = word[2] ✓
│   │   ├── Mark (0,2) as '#'
│   │   ├── Try (1,2) 'C' = word[3] ✓
│   │   │   ├── Mark (1,2) as '#'
│   │   │   ├── Try (2,2) 'E' = word[4] ✓
│   │   │   │   ├── Try (2,1) 'D' = word[5] ✓
│   │   │   │   │   └── index == len(word), return True!
```

---

## Approach 2: Using Direction Array

Cleaner code with direction constants.

```python
def exist_v2(board: list[list[str]], word: str) -> bool:
    """Word search with direction array."""
    rows, cols = len(board), len(board[0])
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # right, left, down, up

    def dfs(row: int, col: int, index: int) -> bool:
        if index == len(word):
            return True

        if (row < 0 or row >= rows or
            col < 0 or col >= cols or
            board[row][col] != word[index]):
            return False

        temp = board[row][col]
        board[row][col] = '#'

        for dr, dc in directions:
            if dfs(row + dr, col + dc, index + 1):
                return True

        board[row][col] = temp
        return False

    for r in range(rows):
        for c in range(cols):
            if dfs(r, c, 0):
                return True
    return False
```

---

## Approach 3: With Early Termination

Pre-check if board contains all required characters.

```python
def exist_optimized(board: list[list[str]], word: str) -> bool:
    """Optimized with character frequency check."""
    from collections import Counter

    # Count characters in board
    board_count = Counter()
    for row in board:
        board_count.update(row)

    # Check if word characters are available
    word_count = Counter(word)
    for char, count in word_count.items():
        if board_count[char] < count:
            return False

    # Optimization: if last char is rarer than first, search backwards
    if board_count[word[0]] > board_count[word[-1]]:
        word = word[::-1]

    rows, cols = len(board), len(board[0])

    def dfs(row: int, col: int, index: int) -> bool:
        if index == len(word):
            return True
        if (row < 0 or row >= rows or col < 0 or col >= cols or
            board[row][col] != word[index]):
            return False

        temp = board[row][col]
        board[row][col] = '#'

        result = (dfs(row + 1, col, index + 1) or
                  dfs(row - 1, col, index + 1) or
                  dfs(row, col + 1, index + 1) or
                  dfs(row, col - 1, index + 1))

        board[row][col] = temp
        return result

    for r in range(rows):
        for c in range(cols):
            if dfs(r, c, 0):
                return True
    return False
```

---

## Word Search II: Find All Words

Find all words from a list that exist in the board.

```python
def find_words(board: list[list[str]], words: list[str]) -> list[str]:
    """
    Find all words from list in board using Trie.

    Time: O(m × n × 4^L × W) naive, O(m × n × 4^L) with Trie
    Space: O(total characters in words) for Trie
    """

    # Build Trie
    class TrieNode:
        def __init__(self):
            self.children = {}
            self.word = None  # Store complete word at end

    root = TrieNode()
    for word in words:
        node = root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.word = word

    rows, cols = len(board), len(board[0])
    result = []

    def dfs(row: int, col: int, node: TrieNode):
        if row < 0 or row >= rows or col < 0 or col >= cols:
            return

        char = board[row][col]
        if char == '#' or char not in node.children:
            return

        next_node = node.children[char]

        # Found a word
        if next_node.word:
            result.append(next_node.word)
            next_node.word = None  # Avoid duplicates

        # Mark visited
        board[row][col] = '#'

        # Explore all directions
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            dfs(row + dr, col + dc, next_node)

        # Backtrack
        board[row][col] = char

        # Optimization: prune empty branches
        if not next_node.children:
            del node.children[char]

    # Start from each cell
    for r in range(rows):
        for c in range(cols):
            dfs(r, c, root)

    return result
```

---

## Marking Visited: Different Approaches

### 1. Modify Board In-Place

```python
temp = board[row][col]
board[row][col] = '#'
# ... recurse ...
board[row][col] = temp
```

### 2. Use Visited Set

```python
def dfs(row, col, index, visited):
    if (row, col) in visited:
        return False
    visited.add((row, col))
    # ... recurse ...
    visited.remove((row, col))
```

### 3. Use Visited Matrix

```python
visited = [[False] * cols for _ in range(rows)]

def dfs(row, col, index):
    if visited[row][col]:
        return False
    visited[row][col] = True
    # ... recurse ...
    visited[row][col] = False
```

**In-place modification** is most common in interviews (space efficient).

---

## Related Problem: Find All Paths

Return all valid paths (not just existence check).

```python
def find_all_paths(board: list[list[str]], word: str) -> list[list[tuple[int, int]]]:
    """Find all paths that form the word."""
    rows, cols = len(board), len(board[0])
    result = []

    def dfs(row: int, col: int, index: int, path: list):
        if index == len(word):
            result.append(path[:])
            return

        if (row < 0 or row >= rows or col < 0 or col >= cols or
            board[row][col] != word[index]):
            return

        temp = board[row][col]
        board[row][col] = '#'
        path.append((row, col))

        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            dfs(row + dr, col + dc, index + 1, path)

        path.pop()
        board[row][col] = temp

    for r in range(rows):
        for c in range(cols):
            dfs(r, c, 0, [])

    return result
```

---

## Complexity Analysis

| Problem | Time | Space | Notes |
|---------|------|-------|-------|
| Word Search | O(m × n × 4^L) | O(L) | L = word length |
| Word Search II (naive) | O(m × n × 4^L × W) | O(L) | W = number of words |
| Word Search II (Trie) | O(m × n × 4^L) | O(total chars) | Trie optimization |

---

## Edge Cases

- [ ] Empty board or empty word
- [ ] Word longer than total cells
- [ ] Single cell board
- [ ] Word not in board
- [ ] Word requiring all cells

---

## Common Mistakes

### 1. Forgetting to Backtrack

```python
board[row][col] = '#'
result = dfs(...)
# WRONG: forgetting to restore
# CORRECT:
board[row][col] = temp
return result
```

### 2. Not Checking All Starting Points

```python
# WRONG: only checking (0,0)
return dfs(0, 0, 0)

# CORRECT: try all cells
for r in range(rows):
    for c in range(cols):
        if dfs(r, c, 0):
            return True
```

### 3. Modifying Board Permanently

```python
# WRONG: not saving original
board[row][col] = '#'

# CORRECT: save and restore
temp = board[row][col]
board[row][col] = '#'
# ... recurse ...
board[row][col] = temp
```

---

## Practice Problems

| # | Problem | Difficulty | Key Insight |
|---|---------|------------|-------------|
| 1 | Word Search | Medium | Basic grid backtracking |
| 2 | Word Search II | Hard | Trie + backtracking |
| 3 | Longest Word in Dictionary | Medium | Trie variant |
| 4 | Search Word in Matrix (8 directions) | Medium | 8 directions |

---

## Interview Tips

1. **Clarify movement**: 4 directions (typical) or 8 directions?
2. **Can cells be reused?**: Usually no within one word
3. **Modify in place**: Saves space, mention it explicitly
4. **Mention Trie**: For multiple words, Trie is expected
5. **Early termination**: Check character frequencies first

---

## Key Takeaways

1. Mark visited cells to avoid reuse in current path
2. Always restore (backtrack) after exploring
3. Try all cells as starting points
4. For multiple words, use Trie for efficiency
5. Direction array makes code cleaner

---

## Next: [09-generate-parentheses.md](./09-generate-parentheses.md)

Learn to generate all valid parentheses combinations.

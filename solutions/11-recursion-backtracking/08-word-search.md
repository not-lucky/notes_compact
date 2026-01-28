# Word Search - Solutions

This document provides optimal solutions and detailed explanations for the practice problems related to Word Search.

---

## 1. Word Search

### Problem Statement

Given an `m x n` grid of characters `board` and a string `word`, return `true` if `word` exists in the grid. The word can be constructed from letters of sequentially adjacent cells, where adjacent cells are horizontally or vertically neighboring. The same letter cell may not be used more than once.

### Examples & Edge Cases

- **Input:** board = [["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]], word = "ABCCED" → **Output:** true
- **Input:** board = [["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]], word = "ABCB" → **Output:** false
- **Edge Case:** Word length > total board size.
- **Edge Case:** All board characters same as the first character of the word.

### Optimal Python Solution (DFS with In-Place Marking)

```python
def exist(board: list[list[str]], word: str) -> bool:
    rows, cols = len(board), len(board[0])

    def dfs(r: int, c: int, i: int) -> bool:
        # Base case: found the whole word
        if i == len(word):
            return True

        # Boundary and match check
        if (r < 0 or r >= rows or
            c < 0 or c >= cols or
            board[r][c] != word[i]):
            return False

        # Mark as visited in-place
        temp = board[r][c]
        board[r][c] = "#"

        # Explore neighbors
        # (up, down, left, right)
        found = (dfs(r + 1, c, i + 1) or
                 dfs(r - 1, c, i + 1) or
                 dfs(r, c + 1, i + 1) or
                 dfs(r, c - 1, i + 1))

        # Backtrack: restore the cell
        board[r][c] = temp
        return found

    for r in range(rows):
        for c in range(cols):
            if dfs(r, c, 0):
                return True

    return False
```

### Detailed Explanation

1. **Starting Points**: We iterate through every cell in the grid. If a cell matches the first character of the word, we start a Depth First Search (DFS) from there.
2. **Path Marking**: To prevent using the same cell twice in a single word, we temporarily change the character in the `board` to a non-alphabetical character like `"#"`.
3. **Backtracking**: After exploring all possible paths from a cell, we change the character back to its original value. This is critical because that cell might be part of a different valid path starting elsewhere.

### Complexity Analysis

- **Time Complexity:** $O(M \cdot N \cdot 4^L)$ - Where $M, N$ are grid dimensions and $L$ is word length. At each cell, we have 4 choices.
- **Space Complexity:** $O(L)$ - Recursion stack depth equals the word length.

---

## 2. Word Search II

### Problem Statement

Given an `m x n` `board` of characters and a list of strings `words`, return all words on the board.

### Optimal Python Solution (Trie + Backtracking)

```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.word = None

class Solution:
    def findWords(self, board: list[list[str]], words: list[str]) -> list[str]:
        # 1. Build Trie
        root = TrieNode()
        for w in words:
            node = root
            for c in w:
                node = node.children.setdefault(c, TrieNode())
            node.word = w

        rows, cols = len(board), len(board[0])
        res = []

        def dfs(r, c, node):
            char = board[r][c]
            if char not in node.children:
                return

            next_node = node.children[char]
            if next_node.word:
                res.append(next_node.word)
                next_node.word = None # Avoid duplicates

            # Mark visited
            board[r][c] = "#"
            for dr, dc in [(0,1), (0,-1), (1,0), (-1,0)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols:
                    dfs(nr, nc, next_node)

            # Backtrack
            board[r][c] = char

            # Optimization: prune empty trie branches
            if not next_node.children:
                node.children.pop(char)

        for r in range(rows):
            for c in range(cols):
                dfs(r, c, root)
        return res
```

### Detailed Explanation

1. **Trie**: Instead of searching for each word individually (which is $O(W \cdot M \cdot N \cdot 4^L)$), we store all words in a Trie. This allows us to search for _multiple words simultaneously_ as we traverse the grid.
2. **Pruning**: If we find a word, we set `node.word = None` to ensure it's not added to the results again. More importantly, we prune leaf nodes from the Trie if they no longer lead to any words, which drastically speeds up the search.

---

## 3. Longest Word in Dictionary

### Problem Statement

Given an array of strings `words`, return the longest word in `words` that can be built one character at a time by other words in `words`.

### Optimal Python Solution (Trie + DFS)

```python
def longestWord(words: list[str]) -> str:
    word_set = set(words)
    words.sort(key=lambda x: (-len(x), x)) # Sort by length desc, then lexicographical

    for word in words:
        if all(word[:i] in word_set for i in range(1, len(word))):
            return word
    return ""
```

### Detailed Explanation

While this can be solved with a Trie, a simple Set and Sort approach is very efficient. We sort the words such that the longest and lexicographically smallest words come first. Then, for each word, we check if all its prefixes exist in the set.

---

## 4. Search Word in Matrix (8 directions)

### Problem Statement

Variation of Word Search where diagonal movements are allowed.

### Optimal Python Solution

```python
def search8Directions(board, word):
    rows, cols = len(board), len(board[0])
    # 8 possible directions
    directions = [(0,1),(0,-1),(1,0),(-1,0),(1,1),(1,-1),(-1,1),(-1,-1)]

    def dfs(r, c, i):
        if i == len(word): return True
        if not (0 <= r < rows and 0 <= c < cols) or board[r][c] != word[i]:
            return False

        temp, board[r][c] = board[r][c], "#"
        for dr, dc in directions:
            if dfs(r + dr, c + dc, i + 1):
                board[r][c] = temp
                return True
        board[r][c] = temp
        return False

    return any(dfs(r, c, 0) for r in range(rows) for c in range(cols))
```

# Solution: Word Search Practice Problems

## Problem 1: Word Search
### Problem Statement
Given an `m x n` grid of characters `board` and a string `word`, return `true` if `word` exists in the grid.
The word can be constructed from letters of sequentially adjacent cells, where adjacent cells are horizontally or vertically neighboring. The same letter cell may not be used more than once.

### Constraints
- `m == board.length`
- `n = board[i].length`
- `1 <= m, n <= 6`
- `1 <= word.length <= 15`

### Example
Input: `board = [["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]], word = "ABCCED"`
Output: `true`

### Python Implementation
```python
def exist(board: list[list[str]], word: str) -> bool:
    """
    Time Complexity: O(N * M * 4^L) where L is word length
    Space Complexity: O(L)
    """
    rows, cols = len(board), len(board[0])
    path = set()

    def dfs(r, c, i):
        if i == len(word):
            return True
        if (r < 0 or c < 0 or
            r >= rows or c >= cols or
            word[i] != board[r][c] or
            (r, c) in path):
            return False

        path.add((r, c))
        res = (dfs(r + 1, c, i + 1) or
               dfs(r - 1, c, i + 1) or
               dfs(r, c + 1, i + 1) or
               dfs(r, c - 1, i + 1))
        path.remove((r, c))
        return res

    for r in range(rows):
        for c in range(cols):
            if dfs(r, c, 0): return True
    return False
```

---

## Problem 2: Word Search II
### Problem Statement
Given an `m x n` board of characters and a list of strings `words`, return all words on the board.
Each word must be constructed from letters of sequentially adjacent cells, where adjacent cells are horizontally or vertically neighboring. The same letter cell may not be used more than once in a word.

### Constraints
- `m == board.length`
- `n == board[i].length`
- `1 <= m, n <= 12`
- `1 <= words.length <= 3 * 10^4`
- `1 <= words[i].length <= 10`

### Example
Input: `board = [["o","a","a","n"],["e","t","a","e"],["i","h","k","r"],["i","f","l","v"]], words = ["oath","pea","eat","rain"]`
Output: `["eat","oath"]`

### Python Implementation
```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.isWord = False

    def addWord(self, word):
        cur = self
        for c in word:
            if c not in cur.children:
                cur.children[c] = TrieNode()
            cur = cur.children[c]
        cur.isWord = True

def findWords(board: list[list[str]], words: list[str]) -> list[str]:
    """
    Time Complexity: O(M * N * 4^L)
    Space Complexity: O(Total chars in words) for Trie
    """
    root = TrieNode()
    for w in words:
        root.addWord(w)

    rows, cols = len(board), len(board[0])
    res, visit = set(), set()

    def dfs(r, c, node, word):
        if (r < 0 or c < 0 or
            r >= rows or c >= cols or
            board[r][c] not in node.children or
            (r, c) in visit):
            return

        visit.add((r, c))
        node = node.children[board[r][c]]
        word += board[r][c]
        if node.isWord:
            res.add(word)

        dfs(r + 1, c, node, word)
        dfs(r - 1, c, node, word)
        dfs(r, c + 1, node, word)
        dfs(r, c - 1, node, word)
        visit.remove((r, c))

    for r in range(rows):
        for c in range(cols):
            dfs(r, c, root, "")

    return list(res)
```

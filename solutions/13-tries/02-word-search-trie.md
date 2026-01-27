# Solutions: Word Search & Tries

## 1. Word Search
(LeetCode 79)

### Problem Statement
Given an `m x n` grid of characters `board` and a string `word`, return `true` if `word` exists in the grid. The word can be constructed from letters of sequentially adjacent cells, where adjacent cells are horizontally or vertically neighboring. The same letter cell may not be used more than once.

### Examples & Edge Cases
**Example:**
```
Input: board = [["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]], word = "ABCCED"
Output: true
```

### Optimal Python Solution
```python
class Solution:
    def exist(self, board: list[list[str]], word: str) -> bool:
        rows, cols = len(board), len(board[0])

        def dfs(r, c, i):
            # Base case: Found the word
            if i == len(word):
                return True
            # Out of bounds or mismatch or already visited
            if (r < 0 or r >= rows or c < 0 or c >= cols or
                board[r][c] != word[i]):
                return False

            # Mark as visited (in-place)
            temp = board[r][c]
            board[r][c] = "#"

            # Explore neighbors
            res = (dfs(r+1, c, i+1) or
                   dfs(r-1, c, i+1) or
                   dfs(r, c+1, i+1) or
                   dfs(r, c-1, i+1))

            # Backtrack
            board[r][c] = temp
            return res

        for r in range(rows):
            for c in range(cols):
                if dfs(r, c, 0):
                    return True
        return False
```

### Explanation
1.  **Backtracking**: We use DFS to explore paths from each cell.
2.  **In-place marking**: To avoid using extra space for a `visited` set, we temporarily modify `board[r][c]` to a special character.
3.  **Backtracking**: After exploring all neighbors, we restore the cell's original value.

### Complexity Analysis
*   **Time Complexity**: $O(M \times N \times 3^L)$ where $M, N$ are grid dimensions and $L$ is word length. We start a DFS from each of the $M \times N$ cells. In each step of the DFS, we explore up to 3 directions (excluding the one we came from) for a maximum depth of $L$.
*   **Space Complexity**: $O(L)$ for the recursion stack, which matches the length of the word being searched.

---

## 2. Word Search II
(LeetCode 212)

### Problem Statement
Given an `m x n` `board` of characters and a list of strings `words`, return all words on the board. Each word must be constructed from letters of sequentially adjacent cells. The same letter cell may not be used more than once in a word.

### Examples & Edge Cases
**Example:**
```
Input: board = [["o","a","a","n"],["e","t","a","e"],["i","h","k","r"],["i","f","l","v"]], words = ["oath","pea","eat","rain"]
Output: ["eat","oath"]
```

### Optimal Python Solution
```python
class Solution:
    def findWords(self, board: list[list[str]], words: list[str]) -> list[str]:
        # Build Trie
        root = {}
        for word in words:
            node = root
            for char in word:
                node = node.setdefault(char, {})
            node['$'] = word # Store the word at the end

        rows, cols = len(board), len(board[0])
        res = []

        def dfs(r, c, node):
            char = board[r][c]
            if char not in node:
                return

            curr_node = node[char]
            if '$' in curr_node:
                res.append(curr_node['$'])
                del curr_node['$'] # Avoid duplicates

            board[r][c] = "#" # Mark visited
            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and board[nr][nc] != "#":
                    dfs(nr, nc, curr_node)
            board[r][c] = char # Backtrack

            # Optimization: Prune the trie node if it has no children
            if not curr_node:
                del node[char]

        for r in range(rows):
            for c in range(cols):
                dfs(r, c, root)
        return res
```

### Explanation
1.  **Trie for Multiple Search**: Searching each word individually is too slow ($O(K \times M \times N \times 3^L)$). Using a Trie allows us to search all words simultaneously in one grid traversal.
2.  **Pruning**: A crucial optimization is removing words from the Trie once they are found and deleting Trie branches that no longer lead to any words.
3.  **DFS with Trie**: We navigate the Trie as we navigate the grid.

### Complexity Analysis
*   **Time Complexity**: $O(M \times N \times 3^L)$ where $M, N$ are grid dimensions and $L$ is the maximum word length. We perform a single grid traversal where the Trie prunes paths that don't lead to any valid words, but the worst-case exploration remains exponential relative to word length.
*   **Space Complexity**: $O(\sum \text{word length})$ to store the Trie containing all words in the dictionary.

---

## 3. Concatenated Words
(LeetCode 472)

### Problem Statement
Given an array of strings `words` (without duplicates), return all the concatenated words in the given list of words. A concatenated word is defined as a string that is comprised entirely of at least two shorter words in the given array.

### Examples & Edge Cases
**Example:**
```
Input: words = ["cat","cats","catsdogcats","dog","dogcatsdog","hippopotamuses","rat","ratcatdogcat"]
Output: ["catsdogcats","dogcatsdog","ratcatdogcat"]
```

### Optimal Python Solution
```python
class Solution:
    def findAllConcatenatedWordsInADict(self, words: list[str]) -> list[str]:
        word_set = set(words)
        memo = {}

        def can_form(word):
            if word in memo: return memo[word]
            for i in range(1, len(word)):
                prefix = word[:i]
                suffix = word[i:]
                if prefix in word_set:
                    if suffix in word_set or can_form(suffix):
                        memo[word] = True
                        return True
            memo[word] = False
            return False

        res = []
        for word in words:
            if can_form(word):
                res.append(word)
        return res
```

### Explanation
1.  **Word Splitting**: For each word, we check if it can be split into a prefix (which exists in our dictionary) and a suffix (which either exists or can itself be decomposed).
2.  **Memoization**: We store the results of sub-problems to avoid redundant calculations.
3.  **Set for O(1) Lookup**: A hashset is more efficient than a Trie here since we are looking for exact matches of word segments.

### Complexity Analysis
*   **Time Complexity**: $O(N \times L^3)$ where $N$ is the number of words and $L$ is the maximum length. For each word, we check all $L$ possible split points. For each split, we perform string slicing ($O(L)$) and a recursive call (memoized).
*   **Space Complexity**: $O(N \times L)$ to store the `word_set` for $O(1)$ lookups and the `memo` dictionary.

---

## 4. Stream of Characters
(LeetCode 1032)

### Problem Statement
Design an algorithm that accepts a stream of characters and checks if a suffix of these characters is a string of a given array of strings `words`.

### Examples & Edge Cases
**Example:**
```
StreamChecker sc = new StreamChecker(["cd", "f", "kl"]);
sc.query('a'); // false
sc.query('c'); // false
sc.query('d'); // true ("cd" is a suffix)
```

### Optimal Python Solution
```python
class StreamChecker:
    def __init__(self, words: list[str]):
        # Store words REVERSED in the Trie
        self.trie = {}
        for word in words:
            node = self.trie
            for char in reversed(word):
                node = node.setdefault(char, {})
            node['$'] = True
        self.history = []

    def query(self, letter: str) -> bool:
        self.history.append(letter)
        node = self.trie
        # Search backwards from the latest character
        for i in range(len(self.history) - 1, -1, -1):
            char = self.history[i]
            if char not in node:
                return False
            node = node[char]
            if '$' in node:
                return True
        return False
```

### Explanation
1.  **Reversed Trie**: Since we are checking suffixes, storing words in reverse in the Trie allows us to match the stream from newest character to oldest.
2.  **Backward Search**: For every query, we walk backwards through our character history in the Trie. As soon as we find a word end, we return `True`.

### Complexity Analysis
*   **Time Complexity**: $O(L)$ per query where $L$ is the maximum length of a word in the dictionary. We only need to check the last $L$ characters of the history against the reversed Trie.
*   **Space Complexity**: $O(N \times L + H)$ to store the Trie and the character history $H$.

---

## 5. Word Squares
(LeetCode 425)

### Problem Statement
Given an array of unique strings `words`, return all the word squares you can build from `words`. A sequence of strings forms a valid word square if the $k$-th row and column read the same string, for each $0 \le k < \text{max}(rows, cols)$.

### Examples & Edge Cases
**Example:**
```
Input: words = ["area","lead","wall","lady","ball"]
Output: [["wall","area","lead","lady"],["ball","area","lead","lady"]]
```

### Optimal Python Solution
```python
class Solution:
    def wordSquares(self, words: list[str]) -> list[list[str]]:
        n = len(words[0])
        # Trie to quickly find words with a given prefix
        trie = {}
        for word in words:
            node = trie
            for char in word:
                node = node.setdefault(char, {})
                if 'list' not in node: node['list'] = []
                node['list'].append(word)

        def get_words_with_prefix(prefix):
            node = trie
            for char in prefix:
                if char not in node: return []
                node = node[char]
            return node.get('list', [])

        res = []
        def backtrack(step, square):
            if step == n:
                res.append(list(square))
                return

            # The prefix for the next word is the i-th char of existing words
            prefix = "".join(word[step] for word in square)
            for candidate in get_words_with_prefix(prefix):
                square.append(candidate)
                backtrack(step + 1, square)
                square.pop()

        for word in words:
            backtrack(1, [word])
        return res
```

### Explanation
1.  **Prefix Requirement**: In a word square, the $k$-th word must start with a prefix formed by the $k$-th characters of the previous $k-1$ words.
2.  **Trie with Cache**: We store all words matching a prefix directly in the Trie nodes to speed up candidate retrieval.
3.  **Backtracking**: We build the square row by row, pruning paths where no word matches the required prefix.

### Complexity Analysis
*   **Time Complexity**: $O(N \times 26^L)$ in the absolute worst case, where $N$ is the number of words and $L$ is the length of each word. However, in practice, the prefix constraints in the word square and the Trie-based prefix lookup prune the search space significantly.
*   **Space Complexity**: $O(N \times L)$ for the Trie storage, where each node stores a list of indices or words sharing that prefix.

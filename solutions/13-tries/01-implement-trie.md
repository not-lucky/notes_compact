# Implement Trie (Prefix Tree)

## Problem Statement

Implement a trie with `insert`, `search`, and `startsWith` methods.

- `insert(word)` - Inserts the string `word` into the trie
- `search(word)` - Returns `true` if `word` is in the trie
- `startsWith(prefix)` - Returns `true` if there's any word with `prefix`

**Example:**
```
Trie trie = new Trie();
trie.insert("apple");
trie.search("apple");   // true
trie.search("app");     // false
trie.startsWith("app"); // true
trie.insert("app");
trie.search("app");     // true
```

## Building Intuition

### Why This Works

A trie exploits the structure of strings: they're sequences of characters, and prefixes are shared. Instead of storing "apple", "application", and "apply" as three separate strings, a trie stores them as a tree where the path "a-p-p-l" is shared. Each node represents a character position, and the path from root to any node spells out a prefix.

The `is_end` flag distinguishes complete words from mere prefixes. The path "a-p-p" exists in our trie, but only "app" (if inserted) would have `is_end = True`. This is why `search("app")` returns False until "app" is explicitly inserted, while `startsWith("app")` returns True as soon as any word with that prefix exists.

The time complexity O(m) for all operations (where m is word/prefix length) is trie's superpower. Compare to storing words in a list: search would be O(n*m) where n is the number of words. Or a hash set: exact search is O(m), but prefix search requires checking all words. Tries give O(m) for both exact and prefix search.

### How to Discover This

When you see "prefix matching" or "autocomplete" or "words sharing common prefixes," think trie. The key question is: "Do I need to efficiently answer queries about prefixes?" If yes, tries are likely optimal. If you only need exact match, a hash set suffices.

### Pattern Recognition

This is the **Trie / Prefix Tree** pattern. Recognize it when:
- Prefix-based operations are required (startsWith, autocomplete)
- Many strings share common prefixes
- You need to efficiently store and search a dictionary of words

## When NOT to Use

- **When only exact match is needed**: A hash set is simpler and equally efficient for exact lookups.
- **When the alphabet is very large**: With Unicode strings (100,000+ possible characters), the children map per node becomes expensive. Consider compressed tries or ternary search trees.
- **When words don't share prefixes**: The trie degenerates into n separate chains with no space savings.
- **When memory is extremely constrained**: Tries can use more memory than a simple hash set due to node overhead.

## Approach

### Structure
- Each node contains children (one for each character) and an end-of-word flag
- Children can be implemented as array (26 letters) or hash map

### Operations
- **Insert**: Traverse/create nodes for each character, mark end
- **Search**: Traverse nodes, check end-of-word flag
- **StartsWith**: Traverse nodes, return true if path exists

## Implementation

```python
class TrieNode:
    def __init__(self):
        self.children = {}  # char -> TrieNode
        self.is_end = False


class Trie:
    """
    Trie implementation using hash map for children.

    Space: O(total characters across all words)
    """
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        """
        Insert word into trie.
        Time: O(m) where m = len(word)
        """
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True

    def search(self, word: str) -> bool:
        """
        Search for exact word.
        Time: O(m)
        """
        node = self._find_node(word)
        return node is not None and node.is_end

    def startsWith(self, prefix: str) -> bool:
        """
        Check if any word starts with prefix.
        Time: O(m)
        """
        return self._find_node(prefix) is not None

    def _find_node(self, prefix: str) -> TrieNode:
        """Helper: traverse to node for given prefix."""
        node = self.root
        for char in prefix:
            if char not in node.children:
                return None
            node = node.children[char]
        return node


class TrieArray:
    """
    Trie using array for children (fixed 26 lowercase letters).
    Faster lookups but more memory if sparse.
    """
    def __init__(self):
        self.children = [None] * 26
        self.is_end = False

    def insert(self, word: str) -> None:
        node = self
        for char in word:
            idx = ord(char) - ord('a')
            if node.children[idx] is None:
                node.children[idx] = TrieArray()
            node = node.children[idx]
        node.is_end = True

    def search(self, word: str) -> bool:
        node = self._find(word)
        return node is not None and node.is_end

    def startsWith(self, prefix: str) -> bool:
        return self._find(prefix) is not None

    def _find(self, prefix: str):
        node = self
        for char in prefix:
            idx = ord(char) - ord('a')
            if node.children[idx] is None:
                return None
            node = node.children[idx]
        return node
```

## Complexity Analysis

| Operation | Time | Space |
|-----------|------|-------|
| insert | O(m) | O(m) new nodes |
| search | O(m) | O(1) |
| startsWith | O(m) | O(1) |

Where m = length of word/prefix

## Visual Representation

```
Words: ["apple", "app", "apply", "bat"]

            root
           /    \
          a      b
          |      |
          p      a
          |      |
          p      t*
         /|
        l* e (from "app")
        |
        e*  (from "apple")
        |
       (y)* (from "apply")

* = is_end = True
```

## Edge Cases

1. **Empty string**: Valid to insert/search (root is end)
2. **Prefix is a word**: `search("app")` vs `startsWith("app")`
3. **Word is prefix of another**: Both should work independently
4. **Single character words**: Single node with is_end = True

## Common Mistakes

1. **Not marking is_end**: Search returns true for prefixes
2. **Creating node before checking**: Wastes memory on failed searches
3. **Confusing search and startsWith**: Search requires is_end

## Variations

### Add and Search with Wildcards
```python
class WordDictionary:
    """
    Design word dictionary with '.' wildcard.
    """
    def __init__(self):
        self.root = TrieNode()

    def addWord(self, word: str) -> None:
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True

    def search(self, word: str) -> bool:
        """
        Search with '.' matching any character.
        Time: O(26^m) worst case with all dots
        """
        def dfs(node: TrieNode, i: int) -> bool:
            if i == len(word):
                return node.is_end

            char = word[i]
            if char == '.':
                # Try all children
                for child in node.children.values():
                    if dfs(child, i + 1):
                        return True
                return False
            else:
                if char not in node.children:
                    return False
                return dfs(node.children[char], i + 1)

        return dfs(self.root, 0)
```

### Word Search II (Multiple Words in Grid)
```python
def find_words(board: list[list[str]], words: list[str]) -> list[str]:
    """
    Find all words from dictionary that exist in board.

    Time: O(M × N × 4^L × W) where L = max word length, W = words
    Space: O(total characters in words)
    """
    # Build trie from words
    root = {}
    for word in words:
        node = root
        for char in word:
            node = node.setdefault(char, {})
        node['$'] = word  # Mark end with the word itself

    rows, cols = len(board), len(board[0])
    result = set()

    def dfs(r: int, c: int, node: dict):
        if '$' in node:
            result.add(node['$'])
            # Optional: remove word to avoid duplicates
            # del node['$']

        if r < 0 or r >= rows or c < 0 or c >= cols:
            return

        char = board[r][c]
        if char not in node:
            return

        board[r][c] = '#'  # Mark visited
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            dfs(r + dr, c + dc, node[char])
        board[r][c] = char  # Restore

    for r in range(rows):
        for c in range(cols):
            dfs(r, c, root)

    return list(result)
```

### Autocomplete System
```python
class AutocompleteSystem:
    """
    Design autocomplete with frequency-based suggestions.
    """
    def __init__(self, sentences: list[str], times: list[int]):
        self.root = {}
        self.current_node = self.root
        self.current_input = []

        for sentence, count in zip(sentences, times):
            self._add(sentence, count)

    def _add(self, sentence: str, count: int):
        node = self.root
        for char in sentence:
            if char not in node:
                node[char] = {}
            node = node[char]
        node['#'] = node.get('#', 0) + count

    def input(self, c: str) -> list[str]:
        if c == '#':
            # End of input, save sentence
            sentence = ''.join(self.current_input)
            self._add(sentence, 1)
            self.current_node = self.root
            self.current_input = []
            return []

        self.current_input.append(c)

        if self.current_node is None or c not in self.current_node:
            self.current_node = None
            return []

        self.current_node = self.current_node[c]

        # DFS to find all sentences
        suggestions = []
        self._dfs(self.current_node, self.current_input[:], suggestions)

        # Sort by frequency (desc), then lexicographically
        suggestions.sort(key=lambda x: (-x[1], x[0]))
        return [s[0] for s in suggestions[:3]]

    def _dfs(self, node, path, suggestions):
        if '#' in node:
            suggestions.append((''.join(path), node['#']))

        for char, child in node.items():
            if char != '#':
                path.append(char)
                self._dfs(child, path, suggestions)
                path.pop()
```

## Related Problems

- **Add and Search Word** - Wildcard matching
- **Word Search II** - Find words in grid using trie
- **Design Search Autocomplete System** - Frequency-based suggestions
- **Replace Words** - Replace with shortest root
- **Map Sum Pairs** - Trie with values
- **Maximum XOR of Two Numbers** - Bit trie

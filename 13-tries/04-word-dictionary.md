# Word Dictionary (Search with Wildcards)

> **Prerequisites:** [Trie Implementation](./01-trie-implementation.md), [Backtracking](../11-recursion-backtracking/README.md)

## Interview Context

"Add and Search Word" (LeetCode 211) tests your ability to extend the basic trie with wildcard matching. The '.' character can match any letter, requiring DFS exploration at wildcard positions. This problem is popular at Meta and Amazon.

---

## Problem Statement

Design a data structure that supports:
- `addWord(word)` - Adds a word to the structure
- `search(word)` - Returns true if word is in the structure; '.' matches any letter

```
WordDictionary wd = new WordDictionary();
wd.addWord("bad");
wd.addWord("dad");
wd.addWord("mad");
wd.search("pad");  // false
wd.search("bad");  // true
wd.search(".ad");  // true (matches "bad", "dad", "mad")
wd.search("b..");  // true (matches "bad")
```

---

## Pattern: Trie + DFS for Wildcards

### Key Insight

- For regular characters: follow the trie path normally
- For '.': try ALL children (DFS branching)
- Match if ANY branch leads to a valid word

### Visualization

```
Words: ["bad", "dad", "mad"]

Trie:
       root
      / | \
     b  d  m
     |  |  |
     a  a  a
     |  |  |
     d* d* d*

Search ".ad":
  At root, '.' → try b, d, m (all children)
    b → 'a' → 'a' exists? yes
      → 'd' → 'd' exists and is_end? yes!
  Found match via 'b' path ✓

Search "b..":
  At root, 'b' → follow 'b'
    At 'b', '.' → try 'a' (only child)
      At 'a', '.' → try 'd' (only child)
        At 'd', end of word? is_end = true ✓
```

---

## Implementation

### Standard Solution

```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False


class WordDictionary:
    """
    Word dictionary supporting '.' wildcard searches.

    Time:
    - addWord: O(L) where L = word length
    - search: O(26^k × L) worst case where k = number of wildcards

    Space: O(total characters in all words)
    """

    def __init__(self):
        self.root = TrieNode()

    def addWord(self, word: str) -> None:
        """Add word to dictionary."""
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True

    def search(self, word: str) -> bool:
        """
        Search for word. '.' matches any single character.
        """
        return self._search(self.root, word, 0)

    def _search(self, node: TrieNode, word: str, index: int) -> bool:
        """Recursive DFS search with wildcard support."""
        # Base case: reached end of word
        if index == len(word):
            return node.is_end

        char = word[index]

        if char == '.':
            # Wildcard: try all children
            for child in node.children.values():
                if self._search(child, word, index + 1):
                    return True
            return False
        else:
            # Regular character: follow path
            if char not in node.children:
                return False
            return self._search(node.children[char], word, index + 1)
```

### Iterative with Stack

```python
class WordDictionary:
    """Iterative approach using explicit stack."""

    def __init__(self):
        self.root = {}

    def addWord(self, word: str) -> None:
        node = self.root
        for char in word:
            if char not in node:
                node[char] = {}
            node = node[char]
        node['$'] = True  # End marker

    def search(self, word: str) -> bool:
        # Stack: (node, index)
        stack = [(self.root, 0)]

        while stack:
            node, i = stack.pop()

            if i == len(word):
                if '$' in node:
                    return True
                continue

            char = word[i]

            if char == '.':
                # Add all children to stack
                for key, child in node.items():
                    if key != '$':
                        stack.append((child, i + 1))
            else:
                if char in node:
                    stack.append((node[char], i + 1))

        return False
```

### Optimized with Length Bucketing

```python
class WordDictionary:
    """
    Optimization: Group words by length.
    If search word length doesn't match, skip entirely.
    """

    def __init__(self):
        self.root = {}
        self.word_lengths = set()  # Track valid lengths

    def addWord(self, word: str) -> None:
        self.word_lengths.add(len(word))
        node = self.root
        for char in word:
            if char not in node:
                node[char] = {}
            node = node[char]
        node['$'] = True

    def search(self, word: str) -> bool:
        # Early termination: no words of this length
        if len(word) not in self.word_lengths:
            return False

        return self._search(self.root, word, 0)

    def _search(self, node, word, i):
        if i == len(word):
            return '$' in node

        char = word[i]

        if char == '.':
            for key, child in node.items():
                if key != '$' and self._search(child, word, i + 1):
                    return True
            return False
        else:
            if char not in node:
                return False
            return self._search(node[char], word, i + 1)
```

---

## Complexity Analysis

| Operation | Best Case | Worst Case | Notes |
|-----------|-----------|------------|-------|
| addWord | O(L) | O(L) | L = word length |
| search (no wildcard) | O(L) | O(L) | Standard trie search |
| search (k wildcards) | O(L) | O(26^k × L) | Branch at each '.' |
| search (all wildcards) | O(26^L) | O(26^L) | Explores entire trie |

### Space Complexity

- Trie storage: O(total characters)
- Recursion stack: O(L) where L = word length

---

## Common Variations

### Multiple Wildcards with '*'

Handle '*' matching zero or more characters:

```python
def search_with_star(self, word: str) -> bool:
    """
    '*' matches zero or more characters.
    Example: "b*d" matches "bd", "bad", "bread"
    """
    def dfs(node, i):
        if i == len(word):
            return node.is_end

        char = word[i]

        if char == '*':
            # Try matching zero characters (skip *)
            if dfs(node, i + 1):
                return True
            # Try matching one or more characters
            for child in node.children.values():
                if dfs(child, i):  # Stay at '*'
                    return True
            return False
        elif char == '.':
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

### Regex-like Matching

```python
def match_pattern(self, pattern: str) -> list[str]:
    """
    Return all words matching pattern.
    '.' = any single char
    '*' = previous char zero or more times

    Example: "a*b.c" matches "bc", "abc", "aaaabc"
    """
    # This becomes similar to regex matching
    # Use DP or NFA simulation
    pass
```

### Magic Dictionary (LeetCode 676)

Find if any word differs by exactly one character:

```python
class MagicDictionary:
    """
    Search returns true if modifying exactly one character
    would make it match a dictionary word.
    """

    def __init__(self):
        self.root = {}

    def buildDict(self, dictionary: list[str]) -> None:
        for word in dictionary:
            node = self.root
            for char in word:
                if char not in node:
                    node[char] = {}
                node = node[char]
            node['$'] = True

    def search(self, word: str) -> bool:
        """Return true if word can match with exactly one modification."""
        return self._search(self.root, word, 0, False)

    def _search(self, node, word, i, modified):
        if i == len(word):
            return modified and '$' in node

        char = word[i]

        if modified:
            # Already modified, must match exactly
            if char not in node:
                return False
            return self._search(node[char], word, i + 1, True)
        else:
            # Try modifying at this position
            for c, child in node.items():
                if c == '$':
                    continue
                if c == char:
                    # No modification
                    if self._search(child, word, i + 1, False):
                        return True
                else:
                    # Modify this character
                    if self._search(child, word, i + 1, True):
                        return True
            return False
```

### Prefix and Suffix Search (LeetCode 745)

```python
class WordFilter:
    """
    Search for word with given prefix and suffix.

    Trick: Store "suffix#prefix" in trie.
    Query: Search for "suffix#prefix"
    """

    def __init__(self, words: list[str]):
        self.root = {}

        for weight, word in enumerate(words):
            # Insert all combinations of suffix#word
            word_with_sep = word + '#'
            for i in range(len(word) + 1):
                # suffix is word[i:]
                key = word[i:] + '#' + word
                node = self.root
                for char in key:
                    if char not in node:
                        node[char] = {}
                    node = node[char]
                    node['weight'] = weight  # Update weight at each node

    def f(self, prefix: str, suffix: str) -> int:
        """Return index of word with given prefix and suffix."""
        search_key = suffix + '#' + prefix
        node = self.root

        for char in search_key:
            if char not in node:
                return -1
            node = node[char]

        return node.get('weight', -1)
```

---

## Edge Cases

1. **Empty word**: Should empty string match empty string?
2. **All wildcards**: "..." matches any 3-letter word
3. **No matches**: Return False
4. **Single character**: "." matches any single-letter word
5. **Wildcard at start vs end**: Both work the same in this implementation
6. **Duplicate words**: addWord twice is idempotent

---

## Interview Tips

1. **Start with regular trie**: Implement addWord first (standard)
2. **Explain wildcard handling**: At '.', we must explore all branches
3. **Discuss complexity**: Highlight exponential worst case
4. **Optimization ideas**: Length bucketing, early termination
5. **Follow-up questions**: What if pattern has '*' for multi-char match?

---

## Step-by-Step Walkthrough

```
Dictionary: ["bad", "dad", "mad"]
Search: ".ad"

_search(root, ".ad", 0)
  char = '.'
  for each child in root.children: [b, d, m]

    _search(node_b, ".ad", 1)
      char = 'a'
      'a' in node_b.children? yes
      _search(node_a, ".ad", 2)
        char = 'd'
        'd' in node_a.children? yes
        _search(node_d, ".ad", 3)
          index == len(word)
          return node_d.is_end → True ✓

  First branch returned True, so return True

Result: True
```

---

## Performance Comparison

| Pattern | Time Complexity | Example |
|---------|-----------------|---------|
| "hello" | O(5) | Exact match |
| ".ello" | O(26 × 4) | Wildcard at start |
| "h.llo" | O(1 + 26 × 3) | Wildcard in middle |
| "....." | O(26^5) | All wildcards |
| ".e.l." | O(26^3 × 2) | Scattered wildcards |

---

## Practice Problems

| # | Problem | Difficulty | Key Concept |
|---|---------|------------|-------------|
| 1 | Add and Search Word | Medium | Wildcard trie search |
| 2 | Implement Magic Dictionary | Medium | Single char modification |
| 3 | Prefix and Suffix Search | Hard | Combined prefix/suffix trie |
| 4 | Camelcase Matching | Medium | Pattern matching variant |
| 5 | Match Substring After Replacement | Hard | Advanced pattern matching |

---

## Related Sections

- [Trie Implementation](./01-trie-implementation.md) - Basic trie operations
- [Backtracking](../11-recursion-backtracking/README.md) - DFS patterns
- [Regular Expressions](../16-math-basics/README.md) - For regex matching context

# Trie Implementation

> **Prerequisites:** [Hash Tables](../03-hashmaps-sets/README.md), [Tree Traversals](../06-trees/README.md)

## Interview Context

"Implement Trie" (LeetCode 208) is a fundamental problem that appears directly in interviews and serves as a building block for more complex trie problems. Interviewers use this to test your understanding of tree-like data structures and object-oriented design.

---

## Building Intuition

**Why Does a Trie Work?**

Imagine you're organizing a dictionary. If you store words in a list, finding "apple" means checking every word—O(n). If you store them in a hashmap, you get O(1) lookup but lose the ability to find "all words starting with 'app'" efficiently.

A trie is like a physical dictionary's edge-indexed tabs, but taken to the extreme: instead of tabs for A, B, C..., you have a branching path for EVERY character position.

**The Key Insight: Shared Prefixes**

```
Words: "apple", "app", "application", "apply"

Without sharing (list): 5 + 3 + 11 + 5 = 24 characters stored
With sharing (trie):    a-p-p-l-e (5) + l-i-c-a-t-i-o-n (8) + y (1) = 14 nodes

The prefix "appl" is stored ONCE and shared by all four words.
```

This sharing is why tries excel at prefix operations. When you traverse to node "app", you've already found ALL words starting with "app"—they're all in the subtree below!

**Why O(L) for Everything?**

Every operation (insert, search, prefix) is exactly L steps, where L is the word length. You're not comparing against n words; you're walking down a fixed path:

```
insert("cat"):   root → c → a → t → mark end   (3 steps)
search("cat"):   root → c → a → t → is_end?    (3 steps)
startsWith("ca"): root → c → a → exists?        (2 steps)

No matter if the trie has 10 or 10 million words, "cat" is always 3 steps.
```

**The is_end Flag: A Subtle But Critical Detail**

Here's a trap that catches many people:

```
Insert "app" and "apple" into trie.
Search for "app" → Should return True
Search for "ap"  → Should return False (not a word, just a prefix)

The path to "ap" EXISTS (it's on the way to "app" and "apple"),
but "ap" was never inserted as a word.

Solution: is_end flag marks "this node completes a word"
```

**Mental Model: The Node as a Question**

Think of each trie node as asking: "What's the next character?"

```
     "What's first?"
           |
    a  b  c  ...  z
   /   |   \
"After 'a'?"  "After 'b'?"  ...
     |
  p  r  t
 /   |   \
...
```

At any point, you can ask "Is there a word that starts with the path I've taken?" (startsWith) or "Is the path I've taken exactly a word?" (search with is_end check).

---

## When NOT to Use Tries

**1. Exact Match Only**

If you only need to check "is this word in the dictionary?" without any prefix operations, a hashset is simpler and faster:

```python
# Trie: ~50 lines of code, O(L) lookup
# HashSet: 1 line, O(L) lookup but lower constant factor

words = {"apple", "banana", "cherry"}
"apple" in words  # Simple, fast, sufficient
```

**2. Memory-Constrained Environments**

Tries can be memory-hungry. Each node stores either:
- HashMap: Python dict overhead (~200+ bytes per node)
- Array: 26 pointers × 8 bytes = 208 bytes per node

For 10,000 short words, a hashset might use 1MB while a trie uses 10MB+.

**3. Highly Sparse Character Sets**

If your strings use Unicode with rare characters, most array slots are empty:

```
Words: ["你好", "世界"]  (Chinese characters)
Using array[65536] per node? Massive waste.
HashMap-based trie works, but consider specialized structures.
```

**4. When Insertion is Rare and Prefix Queries Don't Exist**

Tries shine when you need prefix operations OR when you're building once and querying many times. If you're:
- Doing one-off word checks
- Inserting and deleting frequently
- Never using prefix operations

...then a hashset is cleaner.

**Red Flags (Don't Use Trie):**
- "Find exact match" with no prefix requirement
- "Count occurrences of X" (Counter/hashmap better)
- "Find substring" (not prefix—consider suffix tree or KMP)
- Memory limits mentioned in problem constraints

---

## Pattern: Standard Trie

A Trie is a tree where each node represents a single character, and paths from root to nodes represent prefixes/words.

### Core Components

```
TrieNode:
├── children: mapping from character → TrieNode
├── is_end: boolean marking if this node ends a word
└── (optional) count, word reference, etc.

Trie:
├── root: TrieNode (empty root)
├── insert(word): add word to trie
├── search(word): check if exact word exists
└── startsWith(prefix): check if prefix exists
```

### Visualization

```
Insert: ["app", "apple", "apt", "bat"]

Step 1: insert("app")
        root
         |
         a
         |
         p
         |
         p* ← is_end = True

Step 2: insert("apple")
        root
         |
         a
         |
         p
         |
         p*
         |
         l
         |
         e* ← is_end = True

Step 3: insert("apt")
        root
         |
         a
         |
         p
        / \
       p*  t* ← is_end = True
       |
       l
       |
       e*

Step 4: insert("bat")
        root
       /    \
      a      b
      |      |
      p      a
     / \     |
    p*  t*   t* ← is_end = True
    |
    l
    |
    e*
```

---

## Implementation

### Basic Trie (HashMap-based children)

```python
class TrieNode:
    """A node in the trie structure."""

    def __init__(self):
        self.children = {}  # char -> TrieNode
        self.is_end = False  # True if node marks end of a word


class Trie:
    """
    Prefix tree for efficient string operations.

    Time: O(L) for all operations where L = word/prefix length
    Space: O(total characters across all words)
    """

    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        """Insert a word into the trie."""
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True

    def search(self, word: str) -> bool:
        """Return True if word is in the trie."""
        node = self._find_node(word)
        return node is not None and node.is_end

    def startsWith(self, prefix: str) -> bool:
        """Return True if any word starts with prefix."""
        return self._find_node(prefix) is not None

    def _find_node(self, prefix: str) -> TrieNode | None:
        """Traverse trie following prefix, return final node or None."""
        node = self.root
        for char in prefix:
            if char not in node.children:
                return None
            node = node.children[char]
        return node
```

### Array-based Children (Faster, 26 lowercase letters)

```python
class TrieNode:
    """Node with fixed-size array for lowercase letters only."""

    def __init__(self):
        self.children = [None] * 26  # Index 0-25 for 'a'-'z'
        self.is_end = False

    def _char_to_index(self, char: str) -> int:
        return ord(char) - ord('a')


class Trie:
    """Trie optimized for lowercase letters."""

    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        node = self.root
        for char in word:
            index = ord(char) - ord('a')
            if node.children[index] is None:
                node.children[index] = TrieNode()
            node = node.children[index]
        node.is_end = True

    def search(self, word: str) -> bool:
        node = self._find_node(word)
        return node is not None and node.is_end

    def startsWith(self, prefix: str) -> bool:
        return self._find_node(prefix) is not None

    def _find_node(self, prefix: str) -> TrieNode | None:
        node = self.root
        for char in prefix:
            index = ord(char) - ord('a')
            if node.children[index] is None:
                return None
            node = node.children[index]
        return node
```

---

## Extended Operations

### Delete a Word

```python
def delete(self, word: str) -> bool:
    """
    Delete word from trie. Returns True if word existed.

    Strategy: Use recursion to delete nodes bottom-up,
    but only delete nodes that aren't part of other words.
    """
    def _delete(node: TrieNode, word: str, depth: int) -> bool:
        if depth == len(word):
            # Reached end of word
            if not node.is_end:
                return False  # Word doesn't exist
            node.is_end = False
            return len(node.children) == 0  # Delete if no children

        char = word[depth]
        if char not in node.children:
            return False  # Word doesn't exist

        child = node.children[char]
        should_delete_child = _delete(child, word, depth + 1)

        if should_delete_child:
            del node.children[char]
            # Delete this node if not end of another word and no children
            return not node.is_end and len(node.children) == 0

        return False

    return _delete(self.root, word, 0)
```

### Count Words with Prefix

```python
def countWordsWithPrefix(self, prefix: str) -> int:
    """Count all words that start with prefix."""
    node = self._find_node(prefix)
    if node is None:
        return 0
    return self._count_words(node)

def _count_words(self, node: TrieNode) -> int:
    """Count all words in subtree rooted at node."""
    count = 1 if node.is_end else 0
    for child in node.children.values():
        count += self._count_words(child)
    return count
```

### Get All Words with Prefix

```python
def getWordsWithPrefix(self, prefix: str) -> list[str]:
    """Return all words that start with prefix."""
    result = []
    node = self._find_node(prefix)
    if node is None:
        return result

    def dfs(node: TrieNode, path: list[str]):
        if node.is_end:
            result.append(prefix + ''.join(path))

        for char, child in node.children.items():
            path.append(char)
            dfs(child, path)
            path.pop()

    dfs(node, [])
    return result
```

### Trie with Word Count

```python
class TrieWithCount:
    """Trie that tracks how many times each word was inserted."""

    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        # Use count instead of boolean
        if not hasattr(node, 'count'):
            node.count = 0
        node.count += 1

    def countWord(self, word: str) -> int:
        """Return number of times word was inserted."""
        node = self._find_node(word)
        if node is None or not hasattr(node, 'count'):
            return 0
        return node.count
```

---

## Complexity Analysis

| Operation | Time | Space | Notes |
|-----------|------|-------|-------|
| Insert | O(L) | O(L) | L = word length, may create L nodes |
| Search | O(L) | O(1) | Just traversal |
| StartsWith | O(L) | O(1) | Just traversal |
| Delete | O(L) | O(L) | Recursion stack |
| Get all with prefix | O(L + k) | O(k) | k = total chars in results |

Space for entire trie: O(N × L × A) worst case
- N = number of words
- L = average word length
- A = alphabet size (26 for lowercase)

---

## Common Variations

### 1. Trie with Word Storage

Store the complete word at terminal nodes:

```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.word = None  # Store complete word instead of is_end

# Useful for Word Search II where you need to return the words
```

### 2. Trie with Prefix Count

Track how many words pass through each node:

```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False
        self.prefix_count = 0  # Words passing through this node

def insert(self, word: str) -> None:
    node = self.root
    for char in word:
        if char not in node.children:
            node.children[char] = TrieNode()
        node = node.children[char]
        node.prefix_count += 1
    node.is_end = True
```

### 3. Map Sum Pairs (LeetCode 677)

```python
class MapSum:
    """Insert words with values, sum values for prefix."""

    def __init__(self):
        self.root = {}
        self.scores = {}  # word -> value

    def insert(self, key: str, val: int) -> None:
        delta = val - self.scores.get(key, 0)
        self.scores[key] = val

        node = self.root
        for char in key:
            if char not in node:
                node[char] = {'#sum': 0}
            node[char]['#sum'] += delta
            node = node[char]

    def sum(self, prefix: str) -> int:
        node = self.root
        for char in prefix:
            if char not in node:
                return 0
            node = node[char]
        return node.get('#sum', 0)
```

---

## Edge Cases

1. **Empty string**: Should empty string be a valid word?
2. **Single character**: Works normally
3. **Duplicate inserts**: Typically no-op (already exists)
4. **Delete non-existent**: Return False, no modification
5. **Search for prefix only**: Use `startsWith`, not `search`
6. **Case sensitivity**: Decide upfront (lowercase only vs mixed)

---

## Interview Tips

1. **Ask about alphabet**: Lowercase only? Unicode? This affects array vs hashmap choice
2. **Clarify operations**: Just insert/search or also delete/count?
3. **Space discussion**: Mention tradeoff between array (faster) and hashmap (flexible)
4. **is_end is crucial**: Always emphasize that prefix existing ≠ word existing

---

## Practice Problems

| # | Problem | Difficulty | Key Concept |
|---|---------|------------|-------------|
| 1 | Implement Trie | Medium | Basic implementation |
| 2 | Replace Words | Medium | Shortest prefix replacement |
| 3 | Map Sum Pairs | Medium | Trie with values |
| 4 | Longest Word in Dictionary | Medium | Build word character by character |
| 5 | Search Suggestions System | Medium | Trie + DFS for suggestions |
| 6 | Implement Magic Dictionary | Medium | Trie with one-char tolerance |

---

## Related Sections

- [Word Search II](./02-word-search-trie.md) - Trie combined with DFS
- [Autocomplete System](./03-autocomplete.md) - Trie in system design
- [Word Dictionary](./04-word-dictionary.md) - Wildcard search

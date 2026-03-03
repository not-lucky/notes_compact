# Trie Implementation

> **Prerequisites:** [Hash Tables](../03-hashmaps-sets/README.md), [Tree Traversals](../06-trees/README.md)

## Interview Context

"Implement Trie" (LeetCode 208) is a fundamental problem that appears directly in interviews and serves as a building block for more complex trie problems. Interviewers use this to test your understanding of tree-like data structures and object-oriented design.

---

## Building Intuition

**Why Does a Trie Work?**

Imagine you're organizing a dictionary. If you store words in a list, finding "apple" means checking every word—O(n). If you store them in a hashmap, you get O(1) lookup but lose the ability to find "all words starting with 'app'" efficiently.

A trie (pronounced "try", from re**trie**val) is a tree-like data structure that organizes strings by their prefixes. Think of it like a physical dictionary's edge-indexed tabs, but taken to the extreme: instead of just having tabs for A, B, C..., you have a branching path for EVERY character position.

**The Key Insight: Shared Prefixes**

```
Words: "apple", "app", "application", "apply"

Without sharing (list): 5 + 3 + 11 + 5 = 24 characters stored
With sharing (trie):    a-p-p-l-e (5) + i-c-a-t-i-o-n (7) + y (1) + "app" reuses existing (0) = 13 nodes

The prefix "app" is stored ONCE. "apple" and "apply" further share "appl".
"app" needs zero extra nodes—it just marks the second 'p' as is_end.
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

## Quick Reference

| Operation           | Time     | Space | Notes                               |
| ------------------- | -------- | ----- | ----------------------------------- |
| **Insert**          | O(L)     | O(L)  | L = word length, may create L nodes |
| **Search**          | O(L)     | O(1)  | Just traversal                      |
| **StartsWith**      | O(L)     | O(1)  | Just traversal                      |
| **Delete**          | O(L)     | O(L)  | Recursion stack (or O(1) if iterative) |
| **Get all with prefix** | O(L + k) | O(k)  | k = total chars in results          |

**Space Complexity (Trie Total):**
- **Array-based:** O(N × L × A) worst case — each of up to N×L nodes allocates an array of size A
- **HashMap-based:** O(N × L) worst case — each node only stores entries for characters that exist
- N = number of words, L = average word length, A = alphabet size (26 for lowercase)
- *Using `__slots__` significantly reduces per-node memory overhead in Python.*

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

    __slots__ = ['children', 'is_end']

    def __init__(self):
        self.children: dict[str, 'TrieNode'] = {}  # char -> TrieNode
        self.is_end: bool = False  # True if node marks end of a word


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

    __slots__ = ['children', 'is_end']

    def __init__(self):
        self.children: list['TrieNode | None'] = [None] * 26  # Index 0-25 for 'a'-'z'
        self.is_end: bool = False


class Trie:
    """Trie optimized for lowercase letters."""

    def __init__(self):
        self.root = TrieNode()

    @staticmethod
    def _char_to_index(char: str) -> int:
        """Convert lowercase letter to array index (0-25)."""
        return ord(char) - ord('a')

    def insert(self, word: str) -> None:
        node = self.root
        for char in word:
            index = self._char_to_index(char)
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
            index = self._char_to_index(char)
            if node.children[index] is None:
                return None
            node = node.children[index]
        return node
```

---

## Extended Operations

These methods build upon the basic `Trie` class defined above.

### Iterative Search (Detailed)

While the basic implementation uses a helper method `_find_node`, here's a standalone iterative search method showing the exact logic:

```python
def search_iterative(self, word: str) -> bool:
    """Iterative search without a helper function."""
    node = self.root
    for char in word:
        if char not in node.children:
            return False
        node = node.children[char]
    return node.is_end
```

### Delete a Word

Deleting a word requires careful memory management. We only delete nodes that aren't part of other words.

```python
def delete(self, word: str) -> bool:
    """
    Delete word from trie. Returns True if word existed and was deleted.

    Strategy: Use recursion to find the word bottom-up. As we return,
    delete nodes only if they have no children and are not the end of another word.
    """
    word_found = False

    def _delete(node: TrieNode, word: str, depth: int) -> bool:
        nonlocal word_found

        # Base case: reached the end of the word
        if depth == len(word):
            if node.is_end:
                word_found = True
                node.is_end = False
            # Return True if this node can be deleted (no children and not end of another word)
            return len(node.children) == 0 and not node.is_end

        char = word[depth]
        if char not in node.children:
            return False  # Word doesn't exist

        child = node.children[char]
        should_delete_child = _delete(child, word, depth + 1)

        if should_delete_child:
            del node.children[char]
            # Return True if current node can be deleted
            return len(node.children) == 0 and not node.is_end

        return False

    _delete(self.root, word, 0)
    return word_found
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

    def dfs(current_node: TrieNode, path: list[str]):
        if current_node.is_end:
            result.append(prefix + ''.join(path))

        for char, child in current_node.children.items():
            path.append(char)
            dfs(child, path)
            path.pop()

    dfs(node, [])
    return result
```

### Trie with Word Count

```python
class CountTrieNode:
    __slots__ = ['children', 'count']

    def __init__(self):
        self.children: dict[str, 'CountTrieNode'] = {}
        self.count: int = 0  # Track how many times a word ends here


class TrieWithCount:
    """Trie that tracks how many times each word was inserted."""

    def __init__(self):
        self.root = CountTrieNode()

    def insert(self, word: str) -> None:
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = CountTrieNode()
            node = node.children[char]
        node.count += 1

    def countWord(self, word: str) -> int:
        """Return number of times word was inserted."""
        node = self.root
        for char in word:
            if char not in node.children:
                return 0
            node = node.children[char]
        return node.count
```

---

## Common Variations

### 1. Trie with Word Storage

Store the complete word at terminal nodes:

```python
class WordTrieNode:
    __slots__ = ['children', 'word']

    def __init__(self):
        self.children: dict[str, 'WordTrieNode'] = {}
        self.word: str | None = None  # Store complete word instead of is_end

# Useful for Word Search II where you need to return the words rapidly
```

### 2. Trie with Prefix Count

Track how many words pass through each node:

```python
class PrefixTrieNode:
    __slots__ = ['children', 'is_end', 'prefix_count']

    def __init__(self):
        self.children: dict[str, 'PrefixTrieNode'] = {}
        self.is_end: bool = False
        self.prefix_count: int = 0  # Words passing through this node

# Used within a Trie class:
# def insert(self, word: str) -> None:
#     node = self.root
#     for char in word:
#         if char not in node.children:
#             node.children[char] = PrefixTrieNode()
#         node = node.children[char]
#         node.prefix_count += 1
#     node.is_end = True
```

### 3. Map Sum Pairs (LeetCode 677)

```python
class MapSumNode:
    __slots__ = ['children', 'score_sum']

    def __init__(self):
        self.children: dict[str, 'MapSumNode'] = {}
        self.score_sum: int = 0  # Sum of all scores in subtree

class MapSum:
    """Insert words with values, sum values for prefix."""

    def __init__(self):
        self.root = MapSumNode()
        self.scores: dict[str, int] = {}  # word -> value

    def insert(self, key: str, val: int) -> None:
        # Calculate the difference to update prefix nodes
        delta = val - self.scores.get(key, 0)
        self.scores[key] = val

        node = self.root
        for char in key:
            if char not in node.children:
                node.children[char] = MapSumNode()
            node = node.children[char]
            node.score_sum += delta

    def sum(self, prefix: str) -> int:
        node = self.root
        for char in prefix:
            if char not in node.children:
                return 0
            node = node.children[char]
        return node.score_sum
```

---

## Edge Cases

1. **Empty string**: Should empty string be a valid word? Clarify with interviewer. If yes, root itself is marked `is_end = True`
2. **Single character**: Works normally — one child from root, marked as end
3. **Duplicate inserts**: No-op for basic trie (already `is_end = True`). For count-based trie, increment count
4. **Delete non-existent**: Return False, no modification
5. **Search for prefix only**: Use `startsWith`, not `search` — common mistake
6. **Case sensitivity**: Decide upfront (lowercase only vs mixed). Affects array sizing
7. **Words that are prefixes of each other**: e.g., "app" and "apple" — `is_end` distinguishes them
8. **Very long strings**: O(L) still, but deep recursion in delete can hit Python's recursion limit (~1000). Consider iterative delete for very long strings
9. **Non-alphabetic characters**: If input may contain digits, hyphens, etc., use hashmap-based trie or extend array size

---

## Interview Tips

1. **Ask about alphabet**: Lowercase only? Unicode? This affects array vs hashmap choice
2. **Clarify operations**: Just insert/search or also delete/count?
3. **Space discussion**: Mention tradeoff between array (faster) and hashmap (flexible)
4. **is_end is crucial**: Always emphasize that prefix existing ≠ word existing

---

## Practice Problems

### Progressive Practice (Easy → Medium → Hard)

| #   | Problem                    | LeetCode | Difficulty | Key Concept                       |
| --- | -------------------------- | -------- | ---------- | --------------------------------- |
| 1   | Implement Trie             | 208      | Medium     | Basic insert/search/startsWith    |
| 2   | Longest Word in Dictionary | 720      | Medium     | Build word character by character |
| 3   | Replace Words              | 648      | Medium     | Shortest prefix replacement       |
| 4   | Map Sum Pairs              | 677      | Medium     | Trie with values at nodes         |
| 5   | Implement Magic Dictionary | 676      | Medium     | Trie with one-char tolerance      |
| 6   | Design Add and Search Words Data Structure | 211 | Medium | Trie + DFS for '.' wildcards |
| 7   | Search Suggestions System  | 1268     | Medium     | Trie + DFS for autocomplete       |
| 8   | Maximum XOR of Two Numbers in an Array | 421 | Medium | Bitwise trie (greedy bit choice) |
| 9   | Word Search II             | 212      | Hard       | Trie + backtracking on 2D grid    |
| 10  | Palindrome Pairs           | 336      | Hard       | Trie of reversed words            |
| 11  | Stream of Characters       | 1032     | Hard       | Trie of reversed words + rolling query |

**Suggested order:** Start with #1 to nail the core implementation. Problems #2–#5 add
one twist each. #6–#7 combine trie with DFS. #8 introduces bitwise tries (a common
variant). #9–#11 are hard problems that combine tries with other techniques.

---

## Related Sections

- [Word Dictionary](./02-word-dictionary.md) - Wildcard search with '.' support
- [Replace Words](./03-replace-words.md) - Shortest prefix matching
- [Word Search II](./04-word-search-trie.md) - Trie combined with DFS on grid
- [Autocomplete System](./06-autocomplete.md) - Trie in system design

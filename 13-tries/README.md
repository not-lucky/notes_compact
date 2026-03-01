# Chapter 13: Tries

A **Trie** (pronounced "try", coming from re**trie**val) is a specialized tree data structure designed for efficient storage and retrieval of strings. Also known as a **prefix tree**, a trie stores characters in its nodes, meaning all descendants of a node share a common prefix of the string associated with that node.

Tries excel at prefix-based operations, making them the foundational data structure for autocomplete systems, spell checkers, dictionary validations, and IP routing.

---

## 1. Building Intuition: Why Tries Matter

Imagine you're building a phone's keyboard autocomplete. As the user types "app", you need to instantly suggest "apple", "application", and "applesauce". With 100,000 words in your dictionary:

- **Hashset**: You can check if "apple" exists in $O(1)$, but to find "all words starting with 'app'", you must scan the entire dictionary ($O(n \cdot L)$).
- **Sorted list + binary search**: You can find the range of 'app-' words in $O(\log n)$, but then you must still iterate through the range to collect results.
- **Trie**: You navigate directly to the 'app' node in exactly 3 steps. Everything below that node is a guaranteed valid completion.

### The Core Insight: Shared Prefixes

English words heavily share prefixes ("apple", "application", "apply"). Instead of storing "appl" multiple times, a trie stores it **once**:

```text
a → p → p → l → (branches to e, i, y)
```

Without sharing, storing "apple", "application", and "apply" requires: $5 + 11 + 5 = 21$ characters.
With a trie, they share "appl": $4$ (appl) $+ 1$ (e) $+ 7$ (ication) $+ 1$ (y) = $13$ nodes. **(38% savings)**

### The Magic of $O(L)$

In a trie, your query time depends strictly on the length of the word $L$, **not** the size of the dictionary $n$.

For a dictionary of 1 million words:
- **Exact lookup**: Hashset average is $O(L)$ (must hash the word). Trie is guaranteed $O(L)$ (walk $L$ nodes). They perform similarly.
- **Prefix search**: Hashset is $O(n \cdot L)$ (check every word). Trie is $O(L + k)$ (walk $L$ nodes to the prefix, collect $k$ descendants). Trie wins massively.

---

## 2. Trie Structure Visualization

Think of a trie like a choose-your-own-adventure book where each node is a character, and every path from the root represents a sequence of characters.

```text
Words: ["apple", "app", "apt", "bat"]

             root
           /      \
          a        b
         /          \
        p            a
       /  \           \
      p    t*          t*
     / \
    l   * (marks "app")
   /
  e* (marks "apple")

* = is_end flag (marks the end of a valid word)
```

At any given node, you can ask three critical questions:
1. **"Have I finished a valid word?"** Check the `is_end` boolean flag.
2. **"What continuations exist?"** Check the `children` dictionary or array.
3. **"How many words start here?"** Count the descendants (or store a `count` variable during insertion).

---

## 3. When to Use (and Avoid) Tries

### Strong Indicators (Use Trie)
1. **Prefix matching**: "Find all words starting with..."
2. **Autocomplete/typeahead**: Suggesting completions as a user types.
3. **Spell checking**: Finding words within an edit distance or tracking typos.
4. **Longest prefix matching**: IP routing, URL path matching.
5. **Bitwise Maximum XOR**: Finding the max XOR of two numbers in an array (using a binary trie).
6. **2D Word Search**: Finding dictionary words in a Boggle board (Trie + DFS).

### Red Flags (Avoid Trie)
1. **Exact match only**: If you never need prefix operations, a simple `set()` in Python is infinitely faster and simpler to implement.
2. **Memory constrained**: Nodes have overhead. A Python dict per node means high memory fragmentation. A massive dictionary of millions of short words might take 50MB in a HashSet but 500MB+ in a HashMap-based Trie.
3. **High-Cardinality Alphabets**: 26 lowercase English letters are fine ($O(26)$ space per node). Full Unicode ($65,536+$ characters) explodes memory usage if using arrays, and hash maps get fragmented.
4. **Substring Search**: "Find words containing 'cat'" is NOT a prefix problem. You need an inverted index, suffix tree/array, or KMP algorithm instead.

---

## 4. Time and Space Complexity

Let $L$ be the length of the word, $n$ be the total number of words, and $k$ be the number of results found.

| Operation | Time Complexity | Space Complexity | Description |
| :--- | :--- | :--- | :--- |
| **Insert** | $O(L)$ | $O(L)$ | Add a word. In the worst case, adds $L$ new nodes. |
| **Search (Exact)** | $O(L)$ | $O(1)$ | Traverse $L$ nodes. Returns `is_end`. |
| **StartsWith (Prefix)** | $O(L)$ | $O(1)$ | Traverse $L$ nodes. Returns true if reached without error. |
| **Prefix Words** | $O(L + k)$ | $O(k)$ | Walk $L$ nodes, then DFS to collect $k$ words. |
| **Delete** | $O(L)$ | $O(1)$ | Traverse and unmark `is_end` (and optionally prune dead branches). |

### Space Complexity Breakdown
For $n$ words with average length $L$ and alphabet size $A$:
- **Worst case**: $O(n \cdot L \cdot A)$ (No shared prefixes, all nodes distinct).
- **Best case**: $O(L \cdot A)$ (All words share the same exact prefix path).

---

## 5. Implementation Choices: Array vs HashMap

In Python, you have two primary ways to represent `children`:

```python
# Array-based (26 letters) - Faster, deterministic, more memory
class TrieNodeArray:
    def __init__(self):
        self.children = [None] * 26
        self.is_end = False

# HashMap-based - Flexible, space-efficient for sparse tries
class TrieNodeHash:
    def __init__(self):
        self.children = {}
        self.is_end = False
```

| Aspect | Array-based `[None] * 26` | HashMap-based `{}` |
| :--- | :--- | :--- |
| **Access Time** | $O(1)$ absolute | $O(1)$ amortized (hashing overhead) |
| **Memory** | High (26 pointers per node, mostly null) | Low for sparse tries, higher overhead per key |
| **Best For** | Dense tries, fixed alphabet (e.g., lowercase only) | Sparse tries, arbitrary characters (Unicode) |
| **Interviews** | Safe, shows deep understanding of ASCII math | Standard Pythonic approach, highly recommended |

---

## 6. Standard Trie Template (Python 3)

This is the canonical HashMap-based implementation you should memorize.

```python
from typing import Optional

class TrieNode:
    def __init__(self):
        self.children: dict[str, 'TrieNode'] = {}
        self.is_end: bool = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True

    def search(self, word: str) -> bool:
        node = self._find_node(word)
        return node is not None and node.is_end

    def startsWith(self, prefix: str) -> bool:
        return self._find_node(prefix) is not None

    def _find_node(self, prefix: str) -> Optional[TrieNode]:
        node = self.root
        for char in prefix:
            if char not in node.children:
                return None
            node = node.children[char]
        return node
```

### Common Pitfalls
1. **Forgetting the `is_end` flag**: Just because a node exists doesn't mean the word ends there (e.g., "app" might be a prefix for "apple", but "app" itself might not have been inserted).
2. **Not handling empty strings**: Inserting `""` should just mark the root's `is_end` as `True`.
3. **Memory leaks on delete**: If you delete "apple", you should ideally prune the `e`, `l`, `p`, `p` nodes if they have no other children, rather than just unmarking `is_end`.

---

## 7. Classic Interview Problems

| Pattern | Problems | Key Strategy |
| :--- | :--- | :--- |
| **Basic Trie** | Implement Trie, Design Add/Search Words Data Structure | Standard implementation template. |
| **Trie + DFS (2D Grid)** | Word Search II | Backtrack on the grid while traversing the Trie simultaneously. |
| **Autocomplete** | Design Search Autocomplete System | Store top-$k$ frequencies directly in nodes to speed up retrieval. |
| **Bitwise Trie** | Maximum XOR of Two Numbers in an Array | Insert 32-bit binary strings; greedily follow the *opposite* bit. |

## 8. Chapter Contents

| # | Topic | Key Concepts |
| :--- | :--- | :--- |
| 01 | [Trie Implementation](./01-trie-implementation.md) | Insert, Search, StartsWith, Delete operations. |
| 02 | [Word Dictionary](./02-word-dictionary.md) | Searching with wildcards (`.`) and edit distances. |
| 03 | [Replace Words](./03-replace-words.md) | Shortest prefix match. |
| 04 | [Word Search II](./04-word-search-trie.md) | Trie + DFS optimization on a 2D grid. |
| 06 | [Autocomplete System](./06-autocomplete.md) | Designing a typeahead autocomplete system. |
| 08 | [Maximum XOR](./08-maximum-xor.md) | Using Bitwise tries to solve XOR problems. |

---

## Start: [01-trie-implementation.md](./01-trie-implementation.md)

Begin with the fundamental trie implementation that forms the basis for all prefix-based interview questions.
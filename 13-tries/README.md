# Chapter 13: Tries

A Trie (prefix tree) is a specialized tree data structure used for efficient retrieval of strings. The name comes from "re**trie**val." Tries excel at prefix-based operations, making them essential for autocomplete, spell checking, and IP routing.

## Why Tries Matter

1. **Interview frequency**: Tries appear in ~10-15% of FANG interviews
2. **Unique niche**: Some problems are nearly impossible without tries
3. **Design interviews**: Autocomplete is a classic system design component
4. **Time efficiency**: O(L) operations where L is word length, regardless of dictionary size

---

## Building Intuition

**What Problem Does a Trie Solve?**

Imagine you're building a phone's keyboard autocomplete. As the user types "app", you need to instantly suggest "apple", "application", "applesauce". With 100,000 words in your dictionary:

- **Hashset**: Can check "does 'apple' exist?" but can't find "all words starting with 'app'" without scanning everything
- **Sorted list + binary search**: Can find the range of 'app-' words in O(log n), but then must scan the range
- **Trie**: Navigate directly to the 'app' node; everything below is your answer

**The Core Insight: Shared Prefixes**

English words share prefixes heavily. "apple", "application", "apply" all share "appl". Instead of storing this 4 times, a trie stores it ONCE:

```
a → p → p → l → (branches to e, i, y)

4 nodes for "appl" shared by all 3 words.
Without sharing: 5 + 11 + 5 = 21 characters
With sharing: 4 + 1 + 7 + 1 = 13 characters (38% savings)
```

**Why O(L) for Everything?**

The magic of a trie: your query time depends on word length L, NOT dictionary size n.

```
Dictionary of 1 million words:
  Hashset lookup: O(L) average — must hash the whole word
  Trie lookup: O(L) guaranteed — just walk L nodes

They're the same for exact lookup! But for prefixes...

"Find all words starting with 'app'":
  Hashset: O(n × L) — must check every word
  Trie: O(L + k) — walk 3 nodes to 'app', then collect k results
```

**Mental Model: A Branching Path**

Think of a trie like a choose-your-own-adventure book where each page is a letter:

```
Page 1: "What's your first letter?" → Turn to page A, B, C, ...
Page A: "After 'a', what's next?" → Turn to page AP, AR, AT, ...
Page AP: "After 'ap', what's next?" → Turn to page APP, APT, ...
...
```

At any page (node), you can ask:

- "Have I finished a valid word?" (check is_end flag)
- "What continuations exist?" (check children)
- "How many words start here?" (count descendants)

---

## When NOT to Use Tries

**1. Exact Match Only (No Prefix Operations)**

If you only need "does this word exist?", a hashset is simpler:

```python
# Hashset: 1 line, O(1) average lookup
words = {"apple", "banana"}
"apple" in words  # True

# Trie: 50+ lines of code for the same result
```

Trie shines when you need prefix operations.

**2. Memory-Constrained Environments**

Each trie node carries overhead:

- HashMap-based: ~200+ bytes per node (Python dict overhead)
- Array-based: 26 × 8 = 208 bytes per node

For a million short words, a hashset uses ~50MB; a trie might use 500MB+.

**3. Numeric or High-Cardinality Alphabets**

26-letter alphabet: 26 possible children per node (manageable)
Unicode: 65,536+ possible children per node (explosion!)

For numeric data, segment trees or other structures often work better.

**4. Substring Search (Not Prefix)**

"Find words CONTAINING 'cat'" is not a prefix problem. You'd need:

- Inverted index
- Suffix tree/array
- Full-text search (like Lucene)

**Red Flags That Suggest NOT Using Trie:**

- "Find exact matches only"
- "Memory limit is tight"
- "Search for substring" (not prefix)
- "Unicode/arbitrary alphabet"

---

## Trie vs Other Data Structures

| Operation             | Trie                      | HashMap        | BST            | Sorted Array   |
| --------------------- | ------------------------- | -------------- | -------------- | -------------- |
| Insert                | O(L)                      | O(L)           | O(L log n)     | O(n)           |
| Search                | O(L)                      | O(L)           | O(L log n)     | O(L log n)     |
| Prefix search         | O(L)                      | O(n × L)       | O(n)           | O(n)           |
| Space                 | O(alphabet × total chars) | O(total chars) | O(total chars) | O(total chars) |
| **Prefix operations** | **Excellent**             | Poor           | Poor           | Poor           |

L = word length, n = number of words

---

## Trie Structure Visualization

```
Words: ["apple", "app", "apt", "bat"]

             root
           /      \
          a        b
         /          \
        p            a
       /  \           \
      p    t           t
     /      \
    l        *          *
   /
  e
   \
    *

* = marks end of word
```

---

## When to Use Tries

### Strong Indicators (Use Trie)

1. **Prefix matching**: "Find all words starting with..."
2. **Autocomplete/typeahead**: Suggest completions as user types
3. **Spell checking**: Find words within edit distance
4. **Word validation**: Check if a word exists in dictionary
5. **Longest prefix matching**: IP routing, URL matching

### Weak Indicators (Consider Alternatives)

1. **Exact match only**: HashMap is simpler and faster
2. **Infrequent lookups**: Overhead not justified
3. **Memory constrained**: Tries can be space-intensive
4. **Numeric data**: Segment tree or other structures better

---

## Core Trie Operations

| Operation    | Time     | Space | Description                              |
| ------------ | -------- | ----- | ---------------------------------------- |
| Insert       | O(L)     | O(L)  | Add word to trie                         |
| Search       | O(L)     | O(1)  | Check if exact word exists               |
| StartsWith   | O(L)     | O(1)  | Check if prefix exists                   |
| Delete       | O(L)     | O(1)  | Remove word from trie                    |
| Prefix Words | O(L + k) | O(k)  | Find all words with prefix (k = results) |

---

## Trie Patterns Overview

| Pattern         | Problems                        | Key Strategy                   |
| --------------- | ------------------------------- | ------------------------------ |
| Basic Trie      | Implement trie, word dictionary | Standard implementation        |
| Trie + DFS      | Word Search II, word break      | Combine trie with backtracking |
| Trie + Wildcard | Add and search word             | DFS at wildcard positions      |
| Bitwise Trie    | Maximum XOR                     | Store binary representations   |
| Trie + Count    | Top K frequent words            | Store frequency in nodes       |

---

## Chapter Contents

| #   | Topic                                              | Key Concepts                       |
| --- | -------------------------------------------------- | ---------------------------------- |
| 01  | [Trie Implementation](./01-trie-implementation.md) | Insert, search, startsWith, delete |
| 02  | [Word Search II](./02-word-search-trie.md)         | Trie + DFS optimization            |
| 03  | [Autocomplete System](./03-autocomplete.md)        | Design search autocomplete         |
| 04  | [Word Dictionary](./04-word-dictionary.md)         | Search with wildcards              |
| 05  | [Maximum XOR](./05-maximum-xor.md)                 | Bitwise trie for XOR               |

---

## Implementation Choices

### Array-based vs HashMap-based Children

```python
# Array-based (26 letters) - faster but more memory
class TrieNode:
    def __init__(self):
        self.children = [None] * 26  # Fixed size array
        self.is_end = False

# HashMap-based - flexible, less memory for sparse tries
class TrieNode:
    def __init__(self):
        self.children = {}  # Dynamic size
        self.is_end = False
```

| Aspect      | Array-based                 | HashMap-based                |
| ----------- | --------------------------- | ---------------------------- |
| Access time | O(1)                        | O(1) amortized               |
| Memory      | 26 pointers per node        | Only used letters            |
| Best for    | Dense tries, lowercase only | Sparse tries, any characters |
| Interview   | More common                 | More flexible                |

---

## Common Mistakes

1. **Forgetting is_end flag**: A prefix existing doesn't mean word exists
2. **Memory leaks on delete**: Not cleaning up empty branches
3. **Wrong alphabet size**: Assuming 26 when unicode is possible
4. **Not handling empty string**: Edge case often forgotten
5. **Modifying during iteration**: Concurrent modification issues

---

## Time Complexity Patterns

| Problem Type        | Time           | Why                         |
| ------------------- | -------------- | --------------------------- |
| Insert n words      | O(n × L_avg)   | Each word takes O(L)        |
| Search with prefix  | O(L + k)       | L for prefix, k for results |
| Word search in grid | O(m × n × 4^L) | DFS from each cell          |
| Autocomplete top-k  | O(L + k log k) | Traverse + heap for top-k   |

---

## Space Complexity Analysis

For n words with average length L and alphabet size A:

```
Worst case: O(n × L × A)  - no shared prefixes
Best case:  O(L × A)      - all words share prefixes
Typical:    O(total_chars × A) - some sharing

# Example: ["apple", "app", "application"]
# Nodes: a-p-p-l-e + l-i-c-a-t-i-o-n = 13 nodes
# If stored separately: 5 + 3 + 11 = 19 characters
# Trie saves: 6 characters worth of nodes
```

---

## Classic Interview Problems by Company

| Company   | Favorite Trie Problems                                    |
| --------- | --------------------------------------------------------- |
| Google    | Word Search II, Autocomplete, Concatenated Words          |
| Meta      | Add and Search Word, Implement Trie, Stream of Characters |
| Amazon    | Search Suggestions System, Replace Words                  |
| Microsoft | Longest Word in Dictionary, Prefix and Suffix Search      |
| Apple     | Word Squares, Palindrome Pairs                            |

---

## Trie Problem Signals

Look for these keywords/patterns:

```
- "Prefix" → almost always trie
- "Autocomplete" → trie + frequency
- "Dictionary" → consider trie vs hashmap
- "Word search in grid" → trie + DFS
- "Multiple string matching" → trie over repeated binary search
- "XOR maximum/minimum" → bitwise trie
```

---

## Comparison: When Trie vs HashMap

| Scenario                 | Use Trie | Use HashMap |
| ------------------------ | -------- | ----------- |
| Prefix operations needed | ✓        |             |
| Only exact match         |          | ✓           |
| Autocomplete feature     | ✓        |             |
| Fixed small dictionary   |          | ✓           |
| Memory is critical       |          | ✓           |
| Wildcard search          | ✓        |             |

---

## Common Trie Variations

### 1. Compressed Trie (Radix Tree)

Merge chains of single-child nodes:

```
Standard:  a → p → p → l → e
Compressed: "app" → "le"
```

Used in: IP routing, suffix trees

### 2. Ternary Search Tree

Three children: less, equal, greater

```
Balanced like BST, prefix search like trie
Lower memory than standard trie
```

### 3. Suffix Trie

Insert all suffixes of a string:

```
"banana": banana, anana, nana, ana, na, a
Used for substring search
```

---

## Quick Reference: Standard Trie Template

```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False

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

    def _find_node(self, prefix: str) -> TrieNode:
        node = self.root
        for char in prefix:
            if char not in node.children:
                return None
            node = node.children[char]
        return node
```

---

## Start: [01-trie-implementation.md](./01-trie-implementation.md)

Begin with the fundamental trie implementation that forms the basis for all trie problems.

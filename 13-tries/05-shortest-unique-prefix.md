# Shortest Unique Prefix

[Previous: Word Search Trie](./04-word-search-trie.md) | [Next: Autocomplete](./06-autocomplete.md)

> **Prerequisites:** [Trie Implementation](./01-trie-implementation.md), [Trie with Prefix Count variant](./01-trie-implementation.md#2-trie-with-prefix-count)

## Quick Reference

| Operation | Time Complexity | Space Complexity | Description |
| :--- | :--- | :--- | :--- |
| Build Trie | $O(N \cdot L)$ | $O(N \cdot L)$ | $N$ words of average length $L$. |
| Find One Prefix | $O(L)$ | $O(L)$ | Traverse path up to length $L$, build prefix string. |
| Find All Prefixes | $O(N \cdot L)$ | $O(N \cdot L)$ | One pass per word after trie is built. |

## Interview Context

Finding shortest unique prefixes is a classic trie problem that tests your understanding of **prefix counting**—a trie variant where each node tracks how many words pass through it. It appears on platforms like GeeksforGeeks and in interview prep for Amazon and Google. The core idea also shows up as a subproblem in autocomplete systems and dictionary compression.

This problem is an excellent follow-up to "Implement Trie" (LeetCode 208) because it demonstrates a practical use of augmenting trie nodes with metadata beyond the basic `is_end` flag.

---

## Building Intuition

**The Problem**

Given a list of words, find the shortest prefix for each word such that the prefix uniquely identifies that word among all words in the list.

```
Input:  ["zebra", "dog", "duck", "dove"]
Output: ["z", "dog", "du", "dov"]

"z"   → only "zebra" starts with 'z'
"dog" → "dog" needs all 3 chars (shares "do" with "dove" and "duck")
"du"  → only "duck" starts with "du"
"dov" → only "dove" starts with "dov"
```

**The Naive Approach**

For each word, try prefixes of increasing length until you find one that no other word shares:

```python
for word in words:
    for length in range(1, len(word) + 1):
        prefix = word[:length]
        if no_other_word_starts_with(prefix, words):
            result.append(prefix)
            break
```

This is $O(N^2 \cdot L^2)$—for each word, for each prefix length, you scan all other words. Far too slow for large inputs.

**The Key Insight: Prefix Count**

If we augment each trie node with a `prefix_count` (how many words pass through that node during insertion), then finding the unique prefix becomes trivial:

> **A prefix is unique when you reach a node where `prefix_count == 1`.**

Why does this work? When we insert a word, every node along its path gets its `prefix_count` incremented. If a node's `prefix_count` is 1, it means exactly ONE word in the entire input passes through this node. That means the prefix up to this point uniquely identifies that word—no other word shares this path.

**Step-by-Step Walkthrough**

```
Words: ["zebra", "dog", "duck", "dove"]

Insert "zebra": z(1) → e(1) → b(1) → r(1) → a(1)
Insert "dog":   d(1) → o(1) → g(1)
Insert "duck":  d(2) → u(1) → c(1) → k(1)
Insert "dove":  d(3) → o(2) → v(1) → e(1)

(Numbers in parentheses are prefix_count at each node)
```

Now find unique prefixes:

```
"zebra": z(1) → STOP! prefix_count == 1 → prefix = "z"
"dog":   d(3) → o(2) → g(1) → STOP! → prefix = "dog"
"duck":  d(3) → u(1) → STOP! → prefix = "du"
"dove":  d(3) → o(2) → v(1) → STOP! → prefix = "dov"
```

---

## Visualization

```
Words: ["zebra", "dog", "duck", "dove"]

Trie with prefix_count at each node:

              root
             /    \
          z(1)    d(3)
           |      / \
         e(1)  o(2)  u(1)
           |   / \     \
         b(1) g(1) v(1) c(1)
           |         |     \
         r(1)      e(1)   k(1)
           |
         a(1)

Finding unique prefixes (stop at first node with count == 1):

  "zebra" → z[1] ✓                     → "z"
  "dog"   → d[3] → o[2] → g[1] ✓      → "dog"
  "duck"  → d[3] → u[1] ✓             → "du"
  "dove"  → d[3] → o[2] → v[1] ✓      → "dov"
```

---

## When NOT to Use This Pattern

**1. Duplicate Words in Input**

If two identical words exist (e.g., `["dog", "dog"]`), no prefix can uniquely distinguish them. The `prefix_count` will never reach 1 along the shared path. You'll return the full word, which is arguably wrong since the prefix still isn't unique. Clarify with your interviewer whether duplicates are possible.

**2. One Word is a Prefix of Another**

If input is `["dog", "dogfish"]`, the prefix for `"dog"` will be `"dog"` itself (prefix_count at `g` is 2 because `"dogfish"` also passes through it). This is correct behavior—`"dog"` needs all three characters to distinguish from `"dogfish"`.

**3. Single Word in Input**

With only one word, every node has `prefix_count == 1`, so the result is always just the first character. This is correct but trivial.

**4. When You Need Substring Matching (Not Prefix)**

This pattern only finds distinguishing *prefixes*. If you need the shortest *substring* that identifies a word, you need a suffix trie or other approach.

**Red Flags:**

- "Find unique identifier that could be anywhere in the string" → Not a prefix problem
- "Words may be identical" → Unique prefix undefined; clarify constraints
- "Minimize total prefix length" → Different optimization problem (greedy/DP)

---

## Implementation

### Standard Trie Solution

```python
class TrieNode:
    """Trie node tracking how many words pass through it."""
    __slots__ = ['children', 'prefix_count']

    def __init__(self) -> None:
        self.children: dict[str, 'TrieNode'] = {}
        self.prefix_count: int = 0


class Solution:
    def __init__(self) -> None:
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        """Insert word, incrementing prefix_count at each node along the path."""
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
            node.prefix_count += 1  # One more word passes through here

    def get_shortest_unique_prefix(self, word: str) -> str:
        """
        Walk the trie following `word`. Stop as soon as we reach a node
        where prefix_count == 1, meaning only this word passes through.

        Uses a list + join instead of string concatenation to avoid
        O(L^2) cost from repeated string building.
        """
        node = self.root
        chars: list[str] = []
        for char in word:
            chars.append(char)
            node = node.children[char]
            if node.prefix_count == 1:
                break
        return ''.join(chars)

    def find_prefixes(self, words: list[str]) -> list[str]:
        """
        Find shortest unique prefix for every word.

        Time:  O(N * L) — insert all words, then query all words
        Space: O(N * L) — trie storage
        """
        # Phase 1: Insert all words to build prefix counts
        for word in words:
            self.insert(word)

        # Phase 2: Query each word for its unique prefix
        return [self.get_shortest_unique_prefix(word) for word in words]
```

**Why `list` + `join` instead of `prefix += char`?**

String concatenation with `+=` creates a new string object each iteration. For a word of length $L$, this copies 1 + 2 + ... + L = $O(L^2)$ characters total. Using a list of characters and joining at the end is $O(L)$.

In practice, CPython often optimizes `+=` for strings with a refcount of 1, but this optimization is an implementation detail—not guaranteed and not portable to PyPy or other runtimes. Using `list` + `join` is the idiomatic and reliably $O(L)$ approach.

---

## Edge Cases

1. **Duplicate words:** `["dog", "dog"]` — `prefix_count` at the final `g` node is 2, so the entire word `"dog"` is returned for both. The prefix isn't truly unique. Clarify constraints with interviewer.
2. **One word is a prefix of another:** `["dog", "dogfish"]` — `"dog"` returns `"dog"` (all 3 chars needed), `"dogfish"` returns `"dogf"` (first char after the shared prefix).
3. **All words share no prefix:** `["apple", "banana", "cherry"]` — each returns its first character: `["a", "b", "c"]`.
4. **Single word:** `["hello"]` — returns `"h"` (prefix_count is 1 at every node).
5. **Empty word list:** Returns `[]`.
6. **Single-character words:** `["a", "b", "c"]` — each is its own unique prefix: `["a", "b", "c"]`.
7. **Long shared prefix:** `["aaaa", "aaab", "aaac"]` — returns `["aaaa", "aaab", "aaac"]` since they share `"aaa"` and diverge only at the last character.

---

## Complexity Analysis

| Phase | Time | Space | Notes |
| :--- | :--- | :--- | :--- |
| **Build Trie** | $O(N \cdot L)$ | $O(N \cdot L)$ | $N$ words, average length $L$. Each insertion is $O(L)$. |
| **Find One Prefix** | $O(L)$ | $O(L)$ | Traverse at most $L$ nodes; build result string of length $\leq L$. |
| **Find All Prefixes** | $O(N \cdot L)$ | $O(N \cdot L)$ | Query each of $N$ words. Output size is $O(N \cdot L)$ worst case. |
| **Total** | $O(N \cdot L)$ | $O(N \cdot L)$ | Two linear passes over the input. |

### Space Breakdown

- **Trie nodes:** At most $O(N \cdot L)$ nodes (worst case: no shared prefixes).
- **Output:** At most $O(N \cdot L)$ total characters across all prefixes.
- **Per-node overhead:** `dict` + `int`. Using `__slots__` eliminates per-instance `__dict__`, saving ~100 bytes per node.

---

## Common Variations

### 1. Return Prefix Lengths Instead of Strings

Sometimes you only need the *length* of the shortest unique prefix:

```python
def get_prefix_lengths(self, words: list[str]) -> list[int]:
    """Return the length of the shortest unique prefix for each word."""
    for word in words:
        self.insert(word)

    result: list[int] = []
    for word in words:
        node = self.root
        length = 0
        for char in word:
            length += 1
            node = node.children[char]
            if node.prefix_count == 1:
                break
        result.append(length)
    return result
```

### 2. Shortest Unique Prefix for a Subset

Given a full dictionary and a query list, find unique prefixes only within the dictionary context. Build the trie from the dictionary, then query each word in the subset.

### 3. Minimum Total Prefix Length

A variation asks: what is the minimum *total* length of all unique prefixes? This is simply the sum of prefix lengths from the standard solution. No additional optimization is needed since each prefix is already minimal.

### 4. Encoding Table (Compression)

Shortest unique prefixes can serve as a compression scheme—map each word to its prefix for compact representation in protocols or file headers. The decoder needs the same word list to reconstruct.

---

## Interview Tips

1. **Start by clarifying:** Are all words distinct? Can one word be a prefix of another? This affects whether a valid unique prefix always exists.
2. **Explain prefix_count clearly:** "Each node tracks how many words pass through it during insertion. When only one word passes through a node, the prefix up to that node uniquely identifies that word."
3. **Mention the two-phase approach:** Build the trie first (all inserts), then query. Don't interleave—counts must be final before querying.
4. **Avoid string concatenation in the interview:** Use `list` + `join`. Mention why if asked—it shows awareness of Python string immutability and amortized cost.
5. **Know the edge cases:** Especially duplicates and prefix-of-another. These are common follow-ups.
6. **Compare to alternatives:** A naive $O(N^2 \cdot L)$ approach checks each word's prefixes against all others. The trie reduces this to $O(N \cdot L)$ by precomputing shared prefix information.

---

## Practice Problems

| # | Problem | Difficulty | Key Concept |
| :--- | :--- | :--- | :--- |
| 1 | [Shortest Unique Prefix (GFG)](https://www.geeksforgeeks.org/find-shortest-unique-prefix-every-word-given-list/) | Medium | Core prefix_count technique |
| 2 | Implement Trie (LeetCode 208) | Medium | Foundation for this pattern |
| 3 | Replace Words (LeetCode 648) | Medium | Shortest prefix replacement (related pattern) |
| 4 | Longest Common Prefix (LeetCode 14) | Easy | Trie approach to shared prefixes |
| 5 | Search Suggestions System (LeetCode 1268) | Medium | Prefix-based retrieval |
| 6 | Implement Trie II — Prefix and Word Count (LeetCode 1804) | Medium | prefix_count variant used here |
| 7 | Short Encoding of Words (LeetCode 820) | Medium | Suffix trie / unique suffix problem |

---

## Related Sections

- [Trie Implementation](./01-trie-implementation.md) — Core trie and the Prefix Count variant used here
- [Replace Words](./03-replace-words.md) — Related pattern: find shortest *matching* prefix from a dictionary
- [Autocomplete](./06-autocomplete.md) — Builds on prefix counting for ranked suggestions
- [Word Dictionary](./02-word-dictionary.md) — Wildcard search in tries

# Replace Words

[Previous: Word Dictionary](./02-word-dictionary.md) | [Next: Word Search Trie](./04-word-search-trie.md)

> **Prerequisites:** [Trie Implementation](./01-trie-implementation.md), [Hash Tables](../03-hashmaps-sets/README.md)

## Quick Reference

| Operation | Complexity | Explanation |
| :--- | :--- | :--- |
| **Build Trie** | `O(N \cdot L)` | `N` is number of dictionary words, `L` is average length. |
| **Replace Words** | `O(M \cdot K)` | `M` is number of words in sentence, `K` is average length. Find shortest prefix in Trie. |
| **Total Time** | `O(N \cdot L + M \cdot K)` | Linear in the total size of the input dictionary and sentence. |
| **Space Complexity** | `O(N \cdot L + M \cdot K)` | Space for the Trie and the output sentence. |

## Interview Context

"Replace Words" (LeetCode 648) is a classic medium-level problem that tests your ability to use a Trie for efficient prefix matching. It asks you to replace words in a sentence with their shortest matching "root" from a given dictionary. It frequently appears in interviews at companies like Amazon, Uber, and Google.

---

## Building Intuition

**The Problem**

You are given a dictionary of "roots" (e.g., `["cat", "bat", "rat"]`) and a sentence (e.g., `"the cattle was rattled by the battery"`). You need to replace every word in the sentence with the shortest root that forms a prefix of that word.

Output: `"the cat was rat by the bat"`

**The Naive Approach**

For each word in the sentence, check if any of the dictionary roots is a prefix.

```python
for word in sentence.split():
    for root in dictionary:
        if word.startswith(root):
            replace(word, root)
```

If the dictionary is large and the sentence is long, comparing every word against every root becomes very slow ($O(M \cdot N \cdot L)$ where $M$ is words in sentence, $N$ is dictionary size, $L$ is max word length).

**The Key Insight: Trie for Prefix Matching**

A Trie is the perfect data structure for prefix matching. Instead of comparing a word against every root, we can walk down the Trie.

1.  **Build a Trie** containing all the dictionary roots.
2.  For each word in the sentence, **walk the Trie** character by character.
3.  The moment you hit an `is_end` node, you've found the **shortest root**! You can immediately stop and replace the word.
4.  If you fall off the Trie before hitting an `is_end` node, the word has no root in the dictionary. Keep the original word.

**Why Shortest Prefix?**

Because we stop traversal the moment `is_end` is true. If the dictionary has `["ca", "cat"]`, the Trie path is `c -> a(end) -> t(end)`. When searching for `"cattle"`, we hit the end at `"ca"` and stop, ignoring `"cat"`.

---

## Pattern: Trie for Shortest Prefix Replacement

### Core Components

1.  **TrieNode:** Standard node with children and `is_end` flag (or store the `word` itself at the end node).
2.  **Build Phase:** Insert all roots into the Trie.
3.  **Search Phase:** For each word, find the earliest terminal node.

### Visualization

```text
Dictionary: ["cat", "bat", "rat"]

Trie:
      root
     / | \
    c  b  r
    |  |  |
    a  a  a
    |  |  |
   t* t* t*   (* = is_end)

Sentence: "the cattle was rattled by the battery"

Process "the":
  't' not in root.children -> keep "the"

Process "cattle":
  'c' -> 'a' -> 't' (is_end!) -> replace with "cat"

Process "was":
  'w' not in root.children -> keep "was"

Process "rattled":
  'r' -> 'a' -> 't' (is_end!) -> replace with "rat"
```

---

## Implementation

### Standard Trie Solution

We'll use a standard Trie implementation optimized with `__slots__` and Python 3 typings. We store the actual root word at the terminal node to make replacement easy without needing to track the path.

```python
class TrieNode:
    __slots__ = ['children', 'word']

    def __init__(self):
        self.children: dict[str, 'TrieNode'] = {}
        self.word: str | None = None  # Store the root word here if it's the end

class Solution:
    def replaceWords(self, dictionary: list[str], sentence: str) -> str:
        """
        Replace words with shortest dictionary roots using a Trie.

        Time: O(N*L + M*K) where N=len(dictionary), L=avg root len,
                             M=words in sentence, K=avg word len
        Space: O(N*L + M*K) for Trie and resulting string
        """
        # 1. Build the Trie
        root = TrieNode()
        for word in dictionary:
            node = root
            for char in word:
                if char not in node.children:
                    node.children[char] = TrieNode()
                node = node.children[char]
            node.word = word # Mark end and store the root

        # 2. Process the sentence
        def find_root(word: str) -> str:
            node = root
            for char in word:
                # If we hit a dead end, no root exists
                if char not in node.children:
                    break
                node = node.children[char]
                # If we find a root, it's the shortest because we stop early
                if node.word is not None:
                    return node.word
            return word # Return original if no root found

        # 3. Apply to all words
        words = sentence.split()
        return " ".join(find_root(w) for w in words)
```

### HashSet Alternative (When Dictionary is Small/Roots are Short)

If the roots are generally very short, a HashSet approach can be competitive or even faster in practice due to lower overhead, though it has a worse theoretical time bound if words are very long.

```python
class Solution:
    def replaceWords(self, dictionary: list[str], sentence: str) -> str:
        """
        HashSet approach checking prefixes from shortest to longest.
        """
        roots = set(dictionary)
        words = sentence.split()
        result = []

        for word in words:
            found = False
            # Try prefixes from length 1 up to len(word)
            for i in range(1, len(word) + 1):
                prefix = word[:i]
                if prefix in roots:
                    result.append(prefix)
                    found = True
                    break

            if not found:
                result.append(word)

        return " ".join(result)
```

**Tradeoffs:**
- **Trie:** Consistent $O(L)$ lookup per word. Best when words are long and dictionary is large.
- **HashSet:** Creates many substrings (`word[:i]`). Time is $O(L^2)$ per word for string slicing and hashing. Only better when the matching prefix is found very quickly (at indices 1, 2, or 3) or words are extremely short.

---

## Complexity Analysis

| Operation | Best Case | Worst Case | Notes |
| :--- | :--- | :--- | :--- |
| **Trie Build** | `O(N \cdot L)` | `O(N \cdot L)` | `N` roots of average length `L` |
| **Sentence Process** | `O(M)` | `O(M \cdot K)` | `M` words of length `K`. Best case: mismatch at first char. |
| **Total Time** | `O(N \cdot L + M)` | `O(N \cdot L + M \cdot K)` | Very efficient |

### Space Complexity

- **Trie:** `O(N \cdot L)` to store all roots.
- **Sentence Split/Join:** `O(M \cdot K)` to store the words array and output string.
- **Total Space:** `O(N \cdot L + M \cdot K)`.

---

## Edge Cases

1. **Root is a prefix of another root:** e.g., dictionary has `["ca", "cat"]`. The Trie correctly handles this because `is_end` (or `word`) is set at `'a'`. The search stops at `'a'`, finding the shortest prefix `"ca"`.
2. **Word has no matching root:** The search falls off the Trie and returns the original word.
3. **Empty dictionary:** Handled correctly (returns original sentence).
4. **Sentence has leading/trailing/multiple spaces:** `split()` handles arbitrary whitespace, and `" ".join()` normalizes it to single spaces, which is usually the desired behavior.

---

## Practice Problems

| # | Problem | Difficulty | Key Concept |
| :--- | :--- | :--- | :--- |
| 1 | Replace Words | Medium | Find shortest prefix using Trie |
| 2 | Longest Word in Dictionary | Medium | Find longest word built 1 char at a time |
| 3 | Implement Trie (Prefix Tree) | Medium | Core fundamentals |

---

## Related Sections

- [Trie Implementation](./01-trie-implementation.md) - Basic setup
- [Word Dictionary](./02-word-dictionary.md) - Handling wildcards
- [Word Search II](./04-word-search-trie.md) - Trie combined with DFS

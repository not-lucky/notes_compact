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

**Why This Problem Matters**

This is a pure prefix-matching problem — the bread and butter of tries. Unlike wildcard search (LeetCode 211) where you branch at `.`, here you follow exactly one path per character. The trie gives you $O(K)$ lookup per word regardless of dictionary size, compared to checking every root individually.

**The Naive Approach**

For each word in the sentence, check if any of the dictionary roots is a prefix.

```python
for word in sentence.split():
    for root in dictionary:
        if word.startswith(root):
            replace(word, root)
```

If the dictionary is large and the sentence is long, comparing every word against every root becomes very slow ($O(M \cdot N \cdot L)$ where $M$ is words in sentence, $N$ is dictionary size, $L$ is max word length). Worse, this doesn't guarantee we find the *shortest* root first unless we sort the dictionary by length.

**The Key Insight: Trie for Prefix Matching**

A Trie is the perfect data structure for prefix matching. Instead of comparing a word against every root, we can walk down the Trie.

1.  **Build a Trie** containing all the dictionary roots.
2.  For each word in the sentence, **walk the Trie** character by character.
3.  The moment you hit an `is_end` node, you've found the **shortest root**! You can immediately stop and replace the word.
4.  If you fall off the Trie before hitting an `is_end` node, the word has no root in the dictionary. Keep the original word.

**Why Shortest Prefix?**

Because we stop traversal the moment `is_end` is true. If the dictionary has `["ca", "cat"]`, the Trie path is `c -> a(end) -> t(end)`. When searching for `"cattle"`, we hit the end at `"ca"` and stop, ignoring `"cat"`.

**Mental Model: Walking a Decision Tree**

Think of the trie as a funnel. Each character narrows your position until either:
- You hit a terminal node → found the shortest root, stop immediately
- You hit a dead end (character not in children) → no root exists, keep original word
- You exhaust the word → no root exists, keep original word

---

## When NOT to Use This Pattern

**1. Very Small Dictionary with Short Roots**

If the dictionary has only a handful of roots (e.g., 5) and they're short, a HashSet with prefix checking is simpler and has negligible overhead:

```python
# For 5 short roots, this is fine
roots = set(dictionary)
for word in words:
    for i in range(1, len(word) + 1):
        if word[:i] in roots:
            break
```

**2. Suffix Matching Instead of Prefix**

"Replace words that *end with* a root" requires a reversed trie or suffix structure. A standard prefix trie won't help.

**3. Approximate/Fuzzy Matching**

If you need to replace words with the *closest* root (edit distance), a trie alone isn't sufficient — you'd need BK-trees or trie + Levenshtein automata.

**4. Single Query**

If you're doing a one-time lookup of a single word against a dictionary, building a trie is overkill. Use `word.startswith(root)` with sorted roots.

**Red Flags:**
- "Find closest match" → Not exact prefix, needs different structure
- "Match anywhere in word" → Substring, not prefix
- "Dictionary changes frequently" → Trie rebuild cost matters
- Very few roots + short words → HashSet is simpler

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

### Step-by-Step Walkthrough

Let's trace the trie traversal in detail for a more complex dictionary with overlapping roots:

```text
Dictionary: ["a", "ab", "cat", "cattle"]
Sentence: "abstract cattle cab"

Build phase — insert roots into trie:
  Insert "a":       root -> a*
  Insert "ab":      root -> a* -> b*     (note: 'a' is already end)
  Insert "cat":     root -> a* -> b*
                           c -> a -> t*
  Insert "cattle":  root -> a* -> b*
                           c -> a -> t* -> t -> l -> e*

Trie:
      root
     /    \
    a*     c          (* = word stored here)
    |      |
    b*     a
           |
           t*
           |
           t
           |
           l
           |
           e*

--- Search phase ---

find_root("abstract"):
  node = root
  char 'a': 'a' in root.children? YES → move to node_a
            node_a.word = "a" → FOUND! Return "a"
  (We never even look at 'b','s','t','r','a','c','t')
  Result: "a"

find_root("cattle"):
  node = root
  char 'c': 'c' in root.children? YES → move to node_c
            node_c.word = None → continue
  char 'a': 'a' in node_c.children? YES → move to node_ca
            node_ca.word = None → continue
  char 't': 't' in node_ca.children? YES → move to node_cat
            node_cat.word = "cat" → FOUND! Return "cat"
  (We stop at "cat", never reaching "cattle" even though it's also a root)
  Result: "cat"

find_root("cab"):
  node = root
  char 'c': 'c' in root.children? YES → move to node_c
            node_c.word = None → continue
  char 'a': 'a' in node_c.children? YES → move to node_ca
            node_ca.word = None → continue
  char 'b': 'b' in node_ca.children? NO → DEAD END, break
  Result: "cab" (original word, no matching root)

Final output: "a cat cab"
```

**Key observations from the walkthrough:**
1. **Overlapping roots** (`"a"` and `"ab"`): The shortest wins. `"abstract"` becomes `"a"`, not `"ab"`.
2. **Root that is prefix of another root** (`"cat"` and `"cattle"`): When processing `"cattle"`, we find `"cat"` first and stop.
3. **No matching root** (`"cab"`): We walk partway down the trie, hit a dead end, and keep the original.

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
        # 1. Build the Trie from all dictionary roots
        root = TrieNode()
        for word in dictionary:
            node = root
            for char in word:
                if char not in node.children:
                    node.children[char] = TrieNode()
                node = node.children[char]
            # Store the root word at the terminal node.
            # Guard against duplicates (second insert is a no-op).
            if node.word is None:
                node.word = word

        # 2. For each word, walk the trie to find the shortest matching root
        def find_root(word: str) -> str:
            node = root
            for char in word:
                # Dead end: this character doesn't exist in trie
                if char not in node.children:
                    break
                node = node.children[char]
                # Found shortest root — stop immediately
                if node.word is not None:
                    return node.word
            # No root matched; keep the original word
            return word

        # 3. Apply replacement to all words and reconstruct sentence
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

        Time: O(M * K^2) worst case — for each of M words of length K,
              we try K prefixes. Each prefix word[:i] creates a string
              of length i and hashing it is O(i), giving:
              sum(i for i in range(1, K+1)) = O(K^2) per word.
        Space: O(N*L + M*K) for the set and output.
        """
        roots = set(dictionary)
        words = sentence.split()
        result: list[str] = []

        for word in words:
            found = False
            # Try prefixes from length 1 up to len(word)
            for i in range(1, len(word) + 1):
                prefix = word[:i]  # O(i) slice + O(i) hash
                if prefix in roots:
                    result.append(prefix)
                    found = True
                    break

            if not found:
                result.append(word)

        return " ".join(result)
```

**Tradeoffs:**

| | Trie | HashSet |
| :--- | :--- | :--- |
| **Per-word lookup** | $O(K)$ — walk one path, constant work per char | $O(K^2)$ worst case — `word[:i]` costs $O(i)$ to slice + hash |
| **Build time** | $O(N \cdot L)$ — insert all roots | $O(N \cdot L)$ — hash all roots |
| **Space** | $O(N \cdot L)$ — trie nodes (higher constant) | $O(N \cdot L)$ — hash table (lower constant) |
| **Best for** | Large dictionary, long words | Few short roots, quick early matches |
| **Implementation** | More code, but structured | Simpler, fewer lines |

**Why $O(K^2)$ for HashSet?** Creating `word[:i]` allocates a new string of length `i`, and Python's `set.__contains__` hashes it in $O(i)$. Over all `i` from 1 to $K$: $\sum_{i=1}^{K} O(i) = O(K^2)$. In practice, if a root matches at position 3, you stop early and it's effectively $O(1)$.

---

## Complexity Analysis

### Trie Approach

| Operation | Best Case | Worst Case | Notes |
| :--- | :--- | :--- | :--- |
| **Trie Build** | `O(N * L)` | `O(N * L)` | `N` roots of average length `L` |
| **Sentence Process** | `O(M)` | `O(M * K)` | `M` words of length `K`. Best case: mismatch at first char. |
| **Total Time** | `O(N * L + M)` | `O(N * L + M * K)` | Very efficient |

### HashSet Approach

| Operation | Best Case | Worst Case | Notes |
| :--- | :--- | :--- | :--- |
| **Set Build** | `O(N * L)` | `O(N * L)` | Hash each root |
| **Sentence Process** | `O(M)` | `O(M * K^2)` | Per word: `sum(i for i in 1..K)` = `O(K^2)` for slicing + hashing |
| **Total Time** | `O(N * L + M)` | `O(N * L + M * K^2)` | Slower worst case than Trie |

### Space Complexity

- **Trie:** `O(N * L)` to store all roots. Higher constant factor per node (dict overhead).
- **HashSet:** `O(N * L)` to store all roots. Lower constant factor.
- **Sentence Split/Join:** `O(M * K)` to store the words array and output string.
- **Total Space:** `O(N * L + M * K)` for both approaches.

---

## Edge Cases

1. **Overlapping roots (prefix chain):** e.g., dictionary has `["a", "ab", "abc"]`. All three share a prefix path. The trie correctly returns `"a"` for any word starting with `'a'` because we stop at the first terminal node. The longer roots `"ab"` and `"abc"` are never reached.
2. **Root is a prefix of another root:** e.g., dictionary has `["ca", "cat"]`. The Trie correctly handles this because `word` is set at node `'a'`. The search stops at `"ca"`, finding the shortest prefix.
3. **Word has no matching root:** The search falls off the Trie and returns the original word.
4. **Word exactly equals a root:** e.g., word is `"cat"` and `"cat"` is in the dictionary. The search finds `"cat"` at the terminal node and returns it (effectively no replacement visible, but the logic is correct).
5. **Empty dictionary:** Handled correctly (returns original sentence).
6. **Sentence has leading/trailing/multiple spaces:** `split()` handles arbitrary whitespace, and `" ".join()` normalizes it to single spaces, which is usually the desired behavior.
7. **Duplicate roots in dictionary:** Inserting the same root twice is harmless — the second insert overwrites the same terminal node.
8. **Single-character roots:** e.g., `["a"]` replaces every word starting with `'a'`. This is an important edge case because it can aggressively shorten the output.

---

## Common Variations

### 1. Replace with Longest Root Instead of Shortest

Sometimes the problem asks for the **longest** matching prefix. Instead of stopping at the first terminal node, continue walking and track the last terminal node seen.

```python
def find_longest_root(word: str, root: TrieNode) -> str:
    """Find the longest dictionary root that is a prefix of word."""
    node = root
    longest: str | None = None

    for char in word:
        if char not in node.children:
            break
        node = node.children[char]
        # Track the latest terminal node, don't stop early
        if node.word is not None:
            longest = node.word

    return longest if longest is not None else word
```

### 2. Return All Matching Roots

Collect every root that is a prefix, not just the shortest or longest:

```python
def find_all_roots(word: str, root: TrieNode) -> list[str]:
    """Find all dictionary roots that are prefixes of word."""
    node = root
    matches: list[str] = []

    for char in word:
        if char not in node.children:
            break
        node = node.children[char]
        if node.word is not None:
            matches.append(node.word)

    return matches  # e.g., ["a", "ab"] for word "abstract"
```

### 3. Sorting Dictionary for HashSet Correctness

The HashSet approach naturally finds the shortest prefix because it checks lengths 1, 2, 3, ... in order. But if you want the longest, you'd need to check all lengths and track the best — making the trie approach cleaner.

### 4. Stream Processing

If words arrive one at a time (streaming), the trie is already built once. Each word lookup is independent, making this pattern naturally suited to streaming.

---

## Interview Tips

1. **Start with the trie approach** — it's what the interviewer expects for this problem.
2. **Mention the HashSet alternative** to show breadth of knowledge, but explain why the trie is theoretically better ($O(K)$ vs $O(K^2)$ per word).
3. **Storing the word vs. boolean:** Explain why storing the actual root string at the terminal node avoids reconstructing the path.
4. **Edge case to mention proactively:** Overlapping roots like `["a", "ab"]` — the trie handles this naturally because we stop at the first terminal node.
5. **Follow-up question prep:** "What if we want the longest root?" — change the search to not stop early (variation 1 above).

---

## Practice Problems

| # | Problem | Difficulty | Key Concept |
| :--- | :--- | :--- | :--- |
| 1 | [Replace Words](https://leetcode.com/problems/replace-words/) (LC 648) | Medium | Find shortest prefix using Trie |
| 2 | [Implement Trie (Prefix Tree)](https://leetcode.com/problems/implement-trie-prefix-tree/) (LC 208) | Medium | Core trie fundamentals — prerequisite |
| 3 | [Longest Word in Dictionary](https://leetcode.com/problems/longest-word-in-dictionary/) (LC 720) | Medium | Find longest word built one char at a time |
| 4 | [Map Sum Pairs](https://leetcode.com/problems/map-sum-pairs/) (LC 677) | Medium | Trie with prefix sums — related prefix pattern |
| 5 | [Design Search Autocomplete System](https://leetcode.com/problems/design-search-autocomplete-system/) (LC 642) | Hard | Trie prefix matching with ranking |
| 6 | [Add and Search Word](https://leetcode.com/problems/design-add-and-search-words-data-structure/) (LC 211) | Medium | Prefix trie + wildcard (next step) |
| 7 | [Word Search II](https://leetcode.com/problems/word-search-ii/) (LC 212) | Hard | Trie + DFS on grid |

---

## Related Sections

- [Trie Implementation](./01-trie-implementation.md) - Basic setup
- [Word Dictionary](./02-word-dictionary.md) - Handling wildcards
- [Word Search II](./04-word-search-trie.md) - Trie combined with DFS

# Word Dictionary (Search with Wildcards)

[Previous: Trie Implementation](./01-trie-implementation.md) | [Next: Replace Words](./03-replace-words.md)

> **Prerequisites:** [Trie Implementation](./01-trie-implementation.md), [Backtracking](../11-recursion-backtracking/README.md)

## Quick Reference

| Operation | Complexity | Explanation |
| :--- | :--- | :--- |
| **`addWord(word)`** | `O(L)` | Insert a word of length `L` into the Trie normally. |
| **`search(word)` (No wildcards)** | `O(L)` | Navigate the Trie following exact character matches. |
| **`search(word)` (With `k` wildcards)** | `O(26^k)` | At each of `k` wildcard positions, branch up to 26 paths. Non-wildcard chars follow single paths (no extra factor). |
| **`search(word)` (All wildcards)** | `O(26^L)` | Every position branches — explores entire trie. |
| **Space Complexity** | `O(N \cdot L)` | Where `N` is the number of words, each of length `L`. Storage for all characters. |

## Interview Context

"Add and Search Word" (LeetCode 211) tests your ability to extend the basic trie with wildcard matching. The '.' character can match any letter, requiring DFS exploration at wildcard positions. This problem is popular at Meta and Amazon.

---

## Building Intuition

**Why Wildcards Break the Trie's Speed Guarantee**

Normal trie operations are $O(L)$ because you follow ONE path. The branching factor is essentially 1 per step.

```text
search("cat"): root → c → a → t → done (3 steps, always)
```

But with wildcards, a single `.` branches into up to 26 paths:

```text
search(".at"): root → a? b? c? ... z? (try ALL 26)
                       ↓
               each leads to 'a'? check...
                       ↓
               each leads to 't'? check...
```

**The Key Insight: DFS at Wildcard Positions**

For regular characters, follow the path. For `.`, explore ALL children. Because a wildcard can match any valid transition, we must recursively search *every* branch extending from the current node. This introduces backtracking into an otherwise linear traversal.

```python
def search(node: TrieNode, word: str, i: int) -> bool:
    if i == len(word):
        return node.is_end

    char = word[i]

    if char == '.':
        # Must try ALL children. This requires branching, increasing time complexity
        for child in node.children.values():
            if search(child, word, i + 1):
                return True  # Found via some path
        return False
    else:
        # Normal trie traversal - single path
        if char not in node.children:
            return False
        return search(node.children[char], word, i + 1)
```

**Worst Case: All Wildcards**

If the tree is completely dense (a full 26-ary tree) and the query is entirely wildcards, the search space grows exponentially:

```text
search("....."):  # 5 wildcards
Level 0: 26 branches
Level 1: 26 × 26 = 676 branches
Level 2: 26³ = 17,576 branches
Level 3: 26⁴ = 456,976 branches
Level 4: 26⁵ = 11,881,376 branches

This is O(26^L) — exponential!
```

But in practice, tries are sparse. If only 1,000 5-letter words exist, you can't possibly explore 11 million paths—most branches are dead ends. The trie prunes invalid wildcard paths immediately.

**Why It's Still Better Than Brute Force**

```text
Brute force with n words and wildcards:
  For each of n words: check if pattern matches → O(n × L)

Trie with wildcards:
  Traverse trie, branching at wildcards → O(26^k) worst case
  where k = number of wildcards

If n = 100,000 and k = 2:
  Brute force: 100,000 operations (assuming length is a small constant)
  Trie:        26² = 676 operations

Trie wins when n >> 26^k (many words, few wildcards).
```

**Mental Model: Wildcards as "Parallel Universes"**

Think of each `.` as spawning parallel searches:

```text
Pattern: "b.d"

Universe 1: b-a-d  → explore
Universe 2: b-b-d  → explore
...
Universe 26: b-z-d → explore

If ANY universe finds a match, return True.
```

---

## When NOT to Use This Pattern

**1. All Wildcards or Wildcards at Start**

If the pattern is `"....."` or `".....xyz"`, you're essentially scanning the entire trie. A hashset with linear scan might be simpler:

```python
# Simpler for "....." (any 5-letter word)
any(len(word) == 5 for word in words)
```

**2. Wildcard Matching Multiple Characters**

This pattern handles `.` (single char). For `*` (zero or more), you need different logic:

```text
"b*d" should match: "bd", "bad", "bread"
This requires regex-like NFA simulation, not simple trie DFS.
```

**3. When Dictionary is Small**

For 100 words, regex matching on a list is simpler:

```python
import re
pattern = re.compile("^b.d$")
any(pattern.match(word) for word in words)
```

Trie setup overhead isn't justified.

**4. Substring Wildcards (Not Prefix)**

"Find words containing pattern `'a.c'` anywhere" requires suffix tree or inverted index, not prefix trie.

**Red Flags:**

- Pattern length unrestricted → Could be exponential
- "Match anywhere in string" → Not a prefix problem
- "Match zero or more" → Needs regex/NFA
- Very short dictionary → Linear scan is fine

---

## Problem Statement

Design a data structure that supports:

- `addWord(word)` - Adds a word to the structure
- `search(word)` - Returns true if word is in the structure; `.` matches any letter

```python
wd = WordDictionary()
wd.addWord("bad")
wd.addWord("dad")
wd.addWord("mad")
wd.search("pad")   # False
wd.search("bad")   # True
wd.search(".ad")   # True  (matches "bad", "dad", "mad")
wd.search("b..")   # True  (matches "bad")
```

---

## Pattern: Trie + DFS for Wildcards

### Key Insight

- For regular characters: follow the trie path normally
- For `.`: try ALL children (DFS branching)
- Match if ANY branch leads to a valid word

### Visualization

```text
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
    __slots__ = ('children', 'is_end')

    def __init__(self):
        self.children: dict[str, 'TrieNode'] = {}
        self.is_end: bool = False

class WordDictionary:
    """
    Word dictionary supporting '.' wildcard searches.

    Time:
    - addWord: O(L) where L = word length
    - search: O(26^k) worst case where k = number of wildcards
      (non-wildcard chars follow single paths, wildcards branch up to 26)

    Space: O(N * L) for trie storage, O(L) for recursion stack
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
        self.root: dict = {}

    def addWord(self, word: str) -> None:
        node = self.root
        for char in word:
            if char not in node:
                node[char] = {}
            node = node[char]
        node['$'] = True  # End marker

    def search(self, word: str) -> bool:
        # Stack: (node, index)
        stack: list[tuple[dict, int]] = [(self.root, 0)]

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
        self.root: dict = {}
        self.word_lengths: set[int] = set()  # Track valid lengths

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

    def _search(self, node: dict, word: str, i: int) -> bool:
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

| Operation              | Best Case | Worst Case  | Notes                |
| :--------------------- | :-------- | :---------- | :------------------- |
| **`addWord`**          | `O(L)`    | `O(L)`      | `L` = word length      |
| **`search` (no wildcard)** | `O(L)`    | `O(L)`      | Standard trie search |
| **`search` (`k` wildcards)** | `O(L)`    | `O(26^k)`  | Branch up to 26 paths at each `.`; non-wildcard chars are single-path (no extra `× L` factor) |
| **`search` (all wildcards)** | `O(26^L)` | `O(26^L)`   | Explores entire trie |

### Space Complexity

- **Trie storage**: `O(N \cdot L)` worst case (if no words share prefixes)
- **Recursion stack**: `O(L)` where `L` is the length of the word being searched

---

## Common Variations

### Multiple Wildcards with '\*'

Handle '\*' matching zero or more characters:

```python
def search_with_star(self, word: str) -> bool:
    """
    '*' matches zero or more characters.
    Example: "b*d" matches "bd", "bad", "bread"
    """
    def dfs(node: TrieNode, i: int) -> bool:
        if i == len(word):
            return node.is_end

        char = word[i]

        if char == '*':
            # Option 1: Match zero characters (skip '*')
            if dfs(node, i + 1):
                return True
            # Option 2: Match one+ characters (consume a child, stay at '*')
            # Terminates because the trie is finite and acyclic — each
            # recursive call moves deeper in the trie even though i stays.
            for child in node.children.values():
                if dfs(child, i):
                    return True
            return False
        elif char == '.':
            # Single-char wildcard: try all children
            for child in node.children.values():
                if dfs(child, i + 1):
                    return True
            return False
        else:
            # Exact character match
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

    ⚠️ Exercise: Implement using NFA simulation or DP.
    This requires converting the regex pattern into states and
    simulating transitions — beyond simple trie DFS.
    """
    raise NotImplementedError("Exercise: use NFA simulation or DP")
```

### Magic Dictionary (LeetCode 676)

Find if any word differs by exactly one character:

```python
class MagicDictionary:
    """
    Search returns true if modifying exactly one character
    would make it match a dictionary word.

    Time: O(26 * L) per search — at each position, try all 26 branches
    Space: O(N * L) for trie storage
    """

    def __init__(self):
        self.root: dict = {}

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

    def _search(self, node: dict, word: str, i: int, modified: bool) -> bool:
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

    Trick: For each word, insert all rotations "suffix#word" into the trie.
    Query: Search for "suffix#prefix" as a prefix in the trie.

    Time: O(L^2) per word insertion, O(L) per query
    Space: O(N * L^2) for all rotations
    """

    def __init__(self, words: list[str]):
        self.root: dict = {}

        for weight, word in enumerate(words):
            # Insert all suffix rotations: word[i:]#word for each i
            for i in range(len(word) + 1):
                key = word[i:] + '#' + word
                node = self.root
                for char in key:
                    if char not in node:
                        node[char] = {}
                    node = node[char]
                    node['weight'] = weight  # Latest weight at each prefix node

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
5. **Follow-up questions**: What if pattern has '\*' for multi-char match?

---

## Step-by-Step Walkthrough

```text
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

| Pattern | Time Complexity | Example             |
| :------ | :-------------- | :------------------ |
| `"hello"` | `O(L)`          | Exact match — single path |
| `".ello"` | `O(26)`         | 1 wildcard — branch once, then follow single paths |
| `"h.llo"` | `O(26)`         | 1 wildcard in middle — same branching cost |
| `".e.l."` | `O(26^3)`       | 3 wildcards — branch at each `.` position |
| `"....."` | `O(26^L)`       | All wildcards — explores entire trie |

---

## Practice Problems

### Warm-Up (Easy)

| # | Problem | Key Concept |
| :--- | :--- | :--- |
| 1 | [Longest Common Prefix (LC 14)](https://leetcode.com/problems/longest-common-prefix/) | Basic trie traversal — follow shared path until branching |
| 2 | [Implement Trie (LC 208)](https://leetcode.com/problems/implement-trie-prefix-tree/) | Foundation: insert, search, startsWith before adding wildcards |

### Core (Medium)

| # | Problem | Key Concept |
| :--- | :--- | :--- |
| 3 | [Add and Search Word (LC 211)](https://leetcode.com/problems/design-add-and-search-words-data-structure/) | **This problem** — wildcard trie search with DFS |
| 4 | [Implement Magic Dictionary (LC 676)](https://leetcode.com/problems/implement-magic-dictionary/) | Single char modification — controlled branching |
| 5 | [Camelcase Matching (LC 1023)](https://leetcode.com/problems/camelcase-matching/) | Pattern matching variant with uppercase constraints |
| 6 | [Map Sum Pairs (LC 677)](https://leetcode.com/problems/map-sum-pairs/) | Trie with values — DFS aggregation at wildcard-like prefix |

### Advanced (Hard)

| # | Problem | Key Concept |
| :--- | :--- | :--- |
| 7 | [Prefix and Suffix Search (LC 745)](https://leetcode.com/problems/prefix-and-suffix-search/) | Combined prefix/suffix trie with suffix rotation trick |
| 8 | [Word Search II (LC 212)](https://leetcode.com/problems/word-search-ii/) | Trie + backtracking on 2D grid |
| 9 | [Concatenated Words (LC 472)](https://leetcode.com/problems/concatenated-words/) | DFS + Trie — check if word is composed of other words |
| 10 | [Stream of Characters (LC 1032)](https://leetcode.com/problems/stream-of-characters/) | Reverse trie — match suffix of stream against dictionary |

---

## Related Sections

- [Trie Implementation](./01-trie-implementation.md) - Basic trie operations
- [Replace Words](./03-replace-words.md) - Shortest prefix match
- [Word Search II](./04-word-search-trie.md) - Trie combined with DFS
- [Backtracking](../11-recursion-backtracking/README.md) - DFS patterns
- [Regular Expressions](../16-math-basics/README.md) - For regex matching context

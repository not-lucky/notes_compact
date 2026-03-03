# Concatenated Words

[Previous: Autocomplete](./06-autocomplete.md) | [Next: Maximum XOR](./08-maximum-xor.md)

> **Prerequisites:** [Trie Implementation](./01-trie-implementation.md), [Dynamic Programming](../14-dynamic-programming/README.md)

## Interview Context

Concatenated Words ([LeetCode 472](https://leetcode.com/problems/concatenated-words/)) is a hard-level problem that tests your ability to combine tries (or hash sets) with DFS/DP for word decomposition. It's a favorite at Amazon, Google, and Meta because it layers multiple algorithmic concepts: sorting strategy, trie-based prefix matching, and recursive backtracking with memoization.

---

## Quick Reference

| Aspect | Details |
| :--- | :--- |
| **Pattern** | Trie + DFS (or HashSet + DFS/DP) |
| **Key Insight** | Sort by length so all component words are in the dictionary before we check longer words. |
| **Time Complexity** | $O(N \log N + N \cdot L^2)$ — $N$ words, $L$ max word length. Without memoization, worst case is $O(N \cdot 2^L)$. |
| **Space Complexity** | $O(N \cdot L)$ for the Trie + $O(L)$ recursion/memo. |
| **When to Use** | Word decomposition with a dynamic dictionary; need prefix matching for early termination. |

---

## Problem Statement

Given an array of strings `words` (without duplicates), return all **concatenated words**. A concatenated word is a string that is comprised entirely of **at least two shorter words** also in the array.

```
Input:  ["cat","cats","catsdogcats","dog","dogcatsdog","hippopotamuses","rat","ratcatdogcat"]
Output: ["catsdogcats","dogcatsdog","ratcatdogcat"]

Explanation:
  "catsdogcats" = "cats" + "dog" + "cats"
  "dogcatsdog"  = "dog" + "cats" + "dog"
  "ratcatdogcat" = "rat" + "cat" + "dog" + "cat"
```

---

## Building Intuition

### Why Sort by Length?

A concatenated word is made of **shorter** words. If we process words from shortest to longest, every potential component word is already in our dictionary when we check a longer word.

**Without sorting:** You'd need to first build the entire dictionary, then check every word — but then you'd wrongly count a word as "concatenating with itself." Sorting avoids this naturally: when we check word `W`, only words strictly shorter than `W` are in the trie.

```
words = ["cat", "cats", "catsdogcats", "dog"]

Sorted by length: ["cat", "dog", "cats", "catsdogcats"]

Processing order:
  "cat"          → Nothing in trie yet → INSERT into trie
  "dog"          → Can't form from ["cat"] → INSERT into trie
  "cats"         → "cat" is a prefix & in trie, but "s" alone is NOT
                    → Can't form → INSERT into trie
  "catsdogcats"  → "cat" ✓ + "s" ✗ ... backtrack
                    "cats" ✓ + "dog" ✓ + "cats" ✓ → CONCATENATED ✓
```

### What Happens Without Sorting?

If we insert all words first, then for the word `"cat"` we'd need extra logic to ensure it doesn't match itself as a "concatenation of one word." Sorting elegantly sidesteps this: shorter words are always inserted before longer ones, and a word can only be formed from **strictly shorter** words already present.

### The DFS Strategy

For each word, we walk the trie character by character. Whenever we land on a node marked `is_word`, we have two choices:
1. **Split here:** Recursively check if the remainder of the word can also be formed.
2. **Continue:** Keep walking the trie with the next character (maybe a longer prefix is also a word).

This branching is exactly DFS/backtracking.

```
Checking "catsdogcats":

  c → a → t (is_word! "cat")
       ├── Split here: check "sdogcats" → s not in trie → FAIL
       └── Continue: t → s (is_word! "cats")
            └── Split here: check "dogcats"
                 d → o → g (is_word! "dog")
                      └── Split here: check "cats"
                           c → a → t → s (is_word! "cats")
                                └── Split here: check "" → reached end → SUCCESS ✓
```

---

## Visualization: Incremental Trie Building

```
Step 1: Insert "cat"          Step 2: Insert "dog"

      root                          root
       |                           /    \
       c                          c      d
       |                          |      |
       a                          a      o
       |                          |      |
      t*                         t*     g*

Step 3: Insert "cats"         Step 4: Check "catsdogcats"

      root                    DFS traversal on the trie:
     /    \
    c      d                  "catsdogcats"
    |      |                   ^^^         → "cat"* found, split
    a      o                       ^^^^    → "sdog" — 's' fails, backtrack
    |      |                   ^^^^        → "cats"* found, split
   t*     g*                        ^^^    → "dog"* found, split
    |                                  ^^^^ → "cats"* found, split
   s*                                      → "" end reached → SUCCESS!

(* = is_word)
```

---

## Step-by-Step Walkthrough

**Input:** `words = ["cat", "cats", "catsdogcats", "dog", "dogcatsdog", "hippopotamuses", "rat", "ratcatdogcat"]`

**Step 1 — Sort by length:**

```
["cat", "dog", "rat", "cats", "dogcatsdog", "catsdogcats", "ratcatdogcat", "hippopotamuses"]
 (3)    (3)    (3)    (4)    (10)          (11)           (12)             (14)
```

**Step 2 — Process each word:**

| Word | Action | Reason |
| :--- | :--- | :--- |
| `"cat"` | INSERT | Trie empty, can't form |
| `"dog"` | INSERT | No match in trie |
| `"rat"` | INSERT | No match in trie |
| `"cats"` | INSERT | "cat" + "s" fails ("s" not in trie) |
| `"dogcatsdog"` | **RESULT** | "dog" + "cats" + "dog" ✓ |
| `"catsdogcats"` | **RESULT** | "cats" + "dog" + "cats" ✓ |
| `"ratcatdogcat"` | **RESULT** | "rat" + "cat" + "dog" + "cat" ✓ |
| `"hippopotamuses"` | INSERT | No valid decomposition |

**Output:** `["dogcatsdog", "catsdogcats", "ratcatdogcat"]`

---

## Implementation

### Trie + DFS (Primary Approach)

```python
class TrieNode:
    __slots__ = ['children', 'is_word']

    def __init__(self) -> None:
        self.children: dict[str, 'TrieNode'] = {}
        self.is_word: bool = False


class Trie:
    __slots__ = ['root']

    def __init__(self) -> None:
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_word = True


class Solution:
    def findAllConcatenatedWordsInADict(self, words: list[str]) -> list[str]:
        # Sort by length: ensures all component words are inserted before
        # any word that could be formed from them
        words.sort(key=len)
        trie = Trie()
        result: list[str] = []

        for word in words:
            # Empty strings cannot be concatenated words
            if not word:
                continue

            # Check if word can be formed by 2+ words already in the trie
            if self._can_form(word, 0, trie.root):
                result.append(word)
            else:
                # Insert as a building block for future words
                trie.insert(word)

        return result

    def _can_form(self, word: str, start: int, root: TrieNode) -> bool:
        """
        DFS: check if word[start:] can be formed by concatenating
        one or more words in the trie.
        """
        # Reached end of word — all parts matched successfully
        if start == len(word):
            return True

        node = root
        for i in range(start, len(word)):
            char = word[i]

            # Current prefix doesn't exist in trie — prune this branch
            if char not in node.children:
                return False

            node = node.children[char]

            # Found a valid word ending at position i — try splitting here
            if node.is_word:
                if self._can_form(word, i + 1, root):
                    return True

        # No valid decomposition found from this starting position
        return False
```

### With Memoization (Handles Pathological Cases)

The basic `_can_form` above can have exponential time on adversarial inputs. Consider:

```
words = ["a", "aa", "aaa", ..., "a" * 30]
Checking "a" * 30:
  - "a" matches at index 0 → recurse on "a" * 29
  - "aa" matches at index 1 → recurse on "a" * 28
  - Both branches overlap massively → exponential blowup
```

Without memoization, time is $O(2^L)$ in the worst case because at each of the $L$ positions we may branch. Adding memoization on the `start` index reduces this to $O(L^2)$:

```python
class Solution:
    def findAllConcatenatedWordsInADict(self, words: list[str]) -> list[str]:
        words.sort(key=len)
        trie = Trie()
        result: list[str] = []

        for word in words:
            if not word:
                continue
            # Use a memo set to avoid re-checking the same start index
            if self._can_form_memo(word, 0, trie.root, set()):
                result.append(word)
            else:
                trie.insert(word)

        return result

    def _can_form_memo(
        self, word: str, start: int, root: TrieNode, failed: set[int]
    ) -> bool:
        """DFS with memoization on failed start positions."""
        if start == len(word):
            return True

        # If we already know this start position leads to failure, skip
        if start in failed:
            return False

        node = root
        for i in range(start, len(word)):
            char = word[i]

            if char not in node.children:
                break

            node = node.children[char]

            if node.is_word:
                if self._can_form_memo(word, i + 1, root, failed):
                    return True

        # Mark this start position as a dead end
        failed.add(start)
        return False
```

**Why memoize on `start`?** The recursive call `_can_form(word, start, root)` always uses the same `word` and `root` — the only varying parameter is `start`. If we've already proven that `word[start:]` cannot be decomposed, we never need to try again.

---

## Common Variations

### HashSet + DFS (Simpler, Often Sufficient)

When prefix-based pruning isn't critical, a HashSet is simpler to implement and often fast enough:

```python
class Solution:
    def findAllConcatenatedWordsInADict(self, words: list[str]) -> list[str]:
        word_set: set[str] = set(words)
        result: list[str] = []
        memo: dict[str, bool] = {}

        def can_form(word: str) -> bool:
            if word in memo:
                return memo[word]

            # Try every possible first-word split
            for i in range(1, len(word)):
                prefix = word[:i]
                suffix = word[i:]

                if prefix in word_set:
                    # suffix is itself a known word, OR suffix can be decomposed
                    if suffix in word_set or can_form(suffix):
                        memo[word] = True
                        return True

            memo[word] = False
            return False

        for word in words:
            if can_form(word):
                result.append(word)

        return result
```

**Trade-offs:**

| Aspect | Trie + DFS | HashSet + DFS |
| :--- | :--- | :--- |
| **Prefix Pruning** | Yes — aborts early if prefix doesn't exist in trie | No — must create substrings to check |
| **Substring Creation** | None — walks trie in-place | $O(L)$ per split (`word[:i]`, `word[i:]`) |
| **Code Complexity** | Higher (trie boilerplate) | Lower (just a set) |
| **Best For** | Large dictionaries, long words | Interviews where simplicity matters |

### DP Alternative (Word Break Variant)

This is essentially [Word Break (LeetCode 139)](https://leetcode.com/problems/word-break/) applied to each word, with the constraint of requiring 2+ parts:

```python
class Solution:
    def findAllConcatenatedWordsInADict(self, words: list[str]) -> list[str]:
        word_set: set[str] = set(words)
        result: list[str] = []

        def is_concatenated(word: str) -> bool:
            n = len(word)
            # dp[i] = True if word[:i] can be formed by words in word_set
            dp: list[bool] = [False] * (n + 1)
            dp[0] = True

            for i in range(1, n + 1):
                for j in range(i):
                    # Don't allow using the entire word as a single piece
                    if j == 0 and i == n:
                        continue
                    if dp[j] and word[j:i] in word_set:
                        dp[i] = True
                        break

            return dp[n]

        for word in words:
            if word and is_concatenated(word):
                result.append(word)

        return result
```

**When to prefer DP:** When the problem is a straightforward "can this string be segmented?" check and you want bottom-up clarity. The DP approach is $O(L^2)$ per word with no risk of stack overflow.

---

## Complexity Analysis

### Time Complexity

- **Sorting:** $O(N \log N)$ where $N$ is the number of words.
- **Per-word DFS (without memo):** $O(2^L)$ worst case — at each character position where a word ends, we branch. For a word like `"aaa...a"` (length $L$) with `"a"` in the dictionary, there are $L-1$ possible split points, leading to $2^{L-1}$ paths.
- **Per-word DFS (with memo):** $O(L^2)$ — we try at most $L$ start positions, and for each we scan at most $L$ characters in the trie.
- **Total (with memo):** $O(N \log N + N \cdot L^2)$.

### Space Complexity

- **Trie storage:** $O(N \cdot L)$ in the worst case (no shared prefixes).
- **Recursion stack:** $O(L)$ depth (one frame per split).
- **Memoization set:** $O(L)$ per word (reset between words).
- **Total:** $O(N \cdot L)$.

### HashSet vs Trie Complexity

| Approach | Time per Word | Substring Cost | Early Termination |
| :--- | :--- | :--- | :--- |
| **Trie + DFS (memo)** | $O(L^2)$ | None (walk in-place) | Yes (prefix not in trie) |
| **HashSet + DFS (memo)** | $O(L^2)$ | $O(L)$ per split (slicing) | No |
| **DP** | $O(L^2)$ | $O(L)$ per split (slicing) | No |

In practice, the trie approach wins on long words with large dictionaries because it prunes branches the moment a prefix doesn't exist.

---

## When NOT to Use This Pattern

### Use HashSet + DFS Instead When:

- **Dictionary is small** and words are short — trie overhead isn't justified.
- **You need to code quickly** in an interview — HashSet is fewer lines and less error-prone.
- **No prefix-pruning benefit** — if most prefixes exist in the dictionary, the trie doesn't help prune.

### Use DP Instead When:

- **Word Break variant** — if the problem is "can this single string be segmented?" (LeetCode 139/140), DP is the standard approach.
- **Need bottom-up clarity** — DP avoids recursion depth issues and is easier to reason about.
- **No dynamic dictionary** — if all words are known upfront and you're checking one string, DP is simpler.

### Red Flags (Problem is NOT Concatenated Words):

- "Find all words that can be formed from characters" → Backtracking / frequency counting.
- "Find longest word built one character at a time" → Different trie problem (LeetCode 720).
- "Word break with spaces" → DP (LeetCode 139/140), not concatenated words.

---

## Edge Cases

1. **Empty strings in input:** Skip them — empty string is not a valid concatenated word.
2. **Single-character words:** `"a"` can't be concatenated (need 2+ parts), but it can be a component.
3. **All words are the same length:** No word can be concatenated from others (all components must be *shorter*).
4. **Word is a repeat:** `"aa"` with `["a", "aa"]` — `"aa"` = `"a"` + `"a"` ✓.
5. **Very long words with short components:** `"aaa...a"` (length 1000) with `"a"` in dict — memoization is critical here.
6. **No concatenated words exist:** Return empty list.
7. **Duplicate words in input:** Problem states no duplicates, but defensive code should handle it.

---

## Interview Tips

1. **Start with the sorting insight.** Explain why processing shortest-first lets you build the dictionary incrementally. This shows you understand the problem structure.
2. **Clarify "at least two."** A word matching itself in the dictionary does NOT count — it must be composed of 2+ *shorter* words.
3. **Mention memoization proactively.** Even if the interviewer doesn't ask, point out the exponential worst case and how memoization fixes it. This demonstrates depth.
4. **Know the HashSet alternative.** If the interviewer says "do it without a trie," pivot to HashSet + DFS immediately.
5. **Walk through an example.** Use `"catsdogcats"` to show exactly how the DFS branches and backtracks.
6. **Discuss trade-offs.** Trie gives prefix pruning; HashSet is simpler. DP avoids recursion. Know when each is better.

---

## Practice Problems

| # | Problem | Difficulty | Key Concept |
| :--- | :--- | :--- | :--- |
| 1 | [Concatenated Words (LC 472)](https://leetcode.com/problems/concatenated-words/) | Hard | Trie/HashSet + DFS, sort by length |
| 2 | [Word Break (LC 139)](https://leetcode.com/problems/word-break/) | Medium | DP / DFS+memo for single string segmentation |
| 3 | [Word Break II (LC 140)](https://leetcode.com/problems/word-break-ii/) | Hard | Backtracking all valid segmentations |
| 4 | [Longest Word in Dictionary (LC 720)](https://leetcode.com/problems/longest-word-in-dictionary/) | Medium | Build word one char at a time |
| 5 | [Extra Characters in a String (LC 2707)](https://leetcode.com/problems/extra-characters-in-a-string/) | Medium | DP + set/trie for minimal leftover chars |
| 6 | [Word Search II (LC 212)](https://leetcode.com/problems/word-search-ii/) | Hard | Trie + DFS on 2D grid |

---

## Related Sections

- [Trie Implementation](./01-trie-implementation.md) — Core trie operations used here
- [Word Dictionary](./02-word-dictionary.md) — Trie search with wildcards
- [Replace Words](./03-replace-words.md) — Trie for shortest prefix matching
- [Word Search II](./04-word-search-trie.md) — Trie + DFS on grids
- [Dynamic Programming](../14-dynamic-programming/README.md) — DP alternative (Word Break)

---

[Previous: Autocomplete](./06-autocomplete.md) | [Next: Maximum XOR](./08-maximum-xor.md)

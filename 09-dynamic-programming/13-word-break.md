# Word Break

> **Prerequisites:** [03-1d-dp-basics](./03-1d-dp-basics.md)

## Overview

Word Break determines if a string can be segmented into a sequence of dictionary words.

## Building Intuition

**Why does Word Break need DP?**

1. **Overlapping Subproblems**: To check if "leetcode" can be segmented, we might try "l" + "eetcode" or "le" + "etcode" or "lee" + "tcode" or "leet" + "code". The check for "code" might repeat across different attempts.

2. **Greedy Fails**: Consider s = "catsanddog", dict = ["cat", "cats", "and", "sand", "dog"]. Greedy matching "cats" first leads to "anddog" (fails). But "cat" + "sand" + "dog" works.

3. **The DP State**: dp[i] = "can s[0..i-1] be segmented?" We check all possible last words: if s[j..i-1] is in dictionary AND dp[j] is true, then dp[i] is true.

4. **Optimization Insight**: We only need to check substrings of length ≤ max word length in dictionary. This can significantly prune the inner loop.

5. **Boolean vs Counting vs Enumeration**:
   - Word Break I: Boolean (can segment?)
   - Counting: How many ways? (change OR to +=)
   - Word Break II: Enumerate all (backtracking with memoization)

6. **Mental Model**: Imagine reading a string character by character. At each position, you ask: "Can everything before this be segmented, AND does a dictionary word end right here?" If yes at the final position, the whole string is segmentable.

## Interview Context

Word Break is a FANG+ favorite because:

1. **String + DP combination**: Tests multiple skills
2. **Dictionary lookups**: Set/trie usage
3. **Multiple variants**: Boolean, count, reconstruct
4. **Backtracking extension**: Word Break II

---

## When NOT to Use Word Break DP

1. **Dictionary Has Fixed Small Words**: If all dictionary words are short (max length k), use Trie for O(n×k) instead of O(n²).

2. **Single Dictionary Word Check**: To check if s is exactly one dictionary word, just use set lookup. DP is overkill.

3. **Overlapping Words Not Needed**: If words must partition without reuse (each character used exactly once), standard Word Break applies. But if constraints differ, adapt accordingly.

4. **Very Long String, Large Dictionary**: O(n² × hash) can be slow. Consider Aho-Corasick for O(n + m) where m is total dictionary length.

5. **Need All Segmentations (Word Break II)**: DP gives boolean. For enumeration, use memoized backtracking, but beware exponential output.

**Recognize Word Break Pattern When:**

- Segment string into dictionary words
- Boolean feasibility or count ways
- String matching with multiple valid splits

---

## Problem Statement

Given a string s and dictionary wordDict, return true if s can be segmented into dictionary words.

```
Input: s = "leetcode", wordDict = ["leet", "code"]
Output: true
Explanation: "leetcode" = "leet" + "code"
```

---

## Word Break I: Can Segment?

```python
def word_break(s: str, wordDict: list[str]) -> bool:
    """
    Can s be segmented into dictionary words?

    State: dp[i] = True if s[0..i-1] can be segmented
    Recurrence: dp[i] = any(dp[j] and s[j:i] in dict)

    Time: O(n² × k) where k = average word length for hashing
    Space: O(n)
    """
    word_set = set(wordDict)
    n = len(s)
    dp = [False] * (n + 1)
    dp[0] = True  # Empty string

    for i in range(1, n + 1):
        for j in range(i):
            if dp[j] and s[j:i] in word_set:
                dp[i] = True
                break

    return dp[n]
```

### Optimized: Limit by Word Lengths

```python
def word_break_optimized(s: str, wordDict: list[str]) -> bool:
    """
    Optimize by only checking valid word lengths.

    Time: O(n × m × k) where m = max word length
    Space: O(n)
    """
    word_set = set(wordDict)
    max_len = max(len(w) for w in wordDict) if wordDict else 0

    n = len(s)
    dp = [False] * (n + 1)
    dp[0] = True

    for i in range(1, n + 1):
        # Only check word lengths up to max_len
        for j in range(max(0, i - max_len), i):
            if dp[j] and s[j:i] in word_set:
                dp[i] = True
                break

    return dp[n]
```

---

## Word Break II: All Segmentations

```python
def word_break_ii(s: str, wordDict: list[str]) -> list[str]:
    """
    Return all valid segmentations.

    Time: O(2^n) worst case
    Space: O(n × number of sentences)
    """
    word_set = set(wordDict)
    memo = {}

    def backtrack(start: int) -> list[list[str]]:
        if start in memo:
            return memo[start]

        if start == len(s):
            return [[]]

        result = []
        for end in range(start + 1, len(s) + 1):
            word = s[start:end]
            if word in word_set:
                for rest in backtrack(end):
                    result.append([word] + rest)

        memo[start] = result
        return result

    sentences = backtrack(0)
    return [' '.join(words) for words in sentences]
```

---

## Visual Walkthrough

```
s = "leetcode", wordDict = ["leet", "code"]

dp[0] = True (empty string)

i=1: "l" not in dict → dp[1] = False
i=2: "le" not in dict → dp[2] = False
i=3: "lee" not in dict → dp[3] = False
i=4: "leet" in dict, dp[0]=True → dp[4] = True ✓
i=5: "leetc", "eetc", "etc", "tc", "c" none work → dp[5] = False
i=6: none work → dp[6] = False
i=7: none work → dp[7] = False
i=8: s[4:8]="code" in dict, dp[4]=True → dp[8] = True ✓

Answer: True
```

---

## Trie Optimization

```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_word = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str):
        node = self.root
        for c in word:
            if c not in node.children:
                node.children[c] = TrieNode()
            node = node.children[c]
        node.is_word = True

def word_break_trie(s: str, wordDict: list[str]) -> bool:
    """
    Using Trie for efficient prefix matching.

    Time: O(n² + sum of word lengths)
    Space: O(sum of word lengths + n)
    """
    trie = Trie()
    for word in wordDict:
        trie.insert(word)

    n = len(s)
    dp = [False] * (n + 1)
    dp[0] = True

    for i in range(n):
        if not dp[i]:
            continue

        node = trie.root
        for j in range(i, n):
            if s[j] not in node.children:
                break
            node = node.children[s[j]]
            if node.is_word:
                dp[j + 1] = True

    return dp[n]
```

---

## Related: Concatenated Words

```python
def find_all_concatenated_words(words: list[str]) -> list[str]:
    """
    Find words that are concatenation of other words.

    Time: O(n × m²) where n = words, m = max length
    Space: O(total chars)
    """
    word_set = set(words)
    result = []

    def can_form(word: str) -> bool:
        if not word:
            return False

        n = len(word)
        dp = [False] * (n + 1)
        dp[0] = True

        for i in range(1, n + 1):
            for j in range(i):
                # Must use at least 2 words
                if dp[j] and s[j:i] in word_set:
                    if j > 0 or i < n:  # Avoid matching just the word itself
                        dp[i] = True
                        break

        return dp[n]

    for word in words:
        # Temporarily remove word from set
        word_set.discard(word)
        if can_form(word):
            result.append(word)
        word_set.add(word)

    return result
```

---

## BFS Approach

```python
from collections import deque

def word_break_bfs(s: str, wordDict: list[str]) -> bool:
    """
    BFS approach - treat as graph problem.

    Time: O(n² × k)
    Space: O(n)
    """
    word_set = set(wordDict)
    n = len(s)

    visited = set()
    queue = deque([0])

    while queue:
        start = queue.popleft()

        if start in visited:
            continue
        visited.add(start)

        for end in range(start + 1, n + 1):
            if s[start:end] in word_set:
                if end == n:
                    return True
                queue.append(end)

    return False
```

---

## Edge Cases

```python
# 1. Empty string
s = ""
# Return True (empty can be segmented trivially)

# 2. Empty dictionary
s = "abc", wordDict = []
# Return False

# 3. Single word match
s = "leetcode", wordDict = ["leetcode"]
# Return True

# 4. No valid segmentation
s = "catsandog", wordDict = ["cats", "dog", "sand", "and", "cat"]
# Return False ("o" left over)

# 5. Same word multiple times
s = "aaaa", wordDict = ["a", "aa"]
# Return True (multiple valid segmentations)
```

---

## Common Mistakes

```python
# WRONG: Not checking dp[j] before substring check
for j in range(i):
    if s[j:i] in word_set:  # Missing dp[j] check!
        dp[i] = True

# CORRECT:
for j in range(i):
    if dp[j] and s[j:i] in word_set:
        dp[i] = True


# WRONG: Off-by-one in substring
s[j:i-1] in word_set  # Wrong range

# CORRECT:
s[j:i] in word_set  # s[j:i] is s[j] to s[i-1]


# WRONG: Not handling empty dictionary
max_len = max(len(w) for w in wordDict)  # Error if empty!

# CORRECT:
max_len = max((len(w) for w in wordDict), default=0)
```

---

## Complexity

| Variant                  | Time         | Space             |
| ------------------------ | ------------ | ----------------- |
| Word Break I             | O(n² × k)    | O(n)              |
| Word Break I (optimized) | O(n × m × k) | O(n)              |
| Word Break I (Trie)      | O(n²)        | O(Σ word lengths) |
| Word Break II            | O(2ⁿ) worst  | O(2ⁿ)             |

n = string length, k = average word length for hashing, m = max word length

---

## Interview Tips

1. **Start with DP**: Show systematic thinking
2. **Optimize with max length**: Mention as improvement
3. **Know Word Break II**: Often asked as follow-up
4. **BFS alternative**: Good to mention
5. **Handle edge cases**: Empty string, empty dict

---

## Practice Problems

| #   | Problem                    | Difficulty | Variant       |
| --- | -------------------------- | ---------- | ------------- |
| 1   | Word Break                 | Medium     | Boolean       |
| 2   | Word Break II              | Hard       | All sentences |
| 3   | Concatenated Words         | Hard       | Self-concat   |
| 4   | Extra Characters in String | Medium     | Min leftover  |

---

## Key Takeaways

1. **DP state**: dp[i] = can segment s[0..i-1]
2. **Set for O(1) lookup**: Essential optimization
3. **Limit by max word length**: Further optimization
4. **Word Break II**: Memoized backtracking
5. **Trie for many words**: Alternative approach

---

## Next: [14-regex-matching.md](./14-regex-matching.md)

Learn pattern matching with wildcards and regex.

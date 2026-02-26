# Word Break

> **Prerequisites:** [03-1d-dp-basics](./03-1d-dp-basics.md)

## Overview

Word Break determines if a string can be segmented into a sequence of dictionary words.

## Formal Recurrence

Let $dp[i]$ be a boolean indicating whether the prefix of $s$ of length $i$ (which is $s[0..i-1]$) can be segmented into dictionary words.

To find if $dp[i]$ is `True`, we check all possible split points $j$ before $i$. If the prefix up to $j$ is valid ($dp[j]$ is `True`), AND the remaining substring $s[j..i-1]$ is a valid word in the dictionary, then $dp[i]$ must be `True`.

$$
dp[i] = \bigvee_{j=0}^{i-1} \big( dp[j] \text{ AND } (s[j..i-1] \in \text{wordDict}) \big)
$$

**Base Case:**
- $dp[0] = \text{True}$ (An empty string can be trivially "segmented" into 0 words. This acts as the anchor that allows the first word to match.)

## Building Intuition

**Why does Word Break need DP?**

1. **Overlapping Subproblems**: To check if "leetcode" can be segmented, we might try "l" + "eetcode" or "le" + "etcode" or "lee" + "tcode" or "leet" + "code". The check for whether "code" is segmentable will be repeated across different paths if we just use recursion.
2. **Greedy Fails**: Consider $s$ = "catsanddog", `dict` = ["cat", "cats", "and", "sand", "dog"]. Greedily matching the longest word "cats" leaves "anddog", which fails. But "cat" + "sand" + "dog" works. DP explores all valid branches without committing too early.
3. **The DP State**: `dp[i]` = "can $s[0..i-1]$ be segmented?"
4. **Optimization Insight**: We don't need to check all $j$ from $0$ to $i-1$. We only need to check $j$ values where the distance $i-j$ is less than or equal to the maximum word length in the dictionary. This significantly prunes the inner loop.
5. **Mental Model**: Imagine reading a string character by character. At each position $i$, you look backward and ask: "Is there a valid dictionary word ending right here, AND could everything before that word be cleanly segmented?"

## When NOT to Use Word Break DP

1. **Dictionary Has Fixed Small Words**: If all dictionary words are very short (e.g. length $\leq 5$), building a Trie and doing DFS might be $O(n \times k)$ instead of $O(n^2)$.
2. **Single Dictionary Word Check**: To check if $s$ is exactly one dictionary word, just use `s in word_set`. DP is overkill.
3. **Very Long String, Huge Dictionary**: The standard $O(n^2)$ DP can be slow. Aho-Corasick automaton searches all dictionary words simultaneously in $O(n + m)$ time.
4. **Need All Segmentations (Word Break II)**: Standard DP only gives a boolean or count. If you need to return actual sentences, use Backtracking with Memoization.
5. **Word Order Matters**: Standard Word Break doesn't care about grammar or sequence of words. If "cat dog" is valid but "dog cat" is not, you need a different state machine.

---

## Problem Statement

Given a string $s$ and dictionary `wordDict`, return true if $s$ can be segmented into dictionary words.

```
Input: s = "leetcode", wordDict = ["leet", "code"]
Output: true
Explanation: "leetcode" = "leet" + "code"
```

---

## Implementations

### 1. Top-Down (Memoization)

```python
def word_break_memo(s: str, wordDict: list[str]) -> bool:
    """
    Top-Down DP
    Time: O(n^2 * k) where k is string slicing cost
    Space: O(n)
    """
    word_set = frozenset(wordDict)
    memo = {}

    def dfs(start: int) -> bool:
        if start == len(s):
            return True
        if start in memo:
            return memo[start]

        for end in range(start + 1, len(s) + 1):
            if s[start:end] in word_set and dfs(end):
                memo[start] = True
                return True

        memo[start] = False
        return False

    return dfs(0)
```

### 2. Bottom-Up 1D Tabulation (Standard)

```python
def word_break(s: str, wordDict: list[str]) -> bool:
    """
    Can s be segmented into dictionary words?
    Time: O(n^2 * k) where k = average word length (for slicing/hashing)
    Space: O(n)
    """
    word_set = set(wordDict)
    n = len(s)
    dp = [False] * (n + 1)

    # Base case: empty string
    dp[0] = True

    for i in range(1, n + 1):
        for j in range(i):
            if dp[j] and s[j:i] in word_set:
                dp[i] = True
                break

    return dp[n]
```

### 3. Optimized Tabulation: Limit by Max Word Length (Best Practice)

This changes the time complexity from $O(n^2)$ to $O(n \times m)$ where $m$ is the max word length.

```python
def word_break_optimized(s: str, wordDict: list[str]) -> bool:
    """
    Optimize by only checking valid word lengths.
    Time: O(n * m * k) where m = max word length
    Space: O(n)
    """
    word_set = set(wordDict)
    max_len = max(len(w) for w in wordDict) if wordDict else 0

    n = len(s)
    dp = [False] * (n + 1)
    dp[0] = True

    for i in range(1, n + 1):
        # Only look back up to max_len characters
        start = max(0, i - max_len)
        for j in range(start, i):
            if dp[j] and s[j:i] in word_set:
                dp[i] = True
                break

    return dp[n]
```

---

## Word Break II: All Segmentations

When you need to enumerate all valid paths, use Backtracking + Memoization.
Bottom-up DP is hard to reconstruct when there are exponentially many paths.

```python
def word_break_ii(s: str, wordDict: list[str]) -> list[str]:
    """
    Return all valid segmentations.
    Time: O(2^n) worst case
    Space: O(2^n * n) for memoizing all sentences
    """
    word_set = frozenset(wordDict)
    memo = {}

    def backtrack(start: int) -> list[str]:
        if start in memo:
            return memo[start]

        if start == len(s):
            return [""] # Return empty string to signify valid end

        sentences = []
        for end in range(start + 1, len(s) + 1):
            word = s[start:end]
            if word in word_set:
                # Get all valid sentences for the rest of the string
                for rest in backtrack(end):
                    if rest:
                        sentences.append(word + " " + rest)
                    else:
                        sentences.append(word)

        memo[start] = sentences
        return sentences

    return backtrack(0)
```

---

## DP Table Visualization

`s = "leetcode"`, `wordDict = ["leet", "code"]`

| i | Char | dp[i] | Logic |
| :--- | :--- | :--- | :--- |
| **0** | `""` | `True` | Base Case |
| **1** | `l` | `False` | `s[0:1]="l"` not in dict |
| **2** | `e` | `False` | `s[0:2]="le"` not in dict |
| **3** | `e` | `False` | `s[0:3]="lee"` not in dict |
| **4** | `t` | `True` | `dp[0]` is True AND `s[0:4]="leet"` in dict ✓ |
| **5** | `c` | `False` | `dp[4]` is True but `s[4:5]="c"` not in dict |
| **6** | `o` | `False` | `dp[4]` is True but `s[4:6]="co"` not in dict |
| **7** | `d` | `False` | `dp[4]` is True but `s[4:7]="cod"` not in dict |
| **8** | `e` | `True` | `dp[4]` is True AND `s[4:8]="code"` in dict ✓ |

**Answer**: `dp[8] = True`

---

## Common Mistakes

```python
# WRONG: Not checking dp[j] before substring check
for j in range(i):
    if s[j:i] in word_set:  # Missing dp[j] check!
        dp[i] = True
# This says "if the LAST word is in dict, it's valid"
# ignoring whether the PREFIX was valid!

# CORRECT:
for j in range(i):
    if dp[j] and s[j:i] in word_set:
        dp[i] = True


# WRONG: Off-by-one in substring
s[j:i-1] in word_set  # Missing the last character

# CORRECT:
s[j:i] in word_set  # Python slices up to (but not including) i


# WRONG: Not handling empty dictionary
max_len = max(len(w) for w in wordDict)  # Error if empty!

# CORRECT:
max_len = max((len(w) for w in wordDict), default=0)
```

---

## Complexity Recap

| Variant | Time | Space | Notes |
| :--- | :--- | :--- | :--- |
| Word Break I (Standard) | $O(n^2 \times k)$ | $O(n)$ | $k$ is slice time |
| Word Break I (Optimized) | $O(n \times m \times k)$ | $O(n)$ | $m$ is max word length |
| Word Break I (Trie) | $O(n^2)$ | $O(\text{dict chars})$ | Fast matching |
| Word Break II | $O(2^n)$ worst | $O(2^n)$ | Exponential output |
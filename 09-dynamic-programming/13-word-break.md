# Word Break

> **Prerequisites:** [03-1d-dp-basics](./03-1d-dp-basics.md)

## Overview

The **Word Break** problem asks whether a given string $s$ can be completely segmented into a space-separated sequence of one or more dictionary words. It is a classic example of using Dynamic Programming (DP) to avoid redundant computation when exploring combinations.

If you can break a string `s[0..i]` into valid words, it implies there exists some split point `j` such that `s[0..j]` can be broken into valid words, and the remaining suffix `s[j..i]` is itself a valid dictionary word.

## Building Intuition

Consider a string $s$ = `"catsanddog"` and a dictionary `wordDict = ["cat", "cats", "and", "sand", "dog"]`.

**Why does a Greedy approach fail?**
If we greedily match the longest word, we might pick `"cats"`. The remaining string is `"anddog"`. We match `"and"`, leaving `"dog"`. We match `"dog"`, leaving `""`. This works!
But what if the dictionary was `["cat", "cats", "and", "sand", "dog"]` and the string was `"catsand"`.
If we greedily pick `"cats"`, the remainder is `"and"`. We match `"and"`, leaving `""`. This works!
What if string is `"catsanddog"` and dict is `["cats", "dog", "sand", "and", "cat"]`.
Greedily picking `"cats"` leaves `"anddog"`. In this case we have `"and"` and `"dog"`. But what if dict was `["cats", "dog", "sand", "cat"]` and string is `"catsanddog"`.
If we greedily pick `"cats"`, the remainder is `"anddog"`, which fails because `"and"` isn't in the dict. But `"cat" + "sand" + "dog"` would work!
A greedy choice commits to a path that might lead to a dead end.

**Why does plain recursion fail?**
We can try all possible prefixes: `"c"`, `"ca"`, `"cat"`... If `"cat"` is a word, we recursively check `"sanddog"`. The problem is **overlapping subproblems**. When trying to segment `"leetcode"`, we might reach the substring `"ode"` via multiple paths if the dictionary contained `"l"`, `"le"`, `"eet"`, `"et"`, `"c"`. Computing whether `"ode"` can be segmented is identical regardless of how we got there.

**The DP Solution:**
Instead of re-evaluating the same suffixes or prefixes, we can build the solution incrementally. We ask: "Can the prefix of length $i$ be segmented?"
To answer this, we look at all possible lengths $j$ of the *last word* in that prefix. If the prefix of length $i-j$ is segmentable, and the last $j$ characters form a valid word, then the prefix of length $i$ is segmentable.

## Formal Recurrence

Let $dp[i]$ be a boolean value indicating whether the prefix of $s$ of length $i$ (which corresponds to the substring $s[0 \dots i-1]$) can be segmented into words from the dictionary.

**State:**
$dp[i]$ = `True` if $s[0 \dots i-1]$ can be segmented, `False` otherwise.

**Recurrence Relation:**
For a given length $i$, we check all possible split points $j$ where $0 \le j < i$.
If $dp[j]$ is `True` (meaning the prefix of length $j$ is valid), we only need to check if the remaining substring $s[j \dots i-1]$ is in the dictionary.

$$
dp[i] = \bigvee_{j=0}^{i-1} \big( dp[j] \text{ AND } (s[j \dots i-1] \in \text{wordDict}) \big)
$$

**Base Case:**
- $dp[0] = \text{True}$
An empty string can be trivially "segmented" into 0 words. This base case acts as the anchor that allows the first word in the string to match (when $j=0$).

## Implementations

### 1. Top-Down (Memoization)

This approach is intuitive as it closely mirrors the recursive thought process. We define a function that checks if a suffix starting at index `start` can be segmented.

```python
def wordBreak(s: str, wordDict: list[str]) -> bool:
    """
    Top-Down DP (Memoization)
    Time Complexity: O(n^3) - For every start index (n), we try every end index (n),
                     and taking a substring of length n takes O(n) time.
                     Checking if a word is in a set takes O(1) on average.
    Space Complexity: O(n) - For the recursion stack and memoization dictionary.
    """
    # Use a set for O(1) average time complexity lookups
    word_set = set(wordDict)
    memo = {}

    def dfs(start: int) -> bool:
        # Reached the end of the string successfully
        if start == len(s):
            return True

        # Return previously computed result
        if start in memo:
            return memo[start]

        # Try all possible end indices for the next word
        for end in range(start + 1, len(s) + 1):
            # If the current substring is a valid word AND the rest can be segmented
            if s[start:end] in word_set and dfs(end):
                memo[start] = True
                return True

        # If no valid segmentation is found from this start index
        memo[start] = False
        return False

    return dfs(0)
```

### 2. Bottom-Up Tabulation (Standard)

This is the standard DP approach. We build an array $dp$ of size $n+1$.

```python
def wordBreak(s: str, wordDict: list[str]) -> bool:
    """
    Bottom-Up DP
    Time Complexity: O(n^3) - Outer loop O(n), inner loop O(n), substring slicing O(n).
    Space Complexity: O(n) - For the DP array.
    """
    word_set = set(wordDict)
    n = len(s)

    # dp[i] represents whether s[0...i-1] can be segmented
    dp = [False] * (n + 1)

    # Base case: empty string
    dp[0] = True

    for i in range(1, n + 1):
        for j in range(i):
            # If the prefix ending at j is valid AND the suffix from j to i is a word
            if dp[j] and s[j:i] in word_set:
                dp[i] = True
                break # No need to check other splits once we found a valid one for dp[i]

    return dp[n]
```

### 3. Optimized Tabulation (Length Bounded)

The inner loop in the standard tabulation checks all $j$ from $0$ to $i-1$. However, the suffix $s[j \dots i-1]$ can never be a valid dictionary word if its length ($i-j$) is greater than the longest word in the dictionary. We can optimize the inner loop by only looking back up to the maximum word length.

```python
def wordBreak(s: str, wordDict: list[str]) -> bool:
    """
    Bottom-Up DP optimized by Max Word Length
    Time Complexity: O(n * m^2) - where n is len(s) and m is max word length.
                     Outer loop O(n), inner loop bounded by O(m), substring O(m).
                     If m << n, this is significantly faster than O(n^3).
    Space Complexity: O(n) - For the DP array.
    """
    if not wordDict:
        return False

    word_set = set(wordDict)
    # Find the maximum length of a word in the dictionary
    max_len = max(len(w) for w in wordDict)

    n = len(s)
    dp = [False] * (n + 1)
    dp[0] = True

    for i in range(1, n + 1):
        # We only need to look back at most `max_len` characters.
        # Ensure we don't go out of bounds (j < 0).
        start_j = max(0, i - max_len)

        # Iterate backwards is often faster because we find shorter matching suffixes first
        for j in range(i - 1, start_j - 1, -1):
            if dp[j] and s[j:i] in word_set:
                dp[i] = True
                break

    return dp[n]
```

## DP Table Visualization

Let's trace `s = "leetcode"`, `wordDict = ["leet", "code"]`.
Max word length is 4.

| `i` | String Prefix $s[0\dots i-1]$ | Checked Suffixes $s[j\dots i-1]$ | `dp[i]` | Reason |
| :-- | :---------------------------- | :------------------------------- | :------ | :----- |
| 0   | `""` | None | `True` | Base Case |
| 1   | `"l"` | `"l"` ($j=0$) | `False` | `"l"` not in dict |
| 2   | `"le"` | `"e"` ($j=1$), `"le"` ($j=0$) | `False` | Neither suffix is in dict (and `dp[1]` is False) |
| 3   | `"lee"` | `"e"`, `"ee"`, `"lee"` | `False` | No valid suffix in dict |
| 4   | `"leet"` | `"t"`, `"et"`, `"eet"`, `"leet"` ($j=0$) | `True` | `dp[0]` is `True` & `"leet"` $\in$ dict |
| 5   | `"leetc"` | `"c"`, `"tc"`, `"etc"`, `"eetc"` | `False` | None in dict (max lookback is 4) |
| 6   | `"leetco"`| `"o"`, `"co"`, `"tco"`, `"etco"` | `False` | None in dict |
| 7   | `"leetcod"`| `"d"`, `"od"`, `"cod"`, `"tcod"` | `False` | None in dict |
| 8   | `"leetcode"`| `"e"`, `"de"`, `"ode"`, `"code"` ($j=4$) | `True` | `dp[4]` is `True` & `"code"` $\in$ dict |

Result is `dp[8] = True`.

## Word Break II: Finding All Segmentations

Sometimes you don't just want to know *if* it can be segmented, but you want to return *all possible* sentences. For this, DP tabulation is cumbersome because you have to reconstruct paths. The standard approach is Backtracking with Memoization.

```python
def wordBreakII(s: str, wordDict: list[str]) -> list[str]:
    """
    Return all valid segmentations.
    Time Complexity: O(2^n + n^3) in the worst case (e.g. s="aaaaa", dict=["a","aa","aaa"]).
                     The +n^3 comes from slicing and string concatenation.
    Space Complexity: O(2^n * n) for storing all valid sentences in the worst case.
    """
    word_set = set(wordDict)
    memo = {}

    def backtrack(start: int) -> list[str]:
        # Return memoized result if available
        if start in memo:
            return memo[start]

        # Base case: reached the end, return a list containing an empty string
        # to signify a successful segmentation path.
        if start == len(s):
            return [""]

        valid_sentences = []
        for end in range(start + 1, len(s) + 1):
            word = s[start:end]
            if word in word_set:
                # Recursively get sentences for the remaining suffix
                suffix_sentences = backtrack(end)
                for suffix in suffix_sentences:
                    if suffix == "":
                        # Last word in the sentence
                        valid_sentences.append(word)
                    else:
                        # Append the word with a space to the suffix sentence
                        valid_sentences.append(word + " " + suffix)

        memo[start] = valid_sentences
        return valid_sentences

    return backtrack(0)
```

## Common Mistakes to Avoid

1. **Forgetting to check the previous state (`dp[j]`):**
   ```python
   # WRONG
   for j in range(i):
       if s[j:i] in word_set:
           dp[i] = True
   ```
   This only checks if the *last* chunk is a valid word. It completely ignores whether the prefix before it was valid. It would say `"catsdog"` is valid for `dict=["dog"]` because `"dog"` is at the end.

2. **Off-by-one errors in string slicing:**
   Python slicing `s[start:end]` goes up to, but *does not include*, `end`.
   ```python
   # WRONG
   s[j:i-1] in word_set

   # CORRECT
   s[j:i] in word_set
   ```

3. **Optimizing length without handling empty dictionaries:**
   ```python
   # WRONG: max() throws an error on an empty sequence
   max_len = max(len(w) for w in wordDict)

   # CORRECT
   max_len = max((len(w) for w in wordDict), default=0)
   # Or handle early:
   if not wordDict: return False
   ```

4. **Iterating the inner loop forward instead of backward:**
   When using the max length optimization, it's generally faster to iterate $j$ backwards from $i-1$ down to $i - \text{max\_len}$. If you iterate forward, you might do a lot of long substring checks. Iterating backward checks shorter suffixes first, which are cheaper to slice and hash.

## When NOT to Use Standard Word Break DP

1. **Need all segmentations:** Use Backtracking with Memoization (Word Break II) instead of standard DP.
2. **Finding the *minimum* words:** The problem changes from returning a boolean to finding a minimum value. You'd initialize $dp$ with $\infty$ and use $dp[i] = \min(dp[i], dp[j] + 1)$.
3. **Very long strings / massive dictionary:** $O(n \times m^2)$ can be too slow. A **Trie** can be used to optimize the substring lookup. Instead of slicing the string and hashing it (which takes $O(\text{length})$ time), you can walk down a Trie character by character. If the string is massive and the dictionary is massive, an **Aho-Corasick** automaton provides an $O(n + \text{matches})$ linear time solution to find all matches, which can then be combined with a DP array.
4. **Order matters (Grammar):** If `"cat dog"` is valid but `"dog cat"` is not, the problem requires a state machine or parsing algorithm, not just set lookups.

## Complexity Recap

| Approach | Time Complexity | Space Complexity | Notes |
| :------- | :-------------- | :--------------- | :---- |
| Top-Down Memoization | $O(n^3)$ | $O(n)$ | $O(n^2)$ states, $O(n)$ slicing/hashing |
| Bottom-Up DP (Standard) | $O(n^3)$ | $O(n)$ | $O(n^2)$ loops, $O(n)$ slicing/hashing |
| Bottom-Up DP (Optimized) | $O(n \cdot m^2)$ | $O(n)$ | $m$ is max word length. Best for most cases. |
| Trie + DP | $O(n^2 + \text{dict\_chars})$ | $O(n + \text{dict\_chars})$ | Avoids string slicing overhead entirely. |
| Word Break II (All Paths)| $O(2^n + n^3)$ | $O(2^n \cdot n)$ | Output size can be exponential. |

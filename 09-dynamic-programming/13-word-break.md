# Word Break

> **Prerequisites:** [03-1d-dp-basics](./03-1d-dp-basics.md)

## Overview

The **Word Break** problem (LeetCode 139) asks whether a given string $s$ can be completely segmented into a space-separated sequence of one or more dictionary words. It is a classic example of using Dynamic Programming (DP) to avoid redundant computation when exploring combinations.

If you can break a string `s[0..i]` into valid words, it implies there exists some split point `j` such that `s[0..j]` can be broken into valid words, and the remaining suffix `s[j..i]` is itself a valid dictionary word.

## Building Intuition

Consider a string $s$ = `"catsanddog"` and a dictionary `wordDict = ["cat", "cats", "and", "sand", "dog"]`.

**Why does a Greedy approach fail?**
If we greedily match the longest word, we might pick `"cats"`. The remaining string is `"anddog"`. We match `"and"`, leaving `"dog"`. We match `"dog"`, leaving `""`. This works!

But what if the dictionary was `["cats", "dog", "sand", "and", "cat"]` and the string was `"catsanddog"`.
If we greedily pick `"cats"`, the remainder is `"anddog"`. If we didn't have `"and"` in our dictionary, but only `"sand"`, the greedy approach fails. However, picking `"cat" + "sand" + "dog"` would work perfectly.

A greedy choice commits to a path that might lead to a dead end, failing to explore valid alternatives.

**Why does plain recursion fail?**
We can try all possible prefixes: `"c"`, `"ca"`, `"cat"`... If `"cat"` is a word, we recursively check the remainder `"sanddog"`. The problem is **overlapping subproblems**.

Imagine trying to segment `"leetcode"`. We might reach the remainder `"ode"` via multiple paths if the dictionary contained `"l"`, `"le"`, `"eet"`, `"et"`, `"c"`. Computing whether `"ode"` can be segmented is identical regardless of how we got there. Recomputing it leads to an exponential $O(2^n)$ time complexity.

**The DP Solution:**
Instead of re-evaluating the same suffixes or prefixes, we can build the solution incrementally. We ask: "Can the prefix of length $i$ be segmented?"
To answer this, we look at all possible lengths $j$ of the *last word* in that prefix. If the prefix of length $j$ is segmentable, and the last $i-j$ characters form a valid word, then the prefix of length $i$ is segmentable.

## Formal Recurrence

Let $dp[i]$ be a boolean value indicating whether the prefix of $s$ of length $i$ (which corresponds to the substring $s[0 \dots i-1]$) can be segmented into words from the dictionary.

**State:**
$dp[i]$ = `True` if $s[0 \dots i-1]$ can be segmented, `False` otherwise.

**Recurrence Relation:**
For a given length $i$, we check all possible split points $j$ where $0 \le j < i$.
If $dp[j]$ is `True` (meaning the prefix of length $j$ is valid), we only need to check if the remaining substring $s[j \dots i-1]$ is in the dictionary.

$$
dp[i] = \bigvee_{j=0}^{i-1} \big( dp[j] \text{ AND } (s[j \dots i-1] \in \text{word\_dict}) \big)
$$

**Base Case:**
- $dp[0] = \text{True}$
An empty string can be trivially "segmented" into 0 words. This base case acts as the anchor that allows the first word in the string to match (when $j=0$).

---

## Implementations

### 1. Top-Down (Memoization)

This approach is intuitive as it closely mirrors the recursive thought process. We define a function that checks if a suffix starting at index `start` can be segmented.

```python
def word_break_memo(s: str, word_dict: list[str]) -> bool:
    """
    Time Complexity: O(n^3)
    - For every start index (n), we try every end index (n), taking O(n^2).
    - Inside the loop, string slicing `s[start:end]` and hashing it takes O(n) time.
    - Thus, total time is O(n^3).
    Space Complexity: O(n) for the recursion stack and memoization dictionary.
    """
    # Use a set for O(1) average time complexity lookups
    word_set = set(word_dict)
    memo = {}

    def dfs(start: int) -> bool:
        # Reached the end of the string successfully
        if start == len(s):
            return True

        if start in memo:
            return memo[start]

        # Try all possible end indices for the next word
        for end in range(start + 1, len(s) + 1):
            # If current substring is a valid word AND the rest can be segmented
            if s[start:end] in word_set and dfs(end):
                memo[start] = True
                return True

        memo[start] = False
        return False

    return dfs(0)
```

### 2. Bottom-Up Tabulation (Standard)

This is the standard DP approach. We build an array $dp$ of size $n+1$.

```python
def word_break_tabulation(s: str, word_dict: list[str]) -> bool:
    """
    Time Complexity: O(n^3)
    - Outer loop runs n times.
    - Inner loop runs up to n times.
    - Slicing `s[j:i]` takes O(n) time.
    - Thus, total time is O(n^3).
    Space Complexity: O(n) for the DP array.
    """
    word_set = set(word_dict)
    n = len(s)

    # dp[i] represents whether s[0...i-1] can be segmented
    dp = [False] * (n + 1)
    dp[0] = True # Base case: empty string

    for i in range(1, n + 1):
        for j in range(i):
            # If prefix ending at j is valid AND suffix from j to i is a word
            if dp[j] and s[j:i] in word_set:
                dp[i] = True
                break # No need to check other splits once we found a valid one

    return dp[n]
```

### 3. Optimized Tabulation (Length Bounded)

The inner loop in the standard tabulation checks all $j$ from $0$ to $i-1$. However, the suffix $s[j \dots i-1]$ can never be a valid dictionary word if its length ($i-j$) is greater than the longest word in the dictionary. We can optimize the inner loop by only looking back up to the maximum word length.

```python
def word_break_optimized(s: str, word_dict: list[str]) -> bool:
    """
    Time Complexity: O(n * m^2) where n is len(s) and m is max word length.
    - Outer loop n times, inner loop bounded by O(m).
    - Substring slicing takes O(m).
    - If m << n, this is significantly faster than O(n^3).
    Space Complexity: O(n) for the DP array.
    """
    if not word_dict:
        return False

    word_set = set(word_dict)
    max_len = max(len(w) for w in word_dict)
    n = len(s)

    dp = [False] * (n + 1)
    dp[0] = True

    for i in range(1, n + 1):
        # Only look back at most `max_len` characters
        start_j = max(0, i - max_len)

        # Iterating backwards is often faster: we find shorter matching suffixes first
        for j in range(i - 1, start_j - 1, -1):
            if dp[j] and s[j:i] in word_set:
                dp[i] = True
                break

    return dp[n]
```

---

## DP Table Visualization

Let's trace `s = "leetcode"`, `word_dict = ["leet", "code"]`.
Max word length is 4.

| `i` | String Prefix $s[0\dots i-1]$ | Checked Suffixes $s[j\dots i-1]$ | `dp[i]` | Reason |
| :-- | :---------------------------- | :------------------------------- | :------ | :----- |
| 0   | `""` | None | `True` | Base Case |
| 1   | `"l"` | `"l"` ($j=0$) | `False` | `"l"` not in dict |
| 2   | `"le"` | `"e"` ($j=1$), `"le"` ($j=0$) | `False` | Neither suffix is in dict |
| 3   | `"lee"` | `"e"`, `"ee"`, `"lee"` | `False` | No valid suffix in dict |
| 4   | `"leet"` | `"t"`, `"et"`, `"eet"`, `"leet"` ($j=0$) | `True` | `dp[0]` is `True` & `"leet"` $\in$ dict |
| 5   | `"leetc"` | `"c"`, `"tc"`, `"etc"`, `"eetc"` | `False` | None in dict (max lookback is 4) |
| 6   | `"leetco"`| `"o"`, `"co"`, `"tco"`, `"etco"` | `False` | None in dict |
| 7   | `"leetcod"`| `"d"`, `"od"`, `"cod"`, `"tcod"` | `False` | None in dict |
| 8   | `"leetcode"`| `"e"`, `"de"`, `"ode"`, `"code"` ($j=4$) | `True` | `dp[4]` is `True` & `"code"` $\in$ dict |

Result is `dp[8] = True`.

---

## Word Break II: Finding All Segmentations

Sometimes you don't just want to know *if* it can be segmented, but you want to return *all possible* sentences. For this, DP tabulation is cumbersome because you have to reconstruct paths. The standard approach is Backtracking with Memoization.

```python
def word_break_ii(s: str, word_dict: list[str]) -> list[str]:
    """
    Time Complexity: O(2^n + n^3) worst case (e.g., s="aaaa", dict=["a","aa"]).
    - The output size can be exponential, thus constructing it takes exponential time.
    Space Complexity: O(2^n * n) for storing all valid sentences in the worst case.
    """
    word_set = set(word_dict)
    memo = {}

    def backtrack(start: int) -> list[str]:
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

---

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

3. **Optimizing length without handling empty dictionaries:**
   ```python
   # WRONG: max() throws an error on an empty sequence
   max_len = max(len(w) for w in word_dict)

   # CORRECT
   max_len = max((len(w) for w in word_dict), default=0)
   # Or handle early:
   if not word_dict: return False
   ```

4. **Iterating the inner loop forward instead of backward:**
   When using the max length optimization, it's generally faster to iterate $j$ backwards from $i-1$ down to $i - \text{max\_len}$. If you iterate forward, you might do a lot of long substring checks. Iterating backward checks shorter suffixes first, which are cheaper to slice and hash.

---

## Complexity Summary

| Approach | Time Complexity | Space Complexity | Notes |
| :------- | :-------------- | :--------------- | :---- |
| Top-Down Memoization | $O(n^3)$ | $O(n)$ | $O(n^2)$ states, $O(n)$ slicing/hashing |
| Bottom-Up DP (Standard) | $O(n^3)$ | $O(n)$ | $O(n^2)$ loops, $O(n)$ slicing/hashing |
| Bottom-Up DP (Optimized) | $O(n \cdot m^2)$ | $O(n)$ | $m$ is max word length. Best for most cases. |
| Trie + DP | $O(n^2 + \text{dict\_chars})$ | $O(n + \text{dict\_chars})$ | Avoids string slicing overhead entirely. |
| Word Break II (All Paths)| $O(2^n + n^3)$ | $O(2^n \cdot n)$ | Output size can be exponential. |

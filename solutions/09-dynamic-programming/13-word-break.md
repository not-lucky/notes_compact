# Solutions: Word Break

## 1. Word Break

**Problem:** Can string $s$ be segmented into dictionary words?

### Optimal Python Solution

```python
def word_break(s: str, wordDict: list[str]) -> bool:
    # State: dp[i] = can s[:i] be segmented
    # Optimization: Only check word lengths present in dictionary
    word_set = set(wordDict)
    max_len = max(len(w) for w in wordDict) if wordDict else 0
    dp = [False] * (len(s) + 1)
    dp[0] = True

    for i in range(1, len(s) + 1):
        # Only check j such that length (i-j) <= max_len
        for j in range(max(0, i - max_len), i):
            if dp[j] and s[j:i] in word_set:
                dp[i] = True
                break
    return dp[-1]
```

### Complexity Analysis

- **Time:** $O(n \times L \times k)$ where $n$ is string length, $L$ is max word length, and $k$ is string slicing cost.
- **Space:** $O(n + \text{dictionary\_size})$

---

## 2. Word Break II

**Problem:** Return all valid segmentations.

### Optimal Python Solution

```python
def word_break_ii(s: str, wordDict: list[str]) -> list[str]:
    word_set = set(wordDict)
    memo = {}

    def backtrack(start):
        if start in memo: return memo[start]
        if start == len(s): return [""]

        res = []
        for end in range(start + 1, len(s) + 1):
            word = s[start:end]
            if word in word_set:
                for suffix in backtrack(end):
                    res.append(word + (" " + suffix if suffix else ""))
        memo[start] = res
        return res

    return backtrack(0)
```

### Complexity Analysis

- **Time:** $O(2^n)$ in worst case (exponential number of sentences).
- **Space:** $O(2^n)$ for storing results.

---

## 3. Extra Characters in String

**Problem:** Minimum leftover characters after segmenting $s$ into dictionary words.

### Optimal Python Solution

```python
def min_extra_char(s: str, dictionary: list[str]) -> int:
    word_set = set(dictionary)
    n = len(s)
    dp = [0] * (n + 1) # dp[i] = min extra in s[:i]

    for i in range(1, n + 1):
        dp[i] = dp[i-1] + 1 # Default: current char is extra
        for j in range(i):
            if s[j:i] in word_set:
                dp[i] = min(dp[i], dp[j])

    return dp[n]
```

---

## 4. Concatenated Words

**Problem:** Find all words in a list that are formed by concatenating at least two other words from the same list.

### Optimal Python Solution

```python
def find_all_concatenated_words_in_a_dict(words: list[str]) -> list[str]:
    word_set = set(words)
    memo = {}

    def can_form(word):
        if word in memo: return memo[word]

        for i in range(1, len(word)):
            prefix = word[:i]
            suffix = word[i:]

            # If prefix exists and (suffix exists or can be further split)
            if prefix in word_set and (suffix in word_set or can_form(suffix)):
                memo[word] = True
                return True

        memo[word] = False
        return False

    res = []
    for w in words:
        if not w: continue
        if can_form(w):
            res.append(w)
    return res
```

### Explanation

1.  **Word Break Variant**: For each word, we check if it can be broken into at least two other words.
2.  **Logic**: We split the word into `prefix` and `suffix`. If `prefix` is in the set AND (`suffix` is in the set OR `suffix` itself can be formed from other words), then the word is concatenated.
3.  **Memoization**: We cache results for suffixes to avoid redundant computations across different words.

### Complexity Analysis

- **Time:** $O(N \times L^2)$ - Where $N$ is number of words and $L$ is max length.
- **Space:** $O(N \times L)$ - For the set and memoization cache.

### Complexity Analysis

- **Time:** $O(n^3)$ - Nested loops + string slicing.
- **Space:** $O(n + \text{dictionary\_size})$

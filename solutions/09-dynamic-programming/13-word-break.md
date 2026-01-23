# Word Break Solutions

## Problem: Word Break
Given a string `s` and a dictionary of strings `wordDict`, return `true` if `s` can be segmented into a space-separated sequence of one or more dictionary words.

### Constraints
- 1 <= s.length <= 300
- 1 <= wordDict.length <= 1000
- 1 <= wordDict[i].length <= 20
- `s` and `wordDict[i]` consist of only lowercase English letters.

### Examples
- Input: s = "leetcode", wordDict = ["leet", "code"] -> Output: true
- Input: s = "applepenapple", wordDict = ["apple", "pen"] -> Output: true
- Input: s = "catsandog", wordDict = ["cats", "dog", "sand", "and", "cat"] -> Output: false

### Implementation

```python
def word_break(s: str, wordDict: list[str]) -> bool:
    """
    Determines if s can be segmented into words from wordDict.
    Time complexity: O(n^2 * k) or O(n * max_len * k)
    Space complexity: O(n + size_of_dict)
    """
    word_set = set(wordDict)
    max_len = max((len(w) for w in wordDict), default=0)
    n = len(s)
    # dp[i] means s[:i] can be segmented
    dp = [False] * (n + 1)
    dp[0] = True

    for i in range(1, n + 1):
        # Optimization: only check back up to max_len
        for j in range(max(0, i - max_len), i):
            if dp[j] and s[j:i] in word_set:
                dp[i] = True
                break
    return dp[n]
```

## Problem: Word Break II
Given a string `s` and a dictionary of strings `wordDict`, add spaces in `s` to construct a sentence where each word is a valid dictionary word. Return all such possible sentences in any order.

### Implementation

```python
def word_break_ii(s: str, wordDict: list[str]) -> list[str]:
    """
    Finds all valid segmentations of s.
    Time complexity: O(2^n) in worst case
    Space complexity: O(2^n)
    """
    word_set = set(wordDict)
    memo = {}

    def backtrack(start):
        if start in memo:
            return memo[start]
        if start == len(s):
            return [""]

        res = []
        for end in range(start + 1, len(s) + 1):
            word = s[start:end]
            if word in word_set:
                suffixes = backtrack(end)
                for suffix in suffixes:
                    if suffix == "":
                        res.append(word)
                    else:
                        res.append(word + " " + suffix)
        memo[start] = res
        return res

    return backtrack(0)
```

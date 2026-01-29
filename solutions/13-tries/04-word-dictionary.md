# Solutions: Word Dictionary & Wildcards

## 1. Add and Search Word

(LeetCode 211)

### Problem Statement

Design a data structure that supports adding new words and finding if a string matches any previously added string.
`search(word)` can contain dots `.` where dots can be matched with any letter.

### Examples & Edge Cases

**Example:**

```
addWord("bad")
addWord("dad")
addWord("mad")
search("pad") -> false
search("bad") -> true
search(".ad") -> true
search("b..") -> true
```

### Optimal Python Solution

```python
class WordDictionary:
    def __init__(self):
        self.root = {}

    def addWord(self, word: str) -> None:
        node = self.root
        for char in word:
            node = node.setdefault(char, {})
        node['$'] = True

    def search(self, word: str) -> bool:
        def dfs(node, i):
            if i == len(word):
                return '$' in node

            char = word[i]
            if char == '.':
                # Try all possible children
                for child in node:
                    if child != '$' and dfs(node[child], i + 1):
                        return True
                return False
            else:
                if char not in node:
                    return False
                return dfs(node[char], i + 1)

        return dfs(self.root, 0)
```

### Explanation

1.  **Wildcard Branching**: For a regular character, we follow the single Trie path. For a `.`, we must explore every child branch at that level.
2.  **Recursion (DFS)**: This is necessary to explore the multiple possibilities introduced by wildcards.

### Complexity Analysis

- **Time Complexity**: $O(L)$ for `addWord`, where $L$ is the length of the word being added. For `search`, the worst case is $O(26^k \times L)$ where $k$ is the number of wildcards in the query. In the worst case (all dots), we may explore every node in the Trie.
- **Space Complexity**: $O(N \times L)$ to store all words in the Trie, where $N$ is the number of words.

---

## 2. Implement Magic Dictionary

(LeetCode 676)

### Problem Statement

Design a data structure that determines if changing exactly one character in a given string can match any previously added word.

### Examples & Edge Cases

**Example:**

```
dictionary = ["hello", "leetcode"]
search("hello") -> false (must change EXACTLY one char)
search("hhllo") -> true (change second 'h' to 'e')
```

### Optimal Python Solution

```python
class MagicDictionary:
    def __init__(self):
        self.root = {}

    def buildDict(self, dictionary: list[str]) -> None:
        for word in dictionary:
            node = self.root
            for char in word:
                node = node.setdefault(char, {})
            node['$'] = True

    def search(self, searchWord: str) -> bool:
        def dfs(node, i, modified):
            if i == len(searchWord):
                return modified and '$' in node

            char = searchWord[i]
            # Try to match without modification
            if char in node:
                if dfs(node[char], i + 1, modified):
                    return True

            # Try to match with modification (if not already modified)
            if not modified:
                for other_char in node:
                    if other_char != char and other_char != '$':
                        if dfs(node[other_char], i + 1, True):
                            return True
            return False

        return dfs(self.root, 0, False)
```

### Explanation

1.  **State Tracking**: The DFS state includes a `modified` boolean to ensure we change exactly one character.
2.  **Backtracking**: We try matching the character normally, and we also try substituting it with every other character available in the Trie at that level.

### Complexity Analysis

- **Time Complexity**: $O(\sum L_i)$ for building the Trie. For searching, the time complexity is $O(L \times 26)$ where $L$ is the length of `searchWord`. For each character, we explore all 26 possible branches if we haven't already performed a modification.
- **Space Complexity**: $O(\sum L_i)$ to store the dictionary in the Trie structure.

---

## 3. Prefix and Suffix Search

(LeetCode 745)

### Problem Statement

Design a data structure that supports searching for a word with a given prefix and a given suffix. If there are multiple words, return the index of the word with the maximum weight (index).

### Examples & Edge Cases

**Example:**

```
WordFilter(["apple"])
f("a", "e") -> 0
```

### Optimal Python Solution

```python
class WordFilter:
    def __init__(self, words: list[str]):
        self.trie = {}
        # Trick: For a word like "apple", insert "e#apple", "le#apple", "ple#apple", etc.
        # This allows a single prefix search to find suffix#prefix matches.
        for weight, word in enumerate(words):
            l = len(word)
            for i in range(l + 1):
                suffix = word[i:]
                key = suffix + "#" + word
                node = self.trie
                for char in key:
                    node = node.setdefault(char, {})
                    node['weight'] = weight

    def f(self, prefix: str, suffix: str) -> int:
        node = self.trie
        search_key = suffix + "#" + prefix
        for char in search_key:
            if char not in node:
                return -1
            node = node[char]
        return node['weight']
```

### Explanation

1.  **The Suffix#Prefix Trick**: To handle both prefix and suffix queries in one Trie, we store variants of the word: `suffix + '#' + word`.
2.  **Query**: Searching for `suffix + '#' + prefix` will lead us to the node representing all words with that suffix and prefix.
3.  **Weights**: Since we insert words in increasing order of weight, we simply update the `weight` at every node during insertion to keep the maximum.

### Complexity Analysis

- **Time Complexity**: $O(N \times L^2)$ for initialization, where $N$ is the number of words and $L$ is the maximum length. For each word, we insert $L$ combinations of `suffix + '#' + prefix` into the Trie. Query time is $O(L)$ as we simply traverse the Trie nodes matching the combined key.
- **Space Complexity**: $O(N \times L^2)$ to store all combined suffix and prefix variants in the Trie.

---

## 4. Camelcase Matching

(LeetCode 1023)

### Problem Statement

Given an array of strings `queries` and a string `pattern`, return a boolean array `answer` where `answer[i]` is `true` if `queries[i]` matches `pattern`. A query matches a pattern if we can insert lowercase letters into the pattern to form the query.

### Examples & Edge Cases

**Example:**

```
queries = ["FooBar","FooBarTest","FootBall","FrameBuffer","ForceFeedBack"], pattern = "FB"
Output: [true,false,true,true,false]
```

### Optimal Python Solution

```python
class Solution:
    def camelMatch(self, queries: list[str], pattern: str) -> list[bool]:
        def check(query):
            i = 0
            for char in query:
                if i < len(pattern) and char == pattern[i]:
                    i += 1
                elif char.isupper():
                    # If we encounter an extra uppercase letter not in pattern
                    return False
            return i == len(pattern)

        return [check(q) for q in queries]
```

### Explanation

1.  **Two Pointers**: We iterate through the `query` and the `pattern`.
2.  **Uppercase Constraint**: We can insert lowercase letters, but any uppercase letter in the `query` **must** match the next expected uppercase letter in the `pattern`.

### Complexity Analysis

- **Time Complexity**: $O(N \times L)$ where $N$ is the number of queries and $L$ is the length of each query. We perform a single linear scan of each query string once to verify if it can match the pattern.
- **Space Complexity**: $O(1)$ extra space beyond the result list, as we only use a few pointer variables for the scan.

---

## 5. Match Substring After Replacement

(LeetCode 2301)

### Problem Statement

You are given two strings `s` and `sub`. You are also given a 2D character array `mappings` where `mappings[i] = [old_i, new_i]` indicates that you may replace the character `old_i` in `sub` with `new_i`.
Determine if `sub` can be a substring of `s` after replacing any number of characters.

### Optimal Python Solution

```python
class Solution:
    def matchReplacement(self, s: str, sub: str, mappings: list[list[str]]) -> bool:
        # Create a fast lookup for allowed replacements
        allowed = {}
        for old, new in mappings:
            if old not in allowed: allowed[old] = {old}
            allowed[old].add(new)

        n, m = len(s), len(sub)
        for i in range(n - m + 1):
            match = True
            for j in range(m):
                char_s = s[i + j]
                char_sub = sub[j]
                # Check if s[i+j] is an allowed replacement for sub[j]
                if char_s != char_sub and (char_sub not in allowed or char_s not in allowed[char_sub]):
                    match = False
                    break
            if match: return True
        return False
```

### Explanation

1.  **Replacement Map**: Use a hashmap of sets for $O(1)$ lookup of valid character replacements.
2.  **Sliding Window**: Check every possible starting position in `s`. For each position, verify if the next `len(sub)` characters are either identical or valid replacements.

### Complexity Analysis

- **Time Complexity**: $O(N \times M)$ where $N$ is the length of string `s` and $M$ is the length of string `sub`. For each of the $N-M+1$ starting positions in `s`, we potentially compare $M$ characters, with each comparison taking $O(1)$ time via the `allowed` lookup table.
- **Space Complexity**: $O(K + A)$ where $K$ is the number of mappings and $A$ is the alphabet size. We store all valid character replacements in a dictionary.

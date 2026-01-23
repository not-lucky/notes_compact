# Solution: Autocomplete System Practice Problems

## Problem 1: Search Suggestions System
### Problem Statement
You are given an array of strings `products` and a string `searchWord`.

Design a system that suggests at most three product names from `products` after each character of `searchWord` is typed. Suggested products should have a common prefix with `searchWord`. If there are more than three products with a common prefix, return the three lexicographically minimums products.

Return a list of lists of the suggested products after each character of `searchWord` is typed.

### Python Implementation
```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.suggestions = []

class Solution:
    def suggestedProducts(self, products: list[str], searchWord: str) -> list[list[str]]:
        products.sort()
        root = TrieNode()
        for p in products:
            node = root
            for c in p:
                if c not in node.children:
                    node.children[c] = TrieNode()
                node = node.children[c]
                if len(node.suggestions) < 3:
                    node.suggestions.append(p)

        res = []
        node = root
        for c in searchWord:
            if node and c in node.children:
                node = node.children[c]
                res.append(node.suggestions)
            else:
                node = None
                res.append([])
        return res
```

---

## Problem 2: Top K Frequent Words
### Problem Statement
Given an array of strings `words` and an integer `k`, return the `k` most frequent strings.

Return the answer sorted by the frequency from highest to lowest. Sort the words with the same frequency by their lexicographical order.

### Python Implementation
```python
import collections
import heapq

class WordFreq:
    def __init__(self, word, freq):
        self.word = word
        self.freq = freq

    def __lt__(self, other):
        if self.freq == other.freq:
            return self.word > other.word # Lexicographical order for same freq
        return self.freq < other.freq

def topKFrequent(words: list[str], k: int) -> list[str]:
    counts = collections.Counter(words)
    heap = []
    for word, freq in counts.items():
        heapq.heappush(heap, WordFreq(word, freq))
        if len(heap) > k:
            heapq.heappop(heap)

    res = []
    while heap:
        res.append(heapq.heappop(heap).word)
    return res[::-1]
```

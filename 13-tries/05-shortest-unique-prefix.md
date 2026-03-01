# Shortest Unique Prefix

Find the shortest unique prefix to represent each word in a list.

## Problem Context
Given a list of words, find the shortest prefix for each word that uniquely identifies it among all words in the list.

## Implementation

We can solve this efficiently using a Trie. We update the Trie node to keep track of a `count` that represents how many words share this node (prefix).

1. **Insert**: Update the `insert` function to increment a `prefix_count` at each node.
2. **Find Prefix**: To find the unique prefix for a word, traverse its characters in the Trie until we reach a node where `prefix_count == 1`. This indicates that only this specific word uses this prefix path.

### Python 3 Solution

```python
class TrieNode:
    __slots__ = ['children', 'prefix_count']

    def __init__(self) -> None:
        self.children: dict[str, 'TrieNode'] = {}
        self.prefix_count: int = 0

class Solution:
    def __init__(self) -> None:
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
            node.prefix_count += 1

    def get_shortest_unique_prefix(self, word: str) -> str:
        node = self.root
        prefix = ""
        for char in word:
            prefix += char
            node = node.children[char]
            if node.prefix_count == 1:
                break
        return prefix

    def findPrefixes(self, words: list[str]) -> list[str]:
        # Insert all words into the Trie
        for word in words:
            self.insert(word)

        # Find shortest unique prefix for each word
        return [self.get_shortest_unique_prefix(word) for word in words]
```

## Quick Reference

| Operation | Time Complexity | Space Complexity | Description |
| :--- | :--- | :--- | :--- |
| Build Trie | $O(N \cdot M)$ | $O(N \cdot M)$ | $N$ words of average length $M$. |
| Find Prefix | $O(M)$ | $O(1)$ | Traverse path up to length $M$. |
| Total Find | $O(N \cdot M)$ | $O(N \cdot M)$ | Overall for all words. |

## Navigation

[Previous: Word Search Trie](./04-word-search-trie.md) | [Next: Autocomplete](./06-autocomplete.md)

# Concatenated Words

**Context:** [LeetCode 472 - Concatenated Words](https://leetcode.com/problems/concatenated-words/)

Given an array of strings `words` (without duplicates), return all the concatenated words in the given list of words. A concatenated word is defined as a string that is comprised entirely of at least two shorter words in the given array.

## Quick Reference

| Aspect | Details |
|--------|---------|
| **Pattern** | Trie + Depth-First Search (DFS) |
| **Strategy** | Sort by length, check composability with DFS, insert if not concatenated. |
| **Time Complexity** | $O(N \log N + N \cdot L^2)$, where $N$ is word count and $L$ is max word length. |
| **Space Complexity**| $O(N \cdot L)$ for the Trie and recursion stack. |

## Approach

The optimal approach involves using a Trie combined with Depth-First Search (DFS) and sorting:
1. **Sort words by length:** Since a concatenated word is made of *shorter* words, sorting ensures that when we process a word, all potential component words have already been processed and added to the Trie.
2. **DFS Validation:** For each word, use DFS to traverse the Trie. If we find a valid prefix (where `is_word` is true), we recursively check the remainder of the word.
3. **Dynamic Insertion:** If a word can be composed of shorter words, it's a concatenated word (add to results). If not, we insert it into the Trie so it can be used to form longer words later.

## Implementation

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
        # Sort words by length. Shorter words are evaluated and inserted first.
        words.sort(key=len)
        trie = Trie()
        result: list[str] = []

        for word in words:
            # Skip empty strings as they cannot be concatenated words
            if not word:
                continue

            # If the word can be formed by words already in the Trie, it's concatenated
            if self._can_form(word, 0, trie.root):
                result.append(word)
            else:
                # Otherwise, insert it into the Trie for future words to use
                trie.insert(word)

        return result

    def _can_form(self, word: str, start: int, root: TrieNode) -> bool:
        """
        DFS to check if the substring word[start:] can be formed by words in the Trie.
        """
        # If we reached the end of the word, we successfully matched all parts
        if start == len(word):
            return True

        node = root
        for i in range(start, len(word)):
            char = word[i]

            # If character is not in the current node's children, matching fails
            if char not in node.children:
                return False

            node = node.children[char]

            # If we find a valid word ending, recursively check the remaining substring
            if node.is_word:
                if self._can_form(word, i + 1, root):
                    return True

        return False
```

## Complexity Analysis

- **Time Complexity:**
  - Sorting takes $O(N \log N)$ where $N$ is the number of words.
  - DFS takes $O(L^2)$ per word in the worst case, where $L$ is the length of the word (due to iterating through characters and branching at valid words).
  - Total Time Complexity: $O(N \log N + N \cdot L^2)$.
- **Space Complexity:** $O(N \cdot L)$ to store all words in the Trie, plus $O(L)$ for the recursion stack during DFS.

---

[Previous: Autocomplete](./06-autocomplete.md) | [Next: Maximum XOR](./08-maximum-xor.md)

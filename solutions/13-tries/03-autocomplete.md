# Solutions: Autocomplete & System Design

## 1. Design Search Autocomplete System
(LeetCode 642)

### Problem Statement
Design a search autocomplete system for a search engine. Users may input a sentence (at least one word and end with a special character '#').
For each character they type except '#', you need to return the top 3 historical hot sentences that have a prefix the same as the part of sentence already typed.
The hotness of a sentence is defined by the number of times a user typed the exactly same sentence before.
The returned top 3 hot sentences should be sorted by hotness (descending). If several sentences have the same hotness, use ASCII-code order (ascending).
If less than 3 hot sentences exist, return as many as you can. When the user types '#', it means the sentence is finished, and you should save it.

### Examples & Edge Cases
**Example:**
```
Input:
AutocompleteSystem(["i love you", "island", "iroman", "i love leetcode"], [5, 3, 2, 2])
Input: 'i'
Output: ["i love you", "island", "i love leetcode"]
```

### Optimal Python Solution
```python
import heapq

class AutocompleteSystem:
    def __init__(self, sentences: list[str], times: list[int]):
        self.root = {}
        self.current_input = ""
        # Build Trie with frequencies
        for s, t in zip(sentences, times):
            self._insert(s, t)

    def _insert(self, sentence, count):
        node = self.root
        for char in sentence:
            node = node.setdefault(char, {})
            # Store counts in each node for faster collection
            if 'counts' not in node: node['counts'] = {}
            node['counts'][sentence] = node['counts'].get(sentence, 0) + count

    def input(self, c: str) -> list[str]:
        if c == '#':
            self._insert(self.current_input, 1)
            self.current_input = ""
            return []

        self.current_input += c
        node = self.root
        for char in self.current_input:
            if char not in node:
                return []
            node = node[char]

        # Use a heap to find top 3
        # Sort by (-count, sentence)
        res = []
        counts = node.get('counts', {})
        for sentence, count in counts.items():
            res.append((-count, sentence))

        # Get top 3
        heapq.heapify(res)
        top3 = []
        for _ in range(min(3, len(res))):
            top3.append(heapq.heappop(res)[1])
        return top3
```

### Explanation
1.  **Trie with Frequency Map**: Each node in the Trie stores a dictionary `counts` that maps sentences passing through that node to their frequencies. This avoids DFS during the `input` query.
2.  **Incremental Input**: We maintain `current_input` and traverse the Trie from the root for each character.
3.  **Top-K with Heap**: We use a min-heap (with negated counts for max-heap behavior) to extract the top 3 sentences based on frequency and lexicographical order.

### Complexity Analysis
*   **Time Complexity**:
    - `__init__`: $O(N \times L)$ where $N$ is the number of sentences and $L$ is the average length. Each sentence is inserted into the Trie, taking $O(L)$ time.
    - `input`: $O(L + M \log 3)$ where $L$ is the length of the current input and $M$ is the number of sentences sharing the prefix. We traverse $L$ nodes, then use a heap of size 3 to find the top results from $M$ candidates.
*   **Space Complexity**: $O(N \times L^2)$ in the worst case because each node along a path stores a reference to the full sentence string in its `counts` map.

---

## 2. Top K Frequent Words
(LeetCode 692)

### Problem Statement
Given an array of strings `words` and an integer `k`, return the `k` most frequent strings. Return the answer sorted by the frequency from highest to lowest. Sort the words with the same frequency by their lexicographical order.

### Examples & Edge Cases
**Example:**
```
Input: words = ["i","love","leetcode","i","love","coding"], k = 2
Output: ["i","love"]
```

### Optimal Python Solution
```python
from collections import Counter
import heapq

class Word:
    def __init__(self, word, count):
        self.word = word
        self.count = count

    def __lt__(self, other):
        # Min-heap needs custom comparator:
        # Smaller count is "less"
        # For same count, lexicographically LARGER is "less" (so it stays at top of min-heap to be popped)
        if self.count == other.count:
            return self.word > other.word
        return self.count < other.count

class Solution:
    def topKFrequent(self, words: list[str], k: int) -> list[str]:
        counts = Counter(words)
        heap = []

        for word, count in counts.items():
            heapq.heappush(heap, Word(word, count))
            if len(heap) > k:
                heapq.heappop(heap)

        res = []
        while heap:
            res.append(heapq.heappop(heap).word)
        return res[::-1]
```

### Explanation
1.  **Counter**: First, count frequencies using a hashmap.
2.  **Min-Heap of size K**: To find the Top-K elements, a min-heap is more efficient than sorting.
3.  **Custom Comparator**: We need to handle the tie-break (lexicographical order) correctly within the heap.

### Complexity Analysis
*   **Time Complexity**: $O(N \log K)$ where $N$ is the number of words and $K$ is the number of top elements requested. Building the frequency map takes $O(N)$, and maintaining a min-heap of size $K$ for each unique word takes $O(\text{unique words} \times \log K)$.
*   **Space Complexity**: $O(N)$ to store the frequency counts for all words in the input.

---

## 3. Search Suggestions System
(LeetCode 1268)

### Problem Statement
Given an array of strings `products` and a string `searchWord`. Design a system that suggests at most three product names from `products` after each character of `searchWord` is typed. Suggested products should have a common prefix with `searchWord`. If there are more than three products with a common prefix, return the three lexicographically minimums.

### Examples & Edge Cases
**Example:**
```
Input: products = ["mobile","mouse","moneypot","monitor","mousepad"], searchWord = "mouse"
Output: [["mobile","moneypot","monitor"],["mobile","moneypot","monitor"],["mouse","mousepad"],["mouse","mousepad"],["mouse","mousepad"]]
```

### Optimal Python Solution
```python
class Solution:
    def suggestedProducts(self, products: list[str], searchWord: str) -> list[list[str]]:
        products.sort() # Sorting handles lexicographical requirement
        res = []
        left, right = 0, len(products) - 1

        for i in range(len(searchWord)):
            char = searchWord[i]

            # Narrow the window [left, right] to words matching the prefix
            while left <= right and (len(products[left]) <= i or products[left][i] != char):
                left += 1
            while left <= right and (len(products[right]) <= i or products[right][i] != char):
                right -= 1

            # Pick top 3 from the valid window
            suggestions = []
            for j in range(left, min(left + 3, right + 1)):
                suggestions.append(products[j])
            res.append(suggestions)

        return res
```

### Explanation
1.  **Two Pointers on Sorted Array**: While a Trie is a valid solution, two pointers on a sorted array is often more space-efficient and simpler to implement.
2.  **Shrinking Window**: As we type more characters, the range of valid products in the sorted list can only shrink. We move `left` and `right` pointers to maintain the prefix invariant.

### Complexity Analysis
*   **Time Complexity**: $O(N \log N \cdot L + W)$ where $N$ is the number of products, $L$ is the average length, and $W$ is the length of `searchWord`. Sorting takes $O(N \log N \cdot L)$, and for each of the $W$ characters, we narrow our window in $O(1)$ constant time amortized across all characters.
*   **Space Complexity**: $O(1)$ extra space if we don't count the output list, as we modify the pointers in place on the sorted product list.

---

## 4. Implement Trie II (Prefix Tree)
(LeetCode 1804)

### Problem Statement
Implement a Trie which supports `countWordsEqualTo`, `countWordsStartingWith`, and `erase` operations.

### Optimal Python Solution
```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.count_end = 0     # Words ending at this node
        self.count_prefix = 0  # Words passing through this node

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        node = self.root
        for char in word:
            node = node.children.setdefault(char, TrieNode())
            node.count_prefix += 1
        node.count_end += 1

    def countWordsEqualTo(self, word: str) -> int:
        node = self._find(word)
        return node.count_end if node else 0

    def countWordsStartingWith(self, prefix: str) -> int:
        node = self._find(prefix)
        return node.count_prefix if node else 0

    def erase(self, word: str) -> None:
        node = self.root
        for char in word:
            node = node.children[char]
            node.count_prefix -= 1
        node.count_end -= 1

    def _find(self, s):
        node = self.root
        for char in s:
            if char not in node.children: return None
            node = node.children[char]
        return node
```

### Explanation
1.  **Frequency Tracking**: We add two counters to each node: `count_end` (for exact matches) and `count_prefix` (for prefix matches).
2.  **Efficient Erase**: Because we track prefix counts, `erase` is simply a traversal where we decrement the counts.

### Complexity Analysis
*   **Time Complexity**: $O(L)$ for all operations (insert, count, erase), where $L$ is the length of the string. We traverse the Trie exactly once for each operation, performing $O(1)$ constant-time updates at each node.
*   **Space Complexity**: $O(N \times L)$ for storing all words in the Trie.

---

## 5. Design File System
(LeetCode 1166)

### Problem Statement
Design a file system that allows you to create new paths and associate them with different values.
- `createPath(path, value)`: Creates a new path and returns `True`. If the path already exists or its parent does not exist, return `False`.
- `get(path)`: Returns the value associated with the path or `-1` if the path doesn't exist.

### Optimal Python Solution
```python
class FileNode:
    def __init__(self, value=-1):
        self.children = {}
        self.value = value

class FileSystem:
    def __init__(self):
        self.root = FileNode()

    def createPath(self, path: str, value: int) -> bool:
        parts = path.split("/") # path starts with /, so parts[0] is empty
        node = self.root

        # Traverse to the parent
        for i in range(1, len(parts) - 1):
            if parts[i] not in node.children:
                return False
            node = node.children[parts[i]]

        # Check if the child already exists
        last_part = parts[-1]
        if last_part in node.children:
            return False

        node.children[last_part] = FileNode(value)
        return True

    def get(self, path: str) -> int:
        parts = path.split("/")
        node = self.root
        for i in range(1, len(parts)):
            if parts[i] not in node.children:
                return -1
            node = node.children[parts[i]]
        return node.value
```

### Explanation
1.  **Trie as a Tree**: File systems are naturally hierarchical. Each segment of the path is a node in the Trie.
2.  **Parent Validation**: During `createPath`, we ensure every intermediate directory (parent) exists before adding the leaf node.

### Complexity Analysis
*   **Time Complexity**: $O(L)$ for both `createPath` and `get`, where $L$ is the length of the path. Splitting the path and traversing the nodes both scale linearly with the number of characters/segments in the path.
*   **Space Complexity**: $O(T)$ where $T$ is the total length of all paths created, as we store each unique segment as a node in the tree.

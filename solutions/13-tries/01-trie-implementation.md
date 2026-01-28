# Solutions: Trie Implementation

## 1. Implement Trie (Prefix Tree)
(LeetCode 208)

### Problem Statement
A **Trie** (pronounced as "try") or **prefix tree** is a tree data structure used to efficiently store and retrieve keys in a dataset of strings. There are various applications of this data structure, such as autocomplete and spellcheckers.

Implement the `Trie` class:
*   `Trie()` Initializes the trie object.
*   `void insert(String word)` Inserts the string `word` into the trie.
*   `boolean search(String word)` Returns `true` if the string `word` is in the trie (i.e., was inserted before), and `false` otherwise.
*   `boolean startsWith(String prefix)` Returns `true` if there is a previously inserted string `word` that has the prefix `prefix`, and `false` otherwise.

### Examples & Edge Cases
**Example:**
```
Input:
["Trie", "insert", "search", "search", "startsWith", "insert", "search"]
[[], ["apple"], ["apple"], ["app"], ["app"], ["app"], ["app"]]

Output:
[null, null, true, false, true, null, true]
```

**Edge Cases:**
*   **Prefix vs. Full Word**: Searching for "app" after inserting "apple" should return `False` for `search` but `True` for `startsWith`.
*   **Empty String**: If allowed, it marks the root's `is_end`.
*   **Case Sensitivity**: Usually lowercase English letters, but Tries can be adapted for any character set.

### Optimal Python Solution
```python
class TrieNode:
    def __init__(self):
        # Using a hashmap for flexible character sets
        self.children = {}
        self.is_end = False

class Trie:
    def __init__(self):
        """Initialize the trie with an empty root node."""
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        """Insert a word into the trie by creating nodes for each character."""
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True

    def search(self, word: str) -> bool:
        """Return True if the word exists in the trie and is marked as an end."""
        node = self._find(word)
        return node is not None and node.is_end

    def startsWith(self, prefix: str) -> bool:
        """Return True if any word in the trie starts with the given prefix."""
        return self._find(prefix) is not None

    def _find(self, prefix: str) -> TrieNode:
        """Helper to navigate the trie and return the node at the end of the path."""
        node = self.root
        for char in prefix:
            if char not in node.children:
                return None
            node = node.children[char]
        return node
```

### Explanation
1.  **Node Structure**: Each node contains a map of its children and a boolean flag `is_end`.
2.  **Insertion**: We walk down the tree, creating nodes for characters that don't yet exist. Finally, we mark `is_end = True`.
3.  **Search vs. Prefix**: Both involve walking down the tree. `search` requires that the final node has `is_end` set to `True`, while `startsWith` only requires that the path exists.

### Complexity Analysis
*   **Time Complexity**: $O(L)$ for all operations (insert, search, startsWith), where $L$ is the length of the string. We perform one lookup or insertion for each character in the string. Since hash map operations (for child nodes) are $O(1)$ on average, the total time is proportional only to the word length $L$.
*   **Space Complexity**: $O(N \times L)$ where $N$ is the number of words and $L$ is the average length. In the worst case (no shared prefixes), we store every character as a separate node. However, the true strength of a Trie is that it reduces space for shared prefixes.

---

## 2. Replace Words
(LeetCode 648)

### Problem Statement
In English, we have a concept called **root**, which can be followed by some other word to form another longer word - let's call this word **derivative**. For example, when the root "help" is followed by the word "ful", the derivative "helpful" is formed.

Given a dictionary consisting of many roots and a sentence consisting of words separated by spaces, replace all the derivatives in the sentence with the root forming it. If a derivative can be replaced by more than one root, replace it with the root that has the shortest length.

### Examples & Edge Cases
**Example:**
```
Input: dictionary = ["cat","bat","rat"], sentence = "the cattle was rattled by the battery"
Output: "the cat was rat by the bat"
```

**Edge Cases:**
*   **Multiple Roots**: Use the shortest root (e.g., "a" and "app" both match "apple", use "a").
*   **No Match**: Keep the original word.

### Optimal Python Solution
```python
class Solution:
    def replaceWords(self, dictionary: list[str], sentence: str) -> str:
        # Build a Trie from the dictionary
        root = {}
        for word in dictionary:
            node = root
            for char in word:
                if char not in node:
                    node[char] = {}
                node = node[char]
            node['#'] = word # Store the root at the end node

        def find_root(word):
            node = root
            for char in word:
                if char not in node:
                    break
                node = node[char]
                if '#' in node: # Found the shortest root
                    return node['#']
            return word # No root found

        # Process each word in the sentence
        words = sentence.split()
        return " ".join(find_root(w) for w in words)
```

### Explanation
1.  **Trie for Prefix Search**: We store all roots in a Trie.
2.  **Shortest Root Property**: By returning as soon as we hit an `is_end` (marker `#` in this case), we ensure we pick the shortest root.
3.  **Sentence Processing**: We split the sentence, find the root for each word using the Trie, and join them back.

### Complexity Analysis
*   **Time Complexity**: $O(D \times L + S \times L)$ where $D$ is the number of roots, $S$ is the number of words in the sentence, and $L$ is the average length. Building the Trie takes $O(D \times L)$ as we process each character of each root. Searching for each word in the sentence takes $O(L)$ as we traverse the Trie until we find a root or mismatch.
*   **Space Complexity**: $O(D \times L)$ to store the dictionary in the Trie.

---

## 3. Map Sum Pairs
(LeetCode 677)

### Problem Statement
Design a map that allows you to do the following:
*   Maps a string key to a given value.
*   Returns the sum of the values of all keys that have a given prefix.

### Examples & Edge Cases
**Example:**
```
Input:
["MapSum", "insert", "sum", "insert", "sum"]
[[], ["apple", 3], ["ap"], ["app", 2], ["ap"]]
Output:
[null, null, 3, null, 5]
```

### Optimal Python Solution
```python
class MapSum:
    def __init__(self):
        self.root = {}
        self.values = {} # key -> value mapping to handle updates

    def insert(self, key: str, val: int) -> None:
        # Calculate delta if key already exists
        delta = val - self.values.get(key, 0)
        self.values[key] = val

        node = self.root
        for char in key:
            if char not in node:
                node[char] = {'sum': 0}
            node = node[char]
            node['sum'] += delta # Update sum along the path

    def sum(self, prefix: str) -> int:
        node = self.root
        for char in prefix:
            if char not in node:
                return 0
            node = node[char]
        return node['sum']
```

### Explanation
1.  **Prefix Sum on Path**: Instead of calculating the sum by traversing the subtree during the `sum` query, we store and update the prefix sum at every node during `insert`.
2.  **Handling Updates**: We maintain a `values` map to know if a key is being overwritten, allowing us to calculate the `delta` to adjust existing prefix sums.

### Complexity Analysis
*   **Time Complexity**: $O(L)$ for both `insert` and `sum`. In `insert`, we traverse the length of the key once to update the path sums. In `sum`, we traverse the length of the prefix once to reach the node containing the pre-calculated sum.
*   **Space Complexity**: $O(N \times L)$ to store keys and sums in the Trie nodes.

---

## 4. Longest Word in Dictionary
(LeetCode 720)

### Problem Statement
Given an array of strings `words`, return the longest word in `words` such that every character of it can be built one character at a time by other words in `words`. If there is more than one possible answer, return the longest word with the smallest lexicographical order. If there is no answer, return the empty string.

### Examples & Edge Cases
**Example:**
```
Input: words = ["w","wo","wor","worl","world"]
Output: "world"
```

### Optimal Python Solution
```python
class Solution:
    def longestWord(self, words: list[str]) -> str:
        # Build Trie
        trie = {}
        for word in words:
            node = trie
            for char in word:
                node = node.setdefault(char, {})
            node['$'] = True # Mark end of word

        ans = ""
        # DFS to find longest word built character by character
        def dfs(node, path):
            nonlocal ans
            # Only continue if current path is a valid word (except root)
            if len(path) > len(ans) or (len(path) == len(ans) and "".join(path) < ans):
                ans = "".join(path)

            for char in sorted(node.keys()):
                if char != '$' and '$' in node[char]:
                    path.append(char)
                    dfs(node[char], path)
                    path.pop()

        dfs(trie, [])
        return ans
```

### Explanation
1.  **Trie Construction**: Insert all words.
2.  **DFS with Word Check**: We perform a DFS from the root. A path is only valid if every node on that path (except the root) marks the end of some word in the input.
3.  **Tie-breaking**: We track the longest word and use lexicographical order for same-length ties.

### Complexity Analysis
*   **Time Complexity**: $O(\sum L_i)$ where $L_i$ is the length of the $i$-th word. We process each character of every word once during Trie construction and visit each node at most once during the DFS traversal. Sorting children takes $O(26 \log 26)$ which is constant.
*   **Space Complexity**: $O(\sum L_i)$ to store the Trie and the recursion stack ($O(L_{max})$).

---

## 5. Search Suggestions System
(LeetCode 1268)

### Problem Statement
You are given an array of strings `products` and a string `searchWord`. Design a system that suggests at most three product names from `products` after each character of `searchWord` is typed. Suggested products should have a common prefix with `searchWord`. If there are more than three products with a common prefix, return the three lexicographically minimums.

### Examples & Edge Cases
**Example:**
```
Input: products = ["mobile","mouse","moneypot","monitor","mousepad"], searchWord = "mouse"
Output: [
  ["mobile","moneypot","monitor"],
  ["mobile","moneypot","monitor"],
  ["mouse","mousepad"],
  ["mouse","mousepad"],
  ["mouse","mousepad"]
]
```

### Optimal Python Solution
```python
class Solution:
    def suggestedProducts(self, products: list[str], searchWord: str) -> list[list[str]]:
        # Pre-sort products to easily pick the smallest three
        products.sort()

        # Build Trie and store indices of products passing through each node
        trie = {}
        for i, word in enumerate(products):
            node = trie
            for char in word:
                node = node.setdefault(char, {})
                if 'suggestions' not in node:
                    node['suggestions'] = []
                if len(node['suggestions']) < 3:
                    node['suggestions'].append(word)

        result = []
        node = trie
        for char in searchWord:
            if node is not None and char in node:
                node = node[char]
                result.append(node['suggestions'])
            else:
                node = None
                result.append([])
        return result
```

### Explanation
1.  **Sorting**: Sorting products first allows us to greedily pick the first 3 words encountered for each prefix node.
2.  **Trie with Cache**: At each node, we store a list of up to 3 suggestions. This makes the query phase very efficient.
3.  **Incremental Search**: As we iterate through `searchWord`, we just follow the Trie and return the cached suggestions.

### Complexity Analysis
*   **Time Complexity**: $O(P \log P \cdot L + P \times L + W)$ where $P$ is the number of products, $L$ is the average length, and $W$ is the length of `searchWord`. Sorting products takes $O(P \log P \cdot L)$, building the Trie takes $O(P \times L)$, and searching takes $O(W)$.
*   **Space Complexity**: $O(P \times L)$ for Trie and storing up to 3 suggestions at each node.

---

## 6. Implement Magic Dictionary
(LeetCode 676)

### Problem Statement
Design a data structure that is initialized with a list of different words. Given a string, you should determine if you can change exactly one character in this string to match any word in the data structure.

### Examples & Edge Cases
**Example:**
```
Input: ["MagicDictionary", "buildDict", "search"]
[[], [["hello", "leetcode"]], ["hello"]]
Output: [null, null, false]
# Changing one char in "hello" to match "hello" is not allowed.
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
            if char in node:
                # Case 1: Match the current character (no modification yet or already modified)
                if dfs(node[char], i + 1, modified):
                    return True

            if not modified:
                # Case 2: Try modifying the current character to any other child
                for other_char in node:
                    if other_char != char and other_char != '$':
                        if dfs(node[other_char], i + 1, True):
                            return True
            return False

        return dfs(self.root, 0, False)
```

### Explanation
1.  **Trie Storage**: Store the dictionary in a standard Trie.
2.  **DFS with state**: The `search` function uses DFS with a `modified` boolean flag.
3.  **Branching**: At each character, we can either:
    - Match it (and keep the `modified` status).
    - If not already modified, replace it with any other available character at this Trie level and set `modified = True`.

### Complexity Analysis
*   **Time Complexity**: $O(\sum L_i)$ for building the Trie. For searching, the worst case is $O(L \times 26)$ where $L$ is the length of `searchWord`. For each character position, we might explore all 26 possible substitutions, but we only do this once (due to the `modified` flag).
*   **Space Complexity**: $O(\sum L_i)$ to store the dictionary in the Trie.

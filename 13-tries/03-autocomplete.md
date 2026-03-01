# Design Autocomplete System

> **Prerequisites:** [Trie Implementation](./01-trie-implementation.md), [Heaps](../07-heaps-priority-queues/README.md), [System Design Basics](../17-system-design-basics/README.md)

## Interview Context

Design Search Autocomplete System (LeetCode 642) is a classic problem that appears in both coding interviews and system design rounds. It tests trie knowledge, sorting, and the ability to design APIs. At Google and Meta, this is particularly common given their search products.

---

## Time Complexity Quick Reference

| Approach | Initialization | `input(c)` | Query Time (Best Case) | Query Time (Worst Case) | Space Complexity |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Basic (Terminal Only)** | $O(N \cdot L)$ | $O(p + M \cdot L + M \log M)$ | $O(L)$ (No matches) | $O(M \cdot L + M \log M)$ | $O(\text{total chars})$ |
| **Optimized (Heap/Top-K)** | $O(N \cdot L)$ | $O(p + M \cdot L + M \log K)$ | $O(L)$ (No matches) | $O(M \cdot L + M \log K)$ | $O(\text{total chars})$ |
| **Production-Ready** | $O(N \cdot L \cdot K \log K)$ | $O(K \log K)$ or $O(1)$ | $O(1)$ (Cached Top-K) | $O(1)$ (Cached Top-K) | $O(\text{total chars} + \text{nodes} \cdot K)$ |

*Where $N$ = sentences, $L$ = avg length, $M$ = matches, $K$ = top-k (3 here), $p$ = prefix length.*

---

## Building Intuition

**The Core Problem: Speed vs Relevance**

When you type "app" in a search box, you want suggestions INSTANTLY—under 100ms. But you also want the BEST suggestions (most popular, most relevant). These goals conflict:

```
Speed:     Just return first 3 words starting with "app"
Relevance: Score all 10,000 matching words, sort, return top 3

The challenge: How do we get BOTH speed AND relevance?
```

**Why Tries are Perfect for "Typeahead"**

Each keystroke is an incremental query. You don't search from scratch each time:

```
User types: "a" → "ap" → "app"

Naive approach:
  "a":   Scan all words for 'a' prefix
  "ap":  Scan all words for 'ap' prefix  (wasteful!)
  "app": Scan all words for 'app' prefix (wasteful!)

Trie approach:
  "a":   Move to child 'a' of root, collect results from subtree
  "ap":  Move to child 'p' of current node (already at 'a')
  "app": Move to child 'p' of current node (already at 'ap')

You're EXTENDING your position, not starting over!
```

**The Trade-off Triangle**

```
                    SPEED
                      ↑
                     / \
                    /   \
                   /     \
            MEMORY ←------→ FRESHNESS

Pre-compute everything → Fast queries, lots of memory, stale data
Compute on-demand     → Slow queries, less memory, fresh data
Hybrid (trie + cache) → Balanced trade-off
```

**Three Design Levels**

1. **Terminal Storage Only**: Store sentence + frequency at end of word
   - Query: O(L + m log m) where L = prefix, m = matches
   - Space: O(total characters)

2. **Path Storage**: Store sentences at EVERY node along path
   - Query: O(k log k) just sort top-k at current node
   - Space: O(total chars × average word length)—much more!

3. **Pre-computed Top-K**: Store sorted top-k at each node
   - Query: O(1)—just return cached list
   - Space: O(nodes × k)
   - Downside: Updates are expensive (must update entire path)

**Frequency as Priority**

The heap insight: you don't need to sort ALL matches. You only need top-3:

```python
# Don't do this (sorts everything):
all_matches = collect_all(node)
all_matches.sort(key=lambda x: -x.freq)
return all_matches[:3]

# Do this (stops after 3):
heap = []  # Min-heap of size 3
for match in collect_all(node):
    if len(heap) < 3:
        heappush(heap, match)
    elif match.freq > heap[0].freq:
        heapreplace(heap, match)
return sorted(heap, reverse=True)
```

For 100,000 matches, sorting is O(100,000 log 100,000). Heap is O(100,000 log 3).

---

## When NOT to Use This Pattern

**1. Static, Small Datasets**

If you have 100 sentences that never change, a sorted list with binary search is simpler:

```python
sentences.sort()
# For prefix "app", binary search to find range, return first 3
```

Trie overhead isn't justified.

**2. Full-Text Search (Not Just Prefix)**

Autocomplete is PREFIX matching. If you need:

- "Find sentences containing 'apple'" (not just starting with)
- Fuzzy matching ("aple" → "apple")
- Synonym matching ("car" → also show "automobile")

...then you need an inverted index, not a trie.

**3. Highly Personalized Results**

If suggestions depend heavily on user history, location, time of day, etc., you can't pre-compute effectively. ML-based ranking with a candidate retrieval step is more appropriate.

**4. Rapidly Changing Data**

If sentences and frequencies change every second, maintaining trie consistency becomes expensive. Consider:

- Streaming updates with eventual consistency
- Separate hot/cold trie paths

**Red Flags:**

- "Search by keyword anywhere in text" → Inverted index
- "Correct typos in query" → Edit distance / fuzzy matching
- "Personalized per user" → User-specific tries or ML ranking
- "Real-time trending" → Streaming architecture needed

---

## Problem Statement

Design a search autocomplete system that:

1. Provides suggestions as user types each character
2. Returns top 3 hot sentences that start with the user's input
3. Records new sentences when user presses '#'

```
AutocompleteSystem(["i love you", "island", "iroman", "i love leetcode"], [5, 3, 2, 2])

Input: 'i'
Output: ["i love you", "island", "i love leetcode"]
(sorted by frequency, then alphabetically)

Input: ' '  (space, continuing "i ")
Output: ["i love you", "i love leetcode"]

Input: 'a'  (now "i a")
Output: []

Input: '#'  (end of sentence "i a")
Output: []
Records "i a" with frequency 1
```

---

## Pattern: Trie + Priority Queue

### High-Level Design

```
Components:
1. Trie: Store sentences with their frequencies
2. Heap: Get top-k results
3. Current Input Tracking: Track user's current prefix

Data Flow:
User types 'i' → Find trie node for 'i' → Collect all sentences under node
                 → Sort by (-frequency, sentence) → Return top 3
```

### Visualization

```
Sentences: ["i love you"(5), "island"(3), "iroman"(2), "i love leetcode"(2)]

Trie structure (simplified, showing end nodes):
        root
         |
         i
       / | \
      l  s   r
     /   |    \
   " " land*  oman*
    |
   ...
   |
  you* / leetcode*

At 'i' node: collect all sentences, sort, return top 3
```

---

## Implementation

### Solution with Trie + Sorting

```python
class AutocompleteSystem:
    """
    Autocomplete system using trie for prefix lookup.

    Time:
    - __init__: O(n × L) where n = sentences, L = avg length
    - input: O(p + m × L + m log m) where p = prefix length, m = matches

    Space: O(total characters in sentences)
    """

    def __init__(self, sentences: list[str], times: list[int]):
        self.root = {}
        self.current_node = self.root
        self.current_input = []
        self.dead_node = {}  # Empty node for no matches

        # Build trie with frequencies
        for sentence, count in zip(sentences, times):
            self._insert(sentence, count)

    def _insert(self, sentence: str, count: int) -> None:
        """Insert sentence with frequency count."""
        node = self.root
        for char in sentence:
            if char not in node:
                node[char] = {}
            node = node[char]
        # Store frequency at terminal, '#' is reserved for sentence data
        node['#'] = node.get('#', 0) + count
        node['$'] = sentence  # Store complete sentence

    def input(self, c: str) -> list[str]:
        """Process one character of input."""
        if c == '#':
            # End of sentence - record it
            sentence = ''.join(self.current_input)
            self._insert(sentence, 1)
            # Reset state
            self.current_input = []
            self.current_node = self.root
            return []

        # Add to current input
        self.current_input.append(c)

        # Navigate trie
        if self.current_node is self.dead_node:
            return []

        if c not in self.current_node:
            self.current_node = self.dead_node
            return []

        self.current_node = self.current_node[c]

        # Collect all sentences from current node
        sentences = []
        self._collect(self.current_node, sentences)

        # Sort by (-frequency, sentence) and return top 3
        sentences.sort(key=lambda x: (-x[0], x[1]))
        return [s[1] for s in sentences[:3]]

    def _collect(self, node: dict, result: list) -> None:
        """DFS to collect all (frequency, sentence) pairs from node."""
        if '#' in node:
            result.append((node['#'], node['$']))

        for char, child in node.items():
            if char not in ['#', '$']:
                self._collect(child, result)
```

### Optimized with Heap (Top-K)

```python
import heapq

class TrieItem:
    def __init__(self, freq: int, sentence: str):
        self.freq = freq
        self.sentence = sentence

    def __lt__(self, other):
        # Min-heap logic for top-k elements.
        # We want to keep the elements with MAX frequency and MIN lexicographical string.
        # Therefore, the min-heap should pop (discard) the worst items first:
        # elements with MIN frequency, and if frequencies tie, MAX lexicographical string.
        if self.freq == other.freq:
            # Pop the larger string (descending ASCII order)
            return self.sentence > other.sentence
        # Pop the smaller frequency first
        return self.freq < other.freq

class AutocompleteSystemHeap:
    """Optimized with heap for top-k retrieval."""

    def __init__(self, sentences: list[str], times: list[int]):
        self.root = {}
        self.current_node = self.root
        self.current_input = []

        for sentence, count in zip(sentences, times):
            self._insert(sentence, count)

    def _insert(self, sentence: str, count: int) -> None:
        node = self.root
        for char in sentence:
            if char not in node:
                node[char] = {}
            node = node[char]
        node['freq'] = node.get('freq', 0) + count
        node['sentence'] = sentence

    def input(self, c: str) -> list[str]:
        if c == '#':
            sentence = ''.join(self.current_input)
            self._insert(sentence, 1)
            self.current_input = []
            self.current_node = self.root
            return []

        self.current_input.append(c)

        if self.current_node is None or c not in self.current_node:
            self.current_node = None
            return []

        self.current_node = self.current_node[c]

        # Use heap for top 3
        heap: list[TrieItem] = []  # Min heap of TrieItem
        self._collect_topk(self.current_node, heap, 3)

        # Extract results (heap gives min first, need to reverse)
        result = []
        while heap:
            item = heapq.heappop(heap)
            result.append(item.sentence)
        return result[::-1]

    def _collect_topk(self, node: dict, heap: list[TrieItem], k: int) -> None:
        """Collect top k using min heap."""
        if 'freq' in node:
            item = TrieItem(node['freq'], node['sentence'])
            if len(heap) < k:
                heapq.heappush(heap, item)
            else:
                heapq.heappushpop(heap, item)

        for char, child in node.items():
            if char not in ['freq', 'sentence']:
                self._collect_topk(child, heap, k)
```

### Production-Ready Version

```python
from collections import defaultdict
import heapq
from typing import List

class TrieNode:
    def __init__(self):
        self.children: dict[str, 'TrieNode'] = defaultdict(TrieNode)
        # Pre-compute top 3 items as (frequency, sentence) pairs.
        self.top3: List[tuple[int, str]] = []


class AutocompleteSystem:
    """
    Production-ready autocomplete with truly pre-computed suggestions.

    Optimization: Maintain only the top 3 sentences at each node DURING insertion.
    Trade-off: Slightly more insertion cost, but true O(1) queries.
    """

    def __init__(self, sentences: List[str], times: List[int]):
        self.root = TrieNode()
        self.current_node: 'TrieNode' | None = self.root
        self.current_input: List[str] = []
        # Track total counts for exact updates
        self.sentence_counts: dict[str, int] = defaultdict(int)

        for sentence, count in zip(sentences, times):
            self.sentence_counts[sentence] += count

        for sentence, _ in zip(sentences, times):
            self._insert_path(sentence)

    def _insert_path(self, sentence: str) -> None:
        """Updates the trie path for the given sentence and its current count."""
        count = self.sentence_counts[sentence]
        node = self.root

        # Update root
        self._update_top3(node, sentence, count)

        # Update children along the path
        for char in sentence:
            node = node.children[char]
            self._update_top3(node, sentence, count)

    def _update_top3(self, node: TrieNode, sentence: str, count: int) -> None:
        """Helper to maintain only the top 3 (freq, sentence) pairs at a node."""
        # Check if the sentence is already in the top 3
        found_idx = -1
        for i, (c, s) in enumerate(node.top3):
            if s == sentence:
                found_idx = i
                break

        if found_idx != -1:
            # Update existing count
            node.top3[found_idx] = (count, sentence)
        else:
            # Add new candidate
            node.top3.append((count, sentence))

        # Sort descending by count, ascending by ASCII (sentence)
        node.top3.sort(key=lambda x: (-x[0], x[1]))

        # Enforce the top 3 limit
        if len(node.top3) > 3:
            node.top3.pop()

    def input(self, c: str) -> List[str]:
        if c == '#':
            sentence = ''.join(self.current_input)
            self.sentence_counts[sentence] += 1
            self._insert_path(sentence)

            self.current_input = []
            self.current_node = self.root
            return []

        self.current_input.append(c)

        if not self.current_node or c not in self.current_node.children:
            self.current_node = None
            return []

        self.current_node = self.current_node.children[c]

        # O(1) query! We already pre-computed the top 3 items
        return [s for _, s in self.current_node.top3]
```

---

## Complexity Analysis

| Operation        | Basic Approach     | Optimized (Heap)   | Pre-computed                              |
| ---------------- | ------------------ | ------------------ | ----------------------------------------- |
| Init             | O(n × L)           | O(n × L)           | O(n × L × L)                              |
| Input (per char) | O(m × L + m log m) | O(m × L + m log k) | O(k log k)                                |
| Space            | O(total chars)     | O(total chars)     | O(total chars × avg sentences per prefix) |

Where:

- n = number of sentences
- L = average sentence length
- m = matching sentences
- k = top-k (3 in this problem)

---

## Design Decisions

### What to Store at Each Node?

| Approach      | Store at Node         | Pros            | Cons                     |
| ------------- | --------------------- | --------------- | ------------------------ |
| Terminal only | sentence, freq at end | Less memory     | Must traverse to collect |
| Each node     | sentence map          | O(1) per prefix | More memory              |
| Pre-computed  | top-k sentences       | Fastest query   | Most memory, update cost |

### Handling Ties

```python
# LeetCode requirements: sort by frequency (desc), then alphabetically (asc)
sentences.sort(key=lambda x: (-x.freq, x.sentence))
```

### Real-World Considerations

```
1. Personalization: Weight user's history higher
2. Recency: Recent queries weighted higher
3. Trending: Boost globally popular queries
4. Diversity: Don't show too-similar suggestions
5. Filtering: Remove inappropriate suggestions
```

---

## Common Variations

### Top K Frequent Words (LeetCode 692)

```python
from collections import Counter
import heapq
from typing import List

class WordFreq:
    def __init__(self, freq: int, word: str):
        self.freq = freq
        self.word = word

    def __lt__(self, other):
        # We want to KEEP max freq and min lexicographical.
        # So we POP min freq and max lexicographical.
        if self.freq == other.freq:
            return self.word > other.word
        return self.freq < other.freq

class Solution:
    def topKFrequent(self, words: List[str], k: int) -> List[str]:
        """Return k most frequent words."""
        count = Counter(words)
        heap: List[WordFreq] = []

        for word, freq in count.items():
            item = WordFreq(freq, word)
            if len(heap) < k:
                heapq.heappush(heap, item)
            else:
                heapq.heappushpop(heap, item)

        result = []
        while heap:
            result.append(heapq.heappop(heap).word)
        # Reverse to get decreasing frequency / increasing lexicographical
        return result[::-1]
```

### Search Suggestions System (LeetCode 1268)

```python
import bisect
from typing import List

class Solution:
    def suggestedProducts(self, products: List[str], searchWord: str) -> List[List[str]]:
        """
        Return 3 lexicographically smallest products for each prefix.

        Approach: Sort products, binary search for prefix.
        """
        products.sort()
        result = []
        prefix = ""
        start = 0

        for char in searchWord:
            prefix += char
            # Binary search for first product >= prefix
            start = bisect.bisect_left(products, prefix, start)

            # Collect up to 3 products starting with prefix
            suggestions = []
            for i in range(start, min(start + 3, len(products))):
                if products[i].startswith(prefix):
                    suggestions.append(products[i])
                else:
                    break
            result.append(suggestions)

        return result
```

### With Edit Distance (Fuzzy Matching)

```python
from typing import List

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False
        self.word = ""

class Solution:
    def __init__(self):
        self.root = TrieNode()

    def fuzzy_autocomplete(self, prefix: str, max_distance: int = 1) -> List[str]:
        """
        Return suggestions within edit distance of prefix.
        Used for typo tolerance.
        """
        results = []

        def dfs(node: TrieNode, remaining: str, edits: int) -> None:
            if edits > max_distance:
                return

            if not remaining:
                # Prefix consumed, collect all words from this subtree
                self._collect_words(node, results)
                return

            char = remaining[0]
            rest = remaining[1:]

            for next_char, child in node.children.items():
                if next_char == char:
                    # Exact match
                    dfs(child, rest, edits)
                else:
                    # Substitution
                    dfs(child, rest, edits + 1)

            # Insertion (skip char in prefix, try same node with shorter prefix)
            dfs(node, rest, edits + 1)

            # Deletion (skip char in trie, move to child but keep full prefix)
            for child in node.children.values():
                dfs(child, remaining, edits + 1)

        dfs(self.root, prefix, 0)
        return results

    def _collect_words(self, node: TrieNode, results: List[str]) -> None:
        """Helper to collect all terminal words under a node."""
        if node.is_end:
            results.append(node.word)
        for child in node.children.values():
            self._collect_words(child, results)
```

---

## Edge Cases

1. **Empty input**: Return all top 3 sentences
2. **No matches**: Return empty list
3. **Fewer than 3 matches**: Return all that match
4. **Same frequency**: Sort alphabetically
5. **Special characters**: Handle spaces, punctuation
6. **Very long input**: Consider max length limits
7. **High frequency updates**: Consider write optimization

---

## Interview Tips

1. **Clarify requirements**: How many suggestions? Sorting criteria?
2. **Start simple**: Basic trie + DFS collection first
3. **Identify bottleneck**: Collection and sorting for each character
4. **Optimize incrementally**: Add heap, then pre-computation
5. **Discuss trade-offs**: Memory vs query time
6. **Scale considerations**: Distributed trie, caching, sharding

---

## System Design Extensions

For system design interviews, extend the solution:

```
1. Scale: Shard trie by first character(s)
2. Caching: Cache popular prefixes (1-3 chars)
3. Real-time: Stream processing for frequency updates
4. Personalization: User-specific tries or boosting
5. A/B testing: Track click-through rates
6. Privacy: Aggregate queries, don't store individual
```

---

## Practice Problems

| #   | Problem                           | Difficulty | Key Concept              |
| --- | --------------------------------- | ---------- | ------------------------ |
| 1   | Design Search Autocomplete System | Hard       | Trie + frequency sorting |
| 2   | Top K Frequent Words              | Medium     | Heap + frequency         |
| 3   | Search Suggestions System         | Medium     | Trie or binary search    |
| 4   | Implement Trie II                 | Medium     | Trie with counts         |
| 5   | Design File System                | Medium     | Trie for paths           |

---

## Related Sections

- [Trie Implementation](./01-trie-implementation.md) - Basic trie operations
- [Heaps & Priority Queues](../07-heaps-priority-queues/README.md) - Top-K patterns
- [System Design Basics](../17-system-design-basics/README.md) - Scaling considerations

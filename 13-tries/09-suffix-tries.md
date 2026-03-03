# Suffix Tries

[Previous: Maximum XOR](./08-maximum-xor.md) | [Back to Chapter](./README.md)

> **Prerequisites:** [Trie Implementation](./01-trie-implementation.md)

## Quick Reference

| Operation | Complexity | Explanation |
| :--- | :--- | :--- |
| **Build Suffix Trie** | `O(L²)` | Insert all `L` suffixes of a word of length `L`. |
| **Substring Search** | `O(M)` | Search for a substring of length `M` in the Suffix Trie. |
| **Count Occurrences** | `O(M)` | Navigate substring of length `M`; count stored at each node during build. |
| **Longest Repeated Substring** | `O(L²)` | Build trie, then DFS for deepest node with 2+ children paths. |
| **Space Complexity** | `O(L²)` | Store all suffixes. Memory-heavy compared to optimized trees. |

## Interview Context

Suffix Tries come up in interviews that require **repeated substring queries on a fixed text**. The core insight is that every substring of a string is a prefix of some suffix — so if you build a trie of all suffixes, you can answer any substring query in `O(M)` time.

While you're unlikely to be asked to build a full Suffix Trie from scratch (the `O(L²)` cost makes it impractical for large inputs), understanding the concept is critical because:

1. **It's a stepping stone** to Suffix Trees and Suffix Arrays, which interviewers may ask you to *discuss* in system design rounds (e.g., "How would you build a search engine for genomic data?").
2. **It solves a class of problems** — longest repeated substring, counting distinct substrings, counting occurrences — that appear on LeetCode and in interviews.
3. **It deepens trie understanding** — if you can explain how a Suffix Trie works, you demonstrate mastery of the trie data structure beyond basic prefix matching.

**Typical interview flow:** Discuss the Suffix Trie approach conceptually, acknowledge the `O(L²)` limitation, then pivot to a more practical solution (hashing, binary search + rolling hash, or built-in methods) for the actual implementation.

---

## Building Intuition

**Why Suffixes?**

Every substring of a word `T` is a prefix of some suffix of `T`.
For example, the substrings of "banana" include "ana". "ana" is a prefix of the suffix "anana" (and also the suffix "ana").
If we build a trie containing all suffixes of a text, we can find any substring by simply searching for it as a prefix in that trie!

**Complete Visualization: Suffix Trie for "abc$"**

Using a sentinel character `$` ensures every suffix ends at a unique leaf node. This is important because without it, some suffixes (like "a" in "banana") are prefixes of other suffixes, making leaf counting unreliable.

Suffixes of `"abc$"`:
1. `"abc$"` (starting at index 0)
2. `"bc$"` (starting at index 1)
3. `"c$"` (starting at index 2)
4. `"$"` (starting at index 3)

```
Suffix Trie for "abc$":

              root
          /   |    \    \
         a    b     c    $*
         |    |     |   [3]
         b    c     $*
         |    |    [2]
         c    $*
         |   [1]
         $*
        [0]

  [i] = leaf storing suffix start index i
  $   = sentinel (marks end of original string)
  *   = is_end marker (a complete suffix terminates here)
```

Every path from root to a `$`-leaf represents one suffix.
Every path from root to ANY node represents a substring of `"abc"`.

**Building a Suffix Trie for "banana"**

To build a Suffix Trie for the word "banana", we insert the following suffixes into a standard Trie:
1. "banana"
2. "anana"
3. "nana"
4. "ana"
5. "na"
6. "a"

```
Word: banana

Suffix Trie (Conceptual):
root
├── b - a - n - a - n - a*
├── a
│   ├── n
│   │   ├── a
│   │   │   ├── n - a*       (from suffix "anana")
│   │   │   └── *            (from suffix "ana")
│   └── *                    (from suffix "a")
├── n
│   └── a
│       ├── n - a*           (from suffix "nana")
│       └── *                (from suffix "na")
```

**Searching for "nan" in the Suffix Trie:**

```
Query: Does "nan" exist as a substring of "banana"?

Step 1: Start at root
Step 2: Follow 'n' → found (root has child 'n')
Step 3: Follow 'a' → found ('n' node has child 'a')
Step 4: Follow 'n' → found ('a' node has child 'n')
Step 5: All characters consumed → path exists → "nan" IS a substring ✓

Query: Does "xyz" exist?

Step 1: Start at root
Step 2: Follow 'x' → NOT found (root has no child 'x')
Step 3: Return False → "xyz" is NOT a substring ✗
```

**The Sentinel Character (`$`)**

Adding a sentinel character `$` (a character not in the original alphabet) to the end of the string before building the trie ensures:

1. **No suffix is a prefix of another suffix.** Without `$`, the suffix `"a"` is a prefix of `"ana"` which is a prefix of `"anana"`. With `$`, suffixes become `"a$"`, `"ana$"`, `"anana$"` — all distinct leaf paths.
2. **Leaf nodes have a 1-to-1 correspondence with suffixes.** This makes counting occurrences reliable: the number of leaf nodes in a subtree equals the number of times that substring appears.
3. **Standard convention** in suffix tree/array literature.

**The Problem with Suffix Tries**

While theoretically elegant, generating all suffixes takes `O(L²)` time and `O(L²)` space. For a 10,000-character string, that's up to ~50 million node traversals! This is impractical for large texts.

**Memory-Optimized Alternatives**

1.  **Suffix Trees:** Compress the Suffix Trie by merging nodes with single children into single edges representing strings. This reduces space and construction time to `O(L)` using algorithms like Ukkonen's, but the implementation is notoriously complex and extremely rare in interviews.
2.  **Suffix Arrays:** Instead of a tree, store an array of sorted indices representing the suffixes. This provides `O(L log L)` or `O(L)` construction and `O(M log L)` search, using significantly less memory (`O(L)` space for the array).

### Comparison: Suffix Trie vs Suffix Tree vs Suffix Array

| Aspect | Suffix Trie | Suffix Tree | Suffix Array |
| :--- | :--- | :--- | :--- |
| **Construction Time** | `O(L²)` | `O(L)` (Ukkonen's) | `O(L log L)` or `O(L)` (SA-IS) |
| **Space** | `O(L²)` | `O(L)` | `O(L)` |
| **Substring Search** | `O(M)` | `O(M)` | `O(M log L)` |
| **Implementation** | Simple | Very complex | Moderate |
| **Interview Likelihood** | Conceptual only | Rare (discuss only) | Occasionally (with LCP array) |
| **Practical Use** | Teaching/small strings | Bioinformatics | Competitive programming |

For most interview scenarios requiring substring search, simpler algorithms like KMP (Knuth-Morris-Pratt), Rabin-Karp, or simply using language built-in functions are preferred over implementing Suffix Tries or Trees. However, knowing *what* a Suffix Trie is and how it solves the substring problem conceptually is valuable.

---

## Pattern Implementation: Suffix Trie

Here is how you would implement a basic Suffix Trie. Note the use of `__slots__` to slightly reduce the memory footprint of the numerous nodes.

```python
class TrieNode:
    __slots__ = ['children', 'is_end']

    def __init__(self):
        self.children: dict[str, 'TrieNode'] = {}
        self.is_end: bool = False

class SuffixTrie:
    def __init__(self):
        self.root = TrieNode()

    def _insert_suffix(self, suffix: str) -> None:
        """Insert a single suffix into the trie.

        Despite being a "suffix", insertion works exactly like
        inserting any string into a standard trie.
        """
        node = self.root
        for char in suffix:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True

    def build_from_string(self, text: str) -> None:
        """Build the suffix trie by inserting all suffixes.

        Time: O(L²) where L = len(text)
        Space: O(L²) for all nodes
        """
        # Insert all suffixes: text[0:], text[1:], ..., text[L-1:]
        for i in range(len(text)):
            self._insert_suffix(text[i:])

    def contains_substring(self, substring: str) -> bool:
        """Check if a substring exists within the original text.

        Time: O(M) where M = len(substring)

        Key insight: we do NOT check is_end. Any valid path from the
        root represents a substring, regardless of whether a suffix
        ends there.
        """
        node = self.root
        for char in substring:
            if char not in node.children:
                return False
            node = node.children[char]
        # We only need it to be a valid path, not necessarily an end node
        return True
```

### Complexity Breakdown
- **Time Complexity:**
  - **Construction (`build_from_string`):** `O(L²)`, where `L` is the length of the `text`. We insert `L` suffixes, and the `i`-th suffix has length `L - i`. The sum of lengths is `L + (L-1) + ... + 1 = L(L+1)/2 = O(L²)`.
  - **Search (`contains_substring`):** `O(M)`, where `M` is the length of the `substring` we are searching for.
- **Space Complexity:** `O(L²)` in the worst case to store all characters of all suffixes (e.g., if all characters are distinct). With shared prefixes (like in "banana"), actual space is lower but still `O(L²)` worst case.

---

## Common Variations

### 1. Counting Substring Occurrences

To count how many times a substring appears in the text, navigate to the node where the substring ends, then count how many suffix endpoints (leaves) exist in that subtree.

Using the sentinel character `$` makes this clean — every leaf corresponds to exactly one suffix.

```python
class TrieNode:
    __slots__ = ['children', 'count']

    def __init__(self):
        self.children: dict[str, 'TrieNode'] = {}
        # Number of suffixes (leaves) in this subtree
        self.count: int = 0


class SuffixTrieWithCount:
    """Suffix trie that supports counting substring occurrences.

    Uses a sentinel character '$' to ensure each suffix ends at a
    unique leaf, making the leaf count per subtree equal to the
    number of occurrences of the corresponding substring.
    """
    SENTINEL = '$'

    def __init__(self, text: str):
        self.root = TrieNode()
        self._build(text + self.SENTINEL)

    def _build(self, text: str) -> None:
        """Insert all suffixes and propagate leaf counts upward."""
        for i in range(len(text)):
            node = self.root
            for char in text[i:]:
                if char not in node.children:
                    node.children[char] = TrieNode()
                # Each suffix passes through this node, so increment
                node.count += 1
                node = node.children[char]
            node.count += 1  # count the leaf itself

    def count_occurrences(self, substring: str) -> int:
        """Count how many times substring appears in the original text.

        Time: O(M) where M = len(substring)

        Example:
            trie = SuffixTrieWithCount("banana")
            trie.count_occurrences("ana")  # returns 2
            trie.count_occurrences("ban")  # returns 1
            trie.count_occurrences("xyz")  # returns 0
        """
        node = self.root
        for char in substring:
            if char not in node.children:
                return 0
            node = node.children[char]
        return node.count

    def contains(self, substring: str) -> bool:
        """Check if substring exists in the original text."""
        return self.count_occurrences(substring) > 0
```

### 2. Finding the Longest Repeated Substring

A substring is "repeated" if it occurs at least twice. In the suffix trie, this corresponds to an internal node (non-leaf) that has two or more paths through it. We find the deepest such node.

```python
def longest_repeated_substring(text: str) -> str:
    """Find the longest substring that appears at least twice.

    Approach: Build a suffix trie, then DFS to find the deepest
    internal node (a node with 2+ children or 2+ suffixes passing
    through it).

    Time: O(L²) to build trie + O(L²) to DFS = O(L²)
    Space: O(L²)

    Example:
        longest_repeated_substring("banana")  # returns "ana"
        longest_repeated_substring("abcd")    # returns "" (no repeats)
    """
    if not text:
        return ""

    # Build suffix trie with counts
    trie = SuffixTrieWithCount(text)

    # DFS: find the deepest node with count >= 2
    best: list[str] = [""]

    def dfs(node: TrieNode, path: list[str]) -> None:
        for char, child in node.children.items():
            if char == SuffixTrieWithCount.SENTINEL:
                continue  # skip sentinel paths for the result
            if child.count >= 2:
                path.append(char)
                if len(path) > len(best[0]):
                    best[0] = "".join(path)
                dfs(child, path)
                path.pop()

    dfs(trie.root, [])
    return best[0]
```

### 3. Counting Distinct Substrings

Every node in the suffix trie (excluding root) represents a unique substring. So the number of distinct substrings equals the number of non-root nodes.

```python
def count_distinct_substrings(text: str) -> int:
    """Count the number of distinct non-empty substrings.

    Each node in the suffix trie (except root) corresponds to
    exactly one unique substring.

    Time: O(L²) to build, O(total nodes) to count
    Space: O(L²)

    Example:
        count_distinct_substrings("abc")  # 6: a, ab, abc, b, bc, c
        count_distinct_substrings("aaa")  # 3: a, aa, aaa
    """

    class TrieNode:
        __slots__ = ['children']

        def __init__(self):
            self.children: dict[str, 'TrieNode'] = {}

    root = TrieNode()
    count = 0

    for i in range(len(text)):
        node = root
        for char in text[i:]:
            if char not in node.children:
                node.children[char] = TrieNode()
                count += 1  # new node = new distinct substring
            node = node.children[char]

    return count
```

---

## When to Use This Pattern

Use the Suffix Trie concept when:
- You need to perform **multiple substring searches** on a **fixed text**.
- The text is relatively small (due to `O(L²)` space requirements).
- You need to **count occurrences** of a pattern, find the **longest repeated substring**, or count **distinct substrings**.
- You are discussing conceptual approaches to string matching before moving to more practical/optimized solutions.

## When NOT to Use

| Scenario | Why Not | Better Alternative |
| :--- | :--- | :--- |
| **Large text** (L > ~5000) | `O(L²)` space/time exceeds limits | Suffix Array, KMP, Rabin-Karp |
| **Single substring query** | Building the trie is overkill for one search | `in` operator, KMP, Rabin-Karp |
| **Pattern has wildcards** | Suffix trie doesn't support `.` wildcards natively | Regex, DP |
| **Approximate matching** | Suffix trie is for exact matching only | Edit distance DP, BK-trees |
| **Streaming text** | Can't rebuild trie efficiently as text changes | Rolling hash, Aho-Corasick |
| **Online competitive programming** | `O(L²)` too slow for L > 10⁴ | Suffix Array + LCP, Z-algorithm |

---

## Edge Cases

1. **Empty string:** The suffix trie has only the root node. `contains_substring("")` should return `True` (the empty string is a substring of everything).
2. **Single character:** Only one suffix — the character itself. The trie has one path of length 1.
3. **All identical characters** (e.g., `"aaaa"`): Heavy prefix sharing. All suffixes share a common prefix path. Space is `O(L)` in this best case, not `O(L²)`.
4. **All unique characters** (e.g., `"abcd"`): No prefix sharing at all. This is the worst case for space: exactly `L(L+1)/2` nodes.
5. **Substring is longer than text:** `contains_substring` correctly returns `False` — the path runs out of trie nodes before the query is consumed.
6. **Substring equals full text:** Works correctly — the first suffix inserted is the full text itself.
7. **Sentinel character in input:** If using `$` as sentinel, ensure it doesn't appear in the original text. Choose a character outside the input alphabet.

---

## Interview Tips

1. **Don't implement from scratch unless asked.** The `O(L²)` construction makes suffix tries impractical for most coding problems. Discuss the concept, then code a more efficient approach.
2. **Lead with the key insight:** "Every substring is a prefix of some suffix." This one sentence shows you understand the core idea.
3. **Know the complexity trade-offs.** Be ready to compare Suffix Trie vs Suffix Tree vs Suffix Array when asked "how would you optimize this?"
4. **Pivot gracefully.** If the interviewer asks about substring search, mention the suffix trie conceptually, then say: "For this problem size, I'd use [binary search + rolling hash / KMP / built-in `in`] instead."
5. **The sentinel trick is a detail that impresses.** Mentioning that `$` ensures unique leaf paths shows depth of knowledge.
6. **Connect to practical systems.** Suffix structures underpin tools like `grep`, genome alignment (BLAST), and full-text search indexes.

---

## Step-by-Step Walkthrough: Substring Search

Let's trace `contains_substring("ana")` on the suffix trie built from `"banana"`:

```
Suffix Trie for "banana" (relevant portion):

root
├── b - a - n - a - n - a*
├── a
│   ├── n
│   │   ├── a
│   │   │   ├── n - a*    ← suffix "anana"
│   │   │   └── *         ← suffix "ana"
│   └── *                 ← suffix "a"
├── n
│   └── a
│       ├── n - a*        ← suffix "nana"
│       └── *             ← suffix "na"

Search for "ana":
┌─────────┬────────────────────┬──────────────────────────────┬────────┐
│ Step    │ Character          │ Action                       │ Result │
├─────────┼────────────────────┼──────────────────────────────┼────────┤
│ 1       │ 'a'                │ root.children has 'a' → go   │ ✓      │
│ 2       │ 'n'                │ 'a' node has child 'n' → go  │ ✓      │
│ 3       │ 'a'                │ 'n' node has child 'a' → go  │ ✓      │
│ (done)  │ All chars consumed │ Path exists → return True    │ ✓      │
└─────────┴────────────────────┴──────────────────────────────┴────────┘

Note: We did NOT check is_end. "ana" is a valid substring even though
we landed on a node that may or may not be a suffix endpoint.

Search for "xyz":
┌─────────┬────────────────────┬──────────────────────────────┬────────┐
│ Step    │ Character          │ Action                       │ Result │
├─────────┼────────────────────┼──────────────────────────────┼────────┤
│ 1       │ 'x'                │ root.children has no 'x'     │ ✗      │
│ (done)  │ Return False       │ No path → not a substring    │ ✗      │
└─────────┴────────────────────┴──────────────────────────────┴────────┘
```

---

## Practice Problems

| # | Problem | LeetCode | Difficulty | Key Concept |
| :--- | :--- | :--- | :--- | :--- |
| 1 | Longest Duplicate Substring | [1062](https://leetcode.com/problems/longest-duplicate-substring/) | Hard | Binary search + rolling hash (suffix trie conceptually) |
| 2 | Distinct Substrings (Count) | — (common in OAs) | Medium | Suffix trie node count |
| 3 | Repeated DNA Sequences | [187](https://leetcode.com/problems/repeated-dna-sequences/) | Medium | Fixed-length substring occurrences |
| 4 | Longest Common Substring | — (classic) | Medium | Generalized suffix trie (two strings) |
| 5 | Sum of Scores of Built Strings | [2223](https://leetcode.com/problems/sum-of-scores-of-built-strings/) | Hard | Z-algorithm (suffix trie too slow) |
| 6 | Number of Distinct Substrings in a String | [1698](https://leetcode.com/problems/number-of-distinct-substrings-in-a-string/) | Medium | Suffix trie or rolling hash |

**Progressive practice path:**
1. Start with **#3 (Repeated DNA Sequences)** — fixed-length substring search, solvable with a set but good to think about with suffix tries.
2. Move to **#6 (Distinct Substrings)** — directly maps to counting nodes in a suffix trie.
3. Tackle **#1 (Longest Repeated Substring)** — suffix trie gives the conceptual approach, but you'll need binary search + Rabin-Karp for the actual solution at scale.
4. Try **#5 (Sum of Scores)** — understand why suffix tries are too slow here, and learn the Z-algorithm as the right tool.

---

## Related Sections

- [Trie Implementation](./01-trie-implementation.md) — Foundational trie insert/search/prefix operations
- [Word Dictionary](./02-word-dictionary.md) — Trie with wildcard search (DFS through trie)
- [Chapter README](./README.md) — Overview of all trie patterns and when to use them

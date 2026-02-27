# Alien Dictionary

> **Prerequisites:** [07-topological-sort](./07-topological-sort.md)

## Interview Context

Alien Dictionary is a FANG+ hard problem because:

1. **Graph construction from constraints**: Non-trivial problem modeling
2. **Topological sort application**: Real-world use case
3. **Edge cases**: Many tricky cases to handle
4. **Character ordering**: Different from typical node problems

**FANG Context (Why Google Loves This):**
Google frequently asks this problem because it perfectly tests a candidate's ability to translate an abstract requirement ("derive an alphabet") into a concrete graph algorithm (Directed Acyclic Graph + Topological Sort). It also heavily tests edge case handling (prefixes, cycles, disconnected components) and allows for follow-up questions about lexicographically smallest orderings or memory optimization (arrays vs HashMaps).

This problem appears frequently at Facebook, Google, and Airbnb.

---

## Problem Statement

Given a sorted list of words in an alien language, derive the order of letters in the alien alphabet.

```
Example:
words = ["wrt", "wrf", "er", "ett", "rftt"]

Analysis:
- wrt < wrf → t < f
- wrf < er → w < e
- er < ett → r < t
- ett < rftt → e < r

Order derived: w → e → r → t → f
Output: "wertf"
```

---

## Core Insight: Build Graph from Comparisons

Compare adjacent words to find ordering constraints:

```python
"wrt" vs "wrf":
   w == w  (same)
   r == r  (same)
   t ≠ f   → t comes before f in alphabet

This gives edge: t → f
```

---

## Theory: Formalizing DAG Concepts & Kahn's Algorithm

Before implementing the solution, we need to formalize what we're building: a **Directed Acyclic Graph (DAG)**.

1. **Nodes**: Represent unique characters in the alien language.
2. **Directed Edges ($u \rightarrow v$)**: Represent a strict ordering constraint where character $u$ must appear before character $v$ in the alphabet.
3. **Acyclic requirement**: For a valid alphabet to exist, the graph cannot contain cycles (e.g., $a \rightarrow b \rightarrow c \rightarrow a$ implies $a$ comes before itself, which is impossible).

### Why Kahn's Algorithm Works

Kahn's Algorithm is a Breadth-First Search (BFS) approach to topological sorting:

1. **In-degree Tracking**: For each character, we track its *in-degree* (the number of prerequisite characters that must appear before it).
2. **Zero In-degree Source Nodes**: Any character with an in-degree of `0` has no remaining prerequisites. It is guaranteed safe to place next in our final ordering.
3. **Peeling Edges**: Once we process a character, we logically "remove" it from the graph by decrementing the in-degrees of all its neighbors.
4. **Iterative Resolution**: If a neighbor's in-degree drops to `0`, all its prerequisites have been fulfilled, and it becomes a new source node.

**Cycle Detection**: If the algorithm finishes and we haven't processed all unique characters, it means the remaining characters are locked in a cycle where they endlessly wait for each other (their in-degrees never reached `0`). This definitively proves the input is invalid.

---

## Solution

```python
from collections import defaultdict, deque

def alien_order(words: list[str]) -> str:
    """
    Derive alien alphabet order from sorted words.

    Time: O(total characters)
    Space: O(unique characters)

    Returns empty string if no valid order exists.
    """
    # Build graph and in-degree count
    graph = defaultdict(set)
    in_degree = {}

    # Initialize all characters
    for word in words:
        for c in word:
            if c not in in_degree:
                in_degree[c] = 0

    # Compare adjacent words to find edges
    for i in range(len(words) - 1):
        word1, word2 = words[i], words[i + 1]

        # Edge case: "abc" before "ab" is invalid
        if len(word1) > len(word2) and word1[:len(word2)] == word2:
            return ""

        # Find first different character
        for c1, c2 in zip(word1, word2):
            if c1 != c2:
                # c1 comes before c2
                if c2 not in graph[c1]:
                    graph[c1].add(c2)
                    in_degree[c2] += 1
                break  # Only first difference matters

    # Topological sort using Kahn's algorithm
    queue = deque([c for c in in_degree if in_degree[c] == 0])
    result = []

    while queue:
        c = queue.popleft()
        result.append(c)

        for neighbor in graph[c]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    # Check if all characters are included (no cycle)
    if len(result) != len(in_degree):
        return ""  # Cycle detected

    return ''.join(result)
```

class Solution {
public:
    string alienOrder(vector<string>& words) {
        unordered_map<char, vector<char>> adjList;
        unordered_map<char, int> in_degree;

        for (const string& word : words) {
            for (char c : word) {
                in_degree[c] = 0;
            }
        }

        for (int i = 0; i < words.size() - 1; ++i) {
            string w1 = words[i];
            string w2 = words[i + 1];

            if (w1.length() > w2.length() && w1.substr(0, w2.length()) == w2) {
                return "";
            }

            for (int j = 0; j < min(w1.length(), w2.length()); ++j) {
                if (w1[j] != w2[j]) {
                    adjList[w1[j]].push_back(w2[j]);
                    in_degree[w2[j]]++;
                    break;
                }
            }
        }

        queue<char> q;
        for (auto const& [node, degree] : in_degree) {
            if (degree == 0) q.push(node);
        }

        string result = "";
        while (!q.empty()) {
            char current = q.front();
            q.pop();
            result += current;

            for (char neighbor : adjList[current]) {
                in_degree[neighbor]--;
                if (in_degree[neighbor] == 0) q.push(neighbor);
            }
        }

        return result.length() == in_degree.size() ? result : "";
    }
};
```

---

## Visual Example

```
words = ["wrt", "wrf", "er", "ett", "rftt"]

Step 1: Extract edges from adjacent word comparisons
  wrt vs wrf: t → f
  wrf vs er:  w → e
  er vs ett:  r → t
  ett vs rftt: e → r

Step 2: Build graph
  w → e
  e → r
  r → t
  t → f

In-degrees:
  w: 0, e: 1, r: 1, t: 1, f: 1

Step 3: Topological sort (Kahn's)
  Queue: [w] (only w has in-degree 0)
  Pop w: result = "w", decrement e's in-degree
  Queue: [e]
  Pop e: result = "we", decrement r's in-degree
  Queue: [r]
  Pop r: result = "wer", decrement t's in-degree
  Queue: [t]
  Pop t: result = "wert", decrement f's in-degree
  Queue: [f]
  Pop f: result = "wertf"

Output: "wertf"
```

---

## Edge Cases

### 1. Invalid Order (Prefix Violation)

```python
words = ["abc", "ab"]
# "abc" before "ab" is impossible since "ab" is prefix of "abc"
# Return ""
```

### 2. Cycle

```python
words = ["a", "b", "a"]
# a < b and b < a → cycle
# Return ""
```

### 3. Single Word

```python
words = ["abc"]
# No comparisons possible
# Any order of a, b, c is valid
# Return "abc" (or any permutation)
```

### 4. Multiple Valid Orders

```python
words = ["z", "x"]
# Only constraint: z < x
# Other chars can be anywhere
# Return one valid order: "zx"
```

### 5. Same Character Repeated

```python
words = ["a", "a"]
# Equal words give no new information
# Return "a"
```

---

## Common Mistakes

```python
# WRONG: Not handling prefix case
for c1, c2 in zip(word1, word2):
    if c1 != c2:
        graph[c1].add(c2)
        break
# Missing: Check if word1 > word2 but shares prefix

# CORRECT: Add prefix check
if len(word1) > len(word2) and word1[:len(word2)] == word2:
    return ""


# WRONG: Not initializing all characters
for i in range(len(words) - 1):
    # Only processes characters that differ
    ...
# Characters that never differ aren't included!

# CORRECT: Initialize all characters first
for word in words:
    for c in word:
        if c not in in_degree:
            in_degree[c] = 0


# WRONG: Multiple edges between same chars
if c1 != c2:
    graph[c1].append(c2)  # May add duplicate edges
    in_degree[c2] += 1

# CORRECT: Use set to prevent duplicates
if c2 not in graph[c1]:
    graph[c1].add(c2)
    in_degree[c2] += 1
```

---

## Alternative: DFS Topological Sort

```python
def alien_order_dfs(words: list[str]) -> str:
    """
    DFS-based topological sort.
    """
    graph = defaultdict(set)
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {}

    # Initialize all characters
    for word in words:
        for c in word:
            color[c] = WHITE

    # Build graph
    for i in range(len(words) - 1):
        w1, w2 = words[i], words[i + 1]

        if len(w1) > len(w2) and w1[:len(w2)] == w2:
            return ""

        for c1, c2 in zip(w1, w2):
            if c1 != c2:
                graph[c1].add(c2)
                break

    result = []
    has_cycle = [False]

    def dfs(c: str):
        if has_cycle[0]:
            return
        color[c] = GRAY

        for neighbor in graph[c]:
            if color[neighbor] == GRAY:
                has_cycle[0] = True
                return
            if color[neighbor] == WHITE:
                dfs(neighbor)

        color[c] = BLACK
        result.append(c)

    for c in color:
        if color[c] == WHITE:
            dfs(c)

    if has_cycle[0]:
        return ""

    return ''.join(reversed(result))
```

---

## Lexicographically Smallest Order

If multiple valid orders exist, return lexicographically smallest:

```python
import heapq

def alien_order_lex(words: list[str]) -> str:
    """
    Return lexicographically smallest valid order.
    """
    graph = defaultdict(set)
    in_degree = {}

    for word in words:
        for c in word:
            if c not in in_degree:
                in_degree[c] = 0

    for i in range(len(words) - 1):
        w1, w2 = words[i], words[i + 1]

        if len(w1) > len(w2) and w1[:len(w2)] == w2:
            return ""

        for c1, c2 in zip(w1, w2):
            if c1 != c2:
                if c2 not in graph[c1]:
                    graph[c1].add(c2)
                    in_degree[c2] += 1
                break

    # Use min-heap for lexicographic order
    heap = [c for c in in_degree if in_degree[c] == 0]
    heapq.heapify(heap)
    result = []

    while heap:
        c = heapq.heappop(heap)
        result.append(c)

        for neighbor in graph[c]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                heapq.heappush(heap, neighbor)

    if len(result) != len(in_degree):
        return ""

    return ''.join(result)
```

---

## Complexity Analysis

| Operation        | Time                   | Space           |
| ---------------- | ---------------------- | --------------- |
| Build graph      | O(sum of word lengths) | O(unique chars) |
| Topological sort | O(V + E)               | O(V)            |
| Total            | O(total chars)         | O(unique chars) |

V = unique characters, E = ordering constraints

### Trade-offs: Kahn's Algorithm (BFS) vs DFS Topological Sort

Both approaches achieve the same $O(V+E)$ time complexity, but there are practical differences.

**Kahn's Algorithm (BFS)**
* **Pros**:
    * Intuitive to trace for in-degrees iteratively.
    * Trivial to convert for finding lexicographical orderings by swapping the `Queue` with a `Min-Heap` (Priority Queue).
    * Space complexity is entirely on the heap; no deep function calls risking stack overflow.
* **Cons**:
    * Requires tracking an extra `in_degree` map or array alongside the adjacency list.

**Recursive DFS**
* **Pros**:
    * Very concise to write conceptually: traverse nodes fully and append to result upon function exit, then reverse it.
    * Only requires an adjacency list and a three-state `color` (visited/visiting/unvisited) tracker map.
* **Cons**:
    * Cycle detection relies on the recursive call stack checking the three-state array (visiting a node currently labeled as "Gray"/visiting). It can be trickier to intuitively reason about during an interview.
    * Recursive depth can technically exceed standard stack limits on enormously long cyclic graphs.

---

## Interview Tips

1. **Explain graph construction**: Show how comparisons give edges
2. **Handle all edge cases**: Prefix, cycle, single word
3. **Use set for edges**: Prevent duplicates
4. **Initialize all chars**: Don't miss isolated characters
5. **Multiple valid orders**: Mention this if asked

---

## Practice Problems

| #   | Problem                 | Difficulty | Key Variation            |
| --- | ----------------------- | ---------- | ------------------------ |
| 1   | Alien Dictionary        | Hard       | Core problem             |
| 2   | Course Schedule II      | Medium     | Similar topological sort |
| 3   | Sequence Reconstruction | Medium     | Verify unique order      |

---

## Key Takeaways

1. **Compare adjacent words**: Extract ordering constraints
2. **First difference matters**: Stop after first differing character
3. **Handle prefix case**: Longer prefix word after shorter = invalid
4. **Topological sort**: Apply after building graph
5. **Multiple valid orders**: Unless graph forces unique path

---

## Next: [18-network-delay.md](./18-network-delay.md)

Apply Dijkstra to the Network Delay Time problem.

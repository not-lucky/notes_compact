# Alien Dictionary

> **Prerequisites:** [07-topological-sort](./07-topological-sort.md)

## Interview Context

Alien Dictionary is a FANG+ hard problem because:

1. **Graph construction from constraints**: Non-trivial problem modeling.
2. **Topological sort application**: Real-world use case.
3. **Edge cases**: Many tricky cases to handle (prefixes, disconnected components, cycles).
4. **Character ordering**: Different from typical node-based problems.

**FANG Context (Why Google Loves This):**
Google frequently asks this problem because it perfectly tests a candidate's ability to translate an abstract requirement ("derive an alphabet") into a concrete graph algorithm (Directed Acyclic Graph + Topological Sort). It heavily tests edge case handling and allows for natural follow-up questions about lexicographically smallest orderings or memory optimization.

This problem appears frequently at Meta, Google, and Airbnb.

---


## Warm-up: Verifying an Alien Dictionary

Before deriving the alphabet, let's look at an easier problem: given an alien language's alphabet order, verify if a sequence of words is sorted lexicographically.

**Problem:** Given a string `order` representing the alien alphabet and an array of `words`, return `True` if the words are sorted according to `order`, and `False` otherwise.

```python
def is_alien_sorted(words: list[str], order: str) -> bool:
    """
    Time: O(C) where C is the total number of characters in all words.
    Space: O(1) since order mapping is fixed at 26 characters.
    """
    # Create a mapping from character to its rank (index) in the alphabet
    order_map = {c: i for i, c in enumerate(order)}
    
    # Compare each pair of adjacent words
    for i in range(len(words) - 1):
        w1, w2 = words[i], words[i + 1]
        
        # Check all characters
        for j in range(len(w1)):
            # If w2 is exhausted before finding a difference, w1 is longer and thus greater
            # E.g., "apple" vs "app" -> invalid
            if j == len(w2):
                return False
                
            # If characters differ, they must be in correct order
            if w1[j] != w2[j]:
                if order_map[w1[j]] > order_map[w2[j]]:
                    return False
                break # We found a difference and it's valid, move to next pair of words
                
    return True
```

This warm-up establishes the fundamental logic used in the main Alien Dictionary problem:
1. Lexicographical order is determined by the **first different character**.
2. If two words share a prefix but the first is longer (`"apple"` vs `"app"`), the order is **invalid**.

---

## Problem Statement: Deriving the Dictionary

Given a sorted list of words in an alien language, derive the order of letters in the alien alphabet.

```text
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

```text
"wrt" vs "wrf":
   w == w  (same)
   r == r  (same)
   t ≠ f   → t comes before f in alphabet

This gives a directed edge: t → f
```

---

## Theory: Formalizing DAG Concepts & Kahn's Algorithm

Before implementing the solution, we formalize what we're building: a **Directed Acyclic Graph (DAG)**.

1. **Nodes**: Represent unique characters in the alien language.
2. **Directed Edges ($u \rightarrow v$)**: Represent a strict ordering constraint where character $u$ must appear before character $v$ in the alphabet.
3. **Acyclic requirement**: For a valid alphabet to exist, the graph cannot contain cycles (e.g., $a \rightarrow b \rightarrow c \rightarrow a$ implies $a$ comes before itself, which is impossible).

### Why Kahn's Algorithm Works

Kahn's Algorithm is a Breadth-First Search (BFS) approach to topological sorting:

1. **In-degree Tracking**: For each character, we track its *in-degree* (number of prerequisite characters).
2. **Zero In-degree Source Nodes**: Any character with an in-degree of `0` has no remaining prerequisites. It is guaranteed safe to place next in our ordering.
3. **Peeling Edges**: Once we process a character, we logically "remove" it from the graph by decrementing the in-degrees of all its neighbors.
4. **Iterative Resolution**: If a neighbor's in-degree drops to `0`, all its prerequisites are fulfilled, making it a new source node.

**Cycle Detection**: If the algorithm finishes and we haven't processed all unique characters, the remaining characters are locked in a cycle. This definitively proves the input is invalid.

---

## Solution: Kahn's Algorithm (BFS)

```python
from collections import deque

def alien_order(words: list[str]) -> str:
    """
    Derive alien alphabet order from sorted words.

    Time: O(C) where C is the total number of characters across all words.
    Space: O(U + E) = O(1) where U is unique characters (max 26) and E is edges.
    
    Returns empty string if no valid order exists.
    """
    # 1. Initialize graph and in-degree for ALL unique characters
    graph = {c: set() for word in words for c in word}
    in_degree = {c: 0 for c in graph}

    # 2. Compare adjacent words to find edges
    for i in range(len(words) - 1):
        w1, w2 = words[i], words[i + 1]

        # Edge case: w1 is longer than w2 but shares prefix ("abc" > "ab" is invalid)
        if len(w1) > len(w2) and w1[:len(w2)] == w2:
            return ""

        # Find first different character to create a directed edge
        for c1, c2 in zip(w1, w2):
            if c1 != c2:
                # c1 comes before c2
                if c2 not in graph[c1]:
                    graph[c1].add(c2)
                    in_degree[c2] += 1
                break  # Only the first difference matters

    # 3. Topological sort using Kahn's algorithm
    queue = deque([c for c in in_degree if in_degree[c] == 0])
    result = []

    while queue:
        c = queue.popleft()
        result.append(c)

        for neighbor in graph[c]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    # 4. Check if all characters are included (no cycle)
    if len(result) != len(in_degree):
        return ""  # Cycle detected

    return "".join(result)
```

---

## Visual Example

```text
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
for c1, c2 in zip(w1, w2):
    if c1 != c2:
        graph[c1].add(c2)
        break
# Missing: Check if w1 > w2 but shares prefix

# CORRECT: Add prefix check before checking characters
if len(w1) > len(w2) and w1[:len(w2)] == w2:
    return ""

# WRONG: Not initializing all characters
for i in range(len(words) - 1):
    # Only processes characters that differ
    ...
# Characters that never differ aren't included in the result!

# CORRECT: Initialize all characters first
graph = {c: set() for word in words for c in word}
in_degree = {c: 0 for c in graph}

# WRONG: Creating multiple edges between the same characters
if c1 != c2:
    graph[c1].append(c2)  # List may add duplicate edges
    in_degree[c2] += 1

# CORRECT: Use set to prevent duplicates and conditionally increment in-degree
if c2 not in graph[c1]:
    graph[c1].add(c2)
    in_degree[c2] += 1
```

---

## Alternative: DFS Topological Sort

Using recursion with a 3-state tracking dictionary (Unvisited, Visiting, Visited).

```python
def alien_order_dfs(words: list[str]) -> str:
    """
    DFS-based topological sort using 3-state cycle detection.
    """
    # Initialize graph for all characters
    graph = {c: set() for word in words for c in word}
    
    # Build graph
    for i in range(len(words) - 1):
        w1, w2 = words[i], words[i + 1]

        if len(w1) > len(w2) and w1[:len(w2)] == w2:
            return ""

        for c1, c2 in zip(w1, w2):
            if c1 != c2:
                graph[c1].add(c2)
                break

    # States: Unvisited (not in dict), VISITING = 1, VISITED = 2
    VISITING, VISITED = 1, 2
    states = {}
    result = []

    def dfs(node: str) -> bool:
        if states.get(node) == VISITING:
            return False  # Cycle detected
        if states.get(node) == VISITED:
            return True   # Already processed

        states[node] = VISITING
        for neighbor in graph[node]:
            if not dfs(neighbor):
                return False
                
        states[node] = VISITED
        result.append(node)
        return True

    # Run DFS for every node
    for node in graph:
        if states.get(node) != VISITED:
            if not dfs(node):
                return ""

    # Reverse result to get correct topological order
    return "".join(reversed(result))
```

---

## Lexicographically Smallest Order

If multiple valid orders exist, return the lexicographically smallest. This is easily achieved by replacing Kahn's queue with a Min-Heap.

```python
import heapq

def alien_order_lex(words: list[str]) -> str:
    """
    Return lexicographically smallest valid order.
    """
    graph = {c: set() for word in words for c in word}
    in_degree = {c: 0 for c in graph}

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

    return "".join(result)
```

---

## Complexity Analysis

| Operation        | Time                                | Space                               |
| ---------------- | ----------------------------------- | ----------------------------------- |
| Build graph      | $O(C)$                              | $O(U)$                              |
| Topological sort | $O(U + E)$                          | $O(U)$                              |
| **Total**        | $O(C)$                              | $O(1)$ (since max $U \le 26$)       |

* $C$ = Total characters across all words in the input array.
* $U$ = Unique characters (Max 26 for English lowercase, giving $O(1)$ space).
* $E$ = Number of edges (Max 26 $\times$ 26, effectively $O(1)$).

### Trade-offs: Kahn's Algorithm (BFS) vs DFS Topological Sort

Both approaches achieve $O(C)$ time complexity, but have practical differences.

**Kahn's Algorithm (BFS)**
* **Pros**:
    * Intuitive to trace for in-degrees iteratively.
    * Trivial to convert for finding lexicographical orderings by swapping the `Queue` with a `Min-Heap` (Priority Queue).
* **Cons**:
    * Requires tracking an extra `in_degree` map alongside the adjacency list.

**Recursive DFS**
* **Pros**:
    * Very concise to write: traverse nodes fully and append to result upon function exit, then reverse it.
    * Only requires an adjacency list and a state tracker.
* **Cons**:
    * Harder to adapt for lexicographical constraints.
    * Cycle detection relies on checking states during the recursive call stack, which can be trickier to reason about during an interview.

---

## Interview Tips

1. **Explain graph construction**: Clearly articulate how comparisons give edges.
2. **Handle all edge cases**: Prefix (`abc` > `ab`), cycles, single word inputs.
3. **Use a set for edges**: Prevent duplicate edges from incrementing in-degree multiple times.
4. **Initialize ALL chars**: Don't miss isolated characters that are never part of a difference.
5. **Multiple valid orders**: Acknowledge that standard topological sort returns one of potentially many valid permutations.

---

## Practice Problems

| #   | Problem                 | Difficulty | Key Variation            |
| --- | ----------------------- | ---------- | ------------------------ |
| 1   | Alien Dictionary        | Hard       | Core problem             |
| 2   | Course Schedule II      | Medium     | Similar topological sort |
| 3   | Sequence Reconstruction | Medium     | Verify unique order      |

---

## Key Takeaways

1. **Compare adjacent words**: Extract ordering constraints by finding the first mismatch.
2. **First difference matters**: Stop comparing characters after the first differing character.
3. **Handle prefix case**: A longer word before a shorter prefix word = invalid.
4. **Topological sort**: Use Kahn's Algorithm after building the directed graph.
5. **Check for cycles**: If output length $\neq$ unique characters, return `""`.

---

## Next: [18-network-delay.md](./18-network-delay.md)

Apply Dijkstra to the Network Delay Time problem.
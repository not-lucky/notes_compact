import os

file_path = '/home/lucky/stuff/notes_fang/08-graphs/18-network-delay.md'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add Progressive Understanding
content = content.replace(
    "## Solution: Dijkstra's Algorithm\n\n### Python Implementation",
    "## Progressive Understanding: Why Standard BFS Fails\n\nA common mistake is trying to solve this using standard Breadth-First Search (BFS) just like unweighted shortest path problems. \n\nConsider this graph:\n```text\n    A --(5)--> B\n    |          ^\n   (1)        (1)\n    |          |\n    v          |\n    C ---------+\n```\n\n*   **Standard BFS from A:**\n    1. Visits `B` (distance 5) and `C` (distance 1).\n    2. Since `B` is marked as visited, BFS won't update its distance when exploring `C`'s neighbors. \n    3. The absolute shortest path `A -> C -> B` (total distance 2) is missed.\n\n**Why?** BFS explores by the *number of edges* (hops), assuming each edge takes uniform time. When edge weights differ, a path with more hops can have a smaller total weight.\n\n**The Solution:** We need an algorithm that explores paths based on the *cumulative weight* so far, rather than the number of edges. This is exactly what **Dijkstra's Algorithm** does by using a Priority Queue (Min-Heap) instead of a regular Queue.\n\n---\n\n## Solution: Dijkstra's Algorithm\n\n### Python Implementation"
)

# 2. Update array alternative heading
content = content.replace(
    "## Alternative: Without defaultdict\n\n```python\nimport heapq\n\ndef network_delay_time_alt(times: list[list[int]], n: int, k: int) -> int:\n    \"\"\"\n    Same algorithm with explicit arrays.\n    \"\"\"",
    "## Alternative: Without `defaultdict` (Array-Based)\n\n```python\nimport heapq\n\ndef network_delay_time_alt(times: list[list[int]], n: int, k: int) -> int:\n    \"\"\"\n    Same algorithm with explicit arrays for distance tracking.\n    \"\"\""
)

# 3. Group Bellman-Ford under Alternative Solutions
content = content.replace(
    "## Bellman-Ford Alternative\n\nIf edges could be negative (they can't in this problem, but good to know):",
    "## Alternative Solutions\n\n### Bellman-Ford (For Negative Weights)\n\nIf edges could be negative (they can't in this problem, but it's a good theoretical alternative), we would use Bellman-Ford:"
)

# 4. Group BFS Unweighted
content = content.replace(
    "## BFS for Unweighted (Simplified Version)\n\nIf all delays were 1 (unweighted), could use BFS:",
    "### BFS for Unweighted Graphs (Conceptual)\n\nIf all delays were strictly `1` (unweighted), we could use standard BFS:"
)

# 5. Fix Edge Cases
old_edge_cases = """## Edge Cases

```python
# 1. Source is only node
n = 1, k = 1, times = []
# Return 0 (no delay needed)

# 2. Unreachable node
times = [[1, 2, 1]]  # Only 1 → 2
n = 3, k = 1
# Node 3 unreachable, return -1

# 3. All nodes directly connected to source
times = [[1, 2, 1], [1, 3, 1], [1, 4, 1]]
n = 4, k = 1
# All at distance 1, return 1

# 4. Linear chain
times = [[1, 2, 1], [2, 3, 1], [3, 4, 1]]
n = 4, k = 1
# Cumulative delays: 1, 2, 3
# Return 3
```"""

new_edge_cases = """## Edge Cases

1. **Source is the only node:** `n = 1, k = 1, times = []` → Return `0` (no delay needed).
2. **Disconnected graph / Unreachable nodes:** `times = [[1, 2, 1]], n = 3, k = 1` → Node 3 is unreachable, return `-1`.
3. **All nodes directly connected to source:** `times = [[1, 2, 1], [1, 3, 1], [1, 4, 1]], n = 4, k = 1` → Return `1` (maximum weight of outgoing edges is the answer).
4. **Linear chain:** `times = [[1, 2, 1], [2, 3, 1], [3, 4, 1]], n = 4, k = 1` → Cumulative delays are `1, 2, 3`. Return `3`."""

content = content.replace(old_edge_cases, new_edge_cases)

# 6. Fix Common Mistakes
content = content.replace("# WRONG: Using BFS for weighted graph", "# MISTAKE 1: Using BFS for weighted graph")
content = content.replace("# CORRECT: Use Dijkstra for weighted graphs", "# CORRECT: Use Dijkstra with a Min-Heap")
content = content.replace("# WRONG: Not checking if all nodes reached", "# MISTAKE 2: Not checking if all nodes reached")
content = content.replace("# If some nodes unreachable, should return -1", "# If some nodes are unreachable, we should return -1")
content = content.replace("# WRONG: 0-indexed vs 1-indexed confusion", "# MISTAKE 3: 0-indexed vs 1-indexed confusion")
content = content.replace("# If k is 1-indexed, this is wrong!", "# If k is 1-indexed, this is out of bounds or semantically wrong!")
content = content.replace("# CORRECT: Use n+1 for 1-indexed, or use dict\ndist = [INF] * (n + 1)  # 1-indexed", "# CORRECT: Use n+1 for 1-indexed, or use a dictionary\ndist = [INF] * (n + 1)  # 1-indexed")

# 7. Fix Complexity Analysis
old_complexity = """*   **Priority Queue Operations:**
    *   In the worst case, every edge could lead to a newly found shorter path, resulting in an insertion into the priority queue (`heapq.heappush()`).
    *   Since there are at most $E$ edges, we could potentially push $E$ pairs into the heap.
    *   Extracting the minimum element (`heapq.heappop()`) takes $O(\log(\text{heap size}))$ time. The maximum size of the heap is $O(E)$.
    *   Therefore, popping and pushing operations take bounded by $O(E \log E)$.
    *   Wait, $O(E \log E)$ can be simplified. In a simple graph (no parallel edges between same nodes), the maximum number of edges $E$ is bounded by $V^2$ (i.e., $E \le V^2$).
    *   So, $\log E \le \log(V^2) = 2 \log V$, which means $O(\log E)$ is equivalent to $O(\log V)$.
    *   Thus, the total time spent pushing and popping is $O(E \log V)$.
    *   *(Note: Using an advanced Fibonacci heap, we could optimize this to $O(V \log V + E)$, but the standard binary heap implementation remains $O((V + E) \log V)$.)*
*   **Final Output:** $O(V)$ to iterate over the `dist` array/hashmap to find the maximum distance.
*   **Total Time:** $O(E) + O(V) + O(E \log V) + O(V) = O((V + E) \log V)$.

### 2. Space Complexity: $O(V + E)$

*   **Graph Storage:** $O(V + E)$ memory to store the adjacency list representation of the graph. We have $V$ lists containing a total of $E$ entries.
*   **Distance Array (`dist`):** $O(V)$ memory to track the minimum distance to each node.
*   **Priority Queue:** In the worst-case scenario (like a dense graph), we might push many duplicate node updates before we pop them. The heap can store up to $O(E)$ elements simultaneously.
*   **Total Space:** $O(V + E) + O(V) + O(E) = O(V + E)$."""

new_complexity = """*   **Priority Queue Operations:**
    *   In the worst case, every edge could lead to a newly found shorter path, resulting in an insertion into the priority queue.
    *   Thus, we could push at most $E$ elements into the heap.
    *   Pushing and popping from a heap of size $O(E)$ takes $O(\log E)$ time.
    *   In a simple graph (no parallel edges), the maximum number of edges $E$ is bounded by $V^2$.
    *   Therefore, $\log E \le \log(V^2) = 2 \log V$. This means $O(\log E)$ is strictly equivalent to $O(\log V)$ in big-O notation.
    *   The total time spent on heap operations is bounded by $O(E \log V)$.
    *   *(Note: Using an advanced Fibonacci heap, we could optimize this theoretical bound to $O(V \log V + E)$, but the standard binary heap implementation remains $O((V + E) \log V)$.)*
*   **Final Output:** $O(V)$ to iterate over the `dist` array/hashmap to find the maximum distance.
*   **Total Time:** $O(E) + O(V) + O(E \log V) + O(V) = O((V + E) \log V)$.

### 2. Space Complexity: $O(V + E)$

*   **Graph Storage:** $O(V + E)$ memory to store the adjacency list representation of the graph. We have $V$ lists containing a total of $E$ entries.
*   **Distance Storage (`dist`):** $O(V)$ memory to track the minimum distance to each node.
*   **Priority Queue:** In the worst-case scenario (like a dense graph), we might push many duplicate node updates before we pop them. The heap can store up to $O(E)$ elements simultaneously. Since $O(E) \le O(V^2)$, in strictly sparse graphs it's $O(V)$. However, the general bound of $O(V + E)$ captures all extra memory used.
*   **Total Space:** $O(V + E) + O(V) + O(E) = O(V + E)$."""

content = content.replace(old_complexity, new_complexity)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Update complete")

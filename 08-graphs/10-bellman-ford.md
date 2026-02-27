# Bellman-Ford Algorithm

> **Prerequisites:** [09-dijkstra](./09-dijkstra.md)

## Building Intuition

**The "Repeated Announcements" Mental Model**: Imagine a town where everyone shouts their house number to neighbors. Initially, only you know your distance from home (0). Each round:

1. Everyone shouts their current best known distance
2. Neighbors update if they hear a better path
3. After enough rounds, everyone knows the true shortest distance

```
Round 0: You know your distance (0), others don't know
Round 1: Your direct neighbors learn their distance (1 hop)
Round 2: Their neighbors learn (2 hops via relay)
...
Round V-1: Everyone within V-1 hops knows (covers all possible paths)
```

**Dijkstra's Optimal Substructure vs Bellman-Ford's Exhaustive Search**:
To understand Bellman-Ford, it helps to contrast it with Dijkstra's algorithm.
Dijkstra relies on an **optimal substructure** property: when a node is extracted from the min-heap, its shortest path is finalized because *no path through unexplored nodes can be shorter*. This strictly requires non-negative weights.

Bellman-Ford discards this assumption entirely. It doesn't trust that any node's distance is "final" until the very end. Instead of carefully picking the next best node, Bellman-Ford brute-forces the relaxation of *all* edges, repeatedly.

```
Dijkstra's logic: "Node X is the closest unvisited node. Since all edges are ≥ 0,
                   no alternate route can reach X faster. X is finalized."
                   (Fails with negative weights!)

Bellman-Ford's logic: "I don't know which nodes are finalized. I will just try to
                       improve ALL paths. If I do this enough times (V-1), I guarantee
                       all shortest paths are found, regardless of weight signs."
```

**Why V-1 iterations?**

```
Longest possible shortest path in V nodes uses V-1 edges:
0 → 1 → 2 → 3 → ... → V-1
     (V-1 edges total)

Each iteration guarantees at least one more edge is "correct."
After V-1 iterations, paths with up to V-1 edges are all correct.
```

**The negative weight handling**:
Unlike Dijkstra (which assumes "farther nodes can't help"), Bellman-Ford doesn't assume anything. It just keeps propagating updates until nothing changes.

```
Dijkstra's assumption: Once I finalize node X, no better path exists.
                       FALSE with negative weights!

Bellman-Ford's approach: Keep updating until V-1 rounds.
                         If still updating at round V → negative cycle!
```

**Why the Vth iteration detects negative cycles**:
If a path keeps getting shorter after V-1 iterations, there must be a cycle with negative total weight - you can loop forever getting cheaper!

```
Negative cycle detection:
After V-1 iterations: All finite shortest paths are found
At iteration V: If ANY edge can still be relaxed → negative cycle exists

Why? A shortest path has at most V-1 edges. If we can still improve,
we're using more than V-1 edges → must be cycling!
```

---

## When NOT to Use

**Don't use Bellman-Ford when:**

- **All weights are non-negative** → Dijkstra is O((V+E)logV) vs O(VE)
- **Graph is unweighted** → BFS is O(V+E), much faster
- **Need to process dynamically** → Not designed for updates

**Bellman-Ford is the only choice when:**

- Negative edge weights exist (Dijkstra fails)
- Need to detect negative cycles
- Graph structure doesn't allow Dijkstra optimization

**Common mistake scenarios:**

- Using Bellman-Ford when Dijkstra works → Much slower
- Relaxing from unreachable nodes → dist[u] + w with dist[u]=inf is problematic
- Forgetting to copy array in limited-edges variant → Wrong answers

**The "limited stops" variant trap:**

```
Problem: Cheapest flights with at most K stops

WRONG approach:
for i in range(k+1):
    for each edge (u,v,w):
        dist[v] = min(dist[v], dist[u] + w)
        # Problem: dist[u] might have JUST been updated this round!

CORRECT approach:
for i in range(k+1):
    temp = dist.copy()  # Use previous round's values
    for each edge (u,v,w):
        dist[v] = min(dist[v], temp[u] + w)
```

---

## Interview Context

**FANG Context**: Bellman-Ford is rarely asked directly as a full implementation problem in top tech interviews. It's almost always a follow-up question. The typical pattern is:
- **Interviewer**: "Solve this shortest path problem." (You use BFS or Dijkstra)
- **Interviewer**: "Great. What if the edge weights could be negative?" (You answer: "Dijkstra fails because it relies on optimal substructure. I'd need Bellman-Ford, which runs in O(VE).")

However, understanding the *mechanics* of Bellman-Ford (iterating over all edges $k$ times) is crucial for constrained shortest path problems, like **Cheapest Flights Within K Stops**. That problem is fundamentally a Bellman-Ford variant.

Bellman-Ford is important because:

1. **Handles negative edges**: Unlike Dijkstra
2. **Detects negative cycles**: Returns error if unreachable minimum
3. **Simpler implementation**: Just iterate over all edges
4. **Less common in interviews**: But important to know for completeness

If an interviewer says "edges can be negative", Bellman-Ford is your answer.

---

## Core Concept

Bellman-Ford finds shortest paths by **relaxing all edges V-1 times**. After V-1 iterations, all shortest paths are found (if no negative cycle).

**Relaxation**: If `dist[u] + weight(u,v) < dist[v]`, update `dist[v]`.

```
Why V-1 iterations?
- Shortest path has at most V-1 edges
- Each iteration guarantees at least one more edge is correctly set
- After V-1 iterations, paths of length V-1 are correct
```

---

## Algorithm Template

### Python

---

## Visual Walkthrough

```
Graph:
  0 --4--> 1
  |        |
  5       -3
  |        |
  v        v
  2 --4--> 3

Initial: dist = [0, ∞, ∞, ∞]

Iteration 1 (relax all edges):
  0→1: dist[1] = min(∞, 0+4) = 4
  0→2: dist[2] = min(∞, 0+5) = 5
  1→2: dist[2] = min(5, 4+(-3)) = 1
  2→3: dist[3] = min(∞, 5+4) = 9  [but 2's dist changes]
       Need to recalculate in next iteration

Iteration 2:
  0→1: no change (4 ≤ 0+4)
  0→2: no change (1 < 0+5)
  1→2: no change (1 ≤ 4-3)
  2→3: dist[3] = min(9, 1+4) = 5

Iteration 3: No changes → terminate early

Final: dist = [0, 4, 1, 5]

Path to 3: 0 → 1 → 2 → 3 (cost: 4 + (-3) + 4 = 5)
```

---

## Negative Cycle Detection

```python
def has_negative_cycle(n: int, edges: list[list[int]]) -> bool:
    """
    Check if graph has a negative cycle.

    Time: O(V × E)
    Space: O(V)
    """
    dist = [0] * n  # Start with 0 to detect any negative cycle

    # Relax V-1 times
    for _ in range(n - 1):
        for u, v, w in edges:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w

    # One more relaxation - if anything changes, negative cycle exists
    for u, v, w in edges:
        if dist[u] + w < dist[v]:
            return True

    return False
```

---

## Finding the Negative Cycle

```python
def find_negative_cycle(n: int, edges: list[list[int]]) -> list[int]:
    """
    Find and return nodes in a negative cycle.

    Returns empty list if no negative cycle.
    """
    dist = [0] * n
    parent = [-1] * n

    # Track which node gets updated in the Vth iteration
    cycle_node = -1

    for i in range(n):
        cycle_node = -1
        for u, v, w in edges:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                parent[v] = u
                cycle_node = v

    if cycle_node == -1:
        return []  # No negative cycle

    # Go back n times to ensure we're in the cycle
    for _ in range(n):
        cycle_node = parent[cycle_node]

    # Collect cycle
    cycle = []
    current = cycle_node
    while True:
        cycle.append(current)
        current = parent[current]
        if current == cycle_node:
            cycle.append(current)
            break

    return cycle[::-1]
```

---

## SPFA: Optimized Bellman-Ford

Shortest Path Faster Algorithm - uses queue to only process updated nodes:

```python
from collections import deque

def spfa(n: int, edges: list[list[int]], source: int) -> list[float]:
    """
    SPFA: Optimized Bellman-Ford with queue.

    Time: O(V × E) worst case, often O(E) in practice
    Space: O(V)
    """
    graph = defaultdict(list)
    for u, v, w in edges:
        graph[u].append((v, w))

    dist = [float('inf')] * n
    dist[source] = 0
    in_queue = [False] * n
    count = [0] * n  # For cycle detection

    queue = deque([source])
    in_queue[source] = True

    while queue:
        u = queue.popleft()
        in_queue[u] = False

        for v, w in graph[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w

                if not in_queue[v]:
                    queue.append(v)
                    in_queue[v] = True
                    count[v] += 1

                    if count[v] >= n:
                        return None  # Negative cycle

    return dist
```

---

## Comparison: Dijkstra vs Bellman-Ford

| Aspect                   | Dijkstra             | Bellman-Ford              |
| ------------------------ | -------------------- | ------------------------- |
| Time                     | O((V+E) log V)       | O(V × E)                  |
| Space                    | O(V)                 | O(V)                      |
| Strategy                 | Greedy exploration   | Exhaustive relaxation     |
| Negative edges           | No                   | Yes                       |
| Negative cycle detection | No                   | Yes                       |
| Implementation           | Heap-based           | Simple nested iteration   |
| When to use              | Non-negative weights | Negative weights possible |

---

## Complexity: Deep Dive

**Time Complexity: O(V × E)**

```
Proof:
1. Outer Loop: Runs exactly V - 1 times.
2. Inner Loop: Iterates over all E edges.
3. Total Time = (V - 1) * E = O(V * E)

Note on SPFA variation:
Using a queue (SPFA) dramatically improves the average case time complexity to O(E),
as only nodes with updated distances are pushed to the queue to relax their neighbors.
However, in the worst case (e.g., highly crafted dense graphs or bellman-ford killer graphs),
SPFA still degrades to O(V × E).
```

**Space Complexity: O(V)**

```
Proof:
1. We only need a `dist` array of size V to store the shortest distance to each node.
2. The algorithm doesn't require an adjacency list or any complex data structures;
   it just iterates directly over the `edges` list.
3. Total Space = O(V)

Note: For the "cheapest flights with K stops" variation, we might need O(V) extra space
for a `temp` array during edge relaxation. It remains O(V) overall.
```

---

## Cheapest Flights with K Stops (Bellman-Ford Variant)

```python
def find_cheapest_price_bf(n: int, flights: list[list[int]],
                            src: int, dst: int, k: int) -> int:
    """
    Find cheapest price with at most k stops using Bellman-Ford variant.

    Limit iterations to k+1 (at most k stops = k+1 edges).

    Time: O(k × E)
    Space: O(V)
    """
    dist = [float('inf')] * n
    dist[src] = 0

    for _ in range(k + 1):  # At most k+1 edges
        temp = dist[:]  # Use previous iteration's values

        for u, v, price in flights:
            if temp[u] != float('inf'):
                dist[v] = min(dist[v], temp[u] + price)

    return dist[dst] if dist[dst] != float('inf') else -1
```

---

## When to Use Each Algorithm

| Scenario                            | Algorithm                            |
| ----------------------------------- | ------------------------------------ |
| Non-negative weights                | Dijkstra (faster)                    |
| Negative weights, no negative cycle | Bellman-Ford                         |
| Need to detect negative cycle       | Bellman-Ford                         |
| Limited hops/stops                  | Bellman-Ford with limited iterations |
| Dense graph, non-negative           | Dijkstra                             |
| Sparse graph, any weights           | Bellman-Ford                         |

---

## Edge Cases

```python
# 1. No edges
n = 3, edges = []
# Only source reachable

# 2. Negative self-loop
edges = [[0, 0, -1]]
# Negative cycle at node 0

# 3. Disconnected graph
# Unreachable nodes have infinity distance

# 4. All negative edges (no cycle)
edges = [[0, 1, -2], [1, 2, -3]]
# Valid shortest paths with negative weights

# 5. Negative cycle not reachable from source
# Shortest paths still valid for reachable nodes
```

---

## Common Mistakes

```python
# WRONG: Not using previous iteration's values
for _ in range(n - 1):
    for u, v, w in edges:
        dist[v] = min(dist[v], dist[u] + w)
        # Problem: dist[u] might have just changed!

# CORRECT for limited edges problem:
for _ in range(k + 1):
    temp = dist[:]  # Copy previous state
    for u, v, w in edges:
        dist[v] = min(dist[v], temp[u] + w)

# Note: For standard Bellman-Ford, updating in-place is fine
# because we do V-1 iterations. But for limited hops, must copy.


# WRONG: Relaxing from unreachable nodes
if dist[u] + w < dist[v]:  # dist[u] might be infinity!
    dist[v] = dist[u] + w  # inf + w is still inf (or overflow)

# CORRECT: Check if source is reachable
if dist[u] != float('inf') and dist[u] + w < dist[v]:
    dist[v] = dist[u] + w
```

---

## Interview Tips

1. **Know when to use**: Negative edges → Bellman-Ford
2. **V-1 iterations**: Maximum path length in graph
3. **Cycle detection**: One more iteration after V-1
4. **Limited hops variant**: Use temp array for each iteration
5. **Simple to implement**: Just nested loops over edges

---

## Practice Problems

| #   | Problem                         | Difficulty | Key Variation         |
| --- | ------------------------------- | ---------- | --------------------- |
| 1   | Cheapest Flights Within K Stops | Medium     | Limited iterations    |
| 2   | Network Delay Time              | Medium     | Can use either        |
| 3   | Negative Cycle Detection        | Medium     | Extra iteration       |
| 4   | Path with Minimum Effort        | Medium     | Binary search variant |

---

## Key Takeaways

1. **O(V × E) time**: Slower than Dijkstra but handles negative edges
2. **V-1 iterations**: Each iteration sets one more edge correctly
3. **Vth iteration for cycles**: Any update means negative cycle
4. **Use copy for limited hops**: Prevent using same-iteration updates
5. **SPFA optimization**: Queue-based, faster in practice

---

## Next: [11-shortest-path-unweighted.md](./11-shortest-path-unweighted.md)

Review BFS for shortest path in unweighted graphs.

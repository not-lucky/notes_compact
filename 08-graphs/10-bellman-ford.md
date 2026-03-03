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

**Why exactly V-1 iterations?**

A shortest path in a graph with V vertices can use at most V-1 edges (otherwise it
revisits a vertex, forming a cycle — which can't be part of a shortest path unless
the cycle has negative weight).

```
Key insight: Iteration i guarantees correctness for all shortest paths using ≤ i edges.

Proof by induction:
  Base case (i=0): dist[source] = 0 is correct (0 edges).
  Inductive step: If all paths with ≤ i edges are correct after iteration i,
    then iteration i+1 relaxes every edge (u,v), so any shortest path using
    i+1 edges (optimal prefix of i edges + one more edge) will be found.
  After V-1 iterations: All shortest paths with ≤ V-1 edges are correct.
  Since no shortest path needs more than V-1 edges → all shortest paths are correct.
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
If a path keeps getting shorter after V-1 iterations, there must be a cycle with negative total weight — you can loop forever getting cheaper.

```
Negative cycle detection:
After V-1 iterations: All finite shortest paths are found
At iteration V: If ANY edge can still be relaxed → negative cycle exists

Why? A shortest path has at most V-1 edges. If we can still improve,
we're using more than V-1 edges → must be cycling through a negative-weight loop!
```

---

## When NOT to Use

**Don't use Bellman-Ford when:**

- **All weights are non-negative** → Dijkstra is O((V+E) log V) vs O(VE)
- **Graph is unweighted** → BFS is O(V+E), much faster
- **Need to process dynamically** → Not designed for updates

**Bellman-Ford is the only choice when:**

- Negative edge weights exist (Dijkstra fails)
- Need to detect negative cycles
- Need shortest paths with a limited number of edges (K-stops variant)

**Common mistake scenarios:**

- Using Bellman-Ford when Dijkstra works → Much slower
- Relaxing from unreachable nodes → `dist[u] + w` with `dist[u] = inf` is problematic
- Forgetting to copy array in limited-edges variant → Wrong answers

**The "limited stops" variant trap:**

```
Problem: Cheapest flights with at most K stops

WRONG approach:
for i in range(k+1):
    for u, v, w in edges:
        if dist[u] != float('inf'):
            dist[v] = min(dist[v], dist[u] + w)
        # Problem: dist[u] might have JUST been updated this round!
        # This allows paths with more than k+1 edges.

CORRECT approach:
for i in range(k+1):
    temp = dist.copy()  # Freeze previous round's values
    for u, v, w in edges:
        if temp[u] != float('inf'):
            dist[v] = min(dist[v], temp[u] + w)
```

---

## Interview Context

**FANG Context**: Bellman-Ford is rarely asked directly as a full implementation problem in top tech interviews. It's almost always a follow-up question. The typical pattern is:
- **Interviewer**: "Solve this shortest path problem." (You use BFS or Dijkstra)
- **Interviewer**: "Great. What if the edge weights could be negative?" (You answer: "Dijkstra fails because it relies on optimal substructure. I'd need Bellman-Ford, which runs in O(VE).")

However, understanding the *mechanics* of Bellman-Ford (iterating over all edges k times) is crucial for constrained shortest path problems, like **Cheapest Flights Within K Stops**. That problem is fundamentally a Bellman-Ford variant.

Bellman-Ford is important because:

1. **Handles negative edges**: Unlike Dijkstra
2. **Detects negative cycles**: One extra iteration reveals them
3. **Simpler implementation**: Just nested loops over edges — no heap needed
4. **K-stops variant**: Directly solves constrained shortest-path problems

If an interviewer says "edges can be negative", Bellman-Ford is your answer.

---

## Core Concept

Bellman-Ford finds shortest paths by **relaxing all edges V-1 times**. After V-1 iterations, all shortest paths are found (if no negative cycle).

**Relaxation**: If `dist[u] + weight(u,v) < dist[v]`, update `dist[v]`.

```
Why V-1 iterations?
- A shortest path visits each vertex at most once → at most V-1 edges.
- Iteration i correctly computes all shortest paths with ≤ i edges.
- After V-1 iterations, all possible shortest paths are correct.

Early termination optimization:
- If no distance changes during an entire iteration, all paths are finalized.
- Break early to save time (best case: O(E) instead of O(VE)).
```

---

## Algorithm Template

```python
def bellman_ford(n: int, edges: list[list[int]], source: int) -> list[float]:
    """
    Find shortest distances from source to all vertices.

    Args:
        n: Number of vertices (0-indexed).
        edges: List of [u, v, weight] directed edges.
        source: Starting vertex.

    Returns:
        List of shortest distances. float('inf') for unreachable vertices.
        Raises ValueError if a negative cycle is reachable from source.

    Time:  O(V * E)
    Space: O(V)
    """
    dist = [float('inf')] * n
    dist[source] = 0

    # Relax all edges V-1 times
    for _ in range(n - 1):
        updated = False  # Track if any relaxation happened this round
        for u, v, w in edges:
            if dist[u] != float('inf') and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                updated = True

        # Early termination: no updates means all shortest paths are finalized
        if not updated:
            break

    # V-th iteration: check for negative cycles
    for u, v, w in edges:
        if dist[u] != float('inf') and dist[u] + w < dist[v]:
            raise ValueError("Graph contains a negative-weight cycle reachable from source")

    return dist
```

---

## Visual Walkthrough

```
Graph (directed edges with weights):
  0 --4--> 1
  |        |
  5       -3
  |        |
  v        v
  2 <------+
  |
  4
  |
  v
  3

Edges: (0→1, w=4), (0→2, w=5), (1→2, w=-3), (2→3, w=4)

Initial: dist = [0, ∞, ∞, ∞]

Iteration 1 (relax all edges):
  0→1: dist[1] = min(∞, 0+4) = 4     ✓ updated
  0→2: dist[2] = min(∞, 0+5) = 5     ✓ updated
  1→2: dist[2] = min(5, 4+(-3)) = 1  ✓ updated (negative edge helps!)
  2→3: dist[3] = min(∞, 1+4) = 5     ✓ updated
  dist = [0, 4, 1, 5]

Iteration 2 (relax all edges again):
  0→1: no change (4 ≤ 0+4)
  0→2: no change (1 ≤ 0+5)
  1→2: no change (1 ≤ 4-3)
  2→3: no change (5 ≤ 1+4)
  No updates → early termination!

Final: dist = [0, 4, 1, 5]

Path to 3: 0 → 1 → 2 → 3 (cost: 4 + (-3) + 4 = 5)
Note: Direct 0→2→3 would cost 5+4=9. Going through the negative edge is cheaper!
```

**Note on in-place relaxation**: In standard Bellman-Ford, we relax in-place (updating
`dist` directly). This means within a single iteration, a later edge relaxation can
use a value just updated by an earlier edge in the same iteration. This is fine — it
can only speed up convergence. The V-1 iteration guarantee still holds. However, for
the K-stops variant, we must use a copy to prevent using more edges than allowed.

---

## Negative Cycle Detection

```python
def has_negative_cycle(n: int, edges: list[list[int]]) -> bool:
    """
    Check if graph contains any negative cycle.

    Initializes all distances to 0 (as if there were a virtual source connected
    to every node with weight 0). This detects negative cycles anywhere in the
    graph, not just those reachable from a single source.

    Time: O(V * E)
    Space: O(V)
    """
    dist = [0] * n  # Start with 0 to detect any negative cycle

    # Relax V-1 times
    for _ in range(n - 1):
        for u, v, w in edges:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w

    # V-th relaxation: if anything changes, negative cycle exists
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
    Find and return the nodes forming a negative cycle.

    Returns empty list if no negative cycle exists.

    Strategy:
    1. Run V iterations (not V-1). Track parent pointers.
    2. If any edge relaxes on iteration V, that destination node
       is either in or downstream of a negative cycle.
    3. Walk back through parent pointers V times to guarantee
       we land inside the cycle.
    4. Trace the cycle from that node.
    """
    dist = [0] * n
    parent = [-1] * n
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

    # Walk back n times to ensure we're inside the cycle
    # (cycle_node might be downstream of the cycle, not in it)
    node = cycle_node
    for _ in range(n):
        node = parent[node]

    # Now 'node' is guaranteed to be inside the cycle — trace it
    cycle = []
    current = node
    while True:
        cycle.append(current)
        current = parent[current]
        if current == node:
            cycle.append(current)  # Close the cycle
            break

    return cycle[::-1]
```

---

## Classic Application: Currency Arbitrage

A very common FAANG interview question (especially at Fintech companies or trading firms) asks you to find a **currency arbitrage** opportunity.

**The Problem**: Given a list of currencies and exchange rates (e.g., 1 USD = 0.93 EUR, 1 EUR = 0.85 GBP), can you start with 1 unit of a currency, make a series of trades, and end up with *more* than 1 unit of that same currency?

**The Math**:
We are looking for a cycle of exchange rates $R_1, R_2, ..., R_k$ such that:
$$R_1 \times R_2 \times ... \times R_k > 1$$

Graph algorithms typically *minimize sums*, not *maximize products*. We can convert a product to a sum using logarithms:
$$\log(R_1) + \log(R_2) + ... + \log(R_k) > \log(1) = 0$$

To make this a minimization problem, multiply by $-1$:
$$(-\log R_1) + (-\log R_2) + ... + (-\log R_k) < 0$$

**The Solution**:
1. Represent currencies as vertices.
2. Represent an exchange rate from currency $A$ to $B$ as a directed edge with weight $-\log(\text{rate})$.
3. Run **Bellman-Ford** to detect a negative-weight cycle.
4. If a negative cycle exists, an arbitrage opportunity exists! You can use the `find_negative_cycle` logic to return the exact sequence of trades.

---

## SPFA: Optimized Bellman-Ford

Shortest Path Faster Algorithm — uses a queue to only re-relax nodes whose
distances actually changed, avoiding redundant work on unchanged nodes:

```python
from collections import defaultdict, deque


def spfa(n: int, edges: list[list[int]], source: int) -> list[float]:
    """
    SPFA: Queue-optimized Bellman-Ford.

    Instead of blindly iterating over all edges V-1 times, SPFA maintains a
    queue of "active" nodes whose distances recently improved. Only their
    outgoing edges are relaxed. This is often much faster in practice.

    Negative cycle detection: if any node enters the queue ≥ V times,
    a negative cycle exists (a node's distance keeps decreasing).

    Args:
        n: Number of vertices.
        edges: List of [u, v, weight] directed edges.
        source: Starting vertex.

    Returns:
        List of shortest distances.
        Raises ValueError if a negative cycle is detected.

    Time:  O(V × E) worst case, often O(E) in practice
    Space: O(V + E) for adjacency list and queue
    """
    # Build adjacency list
    graph: dict[int, list[tuple[int, int]]] = defaultdict(list)
    for u, v, w in edges:
        graph[u].append((v, w))

    dist = [float('inf')] * n
    dist[source] = 0
    in_queue = [False] * n
    enqueue_count = [0] * n  # How many times each node entered the queue

    queue: deque[int] = deque([source])
    in_queue[source] = True
    enqueue_count[source] = 1

    while queue:
        u = queue.popleft()
        in_queue[u] = False

        for v, w in graph[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w

                if not in_queue[v]:
                    queue.append(v)
                    in_queue[v] = True
                    enqueue_count[v] += 1

                    # A node entering the queue V times means negative cycle
                    if enqueue_count[v] >= n:
                        raise ValueError("Graph contains a negative-weight cycle")

    return dist
```

---

## Comparison: Dijkstra vs Bellman-Ford

| Aspect                   | Dijkstra               | Bellman-Ford               |
| ------------------------ | ---------------------- | -------------------------- |
| **Time**                 | O((V+E) log V)         | O(V × E)                   |
| **Space**                | O(V + E)               | O(V + E)                   |
| **Strategy**             | Greedy (min-heap)      | Exhaustive relaxation      |
| **Negative edges**       | Fails                  | Handles correctly          |
| **Negative cycles**      | Cannot detect          | Detects via Vth iteration  |
| **Implementation**       | Heap + adjacency list  | Simple nested loops        |
| **Best for**             | Non-negative weights   | Negative weights / K-stops |
| **Early termination**    | When dest is popped    | When no updates in a round |
| **Data structure input** | Adjacency list         | Edge list                  |

**Space note**: Both algorithms are O(V) for the distance array alone. Dijkstra also
needs an adjacency list and heap. Bellman-Ford can work directly on an edge list
(O(E) to store it), but SPFA needs an adjacency list too. In practice, both are O(V+E).

---

## Complexity: Deep Dive

**Time Complexity: O(V × E)**

```
Breakdown:
1. Outer loop: Runs exactly V-1 times (or fewer with early termination).
2. Inner loop: Iterates over all E edges each time.
3. Total: (V-1) × E = O(V × E)

For dense graphs (E ≈ V²): O(V³) — very slow.
For sparse graphs (E ≈ V):  O(V²) — comparable to simple Dijkstra.

SPFA optimization:
- Average case often O(E) because most nodes don't need repeated updates.
- Worst case still O(V × E) — adversarial inputs can force it.
- Competitive programming has known "SPFA killer" test cases.
```

**Space Complexity: O(V)**

```
1. dist array: O(V) to store shortest distances.
2. The algorithm iterates over the edge list directly — no extra graph storage needed
   (the edge list is part of the input, not extra space).
3. For K-stops variant: one additional temp array of size V → still O(V).
4. For SPFA: additional queue and in_queue/count arrays → O(V), plus adjacency list O(E).
```

---

## Cheapest Flights with K Stops (Bellman-Ford Variant)

This is the most common Bellman-Ford problem in FANG interviews (LeetCode 787).

```python
def find_cheapest_price(
    n: int,
    flights: list[list[int]],
    src: int,
    dst: int,
    k: int,
) -> int:
    """
    Find cheapest price from src to dst with at most k stops.

    Key insight: k stops = at most k+1 edges. Run Bellman-Ford for exactly
    k+1 iterations, using a temp copy each round to prevent "chaining"
    updates within the same iteration (which would allow more edges than k+1).

    Time:  O(k × E) where E = len(flights)
    Space: O(V)
    """
    dist = [float('inf')] * n
    dist[src] = 0

    for _ in range(k + 1):  # Exactly k+1 iterations for k stops
        temp = dist[:]  # CRITICAL: snapshot of previous round

        for u, v, price in flights:
            if temp[u] != float('inf') and temp[u] + price < dist[v]:
                dist[v] = temp[u] + price

    return int(dist[dst]) if dist[dst] != float('inf') else -1
```

---

## When to Use Each Algorithm

| Scenario                            | Algorithm                            |
| ----------------------------------- | ------------------------------------ |
| Non-negative weights                | Dijkstra (faster)                    |
| Negative weights, no negative cycle | Bellman-Ford                         |
| Need to detect negative cycles      | Bellman-Ford                         |
| Limited hops/stops                  | Bellman-Ford with limited iterations |
| Unweighted graph                    | BFS (fastest)                        |
| All-pairs shortest paths            | Floyd-Warshall or repeated Dijkstra  |

---

## Edge Cases

1. **No edges**: `n = 3, edges = []`. Only the source is reachable (`dist=0`), all others are `inf`.
2. **Negative self-loop**: `edges = [[0, 0, -1]]`. A negative cycle at node 0.
3. **Disconnected graph**: Unreachable nodes stay at `float('inf')`.
4. **All negative edges (no cycle)**: `edges = [[0, 1, -2], [1, 2, -3]]`. Valid shortest paths exist: `dist = [0, -2, -5]`.
5. **Negative cycle not reachable from source**: Standard Bellman-Ford (from a source) won't detect it. Use `has_negative_cycle()` with `dist=[0]*n` to detect cycles anywhere.
6. **Parallel edges**: Multiple edges between the same pair are handled naturally — all are relaxed.
7. **Negative Cycle found**: You return early, raise ValueError or throw an Exception.

---

## Common Mistakes

1. **Not copying `dist` in the K-stops variant**
   - Standard Bellman-Ford updates in-place, meaning a value updated in iteration $k$ can immediately be used to update another value in the same iteration. This is usually fine (faster convergence).
   - But for "at most K stops", you *must* restrict paths to exactly $k+1$ edges. Using in-place updates could allow a path of length $k+2$ to form in iteration $k$.
   - **Fix**: Use `temp = dist[:]` at the start of each iteration, and always read from `temp` while writing to `dist`.

2. **Relaxing from unreachable nodes**
   - In Python, `float('inf') + (-5)` is still `float('inf')`. However, checking `if dist[u] != float('inf')` avoids meaningless updates and prevents subtle bugs in languages where `INT_MAX + (-5)` might cause underflow or incorrect comparisons.

3. **Confusing "V-1 iterations" with "V iterations"**
   - The loop for finding shortest paths runs **V-1 times**.
   - The check for negative cycles is **one extra iteration (the V-th)**.

4. **Assuming early termination means no negative cycles**
   - If no edges relax in iteration $k < V-1$, you can stop early; there are definitively no negative cycles.
   - However, if updates *do* continue all the way to iteration $V-1$, you *must* run the $V$-th iteration to confirm if a negative cycle exists.

---

## Interview Tips

1. **Know when to use**: Negative edges → Bellman-Ford. Non-negative → Dijkstra.
2. **V-1 iterations**: The maximum number of edges in any shortest path.
3. **Cycle detection**: One extra (Vth) iteration — if any edge relaxes, there's a negative cycle.
4. **Limited hops variant**: Use `temp = dist[:]` each iteration. This is the most common interview application.
5. **Simple to code**: Just nested loops over an edge list — no heap, no adjacency list.
6. **Complexity comparison**: O(VE) vs Dijkstra's O((V+E) log V). Bellman-Ford is slower but more general.

---

## Practice Problems

| #   | Problem                                               | Difficulty | Key Concept                     | Hint                                                           |
| --- | ----------------------------------------------------- | ---------- | ------------------------------- | -------------------------------------------------------------- |
| 1   | [787. Cheapest Flights Within K Stops][lc787]         | Medium     | K-stops Bellman-Ford variant    | Run k+1 iterations with `temp = dist[:]` each round.          |
| 2   | [743. Network Delay Time][lc743]                      | Medium     | Standard shortest path          | Bellman-Ford or Dijkstra both work. Answer is `max(dist)`.     |
| 3   | [1334. Find the City With the Smallest Number of Neighbors at a Threshold Distance][lc1334] | Medium | All-pairs or repeated BF | Run Bellman-Ford from each city. Count reachable within threshold. |
| 4   | [1514. Path with Maximum Probability][lc1514]         | Medium     | Modified relaxation             | Maximize product instead of minimizing sum. Use log transform or flip comparison. |
| 5   | [505. The Maze II][lc505]                             | Medium     | Weighted shortest path          | Model as weighted graph, then apply Dijkstra or Bellman-Ford.  |

[lc787]: https://leetcode.com/problems/cheapest-flights-within-k-stops/
[lc743]: https://leetcode.com/problems/network-delay-time/
[lc1334]: https://leetcode.com/problems/find-the-city-with-the-smallest-number-of-neighbors-at-a-threshold-distance/
[lc1514]: https://leetcode.com/problems/path-with-maximum-probability/
[lc505]: https://leetcode.com/problems/the-maze-ii/

---

## Key Takeaways

1. **O(V × E) time**: Slower than Dijkstra but handles negative edges
2. **V-1 iterations**: Iteration i guarantees shortest paths using ≤ i edges
3. **Vth iteration for cycles**: Any relaxation at this point means a negative cycle exists
4. **Use copy for limited hops**: Prevent "chaining" updates that use extra edges
5. **SPFA optimization**: Queue-based, often O(E) in practice but O(VE) worst case
6. **Interview default**: If negative edges are mentioned, say "Bellman-Ford"

---

## Next: [11-shortest-path-unweighted.md](./11-shortest-path-unweighted.md)

Review BFS for shortest path in unweighted graphs.

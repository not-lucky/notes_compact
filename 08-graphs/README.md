# Chapter 08: Graphs

> **Prerequisites:** [01-complexity-analysis](../01-complexity-analysis/README.md), [05-stacks-queues](../05-stacks-queues/README.md), [07-heaps-priority-queues](../07-heaps-priority-queues/README.md) (for Dijkstra)
>
> Understanding Big-O and queue/stack operations is essential. Recursion knowledge is highly recommended for DFS. Heaps are needed for Dijkstra's algorithm.

## What Is a Graph?

A **graph** is a data structure consisting of **vertices** (nodes) and **edges** (connections between nodes). Graphs generalize trees, linked lists, and grids -- any structure where entities have relationships can be modeled as a graph.

- **Directed vs undirected**: Edges can be one-way (directed) or two-way (undirected).
- **Weighted vs unweighted**: Edges can carry costs/distances or not.
- **Cyclic vs acyclic**: Graphs may contain cycles. A directed acyclic graph (DAG) is especially important for dependency/ordering problems.
- **Dense vs sparse**: Dense graphs have edges close to V^2; sparse graphs have edges close to V. This affects which representation and algorithm to choose.

Many interview problems are **graph problems in disguise**: grids, word transformations, dependency chains, and social networks all map to graph traversals.

---

## Why This Matters for Interviews

Graphs are **among the most challenging and frequently tested topics** at FANG+ companies because:

1. **Versatile modeling**: Many real problems are graph problems in disguise
2. **Multiple algorithms**: BFS, DFS, Dijkstra, topological sort -- all fair game
3. **Pattern recognition**: Grid problems, implicit graphs, dependency resolution
4. **Complexity depth**: Tests both coding and algorithmic thinking
5. **Real applications**: Social networks, routing, dependencies, scheduling
6. **Theoretical foundations**: Understanding graph properties (e.g., bipartite theorems) and complexity analysis (V vs E, dense vs sparse)
7. **Implementation fluency**: Requires discussing trade-offs in representations (adjacency list vs matrix) and memory management

At FANG+ companies, expect at least one graph problem, often disguised as a grid or dependency problem.

**Interview frequency**: Very High. Graphs appear in 40-50% of technical interviews.

---

## Core Patterns to Master

| Pattern           | Frequency | Key Problems                                   |
| ----------------- | --------- | ---------------------------------------------- |
| BFS (Level-order) | Very High | Shortest path unweighted, multi-source BFS     |
| DFS (Traversal)   | Very High | Connected components, cycle detection          |
| Topological Sort  | High      | Course schedule, build order, alien dictionary  |
| Dijkstra          | High      | Shortest path weighted, network delay          |
| Grid BFS/DFS      | Very High | Number of islands, rotting oranges             |
| Cycle Detection   | High      | Directed and undirected graphs                 |
| Bipartite Check   | Medium    | Graph coloring, two-coloring                   |
| Union-Find        | High      | Connected components, redundant connection (see [Chapter 14](../14-union-find/README.md)) |

---

## Chapter Sections

### Phase 1: Foundations (Start Here)

| Section | Topic | Key Takeaway |
| ------- | ----- | ------------ |
| [01-graph-representations](./01-graph-representations.md) | Graph Representations | Adjacency list vs matrix vs edge list |
| [02-bfs-basics](./02-bfs-basics.md) | BFS Traversal | Level-order traversal, shortest path in unweighted graphs |
| [03-dfs-basics](./03-dfs-basics.md) | DFS Traversal | Recursive and iterative approaches |
| [04-connected-components](./04-connected-components.md) | Connected Components | Count and identify connected components |

### Phase 2: Core Algorithms

| Section | Topic | Key Takeaway |
| ------- | ----- | ------------ |
| [05-cycle-detection-directed](./05-cycle-detection-directed.md) | Directed Cycle Detection | Three-color DFS for directed graphs |
| [06-cycle-detection-undirected](./06-cycle-detection-undirected.md) | Undirected Cycle Detection | Parent tracking for undirected graphs |
| [07-topological-sort](./07-topological-sort.md) | Topological Sort | Kahn's (BFS) and DFS-based approaches |
| [09-dijkstra](./09-dijkstra.md) | Dijkstra's Algorithm | Shortest path in weighted graphs (non-negative edges) |
| [11-shortest-path-unweighted](./11-shortest-path-unweighted.md) | Unweighted Shortest Path | BFS as shortest path algorithm |
| [10-bellman-ford](./10-bellman-ford.md) | Bellman-Ford Algorithm | Shortest path with negative edges |

### Phase 3: Interview Problems

| Section | Topic | Key Takeaway |
| ------- | ----- | ------------ |
| [08-course-schedule](./08-course-schedule.md) | Course Schedule Problems | Classic topological sort application |
| [12-clone-graph](./12-clone-graph.md) | Clone Graph | Deep copy with hash map for visited tracking |
| [13-grid-problems](./13-grid-problems.md) | Grid as Graph (Islands, Flood Fill) | Treat 2D grids as implicit graphs |
| [14-rotting-oranges](./14-rotting-oranges.md) | Rotting Oranges (Multi-Source BFS) | Simultaneous BFS expansion from multiple sources |
| [15-word-ladder](./15-word-ladder.md) | Word Ladder (Implicit Graph) | BFS over implicit word-transformation graph |
| [16-bipartite-check](./16-bipartite-check.md) | Bipartite Check (Graph Coloring) | Two-coloring via BFS or DFS |
| [17-alien-dictionary](./17-alien-dictionary.md) | Alien Dictionary | Topological sort from ordering constraints |
| [18-network-delay](./18-network-delay.md) | Network Delay Time | Dijkstra application for single-source shortest path |

---

## Suggested Study Order

```
Phase 1 - Foundations (do these first, in order):
  01 Graph Representations  -->  02 BFS Basics  -->  03 DFS Basics  -->  04 Connected Components

Phase 2 - Core Algorithms (build on foundations):
  05 Cycle Detection (Directed)  -->  06 Cycle Detection (Undirected)
  07 Topological Sort
  11 Shortest Path (Unweighted)  -->  09 Dijkstra  -->  10 Bellman-Ford

Phase 3 - Interview Problems (apply the algorithms):
  08 Course Schedule           (uses: topological sort)
  12 Clone Graph               (uses: BFS/DFS + hash map)
  13 Grid Problems             (uses: BFS/DFS on grids)
  14 Rotting Oranges            (uses: multi-source BFS)
  15 Word Ladder                (uses: BFS on implicit graph)
  16 Bipartite Check            (uses: BFS/DFS coloring)
  17 Alien Dictionary           (uses: topological sort)
  18 Network Delay Time         (uses: Dijkstra)
```

Work through Phase 1 completely before moving on. Within Phase 2, cycle detection and topological sort form one track, while shortest path algorithms form another -- these two tracks can be studied in parallel. Phase 3 problems can be tackled in any order once you have the relevant algorithm from Phase 2.

---

## Common Mistakes Interviewers Watch For

1. **Forgetting visited set**: Infinite loops in cyclic graphs
2. **Wrong traversal choice**: BFS for shortest path, DFS for exhaustive search
3. **Directed vs undirected confusion**: Cycle detection differs significantly
4. **Not handling disconnected graphs**: Must iterate over all nodes
5. **Grid bounds checking**: Off-by-one errors with rows/cols
6. **Dijkstra with negative weights**: Use Bellman-Ford instead
7. **Topological sort on cyclic graph**: Must detect and handle cycles

---

## Time Targets

| Difficulty | Target Time | Examples                                      |
| ---------- | ----------- | --------------------------------------------- |
| Easy       | 10-15 min   | Flood Fill, Number of Islands                 |
| Medium     | 15-25 min   | Course Schedule, Clone Graph, Rotting Oranges |
| Hard       | 25-40 min   | Alien Dictionary, Word Ladder, Network Delay  |

---

## Pattern Recognition Guide

```
"Shortest path, unweighted..."       -> BFS
"Shortest path, weighted..."         -> Dijkstra (or Bellman-Ford if negative edges)
"All paths/permutations..."          -> DFS/Backtracking
"Dependencies/ordering..."           -> Topological Sort
"Connected/grouped..."               -> Union-Find or DFS
"Grid traversal..."                  -> BFS or DFS (grid as implicit graph)
"Level-by-level..."                  -> BFS
"Cycle detection..."                 -> DFS with colors (directed) or parent (undirected)
"Two groups/coloring..."             -> Bipartite check (BFS/DFS)
"Minimum cost/distance..."           -> Dijkstra or BFS depending on weights
```

---

## Quick Reference: Graph Representations

```python
# Adjacency List (most common in interviews)
# using Dict and List for typing: Dict[int, List[int]]
graph = {
    0: [1, 2],
    1: [0, 3],
    2: [0],
    3: [1]
}

# Adjacency Matrix (good for dense graphs)
# Rows represent source node, columns represent destination node
matrix = [
    [0, 1, 1, 0],  # Edges from 0 to 1, 2
    [1, 0, 0, 1],  # Edges from 1 to 0, 3
    [1, 0, 0, 0],  # Edges from 2 to 0
    [0, 1, 0, 0]   # Edges from 3 to 1
]

# Edge List (good for Bellman-Ford, Kruskal's)
# Usually includes weights: (u, v, weight)
edges = [(0, 1, 5), (0, 2, 3), (1, 3, 2)]
```

---

## Key Complexity Facts

| Algorithm        | Time             | Space | Notes                     |
| ---------------- | ---------------- | ----- | ------------------------- |
| BFS              | O(V + E)         | O(V)  | Queue + visited           |
| DFS              | O(V + E)         | O(V)  | Stack/recursion + visited |
| Dijkstra (heap)  | O((V + E) log V) | O(V)  | Priority queue            |
| Bellman-Ford     | O(V * E)         | O(V)  | Edge relaxation           |
| Topological Sort | O(V + E)         | O(V)  | Kahn's or DFS             |
| Union-Find       | O(a(n)) per op   | O(V)  | Nearly constant (inverse Ackermann) |
| Bipartite Check  | O(V + E)         | O(V)  | Two-coloring (BFS or DFS) |

V = vertices, E = edges

---

## BFS vs DFS Quick Reference

| Aspect         | BFS                        | DFS                                |
| -------------- | -------------------------- | ---------------------------------- |
| Data structure | Queue                      | Stack/Recursion                    |
| Explores       | Level by level             | Depth first                        |
| Shortest path  | Yes (unweighted)           | No                                 |
| Space          | O(width)                   | O(height)                          |
| Use when       | Shortest path, level-order | Exhaustive search, cycle detection |

---

## Next Steps

After completing this chapter, continue to [09-dynamic-programming](../09-dynamic-programming/README.md). Graph concepts also connect strongly to [14-union-find](../14-union-find/README.md), which provides an alternative approach for connected component problems.

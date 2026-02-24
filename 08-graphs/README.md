# Chapter 08: Graphs

## Why This Matters for Interviews

Graphs are **among the most challenging and frequently tested topics** at FANG+ companies because:

1. **Versatile modeling**: Many real problems are graph problems in disguise
2. **Multiple algorithms**: BFS, DFS, Dijkstra, topological sort — all fair game
3. **Pattern recognition**: Grid problems, implicit graphs, dependency resolution
4. **Complexity depth**: Tests both coding and algorithmic thinking
5. **Real applications**: Social networks, routing, dependencies, scheduling

At FANG+ companies, expect at least one graph problem, often disguised as a grid or dependency problem.

**Interview frequency**: Very High. Graphs appear in 40-50% of technical interviews.

---

## Core Patterns to Master

| Pattern           | Frequency | Key Problems                                   |
| ----------------- | --------- | ---------------------------------------------- |
| BFS (Level-order) | Very High | Shortest path unweighted, multi-source BFS     |
| DFS (Traversal)   | Very High | Connected components, cycle detection          |
| Topological Sort  | High      | Course schedule, build order, alien dictionary |
| Dijkstra          | High      | Shortest path weighted, network delay          |
| Grid BFS/DFS      | Very High | Number of islands, rotting oranges             |
| Cycle Detection   | High      | Directed and undirected graphs                 |
| Bipartite Check   | Medium    | Graph coloring, two-coloring                   |
| Union-Find        | High      | Connected components, redundant connection     |

---

## Chapter Sections

| Section                                                             | Topic                    | Key Takeaway                          |
| ------------------------------------------------------------------- | ------------------------ | ------------------------------------- |
| [01-graph-representations](./01-graph-representations.md)           | Graph Basics             | Adjacency list vs matrix              |
| [02-bfs-basics](./02-bfs-basics.md)                                 | BFS Traversal            | Level-order, shortest path unweighted |
| [03-dfs-basics](./03-dfs-basics.md)                                 | DFS Traversal            | Recursive and iterative               |
| [04-connected-components](./04-connected-components.md)             | Components               | Count and find connected components   |
| [05-cycle-detection-directed](./05-cycle-detection-directed.md)     | Directed Cycle           | Three-color DFS for directed graphs   |
| [06-cycle-detection-undirected](./06-cycle-detection-undirected.md) | Undirected Cycle         | Parent tracking for undirected graphs |
| [07-topological-sort](./07-topological-sort.md)                     | Topological Sort         | Kahn's algorithm, DFS-based           |
| [08-course-schedule](./08-course-schedule.md)                       | Course Schedule          | Classic topological sort application  |
| [09-dijkstra](./09-dijkstra.md)                                     | Dijkstra's Algorithm     | Shortest path weighted (positive)     |
| [10-bellman-ford](./10-bellman-ford.md)                             | Bellman-Ford             | Shortest path with negative edges     |
| [11-shortest-path-unweighted](./11-shortest-path-unweighted.md)     | Unweighted Shortest Path | BFS for shortest path                 |
| [12-clone-graph](./12-clone-graph.md)                               | Clone Graph              | Deep copy with visited map            |
| [13-grid-problems](./13-grid-problems.md)                           | Grid as Graph            | Islands, flood fill                   |
| [14-rotting-oranges](./14-rotting-oranges.md)                       | Multi-source BFS         | Simultaneous expansion                |
| [15-word-ladder](./15-word-ladder.md)                               | Implicit Graphs          | Word transformation                   |
| [16-bipartite-check](./16-bipartite-check.md)                       | Bipartite Check          | Two-coloring                          |
| [17-alien-dictionary](./17-alien-dictionary.md)                     | Alien Dictionary         | Topological sort from constraints     |
| [18-network-delay](./18-network-delay.md)                           | Network Delay            | Dijkstra application                  |

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
"Shortest path, unweighted..."       → BFS
"Shortest path, weighted..."         → Dijkstra (or Bellman-Ford if negative)
"All paths/permutations..."          → DFS/Backtracking
"Dependencies/ordering..."           → Topological Sort
"Connected/grouped..."               → Union-Find or DFS
"Grid traversal..."                  → BFS or DFS (grid as implicit graph)
"Level-by-level..."                  → BFS
"Cycle detection..."                 → DFS with colors (directed) or parent (undirected)
"Two groups/coloring..."             → Bipartite check (BFS/DFS)
"Minimum cost/distance..."           → Dijkstra or BFS depending on weights
```

---

## Graph Representations

```python
# Adjacency List (most common)
graph = {
    0: [1, 2],
    1: [0, 3],
    2: [0],
    3: [1]
}

# Adjacency Matrix
#     0  1  2  3
# 0 [[0, 1, 1, 0],
# 1  [1, 0, 0, 1],
# 2  [1, 0, 0, 0],
# 3  [0, 1, 0, 0]]

# Edge List
edges = [(0, 1), (0, 2), (1, 3)]
```

---

## Key Complexity Facts

| Algorithm        | Time             | Space | Notes                     |
| ---------------- | ---------------- | ----- | ------------------------- |
| BFS              | O(V + E)         | O(V)  | Queue + visited           |
| DFS              | O(V + E)         | O(V)  | Stack/recursion + visited |
| Dijkstra (heap)  | O((V + E) log V) | O(V)  | Priority queue            |
| Bellman-Ford     | O(V × E)         | O(V)  | Edge relaxation           |
| Topological Sort | O(V + E)         | O(V)  | Kahn's or DFS             |
| Union-Find       | O(α(n)) per op   | O(V)  | Nearly constant           |

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

## Prerequisites

> **Prerequisites:** [01-complexity-analysis](../01-complexity-analysis/README.md), [05-stacks-queues](../05-stacks-queues/README.md)

Understanding Big-O and queue/stack operations is essential. Recursion knowledge is highly recommended for DFS.

---

## Next Steps

Start with [01-graph-representations.md](./01-graph-representations.md) to understand how graphs are stored. Then master BFS and DFS before moving to specialized algorithms like Dijkstra and topological sort. Grid problems are the most common variation in interviews.

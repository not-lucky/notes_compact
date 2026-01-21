# Pattern Selection Flowchart

> **Prerequisites:** [README.md](./README.md)

This decision tree helps you quickly identify the right algorithm pattern based on problem characteristics. Start at the top and follow the branches.

---

## Building Intuition

### Why Flowcharts Work for Pattern Selection

Interview problems aren't random—they're designed to test specific techniques. After solving hundreds of problems, you notice that the same ~15 patterns appear over and over. The flowchart approach works because:

**The key insight**: Problem characteristics strongly predict the solution pattern. If someone says "sorted array, find a pair," you immediately know it's two pointers—not because you memorized it, but because sorted + pair = O(n) two-pointer solution is faster than O(n²) brute force.

### How to Think About Pattern Selection

Think of it like a doctor's diagnostic flowchart:
1. **Symptoms** (input type, constraints) narrow down possibilities
2. **Ruling out** (what patterns definitely won't work) is as important as identifying what will
3. **The first pattern you think of isn't always right**—verify with complexity analysis

### Mental Model: The Funnel

```
All possible algorithms
        ↓
Input type filter (array? graph? string?)
        ↓
Constraint filter (sorted? contiguous? k-related?)
        ↓
Operation filter (search? optimize? count?)
        ↓
1-2 candidate patterns
```

The flowchart systematizes this funnel so you don't waste time considering irrelevant patterns.

### Why This Matters in Interviews

- **45 minutes is short**: Spending 5 minutes on the wrong approach costs you
- **Confidence compounds**: Quickly identifying the pattern lets you focus on implementation details
- **Pattern recognition = expertise**: It's what separates a 6-month LeetCoder from a 2-year one

---

## When NOT to Use Flowcharts

### Don't Use Flowcharts When...

1. **The problem is clearly hybrid**: Some problems combine multiple patterns (e.g., binary search + sliding window). The flowchart leads to one pattern; you need to recognize when two are needed.

2. **Constraints are unusual**: If n ≤ 15, brute force or bitmask DP might work even if the flowchart suggests something else. Always check constraints first.

3. **The problem has a mathematical insight**: Problems like "count number of subarrays divisible by k" need math (prefix sums + modular arithmetic), not pattern matching.

4. **You're stuck in one branch**: If you've been in the "Array → Unsorted → Subarray" branch for 10 minutes without progress, step back. Maybe it's not a sliding window problem at all.

### Common Flowchart Mistakes

- **Forcing the first pattern**: Just because the flowchart says "sliding window" doesn't mean you should ignore that the solution might be simpler
- **Ignoring problem constraints**: Flowcharts optimize for typical cases; atypical constraints change everything
- **Not verifying complexity**: After the flowchart suggests a pattern, verify it achieves the required complexity

---

## Master Decision Tree

```
                    ┌─────────────────────────────┐
                    │   What is the input type?   │
                    └──────────────┬──────────────┘
                                   │
        ┌──────────────┬───────────┼───────────────┬──────────────┐
        ▼              ▼           ▼               ▼              ▼
    ┌───────┐    ┌──────────┐  ┌───────┐    ┌───────────┐   ┌─────────┐
    │ Array │    │  String  │  │ L.List│    │Tree/Graph │   │ Number  │
    └───┬───┘    └────┬─────┘  └───┬───┘    └─────┬─────┘   └────┬────┘
        │             │            │              │              │
        ▼             ▼            ▼              ▼              ▼
   See Array     See String    See Linked    See Tree/      See Math
   Flowchart     Flowchart     List Flow     Graph Flow     Flowchart
```

---

## Array Problem Flowchart

```
┌─────────────────────────────────────────────────────────────────────┐
│                         ARRAY PROBLEM                                │
└───────────────────────────────┬─────────────────────────────────────┘
                                │
                    ┌───────────┴───────────┐
                    │   Is the array sorted? │
                    └───────────┬───────────┘
                         ┌──────┴──────┐
                        YES           NO
                         │             │
              ┌──────────┴──────┐      │
              │ Finding pair/   │      ▼
              │ element?        │   ┌──────────────────────┐
              └────────┬────────┘   │ Subarray/Substring?  │
                  ┌────┴────┐       └──────────┬───────────┘
                 YES       NO            ┌─────┴─────┐
                  │         │           YES         NO
                  ▼         ▼            │           │
            ┌──────────┐ ┌────────────┐  │           ▼
            │   TWO    │ │  BINARY    │  │    ┌───────────────────┐
            │ POINTERS │ │  SEARCH    │  │    │ K largest/smallest│
            │  [O(N)]  │ │ [O(log N)] │  │    └─────────┬─────────┘
            └──────────┘ └────────────┘  │         ┌────┴────┐
                                         │        YES       NO
                                         │         │         │
                                         ▼         ▼         ▼
                                   ┌──────────┐ ┌──────┐ ┌──────────────┐
                                   │ SLIDING  │ │ HEAP │ │ See specific │
                                   │ WINDOW   │ │TOP-K │ │ patterns     │
                                   │  [O(N)]  │ │[O(N log K)]│          │
                                   └──────────┘ └──────┘ └──────────────┘
```

### Array - Detailed Decision Points

```
Is array sorted?
├── YES
│   ├── Find pair summing to target? → TWO POINTERS
│   ├── Find element or insertion point? → BINARY SEARCH
│   ├── Rotated/modified sorted array? → MODIFIED BINARY SEARCH
│   └── Merge with another sorted array? → TWO POINTERS / MERGE
│
└── NO
    ├── Find contiguous subarray with property?
    │   ├── Fixed size k? → SLIDING WINDOW (FIXED)
    │   ├── Variable size with constraint? → SLIDING WINDOW (VARIABLE)
    │   └── Max sum subarray? → KADANE'S ALGORITHM
    │
    ├── Range sum/update queries?
    │   ├── Many queries, no updates? → PREFIX SUM
    │   └── Range updates? → DIFFERENCE ARRAY
    │
    ├── K largest/smallest/frequent?
    │   └── → HEAP (TOP-K)
    │
    ├── Values are 1 to n, find missing/duplicate?
    │   └── → CYCLIC SORT or XOR
    │
    ├── Intervals (start, end)?
    │   └── → MERGE INTERVALS (sort by start)
    │
    ├── Next greater/smaller element?
    │   └── → MONOTONIC STACK
    │
    └── Optimization (min/max)?
        ├── Optimal substructure? → DP
        ├── Local optimal = global optimal? → GREEDY
        └── Minimize maximum or maximize minimum? → BINARY SEARCH ON ANSWER
```

---

## String Problem Flowchart

```
┌─────────────────────────────────────────────────────────────────────┐
│                        STRING PROBLEM                                │
└───────────────────────────────┬─────────────────────────────────────┘
                                │
                    ┌───────────┴────────────┐
                    │ Substring with property?│
                    └───────────┬────────────┘
                         ┌──────┴──────┐
                        YES           NO
                         │             │
                         ▼             ▼
                   ┌──────────┐   ┌─────────────────────┐
                   │ SLIDING  │   │ Character frequency?│
                   │ WINDOW   │   └──────────┬──────────┘
                   │  [O(N)]  │        ┌────┴────┐
                   └──────────┘       YES       NO
                                       │         │
                                       ▼         ▼
                                  ┌─────────┐ ┌───────────────┐
                                  │ HASHMAP │ │ Palindrome?   │
                                  │ COUNT   │ └───────┬───────┘
                                  │  [O(N)]  │    ┌────┴────┐
                                  └─────────┘   YES       NO
                                                 │         │
                                                 ▼         ▼
                                           ┌──────────┐ ┌────────────┐
                                           │ EXPAND   │ │ Pattern    │
                                           │ AROUND   │ │ matching?  │
                                           │ CENTER   │ │ → DP/KMP   │
                                           │  [O(N²)] │ │ [O(N+M)]   │
                                           └──────────┘ └────────────┘
```

### String - Detailed Decision Points

```
String problem?
├── Find substring with property?
│   ├── Longest/shortest substring → SLIDING WINDOW (VARIABLE)
│   ├── All substrings of length k → SLIDING WINDOW (FIXED)
│   └── Substring exists? → TWO POINTERS or HASHMAP
│
├── Anagram/character frequency?
│   ├── Check if anagram → HASHMAP COUNT (compare)
│   ├── Group anagrams → SORTED STRING as key
│   └── Find all anagram positions → SLIDING WINDOW + COUNT
│
├── Palindrome?
│   ├── Check if palindrome → TWO POINTERS
│   ├── Longest palindromic substring → EXPAND AROUND CENTER
│   ├── Longest palindromic subsequence → DP
│   └── Minimum cuts/insertions → DP
│
├── Pattern matching?
│   ├── Regex/wildcard → DP
│   ├── Exact match → KMP / RABIN-KARP
│   └── Prefix matching → TRIE
│
├── Parentheses/brackets?
│   ├── Validate → STACK
│   ├── Longest valid → DP or STACK
│   └── Generate all valid → BACKTRACKING
│
└── Word break/transformation?
    ├── Can break into words? → DP + HASHSET
    └── Transform word to another? → BFS
```

---

## Linked List Problem Flowchart

```
┌─────────────────────────────────────────────────────────────────────┐
│                      LINKED LIST PROBLEM                             │
└───────────────────────────────┬─────────────────────────────────────┘
                                │
                    ┌───────────┴───────────┐
                    │   Cycle detection?    │
                    └───────────┬───────────┘
                         ┌──────┴──────┐
                        YES           NO
                         │             │
                         ▼             ▼
                   ┌──────────┐   ┌───────────────────┐
                   │ FAST/    │   │ Reverse needed?   │
                   │ SLOW     │   └─────────┬─────────┘
                   │ [O(N)]   │        ┌────┴────┐
                   └──────────┘       YES       NO
                                       │         │
                                       ▼         ▼
                                 ┌──────────┐ ┌───────────────┐
                                 │ IN-PLACE │ │ Merge needed? │
                                 │ REVERSAL │ └───────┬───────┘
                                 │  [O(N)]  │    ┌────┴────┐
                                 └──────────┘   YES       NO
                                                 │         │
                                                 ▼         ▼
                                           ┌──────────┐ ┌────────────┐
                                           │ MERGE    │ │ FAST/SLOW  │
                                           │ PATTERN  │ │ (middle)   │
                                           │ [O(N+M)] │ │  [O(N)]    │
                                           └──────────┘ └────────────┘
```

### Linked List - Detailed Decision Points

```
Linked List problem?
├── Detect cycle or find start?
│   └── → FAST/SLOW POINTERS (Floyd's)
│
├── Find middle or nth from end?
│   └── → FAST/SLOW POINTERS
│
├── Reverse (all or part)?
│   ├── Reverse entire list → IN-PLACE REVERSAL
│   ├── Reverse between positions → IN-PLACE + POINTERS
│   └── Reverse k-group → IN-PLACE + RECURSION
│
├── Merge/combine lists?
│   ├── Merge two sorted → TWO POINTERS
│   ├── Merge k sorted → HEAP (MIN-HEAP)
│   └── Interleave lists → TWO POINTERS
│
├── Remove duplicates?
│   ├── Sorted list → TWO POINTERS
│   └── Unsorted list → HASHSET
│
├── Intersection point?
│   └── → TWO POINTERS (align lengths)
│
└── Check palindrome?
    └── → FAST/SLOW + REVERSE second half
```

---

## Tree/Graph Problem Flowchart

```
┌─────────────────────────────────────────────────────────────────────┐
│                       TREE/GRAPH PROBLEM                             │
└───────────────────────────────┬─────────────────────────────────────┘
                                │
                    ┌───────────┴───────────┐
                    │   Tree or Graph?      │
                    └───────────┬───────────┘
                         ┌──────┴──────┐
                        TREE         GRAPH
                         │             │
                         ▼             ▼
              ┌───────────────────┐  ┌─────────────────────┐
              │ Level-by-level?   │  │ Shortest path?      │
              └─────────┬─────────┘  └───────────┬─────────┘
                   ┌────┴────┐             ┌─────┴─────┐
                  YES       NO            YES         NO
                   │         │             │           │
                   ▼         ▼             ▼           ▼
              ┌──────────┐ ┌──────────┐   ┌────────────┐ ┌──────────────┐
              │   BFS    │ │   DFS    │   │    BFS     │ │ Connected    │
              │ [O(V+E)] │ │ [O(V+E)] │   │ (unwgt/wgt)│ │ components?  │
              │          │ │ (paths,  │   │ Dijkstra:  │ │ → DFS/BFS    │
              │          │ │  depth)  │   │ [O(ElogV)] │ │ → UNION-FIND │
              └──────────┘ └──────────┘   └────────────┘ └──────────────┘
```

### Tree - Detailed Decision Points

```
Tree problem?
├── Level-by-level processing?
│   └── → BFS (LEVEL ORDER)
│
├── Path sum or path finding?
│   └── → DFS (RECURSIVE or STACK)
│
├── Lowest Common Ancestor?
│   ├── BST → USE BST PROPERTY
│   └── Binary Tree → DFS with parent tracking
│
├── Validate BST?
│   └── → DFS with min/max bounds
│
├── Serialize/deserialize?
│   └── → BFS or PREORDER DFS
│
├── Construct from traversals?
│   └── → RECURSIVE BUILD with index tracking
│
└── Calculate depth/diameter/balance?
    └── → DFS (POST-ORDER)
```

### Graph - Detailed Decision Points

```
Graph problem?
├── Shortest path?
│   ├── Unweighted → BFS
│   ├── Weighted (positive) → DIJKSTRA
│   └── Negative weights → BELLMAN-FORD
│
├── Detect cycle?
│   ├── Directed → DFS with colors
│   └── Undirected → UNION-FIND or DFS
│
├── Connected components?
│   └── → DFS/BFS or UNION-FIND
│
├── Topological order?
│   └── → KAHN'S (BFS) or DFS
│
├── Bipartite check?
│   └── → BFS/DFS with coloring
│
├── Clone graph?
│   └── → DFS/BFS with HASHMAP
│
└── Grid/matrix as graph?
    ├── Flood fill/islands → DFS/BFS
    ├── Shortest path in grid → BFS
    └── Multi-source BFS → START FROM ALL SOURCES
```

---

## Math/Number Problem Flowchart

```
Math/Number problem?
├── Prime related?
│   ├── Check single number → TRIAL DIVISION to sqrt(n)
│   └── Find all primes to n → SIEVE OF ERATOSTHENES
│
├── GCD/LCM?
│   └── → EUCLIDEAN ALGORITHM
│
├── Power/exponentiation?
│   └── → FAST EXPONENTIATION
│
├── Bit manipulation?
│   ├── Check power of 2 → n & (n-1) == 0
│   ├── Count set bits → BRIAN KERNIGHAN
│   └── Single number (XOR) → XOR all elements
│
├── Random/sampling?
│   ├── K elements from stream → RESERVOIR SAMPLING
│   └── Random with weights → PREFIX SUM + BINARY SEARCH
│
└── Digit operations?
    └── → MOD 10 and DIV 10 pattern
```

---

## Quick Reference Table

| Problem Characteristic | Primary Pattern | Alternative |
|------------------------|-----------------|-------------|
| Sorted array + find pair | Two Pointers | Binary Search |
| Contiguous subarray with constraint | Sliding Window | Prefix Sum |
| Maximum contiguous sum | Kadane's | DP |
| K largest/smallest | Heap | QuickSelect |
| Shortest path (unweighted) | BFS | - |
| Shortest path (weighted) | Dijkstra | Bellman-Ford |
| All paths/combinations | DFS/Backtracking | - |
| Cycle in linked list | Fast/Slow Pointers | - |
| Next greater element | Monotonic Stack | - |
| Connected components | Union-Find | DFS/BFS |
| Optimization with choices | DP | Greedy |
| Values 1 to n, find missing | Cyclic Sort | XOR |
| Prefix matching | Trie | - |
| Overlapping intervals | Sort + Merge | - |

---

## Practice: Pattern Identification

Try to identify the pattern for these problems before looking at the answer:

1. "Find two numbers that sum to target in a sorted array"
2. "Find the longest substring without repeating characters"
3. "Find the kth largest element in an array"
4. "Determine if a linked list has a cycle"
5. "Find the shortest path in a binary maze"
6. "Generate all valid combinations of n pairs of parentheses"
7. "Find next greater element for each element in array"

<details>
<summary>Answers</summary>

1. Two Pointers
2. Sliding Window (Variable)
3. Heap (Top-K) or QuickSelect
4. Fast/Slow Pointers
5. BFS
6. Backtracking
7. Monotonic Stack

</details>

---

## Next: [02-when-to-use-what.md](./02-when-to-use-what.md)

# Chapter 12: Greedy Algorithms

Greedy algorithms make the **locally optimal choice** at each step, building toward a global optimum incrementally. Unlike dynamic programming, they never reconsider past decisions. This works when the problem has the **greedy choice property** -- a locally optimal choice is always part of *some* globally optimal solution.

## Why Greedy Algorithms Matter

1. **Interview frequency**: Greedy problems appear in ~20% of coding interviews
2. **Efficiency**: Often $O(n)$ or $O(n \log n)$ vs exponential DP alternatives
3. **Pattern recognition**: Key skill is recognizing when greedy works vs when DP is needed
4. **Proof skills**: Interviewers may ask you to justify why greedy works

---

## When Does Greedy Work?

A greedy approach is correct when the problem has **both** of these properties:

### 1. Greedy Choice Property

A globally optimal solution can be arrived at by making locally optimal choices. We can commit to the choice that looks best right now and then solve the remaining subproblem, without ever needing to reconsider.

```python
# Example: Coin change with US denominations [25, 10, 5, 1] for 41 cents
# Greedy choice: always take the largest possible coin first.
# 25 -> 10 -> 5 -> 1 = 41 (4 coins, optimal)

# Counterexample: Denominations [1, 3, 4] for 6 cents
# Greedy choice: 4 -> 1 -> 1 = 6 (3 coins)
# Optimal choice: 3 -> 3 = 6 (2 coins)
# Here, the greedy choice of taking '4' locks us out of the optimal solution.
```

### 2. Optimal Substructure

An optimal solution to the problem contains optimal solutions to its subproblems. Once a greedy choice is made, solving the remaining problem optimally yields a globally optimal solution.

```python
# Example: Activity Selection
# Given activities (start, end): A(1, 4), B(3, 5), C(0, 6), D(5, 7)
#
# If we make the greedy choice to pick the activity that ends earliest (A),
# the remaining valid activities are those that start after A ends (>= 4).
# The remaining problem is to select the maximum activities from {D(5, 7)}.
# Solving this subproblem optimally guarantees the whole solution is optimal.
```

> **Note:** DP also requires optimal substructure. The difference is that greedy
> additionally needs the greedy choice property, which lets it commit to one
> subproblem instead of exploring all of them.

---

## Greedy vs Dynamic Programming

The most important skill: knowing when to use each approach.

| Aspect            | Greedy                             | Dynamic Programming                |
| ----------------- | ---------------------------------- | ---------------------------------- |
| **Decision**      | Make the best local choice _now_; never reconsider | Consider all subproblems; pick globally optimal     |
| **Time**          | Usually $O(n)$ or $O(n \log n)$                    | Usually $O(n^2)$ or $O(n \cdot \text{target})$      |
| **Space**         | Usually $O(1)$                                     | Usually $O(n)$ or more                               |
| **Correctness**   | Must prove greedy choice property holds            | Always correct if formulated right                   |
| **When it fails** | Locally optimal choice locks you out of a better global solution (e.g., 0/1 knapsack) | Never misses the global optimum (just slower, needs memoization or tabulation) |

### Decision Tree

```text
Does the problem have Optimal Substructure?
    |
    +-- No --> Neither Greedy nor DP applies
    |
    +-- Yes
        |
        +-- Can you prove the Greedy Choice Property?
            +-- Yes --> Use Greedy (verify with counter-examples first)
            +-- No / Unsure
                |
                +-- Are there overlapping subproblems?
                    +-- Yes --> Use DP
                    +-- No  --> Divide & Conquer (or reconsider Greedy)
```

### Quick Comparison: Greedy vs DP vs BFS

| Problem                | Approach | Why                                           |
| ---------------------- | -------- | --------------------------------------------- |
| Activity Selection     | Greedy   | Earliest end time maximizes remaining room     |
| 0/1 Knapsack           | DP       | Greedy by value/weight ratio fails (blocking)  |
| Fractional Knapsack    | Greedy   | Can take fractions, so best ratio always wins  |
| Coin Change (US coins) | Greedy   | Canonical denominations allow largest-first    |
| Coin Change (general)  | DP       | Greedy fails for arbitrary denominations       |
| Jump Game I            | Greedy   | Reachability is a contiguous prefix            |
| Jump Game III          | BFS      | Bidirectional jumps break the greedy frontier  |

---

## Chapter Contents

| #   | Topic                                              | Key Concepts                                       |
| --- | -------------------------------------------------- | -------------------------------------------------- |
| 01  | [Greedy Basics](./01-greedy-basics.md)             | When greedy works, proof techniques, greedy vs DP  |
| 02  | [Interval Scheduling](./02-interval-scheduling.md) | Activity selection, sort by end time, weighted DP  |
| 03  | [Merge Intervals](./03-merge-intervals.md)         | Merge overlapping intervals, insert, intersections |
| 04  | [Meeting Rooms](./04-meeting-rooms.md)             | Meeting rooms I & II, min-heap / sweep line        |
| 05  | [Jump Game](./05-jump-game.md)                     | Jump game I-V, track max reachable, BFS and DP variants |
| 06  | [Gas Station](./06-gas-station.md)                 | Circular route, reset on deficit, global vs local constraints |
| 07  | [Candy Distribution](./07-candy-distribution.md)   | Two-pass greedy, neighbor constraints              |
| 08  | [Partition Labels](./08-partition-labels.md)       | Last occurrence tracking, interval covering        |

**Progression logic:**
- **01** establishes the theory: what greedy is, when it works, how to prove it.
- **02-04** cover **interval problems** (the most common greedy family), progressing from selecting non-overlapping intervals, to merging overlapping ones, to allocating resources (rooms).
- **05-06** cover **reachability and circular** problems where greedy tracks a frontier or accumulator.
- **07** introduces the **two-pass** pattern, a distinct greedy structure used for constraints across neighbors.
- **08** ties it all together -- partition labels is merge intervals in disguise.

---

## Greedy Patterns Overview

| Pattern             | Core Idea                         | Problems                          |
| ------------------- | --------------------------------- | --------------------------------- |
| Interval Scheduling | Sort by end time, pick greedily   | Activity selection, meeting rooms |
| Merge Intervals     | Sort by start time, extend end    | Overlapping intervals, insert     |
| Jump/Reach          | Track farthest reachable position | Jump game I & II                  |
| Reset on Deficit    | Reset start when accumulator < 0  | Gas station                       |
| Two-Pass            | Left pass then right pass         | Candy, trapping rain water        |
| Partition/Covering  | Track last occurrence, extend     | Partition labels, video stitching |
| Heap-Based          | Always process min/max first      | Meeting rooms II, task scheduler  |

---

## Sorting in Greedy Algorithms

Most greedy algorithms depend on processing elements in the right order. Sorting defines that order, and getting the sort key wrong is the most common source of bugs.

```python
# Sort by start time (default for lists/tuples -- compares element-by-element)
intervals = [[1, 3], [2, 6], [8, 10]]
intervals.sort()  # Equivalent to intervals.sort(key=lambda x: (x[0], x[1]))

# Sort by end time (crucial for activity selection / interval scheduling)
intervals.sort(key=lambda x: x[1])

# Sort by multiple criteria:
# e.g., sort by start time ascending, then by end time descending
# (useful for "remove covered intervals" where longer intervals should come first)
intervals.sort(key=lambda x: (x[0], -x[1]))
```

| Problem            | Sort By         | Why                                        |
| ------------------ | --------------- | ------------------------------------------ |
| Activity selection | End time        | Finishing early maximizes remaining room    |
| Merge intervals    | Start time      | Process left-to-right, extend end          |
| Meeting rooms II   | Start time      | Process arrivals chronologically           |
| Remove covered     | (Start, -End)   | Longer interval first at same start        |

---

## How to Verify a Greedy Approach

Before coding, validate your greedy strategy with this checklist:

### Step 1: Try Counter-Examples

The fastest way to disprove a greedy idea. Think about:
- What if the greedy choice **blocks** a better combination? (0/1 knapsack)
- What if a **short-term sacrifice** leads to a better outcome? (coin change with `[1, 3, 4]`)
- What if **ties** are broken differently? (remove covered intervals)

### Step 2: Sketch a Proof (One of Three Techniques)

**Greedy Stays Ahead**: Show that at every step, the greedy solution is at least as good as any alternative. Compare the greedy's i-th choice with any optimal solution's i-th choice and show greedy never falls behind. *(Used for: activity selection.)*

**Exchange Argument**: Assume an optimal solution differs from greedy, then "exchange" elements to match the greedy choice and show the result is no worse. *(Used for: coin change with US coins, Huffman coding.)*

**Contradiction**: Assume greedy is not optimal and derive a logical contradiction. *(Used for: fractional knapsack.)*

See [01-greedy-basics.md](./01-greedy-basics.md) for detailed proof examples.

### Step 3: Test Edge Cases

- Empty input
- Single element
- All identical values
- Already sorted / reverse sorted
- Boundary conditions (exactly at capacity/limit)

---

## Common Mistakes

1. **Assuming greedy works without proof**: Always verify with edge cases or a formal argument
2. **Wrong sorting criterion**: Sorting by start time when end time is needed (activity selection) or vice versa (merge intervals)
3. **Overlooking tie-breaking**: How ties are broken affects correctness in some problems (e.g., "remove covered intervals" requires `(start, -end)` sort)
4. **Ignoring multi-constraint problems**: Greedy for one metric may violate another constraint entirely
5. **Skipping the proof in interviews**: Interviewers often ask *why* greedy works -- be ready with an informal argument at minimum

---

## Recognizing Greedy Problems

### Signals in the Problem Statement

- **"Maximum number of..."** -- often interval scheduling (sort by end time, greedily select)
- **"Minimum number of..."** -- could be greedy or DP; check if greedy choice property holds
- **"Can you reach/complete..."** -- often greedy with reachability tracking (jump game, gas station)
- **"Partition into..."** -- often greedy with sorting or last-occurrence tracking
- **"Assign/distribute..."** -- often greedy with sorting (cookies, candy)
- **"Lexicographically smallest/largest..."** -- often greedy (build character by character, picking the best available)

### Red Flags (Greedy Probably Won't Work)

| Red Flag | Why Greedy Fails | Alternative |
| --- | --- | --- |
| "Choose exactly k items" | Subset selection often needs DP | DP with state tracking count |
| "Minimize/maximize subject to multiple constraints" | Multiple constraints create complex trade-offs | DP, ILP, or multi-objective optimization |
| "Count all ways" | Greedy makes one choice, can't enumerate | DP with counting |
| "Find all valid configurations" | Greedy commits to one path | Backtracking / DFS |
| "Minimum edits/operations" | Local optimum may require multiple changes | DP (e.g., edit distance) |

---

## Common Time Complexity Patterns

| Problem Type       | Time          | Why                                                      |
| ------------------ | ------------- | -------------------------------------------------------- |
| Interval problems  | $O(n \log n)$ | Sorting dominates; the scan itself is $O(n)$             |
| Single pass greedy | $O(n)$        | One linear traversal making $O(1)$ decisions per element |
| Two-pass greedy    | $O(n)$        | Two linear traversals (e.g., left-to-right then right-to-left) |
| Heap-based greedy  | $O(n \log n)$ | $n$ heap operations at $O(\log n)$ each                  |

---

## Start: [01-greedy-basics.md](./01-greedy-basics.md)

Begin with understanding when greedy algorithms work and how to prove correctness.

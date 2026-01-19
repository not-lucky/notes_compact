# Chapter 12: Greedy Algorithms

Greedy algorithms make locally optimal choices at each step, hoping to find a global optimum. While simpler than dynamic programming, they only work when the problem has the "greedy choice property" — making the locally best choice leads to a globally best solution.

## Why Greedy Algorithms Matter

1. **Interview frequency**: Greedy problems appear in ~20% of coding interviews
2. **Efficiency**: Often O(n) or O(n log n) vs exponential DP alternatives
3. **Pattern recognition**: Key skill is recognizing when greedy works vs when DP is needed
4. **Proof skills**: Interviewers may ask you to justify why greedy works

---

## Greedy vs Dynamic Programming

The most important skill: knowing when to use each approach.

| Aspect | Greedy | Dynamic Programming |
|--------|--------|---------------------|
| **Decision** | Make best local choice now | Consider all subproblems |
| **Time** | Usually O(n) or O(n log n) | Usually O(n²) or O(n × target) |
| **Space** | Usually O(1) | Usually O(n) or more |
| **Correctness** | Must prove greedy choice works | Always correct if formulated right |
| **When it fails** | Locally optimal ≠ globally optimal | Never fails (just slower) |

---

## When Does Greedy Work?

Greedy algorithms work when the problem has these two properties:

### 1. Greedy Choice Property

A globally optimal solution can be arrived at by making locally optimal choices.

```
Example: Coin change with denominations [25, 10, 5, 1] for 41 cents
Greedy: 25 + 10 + 5 + 1 = 41 ✓ (optimal)

Counterexample: Coin change with denominations [1, 3, 4] for 6 cents
Greedy: 4 + 1 + 1 = 6 (3 coins)
Optimal: 3 + 3 = 6 (2 coins) ✗ Greedy fails!
```

### 2. Optimal Substructure

An optimal solution contains optimal solutions to its subproblems.

```
Example: Activity Selection
If we pick activity A (greedy choice), the remaining problem
(activities after A ends) must also be solved optimally.
```

---

## The Greedy Decision Framework

```
Is there a way to order/sort the choices?
    │
    ├── Yes → Consider greedy
    │         │
    │         ├── Can locally best choice always be in optimal solution?
    │         │   │
    │         │   ├── Yes (can prove) → Use greedy
    │         │   │
    │         │   └── No / Unsure → Use DP
    │         │
    │         └── Do choices affect each other (overlap)?
    │             │
    │             ├── No (independent) → Greedy likely works
    │             │
    │             └── Yes (dependent) → DP probably needed
    │
    └── No clear ordering → Usually DP or backtracking
```

---

## Greedy Patterns Overview

| Pattern | Problems | Key Strategy |
|---------|----------|--------------|
| Interval Scheduling | Activity selection, meeting rooms | Sort by end time |
| Merge Intervals | Overlapping intervals | Sort by start time |
| Jump/Reach | Jump game, gas station | Track farthest reachable |
| Two-Pass | Candy, trapping rain water | Left pass then right pass |
| Greedy Choice | Task scheduling, partition | Pick locally optimal |

---

## Chapter Contents

| # | Topic | Key Concepts |
|---|-------|--------------|
| 01 | [Greedy Basics](./01-greedy-basics.md) | When greedy works, proof techniques |
| 02 | [Interval Scheduling](./02-interval-scheduling.md) | Activity selection, maximum meetings |
| 03 | [Merge Intervals](./03-merge-intervals.md) | Merge overlapping intervals |
| 04 | [Meeting Rooms](./04-meeting-rooms.md) | Meeting rooms I and II |
| 05 | [Jump Game](./05-jump-game.md) | Jump game I and II |
| 06 | [Gas Station](./06-gas-station.md) | Circular array, greedy choice |
| 07 | [Candy Distribution](./07-candy-distribution.md) | Two-pass greedy |
| 08 | [Partition Labels](./08-partition-labels.md) | Interval-based partitioning |

---

## Common Proof Techniques

### 1. Greedy Stays Ahead

Show that greedy solution is always at least as good as any other solution at each step.

```
For activity selection:
- Sort activities by end time
- At each step, greedy picks earliest-ending activity
- This leaves maximum room for future activities
- Greedy is never worse than any other choice
```

### 2. Exchange Argument

Show that any optimal solution can be transformed into greedy solution without losing optimality.

```
For coin change (US coins):
- If optimal uses multiple smaller coins where one larger works,
  swap them for the larger coin
- This never increases coin count
- Eventually reach greedy solution
```

### 3. Contradiction

Assume greedy is not optimal, show this leads to contradiction.

```
For Huffman coding:
- Assume greedy tree is not optimal
- Some other tree T' is better
- But we can swap nodes in T' to match greedy without increasing cost
- Contradiction: greedy must be optimal
```

---

## Common Mistakes

1. **Assuming greedy works**: Always verify with edge cases or proof
2. **Wrong sorting criteria**: Sorting by wrong attribute (start vs end time)
3. **Overlooking ties**: How to break ties affects some problems
4. **Not considering all constraints**: Greedy for one metric may violate others
5. **Forgetting proof**: Interviewers may ask WHY greedy works

---

## Time Complexity Patterns

| Problem Type | Time | Why |
|--------------|------|-----|
| Interval problems | O(n log n) | Sorting dominates |
| Single pass greedy | O(n) | One traversal |
| Two-pass greedy | O(n) | Two traversals |
| Heap-based greedy | O(n log n) | n heap operations |

---

## Classic Interview Problems by Company

| Company | Favorite Greedy Problems |
|---------|-------------------------|
| Google | Task Scheduler, Jump Game II, Partition Labels |
| Meta | Meeting Rooms II, Merge Intervals, Queue Reconstruction |
| Amazon | Gas Station, Candy, Assign Cookies |
| Microsoft | Jump Game, Non-overlapping Intervals, Boats to Save People |
| Apple | Lemonade Change, Minimum Number of Arrows |

---

## Quick Reference: Greedy Signals

Look for these keywords/patterns:

```
- "Maximum number of..." → often interval scheduling
- "Minimum number of..." → often greedy or DP
- "Can you reach/complete..." → often greedy with tracking
- "Partition into..." → often greedy with sorting
- "Assign/distribute..." → often greedy with sorting
```

---

## Greedy vs DP: Quick Examples

| Problem | Approach | Why |
|---------|----------|-----|
| Activity Selection | Greedy | Earliest end maximizes remaining time |
| 0/1 Knapsack | DP | Greedy by value/weight ratio fails |
| Fractional Knapsack | Greedy | Can take fractions, ratio works |
| Coin Change (US coins) | Greedy | Special denominations allow it |
| Coin Change (general) | DP | Greedy fails for arbitrary denominations |
| Jump Game I | Greedy | Track max reach as you go |
| Jump Game III | BFS | Bidirectional movement |

---

## Start: [01-greedy-basics.md](./01-greedy-basics.md)

Begin with understanding when greedy algorithms work and how to prove correctness.

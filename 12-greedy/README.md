# Chapter 12: Greedy Algorithms

Greedy algorithms build up a solution piece by piece, always choosing the next piece that offers the most obvious and immediate benefit. In other words, they make the **locally optimal choice** at each step, hoping that these local choices will lead to a **globally optimal solution**.

Unlike dynamic programming, a greedy algorithm **never reconsiders its choices**. Once a decision is made, it is final.

## Why Greedy Algorithms Matter

1. **Interview Frequency**: Greedy problems are very common, testing your logical reasoning and pattern recognition.
2. **Efficiency**: They typically run in $O(N)$ or $O(N \log N)$ time and $O(1)$ space, vastly outperforming exponential or $O(N^2)$ DP alternatives.
3. **Elegance**: A correct greedy solution is often incredibly concise.
4. **Proof Skills**: The challenge isn't usually writing the code, but *proving* that the greedy strategy actually works.

---

## When Does Greedy Work?

A problem must have **both** of these properties for a greedy approach to guarantee an optimal solution:

### 1. Greedy Choice Property
A globally optimal solution can be arrived at by making locally optimal choices. You can commit to the choice that looks best right now and solve the remaining subproblem, without ever needing to look back or consider alternative choices.

```python
def greedy_coin_change(coins: list[int], amount: int) -> list[int]:
    # Assume coins are sorted in descending order
    result = []
    for coin in coins:
        while amount >= coin:
            amount -= coin
            result.append(coin)
    return result

# Example: Coin change with US denominations for 41 cents
# greedy_coin_change([25, 10, 5, 1], 41)
# -> [25, 10, 5, 1] (4 coins, optimal)

# Counterexample: Denominations [4, 3, 1] for 6 cents
# greedy_coin_change([4, 3, 1], 6)
# -> [4, 1, 1] (3 coins, NOT optimal)
# The optimal choice is [3, 3] (2 coins).
# Here, the greedy choice of taking '4' locks us out of the optimal solution.
```

### 2. Optimal Substructure
An optimal solution to the problem contains optimal solutions to its subproblems. Once a greedy choice is made, solving the remaining smaller problem optimally guarantees that the overall solution is optimal.

> **Note:** Dynamic Programming also requires optimal substructure. The key difference is that greedy algorithms additionally possess the *greedy choice property*, allowing them to commit to one subproblem instead of exploring all possibilities.

---

## Greedy vs. Dynamic Programming

The most critical skill in this chapter is knowing when to use which approach.

| Aspect | Greedy | Dynamic Programming |
| :--- | :--- | :--- |
| **Decision** | Make the best local choice *now*; never reconsider. | Consider all subproblems; pick the globally optimal one. |
| **Time** | Usually $O(N)$ or $O(N \log N)$ | Usually $O(N^2)$ or $O(N \cdot \text{target})$ |
| **Space** | Usually $O(1)$ | Usually $O(N)$ or more (for memoization/tabulation) |
| **Correctness** | Must prove the greedy choice property holds. | Always correct if state transitions are formulated properly. |
| **When it fails** | A locally optimal choice locks you out of a better global solution (e.g., 0/1 Knapsack). | Rarely fails on correctness, but may TLE/OOM if state space is too large. |

### The Decision Tree

```text
Does the problem have Optimal Substructure?
    |
    +-- No  --> Neither Greedy nor DP applies
    |
    +-- Yes --> Can you prove the Greedy Choice Property?
                |
                +-- Yes --> Use Greedy (verify with counter-examples first)
                |
                +-- No / Unsure --> Are there overlapping subproblems?
                                    |
                                    +-- Yes --> Use DP
                                    |
                                    +-- No  --> Divide & Conquer
```

---

## Chapter Contents

| # | Topic | Key Concepts |
| :--- | :--- | :--- |
| **01** | [Greedy Basics](./01-greedy-basics.md) | When greedy works, proof techniques, greedy vs DP |
| **02** | [Interval Scheduling](./02-interval-scheduling.md) | Activity selection, sort by end time, maximizing non-overlapping |
| **03** | [Merge Intervals](./03-merge-intervals.md) | Sort by start time, merge overlaps, insert intervals |
| **04** | [Meeting Rooms](./04-meeting-rooms.md) | Resource allocation, min-heap, sweep line algorithms |
| **05** | [Jump Game](./05-jump-game.md) | Track max reachability, greedy frontier, BFS and DP variants |
| **06** | [Gas Station](./06-gas-station.md) | Circular routes, global vs local constraints, reset on deficit |
| **07** | [Candy Distribution](./07-candy-distribution.md) | Two-pass greedy (left-to-right, right-to-left), neighbor constraints |
| **08** | [Partition Labels](./08-partition-labels.md) | Last occurrence tracking, dynamic interval expansion |

**Progression Logic:**
- **01** establishes the theory and foundation.
- **02-04** cover **interval problems**, the most common greedy family, progressing from selecting to merging to allocating.
- **05-06** cover **reachability and circular accumulation**, tracking a frontier or deficit.
- **07** introduces the **two-pass pattern** for bidirectional constraints.
- **08** ties concepts together with a problem that is effectively "merge intervals in disguise."

---

## Greedy Patterns Overview

| Pattern | Core Idea | Common Problems |
| :--- | :--- | :--- |
| **Interval Scheduling** | Sort by end time, pick greedily | Activity Selection, Non-overlapping Intervals |
| **Merge Intervals** | Sort by start time, extend end | Merge Intervals, Insert Interval |
| **Heap-Based Greedy** | Always process the dynamic min/max | Meeting Rooms II, Task Scheduler |
| **Jump / Reach** | Track the farthest reachable position | Jump Game I & II |
| **Reset on Deficit** | Reset start pointer when accumulator < 0 | Gas Station, Maximum Subarray (Kadane's) |
| **Two-Pass** | Resolve constraints left-to-right, then right-to-left | Candy, Trapping Rain Water |
| **Partition / Covering** | Track last occurrence, extend partition boundary | Partition Labels, Video Stitching |

---

## The Greedy Toolkit

To implement greedy algorithms effectively, you need a firm grasp on a few fundamental tools.

### 1. Sorting

Sorting is the backbone of most greedy algorithms. It defines the order in which you process elements. **Getting the sort key wrong is the #1 source of bugs.**

```python
# Sort by start time (default behavior for lists/tuples)
intervals = [[8, 10], [1, 3], [2, 6]]
intervals.sort()
# Now: [[1, 3], [2, 6], [8, 10]]
# Equivalent to: intervals.sort(key=lambda x: (x[0], x[1]))

# Sort by end time (crucial for Activity Selection / Interval Scheduling)
intervals.sort(key=lambda x: x[1])
# Now: [[1, 3], [2, 6], [8, 10]]

# Sort by multiple criteria: Start time ascending, End time descending
# (Useful for "Remove Covered Intervals": longer intervals come first)
intervals = [[1, 4], [1, 3], [2, 6]]
intervals.sort(key=lambda x: (x[0], -x[1]))
# Now: [[1, 4], [1, 3], [2, 6]]
```

### 2. Heaps (Priority Queues)

When the "best" local choice changes dynamically as you process elements, sorting upfront isn't enough. You need a heap to constantly retrieve the current minimum or maximum.
- **Example:** Meeting Rooms II uses a min-heap to track the earliest room release time.

### 3. Running Accumulators

Some greedy problems don't require sorting at all; they just need a single linear scan while updating a running state (like maximum reach or current fuel).
- **Example:** Jump Game, Gas Station.

---

## How to Verify a Greedy Approach

Before writing any code, validate your greedy strategy with this checklist:

### Step 1: Try to Break It (Counter-Examples)
The fastest way to disprove a greedy idea is to find a case where it fails. Think about:
- What if the greedy choice **blocks** a significantly better combination later?
- What if a **short-term sacrifice** leads to a massive long-term gain?
- How are **ties** broken? Does it matter?

### Step 2: Sketch a Proof
If you can't break it, try to prove it. Interviewers may ask you to justify your logic.
- **Greedy Stays Ahead:** Show that at every step, the greedy solution's progress is at least as good as any hypothetical optimal solution. *(Classic for: Interval Scheduling)*
- **Exchange Argument:** Assume an optimal solution differs from your greedy one. Show that you can swap elements to match your greedy choice without making the solution worse. *(Classic for: Coin Change with canonical coins)*
- **Contradiction:** Assume the greedy choice is *not* part of the optimal solution, and prove that this assumption leads to a logical contradiction.

### Step 3: Test Edge Cases
- Empty input or single element
- All elements identical
- Already sorted / reverse sorted inputs
- Exact boundary conditions (e.g., fuel exactly matches distance)

---

## Recognizing Greedy Problems

### Green Flags (Signals to think Greedy)
- **"Maximum/Minimum number of..."** — Often interval scheduling (sort by end time) or finding bounds.
- **"Can you reach..."** — Often reachability tracking.
- **"Partition into..."** — Often last-occurrence tracking.
- **"Lexicographically smallest/largest..."** — Build character by character, picking the best available.

### Red Flags (Greedy will likely fail)
| Red Flag Phrase | Why Greedy Fails | Alternative Approach |
| :--- | :--- | :--- |
| **"Choose exactly $k$ items"** | Hard constraint breaks local optimality. | Dynamic Programming |
| **"Minimize subject to multiple constraints"** | Constraints conflict; trade-offs are required. | DP, or multi-objective optimization |
| **"Count all ways" / "Find all combinations"** | Greedy commits to *one* path; it doesn't enumerate. | Backtracking / DP with counting |
| **"Minimum edits/operations"** | Local minimums get trapped far from global minimums. | DP (e.g., Edit Distance) |

---

## Common Mistakes

1. **Skipping the proof:** Assuming greedy works and jumping into code, only to fail on hidden test cases. Always look for counter-examples first.
2. **Forgetting to sort:** Processing unsorted input when the algorithm assumes ordered data.
3. **Wrong sorting criteria:** Sorting by start time when end time is required (Interval Scheduling), or vice versa.
4. **Modifying the collection while iterating:** Removing elements from a list while looping over it leads to index out-of-bounds or skipped elements. Always build a new result list or iterate backwards.
5. **Ignoring tie-breaking rules:** When sorting by one criterion results in ties, the secondary sorting key can make or break the algorithm (e.g., `(start, -end)`).

---

## Quick Comparison: Similar Problems, Different Paradigms

| Problem | Approach | Why |
| :--- | :--- | :--- |
| **Fractional Knapsack** | Greedy | Can take fractions, so taking highest value-to-weight ratio always wins. |
| **0/1 Knapsack** | DP | Cannot take fractions; greedy choice might block a better packing combination. |
| **Coin Change (US coins)** | Greedy | Denominations allow taking the largest coin safely (exchange argument holds). |
| **Coin Change (General)** | DP | Greedy fails for arbitrary sets (e.g., `[1, 3, 4]` for `6`). |
| **Jump Game I** | Greedy | Reachability is a contiguous prefix; tracking max reach is sufficient. |
| **Jump Game III** | BFS / DFS | Bidirectional jumps break the one-directional greedy frontier. |

---

Let's begin the chapter with the theory and foundation: **[01-greedy-basics.md](./01-greedy-basics.md)**.


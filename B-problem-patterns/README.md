# Appendix B: Problem Patterns Guide

This appendix is your go-to resource for pattern recognition during interviews. Instead of memorizing hundreds of problems, learn to recognize the ~15 core patterns that cover 90%+ of FANG+ interview questions.

---

## Building Intuition

### Why Pattern Recognition is the Key Skill

When you solve a new problem, you're not really inventing a solution from scratch. You're recognizing which of the ~15 common patterns applies and adapting it to the specific constraints. This is what interviewers actually test—can you see the pattern beneath the problem's surface?

**The key insight**: Most interview problems are variations of problems you've already solved. The trick isn't to memorize solutions—it's to develop pattern-matching intuition.

### How Experts See Problems Differently

Beginners see: "Given an array of integers, find two numbers that add up to a target."

Experts see: "This is a lookup problem. I need to check if `target - current` exists. That's either:
1. Sort + two pointers (O(n log n))
2. HashSet for O(1) lookup (O(n))
3. If I need indices, HashMap instead of HashSet"

The difference isn't intelligence—it's pattern vocabulary.

### The 80/20 of Interview Patterns

~80% of FANG interview problems use these patterns:
1. **Two Pointers / Sliding Window** (25% of problems)
2. **DFS/BFS** (20% of problems)
3. **Dynamic Programming** (15% of problems)
4. **Binary Search** (10% of problems)
5. **Heap / Priority Queue** (10% of problems)

The remaining 20% use specialized patterns (Union-Find, Trie, etc.).

### Mental Model: Pattern Recognition as Language

Think of patterns as vocabulary words. When you're fluent in a language, you don't consciously translate—you just understand. Similarly, when you're fluent in patterns:

- You **hear** "contiguous subarray with constraint" and **think** "sliding window"
- You **hear** "shortest path" and **think** "BFS (unweighted) or Dijkstra (weighted)"
- You **hear** "generate all combinations" and **think** "backtracking"

This appendix teaches you that vocabulary.

---

## When NOT to Use Pattern Matching

### Pattern Matching Has Limits

1. **Novel problems require novel thinking**: Some problems genuinely need creative insight. Don't force a pattern when none fits naturally.

2. **Constraints override patterns**: A problem that looks like O(n²) DP might allow O(n log n) with a greedy approach—if constraints hint at it.

3. **Pattern matching ≠ understanding**: If you apply a pattern without understanding WHY it works, you'll struggle with variations.

4. **Interview communication matters**: Even if you recognize the pattern instantly, walk through your reasoning. Interviewers want to see your thought process, not just the answer.

### Anti-Patterns in Pattern Recognition

- **Hammer syndrome**: "I just learned monotonic stacks, so every problem is a nail"
- **Pattern shopping**: Trying patterns randomly until one works
- **Ignoring the problem**: Forcing a pattern instead of reading carefully
- **Over-complicating**: Using advanced patterns when simpler approaches work

---

## Why Pattern Recognition Matters

1. **Limited interview time**: 45 minutes means no time for trial and error
2. **Novel problems**: You'll face problems you haven't seen before
3. **Demonstrates expertise**: Recognizing patterns shows deep understanding
4. **Reduces anxiety**: Confidence comes from knowing you have a framework

---

## The 15 Core Patterns

| # | Pattern | Key Indicator | Example Problems |
|---|---------|---------------|------------------|
| 1 | Two Pointers | Sorted array, find pair | Two Sum II, 3Sum, Container With Water |
| 2 | Sliding Window | Substring/subarray with constraint | Longest Substring, Min Window Substring |
| 3 | Fast & Slow Pointers | Linked list cycle, middle element | Cycle Detection, Happy Number |
| 4 | Merge Intervals | Overlapping ranges | Merge Intervals, Insert Interval |
| 5 | Cyclic Sort | Array with values 1 to n | Find Missing Number, Find Duplicate |
| 6 | In-place Reversal | Linked list manipulation | Reverse Linked List, Reverse Sublist |
| 7 | BFS | Shortest path, level-order | Binary Tree Level Order, Rotting Oranges |
| 8 | DFS | Exhaustive search, paths | Path Sum, Number of Islands |
| 9 | Two Heaps | Find median, streaming | Find Median from Stream |
| 10 | Subsets/Backtracking | All combinations | Subsets, Permutations, N-Queens |
| 11 | Modified Binary Search | Sorted array variants | Search in Rotated Array, Peak Element |
| 12 | Top-K Elements | K largest/smallest | Kth Largest, Top K Frequent |
| 13 | K-way Merge | Merge sorted structures | Merge K Sorted Lists |
| 14 | Dynamic Programming | Optimization, counting paths | Climbing Stairs, Coin Change, LCS |
| 15 | Monotonic Stack | Next greater/smaller element | Daily Temperatures, Largest Rectangle |

---

## Appendix Contents

| # | Topic | What You'll Learn |
|---|-------|-------------------|
| 01 | [Pattern Flowchart](./01-pattern-flowchart.md) | Decision tree for selecting the right pattern |
| 02 | [When to Use What](./02-when-to-use-what.md) | Data structure and algorithm selection guide |
| 03 | [Template Code](./03-template-code.md) | Copy-paste templates for each pattern |

---

## Quick Pattern Detection Checklist

### Before Reading the Full Problem

1. **Input type?** Array, string, linked list, tree, graph?
2. **Sorted?** If sorted → think binary search, two pointers
3. **Contiguous?** Subarray/substring → sliding window
4. **Optimization?** Min/max → DP, greedy, or binary search on answer
5. **Combinations?** All subsets/permutations → backtracking

### Keywords That Signal Patterns

```
"Contiguous subarray/substring"      → Sliding Window
"Pair/triplet that sums to"          → Two Pointers (sort first if needed)
"Shortest path"                      → BFS
"All paths/combinations"             → DFS/Backtracking
"Kth largest/smallest"               → Heap or QuickSelect
"Maximum/minimum with constraint"    → DP or Binary Search on Answer
"Linked list cycle"                  → Fast & Slow Pointers
"Next greater/smaller"               → Monotonic Stack
"Overlapping intervals"              → Sort + Merge
"Find duplicate/missing (1 to n)"    → Cyclic Sort or XOR
```

---

## Pattern Complexity Summary

| Pattern | Typical Time | Typical Space |
|---------|--------------|---------------|
| Two Pointers | O(n) or O(n²) | O(1) |
| Sliding Window | O(n) | O(k) or O(1) |
| Binary Search | O(log n) | O(1) |
| BFS/DFS | O(V + E) | O(V) |
| Backtracking | O(2^n) or O(n!) | O(n) |
| DP | O(n²) or O(n × m) | O(n) to O(n²) |
| Heap Operations | O(n log k) | O(k) |
| Monotonic Stack | O(n) | O(n) |

---

## Interview Strategy

### Step 1: Identify the Pattern (2-3 minutes)
- Read the problem carefully
- Identify input type and constraints
- Look for pattern keywords
- Use the flowchart if stuck

### Step 2: Confirm the Pattern (1-2 minutes)
- Verify with a small example
- Check edge cases mentally
- Estimate complexity

### Step 3: Apply the Template (15-25 minutes)
- Start with the base template
- Adapt to specific problem requirements
- Handle edge cases

### Step 4: Verify (5-10 minutes)
- Walk through with test cases
- Check off-by-one errors
- Verify complexity claims

---

## Common Mistakes

1. **Jumping to code too fast**: Spend time identifying the pattern
2. **Forcing a familiar pattern**: Sometimes the obvious pattern isn't optimal
3. **Ignoring constraints**: n ≤ 1000 vs n ≤ 10^6 changes the approach
4. **Not considering edge cases**: Empty input, single element, all same values

---

## Start: [01-pattern-flowchart.md](./01-pattern-flowchart.md)

Begin with the pattern flowchart to build your decision-making framework.

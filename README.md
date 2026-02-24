# FANG+ Interview DSA Guide

A focused, interview-centric guide to Data Structures and Algorithms designed specifically to prepare you for technical interviews at FANG+ companies (Meta, Apple, Amazon, Netflix, Google, Microsoft, and top-tier startups).

This guide emphasizes **patterns over memorization**, **problem-solving strategies**, and covers the exact topics that appear in real interviews.

---

## Table of Contents

- [Why This Guide](#why-this-guide)
- [Prerequisites](#prerequisites)
- [How to Use This Guide](#how-to-use-this-guide)
- [Study Plans](#study-plans)
  - [4-Week Intensive Plan](#4-week-intensive-plan)
  - [8-Week Comprehensive Plan](#8-week-comprehensive-plan)
  - [Topic-Based Study](#topic-based-study)
- [Chapter Overview](#chapter-overview)
- [Appendices](#appendices)
- [Additional Resources](#additional-resources)

---

## Why This Guide

Most DSA resources are either too academic or too focused on competitive programming. This guide is different:

- **Interview-focused**: Every topic includes "why interviewers ask this" and common variations
- **Pattern-based**: Learn to recognize patterns rather than memorizing hundreds of solutions
- **Practical**: Covers what actually gets asked, not academic completeness
- **Time-conscious**: Includes complexity analysis critical for interview discussions

**What's NOT covered**: Competitive programming-only topics like segment trees, suffix automata, FFT, persistent structures, and advanced computational geometry. These rarely appear in FANG+ interviews, and studying them before mastering the fundamentals is a distraction.

---

## Prerequisites

Before diving in, you should be comfortable with:

### Programming Fundamentals

- **Python proficiency** (or ability to translate concepts to your preferred language)
- Basic syntax: loops, conditionals, functions
- Object-oriented basics: classes, methods, inheritance
- Understanding of references vs values

### Mathematical Foundations

- Basic algebra and arithmetic
- Understanding of logarithms (log base 2)
- Exponents and powers
- Basic probability concepts (helpful but not required)

### Computer Science Basics

- What an array is and how indexing works
- Basic understanding of memory and pointers (conceptual)
- Familiarity with at least one programming environment/IDE

### Recommended But Not Required

- Previous exposure to any DSA course or content
- Experience with LeetCode or similar platforms
- Basic understanding of recursion

---

## How to Use This Guide

### Study Approach

1. **Read the Pattern First**: Each section explains the underlying pattern before diving into problems
2. **Understand, Don't Memorize**: Focus on WHY a solution works, not just the code
3. **Practice Actively**: After reading a pattern, try problems WITHOUT looking at solutions first
4. **Time Yourself**: Set a timer (25-45 minutes for medium problems) to simulate interview conditions
5. **Review Mistakes**: Keep a log of problems you struggled with and revisit them

### Recommended Study Flow

```
Pattern Explanation → Example Walkthrough → Try Similar Problems → Review Edge Cases
```

### Tips for Effective Learning

| Do                                                 | Don't                             |
| -------------------------------------------------- | --------------------------------- |
| Struggle with a problem for 20-30 min before hints | Look at solution immediately      |
| Explain your approach out loud (mock interviewer)  | Code silently                     |
| Review problems you solved after 1 week            | Move on and never revisit         |
| Focus on patterns that connect problems            | Treat each problem as unique      |
| Practice writing clean, readable code              | Sacrifice readability for brevity |
| Trace your code manually before hitting "run"      | Rely entirely on the test button  |

### Time Targets by Difficulty

| Difficulty | Target Time   | Interview Context             |
| ---------- | ------------- | ----------------------------- |
| Easy       | 10-15 minutes | Warm-up, should solve quickly |
| Medium     | 20-30 minutes | Main interview problems       |
| Hard       | 35-45 minutes | Stretch goals, bonus points   |

---

## Study Plans

Choose the plan that fits your timeline. All plans assume 2-4 hours of focused study per day.

### 4-Week Intensive Plan

For those with a tight deadline or prior DSA experience.

| Week       | Focus Areas                    | Chapters                                                                                                           | Daily Goal   |
| ---------- | ------------------------------ | ------------------------------------------------------------------------------------------------------------------ | ------------ |
| **Week 1** | Foundations + Core Patterns    | [01](#01---complexity-analysis), [02](#02---arrays--strings), [03](#03---hashmaps--sets), [04](#04---linked-lists) | 3-4 problems |
| **Week 2** | Linear Data Structures + Trees | [05](#05---stacks--queues), [06](#06---trees), [07](#07---heaps--priority-queues)                                  | 3-4 problems |
| **Week 3** | Graphs + DP                    | [08](#08---graphs), [09](#09---dynamic-programming)                                                                | 3-4 problems |
| **Week 4** | Remaining Topics + Review      | [10](#10---binary-search), [11](#11---recursion--backtracking), [12](#12---greedy-algorithms), Review weak areas   | 4-5 problems |

**Week 1 Detailed Breakdown:**

- Day 1-2: Big-O, Arrays basics, Two Pointers
- Day 3-4: Sliding Window, Prefix Sums
- Day 5-6: HashMaps, Frequency Counting, Two-Sum variants
- Day 7: Linked Lists patterns, Review

**Week 2 Detailed Breakdown:**

- Day 1-2: Stacks (monotonic stack, valid parentheses)
- Day 3-4: Binary Trees (traversals, BST operations)
- Day 5-6: Tree problems (LCA, path sums, construction)
- Day 7: Heaps, Top-K problems, Review

**Week 3 Detailed Breakdown:**

- Day 1-2: Graph representations, BFS, DFS
- Day 3-4: Topological sort, Shortest paths
- Day 5-6: DP fundamentals, 1D DP patterns
- Day 7: 2D DP patterns, Review

**Week 4 Detailed Breakdown:**

- Day 1-2: Binary Search variants, Search space problems
- Day 3-4: Backtracking (subsets, permutations, N-Queens)
- Day 5-6: Greedy algorithms, Interval problems
- Day 7: Full review, Mock interview practice

### 8-Week Comprehensive Plan

For thorough preparation with more time for practice and reinforcement.

| Week | Focus Areas | Chapters | Daily Goal |
|------|-------------|----------|------------|
| **Week 1** | Foundations | [01](#01---complexity-analysis), [02](#02---arrays--strings) (Part 1) | 2-3 problems |
| **Week 2** | Arrays + Hashing | [02](#02---arrays--strings) (Part 2), [03](#03---hashmaps--sets) | 2-3 problems |
| **Week 3** | Linear Structures | [04](#04---linked-lists), [05](#05---stacks--queues) | 2-3 problems |
| **Week 4** | Trees Deep Dive | [06](#06---trees), [07](#07---heaps--priority-queues) | 3 problems |
| **Week 5** | Graphs | [08](#08---graphs) | 3 problems |
| **Week 6** | Dynamic Programming | [09](#09---dynamic-programming) | 3 problems |
| **Week 7** | Search + Recursion + Greedy | [10](#10---binary-search), [11](#11---recursion--backtracking), [12](#12---greedy-algorithms) | 3 problems |
| **Week 8** | Advanced + Review | [13](#13---tries), [14](#14---union-find), [15](#15---bit-manipulation), [18](#18---low-level-design), [19](#19---high-level-design), Mock interviews | 3-4 problems |

**Detailed Weekly Breakdown:**

<details>
<summary><strong>Week 1: Foundations</strong></summary>

- **Day 1-2**: Complexity analysis, Big-O notation, space/time tradeoffs
- **Day 3-4**: Arrays basics, in-place modifications
- **Day 5-6**: Two-pointer technique (same direction, opposite direction)
- **Day 7**: Review + 5 practice problems
</details>

<details>
<summary><strong>Week 2: Arrays + Hashing</strong></summary>

- **Day 1-2**: Sliding window (fixed and variable size)
- **Day 3-4**: Prefix sums, Kadane's algorithm
- **Day 5-6**: HashMap fundamentals, frequency counting
- **Day 7**: Two-sum variants, anagram problems, Review
</details>

<details>
<summary><strong>Week 3: Linear Structures</strong></summary>

- **Day 1-2**: Linked list fundamentals, dummy node technique
- **Day 3-4**: Fast/slow pointers, reversal patterns
- **Day 5-6**: Stack patterns, monotonic stack
- **Day 7**: Queue patterns, sliding window maximum, Review
</details>

<details>
<summary><strong>Week 4: Trees Deep Dive</strong></summary>

- **Day 1-2**: Tree traversals (all types), BST operations
- **Day 3-4**: Tree construction, LCA, path sums
- **Day 5-6**: Heap fundamentals, heapify, Top-K
- **Day 7**: Merge K sorted, median problems, Review
</details>

<details>
<summary><strong>Week 5: Graphs</strong></summary>

- **Day 1-2**: Graph representations, BFS basics
- **Day 3-4**: DFS patterns, connected components
- **Day 5-6**: Topological sort, cycle detection
- **Day 7**: Shortest path algorithms, Review
</details>

<details>
<summary><strong>Week 6: Dynamic Programming</strong></summary>

- **Day 1-2**: DP fundamentals, memoization vs tabulation
- **Day 3-4**: 1D DP patterns (climbing stairs, house robber, coin change)
- **Day 5-6**: 2D DP patterns (unique paths, LCS, edit distance)
- **Day 7**: Knapsack variants, Review
</details>

<details>
<summary><strong>Week 7: Search + Recursion + Greedy</strong></summary>

- **Day 1-2**: Binary search templates, search space problems
- **Day 3-4**: Backtracking fundamentals, subsets/permutations
- **Day 5-6**: Greedy algorithms, interval problems
- **Day 7**: Comprehensive review, identify weak areas
</details>

<details>
<summary><strong>Week 8: Advanced + Mock Interviews</strong></summary>

- **Day 1-2**: Tries, prefix matching
- **Day 3-4**: Union-Find, connected components
- **Day 5-6**: Bit manipulation tricks
- **Day 7**: Mock interview day (2-3 full mock interviews)
</details>

### Topic-Based Study

If you prefer to study by topic or need to focus on specific weak areas:

| Topic                 | Chapters                                                                                 | Best For                       |
| --------------------- | ---------------------------------------------------------------------------------------- | ------------------------------ |
| **Array Mastery**     | [01](#01---complexity-analysis), [02](#02---arrays--strings), [03](#03---hashmaps--sets) | Foundation building            |
| **Linked Structures** | [04](#04---linked-lists), [05](#05---stacks--queues)                                     | Pointer manipulation skills    |
| **Tree/Graph Expert** | [06](#06---trees), [08](#08---graphs)                                                    | Most common interview category |
| **DP Specialist**     | [09](#09---dynamic-programming), [12](#12---greedy-algorithms)                           | Optimization problems          |
| **Search Techniques** | [10](#10---binary-search), [11](#11---recursion--backtracking)                           | Problem-solving fundamentals   |

---

## Chapter Overview

### Core Data Structures & Algorithms

#### 01 - Complexity Analysis
[Go to Chapter](./01-complexity-analysis/)
Big-O notation, space/time tradeoffs, amortized analysis basics, and how to discuss complexity in interviews.

#### 02 - Arrays & Strings
[Go to Chapter](./02-arrays-strings/)
Two-pointer technique, sliding window, prefix sums, Kadane's algorithm, string manipulation, and matrix traversal patterns.

#### 03 - HashMaps & Sets
[Go to Chapter](./03-hashmaps-sets/)
Hash table internals, frequency counting, two-sum variants, anagram grouping, and subarray sum problems.

#### 04 - Linked Lists
[Go to Chapter](./04-linked-lists/)
Fast/slow pointers, reversal patterns, merge operations, intersection detection, and the dummy node technique.

#### 05 - Stacks & Queues
[Go to Chapter](./05-stacks-queues/)
Monotonic stack, valid parentheses, min/max stack, and sliding window maximum with deque.

#### 06 - Trees
[Go to Chapter](./06-trees/)
Tree traversals, BST operations, tree construction, LCA, path sums, diameter, and serialization.

#### 07 - Heaps & Priority Queues
[Go to Chapter](./07-heaps-priority-queues/)
Heap fundamentals, Top-K problems, merge K sorted lists, median from data stream, and task scheduling.

#### 08 - Graphs
[Go to Chapter](./08-graphs/)
Graph representations, BFS, DFS, topological sort, Dijkstra's algorithm, clone graph, and islands problems.

#### 09 - Dynamic Programming
[Go to Chapter](./09-dynamic-programming/)
DP fundamentals, 1D/2D patterns, knapsack variations, palindrome DP, interval DP, and state machine DP.

#### 10 - Binary Search
[Go to Chapter](./10-binary-search/)
Classic binary search, rotated arrays, boundary finding, and search space binary search.

#### 11 - Recursion & Backtracking
[Go to Chapter](./11-recursion-backtracking/)
Recursion fundamentals, subsets, permutations, N-Queens, word search, and pruning techniques.

#### 12 - Greedy Algorithms
[Go to Chapter](./12-greedy/)
Greedy vs DP, interval scheduling, activity selection, jump game variants, and proof techniques.

### Advanced Topics

#### 13 - Tries
[Go to Chapter](./13-tries/)
Trie implementation, prefix matching, autocomplete, and word search optimization.

#### 14 - Union-Find
[Go to Chapter](./14-union-find/)
Union-Find with path compression, union by rank, connected components, and cycle detection.

#### 15 - Bit Manipulation
[Go to Chapter](./15-bit-manipulation/)
Binary operations, XOR tricks, single number variants, counting bits, and power of two checks.

#### 16 - Math for Interviews
[Go to Chapter](./16-math-basics/)
GCD/LCM, prime numbers, modular arithmetic, random sampling, and sqrt decomposition.

#### 17 - System Design Basics
[Go to Chapter](./17-system-design-basics/)
Data structure selection for scale, trade-offs analysis, rate limiting, and LRU/LFU cache implementations.

#### 18 - Low-Level Design
[Go to Chapter](./18-low-level-design/)
Object-oriented design, SOLID principles, design patterns, and case studies like Parking Lot and ATM.

#### 19 - High-Level Design
[Go to Chapter](./19-high-level-design/)
Scalability, availability, distributed systems, databases (SQL vs NoSQL), and system design case studies.

---

## Appendices

### [Appendix A - Python Interview Cheatsheet](./A-python-cheatsheet/)

Collections module, heapq patterns, bisect for binary search, itertools, and common Python interview gotchas.

### [Appendix B - Problem Patterns](./B-problem-patterns/)

Pattern recognition flowchart, "when to use what" decision tree, and template code for each major pattern.

### [Appendix C - Company-Specific Patterns](./C-company-specific/)

Interview patterns specific to Google, Meta, Amazon (with LP integration), Microsoft, and Apple.

### [Solutions](./solutions/)

Full solutions with detailed explanations for all practice problems.

---

## Additional Resources

### Recommended Problem Lists

- **Blind 75**: The original curated list of essential problems
- **NeetCode 150**: Extended list with better coverage
- **Grind 75**: Customizable list based on available time

### Complementary Resources

- LeetCode (primary practice platform)
- AlgoExpert (video explanations)
- NeetCode.io (video walkthroughs)
- Pramp (mock interview practice)

### Books for Deep Dives

- _Cracking the Coding Interview_ by Gayle Laakmann McDowell
- _Elements of Programming Interviews_ by Aziz, Lee, Prakash
- _Algorithm Design Manual_ by Steven Skiena

---

## Contributing

Found an error or have a suggestion? Contributions are welcome. Please ensure any additions follow the interview-focused philosophy of this guide.

---

**Good luck with your interview preparation!**

Remember: Consistency beats intensity. It's better to study 2 hours daily for 8 weeks than to cram 16 hours in the final 2 days.

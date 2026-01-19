# FANG+ Interview DSA Guide: Technical Interview Preparation

## Overview

A focused, interview-centric guide to Data Structures and Algorithms designed specifically to prepare you for technical interviews at FANG+ companies (Meta, Apple, Amazon, Netflix, Google, Microsoft, and top-tier startups). This guide emphasizes patterns, problem-solving strategies, and the exact topics that appear in real interviews.

**Explicitly excluded:** Competitive programming-only topics (suffix automata, HLD, link-cut trees, FFT/NTT, persistent structures, advanced game theory, computational geometry beyond basics).

## Voice & Tone

- **Interview-focused**: Every topic includes "why interviewers ask this" and common variations
- **Pattern-based**: Emphasize recognizing patterns over memorizing solutions
- **Practical**: Focus on what gets asked, not academic completeness
- **Time-conscious**: Include time/space complexity analysis critical for interviews

## Repository Architecture

### Directory Structure
```
/
├── README.md                    # Master Introduction + Study Plan
├── 01-complexity-analysis/      # Big-O, space/time tradeoffs
├── 02-arrays-strings/           # Two pointers, sliding window, prefix sums
├── 03-hashmaps-sets/            # Hash tables, frequency counting
├── 04-linked-lists/             # Reversal, fast/slow pointers, merge
├── 05-stacks-queues/            # Monotonic stack, queue patterns
├── 06-trees/                    # BST, traversals, construction
├── 07-heaps-priority-queues/    # Top-K, merge K sorted, scheduling
├── 08-graphs/                   # BFS, DFS, shortest path, topological sort
├── 09-dynamic-programming/      # 1D/2D DP, common patterns
├── 10-binary-search/            # Search space, rotated arrays
├── 11-recursion-backtracking/   # Permutations, combinations, subsets
├── 12-greedy/                   # Interval scheduling, activity selection
├── 13-tries/                    # Prefix matching, autocomplete
├── 14-union-find/               # Connected components, cycle detection
├── 15-bit-manipulation/         # XOR tricks, bit counting
├── 16-math-basics/              # GCD, primes, modular arithmetic (interview-level)
├── 17-system-design-basics/     # Data structure choices for scale
├── A-python-cheatsheet/         # Python interview tips, stdlib
├── B-problem-patterns/          # Pattern recognition guide
├── C-company-specific/          # Company-specific problem patterns
└── solutions/                   # Full solutions with explanations
```

### Chapter README Requirements
1. **Why This Matters for Interviews**: Frequency at FANG+
2. **Core Patterns**: 3-5 patterns to master
3. **Common Mistakes**: Traps interviewers set
4. **Time Targets**: Expected solve times per difficulty

## Section File Template

### Mandatory Sections
1. **Prerequisites Callout**
   ```markdown
   > **Prerequisites:** [Topic 1](../path/to/file.md), [Topic 2](../path/to/file.md)
   ```

2. **Interview Context**: When/why this pattern appears in interviews

3. **Pattern Explanation**: Step-by-step with visual ASCII diagrams

4. **Complexity Analysis**: Table format
   ```markdown
   | Operation | Time | Space | Notes |
   |-----------|------|-------|-------|
   | Build     | O(n) | O(n)  | ...   |
   ```

5. **Implementation**: Clean Python with comments

6. **Common Variations**: How interviewers twist the problem

7. **Edge Cases**: What to check before submitting

8. **Practice Problems**: Table format, LeetCode-focused
   ```markdown
   | # | Problem | Difficulty | Pattern |
   |---|---------|------------|---------|
   | 1 | Two Sum | Easy | HashMap |
   ```

## Chapter Content (17 Chapters + 3 Appendices)

### 01 - Complexity Analysis (5-6 files)
- Big-O notation fundamentals
- Space vs time tradeoffs
- Amortized analysis basics (dynamic arrays)
- Common complexity classes with examples
- How to discuss complexity in interviews

### 02 - Arrays & Strings (15-18 files)
- Two-pointer technique (same direction, opposite direction)
- Sliding window (fixed size, variable size)
- Prefix sums and difference arrays
- Kadane's algorithm (max subarray)
- String manipulation and comparison
- In-place array modifications
- Matrix traversal patterns

### 03 - HashMaps & Sets (8-10 files)
- Hash table internals (interview-level understanding)
- Frequency counting patterns
- Two-sum variants and generalizations
- Anagram/grouping problems
- Subarray sum problems with prefix + hashmap

### 04 - Linked Lists (8-10 files)
- Fast/slow pointer (cycle detection, middle finding)
- Reversal patterns (full, partial, k-group)
- Merge operations (merge sorted, merge k)
- Intersection and palindrome detection
- Dummy node technique

### 05 - Stacks & Queues (10-12 files)
- Monotonic stack (next greater element)
- Valid parentheses and parsing
- Min/max stack implementations
- Queue using stacks, stack using queues
- Sliding window maximum with deque

### 06 - Trees (15-18 files)
- Tree traversals (inorder, preorder, postorder, level-order)
- BST operations (search, insert, delete, validate)
- Tree construction from traversals
- Lowest Common Ancestor (LCA)
- Path sum problems
- Diameter and depth calculations
- Serialization/deserialization
- Binary tree to linked list conversions

### 07 - Heaps & Priority Queues (8-10 files)
- Heap fundamentals (heapify, push, pop)
- Top-K problems (smallest, largest, frequent)
- Merge K sorted lists/arrays
- Median from data stream
- Task scheduling with cooldown

### 08 - Graphs (18-22 files)
- Graph representations (adjacency list, matrix)
- BFS (shortest path unweighted, level-order)
- DFS (connected components, cycle detection)
- Topological sort (Kahn's algorithm, DFS-based)
- Dijkstra's algorithm (shortest path weighted)
- Bellman-Ford basics (negative edges)
- Clone graph, course schedule problems
- Islands and grid problems (flood fill)
- Bipartite checking

### 09 - Dynamic Programming (18-22 files)
- DP fundamentals (overlapping subproblems, optimal substructure)
- 1D DP patterns (climbing stairs, house robber, coin change)
- 2D DP patterns (unique paths, LCS, edit distance)
- Knapsack variations (0/1, unbounded, bounded)
- Palindrome DP (longest palindromic substring/subsequence)
- Interval DP basics (matrix chain, burst balloons)
- State machine DP (best time to buy/sell stock series)
- DP on strings (word break, regex matching)

### 10 - Binary Search (8-10 files)
- Classic binary search template
- Search in rotated sorted array
- Finding boundaries (first/last occurrence)
- Search space binary search (capacity problems)
- Matrix search (search 2D matrix)

### 11 - Recursion & Backtracking (10-12 files)
- Recursion fundamentals and call stack
- Subsets generation (iterative and recursive)
- Permutations and combinations
- N-Queens and Sudoku solver
- Word search and path finding
- Pruning techniques

### 12 - Greedy (8-10 files)
- Greedy vs DP decision making
- Interval scheduling (meeting rooms, merge intervals)
- Activity selection and job scheduling
- Jump game variants
- Gas station and candy distribution
- Proof techniques for greedy correctness

### 13 - Tries (5-6 files)
- Trie implementation and operations
- Prefix matching and autocomplete
- Word search with Trie optimization
- Design search autocomplete system

### 14 - Union-Find / Disjoint Set (5-6 files)
- Union-Find with path compression
- Union by rank optimization
- Connected components problems
- Cycle detection in undirected graphs
- Accounts merge and similar problems

### 15 - Bit Manipulation (6-8 files)
- Binary representation and operations
- XOR properties and tricks
- Single number variants
- Counting bits patterns
- Power of two checks
- Hamming distance

### 16 - Math for Interviews (6-8 files)
- GCD/LCM (Euclidean algorithm)
- Prime numbers basics (sieve for small ranges)
- Modular arithmetic fundamentals
- Random sampling (reservoir sampling)
- Sqrt decomposition basics

### 17 - System Design Basics (3-4 files)
- Data structure selection for scale
- Trade-offs: HashMap vs Tree vs Heap
- Rate limiting data structures
- LRU/LFU Cache implementations

### Appendix A - Python Cheatsheet (5-6 files)
- Collections module (Counter, defaultdict, deque)
- Heapq module patterns
- Bisect module for binary search
- Itertools for combinations/permutations
- Common gotchas in Python interviews

### Appendix B - Problem Patterns (3-4 files)
- Pattern recognition flowchart
- "When to use what" decision tree
- Template code for each pattern

### Appendix C - Company-Specific (3-4 files)
- Google interview patterns
- Meta interview patterns
- Amazon interview patterns (LP integration)
- Microsoft/Apple patterns

## Problem Sources

- **Primary**: LeetCode (curated lists: Blind 75, NeetCode 150, Grind 75)
- **Secondary**: AlgoExpert, HackerRank
- **Format**: Problem name and difficulty only (no direct links)

## Code Standards

### Python Style
```python
def two_sum(nums: list[int], target: int) -> list[int]:
    """
    Find indices of two numbers that add up to target.

    Time: O(n) - single pass with hashmap
    Space: O(n) - storing seen values
    """
    seen = {}  # value -> index

    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i

    return []  # No solution found
```

## Quick Commands

```bash
# Verify structure
find . -name "README.md" | wc -l

# Check file counts per chapter
for dir in */; do echo "$dir: $(find "$dir" -name '*.md' | wc -l)"; done

# Validate no broken links
grep -r "](../" --include="*.md" | head -20
```

## Acceptance Criteria

- [ ] 17 chapter folders with proper content
- [ ] Each chapter has README.md with interview context
- [ ] ~150-180 section files (focused, not bloated)
- [ ] Each section follows interview-focused template
- [ ] Solutions directory with full explanations
- [ ] 3 appendices with practical reference material
- [ ] All code is clean Python with complexity annotations
- [ ] Problems are LeetCode-focused with difficulty labels
- [ ] No competitive programming-only topics included
- [ ] Pattern recognition emphasized throughout

## Scope Exclusions (Competitive Programming Only)

The following topics are explicitly excluded as they rarely/never appear in FANG+ interviews:
- Segment trees, Fenwick trees (BIT)
- Heavy-Light Decomposition
- Link-Cut trees
- Suffix arrays, suffix trees, suffix automata
- Aho-Corasick algorithm
- FFT/NTT polynomial multiplication
- Persistent data structures
- Computational geometry (convex hull, half-plane intersection)
- Advanced game theory (Sprague-Grundy)
- Network flow algorithms
- Advanced number theory (CRT, Lucas theorem, discrete log)
- Matrix exponentiation
- Digit DP, profile DP

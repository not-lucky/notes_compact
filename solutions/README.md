# Solutions Directory

Complete solutions to key interview problems from Blind 75 and NeetCode 150 with full explanations.

---

## Building Intuition

### How to Learn From Solutions Effectively

Reading solutions without deep engagement leads to a false sense of understanding. You can nod along to an explanation but still fail to reproduce it under interview pressure.

**The key insight**: Solutions are for *understanding*, not *memorization*. Your goal isn't to remember the code—it's to internalize the pattern so you can reconstruct it for similar problems.

### The Three-Phase Learning Model

**Phase 1: Struggle First (20-45 min)**
- Attempt the problem before reading the solution
- Getting stuck builds the context needed to appreciate the solution
- Even failed attempts prime your brain for learning

**Phase 2: Understand Deeply (15-30 min)**
- Don't just read—explain each line to yourself
- Ask "why this approach?" not just "what does this do?"
- Trace through examples by hand

**Phase 3: Rebuild From Scratch (20-30 min)**
- Close the solution and reimplement from memory
- If you can't, you don't truly understand yet
- Repeat until you can write it confidently

### Why "Building Intuition" Sections Matter

Each solution includes a "Building Intuition" section that answers:
- **Why does this work?** The core insight behind the approach
- **How would I discover this?** The thought process to arrive here
- **What pattern is this?** Connect to broader algorithm patterns

This bridges the gap between "here's the answer" and "here's how to think."

---

## When NOT to Use These Solutions

### Don't Use Solutions as a Shortcut

1. **Don't read solutions first**: Without struggling, you won't build problem-solving skills. Solutions should be your last resort, not your first.

2. **Don't copy-paste into interviews**: You need to understand deeply enough to adapt, not recite.

3. **Don't memorize solutions for every problem**: There are thousands of problems but only ~15 patterns. Learn patterns, not problems.

4. **Don't skip complexity analysis**: Understanding WHY the complexity is what it is matters more than knowing the final O(n).

### Signs You're Using Solutions Wrong

- You can explain a solution but can't write it from scratch
- You recognize problems you've seen but can't solve new ones
- You know the answer but can't explain why it works
- You've "done" 200 problems but still struggle in interviews

---

## Structure

Each solution includes:
1. **Problem Statement** - Clear summary of the problem
2. **Approach** - Step-by-step explanation of the solution strategy
3. **Implementation** - Clean Python code with detailed comments
4. **Complexity Analysis** - Time and space complexity with justification
5. **Edge Cases** - Important edge cases to handle

## Directory Layout

```
solutions/
├── 02-arrays-strings/      # Two Sum, 3Sum, Container With Most Water, etc.
├── 03-hashmaps-sets/        # Group Anagrams, Longest Consecutive, etc.
├── 04-linked-lists/         # Reverse List, Detect Cycle, Merge Lists, etc.
├── 05-stacks-queues/        # Valid Parentheses, Min Stack, etc.
├── 06-trees/                # Invert Tree, Max Depth, Same Tree, etc.
├── 07-heaps-priority-queues/# Kth Largest, Merge K Lists, etc.
├── 08-graphs/               # Number of Islands, Clone Graph, etc.
├── 09-dynamic-programming/  # Climbing Stairs, House Robber, Coin Change, etc.
├── 10-binary-search/        # Search Rotated Array, Find Minimum, etc.
├── 11-recursion-backtracking/ # Subsets, Permutations, N-Queens, etc.
├── 12-greedy/               # Jump Game, Gas Station, etc.
├── 13-tries/                # Implement Trie, Word Search II, etc.
├── 14-union-find/           # Number of Connected Components, etc.
└── 15-bit-manipulation/     # Single Number, Counting Bits, etc.
```

## Problem Coverage

### Blind 75 Essentials
- Arrays: Two Sum, Best Time to Buy/Sell Stock, Contains Duplicate, Product of Array
- Strings: Valid Anagram, Valid Palindrome, Longest Substring Without Repeating
- Linked Lists: Reverse, Detect Cycle, Merge Two Sorted, Remove Nth from End
- Trees: Max Depth, Same Tree, Invert, Subtree of Another Tree, LCA
- Graphs: Number of Islands, Clone Graph, Pacific Atlantic Water Flow
- DP: Climbing Stairs, House Robber, Coin Change, Longest Increasing Subsequence
- Intervals: Merge Intervals, Non-overlapping Intervals

### NeetCode 150 Extensions
- Additional problems covering edge cases and variations
- Advanced topics: Monotonic Stack, Tries, Union-Find

## How to Use

1. **First Attempt** - Try solving the problem yourself for 20-45 minutes
2. **Review Solution** - Study the approach and implementation
3. **Understand Complexity** - Make sure you can explain time/space analysis
4. **Practice Edge Cases** - Review what edge cases are handled
5. **Re-implement** - Code the solution from memory

## Solution Template

Each solution follows this structure:

```markdown
# Problem Name

## Problem Statement
[Clear, concise description]

## Approach
[Step-by-step explanation with intuition]

## Implementation
[Python code with comments]

## Complexity Analysis
- **Time**: O(?) - [explanation]
- **Space**: O(?) - [explanation]

## Edge Cases
- [List of edge cases handled]

## Related Problems
- [Similar problems for practice]
```

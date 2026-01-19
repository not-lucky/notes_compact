# Chapter 01: Complexity Analysis

## Why This Matters for Interviews

Complexity analysis is the **foundation of every technical interview**. Before you write a single line of code, interviewers expect you to:

1. **Estimate complexity upfront**: "My approach will be O(n log n) time and O(n) space"
2. **Justify trade-offs**: "We could use O(1) space but it would be O(n²) time"
3. **Optimize when asked**: "Can you do better than O(n²)?"

At FANG+ companies, failing to analyze complexity correctly is often an automatic rejection, even if your code works.

**Interview frequency**: Every single interview will involve complexity discussion.

---

## Core Concepts

This chapter covers:

| Section | Topic | Key Takeaway |
|---------|-------|--------------|
| [01-big-o-notation](./01-big-o-notation.md) | Big-O Fundamentals | Understand and compare growth rates |
| [02-time-complexity](./02-time-complexity.md) | Time Complexity Analysis | Analyze loops, recursion, and nested structures |
| [03-space-complexity](./03-space-complexity.md) | Space Complexity Analysis | Track memory usage including call stack |
| [04-common-patterns](./04-common-patterns.md) | Common Operation Complexities | Quick reference for data structure operations |
| [05-interview-tips](./05-interview-tips.md) | Interview Discussion Tips | How to communicate complexity effectively |

---

## Common Complexity Classes (Quick Reference)

| Complexity | Name | Example |
|------------|------|---------|
| O(1) | Constant | Array access, hash lookup |
| O(log n) | Logarithmic | Binary search |
| O(n) | Linear | Single loop through array |
| O(n log n) | Linearithmic | Merge sort, heap sort |
| O(n²) | Quadratic | Nested loops, bubble sort |
| O(2ⁿ) | Exponential | Recursive subsets generation |
| O(n!) | Factorial | Permutations |

---

## Common Mistakes Interviewers Watch For

1. **Forgetting space complexity**: Only mentioning time, ignoring auxiliary space
2. **Missing recursion stack space**: Recursive solutions often use O(n) or O(log n) stack space
3. **Wrong loop analysis**: Assuming nested loops are always O(n²)
4. **Ignoring input constraints**: Not considering if n could be very large or very small
5. **Over-optimizing**: Spending 20 minutes optimizing O(n log n) to O(n) when not asked

---

## Time Targets

| Task | Target Time |
|------|-------------|
| State complexity of your approach | 30 seconds |
| Justify a trade-off decision | 1 minute |
| Optimize when prompted | 2-5 minutes |

---

## Prerequisites

This is the first chapter - no prerequisites required. However, basic familiarity with:
- Loops and conditionals
- Basic math (exponents, logarithms)
- What an algorithm is

---

## Next Steps

Start with [01-big-o-notation.md](./01-big-o-notation.md) to build your foundation.

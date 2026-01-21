# Chapter 02: Arrays & Strings

## Why This Matters for Interviews

Arrays and strings are the **most frequently tested** data structures in FANG+ interviews. They appear in 60-70% of all coding questions because:

1. **Universal foundation**: Every language has arrays/strings
2. **Easy to explain**: No complex setup needed to discuss the problem
3. **Pattern-rich**: Tests problem-solving ability across multiple techniques
4. **Scalable difficulty**: From "Two Sum" (easy) to "Longest Valid Parentheses" (hard)

At top companies, you'll face 1-2 array/string problems in almost every coding round.

**Interview frequency**: Very high. Expect 2-3 questions per interview loop.

---

## Core Patterns to Master

| Pattern | Frequency | Key Problems |
|---------|-----------|--------------|
| Two Pointers | Very High | 3Sum, Container With Most Water, Remove Duplicates |
| Sliding Window | Very High | Longest Substring Without Repeating, Minimum Window Substring |
| Prefix Sum | High | Subarray Sum Equals K, Range Sum Query |
| Kadane's Algorithm | High | Maximum Subarray, Maximum Product Subarray |
| In-Place Modifications | Medium | Move Zeroes, Sort Colors, Rotate Array |
| Matrix Traversal | Medium | Spiral Matrix, Rotate Image, Search 2D Matrix |

---

## Chapter Sections

| Section | Topic | Key Takeaway |
|---------|-------|--------------|
| [01-array-basics](./01-array-basics.md) | Array Fundamentals | Operations, traversal, rotation basics |
| [02-two-pointers-same-direction](./02-two-pointers-same-direction.md) | Two Pointers (Same Direction) | Fast/slow pointer technique |
| [03-two-pointers-opposite](./03-two-pointers-opposite.md) | Two Pointers (Opposite Direction) | Converging pointers from both ends |
| [04-sliding-window-fixed](./04-sliding-window-fixed.md) | Fixed-Size Sliding Window | Window of constant size k |
| [05-sliding-window-variable](./05-sliding-window-variable.md) | Variable-Size Sliding Window | Expand/shrink based on condition |
| [06-prefix-sum](./06-prefix-sum.md) | Prefix Sum | O(1) range queries after O(n) preprocessing |
| [07-difference-array](./07-difference-array.md) | Difference Array | Efficient range update operations |
| [08-kadanes-algorithm](./08-kadanes-algorithm.md) | Kadane's Algorithm | Maximum subarray in O(n) |
| [09-string-basics](./09-string-basics.md) | String Fundamentals | Immutability, comparison, manipulation |
| [10-string-matching](./10-string-matching.md) | String Matching | Substring search patterns |
| [11-anagram-problems](./11-anagram-problems.md) | Anagram Problems | Character frequency techniques |
| [12-palindrome-strings](./12-palindrome-strings.md) | Palindrome Problems | Check, expand, and construct palindromes |
| [13-matrix-traversal](./13-matrix-traversal.md) | Matrix Traversal | Spiral, diagonal, and search patterns |
| [14-in-place-modifications](./14-in-place-modifications.md) | In-Place Modifications | Modify array without extra space |
| [15-interval-problems](./15-interval-problems.md) | Interval Problems | Merge, insert, and schedule intervals |

---

## Common Mistakes Interviewers Watch For

1. **Off-by-one errors**: Especially in two-pointer and sliding window problems
2. **Not handling empty input**: Always check `if not arr: return ...`
3. **Modifying array while iterating**: Use indices or work backwards
4. **String immutability confusion**: Building strings with `+=` is O(n²)
5. **Missing edge cases**: Single element, all same values, already sorted
6. **Forgetting to return**: Especially after breaking from loops

---

## Time Targets

| Difficulty | Target Time | Examples |
|------------|-------------|----------|
| Easy | 10-15 min | Two Sum, Valid Anagram, Reverse String |
| Medium | 15-25 min | 3Sum, Longest Substring, Merge Intervals |
| Hard | 25-40 min | Minimum Window Substring, Trapping Rain Water |

---

## Pattern Recognition Guide

```
"Find pair/triplet that sums to..."     → Two Pointers (after sorting)
"Longest/shortest substring with..."    → Sliding Window (variable)
"Maximum sum of subarray of size k"     → Sliding Window (fixed)
"Range sum queries"                     → Prefix Sum
"Maximum contiguous subarray"           → Kadane's Algorithm
"Rearrange in-place"                    → Two Pointers (same direction)
"Rotate matrix/array"                   → Reverse-based technique
"Character frequency/anagram"           → HashMap + Array (26 buckets)
```

---

## System Design Connectors

DSA patterns aren't just for interviews; they power the infrastructure we use daily.

| DSA Pattern | System Design Application | Why it works |
| :--- | :--- | :--- |
| **Prefix Sums** | **Time-Series Monitoring** | Efficiently calculate average metrics over any time window in $O(1)$. |
| **Sliding Window** | **Rate Limiters** | Tracking requests in the last $T$ seconds to prevent API abuse. |
| **Difference Arrays** | **Video Encoding / Delta Encoding** | Storing only the change between frames/versions rather than full state. |
| **Two Pointers** | **Database Buffer Pools** | Managing LRU-style eviction policies in memory buffers. |
| **In-Place Modification** | **Memory Management** | Defragmenting memory or garbage collection without allocating new heaps. |

---

## Visualizing Array State
```mermaid
graph LR
    A[Start] --> B{i < length?}
    B -- Yes --> C[Process arr[i]]
    C --> D[i++]
    D --> B
    B -- No --> E[End]
```

---

## Prerequisites

> **Prerequisites:** [01-complexity-analysis](../01-complexity-analysis/README.md)

Understanding Big-O is essential before this chapter, as every technique involves analyzing time/space trade-offs.

---

## Next Steps

Start with [01-array-basics.md](./01-array-basics.md) for foundational array operations, then progress through patterns in order. The two-pointer and sliding window sections are the highest priority for interviews.

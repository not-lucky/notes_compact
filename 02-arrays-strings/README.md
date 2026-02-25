# Chapter 02: Arrays & Strings

## Why This Matters for Interviews

Arrays and strings are the **most frequently tested** data structures in FANG+ interviews. They appear in 60-70% of all coding questions because:

1. **Universal foundation**: Every language has arrays/strings as primitives.
2. **Easy to explain**: No complex setup needed to discuss the problem context.
3. **Pattern-rich**: Tests problem-solving ability across multiple algorithmic techniques.
4. **Scalable difficulty**: From simple lookups to complex multi-pointer optimizations.

**Mental Model**: Think of an array as a row of connected, numbered mailboxes. You can instantly access any mailbox if you know its number ($O(1)$ time). But if you need to insert a new mailbox in the middle, you have to shift all the subsequent mailboxes down to make room ($O(n)$ time).

## Python Specifics to Remember

Before diving into the patterns, keep these critical Python specifics in mind:

1. **Lists are Dynamic Arrays**: A Python `list` is a dynamic array, not a linked list. Appending an element (`list.append()`) is **amortized $O(1)$** time. However, inserting or deleting from the middle (`list.insert(0, val)`) takes $O(n)$ time because all subsequent elements must be shifted in memory.
2. **String Concatenation**: Python strings are immutable. Building a string in a loop using `+=` forces Python to allocate new memory and copy the old characters each time. This results in **$O(n^2)$ time**. Always use `''.join(list_of_strings)` for linear **$O(n)$** concatenation.
3. **Hash Maps (Dictionaries)**: Lookups, insertions, and deletions in Python `dict`s and `set`s are **amortized $O(1)$** time on average. However, it's crucial to mention to your interviewer that the **worst-case time complexity is $O(n)$** due to potential hash collisions.
4. **Tight Bounds ($\Theta$)**: Always provide the tightest bound possible. If an algorithm always iterates through exactly $n$ elements, say $O(n)$, not $O(n^2)$, even though mathematically $O(n^2)$ is technically an upper bound. Interviewers expect the Big-Theta ($\Theta$) tight bound.
5. **Recursive Space Complexity**: If you use recursion for any array or string traversal, you **must** account for the recursive call stack in your space complexity analysis. An algorithm that recurses $n$ times has an $O(n)$ space complexity footprint, even if it uses no extra variables.

---

## Core Patterns to Master

| Pattern                | Frequency | Key Problems                                                  |
| ---------------------- | --------- | ------------------------------------------------------------- |
| Two Pointers           | Very High | 3Sum, Container With Most Water, Remove Duplicates            |
| Sliding Window         | Very High | Longest Substring Without Repeating, Minimum Window Substring |
| Prefix Sum             | High      | Subarray Sum Equals K, Range Sum Query                        |
| Kadane's Algorithm     | High      | Maximum Subarray, Maximum Product Subarray                    |
| In-Place Modifications | Medium    | Move Zeroes, Sort Colors, Rotate Array                        |
| Matrix Traversal       | Medium    | Spiral Matrix, Rotate Image, Search 2D Matrix                 |

---

## Pattern Recognition Guide

When you hear... | Think...
--- | ---
"Find a pair/triplet that sums to X..." | **Two Pointers** (often after sorting the array)
"Longest/shortest contiguous substring with..." | **Variable Sliding Window**
"Maximum sum of a subarray of size $k$" | **Fixed Sliding Window**
"Fast range sum queries over a static array" | **Prefix Sum**
"Maximum contiguous subarray sum" | **Kadane's Algorithm**
"Rearrange elements in-place with $O(1)$ space" | **Two Pointers** (same direction / swap logic)
"Character frequency or anagrams" | **Hash Map** or **Fixed Array (26 buckets)**

---

## Chapter Sections

| Section                                                               | Topic                             | Key Takeaway                                |
| --------------------------------------------------------------------- | --------------------------------- | ------------------------------------------- |
| [01-array-basics](./01-array-basics.md)                               | Array Fundamentals                | Dynamic arrays, shifting, traversal         |
| [02-two-pointers-same-direction](./02-two-pointers-same-direction.md) | Two Pointers (Same Direction)     | Fast/slow pointer technique, in-place swaps |
| [03-two-pointers-opposite](./03-two-pointers-opposite.md)             | Two Pointers (Opposite Direction) | Converging pointers from both ends          |
| [04-sliding-window-fixed](./04-sliding-window-fixed.md)               | Fixed-Size Sliding Window         | Maintaining a window of constant size $k$   |
| [05-sliding-window-variable](./05-sliding-window-variable.md)         | Variable-Size Sliding Window      | Expand/shrink logic based on conditions     |
| [06-prefix-sum](./06-prefix-sum.md)                                   | Prefix Sum                        | $O(1)$ range queries after $O(n)$ setup     |
| [07-difference-array](./07-difference-array.md)                       | Difference Array                  | Efficient overlapping range updates         |
| [08-kadanes-algorithm](./08-kadanes-algorithm.md)                     | Kadane's Algorithm                | Maximum subarray sum in $O(n)$              |
| [09-string-basics](./09-string-basics.md)                             | String Fundamentals               | Immutability, `.join()`, parsing            |
| [10-string-matching](./10-string-matching.md)                         | String Matching                   | Substring search, Rabin-Karp, KMP basics    |
| [11-anagram-problems](./11-anagram-problems.md)                       | Anagram Problems                  | Character frequency counting techniques     |
| [12-palindrome-strings](./12-palindrome-strings.md)                   | Palindrome Problems               | Expand-from-center, two pointers check      |
| [13-matrix-traversal](./13-matrix-traversal.md)                       | Matrix Traversal                  | Spiral, diagonal, grid coordinate math      |
| [14-in-place-modifications](./14-in-place-modifications.md)           | In-Place Modifications            | $O(1)$ space tricks, indexing as state      |
| [15-interval-problems](./15-interval-problems.md)                     | Interval Problems                 | Sorting intervals, merging overlaps         |

---

## Common Mistakes Interviewers Watch For

1. **Off-by-one errors**: Extremely common in two-pointer and sliding window problems. Carefully trace the logic for window sizes (`right - left + 1`).
2. **String immutability confusion**: Using `+=` instead of `.join()`. Interviewers will dock points for saying string concatenation in a loop is $O(n)$. It is $O(n^2)$.
3. **Ignoring hash map worst-case**: Failing to mention that while hash map lookups are amortized $O(1)$, worst-case collisions can degrade to $O(n)$.
4. **Modifying the array while iterating**: Never remove elements from an array while traversing it with a standard `for` loop. Work backwards or use a `while` loop with manual index control.
5. **Not handling edge cases**: Empty strings, arrays with 1 element, arrays with all identical values, negative numbers.

---

## Code Example: Modern Python Standards

Throughout this chapter, we will use modern Python features. You should do the same in interviews:

```python
from typing import Optional

def two_sum(nums: list[int], target: int) -> list[int]:
    """
    Finds indices of two numbers that add up to the target.

    Time Complexity: O(n) tightly bound, as we iterate at most n times.
    Space Complexity: O(n) for the hash map storing seen values.
    """
    seen: dict[int, int] = {}

    for i, num in enumerate(nums):
        complement = target - num
        # Hash map lookup is amortized O(1), worst-case O(n)
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i

    return []
```

---

## Time Targets

| Difficulty | Target Time | Examples                                      |
| ---------- | ----------- | --------------------------------------------- |
| Easy       | 10-15 min   | Two Sum, Valid Anagram, Reverse String        |
| Medium     | 15-25 min   | 3Sum, Longest Substring, Merge Intervals      |
| Hard       | 30-40 min   | Minimum Window Substring, Trapping Rain Water |

---

## Prerequisites

> **Prerequisites:** [01-complexity-analysis](../01-complexity-analysis/README.md)

Understanding Big-O is essential before this chapter. Ensure you are comfortable distinguishing between amortized and worst-case complexities, recognizing recursive call stack overhead, and calculating tight bounds ($\Theta$).

---

## Next Steps

Start with [01-array-basics.md](./01-array-basics.md) for foundational array operations, then progress through patterns in order. The two-pointer and sliding window sections are the highest priority for interviews.
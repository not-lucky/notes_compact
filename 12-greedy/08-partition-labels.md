# Partition Labels

> **Prerequisites:** [Greedy Basics](./01-greedy-basics.md), [Merge Intervals](./03-merge-intervals.md)

## Interview Context

Partition Labels is a classic problem that tests:

1. **Interval transformation**: Recognizing that character appearances define intervals `[first, last]`.
2. **Greedy partitioning**: Finding optimal split points in a single pass.
3. **HashMap usage**: Tracking the last occurrence of each character.
4. **Pattern recognition**: Identifying interval merging problems in disguise.

**Constraints & Assumptions**:
- Input string contains only lowercase English letters (`'a'`-`'z'`).
- String length: typically `1 <= s.length <= 500`.
- Empty string is usually not a valid input, but handle it gracefully if needed.

---

## Problem Statement

You are given a string `s`. We want to partition the string into as many parts as possible so that **each letter appears in at most one part**.

Return a list of integers representing the size of these parts.

```text
Input:  s = "ababcbacadefegdehijhklij"
Output: [9, 7, 8]

Explanation:
The partition is "ababcbaca", "defegde", "hijhklij".
- 'a', 'b', and 'c' only appear in the first part (size 9).
- 'd', 'e', 'f', and 'g' only appear in the second part (size 7).
- 'h', 'i', 'j', 'k', and 'l' only appear in the third part (size 8).
```

---

## Building Intuition

### The "Last Appearance" Rule

Every character in a partition must have ALL its occurrences within that partition. This means: **once you include a character, you must extend the current partition at least to its LAST occurrence.**

```text
s = "ababcbaca"
     012345678

'a' appears at: 0, 2, 6, 8     → last at 8
'b' appears at: 1, 3, 5        → last at 5
'c' appears at: 4, 7           → last at 7

Starting at index 0:
- We see 'a', so the partition MUST extend to at least index 8.
- Along the way, we see 'b' (needs index 5) and 'c' (needs index 7).
- The farthest requirement is index 8 (from 'a').
- When we reach index 8, all requirements are satisfied!
- First partition: indices 0-8, length 9.
```

### Mental Model: Character "Lifespans"

Think of each character as having a "lifespan" from its first to its last occurrence:

```text
s = "ababcbacadefegdehijhklij"
     0         1         2
     012345678901234567890123    (24 characters, indices 0-23)

Character lifespans (first occurrence → last occurrence):
a: [0,  8]  |---------|
b: [1,  5]   |----|
c: [4,  7]       |---|
d: [9, 14]            |-----|
e: [10,15]             |-----|
f: [11,11]              |
g: [13,13]                |
h: [16,19]                    |----|
i: [17,22]                     |------|
j: [18,23]                      |------|
k: [20,20]                          |
l: [21,21]                           |
             ├─ part 1 ─┤├─ part 2 ─┤├── part 3 ──┤
```

Overlapping lifespans MUST be in the same partition. Non-overlapping lifespans CAN be in different partitions.

### Why This Is Really Merge Intervals

Each character creates an interval `[first_occurrence, last_occurrence]`. Overlapping intervals must be merged into the same partition. This is exactly the **merge intervals** pattern!

But wait, we don't need to explicitly sort the intervals! Why?
Because as we scan the string from left to right, we inherently encounter each character's *first* occurrence in sorted order. The string itself acts as our pre-sorted list of interval start times.

### The Greedy "Extending Horizon" Approach

We don't need to explicitly build and merge intervals. We only need the **last occurrence** of each character. Then we scan left to right, maintaining a "horizon"—the farthest index we *must* reach before we can close the current partition.

The horizon can only grow (or stay the same) during a partition; it never shrinks. The exact moment our current index `i` catches up to the horizon, every character in the current partition has been fully accounted for, and we can make a cut!

---

## Solution

```python
def partition_labels(s: str) -> list[int]:
    """
    Partition a string into as many parts as possible so that each letter
    appears in at most one part.

    Time: O(N)
    Space: O(1)
    """
    if not s:
        return []

    # Step 1: Record the last occurrence index of every character
    last_occurrence = {char: i for i, char in enumerate(s)}

    result = []
    partition_start = 0
    partition_end = 0  # "horizon" -- farthest index we must reach

    # Step 2: Scan left to right, extending the horizon as needed
    for i, char in enumerate(s):
        # Extend horizon to include all occurrences of the current character
        partition_end = max(partition_end, last_occurrence[char])

        # When current index reaches horizon, every character in
        # [partition_start, partition_end] is fully contained
        if i == partition_end:
            result.append(partition_end - partition_start + 1)
            partition_start = i + 1

    return result
```

### Complexity Analysis

- **Time Complexity:** $O(N)$, where $N$ is the length of the string.
  - First pass: Build `last_occurrence` dictionary — $O(N)$
  - Second pass: Scan to find partitions — $O(N)$
  - Dictionary lookups and `max()` operations are $O(1)$.
- **Space Complexity:** $O(1)$ auxiliary space.
  - The `last_occurrence` dictionary stores at most 26 entries (one per lowercase English letter), taking $O(26) = O(1)$ space.
  - (The output list is generally not counted as auxiliary space).

---

## Alternative Approaches

### 1. Explicit Merge Intervals (For Understanding)

To make the connection to Merge Intervals concrete, here is a solution that explicitly builds character intervals and merges them.

```python
def partition_labels_via_merge(s: str) -> list[int]:
    if not s: return []

    # Build [first, last] interval for each character
    first, last = {}, {}
    for i, char in enumerate(s):
        if char not in first: first[char] = i
        last[char] = i

    # Create intervals sorted by first occurrence (at most 26 intervals)
    intervals = sorted([[first[c], last[c]] for c in first])

    # Standard merge intervals
    merged = [intervals[0]]
    for start, end in intervals[1:]:
        if start <= merged[-1][1]:
            # Overlap: extend
            merged[-1][1] = max(merged[-1][1], end)
        else:
            # Gap: new partition
            merged.append([start, end])

    return [end - start + 1 for start, end in merged]
```
*Note: This is strictly for educational purposes to prove the relationship to Merge Intervals. The single-pass horizon approach is much cleaner for interviews.*

### 2. Array Instead of HashMap (Micro-optimization)

Since the input contains only lowercase English letters, we can use a fixed-size array of length 26 instead of a hash map for slightly better constant factors.

```python
def partition_labels_array(s: str) -> list[int]:
    last_occurrence = [0] * 26
    for i, char in enumerate(s):
        last_occurrence[ord(char) - ord('a')] = i

    result = []
    start = end = 0

    for i, char in enumerate(s):
        end = max(end, last_occurrence[ord(char) - ord('a')])
        if i == end:
            result.append(end - start + 1)
            start = i + 1

    return result
```

---

## Visual Trace

```text
s = "ababcbacadefegdehijhklij"
     012345678901234567890123   (indices 0-23)

Step 1: Build last_occurrence
last = {a:8, b:5, c:7, d:14, e:15, f:11, g:13, h:19, i:22, j:23, k:20, l:21}

Step 2: Scan left to right
─────────────────────────────────────────────────────────────────────────────
 i  char  last[char]  end = max(end, last)  Action
─────────────────────────────────────────────────────────────────────────────
 0   'a'      8        max(0,  8) =  8
 1   'b'      5        max(8,  5) =  8
 2   'a'      8        max(8,  8) =  8
...
 8   'a'      8        max(8,  8) =  8      i == end! CUT. size = 8-0+1 = 9
─────────────────────────────────────────────────────────────────────────────
 9   'd'     14        max(8, 14) = 14      (new partition, start=9)
10   'e'     15        max(14,15) = 15      horizon extends!
...
15   'e'     15        max(15,15) = 15      i == end! CUT. size = 15-9+1 = 7
─────────────────────────────────────────────────────────────────────────────
16   'h'     19        max(15,19) = 19      (new partition, start=16)
17   'i'     22        max(19,22) = 22      horizon extends!
18   'j'     23        max(22,23) = 23      horizon extends!
...
23   'j'     23        max(23,23) = 23      i == end! CUT. size = 23-16+1 = 8
─────────────────────────────────────────────────────────────────────────────

Result: [9, 7, 8]
```

---

## Why Greedy Works

**Greedy Choice**: End each partition at the *earliest* valid point (the exact moment `i` reaches `partition_end`).

**Why is this optimal?**
1. **Validity**: We *cannot* cut before `partition_end`. If we did, some character in the current partition would have another occurrence later in the string, violating the rule that a character appears in only one part.
2. **Maximality**: We *should not* extend past `partition_end`. Extending would merge the current valid partition with the next one, resulting in fewer total partitions. Since the goal is to maximize the number of partitions, we must cut as early as possible.

---

## Common Mistakes

| Mistake | Consequence | Correction |
| :--- | :--- | :--- |
| **Using first occurrence instead of last** | You cut too early, leaving character occurrences outside. | Track the **last** occurrence to ensure containment. |
| **Cutting when a character repeats** | Doesn't guarantee *all* future occurrences are contained. | Only cut when `i == partition_end` (horizon reached). |
| **Explicitly sorting intervals** | Works, but does unnecessary $O(N \log N)$ work. | Scan the string directly; the left-to-right order *is* the sorted start time. |
| **Off-by-one in partition size** | Outputting `end - start` instead of `end - start + 1`. | Array length for an inclusive range is `end - start + 1`. |

---

## Practice Problems

| Problem | Difficulty | Key Insight |
| :--- | :--- | :--- |
| **[Partition Labels (LC 763)](https://leetcode.com/problems/partition-labels/)** | Medium | The core problem. Track last occurrence, greedily extend horizon. |
| **[Optimal Partition of String (LC 2405)](https://leetcode.com/problems/optimal-partition-of-string/)** | Medium | Minimizing partitions so no letter repeats within a part. Greedy: use a set, cut the moment you see a duplicate. |
| **[Split Array into Consecutive Subsequences (LC 659)](https://leetcode.com/problems/split-array-into-consecutive-subsequences/)** | Medium | Advanced greedy using hashmaps to track subsequence endings and available counts. |

---

## Chapter Summary: Greedy Algorithms

You've completed Chapter 12: Greedy Algorithms!

### Core Patterns Mastered

| Pattern | Mental Model | Classic Problems |
| :--- | :--- | :--- |
| **Interval Scheduling** | Sort by end time, pick the earliest finisher. | Activity Selection, Non-overlapping Intervals |
| **Merge Intervals** | Sort by start time, extend the end. | Merge Intervals, Insert Interval, Partition Labels |
| **Heap-Based Greedy** | Track the dynamic min/max of a resource. | Meeting Rooms II, Task Scheduler |
| **Jump/Reach** | Track the farthest reachable frontier. | Jump Game I & II |
| **Reset on Deficit** | Reset your starting point when an accumulator drops below 0. | Gas Station, Maximum Subarray |
| **Two-Pass** | Resolve neighborhood constraints left-to-right, then right-to-left. | Candy Distribution, Trapping Rain Water |

**The Golden Rule of Greedy Algorithms:**
Always try to break your greedy idea with counter-examples before writing code. If you can't break it, look for a way to prove that the locally optimal choice guarantees the global optimum.

---

## Next Chapter: [13-tries/README.md](../13-tries/README.md)

Learn about Tries - the prefix tree data structure for string problems.

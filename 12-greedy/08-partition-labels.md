# Partition Labels

> **Prerequisites:** [Greedy Basics](./01-greedy-basics.md), [Merge Intervals](./03-merge-intervals.md)

## Interview Context

Partition labels tests:
1. **Interval transformation**: Converting string to intervals
2. **Greedy partitioning**: Finding optimal split points
3. **HashMap usage**: Tracking last occurrences
4. **Pattern recognition**: Interval covering in disguise

---

## Problem Statement

Partition a string into as many parts as possible so that each letter appears in at most one part.

```
Input:  s = "ababcbacadefegdehijhklij"
Output: [9, 7, 8]

Explanation:
Partition: "ababcbaca", "defegde", "hijhklij"
- 'a' only in first part
- 'd' only in second part
- 'h' only in third part
- etc.
```

---

## The Core Insight

**Each character defines an interval: [first occurrence, last occurrence]**

For partitioning:
- A partition must include all occurrences of any character it contains
- Find the smallest valid partition at each step
- The partition ends at the farthest "last occurrence" of any character in it

```
s = "ababcbaca..."

Character intervals:
a: [0, 8]  (first at 0, last at 8)
b: [1, 5]
c: [4, 7]

Starting at index 0:
- We include 'a', so partition must extend to at least index 8
- Along the way, we include 'b' (extends to 5) and 'c' (extends to 7)
- Max extension = 8
- Partition ends at 8
```

---

## Solution

```python
def partition_labels(s: str) -> list[int]:
    """
    Partition string so each letter appears in at most one part.

    Greedy: Track last occurrence of each char, extend partition to include all.

    Time: O(n)
    Space: O(1) - at most 26 characters
    """
    # Find last occurrence of each character
    last = {char: i for i, char in enumerate(s)}

    result = []
    start = 0
    end = 0

    for i, char in enumerate(s):
        # Extend partition to include all of current char
        end = max(end, last[char])

        if i == end:
            # We've reached the end of current partition
            result.append(end - start + 1)
            start = i + 1

    return result
```

---

## Visual Trace

```
s = "ababcbacadefegdehijhklij"
     0123456789...

Last occurrence:
a: 8, b: 5, c: 7, d: 14, e: 15, f: 11, g: 13, h: 19, i: 22, j: 23, k: 20, l: 21

Scan:
i=0 'a': end = max(0, 8) = 8
i=1 'b': end = max(8, 5) = 8
i=2 'a': end = max(8, 8) = 8
i=3 'b': end = max(8, 5) = 8
i=4 'c': end = max(8, 7) = 8
i=5 'b': end = max(8, 5) = 8
i=6 'a': end = max(8, 8) = 8
i=7 'c': end = max(8, 7) = 8
i=8 'a': end = max(8, 8) = 8
       i == end → partition! length = 8 - 0 + 1 = 9

i=9  'd': end = max(9, 14) = 14
i=10 'e': end = max(14, 15) = 15
i=11 'f': end = max(15, 11) = 15
i=12 'e': end = max(15, 15) = 15
i=13 'g': end = max(15, 13) = 15
i=14 'd': end = max(15, 14) = 15
i=15 'e': end = max(15, 15) = 15
        i == end → partition! length = 15 - 9 + 1 = 7

i=16 'h': end = max(16, 19) = 19
...
i=23 'j': end = max(23, 23) = 23
        i == end → partition! length = 23 - 16 + 1 = 8

Result: [9, 7, 8]
```

---

## Why Greedy Works

**Greedy Choice**: End partition as soon as all included characters are complete.

**Why it's optimal**:
1. We can't end earlier (would split a character)
2. Ending later would only make this partition bigger
3. More partitions means smaller partitions (goal: maximize count)

**Proof by construction**:
- At position `i`, if `i == end`, no character in `[start, i]` appears after `i`
- So `[start, i]` is a valid partition
- Starting a new partition at `i+1` is safe

---

## Interval Representation

An alternative view using explicit intervals:

```python
def partition_labels_intervals(s: str) -> list[int]:
    """
    Convert to intervals, then merge and partition.

    Time: O(n log n) due to sorting
    Space: O(26) = O(1)
    """
    # Build intervals for each character
    first = {}
    last = {}

    for i, char in enumerate(s):
        if char not in first:
            first[char] = i
        last[char] = i

    # Create intervals
    intervals = [(first[c], last[c]) for c in first]
    intervals.sort()

    # Merge overlapping intervals
    merged = []
    for start, end in intervals:
        if merged and start <= merged[-1][1]:
            merged[-1] = (merged[-1][0], max(merged[-1][1], end))
        else:
            merged.append((start, end))

    # Convert to lengths
    return [end - start + 1 for start, end in merged]
```

---

## Related Problems

### Merge Intervals

```python
def merge(intervals: list[list[int]]) -> list[list[int]]:
    """Standard merge intervals for reference."""
    intervals.sort()
    merged = [intervals[0]]

    for start, end in intervals[1:]:
        if start <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])

    return merged
```

### Maximum Number of Non-overlapping Substrings

```python
def max_num_of_substrings(s: str) -> list[str]:
    """
    Find maximum number of valid non-overlapping substrings.
    Each substring contains all occurrences of its characters.

    Time: O(n)
    Space: O(1)
    """
    n = len(s)

    # For each character, find bounds of valid substring containing it
    first = {}
    last = {}
    for i, c in enumerate(s):
        if c not in first:
            first[c] = i
        last[c] = i

    # Get valid interval for each character
    def get_interval(c):
        start = first[c]
        end = last[c]
        i = start
        while i <= end:
            char = s[i]
            if first[char] < start:
                return None  # Invalid: would need to extend left
            end = max(end, last[char])
            i += 1
        return (start, end)

    # Collect all valid intervals
    intervals = []
    for c in first:
        interval = get_interval(c)
        if interval:
            intervals.append(interval)

    # Sort by end, then by start (prefer smaller)
    intervals.sort(key=lambda x: (x[1], x[0]))

    result = []
    prev_end = -1
    for start, end in intervals:
        if start > prev_end:
            result.append(s[start:end + 1])
            prev_end = end

    return result
```

### Smallest Sufficient Team (Related Pattern)

Finding minimum covering - different approach but similar thinking.

---

## Complexity Analysis

| Approach | Time | Space | Notes |
|----------|------|-------|-------|
| Single pass greedy | O(n) | O(1) | Most efficient |
| Interval-based | O(n log n) | O(26) | More intuitive |
| Brute force | O(n²) | O(n) | Check each partition |

---

## Edge Cases

- [ ] Single character → [1]
- [ ] All same character → [n] (one partition)
- [ ] All unique characters → [1, 1, 1, ...] (each char is own partition)
- [ ] Empty string → []
- [ ] Two characters alternating → one partition

---

## Pattern Recognition

Partition Labels is really "interval covering" in disguise:

1. Each character creates an interval [first, last]
2. All overlapping intervals must be in same partition
3. Find minimum cuts to separate non-overlapping groups
4. Equivalent to: merge overlapping intervals, count groups

---

## Practice Problems

| # | Problem | Difficulty | Key Insight |
|---|---------|------------|-------------|
| 1 | Partition Labels | Medium | Track last occurrence, greedy extend |
| 2 | Merge Intervals | Medium | Sort by start, merge overlapping |
| 3 | Maximum Number of Non-overlapping Substrings | Hard | Valid substring intervals |
| 4 | Optimal Partition of String | Medium | Partition to minimize duplicates |
| 5 | Video Stitching | Medium | Interval covering |

---

## Interview Tips

1. **Explain the interval insight**: Characters define intervals
2. **Track last occurrence**: Build hashmap first
3. **Trace an example**: Show `end` extending as you scan
4. **Mention alternative**: Explicit interval merging works too
5. **Connect to patterns**: This is interval merging in disguise

---

## Key Takeaways

1. Each character creates interval [first occurrence, last occurrence]
2. Greedy: track maximum "last occurrence" seen in current partition
3. End partition when current index equals max last occurrence
4. O(n) time with O(1) space (26 characters max)
5. Equivalent to merging overlapping character intervals

---

## Chapter Summary

You've completed Chapter 12: Greedy Algorithms! Key patterns learned:

| Pattern | Problems | Key Technique |
|---------|----------|---------------|
| Interval Scheduling | Activity selection | Sort by end time |
| Merge Intervals | Overlapping intervals | Sort by start time |
| Meeting Rooms | Resource allocation | Min-heap or sweep line |
| Jump/Reach | Jump games, gas station | Track farthest reachable |
| Two-Pass | Candy distribution | Forward + backward pass |
| Partition | Partition labels | Track last occurrence |

---

## Next Chapter: [13-tries/README.md](../13-tries/README.md)

Learn about Tries - the prefix tree data structure for string problems.

# Solutions: Partition Labels

## 1. Partition Labels

**Problem Statement**:
You are given a string `s`. We want to partition the string into as many parts as possible so that each letter appears in at most one part. Note that the partition is done so that after concatenating all the parts in order, the resultant string should be `s`. Return a list of integers representing the size of these parts.

**Examples & Edge Cases**:

- **Example 1**:
  - Input: `s = "ababcbacadefegdehijhklij"`
  - Output: `[9,7,8]`
  - Explanation: The partition is "ababcbaca", "defegde", "hijhklij". This is a partition so that each letter appears in at most one part. A partition like "ababcbacadefegde", "hijhklij" is incorrect because it has fewer parts.
- **Example 2**:
  - Input: `s = "eccbbbbdec"`
  - Output: `[10]`
- **Edge Cases**:
  - All characters are the same: `[n]`.
  - All characters are unique: `[1, 1, 1, ...1]`.

**Optimal Python Solution**:

```python
def partitionLabels(s: str) -> list[int]:
    """
    Greedy approach: Track the last occurrence of each character.
    Extend the partition until we reach the last occurrence of all characters
    included in the current segment.
    """
    # 1. Store the last index of each character
    last = {char: i for i, char in enumerate(s)}

    result = []
    # start and end of the current partition
    start = 0
    end = 0

    for i, char in enumerate(s):
        # The current partition must extend to at least the last
        # occurrence of the current character.
        end = max(end, last[char])

        # If the current index has reached the furthest last occurrence
        # required for the current partition, we can close it.
        if i == end:
            # Add length of the partition
            result.append(end - start + 1)
            # Update start for the next partition
            start = i + 1

    return result
```

**Explanation**:

1.  **Requirement**: If we include a character 'a' in a partition, _all_ 'a's must be in that partition. This means the partition must span at least from the first 'a' to the last 'a'.
2.  **The "Horizon"**: We iterate through the string. At each step, we look at the last occurrence of the current character. Our partition _must_ end at or after this last occurrence. We maintain this "horizon" as `end`.
3.  **Closing the Partition**: If we reach our current `end`, it means we have seen all occurrences of every character we've encountered so far in this segment. This is the earliest point we can safely close the partition.
4.  **Greedy Count**: Since we close the partition as early as possible, we naturally maximize the number of partitions.

**Complexity Analysis**:

- **Time Complexity**: `O(N)`, where `N` is the length of the string. We do one pass to build the `last` map and one pass to find the partitions.
- **Space Complexity**: `O(1)` additional space, as the hash map `last` stores at most 26 entries (for the English alphabet).

---

## 2. Optimal Partition of String

**Problem Statement**:
Given a string `s`, partition the string into one or more substrings such that the characters in each substring are unique. That is, no letter appears in a single substring more than once. Return the minimum number of substrings in such a partition.

**Examples & Edge Cases**:

- **Example 1**:
  - Input: `s = "abacaba"`
  - Output: `4` ( "ab", "ac", "ab", "a" )
- **Edge Cases**:
  - String with all unique characters: 1.
  - String with all same characters: `len(s)`.

**Optimal Python Solution**:

```python
def partitionString(s: str) -> int:
    """
    Greedy: Start a new partition as soon as you see a character
    that is already in your current set.
    """
    # Count of partitions (start with 1 if s is not empty)
    partitions = 1
    # Seen characters in the current partition
    seen = set()

    for char in s:
        if char in seen:
            # We must start a new partition
            partitions += 1
            seen = {char}
        else:
            seen.add(char)

    return partitions
```

**Explanation**:

1.  **Greedy Strategy**: We want to make each partition as "long" as possible to minimize the total count.
2.  **Implementation**: We keep adding characters to the current partition until we hit a duplicate. At that point, we reset the `seen` set and increment our partition count.
3.  **Correctness**: Every time we encounter a character already in our `seen` set, we _must_ have started a new partition either at or before that index. Starting exactly there maximizes the remaining string's potential for longer partitions.

**Complexity Analysis**:

- **Time Complexity**: `O(N)`.
- **Space Complexity**: `O(1)` (set size is capped at 26).

---

## 3. Merge Intervals (Character-based view)

**Problem Statement**:
How does Partition Labels relate to Merge Intervals?

**Explanation**:
Partition Labels is essentially **Merge Intervals** where each unique character `c` in the string defines an interval `[first_index(c), last_index(c)]`.

1.  If you have the string `"ababcbaca"`, the intervals are:
    - 'a': [0, 8]
    - 'b': [1, 5]
    - 'c': [4, 7]
2.  If you merge these intervals, they all overlap into a single interval `[0, 8]`.
3.  Each resulting merged interval represents one partition.
4.  The greedy "last occurrence" algorithm is a more space-efficient way to find these merged intervals in a single pass without explicitly creating and sorting them.

**Comparison**:

- **Partition Labels**: One pass, `O(1)` extra space, works on the fly.
- **Merge Intervals Approach**: Extract intervals, sort them, merge them. `O(N + K log K)` where `K` is the number of unique characters.

---

## 4. Maximum Number of Non-overlapping Substrings

**Problem Statement**:
Given a string `s`, find the maximum number of non-overlapping substrings such that if a character is included in a substring, all occurrences of that character in `s` must also be included in that substring.

**Optimal Python Solution (Greedy with Intervals)**:

```python
def maxNumOfSubstrings(s: str) -> list[str]:
    """
    Greedy Interval Selection: Find valid intervals for each character
    and select the maximum number of non-overlapping ones.
    """
    first = {c: i for i, c in enumerate(s[::-1])}
    first = {c: len(s) - 1 - i for c, i in first.items()}
    last = {c: i for i, c in enumerate(s)}

    # 1. For each character, find the smallest valid interval
    intervals = []
    for char in set(s):
        start, end = first[char], last[char]
        curr = start
        is_valid = True
        while curr <= end:
            if first[s[curr]] < start:
                is_valid = False
                break
            end = max(end, last[s[curr]])
            curr += 1
        if is_valid:
            intervals.append([start, end])

    # 2. Greedy selection of non-overlapping intervals (Activity Selection)
    intervals.sort(key=lambda x: x[1])
    res = []
    prev_end = -1
    for start, end in intervals:
        if start > prev_end:
            res.append(s[start:end+1])
            prev_end = end

    return res
```

**Explanation**:

1.  **Validity**: Like Partition Labels, if we take a character, we must take ALL its occurrences. This defines an interval.
2.  **Refinement**: Unlike Partition Labels, these intervals can overlap in complex ways. We first find the minimum valid interval for each character.
3.  **Greedy Choice**: This is now the Activity Selection problem. We sort valid intervals by their end times and pick as many as possible.

**Complexity Analysis**:

- **Time Complexity**: `O(N * 26)`, where `N` is the string length. We might scan the string for each unique character.
- **Space Complexity**: `O(1)` additional space (capped by 26 intervals).

---

## 5. Video Stitching

**Problem Statement**:
Given video clips `[start, end]`, find the minimum number of clips to cover the interval `[0, T]`.

**Optimal Python Solution**:

```python
def videoStitching(clips: list[list[int]], T: int) -> int:
    """
    Greedy: At each step, pick the clip that extends the current reach the farthest.
    """
    max_jump = [0] * (T + 1)
    for s, e in clips:
        if s < T:
            max_jump[s] = max(max_jump[s], e)

    res = 0
    cur_end = 0
    farthest = 0
    for i in range(T):
        farthest = max(farthest, max_jump[i])
        if i == cur_end:
            if farthest <= i: return -1
            cur_end = farthest
            res += 1

    return res
```

**Explanation**:

1.  **Preprocessing**: For each starting point, we only care about the farthest reaching clip.
2.  **Greedy Step**: We iterate through the time range. When we reach the end of the current clip's reach (`cur_end`), we must pick a new clip. We pick the one that extended our `farthest` reach.
3.  **Failure**: If at any point we haven't reached the current time `i`, we can't finish the stitching.

**Complexity Analysis**:

- **Time Complexity**: `O(N + T)`.
- **Space Complexity**: `O(T)`.

# Sliding Window: Fixed Size - Solutions

## Practice Problems

### 1. Maximum Sum Subarray of Size K

**Problem Statement**: Given an array of positive numbers and a positive number `k`, find the maximum sum of any contiguous subarray of size `k`.

**Examples & Edge Cases**:

- Example: `[2, 1, 5, 1, 3, 2], k=3` -> `9` (subarray `[5, 1, 3]`)
- Edge Case: `k` is larger than array length.
- Edge Case: Array with all identical elements.

**Optimal Python Solution**:

```python
def max_sum_subarray(arr, k):
    if not arr or k <= 0 or k > len(arr):
        return 0

    # Calculate sum of first window
    window_sum = sum(arr[:k])
    max_sum = window_sum

    # Slide the window
    for i in range(k, len(arr)):
        # Add the next element and remove the first element of the previous window
        window_sum += arr[i] - arr[i-k]
        max_sum = max(max_sum, window_sum)

    return max_sum
```

**Explanation**:
Instead of recalculating the sum for every subarray of size `k`, we initialize the sum for the first `k` elements. Then, we slide the window by one position at a time, adding the incoming element and subtracting the outgoing element. This reduces the time complexity from O(n\*k) to O(n).

**Complexity Analysis**:

- **Time Complexity**: O(n), where n is the number of elements in the array. We iterate through the array once.
- **Space Complexity**: O(1), as we only store the `window_sum` and `max_sum`.

---

### 2. Maximum Average Subarray I

**Problem Statement**: You are given an integer array `nums` consisting of `n` elements, and an integer `k`. Find a contiguous subarray whose length is equal to `k` that has the maximum average value and return this value.

**Optimal Python Solution**:

```python
def findMaxAverage(nums: list[int], k: int) -> float:
    # Initialize with the sum of the first k elements
    curr_sum = sum(nums[:k])
    max_sum = curr_sum

    for i in range(k, len(nums)):
        curr_sum += nums[i] - nums[i-k]
        if curr_sum > max_sum:
            max_sum = curr_sum

    return max_sum / k
```

**Explanation**:
Since the length `k` is constant, maximizing the average is equivalent to maximizing the sum. We use a fixed sliding window to find the maximum sum and then divide by `k`.

**Complexity Analysis**:

- **Time Complexity**: O(n).
- **Space Complexity**: O(1).

---

### 3. Find All Anagrams in a String

**Problem Statement**: Given two strings `s` and `p`, return an array of all the start indices of `p`'s anagrams in `s`.

**Optimal Python Solution**:

```python
from collections import Counter

def findAnagrams(s: str, p: str) -> list[int]:
    ns, np = len(s), len(p)
    if ns < np:
        return []

    p_count = Counter(p)
    s_count = Counter(s[:np])

    res = []
    if s_count == p_count:
        res.append(0)

    for i in range(np, ns):
        # Add next char
        s_count[s[i]] += 1
        # Remove previous char
        s_count[s[i - np]] -= 1

        if s_count[s[i - np]] == 0:
            del s_count[s[i - np]]

        if s_count == p_count:
            res.append(i - np + 1)

    return res
```

**Explanation**:
An anagram has the same character frequencies. We maintain a frequency map (Counter) of a sliding window of size `len(p)` in string `s`. At each step, we update the map by adding the new character and removing the one that left the window, then compare it with the frequency map of `p`.

**Complexity Analysis**:

- **Time Complexity**: O(n), where n is length of `s`. Map comparison is O(26) = O(1).
- **Space Complexity**: O(1) as the map size is limited by the alphabet size (26).

---

### 4. Permutation in String

**Problem Statement**: Given two strings `s1` and `s2`, return `true` if `s2` contains a permutation of `s1`, or `false` otherwise.

**Optimal Python Solution**:

```python
def checkInclusion(s1: str, s2: str) -> bool:
    n1, n2 = len(s1), len(s2)
    if n1 > n2:
        return False

    cnt1 = [0] * 26
    cnt2 = [0] * 26
    for i in range(n1):
        cnt1[ord(s1[i]) - ord('a')] += 1
        cnt2[ord(s2[i]) - ord('a')] += 1

    if cnt1 == cnt2:
        return True

    for i in range(n1, n2):
        cnt2[ord(s2[i]) - ord('a')] += 1
        cnt2[ord(s2[i-n1]) - ord('a')] -= 1
        if cnt1 == cnt2:
            return True

    return False
```

**Explanation**:
Identical to "Find All Anagrams", but we return `True` as soon as we find one match. We use an array of size 26 for faster comparisons.

**Complexity Analysis**:

- **Time Complexity**: O(n).
- **Space Complexity**: O(1).

---

### 5. Sliding Window Maximum

**Problem Statement**: You are given an array of integers `nums`, there is a sliding window of size `k` which is moving from the very left of the array to the very right. You can only see the `k` numbers in the window. Each time the sliding window moves right by one position. Return the max sliding window.

**Optimal Python Solution**:

```python
from collections import deque

def maxSlidingWindow(nums: list[int], k: int) -> list[int]:
    dq = deque() # store indices
    res = []

    for i in range(len(nums)):
        # Remove indices that are out of the window
        if dq and dq[0] < i - k + 1:
            dq.popleft()

        # Remove elements smaller than the current element from the back
        # Because they will never be the maximum in any future window
        while dq and nums[dq[-1]] < nums[i]:
            dq.pop()

        dq.append(i)

        # Add to result if the first window is complete
        if i >= k - 1:
            res.append(nums[dq[0]])

    return res
```

**Explanation**:
We use a **monotonic deque** to store indices of elements in the current window. We maintain the deque such that the elements are in decreasing order. When a new element arrives, we remove all elements smaller than it from the back. The front of the deque always contains the index of the maximum element for the current window.

**Complexity Analysis**:

- **Time Complexity**: O(n). Each element is added and removed from the deque at most once.
- **Space Complexity**: O(k) for the deque.

---

### 6. Contains Duplicate II

**Problem Statement**: Given an integer array `nums` and an integer `k`, return `true` if there are two distinct indices `i` and `j` in the array such that `nums[i] == nums[j]` and `abs(i - j) <= k`.

**Optimal Python Solution**:

```python
def containsNearbyDuplicate(nums: list[int], k: int) -> bool:
    window = set()
    for i in range(len(nums)):
        if nums[i] in window:
            return True
        window.add(nums[i])
        # Maintain window size k
        if len(window) > k:
            window.remove(nums[i - k])
    return False
```

**Explanation**:
We maintain a hash set representing the elements in a sliding window of size `k`. If we encounter a number already in the set, we've found a duplicate within distance `k`.

**Complexity Analysis**:

- **Time Complexity**: O(n).
- **Space Complexity**: O(min(n, k)).

---

### 7. Repeated DNA Sequences

**Problem Statement**: The DNA sequence is composed of a series of nucleotides abbreviated as 'A', 'C', 'G', and 'T'. Given a string `s` that represents a DNA sequence, return all the 10-letter-long sequences (substrings) that occur more than once in a DNA molecule.

**Optimal Python Solution**:

```python
def findRepeatedDnaSequences(s: str) -> list[str]:
    seen = set()
    res = set()

    # Fixed window size of 10
    for i in range(len(s) - 9):
        window = s[i:i+10]
        if window in seen:
            res.add(window)
        else:
            seen.add(window)

    return list(res)
```

**Explanation**:
We slide a window of fixed size 10 across the string. We use a set to keep track of sequences we've seen and another set to store sequences that appear more than once (to avoid duplicates in the result).

**Complexity Analysis**:

- **Time Complexity**: O(n \* L), where L is the window length (10). String slicing and hashing take O(L).
- **Space Complexity**: O(n \* L) to store the sequences in the sets.

# Set Operations - Solutions

## 1. Intersection of Two Arrays
Given two integer arrays `nums1` and `nums2`, return an array of their intersection. Each element in the result must be unique and you may return the result in any order.

### Problem Statement
Find common unique elements between two arrays.

### Examples & Edge Cases
**Example:**
- Input: `nums1 = [1, 2, 2, 1], nums2 = [2, 2]`
- Output: `[2]`

**Edge Cases:**
- No common elements.
- Arrays are identical.
- One array is empty.

### Optimal Python Solution
```python
def intersection(nums1: list[int], nums2: list[int]) -> list[int]:
    """
    Convert both arrays to sets and use the intersection operator.
    """
    set1 = set(nums1)
    set2 = set(nums2)
    return list(set1 & set2)
```

### Explanation
By converting the arrays to sets, we automatically remove duplicates within each array. The `&` operator then finds the elements that exist in both sets.

### Complexity Analysis
- **Time Complexity**: O(n + m), where n and m are lengths of the arrays.
- **Space Complexity**: O(n + m).

---

## 2. Intersection of Two Arrays II
Find common elements, but include duplicates based on their frequency in both arrays.

### Optimal Python Solution
```python
from collections import Counter

def intersect(nums1: list[int], nums2: list[int]) -> list[int]:
    """
    Use a Counter for the first array and decrement for the second.
    """
    counts = Counter(nums1)
    result = []
    for num in nums2:
        if counts[num] > 0:
            result.append(num)
            counts[num] -= 1
    return result
```

### Complexity Analysis
- **Time Complexity**: O(n + m).
- **Space Complexity**: O(min(n, m)) to store counts of the smaller array.

---

## 3. Contains Duplicate
(Discussed in earlier files). Use `len(set(nums)) != len(nums)`.

---

## 4. Single Number
(Discussed in Frequency file). Use `res ^= num`.

---

## 5. Happy Number
Write an algorithm to determine if a number `n` is happy. A happy number is a number defined by the following process: Starting with any positive integer, replace the number by the sum of the squares of its digits. Repeat the process until the number equals 1 (where it will stay), or it loops endlessly in a cycle which does not include 1.

### Optimal Python Solution
```python
def isHappy(n: int) -> bool:
    """
    Use a set to detect if we've entered a cycle.
    """
    def get_next(number):
        total_sum = 0
        while number > 0:
            number, digit = divmod(number, 10)
            total_sum += digit ** 2
        return total_sum

    seen = set()
    while n != 1 and n not in seen:
        seen.add(n)
        n = get_next(n)

    return n == 1
```

### Complexity Analysis
- **Time Complexity**: O(log n).
- **Space Complexity**: O(log n).

---

## 6. Longest Consecutive Sequence
Given an unsorted array of integers `nums`, return the length of the longest consecutive elements sequence.

### Optimal Python Solution
```python
def longestConsecutive(nums: list[int]) -> int:
    """
    1. Store all numbers in a set for O(1) lookup.
    2. Only start counting a sequence if the number is a 'start' (num-1 not in set).
    """
    num_set = set(nums)
    longest = 0

    for num in num_set:
        # Check if this is the start of a sequence
        if (num - 1) not in num_set:
            length = 1
            while (num + length) in num_set:
                length += 1
            longest = max(longest, length)

    return longest
```

### Explanation
We only check for a sequence starting from the smallest element of that sequence. This ensures we don't redundantly count the same sequence for every element in it.

### Complexity Analysis
- **Time Complexity**: O(n). Each number is visited at most twice.
- **Space Complexity**: O(n).

---

## 7. Missing Number
Given an array `nums` containing `n` distinct numbers in the range `[0, n]`, return the only number in the range that is missing from the array.

### Optimal Python Solution
```python
def missingNumber(nums: list[int]) -> int:
    """
    Gauss' Sum Formula: Sum(0...n) = n * (n + 1) / 2
    """
    n = len(nums)
    expected_sum = n * (n + 1) // 2
    actual_sum = sum(nums)
    return expected_sum - actual_sum
```

---

## 8. Find All Numbers Disappeared in an Array
(Discussed in Frequency file - Index Marking).

---

## 9. Isomorphic Strings
Given two strings `s` and `t`, determine if they are isomorphic. Two strings are isomorphic if the characters in `s` can be replaced to get `t`.

### Optimal Python Solution
```python
def isIsomorphic(s: str, t: str) -> bool:
    """
    Create a mapping for BOTH directions to ensure a 1-to-1 relationship.
    """
    s_to_t = {}
    t_to_s = {}

    for c1, c2 in zip(s, t):
        if (c1 in s_to_t and s_to_t[c1] != c2) or \
           (c2 in t_to_s and t_to_s[c2] != c1):
            return False
        s_to_t[c1] = c2
        t_to_s[c2] = c1

    return True
```

---

## 10. Word Pattern
Given a `pattern` and a string `s`, find if `s` follows the same pattern.

### Optimal Python Solution
Similar to Isomorphic Strings. Split `s` into words and perform bidirectional mapping between `pattern` characters and `words`.
O(n) Time, O(n) Space.

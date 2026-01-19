# Binary Search Template

> **Prerequisites:** Basic array knowledge, understanding of O(log n) complexity

## Interview Context

Binary search template questions test:
1. **Implementation accuracy**: Can you write bug-free binary search?
2. **Edge case handling**: Empty arrays, single elements, not found
3. **Variant recognition**: Which template applies to which problem?
4. **Overflow prevention**: Proper midpoint calculation

---

## Why Binary Search Works

Binary search requires a **monotonic property**:

```
Search space: [False, False, False, True, True, True]
                                   ↑
              Binary search finds this transition point
```

At each step, we can eliminate half the search space because:
- If condition is true at `mid`, answer is at or before `mid`
- If condition is false at `mid`, answer is after `mid`

---

## The Three Templates

### Template 1: Find Exact Match

Used when searching for a specific target value.

```python
def binary_search(nums: list[int], target: int) -> int:
    """
    Find target in sorted array.

    Time: O(log n)
    Space: O(1)
    """
    left, right = 0, len(nums) - 1

    while left <= right:
        mid = left + (right - left) // 2

        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return -1
```

**Key points:**
- Use `<=` in condition (search until left crosses right)
- Return `mid` immediately when found
- Move `left = mid + 1` or `right = mid - 1` (never include mid)

---

### Template 2: Find Left Boundary (First Occurrence)

Used when finding the first position where condition becomes true.

```python
def find_left_boundary(nums: list[int], target: int) -> int:
    """
    Find first occurrence of target (or insertion point).

    Time: O(log n)
    Space: O(1)
    """
    left, right = 0, len(nums) - 1
    result = -1

    while left <= right:
        mid = left + (right - left) // 2

        if nums[mid] >= target:
            if nums[mid] == target:
                result = mid
            right = mid - 1
        else:
            left = mid + 1

    return result
```

Alternative (returns insertion point):

```python
def find_left_boundary_v2(nums: list[int], target: int) -> int:
    """
    Find leftmost position where target could be inserted.

    Returns index of first element >= target.
    """
    left, right = 0, len(nums)  # Note: right = len(nums)

    while left < right:  # Note: < not <=
        mid = left + (right - left) // 2

        if nums[mid] < target:
            left = mid + 1
        else:
            right = mid

    return left
```

---

### Template 3: Find Right Boundary (Last Occurrence)

Used when finding the last position where condition is true.

```python
def find_right_boundary(nums: list[int], target: int) -> int:
    """
    Find last occurrence of target.

    Time: O(log n)
    Space: O(1)
    """
    left, right = 0, len(nums) - 1
    result = -1

    while left <= right:
        mid = left + (right - left) // 2

        if nums[mid] <= target:
            if nums[mid] == target:
                result = mid
            left = mid + 1
        else:
            right = mid - 1

    return result
```

---

## Template Comparison

| Template | Loop Condition | Mid Calculation | When Mid Found |
|----------|---------------|-----------------|----------------|
| Exact Match | `left <= right` | `left + (right-left)//2` | Return immediately |
| Left Boundary | `left <= right` or `left < right` | Same | Continue searching left |
| Right Boundary | `left <= right` | Same | Continue searching right |

---

## Visual Walkthrough

### Finding target = 5 in [1, 2, 3, 5, 5, 5, 8, 9]

**Exact match (finds any 5):**
```
[1, 2, 3, 5, 5, 5, 8, 9]
 L           M        R     mid=3, nums[3]=5, return 3
```

**Left boundary (finds first 5):**
```
[1, 2, 3, 5, 5, 5, 8, 9]
 L           M        R     mid=3, nums[3]=5 >= 5, result=3, R=2
 L     M  R                 mid=1, nums[1]=2 < 5, L=2
       LM R                 mid=2, nums[2]=3 < 5, L=3
       R  L                 L > R, return result=3
```

**Right boundary (finds last 5):**
```
[1, 2, 3, 5, 5, 5, 8, 9]
 L           M        R     mid=3, nums[3]=5 <= 5, result=3, L=4
             L     M  R     mid=5, nums[5]=5 <= 5, result=5, L=6
                   L  MR    mid=6, nums[6]=8 > 5, R=5
                   RL       L > R, return result=5
```

---

## Python's bisect Module

Python provides built-in binary search:

```python
import bisect

nums = [1, 2, 3, 5, 5, 5, 8, 9]

# Find leftmost insertion point
bisect.bisect_left(nums, 5)   # Returns 3

# Find rightmost insertion point
bisect.bisect_right(nums, 5)  # Returns 6

# Insert while maintaining order
bisect.insort_left(nums, 4)   # Inserts 4 at index 3
```

**Using bisect for boundary finding:**

```python
import bisect

def first_occurrence(nums: list[int], target: int) -> int:
    idx = bisect.bisect_left(nums, target)
    if idx < len(nums) and nums[idx] == target:
        return idx
    return -1

def last_occurrence(nums: list[int], target: int) -> int:
    idx = bisect.bisect_right(nums, target) - 1
    if idx >= 0 and nums[idx] == target:
        return idx
    return -1
```

---

## Avoiding Common Bugs

### 1. Integer Overflow (Not in Python, but important for other languages)

```python
# Wrong (can overflow in C++/Java)
mid = (left + right) // 2

# Correct
mid = left + (right - left) // 2
```

### 2. Infinite Loops

```python
# Wrong - infinite loop when left == right
while left < right:
    mid = left + (right - left) // 2
    if nums[mid] < target:
        left = mid  # Should be mid + 1

# Correct
while left < right:
    mid = left + (right - left) // 2
    if nums[mid] < target:
        left = mid + 1
```

### 3. Off-by-One Errors

```python
# Know your bounds
# Template 1: right = len(nums) - 1
# Template 2: right = len(nums) when returning insertion point
```

### 4. Empty Array

```python
def binary_search_safe(nums: list[int], target: int) -> int:
    if not nums:
        return -1
    # ... rest of search
```

---

## Complexity Analysis

| Operation | Time | Space | Notes |
|-----------|------|-------|-------|
| Binary Search | O(log n) | O(1) | Halves search space each step |
| Recursive Binary Search | O(log n) | O(log n) | Call stack depth |
| Finding All Occurrences | O(log n + k) | O(1) | k = number of occurrences |

---

## Common Variations

### 1. Square Root

```python
def sqrt(x: int) -> int:
    """Find floor of square root."""
    if x < 2:
        return x

    left, right = 1, x // 2

    while left <= right:
        mid = left + (right - left) // 2
        if mid * mid == x:
            return mid
        elif mid * mid < x:
            left = mid + 1
        else:
            right = mid - 1

    return right
```

### 2. First Bad Version

```python
def first_bad_version(n: int) -> int:
    """Find first bad version (API: is_bad(version) -> bool)."""
    left, right = 1, n

    while left < right:
        mid = left + (right - left) // 2
        if is_bad(mid):
            right = mid
        else:
            left = mid + 1

    return left
```

### 3. Guess Number

```python
def guess_number(n: int) -> int:
    """Guess number (API: guess(num) -> -1/0/1)."""
    left, right = 1, n

    while left <= right:
        mid = left + (right - left) // 2
        result = guess(mid)
        if result == 0:
            return mid
        elif result == -1:
            right = mid - 1
        else:
            left = mid + 1

    return -1
```

---

## Edge Cases Checklist

- [ ] Empty array
- [ ] Single element array
- [ ] Target smaller than all elements
- [ ] Target larger than all elements
- [ ] Target not in array
- [ ] Duplicate elements
- [ ] All elements are the same

---

## Practice Problems

| # | Problem | Difficulty | Key Insight |
|---|---------|------------|-------------|
| 1 | Binary Search | Easy | Standard template |
| 2 | Sqrt(x) | Easy | Search on answer |
| 3 | First Bad Version | Easy | Left boundary |
| 4 | Guess Number Higher or Lower | Easy | Standard template |
| 5 | Search Insert Position | Easy | Left boundary/insertion point |
| 6 | Valid Perfect Square | Easy | Search on answer |
| 7 | Count Negative Numbers in Sorted Matrix | Easy | Binary search per row |

---

## Interview Tips

1. **Clarify the problem**: Sorted? Duplicates? What to return if not found?
2. **Choose the right template**: Match the problem to a template
3. **Check bounds carefully**: `<=` vs `<`, `mid+1` vs `mid`
4. **Test with examples**: Walk through with [1], [1,2], and [1,2,3]
5. **Consider edge cases**: Empty, single element, boundaries

---

## Key Takeaways

1. Three templates: exact match, left boundary, right boundary
2. Always use `left + (right - left) // 2` for midpoint
3. Know when to return immediately vs continue searching
4. Python's `bisect` module handles most cases
5. Test with small arrays to verify correctness

---

## Next: [02-first-last-occurrence.md](./02-first-last-occurrence.md)

Deep dive into finding boundaries in sorted arrays.

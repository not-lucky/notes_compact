# Two Pointers: Opposite Direction

> **Prerequisites:** [01-array-basics.md](./01-array-basics.md)

## Overview

Opposite-direction two pointers (converging pointers) start at opposite ends of an array and move toward each other based on comparisons. This pattern exploits sorted order or symmetry to achieve O(n) solutions where brute force would be O(n²).

## Building Intuition

**Why does converging from both ends work?**

The key insight is **elimination by comparison**. At each step, we can definitively rule out a large portion of the search space:

1. **The Sorted Array Insight**: In a sorted array, moving the left pointer increases the sum, moving the right decreases it. We have a "steering wheel" to navigate toward our target. This is why Two Sum on sorted arrays is O(n) instead of O(n²).

2. **The Bottleneck Principle**: In container problems, the shorter wall limits the water level. Moving the taller wall can only decrease area (width shrinks, height can't improve). Moving the shorter wall might find a taller one. At each step, we try the only option that could possibly improve.

3. **Symmetry Exploitation**: Palindrome checking works because we only need to verify character pairs from both ends. If outer characters match, the inner substring determines palindrome-ness.

**Mental Model**: Think of two people searching a sorted bookshelf—one from each end. They're looking for a specific total page count by combining two books. If their current sum is too small, the left person moves right (bigger books). If too large, the right person moves left (smaller books). They never miss the answer because they're "squeezing" the search space systematically.

**Why We Don't Miss Solutions**:
```
Looking for sum = 10 in sorted [1, 2, 4, 6, 8]
                                 L           R

If 1 + 8 = 9 < 10:
  - All pairs (1, x) where x ≤ 8 will sum ≤ 9
  - We can safely eliminate all of them by moving L right
  - We don't lose any valid pairs!
```

## When NOT to Use Opposite-Direction Two Pointers

This pattern requires specific conditions:

1. **Unsorted Array (for pair problems)**: Two Sum with unsorted data needs a hash map (O(n) with O(n) space), not two pointers. Sorting first costs O(n log n).

2. **Need All Pairs, Not Just One**: If you need all pairs summing to target, two pointers work, but tracking duplicates gets tricky. Hash map may be cleaner.

3. **More Than Two Elements**: For 3Sum or 4Sum, you still use two pointers, but with outer loops fixing elements. Pure two-pointer only handles pairs.

4. **No Natural Ordering**: If there's no sorted order or symmetric structure to exploit, converging pointers have no basis for deciding which to move.

5. **Minimum Instead of Feasibility**: Two pointers find "first valid" or "any valid" easily. Finding "minimum that satisfies X" may need binary search instead.

**Red Flags:**
- "Array is not sorted" (for sum problems) → Use hash map
- "Return indices from original unsorted array" → Sorting loses indices; use hash map
- "Minimize/maximize some function" → May need binary search on answer

---

## Interview Context

Opposite-direction two pointers (converging pointers) are essential for:

- Finding pairs in sorted arrays
- Optimizing area/volume problems
- Palindrome checking
- Container problems (trapping water)

This is one of the most common patterns—expect to use it in every interview loop.

---

## Core Concept

Start pointers at opposite ends and move them toward each other based on comparisons:

```
Initial state:
┌───┬───┬───┬───┬───┬───┬───┐
│ 1 │ 2 │ 3 │ 5 │ 7 │ 8 │ 9 │
└───┴───┴───┴───┴───┴───┴───┘
  ↑                       ↑
left                   right

Move based on condition until left >= right
```

---

## Template: Two Sum (Sorted Array)

```python
def two_sum_sorted(arr: list[int], target: int) -> list[int]:
    """
    Find indices of two numbers that sum to target.
    Array is sorted.

    Time: O(n)
    Space: O(1)

    Example:
    arr = [2, 7, 11, 15], target = 9
    → [0, 1] (2 + 7 = 9)
    """
    left, right = 0, len(arr) - 1

    while left < right:
        current_sum = arr[left] + arr[right]

        if current_sum == target:
            return [left, right]
        elif current_sum < target:
            left += 1   # Need larger sum
        else:
            right -= 1  # Need smaller sum

    return []  # No solution found
```

### Why This Works

```
sorted: [2, 7, 11, 15], target = 9

left=0, right=3: 2 + 15 = 17 > 9 → right--
left=0, right=2: 2 + 11 = 13 > 9 → right--
left=0, right=1: 2 + 7  = 9  = 9 → found!

Key insight: in sorted array, moving right decreases sum,
moving left increases sum. So we can always move toward target.
```

---

## Template: 3Sum

```python
def three_sum(nums: list[int]) -> list[list[int]]:
    """
    Find all unique triplets that sum to zero.

    Time: O(n²) - O(n log n) sort + O(n) × O(n) two-sum
    Space: O(1) excluding output (O(n) for sort in some languages)

    Example:
    [-1, 0, 1, 2, -1, -4] → [[-1, -1, 2], [-1, 0, 1]]
    """
    nums.sort()
    result = []
    n = len(nums)

    for i in range(n - 2):
        # Skip duplicate first elements
        if i > 0 and nums[i] == nums[i - 1]:
            continue

        # Early termination: if smallest is positive, no solution
        if nums[i] > 0:
            break

        left, right = i + 1, n - 1
        target = -nums[i]

        while left < right:
            current_sum = nums[left] + nums[right]

            if current_sum == target:
                result.append([nums[i], nums[left], nums[right]])

                # Skip duplicates
                while left < right and nums[left] == nums[left + 1]:
                    left += 1
                while left < right and nums[right] == nums[right - 1]:
                    right -= 1

                left += 1
                right -= 1
            elif current_sum < target:
                left += 1
            else:
                right -= 1

    return result
```

---

## Template: Container With Most Water

```python
def max_area(heights: list[int]) -> int:
    """
    Find two lines that form container holding most water.

    Time: O(n)
    Space: O(1)

    Visual:
    |       |
    |   |   |
    | | | | |
    1 8 6 2 5 4 8 3 7
        ↑           ↑
      left       right
    """
    left, right = 0, len(heights) - 1
    max_water = 0

    while left < right:
        width = right - left
        height = min(heights[left], heights[right])
        max_water = max(max_water, width * height)

        # Move the shorter line (it's the bottleneck)
        if heights[left] < heights[right]:
            left += 1
        else:
            right -= 1

    return max_water
```

### Why Move the Shorter Line?

```
Current area = min(left_height, right_height) × width

If we move the taller line:
- width decreases by 1
- height can only stay same or decrease (limited by shorter)
- area guaranteed to decrease or stay same

If we move the shorter line:
- width decreases by 1
- height might increase (new line could be taller)
- area might increase

So moving shorter line is the only way to potentially improve.
```

---

## Template: Valid Palindrome

```python
def is_palindrome(s: str) -> bool:
    """
    Check if string is palindrome (ignore non-alphanumeric).

    Time: O(n)
    Space: O(1)
    """
    left, right = 0, len(s) - 1

    while left < right:
        # Skip non-alphanumeric
        while left < right and not s[left].isalnum():
            left += 1
        while left < right and not s[right].isalnum():
            right -= 1

        if s[left].lower() != s[right].lower():
            return False

        left += 1
        right -= 1

    return True
```

---

## Template: Trapping Rain Water

```python
def trap_rain_water(heights: list[int]) -> int:
    """
    Calculate total water trapped between bars.

    Time: O(n)
    Space: O(1)

    Concept: At each position, water = min(left_max, right_max) - height

    Visual:
        |
    |   || |
    |_|_||_|_|
    0 1 0 2 1 0 1 3 2 1 2 1

    Water trapped: 6 units
    """
    if not heights:
        return 0

    left, right = 0, len(heights) - 1
    left_max, right_max = 0, 0
    water = 0

    while left < right:
        if heights[left] < heights[right]:
            if heights[left] >= left_max:
                left_max = heights[left]
            else:
                water += left_max - heights[left]
            left += 1
        else:
            if heights[right] >= right_max:
                right_max = heights[right]
            else:
                water += right_max - heights[right]
            right -= 1

    return water
```

### Why This Works

```
At position left:
- left_max = tallest bar to the left of left (including)
- We know right_max >= heights[right] > heights[left]
- So min(left_max, right_max) is determined by left_max
- Water at left = left_max - heights[left]

We can compute water at left without knowing exact right_max!
Same logic applies symmetrically for right.
```

---

## Template: Reverse Array In-Place

```python
def reverse(arr: list[int]) -> None:
    """
    Reverse array in-place.

    Time: O(n)
    Space: O(1)
    """
    left, right = 0, len(arr) - 1

    while left < right:
        arr[left], arr[right] = arr[right], arr[left]
        left += 1
        right -= 1
```

---

## Template: Sort Colors (Dutch National Flag)

```python
def sort_colors(nums: list[int]) -> None:
    """
    Sort array containing only 0, 1, 2 in-place.
    One pass, O(1) space.

    Uses THREE pointers:
    - low: boundary for 0s (next position to place 0)
    - mid: current element
    - high: boundary for 2s (next position to place 2)

    Invariant:
    [0...low-1] = all 0s
    [low...mid-1] = all 1s
    [high+1...n-1] = all 2s
    """
    low, mid, high = 0, 0, len(nums) - 1

    while mid <= high:
        if nums[mid] == 0:
            nums[low], nums[mid] = nums[mid], nums[low]
            low += 1
            mid += 1
        elif nums[mid] == 1:
            mid += 1
        else:  # nums[mid] == 2
            nums[mid], nums[high] = nums[high], nums[mid]
            high -= 1
            # Don't increment mid! Need to check swapped element
```

---

## Common Variations

### Two Sum Closest

```python
def two_sum_closest(arr: list[int], target: int) -> list[int]:
    """
    Find pair with sum closest to target.

    Time: O(n log n) for sort + O(n) for search
    Space: O(1)
    """
    arr.sort()
    left, right = 0, len(arr) - 1
    closest_diff = float('inf')
    result = []

    while left < right:
        current_sum = arr[left] + arr[right]
        diff = abs(current_sum - target)

        if diff < closest_diff:
            closest_diff = diff
            result = [arr[left], arr[right]]

        if current_sum < target:
            left += 1
        elif current_sum > target:
            right -= 1
        else:
            return result  # Exact match

    return result
```

### Count Pairs with Sum Less Than Target

```python
def count_pairs_less_than(arr: list[int], target: int) -> int:
    """
    Count pairs with sum < target.

    Time: O(n log n)
    Space: O(1)
    """
    arr.sort()
    left, right = 0, len(arr) - 1
    count = 0

    while left < right:
        if arr[left] + arr[right] < target:
            # All pairs (left, left+1), (left, left+2), ..., (left, right) work
            count += right - left
            left += 1
        else:
            right -= 1

    return count
```

---

## Edge Cases

```python
# Empty or single element
[] → no pairs possible
[5] → no pairs possible

# Two elements
[1, 2], target=3 → [0, 1]

# All same elements
[5, 5, 5, 5], target=10 → any pair works

# No valid pair
[1, 2, 3], target=10 → []

# Negative numbers (still works with sorting)
[-3, -1, 0, 2, 4], target=1 → [-1, 2] or [-3, 4]
```

---

## When to Use Each Direction

| Same Direction | Opposite Direction |
|----------------|-------------------|
| Remove duplicates | Find pairs in sorted |
| Partition array | Palindrome check |
| Sliding window | Container problems |
| Stream processing | Binary search variant |

---

## Practice Problems

| # | Problem | Difficulty | Pattern |
|---|---------|------------|---------|
| 1 | Two Sum II (Sorted) | Medium | Basic opposite |
| 2 | 3Sum | Medium | Fix one + two pointers |
| 3 | 3Sum Closest | Medium | Track closest |
| 4 | Container With Most Water | Medium | Max area |
| 5 | Trapping Rain Water | Hard | Left/right max |
| 6 | Valid Palindrome | Easy | Skip non-alphanum |
| 7 | Sort Colors | Medium | Dutch flag |
| 8 | 4Sum | Medium | Two layers + two pointers |

---

## Key Takeaways

1. **Sorted array** → two pointers often works
2. **Move based on comparison** with target
3. **Move the bottleneck** (shorter/smaller element)
4. **Skip duplicates** for unique solutions
5. **Three pointers** for three-way partition

---

## Next: [04-sliding-window-fixed.md](./04-sliding-window-fixed.md)

Learn the fixed-size sliding window for subarray problems.

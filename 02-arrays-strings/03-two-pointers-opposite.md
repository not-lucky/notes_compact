# Two Pointers: Opposite Direction

> **Prerequisites:** [01-array-basics.md](./01-array-basics.md)

## Overview

Opposite-direction two pointers (converging pointers) start at opposite ends of an array and move toward each other based on comparisons. This pattern exploits sorted order or symmetry to achieve $O(n)$ solutions where a brute force approach would require $O(n^2)$.

## Building Intuition

**Why does converging from both ends work?**

The key insight is **elimination by comparison**. At each step, we can definitively rule out a large portion of the search space:

1. **The Sorted Array Insight**: In a sorted array, moving the left pointer increases the sum, moving the right decreases it. We have a "steering wheel" to navigate toward our target. This is why Two Sum on sorted arrays is $\Theta(n)$ instead of $O(n^2)$.
2. **The Bottleneck Principle**: Think of pouring water into a container formed by two walls. The shorter wall determines how much water it can hold, no matter how tall the other wall is. Moving the taller wall inward only shrinks the width, decreasing the volume. Moving the shorter wall is the *only* hope of finding a taller boundary to increase the volume.
3. **Symmetry Exploitation**: Palindrome checking works because we only need to verify character pairs from both ends. If the outermost characters match, the inner substring alone determines if it's a palindrome.

**Mental Model**: Think of two friends, Alice and Bob, standing at opposite ends of a very long, sorted row of books. They need to find two books whose page counts add up exactly to 500 pages.
- Alice is at the start (shortest books).
- Bob is at the end (longest books).
- They shout their current total to each other.
- If the total is too small (e.g., 400 pages), Bob can't help by moving left (the books only get smaller). Only Alice can help by moving right to a thicker book.
- If the total is too large (e.g., 600 pages), Alice moving right makes it worse. Bob must move left to a thinner book.

They never miss the answer because they're systematically "squeezing" the search space, discarding books they *know* cannot possibly form the target sum with any remaining book. This guarantees they check the necessary pairs in exactly one pass, ensuring a tight bound of $\Theta(n)$ time complexity.

**Why We Don't Miss Solutions**:

```text
Looking for sum = 10 in sorted [1, 2, 4, 6, 8]
                                 L           R

If 1 + 8 = 9 < 10:
  - All pairs (1, x) where x <= 8 will sum <= 9.
  - We can safely eliminate all of them by moving L right.
  - We don't lose any valid pairs!
```

## When NOT to Use Opposite-Direction Two Pointers

This pattern requires specific conditions:

1. **Unsorted Array (for pair problems)**: Two Sum with unsorted data needs a hash map (amortized $\Theta(1)$, worst-case $O(n)$ insertions and lookups with $\Theta(n)$ space), not two pointers. Sorting first costs $\Theta(n \log n)$.
2. **Need All Pairs, Not Just One**: If you need all pairs summing to a target, two pointers can work, but tracking duplicates gets tricky. A hash map might be cleaner depending on the requirements.
3. **More Than Two Elements**: For 3Sum or 4Sum, you still use two pointers, but with outer loops fixing elements. Pure two-pointer only handles pairs.
4. **No Natural Ordering**: If there's no sorted order or symmetric structure to exploit, converging pointers have no basis for deciding which to move.
5. **Minimum Instead of Feasibility**: Two pointers find "first valid" or "any valid" easily. Finding "minimum that satisfies X" may need binary search instead.

**Red Flags:**

- "Array is not sorted" (for sum problems) → Use a hash map.
- "Return indices from original unsorted array" → Sorting loses indices; use a hash map.
- "Minimize/maximize some function" → May need binary search on the answer.
- "String concatenation" in Python → Using `+=` in loops is typically $\Theta(n^2)$ time architecture-wise due to memory reallocation. Consider `.join()` if manipulating arrays for string results.

---

## Interview Context

Opposite-direction two pointers (converging pointers) are essential for:

- Finding pairs in sorted arrays
- Optimizing area/volume problems
- Palindrome checking
- Container problems (trapping water)

This is one of the most common patterns—expect to use it in almost every interview loop.

---

## Core Concept

Start pointers at opposite ends and move them toward each other based on comparisons:

```text
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

### Problem: Two Sum II - Input Array Is Sorted
**Problem Statement:** Given a 1-indexed array of integers that is already sorted in non-decreasing order, find two numbers such that they add up to a specific target number.

**Why it works:**
In a sorted array, the sum of elements at `left` and `right` can be adjusted predictably.
1. If the current sum is too small, the only way to increase it (without using a hash map) is to move the `left` pointer to a larger value.
2. If the current sum is too large, the only way to decrease it is to move the `right` pointer to a smaller value.
Because the array is sorted, this "squeezing" approach covers all possible pairs in $\Theta(n)$ time without missing any.

```python
def two_sum_sorted(arr: list[int], target: int) -> list[int]:
    """
    Find indices of two numbers that sum to target.
    Array is sorted.

    Time Complexity: O(n) (tight bound: \Theta(n))
    Space Complexity: \Theta(1)

    Example:
    arr = [2, 7, 11, 15], target = 9
    -> [0, 1] (2 + 7 = 9)
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

```text
sorted: [2, 7, 11, 15], target = 9

left=0, right=3: 2 + 15 = 17 > 9 -> right--
left=0, right=2: 2 + 11 = 13 > 9 -> right--
left=0, right=1: 2 + 7  = 9  = 9 -> found!

Key insight: in sorted array, moving right decreases sum,
moving left increases sum. So we can always move toward target.
```

---

## Template: 3Sum

### Problem: 3Sum
**Problem Statement:** Given an integer array `nums`, return all unique triplets `[nums[i], nums[j], nums[k]]` such that `i != j`, `i != k`, and `j != k`, and `nums[i] + nums[j] + nums[k] == 0`.

**Why it works:**
This is an extension of Two Sum.
1. First, we sort the array to enable two-pointers and handle duplicates easily.
2. We fix one element `nums[i]` and then look for two other elements that sum to `-nums[i]` using the Two Sum (Sorted) technique.
3. We skip duplicate values for both the fixed element and the two pointers to ensure the result contains only unique triplets.
Sorting makes the $\Theta(n^2)$ approach much more efficient than a brute-force $\Theta(n^3)$. Note that Python lists are dynamic arrays, but sorting them in-place with `.sort()` (Timsort) is highly optimized.

```python
def three_sum(nums: list[int]) -> list[list[int]]:
    """
    Find all unique triplets that sum to zero.

    Time Complexity: O(n^2) - \Theta(n \log n) sort + O(n) x O(n) two-sum
    Space Complexity: O(n)
        Python's Timsort uses up to O(n) extra space in the worst case.

    Example:
    [-1, 0, 1, 2, -1, -4] -> [[-1, -1, 2], [-1, 0, 1]]
    """
    nums.sort()
    result = []
    n = len(nums)

    for i in range(n - 2):
        # Skip duplicate first elements
        if i > 0 and nums[i] == nums[i - 1]:
            continue

        # Early termination: if smallest is positive, no sum to 0 is possible
        if nums[i] > 0:
            break

        left, right = i + 1, n - 1
        target = -nums[i]

        while left < right:
            current_sum = nums[left] + nums[right]

            if current_sum == target:
                result.append([nums[i], nums[left], nums[right]])

                # Skip duplicates for both pointers
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

### Problem: Container With Most Water
**Problem Statement:** You are given an integer array `heights`. Find two lines that together with the x-axis form a container, such that the container contains the most water.

**Why it works:**
The amount of water is limited by the shorter line: `Area = min(h1, h2) * width`.
1. We start with the widest possible width (`left=0`, `right=n-1`).
2. To find a larger area, we must find taller lines, because moving pointers always decreases the width.
3. Moving the taller line is useless because the area will still be limited by the same (or even shorter) shorter line, but with a smaller width.
4. Therefore, we *must* move the pointer pointing to the shorter line in hopes of finding a taller one.

```python
def max_area(heights: list[int]) -> int:
    """
    Find two lines that form a container holding the most water.

    Time Complexity: O(n) (tight bound: \Theta(n))
    Space Complexity: \Theta(1)

    Visual:
    |       |
    |   |   |
    | | | | |
    1 8 6 2 5 4 8 3 7
        ^           ^
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

```text
Current area = min(left_height, right_height) * width

If we move the taller line:
- width decreases by 1.
- height can only stay the same or decrease (limited by the shorter line).
- area is GUARANTEED to decrease or stay the same.

If we move the shorter line:
- width decreases by 1.
- height might increase (the new line could be taller).
- area MIGHT increase.

So moving the shorter line is the ONLY way to potentially improve our result.
```

---

## Template: Valid Palindrome

### Problem: Valid Palindrome
**Problem Statement:** Given a string `s`, return `true` if it is a palindrome, or `false` otherwise, after converting all uppercase letters into lowercase letters and removing all non-alphanumeric characters.

**Why it works:**
A palindrome is perfectly symmetric. Think of folding a piece of paper in half.
1. We use `left` and `right` pointers from both ends.
2. We skip any "noise" (non-alphanumeric characters).
3. We compare the characters. If they don't match, it's not a palindrome.
By converging from both ends, we elegantly verify the symmetry in a single pass.

```python
def is_palindrome(s: str) -> bool:
    """
    Check if a string is a palindrome (ignoring non-alphanumeric chars).

    Time Complexity: O(n) (tight bound: \Theta(n))
    Space Complexity: \Theta(1)
    """
    left, right = 0, len(s) - 1

    while left < right:
        # Skip non-alphanumeric from the left
        while left < right and not s[left].isalnum():
            left += 1
        # Skip non-alphanumeric from the right
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

### Problem: Trapping Rain Water
**Problem Statement:** Given `n` non-negative integers representing an elevation map where the width of each bar is `1`, compute how much water it can trap after raining.

**Why it works:**
The water trapped at any index `i` is determined by the highest bars to its left and right: `min(max_left_so_far, max_right_so_far) - height[i]`.
1. We use two pointers from the ends.
2. We maintain `left_max` and `right_max`.
3. If `height[left] < height[right]`, we know the water at `left` is determined *entirely* by `left_max`. Why? Because `right_max` is guaranteed to be at least `height[right]`, which is already taller than `height[left]`.
4. This allows us to calculate water at the smaller height's pointer without needing to know the absolute maximum peak on the other side.

```python
def trap_rain_water(heights: list[int]) -> int:
    """
    Calculate the total water trapped between bars.

    Time Complexity: O(n) (tight bound: \Theta(n))
    Space Complexity: \Theta(1)

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

```text
At position left:
- left_max = tallest bar to the left of left (inclusive).
- We know right_max >= heights[right] > heights[left].
- So min(left_max, right_max) is wholly determined by left_max.
- Water at left = left_max - heights[left].

We can perfectly compute water at `left` without knowing the exact `right_max`!
The same logic applies symmetrically for the right side.
```

---

## Template: Reverse Array In-Place

```python
def reverse(arr: list[int]) -> None:
    """
    Reverse array in-place.

    Time Complexity: O(n) (tight bound: \Theta(n))
    Space Complexity: \Theta(1)
    """
    left, right = 0, len(arr) - 1

    while left < right:
        arr[left], arr[right] = arr[right], arr[left]
        left += 1
        right -= 1
```

---

## Template: Sort Colors (Dutch National Flag)

### Problem: Sort Colors
**Problem Statement:** Given an array `nums` with `n` objects colored red, white, or blue, sort them in-place so that objects of the same color are adjacent, with the colors in the order red, white, and blue (0, 1, 2).

**Why it works:**
This is a three-way partition problem, conceptualized by Edsger Dijkstra.
1. `low` marks the boundary for 0s (red), `high` for 2s (blue), and `mid` is the current element we are inspecting.
2. If `arr[mid] == 0`, we swap it into the `low` region and advance both `low` and `mid`.
3. If `arr[mid] == 2`, we swap it into the `high` region and decrement `high`. **Crucially, we do not advance `mid`**, because the element swapped from `high` into `mid` needs to be evaluated.
4. If `arr[mid] == 1`, it's exactly where it belongs (the middle region), so we just advance `mid`.

```python
def sort_colors(nums: list[int]) -> None:
    """
    Sort array containing only 0, 1, 2 in-place.
    One pass, \Theta(1) space.

    Uses THREE pointers:
    - low: boundary for 0s (next position to place a 0)
    - mid: current element
    - high: boundary for 2s (next position to place a 2)

    Invariant:
    [0 ... low-1]  = all 0s
    [low ... mid-1] = all 1s
    [high+1 ... n-1] = all 2s
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
            # Don't increment mid! We must evaluate the newly swapped element.
```

---

## Common Variations

### Two Sum Closest

```python
def two_sum_closest(arr: list[int], target: int) -> list[int]:
    """
    Find a pair with a sum closest to the target.

    Time Complexity: O(n \log n) for sort + \Theta(n) for search -> O(n \log n) total
    Space Complexity: O(n)
        Python's Timsort uses up to O(n) extra space.
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
            return result  # Exact match, can't get closer

    return result
```

### Count Pairs with Sum Less Than Target

```python
def count_pairs_less_than(arr: list[int], target: int) -> int:
    """
    Count pairs with sum < target.

    Time Complexity: O(n \log n)
    Space Complexity: O(n)
        Python's Timsort uses up to O(n) extra space.
    """
    arr.sort()
    left, right = 0, len(arr) - 1
    count = 0

    while left < right:
        if arr[left] + arr[right] < target:
            # If arr[left] + arr[right] < target, then replacing right
            # with any index between left+1 and right will also be < target
            # because the array is sorted.
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
[] -> no pairs possible
[5] -> no pairs possible

# Two elements
[1, 2], target=3 -> [0, 1]

# All same elements
[5, 5, 5, 5], target=10 -> any pair works

# No valid pair
[1, 2, 3], target=10 -> []

# Negative numbers (still works perfectly with sorting)
[-3, -1, 0, 2, 4], target=1 -> [-1, 2] or [-3, 4]
```

---

## When to Use Each Direction

| Same Direction (Sliding Window) | Opposite Direction (Converging Pointers) |
| :------------------------------ | :--------------------------------------- |
| Remove duplicates               | Find pairs in sorted arrays              |
| Partition array (fast/slow)     | Palindrome check                         |
| Contiguous subarrays            | Container/Area problems                  |
| Stream processing               | Binary search variants                   |

---

## Practice Problems

| # | Problem                   | Difficulty | Pattern                   |
| - | :------------------------ | :--------- | :------------------------ |
| 1 | Two Sum II (Sorted)       | Medium     | Basic opposite            |
| 2 | 3Sum                      | Medium     | Fix one + two pointers    |
| 3 | 3Sum Closest              | Medium     | Track closest             |
| 4 | Container With Most Water | Medium     | Max area bottleneck       |
| 5 | Trapping Rain Water       | Hard       | Left/right max tracking   |
| 6 | Valid Palindrome          | Easy       | Skip non-alphanum, verify |
| 7 | Sort Colors               | Medium     | Dutch flag (3-way)        |
| 8 | 4Sum                      | Medium     | Two loops + two pointers  |

---

## Key Takeaways

1. **Sorted array** -> Converging two pointers is almost always the right tool.
2. **Move based on comparison** -> Navigate towards the target like turning a steering wheel.
3. **Move the bottleneck** -> For area problems, moving the shorter element is the only way to improve.
4. **Skip duplicates** -> Crucial for returning unique solutions in problems like 3Sum.
5. **Three pointers** -> Elegant solution for three-way partition problems like Dutch National Flag.

---

## Next: [04-sliding-window-fixed.md](./04-sliding-window-fixed.md)

Learn the fixed-size sliding window for contiguous subarray problems.
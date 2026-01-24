# Two Sum Pattern - Solutions

## 1. Two Sum
Given an array of integers `nums` and an integer `target`, return indices of the two numbers such that they add up to `target`.

### Problem Statement
Find two distinct indices `i` and `j` in `nums` such that `nums[i] + nums[j] == target`. You may assume that each input would have exactly one solution, and you may not use the same element twice.

### Examples & Edge Cases
**Example 1:**
- Input: `nums = [2, 7, 11, 15], target = 9`
- Output: `[0, 1]` (2 + 7 = 9)

**Example 2:**
- Input: `nums = [3, 2, 4], target = 6`
- Output: `[1, 2]` (2 + 4 = 6)

**Edge Cases:**
- Negative numbers in `nums`.
- Target is 0 or negative.
- The two numbers are identical (e.g., `nums=[3, 3], target=6`).
- Large input size.

### Optimal Python Solution
```python
def twoSum(nums: list[int], target: int) -> list[int]:
    """
    Use a hashmap to store (value -> index) of elements we have already seen.
    For each number, check if its complement (target - num) exists in the map.
    """
    # Map to store: value -> index
    seen = {}

    for i, num in enumerate(nums):
        complement = target - num

        # If the complement has been seen before, we found the pair
        if complement in seen:
            return [seen[complement], i]

        # Otherwise, store current number and its index for future lookups
        seen[num] = i

    return [] # Should not happen based on problem constraints
```

### Explanation
1.  **Complement Calculation**: For every number `x`, we need another number `y` such that `x + y = target`. This means `y = target - x`. We call `y` the "complement".
2.  **One-Pass Strategy**: We iterate through the array once. At each step:
    - We calculate the required `complement`.
    - We check if this `complement` is in our `seen` dictionary.
    - If it is, we've found our two numbers! One is at the current index `i`, and the other is at the index stored in the dictionary.
    - If not, we store the current number `num` and its index `i` in the dictionary so that future numbers can look it up.
3.  **Why it works**: By storing numbers we've already visited, we transform a search problem (O(n)) into a lookup problem (O(1)).

### Complexity Analysis
- **Time Complexity**: O(n). We traverse the list of `n` elements exactly once. Each lookup and insertion in the hashmap takes O(1) time on average.
- **Space Complexity**: O(n). In the worst case, we might store `n - 1` elements in the hashmap before finding the solution.

---

## 2. Two Sum II - Input Array Is Sorted
Given a 1-indexed array of integers `numbers` that is already sorted in non-decreasing order, find two numbers such that they add up to a specific `target` number.

### Problem Statement
Find indices `i` and `j` (1-indexed) such that `numbers[i] + numbers[j] == target`. Since the array is sorted, we can optimize space compared to the hashmap approach.

### Examples & Edge Cases
**Example:**
- Input: `numbers = [2, 7, 11, 15], target = 9`
- Output: `[1, 2]`

**Edge Cases:**
- Two identical numbers adding to target.
- Summing negative numbers.
- Very large array.

### Optimal Python Solution
```python
def twoSumSorted(numbers: list[int], target: int) -> list[int]:
    """
    Since the array is sorted, use two pointers (left and right).
    Adjust pointers based on the current sum relative to the target.
    """
    left = 0
    right = len(numbers) - 1

    while left < right:
        current_sum = numbers[left] + numbers[right]

        if current_sum == target:
            # Found the pair, return 1-indexed results
            return [left + 1, right + 1]
        elif current_sum < target:
            # Sum is too small, increase the left pointer to get a larger value
            left += 1
        else:
            # Sum is too large, decrease the right pointer to get a smaller value
            right -= 1

    return []
```

### Explanation
1.  **Two Pointers**: We place one pointer at the start (`left`) and one at the end (`right`).
2.  **Greedy Movement**:
    - If `sum == target`, we are done.
    - If `sum < target`, we need a larger sum. Since the array is sorted, moving `left` to the right increases the sum.
    - If `sum > target`, we need a smaller sum. Moving `right` to the left decreases the sum.
3.  **Efficiency**: This avoids the O(n) extra space used by a hashmap.

### Complexity Analysis
- **Time Complexity**: O(n). We move the pointers at most `n` times total.
- **Space Complexity**: O(1). We only use two variables for the pointers.

---

## 3. 3Sum
Given an integer array `nums`, return all the triplets `[nums[i], nums[j], nums[k]]` such that `i != j`, `i != k`, and `j != k`, and `nums[i] + nums[j] + nums[k] == 0`.

### Problem Statement
Find all unique triplets that sum to zero. The solution set must not contain duplicate triplets.

### Examples & Edge Cases
**Example:**
- Input: `nums = [-1, 0, 1, 2, -1, -4]`
- Output: `[[-1, -1, 2], [-1, 0, 1]]`

**Edge Cases:**
- Array length < 3.
- All zeros.
- Large number of duplicates (e.g., `[0, 0, 0, 0]`).

### Optimal Python Solution
```python
def threeSum(nums: list[int]) -> list[list[int]]:
    """
    1. Sort the array.
    2. Iterate through each element as a potential first element 'a'.
    3. Use two pointers for the remaining elements to find 'b' and 'c' such that b + c = -a.
    """
    nums.sort()
    result = []

    for i in range(len(nums) - 2):
        # Skip duplicates for the first element to avoid duplicate triplets
        if i > 0 and nums[i] == nums[i - 1]:
            continue

        # Reduce problem to Two Sum II: find b + c = -nums[i]
        left, right = i + 1, len(nums) - 1
        target = -nums[i]

        while left < right:
            current_sum = nums[left] + nums[right]

            if current_sum == target:
                result.append([nums[i], nums[left], nums[right]])
                # Skip duplicate values for second and third elements
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

### Explanation
We fix one number `nums[i]` and then solve the "Two Sum II" problem for the remaining part of the array to find two other numbers that sum to `-nums[i]`. Sorting is key here because it allows us to use the two-pointer optimization and easily skip duplicate numbers to ensure our results are unique.

### Complexity Analysis
- **Time Complexity**: O(n²). Sorting takes O(n log n). The nested loops take O(n²): we iterate `n` times, and for each iteration, the two-pointer scan takes O(n).
- **Space Complexity**: O(n) or O(log n) depending on the sorting implementation's internal space usage.

---

## 4. 3Sum Closest
Given an integer array `nums` of length `n` and an integer `target`, find three integers in `nums` such that the sum is closest to `target`.

### Problem Statement
Return the sum of the three integers. You may assume that each input would have exactly one solution.

### Examples & Edge Cases
**Example:**
- Input: `nums = [-1, 2, 1, -4], target = 1`
- Output: `2` ((-1) + 2 + 1 = 2)

### Optimal Python Solution
```python
def threeSumClosest(nums: list[int], target: int) -> int:
    nums.sort()
    closest_sum = float('inf')

    for i in range(len(nums) - 2):
        left, right = i + 1, len(nums) - 1

        while left < right:
            current_sum = nums[i] + nums[left] + nums[right]

            if current_sum == target:
                return target

            # Update closest_sum if current_sum is nearer to target
            if abs(target - current_sum) < abs(target - closest_sum):
                closest_sum = current_sum

            if current_sum < target:
                left += 1
            else:
                right -= 1

    return closest_sum
```

### Complexity Analysis
- **Time Complexity**: O(n²). Same logic as 3Sum.
- **Space Complexity**: O(log n) to O(n) for sorting.

---

## 5. 4Sum
Given an array `nums` and an integer `target`, return all unique quadruplets that sum to `target`.

### Optimal Python Solution
```python
def fourSum(nums: list[int], target: int) -> list[list[int]]:
    nums.sort()
    result = []
    n = len(nums)

    for i in range(n - 3):
        if i > 0 and nums[i] == nums[i - 1]: continue
        for j in range(i + 1, n - 2):
            if j > i + 1 and nums[j] == nums[j - 1]: continue

            left, right = j + 1, n - 1
            while left < right:
                curr = nums[i] + nums[j] + nums[left] + nums[right]
                if curr == target:
                    result.append([nums[i], nums[j], nums[left], nums[right]])
                    while left < right and nums[left] == nums[left + 1]: left += 1
                    while left < right and nums[right] == nums[right - 1]: right -= 1
                    left += 1
                    right -= 1
                elif curr < target:
                    left += 1
                else:
                    right -= 1
    return result
```

### Complexity Analysis
- **Time Complexity**: O(n³). Three nested levels of loops (fix two, then two-pointer scan).
- **Space Complexity**: O(log n) for sorting.

---

## 6. Two Sum Less Than K
Given an array `nums` and an integer `k`, return the maximum `sum` such that `sum < k` and `sum = nums[i] + nums[j]` for `i != j`.

### Optimal Python Solution
```python
def twoSumLessThanK(nums: list[int], k: int) -> int:
    nums.sort()
    left, right = 0, len(nums) - 1
    max_sum = -1

    while left < right:
        curr = nums[left] + nums[right]
        if curr < k:
            max_sum = max(max_sum, curr)
            left += 1
        else:
            right -= 1
    return max_sum
```

### Complexity Analysis
- **Time Complexity**: O(n log n) due to sorting. The scan is O(n).
- **Space Complexity**: O(1).

---

## 7. Pairs of Songs With Total Duration Divisible by 60
You are given a list of song durations `time`. Return the number of pairs of songs for which their total duration is divisible by 60.

### Optimal Python Solution
```python
from collections import defaultdict

def numPairsDivisibleBy60(time: list[int]) -> int:
    """
    Use modular arithmetic. (a + b) % 60 == 0 if:
    1. a % 60 == 0 AND b % 60 == 0
    2. (a % 60) + (b % 60) == 60
    """
    remainder_counts = defaultdict(int)
    count = 0

    for t in time:
        remainder = t % 60
        complement = (60 - remainder) % 60 # Handles 0 remainder correctly

        count += remainder_counts[complement]
        remainder_counts[remainder] += 1

    return count
```

### Complexity Analysis
- **Time Complexity**: O(n). Single pass over the songs.
- **Space Complexity**: O(1). The map has at most 60 keys.

---

## 8. Count Pairs With XOR in a Range
(Note: This is usually solved with a Trie, but a basic frequency map approach works for smaller ranges. For CTF/competitive programming context, we focus on the intuition.)
Given an array `nums` and two integers `low` and `high`, return the number of nice pairs. A nice pair is `(i, j)` where `0 <= i < j < n` and `low <= (nums[i] XOR nums[j]) <= high`.

*This problem is typically O(n log(max_val)) using a Bit Trie.*
Instead of a full implementation here, we note the connection: `a XOR b = target` is equivalent to `a XOR target = b`. This is the "Two Sum" property for XOR.
- **Time Complexity**: O(n log(max_val)).
- **Space Complexity**: O(n log(max_val)) for the Trie.

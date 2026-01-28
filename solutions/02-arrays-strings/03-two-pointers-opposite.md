# Two Pointers: Opposite Direction - Solutions

## Practice Problems

### 1. Two Sum II (Sorted)

**Problem Statement**: Given a 1-indexed array of integers `numbers` that is already sorted in non-decreasing order, find two numbers such that they add up to a specific `target` number. Return the indices of the two numbers, `index1` and `index2`, added by one.

**Examples & Edge Cases**:

- Example: `numbers = [2,7,11,15], target = 9` -> `[1, 2]`
- Edge Case: Exactly one solution exists.
- Edge Case: Target is formed by negative numbers.

**Optimal Python Solution**:

```python
def twoSum(numbers: list[int], target: int) -> list[int]:
    left = 0
    right = len(numbers) - 1

    while left < right:
        current_sum = numbers[left] + numbers[right]
        if current_sum == target:
            # 1-indexed result
            return [left + 1, right + 1]
        elif current_sum < target:
            left += 1
        else:
            right -= 1

    return []
```

**Explanation**:
In a sorted array, we use two pointers at the ends. If the sum is too small, we move the left pointer to increase the sum. If the sum is too large, we move the right pointer to decrease it.

**Complexity Analysis**:

- **Time Complexity**: O(n), where n is the length of the array.
- **Space Complexity**: O(1).

---

### 2. 3Sum

**Problem Statement**: Given an integer array `nums`, return all the triplets `[nums[i], nums[j], nums[k]]` such that `i != j`, `i != k`, and `j != k`, and `nums[i] + nums[j] + nums[k] == 0`. The solution set must not contain duplicate triplets.

**Optimal Python Solution**:

```python
def threeSum(nums: list[int]) -> list[list[int]]:
    nums.sort()
    res = []
    n = len(nums)

    for i in range(n):
        # Skip duplicate values for the first element
        if i > 0 and nums[i] == nums[i-1]:
            continue

        # We need nums[j] + nums[k] == -nums[i]
        target = -nums[i]
        left, right = i + 1, n - 1

        while left < right:
            s = nums[left] + nums[right]
            if s == target:
                res.append([nums[i], nums[left], nums[right]])
                # Skip duplicate values for second and third elements
                while left < right and nums[left] == nums[left+1]:
                    left += 1
                while left < right and nums[right] == nums[right-1]:
                    right -= 1
                left += 1
                right -= 1
            elif s < target:
                left += 1
            else:
                right -= 1
    return res
```

**Explanation**:
We sort the array first. Then we iterate through the array, fixing one element as the "first" element of our triplet. For the remaining part of the array, we perform a standard Two Sum (Sorted) to find two numbers that add up to the negative of our fixed element. To avoid duplicates, we skip identical elements for all three positions.

**Complexity Analysis**:

- **Time Complexity**: O(n²), where n is the length of the array. Sorting takes O(n log n) and the nested loops take O(n²).
- **Space Complexity**: O(log n) to O(n) depending on the sorting implementation.

---

### 3. 3Sum Closest

**Problem Statement**: Given an integer array `nums` of length `n` and an integer `target`, find three integers in `nums` such that the sum is closest to `target`. Return the sum of the three integers.

**Optimal Python Solution**:

```python
def threeSumClosest(nums: list[int], target: int) -> int:
    nums.sort()
    n = len(nums)
    closest_sum = float('inf')

    for i in range(n):
        left, right = i + 1, n - 1
        while left < right:
            current_sum = nums[i] + nums[left] + nums[right]
            if current_sum == target:
                return current_sum

            if abs(current_sum - target) < abs(closest_sum - target):
                closest_sum = current_sum

            if current_sum < target:
                left += 1
            else:
                right -= 1

    return closest_sum
```

**Explanation**:
Similar to 3Sum, we sort the array and iterate through it. For each element, we use two pointers to find the pair that makes the triplet sum as close to the target as possible, updating our `closest_sum` whenever we find a better one.

**Complexity Analysis**:

- **Time Complexity**: O(n²).
- **Space Complexity**: O(log n) for sorting.

---

### 4. Container With Most Water

**Problem Statement**: You are given an integer array `height` of length `n`. There are `n` vertical lines drawn such that the two endpoints of the `i-th` line are `(i, 0)` and `(i, height[i])`. Find two lines that together with the x-axis form a container, such that the container contains the most water. Return the maximum amount of water a container can store.

**Optimal Python Solution**:

```python
def maxArea(height: list[int]) -> int:
    left, right = 0, len(height) - 1
    max_water = 0

    while left < right:
        # Calculate current area
        width = right - left
        h = min(height[left], height[right])
        max_water = max(max_water, width * h)

        # Move the pointer pointing to the shorter line
        if height[left] < height[right]:
            left += 1
        else:
            right -= 1

    return max_water
```

**Explanation**:
The area is limited by the shorter line. Moving the taller line will only decrease the width without any chance of increasing the height limit. Therefore, we must move the shorter line's pointer to potentially find a taller line that compensates for the decreased width.

**Complexity Analysis**:

- **Time Complexity**: O(n).
- **Space Complexity**: O(1).

---

### 5. Trapping Rain Water

**Problem Statement**: Given `n` non-negative integers representing an elevation map where the width of each bar is 1, compute how much water it can trap after raining.

**Optimal Python Solution**:

```python
def trap(height: list[int]) -> int:
    if not height:
        return 0

    left, right = 0, len(height) - 1
    left_max, right_max = height[left], height[right]
    total_water = 0

    while left < right:
        if left_max < right_max:
            left += 1
            left_max = max(left_max, height[left])
            total_water += left_max - height[left]
        else:
            right -= 1
            right_max = max(right_max, height[right])
            total_water += right_max - height[right]

    return total_water
```

**Explanation**:
The amount of water at any index is `min(max_left, max_right) - height[i]`. We use two pointers and track the maximum height seen from the left and right. By always processing the side with the smaller current maximum, we can guarantee that the "other side's" maximum is at least as large, satisfying the `min` condition.

**Complexity Analysis**:

- **Time Complexity**: O(n).
- **Space Complexity**: O(1).

---

### 6. Valid Palindrome

**Problem Statement**: Given a string `s`, return `true` if it is a palindrome, or `false` otherwise, after converting all uppercase letters into lowercase letters and removing all non-alphanumeric characters.

**Optimal Python Solution**:

```python
def isPalindrome(s: str) -> bool:
    left, right = 0, len(s) - 1

    while left < right:
        # Move pointers to the next alphanumeric characters
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

**Explanation**:
We use two pointers at the start and end of the string. We skip non-alphanumeric characters and compare the lowercase versions of the characters at the pointers.

**Complexity Analysis**:

- **Time Complexity**: O(n).
- **Space Complexity**: O(1).

---

### 7. Sort Colors

**Problem Statement**: Sort an array containing 0s, 1s, and 2s in-place.

**Optimal Python Solution**:

```python
def sortColors(nums: list[int]) -> None:
    low = 0
    curr = 0
    high = len(nums) - 1

    while curr <= high:
        if nums[curr] == 0:
            nums[low], nums[curr] = nums[curr], nums[low]
            low += 1
            curr += 1
        elif nums[curr] == 2:
            nums[high], nums[curr] = nums[curr], nums[high]
            high -= 1
        else:
            curr += 1
```

**Explanation**:
This uses three pointers to partition the array into three sections.

**Complexity Analysis**:

- **Time Complexity**: O(n).
- **Space Complexity**: O(1).

---

### 8. 4Sum

**Problem Statement**: Given an array `nums` of `n` integers, return an array of all unique quadruplets `[nums[a], nums[b], nums[c], nums[d]]` such that their sum is equal to `target`.

**Optimal Python Solution**:

```python
def fourSum(nums: list[int], target: int) -> list[list[int]]:
    nums.sort()
    n = len(nums)
    res = []

    for i in range(n - 3):
        if i > 0 and nums[i] == nums[i-1]:
            continue
        for j in range(i + 1, n - 2):
            if j > i + 1 and nums[j] == nums[j-1]:
                continue

            # Standard Two Sum (Sorted) for the remaining two
            left, right = j + 1, n - 1
            rem_target = target - nums[i] - nums[j]

            while left < right:
                s = nums[left] + nums[right]
                if s == rem_target:
                    res.append([nums[i], nums[j], nums[left], nums[right]])
                    while left < right and nums[left] == nums[left+1]:
                        left += 1
                    while left < right and nums[right] == nums[right-1]:
                        right -= 1
                    left += 1
                    right -= 1
                elif s < rem_target:
                    left += 1
                else:
                    right -= 1
    return res
```

**Explanation**:
4Sum is solved by nesting loops to reduce it to a 3Sum problem, then a 2Sum problem. We sort the array and use pointers while being careful to skip duplicates at each level.

**Complexity Analysis**:

- **Time Complexity**: O(n³).
- **Space Complexity**: O(log n) for sorting.

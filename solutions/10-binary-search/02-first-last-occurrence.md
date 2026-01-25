# First and Last Occurrence Solutions

## 1. Find First and Last Position of Element in Sorted Array
[LeetCode 34](https://leetcode.com/problems/find-first-and-last-position-of-element-in-sorted-array/)

### Problem Description
Given an array of integers `nums` sorted in non-decreasing order, find the starting and ending position of a given `target` value. If `target` is not found in the array, return `[-1, -1]`.

### Solution
```python
def searchRange(nums: list[int], target: int) -> list[int]:
    def find_boundary(is_first: bool) -> int:
        left, right = 0, len(nums) - 1
        res = -1
        while left <= right:
            mid = left + (right - left) // 2
            if nums[mid] == target:
                res = mid
                if is_first:
                    right = mid - 1
                else:
                    left = mid + 1
            elif nums[mid] < target:
                left = mid + 1
            else:
                right = mid - 1
        return res

    return [find_boundary(True), find_boundary(False)]
```
- **Time Complexity**: O(log n)
- **Space Complexity**: O(1)

---

## 2. Count of Smaller Numbers After Self
[LeetCode 315](https://leetcode.com/problems/count-of-smaller-numbers-after-self/)

### Problem Description
Given an integer array `nums`, return an integer array `counts` where `counts[i]` is the number of smaller elements to the right of `nums[i]`.

### Solution
```python
import bisect

def countSmaller(nums: list[int]) -> list[int]:
    """
    Using binary search (bisect) to maintain a sorted list of seen elements.
    Time: O(n log n) - n elements, each takes log n to find index and n to insert.
    Actually O(n^2) in worst case due to list insertion, but efficient for many test cases.
    Optimal is O(n log n) using Merge Sort or Fenwick Tree.
    """
    res = []
    sorted_list = []

    # Iterate from right to left
    for num in reversed(nums):
        # Find the insertion point (left) to see how many elements are smaller
        idx = bisect.bisect_left(sorted_list, num)
        res.append(idx)
        # Insert while maintaining sorted order
        bisect.insort(sorted_list, num)

    return res[::-1]
```
- **Time Complexity**: O(n log n) average (due to bisect), O(n²) worst (due to list insertion)
- **Space Complexity**: O(n)

---

## 3. Find Smallest Letter Greater Than Target
[LeetCode 744](https://leetcode.com/problems/find-smallest-letter-greater-than-target/)

### Problem Description
You are given an array of characters `letters` that is sorted in non-decreasing order, and a character `target`. There are at least two different characters in `letters`. Return the smallest character in `letters` that is lexicographically greater than `target`. If such a character does not exist, return the first character in `letters`.

### Solution
```python
def nextGreatestLetter(letters: list[str], target: str) -> str:
    left, right = 0, len(letters) - 1

    if target >= letters[-1]:
        return letters[0]

    while left < right:
        mid = left + (right - left) // 2
        if letters[mid] <= target:
            left = mid + 1
        else:
            right = mid

    return letters[left]
```
- **Time Complexity**: O(log n)
- **Space Complexity**: O(1)

---

## 4. Single Element in a Sorted Array
[LeetCode 540](https://leetcode.com/problems/single-element-in-a-sorted-array/)

### Problem Description
You are given a sorted array consisting of only integers where every element appears exactly twice, except for one element which appears exactly once. Return the single element that appears only once. Your solution must run in O(log n) time and O(1) space.

### Solution
```python
def singleNonDuplicate(nums: list[int]) -> int:
    left, right = 0, len(nums) - 1

    while left < right:
        mid = left + (right - left) // 2
        # Ensure mid is even to check pair
        if mid % 2 == 1:
            mid -= 1

        if nums[mid] == nums[mid + 1]:
            # Pair is intact, single element is on the right
            left = mid + 2
        else:
            # Pair is broken, single element is on the left or is mid
            right = mid

    return nums[left]
```
- **Time Complexity**: O(log n)
- **Space Complexity**: O(1)

---

## 5. Find Minimum in Rotated Sorted Array
[LeetCode 153](https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/)

### Problem Description
Find the minimum element in a sorted rotated array of unique elements.

### Solution
```python
def findMin(nums: list[int]) -> int:
    left, right = 0, len(nums) - 1
    if nums[left] <= nums[right]:
        return nums[left]
    while left < right:
        mid = left + (right - left) // 2
        if nums[mid] > nums[right]:
            left = mid + 1
        else:
            right = mid
    return nums[left]
```
- **Time Complexity**: O(log n)
- **Space Complexity**: O(1)

---

## 6. Search Insert Position
[LeetCode 35](https://leetcode.com/problems/search-insert-position/)

### Problem Description
Given a sorted array of distinct integers and a target value, return the index if the target is found. If not, return the index where it would be if it were inserted in order.

### Solution
```python
def searchInsert(nums: list[int], target: int) -> int:
    left, right = 0, len(nums) - 1
    while left <= right:
        mid = left + (right - left) // 2
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return left
```
- **Time Complexity**: O(log n)
- **Space Complexity**: O(1)

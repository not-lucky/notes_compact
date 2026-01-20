# Two Sum

## Problem Statement

Given an array of integers `nums` and an integer `target`, return the indices of the two numbers such that they add up to `target`.

You may assume that each input would have exactly one solution, and you may not use the same element twice.

**Example:**
```
Input: nums = [2, 7, 11, 15], target = 9
Output: [0, 1]
Explanation: nums[0] + nums[1] = 2 + 7 = 9
```

## Approach

### Brute Force (Not Recommended)
Check every pair of numbers - O(n²) time complexity.

### Optimal: Hash Map (One Pass)
1. For each number, calculate its complement (target - num)
2. Check if complement exists in hash map
3. If yes, return both indices
4. If no, store current number and its index in hash map

**Key Insight:** Instead of searching for pairs, search for complements.

```
nums = [2, 7, 11, 15], target = 9

Step 1: num=2, complement=7, seen={} → not found, add {2: 0}
Step 2: num=7, complement=2, seen={2: 0} → found! return [0, 1]
```

## Implementation

```python
def two_sum(nums: list[int], target: int) -> list[int]:
    """
    Find two numbers that add up to target.

    Time: O(n) - single pass through array
    Space: O(n) - hash map stores at most n elements
    """
    seen = {}  # value -> index

    for i, num in enumerate(nums):
        complement = target - num

        if complement in seen:
            return [seen[complement], i]

        seen[num] = i

    return []  # No solution (shouldn't happen per problem guarantee)


def two_sum_sorted(nums: list[int], target: int) -> list[int]:
    """
    Variant: If array is sorted, use two pointers.

    Time: O(n) - single pass
    Space: O(1) - no extra space
    """
    left, right = 0, len(nums) - 1

    while left < right:
        current_sum = nums[left] + nums[right]

        if current_sum == target:
            return [left, right]
        elif current_sum < target:
            left += 1  # Need larger sum
        else:
            right -= 1  # Need smaller sum

    return []
```

## Complexity Analysis

### Hash Map Approach
| Aspect | Complexity | Explanation |
|--------|------------|-------------|
| Time | O(n) | Single pass through array, O(1) hash lookups |
| Space | O(n) | Hash map stores up to n elements |

### Two Pointers (Sorted)
| Aspect | Complexity | Explanation |
|--------|------------|-------------|
| Time | O(n) | Single pass with two pointers |
| Space | O(1) | Only using two pointer variables |

## Edge Cases

1. **Minimum array size**: Array with exactly 2 elements
2. **Negative numbers**: Works the same way with negatives
3. **Zero in array**: `[0, 4, 3, 0]`, target=0 → `[0, 3]`
4. **Duplicate values**: `[3, 3]`, target=6 → `[0, 1]`
5. **Target requires same element twice**: Not allowed per problem constraints

## Common Mistakes

1. **Using same element twice**: `seen[num] = i` must come AFTER checking complement
2. **Returning values instead of indices**: Problem asks for indices
3. **Off-by-one errors**: Make sure to return both indices correctly

## Variations

### Two Sum II - Input Array Is Sorted
Use two pointers approach for O(1) space.

### Two Sum III - Data Structure Design
Design a class that supports `add()` and `find()` operations.

### Two Sum IV - Input is a BST
Use DFS + hash set, or inorder traversal + two pointers.

## Related Problems

- **3Sum** - Find three numbers that sum to zero
- **4Sum** - Find four numbers that sum to target
- **Two Sum Less Than K** - Find pair with sum < k and maximize
- **Subarray Sum Equals K** - Uses similar prefix sum + hash map technique

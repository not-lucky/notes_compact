# Subarray Sum with HashMap - Solutions

## 1. Subarray Sum Equals K
Given an array of integers `nums` and an integer `k`, return the total number of subarrays whose sum equals to `k`.

### Problem Statement
Find how many contiguous segments of the array add up to exactly `k`.

### Examples & Edge Cases
**Example 1:**
- Input: `nums = [1, 1, 1], k = 2`
- Output: `2`

**Example 2:**
- Input: `nums = [1, 2, 3], k = 3`
- Output: `2` ([1,2] and [3])

**Edge Cases:**
- Negative numbers in `nums`.
- `k = 0`.
- Array has one element.

### Optimal Python Solution
```python
def subarraySum(nums: list[int], k: int) -> int:
    """
    Use Prefix Sums and a HashMap.
    If sum(i...j) = k, then prefixSum[j] - prefixSum[i-1] = k.
    This implies prefixSum[i-1] = prefixSum[j] - k.
    """
    count = 0
    curr_sum = 0
    # map to store frequency of prefix sums
    # We initialize with {0: 1} to handle subarrays starting at index 0
    prefix_sums = {0: 1}

    for num in nums:
        curr_sum += num

        # Check if (curr_sum - k) has been seen before
        if curr_sum - k in prefix_sums:
            count += prefix_sums[curr_sum - k]

        # Record this prefix sum
        prefix_sums[curr_sum] = prefix_sums.get(curr_sum, 0) + 1

    return count
```

### Explanation
1.  **Prefix Sum Concept**: A prefix sum at index `j` is the sum of all elements from `0` to `j`.
2.  **The Formula**: The sum of a subarray between index `i` and `j` is `PrefixSum[j] - PrefixSum[i-1]`. We want this to be `k`.
3.  **Hashmap Optimization**: As we iterate, we keep track of how many times each `PrefixSum` has occurred. For each new `curr_sum`, we check if `curr_sum - k` exists in our history. If it does, every time `curr_sum - k` occurred in the past marks the start of a valid subarray ending right now.
4.  **Dummy Entry**: `{0: 1}` is critical. It represents the case where `curr_sum` itself is equal to `k`, meaning the subarray starts at the very beginning of the array.

### Complexity Analysis
- **Time Complexity**: O(n). We iterate through the array once.
- **Space Complexity**: O(n). In the worst case, we store `n` unique prefix sums in the hashmap.

---

## 2. Subarray Sums Divisible by K
Given an integer array `nums` and an integer `k`, return the number of non-empty subarrays that have a sum divisible by `k`.

### Optimal Python Solution
```python
def subarraysDivByK(nums: list[int], k: int) -> int:
    """
    If (sum_j - sum_i) % k == 0, then sum_j % k == sum_i % k.
    Count frequencies of prefix sum remainders.
    """
    count = 0
    curr_sum = 0
    # map to store frequency of remainders
    remainders = {0: 1}

    for num in nums:
        curr_sum += num
        rem = curr_sum % k

        # Python handles negative modulo correctly (e.g., -1 % 5 = 4)
        if rem in remainders:
            count += remainders[rem]

        remainders[rem] = remainders.get(rem, 0) + 1

    return count
```

### Complexity Analysis
- **Time Complexity**: O(n).
- **Space Complexity**: O(k). There are at most `k` unique remainders.

---

## 3. Maximum Size Subarray Sum Equals K
Given an array `nums` and an integer `k`, find the maximum length of a subarray that sums to `k`. If there isn't one, return 0 instead.

### Optimal Python Solution
```python
def maxSubArrayLen(nums: list[int], k: int) -> int:
    """
    Similar to counting, but store the FIRST index each prefix sum occurs.
    Longest length = current_index - first_index_of_(curr_sum - k).
    """
    first_seen = {0: -1}
    curr_sum = 0
    max_len = 0

    for i, num in enumerate(nums):
        curr_sum += num

        if curr_sum - k in first_seen:
            max_len = max(max_len, i - first_seen[curr_sum - k])

        # Only record the first time we see a prefix sum to maximize distance
        if curr_sum not in first_seen:
            first_seen[curr_sum] = i

    return max_len
```

### Complexity Analysis
- **Time Complexity**: O(n).
- **Space Complexity**: O(n).

---

## 4. Contiguous Array
Given a binary array `nums`, return the maximum length of a contiguous subarray with an equal number of 0 and 1.

### Optimal Python Solution
```python
def findMaxLength(nums: list[int]) -> int:
    """
    Treat 0 as -1. The problem becomes: find the longest subarray with sum 0.
    """
    # map stores prefix_sum -> first_index
    first_seen = {0: -1}
    curr_sum = 0
    max_len = 0

    for i, num in enumerate(nums):
        # Transform 0 to -1
        curr_sum += (1 if num == 1 else -1)

        if curr_sum in first_seen:
            max_len = max(max_len, i - first_seen[curr_sum])
        else:
            first_seen[curr_sum] = i

    return max_len
```

---

## 5. Continuous Subarray Sum
Given an integer array `nums` and an integer `k`, return `true` if `nums` has a continuous subarray of size at least two whose sum is a multiple of `k`.

### Optimal Python Solution
```python
def checkSubarraySum(nums: list[int], k: int) -> bool:
    # remainder -> first_index
    first_seen = {0: -1}
    curr_sum = 0

    for i, num in enumerate(nums):
        curr_sum += num
        rem = curr_sum % k

        if rem in first_seen:
            if i - first_seen[rem] >= 2:
                return True
        else:
            first_seen[rem] = i
    return False
```

---

## 6. Binary Subarrays With Sum
Given a binary array `nums` and an integer `goal`, return the number of non-empty subarrays with a sum equal to `goal`.

### Optimal Python Solution
Same logic as "Subarray Sum Equals K". Since it's binary, `curr_sum` is non-decreasing, but the hashmap approach remains O(n) and works perfectly.

---

## 7. Count Nice Subarrays
Given an array of integers `nums` and an integer `k`. A continuous subarray is called nice if there are `k` odd numbers on it. Return the number of nice subarrays.

### Optimal Python Solution
Transform: replace odd with 1, even with 0. Problem becomes "Binary Subarrays with Sum K".
O(n) Time, O(n) Space.

---

## 8. Minimum Size Subarray Sum
Given an array of positive integers `nums` and a positive integer `target`, return the minimal length of a contiguous subarray of which the sum is greater than or equal to `target`. If there is no such subarray, return 0 instead.

### Optimal Python Solution (Sliding Window)
```python
def minSubArrayLen(target: int, nums: list[int]) -> int:
    """
    Since all numbers are positive, use sliding window for O(1) space.
    """
    l = 0
    curr_sum = 0
    res = float('inf')

    for r in range(len(nums)):
        curr_sum += nums[r]
        while curr_sum >= target:
            res = min(res, r - l + 1)
            curr_sum -= nums[l]
            l += 1

    return res if res != float('inf') else 0
```
**Crucial Note**: We use sliding window here because elements are positive, making the prefix sums monotonic. If there were negatives, we would need a different approach (like a segment tree or binary search on prefix sums).

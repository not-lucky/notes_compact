# Prefix Sum - Solutions

## Practice Problems

### 1. Range Sum Query - Immutable

**Problem Statement**: Given an integer array `nums`, handle multiple queries of the form: calculate the sum of the elements of `nums` between indices `left` and `right` inclusive.

**Optimal Python Solution**:

```python
class NumArray:
    def __init__(self, nums: list[int]):
        # prefix[i] stores the sum of nums[0...i-1]
        self.prefix = [0] * (len(nums) + 1)
        for i in range(len(nums)):
            self.prefix[i + 1] = self.prefix[i] + nums[i]

    def sumRange(self, left: int, right: int) -> int:
        # Sum of nums[left...right] = prefix[right+1] - prefix[left]
        return self.prefix[right + 1] - self.prefix[left]
```

**Explanation**:
We precompute a prefix sum array where `prefix[i]` is the sum of the first `i` elements. To get the sum of elements from index `left` to `right`, we take the cumulative sum up to `right` and subtract the cumulative sum up to `left - 1`. Using a leading zero (`prefix[0] = 0`) simplifies the formula to `prefix[right + 1] - prefix[left]`.

**Complexity Analysis**:

- **Time Complexity**:
  - Initialization: O(n) to build the prefix sum array.
  - Query: O(1) per `sumRange` call.
- **Space Complexity**: O(n) to store the prefix sum array.

---

### 2. Range Sum Query 2D - Immutable

**Problem Statement**: Given a 2D matrix `matrix`, handle multiple queries of the form: calculate the sum of the elements of `matrix` inside the rectangle defined by its upper left corner `(row1, col1)` and lower right corner `(row2, col2)`.

**Optimal Python Solution**:

```python
class NumMatrix:
    def __init__(self, matrix: list[list[int]]):
        if not matrix or not matrix[0]: return
        R, C = len(matrix), len(matrix[0])
        self.ps = [[0] * (C + 1) for _ in range(R + 1)]

        for r in range(R):
            for c in range(C):
                self.ps[r + 1][c + 1] = (matrix[r][c] +
                                         self.ps[r][c + 1] +
                                         self.ps[r + 1][c] -
                                         self.ps[r][c])

    def sumRegion(self, r1: int, c1: int, r2: int, c2: int) -> int:
        return (self.ps[r2 + 1][c2 + 1] -
                self.ps[r1][c2 + 1] -
                self.ps[r2 + 1][c1] +
                self.ps[r1][c1])
```

**Explanation**:
We extend the 1D prefix sum concept to 2D. `ps[r+1][c+1]` stores the sum of all elements in the rectangle from `(0,0)` to `(r,c)`. To find any sub-rectangle sum, we use the inclusion-exclusion principle: take the large rectangle from origin, subtract the top and left rectangles, and add back the top-left corner that was subtracted twice.

**Complexity Analysis**:

- **Time Complexity**: Initialization O(R\*C), Query O(1).
- **Space Complexity**: O(R\*C).

---

### 3. Subarray Sum Equals K

**Problem Statement**: Given an array of integers `nums` and an integer `k`, return the total number of subarrays whose sum equals to `k`.

**Optimal Python Solution**:

```python
def subarraySum(nums: list[int], k: int) -> int:
    count = 0
    curr_sum = 0
    # Map to store frequency of prefix sums
    # Base case: a prefix sum of 0 has been seen once
    prefix_sums = {0: 1}

    for num in nums:
        curr_sum += num
        # If curr_sum - k is in prefix_sums, it means there are
        # subarrays ending here that sum to k
        if curr_sum - k in prefix_sums:
            count += prefix_sums[curr_sum - k]

        prefix_sums[curr_sum] = prefix_sums.get(curr_sum, 0) + 1

    return count
```

**Explanation**:
Let $S[i]$ be the prefix sum up to index $i$. A subarray from $j$ to $i$ has sum $k$ if $S[i] - S[j-1] = k$, or $S[j-1] = S[i] - k$. As we iterate, we store the frequency of each prefix sum we encounter in a hash map. At each index, we check how many times the value `current_prefix_sum - k` has appeared previously.

**Complexity Analysis**:

- **Time Complexity**: O(n), single pass.
- **Space Complexity**: O(n) to store the hash map.

---

### 4. Subarray Sums Divisible by K

**Problem Statement**: Given an integer array `nums` and an integer `k`, return the number of non-empty subarrays that have a sum divisible by `k`.

**Optimal Python Solution**:

```python
def subarraysDivByK(nums: list[int], k: int) -> int:
    # Use mod frequencies. (sum1 - sum2) % k == 0 => sum1 % k == sum2 % k
    mod_counts = {0: 1}
    curr_sum = 0
    res = 0

    for num in nums:
        curr_sum += num
        mod = curr_sum % k
        # Handle negative numbers in Python: % k already returns [0, k-1]
        if mod in mod_counts:
            res += mod_counts[mod]
        mod_counts[mod] = mod_counts.get(mod, 0) + 1

    return res
```

**Explanation**:
The sum of a subarray $nums[i...j]$ is divisible by $k$ if $PrefixSum[j] \equiv PrefixSum[i-1] \pmod k$. We track the frequency of each remainder we see. If we encounter a remainder we've seen $n$ times before, it means there are $n$ subarrays ending at the current index that are divisible by $k$.

**Complexity Analysis**:

- **Time Complexity**: O(n).
- **Space Complexity**: O(k) for the hash map of remainders.

---

### 5. Product of Array Except Self

**Problem Statement**: Return an array `answer` where `answer[i]` is the product of all elements except `nums[i]`. No division allowed.

**Optimal Python Solution**:

```python
def productExceptSelf(nums: list[int]) -> list[int]:
    n = len(nums)
    res = [1] * n

    # Forward pass: calculate prefix products
    prefix = 1
    for i in range(n):
        res[i] = prefix
        prefix *= nums[i]

    # Backward pass: multiply by suffix products
    suffix = 1
    for i in range(n - 1, -1, -1):
        res[i] *= suffix
        suffix *= nums[i]

    return res
```

**Explanation**:
Any element's "product except self" is the product of everything to its left (prefix) multiplied by everything to its right (suffix). We compute the prefixes first, then iterate backwards to calculate and multiply the suffixes.

**Complexity Analysis**:

- **Time Complexity**: O(n).
- **Space Complexity**: O(1) extra space (excluding output).

---

### 6. Find Pivot Index

**Problem Statement**: Find the index where the sum of numbers to the left is equal to the sum of numbers to the right.

**Optimal Python Solution**:

```python
def pivotIndex(nums: list[int]) -> int:
    total = sum(nums)
    left_sum = 0

    for i, num in enumerate(nums):
        # right_sum = total - left_sum - nums[i]
        if left_sum == (total - left_sum - num):
            return i
        left_sum += num

    return -1
```

**Explanation**:
Instead of a full prefix sum array, we just need the `total` sum and a running `left_sum`. At any index `i`, the `right_sum` is simply `total - left_sum - nums[i]`. We check for equality and return the index.

**Complexity Analysis**:

- **Time Complexity**: O(n).
- **Space Complexity**: O(1).

---

### 7. Continuous Subarray Sum

**Problem Statement**: Given an integer array `nums` and an integer `k`, return `true` if `nums` has a continuous subarray of size at least two whose elements sum up to a multiple of `k`.

**Optimal Python Solution**:

```python
def checkSubarraySum(nums: list[int], k: int) -> bool:
    # Map remainders to their first occurrence index
    rem_map = {0: -1} # Sum of 0 before starting at index -1
    curr_sum = 0

    for i, num in enumerate(nums):
        curr_sum += num
        rem = curr_sum % k

        if rem in rem_map:
            # Check if subarray length is at least 2
            if i - rem_map[rem] >= 2:
                return True
        else:
            rem_map[rem] = i

    return False
```

**Explanation**:
Similar to Problem 4, we use remainders. To ensure the length is at least 2, we store the _index_ of the first time we saw a remainder. If we see the same remainder at index `i`, and `i - first_index >= 2`, we found a valid subarray.

**Complexity Analysis**:

- **Time Complexity**: O(n).
- **Space Complexity**: O(min(n, k)).

---

### 8. Maximum Size Subarray Sum Equals K

**Problem Statement**: Given an array `nums` and a target `k`, find the maximum length of a subarray that sums to `k`.

**Optimal Python Solution**:

```python
def maxSubArrayLen(nums: list[int], k: int) -> int:
    prefix_map = {0: -1} # prefix_sum -> first occurrence index
    curr_sum = 0
    max_len = 0

    for i, num in enumerate(nums):
        curr_sum += num

        if curr_sum - k in prefix_map:
            max_len = max(max_len, i - prefix_map[curr_sum - k])

        # Only store the FIRST occurrence to maximize length
        if curr_sum not in prefix_map:
            prefix_map[curr_sum] = i

    return max_len
```

**Explanation**:
We use the prefix sum approach with a hash map. Since we want the _maximum_ length, we only record the index of the _first_ time we see a particular prefix sum. This ensures that when we find a match, the distance between the current index and the recorded index is as large as possible.

**Complexity Analysis**:

- **Time Complexity**: O(n).
- **Space Complexity**: O(n).

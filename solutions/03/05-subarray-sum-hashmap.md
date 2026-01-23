# Subarray Sum with HashMap

## Practice Problems

### 1. Subarray Sum Equals K
**Difficulty:** Medium
**Key Technique:** Prefix Sum + HashMap (Count)

```python
def subarray_sum(nums: list[int], k: int) -> int:
    """
    Time: O(n)
    Space: O(n)
    """
    count = 0
    prefix_sum = 0
    prefix_count = {0: 1} # prefix_sum -> count
    for n in nums:
        prefix_sum += n
        if prefix_sum - k in prefix_count:
            count += prefix_count[prefix_sum - k]
        prefix_count[prefix_sum] = prefix_count.get(prefix_sum, 0) + 1
    return count
```

### 2. Subarray Sums Divisible by K
**Difficulty:** Medium
**Key Technique:** Prefix Mod + HashMap (Count)

```python
def subarrays_div_by_k(nums: list[int], k: int) -> int:
    """
    Time: O(n)
    Space: O(k)
    """
    count = 0
    prefix_sum = 0
    mod_count = {0: 1} # mod -> count
    for n in nums:
        prefix_sum += n
        mod = prefix_sum % k
        if mod in mod_count:
            count += mod_count[mod]
        mod_count[mod] = mod_count.get(mod, 0) + 1
    return count
```

### 3. Maximum Size Subarray Sum Equals K
**Difficulty:** Medium
**Key Technique:** Prefix Sum + HashMap (First Occurrence)

```python
def max_subarray_len(nums: list[int], k: int) -> int:
    """
    Time: O(n)
    Space: O(n)
    """
    prefix_sum = 0
    first_occ = {0: -1} # prefix_sum -> index
    max_len = 0
    for i, n in enumerate(nums):
        prefix_sum += n
        if prefix_sum - k in first_occ:
            max_len = max(max_len, i - first_occ[prefix_sum - k])
        if prefix_sum not in first_occ:
            first_occ[prefix_sum] = i
    return max_len
```

### 4. Contiguous Array
**Difficulty:** Medium
**Key Technique:** Prefix Sum (0 -> -1) + HashMap (First Occurrence)

```python
def find_max_length(nums: list[int]) -> int:
    """
    Longest subarray with equal number of 0s and 1s.
    Time: O(n)
    Space: O(n)
    """
    prefix_sum = 0
    first_occ = {0: -1}
    max_len = 0
    for i, n in enumerate(nums):
        prefix_sum += (1 if n == 1 else -1)
        if prefix_sum in first_occ:
            max_len = max(max_len, i - first_occ[prefix_sum])
        else:
            first_occ[prefix_sum] = i
    return max_len
```

### 5. Continuous Subarray Sum
**Difficulty:** Medium
**Key Technique:** Prefix Mod + HashMap (First Occurrence) + Size check

```python
def check_subarray_sum(nums: list[int], k: int) -> bool:
    """
    Subarray of size >= 2 whose sum is a multiple of k.
    Time: O(n)
    Space: O(min(n, k))
    """
    prefix_sum = 0
    first_occ = {0: -1}
    for i, n in enumerate(nums):
        prefix_sum += n
        mod = prefix_sum % k
        if mod in first_occ:
            if i - first_occ[mod] >= 2:
                return True
        else:
            first_occ[mod] = i
    return False
```

### 6. Binary Subarrays With Sum
**Difficulty:** Medium
**Key Technique:** Prefix Sum + HashMap

```python
def num_subarrays_with_sum(nums: list[int], goal: int) -> int:
    """
    Time: O(n)
    Space: O(n)
    """
    cnt = {0: 1}
    prefix = 0
    res = 0
    for n in nums:
        prefix += n
        res += cnt.get(prefix - goal, 0)
        cnt[prefix] = cnt.get(prefix, 0) + 1
    return res
```

### 7. Count Nice Subarrays
**Difficulty:** Medium
**Key Technique:** Prefix Sum (Odd count) + HashMap

```python
def number_of_subarrays(nums: list[int], k: int) -> int:
    """
    Subarrays with exactly k odd numbers.
    Time: O(n)
    Space: O(n)
    """
    cnt = {0: 1}
    prefix = 0
    res = 0
    for n in nums:
        prefix += n % 2
        res += cnt.get(prefix - k, 0)
        cnt[prefix] = cnt.get(prefix, 0) + 1
    return res
```

### 8. Minimum Size Subarray Sum
**Difficulty:** Medium
**Key Technique:** Sliding window (Positive numbers only)

```python
def min_subarray_len(target: int, nums: list[int]) -> int:
    """
    Time: O(n)
    Space: O(1)
    """
    l = 0
    curr = 0
    res = float('inf')
    for r in range(len(nums)):
        curr += nums[r]
        while curr >= target:
            res = min(res, r - l + 1)
            curr -= nums[l]
            l += 1
    return res if res != float('inf') else 0
```

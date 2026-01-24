# Solutions: XOR Tricks

## 1. Missing Number

**Problem Statement:**
Given an array `nums` containing `n` distinct numbers in the range `[0, n]`, return the only number in the range that is missing from the array.

**Constraints:**
- `n == nums.length`
- `1 <= n <= 10^4`
- `0 <= nums[i] <= n`

**Example:**
- Input: `nums = [3,0,1]`
- Output: `2`

**Python Implementation:**
```python
def missingNumber(nums: list[int]) -> int:
    n = len(nums)
    result = n
    for i in range(n):
        result ^= i ^ nums[i]
    return result
```

## 2. Single Number III

**Problem Statement:**
Given an integer array `nums`, in which exactly two elements appear only once and all the other elements appear exactly twice. Find the two elements that appear only once.

**Constraints:**
- `2 <= nums.length <= 3 * 10^4`
- `-2^31 <= nums[i] <= 2^31 - 1`

**Example:**
- Input: `nums = [1,2,1,3,2,5]`
- Output: `[3,5]`

**Python Implementation:**
```python
def singleNumber3(nums: list[int]) -> list[int]:
    xor_all = 0
    for num in nums:
        xor_all ^= num

    diff_bit = xor_all & (-xor_all)

    a, b = 0, 0
    for num in nums:
        if num & diff_bit:
            a ^= num
        else:
            b ^= num
    return [a, b]
```

## 3. Sum of Two Integers

**Problem Statement:**
Given two integers `a` and `b`, return the sum of the two integers without using the operators `+` and `-`.

**Constraints:**
- `-1000 <= a, b <= 1000`

**Example:**
- Input: `a = 1, b = 2`
- Output: `3`

**Python Implementation:**
```python
def getSum(a: int, b: int) -> int:
    mask = 0xFFFFFFFF
    max_int = 0x7FFFFFFF

    while b != 0:
        a, b = (a ^ b) & mask, ((a & b) << 1) & mask

    return a if a <= max_int else ~(a ^ mask)
```

## 4. Decode XORed Array

**Problem Statement:**
There is a hidden integer array `arr` that consists of `n` non-negative integers. It was encoded into another integer array `encoded` of length `n - 1`, where `encoded[i] = arr[i] XOR arr[i + 1]`. Given the `encoded` array and the first element `first`, return the original array `arr`.

**Constraints:**
- `2 <= n <= 10^4`
- `encoded.length == n - 1`
- `0 <= encoded[i] <= 10^5`
- `0 <= first <= 10^5`

**Example:**
- Input: `encoded = [1,2,3], first = 1`
- Output: `[1,0,2,1]`

**Python Implementation:**
```python
def decode(encoded: list[int], first: int) -> list[int]:
    result = [first]
    for val in encoded:
        result.append(result[-1] ^ val)
    return result
```

## 5. XOR Queries of a Subarray

**Problem Statement:**
Given the array `arr` of positive integers and the array `queries` where `queries[i] = [Li, Ri]`. For each query `i` compute the XOR of elements from `Li` to `Ri` (that is, `arr[Li] XOR arr[Li+1] XOR ... XOR arr[Ri]`). Return an array containing the results of the queries.

**Constraints:**
- `1 <= arr.length <= 3 * 10^4`
- `1 <= arr[i] <= 10^9`
- `1 <= queries.length <= 3 * 10^4`
- `queries[i].length == 2`
- `0 <= queries[i][0] <= queries[i][1] < arr.length`

**Example:**
- Input: `arr = [1,3,4,8], queries = [[0,1],[1,2],[0,3],[3,3]]`
- Output: `[2,7,14,8]`

**Python Implementation:**
```python
def xorQueries(arr: list[int], queries: list[list[int]]) -> list[int]:
    # Build prefix XOR array
    prefix = [0] * (len(arr) + 1)
    for i in range(len(arr)):
        prefix[i+1] = prefix[i] ^ arr[i]

    result = []
    for L, R in queries:
        # XOR of [L, R] = prefix[R+1] ^ prefix[L]
        result.append(prefix[R+1] ^ prefix[L])
    return result
```

## 6. Maximum XOR of Two Numbers in an Array

**Problem Statement:**
Given an integer array `nums`, return the maximum result of `nums[i] XOR nums[j]`, where `0 <= i <= j < n`.

**Constraints:**
- `1 <= nums.length <= 2 * 10^5`
- `0 <= nums[i] <= 2^31 - 1`

**Example:**
- Input: `nums = [3,10,5,25,2,8]`
- Output: `28` (5 XOR 25 = 28)

**Python Implementation:**
```python
def findMaximumXOR(nums: list[int]) -> int:
    max_xor = 0
    mask = 0
    # Process from MSB (30) to LSB (0)
    for i in range(30, -1, -1):
        mask |= (1 << i)
        prefixes = {num & mask for num in nums}

        # Greedy: Try to set the i-th bit to 1
        candidate = max_xor | (1 << i)
        for p in prefixes:
            if (candidate ^ p) in prefixes:
                max_xor = candidate
                break
    return max_xor
```

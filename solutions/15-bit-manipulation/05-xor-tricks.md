# XOR Tricks Solutions

## 1. Missing Number

**Problem Statement**: Given an array `nums` containing `n` distinct numbers in the range `[0, n]`, return the only number in the range that is missing from the array.

### Examples & Edge Cases

- **Example 1**: `nums = [3, 0, 1]` → `2`
- **Example 2**: `nums = [0, 1]` → `2`
- **Edge Cases**:
  - Missing number is 0 or n.

### Optimal Python Solution

```python
def missingNumber(nums: list[int]) -> int:
    """
    Finds the missing number using XOR properties.
    Everything that appears twice cancels out.
    """
    n = len(nums)
    missing = n # Start with n because range is [0, n]

    for i, num in enumerate(nums):
        # XOR with index and with value
        missing ^= i ^ num

    return missing
```

### Explanation

We use the XOR property `a ^ a = 0` and `a ^ 0 = a`. If we XOR all numbers from the sequence `0, 1, ..., n` and all numbers from the array `nums`, every number that is present in the array will appear exactly twice (once in the sequence and once in the array). The missing number will appear only once (in the sequence). XORing everything together will cancel out the duplicates, leaving only the missing number.

### Complexity Analysis

- **Time Complexity**: O(N) where N is the length of `nums`.
- **Space Complexity**: O(1) as we only use a single variable.

---

## 2. Single Number III

**Problem Statement**: Given an integer array `nums`, in which exactly two elements appear only once and all the other elements appear exactly twice. Find the two elements that appear only once. You can return the answer in any order.

### Examples & Edge Cases

- **Example**: `nums = [1, 2, 1, 3, 2, 5]` → `[3, 5]`
- **Edge Cases**:
  - Smallest array: `[a, b]`.

### Optimal Python Solution

```python
def singleNumber(nums: list[int]) -> list[int]:
    """
    Finds two unique numbers using XOR and partitioning.
    """
    # 1. XOR all numbers to get x ^ y
    xor_all = 0
    for num in nums:
        xor_all ^= num

    # 2. Find a bit where x and y differ
    # x & -x isolates the rightmost set bit
    diff_bit = xor_all & -xor_all

    # 3. Partition into two groups and XOR each group
    a, b = 0, 0
    for num in nums:
        if num & diff_bit:
            a ^= num
        else:
            b ^= num

    return [a, b]
```

### Explanation

First, we XOR all numbers in the array. Since all numbers except two (let's call them `x` and `y`) appear twice, the result will be `x ^ y`. Because `x != y`, there must be at least one bit position where they differ (one has 0, the other has 1). We isolate one such bit (the rightmost set bit) and use it to divide all numbers into two groups. Each group will contain one of the unique numbers and pairs of other numbers. XORing each group separately results in `x` and `y`.

### Complexity Analysis

- **Time Complexity**: O(N) where N is the number of elements in `nums`.
- **Space Complexity**: O(1) as we use constant extra space.

---

## 3. Sum of Two Integers

**Problem Statement**: Given two integers `a` and `b`, return the sum of the two integers without using the operators `+` and `-`.

### Examples & Edge Cases

- **Example**: `a = 1, b = 2` → `3`
- **Edge Cases**:
  - Negative numbers: Python requires masking because it handles arbitrary-precision integers.

### Optimal Python Solution

```python
def getSum(a: int, b: int) -> int:
    """
    Adds two integers using XOR for sum and AND for carry.
    Handles negative numbers by masking to 32 bits.
    """
    mask = 0xFFFFFFFF
    # 32-bit max positive integer
    max_int = 0x7FFFFFFF

    while b & mask:
        # Carry happens when both bits are 1
        carry = (a & b) << 1
        # XOR gives sum without carry
        a = a ^ b
        b = carry

    # If result is within 32-bit positive range, return as is
    # Otherwise, convert back to Python's negative representation
    a &= mask
    return a if a <= max_int else ~(a ^ mask)
```

### Explanation

Addition can be broken down into two parts: the sum without carry and the carry itself. The XOR operator (`a ^ b`) provides the sum of bits without considering carries. The AND operator followed by a left shift (`(a & b) << 1`) identifies where carries occur and moves them to the next bit position. We repeat this process until there are no more carries. In Python, we use `0xFFFFFFFF` to mask results to 32 bits, simulating fixed-width integer behavior.

### Complexity Analysis

- **Time Complexity**: O(1) in terms of bit length (at most 32 iterations for 32-bit integers).
- **Space Complexity**: O(1).

---

## 4. Decode XORed Array

**Problem Statement**: There is a hidden integer array `arr` that consists of `n` non-negative integers. It was encoded into another integer array `encoded` of length `n - 1`, where `encoded[i] = arr[i] XOR arr[i + 1]`. You are given the `encoded` array and the `first` element of `arr`. Return the original array `arr`.

### Examples & Edge Cases

- **Example**: `encoded = [1, 2, 3], first = 1` → `[1, 0, 2, 1]`
- **Edge Cases**:
  - `encoded` length is 1.

### Optimal Python Solution

```python
def decode(encoded: list[int], first: int) -> list[int]:
    """
    Decodes the array using the property: if a ^ b = c, then b = a ^ c.
    """
    arr = [first]
    for val in encoded:
        # arr[i+1] = arr[i] ^ encoded[i]
        arr.append(arr[-1] ^ val)
    return arr
```

### Explanation

The encoding is `encoded[i] = arr[i] ^ arr[i+1]`. By XORing both sides with `arr[i]`, we get `arr[i] ^ encoded[i] = arr[i] ^ arr[i] ^ arr[i+1]`. Since `arr[i] ^ arr[i] = 0`, we have `arr[i+1] = arr[i] ^ encoded[i]`. We can use this to iteratively reconstruct the original array starting from the given `first` element.

### Complexity Analysis

- **Time Complexity**: O(N) where N is the length of the `encoded` array.
- **Space Complexity**: O(N) to store the reconstructed array.

---

## 5. XOR Queries of a Subarray

**Problem Statement**: Given the array `arr` of positive integers and the array `queries` where `queries[i] = [Li, Ri]`, for each query compute the XOR value from index `Li` to `Ri`. Return an array containing the results.

### Examples & Edge Cases

- **Example**: `arr = [1, 3, 4, 8], queries = [[0, 1], [1, 2], [0, 3], [3, 3]]` → `[2, 7, 14, 8]`
- **Edge Cases**:
  - Queries on the same index: `[i, i]`.
  - Query on the whole array.

### Optimal Python Solution

```python
def xorQueries(arr: list[int], queries: list[list[int]]) -> list[int]:
    """
    Computes subarray XORs efficiently using a prefix XOR array.
    """
    # 1. Build prefix XOR array
    # prefix[i] = arr[0] ^ arr[1] ^ ... ^ arr[i-1]
    prefix = [0] * (len(arr) + 1)
    for i in range(len(arr)):
        prefix[i+1] = prefix[i] ^ arr[i]

    # 2. Answer queries in O(1)
    # XOR(L, R) = prefix[R+1] ^ prefix[L]
    result = []
    for L, R in queries:
        result.append(prefix[R+1] ^ prefix[L])

    return result
```

### Explanation

Calculating XOR for each query naively would take O(Q \* N). Instead, we use a technique similar to prefix sums. We create a `prefix` array where `prefix[i]` stores the XOR of all elements from `arr[0]` to `arr[i-1]`. The XOR sum of a subarray `arr[L...R]` is then `prefix[R+1] ^ prefix[L]`. This works because XORing `prefix[L]` into `prefix[R+1]` cancels out all elements from index `0` to `L-1`.

### Complexity Analysis

- **Time Complexity**: O(N + Q) where N is the length of `arr` and Q is the number of queries.
- **Space Complexity**: O(N) to store the prefix XOR array.

---

## 6. Maximum XOR of Two Numbers in an Array

**Problem Statement**: Given an integer array `nums`, return the maximum result of `nums[i] XOR nums[j]`, where `0 <= i <= j < n`.

### Examples & Edge Cases

- **Example**: `nums = [3, 10, 5, 25, 2, 8]` → `28` (5 ^ 25 = 28)

### Optimal Python Solution

```python
def findMaximumXOR(nums: list[int]) -> int:
    """
    Finds maximum XOR using a greedy approach with bitmasks.
    """
    max_xor = 0
    mask = 0

    # Iterate from most significant bit to least
    for i in range(31, -1, -1):
        # The mask will be 111...000 (i ones)
        mask |= (1 << i)

        # Collect prefixes of all numbers up to bit i
        prefixes = {num & mask for num in nums}

        # Try to see if we can set the i-th bit of max_xor to 1
        candidate = max_xor | (1 << i)

        # If there exist two prefixes p1, p2 such that p1 ^ p2 = candidate
        # then p1 ^ candidate = p2. If p2 is in our prefixes, we found them!
        for p in prefixes:
            if (p ^ candidate) in prefixes:
                max_xor = candidate
                break

    return max_xor
```

### Explanation

We build the maximum XOR bit by bit, from the most significant bit to the least significant. For each bit position `i`, we check if it's possible to have a 1 in that position for our `max_xor`. We assume it is possible (creating a `candidate`), and then check if there are two prefixes in our set that XOR to this `candidate`. We use the property `a ^ b = c => a ^ c = b`.

### Complexity Analysis

- **Time Complexity**: O(N \* log M) where M is the maximum value in `nums`. We iterate 32 times, and in each iteration, we traverse the array.
- **Space Complexity**: O(N) to store the prefixes.

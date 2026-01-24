# Solutions: Counting Bits

## 1. Number of 1 Bits

**Problem Statement:**
Write a function that takes the binary representation of a positive integer and returns the number of '1' bits it has (also known as the Hamming weight).

**Constraints:**
- The input must be a binary string of length 32.

**Example:**
- Input: `n = 11` (binary: 1011)
- Output: `3`

**Python Implementation:**
```python
def hammingWeight(n: int) -> int:
    count = 0
    while n:
        n &= n - 1  # Brian Kernighan's trick: clears rightmost set bit
        count += 1
    return count
```

## 2. Counting Bits

**Problem Statement:**
Given an integer `n`, return an array `ans` of length `n + 1` such that for each `i` (`0 <= i <= n`), `ans[i]` is the number of `1`'s in the binary representation of `i`.

**Constraints:**
- `0 <= n <= 10^5`

**Example:**
- Input: `n = 5`
- Output: `[0,1,1,2,1,2]`

**Python Implementation:**
```python
def countBits(n: int) -> list[int]:
    bits = [0] * (n + 1)
    for i in range(1, n + 1):
        # DP: i >> 1 is i with LSB removed. Add 1 if LSB was set.
        bits[i] = bits[i >> 1] + (i & 1)
    return bits
```

## 3. Hamming Distance

**Problem Statement:**
The Hamming distance between two integers is the number of positions at which the corresponding bits are different. Given two integers `x` and `y`, return the Hamming distance between them.

**Constraints:**
- `0 <= x, y <= 2^31 - 1`

**Example:**
- Input: `x = 1, y = 4`
- Output: `2`

**Python Implementation:**
```python
def hammingDistance(x: int, y: int) -> int:
    xor = x ^ y
    count = 0
    while xor:
        xor &= xor - 1
        count += 1
    return count
```

## 4. Total Hamming Distance

**Problem Statement:**
The Hamming distance between two integers is the number of positions at which the corresponding bits are different. Given an integer array `nums`, return the sum of Hamming distances between all the pairs of the integers in `nums`.

**Constraints:**
- `1 <= nums.length <= 10^4`
- `0 <= nums[i] <= 10^9`
- The answer for the test cases will fit within a 32-bit integer.

**Example:**
- Input: `nums = [4,14,2]`
- Output: `6`

**Python Implementation:**
```python
def totalHammingDistance(nums: list[int]) -> int:
    n = len(nums)
    total = 0
    for bit in range(32):
        ones = sum((num >> bit) & 1 for num in nums)
        zeros = n - ones
        total += ones * zeros
    return total
```

## 5. Minimum Bit Flips to Convert Number

**Problem Statement:**
A bit flip of a number `x` is choosing a bit in the binary representation of `x` and flipping it from either 0 to 1 or 1 to 0. Given two integers `start` and `goal`, return the minimum number of bit flips to convert `start` to `goal`.

**Constraints:**
- `0 <= start, goal <= 10^9`

**Example:**
- Input: `start = 10, goal = 7`
- Output: `3` (1010 to 0111)

**Python Implementation:**
```python
def minBitFlips(start: int, goal: int) -> int:
    xor = start ^ goal
    count = 0
    while xor:
        xor &= xor - 1
        count += 1
    return count
```

## 6. Prime Number of Set Bits in Binary Representation

**Problem Statement:**
Given two integers `left` and `right`, return the count of numbers in the inclusive range `[left, right]` having a prime number of set bits in their binary representation.

**Constraints:**
- `1 <= left <= right <= 10^6`
- `0 <= right - left <= 10^4`

**Example:**
- Input: `left = 6, right = 10`
- Output: `4`

**Python Implementation:**
```python
def countPrimeSetBits(left: int, right: int) -> int:
    # 32-bit primes: 2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31
    primes = {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31}
    count = 0
    for num in range(left, right + 1):
        if bin(num).count('1') in primes:
            count += 1
    return count
```

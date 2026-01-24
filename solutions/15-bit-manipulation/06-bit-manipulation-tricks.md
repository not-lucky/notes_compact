# Solutions: Bit Manipulation Tricks

## 1. Reverse Bits

**Problem Statement:**
Reverse bits of a given 32 bits unsigned integer.

**Constraints:**
- The input must be a binary string of length 32.

**Example:**
- Input: `n = 43261596` (00000010100101000001111010011100)
- Output: `964176192` (00111001011110000010100101000000)

**Python Implementation:**
```python
def reverseBits(n: int) -> int:
    result = 0
    for _ in range(32):
        result = (result << 1) | (n & 1)
        n >>= 1
    return result
```

## 2. Subsets

**Problem Statement:**
Given an integer array `nums` of unique elements, return all possible subsets (the power set). The solution set must not contain duplicate subsets. Return the solution in any order.

**Constraints:**
- `1 <= nums.length <= 10`
- `-10 <= nums[i] <= 10`
- All the numbers of `nums` are unique.

**Example:**
- Input: `nums = [1,2,3]`
- Output: `[[],[1],[2],[1,2],[3],[1,3],[2,3],[1,2,3]]`

**Python Implementation:**
```python
def subsets(nums: list[int]) -> list[list[int]]:
    n = len(nums)
    result = []
    # 2^n combinations
    for mask in range(1 << n):
        subset = []
        for i in range(n):
            if (mask >> i) & 1:
                subset.append(nums[i])
        result.append(subset)
    return result
```

## 3. Gray Code

**Problem Statement:**
An n-bit gray code sequence is a sequence of 2^n integers where:
- Every integer is in the inclusive range [0, 2^n - 1].
- The first integer is 0.
- An integer appears no more than once in the sequence.
- The binary representation of every pair of adjacent integers differs by exactly one bit.
- The binary representation of the first and last integers differs by exactly one bit.
Given an integer `n`, return any valid n-bit gray code sequence.

**Constraints:**
- `1 <= n <= 16`

**Example:**
- Input: `n = 2`
- Output: `[0,1,3,2]`

**Python Implementation:**
```python
def grayCode(n: int) -> list[int]:
    # Formula for gray code: G(i) = i ^ (i >> 1)
    return [i ^ (i >> 1) for i in range(1 << n)]
```

## 4. Single Number II

**Problem Statement:**
Given an integer array `nums` where every element appears three times except for one, which appears exactly once. Find the single element and return it.

**Constraints:**
- `1 <= nums.length <= 3 * 10^4`
- `-2^31 <= nums[i] <= 2^31 - 1`

**Example:**
- Input: `nums = [2,2,3,2]`
- Output: `3`

**Python Implementation:**
```python
def singleNumber2(nums: list[int]) -> int:
    ones = 0  # Bits seen once (mod 3)
    twos = 0  # Bits seen twice (mod 3)

    for num in nums:
        ones = (ones ^ num) & ~twos
        twos = (twos ^ num) & ~ones

    return ones
```

## 5. Maximum XOR of Two Numbers in an Array

**Problem Statement:**
Given an integer array `nums`, return the maximum result of `nums[i] XOR nums[j]`.

**Constraints:**
- `1 <= nums.length <= 2 * 10^5`
- `0 <= nums[i] <= 2^31 - 1`

**Example:**
- Input: `nums = [3,10,5,25,2,8]`
- Output: `28`

**Python Implementation:**
```python
def findMaximumXOR(nums: list[int]) -> int:
    max_xor = 0
    mask = 0
    for i in range(30, -1, -1):
        mask |= (1 << i)
        prefixes = {num & mask for num in nums}

        candidate = max_xor | (1 << i)
        for p in prefixes:
            if (candidate ^ p) in prefixes:
                max_xor = candidate
                break
    return max_xor
```

## 6. UTF-8 Validation

**Problem Statement:**
Given an integer array `data` representing the data, return whether it is a valid UTF-8 encoding.

**Constraints:**
- `1 <= data.length <= 2 * 10^4`
- `0 <= data[i] <= 255`

**Example:**
- Input: `data = [197, 130, 1]`
- Output: `true`

**Python Implementation:**
```python
def validUtf8(data: list[int]) -> bool:
    n_bytes = 0

    # Masks to check the leading bits of a byte
    mask1 = 1 << 7
    mask2 = 1 << 6

    for num in data:
        # Get only the last 8 bits
        num = num & 0xFF

        if n_bytes == 0:
            # Determine how many bytes in this UTF-8 character
            mask = 1 << 7
            while mask & num:
                n_bytes += 1
                mask >>= 1

            # 1-byte character
            if n_bytes == 0:
                continue

            # Invalid scenarios
            if n_bytes == 1 or n_bytes > 4:
                return False
        else:
            # Continuation bytes must start with 10
            if not (num & mask1 and not (num & mask2)):
                return False

        n_bytes -= 1

    return n_bytes == 0
```

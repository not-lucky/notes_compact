# Solutions: Power of Two

## 1. Power of Two

**Problem Statement:**
Given an integer `n`, return `true` if it is a power of two. Otherwise, return `false`. An integer `n` is a power of two if there exists an integer `x` such that `n == 2^x`.

**Constraints:**
- `-2^31 <= n <= 2^31 - 1`

**Example:**
- Input: `n = 16`
- Output: `true`

**Python Implementation:**
```python
def isPowerOfTwo(n: int) -> bool:
    return n > 0 and (n & (n - 1)) == 0
```

## 2. Power of Three

**Problem Statement:**
Given an integer `n`, return `true` if it is a power of three. Otherwise, return `false`. An integer `n` is a power of three if there exists an integer `x` such that `n == 3^x`.

**Constraints:**
- `-2^31 <= n <= 2^31 - 1`

**Example:**
- Input: `n = 27`
- Output: `true`

**Python Implementation:**
```python
def isPowerOfThree(n: int) -> bool:
    # 3^19 = 1162261467 is the largest power of 3 that fits in a 32-bit signed integer
    return n > 0 and 1162261467 % n == 0
```

## 3. Power of Four

**Problem Statement:**
Given an integer `n`, return `true` if it is a power of four. Otherwise, return `false`. An integer `n` is a power of four if there exists an integer `x` such that `n == 4^x`.

**Constraints:**
- `-2^31 <= n <= 2^31 - 1`

**Example:**
- Input: `n = 16`
- Output: `true`

**Python Implementation:**
```python
def isPowerOfFour(n: int) -> bool:
    # n must be positive and power of 2
    # AND the set bit must be at an even position (0, 2, 4...)
    # 0x55555555 = 01010101... (1s at even positions)
    return n > 0 and (n & (n - 1)) == 0 and (n & 0x55555555) != 0
```

## 4. Bitwise AND of Numbers Range

**Problem Statement:**
Given two integers `left` and `right` that represent the range `[left, right]`, return the bitwise AND of all numbers in this range, inclusive.

**Constraints:**
- `0 <= left <= right <= 2^31 - 1`

**Example:**
- Input: `left = 5, right = 7`
- Output: `4`

**Python Implementation:**
```python
def rangeBitwiseAnd(left: int, right: int) -> int:
    shift = 0
    while left < right:
        left >>= 1
        right >>= 1
        shift += 1
    return left << shift
```

## 5. Find Highest Set Bit

**Problem Statement:**
Given a positive integer `n`, find the position of the highest set bit (MSB).

**Constraints:**
- `1 <= n <= 2^31 - 1`

**Example:**
- Input: `n = 10` (1010 binary)
- Output: `3` (position 3 from right, 0-indexed)

**Python Implementation:**
```python
def findMSB(n: int) -> int:
    if n <= 0:
        return -1
    return n.bit_length() - 1
```

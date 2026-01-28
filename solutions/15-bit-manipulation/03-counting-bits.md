# Counting Bits Solutions

## 1. Number of 1 Bits
**Problem Statement**: Write a function that takes a positive integer and returns the number of '1' bits it has (also known as the Hamming weight).

### Examples & Edge Cases
- **Example 1**: `n = 11` (1011) → `3`
- **Example 2**: `n = 128` (10000000) → `1`
- **Edge Cases**:
    - Power of 2: Exactly one bit.
    - `0`: Zero bits.

### Optimal Python Solution
```python
def hammingWeight(n: int) -> int:
    """
    Counts set bits using Brian Kernighan's algorithm.
    Logic: n & (n-1) always clears the rightmost set bit.
    """
    count = 0
    while n:
        # Clear the rightmost set bit
        n &= (n - 1)
        count += 1
    return count
```

### Explanation
Brian Kernighan's algorithm is the most efficient way to count set bits manually. The operation `n & (n - 1)` removes the rightmost set bit of `n`. By repeating this in a loop until `n` becomes 0, the number of iterations will equal the number of set bits.

### Complexity Analysis
- **Time Complexity**: O(K) where K is the number of set bits. In the worst case (all bits set), it's O(bits), which is O(1) for fixed-size integers.
- **Space Complexity**: O(1).

---

## 2. Counting Bits
**Problem Statement**: Given an integer `n`, return an array `ans` of length `n + 1` such that for each `i` (`0 <= i <= n`), `ans[i]` is the number of `1`'s in the binary representation of `i`.

### Examples & Edge Cases
- **Example**: `n = 5` → `[0, 1, 1, 2, 1, 2]`
- **Edge Cases**:
    - `n = 0`: `[0]`.

### Optimal Python Solution
```python
def countBits(n: int) -> list[int]:
    """
    Generates bit counts for 0 to n using Dynamic Programming.
    """
    ans = [0] * (n + 1)
    for i in range(1, n + 1):
        # bits[i] = bits[i with rightmost set bit cleared] + 1
        ans[i] = ans[i & (i - 1)] + 1
    return ans
```

### Explanation
We use Dynamic Programming. The number of bits in `i` is 1 plus the number of bits in the number obtained by clearing `i`'s rightmost set bit. Since `i & (i - 1)` is always smaller than `i`, we already have its bit count stored in our `ans` array.

### Complexity Analysis
- **Time Complexity**: O(N) as we compute each value in the array once in constant time.
- **Space Complexity**: O(N) to store the result array.

---

## 3. Hamming Distance
**Problem Statement**: The Hamming distance between two integers is the number of positions at which the corresponding bits are different. Given two integers `x` and `y`, return the Hamming distance.

### Examples & Edge Cases
- **Example**: `x = 1`, `y = 4` → `2` (1 is 0001, 4 is 0100)
- **Edge Cases**:
    - `x == y`: Distance 0.

### Optimal Python Solution
```python
def hammingDistance(x: int, y: int) -> int:
    """
    Calculates Hamming distance using XOR and Brian Kernighan's.
    """
    # XOR gives 1s at positions where bits differ
    xor_res = x ^ y
    distance = 0
    while xor_res:
        # Count set bits in the XOR result
        xor_res &= (xor_res - 1)
        distance += 1
    return distance
```

### Explanation
The Hamming distance is simply the count of bits that are different between two numbers. XORing `x` and `y` results in a number where a bit is set to 1 if and only if the corresponding bits in `x` and `y` were different. We then use Brian Kernighan's algorithm to count the set bits in the XOR result.

### Complexity Analysis
- **Time Complexity**: O(K) where K is the number of differing bits.
- **Space Complexity**: O(1).

---

## 4. Total Hamming Distance
**Problem Statement**: Find the sum of Hamming distances between all pairs of integers in an array.

### Examples & Edge Cases
- **Example**: `[4, 14, 2]` → `6`
- **Edge Cases**:
    - Large array: O(N^2) would be too slow.

### Optimal Python Solution
```python
def totalHammingDistance(nums: list[int]) -> int:
    """
    Calculates total Hamming distance by counting 1s at each bit position.
    """
    total = 0
    n = len(nums)
    # Iterate through each of the 32 bit positions
    for i in range(32):
        # Count how many numbers have the i-th bit set
        count_ones = 0
        for num in nums:
            count_ones += (num >> i) & 1

        # Total pairs with different bits at this position = count_ones * count_zeros
        count_zeros = n - count_ones
        total += count_ones * count_zeros

    return total
```

### Explanation
Instead of comparing pairs (which is O(N^2)), we look at each bit position independently. For the `i`-th bit, if `k` numbers have a 1 and `n-k` numbers have a 0, then there are `k * (n-k)` pairs that differ at that specific bit position. Summing these contributions across all bit positions gives the total Hamming distance.

### Complexity Analysis
- **Time Complexity**: O(32 * N) = O(N).
- **Space Complexity**: O(1).

---

## 5. Minimum Bit Flips to Convert Number
**Problem Statement**: Given two integers `start` and `goal`, return the minimum number of bit flips to convert `start` to `goal`.

### Examples & Edge Cases
- **Example**: `start = 10` (1010), `goal = 7` (0111) → `3`
- **Edge Cases**:
    - `start == goal`: 0 flips.

### Optimal Python Solution
```python
def minBitFlips(start: int, goal: int) -> int:
    """
    Minimum bit flips is exactly the Hamming distance.
    """
    xor = start ^ goal
    count = 0
    while xor:
        xor &= (xor - 1)
        count += 1
    return count
```

### Explanation
The number of bits that need to be flipped to change `start` into `goal` is exactly the number of positions where their bits differ. This is the definition of Hamming distance. We XOR the two numbers and count the set bits in the result.

### Complexity Analysis
- **Time Complexity**: O(K) where K is the number of flips.
- **Space Complexity**: O(1).

---

## 6. Prime Number of Set Bits in Binary Representation
**Problem Statement**: Given two integers `left` and `right`, return the count of numbers in the inclusive range `[left, right]` having a prime number of set bits in their binary representation.

### Examples & Edge Cases
- **Example**: `left = 6, right = 10` → `4` (6: 2 bits, 7: 3 bits, 9: 2 bits, 10: 2 bits)
- **Edge Cases**:
    - Range can be up to 10^6.

### Optimal Python Solution
```python
def countPrimeSetBits(left: int, right: int) -> int:
    """
    Counts numbers in range with a prime number of set bits.
    """
    # Possible prime counts for a 32-bit integer
    primes = {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31}
    count = 0
    for num in range(left, right + 1):
        # Use Python built-in to count set bits
        if bin(num).count('1') in primes:
            count += 1
    return count
```

### Explanation
For each number in the range, we count its set bits. Since the maximum value of a bit count for a 32-bit integer is 32, we can pre-define the small set of prime numbers up to 31. We increment our counter if the bit count is in this set.

### Complexity Analysis
- **Time Complexity**: O(N * log M) where N is the number of integers in the range and M is the maximum value. `bin(num).count('1')` is very fast.
- **Space Complexity**: O(1).

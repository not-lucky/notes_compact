# Bit Manipulation Tricks Solutions

## 1. Reverse Bits
**Problem Statement**: Reverse bits of a given 32 bits unsigned integer.

### Examples & Edge Cases
- **Example**: `00000010100101000001111010011100` → `00111001011110000010100101000000`
- **Edge Cases**:
    - `0`: Returns `0`.
    - `0xFFFFFFFF`: Returns `0xFFFFFFFF`.

### Optimal Python Solution
```python
def reverseBits(n: int) -> int:
    """
    Reverses 32 bits using bitwise operations.
    """
    res = 0
    for _ in range(32):
        # Shift result left to make room
        res <<= 1
        # Extract LSB of n and OR it into res
        res |= (n & 1)
        # Shift n right to get next bit
        n >>= 1
    return res
```

### Explanation
We treat the integer as a sequence of 32 bits. We iterate 32 times, in each step moving the rightmost bit of `n` to the rightmost position of our `res`. To do this, we shift `res` left at the start of each loop and shift `n` right at the end. This effectively reverses the order of the bits.

### Complexity Analysis
- **Time Complexity**: O(1) as we always perform 32 iterations.
- **Space Complexity**: O(1).

---

## 2. Subsets
**Problem Statement**: Given an integer array `nums` of unique elements, return all possible subsets (the power set). The solution set must not contain duplicate subsets. Return the solution in any order.

### Examples & Edge Cases
- **Example**: `nums = [1, 2, 3]` → `[[], [1], [2], [1, 2], [3], [1, 3], [2, 3], [1, 2, 3]]`
- **Edge Cases**:
    - Empty list: `[[]]`.

### Optimal Python Solution
```python
def subsets(nums: list[int]) -> list[list[int]]:
    """
    Generates all subsets using bitmasking.
    A bitmask of length n can represent any subset of a set of size n.
    """
    n = len(nums)
    output = []

    # There are 2^n possible subsets
    for i in range(1 << n):
        # Create a bitmask from i
        # Each set bit in the mask indicates inclusion of the element
        subset = []
        for j in range(n):
            if (i >> j) & 1:
                subset.append(nums[j])
        output.append(subset)

    return output
```

### Explanation
A set of size `n` has `2^n` possible subsets. We can map each subset to a unique binary number from `0` to `2^n - 1`. For a given number `i`, if its `j`-th bit is `1`, it means the `j`-th element of `nums` is included in that specific subset. By iterating through all such numbers, we generate every possible subset exactly once.

### Complexity Analysis
- **Time Complexity**: O(N * 2^N) to generate all subsets and iterate through each bit.
- **Space Complexity**: O(N * 2^N) to store all subsets.

---

## 3. Gray Code
**Problem Statement**: An n-bit gray code sequence is a sequence of 2^n integers where every adjacent pair of integers differs by exactly one bit. Given an integer `n`, return any valid n-bit gray code sequence.

### Examples & Edge Cases
- **Example 1**: `n = 2` → `[0, 1, 3, 2]`
- **Example 2**: `n = 1` → `[0, 1]`

### Optimal Python Solution
```python
def grayCode(n: int) -> list[int]:
    """
    Generates Gray code sequence using the standard conversion formula.
    Binary to Gray formula: G(i) = i ^ (i >> 1)
    """
    # Total 2^n numbers in the sequence
    return [i ^ (i >> 1) for i in range(1 << n)]
```

### Explanation
The conversion from binary representation `i` to its Gray code counterpart `G(i)` is given by the formula `i ^ (i >> 1)`. This formula ensures that the Gray code of `i` and `i+1` differs by exactly one bit. By generating this for all `i` from `0` up to `2^n - 1`, we get the full sequence.

### Complexity Analysis
- **Time Complexity**: O(2^N).
- **Space Complexity**: O(2^N) for the result list.

---

## 4. Single Number II
**Problem Statement**: Every element appears three times except for one which appears once. Find that single one.

### Examples & Edge Cases
- **Example**: `[2, 2, 3, 2]` → `3`

### Optimal Python Solution
```python
def singleNumber(nums: list[int]) -> int:
    """
    Uses bit counting at each position to find the unique number.
    """
    res = 0
    for i in range(32):
        count = 0
        for num in nums:
            # Count how many numbers have i-th bit set
            if (num >> i) & 1:
                count += 1

        # If count is not divisible by 3, the unique number has this bit set
        if count % 3:
            # Handle sign bit (31st bit) for Python's integers
            if i == 31:
                res -= (1 << i)
            else:
                res |= (1 << i)
    return res
```

### Explanation
We iterate through all 32 possible bit positions. For each position, we count how many numbers in the array have that bit set. If a number appears three times, its bits contribute `3` (or `0`) to the count. The only way the `count % 3` is non-zero is if the unique number (which appears once) has that bit set.

### Complexity Analysis
- **Time Complexity**: O(32 * N) = O(N).
- **Space Complexity**: O(1).

---

## 5. Maximum XOR of Two Numbers in an Array
**Problem Statement**: Given an integer array `nums`, return the maximum result of `nums[i] XOR nums[j]`.

### Examples & Edge Cases
- **Example**: `[3, 10, 5, 25, 2, 8]` → `28`

### Optimal Python Solution
```python
def findMaximumXOR(nums: list[int]) -> int:
    """
    Finds the maximum XOR by building the result bit by bit.
    """
    max_res = 0
    mask = 0
    for i in range(31, -1, -1):
        # Build mask to isolate prefixes
        mask |= (1 << i)
        prefixes = {num & mask for num in nums}

        # Greedy choice: Try to make the i-th bit 1
        candidate = max_res | (1 << i)

        # Check if two prefixes x, y exist such that x ^ y = candidate
        # Using x ^ candidate = y
        for p in prefixes:
            if (p ^ candidate) in prefixes:
                max_res = candidate
                break
    return max_res
```

### Explanation
We greedily try to set each bit of the result to `1`, starting from the most significant bit. For each bit `i`, we collect the prefixes of all numbers up to that bit. We check if there are any two prefixes in our set that XOR to our `candidate` maximum. If such a pair exists, our `candidate` becomes the new `max_res`.

### Complexity Analysis
- **Time Complexity**: O(32 * N) = O(N).
- **Space Complexity**: O(N) to store prefixes.

---

## 6. UTF-8 Validation
**Problem Statement**: Given an integer array `data` representing the data, return whether it is a valid UTF-8 encoding.

### Examples & Edge Cases
- **Example**: `data = [197, 130, 1]` → `true`

### Optimal Python Solution
```python
def validUtf8(data: list[int]) -> bool:
    """
    Validates UTF-8 encoding by checking leading bits.
    """
    n_bytes = 0

    for num in data:
        # We only care about the last 8 bits of each integer
        bin_rep = format(num, '#010b')[-8:]

        if n_bytes == 0:
            # Count how many leading 1s the current byte has
            for bit in bin_rep:
                if bit == '1':
                    n_bytes += 1
                else:
                    break

            # 1-byte character starts with 0
            if n_bytes == 0:
                continue

            # Invalid UTF-8 cases
            if n_bytes == 1 or n_bytes > 4:
                return False
        else:
            # Continuation bytes must start with '10'
            if not (bin_rep[0] == '1' and bin_rep[1] == '0'):
                return False

        # One byte of the character sequence processed
        n_bytes -= 1

    return n_bytes == 0
```

### Explanation
UTF-8 characters are 1 to 4 bytes long. The first byte tells us how many bytes are in the character by the number of leading 1s. Every subsequent byte in that character's sequence must start with the prefix `10`. We maintain a counter `n_bytes` to keep track of how many continuation bytes we are expecting.

### Complexity Analysis
- **Time Complexity**: O(N) where N is the length of `data`.
- **Space Complexity**: O(1) (excluding the `bin_rep` string which is constant length 8).

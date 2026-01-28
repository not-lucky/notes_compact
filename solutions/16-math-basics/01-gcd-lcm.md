# Practice Problems: GCD and LCM

This file contains optimal Python solutions for the practice problems listed in the GCD and LCM notes.

---

## 1. Greatest Common Divisor of Strings

**Problem Statement:**
Given two strings `str1` and `str2`, return the largest string `x` such that `x` divides both `str1` and `str2`. A string `x` divides `s` if `s` is formed by concatenating `x` one or more times.

**Examples & Edge Cases:**

- **Example 1:** `str1 = "ABCABC", str2 = "ABC"` -> Output: `"ABC"`
- **Example 2:** `str1 = "ABABAB", str2 = "ABAB"` -> Output: `"AB"`
- **Example 3:** `str1 = "LEET", str2 = "CODE"` -> Output: `""`
- **Edge Case:** Empty strings (not possible per constraints usually, but return `""`).
- **Edge Case:** One string is much longer than the other but no common divisor exists.

**Optimal Python Solution:**

```python
import math

def gcdOfStrings(str1: str, str2: str) -> str:
    """
    Returns the greatest common divisor string of str1 and str2.
    """
    # Check if a common divisor exists by concatenating in different orders
    if str1 + str2 != str2 + str1:
        return ""

    # The length of the GCD string must be the GCD of the lengths of the two strings
    gcd_len = math.gcd(len(str1), len(str2))
    return str1[:gcd_len]
```

**Explanation:**

1. **Existential Check**: If `str1` and `str2` share a common divisor string `x`, then `str1` is some multiple of `x` (say `n*x`) and `str2` is `m*x`. Thus, `str1 + str2` and `str2 + str1` will both be `(n+m)*x`, making them identical. If `str1 + str2 != str2 + str1`, no such `x` exists.
2. **Length Property**: If they do share a divisor, the largest such divisor must have a length equal to the greatest common divisor of the lengths of `str1` and `str2`.
3. **Extraction**: Simply return the prefix of `str1` with the calculated `gcd_len`.

**Complexity Analysis:**

- **Time Complexity:** $O(n + m)$, where $n$ and $m$ are the lengths of the two strings. String concatenation and comparison take linear time.
- **Space Complexity:** $O(n + m)$ to store the concatenated strings for comparison.

---

## 2. Water and Jug Problem

**Problem Statement:**
You are given two jugs with capacities `jug1Capacity` and `jug2Capacity` liters. There is an infinite amount of water supply available. Determine whether it is possible to measure exactly `targetCapacity` liters using these two jugs.

You can:

- Fill any jug to its full capacity.
- Empty any jug.
- Pour water from one jug into another until the receiving jug is full or the sending jug is empty.

**Examples & Edge Cases:**

- **Example 1:** `jug1 = 3, jug2 = 5, target = 4` -> Output: `True`
- **Example 2:** `jug1 = 2, jug2 = 6, target = 5` -> Output: `False`
- **Edge Case:** `targetCapacity > jug1Capacity + jug2Capacity` -> Output: `False` (cannot hold more than total capacity).
- **Edge Case:** `targetCapacity = 0` -> Output: `True` (already have 0).

**Optimal Python Solution:**

```python
import math

def canMeasureWater(jug1Capacity: int, jug2Capacity: int, targetCapacity: int) -> bool:
    """
    Determines if targetCapacity can be measured using jugs of jug1Capacity and jug2Capacity.
    Uses Bézout's Identity.
    """
    # Total water cannot exceed total capacity
    if targetCapacity > jug1Capacity + jug2Capacity:
        return False

    # If target is 0, it's always possible (empty jugs)
    if targetCapacity == 0:
        return True

    # Target must be a multiple of the GCD of the two jug capacities
    return targetCapacity % math.gcd(jug1Capacity, jug2Capacity) == 0
```

**Explanation:**

1. **Bézout's Identity**: This problem can be modeled as finding integers $a$ and $b$ such that $a \cdot x + b \cdot y = z$, where $x$ and $y$ are jug capacities and $z$ is the target.
2. **Mathematical Condition**: The equation $ax + by = z$ has a solution in integers if and only if $z$ is a multiple of $\gcd(x, y)$.
3. **Physical Constraint**: We also cannot measure more water than the total capacity of both jugs combined, so $z \le x + y$ must hold.

**Complexity Analysis:**

- **Time Complexity:** $O(\log(\min(x, y)))$, which is the time complexity of the Euclidean algorithm for GCD.
- **Space Complexity:** $O(1)$ as we only use a few integer variables.

---

## 3. Ugly Number II

**Problem Statement:**
An ugly number is a positive integer whose prime factors are limited to 2, 3, and 5. Given an integer `n`, return the `n`-th ugly number.

**Examples & Edge Cases:**

- **Example 1:** `n = 10` -> Output: `12` (Ugly numbers: 1, 2, 3, 4, 5, 6, 8, 9, 10, 12)
- **Example 2:** `n = 1` -> Output: `1`
- **Edge Case:** `n` is large (e.g., 1690) -> Requires an efficient $O(n)$ approach.

**Optimal Python Solution:**

```python
def nthUglyNumber(n: int) -> int:
    """
    Finds the n-th ugly number using dynamic programming and three pointers.
    """
    # dp[i] will store the (i+1)-th ugly number
    dp = [0] * n
    dp[0] = 1

    # Pointers for multiples of 2, 3, and 5
    i2 = i3 = i5 = 0

    for i in range(1, n):
        # Calculate next possible ugly numbers
        next2 = dp[i2] * 2
        next3 = dp[i3] * 3
        next5 = dp[i5] * 5

        # Choose the minimum as the next ugly number
        curr_min = min(next2, next3, next5)
        dp[i] = curr_min

        # Increment pointers whose product matches the current minimum
        if curr_min == next2:
            i2 += 1
        if curr_min == next3:
            i3 += 1
        if curr_min == next5:
            i5 += 1

    return dp[-1]
```

**Explanation:**

1. **DP Approach**: We build the sequence of ugly numbers from 1. Every ugly number (except 1) is a multiple of a previous ugly number by 2, 3, or 5.
2. **Three Pointers**: We maintain three pointers (`i2`, `i3`, `i5`) that track the index of the last ugly number used to generate a multiple of 2, 3, and 5 respectively.
3. **Avoid Duplicates**: By using `if` instead of `elif`, we increment multiple pointers if they produce the same value (e.g., $2 \times 3 = 6$ and $3 \times 2 = 6$), preventing duplicates in our `dp` array.

**Complexity Analysis:**

- **Time Complexity:** $O(n)$ because we iterate $n$ times to fill the `dp` array.
- **Space Complexity:** $O(n)$ to store the list of the first $n$ ugly numbers.

---

## 4. Fraction to Recurring Decimal

**Problem Statement:**
Given two integers representing the `numerator` and `denominator` of a fraction, return the fraction in string format. If the fractional part is repeating, enclose the repeating part in parentheses.

**Examples & Edge Cases:**

- **Example 1:** `numerator = 1, denominator = 2` -> Output: `"0.5"`
- **Example 2:** `numerator = 2, denominator = 1` -> Output: `"2"`
- **Example 3:** `numerator = 4, denominator = 333` -> Output: `"0.(012)"`
- **Edge Case:** Negative numbers (e.g., `-50 / 8 = -6.25`).
- **Edge Case:** Numerator is 0.
- **Edge Case:** Large integers that might overflow in other languages (Python handles this).

**Optimal Python Solution:**

```python
def fractionToDecimal(numerator: int, denominator: int) -> str:
    """
    Converts fraction to decimal string, handling recurring parts with parentheses.
    """
    if numerator == 0:
        return "0"

    res = []
    # Handle signs
    if (numerator < 0) ^ (denominator < 0):
        res.append("-")

    num, den = abs(numerator), abs(denominator)

    # Integer part
    res.append(str(num // den))
    remainder = num % den

    if remainder == 0:
        return "".join(res)

    # Fractional part
    res.append(".")
    remainder_map = {}

    while remainder != 0:
        # If remainder is seen before, we found a cycle
        if remainder in remainder_map:
            res.insert(remainder_map[remainder], "(")
            res.append(")")
            break

        # Record the position of this remainder
        remainder_map[remainder] = len(res)

        # Standard long division
        remainder *= 10
        res.append(str(remainder // den))
        remainder %= den

    return "".join(res)
```

**Explanation:**

1. **Sign and Integer Part**: Determine if the result is negative and calculate the part before the decimal point.
2. **Long Division**: Simulate long division for the fractional part.
3. **Cycle Detection**: Use a hash map (`remainder_map`) to store the index where each remainder first appeared. If a remainder repeats, the digits generated from that point onwards will also repeat.
4. **Formatting**: Insert parentheses at the recorded index of the repeated remainder.

**Complexity Analysis:**

- **Time Complexity:** $O(\text{denominator})$ in the worst case, as there are at most `denominator` possible remainders before a cycle starts or the division terminates.
- **Space Complexity:** $O(\text{denominator})$ to store the remainders in the hash map and the resulting digits.

---

## 5. X of a Kind in a Deck of Cards

**Problem Statement:**
In a deck of cards, each card has an integer written on it. Return `True` if and only if you can choose $X \ge 2$ such that you can split the entire deck into 1 or more groups of cards, where:

- Each group has exactly $X$ cards.
- All the cards in each group have the same integer.

**Examples & Edge Cases:**

- **Example 1:** `deck = [1,2,3,4,4,3,2,1]` -> Output: `True` (Groups: `[1,1], [2,2], [3,3], [4,4]`, $X=2$)
- **Example 2:** `deck = [1,1,1,2,2,2,3,3]` -> Output: `False`
- **Edge Case:** `deck = [1]` -> Output: `False` ($X$ must be $\ge 2$).
- **Edge Case:** All cards are the same -> Output: `True` (if deck size $\ge 2$).

**Optimal Python Solution:**

```python
import collections
import math
from functools import reduce

def hasGroupsSizeX(deck: list[int]) -> bool:
    """
    Checks if deck can be partitioned into groups of size X >= 2.
    """
    # Count occurrences of each card
    counts = collections.Counter(deck).values()

    # The common group size X must be a divisor of all counts
    # The largest possible X is the GCD of all counts
    common_gcd = reduce(math.gcd, counts)

    # Condition: X >= 2
    return common_gcd >= 2
```

**Explanation:**

1. **Frequency Counting**: First, count how many times each card appears in the deck.
2. **GCD Logic**: For a valid group size $X$ to exist, $X$ must evenly divide the frequency of every card type present.
3. **Maximum $X$**: The greatest possible $X$ is the GCD of all these frequencies. If this GCD is 2 or greater, we can partition the deck into groups of that size (or any of its prime factors).
4. **Conclusion**: If $\gcd(\text{counts}) \ge 2$, return `True`.

**Complexity Analysis:**

- **Time Complexity:** $O(N + K \log^2(\max\_count))$, where $N$ is the number of cards and $K$ is the number of unique cards. Counting takes $O(N)$, and calculating GCD for $K$ numbers takes $O(K \log^2(\max\_count))$.
- **Space Complexity:** $O(K)$ to store the counts of unique cards in the hash map.

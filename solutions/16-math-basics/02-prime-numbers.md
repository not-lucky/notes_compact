# Practice Problems: Prime Numbers

This file contains optimal Python solutions for the practice problems listed in the Prime Numbers notes.

---

## 1. Count Primes

**Problem Statement:**
Given an integer `n`, return the number of prime numbers that are strictly less than `n`.

**Examples & Edge Cases:**
- **Example 1:** `n = 10` -> Output: `4` (Primes: 2, 3, 5, 7)
- **Example 2:** `n = 0` -> Output: `0`
- **Example 3:** `n = 1` -> Output: `0`
- **Edge Case:** `n` is large (e.g., $5 \times 10^6$) -> Requires $O(n \log \log n)$ time.

**Optimal Python Solution:**
```python
def countPrimes(n: int) -> int:
    """
    Counts primes less than n using the Sieve of Eratosthenes.
    """
    if n < 3:
        return 0

    # Initialize a boolean array 'is_prime'
    is_prime = [True] * n
    is_prime[0] = is_prime[1] = False

    # Mark multiples of primes starting from 2
    for i in range(2, int(n**0.5) + 1):
        if is_prime[i]:
            # Sieve optimization: start marking from i*i
            for j in range(i * i, n, i):
                is_prime[j] = False

    # The number of True values in the array is the prime count
    return sum(is_prime)
```

**Explanation:**
1. **Sieve of Eratosthenes**: This is the most efficient way to find all primes up to $n$.
2. **Elimination**: We start with all numbers marked as prime. Starting from 2, we mark all of its multiples (4, 6, 8...) as non-prime. We repeat this for every prime we encounter.
3. **Optimization**: For a prime $i$, we only need to start marking its multiples from $i^2$, because smaller multiples like $2i, 3i, \dots$ would have already been marked by smaller primes.
4. **Boundary**: We only need to iterate up to $\sqrt{n}$.

**Complexity Analysis:**
- **Time Complexity:** $O(n \log \log n)$. This is a well-known complexity for the Sieve of Eratosthenes.
- **Space Complexity:** $O(n)$ to store the boolean array representing the primality of each number.

---

## 2. Ugly Number

**Problem Statement:**
An ugly number is a positive integer whose prime factors are limited to 2, 3, and 5. Given an integer `n`, return `True` if `n` is an ugly number.

**Examples & Edge Cases:**
- **Example 1:** `n = 6` -> Output: `True` ($6 = 2 \times 3$)
- **Example 2:** `n = 1` -> Output: `True` (1 has no prime factors, vacuously true)
- **Example 3:** `n = 14` -> Output: `False` ($14 = 2 \times 7$, contains prime factor 7)
- **Edge Case:** `n <= 0` -> Output: `False` (ugly numbers must be positive).

**Optimal Python Solution:**
```python
def isUgly(n: int) -> bool:
    """
    Checks if n is an ugly number by dividing out 2, 3, and 5.
    """
    if n <= 0:
        return False

    # Repeatedly divide by 2, 3, and 5
    for p in [2, 3, 5]:
        while n % p == 0:
            n //= p

    # If the remaining number is 1, all prime factors were 2, 3, or 5
    return n == 1
```

**Explanation:**
1. **Factor Removal**: We divide the number $n$ by 2 as many times as possible, then by 3, then by 5.
2. **Termination**: If $n$ was composed solely of these three prime factors, after all divisions, $n$ must be reduced to 1.
3. **Constraint**: If $n \le 0$, it cannot be an ugly number by definition.

**Complexity Analysis:**
- **Time Complexity:** $O(\log n)$. Each division significantly reduces the size of $n$.
- **Space Complexity:** $O(1)$ as we only use a few constant-sized variables.

---

## 3. Ugly Number II

**Problem Statement:**
Given an integer `n`, return the `n`-th ugly number. Ugly numbers are positive integers whose prime factors are limited to 2, 3, and 5.

**Examples & Edge Cases:**
- **Example 1:** `n = 10` -> Output: `12`
- **Edge Case:** `n = 1` -> Output: `1`.

**Optimal Python Solution:**
```python
def nthUglyNumber(n: int) -> int:
    """
    Finds the n-th ugly number using dynamic programming and three pointers.
    """
    dp = [0] * n
    dp[0] = 1
    i2 = i3 = i5 = 0

    for i in range(1, n):
        # Candidates for next ugly number
        m2, m3, m5 = dp[i2] * 2, dp[i3] * 3, dp[i5] * 5

        # Select the minimum candidate
        curr = min(m2, m3, m5)
        dp[i] = curr

        # Advance pointers that produced the minimum value
        if curr == m2: i2 += 1
        if curr == m3: i3 += 1
        if curr == m5: i5 += 1

    return dp[n-1]
```

**Explanation:**
1. **Sequential Generation**: Since we need the $n$-th number in sorted order, we use DP to generate them sequentially.
2. **Min-Selection**: At each step, we look at the smallest multiple of 2, 3, and 5 that we haven't included yet.
3. **Deduplication**: By checking `if` for all three pointers separately, we handle cases where multiple products yield the same value (like $2 \times 3 = 6$ and $3 \times 2 = 6$), incrementing both pointers to avoid duplicates.

**Complexity Analysis:**
- **Time Complexity:** $O(n)$ to iterate through $n$ steps.
- **Space Complexity:** $O(n)$ to store the array of ugly numbers.

---

## 4. Super Ugly Number

**Problem Statement:**
A super ugly number is a positive integer whose prime factors are in the given list of `primes`. Given an integer `n` and a list of integers `primes`, return the `n`-th super ugly number.

**Examples & Edge Cases:**
- **Example 1:** `n = 12, primes = [2,7,13,19]` -> Output: `32`
- **Edge Case:** Large number of primes -> $O(n \times k)$ where $k$ is the number of primes.

**Optimal Python Solution:**
```python
import heapq

def nthSuperUglyNumber(n: int, primes: list[int]) -> int:
    """
    Finds the n-th super ugly number using a min-heap or pointer array.
    """
    ugly = [0] * n
    ugly[0] = 1

    # pointers[j] stores the index in 'ugly' list to multiply primes[j] with
    pointers = [0] * len(primes)
    # next_elements[j] stores the value of ugly[pointers[j]] * primes[j]
    next_elements = [p for p in primes]

    for i in range(1, n):
        # Find the minimum among all next possible ugly numbers
        target = min(next_elements)
        ugly[i] = target

        # Update pointers for all primes that reached the target value
        for j in range(len(primes)):
            if next_elements[j] == target:
                pointers[j] += 1
                next_elements[j] = ugly[pointers[j]] * primes[j]

    return ugly[-1]
```

**Explanation:**
1. **Generalization**: This is a direct generalization of Ugly Number II. Instead of 3 pointers, we use $k$ pointers where $k$ is the length of the `primes` list.
2. **Efficiency**: For each new ugly number, we scan the $k$ possible next candidates.
3. **Pointers**: `pointers[j]` keeps track of which ugly number `primes[j]` should multiply next to generate a potential candidate.

**Complexity Analysis:**
- **Time Complexity:** $O(n \cdot k)$, where $n$ is the target index and $k$ is the number of primes.
- **Space Complexity:** $O(n + k)$ to store the result array and pointer arrays.

---

## 5. Happy Number

**Problem Statement:**
A happy number is defined by replacing the number with the sum of the squares of its digits. Repeat the process. If it eventually reaches 1, it is happy. If it loops endlessly in a cycle that does not include 1, it is not happy.

**Examples & Edge Cases:**
- **Example 1:** `n = 19` -> Output: `True` ($1^2 + 9^2 = 82 \to 8^2 + 2^2 = 68 \to 6^2 + 8^2 = 100 \to 1^2 + 0^2 + 0^2 = 1$).
- **Example 2:** `n = 2` -> Output: `False` (Enter cycle).

**Optimal Python Solution:**
```python
def isHappy(n: int) -> bool:
    """
    Detects if n is a happy number using Floyd's Cycle-Finding Algorithm.
    """
    def get_next(number):
        total_sum = 0
        while number > 0:
            number, digit = divmod(number, 10)
            total_sum += digit ** 2
        return total_sum

    slow = n
    fast = get_next(n)

    # If there's a cycle, fast and slow will eventually meet.
    # If it reaches 1, it's happy.
    while fast != 1 and slow != fast:
        slow = get_next(slow)
        fast = get_next(get_next(fast))

    return fast == 1
```

**Explanation:**
1. **Cycle Detection**: The sequence will either converge to 1 or enter a cycle. We can use Floyd's "Tortoise and Hare" algorithm to detect cycles with constant space.
2. **Transition**: The `get_next` function calculates the sum of squares of digits.
3. **Termination**: If `fast` reaches 1, the number is happy. If `fast` meets `slow` at a value other than 1, it's stuck in a cycle and not happy.

**Complexity Analysis:**
- **Time Complexity:** $O(\log n)$. The number of steps to reach 1 or a cycle is relatively small and related to the number of digits.
- **Space Complexity:** $O(1)$ since we only store two integers (`slow` and `fast`).

---

## 6. Perfect Number

**Problem Statement:**
A perfect number is a positive integer that is equal to the sum of its positive divisors, excluding the number itself. Given an integer `n`, return `True` if `n` is a perfect number.

**Examples & Edge Cases:**
- **Example 1:** `n = 28` -> Output: `True` (Divisors: 1, 2, 4, 7, 14. $1+2+4+7+14 = 28$).
- **Example 2:** `n = 7` -> Output: `False`.
- **Edge Case:** `n = 1` -> Output: `False` (Divisors: none excluding itself).

**Optimal Python Solution:**
```python
def checkPerfectNumber(num: int) -> bool:
    """
    Checks if a number is perfect by summing divisors up to sqrt(num).
    """
    if num <= 1:
        return False

    divisor_sum = 1 # 1 is always a divisor for num > 1

    # Iterate up to sqrt(num)
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0:
            divisor_sum += i
            # If divisors are distinct, add the pair divisor
            if i * i != num:
                divisor_sum += num // i

    return divisor_sum == num
```

**Explanation:**
1. **Divisor Pairs**: If $i$ is a divisor of $n$, then $n/i$ is also a divisor.
2. **Efficiency**: By iterating only up to $\sqrt{n}$, we find all divisor pairs in $O(\sqrt{n})$ time.
3. **Special Case**: We handle 1 separately as its only divisor is itself, and the problem requires divisors *excluding* the number itself.

**Complexity Analysis:**
- **Time Complexity:** $O(\sqrt{n})$.
- **Space Complexity:** $O(1)$.

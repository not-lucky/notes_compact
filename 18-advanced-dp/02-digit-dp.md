# Digit DP

> **Prerequisites:** [09-dynamic-programming](../09-dynamic-programming/README.md), [11-recursion-backtracking](../11-recursion-backtracking/README.md)

## Overview

Digit DP is used to solve problems that ask for the count (or sum) of integers in a range $[L, R]$ that satisfy a specific property. Instead of iterating through every number (which is $O(R)$), we construct the number digit by digit from left to right.

The range $[L, R]$ is usually handled as: `count(R) - count(L - 1)`.

## Building Intuition

Imagine you are filling slots for a number with up to $D$ digits.
- To stay $\le$ the target number $N$, you must keep track of a `tight` constraint.
- If you have already placed a digit smaller than the corresponding digit in $N$, you are no longer constrained (all future digits $0-9$ are valid).
- If you are still matching the prefix of $N$, your next digit can only go up to $N[i]$.

**Common State Variables**:
1.  `index`: Current digit position being filled (left to right).
2.  `is_tight`: Boolean, true if we are restricted by the target number's prefix.
3.  `is_started`: Boolean, true if we have placed a non-zero digit (handles leading zeros).
4.  `custom_state`: Problem-specific (e.g., sum of digits, count of '4's, etc.).

---

## Template

```python
def solve(n_str: str):
    memo = {}

    def dp(idx, is_tight, is_started, custom_val):
        state = (idx, is_tight, is_started, custom_val)
        if state in memo: return memo[state]

        if idx == len(n_str):
            # Return 1 if custom_val satisfies condition, else 0
            return 1 if condition(custom_val) else 0

        res = 0
        # Determine upper bound for current digit
        upper = int(n_str[idx]) if is_tight else 9

        for digit in range(upper + 1):
            new_tight = is_tight and (digit == upper)
            new_started = is_started or (digit > 0)

            # Update custom_val based on digit
            res += dp(idx + 1, new_tight, new_started,
                      update(custom_val, digit, new_started))

        memo[state] = res
        return res

    return dp(0, True, False, initial_val)
```

---

## Problem 1: Number of Digit One (LeetCode 233)

Given an integer $n$, count the total number of digit 1 appearing in all non-negative integers $\le n$.

### Intuition
We fill digits and track how many 1s we've accumulated so far.

### Solution

```python
def count_digit_one(n: int) -> int:
    s = str(n)
    memo = {}

    def dp(idx, is_tight, count):
        state = (idx, is_tight, count)
        if state in memo: return memo[state]

        if idx == len(s):
            return count

        res = 0
        upper = int(s[idx]) if is_tight else 9

        for digit in range(upper + 1):
            new_tight = is_tight and (digit == upper)
            res += dp(idx + 1, new_tight, count + (1 if digit == 1 else 0))

        memo[state] = res
        return res

    return dp(0, True, 0)
```

---

## Problem 2: Numbers At Most N Given Digit Set (LeetCode 902)

Given a sorted set of digits and an integer $n$, find how many positive integers can be generated using these digits that are $\le n$.

### Intuition
We can have numbers with fewer digits than $n$, or numbers with the same number of digits. The `is_started` flag is crucial here because we can only pick digits from our set once we've "started" the number.

### Solution

```python
def at_most_n_given_digit_set(digits: list[str], n: int) -> int:
    s = str(n)
    digit_set = set(map(int, digits))
    memo = {}

    def dp(idx, is_tight, is_started):
        state = (idx, is_tight, is_started)
        if state in memo: return memo[state]

        if idx == len(s):
            return 1 if is_started else 0

        res = 0
        # Choice 1: Skip current digit (if not started)
        if not is_started:
            res += dp(idx + 1, False, False)

        # Choice 2: Pick a digit from the set
        upper = int(s[idx]) if is_tight else 9
        for d in digit_set:
            if d <= upper:
                res += dp(idx + 1, is_tight and (d == upper), True)

        memo[state] = res
        return res

    return dp(0, True, False)
```

---

## Summary Checklist

- [ ] Use `count(R) - count(L-1)` for range queries.
- [ ] Convert the number to a string for easy indexing.
- [ ] Maintain `is_tight` to stay within range.
- [ ] Maintain `is_started` (or `is_leading_zero`) if 0 is special or number length matters.
- [ ] Use memoization to avoid redundant subproblems.

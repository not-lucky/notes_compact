# Itertools Module

> **Prerequisites:** Basic Python knowledge

## Building Intuition

### Why Does itertools Exist?

Generating combinations, permutations, and products is tedious and error-prone. `itertools` provides these as lazy iterators - they generate values on-demand, not all at once in memory.

**The core insight**: Many brute-force solutions require "try all combinations" or "try all orderings." `itertools` makes this a one-liner, letting you focus on the filtering logic.

### The Combinatorial Zoo

Here's the key distinction between the main functions:

```
Given [A, B, C], choose 2:

permutations: Order matters, no replacement
  → (A,B), (A,C), (B,A), (B,C), (C,A), (C,B)  [6 results]

combinations: Order doesn't matter, no replacement
  → (A,B), (A,C), (B,C)                        [3 results]

combinations_with_replacement: Order doesn't matter, replacement allowed
  → (A,A), (A,B), (A,C), (B,B), (B,C), (C,C)   [6 results]

product: All combinations of choices (Cartesian product)
  product([A,B], [1,2]) → (A,1), (A,2), (B,1), (B,2)
```

### Visual Mental Model

**Permutations** - "Arrange people in a line"
```
3 people, 3 positions: 3! = 6 ways
┌─┐┌─┐┌─┐
│A││B││C│  ABC, ACB, BAC, BCA, CAB, CBA
└─┘└─┘└─┘
```

**Combinations** - "Choose a committee"
```
3 people, pick 2: C(3,2) = 3 ways
Who's on the team, not who sits where
{A,B}, {A,C}, {B,C}
```

**Product** - "Menu choices"
```
Entree: [pasta, steak]
Side:   [salad, soup]

All meals: (pasta,salad), (pasta,soup), (steak,salad), (steak,soup)
```

### Why Lazy Iterators?

`permutations(range(10))` generates 3,628,800 items. Loading all into memory is wasteful if you only need to find one that satisfies a condition.

```python
# Memory-efficient: stops at first match
for p in permutations(range(10)):
    if is_valid(p):
        print(p)
        break  # Didn't generate all 3.6M permutations!

# Memory-wasteful: generates everything
all_perms = list(permutations(range(10)))  # Uses ~300MB
```

## When NOT to Use

### Avoid itertools when:
- **Output is huge and you'll consume it all**: `list(permutations(range(12)))` is 479 million items - you'll run out of memory
- **A mathematical formula exists**: Don't generate all permutations just to count them (use `math.factorial`)
- **Smarter algorithms exist**: Don't brute-force when DP or greedy works

### Common mistakes:
```python
# WRONG: Converting to list unnecessarily
all_combos = list(combinations(range(20), 10))  # 184,756 items in memory
for c in all_combos:  # Should iterate directly!
    process(c)

# CORRECT: Iterate directly
for c in combinations(range(20), 10):
    process(c)

# WRONG: Forgetting iterators are consumed
perms = permutations([1, 2, 3])
list(perms)  # [(1,2,3), (1,3,2), ...]
list(perms)  # [] - empty! Iterator exhausted

# CORRECT: Create new iterator or store in list
perms_list = list(permutations([1, 2, 3]))  # Reusable

# WRONG: groupby on unsorted data
data = [1, 2, 1, 2]
for k, g in groupby(data):
    print(k, list(g))
# 1 [1]
# 2 [2]
# 1 [1]  <- Not merged!
# 2 [2]

# CORRECT: Sort first for full grouping
for k, g in groupby(sorted(data)):
    print(k, list(g))
# 1 [1, 1]
# 2 [2, 2]
```

### Performance considerations:
- **n matters a lot**: `permutations(range(10))` = 3.6M items, `permutations(range(13))` = 6.2 billion
- **Use early termination**: `any()`, `all()`, or explicit `break` when you find what you need
- **Consider backtracking**: For constrained problems, backtracking prunes invalid paths earlier than filtering all permutations

---

## Interview Context

The `itertools` module provides efficient iterators for combinatorial tasks. Essential for:

- **Permutations/Combinations**: Generate all arrangements
- **Cartesian product**: Generate all combinations of choices
- **Grouping**: Group consecutive equal elements
- **Infinite iterators**: Count, cycle, repeat

---

## Combinatorial Iterators

### Permutations

All possible orderings (order matters).

```python
from itertools import permutations

# All permutations of length 3
list(permutations([1, 2, 3]))
# [(1,2,3), (1,3,2), (2,1,3), (2,3,1), (3,1,2), (3,2,1)]

# Permutations of length 2
list(permutations([1, 2, 3], 2))
# [(1,2), (1,3), (2,1), (2,3), (3,1), (3,2)]

# String permutations
list(permutations("abc"))
# [('a','b','c'), ('a','c','b'), ...]

# Count: n! / (n-r)! = n! for r=n
# permutations([1,2,3]) = 3! = 6
# permutations([1,2,3], 2) = 3! / 1! = 6
```

### Combinations

All ways to choose k items (order doesn't matter).

```python
from itertools import combinations

# Choose 2 from 4
list(combinations([1, 2, 3, 4], 2))
# [(1,2), (1,3), (1,4), (2,3), (2,4), (3,4)]

# Choose 3 from 4
list(combinations([1, 2, 3, 4], 3))
# [(1,2,3), (1,2,4), (1,3,4), (2,3,4)]

# Choose all (k = n)
list(combinations([1, 2, 3], 3))
# [(1, 2, 3)]

# Count: C(n, k) = n! / (k! * (n-k)!)
# combinations([1,2,3,4], 2) = 4! / (2! * 2!) = 6
```

### Combinations with Replacement

Allow repeated elements.

```python
from itertools import combinations_with_replacement

# Choose 2 with repetition allowed
list(combinations_with_replacement([1, 2, 3], 2))
# [(1,1), (1,2), (1,3), (2,2), (2,3), (3,3)]

# Useful for: coin change, dice rolls with same values
```

### Product (Cartesian Product)

All combinations of elements from multiple iterables.

```python
from itertools import product

# Two lists
list(product([1, 2], ['a', 'b']))
# [(1,'a'), (1,'b'), (2,'a'), (2,'b')]

# Self-product (repeat)
list(product([0, 1], repeat=3))
# All 3-bit binary numbers:
# [(0,0,0), (0,0,1), (0,1,0), (0,1,1), (1,0,0), (1,0,1), (1,1,0), (1,1,1)]

# Multiple ranges
list(product(range(2), range(3)))
# [(0,0), (0,1), (0,2), (1,0), (1,1), (1,2)]

# Equivalent nested loops:
# for i in range(2):
#     for j in range(3):
#         print((i, j))
```

---

## Interview Patterns

### Generate All Subsets

```python
from itertools import combinations

def subsets(nums: list[int]) -> list[list[int]]:
    """Generate all subsets (power set)."""
    result = []
    for k in range(len(nums) + 1):
        for combo in combinations(nums, k):
            result.append(list(combo))
    return result

print(subsets([1, 2, 3]))
# [[], [1], [2], [3], [1,2], [1,3], [2,3], [1,2,3]]
```

### Generate All Permutations

```python
from itertools import permutations

def permute(nums: list[int]) -> list[list[int]]:
    """Generate all permutations."""
    return [list(p) for p in permutations(nums)]

print(permute([1, 2, 3]))
# [[1,2,3], [1,3,2], [2,1,3], [2,3,1], [3,1,2], [3,2,1]]
```

### Letter Combinations of Phone Number

```python
from itertools import product

def letter_combinations(digits: str) -> list[str]:
    """Generate all letter combinations for phone number."""
    if not digits:
        return []

    phone = {
        '2': 'abc', '3': 'def', '4': 'ghi', '5': 'jkl',
        '6': 'mno', '7': 'pqrs', '8': 'tuv', '9': 'wxyz'
    }

    letters = [phone[d] for d in digits]
    return [''.join(combo) for combo in product(*letters)]

print(letter_combinations("23"))
# ['ad', 'ae', 'af', 'bd', 'be', 'bf', 'cd', 'ce', 'cf']
```

---

## Infinite Iterators

### count

```python
from itertools import count

# Count from 0
for i in count():
    if i > 5:
        break
    print(i)  # 0, 1, 2, 3, 4, 5

# Count from start with step
for i in count(10, 2):  # 10, 12, 14, ...
    if i > 16:
        break
    print(i)

# Useful with zip
list(zip(count(), ['a', 'b', 'c']))
# [(0, 'a'), (1, 'b'), (2, 'c')]
```

### cycle

```python
from itertools import cycle

# Repeat infinitely
colors = cycle(['red', 'green', 'blue'])
for i in range(7):
    print(next(colors))
# red, green, blue, red, green, blue, red

# Useful for round-robin
def round_robin(items, n):
    it = cycle(items)
    return [next(it) for _ in range(n)]

print(round_robin([1, 2, 3], 7))  # [1, 2, 3, 1, 2, 3, 1]
```

### repeat

```python
from itertools import repeat

# Repeat value n times
list(repeat(5, 3))  # [5, 5, 5]

# Infinite repeat (use with zip)
list(zip(repeat('x'), range(3)))
# [('x', 0), ('x', 1), ('x', 2)]

# Useful with map
list(map(pow, range(5), repeat(2)))
# [0, 1, 4, 9, 16] - each number squared
```

---

## Grouping Iterators

### groupby

Groups consecutive equal elements.

```python
from itertools import groupby

# Basic grouping
data = [1, 1, 2, 2, 2, 3, 1, 1]
for key, group in groupby(data):
    print(key, list(group))
# 1 [1, 1]
# 2 [2, 2, 2]
# 3 [3]
# 1 [1, 1]  <- Note: 1s not merged!

# IMPORTANT: groupby only groups CONSECUTIVE elements!
# For full grouping, sort first:
data = [1, 1, 2, 2, 2, 3, 1, 1]
for key, group in groupby(sorted(data)):
    print(key, list(group))
# 1 [1, 1, 1, 1]
# 2 [2, 2, 2]
# 3 [3]

# With key function
words = ['apple', 'ant', 'banana', 'bat', 'cat']
for key, group in groupby(sorted(words), key=lambda x: x[0]):
    print(key, list(group))
# a ['ant', 'apple']
# b ['banana', 'bat']
# c ['cat']
```

### Run-Length Encoding

```python
from itertools import groupby

def run_length_encode(s: str) -> list[tuple[str, int]]:
    """Encode consecutive repeated characters."""
    return [(char, len(list(group))) for char, group in groupby(s)]

print(run_length_encode("aaabbbcc"))
# [('a', 3), ('b', 3), ('c', 2)]

def run_length_decode(encoded: list[tuple[str, int]]) -> str:
    """Decode run-length encoding."""
    return ''.join(char * count for char, count in encoded)

print(run_length_decode([('a', 3), ('b', 3), ('c', 2)]))
# 'aaabbbcc'
```

---

## Filtering Iterators

### filterfalse

```python
from itertools import filterfalse

# Keep elements where predicate is False
list(filterfalse(lambda x: x % 2, range(10)))
# [0, 2, 4, 6, 8] - even numbers (not odd)

# Opposite of filter()
list(filter(lambda x: x % 2, range(10)))
# [1, 3, 5, 7, 9] - odd numbers
```

### takewhile / dropwhile

```python
from itertools import takewhile, dropwhile

# Take while condition is True
list(takewhile(lambda x: x < 5, [1, 3, 5, 2, 4]))
# [1, 3] - stops at first 5

# Drop while condition is True
list(dropwhile(lambda x: x < 5, [1, 3, 5, 2, 4]))
# [5, 2, 4] - starts from first 5
```

### compress

```python
from itertools import compress

# Select elements where selector is True
list(compress('ABCDEF', [1, 0, 1, 0, 1, 1]))
# ['A', 'C', 'E', 'F']
```

---

## Accumulating Iterators

### accumulate

```python
from itertools import accumulate
import operator

# Running sum (default)
list(accumulate([1, 2, 3, 4, 5]))
# [1, 3, 6, 10, 15]

# Running product
list(accumulate([1, 2, 3, 4, 5], operator.mul))
# [1, 2, 6, 24, 120]

# Running max
list(accumulate([3, 1, 4, 1, 5, 9, 2, 6], max))
# [3, 3, 4, 4, 5, 9, 9, 9]

# Running min
list(accumulate([3, 1, 4, 1, 5, 9, 2, 6], min))
# [3, 1, 1, 1, 1, 1, 1, 1]

# Custom function
list(accumulate([1, 2, 3], lambda a, b: a + 2*b))
# [1, 5, 11] - 1, 1+2*2=5, 5+2*3=11
```

---

## Chain Iterators

### chain

```python
from itertools import chain

# Combine multiple iterables
list(chain([1, 2], [3, 4], [5]))
# [1, 2, 3, 4, 5]

# Flatten list of lists
lists = [[1, 2], [3, 4], [5, 6]]
list(chain.from_iterable(lists))
# [1, 2, 3, 4, 5, 6]

# Alternative to nested loops
list(chain.from_iterable(combinations([1, 2, 3], r) for r in range(4)))
# All subsets!
```

### zip_longest

```python
from itertools import zip_longest

# Zip with fill value
list(zip_longest([1, 2, 3], ['a', 'b'], fillvalue='?'))
# [(1, 'a'), (2, 'b'), (3, '?')]

# Compare to regular zip (stops at shortest)
list(zip([1, 2, 3], ['a', 'b']))
# [(1, 'a'), (2, 'b')]
```

---

## Complexity Summary

| Function | Time | Notes |
|----------|------|-------|
| permutations(n, r) | O(n!/(n-r)!) | All orderings |
| combinations(n, r) | O(C(n,r)) | All subsets of size r |
| product(*iterables) | O(∏len) | Cartesian product |
| groupby | O(n) | Single pass |
| accumulate | O(n) | Single pass |

---

## Common Mistakes

1. **groupby requires sorted input**: Only groups consecutive elements
2. **Iterators are consumed**: Can only iterate once
3. **Large outputs**: permutations(10) = 3,628,800 items
4. **Memory with list()**: Use directly in loops instead

```python
# Bad: Creates huge list
all_perms = list(permutations(range(10)))  # 3.6M items!

# Good: Iterate directly
for p in permutations(range(10)):
    process(p)
    if condition:
        break
```

---

## Practice Problems

| # | Problem | Function |
|---|---------|----------|
| 1 | Subsets | combinations |
| 2 | Permutations | permutations |
| 3 | Letter Combinations | product |
| 4 | Combination Sum | combinations_with_replacement |
| 5 | Generate Parentheses | Custom with product |
| 6 | Count and Say | groupby |
| 7 | Running Sum | accumulate |

---

## Related Sections

- [Collections Module](./01-collections-module.md) - Counter for counting
- [Common Gotchas](./05-common-gotchas.md) - Iterator consumption

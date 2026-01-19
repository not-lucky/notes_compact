# Big-O Notation Fundamentals

> **Prerequisites:** None - this is where it all begins

## Interview Context

Big-O notation is the language of algorithm efficiency. In every FANG+ interview, you'll use it to:

- Describe your solution's efficiency before coding
- Compare different approaches
- Respond to "Can you do better?" prompts

Interviewers don't expect you to derive mathematical proofs—they want you to quickly and correctly identify complexity classes.

---

## What is Big-O?

Big-O describes the **upper bound** of an algorithm's growth rate as input size increases. It answers: "In the worst case, how does the runtime/space grow as n gets large?"

### Key Insight

Big-O ignores constants and lower-order terms because they become irrelevant at scale:

```
O(2n + 5) → O(n)
O(n² + n) → O(n²)
O(100) → O(1)
```

We care about **how it scales**, not the exact count.

---

## Common Complexity Classes

### O(1) - Constant Time

Runtime doesn't change with input size.

```python
def get_first(arr: list[int]) -> int:
    """
    Time: O(1) - single operation regardless of array size
    """
    return arr[0] if arr else None

def hash_lookup(d: dict, key: str) -> int:
    """
    Time: O(1) average - hash table direct access
    """
    return d.get(key)
```

**Examples**: Array indexing, hash table lookup, stack push/pop

---

### O(log n) - Logarithmic Time

Runtime grows logarithmically—doubling input adds constant work.

```python
def binary_search(arr: list[int], target: int) -> int:
    """
    Time: O(log n) - halving search space each iteration
    """
    left, right = 0, len(arr) - 1

    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return -1
```

**Why log n?** Each step eliminates half the remaining elements. For n=1,000,000 elements, binary search takes at most ~20 steps (log₂(1,000,000) ≈ 20).

**Examples**: Binary search, balanced BST operations, finding digits in a number

---

### O(n) - Linear Time

Runtime grows linearly with input size.

```python
def find_max(arr: list[int]) -> int:
    """
    Time: O(n) - must check each element once
    """
    if not arr:
        return None

    max_val = arr[0]
    for num in arr:
        max_val = max(max_val, num)
    return max_val

def has_target(arr: list[int], target: int) -> bool:
    """
    Time: O(n) - worst case: target at end or not present
    """
    for num in arr:
        if num == target:
            return True
    return False
```

**Examples**: Linear search, traversing array/linked list, counting elements

---

### O(n log n) - Linearithmic Time

Common in efficient sorting algorithms.

```python
def merge_sort(arr: list[int]) -> list[int]:
    """
    Time: O(n log n)
    - log n levels of recursion (halving each time)
    - n work at each level (merging)
    """
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])

    return merge(left, right)

def merge(left: list[int], right: list[int]) -> list[int]:
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])
    return result
```

**Examples**: Merge sort, heap sort, quicksort (average case), many divide-and-conquer algorithms

---

### O(n²) - Quadratic Time

Runtime grows with the square of input size. Usually indicates nested loops.

```python
def has_duplicate_naive(arr: list[int]) -> bool:
    """
    Time: O(n²) - comparing every pair
    """
    n = len(arr)
    for i in range(n):
        for j in range(i + 1, n):
            if arr[i] == arr[j]:
                return True
    return False

def bubble_sort(arr: list[int]) -> list[int]:
    """
    Time: O(n²) - n passes, each pass does n comparisons
    """
    n = len(arr)
    for i in range(n):
        for j in range(n - 1 - i):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr
```

**Examples**: Nested loops over same input, bubble/insertion/selection sort, brute force pair checking

---

### O(2ⁿ) - Exponential Time

Runtime doubles with each additional input element.

```python
def fibonacci_naive(n: int) -> int:
    """
    Time: O(2^n) - each call spawns two more calls
    """
    if n <= 1:
        return n
    return fibonacci_naive(n - 1) + fibonacci_naive(n - 2)

def all_subsets(nums: list[int]) -> list[list[int]]:
    """
    Time: O(2^n) - there are 2^n possible subsets
    """
    result = [[]]
    for num in nums:
        result += [subset + [num] for subset in result]
    return result
```

**Examples**: Recursive Fibonacci (without memoization), generating all subsets, brute force subset sum

---

### O(n!) - Factorial Time

The worst common complexity. Grows astronomically fast.

```python
def all_permutations(nums: list[int]) -> list[list[int]]:
    """
    Time: O(n!) - n choices for first, n-1 for second, etc.
    """
    if len(nums) <= 1:
        return [nums[:]]

    result = []
    for i in range(len(nums)):
        rest = nums[:i] + nums[i+1:]
        for perm in all_permutations(rest):
            result.append([nums[i]] + perm)
    return result
```

**Examples**: Generating all permutations, brute force traveling salesman

---

## Complexity Comparison Chart

For n = 1,000:

| Complexity | Operations | Practical? |
|------------|------------|------------|
| O(1) | 1 | ✓ Instant |
| O(log n) | 10 | ✓ Instant |
| O(n) | 1,000 | ✓ Fast |
| O(n log n) | 10,000 | ✓ Fast |
| O(n²) | 1,000,000 | ✓ Acceptable |
| O(2ⁿ) | 10^301 | ✗ Impossible |
| O(n!) | 10^2567 | ✗ Impossible |

For n = 1,000,000:

| Complexity | Operations | Practical? |
|------------|------------|------------|
| O(1) | 1 | ✓ Instant |
| O(log n) | 20 | ✓ Instant |
| O(n) | 1,000,000 | ✓ Fast |
| O(n log n) | 20,000,000 | ✓ Acceptable |
| O(n²) | 10^12 | ⚠ Very slow |
| O(2ⁿ) | ∞ | ✗ Impossible |

---

## Visual Growth Comparison

```
Operations
    |
    |                                      O(n²)
    |                                  ****
    |                              ****
    |                          ****
    |                      ****        O(n log n)
    |                  ****      ------
    |              ****    ------
    |          ****  ------            O(n)
    |      ****------              --------
    |  ****--- O(log n)       --------
    |**---..................--------
    +-----|-----|-----|-----|-----> n
          10    20    30    40
```

---

## Rules for Determining Big-O

### Rule 1: Drop Constants

```python
# Both are O(n)
for i in range(n):       # O(n)
    pass

for i in range(2 * n):   # O(2n) → O(n)
    pass
```

### Rule 2: Drop Lower-Order Terms

```python
# This is O(n²), not O(n² + n)
for i in range(n):           # O(n)
    for j in range(n):       # × O(n) = O(n²)
        pass

for i in range(n):           # + O(n)
    pass
# Total: O(n² + n) → O(n²)
```

### Rule 3: Different Inputs, Different Variables

```python
def process(arr1: list, arr2: list):
    """
    Time: O(a + b), NOT O(n)
    Use different variables for different inputs.
    """
    for x in arr1:    # O(a) where a = len(arr1)
        pass
    for y in arr2:    # O(b) where b = len(arr2)
        pass
```

### Rule 4: Add Steps, Multiply Nested

```python
# Sequential = ADD
for x in arr:    # O(n)
    pass
for y in arr:    # O(n)
    pass
# Total: O(n) + O(n) = O(2n) → O(n)

# Nested = MULTIPLY
for x in arr:          # O(n)
    for y in arr:      #   × O(n)
        pass
# Total: O(n) × O(n) = O(n²)
```

---

## Common Mistakes

### Mistake 1: Nested Loop ≠ Always O(n²)

```python
# This is O(n), not O(n²)
def two_pointer(arr: list[int]) -> int:
    left, right = 0, len(arr) - 1
    while left < right:  # Each element visited at most once
        left += 1  # or right -= 1
    # Total operations: n, not n²
```

### Mistake 2: Ignoring Hidden Loops

```python
# This is O(n²), not O(n)
for i in range(n):
    if target in arr:  # 'in' is O(n) for lists!
        pass
# Total: O(n) × O(n) = O(n²)
```

### Mistake 3: String Concatenation

```python
# This is O(n²), not O(n)
s = ""
for char in chars:     # O(n) iterations
    s += char          # Each += creates new string: O(current length)
# Total: 1 + 2 + 3 + ... + n = O(n²)

# Fixed: O(n)
s = "".join(chars)  # Join is O(n) total
```

---

## Practice: Identify the Complexity

Try to identify the time complexity before checking answers.

```python
# Problem 1
def mystery1(n):
    for i in range(n):
        for j in range(i):
            pass
```

<details>
<summary>Answer 1</summary>

O(n²). The inner loop runs 0 + 1 + 2 + ... + (n-1) = n(n-1)/2 times.
</details>

```python
# Problem 2
def mystery2(n):
    i = n
    while i > 0:
        i //= 2
```

<details>
<summary>Answer 2</summary>

O(log n). We're halving i each iteration.
</details>

```python
# Problem 3
def mystery3(arr):
    result = []
    for x in arr:
        if x not in result:
            result.append(x)
    return result
```

<details>
<summary>Answer 3</summary>

O(n²). The `in` check on a list is O(n), done n times.
</details>

---

## Practice Problems

| # | Problem | Difficulty | Focus |
|---|---------|------------|-------|
| 1 | Analyze nested loop patterns | Easy | Basic analysis |
| 2 | Compare two approaches | Easy | Trade-off thinking |
| 3 | Identify hidden complexity | Medium | String/list operations |
| 4 | Recursion tree analysis | Medium | Exponential vs polynomial |

---

## Key Takeaways

1. **Big-O describes growth rate**, not exact operations
2. **Drop constants and lower-order terms**
3. **Use different variables for different inputs**
4. **Add sequential steps, multiply nested steps**
5. **Watch for hidden O(n) operations** (list `in`, string `+`)

---

## Next: [02-time-complexity.md](./02-time-complexity.md)

Deep dive into analyzing loops, recursion, and nested structures.

# Binary Search Template

> **Prerequisites:** Basic array knowledge, understanding of $O(\log n)$ complexity

## Interview Context

Binary search is one of the most fundamental algorithms, yet one of the most frequently failed in interviews. Donald Knuth famously noted that while the first binary search was published in 1946, the first published binary search without bugs did not appear until 1962.

Interviewers test:
1. **Implementation accuracy**: Can you write bug-free binary search on the first try? (Off-by-one errors and infinite loops are lethal).
2. **Variant recognition**: Can you identify that a problem requires binary search even when there's no explicitly sorted array?
3. **Boundary conditions**: Do you know when to use `<` vs `<=`, or `mid` vs `mid + 1`?
4. **Search Space Reduction**: Can you define a monotonic boolean function to search over a range of answers (Binary Search on Answer)?

---

## Building Intuition: The Monotonic Property

**Why does binary search work?**

Binary search doesn't just require "sorted data"—it requires a **monotonic property**. This is any condition that transitions from `False` $\rightarrow$ `True` (or `True` $\rightarrow$ `False`) exactly once.

```text
Index:     [0] [1] [2] [3] [4] [5] [6]
Condition: [F] [F] [F] [T] [T] [T] [T]
                       ↑
        Binary search finds this boundary
```

**Mental Model: The Boolean Divide**
Imagine evaluating a condition on your search space. Everything before some point evaluates to `False`, and everything from that point onward evaluates to `True`. Binary search finds where the boundary changes—in $O(\log n)$ time.

**Why Halving Works**:
1. Pick the middle element `mid`.
2. Evaluate the condition at `mid`.
3. If `True`: the transition boundary is at or before `mid` $\rightarrow$ discard the right half.
4. If `False`: the transition boundary is after `mid` $\rightarrow$ discard the left half.
5. Each step halves the search space: $n \rightarrow n/2 \rightarrow n/4 \rightarrow ... \rightarrow 1$.

This gives exactly $\lfloor \log_2(n) \rfloor + 1$ steps.

**The "Sorted Array" is just a Special Case**
When searching for a target in a sorted array:
- Condition = `nums[mid] >= target`
- The condition transitions from `False` $\rightarrow$ `True` at the first occurrence of the target.

---

## The Three Core Templates

Mastering binary search means mastering how to adjust your search space boundaries. While there are many ways to write binary search, sticking to these standard templates minimizes bugs.

### Template 1: Find Exact Match (Standard)

Used when searching for a specific target value. **You can stop early if you find it.**

```python
def binary_search(nums: list[int], target: int) -> int:
    """
    Find target in sorted array. Returns index or -1 if not found.
    Time: O(log n) | Space: O(1)
    """
    left, right = 0, len(nums) - 1

    # Loop condition: <= because the search space is [left, right] inclusive
    while left <= right:
        # Prevent integer overflow (crucial in C++/Java, in Python 3 integers have arbitrary precision)
        mid = left + (right - left) // 2

        if nums[mid] == target:
            return mid          # Found exact match, exit immediately
        elif nums[mid] < target:
            left = mid + 1      # Discard left half (nums[mid] is too small)
        else:
            right = mid - 1     # Discard right half (nums[mid] is too large)

    return -1
```

**Key Signatures:**
- Initial bounds: `left = 0`, `right = len(nums) - 1`.
- Loop condition: `left <= right` (Runs even when `left == right` to check the last element).
- Early exit: `return mid` inside the loop.
- Boundary updates: `left = mid + 1` and `right = mid - 1`.

---

### Template 2: Find Left Boundary (First Occurrence / Insertion Point)

Used when finding the **first** position where a condition becomes true (e.g., first occurrence of duplicates, or where to insert an element). **You cannot stop early.**

This is the most versatile and robust template. It maintains the invariant that the answer is always within the `[left, right]` range.

```python
def find_left_boundary(nums: list[int], target: int) -> int:
    """
    Find first occurrence of target or the insertion point (bisect_left).
    Returns the leftmost index where nums[i] >= target.
    """
    # Note: right = len(nums), NOT len(nums) - 1.
    # Target might need to be inserted at the very end.
    left, right = 0, len(nums)

    while left < right:  # Terminate when left == right
        # Prevent integer overflow (crucial in C++/Java, in Python 3 integers have arbitrary precision)
        mid = left + (right - left) // 2

        if nums[mid] < target:
            left = mid + 1      # Mid is strictly less than target, answer must be to the right
        else:
            right = mid         # Mid is >= target. It COULD be the answer, so keep it in search space

    # At the end of the loop, left == right.
    return left
```

**Key Signatures:**
- Initial bounds: `left = 0`, `right = len(nums)` (The possible answers are `0` through `len(nums)`).
- Loop condition: `left < right` (terminates exactly when `left == right`, leaving one unambiguous answer).
- Boundary updates: `left = mid + 1` and `right = mid` (Never `right = mid - 1`, because `mid` might be the answer).
- Return `left` (or `right`, they are equal).

*Note: If you specifically need to know if the target exists, you check `if left < len(nums) and nums[left] == target` after the loop.*

---

### Template 3: Find Right Boundary (Last Occurrence)

Used when finding the **last** position where a condition is true (e.g., the last occurrence of a target).

Similar to Template 2, but the logic is mirrored.

```python
def find_right_boundary(nums: list[int], target: int) -> int:
    """
    Find the last occurrence of a target.
    Returns the rightmost index where nums[i] == target.
    """
    if not nums:
        return -1

    left, right = 0, len(nums) - 1

    while left < right:
        # CRITICAL: When using left = mid, we must bias mid to the RIGHT
        # by adding 1, otherwise we get infinite loops when left == right - 1
        mid = left + (right - left + 1) // 2

        if nums[mid] > target:
            right = mid - 1     # Mid is strictly greater than target, answer must be to the left
        else:
            left = mid          # Mid is <= target. It COULD be the answer, so keep it in search space

    # At the end of the loop, left == right
    return left if nums[left] == target else -1
```

**Key Signatures:**
- Loop condition: `left < right`.
- Mid calculation: **`mid = left + (right - left + 1) // 2`** (Rounds up).
- Boundary updates: `left = mid` and `right = mid - 1`.

---

## Visual Walkthrough: Left vs Right Boundary

Target = `5` in `[1, 2, 3, 5, 5, 5, 8, 9]`

**Left boundary (finds first 5 using `bisect_left` template):**
```text
[1, 2, 3, 5, 5, 5, 8, 9] (len=8)
 L           M           R   (left=0, right=8) mid=4 (0+(8-0)//2 = 4), nums[4]=5 >= 5 -> right=mid=4
 L     M     R               (left=0, right=4) mid=2 (0+(4-0)//2 = 2), nums[2]=3 < 5  -> left=mid+1=3
          LM R               (left=3, right=4) mid=3 (3+(4-3)//2 = 3), nums[3]=5 >= 5 -> right=mid=3
          LR                 (left=3, right=3) left==right, loop terminates. Return 3.
```

**Right boundary (finds last 5 using Template 3):**
```text
[1, 2, 3, 5, 5, 5, 8, 9] (len=8)
 L           M        R      (left=0, right=7) mid=4 (0+(7-0+1)//2 = 4), nums[4]=5 <= 5 -> left=mid=4
             L     M  R      (left=4, right=7) mid=6 (4+(7-4+1)//2 = 6), nums[6]=8 > 5  -> right=mid-1=5
             LM R            (left=4, right=5) mid=5 (4+(5-4+1)//2 = 5), nums[5]=5 <= 5 -> left=mid=5
                LR           (left=5, right=5) left==right, loop terminates. Return 5.
```

---

## Python's `bisect` Module

In a Python interview, clarify if you can use the standard library. If yes, `bisect` is incredibly powerful and handles the `left < right` logic perfectly.

```python
import bisect

nums = [1, 2, 3, 5, 5, 5, 8, 9]

# bisect_left: Find leftmost insertion point
# Returns the index of the FIRST element >= target
bisect.bisect_left(nums, 5)   # Returns 3

# bisect_right: Find rightmost insertion point
# Returns the index of the FIRST element > target
bisect.bisect_right(nums, 5)  # Returns 6

# bisect is an alias for bisect_right
bisect.bisect(nums, 5)        # Returns 6
```

**Building exact lookups using `bisect`:**
```python
def first_occurrence(nums: list[int], target: int) -> int:
    idx = bisect.bisect_left(nums, target)
    # Check if target is actually at the found index
    if idx < len(nums) and nums[idx] == target:
        return idx
    return -1

def last_occurrence(nums: list[int], target: int) -> int:
    # bisect_right gives the index of the first element strictly > target
    # The last occurrence of target will be immediately before this index
    idx = bisect.bisect_right(nums, target) - 1
    # Check if target is actually at the preceding index
    if idx >= 0 and nums[idx] == target:
        return idx
    return -1
```

---

## Advanced: Binary Search on Answer

This is the **most frequently tested FANG binary search pattern**.
The array isn't sorted, but the *answer space* is monotonic.

**Pattern:**
You need to find a minimum or maximum value that satisfies a certain condition.
1. Define the search space: `[min_possible_answer, max_possible_answer]`.
2. Define a helper function: `is_valid(guess) -> bool` that runs in $O(N)$.
3. Use binary search (Template 2) to find the boundary where `is_valid` flips.

**Example Conceptual Problem:** "Koko Eating Bananas" (Find minimum eating speed $k$).
- If $k=1$, it takes too long (`is_valid(1) == False`).
- If $k=100$, she finishes in time (`is_valid(100) == True`).
- If she can finish at speed $k$, she can *definitely* finish at speed $k+1$.
- The condition `is_valid(k)` is monotonic: `[F, F, F, T, T, T]`.
- We want to find the **first** `True` (Left Boundary).

```python
def solve(params):
    # Search space: possible answers for k
    left, right = min_possible_k, max_possible_k

    while left < right:
        # Prevent integer overflow
        mid = left + (right - left) // 2

        if is_valid(mid, params):
            # mid works, but can we find a SMALLER valid k?
            # keep mid in the search space
            right = mid
        else:
            # mid is too small, must be strictly larger
            left = mid + 1

    return left # or right, they are equal
```

Total Time Complexity: $O(N \log M)$ where $N$ is array size and $M$ is the answer space size (`max_ans - min_ans`).

---

## Avoiding Common Bugs

### 1. Integer Overflow
```python
# Wrong (can overflow in C++/Java if left + right > 2^31 - 1)
mid = (left + right) // 2

# Correct (prevents overflow in C++/Java, equivalent in Python)
# Note: Python 3 uses arbitrary-precision integers, so overflow does not happen.
# However, this is still the standard way to write binary search and shows interviewers
# you understand memory constraints in other languages.
mid = left + (right - left) // 2
```

### 2. Infinite Loops
Occurs when `left == right - 1` and the search space doesn't shrink.
```python
# DANGER: Infinite loop if left = 0, right = 1 and we do:
mid = left + (right - left) // 2  # mid = 0
if condition:
    left = mid   # left remains 0 forever! Search space [0, 1] never shrinks.

# The Golden Rule to prevent infinite loops:
# If you use `left = mid`, your mid calculation MUST round up:
# mid = left + (right - left + 1) // 2

# If you use `right = mid`, your mid calculation MUST round down (default):
# mid = left + (right - left) // 2
```

### 3. Edge Cases Checklist
- [ ] Empty array (`if not nums: return ...`)
- [ ] Array with 1 element (walk through it manually)
- [ ] Target is smaller than the 0th element
- [ ] Target is larger than the last element
- [ ] Array size is even vs. odd (does your mid calculation handle both correctly?)
- [ ] Duplicates in the array (Do you need first, last, or any?)

---

## When NOT to Use Binary Search

Binary search is powerful but has specific requirements. Watch out for these traps:

1. **Unsorted Data Without a Monotonic Property**
   - e.g. `[3, 1, 4, 1, 5]`. If you evaluate `nums[mid] >= 4`, it's `[False, False, True, False, True]`. There is no single transition point.

2. **When You Need ALL Occurrences (and there are many)**
   - If a target appears $K$ times, finding all of them takes $O(\log N + K)$. If $K \approx N$ (e.g., an array of all `5`s), this degrades to $O(N)$. Just use a linear scan.

3. **Linked Lists**
   - Binary search requires $O(1)$ random access. Reaching the middle of a linked list takes $O(N)$. Binary search on a linked list is $O(N \log N)$—worse than an $O(N)$ linear scan!

4. **Dynamic Data (Frequent Inserts/Deletes)**
   - Inserting into a sorted array takes $O(N)$. If you are constantly adding elements and then searching, your overall time is dominated by the $O(N)$ inserts. Use a Balanced BST (like `SortedList` in Python) or a Hash Map instead.

---

## Practice Problems

| Problem | Type | Key Insight |
|---------|------|-------------|
| [Binary Search](https://leetcode.com/problems/binary-search/) | Template 1 | Standard Exact Match |
| [Search Insert Position](https://leetcode.com/problems/search-insert-position/) | Template 2 | `bisect_left` pattern |
| [Find First and Last Position](https://leetcode.com/problems/find-first-and-last-position-of-element-in-sorted-array/) | Template 2/3 | Left and Right boundaries |
| [Sqrt(x)](https://leetcode.com/problems/sqrtx/) | Search Space | Binary Search on Answer `[1, x//2]` |
| [Koko Eating Bananas](https://leetcode.com/problems/koko-eating-bananas/) | Search Space | Monotonic boolean function over `[1, max(piles)]` |
| [Find Peak Element](https://leetcode.com/problems/find-peak-element/) | Unsorted BS | Look at slope `nums[mid] < nums[mid+1]` |

---

## Next: [02-first-last-occurrence.md](./02-first-last-occurrence.md)

Deep dive into the problem of finding boundaries in sorted arrays.
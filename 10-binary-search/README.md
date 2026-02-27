# Chapter 10: Binary Search

Binary search is one of the most heavily tested algorithms in FANG+ interviews, appearing in roughly 20% of all algorithmic coding rounds. While candidates often brush it off as a simple "find $x$ in a sorted array" problem, top-tier companies rarely test the basic version. Instead, they use binary search to evaluate your ability to identify hidden monotonicity, design optimization boundaries, and—most importantly—write bug-free boundary logic without falling into infinite loops or off-by-one errors.

Mastering binary search means moving beyond the basic `left <= right` template and understanding how to construct a custom `condition(mid)` function to search abstract "answer spaces."

---

## Why Binary Search Matters

1. **The $O(\log N)$ Imperative**: In a FANG interview, if a problem specifies $O(\log N)$ time complexity or deals with an already sorted dataset, binary search is almost certainly required.
2. **Abstract Optimization**: Binary search isn't just for arrays. It's the primary tool for solving "find the minimum capacity" or "find the maximum days" optimization problems (Binary Search on Answer).
3. **Extreme Edge-Case Testing**: Binary search exposes sloppy coding. Interviewers love it because it immediately reveals whether a candidate can cleanly handle $+1/-1$ boundaries and track search spaces accurately without relying on trial-and-error debugging.

---

## The Core Insight: Monotonicity

Binary search works on any search space that exhibits a **monotonic property**.

You do *not* need a sorted array of numbers. You only need a space where, if you apply a boolean condition, the results look like this:
`[False, False, False, True, True, True]` or `[True, True, True, False, False, False]`

**The Goal**: Find the exact boundary—the *first* `True` or the *last* `False`.

If you can define a `condition(mid)` that evaluates to `False` for the first half of your search space and `True` for the second half, you can use binary search to find the transition point in $O(\log(\text{range}))$ time.

---

## The Three FANG Templates

Many candidates struggle because they try to force every problem into a single binary search template. To succeed in FANG interviews, you need to understand the **three core templates** and exactly when to use them.

### Template 1: `left <= right` (Find Exact Match)

Use this when you are searching for a specific target and can terminate early if you find it. This is the classic textbook template.

- **Loop Condition**: `while left <= right:`
- **Mid Calculation**: `mid = left + (right - left) // 2` (Prevents integer overflow in C++/Java, though Python handles arbitrarily large integers automatically).
- **Updates**: `left = mid + 1`, `right = mid - 1`
- **Post-Loop**: `left` will be `right + 1`. The loop ends when `left > right`.

```python
def binary_search_exact(nums: list[int], target: int) -> int:
    left, right = 0, len(nums) - 1

    while left <= right:
        mid = left + (right - left) // 2

        if nums[mid] == target:
            return mid  # Found exact match
        elif nums[mid] < target:
            left = mid + 1  # Target must be strictly to the right
        else:
            right = mid - 1 # Target must be strictly to the left

    return -1  # Target not found
```

### Template 2: `left < right` (Find Boundary / First True)

Use this when you are searching for a boundary (e.g., the *first* element that satisfies a condition) and you *cannot* or *do not want to* terminate early. This is the most important template for **Binary Search on Answer Space** and **Boundary Finding**.

- **Loop Condition**: `while left < right:`
- **Mid Calculation**: `mid = left + (right - left) // 2` (Biased left, naturally handles `left = mid + 1` updates).
- **Updates**: `right = mid` (Keep `mid` in search space as it might be the answer), `left = mid + 1` (Exclude `mid` as it's definitely not the answer).
- **Post-Loop**: `left == right`. You have narrowed down the search space to exactly one element. You must check if this single element actually satisfies the condition (post-processing).

```python
from typing import Callable

def binary_search_first_true(left: int, right: int, condition: Callable[[int], bool]) -> int:
    # Example: Finding the FIRST occurrence or FIRST valid answer
    # Boolean array looks like: [False, False, True, True, True]

    # Store the original bounds in case no element satisfies the condition
    # For binary search on an array, right would normally be len(nums) - 1
    # For binary search on answer space, it would be the max possible answer
    original_right = right

    while left < right:
        mid = left + (right - left) // 2

        if condition(mid):
            # mid satisfies the condition, so it could be the first True
            # The answer is at mid or to the left of mid
            right = mid
        else:
            # mid does NOT satisfy the condition
            # The answer must be strictly to the right of mid
            left = mid + 1

    # After loop, left == right. Check if the element actually satisfies the condition.
    # If the original right bound didn't satisfy it, then none did.
    return left if condition(left) else -1
```

> **Warning:** If you need to find the *last* `True` (e.g., `[True, True, False]`), you must **bias `mid` to the right**: `mid = left + (right - left + 1) // 2`.
> If you don't do this, and your logic is `left = mid` and `right = mid - 1`, the loop will run infinitely when the search space is exactly 2 elements (e.g., `left + 1 == right`)!

### Template 3: `left + 1 < right` (Compare with Neighbors / Open Boundary)

Use this when you need to safely access `mid - 1` or `mid + 1` inside the loop without going out of bounds, or when the problem doesn't easily map to the first two templates. Great for **Peak Finding** or heavily rotated array problems.

- **Loop Condition**: `while left + 1 < right:` (Loop exits when 2 elements remain).
- **Mid Calculation**: `mid = left + (right - left) // 2`
- **Updates**: `left = mid` or `right = mid` (No `+ 1` or `- 1` needed).
- **Post-Loop**: You are left with two adjacent elements (`left` and `right`). You must check both manually in post-processing.

```python
def find_peak_element(nums: list[int]) -> int:
    if not nums:
        return -1
    if len(nums) == 1:
        return 0

    left, right = 0, len(nums) - 1

    while left + 1 < right:
        mid = left + (right - left) // 2

        # Compare mid with its right neighbor safely
        if nums[mid] < nums[mid + 1]:
            # Peak must be strictly to the right
            left = mid
        else:
            # Peak must be at mid or to the left
            right = mid

    # Post-processing: check which of the remaining two elements is the peak
    # (Since we're looking for ANY peak, we just pick the larger one)
    return left if nums[left] >= nums[right] else right
```

---

## FANG Favorite: Binary Search on Answer Space

This is the most common "Hard" or tricky "Medium" pattern at Google, Amazon, and Meta.

Instead of searching an index in an array, you search a range of possible *answers* (e.g., from $1$ to $\text{max\_val}$). For each mid-point, you run a feasibility function to check: "Is it possible to achieve the goal with this value?"

**The Pattern:**
1. Identify the absolute minimum possible answer (`left`).
2. Identify the absolute maximum possible answer (`right`).
3. Create a `can_achieve(mid)` function that returns a boolean `True` or `False`. This function should establish a monotonic boundary.
4. Use **Template 2** (`left < right`) to find the exact transition boundary.

**Classic Example:** *Koko Eating Bananas*.
- **Problem**: Koko loves to eat bananas. There are `n` piles of bananas, the `i`th pile has `piles[i]` bananas. The guards have gone and will come back in `h` hours. Find the minimum integer eating speed `k` such that she can eat all the bananas within `h` hours.
- `left = 1` (Minimum eating speed is 1 banana/hour).
- `right = max(piles)` (Maximum useful eating speed; eating faster than the largest pile doesn't save any more time since she only eats one pile per hour).
- `can_achieve(speed)` iterates through `piles` in $O(N)$ time to see if the total time taken $\le h$.
- Since we want the *minimum* speed, we use Template 2 to find the first `True` condition.

---

## Time and Space Complexity

| Operation / Pattern | Time Complexity | Space Complexity |
| :--- | :--- | :--- |
| Classic Binary Search | $O(\log N)$ | $O(1)$ iterative, $O(\log N)$ recursive |
| Search in 2D Matrix | $O(\log(M \cdot N))$ | $O(1)$ |
| Binary Search on Answer Space | $O(\text{cost} \cdot \log(\text{Range}))$* | $O(1)$ auxiliary |
| Find Peak / Rotated Minimum | $O(\log N)$ | $O(1)$ |

*\*Where $\text{cost}$ is the time complexity of the feasibility check function `can_achieve(mid)` (usually $O(N)$).*

---

## Common Interview Pitfalls

1. **Integer Overflow:** While Python automatically scales integers making `(left + right) // 2` perfectly safe, FANG interviewers often code in strongly-typed languages like C++, Java, or Go. ALWAYS write `left + (right - left) // 2` to demonstrate your understanding of memory limits and integer overflow.
2. **Infinite Loops (The Deadliest Trap):**
   - Typically occurs in Template 2 when `left` and `right` are adjacent (e.g., `left=3, right=4`).
   - `mid` calculates to `3` (due to integer truncation). If your logic branches to an update of `left = mid`, then `left` remains `3`. The search space didn't shrink, and the loop never terminates.
   - *The Fix:* Ensure the search space ALWAYS shrinks. If your logic requires `left = mid`, you **must** bias `mid` to the right: `mid = left + (right - left + 1) // 2`.
3. **Off-By-One Errors:** Confusing whether you want `left = mid` vs `left = mid + 1` (or `right = mid` vs `right = mid - 1`).
   - *The Fix:* Ask yourself: "Can `mid` possibly be the final answer?"
     - If **yes**, you must include it in the remaining search space (`left = mid` or `right = mid`).
     - If **no** (because it definitely fails the condition), you can safely exclude it (`left = mid + 1` or `right = mid - 1`).

---

## Quick Reference: Algorithm Selection Flowchart

```text
Is the dataset sorted or mostly sorted (e.g., rotated)?
    │
    ├── Yes → Do you need to find an exact element, a boundary, or an insertion point?
    │         │
    │         ├── Yes → Use standard Binary Search (Templates 1 or 2).
    │         │
    │         └── No → Consider Two Pointers (e.g., finding pairs that sum to target).
    │
    └── No → Is the problem asking to find a "minimum max" or "maximum min"?
             │ (e.g., minimize the maximum load, maximize the minimum distance)
             │
             ├── Yes → Binary Search on Answer Space (Google/Amazon favorite).
             │         1. Define the search space [min_ans, max_ans].
             │         2. Write an O(N) `is_valid(mid)` function.
             │         3. Use Template 2.
             │
             └── No → Does the problem have a monotonic property or local peaks?
                      │
                      ├── Yes → Binary Search works (e.g., Find Peak Element using Template 3).
                      │
                      └── No → Binary search won't work. Consider Two Pointers,
                               DP, Sliding Window, or Sorting first.
```

---

## Chapter Contents

| # | Topic | Key Concepts |
| :--- | :--- | :--- |
| 01 | [Binary Search Template](./01-binary-search-template.md) | Standard templates, iterative vs recursive, boundary logic |
| 02 | [First/Last Occurrence](./02-first-last-occurrence.md) | Boundary finding, handling duplicates, `bisect` module |
| 03 | [Search Rotated Array](./03-search-rotated-array.md) | Finding sorted halves, nested conditions, monotonicity |
| 04 | [Find Minimum Rotated](./04-find-minimum-rotated.md) | Minimum in rotated arrays, monotonic checks, template 2/3 |
| 05 | [Peak Element](./05-peak-element.md) | Local optimization, comparing with neighbors, template 3 |
| 06 | [Search Space](./06-search-space.md) | **Crucial:** Binary search on answer space, Koko, capacity |
| 07 | [Matrix Search](./07-matrix-search.md) | Flattening 2D arrays, stair-step search, $O(M+N)$ optimization |
| 08 | [Median Two Arrays](./08-median-two-arrays.md) | Partitioning two sorted arrays, $O(\log(\min(M, N)))$ |

---

## Start Here: [01-binary-search-template.md](./01-binary-search-template.md)

Begin by solidifying your mastery of the exact templates.
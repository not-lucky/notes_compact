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
- **Mid Calculation**: `mid = left + (right - left) // 2`
- **Updates**: `left = mid + 1`, `right = mid - 1`
- **Post-Loop**: `left` will be `right + 1`.

```python
def binary_search_exact(nums: list[int], target: int) -> int:
    left, right = 0, len(nums) - 1

    while left <= right:
        mid = left + (right - left) // 2

        if nums[mid] == target:
            return mid  # Found exact match
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return -1  # Target not found
```

### Template 2: `left < right` (Find Boundary / First True)

Use this when you are searching for a boundary (e.g., the *first* element that satisfies a condition) and you *cannot* terminate early. This is the most important template for **Binary Search on Answer** and **Boundary Finding**.

- **Loop Condition**: `while left < right:`
- **Mid Calculation**: `mid = left + (right - left) // 2` (Biased left)
- **Updates**: `right = mid` (Keep `mid` as it might be the answer), `left = mid + 1`
- **Post-Loop**: `left == right`. No need to decide which to return.

```python
from typing import Callable

def binary_search_first_true(left: int, right: int, condition: Callable[[int], bool]) -> int:
    # Example: Finding the FIRST occurrence or FIRST valid answer
    # Boolean array looks like: [False, False, True, True, True]

    while left < right:
        mid = left + (right - left) // 2

        if condition(mid):
            right = mid  # mid might be the first True, keep it in the search space
        else:
            left = mid + 1 # mid is False, answer must be strictly to the right

    # After loop, left == right. Check if the element actually satisfies the condition
    return left if condition(left) else -1
```

> **Warning:** If you use `left < right` to find the *last* `True` (e.g., `[True, True, False]`), you must bias `mid` to the right: `mid = left + (right - left + 1) // 2`. If you don't, `left` and `right` can get stuck infinitely when `left + 1 == right`!

### Template 3: `left + 1 < right` (Compare with Neighbors)

Use this when you need to access `mid - 1` or `mid + 1` inside the loop without going out of bounds. Great for **Peak Finding** or heavily rotated array problems.

- **Loop Condition**: `while left + 1 < right:`
- **Mid Calculation**: `mid = left + (right - left) // 2`
- **Updates**: `left = mid` or `right = mid`
- **Post-Loop**: You are left with two elements (`left` and `right`). You must check both manually.

```python
def binary_search_neighbors(nums: list[int]) -> int:
    if not nums: return -1

    left, right = 0, len(nums) - 1

    while left + 1 < right:
        mid = left + (right - left) // 2

        # Condition logic here. Example: checking peak
        if nums[mid] > nums[mid - 1]:
            left = mid
        else:
            right = mid

    # Post-processing: manually check the remaining two elements
    if condition(left): return left
    if condition(right): return right
    return -1
```

---

## FANG Favorite: Binary Search on Answer Space

This is the most common "Hard" or tricky "Medium" pattern at Google, Amazon, and Meta.

Instead of searching an array, you search a range of possible *answers* (e.g., $1$ to $\text{max\_val}$). For each mid-point, you run a feasibility function to check: "Is it possible to achieve the goal with this value?"

**The Pattern:**
1. Identify the absolute minimum possible answer (`left`).
2. Identify the absolute maximum possible answer (`right`).
3. Create a `can_achieve(k)` function that returns `True` or `False`.
4. Use **Template 2** (`left < right`) to find the boundary.

**Classic Example:** *Koko Eating Bananas*.
`left` = 1 (minimum eating speed)
`right` = max(piles) (maximum useful eating speed)
`can_achieve(speed)` iterates through piles in $O(N)$ to see if total time $\le H$.

---

## Time and Space Complexity

| Operation / Pattern | Time Complexity | Space Complexity |
| :--- | :--- | :--- |
| Classic Binary Search | $O(\log N)$ | $O(1)$ iterative, $O(\log N)$ recursive |
| Search in 2D Matrix | $O(\log(M \cdot N))$ | $O(1)$ |
| Binary Search on Answer Space | $O(\log(\text{Range}) \cdot O(\text{cost}))$* | $O(1)$ auxiliary |
| Find Peak / Rotated Minimum | $O(\log N)$ | $O(1)$ |

*\* Where $O(\text{cost})$ is the time complexity of the feasibility check function `condition(mid)` (usually $O(N)$).*

---

## Common Interview Pitfalls

1. **Integer Overflow:** In Python, integers automatically scale, so `(left + right) // 2` is safe. However, FANG interviewers often code in C++, Java, or Go. ALWAYS write `left + (right - left) // 2` to show you understand overflow limits.
2. **Infinite Loops:**
   - Occurs when `left` and `right` are adjacent (e.g., `left=3, right=4`).
   - `mid` calculates to `3`. If your logic updates `left = mid`, then `left` remains `3`. The loop never terminates.
   - *Fix:* Ensure search space ALWAYS shrinks. If `left = mid` is possible, bias `mid` to the right: `mid = left + (right - left + 1) // 2`.
3. **Off-By-One Indexing:** Confusing whether you want `left = mid` vs `left = mid + 1`. Ask yourself: "Can `mid` possibly be the final answer?" If yes, include it (`left/right = mid`). If no, exclude it (`mid +/- 1`).

---

## Quick Reference: Algorithm Selection Flowchart

```text
Is the data already sorted?
    │
    ├── Yes → Do you need to find an element, boundary, or insertion point?
    │         │
    │         └── Yes → Use standard Binary Search Templates.
    │
    └── No → Is the problem asking for a "minimum max" or "maximum min"?
              │ (e.g., minimize the maximum load, maximize the minimum distance)
              │
              ├── Yes → Binary Search on Answer Space (Google/Amazon favorite).
              │         1. Define the range [min_ans, max_ans].
              │         2. Write an O(N) `is_valid(mid)` function.
              │
              └── No → Can you define a boolean condition that is monotonic?
                       │
                       ├── Yes → Binary Search for the boundary.
                       │
                       └── No → Binary search won't work. Consider Two Pointers,
                                DP, Sliding Window, or Sorting first.
```

---

## Chapter Contents

| # | Topic | Key Concepts |
| :--- | :--- | :--- |
| 01 | [Binary Search Template](./01-binary-search-template.md) | Standard templates, iterative vs recursive |
| 02 | [First/Last Occurrence](./02-first-last-occurrence.md) | Boundary finding, handling duplicates |
| 03 | [Search Rotated Array](./03-search-rotated-array.md) | Finding sorted halves, nested conditions |
| 04 | [Find Minimum Rotated](./04-find-minimum-rotated.md) | Minimum in rotated arrays, monotonic checks |
| 05 | [Peak Element](./05-peak-element.md) | Local optimization, comparing with neighbors |
| 06 | [Search Space](./06-search-space.md) | **Crucial:** Binary search on answer space |
| 07 | [Matrix Search](./07-matrix-search.md) | Flattening 2D arrays, stair-step search |
| 08 | [Median Two Arrays](./08-median-two-arrays.md) | Partitioning two sorted arrays, $O(\log(\min(M, N)))$ |

---

## Start: [01-binary-search-template.md](./01-binary-search-template.md)

Begin by solidifying your mastery of the exact templates.
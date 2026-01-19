# Chapter 10: Binary Search

Binary Search is a foundational algorithm that appears frequently in FANG+ interviews. Beyond simple array lookups, it's used to search on abstract "answer spaces" for optimization problems.

## Why Binary Search Matters

1. **Interview frequency**: Binary search variants appear in ~20% of coding interviews
2. **Efficiency indicator**: Shows understanding of O(log n) vs O(n) optimization
3. **Versatility**: Applies to arrays, answer spaces, and optimization problems
4. **Edge case handling**: Tests attention to detail with off-by-one errors

---

## The Core Insight

Binary search works when the search space has a **monotonic property**:
- If condition is true at position `mid`, it's true for all positions to one side
- If condition is false at position `mid`, it's false for all positions to the other side

---

## Binary Search Patterns Overview

| Pattern | Problems | Key Insight |
|---------|----------|-------------|
| Classic Search | Find target | Standard template |
| Boundary Finding | First/last occurrence | Search for transition point |
| Rotated Array | Search rotated sorted | Identify sorted half |
| Peak Finding | Find peak element | Compare with neighbors |
| Answer Space | Capacity problems | Binary search on answer |
| Matrix Search | 2D matrix | Treat as 1D or use rows/cols |

---

## Chapter Contents

| # | Topic | Key Concepts |
|---|-------|--------------|
| 01 | [Binary Search Template](./01-binary-search-template.md) | Standard templates, variants |
| 02 | [First/Last Occurrence](./02-first-last-occurrence.md) | Boundary finding |
| 03 | [Search Rotated Array](./03-search-rotated-array.md) | Rotated sorted arrays |
| 04 | [Find Minimum Rotated](./04-find-minimum-rotated.md) | Minimum in rotated array |
| 05 | [Peak Element](./05-peak-element.md) | Finding peaks in arrays |
| 06 | [Search Space](./06-search-space.md) | Binary search on answer |
| 07 | [Matrix Search](./07-matrix-search.md) | 2D matrix search patterns |
| 08 | [Median Two Arrays](./08-median-two-arrays.md) | Median of sorted arrays |

---

## The Two Templates

### Template 1: Standard (find exact match)

```python
def binary_search(nums: list[int], target: int) -> int:
    left, right = 0, len(nums) - 1

    while left <= right:
        mid = left + (right - left) // 2

        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return -1
```

### Template 2: Boundary (find transition point)

```python
def find_boundary(nums: list[int], target: int) -> int:
    left, right = 0, len(nums) - 1
    result = -1

    while left <= right:
        mid = left + (right - left) // 2

        if condition(nums[mid]):
            result = mid
            right = mid - 1  # or left = mid + 1
        else:
            left = mid + 1   # or right = mid - 1

    return result
```

---

## Common Mistakes

1. **Integer overflow**: Use `left + (right - left) // 2` not `(left + right) // 2`
2. **Infinite loops**: Check that `left` and `right` always converge
3. **Off-by-one**: Know whether to include `mid` in next search range
4. **Wrong condition**: Ensure the monotonic property holds
5. **Edge cases**: Empty array, single element, target not found

---

## Time Complexity

| Operation | Time | Space |
|-----------|------|-------|
| Binary Search | O(log n) | O(1) |
| Binary Search (recursive) | O(log n) | O(log n) |
| Search in Matrix | O(log(m×n)) | O(1) |
| Search Space | O(log(range) × cost) | O(1) |

---

## Common Interview Problems by Company

| Company | Favorite Binary Search Problems |
|---------|-------------------------------|
| Google | Koko Eating Bananas, Median Two Arrays |
| Meta | Search Rotated Array, Peak Element |
| Amazon | Capacity to Ship, Find Minimum Rotated |
| Microsoft | Search 2D Matrix, First Bad Version |
| Apple | First/Last Position, Square Root |

---

## Quick Reference: When to Use Binary Search

```
Is the search space sorted or has monotonic property?
    │
    ├── Yes → Can I eliminate half at each step?
    │         │
    │         ├── Yes → Use Binary Search
    │         │
    │         └── No → Consider other approaches
    │
    └── No → Can I define a condition that's monotonic?
              │
              ├── Yes → Binary search on answer space
              │
              └── No → Linear search or other methods
```

---

## Start: [01-binary-search-template.md](./01-binary-search-template.md)

Begin with mastering the fundamental binary search templates.

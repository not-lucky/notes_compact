# Improve Merge K Sorted Lists note

- [x] Analyze `05-merge-k-sorted.md`
- [x] Fix the bug in `smallest_range` where it didn't heapify and checked `heap[0][0]` prematurely. Changed it to iterative push with initial max tracking.
- [x] Improve Divide & Conquer code to be truly `O(1)` auxiliary space (in-place iterative approach) instead of creating new lists in each round.
- [x] Update the Comparison of Approaches table to reflect the true `O(1)` space of the improved Divide & Conquer method.
- [x] Clarify `N` (total elements) vs `k` (number of lists) everywhere, changing `n` to `N` for clarity.
- [x] Improve tiebreaker explanation to include the Wrapper Class approach (very common Object-Oriented follow up).
- [x] Polish edge case phrasing and explanation of external merge sort for disk-based files.
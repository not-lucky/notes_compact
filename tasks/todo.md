# Plan: Improve 10-binary-search/03-search-rotated-array.md

- [x] 1. Fix Approach 2 two-pass method. The first pass to find the minimum element has a bug: the target element logic and the way the array is split after finding the pivot needs to be verified and explained more clearly. Also, the `search_via_pivot` function is generally considered worse than one-pass by many interviewers because it traverses the array twice (even though it's 2 * log N = log N).
- [x] 2. Fix the duplicate handling in the `search_with_duplicates` approach. The current code has a bug where it might skip the target if `nums[left] == target` or `nums[right] == target` before shrinking.
- [x] 3. Enhance explanations of "One Sorted Half" rule and visual walk-throughs.
- [x] 4. Check for edge cases and ensure the implementation is robust (e.g., array length 1, 2).
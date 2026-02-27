# Plan: Improve Binary Search Template Notes

- [ ] 1. Analyze 10-binary-search/01-binary-search-template.md for correctness, clarity, and code readability
- [x] 2. Fix bug in Template 3 (right boundary): condition `left < len(nums)` is redundant since `left` starts at `0` and goes up to `len(nums) - 1`.
- [x] 3. Improve explanations for integer overflow, clarifying Python 3 vs C++/Java behavior.
- [x] 4. Check `bisect` section and fix any ambiguities.
- [ ] 5. Improve explanations of the "Binary Search on Answer" pattern.
- [ ] 6. Ensure mathematical notation is correctly formatted and visually consistent.

# Plan: Improve 10-binary-search/02-first-last-occurrence.md

- [ ] 1. Review and fix the `find_first` implementation. The current `left = mid + 1` logic is okay but let's make sure it strictly follows the templates defined in `01-binary-search-template.md`.
- [ ] 2. Review and fix the `find_last` implementation. The `mid = left + (right - left + 1) // 2` logic is correct for template 3, but let's ensure the explanation is solid and the code is perfectly clean.
- [ ] 3. Fix the `search_range_bisect` Python code.
- [ ] 4. Review `singleNonDuplicate` and `nextGreatestLetter` problems. Ensure the code and explanations are correct and robust. `singleNonDuplicate` explanation is slightly confusing; `nums[mid] == nums[mid ^ 1]` is a neat trick but maybe too clever for a basic explanation without a simpler version first.
- [ ] 5. Improve markdown formatting, flow, and clarity of the explanations.
# Plan: Improve Peak Element notes

- [x] Analyze the current notes for correctness, clarity, and code readability
- [x] Review Leetcode 162 `find_peak_element` implementation
- [x] Review Leetcode 852 `peak_index_in_mountain_array` implementation
- [x] Review Leetcode 1095 `findInMountainArray` implementation
- [x] Review Leetcode 1901 `findPeakGrid` implementation
- [x] Improve explanations of the intuition and mental models
- [x] Update code snippets to be consistent with the standard binary search template, or clearly explain why the alternative template (`left < right`) is used for this specific problem
- [x] Fix formatting and structure issues

## Review
The `10-binary-search/05-peak-element.md` file was improved.
- Analyzed the notes for correctness, clarity, and code readability
- Improved intuition, fixing up the mountain analogy and explanations.
- Emphasized that this problem intentionally uses the `left < right` loop condition (Template 2) to avoid an out-of-bounds error when calculating `nums[mid + 1]`.
- Re-verified implementation for 1095 Find in Mountain Array. Updated to use the binary search template.
- Found an issue in the 1901 Find a Peak Element II time complexity description and corrected it to $O(n \log m)$ or $O(m \log n)$ depending on rows vs columns. Fixed an implementation issue.
- Standardized formatting across the file.

# Plan: Improve 10-binary-search/02-first-last-occurrence.md

- [x] 1. Review and fix the `find_first` implementation. The current `left = mid + 1` logic is okay but let's make sure it strictly follows the templates defined in `01-binary-search-template.md`.
- [x] 2. Review and fix the `find_last` implementation. The `mid = left + (right - left + 1) // 2` logic is correct for template 3, but let's ensure the explanation is solid and the code is perfectly clean.
- [x] 3. Fix the `search_range_bisect` Python code.
- [x] 4. Review `singleNonDuplicate` and `nextGreatestLetter` problems. Ensure the code and explanations are correct and robust. `singleNonDuplicate` explanation is slightly confusing; `nums[mid] == nums[mid ^ 1]` is a neat trick but maybe too clever for a basic explanation without a simpler version first.
- [x] 5. Improve markdown formatting, flow, and clarity of the explanations.

## Review
The `10-binary-search/02-first-last-occurrence.md` file was improved.
- Fixed `find_first` template alignment, including right boundary initialization check and integer overflow comment
- Fixed `find_last` to mention integer overflow and strictly use Template 3
- Fixed a bug in `search_range_bisect` where checking `right_idx > 0` before subtracting `1` was implicitly guaranteed but missing a comment
- Clarified `singleNonDuplicate` condition with `nums[mid] == nums[mid ^ 1]` trick.
- Updated `nextGreatestLetter` to clearly map to Template 2.
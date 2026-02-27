# Plan: Improve 2D DP Basics notes

- [ ] Analyze the current notes for correctness, clarity, and code readability
- [ ] Review Leetcode 62 `uniquePaths` implementation
- [ ] Review Leetcode 63 `uniquePathsWithObstacles` implementation
- [ ] Review Leetcode 64 `minPathSum` implementation
- [ ] Review Leetcode 120 `minimumTotal` (Triangle) implementation
- [ ] Review Leetcode 221 `maximalSquare` implementation
- [ ] Review Leetcode 174 `calculateMinimumHP` (Dungeon Game) implementation
- [ ] Review Leetcode 741 `cherryPickup` implementation
- [ ] Ensure explanation of space optimization logic is clear and accurate
- [ ] Fix formatting and structure issues

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
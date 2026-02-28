# Chapter 09: Dynamic Programming Notes Review and Improvement Plan

## 13-word-break.md
- [x] Read and analyze `09-dynamic-programming/13-word-break.md`.
- [x] Ensure formatting consistency.
- [x] Make the DP recurrence explanation cleaner.
- [x] Clarify the time complexity explanation in Tabulation (string slicing `O(n)`).

## 14-regex-matching.md
- [x] Read and analyze `09-dynamic-programming/14-regex-matching.md`.
- [x] Improve readability of the 2D DP Recurrence relation.
- [x] Standardize the time/space complexity notation ($O(m \times n)$ instead of $O(M \times N)$).
- [x] Ensure consistent heading styles.

## Final Review
- [ ] Ensure consistent tone and formatting across files.
- [ ] Add summary review to this file.

### Summary Review:
- **01-dp-fundamentals.md:** Corrected variable casing $O(N) \to O(n)$ for consistency. Standardized headings. Fixed typos and improved explanations for `Constraints` and `@functools.lru_cache` usage in interviews.
- **02-memoization-vs-tabulation.md:** Corrected variable casing $O(N) \to O(n)$ and $M \times N \to m \times n$. Added "Chapter 09:" to the title. Improved the explanation for boundary conditions under the pitfalls section.
- **07-2d-dp-basics.md:** Made python code standard with snake case variable names. Rewrote Visual sections using nice ascii boxes. Fixed boundary cases with finding max and padding.
- **08-longest-common-subsequence.md:** Fixed some markdown formatting for inline code blocks. Made some ascii box visualizations. Standardized variable names. Added next link to edit distance.
- **13-word-break.md:** Updated python style casing, improved markdown structure, formatting. Rewrote time complexity to properly explain strings slicing logic. Fixed some notation issues.
- **14-regex-matching.md:** Switched $O(N \times M)$ variable names to properly be $O(n \times m)$ like other files. Cleaned up markdown.
- **11-knapsack-unbounded.md:** Standardized variable naming in code and math formulas ($W \to w$, $wt \to weight$, $val \to value$). Fixed typo in alternative loop explanation. Improved explanation of forward versus backward traversal to align better with code.
- **12-palindrome-dp.md:** Fixed typo `is_palindromedrome`, renamed `is_palin` to `is_palindrome` for clarity. Aligned complexity annotations with standard style (`Time: O(...)` vs `Time Complexity:`).
- **17-burst-balloons.md:** Clarified explanation for virtual boundaries. Improved `dfs` and tabulation loop comments. Restructured "Visual Walkthrough" using markdown tables. Enhanced `removeBoxes` inline comments. Standardized big-O notation.
- **18-dp-on-strings.md:** Clarified 1D state optimization in `num_distinct`. Fixed base case logic explanations in `is_interleave`. Rewrote `is_scramble` string slicing logic to highlight Python `Counter` vs sorting speedups and correct Big-O analysis. Extracted complex index math in `longest_valid_parentheses` into a readable variable. Standardized big-O notation.
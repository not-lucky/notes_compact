# Improve 10-binary-search/01-binary-search-template.md

- [x] Analyze `01-binary-search-template.md` for errors, clarity, and optimality.
- [x] Fix any issues in explanations (e.g., maximization vs minimization logic, loop conditions, feasibility checks).
- [x] Ensure all code implementations are correct, well-commented, and optimal.
- [x] Update the file with the improved content.
- [x] Verify changes using plan mode principles.

Modifications made:
1.  **Clarified Template 1**: Emphasized that this template is for finding exact matches where you *can stop early*.
2.  **Overhauled Template 2 (Left Boundary)**: Completely rewrote the explanation and code to use the standard, robust `left < right` template. This is the "insert" or `bisect_left` pattern, which is vastly preferred in interviews because it's much harder to get wrong once you understand it. It also removes the need for `result` variable.
3.  **Added Template 3 (Right Boundary)**: Similar to Template 2, this now uses the correct `left < right` pattern with the crucial detail of calculating `mid` by rounding up `mid = left + (right - left + 1) // 2` to prevent infinite loops.
4.  **Improved Visual Walkthrough**: Updated the visual walkthrough to match the new `left < right` logic for both left and right boundary templates, showing step-by-step how `left` and `right` converge.
5.  **Refined Binary Search on Answer**: Updated the template to use the `left < right` logic, making it cleaner and more consistent with the boundary templates.
6.  **Clarified Infinite Loops**: Added a crucial "Golden Rule" for preventing infinite loops:
    *   If using `left = mid`, `mid` calculation MUST round up.
    *   If using `right = mid`, `mid` calculation MUST round down.
7.  **General Formatting and Readability**: Made the headings clearer, improved comments in the code, and ensured consistent formatting.
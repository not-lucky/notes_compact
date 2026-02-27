# Rewrite DP on Strings Notes

1.  **Analyze current content:** [Completed]
    *   Review `09-dynamic-programming/18-dp-on-strings.md` for errors, clarity, and correctness.
    *   Check code snippets for bugs and style issues.
2.  **Plan improvements:** [Completed]
    *   Enhance explanations of state definitions and transitions.
    *   Ensure all code snippets are correct, well-commented, and Pythonic.
    *   Add complexity analysis where missing or incorrect.
    *   Reorganize content for better flow if needed.
3.  **Implement changes:** [Completed]
    *   Rewrite sections for better clarity and depth.
    *   Update code blocks.
4.  **Verify changes:** [Completed]
    *   Check markdown formatting.
    *   Verify code logic (tested Python snippets).
5.  **Final review:** [Completed]
    *   Update `tasks/todo.md` with results.

# Matrix Chain Multiplication Review
- Read current `09-dynamic-programming/16-matrix-chain.md`
- Analyzed the text for errors, clarity, and correctness.
- Fixed DP bugs and poor indexing:
  - Translated all code from 1-indexed to 0-indexed which makes the Python loops *much* simpler and less error-prone.
  - Rewrote the recurrence relation and explanations to match 0-indexed variables.
  - Clarified the interval DP intuition, especially *why* we must loop by length.
  - Added specific comments explaining the `k-1` step optimization in the `merge_stones` problem (ensuring the left partition can reduce to exactly 1 pile).
  - Updated the general `interval_dp_template` to strictly follow 0-indexed arrays with clearly named variables (`length`, `i`, `j`, `k`).
  - Addressed complexity limits explicitly (e.g. O(n³) is usually too slow for n > 500 without Knuth optimization).
# DP Notes Update Plan

## 09-dynamic-programming/01-dp-fundamentals.md
- [x] Expand "When NOT to use DP" sections with concrete counter-examples (e.g., greedy vs DP)
- [x] Add explicit explanations for the logic behind base cases

## 09-dynamic-programming/02-memoization-vs-tabulation.md
- [x] Include Top-Down (Memoization) alongside Tabulation for complex problems to aid intuition
- [x] Add explicit explanations for the logic behind base cases
- [x] Ensure mathematical recurrence relations are shown (if applicable here, maybe Fibonacci)

## 09-dynamic-programming/03-1d-dp-basics.md
- [x] Add formal mathematical recurrence relations (using `$$...$$`) for Fibonacci and Climbing Stairs before code
- [x] Standardize DP table visualizations (using Markdown tables)
- [x] Add explicit explanations for the logic behind base cases (e.g., why `dp[0] = 1`)
- [x] Explicitly explain the logic of space optimization

## 09-dynamic-programming/04-house-robber.md
- [x] Add formal mathematical recurrence relations before code
- [x] Improve Code Clarity: Rename generic variables (e.g., `prev1`/`prev2` -> `prev_max`/`curr_max` or `rob_current`/`skip_current`)
- [x] Explicitly explain the logic of space optimization
- [x] Add explicit explanations for the logic behind base cases
- [x] Include Top-Down (Memoization) alongside Tabulation

## 09-dynamic-programming/05-coin-change.md
- [x] Add formal mathematical recurrence relations before code
- [x] Standardize DP table visualizations (using Markdown tables)
- [x] Explain backward/forward iteration differences clearly
- [x] Add explicit explanations for the logic behind base cases (e.g., why `dp[0] = 0` or `1` depending on variant)
- [x] Include Top-Down (Memoization) alongside Tabulation

## 09-dynamic-programming/10-knapsack-01.md
- [ ] Add formal mathematical recurrence relation using LaTeX blocks before code.
- [ ] Flesh out the "Why iterate backwards?" with a conceptual explanation of preventing item reuse in the 1D space optimization.
- [ ] Standardize DP table visualizations (Markdown tables).
- [ ] Improve Code Clarity and explanations of base cases.
- [ ] Expand "When NOT to use DP" section with concrete counter-examples.
- [ ] Include Top-Down (Memoization) alongside Tabulation.

## 09-dynamic-programming/11-knapsack-unbounded.md
- [ ] Add formal mathematical recurrence relation using LaTeX blocks before code.
- [ ] Standardize DP table visualizations (Markdown tables).
- [ ] Improve Code Clarity and explanations of base cases.
- [ ] Expand "When NOT to use DP" section with concrete counter-examples.
- [ ] Include Top-Down (Memoization) alongside Tabulation.

## 09-dynamic-programming/12-palindrome-dp.md
- [ ] Add formal mathematical recurrence relation using LaTeX blocks before code.
- [ ] Group problems logically by Substring vs Subsequence patterns.
- [ ] Standardize DP table visualizations (Markdown tables).
- [ ] Improve Code Clarity and explanations of base cases.
- [ ] Expand "When NOT to use DP" section with concrete counter-examples.
- [ ] Include Top-Down (Memoization) alongside Tabulation.

## 09-dynamic-programming/13-word-break.md
- [ ] Add formal mathematical recurrence relation using LaTeX blocks before code.
- [ ] Explain base cases (`dp[0] = True`) clearly.
- [ ] Standardize DP table visualizations (Markdown tables).
- [ ] Improve Code Clarity and explanations of base cases.
- [ ] Expand "When NOT to use DP" section with concrete counter-examples.
- [ ] Include Top-Down (Memoization) alongside Tabulation.

## 09-dynamic-programming/14-regex-matching.md
- [ ] Add formal mathematical recurrence relations (LaTeX `$$...$$`) before code
- [ ] Standardize DP table visualizations
- [ ] Enhance explanations of base cases and space optimization
- [ ] Expand "When NOT to use DP" section with concrete counter-examples
- [ ] Include Top-Down (Memoization) alongside Tabulation
- [ ] Improve code clarity

## 09-dynamic-programming/15-buy-sell-stock.md
- [ ] Add formal mathematical recurrence relations (LaTeX `$$...$$`) before code
- [ ] Rename generic state variables (`hold`/`cash`) to more descriptive terms (`max_profit_holding_stock` / `max_profit_empty_handed`)
- [ ] Standardize DP table visualizations
- [ ] Enhance explanations of base cases and space optimization
- [ ] Expand "When NOT to use DP" section with concrete counter-examples
- [ ] Include Top-Down (Memoization) alongside Tabulation
- [ ] Improve code clarity

## 09-dynamic-programming/16-matrix-chain.md
- [ ] Add $O(n^3)$ interval DP recurrence mathematically (LaTeX `$$...$$`) before code
- [ ] Standardize DP table visualizations
- [ ] Enhance explanations of base cases and space optimization
- [ ] Expand "When NOT to use DP" section with concrete counter-examples
- [ ] Include Top-Down (Memoization) alongside Tabulation
- [ ] Improve code clarity

## 09-dynamic-programming/17-burst-balloons.md
- [ ] Add $O(n^3)$ interval DP recurrence mathematically (LaTeX `$$...$$`) before code
- [ ] Standardize DP table visualizations
- [ ] Enhance explanations of base cases and space optimization
- [ ] Expand "When NOT to use DP" section with concrete counter-examples
- [ ] Include Top-Down (Memoization) alongside Tabulation
- [ ] Improve code clarity

## 09-dynamic-programming/18-dp-on-strings.md
- [ ] Major Restructure: Group by sub-pattern (1D Prefix, 2D Sequence alignment, Palindromic strings)
- [ ] Add formal mathematical recurrence relations (LaTeX `$$...$$`) before code
- [ ] Standardize DP table visualizations
- [ ] Enhance explanations of base cases and space optimization
- [ ] Expand "When NOT to use DP" section with concrete counter-examples
- [ ] Include Top-Down (Memoization) alongside Tabulation
- [ ] Improve code clarity

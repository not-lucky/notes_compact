# Plan for Rewriting 05-coin-change.md

## Goals
- Fix any factual errors (particularly around permutations vs combinations explanation).
- Improve educational clarity (intuition behind *why* the loop order changes things).
- Enhance code readability and style.
- Make the structure consistent with previous rewritten chapters (like 03-1d-dp-basics.md and others).

## Issues Found in Current Version
1. **Permutations vs Combinations Explanation**: The explanation of *why* swapping the loop order calculates permutations vs combinations is weak. It just says "What happens if you swap the loop order? You calculate permutations". This is the absolute hardest concept for learners and needs a robust visual or conceptual explanation (e.g., treating combinations as adding a specific coin to all possible sums, while permutations treats each sum as reachable by adding *any* coin as the *last* step).
2. **Missing dimensions explanation**: It's helpful to explain Coin Change II (combinations) first as a 2D DP problem (where `dp[i][a]` is the number of ways to make amount `a` using the first `i` coins) and then show how it optimizes to 1D. This makes the loop order intrinsically obvious.
3. **BFS section**: It's good, but maybe slightly out of place in a DP guide unless explicitly framed as an alternative state-space search. I'll keep it but refine its framing.
4. **Code style**: Needs type hints, consistent docstrings, and clean Python.
5. **Path restoration**: The explanation is okay but can be clearer.

## Proposed Structure
1. **Overview & Intuition**: What is Unbounded Knapsack?
2. **Problem 1: Minimum Coins (Coin Change)**
   - Why Greedy Fails (good as is, just polish).
   - DP Approach (State, Recurrence, Base Case).
   - Visual Walkthrough.
   - Code (Bottom-Up & Top-Down).
3. **Problem 2: Number of Ways (Coin Change II - Combinations)**
   - The core problem.
   - **Crucial Concept: Why Loop Order Matters** (This needs a deep dive). Explain the 2D origin.
   - Code.
4. **Problem 3: Permutations (Combination Sum IV)**
   - Contrast with Coin Change II.
   - Code.
5. **Alternative Approach: BFS for Shortest Path**
   - Framing it as state-space search.
6. **Restoring the Path**
7. **Common Pitfalls**
8. **Practice Problems**

## Execution Steps
1. Write the new content in a temporary file.
2. Review the new content against the original.
3. Replace the original file.
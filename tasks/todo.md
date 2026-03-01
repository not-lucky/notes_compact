# Chapter 12: Greedy Algorithms - Analysis and Improvement

## Plan

- [x] Improve `12-greedy/01-greedy-basics.md`
- [x] Improve `12-greedy/02-interval-scheduling.md`
- [x] Improve `12-greedy/03-merge-intervals.md`
- [x] Improve `12-greedy/04-meeting-rooms.md`
- [x] Improve `12-greedy/05-jump-game.md`
- [x] Improve `12-greedy/06-gas-station.md`
- [x] Improve `12-greedy/07-candy-distribution.md`
- [x] Improve `12-greedy/08-partition-labels.md`
- [x] Improve `12-greedy/README.md`

## Instructions for subagents
For each file:
1. Fix anything that is wrong.
2. Improve explanations, correctness, and code readability.
3. Ensure only Python3 code is used.
4. Add good and progressive problems if needed for better understanding.

## Subagent Notes (08-partition-labels.md)
1. Read the file.
2. The explanation of why it works and the visual traces are generally excellent.
3. The LC 1520 "Maximum Number of Non-overlapping Substrings" solution has some logic that seems a bit complicated and off for a sketch. The explanation says "Step 1: Find first and last occurrence", "Step 2: expand interval", "Step 3: Collect valid intervals". The code seems pseudo-codey and complex for a Markdown note. I'll review and see if I can make it cleaner.
4. The Python code blocks are typed and clean.
5. I'll refine the LC 1520 sketch or replace it with a cleaner version. Actually, let's test that LC 1520 sketch.

**Updates:**
- Rewrote the README.md to be an excellent introductory index, grouping topics logically and clearly comparing Greedy vs. Dynamic Programming and BFS.
- Rewrote 08-partition-labels.md to emphasize the horizon extension pattern and relationship to Merge Intervals. Improved the LC 1520 sketch to be mathematically precise and much more readable Python code.
- Reviewed and improved README.md.
- Enhanced 05-jump-game.md with LC 1871 (Reachable Zeros with Min/Max Jump), optimized table comparisons, fixed typos and logic bugs in code sketches.

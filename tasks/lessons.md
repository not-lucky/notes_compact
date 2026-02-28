## Lessons Learned: Greedy Problems (Merge Intervals)

- Always explicitly mention the time/space complexity tradeoffs (e.g., O(1) space if modifying in-place vs O(n) for new output array).
- For `employee_free_time`, highlight the optimal Min-Heap approach O(n log k) as it demonstrates advanced interval merging.
- When creating visual traces, use explicit state values (like `merged[-1][1] = 3`) to map directly to the code logic.
- Differentiate between "Overlap Detection" and "Adjacent Detection", as interviewers often care about the subtle `<` vs `<=`.
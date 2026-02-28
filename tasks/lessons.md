## Lessons Learned: Greedy Problems (Merge Intervals)

- Always explicitly mention the time/space complexity tradeoffs (e.g., O(1) space if modifying in-place vs O(n) for new output array).
- For `employee_free_time`, highlight the optimal Min-Heap approach O(n log k) as it demonstrates advanced interval merging.
- When creating visual traces, use explicit state values (like `merged[-1][1] = 3`) to map directly to the code logic.
- Differentiate between "Overlap Detection" and "Adjacent Detection", as interviewers often care about the subtle `<` vs `<=`.

## Lessons Learned: Greedy Problems (Interval Scheduling)

- Emphasize the intuition difference between sorting by start time vs end time. End time sorting is critical because "earliest end time leaves maximum room for future activities."
- Explicitly differentiate between overlapping and touching intervals (e.g., `start >= last_end` vs `start > last_end`). Mention that clarifying this in an interview is essential.
- Include a specific example of why sorting by duration fails.
- Provide DP alternative solutions (e.g., Weighted Interval Scheduling) when Greedy fails due to added constraints (like weights/values).
- Be extremely meticulous with algorithm correctness. E.g., fixing a binary search in DP where finding the *rightmost* element requires storing the last valid index.
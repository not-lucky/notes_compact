# Advanced Dynamic Programming

This directory covers advanced DP patterns frequently encountered in Senior/Staff Level (L5+) interviews.

## Patterns

1.  **[Bitmask DP](./01-bitmask-dp.md)**: Handling states involving small sets ($N \le 20$).
2.  **[Digit DP](./02-digit-dp.md)**: Counting or summing properties of numbers within a range $[L, R]$.
3.  **[DP on Trees](./03-tree-dp.md)**: Optimization and rerooting techniques on tree structures.

## Learning Path

1.  Ensure you are comfortable with [Standard DP](../09-dynamic-programming/README.md).
2.  Master **Bitmask DP** first, as it's the most common "hard" DP pattern in general software engineering interviews.
3.  Study **DP on Trees**, specifically the **Rerooting** technique, which is a common differentiator for Senior roles.
4.  Learn **Digit DP** if you are targeting top-tier firms (Google, Meta) or competitive programming.

## Common Complexity Classes

| Technique | Common Time Complexity | Common Constraint |
|-----------|-------------------------|-------------------|
| Bitmask DP | $O(2^N \cdot N)$ or $O(2^N \cdot N^2)$ | $N \le 20$ |
| Digit DP | $O(\text{digits} \cdot \text{base} \cdot \text{states})$ | $N \le 10^{18}$ |
| Tree DP | $O(N)$ or $O(N \log N)$ | $N \le 10^5$ |
| Rerooting DP | $O(N)$ | $N \le 10^5$ |

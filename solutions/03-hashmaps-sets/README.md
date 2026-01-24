# Chapter 03: HashMaps & Sets - Solutions

This folder contains optimal solutions and explanations for all practice problems listed in Chapter 03.

## Solutions Directory

| Section | Topic | Key Takeaway |
|---------|-------|--------------|
| [01-hash-table-basics](./01-hash-table-basics.md) | Hash Table Internals | Understand hashing, collisions, and O(1) guarantees |
| [02-two-sum-pattern](./02-two-sum-pattern.md) | Two Sum Pattern | The classic complement lookup technique |
| [03-frequency-counting](./03-frequency-counting.md) | Frequency Counting | Counter patterns and top K problems |
| [04-anagram-grouping](./04-anagram-grouping.md) | Anagram Problems | Group by signature using hashmap |
| [05-subarray-sum-hashmap](./05-subarray-sum-hashmap.md) | Subarray Sum + HashMap | Prefix sum with hashmap for O(n) solutions |
| [06-set-operations](./06-set-operations.md) | Set Operations | Intersection, union, and uniqueness problems |
| [07-design-hashmap](./07-design-hashmap.md) | Design HashMap | Build your own hash table from scratch |
| [08-advanced-patterns](./08-advanced-patterns.md) | Advanced Patterns | LRU Cache, RandomizedSet, and more |

## General Tips for HashMap Problems

1.  **Always Consider Space-Time Trade-off**: HashMaps are the primary tool for trading memory (O(n) space) for speed (O(n) or O(1) time).
2.  **Use `collections.Counter`**: In Python, this is a highly optimized way to count frequencies.
3.  **Handle Duplicates Carefully**: Decide whether you need to store indices (if you need to return them) or just existence/counts.
4.  **Prefix Sum + HashMap**: This is a very common "Medium" level pattern for subarray sum problems.
5.  **Two-Pointer Optimization**: If the input is sorted, you can often replace a HashMap with two pointers to achieve O(1) space.

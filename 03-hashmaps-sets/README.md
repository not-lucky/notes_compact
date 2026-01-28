# Chapter 03: HashMaps & Sets

## Why This Matters for Interviews

HashMaps (dictionaries) and Sets are the **most powerful weapons** in your interview arsenal. They appear in 40-50% of all coding problems because:

1. **O(1) lookup magic**: Transform O(n²) brute force into O(n) elegant solutions
2. **Pattern versatility**: Frequency counting, two-sum, subarray problems, deduplication
3. **Universal applicability**: Almost any problem can be optimized with a hashmap
4. **Follow-up questions**: "Can you do better than O(n²)?" → The answer is usually a hashmap

At FANG+ companies, mastering hashmaps often means the difference between passing and failing.

**Interview frequency**: Very high. Expect 1-2 hashmap-based questions per interview.

---

## Core Patterns to Master

| Pattern            | Frequency | Key Problems                                               |
| ------------------ | --------- | ---------------------------------------------------------- |
| Two Sum Pattern    | Very High | Two Sum, 4Sum, K-Sum variants                              |
| Frequency Counting | Very High | Top K Frequent, Valid Anagram, Majority Element            |
| Subarray + HashMap | High      | Subarray Sum Equals K, Longest Substring Without Repeating |
| Anagram Grouping   | High      | Group Anagrams, Find All Anagrams in a String              |
| Set Operations     | Medium    | Intersection, Union, Happy Number                          |
| Design HashMap     | Medium    | Design HashMap, Design HashSet, LRU Cache                  |

---

## Chapter Sections

| Section                                                 | Topic                  | Key Takeaway                                        |
| ------------------------------------------------------- | ---------------------- | --------------------------------------------------- |
| [01-hash-table-basics](./01-hash-table-basics.md)       | Hash Table Internals   | Understand hashing, collisions, and O(1) guarantees |
| [02-two-sum-pattern](./02-two-sum-pattern.md)           | Two Sum Pattern        | The classic complement lookup technique             |
| [03-frequency-counting](./03-frequency-counting.md)     | Frequency Counting     | Counter patterns and top K problems                 |
| [04-anagram-grouping](./04-anagram-grouping.md)         | Anagram Problems       | Group by signature using hashmap                    |
| [05-subarray-sum-hashmap](./05-subarray-sum-hashmap.md) | Subarray Sum + HashMap | Prefix sum with hashmap for O(n) solutions          |
| [06-set-operations](./06-set-operations.md)             | Set Operations         | Intersection, union, and uniqueness problems        |
| [07-design-hashmap](./07-design-hashmap.md)             | Design HashMap         | Build your own hash table from scratch              |
| [08-advanced-patterns](./08-advanced-patterns.md)       | Advanced Patterns      | LRU Cache, RandomizedSet, and more                  |

---

## Common Mistakes Interviewers Watch For

1. **Forgetting edge cases**: Empty input, single element, all duplicates
2. **Wrong hashmap key**: Using mutable objects (lists) as keys
3. **Off-by-one in frequency**: Not initializing or not handling missing keys
4. **Hash collision ignorance**: Assuming O(1) is always O(1) (it's average case)
5. **Not considering space**: HashMaps trade space for time
6. **Overcomplicating**: Using hashmap when a simple set suffices

---

## Time Targets

| Difficulty | Target Time | Examples                                     |
| ---------- | ----------- | -------------------------------------------- |
| Easy       | 10-15 min   | Two Sum, Valid Anagram, Contains Duplicate   |
| Medium     | 15-25 min   | Group Anagrams, Top K Frequent, Subarray Sum |
| Hard       | 25-40 min   | LRU Cache, Minimum Window Substring          |

---

## Pattern Recognition Guide

```
"Find pair that sums to..."           → HashMap (two-sum pattern)
"Count frequency of elements..."      → HashMap + Counter
"Group elements by some property..."  → HashMap with signature key
"Find subarray with sum..."           → Prefix sum + HashMap
"Check if element exists..."          → Set
"Remove duplicates..."                → Set
"Find intersection/union..."          → Set operations
"Design a data structure..."          → HashMap + auxiliary structures
```

---

## Key Complexity Facts

| Operation | HashMap (dict) | Set          |
| --------- | -------------- | ------------ |
| Insert    | O(1) average   | O(1) average |
| Lookup    | O(1) average   | O(1) average |
| Delete    | O(1) average   | O(1) average |
| Iteration | O(n)           | O(n)         |
| Space     | O(n)           | O(n)         |

**Note**: Worst case is O(n) due to hash collisions, but this rarely happens with good hash functions.

---

## Prerequisites

> **Prerequisites:** [01-complexity-analysis](../01-complexity-analysis/README.md), [02-arrays-strings](../02-arrays-strings/README.md)

Understanding Big-O notation is essential. Array/string basics help since many hashmap problems operate on these data types.

---

## Next Steps

Start with [01-hash-table-basics.md](./01-hash-table-basics.md) to understand how hash tables work under the hood. Then progress through the patterns - the two-sum pattern and frequency counting are the highest priority for interviews.

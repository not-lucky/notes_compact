# Solution: Linked List Chapter README

## Practice Problems Summary

This chapter covers all essential linked list patterns for technical interviews. Below is a summary of the practice problems solved in this chapter, organized by section.

### [01-linked-list-basics](./01-linked-list-basics.md)
- **Delete Node in a Linked List**: O(1) deletion without head access.
- **Remove Linked List Elements**: Basic deletion with dummy node.
- **Design Linked List**: Full implementation of a linked list.
- **Middle of the Linked List**: Basic fast-slow pointer usage.
- **Convert Binary Number in LL to Integer**: Traversal with computation.

### [02-fast-slow-pointers](./02-fast-slow-pointers.md)
- **Middle of the Linked List**: Optimal middle finding.
- **Linked List Cycle**: Floyd's Cycle Detection.
- **Linked List Cycle II**: Find the start of the cycle.
- **Remove Nth Node From End**: One-pass solution using two pointers.
- **Palindrome Linked List**: Optimal O(1) space check.

### [03-reversal-patterns](./03-reversal-patterns.md)
- **Reverse Linked List**: Fundamental iterative reversal.
- **Reverse Linked List II**: Partial list reversal.
- **Swap Nodes in Pairs**: Pairwise reversal.
- **Reverse Nodes in k-Group**: Complex k-group reversal.
- **Rotate List**: Rotation via reversal concepts.

### [04-merge-lists](./04-merge-lists.md)
- **Merge Two Sorted Lists**: Basic two-pointer merge.
- **Merge k Sorted Lists**: Divide & conquer or heap-based merge.
- **Sort List**: O(n log n) merge sort on linked list.
- **Add Two Numbers**: Addition as a merge variant.

### [05-intersection-detection](./05-intersection-detection.md)
- **Intersection of Two Linked Lists**: Distance equalization technique.
- **Find the Duplicate Number**: Cycle detection in an array.

### [06-palindrome-list](./06-palindrome-list.md)
- **Palindrome Linked List**: Middle find + reverse + compare.
- **Valid Palindrome**: String variant for comparison.
- **Valid Palindrome II**: String variant allowing one deletion.
- **Reorder List**: Split + reverse + merge.

### [07-dummy-node-technique](./07-dummy-node-technique.md)
- **Remove Linked List Elements**: Handling head deletion.
- **Remove Nth Node From End**: Handling head removal.
- **Partition List**: Using multiple dummies for list building.
- **Remove Duplicates from Sorted List II**: Clean duplicate removal.

### [08-copy-with-random](./08-copy-with-random.md)
- **Copy List with Random Pointer**: Interleaving technique for O(1) extra space.
- **Clone Graph**: Deep copy for general graphs using DFS/HashMap.

---

## Mastering Linked Lists

To master linked lists, focus on these three habits:
1. **Always use a dummy node** for any operation that might change the head.
2. **Handle Null checks** before every `.next` access.
3. **Draw the pointers** to visualize the state before and after each modification.

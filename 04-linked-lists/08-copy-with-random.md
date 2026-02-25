# Copy List with Random Pointer

> **Prerequisites:** [01-linked-list-basics](./01-linked-list-basics.md), [03-hashmaps-sets](../03-hashmaps-sets/README.md)

## Overview

Deep copying a linked list with random pointers requires creating entirely new nodes where both `next` and `random` pointers reference the new nodes, not the originals. The challenge is mapping old nodes to new nodes. HashMap gives $\Theta(n)$ time/space; the interleaving technique achieves $\Theta(1)$ extra space.

## Building Intuition

**Why is this problem tricky?**

Simple linked list copying is straightforward—traverse and create nodes. But random pointers create a chicken-and-egg problem:

```
When copying node A, A.random might point to node C.
But C's copy might not exist yet!

Original:  [A] → [B] → [C] → None
            ↓           ↑
            └───────────┘  (A.random = C)

We need: [A'] → [B'] → [C'] → None
          ↓            ↑
          └────────────┘  (A'.random = C', not C!)
```

You can't set random pointers until all copy nodes exist. But you can't create all nodes without losing track of which copy corresponds to which original.

**Solution 1: HashMap as a Translation Table**

```
old_to_new = {A: A', B: B', C: C'}

# Now setting random is easy:
A'.random = old_to_new[A.random]
         = old_to_new[C]
         = C'
```

The hashmap acts as a translator between the old world and the new world. Every old node maps to its corresponding new node.

**Solution 2: Interleaving—The $\Theta(1)$ Space Magic**

Instead of a separate data structure, embed the mapping in the list itself:

```
Step 1: Interleave copies
Original:  [A] → [B] → [C] → None
Becomes:   [A] → [A'] → [B] → [B'] → [C] → [C'] → None

Now: A.next = A' (the copy is always right after the original!)

Step 2: Set random pointers
A.random = C
A'.random = A.random.next = C.next = C'

The pattern: copy.random = original.random.next

Step 3: Unweave the lists
Extract: [A'] → [B'] → [C'] → None
Restore: [A] → [B] → [C] → None
```

The interleaving uses the list structure itself as the hashmap!

**Why the Index Matters in Heap-Based Deep Copy**:
If you try to put nodes in a heap (for other reasons):

```python
heappush(heap, (node.val, node))  # FAILS if two nodes have same value
heappush(heap, (node.val, index, node))  # Works—index is tiebreaker
```

Python compares tuples left-to-right. If values are equal, it tries to compare nodes, which raises TypeError. An index ensures unique ordering.

**What "Deep Copy" Really Means**:

```python
# Shallow copy: new list, same nodes
copy_head = original_head  # Just copying reference

# Deep copy: new list, new nodes
# No node in copy_list is the same object as any node in original_list
assert all(copy_node is not orig_node for ...)
```

Deep copy means complete independence. Modifying the copy doesn't affect the original.

## When NOT to Use These Techniques

1. **No Random Pointers**: For simple linked lists, just traverse and copy. No need for hashmaps or interleaving.

2. **Immutable/Read-Only Lists**: Interleaving modifies the original list temporarily. If the list can't be modified (concurrent access, immutability requirements), use the hashmap approach.

3. **Memory is More Important than Clarity**: Interleaving is $\Theta(1)$ space but harder to understand and debug. If $\Theta(n)$ space is acceptable, hashmap is cleaner.

4. **Graph Structures (Not Just Lists)**: For general graphs with cycles, DFS/BFS with hashmap is the standard approach. Interleaving doesn't generalize beyond linked lists.

5. **When the Node Type Isn't Hashable**: The hashmap approach requires nodes to be valid dict keys. Custom `__hash__` might be needed for unusual node types.

**Common Mistake**: Forgetting that `node.random` could be `None`. Always check before doing `node.random.next`:

```python
if current.random:
    current.next.random = current.random.next
# else: copy.random stays None (default)
```

## Interview Context

Deep copying a linked list with random pointers is a **challenging interview favorite** because:

1. **Tests multiple skills**: Pointer manipulation, hashing, space optimization
2. **Real-world relevance**: Copying complex data structures (graphs, DAGs)
3. **Multiple approaches**: HashMap vs interleaving technique
4. **Edge case complexity**: None pointers, self-references, cycles

This problem (LeetCode 138) is asked frequently at top tech companies.

---

## Problem Definition

Given a linked list where each node has:

- `val`: Integer value
- `next`: Pointer to next node
- `random`: Pointer to any node in the list (or None)

Create a **deep copy** - a completely new list where:

- All nodes are newly created
- `next` and `random` pointers point to the new nodes (not original)

```python
class Node:
    def __init__(self, val: int, next=None, random=None):
        self.val = val
        self.next = next
        self.random = random
```

### Visual Example

```
Original:
  ┌──────────────────────────┐
  │                          ↓
[1] ──→ [2] ──→ [3] ──→ [4] ──→ None
  ↑       │       │       │
  │       │       ↓       │
  │       └──────[3]      │
  │                       │
  └───────────────────────┘

Node 1: next=2, random=4
Node 2: next=3, random=3
Node 3: next=4, random=None
Node 4: next=None, random=1

Deep copy must replicate exact structure with NEW nodes.
```

---

## Approach 1: HashMap (Two Pass)

```python
from typing import Optional

def copy_random_list_hashmap(head: Optional[Node]) -> Optional[Node]:
    """
    Deep copy using HashMap.

    Time Complexity: $O(n)$
    Space Complexity: $O(n)$ for the hashmap
    """
    if not head:
        return None

    # Pass 1: Create all nodes, store mapping old → new
    old_to_new = {}
    current = head

    while current:
        old_to_new[current] = Node(current.val)
        current = current.next

    # Pass 2: Connect next and random pointers
    current = head

    while current:
        new_node = old_to_new[current]
        new_node.next = old_to_new.get(current.next)
        new_node.random = old_to_new.get(current.random)
        current = current.next

    return old_to_new[head]
```

### Visual Walkthrough

```
Original: [1] → [2] → [3] → None
          ↓     ↓
          [3]   [1]

Pass 1: Create new nodes
old_to_new = {
    old_1: new_1,
    old_2: new_2,
    old_3: new_3
}

Pass 2: Connect pointers
  new_1.next = old_to_new[old_2] = new_2
  new_1.random = old_to_new[old_3] = new_3

  new_2.next = old_to_new[old_3] = new_3
  new_2.random = old_to_new[old_1] = new_1

  new_3.next = old_to_new[None] = None
  new_3.random = old_to_new[None] = None

Result: [1'] → [2'] → [3'] → None
         ↓      ↓
        [3']   [1']
```

---

## Approach 2: HashMap (Single Pass)

```python
def copy_random_list_single_pass(head: Optional[Node]) -> Optional[Node]:
    """
    Deep copy using HashMap in single pass.
    Uses getOrCreate pattern.

    Time Complexity: $O(n)$
    Space Complexity: $O(n)$
    """
    if not head:
        return None

    old_to_new = {}

    def get_or_create(node: Optional[Node]) -> Optional[Node]:
        """Get existing copy or create new one."""
        if not node:
            return None
        if node not in old_to_new:
            old_to_new[node] = Node(node.val)
        return old_to_new[node]

    current = head

    while current:
        new_node = get_or_create(current)
        new_node.next = get_or_create(current.next)
        new_node.random = get_or_create(current.random)
        current = current.next

    return old_to_new[head]
```

---

## Approach 3: Interleaving ($O(1)$ Space)

This clever approach avoids using a hashmap by interleaving copied nodes with original nodes.

```python
def copy_random_list(head: Optional[Node]) -> Optional[Node]:
    """
    Deep copy using interleaving technique.

    LeetCode 138: Copy List with Random Pointer

    Time Complexity: $O(n)$
    Space Complexity: $O(1)$ - no hashmap needed
    """
    if not head:
        return None

    # Step 1: Create interleaved copies
    # Original: A → B → C
    # After:    A → A' → B → B' → C → C'
    current = head
    while current:
        copy = Node(current.val)
        copy.next = current.next
        current.next = copy
        current = copy.next

    # Step 2: Set random pointers for copies
    current = head
    while current:
        if current.random:
            current.next.random = current.random.next
        current = current.next.next

    # Step 3: Separate the two lists
    current = head
    new_head = head.next

    while current:
        copy = current.next
        current.next = copy.next
        if copy.next:
            copy.next = copy.next.next
        current = current.next

    return new_head
```

### Visual Walkthrough

```
Original: [1] → [2] → [3] → None
           ↓     ↓
          [3]   [1]

Step 1: Interleave copies
[1] → [1'] → [2] → [2'] → [3] → [3'] → None

Step 2: Set random pointers
  1'.random = 1.random.next = 3' (3 points to 3')
  2'.random = 2.random.next = 1' (1 points to 1')
  3'.random = None

[1] → [1'] → [2] → [2'] → [3] → [3'] → None
        ↓            ↓
       [3']         [1']

Step 3: Separate lists
Original: [1] → [2] → [3] → None
Copy:     [1'] → [2'] → [3'] → None
            ↓      ↓
           [3']   [1']
```

---

## Detailed Step 3 Walkthrough

```python
# Initial state after Step 2:
# [1] → [1'] → [2] → [2'] → [3] → [3'] → None
#  ↑     ↑
#  current copy

# Iteration 1:
current = [1]
copy = [1']
current.next = copy.next = [2]      # [1] → [2]
copy.next = copy.next.next = [2']   # [1'] → [2']
current = [2]

# Iteration 2:
current = [2]
copy = [2']
current.next = copy.next = [3]      # [2] → [3]
copy.next = copy.next.next = [3']   # [2'] → [3']
current = [3]

# Iteration 3:
current = [3]
copy = [3']
current.next = copy.next = None     # [3] → None
copy.next = None (no copy.next.next)  # [3'] → None
current = None

# Done!
```

---

## Complexity Comparison

| Approach              | Time Complexity | Space Complexity |
| --------------------- | --------------- | ---------------- |
| HashMap (two pass)    | $\Theta(n)$            | $\Theta(n)$             |
| HashMap (single pass) | $\Theta(n)$            | $\Theta(n)$             |
| Interleaving          | $\Theta(n)$            | $\Theta(1)$*            |

\*$\Theta(1)$ extra space (the copied list itself is $\Theta(n)$ but that is required for the output and typically not counted against the space complexity of the algorithm).

---

## Edge Cases

```python
# 1. Empty list
head = None
# Return None

# 2. Single node with random to itself
node = Node(1)
node.random = node
# Copy should also point to itself (the new node)

# 3. Single node with random to None
node = Node(1)
node.random = None
# Simple case

# 4. All randoms are None
# Essentially a simple deep copy

# 5. All randoms point to same node
# [1] → [2] → [3]
#  ↓     ↓     ↓
# [2]   [2]   [2]
# All copies should point to new node 2

# 6. Cycle in next pointers (not typically in this problem)
# Standard problem assumes no cycle in next, only random varies
```

---

## Testing Helper

```python
def create_test_list(vals_and_random_indices: list[tuple[int, Optional[int]]]) -> Optional[Node]:
    """
    Create test list from values and random pointer indices.
    Format: [(val, random_index), ...]
    random_index is 0-based, or None for no random pointer.
    """
    if not vals_and_random_indices:
        return None

    # Create nodes
    nodes = [Node(val) for val, _ in vals_and_random_indices]

    # Connect next pointers
    for i in range(len(nodes) - 1):
        nodes[i].next = nodes[i + 1]

    # Connect random pointers
    for i, (_, random_idx) in enumerate(vals_and_random_indices):
        if random_idx is not None:
            nodes[i].random = nodes[random_idx]

    return nodes[0]


def verify_deep_copy(original: Optional['Node'], copy: Optional['Node']) -> bool:
    """Verify that copy is a valid deep copy."""
    if not original and not copy:
        return True
    if not original or not copy:
        return False

    orig_nodes = {}
    copy_nodes = {}

    # Collect all nodes
    curr = original
    i = 0
    while curr:
        orig_nodes[curr] = i
        curr = curr.next
        i += 1

    curr = copy
    i = 0
    while curr:
        copy_nodes[curr] = i
        curr = curr.next
        i += 1

    # Verify no shared nodes
    for node in orig_nodes:
        if node in copy_nodes:
            return False  # Shared reference!

    # Verify structure matches
    o, c = original, copy
    while o and c:
        if o.val != c.val:
            return False
        if (o.random is None) != (c.random is None):
            return False
        if o.random and c.random:
            if orig_nodes[o.random] != copy_nodes[c.random]:
                return False
        o = o.next
        c = c.next

    return o is None and c is None
```

---

## Variation: Clone Graph

The same concepts apply to cloning a graph (LeetCode 133):

```python
def clone_graph(node: 'Optional[Node]') -> 'Optional[Node]':
    """
    Clone an undirected graph using DFS + HashMap.

    Time Complexity: $O(V + E)$ where V is number of vertices and E is number of edges
    Space Complexity: $O(V)$ for the recursion stack and hashmap
    """
    if not node:
        return None

    old_to_new = {}

    def dfs(node: 'Node') -> 'Node':
        if node in old_to_new:
            return old_to_new[node]

        copy = Node(node.val)
        old_to_new[node] = copy

        for neighbor in node.neighbors:
            copy.neighbors.append(dfs(neighbor))

        return copy

    return dfs(node)
```

---

## Interview Tips

1. **Start with HashMap approach**: Easier to explain and implement correctly
2. **Mention $O(1)$ space optimization**: Shows deeper knowledge
3. **Draw the interleaving**: Visual explanation is crucial
4. **Handle edge cases verbally**: Empty list, self-references
5. **Verify deep copy**: Explain that no original nodes should be in the copy

---

## Practice Problems

| #   | Problem                               | Difficulty | Key Concept             |
| --- | ------------------------------------- | ---------- | ----------------------- |
| 1   | Copy List with Random Pointer         | Medium     | Deep copy with random   |
| 2   | Clone Graph                           | Medium     | Same concept for graphs |
| 3   | Clone Binary Tree with Random Pointer | Medium     | Same concept for trees  |

---

## Key Takeaways

1. **HashMap approach** is $O(n)$ time and $O(n)$ space - simple and reliable
2. **Interleaving approach** is $O(n)$ time and $O(1)$ extra space - optimal
3. **Two-phase HashMap**: Create nodes first, connect pointers second
4. **Interleaving phases**: Insert copies, set random, separate lists
5. **Always verify**: Deep copy means NO shared references to original
6. **Same pattern for graphs**: DFS/BFS + HashMap for general graph cloning

---

## Summary: Chapter 04 Complete

You've now learned all the essential linked list patterns:

1. **Basics**: Node structure, traversal, insert, delete
2. **Fast-slow pointers**: Cycle detection, find middle, nth from end
3. **Reversal patterns**: Full, partial, k-group reversal
4. **Merge operations**: Merge sorted, merge k, sort list
5. **Intersection detection**: Two-pointer technique
6. **Palindrome check**: Combine fast-slow with reversal
7. **Dummy node**: Simplify edge cases
8. **Deep copy**: HashMap and interleaving techniques

These patterns cover the vast majority of linked list interview questions. Practice combining them for complex problems!

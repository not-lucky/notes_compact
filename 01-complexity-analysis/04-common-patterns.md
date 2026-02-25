# Common Operation Complexities

> **Prerequisites:** [01-big-o-notation.md](./01-big-o-notation.md) | [02-time-complexity.md](./02-time-complexity.md)

Understanding the time and space complexity of common data structures and algorithms is non-negotiable for coding interviews. You should intuitively know the cost of every operation you perform.

## Building Intuition

**The "Data Structure Toolkit" Mental Model**

Think of data structures as physical tools with specific constraints and strengths:

```text
Array/List = Bookshelf with a fixed number of slots
  - Finding a specific book by title: Check each book → O(n)
  - Getting the 5th book: Reach directly to slot 5 → O(1)
  - Inserting a book at the front: Shift ALL other books to the right → O(n)

Hash Table = The Magic Librarian
  - Finding a specific book: The librarian instantly tells you its exact location → O(1)
  - Constraint: No inherent sorting or ordering of books.

Heap = Emergency Room Triage
  - Get the most urgent patient: Always sitting at the front door → O(1)
  - Admit new patient: Nurse quickly sorts them into the right priority slot → O(log n)

Tree = The Corporate Hierarchy
  - Finding a specific employee: Ask the CEO, who directs you down the correct branch. 
  - Each step eliminates half the company (if balanced) → O(log n)
```

**The "Why Hash Tables Are Magic" Insight**
Hash tables convert the act of *searching* into *arithmetic*. Instead of checking items iteratively ("Is this it?"), a hash function calculates the exact memory address: `address = hash(key)`. This makes lookup O(1)—it's calculation, not searching.

---

## Python Built-in Types & Complexities

Python abstracts away many underlying memory management details, but under the hood, standard complexities apply. 

### `list` (Dynamic Array)

Python lists are dynamic arrays, **not** linked lists. They allocate contiguous blocks of memory.

| Operation                        | Average Case | Worst Case | Notes                                      |
| -------------------------------- | ------------ | ---------- | ------------------------------------------ |
| Access `arr[i]`                  | O(1)         | O(1)       | Direct memory address calculation          |
| Append `arr.append(x)`           | O(1)*        | O(n)       | *Amortized O(1). O(n) when resizing array  |
| Pop last `arr.pop()`             | O(1)         | O(1)       | Decrements internal size pointer           |
| Insert at index `arr.insert(i,x)`| O(n)         | O(n)       | Must shift all subsequent elements right   |
| Delete at index `arr.pop(i)`     | O(n)         | O(n)       | Must shift all subsequent elements left    |
| Search `x in arr`                | O(n)         | O(n)       | Linear scan                                |
| Slice `arr[i:j]`                 | O(k)         | O(n)       | `k = j - i`. Creates a new array copy      |
| Sort `arr.sort()`                | O(n log n)   | O(n log n) | Uses Timsort (highly optimized)            |

> 🚩 **Red Flag:** Using `arr.insert(0, x)` or `arr.pop(0)` in a loop creates an **O(n²)** algorithm. Use `collections.deque` instead.

### `dict` (Hash Map)

Python dictionaries are highly optimized hash tables. In Python 3.7+, they also guarantee **insertion order**.

| Operation           | Average Case | Worst Case | Notes                                |
| ------------------- | ------------ | ---------- | ------------------------------------ |
| Get `d[key]`        | O(1)         | O(n)       | Worst case happens on hash collision |
| Set `d[key] = val`  | O(1)         | O(n)       | May trigger resize / hash collision  |
| Delete `del d[key]` | O(1)         | O(n)       | Hash collision                       |
| Search `key in d`   | O(1)         | O(n)       | Checks keys, NOT values              |

> 💡 **Gotcha:** `d.keys()`, `d.values()`, and `d.items()` return *views* in O(1) time. However, actually *iterating* through those views takes O(n) time.

### `set` (Hash Set)

Implemented exactly like a dictionary, but only stores keys.

| Operation              | Average Case             | Worst Case | Notes                               |
| ---------------------- | ------------------------ | ---------- | ----------------------------------- |
| Add/Remove `s.add(x)`  | O(1)                     | O(n)       | Hash collision                      |
| Search `x in s`        | O(1)                     | O(n)       | Highly optimized membership check   |
| Union `s \| t`         | O(len(s) + len(t))       | -          | Must iterate and hash both sets     |
| Intersection `s & t`   | O(min(len(s), len(t)))   | -          | Iterates smaller set, checks larger |

> 🏆 **Pro-Tip:** If you need to repeatedly check if elements exist in an array, convert it to a set first! `x in arr` is O(n), but `x in set(arr)` is O(1). 

### `str` (Immutable Array of Characters)

Strings in Python are immutable. Any modification creates a completely new string.

| Operation                 | Time            | Notes                                   |
| ------------------------- | --------------- | --------------------------------------- |
| Access `s[i]`             | O(1)            | Direct indexing                         |
| Search `sub in s`         | O(n * m)        | `n=len(s)`, `m=len(sub)`. Substring search |
| Concatenate `s + t`       | O(n + m)        | Allocates new string, copies both       |
| Join `"".join(list)`      | O(N)            | `N = total chars`. Efficient building   |

> 🚩 **Red Flag:** `s += char` in a loop is conceptually **O(n²)** because it creates a new string every iteration. Always append to a `list` and use `"".join()` at the end.

### `collections.deque` (Doubly-Ended Queue)

Implemented as a doubly-linked list of blocks. Ideal for Queues and Stacks.

| Operation                     | Time | Notes                                 |
| ----------------------------- | ---- | ------------------------------------- |
| Append/Pop right `d.append()` | O(1) | Same as list                          |
| Append/Pop left `d.popleft()` | O(1) | **Much faster than list `pop(0)`**    |
| Access `d[i]`                 | O(n) | Must traverse links (no random access)|

### `heapq` (Min-Heap)

Python implements heaps using standard arrays (lists). It only provides a Min-Heap natively.

| Operation                    | Time     | Notes                                 |
| ---------------------------- | -------- | ------------------------------------- |
| Push `heappush(h, x)`        | O(log n) | Bubbles up to maintain heap property  |
| Pop min `heappop(h)`         | O(log n) | Swaps with last, bubbles down         |
| Peek min `h[0]`              | O(1)     | Smallest element is always at index 0 |
| Heapify `heapify(arr)`       | O(n)     | **Not O(n log n)!** Highly optimized  |

> 💡 **Gotcha:** For a Max-Heap in Python, insert elements as negative values: `heappush(h, -val)`.

---

## Standard Data Structure Reference

### Linked Lists

| Structure           | Access | Search | Insert (at known node) | Delete (at known node) |
| ------------------- | ------ | ------ | ---------------------- | ---------------------- |
| Singly Linked List  | O(n)   | O(n)   | O(1)                   | O(n)*                  |
| Doubly Linked List  | O(n)   | O(n)   | O(1)                   | O(1)                   |

*\*Singly linked lists require traversing from the head to find the "previous" node to perform a deletion.*

### Trees

| Structure           | Search   | Insert   | Delete   | Min/Max  | Notes |
| ------------------- | -------- | -------- | -------- | -------- | ----- |
| Binary Search Tree  | O(log n) | O(log n) | O(log n) | O(log n) | Worst-case is O(n) if unbalanced (e.g., straight line) |
| Balanced BST (AVL)  | O(log n) | O(log n) | O(log n) | O(log n) | Always balanced. Python has no built-in balanced BST. |
| Trie (Prefix Tree)  | O(L)     | O(L)     | O(L)     | -        | `L` is the length of the word. Incredible for string prefixes. |

### Graphs

Where `V = Vertices (Nodes)` and `E = Edges`.

| Operation         | Adjacency List `dict[list]` | Adjacency Matrix `list[list]` |
| ----------------- | --------------------------- | ----------------------------- |
| Space Complexity  | O(V + E)                    | O(V²)                         |
| Check Edge Exists | O(degree(V))                | O(1)                          |
| Get Neighbors     | O(degree(V))                | O(V)                          |
| Add Vertex        | O(1)                        | O(V²)                         |
| Traversal (BFS/DFS)| O(V + E)                   | O(V²)                         |

```python
# Adjacency List (Preferred for 90% of interview problems - sparse graphs)
graph = {
    'A': ['B', 'C'],
    'B': ['A', 'D'],
    'C': ['A'],
    'D': ['B']
}

# Adjacency Matrix (Preferred for dense graphs or rapid edge lookups)
matrix = [
    [0, 1, 1, 0],  # A connects to B(1), C(2)
    [1, 0, 0, 1],  # B connects to A(0), D(3)
    [1, 0, 0, 0],  # C connects to A(0)
    [0, 1, 0, 0]   # D connects to B(1)
]
```

---

## Sorting Algorithms

| Algorithm      | Best Time  | Avg Time   | Worst Time | Space    | Stable | Notes |
| -------------- | ---------- | ---------- | ---------- | -------- | ------ | ----- |
| **Merge Sort** | O(n log n) | O(n log n) | O(n log n) | O(n)     | Yes    | Divide & conquer. Great for linked lists. |
| **Quick Sort** | O(n log n) | O(n log n) | O(n²)      | O(log n) | No     | Standard generic sort. In-place. |
| **Heap Sort**  | O(n log n) | O(n log n) | O(n log n) | O(1)     | No     | Selects max repeatedly. In-place. |
| **Timsort**    | O(n)       | O(n log n) | O(n log n) | O(n)     | Yes    | Python's `sort()`. Hybrid merge/insertion. |
| **Counting Sort**| O(n + k) | O(n + k)   | O(n + k)   | O(n + k) | Yes    | `k` is range of elements. Beats O(n log n) for small ranges! |

---

## When NOT to Use These Structures

Choosing the right structure is half the battle in an interview.

**When NOT to use a Hash Table:**
- You need data sorted (hash tables have arbitrary order).
- You need the closest/smallest/largest value (use a Tree or Heap).
- You are strictly memory constrained (Hash Tables allocate extra empty space to avoid collisions).

**When NOT to use an Array/List:**
- You need to frequently add/remove elements from the front or middle (O(n) shifting overhead).
- You need fast lookups by a specific ID or Key.

**When NOT to use a Heap:**
- You need to search for a specific arbitrary value (Searching a heap is O(n)).
- You need to easily remove arbitrary values.

---

## The "Cheat Sheet" Summary

Ask yourself what operation is the bottleneck in your algorithm, and pick the structure that makes it fast:

| If you mostly need to...      | Use this Data Structure | Resulting Time |
| ----------------------------- | ----------------------- | -------------- |
| Look up values by ID/Key      | Hash Map (`dict`)       | O(1)           |
| Check if something exists     | Hash Set (`set`)        | O(1)           |
| Process items front-to-back   | Queue (`deque`)         | O(1) push/pop  |
| Constantly find the Min/Max   | Priority Queue (`heapq`)| O(1) peek, O(log n) push/pop |
| Search in a sorted list       | Binary Search (`bisect`)| O(log n)       |
| Search for string prefixes    | Trie (Prefix Tree)      | O(length of word)|

---

## Next Steps

Now that you know the costs, learn how to communicate them effectively to your interviewer:

**Next:** [05-interview-tips.md](./05-interview-tips.md)

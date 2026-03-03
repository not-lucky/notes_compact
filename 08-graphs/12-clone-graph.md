# Clone Graph

> **Prerequisites:** [02-bfs-basics](./02-bfs-basics.md), [03-dfs-basics](./03-dfs-basics.md)

## Interview Context

Clone Graph is a FANG+ favorite because:

1. **Tests graph traversal**: BFS or DFS with a twist.
2. **Deep copy concept**: Understanding references vs values.
3. **HashMap for mapping**: Old node → new node.
4. **Clean code skills**: Handling the recursive structure.

**FANG Context**: This problem is particularly emphasized at **Meta**, where it frequently appears in phone screens and onsites. Meta loves it because it perfectly tests core CS fundamentals (pointers, recursion, hash maps, graph traversal) in a compact, 15-minute implementation window. Google also asks variations of this, often involving distributed graphs or more complex node structures.

---

## Problem Statement

Given a reference to a node in a connected undirected graph, return a **deep copy** (clone) of the graph.

Each node contains a value and a list of neighbors.

```
Input:
    1 --- 2
    |     |
    4 --- 3

Output: New graph with same structure, different objects
```

---

## Node Definition

Using standard typing which is universally accepted in interview environments:

```python
from typing import Optional, List, Dict

class Node:
    def __init__(self, val: int = 0, neighbors: Optional[List['Node']] = None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []
```

---

## Core Intuition: Why a HashMap?

The fundamental challenge of cloning a graph (vs. a tree) is **cycles**. In a tree, every node is visited exactly once via its single parent. In a graph, node A may point to node B, and node B may point back to A. A naive recursive clone will loop forever.

**The HashMap (`old_node → cloned_node`) solves two problems simultaneously:**

1. **Cycle breaking**: Before recursing into a neighbor, we check the map. If the neighbor is already there, we return the existing clone instead of creating a new one. This breaks infinite loops.
2. **Identity preservation**: Every original node maps to exactly one clone. Without the map, a node reachable via two different paths would be cloned twice, producing a structurally incorrect copy.

**Critical ordering rule**: We must insert the clone into the map **before** recursing into its neighbors. If we recurse first and insert after, a cycle back to the current node will not find it in the map, causing infinite recursion.

```python
# WRONG order (infinite recursion on cycles):
clone = Node(node.val)
for neighbor in node.neighbors:       # recurse BEFORE storing
    clone.neighbors.append(dfs(neighbor))
cloned[node] = clone                  # too late — cycle already hit

# CORRECT order:
clone = Node(node.val)
cloned[node] = clone                  # store BEFORE recursing
for neighbor in node.neighbors:
    clone.neighbors.append(dfs(neighbor))
```

---

## DFS Approach (Recursive)

```python
def clone_graph_dfs(node: Optional['Node']) -> Optional['Node']:
    """
    Clone graph using DFS with HashMap.

    Time:  O(V + E) — visit every node and traverse every edge once
    Space: O(V)     — HashMap stores V clones + recursion stack up to O(V) deep
    """
    if not node:
        return None

    # Map: original node -> cloned node
    cloned: Dict['Node', 'Node'] = {}

    def dfs(curr: 'Node') -> 'Node':
        # Already cloned? Return existing clone (cycle breaker)
        if curr in cloned:
            return cloned[curr]

        # Create clone and register it BEFORE recursing (critical for cycles)
        clone = Node(curr.val)
        cloned[curr] = clone

        # Recursively clone each neighbor
        for neighbor in curr.neighbors:
            clone.neighbors.append(dfs(neighbor))

        return clone

    return dfs(node)
```

---

## BFS Approach

BFS clones level by level. The key difference from DFS: we create a neighbor's clone **when we first discover it** (not when we process it). This means by the time we process a node, all its neighbors already exist in the map, and we just wire up the edges.

```python
from collections import deque

def clone_graph_bfs(node: Optional['Node']) -> Optional['Node']:
    """
    Clone graph using BFS with HashMap.

    Time:  O(V + E)
    Space: O(V) — HashMap + queue (no recursion stack)
    """
    if not node:
        return None

    # Seed the map with the starting node's clone
    cloned: Dict['Node', 'Node'] = {node: Node(node.val)}
    queue: deque['Node'] = deque([node])

    while queue:
        curr = queue.popleft()

        for neighbor in curr.neighbors:
            if neighbor not in cloned:
                # First time seeing this neighbor — create its clone
                cloned[neighbor] = Node(neighbor.val)
                queue.append(neighbor)

            # Wire the edge: cloned curr -> cloned neighbor
            cloned[curr].neighbors.append(cloned[neighbor])

    return cloned[node]
```

---

## DFS vs BFS: When to Use Which

| Aspect               | Recursive DFS                      | BFS / Iterative DFS          |
| -------------------- | ---------------------------------- | ---------------------------- |
| Code simplicity      | Most concise                       | Slightly more boilerplate    |
| Stack overflow risk  | Yes — recursion depth up to O(V)   | No — uses heap memory        |
| Interview preference | Fine for small graphs              | Safer for "what about scale?"|
| Traversal order      | Depth-first (follows one path)     | Level-order (BFS)            |

**Rule of thumb for interviews**: Start with recursive DFS (cleaner code), then mention BFS as a follow-up that avoids stack overflow on deep/large graphs.

---

## Edge Types (Theory Deep Dive)

When performing graph DFS or BFS, there are four types of edges we might encounter. This is critical theory for understanding traversal and cycle detection.

1. **Tree Edge**: Discovers a new unvisited node. These edges form the DFS/BFS spanning tree.
   - Example: Visiting neighbor `2` from node `1` for the first time.
2. **Back Edge**: Connects a node to an ancestor in the DFS tree. Always indicates a cycle.
   - Example: Exploring node `1` (already on the current DFS path) from node `4`.
3. **Forward Edge**: Connects a node to a descendant in the DFS tree that is *not* a direct child.
   - Note: Forward edges only exist in **directed** graphs.
4. **Cross Edge**: Connects two nodes where neither is an ancestor of the other.
   - Note: In an **undirected** graph, every non-tree edge during a DFS is a back edge. Forward and cross edges do not exist in undirected DFS.

**Why this matters for Clone Graph**:
Since Clone Graph operates on undirected graphs, every time we encounter an already-cloned node during DFS (i.e., it exists in our HashMap), we are traversing a **back edge**. The HashMap lookup prevents us from re-cloning and falling into an infinite loop. This is why the HashMap serves double duty: it is both a "visited set" and an "old-to-new mapping."

---

## Visual Walkthrough (DFS)

```
Original:
    1 --- 2
    |     |
    4 --- 3

DFS from node 1:

Step 1: Visit 1 → Create clone 1'
        cloned = {1: 1'}
        Recurse into neighbors of 1: [2, 4]

Step 2: Visit 2 → Create clone 2'
        cloned = {1: 1', 2: 2'}
        Recurse into neighbors of 2: [1, 3]

Step 3: Visit 1 → already in cloned, return 1' (back edge — cycle handled!)
        Visit 3 → Create clone 3'
        cloned = {1: 1', 2: 2', 3: 3'}
        2'.neighbors = [1', 3']
        Recurse into neighbors of 3: [2, 4]

Step 4: Visit 2 → already cloned, return 2'
        Visit 4 → Create clone 4'
        cloned = {1: 1', 2: 2', 3: 3', 4: 4'}
        3'.neighbors = [2', 4']
        Recurse into neighbors of 4: [1, 3]

Step 5: Visit 1 → already cloned, return 1'
        Visit 3 → already cloned, return 3'
        4'.neighbors = [1', 3']

Step 6: Backtrack to step 1, add 4' to 1's neighbors
        1'.neighbors = [2', 4']

Done! Return 1'
```

---

## Iterative DFS

Uses an explicit stack instead of the call stack. Structurally identical to BFS but with a stack (LIFO) instead of a queue (FIFO). This gives depth-first ordering without recursion stack overflow risk.

```python
def clone_graph_iterative_dfs(node: Optional['Node']) -> Optional['Node']:
    """
    Clone graph using iterative DFS (explicit stack).

    Time:  O(V + E)
    Space: O(V)
    """
    if not node:
        return None

    cloned: Dict['Node', 'Node'] = {node: Node(node.val)}
    stack: List['Node'] = [node]

    while stack:
        curr = stack.pop()

        for neighbor in curr.neighbors:
            if neighbor not in cloned:
                cloned[neighbor] = Node(neighbor.val)
                stack.append(neighbor)

            # Wire edge: cloned curr -> cloned neighbor
            cloned[curr].neighbors.append(cloned[neighbor])

    return cloned[node]
```

---


## Progressive Examples to Build Understanding

To truly master cloning structures, it helps to see how the pattern evolves from simple to complex.

### 1. Clone a 1D Array (No references, just values)
The simplest clone. We just copy values.
```python
def clone_array(arr: List[int]) -> List[int]:
    return [x for x in arr]
```

### 2. Clone a Binary Tree (Acyclic, directional references)
Since trees cannot have cycles and each node is reached from exactly one parent, we don't need a visited map.
```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def clone_binary_tree(root: Optional[TreeNode]) -> Optional[TreeNode]:
    if not root:
        return None
    clone = TreeNode(root.val)
    clone.left = clone_binary_tree(root.left)
    clone.right = clone_binary_tree(root.right)
    return clone
```

### 3. Clone a DAG (Directed Acyclic Graph)
Here we have direction, but nodes can be reached via multiple paths (shared subtrees). We don't have infinite loops, but without a map, we might clone the same node multiple times, breaking the structure.
```python
# A map is required to preserve structure and avoid redundant work
def clone_dag(node: Optional['Node'], cloned: Dict['Node', 'Node']) -> Optional['Node']:
    if not node:
        return None
    if node in cloned:
        return cloned[node]
    
    clone = Node(node.val)
    cloned[node] = clone
    for neighbor in node.neighbors:
        clone.neighbors.append(clone_dag(neighbor, cloned))
    return clone
```

### 4. Clone a Cyclic Graph (Undirected/Directed with cycles)
The standard Clone Graph problem. The map is required both for structure preservation AND to break infinite recursion loops caused by cycles.

## Common Variations

### Clone Linked List with Random Pointer (LC 138)

```python
class NodeRandom:
    def __init__(self, val: int = 0,
                 next: Optional['NodeRandom'] = None,
                 random: Optional['NodeRandom'] = None):
        self.val = val
        self.next = next
        self.random = random


def copy_random_list(head: Optional['NodeRandom']) -> Optional['NodeRandom']:
    """
    Clone linked list with random pointers using HashMap (two-pass).

    Time:  O(n)
    Space: O(n)
    """
    if not head:
        return None

    # Pass 1: Create all clone nodes (no pointers yet)
    cloned: Dict['NodeRandom', 'NodeRandom'] = {}
    curr = head
    while curr:
        cloned[curr] = NodeRandom(curr.val)
        curr = curr.next

    # Pass 2: Wire next and random pointers via the map
    curr = head
    while curr:
        if curr.next:
            cloned[curr].next = cloned[curr.next]
        if curr.random:
            cloned[curr].random = cloned[curr.random]
        curr = curr.next

    return cloned[head]
```

### Clone N-ary Tree

Trees have no cycles, so the HashMap is unnecessary unless the "tree" turns out to have shared subtrees (a DAG). For a pure tree, recursion is sufficient.

```python
class NaryNode:
    def __init__(self, val: int = 0, children: Optional[List['NaryNode']] = None):
        self.val = val
        self.children = children if children is not None else []


def clone_tree(root: Optional['NaryNode']) -> Optional['NaryNode']:
    """
    Clone N-ary tree using DFS.
    Since trees have no cycles, a visited HashMap is not required.

    Time:  O(n)
    Space: O(h) — recursion stack where h is the tree height
    """
    if not root:
        return None

    clone = NaryNode(root.val)
    for child in root.children:
        clone.children.append(clone_tree(child))

    return clone
```

### O(1) Space Approach (Three-Pass Interleaving)

For linked list with random pointer only. Exploits the list structure by interleaving clones with originals, then separating them.

```python
def copy_random_list_o1(head: Optional['NodeRandom']) -> Optional['NodeRandom']:
    """
    Clone linked list with random pointer using O(1) extra space.

    Technique: Interleave clones into the original list, then separate.

    Time:  O(n)
    Space: O(1)
    """
    if not head:
        return None

    # Pass 1: Create clones interleaved with originals
    # 1 -> 1' -> 2 -> 2' -> 3 -> 3'
    curr = head
    while curr:
        clone = NodeRandom(curr.val, next=curr.next)
        curr.next = clone
        curr = clone.next

    # Pass 2: Set random pointers using interleaved structure
    curr = head
    while curr:
        if curr.random:
            curr.next.random = curr.random.next  # clone's random = original's random's clone
        curr = curr.next.next

    # Pass 3: Separate the two interleaved lists
    dummy = NodeRandom(0)
    clone_curr = dummy
    curr = head

    while curr:
        clone_curr.next = curr.next       # extract clone
        curr.next = curr.next.next        # restore original

        clone_curr = clone_curr.next
        curr = curr.next

    return dummy.next
```

---

## Edge Cases

```python
# 1. Empty graph → return None
clone_graph_dfs(None)  # Returns None

# 2. Single node, no neighbors
node = Node(1)
# Clone has val=1, empty neighbors list

# 3. Single node, self-loop (tests cycle handling on simplest case)
node = Node(1)
node.neighbors = [node]
# Clone must reference ITSELF, not the original node

# 4. Fully connected graph (complete graph)
# Every node connected to every other node — stress tests the map

# 5. Linear chain (1 - 2 - 3 - 4)
# Deepest recursion — tests stack depth
```

---

## Common Mistakes

```python
# MISTAKE 1: No HashMap → infinite recursion on cycles
def clone_wrong(node: Optional['Node']) -> Optional['Node']:
    if not node:
        return None
    clone = Node(node.val)
    for neighbor in node.neighbors:
        clone.neighbors.append(clone_wrong(neighbor))  # Infinite loop on cycles!
    return clone


# MISTAKE 2: Shallow copy of neighbors (points to ORIGINAL neighbor objects)
def clone_shallow(node: 'Node') -> 'Node':
    clone = Node(node.val)
    clone.neighbors = node.neighbors  # Wrong! These are the original nodes!
    return clone


# MISTAKE 3: Appending original neighbor instead of its clone
# cloned[curr].neighbors.append(neighbor)        # WRONG — original node
# cloned[curr].neighbors.append(cloned[neighbor]) # CORRECT — cloned node


# MISTAKE 4: Storing in map AFTER recursing (infinite recursion on cycles)
def clone_late_store(node: 'Node') -> 'Node':
    clone = Node(node.val)
    for neighbor in node.neighbors:
        clone.neighbors.append(clone_late_store(neighbor))  # Recursion hits node again before it's mapped!
    cloned[node] = clone  # Too late (assuming a global or closure `cloned` map) (assuming a global or closure  map) (assuming a global or closure  map)
    return clone
```

---

## Complexity Analysis

| Approach          | Time     | Space    | Notes                                  |
| ----------------- | -------- | -------- | -------------------------------------- |
| DFS (recursive)   | O(V + E) | O(V)     | Recursion stack can be up to O(V) deep |
| BFS               | O(V + E) | O(V)     | Queue-based, no stack overflow risk    |
| Iterative DFS     | O(V + E) | O(V)     | Explicit stack, no stack overflow risk |
| Three-pass (list) | O(n)     | O(1)     | Only for linked list variant           |

**Why O(V + E)?** We visit each node exactly once (V) and traverse each edge exactly once during neighbor iteration (E). The HashMap lookup is O(1) amortized.

**Recursion Stack Depth Warning**:
- Worst case (linear chain of V nodes): recursion depth = V.
- Python's default recursion limit is ~1000. Large linear graphs will raise `RecursionError`.
- **FANG follow-up**: Mention this proactively. Iterative BFS/DFS uses heap memory (queue/stack) instead of the call stack, avoiding this limit entirely.

---

## Interview Tips

1. **Clarify deep vs shallow copy**: "I'll create entirely new node objects with the same values and structure."
2. **Immediately mention the HashMap**: "I'll use a dictionary mapping original nodes to their clones to handle cycles and avoid duplicates."
3. **Explain cycle handling**: "I store each clone in the map before recursing into its neighbors, so if I encounter it again via a cycle, I return the existing clone."
4. **Verify clone references**: After coding, trace through an edge to confirm you're appending `cloned[neighbor]`, not `neighbor`.
5. **Know both BFS and DFS**: Start with whichever you're more comfortable with, but be ready to implement the other if asked.
6. **Mention the stack overflow risk** of recursive DFS for bonus points.

---

## Practice Problems

| #   | Problem                                         | LC #   | Difficulty | Key Concept                              |
| --- | ----------------------------------------------- | ------ | ---------- | ---------------------------------------- |
| 1   | Clone Graph                                     | 133    | Medium     | Core problem — HashMap + DFS/BFS         |
| 2   | Copy List with Random Pointer                   | 138    | Medium     | Deep copy with non-sequential pointers   |
| 3   | Clone N-ary Tree                                | 1490   | Medium     | Simpler structure, no cycles (Premium)   |
| 4   | Clone Binary Tree with Random Pointer           | 1485   | Medium     | Combines tree traversal + random pointer |
| 5   | Number of Connected Components in Undirected Graph | 323 | Medium     | Graph traversal foundation (DFS or BFS)  |
| 6   | Course Schedule (cycle detection)               | 207    | Medium     | Cycle detection in directed graph        |
| 7   | Reconstruct Itinerary                           | 332    | Hard       | Graph construction + DFS (Eulerian path) |

**Progression**:
- Start with **LC 1490** (no cycles, pure cloning practice).
- Then **LC 133** (add cycle handling).
- Then **LC 138** (different data structure, same pattern).
- Then **LC 1485** (combines tree + random pointer).
- Then **LC 323, 207, 332** for broader graph traversal fluency.

---

## Key Takeaways

1. **HashMap is the backbone**: Maps `original → clone`, serves as both visited set and identity map.
2. **Store clone BEFORE recursing**: Prevents infinite loops on cycles.
3. **Use cloned neighbors, never originals**: `clone.neighbors.append(dfs(neighbor))` not `clone.neighbors.append(neighbor)`.
4. **BFS and DFS both work**: BFS avoids stack overflow; DFS is more concise.
5. **Handle `None` input**: Return `None` for empty graph.
6. **The pattern generalizes**: Any "deep copy a structure with cross-references" uses the same HashMap approach.

---

## Next: [13-grid-problems.md](./13-grid-problems.md)

Learn common grid/island problems.

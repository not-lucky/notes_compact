# Clone Graph

> **Prerequisites:** [02-bfs-basics](./02-bfs-basics.md), [03-dfs-basics](./03-dfs-basics.md)

## Interview Context

Clone Graph is a FANG+ favorite because:

1. **Tests graph traversal**: BFS or DFS with a twist
2. **Deep copy concept**: Understanding references vs values
3. **HashMap for mapping**: Old node → new node
4. **Clean code skills**: Handling the recursive structure

This problem appears frequently at Meta and Google.

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

```python
class Node:
    def __init__(self, val=0, neighbors=None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []
```

---

## DFS Approach (Recursive)

```python
def clone_graph_dfs(node: 'Node') -> 'Node':
    """
    Clone graph using DFS with HashMap.

    Time: O(V + E)
    Space: O(V) for HashMap and recursion stack
    """
    if not node:
        return None

    # Map: original node -> cloned node
    cloned = {}

    def dfs(node: 'Node') -> 'Node':
        if node in cloned:
            return cloned[node]

        # Create clone
        clone = Node(node.val)
        cloned[node] = clone

        # Clone neighbors
        for neighbor in node.neighbors:
            clone.neighbors.append(dfs(neighbor))

        return clone

    return dfs(node)
```

---

## BFS Approach

```python
from collections import deque

def clone_graph_bfs(node: 'Node') -> 'Node':
    """
    Clone graph using BFS with HashMap.

    Time: O(V + E)
    Space: O(V)
    """
    if not node:
        return None

    # Create clone of starting node
    cloned = {node: Node(node.val)}
    queue = deque([node])

    while queue:
        curr = queue.popleft()

        for neighbor in curr.neighbors:
            if neighbor not in cloned:
                # Create clone of neighbor
                cloned[neighbor] = Node(neighbor.val)
                queue.append(neighbor)

            # Add cloned neighbor to current clone's neighbors
            cloned[curr].neighbors.append(cloned[neighbor])

    return cloned[node]
```

---

## Visual Walkthrough (DFS)

```
Original:
    1 --- 2
    |     |
    4 --- 3

DFS from node 1:

Step 1: Create clone of 1
        cloned = {1: 1'}
        Process neighbors of 1: [2, 4]

Step 2: Clone 2, add to 1's neighbors
        cloned = {1: 1', 2: 2'}
        1'.neighbors = [2']
        Process neighbors of 2: [1, 3]

Step 3: 1 already cloned, skip
        Clone 3, add to 2's neighbors
        cloned = {1: 1', 2: 2', 3: 3'}
        2'.neighbors = [1', 3']
        Process neighbors of 3: [2, 4]

Step 4: 2 already cloned, skip
        Clone 4, add to 3's neighbors
        cloned = {1: 1', 2: 2', 3: 3', 4: 4'}
        3'.neighbors = [2', 4']
        Process neighbors of 4: [1, 3]

Step 5: 1 and 3 already cloned
        4'.neighbors = [1', 3']

Step 6: Back to step 1, add 4' to 1's neighbors
        1'.neighbors = [2', 4']

Done! Return 1'
```

---

## Iterative DFS

```python
def clone_graph_iterative(node: 'Node') -> 'Node':
    """
    Clone graph using iterative DFS.

    Time: O(V + E)
    Space: O(V)
    """
    if not node:
        return None

    cloned = {node: Node(node.val)}
    stack = [node]

    while stack:
        curr = stack.pop()

        for neighbor in curr.neighbors:
            if neighbor not in cloned:
                cloned[neighbor] = Node(neighbor.val)
                stack.append(neighbor)

            cloned[curr].neighbors.append(cloned[neighbor])

    return cloned[node]
```

---

## Common Variations

### Clone Graph with Random Pointer

```python
class NodeRandom:
    def __init__(self, val=0, next=None, random=None):
        self.val = val
        self.next = next
        self.random = random


def copy_random_list(head: 'NodeRandom') -> 'NodeRandom':
    """
    Clone linked list with random pointers.

    Time: O(n)
    Space: O(n)
    """
    if not head:
        return None

    # First pass: create all clones
    cloned = {}
    curr = head
    while curr:
        cloned[curr] = NodeRandom(curr.val)
        curr = curr.next

    # Second pass: set next and random pointers
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

```python
class NaryNode:
    def __init__(self, val=0, children=None):
        self.val = val
        self.children = children if children else []


def clone_tree(root: 'NaryNode') -> 'NaryNode':
    """
    Clone N-ary tree.

    Time: O(n)
    Space: O(n)
    """
    if not root:
        return None

    cloned = {}

    def dfs(node):
        if node in cloned:
            return cloned[node]

        clone = NaryNode(node.val)
        cloned[node] = clone

        for child in node.children:
            clone.children.append(dfs(child))

        return clone

    return dfs(root)
```

---

## O(1) Space Approach (Three-Pass)

For linked list with random pointer, can achieve O(1) space:

```python
def copy_random_list_o1(head: 'NodeRandom') -> 'NodeRandom':
    """
    Clone with O(1) extra space using interleaving.

    Time: O(n)
    Space: O(1)
    """
    if not head:
        return None

    # Pass 1: Create clones and interleave
    # 1 -> 1' -> 2 -> 2' -> 3 -> 3'
    curr = head
    while curr:
        clone = NodeRandom(curr.val)
        clone.next = curr.next
        curr.next = clone
        curr = clone.next

    # Pass 2: Set random pointers
    curr = head
    while curr:
        if curr.random:
            curr.next.random = curr.random.next
        curr = curr.next.next

    # Pass 3: Separate lists
    dummy = NodeRandom(0)
    clone_curr = dummy
    curr = head

    while curr:
        clone_curr.next = curr.next
        curr.next = curr.next.next

        clone_curr = clone_curr.next
        curr = curr.next

    return dummy.next
```

---

## Edge Cases

```python
# 1. Empty graph
clone_graph(None)  # Return None

# 2. Single node, no neighbors
node = Node(1)
# Clone has val=1, empty neighbors

# 3. Single node, self-loop
node = Node(1)
node.neighbors = [node]
# Clone should reference itself, not original

# 4. Fully connected
# All nodes connected to all others

# 5. Linear chain
# 1 - 2 - 3 - 4
```

---

## Common Mistakes

```python
# WRONG: Not using HashMap (creates infinite recursion)
def clone_wrong(node):
    if not node:
        return None
    clone = Node(node.val)
    for neighbor in node.neighbors:
        clone.neighbors.append(clone_wrong(neighbor))  # Infinite loop!
    return clone


# WRONG: Shallow copy of neighbors
def clone_shallow(node):
    clone = Node(node.val)
    clone.neighbors = node.neighbors  # Points to original neighbors!


# WRONG: Adding original neighbors
cloned[curr].neighbors.append(neighbor)  # Should be cloned[neighbor]


# CORRECT: Map original to clone
cloned = {}
def dfs(node):
    if node in cloned:
        return cloned[node]  # Return existing clone
    clone = Node(node.val)
    cloned[node] = clone  # Store before processing neighbors
    for neighbor in node.neighbors:
        clone.neighbors.append(dfs(neighbor))
    return clone
```

---

## Complexity Analysis

| Approach          | Time     | Space |
| ----------------- | -------- | ----- |
| DFS               | O(V + E) | O(V)  |
| BFS               | O(V + E) | O(V)  |
| Three-pass (list) | O(n)     | O(1)  |

Space is for the HashMap (or interleaved list structure).

---

## Interview Tips

1. **Clarify deep vs shallow**: Deep copy creates new objects
2. **HashMap is key**: Maps original nodes to clones
3. **Handle cycles**: HashMap prevents infinite loops
4. **Check clone references**: Cloned neighbor, not original
5. **Know both BFS and DFS**: Either works

---

## Practice Problems

| #   | Problem                               | Difficulty | Key Variation       |
| --- | ------------------------------------- | ---------- | ------------------- |
| 1   | Clone Graph                           | Medium     | Core problem        |
| 2   | Copy List with Random Pointer         | Medium     | Linked list variant |
| 3   | Clone Binary Tree with Random Pointer | Medium     | Tree variant        |
| 4   | Clone N-ary Tree                      | Easy       | Simpler structure   |

---

## Key Takeaways

1. **HashMap for mapping**: Old node → new node
2. **Visit before recursing**: Prevents infinite loops
3. **Deep copy neighbors**: Use cloned neighbors, not originals
4. **BFS or DFS**: Both work equally well
5. **Handle null input**: Return null for null

---

## Next: [13-grid-problems.md](./13-grid-problems.md)

Learn common grid/island problems.

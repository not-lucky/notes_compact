# Solution: Copy List with Random Pointer Practice Problems

## Problem 1: Copy List with Random Pointer
### Problem Statement
A linked list of length `n` is given such that each node contains an additional random pointer, which could point to any node in the list, or null. Construct a deep copy of the list.

### Constraints
- `0 <= n <= 1000`
- `-10^4 <= Node.val <= 10^4`
- `Node.random` is null or is pointing to some node in the linked list.

### Example
Input: `head = [[7,null],[13,0],[11,4],[10,2],[1,0]]`
Output: `[[7,null],[13,0],[11,4],[10,2],[1,0]]`

### Python Implementation
```python
class Node:
    def __init__(self, x: int, next: 'Node' = None, random: 'Node' = None):
        self.val = int(x)
        self.next = next
        self.random = random

def copyRandomList(head: 'Node') -> 'Node':
    """
    Time Complexity: O(n)
    Space Complexity: O(1) (excluding the space for the new list)

    Interleaving technique to avoid O(n) space for hashmap.
    """
    if not head:
        return None

    # Step 1: Interleave copies
    curr = head
    while curr:
        new_node = Node(curr.val, curr.next)
        curr.next = new_node
        curr = new_node.next

    # Step 2: Set random pointers
    curr = head
    while curr:
        if curr.random:
            curr.next.random = curr.random.next
        curr = curr.next.next

    # Step 3: Separate lists
    curr = head
    new_head = head.next
    while curr:
        copy = curr.next
        curr.next = copy.next
        if copy.next:
            copy.next = copy.next.next
        curr = curr.next

    return new_head
```

---

## Problem 2: Clone Graph
### Problem Statement
Given a reference of a node in a connected undirected graph. Return a deep copy (clone) of the graph. Each node in the graph contains a value (`int`) and a list of its neighbors (`List[Node]`).

### Constraints
- The number of nodes in the graph is between `0` and `100`.
- `1 <= Node.val <= 100`
- `Node.val` is unique for each node.
- There are no repeated edges and no self-loops in the graph.
- The Graph is connected and all nodes can be visited starting from the given node.

### Example
Input: `adjList = [[2,4],[1,3],[2,4],[1,3]]`
Output: `[[2,4],[1,3],[2,4],[1,3]]`

### Python Implementation
```python
class GraphNode:
    def __init__(self, val=0, neighbors=None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []

def cloneGraph(node: 'GraphNode') -> 'GraphNode':
    """
    Time Complexity: O(V + E)
    Space Complexity: O(V)
    """
    if not node:
        return None

    old_to_new = {}

    def dfs(n):
        if n in old_to_new:
            return old_to_new[n]

        copy = GraphNode(n.val)
        old_to_new[n] = copy

        for neighbor in n.neighbors:
            copy.neighbors.append(dfs(neighbor))
        return copy

    return dfs(node)
```

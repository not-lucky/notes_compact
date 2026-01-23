# Clone Graph

## Practice Problems

### 1. Clone Graph
**Difficulty:** Medium
**Concept:** Core problem

```python
from typing import Optional, Dict

class Node:
    def __init__(self, val = 0, neighbors = None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []

def clone_graph(node: Optional['Node']) -> Optional['Node']:
    """
    Given a reference of a node in a connected undirected graph.
    Return a deep copy (clone) of the graph.

    Time: O(V + E)
    Space: O(V)
    """
    if not node:
        return None

    old_to_new: Dict['Node', 'Node'] = {}

    def dfs(curr: 'Node') -> 'Node':
        if curr in old_to_new:
            return old_to_new[curr]

        copy = Node(curr.val)
        old_to_new[curr] = copy

        for neighbor in curr.neighbors:
            copy.neighbors.append(dfs(neighbor))

        return copy

    return dfs(node)
```

### 2. Copy List with Random Pointer
**Difficulty:** Medium
**Concept:** Linked list variant

```python
from typing import Optional

class Node:
    def __init__(self, x: int, next: 'Node' = None, random: 'Node' = None):
        self.val = int(x)
        self.next = next
        self.random = random

def copy_random_list(head: Optional['Node']) -> Optional['Node']:
    """
    Clone a linked list where each node has a random pointer.

    Time: O(N)
    Space: O(N)
    """
    if not head:
        return None

    # Map: old node -> new node
    cloned = {}

    curr = head
    while curr:
        cloned[curr] = Node(curr.val)
        curr = curr.next

    curr = head
    while curr:
        if curr.next:
            cloned[curr].next = cloned[curr.next]
        if curr.random:
            cloned[curr].random = cloned[curr.random]
        curr = curr.next

    return cloned[head]
```

### 3. Clone N-ary Tree
**Difficulty:** Easy
**Concept:** Simpler structure

```python
from typing import Optional, List

class Node:
    def __init__(self, val=None, children=None):
        self.val = val
        self.children = children if children is not None else []

def clone_tree(root: Optional['Node']) -> Optional['Node']:
    """
    Clone an N-ary tree.

    Time: O(N)
    Space: O(N)
    """
    if not root:
        return None

    copy = Node(root.val)
    for child in root.children:
        copy.children.append(clone_tree(child))

    return copy
```

# Solutions: Copy List with Random Pointer

## 1. Copy List with Random Pointer

**Problem Statement**: A linked list of length `n` is given such that each node contains an additional random pointer, which could point to any node in the list, or `null`.
Construct a deep copy of the list. The deep copy should consist of exactly `n` brand new nodes, where each new node has its value set to the value of its corresponding original node. Both the `next` and `random` pointer of the new nodes should point to new nodes in the copied list such that the pointers in the original list and copied list represent the same list state. None of the pointers in the new list should point to nodes in the original list.

### Examples & Edge Cases

- **Example 1**: `head = [[7,null],[13,0],[11,4],[10,2],[1,0]]`.
- **Edge Case**: Empty list.
- **Edge Case**: `random` pointers pointing to itself or to nodes already processed.

### Optimal Python Solution

```python
class Node:
    def __init__(self, x: int, next: 'Node' = None, random: 'Node' = None):
        self.val = int(x)
        self.next = next
        self.random = random

def copyRandomList(head: 'Node') -> 'Node':
    """
    Three-step O(1) space approach:
    1. Create interleaved copies: A -> A' -> B -> B'
    2. Set random pointers for copies: A'.random = A.random.next
    3. Separate original and copy lists.
    """
    if not head:
        return None

    # Step 1: Create new nodes and interleave them
    curr = head
    while curr:
        new_node = Node(curr.val, curr.next)
        curr.next = new_node
        curr = new_node.next

    # Step 2: Set random pointers for the new nodes
    curr = head
    while curr:
        if curr.random:
            curr.next.random = curr.random.next
        curr = curr.next.next

    # Step 3: Separate the lists
    curr = head
    copy_head = head.next
    while curr:
        copy = curr.next
        curr.next = copy.next
        if copy.next:
            copy.next = copy.next.next
        curr = curr.next

    return copy_head
```

### Explanation

The interleaving technique is the most space-efficient way to map old nodes to new nodes. By placing each copy immediately after its original node (`A -> A'`), we can find the copy of any original node `X` by simply looking at `X.next`. This allows us to set `random` pointers easily: the copy of `curr.random` is `curr.random.next`. Finally, we restore the original list and extract the copy list.

### Complexity Analysis

- **Time Complexity**: O(n). We make three linear passes over the list.
- **Space Complexity**: O(1). We don't use any extra data structures (like a hashmap) to store the mapping.

---

## 2. Clone Graph

**Problem Statement**: Given a reference of a node in a connected undirected graph. Return a deep copy (clone) of the graph. Each node in the graph contains a value (int) and a list (List[Node]) of its neighbors.

### Examples & Edge Cases

- **Example 1**: `adjList = [[2,4],[1,3],[2,4],[1,3]]` -> `[[2,4],[1,3],[2,4],[1,3]]`
- **Edge Case**: Empty graph.
- **Edge Case**: Graph with cycles.

### Optimal Python Solution

```python
class Node:
    def __init__(self, val = 0, neighbors = None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []

def cloneGraph(node: 'Node') -> 'Node':
    """
    Use a HashMap to store the mapping from original nodes to their clones.
    Use DFS to traverse and clone the graph.
    """
    if not node:
        return None

    old_to_new = {}

    def dfs(curr):
        if curr in old_to_new:
            return old_to_new[curr]

        # Create clone and add to mapping before processing neighbors (to handle cycles)
        copy = Node(curr.val)
        old_to_new[curr] = copy

        for neighbor in curr.neighbors:
            copy.neighbors.append(dfs(neighbor))

        return copy

    return dfs(node)
```

### Explanation

We use a dictionary to keep track of nodes we've already cloned. When we visit a node, we first create its clone. Then, for each of its neighbors, we recursively call the cloning function. If a neighbor has already been cloned, we simply retrieve the clone from our dictionary. This handles cycles and ensures each node is only cloned once.

### Complexity Analysis

- **Time Complexity**: O(V + E), where `V` is the number of vertices and `E` is the number of edges. We visit each node and each edge once.
- **Space Complexity**: O(V). The dictionary stores a mapping for every node, and the recursion stack can go up to `V` deep.

---

## 3. Clone Binary Tree with Random Pointer

**Problem Statement**: Given a binary tree where each node has an additional `random` pointer. Return a deep copy of the tree.

### Optimal Python Solution

```python
def copyRandomBinaryTree(root: 'Node') -> 'Node':
    """
    Similar to Clone Graph, use a HashMap to store the mapping
    from original nodes to clones and traverse the tree.
    """
    if not root:
        return None

    mapping = {None: None}

    # Pass 1: Clone all nodes and store in mapping
    def clone_nodes(node):
        if not node: return
        mapping[node] = Node(node.val)
        clone_nodes(node.left)
        clone_nodes(node.right)

    clone_nodes(root)

    # Pass 2: Connect left, right, and random pointers
    def connect_pointers(node):
        if not node: return
        copy = mapping[node]
        copy.left = mapping.get(node.left)
        copy.right = mapping.get(node.right)
        copy.random = mapping.get(node.random)
        connect_pointers(node.left)
        connect_pointers(node.right)

    connect_pointers(root)
    return mapping[root]
```

### Explanation

Since tree nodes don't easily allow interleaving (like linked lists), a two-pass approach with a HashMap is the most straightforward. First, we traverse the tree (e.g., using DFS) to create all new nodes and store them in a map. In the second pass, we use the map to set all `left`, `right`, and `random` pointers to their corresponding clones.

### Complexity Analysis

- **Time Complexity**: O(n). We visit each node twice.
- **Space Complexity**: O(n). To store the mapping and for the recursion stack.

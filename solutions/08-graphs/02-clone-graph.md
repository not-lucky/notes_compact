# Clone Graph

## Problem Statement

Given a reference of a node in a connected undirected graph, return a deep copy of the graph.

Each node contains a value and a list of its neighbors.

**Example:**
```
Input: adjList = [[2,4],[1,3],[2,4],[1,3]]
Output: [[2,4],[1,3],[2,4],[1,3]]

Graph:
1 --- 2
|     |
4 --- 3
```

## Building Intuition

### Why This Works

The fundamental challenge in cloning a graph is that nodes reference each other through their neighbor lists, creating a chicken-and-egg problem. You can't fully create node A until you've created its neighbor B, but B might also need A as a neighbor. The hash map solves this elegantly by decoupling node creation from neighbor assignment.

When we encounter a node for the first time, we immediately create its clone and store the mapping. This clone initially has no neighbors - that's okay. As we traverse the graph, whenever we need a reference to a cloned node (to add to someone's neighbor list), we either find it in the map or create it first. The map serves as both a "visited" set (preventing infinite loops in cyclic graphs) and a translation table (original node to clone node).

The beauty is that by the time DFS completes, all neighbor lists are correctly populated. Each edge in the original graph is traversed exactly once in each direction, and each traversal adds the appropriate clone reference to a neighbor list.

### How to Discover This

When you see "deep copy" or "clone" for any data structure with cycles (graphs, linked lists with random pointers), think: "I need a mapping from original to clone." The pattern is always: (1) create clone nodes, (2) store the mapping, (3) use the mapping to wire up references. DFS or BFS determines the order of creation, but the hash map is the essential tool.

### Pattern Recognition

This is the **Structure Cloning with Hash Map** pattern. Recognize it when:
- You need to deep copy a data structure with arbitrary references
- The structure may contain cycles
- References must point to cloned objects, not originals

## When NOT to Use

- **When the structure is acyclic (like a tree)**: You can clone recursively without a hash map since there are no cycles to handle.
- **When shallow copy is acceptable**: If you only need to copy the structure, not the referenced objects, this is overkill.
- **When memory is extremely constrained**: The hash map requires O(V) extra space. For linked lists, the interleaving technique (O(1) space) is an alternative.
- **When nodes don't have unique identities**: If two nodes can be "equal" but different, you need a different approach (like using object IDs).

## Approach

### DFS with Hash Map
1. Use hash map to store mapping from original to cloned nodes
2. DFS through graph, cloning each node
3. Hash map prevents revisiting and enables neighbor linking

### BFS Alternative
Same logic but uses queue for traversal.

## Implementation

```python
class Node:
    def __init__(self, val=0, neighbors=None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []


def clone_graph(node: Node) -> Node:
    """
    Clone graph using DFS.

    Time: O(V + E) - visit each node and edge
    Space: O(V) - hash map + recursion stack
    """
    if not node:
        return None

    cloned = {}  # original node -> cloned node

    def dfs(original: Node) -> Node:
        if original in cloned:
            return cloned[original]

        # Create clone
        clone = Node(original.val)
        cloned[original] = clone

        # Clone neighbors
        for neighbor in original.neighbors:
            clone.neighbors.append(dfs(neighbor))

        return clone

    return dfs(node)


def clone_graph_bfs(node: Node) -> Node:
    """
    Clone graph using BFS.

    Time: O(V + E)
    Space: O(V)
    """
    if not node:
        return None

    from collections import deque

    cloned = {node: Node(node.val)}
    queue = deque([node])

    while queue:
        original = queue.popleft()

        for neighbor in original.neighbors:
            if neighbor not in cloned:
                cloned[neighbor] = Node(neighbor.val)
                queue.append(neighbor)

            cloned[original].neighbors.append(cloned[neighbor])

    return cloned[node]


def clone_graph_iterative_dfs(node: Node) -> Node:
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
        original = stack.pop()

        for neighbor in original.neighbors:
            if neighbor not in cloned:
                cloned[neighbor] = Node(neighbor.val)
                stack.append(neighbor)

            cloned[original].neighbors.append(cloned[neighbor])

    return cloned[node]
```

## Complexity Analysis

| Aspect | Complexity | Explanation |
|--------|------------|-------------|
| Time | O(V + E) | Visit each vertex and edge once |
| Space | O(V) | Hash map stores all nodes |

## Visual Walkthrough

```
Original Graph:
1 --- 2
|     |
4 --- 3

DFS from node 1:

Step 1: Visit 1
  cloned = {1: Node(1)}
  Process neighbors: [2, 4]

Step 2: Visit 2 (neighbor of 1)
  cloned = {1: Node(1), 2: Node(2)}
  Process neighbors: [1, 3]
  - 1 already cloned, return it
  - DFS(3)

Step 3: Visit 3
  cloned = {..., 3: Node(3)}
  Process neighbors: [2, 4]
  - 2 already cloned
  - DFS(4)

Step 4: Visit 4
  cloned = {..., 4: Node(4)}
  Process neighbors: [1, 3]
  - Both already cloned

Unwinding builds neighbor lists.
```

## Edge Cases

1. **Null node**: Return None
2. **Single node, no neighbors**: Clone just the node
3. **Single node, self-loop**: Clone handles cycles
4. **Fully connected graph**: Works correctly
5. **Long chain graph**: DFS depth could be deep

## Common Mistakes

1. **Creating nodes without hash map**: Leads to duplicate clones
2. **Infinite loop without visited check**: Hash map prevents this
3. **Shallow copy of neighbors list**: Must deep copy neighbors too
4. **Modifying original graph**: Should only read original

## Variations

### Copy List with Random Pointer
```python
class ListNode:
    def __init__(self, val=0, next=None, random=None):
        self.val = val
        self.next = next
        self.random = random


def copy_random_list(head: ListNode) -> ListNode:
    """
    Clone linked list with random pointers.

    Time: O(n)
    Space: O(n)
    """
    if not head:
        return None

    old_to_new = {}

    # First pass: create all nodes
    current = head
    while current:
        old_to_new[current] = ListNode(current.val)
        current = current.next

    # Second pass: set pointers
    current = head
    while current:
        clone = old_to_new[current]
        clone.next = old_to_new.get(current.next)
        clone.random = old_to_new.get(current.random)
        current = current.next

    return old_to_new[head]


def copy_random_list_O1_space(head: ListNode) -> ListNode:
    """
    Clone using interleaving technique.
    O(1) extra space (excluding output).
    """
    if not head:
        return None

    # Step 1: Interleave clones
    # A -> A' -> B -> B' -> C -> C'
    current = head
    while current:
        clone = ListNode(current.val, current.next)
        current.next = clone
        current = clone.next

    # Step 2: Set random pointers
    current = head
    while current:
        if current.random:
            current.next.random = current.random.next
        current = current.next.next

    # Step 3: Separate lists
    new_head = head.next
    current = head
    while current:
        clone = current.next
        current.next = clone.next
        clone.next = clone.next.next if clone.next else None
        current = current.next

    return new_head
```

### Clone N-ary Tree
```python
def clone_tree(root: 'Node') -> 'Node':
    """
    Clone N-ary tree.
    """
    if not root:
        return None

    clone = Node(root.val)
    clone.children = [clone_tree(child) for child in root.children]
    return clone
```

### Clone Binary Tree with Random Pointer
```python
def clone_binary_tree_random(root: 'NodeCopy') -> 'NodeCopy':
    """
    Clone binary tree where nodes have random pointers.
    """
    if not root:
        return None

    node_map = {}

    def clone(node):
        if not node:
            return None
        if node in node_map:
            return node_map[node]

        copy = NodeCopy(node.val)
        node_map[node] = copy

        copy.left = clone(node.left)
        copy.right = clone(node.right)
        copy.random = clone(node.random)

        return copy

    return clone(root)
```

## Related Problems

- **Copy List with Random Pointer** - Linked list version
- **Clone Binary Tree with Random Pointer** - Tree version
- **Clone N-ary Tree** - Simpler tree cloning
- **All Paths From Source to Target** - Graph traversal
- **Find if Path Exists in Graph** - Basic graph connectivity

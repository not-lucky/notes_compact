# Copy List with Random Pointer

## Practice Problems

### 1. Copy List with Random Pointer (HashMap)
**Difficulty:** Medium
**Key Technique:** HashMap (Old -> New)

```python
def copy_random_list_hash(head: Node) -> Node:
    """
    Time: O(n)
    Space: O(n)
    """
    if not head: return None
    old_to_new = {None: None}

    # Pass 1: Create new nodes
    curr = head
    while curr:
        old_to_new[curr] = Node(curr.val)
        curr = curr.next

    # Pass 2: Connect pointers
    curr = head
    while curr:
        copy = old_to_new[curr]
        copy.next = old_to_new[curr.next]
        copy.random = old_to_new[curr.random]
        curr = curr.next

    return old_to_new[head]
```

### 2. Copy List with Random Pointer (Interleaving)
**Difficulty:** Medium
**Key Technique:** Interleave -> Set Random -> Separate

```python
def copy_random_list_optimal(head: Node) -> Node:
    """
    Time: O(n)
    Space: O(1)
    """
    if not head: return None

    # Step 1: Interleave
    curr = head
    while curr:
        copy = Node(curr.val, curr.next)
        curr.next = copy
        curr = copy.next

    # Step 2: Random pointers
    curr = head
    while curr:
        if curr.random:
            curr.next.random = curr.random.next
        curr = curr.next.next

    # Step 3: Separate
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

### 3. Clone Graph
**Difficulty:** Medium
**Key Technique:** DFS/BFS + HashMap

```python
def clone_graph(node: 'Node') -> 'Node':
    """
    Time: O(V + E)
    Space: O(V)
    """
    if not node: return None
    old_to_new = {}

    def dfs(n):
        if n in old_to_new: return old_to_new[n]
        copy = Node(n.val)
        old_to_new[n] = copy
        for nei in n.neighbors:
            copy.neighbors.append(dfs(nei))
        return copy

    return dfs(node)
```

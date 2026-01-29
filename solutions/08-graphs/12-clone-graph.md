# Solutions: Clone Graph

## Practice Problems

| #   | Problem                               | Difficulty | Key Variation       |
| --- | ------------------------------------- | ---------- | ------------------- |
| 1   | Clone Graph                           | Medium     | Core problem        |
| 2   | Copy List with Random Pointer         | Medium     | Linked list variant |
| 3   | Clone Binary Tree with Random Pointer | Medium     | Tree variant        |
| 4   | Clone N-ary Tree                      | Easy       | Simpler structure   |

---

## 1. Clone Graph

### Problem Statement

Deep copy a connected undirected graph.

### Optimal Python Solution

```python
class Node:
    def __init__(self, val=0, neighbors=None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []

def cloneGraph(node: 'Node') -> 'Node':
    if not node: return None
    clones = {node: Node(node.val)}
    queue = deque([node])

    while queue:
        curr = queue.popleft()
        for neighbor in curr.neighbors:
            if neighbor not in clones:
                clones[neighbor] = Node(neighbor.val)
                queue.append(neighbor)
            clones[curr].neighbors.append(clones[neighbor])
    return clones[node]
```

### Explanation

- **Algorithm**: BFS with a hash map.
- **Mapping**: `clones` maps original nodes to their new copies.
- **Complexity**: Time O(V + E), Space O(V).

---

## 2. Copy List with Random Pointer

### Problem Statement

Clone a linked list where each node has a `next` and a `random` pointer.

### Optimal Python Solution (O(1) Space)

```python
class Node:
    def __init__(self, x: int, next: 'Node' = None, random: 'Node' = None):
        self.val = int(x)
        self.next = next
        self.random = random

def copyRandomList(head: 'Node') -> 'Node':
    if not head: return None

    # 1. Interleave clones
    curr = head
    while curr:
        new_node = Node(curr.val, curr.next)
        curr.next = new_node
        curr = new_node.next

    # 2. Set random pointers
    curr = head
    while curr:
        if curr.random:
            curr.next.random = curr.random.next
        curr = curr.next.next

    # 3. Separate lists
    dummy = Node(0)
    copy_curr = dummy
    curr = head
    while curr:
        copy_curr.next = curr.next
        curr.next = curr.next.next
        copy_curr = copy_curr.next
        curr = curr.next
    return dummy.next
```

### Explanation

- **Strategy**: Instead of a hash map, we interleave the original and copied nodes.
- **Complexity**: Time O(N), Space O(1) (excluding the output).

---

## 3. Clone Binary Tree with Random Pointer

### Problem Statement

Deep copy a binary tree where each node has a `random` pointer.

### Optimal Python Solution

```python
def copyRandomBinaryTree(root):
    if not root: return None
    clones = {}

    def get_clone(node):
        if not node: return None
        if node not in clones:
            clones[node] = Node(node.val)
            clones[node].left = get_clone(node.left)
            clones[node].right = get_clone(node.right)
            clones[node].random = get_clone(node.random)
        return clones[node]

    return get_clone(root)
```

---

## 4. Clone N-ary Tree

### Problem Statement

Deep copy an N-ary tree.

### Optimal Python Solution

```python
def cloneTree(root):
    if not root: return None
    clone = Node(root.val)
    for child in root.children:
        clone.children.append(cloneTree(child))
    return clone
```

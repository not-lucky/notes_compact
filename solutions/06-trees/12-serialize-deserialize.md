# Serialize and Deserialize Binary Tree Solutions

## 1. Serialize and Deserialize Binary Tree
**Problem Statement**: Design an algorithm to serialize and deserialize a binary tree. Serialization is the process of converting a data structure or object into a sequence of bits so that it can be stored in a file or memory buffer, or transmitted across a network connection link to be reconstructed later in the same or another computer environment.

### Examples & Edge Cases
- **Example 1**: `root = [1,2,3,None,None,4,5]` → Serialized: `"1,2,#,#,3,4,#,#,5,#,#"`
- **Edge Case - Empty Tree**: `root = None` → Serialized: `""`
- **Edge Case - Single Node**: `root = [1]` → Serialized: `"1,#,#"`

### Optimal Python Solution (Preorder DFS)
```python
class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

class Codec:
    def serialize(self, root: TreeNode) -> str:
        """Encodes a tree to a single string."""
        res = []
        def dfs(node):
            if not node:
                res.append("#")
                return
            # Add current node then children (Preorder)
            res.append(str(node.val))
            dfs(node.left)
            dfs(node.right)

        dfs(root)
        return ",".join(res)

    def deserialize(self, data: str) -> TreeNode:
        """Decodes your encoded data to tree."""
        if not data:
            return None

        # Use an iterator to cleanly consume values one by one
        vals = iter(data.split(","))

        def dfs():
            val = next(vals)
            if val == "#":
                return None

            node = TreeNode(int(val))
            # The structure of the recursive calls MUST match the serialization order
            node.left = dfs()
            node.right = dfs()
            return node

        return dfs()
```

### Explanation
1.  **Serialization Choice**: Preorder traversal (`Root, Left, Right`) is excellent for serialization because the root of the tree (or subtree) is always the first element processed.
2.  **Handling Nulls**: To preserve the structure, we MUST explicitly record `None` children (using a marker like `#`). A preorder traversal *without* null markers is insufficient to uniquely reconstruct a general binary tree.
3.  **Deserialization Logic**: We split the string and use an iterator. The recursive function `dfs()` creates a node, then calls itself for the left child, then for the right. Because of the preorder nature, the next value in the iterator is always the correct value for the current child we are building.

### Complexity Analysis
- **Time Complexity**: **O(n)**. We visit every node once during both serialization and deserialization.
- **Space Complexity**: **O(n)**. The serialized string and the recursion stack take $O(n)$ space.

---

## 2. Serialize and Deserialize BST
**Problem Statement**: Optimize the codec specifically for Binary Search Trees (BST).

### Optimal Python Solution (Compact Representation)
```python
class CodecBST:
    def serialize(self, root: TreeNode) -> str:
        # For BST, we only need preorder. No null markers needed!
        # Because we can use the BST property (min/max range) to find where children end.
        res = []
        def preorder(node):
            if node:
                res.append(str(node.val))
                preorder(node.left)
                preorder(node.right)
        preorder(root)
        return ",".join(res)

    def deserialize(self, data: str) -> TreeNode:
        if not data: return None
        vals = [int(x) for x in data.split(",")]
        idx = 0

        def build(lower, upper):
            nonlocal idx
            if idx == len(vals) or not (lower < vals[idx] < upper):
                return None

            val = vals[idx]
            idx += 1
            root = TreeNode(val)
            root.left = build(lower, val)
            root.right = build(val, upper)
            return root

        return build(float('-inf'), float('inf'))
```

### Explanation
- **Optimization**: For a BST, the inorder traversal is just the sorted preorder array. Since `Preorder + Inorder` uniquely identifies a tree, we only need to store the `Preorder`.
- **Space**: This saves space by not storing any `#` markers for null children.

### Complexity Analysis
- **Time Complexity**: **O(n)**.
- **Space Complexity**: **O(n)**.

---

## 3. Serialize and Deserialize N-ary Tree
**Problem Statement**: Serialize a tree where each node can have $N$ children.

### Optimal Python Solution
```python
class Node:
    def __init__(self, val=None, children=None):
        self.val = val
        self.children = children if children else []

class CodecNary:
    def serialize(self, root: 'Node') -> str:
        if not root: return ""
        res = []
        def dfs(node):
            res.append(str(node.val))
            res.append(str(len(node.children))) # Record number of children
            for child in node.children:
                dfs(child)
        dfs(root)
        return ",".join(res)

    def deserialize(self, data: str) -> 'Node':
        if not data: return None
        vals = iter(data.split(","))

        def dfs():
            val = int(next(vals))
            num_children = int(next(vals))
            node = Node(val, [])
            for _ in range(num_children):
                node.children.append(dfs())
            return node

        return dfs()
```

### Explanation
- **Structure**: For N-ary trees, knowing "where children end" is harder. We solve this by recording the **number of children** (`len(node.children)`) immediately after the node's value.

### Complexity Analysis
- **Time Complexity**: **O(n)**.
- **Space Complexity**: **O(n)**.

---

## 4. Construct Binary Tree from String
**Problem Statement**: Construct a binary tree from a string consisting of an integer followed by zero, one or two pairs of parentheses (e.g., `"4(2(3)(1))(6(5))"`).

### Optimal Python Solution
```python
def str2tree(s: str) -> TreeNode:
    if not s: return None

    # Find the value of the root
    i = 0
    while i < len(s) and (s[i].isdigit() or s[i] == '-'):
        i += 1
    root = TreeNode(int(s[:i]))

    if i < len(s):
        # Find the matching parentheses for the left child
        start = i
        count = 0
        while i < len(s):
            if s[i] == '(': count += 1
            elif s[i] == ')': count -= 1
            if count == 0: break
            i += 1
        root.left = str2tree(s[start+1:i])

        # If there's more, it's the right child
        if i + 1 < len(s):
            root.right = str2tree(s[i+2:-1])

    return root
```

### Complexity Analysis
- **Time Complexity**: **O(n²)** (due to string slicing). Can be optimized to $O(n)$ with global index.
- **Space Complexity**: **O(h)**.

---

## 5. Verify Preorder Serialization of a Binary Tree
**Problem Statement**: Without reconstructing the tree, verify if a string represents a valid preorder serialization.

### Optimal Python Solution
```python
def isValidSerialization(preorder: str) -> bool:
    # Use the concept of 'slots' or 'indegree/outdegree'
    # Initially, we have 1 slot (for the root)
    slots = 1

    for node in preorder.split(','):
        # Each node consumes 1 slot
        slots -= 1

        # If slots become negative, it's invalid
        if slots < 0:
            return False

        # If node is not null, it provides 2 new slots for children
        if node != '#':
            slots += 2

    # A valid tree leaves exactly 0 slots empty at the end
    return slots == 0
```

### Complexity Analysis
- **Time Complexity**: **O(n)**.
- **Space Complexity**: **O(1)** (if we use a generator instead of split).

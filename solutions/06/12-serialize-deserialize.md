# Serialize and Deserialize Binary Tree

## Practice Problems

### 1. Serialize and Deserialize Binary Tree
**Difficulty:** Hard
**Concept:** Preorder traversal with null markers

```python
from typing import Optional

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Codec:
    """
    Serializes and deserializes a binary tree using preorder traversal.
    Time: O(n)
    Space: O(n)
    """
    def serialize(self, root: Optional[TreeNode]) -> str:
        res = []
        def dfs(node):
            if not node:
                res.append("#")
                return
            res.append(str(node.val))
            dfs(node.left)
            dfs(node.right)
        dfs(root)
        return ",".join(res)

    def deserialize(self, data: str) -> Optional[TreeNode]:
        values = iter(data.split(","))
        def dfs():
            val = next(values)
            if val == "#":
                return None
            node = TreeNode(int(val))
            node.left = dfs()
            node.right = dfs()
            return node
        return dfs()
```

### 2. Serialize and Deserialize BST
**Difficulty:** Medium
**Concept:** Preorder only (BST property)

```python
class BSTCodec:
    """
    Serializes and deserializes a BST using preorder only.
    Time: O(n)
    Space: O(n)
    """
    def serialize(self, root: Optional[TreeNode]) -> str:
        res = []
        def dfs(node):
            if not node:
                return
            res.append(str(node.val))
            dfs(node.left)
            dfs(node.right)
        dfs(root)
        return ",".join(res)

    def deserialize(self, data: str) -> Optional[TreeNode]:
        if not data:
            return None
        values = [int(v) for v in data.split(",")]
        idx = 0

        def build(lower, upper):
            nonlocal idx
            if idx == len(values) or not (lower < values[idx] < upper):
                return None

            val = values[idx]
            idx += 1
            node = TreeNode(val)
            node.left = build(lower, val)
            node.right = build(val, upper)
            return node

        return build(float('-inf'), float('inf'))
```

### 3. Verify Preorder Serialization of a Binary Tree
**Difficulty:** Medium
**Concept:** Indegree/outdegree count

```python
def is_valid_serialization(preorder: str) -> bool:
    """
    Verifies if a preorder traversal string is a valid serialization.
    Time: O(n)
    Space: O(1)
    """
    slots = 1 # root slot
    for node in preorder.split(","):
        slots -= 1 # use one slot
        if slots < 0:
            return False
        if node != "#":
            slots += 2 # add two slots for children
    return slots == 0
```

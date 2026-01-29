# Serialize and Deserialize Binary Tree

> **Prerequisites:** [02-tree-traversals](./02-tree-traversals.md), [03-level-order-traversal](./03-level-order-traversal.md)

## Interview Context

Serialization is important because:

1. **Classic interview problem**: Frequently asked at Google, Meta, Amazon
2. **Tests design skills**: Multiple valid approaches, need to justify choice
3. **Practical applications**: Storing trees in databases, network transmission
4. **Covers multiple concepts**: Traversals, string manipulation, design

This is a **Hard** problem on LeetCode but very common in interviews.

---

## Core Concept: What is Serialization?

Serialization converts a data structure into a format that can be stored or transmitted and later reconstructed.

```
Tree:                Serialized:
       1             "1,2,#,#,3,4,#,#,5,#,#" (preorder)
      / \            or
     2   3           "1,2,3,#,#,4,5" (level-order)
        / \
       4   5

# represents null
```

---

## Approach 1: Preorder DFS

### Serialization

```python
class Codec:
    """
    Serialize/deserialize using preorder traversal.

    LeetCode 297: Serialize and Deserialize Binary Tree
    """

    def serialize(self, root: TreeNode) -> str:
        """
        Encode tree to string using preorder.

        Time: O(n)
        Space: O(n)
        """
        result = []

        def dfs(node):
            if not node:
                result.append("#")
                return

            result.append(str(node.val))
            dfs(node.left)
            dfs(node.right)

        dfs(root)
        return ",".join(result)
```

### Deserialization

```python
    def deserialize(self, data: str) -> TreeNode:
        """
        Decode string to tree.

        Time: O(n)
        Space: O(n)
        """
        if not data:
            return None

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

### Visual Walkthrough

```
Tree:
       1
      / \
     2   3
        / \
       4   5

Serialize (preorder: Root, Left, Right):
- Visit 1: output "1"
- Visit 2: output "2"
- Visit 2.left (null): output "#"
- Visit 2.right (null): output "#"
- Visit 3: output "3"
- Visit 4: output "4"
- Visit 4.left (null): output "#"
- Visit 4.right (null): output "#"
- Visit 5: output "5"
- Visit 5.left (null): output "#"
- Visit 5.right (null): output "#"

Result: "1,2,#,#,3,4,#,#,5,#,#"

Deserialize:
- Read "1" → create node(1)
- Read "2" → create node(2), attach as left of 1
- Read "#" → null (left of 2)
- Read "#" → null (right of 2)
- Read "3" → create node(3), attach as right of 1
- ... and so on
```

---

## Approach 2: Level-Order BFS

```python
from collections import deque

class CodecBFS:
    """Serialize/deserialize using level-order traversal."""

    def serialize(self, root: TreeNode) -> str:
        """
        Encode using BFS (level-order).

        Time: O(n)
        Space: O(n)
        """
        if not root:
            return ""

        result = []
        queue = deque([root])

        while queue:
            node = queue.popleft()

            if node:
                result.append(str(node.val))
                queue.append(node.left)
                queue.append(node.right)
            else:
                result.append("#")

        # Remove trailing nulls (optional optimization)
        while result and result[-1] == "#":
            result.pop()

        return ",".join(result)

    def deserialize(self, data: str) -> TreeNode:
        """
        Decode using BFS.

        Time: O(n)
        Space: O(n)
        """
        if not data:
            return None

        values = data.split(",")
        root = TreeNode(int(values[0]))
        queue = deque([root])
        i = 1

        while queue and i < len(values):
            node = queue.popleft()

            # Left child
            if i < len(values) and values[i] != "#":
                node.left = TreeNode(int(values[i]))
                queue.append(node.left)
            i += 1

            # Right child
            if i < len(values) and values[i] != "#":
                node.right = TreeNode(int(values[i]))
                queue.append(node.right)
            i += 1

        return root
```

---

## Approach 3: Parentheses Notation

```python
class CodecParens:
    """Use parentheses to denote structure."""

    def serialize(self, root: TreeNode) -> str:
        """
        Format: val(left)(right)
        Example: 1(2()(4))(3)

        Time: O(n)
        Space: O(n)
        """
        if not root:
            return ""

        left = self.serialize(root.left)
        right = self.serialize(root.right)

        if not left and not right:
            return str(root.val)

        return f"{root.val}({left})({right})"

    def deserialize(self, data: str) -> TreeNode:
        """
        Parse parentheses notation.

        Time: O(n)
        Space: O(n)
        """
        if not data:
            return None

        # Find value (everything before first '(')
        paren_idx = data.find('(')
        if paren_idx == -1:
            return TreeNode(int(data))

        val = int(data[:paren_idx])
        node = TreeNode(val)

        # Find matching parentheses for left and right
        # Left: from first '(' to its matching ')'
        left_start = paren_idx + 1
        count = 1
        i = left_start

        while count > 0:
            if data[i] == '(':
                count += 1
            elif data[i] == ')':
                count -= 1
            i += 1

        left_end = i - 1
        right_start = i + 1  # Skip '(' after left's ')'
        right_end = len(data) - 1  # Last ')'

        node.left = self.deserialize(data[left_start:left_end])
        node.right = self.deserialize(data[right_start:right_end])

        return node
```

---

## BST Serialization (Preorder Only)

For BST, we only need preorder because BST property provides ordering.

```python
class CodecBST:
    """
    Serialize BST using preorder only (no null markers needed).

    LeetCode 449: Serialize and Deserialize BST
    """

    def serialize(self, root: TreeNode) -> str:
        """
        Just preorder values (BST can be reconstructed).

        Time: O(n)
        Space: O(n)
        """
        result = []

        def preorder(node):
            if node:
                result.append(str(node.val))
                preorder(node.left)
                preorder(node.right)

        preorder(root)
        return ",".join(result)

    def deserialize(self, data: str) -> TreeNode:
        """
        Reconstruct BST from preorder.

        Time: O(n)
        Space: O(n)
        """
        if not data:
            return None

        values = [int(x) for x in data.split(",")]
        idx = [0]

        def build(min_val, max_val):
            if idx[0] >= len(values):
                return None

            val = values[idx[0]]
            if val < min_val or val > max_val:
                return None

            idx[0] += 1
            node = TreeNode(val)
            node.left = build(min_val, val)
            node.right = build(val, max_val)
            return node

        return build(float('-inf'), float('inf'))
```

---

## N-ary Tree Serialization

```python
class CodecNary:
    """Serialize N-ary tree."""

    def serialize(self, root: 'Node') -> str:
        """
        Use # to mark end of children list.

        Example: 1[3,5,6]2[#]4[#]#
        Or simpler: 1,3,3,5,6,2,#,4,# (value, num_children, children...)
        """
        if not root:
            return ""

        result = []

        def dfs(node):
            result.append(str(node.val))
            result.append(str(len(node.children)))
            for child in node.children:
                dfs(child)

        dfs(root)
        return ",".join(result)

    def deserialize(self, data: str) -> 'Node':
        if not data:
            return None

        values = iter(data.split(","))

        def dfs():
            val = int(next(values))
            num_children = int(next(values))
            node = Node(val, [])
            for _ in range(num_children):
                node.children.append(dfs())
            return node

        return dfs()
```

---

## Complexity Analysis

| Approach        | Time (Serialize) | Time (Deserialize) | Space |
| --------------- | ---------------- | ------------------ | ----- |
| Preorder DFS    | O(n)             | O(n)               | O(n)  |
| Level-order BFS | O(n)             | O(n)               | O(n)  |
| BST (no nulls)  | O(n)             | O(n)               | O(n)  |
| Parentheses     | O(n)             | O(n²)\*            | O(n)  |

\*Parentheses parsing can be O(n²) due to string operations; can be optimized.

---

## Trade-offs Between Approaches

| Approach     | Pros                   | Cons                    |
| ------------ | ---------------------- | ----------------------- |
| Preorder     | Simple, intuitive      | Lots of null markers    |
| Level-order  | Natural representation | Same null markers issue |
| Parentheses  | Clear structure        | Complex parsing         |
| BST preorder | No null markers        | Only works for BST      |

---

## Edge Cases

```python
# 1. Empty tree
root = None
# → serialize: "" or "#" (design choice)
# → deserialize: None

# 2. Single node
root = TreeNode(1)
# → serialize: "1,#,#" (preorder) or "1" (level-order optimized)

# 3. Skewed tree
#     1
#      \
#       2
#        \
#         3
# → serialize: "1,#,2,#,3,#,#"

# 4. Negative values
root = TreeNode(-1)
# → serialize: "-1,#,#"

# 5. Large values
root = TreeNode(2147483647)
# → Handle integer range properly
```

---

## Interview Tips

1. **Choose your approach**: Preorder is usually simplest to explain
2. **Clarify format**: What's the null representation? Delimiter?
3. **Handle edge cases**: Empty tree, single node, negative values
4. **Discuss trade-offs**: Why preorder over level-order?
5. **BST is special case**: Mention no null markers needed

---

## Practice Problems

| #   | Problem                               | Difficulty | Key Concept               |
| --- | ------------------------------------- | ---------- | ------------------------- |
| 1   | Serialize and Deserialize Binary Tree | Hard       | General binary tree       |
| 2   | Serialize and Deserialize BST         | Medium     | BST - no null markers     |
| 3   | Serialize and Deserialize N-ary Tree  | Hard       | N-ary with child count    |
| 4   | Construct Binary Tree from String     | Medium     | Parentheses format        |
| 5   | Verify Preorder Serialization         | Medium     | Validate without building |

---

## Key Takeaways

1. **Preorder + nulls**: Sufficient for any binary tree
2. **BST special case**: Preorder only (BST property handles order)
3. **Level-order**: More intuitive visualization
4. **Iterator pattern**: Use `iter()` for clean deserialization
5. **Design choices**: Delimiter, null representation matter

---

## Next: [13-binary-tree-to-list.md](./13-binary-tree-to-list.md)

Learn to convert binary trees to linked lists.

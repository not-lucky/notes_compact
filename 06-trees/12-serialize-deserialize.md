# Serialize and Deserialize Binary Tree

> **Prerequisites:** [02-tree-traversals](./02-tree-traversals.md), [03-level-order-traversal](./03-level-order-traversal.md)

## Interview Context

Serialization is important because:

1. **Classic interview problem**: Frequently asked at Google, Meta, Amazon.
2. **Tests design skills**: Multiple valid approaches, need to justify choice.
3. **Practical applications**: Storing trees in databases, network transmission.
4. **Covers multiple concepts**: Traversals, string manipulation, design.

This is a **Hard** problem on LeetCode but very common in interviews.

---

## Core Concept: What is Serialization?

Serialization converts a data structure into a format that can be stored or transmitted and later reconstructed.

```text
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
from typing import Optional

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class CodecDFS:
    r"""
    Serialize/deserialize using preorder traversal.

    LeetCode 297: Serialize and Deserialize Binary Tree
    """

    def serialize(self, root: Optional[TreeNode]) -> str:
        r"""
        Encode tree to string using preorder.

        Time Complexity:  $\mathcal{O}(N)$ where $N$ is the number of nodes.
        Space Complexity: $\mathcal{O}(N)$ worst-case for the recursion stack (skewed tree) and the result list.
        """
        result = []

        def dfs(node: Optional[TreeNode]) -> None:
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
    def deserialize(self, data: str) -> Optional[TreeNode]:
        r"""
        Decode string back to a tree.

        Time Complexity:  $\mathcal{O}(N)$ where $N$ is the number of tokens in the string.
        Space Complexity: $\mathcal{O}(N)$ for the recursion stack and the `values` iterator.
        """
        if not data:
            return None

        # iter() allows us to process elements sequentially in O(1) time per element
        values = iter(data.split(","))

        def dfs() -> Optional[TreeNode]:
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

```text
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
- Read "1" -> create node(1)
- Read "2" -> create node(2), attach as left of 1
- Read "#" -> null (left of 2)
- Read "#" -> null (right of 2)
- Read "3" -> create node(3), attach as right of 1
- ... and so on
```

---

## Approach 2: Level-Order BFS

```python
from collections import deque
from typing import Optional

class CodecBFS:
    r"""Serialize/deserialize using level-order traversal."""

    def serialize(self, root: Optional[TreeNode]) -> str:
        r"""
        Encode using BFS (level-order).

        Time Complexity:  $\mathcal{O}(N)$
        Space Complexity: $\mathcal{O}(W)$ where $W$ is max width of the tree, up to $\approx N/2$ for the queue.
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

        # Remove trailing nulls (optional optimization to save space)
        while result and result[-1] == "#":
            result.pop()

        return ",".join(result)

    def deserialize(self, data: str) -> Optional[TreeNode]:
        r"""
        Decode using BFS.

        Time Complexity:  $\mathcal{O}(N)$
        Space Complexity: $\mathcal{O}(W)$ where $W$ is the max width of the tree (for the queue).
        """
        if not data:
            return None

        values = data.split(",")
        root = TreeNode(int(values[0]))
        queue = deque([root])
        i = 1

        while queue and i < len(values):
            node = queue.popleft()

            # Process Left child
            if i < len(values) and values[i] != "#":
                node.left = TreeNode(int(values[i]))
                queue.append(node.left)
            i += 1

            # Process Right child
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
    r"""Use parentheses to denote structure."""

    def serialize(self, root: Optional[TreeNode]) -> str:
        r"""
        Format: val(left)(right)
        Example: 1(2)(3(4)(5))

        Time Complexity:  $\mathcal{O}(N)$
        Space Complexity: $\mathcal{O}(N)$ worst-case for the call stack.
        """
        if not root:
            return ""

        left = self.serialize(root.left)
        right = self.serialize(root.right)

        # Optimization: omit empty children if leaf node
        if not left and not right:
            return str(root.val)

        return f"{root.val}({left})({right})"

    def deserialize(self, data: str) -> Optional[TreeNode]:
        r"""
        Parse parentheses notation linearly.

        Time Complexity:  $\mathcal{O}(N)$ as each character is processed at most a constant number of times.
        Space Complexity: $\mathcal{O}(N)$ worst-case for recursion stack depth.
        """
        if not data:
            return None

        i = [0]
        n = len(data)

        def parse_node() -> Optional[TreeNode]:
            if i[0] >= n or data[i[0]] == ')':
                return None

            # Parse numeric value
            start = i[0]
            while i[0] < n and (data[i[0]].isdigit() or data[i[0]] == '-'):
                i[0] += 1

            if start == i[0]:  # No valid number parsed
                return None

            val = int(data[start:i[0]])
            node = TreeNode(val)

            # Check for left child
            if i[0] < n and data[i[0]] == '(':
                i[0] += 1  # consume '('
                node.left = parse_node()
                i[0] += 1  # consume ')'

            # Check for right child
            if i[0] < n and data[i[0]] == '(':
                i[0] += 1  # consume '('
                node.right = parse_node()
                i[0] += 1  # consume ')'

            return node

        return parse_node()
```

---

## BST Serialization (Preorder Only)

For BST, we only need a preorder traversal. The BST property provides the strict ordering required to distinguish between left and right branches without needing `#` null markers.

```python
class CodecBST:
    r"""
    Serialize BST using preorder only (no null markers needed).

    LeetCode 449: Serialize and Deserialize BST
    """

    def serialize(self, root: Optional[TreeNode]) -> str:
        r"""
        Just preorder values (BST can be mathematically reconstructed).

        Time Complexity:  $\mathcal{O}(N)$
        Space Complexity: $\mathcal{O}(N)$ for result list and call stack.
        """
        result = []

        def preorder(node: Optional[TreeNode]) -> None:
            if node:
                result.append(str(node.val))
                preorder(node.left)
                preorder(node.right)

        preorder(root)
        return ",".join(result)

    def deserialize(self, data: str) -> Optional[TreeNode]:
        r"""
        Reconstruct BST dynamically from preorder traversal bounds.

        Time Complexity:  $\mathcal{O}(N)$ using index tracking.
        Space Complexity: $\mathcal{O}(N)$ worst-case for recursion stack.
        """
        if not data:
            return None

        values = [int(x) for x in data.split(",")]
        idx = [0]

        def build(min_val: float, max_val: float) -> Optional[TreeNode]:
            if idx[0] >= len(values):
                return None

            val = values[idx[0]]

            # If the current value doesn't fit the valid BST range, it doesn't belong here
            if not (min_val < val < max_val):
                return None

            idx[0] += 1
            node = TreeNode(val)

            # Left subtree values must be smaller than the current node's value
            node.left = build(min_val, val)

            # Right subtree values must be larger than the current node's value
            node.right = build(val, max_val)

            return node

        return build(float('-inf'), float('inf'))
```

---

## N-ary Tree Serialization

```python
class Node:
    def __init__(self, val: int = 0, children: Optional[list['Node']] = None):
        self.val = val
        self.children = children if children is not None else []

class CodecNary:
    r"""Serialize N-ary tree."""

    def serialize(self, root: Optional[Node]) -> str:
        r"""
        Store value followed by its number of children, then its children.
        Format: value, num_children, children...

        Time Complexity:  $\mathcal{O}(N)$
        Space Complexity: $\mathcal{O}(N)$
        """
        if not root:
            return ""

        result = []

        def dfs(node: Node) -> None:
            result.append(str(node.val))
            result.append(str(len(node.children)))
            for child in node.children:
                dfs(child)

        dfs(root)
        return ",".join(result)

    def deserialize(self, data: str) -> Optional[Node]:
        r"""
        Time Complexity:  $\mathcal{O}(N)$
        Space Complexity: $\mathcal{O}(N)$
        """
        if not data:
            return None

        values = iter(data.split(","))

        def dfs() -> Node:
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

| Approach | Time (Serialize) | Time (Deserialize) | Space |
| :--- | :--- | :--- | :--- |
| **Preorder DFS** | $\mathcal{O}(N)$ | $\mathcal{O}(N)$ | $\mathcal{O}(N)$ |
| **Level-order BFS** | $\mathcal{O}(N)$ | $\mathcal{O}(N)$ | $\mathcal{O}(W)$ queue width |
| **BST (no nulls)** | $\mathcal{O}(N)$ | $\mathcal{O}(N)$ | $\mathcal{O}(N)$ |
| **Parentheses** | $\mathcal{O}(N)$ | $\mathcal{O}(N)$ linearly optimized | $\mathcal{O}(N)$ call stack |

---

## Trade-offs Between Approaches

| Approach | Pros | Cons |
| :--- | :--- | :--- |
| **Preorder** | Simple, intuitive | Lots of null markers required |
| **Level-order** | Natural representation | Lots of null markers required |
| **Parentheses** | Clear structure visually | Complex parsing |
| **BST preorder** | No null markers needed | Only works for valid BSTs |

---

## Edge Cases

```python
# 1. Empty tree
root = None
# -> serialize: "" or "#" (design choice)
# -> deserialize: None

# 2. Single node
root = TreeNode(1)
# -> serialize: "1,#,#" (preorder) or "1" (level-order optimized)

# 3. Skewed tree
#     1
#      \
#       2
#        \
#         3
# -> serialize: "1,#,2,#,3,#,#"

# 4. Negative values
root = TreeNode(-1)
# -> serialize: "-1,#,#"

# 5. Large values
root = TreeNode(2147483647)
# -> Handle integer range properly (Python does this implicitly, but C++/Java requires long)
```

---

## Interview Tips

1. **Choose your approach**: Preorder is usually simplest to explain.
2. **Clarify format**: What's the null representation? Delimiter?
3. **Handle edge cases**: Empty tree, single node, negative values.
4. **Discuss trade-offs**: Why preorder over level-order?
5. **BST is special case**: Mention no null markers needed due to strict bounded logic.

---

## Practice Problems

| # | Problem | Difficulty | Key Concept |
| :--- | :--- | :--- | :--- |
| 1 | Serialize and Deserialize Binary Tree | Hard | General binary tree |
| 2 | Serialize and Deserialize BST | Medium | BST - no null markers |
| 3 | Serialize and Deserialize N-ary Tree | Hard | N-ary with child count |
| 4 | Construct Binary Tree from String | Medium | Parentheses format |
| 5 | Verify Preorder Serialization | Medium | Validate without building |

---

## Key Takeaways

1. **Preorder + nulls**: Sufficient for any binary tree.
2. **BST special case**: Preorder only (BST mathematical property handles order implicitly).
3. **Level-order**: More intuitive visualization and good for horizontal data mapping.
4. **Iterator pattern**: Use `iter(data)` in Python for clean $\mathcal{O}(1)$ sequential chunk deserialization without mutating arrays.
5. **Design choices**: Delimiter choice, trailing null optimization, and base-case representations matter.

---

<details>
<summary><b>Python Runner Script (For testing all variations)</b></summary>

```python
if __name__ == "__main__":
    # Test Tree:
    #      1
    #     / \
    #    2   3
    #       / \
    #      4   5
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.right = TreeNode(3, TreeNode(4), TreeNode(5))

    print("--- 1. Preorder DFS ---")
    codec_dfs = CodecDFS()
    dfs_str = codec_dfs.serialize(root)
    print("Serialized:", dfs_str)
    dfs_des = codec_dfs.deserialize(dfs_str)
    print("Deserialized Root Val:", dfs_des.val, "| Left:", dfs_des.left.val)

    print("\n--- 2. Level-order BFS ---")
    codec_bfs = CodecBFS()
    bfs_str = codec_bfs.serialize(root)
    print("Serialized:", bfs_str)
    bfs_des = codec_bfs.deserialize(bfs_str)
    print("Deserialized Root Val:", bfs_des.val, "| Left:", bfs_des.left.val)

    print("\n--- 3. Parentheses Notation ---")
    codec_parens = CodecParens()
    parens_str = codec_parens.serialize(root)
    print("Serialized:", parens_str)
    parens_des = codec_parens.deserialize(parens_str)
    print("Deserialized Root Val:", parens_des.val, "| Left:", parens_des.left.val)

    print("\n--- 4. BST Optimization ---")
    bst_root = TreeNode(2, TreeNode(1), TreeNode(3))
    codec_bst = CodecBST()
    bst_str = codec_bst.serialize(bst_root)
    print("Serialized (No Nulls):", bst_str)
    bst_des = codec_bst.deserialize(bst_str)
    print("Deserialized BST Val:", bst_des.val, "| Left:", bst_des.left.val)

    print("\n--- 5. N-ary Tree ---")
    nary_root = Node(1, [Node(3, [Node(5), Node(6)]), Node(2), Node(4)])
    codec_nary = CodecNary()
    nary_str = codec_nary.serialize(nary_root)
    print("Serialized:", nary_str)
    nary_des = codec_nary.deserialize(nary_str)
    print("Deserialized N-ary Val:", nary_des.val, "| Children len:", len(nary_des.children))
```

</details>

## Next: [13-binary-tree-to-list.md](./13-binary-tree-to-list.md)

Learn to convert binary trees to linked lists.
# Solution: Serialize and Deserialize Binary Tree Practice Problems

## Problem 1: Serialize and Deserialize Binary Tree
### Problem Statement
Serialization is the process of converting a data structure or object into a sequence of bits so that it can be stored in a file or memory buffer, or transmitted across a network connection link to be reconstructed later in the same or another computer environment.

Design an algorithm to serialize and deserialize a binary tree. There is no restriction on how your serialization/deserialization algorithm should work. You just need to ensure that a binary tree can be serialized to a string and this string can be deserialized to the original tree structure.

### Constraints
- The number of nodes in the tree is in the range `[0, 10^4]`.
- `-1000 <= Node.val <= 1000`

### Example
Input: `root = [1,2,3,null,null,4,5]`
Output: `[1,2,3,null,null,4,5]`

### Python Implementation
```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Codec:
    def serialize(self, root):
        """Encodes a tree to a single string."""
        def dfs(node):
            if not node:
                res.append("null")
                return
            res.append(str(node.val))
            dfs(node.left)
            dfs(node.right)

        res = []
        dfs(root)
        return ",".join(res)

    def deserialize(self, data):
        """Decodes your encoded data to tree."""
        def dfs():
            val = next(vals)
            if val == "null":
                return None
            node = TreeNode(int(val))
            node.left = dfs()
            node.right = dfs()
            return node

        vals = iter(data.split(","))
        return dfs()
```

---

## Problem 2: Serialize and Deserialize BST
### Problem Statement
Design an algorithm to serialize and deserialize a binary search tree. There is no restriction on how your serialization/deserialization algorithm should work. You just need to ensure that a binary search tree can be serialized to a string and this string can be deserialized to the original BST structure.

The encoded string should be as compact as possible.

### Constraints
- The number of nodes in the tree is in the range `[0, 10^4]`.
- `0 <= Node.val <= 10^4`
- The input tree is guaranteed to be a binary search tree.

### Example
Input: `root = [2,1,3]`
Output: `[2,1,3]`

### Python Implementation
```python
class Codec:
    def serialize(self, root):
        """Encodes a tree to a single string."""
        res = []
        def preorder(node):
            if node:
                res.append(str(node.val))
                preorder(node.left)
                preorder(node.right)
        preorder(root)
        return ",".join(res)

    def deserialize(self, data):
        """Decodes your encoded data to tree."""
        if not data:
            return None
        vals = [int(v) for v in data.split(",")]
        def build(lower, upper):
            if not vals or not (lower < vals[0] < upper):
                return None
            val = vals.pop(0)
            node = TreeNode(val)
            node.left = build(lower, val)
            node.right = build(val, upper)
            return node
        return build(float('-inf'), float('inf'))
```

---

## Problem 3: Serialize and Deserialize N-ary Tree
### Problem Statement
Design an algorithm to serialize and deserialize an N-ary tree. An N-ary tree is a rooted tree in which each node has no more than N children. There is no restriction on how your serialization/deserialization algorithm should work. You just need to ensure that an N-ary tree can be serialized to a string and this string can be deserialized to the original tree structure.

### Constraints
- The number of nodes in the tree is in the range `[0, 10^4]`.
- `0 <= Node.val <= 10^4`
- The N-ary tree height is less than or equal to `1000`.

### Python Implementation
```python
class Node:
    def __init__(self, val=None, children=None):
        self.val = val
        self.children = children if children else []

class Codec:
    def serialize(self, root):
        """Encodes a tree to a single string."""
        if not root:
            return ""
        res = []
        def dfs(node):
            res.append(str(node.val))
            res.append(str(len(node.children)))
            for child in node.children:
                dfs(child)
        dfs(root)
        return ",".join(res)

    def deserialize(self, data):
        """Decodes your encoded data to tree."""
        if not data:
            return None
        vals = iter(data.split(","))
        def dfs():
            val = int(next(vals))
            size = int(next(vals))
            node = Node(val, [])
            for _ in range(size):
                node.children.append(dfs())
            return node
        return dfs()
```

---

## Problem 4: Construct Binary Tree from String
### Problem Statement
You need to construct a binary tree from a string consisting of parenthesis and integers.

The whole input represents a binary tree. It contains an integer followed by zero, one or two pairs of parenthesis. The first pair of parenthesis contains a child binary tree and the second pair of parenthesis contains another child binary tree.

### Constraints
- `0 <= s.length <= 5 * 10^4`
- `s` consists of digits, `'('`, `')'`, and `'-'`.

### Example
Input: `s = "4(2(3)(1))(6(5))"`
Output: `[4,2,6,3,1,5]`

### Python Implementation
```python
def str2tree(s: str) -> TreeNode:
    """
    Time Complexity: O(n)
    Space Complexity: O(h)
    """
    if not s:
        return None

    i = 0
    while i < len(s) and (s[i].isdigit() or s[i] == '-'):
        i += 1
    val = int(s[:i])
    root = TreeNode(val)

    if i < len(s):
        start = i
        count = 0
        while i < len(s):
            if s[i] == '(': count += 1
            elif s[i] == ')': count -= 1
            if count == 0: break
            i += 1
        root.left = str2tree(s[start+1:i])

        i += 1
        if i < len(s):
            root.right = str2tree(s[i+1:-1])

    return root
```

---

## Problem 5: Verify Preorder Serialization of a Binary Tree
### Problem Statement
One way to serialize a binary tree is to use preorder traversal. When we encounter a non-null node, we record the node's value. If it is a null node, we record using a sentinel value such as `'#'`.

Given a string of comma-separated values `preorder`, return `true` if it is a correct preorder serialization of a binary tree.

It is guaranteed that each comma-separated value in the string must be either an integer or a character `'#'` representing null pointer.

You may not reconstruct the tree.

### Constraints
- `1 <= preorder.length <= 10^4`
- `preorder` consists of integers and `'#'` separated by commas.

### Example
Input: `preorder = "9,3,4,#,#,1,#,#,2,#,6,#,#"`
Output: `true`

### Python Implementation
```python
def isValidSerialization(preorder: str) -> bool:
    """
    Time Complexity: O(n)
    Space Complexity: O(1)
    """
    slots = 1
    for node in preorder.split(','):
        slots -= 1
        if slots < 0:
            return False
        if node != '#':
            slots += 2
    return slots == 0
```

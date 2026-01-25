# BST Operations Solutions

## 1. Search in a Binary Search Tree
**Problem Statement**: You are given the `root` of a binary search tree (BST) and an integer `val`. Find the node in the BST that the node's value equals `val` and return the subtree rooted with that node. If such a node does not exist, return `null`.

### Examples & Edge Cases
- **Example 1**: `root = [4,2,7,1,3], val = 2` → Output: `[2,1,3]`
- **Example 2**: `root = [4,2,7,1,3], val = 5` → Output: `null`
- **Edge Case - Value is root**: Returns the entire tree.
- **Edge Case - Value is leaf**: Returns a single node subtree.

### Optimal Python Solution
```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def searchBST(root: TreeNode, val: int) -> TreeNode:
    # Use iterative approach for O(1) space
    curr = root
    while curr:
        if curr.val == val:
            return curr
        elif val < curr.val:
            curr = curr.left
        else:
            curr = curr.right
    return None
```

### Explanation
1.  **BST Property**: In a BST, for any node, all values in the left subtree are smaller and all values in the right subtree are larger.
2.  **Navigation**: We compare `val` to the current node. If it's smaller, we go left; if larger, we go right.
3.  **Completion**: If we find the value, we return the node. If we hit `None`, the value isn't in the tree.

### Complexity Analysis
- **Time Complexity**: **O(h)**. In the worst case, we travel from root to leaf. $h = \log n$ for balanced trees, $h = n$ for skewed trees.
- **Space Complexity**: **O(1)**. The iterative approach uses no extra memory.

---

## 2. Insert into a Binary Search Tree
**Problem Statement**: You are given the `root` of a binary search tree (BST) and a `value` to insert into the tree. Return the `root` of the BST after the insertion. It is guaranteed that the new value does not exist in the original BST.

### Examples & Edge Cases
- **Example 1**: `root = [4,2,7,1,3], val = 5` → Output: `[4,2,7,1,3,5]`
- **Edge Case - Empty Tree**: `root = None, val = 5` → Output: `[5]` (returns new node as root).

### Optimal Python Solution
```python
def insertIntoBST(root: TreeNode, val: int) -> TreeNode:
    if not root:
        return TreeNode(val)

    curr = root
    while True:
        if val < curr.val:
            # If there's space on the left, insert
            if not curr.left:
                curr.left = TreeNode(val)
                break
            curr = curr.left
        else:
            # If there's space on the right, insert
            if not curr.right:
                curr.right = TreeNode(val)
                break
            curr = curr.right

    return root
```

### Explanation
1.  **Find the Leaf**: Similar to search, we traverse down the tree based on the BST property until we find a `None` spot where the node *should* be.
2.  **Attachment**: Once we find an empty child pointer in the correct direction, we create a new `TreeNode` and attach it.
3.  **Return**: We return the original `root` (unless the original was `None`).

### Complexity Analysis
- **Time Complexity**: **O(h)**.
- **Space Complexity**: **O(1)**.

---

## 3. Delete Node in a BST
**Problem Statement**: Given a `root` node reference of a BST and a `key`, delete the node with the given `key` in the BST. Return the `root` node reference (possibly updated) of the BST.

### Examples & Edge Cases
- **Example 1**: `root = [5,3,6,2,4,None,7], key = 3` → Output: `[5,4,6,2,None,None,7]`
- **Edge Case - Delete Leaf**: Simply remove the node.
- **Edge Case - Delete node with one child**: Replace the node with its child.
- **Edge Case - Delete node with two children**: Replace the node with its inorder successor (smallest in right subtree) or predecessor.

### Optimal Python Solution
```python
def deleteNode(root: TreeNode, key: int) -> TreeNode:
    if not root:
        return None

    # 1. Locate the node
    if key < root.val:
        root.left = deleteNode(root.left, key)
    elif key > root.val:
        root.right = deleteNode(root.right, key)
    else:
        # Found the node! Handle 3 cases:

        # Case 1 & 2: Node has 0 or 1 child
        if not root.left:
            return root.right
        if not root.right:
            return root.left

        # Case 3: Node has 2 children
        # Find inorder successor (minimum in right subtree)
        successor = root.right
        while successor.left:
            successor = successor.left

        # Replace current node's value with successor's value
        root.val = successor.val
        # Delete the successor node from the right subtree
        root.right = deleteNode(root.right, successor.val)

    return root
```

### Explanation
1.  **Recursive Search**: We recurse left or right until we find the target node.
2.  **Case 1 (Leaf)**: `not root.left` and `not root.right` will return `None` (root.right), effectively deleting the node.
3.  **Case 2 (One Child)**: If only `root.left` is missing, we return `root.right` to the parent, bypassing the current node.
4.  **Case 3 (Two Children)**: We find the "Inorder Successor" (the smallest value in the right subtree). We copy its value to the current node and then recursively delete the successor node from the right subtree.

### Complexity Analysis
- **Time Complexity**: **O(h)**. We traverse to find the node, and in Case 3, we traverse again to find the successor. Both are proportional to height.
- **Space Complexity**: **O(h)**. Space used by the recursion stack.

---

## 4. Inorder Successor in BST
**Problem Statement**: Given a binary search tree and a node `p` in it, find the in-order successor of that node in the BST. The successor of a node `p` is the node with the smallest key greater than `p.val`.

### Optimal Python Solution
```python
def inorderSuccessor(root: TreeNode, p: TreeNode) -> TreeNode:
    successor = None

    while root:
        if p.val < root.val:
            # Current node is a potential successor, but there might be a smaller one on the left
            successor = root
            root = root.left
        else:
            # Current node and everything left is too small, go right
            root = root.right

    return successor
```

### Complexity Analysis
- **Time Complexity**: **O(h)**.
- **Space Complexity**: **O(1)**.

---

## 5. Range Sum of BST
**Problem Statement**: Given the `root` node of a binary search tree and two integers `low` and `high`, return the sum of values of all nodes with a value in the inclusive range `[low, high]`.

### Optimal Python Solution
```python
def rangeSumBST(root: TreeNode, low: int, high: int) -> int:
    if not root:
        return 0

    # If current node is too small, entire left subtree is too small
    if root.val < low:
        return rangeSumBST(root.right, low, high)

    # If current node is too large, entire right subtree is too large
    if root.val > high:
        return rangeSumBST(root.left, low, high)

    # Node is in range, add it and check both children
    return root.val + rangeSumBST(root.left, low, high) + rangeSumBST(root.right, low, high)
```

### Complexity Analysis
- **Time Complexity**: **O(n)**. In the worst case, we check every node.
- **Space Complexity**: **O(h)**.

---

## 6. Closest Binary Search Tree Value
**Problem Statement**: Given the `root` of a binary search tree and a `target` value, return the value in the BST that is closest to the `target`.

### Optimal Python Solution
```python
def closestValue(root: TreeNode, target: float) -> int:
    closest = root.val

    while root:
        # Update closest if the current node is "better"
        if abs(root.val - target) < abs(closest - target):
            closest = root.val

        # Standard BST search logic
        if target < root.val:
            root = root.left
        else:
            root = root.right

    return closest
```

### Complexity Analysis
- **Time Complexity**: **O(h)**.
- **Space Complexity**: **O(1)**.

---

## 7. Trim a Binary Search Tree
**Problem Statement**: Given the `root` of a binary search tree and the lowest and highest boundaries as `low` and `high`, trim the tree so that all its elements lies in `[low, high]`. Trimming the tree should not change the relative structure of the elements that will remain in the tree.

### Optimal Python Solution
```python
def trimBST(root: TreeNode, low: int, high: int) -> TreeNode:
    if not root:
        return None

    # If root is too small, discard root and left subtree, return trimmed right subtree
    if root.val < low:
        return trimBST(root.right, low, high)

    # If root is too large, discard root and right subtree, return trimmed left subtree
    if root.val > high:
        return trimBST(root.left, low, high)

    # Root is in range, connect trimmed subtrees to it
    root.left = trimBST(root.left, low, high)
    root.right = trimBST(root.right, low, high)

    return root
```

### Complexity Analysis
- **Time Complexity**: **O(n)**. We visit each node once.
- **Space Complexity**: **O(h)**.

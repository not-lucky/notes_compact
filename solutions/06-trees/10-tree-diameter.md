# Tree Diameter Solutions

## 1. Diameter of Binary Tree
**Problem Statement**: Given the `root` of a binary tree, return the length of the **diameter** of the tree. The diameter of a binary tree is the length of the longest path between any two nodes in a tree. This path may or may not pass through the root.

### Examples & Edge Cases
- **Example 1**: `root = [1,2,3,4,5]` → Output: `3` (Path `4->2->5` or `4->2->1->3`)
- **Edge Case - Single Node**: `root = [1]` → Output: `0`
- **Edge Case - Path not through root**: A very deep branch on the left can contain the diameter.

### Optimal Python Solution
```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def diameterOfBinaryTree(root: TreeNode) -> int:
    # Use a list to store mutable global state
    diameter = [0]

    def get_height(node):
        if not node:
            return 0

        # Recursively get heights of subtrees
        left_h = get_height(node.left)
        right_h = get_height(node.right)

        # The longest path through this node is (left height + right height)
        # We update our global max diameter
        diameter[0] = max(diameter[0], left_h + right_h)

        # Return height of this node to the parent
        return 1 + max(left_h, right_h)

    get_height(root)
    return diameter[0]
```

### Explanation
1.  **Insight**: For any node in the tree, the longest path that *peaks* at that node is the sum of the heights of its left and right subtrees.
2.  **Global Maximum**: We perform a post-order traversal ($O(n)$) to calculate heights. As we compute the height for each node, we "sneakily" calculate the diameter through that node and update a global variable if it's the largest seen so far.
3.  **Recursive Step**: Each node returns its height ($1 + \max(\text{left}, \text{right})$) so that its parent can perform its own calculation.

### Complexity Analysis
- **Time Complexity**: **O(n)**. We visit every node once.
- **Space Complexity**: **O(h)**. The space used by the recursion stack.

---

## 2. Binary Tree Maximum Path Sum
**Problem Statement**: Find the maximum path sum of any non-empty path.

### Optimal Python Solution
```python
def maxPathSum(root: TreeNode) -> int:
    max_path = float('-inf')

    def get_max_gain(node):
        nonlocal max_path
        if not node:
            return 0

        # Calculate max contribution from subtrees (ignoring negative paths)
        left_gain = max(get_max_gain(node.left), 0)
        right_gain = max(get_max_gain(node.right), 0)

        # Update global max path if path through this node is better
        max_path = max(max_path, node.val + left_gain + right_gain)

        # Return max gain to parent (can only pick one subtree)
        return node.val + max(left_gain, right_gain)

    get_max_gain(root)
    return max_path
```

### Explanation
- This follows the exact same pattern as Diameter. Instead of height, we calculate "Max Gain".
- At each node, we check if the path *starting in left subtree, going through current node, and ending in right subtree* is the maximum.
- We return only the best single-branch contribution to the parent.

### Complexity Analysis
- **Time Complexity**: **O(n)**.
- **Space Complexity**: **O(h)**.

---

## 3. Longest Univalue Path
**Problem Statement**: Find the length of the longest path where each node in the path has the same value.

### Optimal Python Solution
```python
def longestUnivaluePath(root: TreeNode) -> int:
    ans = 0

    def dfs(node):
        nonlocal ans
        if not node:
            return 0

        left_len = dfs(node.left)
        right_len = dfs(node.right)

        left_arrow = right_arrow = 0
        if node.left and node.left.val == node.val:
            left_arrow = left_len + 1
        if node.right and node.right.val == node.val:
            right_arrow = right_len + 1

        ans = max(ans, left_arrow + right_arrow)
        return max(left_arrow, right_arrow)

    dfs(root)
    return ans
```

### Complexity Analysis
- **Time Complexity**: **O(n)**.
- **Space Complexity**: **O(h)**.

---

## 4. Longest Path With Different Adjacent Characters
**Problem Statement**: Given a tree where each node has a character, find the longest path such that no two adjacent nodes have the same character.

### Optimal Python Solution
```python
def longestPath(parent: list[int], s: str) -> int:
    from collections import defaultdict
    children = defaultdict(list)
    for i, p in enumerate(parent):
        if p != -1:
            children[p].append(i)

    res = 0

    def dfs(node):
        nonlocal res
        # Track the top two longest paths from children
        max1 = max2 = 0

        for child in children[node]:
            child_len = dfs(child)
            # If adjacent characters are different, this child can contribute
            if s[node] != s[child]:
                if child_len > max1:
                    max2 = max1
                    max1 = child_len
                elif child_len > max2:
                    max2 = child_len

        # Diameter at this node
        res = max(res, max1 + max2 + 1)
        # Return height for parent
        return max1 + 1

    dfs(0)
    return res
```

### Explanation
- This is a generalization of binary tree diameter to **N-ary trees**.
- Instead of just `left` and `right`, we iterate through all children and keep track of the **two longest valid paths**.

### Complexity Analysis
- **Time Complexity**: **O(n)**. Each node and edge is processed once.
- **Space Complexity**: **O(n)**. For child adjacency list and recursion.

---

## 5. Tree Diameter
**Problem Statement**: Given an undirected tree (as an edge list), find its diameter.

### Optimal Python Solution
```python
def treeDiameter(edges: list[list[int]]) -> int:
    from collections import defaultdict, deque
    if not edges: return 0

    adj = defaultdict(list)
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)

    def bfs(start_node):
        distances = {start_node: 0}
        queue = deque([start_node])
        farthest_node = start_node
        max_dist = 0

        while queue:
            curr = queue.popleft()
            if distances[curr] > max_dist:
                max_dist = distances[curr]
                farthest_node = curr

            for neighbor in adj[curr]:
                if neighbor not in distances:
                    distances[neighbor] = distances[curr] + 1
                    queue.append(neighbor)

        return farthest_node, max_dist

    # 1. Start from arbitrary node (0) to find the first endpoint
    node1, _ = bfs(0)
    # 2. Start from that endpoint to find the other endpoint
    _, diameter = bfs(node1)

    return diameter
```

### Explanation
- **Two BFS Theorem**: In an undirected tree, if you start a BFS from any node `A` and find the farthest node `B`, then a BFS starting from `B` will find the farthest node `C` in the entire tree. The distance `B-C` is the diameter.

### Complexity Analysis
- **Time Complexity**: **O(n)**. Two BFS passes.
- **Space Complexity**: **O(n)**. Adjacency list and BFS queue.

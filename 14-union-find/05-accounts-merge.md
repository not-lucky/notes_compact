# Accounts Merge

> **Prerequisites:** [Union-Find Basics](./01-union-find-basics.md), [Connected Components](./04-connected-components.md)

## Interview Context

"Accounts Merge" (LeetCode 721) is a classic Union-Find problem that combines the data structure with string mapping. It tests your ability to map non-integer elements to Union-Find indices and correctly group related elements.

---

## Building Intuition

**The "Email Detective" Mental Model**

Imagine you're a detective trying to identify people based on their email addresses:

```
Evidence:
Account 1: "John" uses john@gmail.com, john@work.com
Account 2: "John" uses john@home.com
Account 3: "John" uses john@work.com, john@school.com

Deduction:
- Accounts 1 and 3 share john@work.com → SAME PERSON!
- Account 2 has no overlap → DIFFERENT PERSON

Result: Two distinct people named "John"
```

The key insight: **Emails are the fingerprints**, not names. Two accounts merge if they share ANY email.

**The Transitive Chain**

```
Account A: email1, email2
Account B: email2, email3
Account C: email3, email4

email1 ←→ email2 ←→ email3 ←→ email4
         (all connected transitively!)

All four emails belong to ONE person.
```

**Why Union-Find Fits Perfectly**

This is a connectivity problem in disguise:
- **Nodes**: Email addresses
- **Edges**: Emails appearing in the same account
- **Groups**: All emails of one real person

Union-Find excels because:
1. We union all emails within each account
2. Transitive connections happen automatically
3. Final grouping is efficient via find()

```
Traditional approach (graph + DFS):
- Build adjacency list of email connections
- DFS from each unvisited email
- Track visited to avoid duplicates
- Complex bookkeeping

Union-Find approach:
- Union emails in same account (single loop)
- Group by root (simple dict aggregation)
- Clean, efficient
```

---

## When NOT to Use Union-Find for Merging

**1. When Merge Logic is Complex**

Union-Find assumes binary connectivity: either connected or not. For nuanced merging rules:

```python
# "Merge accounts if they share 2+ emails" → Can't use basic UF
# "Merge accounts if names match AND share email" → Needs preprocessing

# Union-Find assumes: share ANY email = same person
```

**2. When You Need to Preserve Original Groups**

If you need to track which original accounts contributed to each merged account, Union-Find loses that information:

```python
# Union-Find: Tells you "these 5 emails belong together"
# Doesn't tell you: "This came from accounts 1, 3, and 7"

# If you need provenance, track it separately
```

**3. When Un-Merging is Required**

If accounts can later be "split" (e.g., user requests separation), Union-Find can't undo merges efficiently:

```python
# Union is permanent in standard Union-Find
# For reversible merging, consider different data structures
```

**4. For Small Input Sizes**

If there are only a few accounts (< 100), a simpler approach might be clearer:

```python
# Build graph, run DFS, group by component
# More lines of code but easier to understand
# For interview: mention you'd use Union-Find for scale
```

---

## Problem Statement

Given a list of accounts where each account contains a name followed by emails, merge accounts that share at least one email. Return the merged accounts with emails sorted.

### Example

```
Input:
accounts = [
    ["John", "john@gmail.com", "john@work.com"],
    ["John", "john@home.com"],
    ["Mary", "mary@gmail.com"],
    ["John", "john@work.com", "john@school.com"]
]

Output:
[
    ["John", "john@gmail.com", "john@home.com", "john@school.com", "john@work.com"],
    ["Mary", "mary@gmail.com"]
]

Explanation:
- Accounts 0 and 3 share "john@work.com" → merge
- Account 1 has a different John (no shared email)
- Wait, actually account 1 stays separate

Correction - let me re-read:
Account 0: John - john@gmail.com, john@work.com
Account 3: John - john@work.com, john@school.com
These share john@work.com → merge into one John account

Account 1: John - john@home.com (no overlap) → separate
Account 2: Mary - mary@gmail.com → separate
```

---

## Approach: Union-Find with Email Mapping

### Key Steps

1. **Map emails to indices**: Each unique email gets an index
2. **Union emails in same account**: All emails in one account belong together
3. **Group by root**: Find all emails with same root
4. **Build result**: Associate each group with account name

### Visualization

```
Account 0: john@gmail.com, john@work.com
Account 1: john@home.com
Account 2: mary@gmail.com
Account 3: john@work.com, john@school.com

Step 1: Assign indices
john@gmail.com  → 0
john@work.com   → 1
john@home.com   → 2
mary@gmail.com  → 3
john@school.com → 4

Step 2: Union within accounts
Account 0: union(0, 1)  → {0, 1}
Account 1: (single email, no union)
Account 2: (single email, no union)
Account 3: union(1, 4)  → {0, 1, 4}

Step 3: Final groups
Root 0: [0, 1, 4] → john@gmail.com, john@work.com, john@school.com
Root 2: [2] → john@home.com
Root 3: [3] → mary@gmail.com
```

---

## Implementation

```python
def accountsMerge(accounts: list[list[str]]) -> list[list[str]]:
    """
    Merge accounts with Union-Find.

    Time: O(n × k × α(n × k)) where n = accounts, k = avg emails per account
    Space: O(n × k)
    """
    from collections import defaultdict

    # Map each email to an index
    email_to_idx = {}
    email_to_name = {}
    idx = 0

    for account in accounts:
        name = account[0]
        for email in account[1:]:
            if email not in email_to_idx:
                email_to_idx[email] = idx
                email_to_name[email] = name
                idx += 1

    # Union-Find on indices
    n = len(email_to_idx)
    parent = list(range(n))
    rank = [0] * n

    def find(x: int) -> int:
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    def union(x: int, y: int) -> None:
        px, py = find(x), find(y)
        if px == py:
            return
        if rank[px] < rank[py]:
            px, py = py, px
        parent[py] = px
        if rank[px] == rank[py]:
            rank[px] += 1

    # Union all emails in the same account
    for account in accounts:
        first_email = account[1]
        first_idx = email_to_idx[first_email]

        for email in account[2:]:
            union(first_idx, email_to_idx[email])

    # Group emails by root
    groups = defaultdict(list)
    for email, idx in email_to_idx.items():
        root = find(idx)
        groups[root].append(email)

    # Build result
    result = []
    for root, emails in groups.items():
        # Get name from any email in the group
        name = email_to_name[emails[0]]
        # Sort emails and prepend name
        result.append([name] + sorted(emails))

    return result
```

---

## Alternative: Direct Email-to-Email Union

Instead of mapping to indices, union emails directly using a dictionary-based Union-Find.

```python
def accountsMerge_v2(accounts: list[list[str]]) -> list[list[str]]:
    """
    Direct email-to-email Union-Find without index mapping.

    Cleaner code, same complexity.
    """
    from collections import defaultdict

    parent = {}

    def find(x: str) -> str:
        if x not in parent:
            parent[x] = x
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    def union(x: str, y: str) -> None:
        parent[find(y)] = find(x)

    # Map each email to its account name
    email_to_name = {}

    for account in accounts:
        name = account[0]
        first_email = account[1]
        email_to_name[first_email] = name

        for email in account[1:]:
            email_to_name[email] = name
            union(first_email, email)

    # Group emails by root
    groups = defaultdict(list)
    for email in email_to_name:
        groups[find(email)].append(email)

    # Build result
    result = []
    for root, emails in groups.items():
        name = email_to_name[root]
        result.append([name] + sorted(emails))

    return result
```

---

## Step-by-Step Trace

```python
accounts = [
    ["John", "a@g.com", "b@g.com"],
    ["John", "c@g.com"],
    ["John", "b@g.com", "d@g.com"],
    ["Mary", "e@g.com"]
]

# After building parent map and unions:
# Account 0: union(a, b)
# Account 2: union(b, d) → a, b, d all connected

# parent after path compression:
# a → a (root)
# b → a
# c → c (root)
# d → a
# e → e (root)

# Groups:
# find(a) = a → [a, b, d]
# find(c) = c → [c]
# find(e) = e → [e]

# Result:
# ["John", "a@g.com", "b@g.com", "d@g.com"]
# ["John", "c@g.com"]
# ["Mary", "e@g.com"]
```

---

## Problem Variation: Similar String Groups

**LeetCode 839**: Two strings are similar if you can swap two letters in one to get the other. Group all similar strings.

```python
def numSimilarGroups(strs: list[str]) -> int:
    """
    Count groups of similar strings.

    Time: O(n² × m) where n = len(strs), m = string length
    Space: O(n)
    """
    n = len(strs)
    parent = list(range(n))

    def find(x: int) -> int:
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    def union(x: int, y: int) -> None:
        parent[find(y)] = find(x)

    def similar(s1: str, s2: str) -> bool:
        """Check if s1 and s2 differ by exactly 2 swapped positions."""
        diff = []
        for i, (c1, c2) in enumerate(zip(s1, s2)):
            if c1 != c2:
                diff.append(i)
                if len(diff) > 2:
                    return False

        if len(diff) == 0:
            return True  # Same string
        if len(diff) == 2:
            i, j = diff
            return s1[i] == s2[j] and s1[j] == s2[i]
        return False

    # Check all pairs
    for i in range(n):
        for j in range(i + 1, n):
            if similar(strs[i], strs[j]):
                union(i, j)

    # Count unique roots
    return len(set(find(i) for i in range(n)))
```

---

## Problem Variation: Sentence Similarity II

**LeetCode 737**: Words are similar if they're in the same similarity group (transitive). Check if two sentences are similar.

```python
def areSentencesSimilarTwo(
    sentence1: list[str],
    sentence2: list[str],
    similarPairs: list[list[str]]
) -> bool:
    """
    Check sentence similarity with transitive similar words.

    Time: O(n × α(p)) where n = sentence length, p = pairs
    Space: O(p)
    """
    if len(sentence1) != len(sentence2):
        return False

    parent = {}

    def find(x: str) -> str:
        if x not in parent:
            parent[x] = x
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    def union(x: str, y: str) -> None:
        parent[find(y)] = find(x)

    # Build similarity groups
    for w1, w2 in similarPairs:
        union(w1, w2)

    # Check each word pair
    for w1, w2 in zip(sentence1, sentence2):
        if w1 == w2:
            continue
        if find(w1) != find(w2):
            return False

    return True
```

---

## Common Patterns

### 1. String-to-Index Mapping

```python
# When Union-Find needs integer indices but input is strings
item_to_idx = {}
idx = 0

for item in items:
    if item not in item_to_idx:
        item_to_idx[item] = idx
        idx += 1

# Now use item_to_idx[item] as Union-Find index
```

### 2. Dictionary-Based Union-Find

```python
# When items are hashable but not integers
parent = {}

def find(x):
    if x not in parent:
        parent[x] = x  # Initialize on first access
    if parent[x] != x:
        parent[x] = find(parent[x])
    return parent[x]
```

### 3. First Element as Representative

```python
# Union all items to the first item in each group
for group in groups:
    first = group[0]
    for item in group[1:]:
        union(first, item)
```

---

## Complexity Analysis

For Accounts Merge with n accounts and k emails per account:

| Operation | Time | Space |
|-----------|------|-------|
| Build email map | O(n × k) | O(n × k) |
| Union operations | O(n × k × α(n × k)) | O(1) |
| Group by root | O(n × k × α(n × k)) | O(n × k) |
| Sort groups | O(n × k × log k) | O(1) |
| **Total** | **O(n × k × log k)** | **O(n × k)** |

---

## Edge Cases

1. **Single account**: Return as-is with sorted emails
2. **No overlapping emails**: Each account stays separate
3. **All same email**: All accounts merge into one
4. **Same name, different people**: Name doesn't matter for merging
5. **Empty emails in account**: Handle edge case if possible

---

## Interview Tips

1. **Clarify transitivity**: "If A shares email with B, and B with C, then A and C merge?"
2. **Ask about name conflicts**: "Same name but different email sets?"
3. **Output format**: "Sorted emails? Specific order of accounts?"
4. **String vs index**: Mention both approaches, use cleaner one

---

## Practice Problems

| # | Problem | Difficulty | Key Concept |
|---|---------|------------|-------------|
| 1 | Accounts Merge | Medium | Email grouping |
| 2 | Similar String Groups | Hard | Pair-wise similarity |
| 3 | Sentence Similarity II | Medium | Transitive similarity |
| 4 | Synonymous Sentences | Medium | Word grouping |
| 5 | Evaluate Division | Medium | Weighted Union-Find |

---

## Related Sections

- [Connected Components](./04-connected-components.md) - Basic grouping
- [Redundant Connection](./06-redundant-connection.md) - Cycle detection
- [Hash Tables](../03-hashmaps-sets/README.md) - String mapping

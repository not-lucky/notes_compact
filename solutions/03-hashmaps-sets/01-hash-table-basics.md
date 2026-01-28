# Hash Table Basics - Solutions

## 1. Design HashMap

Design a HashMap without using any built-in hash table libraries.

### Problem Statement

Implement the `MyHashMap` class:

- `MyHashMap()` initializes the object with an empty map.
- `void put(int key, int value)` inserts a `(key, value)` pair into the HashMap. If the `key` already exists in the map, update the corresponding `value`.
- `int get(int key)` returns the `value` to which the specified `key` is mapped, or `-1` if this map contains no mapping for the `key`.
- `void remove(key)` removes the `key` and its corresponding `value` if the map contains the mapping for the `key`.

### Examples & Edge Cases

**Example:**

```python
myHashMap = MyHashMap()
myHashMap.put(1, 1) # The map is now [[1,1]]
myHashMap.put(2, 2) # The map is now [[1,1], [2,2]]
myHashMap.get(1)    # return 1
myHashMap.get(3)    # return -1 (i.e., not found)
myHashMap.put(2, 1) # The map is now [[1,1], [2,1]] (i.e., update the existing value)
myHashMap.get(2)    # return 1
myHashMap.remove(2) # remove the mapping for 2, the map is now [[1,1]]
myHashMap.get(2)    # return -1 (i.e., not found)
```

**Edge Cases:**

- `key` or `value` is 0.
- Removing a key that doesn't exist.
- Updating an existing key.
- Hash collisions (multiple keys mapping to the same bucket).
- Large number of operations.

### Optimal Python Solution

```python
class MyHashMap:
    """
    Implementation using Separate Chaining to handle collisions.
    We use a fixed-size array of buckets, where each bucket is a list
    of [key, value] pairs.
    """

    def __init__(self):
        # Choose a prime number for the number of buckets to reduce collisions
        self.size = 1009
        self.buckets = [[] for _ in range(self.size)]

    def _hash(self, key: int) -> int:
        # Simple modulo hash function
        return key % self.size

    def put(self, key: int, value: int) -> None:
        """
        Inserts or updates the value for a given key.
        """
        idx = self._hash(key)
        bucket = self.buckets[idx]

        # Check if key already exists in the bucket
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value) # Update existing
                return

        # Key not found, append to the bucket
        bucket.append((key, value))

    def get(self, key: int) -> int:
        """
        Returns the value for the key, or -1 if not found.
        """
        idx = self._hash(key)
        bucket = self.buckets[idx]

        for k, v in bucket:
            if k == key:
                return v
        return -1

    def remove(self, key: int) -> None:
        """
        Removes the mapping for the key if it exists.
        """
        idx = self._hash(key)
        bucket = self.buckets[idx]

        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket.pop(i)
                return
```

### Explanation

1.  **Buckets**: We initialize an array of 1009 empty lists (buckets). We use 1009 because it's a prime number, which helps distribute keys more evenly and reduces the frequency of collisions.
2.  **Hashing**: The `_hash` function takes a key and returns `key % 1009`. This maps every integer key to an index between 0 and 1008.
3.  **Put**: We find the correct bucket using the hash. We then iterate through the pairs in that bucket. If the key is found, we update its value. If not, we append the new `(key, value)` pair.
4.  **Get**: We find the bucket and search for the key. If found, return the value; otherwise, return -1.
5.  **Remove**: We find the bucket and search for the key. If found, we remove that pair from the list using `pop(i)`.

### Complexity Analysis

- **Time Complexity**:
  - **Average Case**: O(1) for all operations. With a good distribution, the number of elements in each bucket remains small and constant on average.
  - **Worst Case**: O(n), where n is the number of keys. This happens if all keys hash to the same bucket (a "catastrophic" collision).
- **Space Complexity**: O(n + k), where n is the number of unique keys inserted and k is the number of buckets (1009). We need space for the buckets themselves and for the elements stored within them.

---

## 2. Design HashSet

Design a HashSet without using any built-in hash table libraries.

### Problem Statement

Implement the `MyHashSet` class:

- `void add(key)` inserts the value `key` into the HashSet.
- `bool contains(key)` returns whether the value `key` exists in the HashSet or not.
- `void remove(key)` removes the value `key` in the HashSet. If `key` does not exist in the HashSet, do nothing.

### Examples & Edge Cases

**Example:**

```python
myHashSet = MyHashSet()
myHashSet.add(1)      # set = [1]
myHashSet.add(2)      # set = [1, 2]
myHashSet.contains(1) # return True
myHashSet.contains(3) # return False (not found)
myHashSet.add(2)      # set = [1, 2] (already exists)
myHashSet.contains(2) # return True
myHashSet.remove(2)   # set = [1]
myHashSet.contains(2) # return False (already removed)
```

**Edge Cases:**

- Adding the same key multiple times (should only store it once).
- Removing a key that doesn't exist.
- Hashing 0.

### Optimal Python Solution

```python
class MyHashSet:
    """
    Implementation using Separate Chaining.
    Each bucket stores a list of unique keys.
    """

    def __init__(self):
        self.size = 1009
        self.buckets = [[] for _ in range(self.size)]

    def _hash(self, key: int) -> int:
        return key % self.size

    def add(self, key: int) -> None:
        idx = self._hash(key)
        bucket = self.buckets[idx]
        if key not in bucket:
            bucket.append(key)

    def remove(self, key: int) -> None:
        idx = self._hash(key)
        bucket = self.buckets[idx]
        if key in bucket:
            bucket.remove(key)

    def contains(self, key: int) -> bool:
        idx = self._hash(key)
        bucket = self.buckets[idx]
        return key in bucket
```

### Explanation

The logic is almost identical to the HashMap implementation, but simpler because we only store keys, not values. We use the same prime-sized bucket array and modulo hashing. For `add`, we first check if the key is already present in the bucket to maintain the "set" property of uniqueness.

### Complexity Analysis

- **Time Complexity**:
  - **Average Case**: O(1) for `add`, `remove`, and `contains`.
  - **Worst Case**: O(n) if all elements hash to one bucket.
- **Space Complexity**: O(n + k) where n is unique elements and k is buckets.

---

## 3. Contains Duplicate

Given an integer array `nums`, return `true` if any value appears at least twice in the array, and return `false` if every element is distinct.

### Problem Statement

Determine if an array contains any duplicate elements.

### Examples & Edge Cases

**Example 1:**

- Input: `nums = [1, 2, 3, 1]`
- Output: `true`

**Example 2:**

- Input: `nums = [1, 2, 3, 4]`
- Output: `false`

**Edge Cases:**

- Empty array: Should return `false`.
- Array with one element: Should return `false`.
- Array with all identical elements: Should return `true`.

### Optimal Python Solution

```python
def containsDuplicate(nums: list[int]) -> bool:
    """
    Use a set to track seen numbers.
    If we encounter a number already in the set, we found a duplicate.
    """
    seen = set()
    for num in nums:
        if num in seen:
            return True
        seen.add(num)
    return False

# Alternative Pythonic way:
# return len(nums) != len(set(nums))
```

### Explanation

We iterate through the array once. For each number, we check if it's already in our `seen` set. If it is, that's a duplicate, so we return `True`. If we finish the loop without finding any duplicates, we return `False`. Using a set allows us to perform the "has this been seen?" check in O(1) average time.

### Complexity Analysis

- **Time Complexity**: O(n). We traverse the array of length `n` exactly once. Each set lookup and insertion is O(1) on average.
- **Space Complexity**: O(n). In the worst case (no duplicates), we store all `n` elements in the set.

---

## 4. Jewels and Stones

You're given strings `jewels` representing the types of stones that are jewels, and `stones` representing the stones you have. Each character in `stones` is a type of stone you have. You want to know how many of the stones you have are also jewels.

### Problem Statement

Count how many characters in the `stones` string appear in the `jewels` string. Letters are case-sensitive.

### Examples & Edge Cases

**Example 1:**

- Input: `jewels = "aA"`, `stones = "aAAbbbb"`
- Output: `3`

**Example 2:**

- Input: `jewels = "z"`, `stones = "ZZ"`
- Output: `0`

**Edge Cases:**

- `jewels` or `stones` is empty.
- No jewels found in stones.
- All stones are jewels.

### Optimal Python Solution

```python
def numJewelsInStones(jewels: str, stones: str) -> int:
    """
    Convert jewels string to a set for O(1) lookup.
    Iterate through stones and count those that are in the jewels set.
    """
    jewel_set = set(jewels)
    count = 0

    for stone in stones:
        if stone in jewel_set:
            count += 1

    return count
```

### Explanation

1.  **Preprocessing**: We convert the `jewels` string into a set. This is important because searching for a character in a string is O(m) where m is length of the string, but searching in a set is O(1).
2.  **Counting**: We iterate through each character in `stones`. For each character, we check if it exists in our `jewel_set`. If it does, we increment our counter.

### Complexity Analysis

- **Time Complexity**: O(n + m), where n is the length of `stones` and m is the length of `jewels`. We spend O(m) to build the set and O(n) to iterate through the stones.
- **Space Complexity**: O(m) to store the `jewel_set`.

---

## 5. First Unique Character in a String

Given a string `s`, find the first non-repeating character in it and return its index. If it does not exist, return `-1`.

### Problem Statement

Identify the index of the first character that appears exactly once in the string.

### Examples & Edge Cases

**Example 1:**

- Input: `s = "leetcode"`
- Output: `0` ('l' appears once and is first)

**Example 2:**

- Input: `s = "loveleetcode"`
- Output: `2` ('v' appears once and is first)

**Example 3:**

- Input: `s = "aabb"`
- Output: `-1`

**Edge Cases:**

- String with only one character.
- String where all characters repeat.
- Very long strings.

### Optimal Python Solution

```python
from collections import Counter

def firstUniqChar(s: str) -> int:
    """
    1. Count frequencies of all characters.
    2. Iterate through string again and find first char with frequency 1.
    """
    # Use Counter to get character frequencies
    count = Counter(s)

    # Iterate through the string to maintain order
    for i, char in enumerate(s):
        if count[char] == 1:
            return i

    return -1
```

### Explanation

1.  **Counting**: We first traverse the string to count how many times each character appears. We use `collections.Counter`, which is a specialized dictionary for counting.
2.  **Searching**: We traverse the string a second time. Since we want the _first_ unique character, we must iterate through the string characters in their original order. For each character, we check our frequency map. The first character with a count of 1 is our answer.

### Complexity Analysis

- **Time Complexity**: O(n). We traverse the string twice: once to count (O(n)) and once to find the first unique (O(n)). 2n simplifies to O(n).
- **Space Complexity**: O(1). While we use a hashmap, the number of unique characters is capped by the size of the alphabet (e.g., 26 for lowercase English letters), which is constant.

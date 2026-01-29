# Frequency Counting

> **Prerequisites:** [01-hash-table-basics.md](./01-hash-table-basics.md)

## Interview Context

Frequency counting is one of the most versatile hashmap patterns. It appears in:

- Top K problems (most frequent, least frequent)
- Anagram and character frequency problems
- Finding duplicates, majorities, and unique elements
- Bucket sort and counting sort variations

The key insight: counting occurrences transforms comparison problems into lookup problems.

**Interview frequency**: Very high. You'll use Counter or frequency maps in almost every hashmap problem.

---

## Building Intuition

**The Core Insight: Counting Enables O(1) Decisions**

Without frequency counting:

```
"How many times does 5 appear?" → Scan entire array → O(n)
```

With frequency counting (one-time O(n) preprocessing):

```
freq = {5: 3, 2: 2, 7: 1}
"How many times does 5 appear?" → freq[5] → O(1)
```

You pay O(n) once to answer unlimited questions in O(1).

**Mental Model: Inventory Sheet**

Think of a warehouse inventory:

- Walking the aisles to count each item type → O(n) every time
- Building an inventory sheet first → O(n) once, O(1) lookups forever

**Why Bucket Sort Works for Top K**

The magical O(n) trick: frequency is bounded by array size.

```
nums = [1,1,1,2,2,3], n=6

Maximum possible frequency = 6
Create 6 buckets (one per frequency):

bucket[0] = []
bucket[1] = [3]      ← appears 1 time
bucket[2] = [2]      ← appears 2 times
bucket[3] = [1]      ← appears 3 times
bucket[4] = []
bucket[5] = []
bucket[6] = []

Top K? Walk buckets from right to left!
```

No sorting needed—frequency IS the index.

**Why Boyer-Moore Is Genius**

The voting algorithm uses a key observation: if there's a majority element (>n/2), it can "afford" to be cancelled by all other elements and still survive.

```
[2, 2, 1, 1, 1, 2, 2]

Think of it as a battle:
- Each 2 "cancels" one non-2
- Each non-2 "cancels" one 2
- Majority survives because it has more soldiers

Result: The candidate after all battles is the majority.
```

**Pattern Recognition: When to Use XOR**

XOR has magical properties:

- `a ^ a = 0` (any number XORed with itself is 0)
- `a ^ 0 = a` (any number XORed with 0 is itself)
- Commutative and associative

So for "find the single non-duplicate":

```
XOR all elements → duplicates cancel to 0 → only unique remains
```

No hashmap needed, O(1) space!

---

## When NOT to Use Frequency Counting

**1. You Need Order Information**

Frequency maps lose positional information:

```python
# "Find first element that appears k times" → need to track positions too
# "Find longest streak of same element" → sliding window is better
```

**2. Counting Isn't the Question**

Some problems look like counting but aren't:

```python
# "Find two numbers that sum to target" → Two Sum, not frequency
# "Find longest increasing subsequence" → DP, not frequency
```

**3. Memory Constraints Are Tight**

Counter uses O(k) space where k = unique elements:

```python
# Stream of 10 billion elements with 1 billion unique values
# Counter would use 1 billion entries → too much memory
# Use probabilistic structures (Count-Min Sketch, HyperLogLog)
```

**4. You Need Approximate Answers**

For "roughly how many unique?" or "approximately top-K":

- Probabilistic algorithms are better
- Exact counting is overkill

**5. Streaming Data with Limited Memory**

For unbounded streams:

- Boyer-Moore works for majority (O(1) space)
- But generic "top K" on infinite stream needs different approach

**Red Flags:**

- "Maintain order of first occurrence" → Use OrderedDict or track separately
- "Streaming with bounded memory" → Probabilistic structures
- "Approximate answer acceptable" → Sketch algorithms
- "Find position of kth unique" → Need position tracking too

---

## Core Concept

**Frequency Map**: A hashmap where keys are elements and values are their counts.

```
nums = [1, 2, 2, 3, 3, 3]

Frequency Map:
{
  1: 1,
  2: 2,
  3: 3
}
```

---

## Template: Basic Frequency Counting

**Problem**: Given an array of elements, count the number of occurrences for each unique element.

**Explanation**: We iterate through the array once and use a hashmap to store each element as a key and its frequency as the value. This allows us to retrieve the count of any element in O(1) time after an O(n) preprocessing step. Python's `collections.Counter` is a highly optimized tool for this specific task.

```python
def frequency_count(nums: list) -> dict:
    """
    Count frequency of each element.

    Time: O(n)
    Space: O(k) where k = unique elements
    """
    freq = {}

    for num in nums:
        freq[num] = freq.get(num, 0) + 1

    return freq

# Using defaultdict
from collections import defaultdict

def frequency_count_defaultdict(nums: list) -> dict:
    freq = defaultdict(int)

    for num in nums:
        freq[num] += 1

    return freq

# Using Counter (most Pythonic)
from collections import Counter

def frequency_count_counter(nums: list) -> Counter:
    return Counter(nums)
```

---

## Template: Top K Frequent Elements

**Problem**: Given an integer array `nums` and an integer `k`, return the `k` most frequent elements.

**Explanation**: After counting frequencies, we can use a min-heap to keep track of the top `k` elements. By maintaining a heap of size `k`, we can process all elements in O(n log k) time. Alternatively, we can use bucket sort for O(n) time if the frequencies are bounded by the input size.

```python
def top_k_frequent(nums: list[int], k: int) -> list[int]:
    """
    Find k most frequent elements.

    Time: O(n log k) with heap, O(n) with bucket sort
    Space: O(n)

    Example:
    nums = [1, 1, 1, 2, 2, 3], k = 2 → [1, 2]
    """
    from collections import Counter
    import heapq

    count = Counter(nums)

    # Method 1: Use heap (O(n log k))
    return heapq.nlargest(k, count.keys(), key=count.get)

    # Method 2: Use Counter's built-in (O(n log n))
    # return [item for item, freq in count.most_common(k)]
```

### Bucket Sort Approach (O(n))

**Problem**: Find the `k` most frequent elements in linear time.

**Explanation**: Since the frequency of any element cannot exceed the total number of elements `n`, we can create an array of "buckets" where the index represents the frequency. We place elements into the bucket corresponding to their frequency. Then, we traverse the buckets from highest index to lowest to collect the `k` most frequent elements.

```python
def top_k_frequent_bucket(nums: list[int], k: int) -> list[int]:
    """
    Bucket sort approach for O(n) time.

    Key insight: frequency is bounded by n, so use frequency as index.

    Time: O(n)
    Space: O(n)
    """
    from collections import Counter

    count = Counter(nums)
    n = len(nums)

    # buckets[i] = list of elements with frequency i
    buckets = [[] for _ in range(n + 1)]

    for num, freq in count.items():
        buckets[freq].append(num)

    # Collect top k from highest frequency buckets
    result = []
    for i in range(n, 0, -1):
        for num in buckets[i]:
            result.append(num)
            if len(result) == k:
                return result

    return result
```

### Visual Trace (Bucket Sort)

```
nums = [1, 1, 1, 2, 2, 3], k = 2

count = {1: 3, 2: 2, 3: 1}

buckets (index = frequency):
[0]: []
[1]: [3]
[2]: [2]
[3]: [1]
[4]: []
[5]: []
[6]: []

Traverse from right: [1, 2]
```

---

## Template: Top K Frequent Words

**Problem**: Given an array of strings `words` and an integer `k`, return the `k` most frequent strings. The result should be sorted by frequency from highest to lowest, and words with the same frequency should be sorted by their lexicographical order.

**Explanation**: We use a frequency map and then a heap to find the top `k` elements. To handle the secondary sorting requirement (lexicographical order for ties), we use a custom comparator or negate frequencies in a min-heap.

```python
def top_k_frequent_words(words: list[str], k: int) -> list[str]:
    """
    Find k most frequent words. If same frequency, sort alphabetically.

    Time: O(n log k)
    Space: O(n)

    Example:
    words = ["i", "love", "leetcode", "i", "love", "coding"], k = 2
    → ["i", "love"]
    """
    from collections import Counter
    import heapq

    count = Counter(words)

    # Custom comparator: higher frequency first, then alphabetically
    # heapq is min-heap, so negate frequency
    return heapq.nsmallest(k, count.keys(), key=lambda x: (-count[x], x))
```

---

## Template: K Most Frequent Strings (Follow-up: Optimize Tie-breaking)

```python
def top_k_words_optimized(words: list[str], k: int) -> list[str]:
    """
    Using min-heap for O(n log k) with proper tie-breaking.
    """
    from collections import Counter
    import heapq

    count = Counter(words)

    # Wrapper class for custom comparison
    class Element:
        def __init__(self, word, freq):
            self.word = word
            self.freq = freq

        def __lt__(self, other):
            # Min-heap: lower frequency should be at top
            # For same frequency: reverse alphabetical (z < a for min-heap)
            if self.freq == other.freq:
                return self.word > other.word  # Reversed for min-heap
            return self.freq < other.freq

    heap = []
    for word, freq in count.items():
        heapq.heappush(heap, Element(word, freq))
        if len(heap) > k:
            heapq.heappop(heap)

    # Pop all and reverse
    result = []
    while heap:
        result.append(heapq.heappop(heap).word)

    return result[::-1]
```

---

## Template: Majority Element (> n/2)

**Problem**: Given an array `nums` of size `n`, return the majority element. The majority element is the element that appears more than `⌊n / 2⌋` times.

**Explanation**: While a hashmap can solve this in O(n) space, the Boyer-Moore Voting Algorithm achieves O(n) time and O(1) space. It works by maintaining a candidate and a counter. If the current number matches the candidate, we increment the counter; otherwise, we decrement it. If the counter reaches zero, we pick the current number as the new candidate. The majority element is guaranteed to survive this "cancellation" process.

```python
def majority_element(nums: list[int]) -> int:
    """
    Find element that appears more than n/2 times.
    Guaranteed to exist.

    Time: O(n)
    Space: O(1) with Boyer-Moore, O(n) with Counter
    """
    # Method 1: Counter (O(n) space)
    from collections import Counter
    count = Counter(nums)
    return max(count.keys(), key=count.get)


def majority_element_boyer_moore(nums: list[int]) -> int:
    """
    Boyer-Moore Voting Algorithm - O(1) space.

    Key insight: Majority element "survives" cancellation.
    """
    candidate = None
    count = 0

    for num in nums:
        if count == 0:
            candidate = num
            count = 1
        elif num == candidate:
            count += 1
        else:
            count -= 1

    return candidate
```

### Visual: Boyer-Moore

```
nums = [2, 2, 1, 1, 1, 2, 2]

Step 1: candidate=2, count=1
Step 2: candidate=2, count=2
Step 3: candidate=2, count=1 (1 cancels one 2)
Step 4: candidate=2, count=0 (1 cancels one 2)
Step 5: candidate=1, count=1 (new candidate)
Step 6: candidate=1, count=0 (2 cancels)
Step 7: candidate=2, count=1 (new candidate)

Result: 2 (verify by counting if not guaranteed)
```

---

## Template: Majority Element II (> n/3)

**Problem**: Given an integer array of size `n`, find all elements that appear more than `⌊n / 3⌋` times.

**Explanation**: This is an extension of Boyer-Moore. Since at most two elements can appear more than `n/3` times, we maintain two candidates and two counters. After one pass, we must perform a second pass to verify that the candidates actually meet the frequency requirement.

```python
def majority_element_ii(nums: list[int]) -> list[int]:
    """
    Find all elements appearing more than n/3 times.
    At most 2 such elements can exist.

    Time: O(n)
    Space: O(1)
    """
    if not nums:
        return []

    # Boyer-Moore for 2 candidates
    candidate1, candidate2 = None, None
    count1, count2 = 0, 0

    for num in nums:
        if candidate1 == num:
            count1 += 1
        elif candidate2 == num:
            count2 += 1
        elif count1 == 0:
            candidate1 = num
            count1 = 1
        elif count2 == 0:
            candidate2 = num
            count2 = 1
        else:
            count1 -= 1
            count2 -= 1

    # Verify candidates
    result = []
    threshold = len(nums) // 3

    for candidate in [candidate1, candidate2]:
        if candidate is not None and nums.count(candidate) > threshold:
            result.append(candidate)

    return result
```

---

## Template: First Unique Character

**Problem**: Given a string `s`, find the first non-repeating character in it and return its index. If it does not exist, return -1.

**Explanation**: We perform two passes. In the first pass, we build a frequency map of all characters in the string. In the second pass, we iterate through the string again and return the index of the first character whose frequency is 1.

```python
def first_uniq_char(s: str) -> int:
    """
    Find index of first non-repeating character.

    Time: O(n)
    Space: O(1) - at most 26 letters

    Example:
    "leetcode" → 0 (l is first unique)
    "loveleetcode" → 2 (v is first unique)
    """
    from collections import Counter

    count = Counter(s)

    for i, char in enumerate(s):
        if count[char] == 1:
            return i

    return -1
```

---

## Template: Find All Duplicates

**Problem**: Given an integer array `nums` of length `n` where all the integers of `nums` are in the range `[1, n]` and each integer appears once or twice, return an array of all the integers that appears twice.

**Explanation**: Since the numbers are within the range `[1, n]`, we can use the array itself as a hashmap to save space. We iterate through the array and for each number `x`, we treat `abs(x)-1` as an index and negate the value at that index. If we encounter a value that is already negative, it means we've seen `abs(x)` before, identifying it as a duplicate.

```python
def find_duplicates(nums: list[int]) -> list[int]:
    """
    Find all elements that appear exactly twice.
    Constraints: 1 <= nums[i] <= n where n = len(nums)

    Time: O(n)
    Space: O(1) - using array itself
    """
    result = []

    for num in nums:
        index = abs(num) - 1

        if nums[index] < 0:
            result.append(abs(num))  # Already seen
        else:
            nums[index] *= -1  # Mark as seen

    return result
```

### Visual Trace

```
nums = [4, 3, 2, 7, 8, 2, 3, 1]

num=4: nums[3] positive → negate → [4, 3, 2, -7, 8, 2, 3, 1]
num=3: nums[2] positive → negate → [4, 3, -2, -7, 8, 2, 3, 1]
num=2: nums[1] positive → negate → [4, -3, -2, -7, 8, 2, 3, 1]
num=7: nums[6] positive → negate → [4, -3, -2, -7, 8, 2, -3, 1]
num=8: nums[7] positive → negate → [4, -3, -2, -7, 8, 2, -3, -1]
num=2: nums[1] negative → DUPLICATE! add 2
num=3: nums[2] negative → DUPLICATE! add 3
num=1: nums[0] positive → negate

Result: [2, 3]
```

---

## Template: Single Number (XOR Trick)

**Problem**: Given a non-empty array of integers `nums`, every element appears twice except for one. Find that single one.

**Explanation**: The XOR operation has the property that `a ^ a = 0` and `a ^ 0 = a`. By XORing all elements in the array, all pairs of duplicates will cancel each other out, leaving only the single number that appears once. This provides an O(n) time and O(1) space solution without needing a hashmap.

```python
def single_number(nums: list[int]) -> int:
    """
    Every element appears twice except one. Find it.

    Time: O(n)
    Space: O(1) - no hashmap needed!

    Key insight: XOR of same numbers = 0, XOR with 0 = number itself
    a ^ a = 0
    a ^ 0 = a
    """
    result = 0

    for num in nums:
        result ^= num

    return result
```

---

## Template: Contains Duplicate

**Problem**: Given an integer array `nums`, return `true` if any value appears at least twice in the array, and return `false` if every element is distinct.

**Explanation**: We use a `set` to store elements as we see them. If an element is already in the set, we found a duplicate. Alternatively, comparing the length of the array to the length of its set version provides a concise one-line solution.

```python
def contains_duplicate(nums: list[int]) -> bool:
    """
    Check if any element appears at least twice.

    Time: O(n)
    Space: O(n)
    """
    return len(nums) != len(set(nums))

# Or with early exit
def contains_duplicate_early_exit(nums: list[int]) -> bool:
    """
    Early exit version - stops as soon as a duplicate is found.
    """
    seen = set()

    for num in nums:
        if num in seen:
            return True
        seen.add(num)

    return False
```

---

## Template: Contains Duplicate II (Within K Distance)

**Problem**: Given an integer array `nums` and an integer `k`, return `true` if there are two distinct indices `i` and `j` in the array such that `nums[i] == nums[j]` and `abs(i - j) <= k`.

**Explanation**: We use a hashmap to store the most recent index of each value. As we iterate, if we see a value that is already in the map, we check if the difference between the current index and the stored index is `≤ k`. If so, we return `true`. Otherwise, we update the map with the new index.

```python
def contains_nearby_duplicate(nums: list[int], k: int) -> bool:
    """
    Check if nums[i] == nums[j] and |i - j| <= k.

    Time: O(n)
    Space: O(min(n, k))
    """
    seen = {}  # value → most recent index

    for i, num in enumerate(nums):
        if num in seen and i - seen[num] <= k:
            return True
        seen[num] = i

    return False

# Sliding window approach (O(k) space)
def contains_nearby_duplicate_window(nums: list[int], k: int) -> bool:
    window = set()

    for i, num in enumerate(nums):
        if num in window:
            return True

        window.add(num)

        if len(window) > k:
            window.remove(nums[i - k])

    return False
```

---

## Template: Contains Duplicate III (Within K Distance and Value Diff)

**Problem**: Given an integer array `nums` and two integers `k` and `t`, return `true` if there are two distinct indices `i` and `j` such that `abs(nums[i] - nums[j]) <= t` and `abs(i - j) <= k`.

**Explanation**: We use a bucket sort-like approach to group numbers by their values. Each bucket has a width of `t + 1`. If two numbers fall into the same bucket, their difference is at most `t`. We also check adjacent buckets for potential matches. We maintain a sliding window of size `k` by removing old buckets as we move forward.

```python
def contains_nearby_almost_duplicate(nums: list[int], k: int, t: int) -> bool:
    """
    Check if nums[i] ≈ nums[j] (diff <= t) and |i - j| <= k.

    Time: O(n) with bucket sort
    Space: O(min(n, k))
    """
    if t < 0:
        return False

    buckets = {}
    bucket_size = t + 1  # Bucket width

    for i, num in enumerate(nums):
        bucket_id = num // bucket_size

        # Same bucket → diff <= t
        if bucket_id in buckets:
            return True

        # Adjacent buckets might also work
        if bucket_id - 1 in buckets and num - buckets[bucket_id - 1] <= t:
            return True
        if bucket_id + 1 in buckets and buckets[bucket_id + 1] - num <= t:
            return True

        buckets[bucket_id] = num

        # Maintain window size k
        if i >= k:
            old_bucket = nums[i - k] // bucket_size
            del buckets[old_bucket]

    return False
```

---

## Edge Cases

```python
# Empty array
[] → handle specially

# All same elements
[1, 1, 1, 1] → frequency = 4

# All unique elements
[1, 2, 3, 4] → each frequency = 1

# Negative numbers
[-1, -1, 2] → Counter handles correctly

# Zero frequency (doesn't exist)
Counter({1: 2}).get(3, 0)  # Returns 0

# Large k in top K
k > unique elements → return all unique
```

---

## Counter Cheat Sheet

```python
from collections import Counter

c = Counter([1, 1, 2, 2, 2, 3])

# Basic operations
c[1]                    # 2 (frequency of 1)
c[999]                  # 0 (missing key returns 0, not KeyError!)
c.most_common(2)        # [(2, 3), (1, 2)]
c.total()               # 6 (sum of counts, Python 3.10+)

# Arithmetic
c + Counter([1, 2])     # Counter({2: 4, 1: 3, 3: 1})
c - Counter([1, 2, 2])  # Counter({2: 1, 1: 1, 3: 1})
+c                      # Remove zero/negative counts

# Update
c.update([1, 1, 1])     # Add counts: {1: 5, 2: 3, 3: 1}
c.subtract([1, 1])      # Subtract counts: {1: 3, 2: 3, 3: 1}

# Convert
list(c.elements())      # [1, 1, 2, 2, 2, 3] (repeat each count times)
dict(c)                 # Convert to regular dict
```

---

## Practice Problems

| #   | Problem                      | Difficulty | Pattern                |
| --- | ---------------------------- | ---------- | ---------------------- |
| 1   | Top K Frequent Elements      | Medium     | Heap or bucket sort    |
| 2   | Top K Frequent Words         | Medium     | Heap with tie-breaking |
| 3   | Majority Element             | Easy       | Boyer-Moore or Counter |
| 4   | Majority Element II          | Medium     | Boyer-Moore extended   |
| 5   | First Unique Character       | Easy       | Counter + scan         |
| 6   | Single Number                | Easy       | XOR trick              |
| 7   | Contains Duplicate           | Easy       | Set                    |
| 8   | Contains Duplicate II        | Easy       | Sliding window set     |
| 9   | Sort Characters By Frequency | Medium     | Counter + sort         |
| 10  | Find All Duplicates          | Medium     | Index marking          |

---

## Key Takeaways

1. **Counter is your friend** - use it instead of manual dict
2. **Bucket sort gives O(n)** for top K when frequencies are bounded
3. **Boyer-Moore for O(1) space** majority element
4. **XOR trick for single number** - no hashmap needed
5. **Sliding window set** for "within distance k" problems
6. **Counter[missing] = 0** - no KeyError!

---

## Next: [04-anagram-grouping.md](./04-anagram-grouping.md)

Learn how to use hashmaps to group anagrams and solve character frequency problems.

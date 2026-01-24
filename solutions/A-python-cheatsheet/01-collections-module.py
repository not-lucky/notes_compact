from collections import Counter, defaultdict, deque, OrderedDict, namedtuple

# 1. Valid Anagram
def is_anagram(s: str, t: str) -> bool:
    return Counter(s) == Counter(t)

# 2. Top K Frequent Elements
def top_k_frequent(nums: list[int], k: int) -> list[int]:
    return [x for x, _ in Counter(nums).most_common(k)]

# 3. Group Anagrams
def group_anagrams(strs: list[str]) -> list[list[str]]:
    groups = defaultdict(list)
    for s in strs:
        key = "".join(sorted(s))
        groups[key].append(s)
    return list(groups.values())

# 4. Sliding Window Maximum
def max_sliding_window(nums: list[int], k: int) -> list[int]:
    dq = deque()  # Store indices
    result = []
    for i, num in enumerate(nums):
        while dq and nums[dq[-1]] < num:
            dq.pop()
        dq.append(i)
        if dq[0] <= i - k:
            dq.popleft()
        if i >= k - 1:
            result.append(nums[dq[0]])
    return result

# 5. LRU Cache
class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = OrderedDict()

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)

# 6. Number of Recent Calls
class RecentCounter:
    def __init__(self):
        self.requests = deque()

    def ping(self, t: int) -> int:
        self.requests.append(t)
        while self.requests[0] < t - 3000:
            self.requests.popleft()
        return len(self.requests)

if __name__ == "__main__":
    # Tests
    print("Valid Anagram:", is_anagram("anagram", "nagaram"))
    print("Top K Frequent:", top_k_frequent([1,1,1,2,2,3], 2))
    print("Group Anagrams:", group_anagrams(["eat","tea","tan","ate","nat","bat"]))
    print("Sliding Window Max:", max_sliding_window([1,3,-1,-3,5,3,6,7], 3))

    lru = LRUCache(2)
    lru.put(1, 1)
    lru.put(2, 2)
    print("LRU Get 1:", lru.get(1))
    lru.put(3, 3)
    print("LRU Get 2 (should be -1):", lru.get(2))

    rc = RecentCounter()
    print("Recent Calls (ping 1):", rc.ping(1))
    print("Recent Calls (ping 100):", rc.ping(100))
    print("Recent Calls (ping 3001):", rc.ping(3001))
    print("Recent Calls (ping 3002):", rc.ping(3002))

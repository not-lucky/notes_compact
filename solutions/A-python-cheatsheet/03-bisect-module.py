import bisect

# 1. Search Insert Position
def search_insert(nums: list[int], target: int) -> int:
    return bisect.bisect_left(nums, target)

# 2. Find First and Last Position
def search_range(nums: list[int], target: int) -> list[int]:
    left = bisect.bisect_left(nums, target)
    if left == len(nums) or nums[left] != target:
        return [-1, -1]
    right = bisect.bisect_right(nums, target) - 1
    return [left, right]

# 3. Time Based Key-Value Store
class TimeMap:
    def __init__(self):
        self.store = {}

    def set(self, key: str, value: str, timestamp: int) -> None:
        if key not in self.store:
            self.store[key] = ([], [])
        self.store[key][0].append(timestamp)
        self.store[key][1].append(value)

    def get(self, key: str, timestamp: int) -> str:
        if key not in self.store:
            return ""
        times, values = self.store[key]
        idx = bisect.bisect_right(times, timestamp) - 1
        return values[idx] if idx >= 0 else ""

# 4. Count of Smaller Numbers After Self (Simplified: count of elements < target in sorted list)
def count_smaller_than(nums: list[int], target: int) -> int:
    # Assuming nums is sorted for this module's context
    return bisect.bisect_left(nums, target)

# 5. Russian Doll Envelopes (LIS part)
def max_envelopes(envelopes: list[list[int]]) -> int:
    if not envelopes: return 0
    # Sort width asc, height desc
    envelopes.sort(key=lambda x: (x[0], -x[1]))
    heights = [e[1] for e in envelopes]

    # LIS using bisect
    tails = []
    for h in heights:
        idx = bisect.bisect_left(tails, h)
        if idx == len(tails):
            tails.append(h)
        else:
            tails[idx] = h
    return len(tails)

# 6. H-Index II
def h_index_ii(citations: list[int]) -> int:
    n = len(citations)
    # Binary search for the first index i where citations[i] >= n - i
    # This can be done using bisect_left by wrapping the access
    class CitationWrapper:
        def __len__(self): return n
        def __getitem__(self, i):
            return citations[i] >= n - i

    # Actually, standard binary search is easier here, but let's try to use bisect logic
    # We want to find the first True in [citations[i] >= n - i]
    # Since citations is sorted, this is monotonic
    left = 0
    right = n - 1
    res = 0
    while left <= right:
        mid = (left + right) // 2
        if citations[mid] >= n - mid:
            res = n - mid
            right = mid - 1
        else:
            left = mid + 1
    return res

if __name__ == "__main__":
    print("Search Insert (5):", search_insert([1,3,5,6], 5))
    print("Search Range (8):", search_range([5,7,7,8,8,10], 8))

    tm = TimeMap()
    tm.set("foo", "bar", 1)
    print("TimeMap Get (foo, 1):", tm.get("foo", 1))
    print("TimeMap Get (foo, 3):", tm.get("foo", 3))

    print("Russian Doll Envelopes:", max_envelopes([[5,4],[6,4],[6,7],[2,3]]))
    print("H-Index II:", h_index_ii([0,1,3,5,6]))
